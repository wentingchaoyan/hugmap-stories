import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
export function applyLocalProposals(html) {
  const proposals = JSON.parse(fs.readFileSync(path.join(here, 'local-illustration-proposals.json'), 'utf8'));
  const tag = '<script type="application/json" id="local-illustration-proposals">' + JSON.stringify(proposals).replace(/</g, '\\u003c') + '</script>';
  html = html.replace(/<script type="application\/json" id="local-illustration-proposals">[\s\S]*?<\/script>/, '');
  const start = '<script>\nconst snapshots=';
  if (!html.includes(start)) throw new Error('Inventory snapshot script not found');
  html = html.replace(start, tag + start);
  const oldRows = 'const rows=t=>snapshots[env].tables[t].rows.filter(x=>!x.is_deleted_flag&&(x.is_active??true));';
  const previousRows = `const rows=t=>{const p=JSON.parse(document.querySelector('#local-illustration-proposals').textContent);const base=snapshots[env].tables[t].rows;const extra=env===p.environment?(p.tables[t]||[]):[];return [...base,...extra.filter(x=>!base.some(b=>b.id===x.id||t==='illustration'&&b.asset_key===x.asset_key))].filter(x=>!x.is_deleted_flag&&(x.is_active??true));};`;
  const newRows = previousRows.replace("env===p.environment?", "env===p.environment&&p.status!=='registered-in-development'?");
  html = html.replace(previousRows, newRows);
  if (!html.includes(oldRows) && !html.includes(newRows)) throw new Error('Inventory rows adapter not found');
  html = html.replace(oldRows, newRows);
  html = html.replace("esc(i.title_ja)+'</b>", "esc(i.title_ja)+(i.local_proposal?'〈制作案〉':'')+'</b>");
  html = html.replace("i.itemIds.size+' items linked</small>", "i.itemIds.size+(i.local_proposal?' items 提案紐づき':' items linked')+'</small><small>'+esc(i.proposal_note||'')+'</small>");
  html = html.replace("(mids.has(i.id)?'紐づき済':'未紐づき')", "(mids.has(i.id)?(s.images.some(x=>x.local_proposal&&x.itemIds.has(i.id))?'提案紐づき':'紐づき済'):'未紐づき')");
  html = html.replace('src="../participatory-growth-frame-studies/', 'alt="\'+esc(i.alt_text_ja||i.title_ja)+\'" src="../participatory-growth-frame-studies/');
  // Avoid repeating the alt attribute on successive applications.
  html = html.replace(/(alt="'\+esc\(i.alt_text_ja\|\|i.title_ja\)\+'" )\1/g, '$1');
  return html;
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const output = path.join(here, 'stage-illustration-inventory-review.html');
  fs.writeFileSync(output, applyLocalProposals(fs.readFileSync(output, 'utf8')));
  console.log('Applied local proposals without changing database snapshots.');
}
