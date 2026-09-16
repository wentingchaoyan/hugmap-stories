#!/usr/bin/env python3
"""Normalize child silhouette lines in participatory-growth frames."""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


TARGET = np.array([0xFA, 0x99, 0x7B], dtype=np.float32)

# Mimo scenes contain several orange roles at once: the child, a lighter
# parent, Mimo's saturated scarf/U, and action marks. These conservative
# regions isolate only the faceless child silhouette in each approved frame.
MIMO_CHILD_REGIONS: dict[str, tuple[int, int, int, int]] = {
    "mimo-frame-aac-one-word.png": (60, 400, 550, 1020),
    "mimo-frame-body-parts-song.png": (550, 420, 930, 1030),
    "mimo-frame-bubble-play.png": (100, 350, 590, 1080),
    "mimo-frame-child-leads-imitation.png": (150, 170, 760, 1100),
    "mimo-frame-choice-response.png": (100, 430, 520, 1030),
    "mimo-frame-choice-with-reason.png": (400, 280, 820, 1100),
    "mimo-frame-doctor-pretend.png": (150, 230, 830, 1020),
    "mimo-frame-emotion-expression.png": (150, 400, 650, 1160),
    "mimo-frame-event-sequence.png": (20, 330, 450, 1000),
    "mimo-frame-experience-feeling.png": (430, 300, 930, 900),
    "mimo-frame-freeze-notice.png": (100, 180, 640, 1120),
    "mimo-frame-hidden-find.png": (70, 120, 800, 1100),
    "mimo-frame-imitation-arms-up.png": (100, 180, 780, 1110),
    "mimo-frame-noticing-letters.png": (120, 200, 720, 1100),
    "mimo-frame-one-word-more.png": (100, 430, 540, 1000),
    "mimo-frame-parent-child-pretend-meal.png": (130, 400, 500, 900),
    "mimo-frame-peace-sign.png": (220, 120, 700, 1140),
    "mimo-frame-pretend-cooking.png": (90, 230, 730, 1080),
    "mimo-frame-pretend-feeding.png": (120, 230, 720, 1050),
    "mimo-frame-pretend-phone.png": (150, 150, 630, 1100),
    "mimo-frame-pretend-shop.png": (20, 330, 510, 1050),
    "mimo-frame-refusal-boundary.png": (100, 150, 820, 1100),
    "mimo-frame-request-sign.png": (140, 260, 700, 1060),
    "mimo-frame-rhythm-copy.png": (130, 320, 620, 1100),
    "mimo-frame-routine-shoe-message.png": (100, 350, 520, 1020),
    "mimo-frame-shared-pointing.png": (240, 240, 780, 1150),
    "mimo-frame-shared-reading.png": (100, 350, 610, 1000),
    "mimo-frame-show-and-receive.png": (150, 100, 730, 1150),
    "mimo-frame-social-referencing.png": (140, 300, 500, 1000),
    "mimo-frame-three-photo-story.png": (380, 230, 800, 760),
    "mimo-frame-three-step-entry.png": (180, 220, 700, 1030),
    "mimo-frame-turn-taking-cards.png": (50, 400, 580, 1000),
    "mimo-frame-two-picture-schedule.png": (0, 340, 500, 970),
    "mimo-frame-voice-pingpong.png": (0, 90, 620, 1254),
    "mimo-frame-wave-response.png": (160, 170, 700, 1120),
    "mimo-frame-word-expansion.png": (100, 400, 530, 1000),
}


def orange_mask(rgb: np.ndarray) -> np.ndarray:
    """Select orange/pink line pixels while excluding beige and yellow scenery."""
    r, g, b = (rgb[..., i].astype(np.int16) for i in range(3))
    return (
        (r >= 220)
        & (g >= 70)
        & (g <= 190)
        & (b >= 35)
        & (b <= 180)
        & (r - g >= 45)
        & (r - b >= 55)
    )


