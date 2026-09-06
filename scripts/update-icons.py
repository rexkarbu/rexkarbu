"""Generate consistent pixel-styled tool tiles from pinned Simple Icons. Stdlib only."""
from concurrent.futures import ThreadPoolExecutor
from html import escape
import json
from pathlib import Path
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

COMMIT = "9ddef18c4247eab3819ec280f07cb8e95dc2a274"  # Simple Icons 16.13.0
BASE = f"https://raw.githubusercontent.com/simple-icons/simple-icons/{COMMIT}/"
ICONS = {
    "typescript": "TypeScript",
    "javascript": "JavaScript",
    "react": "React",
    "nextdotjs": "Next.js",
    "electron": "Electron",
    "vite": "Vite",
}
OUT = Path(__file__).resolve().parents[1] / "assets/icons"
RAW = OUT / "raw"


def fetch(file):
    url = file if file.startswith("https://") else BASE + file
    with urlopen(Request(url, headers={"User-Agent": "rexkarbu-profile-icons"}), timeout=30) as response:
        return response.read().decode("utf-8")


def get_raw_svg(slug):
    raw_path = RAW / f"{slug}.svg"
    if raw_path.is_file():
        return raw_path.read_text(encoding="utf-8")
    content = fetch(f"icons/{slug}.svg")
    RAW.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(content, encoding="utf-8")
    return content


def tile(slug, raw_svg):
    source = ET.fromstring(raw_svg)
    paths = source.findall("{http://www.w3.org/2000/svg}path")
    if not paths or source.attrib.get("viewBox") != "0 0 24 24":
        raise ValueError(f"Unexpected source SVG for {slug}")
    shapes = "".join(f'<path d="{escape(p.attrib["d"], quote=True)}"/>' for p in paths)
    title = ICONS[slug]
    color = "#E6EDF3" if slug == "nextdotjs" else "#9DB7A5"

    # 80x88 tile with pixel-cut corners (4px chamfer), midnight blue background,
    # thin sage border, centered amber accent, 34px logo, and legible tech label.
    border_path = "M 4 0.5 L 76 0.5 L 79.5 4 L 79.5 84 L 76 87.5 L 4 87.5 L 0.5 84 L 0.5 4 Z"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="80" height="88" viewBox="0 0 80 88" role="img" aria-label="{title}">\n'
        f'  <title>{title}</title>\n'
        f'  <path d="{border_path}" fill="#17243A" stroke="#9DB7A5" stroke-width="1"/>\n'
        f'  <rect x="36" y="4" width="8" height="2" fill="#E5B567"/>\n'
        f'  <g transform="translate(23 15) scale(1.416667)" fill="{color}">\n'
        f'    {shapes}\n'
        f'  </g>\n'
        f'  <text x="40" y="72" text-anchor="middle" fill="#E6EDF3" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, Helvetica, Arial, sans-serif" font-size="10.5" font-weight="500">{title}</text>\n'
        f'</svg>\n'
    )


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=6) as pool:
        raw_svgs = dict(zip(ICONS, pool.map(get_raw_svg, ICONS)))

    tiles = {slug: tile(slug, raw_svgs[slug]) for slug in ICONS}

    try:
        metadata = json.loads(fetch("data/simple-icons.json"))
        selected = [entry for entry in metadata if entry["title"] in ICONS.values()]
        license_text = fetch("LICENSE.md")
        js_license = fetch("https://raw.githubusercontent.com/voodootikigod/logo.js/1544bdeed6d618a6cfe4f0650d04ab8d9cfa76d9/LICENSE")
        (OUT / "LICENSE.md").write_text(license_text, encoding="utf-8")
        (OUT / "JAVASCRIPT-LICENSE.txt").write_text(js_license, encoding="utf-8")
        sources = {
            "collection": "Simple Icons",
            "version": "16.13.0",
            "commit": COMMIT,
            "collection_license": "CC0-1.0",
            "icons": selected,
        }
        (OUT / "sources.json").write_text(json.dumps(sources, indent=2) + "\n", encoding="utf-8")
    except Exception as err:
        print(f"Notice: using cached metadata/license ({err})")

    for slug, image in tiles.items():
        (OUT / f"{slug}.svg").write_text(image, encoding="utf-8")
    print("Saved raw icons, rendered six local tool tiles, and updated metadata")


if __name__ == "__main__":
    main()
