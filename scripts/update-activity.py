"""Build profile assets from public GitHub data. Python 3.10+ and Node.js 24."""
import argparse
from datetime import date, datetime, timedelta, timezone
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OWNER = "rexkarbu"
SNK_COMMIT = "a041d6c27ba561a39f5be9c26a784812765e434b"
# Git blob ID verified in the tree of the upstream commit above.
SNK_BLOBS = {
    "index.js": "a63c6275053d4d1252c310892bb8bf7ca9b375ab",
    "578.index.js": "336aa893d04eb8effb9b3cdfdfd98f3bf98dca48",
}
SNK_URL = f"https://raw.githubusercontent.com/Platane/snk/{SNK_COMMIT}/svg-only/dist/"
COLORS = ["#17243A", "#344943", "#5A7968", "#7F9F8B", "#9DB7A5"]
FILES = {"data.json", "github-stats.svg", "contribution-trail.svg", "contribution-trail-static.svg", "README.md"}
SVG_NS = "http://www.w3.org/2000/svg"


def fetch(url):
    headers = {"User-Agent": "rexkarbu-profile-assets", "Accept": "application/vnd.github+json"}
    # Authentication is limited to GitHub's public REST endpoints. The public
    # calendar and renderer never receive a token or authenticated profile page.
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=45) as response:
        if response.status != 200:
            raise ValueError(f"Unexpected HTTP status for {url}")
        return response.read()


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = {}
        self.tips = {}
        self.tip = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "td" and "data-date" in attrs and "data-level" in attrs:
            self.cells[attrs["id"]] = {"date": attrs["data-date"], "level": int(attrs["data-level"])}
        if tag == "tool-tip":
            self.tip = attrs.get("for")
            self.tips[self.tip] = ""

    def handle_data(self, data):
        if self.tip is not None:
            self.tips[self.tip] += data

    def handle_endtag(self, tag):
        if tag == "tool-tip":
            self.tip = None

    def days(self):
        result = []
        for cell_id, cell in self.cells.items():
            count = re.match(r"\s*(No|[\d,]+) contributions? on\b", self.tips.get(cell_id, ""))
            if not count:
                raise ValueError("GitHub calendar markup changed: missing contribution count")
            count = 0 if count[1] == "No" else int(count[1].replace(",", ""))
            result.append({**cell, "count": count})
        return sorted(result, key=lambda day: day["date"])


def collect():
    repos = {}
    page = 1
    while True:
        batch = json.loads(fetch(f"https://api.github.com/users/{OWNER}/repos?type=owner&per_page=100&page={page}"))
        if not isinstance(batch, list):
            raise ValueError("Expected a public repository list")
        for repo in batch:
            if repo["owner"]["login"] == OWNER and repo["private"] is False:
                repos[repo["id"]] = repo
        if len(batch) < 100:
            break
        page += 1
        if page > 100:
            raise ValueError("Unexpected repository pagination")
    calendar_url = f"https://github.com/users/{OWNER}/contributions"
    parser = CalendarParser()
    parser.feed(fetch(calendar_url).decode("utf-8"))
    days = parser.days()
    data = {
        "schema": 1,
        "owner": OWNER,
        "updated_utc": datetime.now(timezone.utc).date().isoformat(),
        "repositories": {
            "count": len(repos),
            "stars_received": sum(repo["stargazers_count"] for repo in repos.values()),
            "source": f"https://api.github.com/users/{OWNER}/repos",
            "scope": "All public repositories owned by rexkarbu, including forks and the profile repository",
        },
        "calendar": {"source": calendar_url, "days": days},
        "generator": {"name": "Platane/snk", "commit": SNK_COMMIT},
    }
    validate_data(data)
    return data


def validate_data(data):
    if data["schema"] != 1 or data["owner"] != OWNER:
        raise ValueError("Unexpected snapshot owner/schema")
    date.fromisoformat(data["updated_utc"])
    for value in (data["repositories"]["count"], data["repositories"]["stars_received"]):
        if type(value) is not int or value < 0:
            raise ValueError("Invalid repository metric")
    days = data["calendar"]["days"]
    if not 350 <= len(days) <= 371:
        raise ValueError("Expected approximately one year of calendar cells")
    previous = None
    for day in days:
        current = date.fromisoformat(day["date"])
        if previous is not None and current != previous + timedelta(days=1):
            raise ValueError("Calendar dates must be unique, ordered, and consecutive")
        if type(day["level"]) is not int or not 0 <= day["level"] <= 4:
            raise ValueError("Invalid contribution level")
        if type(day["count"]) is not int or day["count"] < 0 or (day["count"] == 0) != (day["level"] == 0):
            raise ValueError("Invalid contribution count/level")
        previous = current
    if days[-1]["date"] > data["updated_utc"]:
        raise ValueError("Calendar extends beyond its snapshot date")