def mimo_child_orange_mask(rgb: np.ndarray) -> np.ndarray:
    """Include legacy saturated child strokes inside a known Mimo child region."""
    r, g, b = (rgb[..., i].astype(np.int16) for i in range(3))
    return (
        (r >= 220)
        & (g >= 50)
        & (g <= 190)
        & (b >= 15)
        & (b <= 180)
        & (r - g >= 45)
        & (r - b >= 55)
    )


def large_components(mask: np.ndarray, minimum: int = 700) -> np.ndarray:
    """Keep large connected orange components (the child), not Gen's small accents."""
    height, width = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    kept = np.zeros_like(mask, dtype=bool)
    for y0, x0 in zip(*np.nonzero(mask & ~seen)):
        if seen[y0, x0]:
            continue
        queue = deque([(int(y0), int(x0))])
        seen[y0, x0] = True
        points: list[tuple[int, int]] = []
        while queue:
            y, x = queue.popleft()
            points.append((y, x))
            for yy in range(max(0, y - 1), min(height, y + 2)):
                for xx in range(max(0, x - 1), min(width, x + 2)):
                    if mask[yy, xx] and not seen[yy, xx]:
                        seen[yy, xx] = True
                        queue.append((yy, xx))
        if len(points) >= minimum:
            ys, xs = zip(*points)
            kept[np.asarray(ys), np.asarray(xs)] = True
    return kept


def child_line_components(
    rgb: np.ndarray,
    *,
    minimum: int = 700,
    exclude_saturated_accents: bool = False,
    frame_name: str | None = None,
) -> np.ndarray:
    """Keep child-line components while excluding small marks and Mimo accents."""
    region = MIMO_CHILD_REGIONS.get(frame_name or "")
    mask = mimo_child_orange_mask(rgb) if region is not None else orange_mask(rgb)
    if region is not None:
        x0, y0, x1, y1 = region
        inside = np.zeros_like(mask)
        inside[y0:y1, x0:x1] = True
        mask &= inside
        minimum = 500
    height, width = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    kept = np.zeros_like(mask, dtype=bool)
    for y0, x0 in zip(*np.nonzero(mask & ~seen)):
        if seen[y0, x0]:
            continue
        queue = deque([(int(y0), int(x0))])
        seen[y0, x0] = True
        points: list[tuple[int, int]] = []
        while queue:
            y, x = queue.popleft()
            points.append((y, x))
            for yy in range(max(0, y - 1), min(height, y + 2)):
                for xx in range(max(0, x - 1), min(width, x + 2)):
                    if mask[yy, xx] and not seen[yy, xx]:
                        seen[yy, xx] = True
                        queue.append((yy, xx))
        if len(points) < minimum:
            continue
        ys, xs = zip(*points)
        component = (np.asarray(ys), np.asarray(xs))
        median = np.median(rgb[component], axis=0)
        # Mimo's scarf, chest U, and action marks use a much more saturated
        # orange than the child outline. Keep them unchanged.
        if region is None and exclude_saturated_accents and (median[1] < 110 or median[2] < 65):
            continue
        kept[component] = True
    return kept


def skeletonize(mask: np.ndarray) -> np.ndarray:
    """Return a one-pixel centerline using Zhang-Suen thinning."""
    work = mask.copy()
    while True:
        changed = False
        for first_pass in (True, False):
            padded = np.pad(work, 1)
            p2 = padded[:-2, 1:-1]
            p3 = padded[:-2, 2:]
            p4 = padded[1:-1, 2:]
            p5 = padded[2:, 2:]
            p6 = padded[2:, 1:-1]
            p7 = padded[2:, :-2]
            p8 = padded[1:-1, :-2]
            p9 = padded[:-2, :-2]
            neighbours = (p2, p3, p4, p5, p6, p7, p8, p9)
            count = sum(n.astype(np.uint8) for n in neighbours)
            transitions = sum(
                ((~neighbours[i]) & neighbours[(i + 1) % 8]).astype(np.uint8)
                for i in range(8)
            )
            if first_pass:
                condition_a = ~(p2 & p4 & p6)
                condition_b = ~(p4 & p6 & p8)
            else:
                condition_a = ~(p2 & p4 & p8)
                condition_b = ~(p2 & p6 & p8)
            remove = (
                work
                & (count >= 2)
                & (count <= 6)
                & (transitions == 1)
                & condition_a
                & condition_b
            )
            if remove.any():
                work[remove] = False
                changed = True
        if not changed:
            return work


