"""Render the researched prop catalog as static HTML, including for file:// viewing."""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parent

def render():
    data = json.loads((ROOT / 'specialist-props.json').read_text())
    path = ROOT / 'index.html'
    page = path.read_text()
    esc = html.escape
    for group in data['groups']:
        cid = group['character']
        cards = []
        for i, item in enumerate(group['items'], 1):
            source = data['sources'][item['source']]
            photo = item['photo']
            cards.append(f'''<article class="toolcard" id="{esc(item['id'])}">
<a class="toolphoto" href="{esc(photo['path'], quote=True)}" target="_blank" rel="noopener" aria-label="{esc(item['name'])}の写真を拡大">
<img src="{esc(photo['path'], quote=True)}" alt="{esc(photo['alt'])}" width="480" height="320" loading="lazy" decoding="async">
<span>{esc(photo['kind'])} ↗</span></a>
<div class="toolmeta"><span>{i:02d}</span><small>{esc(item['context'])}</small></div>
<h5>{esc(item['name'])}</h5>
<p class="toolpreview">{esc(item['scene'])}</p>
<details class="tooldetails"><summary>用途・出典を見る</summary>
<p>{esc(item['sourceFact'])}</p>
<p><b>使う場面</b> {esc(item['scene'])}</p>
<p class="toolshape"><b>描くとき</b> {esc(item['design'])}</p>
<p><a href="{esc(source['url'], quote=True)}" target="_blank" rel="noopener noreferrer">用途の出典：{esc(source['title'])} ↗</a></p>
<p><a href="{esc(photo['sourceUrl'], quote=True)}" target="_blank" rel="noopener noreferrer">写真：{esc(photo['credit'])} ↗</a></p>
</details>
</article>''')
        block = f'''<!-- specialist-props:{cid}:start -->
<div class="specialisttools">
<div class="toolrailhead"><p>{esc(group['role'])}</p>
<div class="toolrailcontrols"><span class="toolposition" aria-live="polite">1 / 10</span>
<button type="button" data-tool-direction="-1" aria-controls="tools-{cid}" aria-label="{esc(group['name'])}の前の道具" disabled>←</button>
<button type="button" data-tool-direction="1" aria-controls="tools-{cid}" aria-label="{esc(group['name'])}の次の道具">→</button></div></div>
<div class="toolgrid" id="tools-{cid}" tabindex="0" role="region" aria-label="{esc(group['name'])}の道具10点。左右にスクロールできます">{''.join(cards)}</div>
</div>
<!-- specialist-props:{cid}:end -->'''
        pattern = rf'<!-- specialist-props:{cid}:start -->.*?<!-- specialist-props:{cid}:end -->'
        if re.search(pattern, page, re.S):
            page = re.sub(pattern, lambda _: block, page, flags=re.S)
        else:
            anchor = f'<article class="propgroup" id="props-{cid}"><h3>{group["name"]}</h3>'
            assert page.count(anchor) == 1, cid
            page = page.replace(anchor, anchor + '\n' + block + '\n<h4>基本小物・背景の見本</h4>')
    path.write_text(page)

if __name__ == '__main__':
    render()