def stats_svg(data):
    repos = data["repositories"]
    return f'''<svg xmlns="{SVG_NS}" width="480" height="148" viewBox="0 0 480 148" role="img" aria-labelledby="title desc">
<title id="title">Rex's public repository snapshot</title>
<desc id="desc">{repos['count']} public repositories and {repos['stars_received']} stars received. Updated {data['updated_utc']} UTC.</desc>
<rect width="480" height="148" rx="8" fill="#0D1117"/>
<path d="M20 20h6v6h-6zm9 0h6v6h-6z" fill="#E5B567"/>
<text x="46" y="27" fill="#9DB7A5" font-family="monospace" font-size="13">GITHUB / PUBLIC SNAPSHOT</text>
<path d="M240 48v56" stroke="#17243A" stroke-width="2"/>
<g font-family="sans-serif" fill="#E6EDF3" font-size="34" font-weight="600">
<text x="24" y="82">{repos['count']}</text><text x="264" y="82">{repos['stars_received']}</text></g>
<g font-family="sans-serif" fill="#9DB7A5" font-size="15">
<text x="24" y="105">Public repositories</text><text x="264" y="105">Stars received</text></g>
<text x="24" y="131" fill="#E6EDF3" font-family="monospace" font-size="12">Updated {data['updated_utc']} UTC</text>
</svg>\n'''