def fixed_pixel_stroke(centerline: np.ndarray, width: int) -> np.ndarray:
    """Rasterize the centerline at a visually antialiased fixed pixel width."""
    small = Image.fromarray(centerline.astype(np.uint8) * 255)
    scale = 4
    large = small.resize((small.width * scale, small.height * scale), Image.Resampling.NEAREST)
    # A 1 px centerline becomes 4 px at 4x. Expand symmetrically to the
    # requested width before antialiased downsampling.
    filter_size = width * scale - scale + 1
    large = large.filter(ImageFilter.MaxFilter(filter_size))
    return np.asarray(
        large.resize(small.size, Image.Resampling.LANCZOS), dtype=np.uint8
    )


def shrink_stroke_one_pixel(mask: np.ndarray) -> np.ndarray:
    """Shrink an existing smooth stroke by one total output pixel."""
    small = Image.fromarray(mask.astype(np.uint8) * 255)
    scale = 4
    large = small.resize((small.width * scale, small.height * scale), Image.Resampling.LANCZOS)
    # A 5 px minimum filter removes 2 high-resolution pixels per side:
    # 4 high-resolution pixels, or exactly 1 output pixel, in total width.
    large = large.filter(ImageFilter.MinFilter(5))
    return np.asarray(
        large.resize(small.size, Image.Resampling.LANCZOS), dtype=np.uint8
    )


def resize_stroke(mask: np.ndarray, delta_pixels: int) -> np.ndarray:
    """Resize an existing stroke by a total number of output pixels."""
    small = Image.fromarray(mask.astype(np.uint8) * 255)
    scale = 4
    large = small.resize((small.width * scale, small.height * scale), Image.Resampling.LANCZOS)
    if delta_pixels < 0:
        large = large.filter(ImageFilter.MinFilter(abs(delta_pixels) * scale + 1))
    elif delta_pixels > 0:
        large = large.filter(ImageFilter.MaxFilter(delta_pixels * scale + 1))
    return np.asarray(
        large.resize(small.size, Image.Resampling.LANCZOS), dtype=np.uint8
    )


