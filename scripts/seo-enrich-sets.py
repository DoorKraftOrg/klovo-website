#!/usr/bin/env python3
"""
SEO enrichment for set markdown files.
- Adds upc field (after sku)
- Adds seoTitle field (after title) — short, keyword-rich
- Replaces '300 lb Shelves' → '500 lb Cabinet' in longTitle (brand standard)
- Replaces 'Fixed shelves hold 300 lbs each' → 'Each cabinet holds up to 500 lbs'
- Replaces 'Fixed shelves support 300 lbs each' → 'Each cabinet holds up to 500 lbs'

Idempotent — running twice does nothing the second time.
"""
import re
from pathlib import Path

CONTENT_DIR = Path(__file__).parent.parent / "src" / "content" / "sets"

# slug → (upc, seoTitle)
SETS = {
    "2ft-utility":              ("850085276094", "2 ft. Utility Modular Garage Cabinet Set"),
    "4ft-home-gym-locker":      ("850085276032", "4 ft. Home Gym Locker Modular Garage Cabinet Set"),
    "6ft-garage-desk":          ("850085276001", "6 ft. Garage Desk Modular Garage Cabinet Set"),
    "6ft-craft-bench":          ("850085276025", "6 ft. Craft Bench Modular Garage Cabinet Set"),
    "8ft-garage-office":        ("850085276018", "8 ft. Garage Office Modular Garage Cabinet Set"),
    "8ft-wfh-studio":           ("850085276087", "8 ft. WFH Studio Modular Garage Cabinet Set"),
    "8ft-garage-storage":       ("850085276063", "8 ft. Storage Modular Garage Cabinet Set"),
    "8ft-workshop":             ("850085276056", "8 ft. Workshop Modular Garage Cabinet Set"),
    "10ft-mudroom":             ("850085276131", "10 ft. Mudroom Modular Garage Cabinet Set"),
    "10ft-wfh-design-hero":     ("850085276117", "10 ft. Home Office Modular Garage Cabinet Set"),
    "10ft-home-gym-wall":       ("850085276049", "10 ft. Home Gym Wall Modular Garage Cabinet Set"),
    "10ft-pro-workshop":        ("850085276070", "10 ft. Pro Workshop Modular Garage Cabinet Set"),
    "12ft-family-mudroom":      ("850085276100", "12 ft. Family Mudroom Modular Garage Cabinet Set"),
    "14ft-command-center":      ("850085276124", "14 ft. Workshop + Storage Modular Garage Cabinet Set"),
    "15ft-two-car-garage-wall": ("850085276148", "15 ft. Two-Car Garage Wall Modular Cabinet Set"),
    "16ft-floor-to-ceiling":    ("850085276155", "16 ft. Floor-to-Ceiling Modular Garage Cabinet Set"),
}

REPLACEMENTS = [
    ("300 lb Shelves",                          "500 lb Cabinet"),
    ("Fixed shelves hold 300 lbs each",         "Each cabinet holds up to 500 lbs"),
    ("Fixed shelves support 300 lbs each",      "Each cabinet holds up to 500 lbs"),
]

def enrich_file(path: Path, upc: str, seo_title: str) -> dict:
    """Returns a dict of {action: count} describing what was done."""
    text = path.read_text()
    changes = {"upc_added": 0, "seoTitle_added": 0, "lb_replacements": 0}

    # Allow escaped quotes inside the YAML string: (?:[^"\\]|\\.)*
    line_pat = lambda key: rf'(^{key}: "(?:[^"\\]|\\.)*"\n)'

    # Add upc after sku line, if not present
    if "upc:" not in text:
        new_text, n = re.subn(line_pat("sku"), rf'\1upc: "{upc}"\n', text, count=1, flags=re.MULTILINE)
        if n == 1:
            text = new_text
            changes["upc_added"] = 1

    # Add seoTitle after title line, if not present
    if "seoTitle:" not in text:
        new_text, n = re.subn(line_pat("title"), rf'\1seoTitle: "{seo_title}"\n', text, count=1, flags=re.MULTILINE)
        if n == 1:
            text = new_text
            changes["seoTitle_added"] = 1

    # Run lb-related replacements anywhere in file
    for old, new in REPLACEMENTS:
        if old in text:
            count = text.count(old)
            text = text.replace(old, new)
            changes["lb_replacements"] += count

    path.write_text(text)
    return changes

def main():
    total = {"upc_added": 0, "seoTitle_added": 0, "lb_replacements": 0}
    for slug, (upc, seo_title) in SETS.items():
        path = CONTENT_DIR / f"{slug}.md"
        if not path.exists():
            print(f"  ! MISSING: {path}")
            continue
        c = enrich_file(path, upc, seo_title)
        bits = []
        if c["upc_added"]:        bits.append("upc")
        if c["seoTitle_added"]:   bits.append("seoTitle")
        if c["lb_replacements"]:  bits.append(f"{c['lb_replacements']}× lb-fix")
        print(f"  {slug:30s}  {' + '.join(bits) if bits else 'no-op'}")
        for k in total:
            total[k] += c[k]
    print(f"\nTotals: upc={total['upc_added']}, seoTitle={total['seoTitle_added']}, lb-replacements={total['lb_replacements']}")

if __name__ == "__main__":
    main()
