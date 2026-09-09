from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "outputs/groups/main-three-owl-step1a-scale-check-v4-luke-brows.png"
TARGET = HERE / "outputs/groups/main-three-owl-small-mascot-turnaround.png"
FONT = "/System/Library/Fonts/Supplemental/Verdana.ttf"
SCALE = 0.60


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size)


def ink_layer(image: Image.Image, box: tuple[int, int, int, int], target_height: int | None = None) -> Image.Image:
    crop = image.crop(box).convert("RGBA")
    pixels = crop.load()
    for y in range(crop.height):
        for x in range(crop.width):
            r, g, b, _ = pixels[x, y]
            gray = (r + g + b) // 3
            # Keep only the dark character strokes. This removes the paper and
            # pale construction guides while preserving anti-aliased edges.
            alpha = max(0, min(255, int((150 - gray) * 255 / 110)))
            pixels[x, y] = (18, 18, 18, alpha)
    if target_height is None:
        size = (round(crop.width * SCALE), round(crop.height * SCALE))
        resized = crop.resize(size, Image.Resampling.LANCZOS)
        alpha = resized.getchannel("A").point(lambda value: 0 if value < 10 else min(255, round(value * 1.12)))
        resized.putalpha(alpha)
        return resized

    alpha_box = crop.getchannel("A").getbbox()
    if alpha_box:
        crop = crop.crop(alpha_box)
    target_width = round(crop.width * target_height / crop.height)
    resized = crop.resize((target_width, target_height), Image.Resampling.LANCZOS)
    alpha = resized.getchannel("A").point(lambda value: 0 if value < 10 else min(255, round(value * 1.12)))
    resized.putalpha(alpha)
    return resized


def v_dimension(draw: ImageDraw.ImageDraw, x: int, top: int, bottom: int) -> None:
    draw.line((x, top, x, bottom), fill="#222222", width=2)
    draw.line((x - 6, top + 8, x, top, x + 6, top + 8), fill="#222222", width=2)
    draw.line((x - 6, bottom - 8, x, bottom, x + 6, bottom - 8), fill="#222222", width=2)


source = Image.open(SOURCE).convert("RGB")
target = Image.open(TARGET).convert("RGBA")
turnaround_source = target.convert("RGB")
draw = ImageDraw.Draw(target)
paper = "#fbfaf7"

# Character-only source crops from the fixed STEP 2 image. The four crops are
# all placed at one shared 60% scale, so their relative sizes cannot drift.
specs = [
    # name, STEP 2 front crop, row top, baseline, STEP 2 full height,
    # side source crop, back source crop
    ("MIMO", (150, 500, 315, 844), 135, 414, 340, (430, 140, 690, 414), (700, 140, 930, 414)),
    ("GEN", (470, 350, 690, 844), 450, 804, 488, (430, 450, 690, 804), (700, 450, 930, 804)),
    ("LUKE", (790, 395, 1140, 844), 840, 1153, 440, (430, 840, 710, 1153), (700, 840, 1000, 1153)),
    ("OWL", (1160, 440, 1430, 844), 1195, 1457, 397, (430, 1195, 690, 1457), (700, 1195, 930, 1457)),
]

for name, crop_box, row_top, baseline, full_height, side_box, back_box in specs:
    # Clear only the old FRONT drawing; row label, SIDE and BACK remain intact.
    draw.rectangle((125, row_top, 430, baseline), fill=paper)
    layer = ink_layer(source, crop_box)
    x = 260 - layer.width // 2
    y = baseline - layer.height
    target.alpha_composite(layer, (x, y))

    # Restore the technical baseline and record both the STEP 2 source height
    # and its exact 60% height on this turnaround sheet.
    draw.line((125, baseline, 430, baseline), fill="#777777", width=1)
    sheet_height = round(full_height * SCALE)
    v_dimension(draw, 408, baseline - sheet_height, baseline)

    # SIDE and BACK are trimmed and uniformly resized to the exact same full
    # height as FRONT. Their internal width/depth proportions remain unchanged.
    for view_box, center_x, clear_left, clear_right in (
        (side_box, 550, 431, 699),
        (back_box, 815, 700, 1000),
    ):
        view = ink_layer(turnaround_source, view_box, target_height=sheet_height)
        draw.rectangle((clear_left, row_top, clear_right, baseline), fill=paper)
        target.alpha_composite(view, (center_x - view.width // 2, baseline - view.height))
        draw.line((clear_left, baseline, clear_right, baseline), fill="#777777", width=1)

# Explicit lock note prevents the front views being mistaken for redrawn forms.
notes = [
    "FRONT = STEP 2 LINE ART × 60%  •  HEAD / NOSE / MOUTH LOCKED",
    "FULL  STEP2/SHEET:  MIMO 340/204  •  GEN 488/293  •  LUKE 440/264  •  OWL 397/238 px",
    "HEAD: MIMO 122×133  •  GEN 180×160  •  LUKE 142×184  •  LUKE TORSO 219  •  OWL BODY 218 px",
]
for index, note in enumerate(notes):
    note_font = font(11 if index else 12)
    box = draw.textbbox((0, 0), note, font=note_font)
    y = 8 + index * 18
    draw.rectangle((512 - (box[2] - box[0]) // 2 - 7, y - 2, 512 + (box[2] - box[0]) // 2 + 7, y + 16), fill=paper)
    draw.text((512 - (box[2] - box[0]) // 2, y), note, fill="#222222", font=note_font)

target.convert("RGB").save(TARGET, quality=95)
