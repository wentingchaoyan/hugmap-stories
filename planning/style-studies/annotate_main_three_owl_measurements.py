from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).parent
SOURCE = ROOT / "outputs/groups/main-three-owl-step1a-scale-check.png"
OUTPUT = ROOT / "outputs/groups/main-three-owl-step1a-pixel-guide.png"

ORANGE = (237, 106, 55, 255)
WINE = (155, 49, 85, 255)
BLUE = (54, 137, 163, 255)
PAPER = (255, 250, 242, 235)
GUIDE = (145, 184, 196, 165)


def font(size: int):
    candidates = [
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


LABEL = font(18)
SMALL = font(15)


def text_box(draw, xy, text, color, anchor="mm", small=False):
    selected = SMALL if small else LABEL
    box = draw.textbbox(xy, text, font=selected, anchor=anchor)
    draw.rounded_rectangle(
        (box[0] - 5, box[1] - 3, box[2] + 5, box[3] + 3),
        radius=5,
        fill=PAPER,
    )
    draw.text(xy, text, font=selected, fill=color, anchor=anchor)


def vertical(draw, x, y1, y2, text, color, side="right"):
    draw.line((x, y1, x, y2), fill=color, width=2)
    draw.line((x - 10, y1, x + 10, y1), fill=color, width=2)
    draw.line((x - 10, y2, x + 10, y2), fill=color, width=2)
    anchor = "lm" if side == "right" else "rm"
    dx = 11 if side == "right" else -11
    text_box(draw, (x + dx, (y1 + y2) // 2), text, color, anchor, small=True)


def horizontal(draw, x1, x2, y, text, color):
    draw.line((x1, y, x2, y), fill=color, width=2)
    draw.line((x1, y - 10, x1, y + 10), fill=color, width=2)
    draw.line((x2, y - 10, x2, y + 10), fill=color, width=2)
    text_box(draw, ((x1 + x2) // 2, y - 8), text, color, "ms", small=True)


image = Image.open(SOURCE).convert("RGBA")
overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

draw.line((60, 846, 1470, 846), fill=GUIDE, width=1)

# Visible line-envelope measurements on this exact 1536 x 1024 image.
vertical(draw, 112, 369, 848, "全高 479px", ORANGE)
horizontal(draw, 141, 323, 418, "頭幅 182px", WINE)
vertical(draw, 341, 430, 641, "頭高 211px", WINE)

vertical(draw, 455, 355, 847, "全高 492px", ORANGE)
horizontal(draw, 498, 689, 442, "頭幅 191px", WINE)
vertical(draw, 710, 454, 621, "頭高 167px", WINE)

vertical(draw, 795, 372, 850, "全高 478px", ORANGE)
horizontal(draw, 859, 1014, 402, "頭幅 155px", WINE)
vertical(draw, 1028, 414, 615, "頭高 201px", WINE)

# OWL has an integrated head/body mass, so use outer-envelope and facial-disk measures.
vertical(draw, 1168, 446, 845, "全高 399px", ORANGE)
horizontal(draw, 1193, 1411, 475, "身体外形幅 218px", BLUE)
horizontal(draw, 1219, 1392, 703, "顔盤幅 173px", BLUE)
vertical(draw, 1426, 519, 704, "顔盤高 185px", BLUE, side="left")
text_box(draw, (1305, 876), "翼長 146px／頭胴一体型", BLUE, small=True)

draw.rounded_rectangle(
    (1025, 902, 1470, 990),
    radius=10,
    fill=PAPER,
    outline=(212, 206, 198, 255),
    width=1,
)
draw.line((1045, 926, 1085, 926), fill=ORANGE, width=2)
draw.text((1095, 916), "全高（耳・冠羽込み）", font=SMALL, fill=ORANGE)
draw.line((1045, 952, 1085, 952), fill=WINE, width=2)
draw.text((1095, 942), "頭部（耳・冠羽を除く）", font=SMALL, fill=WINE)
draw.line((1045, 978, 1085, 978), fill=BLUE, width=2)
draw.text((1095, 968), "フクロウ一体型身体・顔盤", font=SMALL, fill=BLUE)

Image.alpha_composite(image, overlay).convert("RGB").save(OUTPUT, quality=96)
print(OUTPUT)
