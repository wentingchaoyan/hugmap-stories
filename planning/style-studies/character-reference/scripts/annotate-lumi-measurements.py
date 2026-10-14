"""Annotate existing artwork without regenerating or deforming the character.

Landmarks are manually read from the source raster, to approximately ±3 px.
Lengths are differences of coordinates, including visible stroke boundaries.
"""
from pathlib import Path
import base64
import json

BASE = Path(__file__).resolve().parents[1]
ASSETS = BASE / 'assets'
measurements = {
    'method': 'Manual raster landmarks, approximately ±3 px; not physical dimensions. H=1000 normalizes each adult to the same overall height.',
    'approved_front': {'file': 'lumi-front-color.png', 'height': 967, 'head_width': 466, 'head_height': 390, 'body_height': 488, 'wing_height': 357, 'exposed_legs_feet': 125, 'eye_center_distance': 187, 'beak_width': 46, 'beak_height': 78},
    'current_turnaround_front': {'file': 'lumi-turnaround-white.png', 'height': 636, 'head_width': 313, 'head_height': 260, 'body_height': 306, 'wing_height': 242, 'exposed_legs_feet': 97, 'eye_center_distance': 132, 'beak_width': 34, 'beak_height': 52},
    'current_turnaround_views': {'front_height': 636, 'side_height': 638, 'back_height': 635},
    'lower_color_parent': {'file': 'lumi-parent-child-color.png', 'height': 869, 'head_width': 424, 'head_height': 355},
    'lower_color_child': {'file': 'lumi-parent-child-color.png', 'height': 691, 'head_width': 371, 'head_height': 298},
    'definitions': {'height': 'Ear tuft tip to lowest toe; not the horizontal floor line.', 'head_height': 'Ear tuft tip to lower head contour, partly occluded by bow.', 'head_width': 'Maximum head silhouette width, excluding wings.', 'body_height': 'Shoulder/wing-root level to bottom of belly, excluding legs.', 'wing_height': 'Wing root to lowest feather tip.', 'exposed_legs_feet': 'Bottom of belly to lowest toe; includes feet.', 'eye_center_distance': 'Horizontal distance between dark pupil centers.'},
    'status': 'Corrected to match lower_color_parent proportions. Target head width 488 and head height 409 at H=1000; measured front 492 and 409. Raster generation retains small deviations.'
}
def norm(key, field):
    d = measurements[key]
    return round(1000*d[field]/d['height'])

parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="2500" height="1560" viewBox="0 0 2500 1560">',
    '<title>LUMI 三面図・寸法比較</title><desc>現在の三面図の実測値と、承認済み正面図および下段の親子カラー図の比率を比較。全高1000の相対単位。</desc>',
    '<defs><marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10Z" fill="#7D2741"/></marker></defs>',
    '<rect width="2500" height="1560" fill="white"/>',
    '<style>text{font-family:"Hiragino Sans","Noto Sans JP",sans-serif;fill:#291712}.dim{stroke:#7D2741;stroke-width:2;fill:none;marker-start:url(#arrow);marker-end:url(#arrow)}.ext{stroke:#7D2741;stroke-width:1;stroke-dasharray:5 5}.label{font-size:23px;fill:#7D2741;paint-order:stroke;stroke:white;stroke-width:7px;stroke-linejoin:round}.small{font-size:22px}.cell{font-size:25px}</style>']
def text(x,y,s,cls='',size=None):
    parts.append(f'<text x="{x}" y="{y}" class="{cls}"'+(f' font-size="{size}"' if size else '')+f'>{s}</text>')
text(75,65,'LUMI｜三面図と寸法の確認',size=40)
text(75,110,'単位：正面の全高 H = 1000（相対寸法・cmではありません）／下段カラー版の親に合わせて比率を修正・再計測。',size=25)
data=base64.b64encode((ASSETS/'lumi-turnaround-white.png').read_bytes()).decode()
parts.append(f'<image x="160" y="180" width="2172" height="724" href="data:image/png;base64,{data}"/>')
text(550,163,'正面',size=28); text(1130,163,'側面',size=28); text(1780,163,'背面',size=28)
def vertical(x,y1,y2,edge,label):
    parts.append(f'<path class="ext" d="M{x} {y1}H{edge} M{x} {y2}H{edge}"/><path class="dim" d="M{x} {y1}V{y2}"/>')
    text(x-16,(y1+y2)/2,label,'label')
def horizontal(x1,x2,y,edge,label):
    parts.append(f'<path class="ext" d="M{x1} {y}V{edge} M{x2} {y}V{edge}"/><path class="dim" d="M{x1} {y}H{x2}"/>')
    text((x1+x2)/2-55,y-14,label,'label')
vertical(300,219,855,535,'全高 1000')
vertical(490,219,479,563,'頭高 409')
horizontal(558,871,195,258,'頭幅 492')
vertical(940,453,759,825,'胴高 481')
vertical(885,454,696,915,'翼高 381')
vertical(850,758,855,780,'脚＋足 153')
horizontal(650,782,520,365,'目の間隔 208')
vertical(1450,216,854,1220,'全高 1003')
vertical(2225,219,854,1900,'全高 998')
text(80,943,'寸法の定義：全高は耳羽の先〜足指の最下端。胴高は肩〜腹の底。翼・頭・胴の範囲は重なるため、足し合わせません。','small')
text(80,982,'手動計測の概算（元画像で約 ±3 px）。基準線と足指の最下端は一致していません。側面・背面の全高も正面と同じ縮尺で表示。','small')

text(80,1040,'正面の比率比較｜同じ全高1000に揃えた場合',size=30)
xs=[90,670,1100,1510,1910]
for x,t in zip(xs,['パーツ','承認済み正面','現在の三面図','下段カラー・親','下段カラー・子']): text(x,1090,t,'cell')
rows=[('頭幅','head_width'),('頭高（耳羽を含む）','head_height'),('胴高／翼高','body_height'),('脚＋足／目の中心間隔','exposed_legs_feet'),('くちばし 幅 × 高さ','beak_width')]
for i,(label,field) in enumerate(rows):
    y=1140+i*53
    parts.append(f'<path d="M80 {y+14}H2400" stroke="#DCD5D2"/>')
    text(xs[0],y,label,'cell')
    for col,key in enumerate(['approved_front','current_turnaround_front','lower_color_parent','lower_color_child'],1):
        d=measurements[key]
        if field not in d: v='—'
        elif field=='body_height': v=f'{norm(key,field)} / {norm(key,"wing_height")}'
        elif field=='exposed_legs_feet': v=f'{norm(key,field)} / {norm(key,"eye_center_distance")}'
        elif field=='beak_width': v=f'{norm(key,field)} × {norm(key,"beak_height")}'
        else: v=str(norm(key,field))
        text(xs[col],y,v,'cell')
text(80,1450,'下段の親子：親の全高を1000とすると、子は約795。上表の子の値は、子自身の全高を1000に換算した「形の比率」です。','small')
text(80,1493,'今回の基準は下段カラー版の親（頭幅488・頭高409）。修正後の正面は492・409で、頭幅の差は約0.8％。','small')
parts.append('</svg>')
(ASSETS/'lumi-turnaround-measured.svg').write_text('\n'.join(parts))
(ASSETS/'lumi-measurements.json').write_text(json.dumps(measurements,ensure_ascii=False,indent=2)+'\n')
print('Saved measured SVG and measurement JSON.')
