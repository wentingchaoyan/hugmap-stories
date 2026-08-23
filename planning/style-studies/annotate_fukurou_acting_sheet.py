from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).parent
IMAGE = ROOT / "outputs/characters/fukurou/fukurou-character-acting-sheet.png"


def font(size: int, bold: bool = False):
    weight = "W6" if bold else "W3"
    path = Path(f"/System/Library/Fonts/ヒラギノ角ゴシック {weight}.ttc")
    return ImageFont.truetype(path, size)


items = [
    ("1｜前後を並べる", "「その前には、何があった？」"),
    ("2｜時間をつなぐ", "「そのあと、どうなった？」"),
    ("3｜新事実に気づく", "「もう一つ、分かったことがあるね」"),
    ("4｜結論を待つ", "「まだ答えは一つにしないでおこう」"),
    ("5｜違いを比べる", "「起きなかった日は、何が違った？」"),
    ("6｜感情を受け止める", "「突然に見えて、びっくりしたね」"),
    ("7｜仮説を開く", "「理由はいくつか重なっているかもしれない」"),
    ("8｜納得して揃える", "「いったん、ここまでを並べよう」"),
]

image = Image.open(IMAGE).convert("RGBA")
overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)
cell_w = image.width // 4

for index, (action, words) in enumerate(items):
    col = index % 4
    row = index // 4
    x = col * cell_w + 14
    y = 12 if row == 0 else image.height // 2 + 6
    draw.rounded_rectangle(
        (x, y, x + cell_w - 28, y + 57),
        radius=8,
        fill=(255, 251, 245, 225),
        outline=(207, 198, 190, 190),
        width=1,
    )
    draw.text((x + 9, y + 6), action, font=font(16, True), fill=(107, 55, 62, 255))
    draw.text((x + 9, y + 31), words, font=font(12), fill=(65, 61, 58, 255))

Image.alpha_composite(image, overlay).convert("RGB").save(IMAGE, quality=96)
print(IMAGE)
