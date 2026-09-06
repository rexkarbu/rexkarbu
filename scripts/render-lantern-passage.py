"""Render the original Lantern Passage cutout animation. Python 3.10+, Pillow, NumPy.

No network, image model, video service, or token is needed to render saved sources.
The old animate-banner.py remains available for the archived workshop illustration.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/banner/source"
SIZE = (1200, 360)
SCALE = 2  # Supersampling only the moving character keeps ink edges smooth.
RIG_SIZE = (200, 180)
GROUND = 300
LEFT, RIGHT = 400, 800
PALETTE = {"amber": (229, 181, 103), "mist": (157, 183, 165)}
TAU = 2 * math.pi


def ease(value):
    value = max(0.0, min(1.0, value))
    return value * value * (3 - 2 * value)


def distance(t):
    """400 px in 3.2 s, with smooth acceleration at both ends."""
    ramp, duration = 0.24, 3.2
    speed = (RIGHT - LEFT) / (duration - ramp)
    if t < ramp:
        return speed * (t / 2 - ramp * math.sin(math.pi * t / ramp) / (2 * math.pi))
    if t > duration - ramp:
        return RIGHT - LEFT - distance(duration - t)
    return speed * (t - ramp / 2)


def gait(phase):
    """Stance: world-space foot position stays fixed. Swing: lift and recover."""
    phase %= 1
    if phase < 0.5:
        return 20 - 80 * phase, 0.0
    swing = (phase - 0.5) * 2
    # Match horizontal derivative to stance at contact and toe-off.
    x = -20 - 40 * swing + 240 * swing**2 - 160 * swing**3
    return x, -14 * math.sin(math.pi * swing)**2


def resting_feet(progress, preparing=False):
    """Reposition one foot at a time; each reposition includes a small lift."""
    values = []
    for index, sign in enumerate((1, -1)):
        local = max(0.0, min(1.0, progress * 2 - (1 - index)))
        start, end = (7, 20) if preparing else (20, 7)
        values.append((sign * (start + (end - start) * ease(local)),
                       -5 * math.sin(math.pi * local)**2))
    return values


def pose(seconds):
    """Two symmetric 4.5 s halves make a continuous 9 s master timeline."""
    half = int(seconds // 4.5) % 2
    local = seconds % 4.5
    facing = 1 if half == 0 else -1
    origin = LEFT if half == 0 else RIGHT
    if local < 3.2:
        traveled = distance(local)
        phase = traveled / 80
        ramp = min(local / 0.24, (3.2 - local) / 0.24, 1)
        active = ease(ramp)
        feet = (gait(phase), gait(phase + 0.5))
        return origin + facing * traveled, facing, 1.0, phase, active, feet, "walk"
    x = RIGHT if half == 0 else LEFT
    if local < 3.7:
        feet = resting_feet((local - 3.2) / 0.5)
        return x, facing, 1.0, 5.0, 0.0, feet, "settle"
    if local < 4.0:
        turn = (local - 3.7) / 0.3
        # A brief perspective turn of the cutout; never morph facial features.
        width = 0.35 + 0.65 * abs(math.cos(math.pi * turn))
        return x, facing if turn < 0.5 else -facing, width, 5.0, 0.0, ((7, 0), (-7, 0)), "turn"
    return x, -facing, 1.0, 5.0, 0.0, resting_feet((local - 4.0) / 0.5, True), "prepare"


def extract_parts():
    sheet = Image.open(SOURCE / "traveler-sheet.png").convert("RGB")
    rgb = np.asarray(sheet).astype(np.int16)
    # The generator returned an RGB checkerboard. Remove only light neutral
    # background connected to the canvas edge; preserve enclosed cloth colors.
    neutral = ((rgb.max(2) - rgb.min(2) < 18) & (rgb.min(2) > 205))
    flood = Image.fromarray((neutral * 255).astype("uint8")).copy()
    ImageDraw.floodfill(flood, (0, 0), 128, thresh=0)
    alpha = Image.fromarray(np.where(np.asarray(flood) == 128, 0, 255).astype("uint8"))
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.45))
    sheet.putalpha(alpha)
    boxes = {"body": (78, 128, 542, 825), "leg": (680, 290, 880, 849),
             "arm": (1004, 374, 1134, 773), "tail": (1240, 350, 1467, 860)}
    return {name: sheet.crop(box) for name, box in boxes.items()}


def segment(canvas, sprite, start, end, target_start, target_end, width=0.11, shade=1.0):
    """Map an illustrated limb between two joints, retaining its painted texture."""
    start, end, a, b = (np.array(p, dtype=float) for p in (start, end, target_start, target_end))
    direction, target = end - start, b - a
    unit = direction / np.linalg.norm(direction)
    normal = np.array((-unit[1], unit[0]))
    aim = target / np.linalg.norm(target)
    across = np.array((-aim[1], aim[0]))
    matrix = np.outer(aim, unit) * np.linalg.norm(target) / np.linalg.norm(direction)
    matrix += np.outer(across, normal) * width
    matrix *= SCALE
    offset = a * SCALE - matrix @ start
    inverse = np.linalg.inv(matrix)
    translation = -inverse @ offset
    coefficients = (*inverse[0], translation[0], *inverse[1], translation[1])
    result = sprite.transform(canvas.size, Image.Transform.AFFINE, coefficients, Image.Resampling.BICUBIC)
    if shade != 1:
        result = ImageEnhance.Brightness(result).enhance(shade)
    canvas.alpha_composite(result)


def knee(hip, ankle):
    """Two-bone inverse kinematics; knees bend toward the direction of travel."""
    hip, ankle = np.array(hip), np.array(ankle)
    delta = ankle - hip
    length = float(np.linalg.norm(delta))
    upper, lower = 29.0, 29.0
    if length >= upper + lower:
        raise ValueError("Rig overextended; adjust stride, ground, or hip height")
    along = (upper**2 - lower**2 + length**2) / (2 * length)
    height = math.sqrt(max(0, upper**2 - along**2))
    unit = delta / length
    return hip + unit * along + np.array((unit[1], -unit[0])) * height


def render_character(parts, seconds):
    x, facing, turn_width, phase, activity, feet, action = pose(seconds)
    rig = Image.new("RGBA", tuple(n * SCALE for n in RIG_SIZE))
    breath = 0.5 * math.sin(TAU * seconds / 4.5)
    bob = activity * (1 - math.cos(2 * TAU * phase)) * 1.0 + (1 - activity) * breath
    hip = (100, 101 + bob)
    leg = parts["leg"]
    upper = leg.crop((0, 0, 200, 309))
    lower = leg.crop((0, 266, 200, 477))
    boot = leg.crop((0, 419, 200, 559))
    for index in (1, 0):
        foot_x, lift = feet[index]
        ankle = (100 + foot_x, 154 + lift)
        joint = knee(hip, ankle)
        shade = 0.73 if index else 1.0
        segment(rig, upper, (87, 14), (71, 287), hip, joint, 0.105, shade)
        segment(rig, lower, (71, 21), (69, 193), joint, ankle, 0.105, shade)
        # Ankle-to-sole stays vertical during contact, so boots stay on the path.
        segment(rig, boot, (69, 40), (69, 133), ankle, (ankle[0], 160 + lift), 0.11, shade)

    lag = math.sin(TAU * phase - 0.8) * activity + 0.25 * math.sin(TAU * seconds / 4.5)
    segment(rig, parts["tail"], (171, 22), (58, 448), (91, 73 + bob),
            (75 - lag * 5, 114 + bob), 0.1, 0.83)
    swing = math.cos(TAU * phase) * activity * 10
    segment(rig, parts["arm"], (65, 24), (77, 350), (94, 72 + bob),
            (94 + swing, 108 + bob), 0.10, 0.76)

    body = parts["body"].resize((60 * SCALE, 90 * SCALE), Image.Resampling.LANCZOS)
    padded = Image.new("RGBA", (84 * SCALE, 94 * SCALE))
    padded.alpha_composite(body, (12 * SCALE, 0))
    mesh = []
    for top in range(0, padded.height, 8):
        bottom = min(padded.height, top + 8)
        def shift(y):
            weight = max(0, (y / SCALE - 43) / 47)**1.4
            return 3.2 * SCALE * lag * weight
        s0, s1 = shift(top), shift(bottom)
        mesh.append(((0, top, padded.width, bottom),
                     (-s0, top, -s1, bottom, padded.width - s1, bottom, padded.width - s0, top)))
    body = padded.transform(padded.size, Image.Transform.MESH, mesh, Image.Resampling.BICUBIC)
    rig.alpha_composite(body, (61 * SCALE, round((12 + bob) * SCALE)))
    segment(rig, parts["arm"], (65, 24), (77, 350), (110, 73 + bob),
            (110 - swing, 109 + bob), 0.10)

    rig = rig.resize(RIG_SIZE, Image.Resampling.LANCZOS)
    if facing < 0:
        rig = ImageOps.mirror(rig)
    if turn_width < 1:
        rig = rig.resize((round(RIG_SIZE[0] * turn_width), RIG_SIZE[1]), Image.Resampling.LANCZOS)
    return rig, (round(x - rig.width / 2), GROUND - 160), action


def background():
    source = Image.open(SOURCE / "garden.png").convert("RGB")
    width, height = source.size
    # Keep the full width. Crop excess bottom masonry, never tile or stretch.
    crop_height = round(width * SIZE[1] / SIZE[0])
    return source.crop((0, 0, width, crop_height)).resize(SIZE, Image.Resampling.LANCZOS).convert("RGBA")


def atmosphere(base):
    """Reusable soft layers: illumination moves locally, not the entire image."""
    lights = []
    for cx, cy in ((277, 90), (594, 88), (915, 90)):
        layer = Image.new("RGBA", SIZE)
        draw = ImageDraw.Draw(layer)
        for radius in range(42, 0, -1):
            strength = round(36 * (1 - radius / 43)**2)
            draw.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), fill=(*PALETTE["amber"], strength))
        lights.append(layer)
    fog = Image.new("RGBA", SIZE)
    draw = ImageDraw.Draw(fog)
    for box in ((70, 250, 510, 277), (540, 208, 940, 238), (735, 270, 1160, 293)):
        draw.ellipse(box, fill=(*PALETTE["mist"], 13))
    fog = fog.filter(ImageFilter.GaussianBlur(14))
    rng = np.random.default_rng(260907)
    particles = [(float(rng.uniform(190, 1020)), float(rng.uniform(132, 276)),
                  float(rng.uniform(0, TAU)), float(rng.uniform(0.8, 1.5))) for _ in range(12)]
    return lights, fog, particles


def render_frame(base, parts, layers, seconds):
    phase = seconds / 9
    lights, fog, particles = layers
    frame = base.copy()
    for index, light in enumerate(lights):
        layer = light.copy()
        strength = 0.68 + 0.30 * math.sin(TAU * phase * 2 + index * 1.4)
        layer.putalpha(light.getchannel("A").point(lambda value: round(value * strength)))
        frame.alpha_composite(layer)
    frame.alpha_composite(fog, (round(18 * math.sin(TAU * phase)), round(2 * math.cos(TAU * phase))))
    motes = Image.new("RGBA", SIZE)
    draw = ImageDraw.Draw(motes)
    for px, py, offset, radius in particles:
        px += 9 * math.sin(TAU * phase + offset)
        py += 6 * math.cos(TAU * phase + offset)
        alpha = round(100 + 45 * math.sin(TAU * phase * 2 + offset))
        draw.ellipse((px-radius-2, py-radius-2, px+radius+2, py+radius+2), fill=(*PALETTE["amber"], 12))
        draw.ellipse((px-radius, py-radius, px+radius, py+radius), fill=(*PALETTE["amber"], alpha))
    frame.alpha_composite(motes)
    x = pose(seconds)[0]
    shadow = Image.new("RGBA", SIZE)
    ImageDraw.Draw(shadow).ellipse((x-30, GROUND-3, x+31, GROUND+5), fill=(9, 19, 23, 105))
    frame.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(2)))
    character, position, _ = render_character(parts, seconds)
    frame.alpha_composite(character, position)
    return frame.convert("RGB")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duration", type=float, default=9.0, help="Loop seconds; scales the whole timeline")
    parser.add_argument("--fps", type=int, default=16)
    parser.add_argument("--colors", type=int, default=192)
    parser.add_argument("--output", type=Path, default=ROOT / "assets/banner")
    parser.add_argument("--frames", type=Path, help="Optional decoded RGB frames for visual review; outside repo recommended")
    args = parser.parse_args()
    if not 8 <= args.fps <= 25 or not 32 <= args.colors <= 256 or not 4 <= args.duration <= 20:
        parser.error("Use fps 8..25, colors 32..256, duration 4..20 seconds")
    args.output.mkdir(parents=True, exist_ok=True)
    if args.frames:
        args.frames.mkdir(parents=True, exist_ok=True)
    base, parts = background(), extract_parts()
    layers = atmosphere(base)
    count = round(args.duration * args.fps)
    frames = []
    for index in range(count):
        frame = render_frame(base, parts, layers, 9 * index / count)
        frames.append(frame)
        if args.frames:
            frame.save(args.frames / f"frame-{index:03}.png")
    # Sample the whole walk so cloak/skin colors have room in the global palette.
    samples = Image.new("RGB", (SIZE[0], SIZE[1] * 12))
    for i in range(12):
        samples.paste(frames[round(i * (count-1) / 11)], (0, SIZE[1] * i))
    palette = samples.quantize(colors=args.colors, dither=Image.Dither.NONE)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    # GIF stores centiseconds. Alternate delays to keep the exact loop duration.
    delays = [10 * (round((i+1) * args.duration * 100 / count) - round(i * args.duration * 100 / count)) for i in range(count)]
    gif = args.output / "lantern-passage.gif"
    png = args.output / "lantern-passage.png"
    indexed[0].save(gif, save_all=True, append_images=indexed[1:], duration=delays,
                    loop=0, optimize=True, disposal=1)
    frames[round(count * 1.6 / 9)].save(png, optimize=True)
    manifest = {"resolution": list(SIZE), "frames": count, "duration_ms": sum(delays),
                "average_fps": count * 1000 / sum(delays), "palette_colors": args.colors,
                "loop": "infinite", "gif_bytes": gif.stat().st_size, "png_bytes": png.stat().st_size,
                "source_sha256": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                                   for path in sorted(SOURCE.glob("*.png"))}}
    (args.output / "render-info.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
