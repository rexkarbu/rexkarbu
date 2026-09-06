"""Refresh the six local tool icons from a pinned Simple Icons release. Stdlib only."""
from concurrent.futures import ThreadPoolExecutor
from html import escape
import json
from pathlib import Path
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

COMMIT = "9ddef18c4247eab3819ec280f07cb8e95dc2a274"  # Simple Icons 16.13.0
BASE = f"https://raw.githubusercontent.com/simple-icons/simple-icons/{COMMIT}/"
ICONS = {"typescript": "TypeScript", "javascript": "JavaScript", "react": "React",
         "nextdotjs": "Next.js", "electron": "Electron", "vite": "Vite"}
OUT = Path(__file__).resolve().parents[1] / "assets/icons"


def fetch(file):
    url = file if file.startswith("https://") else BASE + file
    with urlopen(Request(url, headers={"User-Agent": "rexkarbu-profile-icons"}), timeout=30) as response:
        return response.read().decode("utf-8")


def icon(slug):
    source = ET.fromstring(fetch(f"icons/{slug}.svg"))
    paths = source.findall("{http://www.w3.org/2000/svg}path")
    if not paths or source.attrib.get("viewBox") != "0 0 24 24":
        raise ValueError(f"Unexpected source SVG for {slug}")
    shapes = "".join(f'<path d="{escape(p.attrib["d"], quote=True)}"/>' for p in paths)
    # Original paths; only presentation color and a dark square are added.
    color = "#E6EDF3" if slug == "nextdotjs" else "#9DB7A5"
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 28 28" role="img"><title>{ICONS[slug]}</title><path fill="#0D1117" d="M0 0h28v28H0z"/><g transform="translate(3 3) scale(.916667)" fill="{color}">{shapes}</g></svg>\n'


def main():
    with ThreadPoolExecutor(max_workers=6) as pool:
        images = dict(zip(ICONS, pool.map(icon, ICONS)))
    metadata = json.loads(fetch("data/simple-icons.json"))
    selected = [entry for entry in metadata if entry["title"] in ICONS.values()]
    license_text = fetch("LICENSE.md")
    js_license = fetch("https://raw.githubusercontent.com/voodootikigod/logo.js/1544bdeed6d618a6cfe4f0650d04ab8d9cfa76d9/LICENSE")
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, image in images.items():
        (OUT / f"{slug}.svg").write_text(image, encoding="utf-8")
    (OUT / "LICENSE.md").write_text(license_text, encoding="utf-8")
    (OUT / "JAVASCRIPT-LICENSE.txt").write_text(js_license, encoding="utf-8")
    sources = {"collection": "Simple Icons", "version": "16.13.0", "commit": COMMIT,
               "collection_license": "CC0-1.0", "icons": selected}
    (OUT / "sources.json").write_text(json.dumps(sources, indent=2) + "\n", encoding="utf-8")
    print("Saved six local icons, collection license, and per-icon source metadata")


if __name__ == "__main__":
    main()
