from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).parent
SOURCE = ROOT / "outputs/groups/12-main-three-after-head-neutral-turnaround-v1.png"
OUTPUT = ROOT / "outputs/groups/12-main-three-after-head-neutral-turnaround-measurement-guide-v1.png"

# Pixel measurements use the visible outer contour. Head measurements exclude
# crest/ears; total height includes them and ends at the lowest foot contour.
SPECS = [
    {"name": "MIMO", "body": (269, 19, 430, 312), "head": (307, 52, 405, 180), "width_y": 129},
    {"name": "GEN", "body": (267, 347, 439, 660), "head": (288, 418, 430, 528), "width_y": 482},
    {"name": "LUKE", "body": (281, 703, 408, 983), "head": (301, 738, 393, 837), "width_y": 788},
]

WINE = (139, 41, 75, 255)
ORANGE = (239, 106, 58, 255)
PAPER = (255, 253, 251, 235)
GUIDE = (73, 126, 145, 92)


def font(size: int):
    candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


LABEL = font(17)
SMALL = font(15)


def label(draw, xy, text, color, anchor="mm"):
    box = draw.textbbox(xy, text, font=SMALL, anchor=anchor, stroke_width=0)
    pad = 4
    bg = (box[0] - pad, box[1] - 2, box[2] + pad, box[3] + 2)
    draw.rounded_rectangle(bg, radius=5, fill=PAPER)
    draw.text(xy, text, font=SMALL, fill=color, anchor=anchor)


def arrowhead(draw, point, direction, color):
    x, y = point
    s = 6
    if direction == "up":
        pts = [(x, y), (x - s, y + s * 2), (x + s, y + s * 2)]
    elif direction == "down":
        pts = [(x, y), (x - s, y - s * 2), (x + s, y - s * 2)]
    elif direction == "left":
        pts = [(x, y), (x + s * 2, y - s), (x + s * 2, y + s)]
    else:
        pts = [(x, y), (x - s * 2, y - s), (x - s * 2, y + s)]
    draw.polygon(pts, fill=color)


def vertical_dimension(draw, x, y1, y2, target_x, text, color, side="left"):
    draw.line((x, y1, x, y2), fill=color, width=2)
    draw.line((x, y1, target_x, y1), fill=color, width=1)
    draw.line((x, y2, target_x, y2), fill=color, width=1)
    arrowhead(draw, (x, y1), "up", color)
    arrowhead(draw, (x, y2), "down", color)
    dx = -8 if side == "left" else 8
    anchor = "rm" if side == "left" else "lm"
    label(draw, (x + dx, (y1 + y2) // 2), text, color, anchor)


def horizontal_dimension(draw, x1, x2, y, target_y, text, color):
    draw.line((x1, y, x2, y), fill=color, width=2)
    draw.line((x1, y, x1, target_y), fill=color, width=1)
    draw.line((x2, y, x2, target_y), fill=color, width=1)
    arrowhead(draw, (x1, y), "left", color)
    arrowhead(draw, (x2, y), "right", color)
    label(draw, ((x1 + x2) // 2, y - 10), text, color, "ms")


def dashed_line(draw, xy, fill, width=1, dash=9, gap=7):
    x1, y1, x2, y2 = xy
    if y1 == y2:
        x = x1
        while x < x2:
            draw.line((x, y1, min(x + dash, x2), y2), fill=fill, width=width)
            x += dash + gap
    else:
        y = y1
        while y < y2:
            draw.line((x1, y, x2, min(y + dash, y2)), fill=fill, width=width)
            y += dash + gap


image = Image.open(SOURCE).convert("RGBA")
overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

for spec in SPECS:
    bx1, by1, bx2, by2 = spec["body"]
    hx1, hy1, hx2, hy2 = spec["head"]
    total_h = by2 - by1
    head_w = hx2 - hx1
    head_h = hy2 - hy1

    # Construction guides: consistent centers for front/side/back and exact
    # front-view head-top, chin, and ground levels.
    row_top = max(0, by1 - 6)
    row_bottom = min(image.height - 1, by2 + 6)
    for center_x in (354, 766, 1161):
        dashed_line(draw, (center_x, row_top, center_x, row_bottom), GUIDE)
    for guide_y in (hy1, hy2, by2):
        dashed_line(draw, (220, guide_y, 1290, guide_y), GUIDE)

    vertical_dimension(draw, bx1 - 23, by1, by2, bx1 - 3, f"HEIGHT {total_h} px", ORANGE)
    # Width is measured on the widest head-contour scanline, while the label
    # is lifted above it to avoid covering the face.
    horizontal_dimension(draw, hx1, hx2, spec["width_y"], spec["width_y"], f"HEAD W {head_w} px", WINE)
    vertical_dimension(draw, hx2 + 19, hy1, hy2, hx2 + 3, f"HEAD H {head_h} px", WINE, "right")

draw.rounded_rectangle((1185, 27, 1508, 118), radius=10, fill=(255, 253, 251, 225), outline=(221, 213, 208, 255), width=1)
draw.text((1201, 42), "ORANGE: total height (incl. ears/crest)", font=SMALL, fill=ORANGE)
draw.text((1201, 67), "WINE: head contour (excl. ears/crest)", font=SMALL, fill=WINE)
draw.text((1201, 92), "BLUE: center / head / ground guides", font=SMALL, fill=(73, 126, 145, 220))

result = Image.alpha_composite(image, overlay).convert("RGB")
result.save(OUTPUT, quality=95)
print(OUTPUT)
