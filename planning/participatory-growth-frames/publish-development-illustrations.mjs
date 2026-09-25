import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import assert from 'node:assert/strict';

const here = path.dirname(fileURLToPath(import.meta.url));
const manifest = JSON.parse(fs.readFileSync(path.join(here, 'development-illustration-publish-receipt.json')));
const apply = process.argv.includes('--apply');
const expectedRef = 'dltohjfxawjonomvxfsd';
assert.equal(manifest.environment, 'development');
assert.equal(manifest.projectRef, expectedRef);
const url = `https://${expectedRef}.supabase.co`;
// Credentials stay in process memory and are never written to the manifest or logs.
const keys = JSON.parse(execFileSync('supabase', ['projects', 'api-keys', '--project-ref', expectedRef, '--output', 'json'], { stdio: ['ignore', 'pipe', 'pipe'] }));
const key = keys.find(k => k.name === 'service_role')?.api_key;
assert.ok(key, 'Development service-role key unavailable');
const headers = { apikey: key, Authorization: `Bearer ${key}` };
async function request(route, options = {}) {
  const response = await fetch(url + route, { ...options, headers: { ...headers, ...options.headers } });
  if (!response.ok) throw new Error(`${options.method || 'GET'} ${route}: HTTP ${response.status}`);
  return response;
}
const read = async table => (await request(`/rest/v1/${table}?select=*`)).json();
const [existing, bucket] = await Promise.all([read('illustration'), request('/storage/v1/bucket/public-assets').then(r => r.json())]);
assert.equal(bucket.public, true);
// SQL records are maintained exclusively in withu/sql/content-model-v2/006 and 008.
// This tool only reuploads the assets listed in the development receipt.
const images = manifest.illustrations;
const digest = bytes => createHash('sha256').update(bytes).digest('hex');
const files = images.map(row => {
  assert.equal(path.basename(row.asset_key), row.asset_key);

  const clashes = existing.filter(r => r.id === row.id || r.asset_key === row.asset_key);
  assert.ok(clashes.length === 1 && clashes.every(r => r.id === row.id && r.asset_key === row.asset_key), `Conflicting existing image: ${row.asset_key}`);
  const bytes = fs.readFileSync(path.join(here, '../participatory-growth-frame-studies', row.asset_key));
  assert.equal(bytes.subarray(1, 4).toString(), 'PNG');
  return { row, bytes, sha256: digest(bytes) };
});
console.log(`Validated development: ${files.length} existing image assets.`);
if (!apply) {
  console.log('Dry run only. Use --apply to upload images only.');
} else {
  for (const { row, bytes, sha256 } of files) {
    const object = `public-assets/growth-frames/${row.asset_key}`;
    await request(`/storage/v1/object/${object}`, { method: 'POST', headers: { 'Content-Type': 'image/png', 'x-upsert': 'true', 'cache-control': '3600' }, body: bytes });
    const uploaded = Buffer.from(await (await request(`/storage/v1/object/${object}`)).arrayBuffer());
    assert.equal(digest(uploaded), sha256, `Uploaded bytes differ: ${row.asset_key}`);
    const publicResponse = await fetch(`${url}/storage/v1/object/public/${object}?sha=${sha256}`);
    assert.equal(publicResponse.status, 200);
    assert.equal(digest(Buffer.from(await publicResponse.arrayBuffer())), sha256);
    console.log(`Uploaded and verified ${row.asset_key}`);
  }
  console.log('All image assets verified. Database rows are unchanged; use the withu SQL seeds for data changes.');
}
