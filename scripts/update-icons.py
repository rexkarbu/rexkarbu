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
    d = escape(paths[0].attrib["d"], quote=True)
    title = ICONS[slug]

    # 48x48 modern squircle badge with dark background, subtle border, and brand artwork
    if slug == "nextdotjs":
        inner = f'<circle cx="12" cy="12" r="11.5" fill="#FFFFFF"/><path d="{d}" fill="#000000"/>'
    elif slug == "typescript":
        inner = f'<rect width="24" height="24" rx="2" fill="#FFFFFF"/><path d="{d}" fill="#3178C6"/>'
    elif slug == "javascript":
        inner = f'<rect width="24" height="24" fill="#000000"/><path d="{d}" fill="#F7DF1E"/>'
    elif slug == "react":
        inner = f'<path d="{d}" fill="#61DAFB"/>'
    elif slug == "electron":
        inner = f'<path d="{d}" fill="#9FEAF9"/>'
    elif slug == "vite":
        inner = f'<path d="{d}" fill="#BD34FE"/>'

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48" role="img" aria-label="{title}">\n'
        f'  <title>{title}</title>\n'
        f'  <rect width="48" height="48" rx="11" fill="#161B22" stroke="#30363D" stroke-width="1"/>\n'
        f'  <g transform="translate(10 10) scale(1.166667)">\n'
        f'    {inner}\n'
        f'  </g>\n'
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
