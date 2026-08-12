from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "outputs/groups/45-main-three-small-mascot-with-u-monochrome-v5-gen-lower-hem-top-only.png"
OUTPUT = ROOT / "outputs/groups/47-main-three-small-mascot-pixel-lock-v4-gen-lower-hem.png"

CANVAS = (1536, 1024)
PAPER = (250, 248, 244)
INK = (49, 43, 40)
MUTED = (112, 102, 97)
GUIDE = (107, 145, 156)
ACCENT = (146, 52, 79)
LINE = (219, 212, 207)

SPECS = [
    {
        "name": "MIMO",
        "crop": (140, 45, 510, 670),
        "center": 300,
        "height": 224,
        "head": "74 x 96 px",
        "limb_label": "WING 48 px",
        "clothes_label": "SHORT TOP 48 px",
        "limb": 48,
        "clothes": 48,
        "logo": 14,
    },
    {
        "name": "GEN",
        "crop": (540, 35, 970, 680),
        "center": 768,
        "height": 240,
        "head": "108 x 84 px",
        "limb_label": "ARM 64 px MIN",
        "clothes_label": "SHORT TOP 60 px",
        "limb": 64,
        "clothes": 60,
        "logo": 14,
    },
    {
        "name": "LUKE",
        "crop": (950, 95, 1510, 690),
        "center": 1236,
        "height": 216,
        "head": "84 x 80 px",
        "limb_label": "ARM 56 px MIN",
        "clothes_label": "VEST 72 px VISIBLE",
        "limb": 56,
        "clothes": 72,
        "logo": 14,
    },
]


def font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size, index=1 if bold and path.suffix == ".ttc" else 0)
            except OSError:
                continue
    return ImageFont.load_default()


TITLE = font(34, True)
SUBTITLE = font(17)
NAME = font(23, True)
VALUE = font(18, True)
SMALL = font(14)
TINY = font(12)


def tight_crop(image):
    gray = image.convert("L")
    mask = gray.point(lambda value: 255 if value < 232 else 0)
    bbox = mask.getbbox()
    if bbox is None:
        raise RuntimeError("No drawing detected in crop")
    return image.crop(bbox)


def label(draw, xy, text, color=INK, font_obj=SMALL, anchor="mm", fill=PAPER):
    box = draw.textbbox(xy, text, font=font_obj, anchor=anchor)
    padded = (box[0] - 5, box[1] - 3, box[2] + 5, box[3] + 3)
    draw.rounded_rectangle(padded, radius=5, fill=fill)
    draw.text(xy, text, fill=color, font=font_obj, anchor=anchor)


def vertical_dimension(draw, x, y1, y2, text, color):
    draw.line((x, y1, x, y2), fill=color, width=2)
    draw.line((x - 8, y1, x + 8, y1), fill=color, width=2)
    draw.line((x - 8, y2, x + 8, y2), fill=color, width=2)
    draw.polygon([(x, y1), (x - 4, y1 + 9), (x + 4, y1 + 9)], fill=color)
    draw.polygon([(x, y2), (x - 4, y2 - 9), (x + 4, y2 - 9)], fill=color)
    label(draw, (x, (y1 + y2) // 2), text, color, TINY)


def horizontal_dimension(draw, x1, x2, y, text, color):
    draw.line((x1, y, x2, y), fill=color, width=2)
    draw.line((x1, y - 7, x1, y + 7), fill=color, width=2)
    draw.line((x2, y - 7, x2, y + 7), fill=color, width=2)
    draw.polygon([(x1, y), (x1 + 9, y - 4), (x1 + 9, y + 4)], fill=color)
    draw.polygon([(x2, y), (x2 - 9, y - 4), (x2 - 9, y + 4)], fill=color)
    label(draw, ((x1 + x2) // 2, y), text, color, TINY)


source = Image.open(SOURCE).convert("RGB")
canvas = Image.new("RGB", CANVAS, PAPER)
draw = ImageDraw.Draw(canvas)

draw.text((64, 52), "SMALL MASCOT — 1x PIXEL LOCK", fill=INK, font=TITLE)
draw.text(
    (64, 101),
    "Neutral front models are copied from the approved hand-drawn study. Pixel values below are normative for every pose.",
    fill=MUTED,
    font=SUBTITLE,
)
draw.line((64, 136, 1472, 136), fill=LINE, width=1)

ground_y = 520
panel_top = 166
for index, spec in enumerate(SPECS):
    panel_x1 = 64 + index * 469
    panel_x2 = panel_x1 + 438
    draw.rounded_rectangle((panel_x1, panel_top, panel_x2, 888), radius=18, fill=(255, 253, 250), outline=LINE, width=1)

    character = tight_crop(source.crop(spec["crop"]))
    scale = spec["height"] / character.height
    resized = character.resize((round(character.width * scale), spec["height"]), Image.Resampling.LANCZOS)
    paste_x = spec["center"] - resized.width // 2
    paste_y = ground_y - spec["height"]
    canvas.paste(resized, (paste_x, paste_y))

    draw.line((panel_x1 + 24, ground_y, panel_x2 - 24, ground_y), fill=GUIDE, width=1)
    draw.line((spec["center"], paste_y - 8, spec["center"], ground_y + 8), fill=GUIDE, width=1)
    vertical_dimension(draw, panel_x1 + 36, paste_y, ground_y, f'TOTAL {spec["height"]} px', ACCENT)

    name_y = 568
    draw.text((spec["center"], name_y), spec["name"], fill=INK, font=NAME, anchor="mm")
    draw.text((spec["center"], name_y + 38), f'HEAD {spec["head"]}', fill=ACCENT, font=VALUE, anchor="mm")

    bar_x1 = panel_x1 + 64
    bar_x2 = panel_x2 - 64
    arm_y = 672
    clothes_y = 758
    draw.text((bar_x1, arm_y - 28), spec["limb_label"], fill=INK, font=SMALL)
    horizontal_dimension(draw, bar_x1, bar_x1 + spec["limb"], arm_y, f'{spec["limb"]} px', GUIDE)
    draw.text((bar_x1, clothes_y - 28), spec["clothes_label"], fill=INK, font=SMALL)
    horizontal_dimension(draw, bar_x1, bar_x1 + spec["clothes"], clothes_y, f'{spec["clothes"]} px', GUIDE)
    draw.text((bar_x1 + 150, clothes_y - 28), "CHEST U", fill=INK, font=SMALL)
    horizontal_dimension(draw, bar_x1 + 150, bar_x1 + 150 + spec["logo"], clothes_y, f'{spec["logo"]} px', GUIDE)

    if spec["name"] == "GEN":
        note = "Lowered short top + no pants\nShoulder-to-tip stays 64 px"
    elif spec["name"] == "LUKE":
        note = "Vest front must remain visible\nArm never shorter than 56 px"
    else:
        note = "Short top + exposed feather body\nSmall chest U remains visible"
    draw.multiline_text((bar_x1, 810), note, fill=MUTED, font=TINY, spacing=5)

draw.rounded_rectangle((64, 918, 1472, 976), radius=12, fill=(241, 236, 232), outline=LINE, width=1)
draw.text(
    (82, 947),
    "POSE RULE  |  preserve TOTAL / HEAD / LIMB / CLOTHES px; rotate and bend masses without scaling them. U emblem stays fully visible.",
    fill=INK,
    font=SMALL,
    anchor="lm",
)

canvas.save(OUTPUT, quality=95)
print(OUTPUT)
