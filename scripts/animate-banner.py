"""Create a quiet monitor-light loop from the checked-in PNG. Requires Pillow."""

from math import cos, pi
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance


ASSETS = Path(__file__).resolve().parents[1] / "assets"
SIZE = (1200, 360)
# Coordinates in the final PNG, inside the monitor bezel (left, top, right, bottom).
MONITOR = (294, 90, 543, 249)
FRAME_COUNT = 24
FRAME_MS = 160


def main():
    with Image.open(ASSETS / "rexs-night-workshop.png") as source:
        base = source.convert("RGB")
    if base.size != SIZE:
        raise SystemExit("Expected a 1200 x 360 PNG; update SIZE and MONITOR for a new composition.")

    mask = Image.new("L", SIZE, 0)
    ImageDraw.Draw(mask).rectangle(MONITOR, fill=255)
    darkest = Image.composite(ImageEnhance.Brightness(base).enhance(0.92), base, mask)

    # One shared palette prevents unrelated pixels from shimmering between frames.
    samples = Image.new("RGB", (SIZE[0], SIZE[1] * 2))
    samples.paste(base, (0, 0))
    samples.paste(darkest, (0, SIZE[1]))
    palette = samples.quantize(colors=128, dither=Image.Dither.NONE)

    frames = []
    for index in range(FRAME_COUNT):
        # Starts at the still image; a smooth 8% dip over a 3.84-second loop.
        darkness = 0.04 * (1 - cos(2 * pi * index / FRAME_COUNT))
        dimmed = ImageEnhance.Brightness(base).enhance(1 - darkness)
        frame = Image.composite(dimmed, base, mask)
        frames.append(frame.quantize(palette=palette, dither=Image.Dither.NONE))

    destination = ASSETS / "rexs-night-workshop.gif"
    frames[0].save(
        destination,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_MS,
        loop=0,
        optimize=True,
        disposal=1,
    )
    print(f"Saved {destination.name}: {destination.stat().st_size:,} bytes, 3.84-second loop")


if __name__ == "__main__":
    main()
