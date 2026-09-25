import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import assert from 'node:assert/strict';

const here = path.dirname(fileURLToPath(import.meta.url));
const manifest = JSON.parse(fs.readFileSync(path.join(here, 'development-illustration-seed.json')));
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
const [existing, stages, items, bucket] = await Promise.all([read('illustration'), read('category_stage'), read('development_item'), request('/storage/v1/bucket/public-assets').then(r => r.json())]);
assert.equal(bucket.public, true);
const images = manifest.tables.illustration;
const mappings = manifest.tables.illustration_development_item;
const digest = bytes => createHash('sha256').update(bytes).digest('hex');
const files = images.map(row => {
  assert.equal(path.basename(row.asset_key), row.asset_key);
  assert.equal(row.storage_bucket, manifest.storageBucket);
  assert.ok(stages.some(s => s.id === row.category_stage_id && !s.is_deleted_flag));
  const clashes = existing.filter(r => r.id === row.id || r.code === row.code || r.asset_key === row.asset_key);
  assert.ok(clashes.every(r => r.id === row.id && r.code === row.code && r.asset_key === row.asset_key), `Conflicting existing image: ${row.code}`);
  const bytes = fs.readFileSync(path.join(here, '../participatory-growth-frame-studies', row.asset_key));
  assert.equal(bytes.subarray(1, 4).toString(), 'PNG');
  return { row, bytes, sha256: digest(bytes) };
});
for (const link of mappings) {
  const image = images.find(r => r.id === link.illustration_id);
  assert.ok(image);
  assert.ok(items.some(i => i.id === link.development_item_id && i.stage_id === image.category_stage_id && !i.is_deleted_flag));
}
console.log(`Validated development: ${files.length} images, ${mappings.length} item links.`);
if (!apply) {
  console.log('Dry run only. Use --apply to upload and register.');
} else {
  for (const { row, bytes, sha256 } of files) {
    const object = `${manifest.storageBucket}/${manifest.storageDirectory}/${row.asset_key}`;
    await request(`/storage/v1/object/${object}`, { method: 'POST', headers: { 'Content-Type': 'image/png', 'x-upsert': 'true', 'cache-control': '3600' }, body: bytes });
    const uploaded = Buffer.from(await (await request(`/storage/v1/object/${object}`)).arrayBuffer());
    assert.equal(digest(uploaded), sha256, `Uploaded bytes differ: ${row.asset_key}`);
    const publicResponse = await fetch(`${url}/storage/v1/object/public/${object}?sha=${sha256}`);
    assert.equal(publicResponse.status, 200);
    assert.equal(digest(Buffer.from(await publicResponse.arrayBuffer())), sha256);
    console.log(`Uploaded and verified ${row.asset_key}`);
  }
  // Re-runs safely complete partial runs; unrelated records and mappings are preserved.
  for (const [table, rows] of Object.entries(manifest.tables)) {
    const conflict = table === 'illustration' ? 'id' : 'illustration_id,development_item_id';
    await request(`/rest/v1/${table}?on_conflict=${conflict}`, { method: 'POST', headers: { 'Content-Type': 'application/json', Prefer: 'resolution=merge-duplicates' }, body: JSON.stringify(rows) });
    const actual = await read(table);
    for (const expected of rows) {
      const found = actual.find(r => table === 'illustration' ? r.id === expected.id : r.illustration_id === expected.illustration_id && r.development_item_id === expected.development_item_id);
      assert.ok(found);
      for (const [k, v] of Object.entries(expected)) assert.deepEqual(found[k], v, `${table}.${k}`);
    }
    console.log(`Registered and verified ${table}: ${rows.length}`);
  }
  const receipt = { environment: 'development', projectRef: expectedRef, verifiedAt: new Date().toISOString(), illustrations: files.map(f => ({ id: f.row.id, asset_key: f.row.asset_key, sha256: f.sha256 })), mappingCount: mappings.length };
  fs.writeFileSync(path.join(here, 'development-illustration-publish-receipt.json'), JSON.stringify(receipt, null, 2) + '\n');
}
