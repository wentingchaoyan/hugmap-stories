from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).parent
BASE = ROOT / "outputs/groups/49-main-three-small-mascot-turnaround-gate-v2-luke-face-lock.png"
OWL = ROOT / "outputs/characters/fukurou/fukurou-step1a-small-mascot-lock.png"
OUTPUT = ROOT / "outputs/groups/main-three-owl-small-mascot-turnaround.png"


def get_font(size: int):
    candidates = [
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


base = Image.open(BASE).convert("RGB")
owl = Image.open(OWL).convert("RGB")

# Keep the existing three-character sheet untouched and extend it by one row.
canvas = Image.new("RGB", (base.width, 1900), (250, 248, 245))
canvas.paste(base, (0, 0))

# Sample the paper background so the added row joins the original sheet softly.
paper = owl.crop((0, 930, owl.width, 1000)).resize((base.width, 364))
canvas.paste(paper, (0, 1536))

draw = ImageDraw.Draw(canvas)
draw.text((59, 1643), "OWL", font=get_font(25), fill=(20, 20, 20))

# Extract the approved FRONT / SIDE / BACK drawings, then scale all three equally.
crops = [
    owl.crop((58, 420, 365, 925)),
    owl.crop((366, 420, 674, 925)),
    owl.crop((668, 420, 976, 925)),
]
centers = [250, 550, 850]
scale = 0.68
baseline = 1855

for crop, center in zip(crops, centers):
    size = (round(crop.width * scale), round(crop.height * scale))
    view = crop.resize(size, Image.Resampling.LANCZOS)
    gray = view.convert("L")
    alpha = gray.point(lambda value: max(0, min(255, (218 - value) * 12)))
    ink = Image.new("RGBA", view.size, (25, 25, 25, 0))
    ink.putalpha(alpha)
    left = round(center - view.width / 2)
    canvas.paste(ink, (left, baseline - view.height), ink)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
canvas.save(OUTPUT, quality=96)
print(OUTPUT)
