from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "outputs/groups/main-three-owl-step1a-scale-check-v4-luke-brows.png"
OUTPUT = HERE / "outputs/groups/main-three-owl-step1a-pixel-guide.png"
FONT = "/System/Library/Fonts/Supplemental/Verdana.ttf"


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size)


def vertical(draw: ImageDraw.ImageDraw, x: int, top: int, bottom: int, label: str, tx: int, ty: int) -> None:
    draw.line((x, top, x, bottom), fill="#111111", width=2)
    draw.line((x - 8, top + 10, x, top, x + 8, top + 10), fill="#111111", width=2)
    draw.line((x - 8, bottom - 10, x, bottom, x + 8, bottom - 10), fill="#111111", width=2)
    draw.text((tx, ty), label, fill="#111111", font=font(22), spacing=2)


def horizontal(draw: ImageDraw.ImageDraw, left: int, right: int, y: int, label: str, tx: int, ty: int) -> None:
    draw.line((left, y, right, y), fill="#111111", width=2)
    draw.line((left + 10, y - 8, left, y, left + 10, y + 8), fill="#111111", width=2)
    draw.line((right - 10, y - 8, right, y, right - 10, y + 8), fill="#111111", width=2)
    draw.text((tx, ty), label, fill="#111111", font=font(18))


image = Image.open(SOURCE).convert("RGB")
draw = ImageDraw.Draw(image)

# Preserve the STEP 2 character pixels 1:1; only replace the heading and add dimensions.
draw.rectangle((285, 45, 1260, 135), fill="#faf9f6")
title = "STEP 2 — PIXEL MEASUREMENT"
title_box = draw.textbbox((0, 0), title, font=font(42))
draw.text(((1536 - (title_box[2] - title_box[0])) / 2, 52), title, fill="#111111", font=font(42))

vertical(draw, 118, 503, 844, "", 0, 0)
vertical(draw, 438, 356, 844, "", 0, 0)
vertical(draw, 770, 404, 844, "", 0, 0)
vertical(draw, 1150, 447, 844, "", 0, 0)

# Keep height labels in the open area beneath the names so they cannot change
# the apparent width of a character or merge visually with Luke's tail.
draw.text((188, 300), "FULL 340 px", fill="#111111", font=font(20))
draw.text((535, 270), "FULL 488 px", fill="#111111", font=font(20))
draw.text((875, 300), "FULL 440 px", fill="#111111", font=font(20))
draw.text((1245, 300), "FULL 397 px", fill="#111111", font=font(20))

horizontal(draw, 176, 294, 480, "HEAD 122×133 px", 158, 447)
horizontal(draw, 497, 677, 330, "HEAD 180×160 px", 495, 297)
horizontal(draw, 855, 997, 378, "HEAD 142×184 px", 842, 345)
horizontal(draw, 1192, 1410, 422, "BODY W 218 px", 1200, 389)

details = "LUKE TORSO W 219 px • OWL FACE 173×185 px • OWL WING 146 px"
details_box = draw.textbbox((0, 0), details, font=font(17))
draw.text(((1536 - (details_box[2] - details_box[0])) / 2, 915), details, fill="#111111", font=font(17))

footer = "SAME 1536 × 1024 COORDINATES • CHARACTERS COPIED 1:1 FROM STEP 2"
footer_box = draw.textbbox((0, 0), footer, font=font(17))
draw.text(((1536 - (footer_box[2] - footer_box[0])) / 2, 952), footer, fill="#111111", font=font(17))

image.save(OUTPUT, quality=95)