def static_trail(data):
    days = data["calendar"]["days"]
    first = date.fromisoformat(days[0]["date"])
    origin = first - timedelta(days=(first.weekday() + 1) % 7)
    width = ((date.fromisoformat(days[-1]["date"]) - origin).days // 7 + 3) * 16
    parts = [f'<svg xmlns="{SVG_NS}" width="{width}" height="192" viewBox="-16 -32 {width} 192" role="img">',
             f'<title>Static GitHub contribution calendar for Rex, {days[0]["date"]} to {days[-1]["date"]}</title>',
             f'<rect x="-16" y="-32" width="{width}" height="192" fill="#0D1117"/>']
    for day in days:
        current = date.fromisoformat(day["date"])
        x = (current - origin).days // 7 * 16 + 2
        y = (current.weekday() + 1) % 7 * 16 + 2
        parts.append(f'<rect x="{x}" y="{y}" width="12" height="12" rx="2" fill="{COLORS[day["level"]]}"><title>{day["date"]}: {day["count"]} contributions</title></rect>')
    parts.append('<path d="M2-16h12v12H2zm16 0h12v12H18zm16 0h12v12H34zm16 0h12v12H50z" fill="#E5B567"/>')
    return "\n".join(parts + ["</svg>\n"])


def snapshot_readme(data):
    repos, days = data["repositories"], data["calendar"]["days"]
    total = sum(day["count"] for day in days)
    active = sum(day["count"] > 0 for day in days)
    return f'''# GitHub activity snapshot

Updated **{data['updated_utc']} (UTC)**. These files show the last successful refresh, not a live feed.

## Public repositories

- **{repos['count']} public repositories** owned by rexkarbu, including forks and this profile repository.
- **{repos['stars_received']} stars received** across those repositories.
- Source: [GitHub's public repository API]({repos['source']}). All result pages are included; private repositories are excluded. This snapshot covers the account, independently of the three featured projects. Stars are a repository metric, not a skill rating.

## Contribution calendar

Period: **{days[0]['date']} through {days[-1]['date']}**, inclusive. The calendar contains **{total} contributions across {active} active days**.

Source: [the publicly visible GitHub contribution calendar]({data['calendar']['source']}). GitHub defines which activity appears here. If the account opts to expose anonymous private-contribution counts, the public calendar may include those counts; no private repository names or contents are collected.

[View the static calendar](contribution-trail-static.svg) · [View the animation](contribution-trail.svg) · [Machine-readable snapshot](data.json)

The snake is a decorative traversal of the real calendar, not a timeline of individual coding sessions. Colors represent GitHub's contribution intensity levels. Reduced motion selects the static calendar.

Rendered with [Platane/snk at the pinned commit](https://github.com/Platane/snk/tree/{SNK_COMMIT}), using a local adapter for the saved public calendar. The same dates, counts, and levels feed both views.

See [profile maintenance](../../docs/profile-maintenance.md) for refresh commands and failure recovery.
'''


def validate_folder(folder):
    if {path.name for path in folder.iterdir()} != FILES:
        raise ValueError("Activity output must contain exactly the five expected files")
    for name in FILES:
        path = folder / name
        if not path.is_file() or path.is_symlink() or not 0 < path.stat().st_size < 2_000_000:
            raise ValueError(f"Invalid output file: {name}")
    validate_data(json.loads((folder / "data.json").read_text(encoding="utf-8")))
    for path in folder.glob("*.svg"):
        document = ET.parse(path)
        if document.getroot().tag != f"{{{SVG_NS}}}svg":
            raise ValueError("Invalid SVG root")
        for element in document.iter():
            if element.tag.split("}")[-1] in {"script", "foreignObject", "image", "use"}:
                raise ValueError("Unexpected embedded/external SVG content")
            if any(key.lower().startswith("on") or key.split("}")[-1] == "href" for key in element.attrib):
                raise ValueError("Unexpected SVG event or external reference")
        content = path.read_text(encoding="utf-8")
        if "url(" in content.lower():
            raise ValueError("Unexpected SVG CSS resource")
        if path.name.endswith("-static.svg") and ("<style" in content or "<animate" in content):
            raise ValueError("Static SVG contains animation")
    if "@keyframes" not in (folder / "contribution-trail.svg").read_text(encoding="utf-8"):
        raise ValueError("Contribution animation was not generated")


def install(source, destination):
    validate_folder(source)
    destination.mkdir(parents=True, exist_ok=True)
    # Run all network, rendering, and validation work before replacing any asset.
    for name in sorted(FILES):
        shutil.copyfile(source / name, destination / name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "assets/activity")
    parser.add_argument("--snapshot", type=Path, help="Reuse saved public data without fetching fresh metrics")
    parser.add_argument("--bundle-dir", type=Path, help="Directory containing cached index.js and 578.index.js; hashes are still verified")
    parser.add_argument("--validate", type=Path, help="Validate an existing output directory without networking")
    parser.add_argument("--install", type=Path, help="Install a complete validated output directory locally")
    args = parser.parse_args()
    if args.validate:
        validate_folder(args.validate)
        print("Activity assets validated")
        return
    if args.install:
        install(args.install, args.output)
        print("Validated assets installed locally")
        return
    data = json.loads(args.snapshot.read_text(encoding="utf-8")) if args.snapshot else collect()
    validate_data(data)
    with tempfile.TemporaryDirectory(prefix="rex-profile-") as temp:
        temp = Path(temp)
        stage = temp / "output"
        stage.mkdir()
        for name, expected_hash in SNK_BLOBS.items():
            bundle_bytes = (args.bundle_dir / name).read_bytes() if args.bundle_dir else fetch(SNK_URL + name)
            blob = b"blob " + str(len(bundle_bytes)).encode() + b"\0" + bundle_bytes
            if hashlib.sha1(blob).hexdigest() != expected_hash:
                raise ValueError(f"Upstream {name} failed the pinned Git blob integrity check")
            (temp / name).write_bytes(bundle_bytes)
        bundle = temp / "index.js"
        (stage / "data.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        subprocess.run(["node", str(ROOT / "scripts/render-trail.cjs"), str(stage / "data.json"), str(bundle), str(stage / "contribution-trail.svg")], check=True, timeout=180)
        trail = stage / "contribution-trail.svg"
        svg = trail.read_text(encoding="utf-8")
        # Keep upstream animation intact; add an opaque workshop-colored backdrop.
        viewbox = re.search(r'viewBox="([^"]+)"', svg)
        if not viewbox:
            raise ValueError("Missing SVG viewBox")
        x, y, width, height = map(float, viewbox[1].split())
        svg = svg.replace("</desc>", f'</desc><rect x="{x:g}" y="{y:g}" width="{width:g}" height="{height:g}" fill="#0D1117"/>', 1)
        trail.write_text(svg + "\n", encoding="utf-8")
        (stage / "github-stats.svg").write_text(stats_svg(data), encoding="utf-8")
        (stage / "contribution-trail-static.svg").write_text(static_trail(data), encoding="utf-8")
        (stage / "README.md").write_text(snapshot_readme(data), encoding="utf-8")
        install(stage, args.output)
    print(f"Activity assets updated: {args.output}")


if __name__ == "__main__":
    main()