def inpaint_line(rgb: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Fill the old line from adjacent pixels before drawing the fixed-width one."""
    result = rgb.astype(np.float32).copy()
    unknown = mask.copy()
    height, width = unknown.shape
    for _ in range(12):
        if not unknown.any():
            break
        padded_values = np.pad(result, ((1, 1), (1, 1), (0, 0)), mode="edge")
        padded_known = np.pad(~unknown, 1, mode="constant", constant_values=False)
        total = np.zeros_like(result)
        weights = np.zeros((height, width), dtype=np.float32)
        for dy in range(3):
            for dx in range(3):
                if dy == 1 and dx == 1:
                    continue
                known = padded_known[dy : dy + height, dx : dx + width]
                total += padded_values[dy : dy + height, dx : dx + width] * known[..., None]
                weights += known
        fillable = unknown & (weights > 0)
        result[fillable] = total[fillable] / weights[fillable, None]
        unknown[fillable] = False
    return np.rint(result).clip(0, 255).astype(np.uint8)


def propagate_line_color(rgb: np.ndarray, mask: np.ndarray, steps: int = 6) -> np.ndarray:
    """Extend each source stroke's own color a few pixels for rerasterization."""
    result = rgb.astype(np.float32).copy()
    known = mask.copy()
    height, width = known.shape
    for _ in range(steps):
        padded_values = np.pad(result, ((1, 1), (1, 1), (0, 0)), mode="edge")
        padded_known = np.pad(known, 1, mode="constant", constant_values=False)
        total = np.zeros_like(result)
        weights = np.zeros((height, width), dtype=np.float32)
        for dy in range(3):
            for dx in range(3):
                if dy == 1 and dx == 1:
                    continue
                source_known = padded_known[dy : dy + height, dx : dx + width]
                total += padded_values[dy : dy + height, dx : dx + width] * source_known[..., None]
                weights += source_known
        fillable = ~known & (weights > 0)
        result[fillable] = total[fillable] / weights[fillable, None]
        known[fillable] = True
    return result


def enclosed_fill(mask: np.ndarray) -> np.ndarray:
    """Find regions enclosed by a line mask, ignoring everything outside its bbox."""
    ys, xs = np.nonzero(mask)
    if not len(xs):
        return np.zeros_like(mask)
    margin = 8
    y0, y1 = max(0, int(ys.min()) - margin), min(mask.shape[0], int(ys.max()) + margin + 1)
    x0, x1 = max(0, int(xs.min()) - margin), min(mask.shape[1], int(xs.max()) + margin + 1)
    # The child can touch the slide or contain tiny antialias gaps. A wider
    # temporary barrier closes only those gaps; the drawn outline itself is
    # left untouched.
    barrier = np.asarray(
        Image.fromarray(mask.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(15))
    ) > 0
    crop = barrier[y0:y1, x0:x1]
    outside = np.zeros_like(crop)
    queue: deque[tuple[int, int]] = deque()
    for y in range(crop.shape[0]):
        for x in (0, crop.shape[1] - 1):
            if not crop[y, x] and not outside[y, x]:
                outside[y, x] = True
                queue.append((y, x))
    for x in range(crop.shape[1]):
        for y in (0, crop.shape[0] - 1):
            if not crop[y, x] and not outside[y, x]:
                outside[y, x] = True
                queue.append((y, x))
    while queue:
        y, x = queue.popleft()
        for yy, xx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if (
                0 <= yy < crop.shape[0]
                and 0 <= xx < crop.shape[1]
                and not crop[yy, xx]
                and not outside[yy, xx]
            ):
                outside[yy, xx] = True
                queue.append((yy, xx))
    result = np.zeros_like(mask)
    result[y0:y1, x0:x1] = ~outside & ~crop
    return result


def process(
    path: Path,
    output: Path,
    *,
    fixed_width: bool = True,
    line_width: int = 4,
    preserve_color: bool = False,
    shrink_one_pixel: bool = False,
    auto_width: bool = False,
    target_width: float = 4.3,
    exclude_saturated_accents: bool = False,
    white_fill: bool = False,
) -> tuple[int, int, float, int]:
    image = Image.open(path).convert("RGB")
    rgb = np.asarray(image).copy()
    selected = child_line_components(
        rgb,
        exclude_saturated_accents=exclude_saturated_accents,
        frame_name=path.name,
    )
    if not selected.any():
        return 0, 0, 0.0, 0

    # Include the existing antialiased edge pixels around the selected line.
    expanded = np.asarray(
        Image.fromarray(selected.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(5))
    ) > 0
    r, g, b = (rgb[..., i].astype(np.int16) for i in range(3))
    if path.name in MIMO_CHILD_REGIONS:
        soft_orange = (
            expanded
            & (r >= 220)
            & (g >= 45)
            & (g <= 220)
            & (b >= 15)
            & (b <= 205)
            & (r - g >= 25)
            & (r - b >= 35)
        )
    else:
        soft_orange = (
            expanded
            & (r >= 220)
            & (g >= 85)
            & (g <= 220)
            & (b >= 55)
            & (b <= 205)
            & (r - g >= 25)
            & (r - b >= 35)
        )

    if white_fill:
        rgb[enclosed_fill(selected)] = 255

    width_before = float(selected.sum()) / max(1, int(skeletonize(selected).sum()))
    delta_pixels = 0

    if auto_width:
        if 3.5 <= width_before <= 4.8:
            delta_pixels = 0
        else:
            delta_pixels = int(np.clip(np.rint(target_width - width_before), -4, 4))
        if delta_pixels == 0:
            # Preserve already-acceptable smooth geometry; only normalize its
            # center color and antialiased coverage.
            source = rgb[soft_orange].astype(np.float32)
            coverage = np.clip((255.0 - source.min(axis=1)) / 125.0, 0.18, 1.0)[:, None]
            normalized = 255.0 - coverage * (255.0 - TARGET)
            rgb[soft_orange] = np.rint(normalized).clip(0, 255).astype(np.uint8)
            changed = int(soft_orange.sum())
        else:
            stroke = resize_stroke(soft_orange, delta_pixels)
            erase = np.asarray(
                Image.fromarray(soft_orange.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(3))
            ) > 0
            rgb = inpaint_line(rgb, erase)
            alpha = (stroke.astype(np.float32) / 255.0)[..., None]
            rgb = np.rint(rgb * (1.0 - alpha) + TARGET * alpha).clip(0, 255).astype(np.uint8)
            changed = int((stroke > 0).sum())
    elif shrink_one_pixel:
        stroke = shrink_stroke_one_pixel(soft_orange)
        line_colors = propagate_line_color(rgb, selected)
        erase = np.asarray(
            Image.fromarray(soft_orange.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(3))
        ) > 0
        rgb = inpaint_line(rgb, erase)
        alpha = (stroke.astype(np.float32) / 255.0)[..., None]
        rgb = np.rint(rgb * (1.0 - alpha) + line_colors * alpha).clip(0, 255).astype(np.uint8)
        changed = int((stroke > 0).sum())
    elif fixed_width:
        centerline = skeletonize(selected)
        stroke = fixed_pixel_stroke(centerline, line_width)
        erase = np.asarray(
            Image.fromarray(soft_orange.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(3))
        ) > 0
        line_colors = propagate_line_color(rgb, selected) if preserve_color else None
        rgb = inpaint_line(rgb, erase)
        alpha = (stroke.astype(np.float32) / 255.0)[..., None]
        paint = line_colors if line_colors is not None else TARGET
        rgb = np.rint(rgb * (1.0 - alpha) + paint * alpha).clip(0, 255).astype(np.uint8)
        changed = int((stroke > 0).sum())
    else:
        source = rgb[soft_orange].astype(np.float32)
        coverage = np.clip((255.0 - source.min(axis=1)) / 125.0, 0.18, 1.0)[:, None]
        normalized = 255.0 - coverage * (255.0 - TARGET)
        rgb[soft_orange] = np.rint(normalized).clip(0, 255).astype(np.uint8)
        changed = int(soft_orange.sum())
    Image.fromarray(rgb, "RGB").save(output, optimize=True)
    return int(selected.sum()), changed, width_before, delta_pixels


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--output-directory", type=Path)
    parser.add_argument("--color-only", action="store_true")
    parser.add_argument("--white-fill", action="store_true")
    parser.add_argument("--line-width", type=int, choices=(3, 4), default=4)
    parser.add_argument("--preserve-color", action="store_true")
    parser.add_argument("--shrink-one-pixel", action="store_true")
    parser.add_argument("--auto-width", action="store_true")
    parser.add_argument("--target-width", type=float, default=4.3)
    parser.add_argument("--prefix", choices=("gen", "mimo"), default="gen")
    parser.add_argument("--only", nargs="*")
    args = parser.parse_args()
    destination = args.output_directory or args.directory
    destination.mkdir(parents=True, exist_ok=True)
    paths = sorted(args.directory.glob(f"{args.prefix}-frame-*.png"))
    if args.only:
        allowed = set(args.only)
        paths = [path for path in paths if path.name in allowed]
    for path in paths:
        selected, changed, width_before, delta_pixels = process(
            path,
            destination / path.name,
            fixed_width=not args.color_only,
            line_width=args.line_width,
            preserve_color=args.preserve_color,
            shrink_one_pixel=args.shrink_one_pixel,
            auto_width=args.auto_width,
            target_width=args.target_width,
            exclude_saturated_accents=args.prefix == "mimo",
            white_fill=args.white_fill,
        )
        print(
            f"{path.name}: core={selected} changed={changed} "
            f"width={width_before:.2f} delta={delta_pixels:+d}px"
        )


if __name__ == "__main__":
    main()
