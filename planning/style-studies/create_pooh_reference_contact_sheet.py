from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
ASSET_DIR = ROOT / "outputs/references/pooh"
OUTPUT = ASSET_DIR / "08-pooh-direct-image-reference-sheet-v1.png"

PAPER = (247, 244, 239)
CARD = (255, 253, 250)
INK = (49, 43, 40)
MUTED = (112, 102, 97)
LINE = (218, 211, 205)
ACCENT = (139, 41, 75)


def font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size, index=1 if bold else 0)
            except OSError:
                continue
    return ImageFont.load_default()


TITLE = font(34, True)
SUBTITLE = font(17)
LABEL = font(19, True)
BODY = font(15)
SMALL = font(12)


def contain(image, size, background=CARD):
    fitted = ImageOps.contain(image.convert("RGB"), size, Image.Resampling.LANCZOS)
    result = Image.new("RGB", size, background)
    x = (size[0] - fitted.width) // 2
    y = (size[1] - fitted.height) // 2
    result.paste(fitted, (x, y))
    return result


def wrapped(draw, text, x, y, width, font_obj, fill, line_height):
    line = ""
    lines = []
    for char in text:
        candidate = line + char
        if draw.textlength(candidate, font=font_obj) > width and line:
            lines.append(line)
            line = char
        else:
            line = candidate
    if line:
        lines.append(line)
    for item in lines:
        draw.text((x, y), item, font=font_obj, fill=fill)
        y += line_height
    return y


canvas = Image.new("RGB", (1800, 1480), PAPER)
draw = ImageDraw.Draw(canvas)

draw.text((70, 52), "POOH｜感情・ポーズの直接画像REFERENCE", font=TITLE, fill=INK)
draw.text(
    (70, 105),
    "原作挿絵を、形の模倣ではなく『身体で感情を伝える仕組み』の観察用に並べる。",
    font=SUBTITLE,
    fill=MUTED,
)

# User-provided layout reference: shown small to study coverage and comparison density.
draw.rounded_rectangle((70, 150, 1730, 535), radius=18, fill=CARD, outline=LINE, width=1)
layout = Image.open(ASSET_DIR / "00-user-layout-reference.png")
layout_thumb = contain(layout, (650, 330))
canvas.paste(layout_thumb, (95, 177))
draw.text((790, 185), "添付例から参考にする構成", font=LABEL, fill=ACCENT)
notes = [
    "・単独ポーズと複数人ポーズを同じ一枚で比較する",
    "・歩く／抱える／見る／渡すなど、動詞の種類を増やす",
    "・小道具、相手、環境との接触で感情を説明する",
    "・正面立ちだけでなく、横向き・座り・前傾を混ぜる",
    "・HugMapでは固有の輪郭・服・顔・構図をコピーしない",
]
y = 232
for note in notes:
    y = wrapped(draw, note, 790, y, 860, BODY, INK, 31) + 8

items = [
    ("01-look-up-bees.jpg", "気づく｜視線が先に上へ動く", "Mimo: 目→くちばし→頭の傾き"),
    ("02-walking-humming.jpg", "歩く｜足運びが内面のリズムになる", "Gen: 表情より歩幅と前傾"),
    ("03-stuck-at-door.jpg", "困る｜環境との接触が状況を語る", "顔を大げさに歪めない"),
    ("04-tracking-with-piglet.jpg", "一緒に見る｜視線と進行方向を共有", "相手との距離で関係を表す"),
    ("05-carrying-gift.jpg", "運ぶ・渡す｜小道具が目的を作る", "Luke: 道具は一場面一種類"),
    ("06-practicing-jumps.jpg", "考える→試す｜連続ポーズで差を作る", "指差しではなく全身の変化"),
    ("07-walking-together.jpg", "並んで進む｜歩幅と接地線を揃える", "先生が先導しすぎない"),
]

card_w, card_h = 398, 390
gap_x, gap_y = 28, 28
start_x, start_y = 70, 575
for index, (filename, title, insight) in enumerate(items):
    row = index // 4
    col = index % 4
    x1 = start_x + col * (card_w + gap_x)
    y1 = start_y + row * (card_h + gap_y)
    draw.rounded_rectangle((x1, y1, x1 + card_w, y1 + card_h), radius=16, fill=CARD, outline=LINE, width=1)
    image = Image.open(ASSET_DIR / filename)
    image_box = contain(image, (350, 250))
    canvas.paste(image_box, (x1 + 24, y1 + 20))
    draw.text((x1 + 24, y1 + 287), title, font=BODY, fill=INK)
    wrapped(draw, insight, x1 + 24, y1 + 322, 350, SMALL, MUTED, 22)

# Source / usage note in the eighth slot.
x1 = start_x + 3 * (card_w + gap_x)
y1 = start_y + 1 * (card_h + gap_y)
draw.rounded_rectangle((x1, y1, x1 + card_w, y1 + card_h), radius=16, fill=(239, 233, 229), outline=LINE, width=1)
draw.text((x1 + 28, y1 + 34), "SOURCE / USE", font=LABEL, fill=ACCENT)
y = wrapped(
    draw,
    "画像: E. H. Shepard 挿絵／Project Gutenberg版 Winnie-the-Pooh (1926)。このシートは内部研究用。地域により権利状況が異なるため、完成物へ画像を流用しない。",
    x1 + 28,
    y1 + 82,
    338,
    BODY,
    INK,
    29,
)
wrapped(
    draw,
    "観察対象: 重心、視線、頭の角度、腕全体、小道具、相手との距離。",
    x1 + 28,
    y + 28,
    338,
    BODY,
    MUTED,
    29,
)

draw.text(
    (70, 1434),
    "Source: https://www.gutenberg.org/cache/epub/67098/pg67098-images.html",
    font=SMALL,
    fill=MUTED,
)

canvas.save(OUTPUT, quality=95)
print(OUTPUT)
