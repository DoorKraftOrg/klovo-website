#!/usr/bin/env python3
"""
Normalize blog + ported Shopify page copy so it matches the canonical
hand-authored live pages on klovo.com.

Scope:
  - src/content/blog/*.md          (ported Shopify blog posts)
  - src/pages/pages/*.astro        (ported Shopify pages)

Explicitly OUT of scope (source of truth — never touched):
  - src/pages/assembly.astro
  - src/pages/faq.astro
  - src/pages/index.astro
  - src/pages/sets/[slug].astro
  - src/content/sets/*.md

What this script enforces:
  1. Assembly time: "90 seconds" (as a whole-cabinet assembly claim) -> "2–3 minutes".
     We do NOT touch:
       - competitor assembly times (e.g. "45-90 minutes", "30-90 minutes")
       - frontmatter `canonical:` URLs (which contain "take-90-seconds" in slugs)
       - file paths / blog slug references (URLs with "90-seconds" are kept)
  2. "Clik" dead term -> should not appear. We only report; no replacements performed.
  3. Tool-free: we keep "almost tool-free" and "tool-free" phrasings that already exist.
     We do NOT rewrite "no tools required" / "zero tools" en masse here — those are
     tonally acceptable in many existing sentences; the canonical language guide
     permits "the only tool you'll need is a screwdriver for the back panel" as an
     alternative. Heavy rewrites on that front are left for a separate copy pass.

The script is idempotent: running it twice yields no additional changes.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT / "src" / "content" / "blog"
PAGES_DIR = ROOT / "src" / "pages" / "pages"

# --- Assembly time replacement rules (ordered; earlier rules win) -----------
# Each rule: (compiled regex, replacement, category)
# We match "90 seconds" only in KLOVO / whole-cabinet contexts. Competitor
# ranges like "45-90 minutes" are naturally safe because they use "minutes",
# not "seconds".

ASSEMBLY_RULES: list[tuple[re.Pattern[str], str, str]] = [
    # Headings / H2 / titles — "90-Second" and "90 Second"
    (re.compile(r"\b90[- ]Second Assembly\b"), "2–3 Minute Assembly", "assembly-time"),
    (re.compile(r"\b90[- ]Second Cabinet Assembly\b"), "2–3 Minute Cabinet Assembly", "assembly-time"),
    (re.compile(r"\b90[- ]Second DIY Assembly\b"), "2–3 Minute DIY Assembly", "assembly-time"),
    (re.compile(r"\b90[- ]Second GlideLock Assembly\b"), "2–3 Minute GlideLock Assembly", "assembly-time"),
    (re.compile(r"\b90[- ]second GlideLock assembly\b"), "2–3 minute GlideLock assembly", "assembly-time"),
    (re.compile(r"\b90[- ]second assembly\b"), "2–3 minute assembly", "assembly-time"),
    (re.compile(r"\b90[- ]Second Assembly\b"), "2–3 Minute Assembly", "assembly-time"),

    # Title case "90 Seconds" as section header
    (re.compile(r"\bTake 90 Seconds\b"), "Take 2–3 Minutes", "assembly-time"),
    (re.compile(r"\b90 Seconds vs\."), "2–3 Minutes vs.", "assembly-time"),

    # Loose hyphenated forms: "90-second DIY assembly", "90-second carcass assembly", etc.
    (re.compile(r"\b90[- ]second DIY assembly\b"), "2–3 minute DIY assembly", "assembly-time"),
    (re.compile(r"\b90[- ]second carcass assembly\b"), "2–3 minute carcass assembly", "assembly-time"),
    (re.compile(r"\b90[- ]second cabinet assembly\b", re.I), "2–3 minute cabinet assembly", "assembly-time"),

    # Table cell style: "~90 seconds", "\~90 seconds", "~90 sec"
    (re.compile(r"\\?~\s*90 seconds? per cabinet"), "~2–3 minutes per cabinet", "assembly-time"),
    (re.compile(r"\\?~\s*90 seconds?\b"), "~2–3 minutes", "assembly-time"),
    (re.compile(r"\\?~\s*90 sec(?!ond)\b"), "~2–3 min", "assembly-time"),

    # Common sentence forms
    (re.compile(r"in about 90 seconds"), "in about 2–3 minutes", "assembly-time"),
    (re.compile(r"in approximately 90 seconds"), "in approximately 2–3 minutes", "assembly-time"),
    (re.compile(r"approximately 90 seconds"), "approximately 2–3 minutes", "assembly-time"),
    (re.compile(r"in roughly 90 seconds"), "in roughly 2–3 minutes", "assembly-time"),
    (re.compile(r"roughly 90 seconds"), "roughly 2–3 minutes", "assembly-time"),
    (re.compile(r"in under 90 seconds"), "in about 2–3 minutes", "assembly-time"),
    (re.compile(r"under 90 seconds"), "about 2–3 minutes", "assembly-time"),
    (re.compile(r"in 90 seconds"), "in 2–3 minutes", "assembly-time"),
    (re.compile(r"Ninety seconds\b"), "Two to three minutes", "assembly-time"),

    # "90 seconds per cabinet" / "per shelf"
    (re.compile(r"\b90 seconds per cabinet\b"), "2–3 minutes per cabinet", "assembly-time"),
    (re.compile(r"\b90 seconds per shelf\b"), "2–3 minutes per cabinet", "assembly-time"),
    (re.compile(r"\b90 seconds each\b"), "2–3 minutes each", "assembly-time"),
    (re.compile(r"\b90 seconds/cabinet\b"), "2–3 minutes/cabinet", "assembly-time"),
    (re.compile(r"\b90 seconds to 5 minutes per cabinet\b"), "2–3 minutes per cabinet", "assembly-time"),

    # Comparison table cells like "90 seconds (GlideLock...)"
    (re.compile(r"\b90 seconds \(GlideLock"), "2–3 minutes (GlideLock", "assembly-time"),

    # Final catch-all: standalone "90 seconds" when it clearly means whole-cabinet time.
    # We restrict this to lines NOT containing "45" or "30-90" etc. by requiring
    # that the phrase isn't preceded by "-" or a digit-range marker.
    (re.compile(r"(?<![-0-9])\b90 seconds\b(?! to \d)"), "2–3 minutes", "assembly-time"),
]


def is_source_of_truth(path: Path) -> bool:
    """These files are canonical; never modify."""
    rel = path.relative_to(ROOT).as_posix()
    if rel in {
        "src/pages/assembly.astro",
        "src/pages/faq.astro",
        "src/pages/index.astro",
    }:
        return True
    if rel.startswith("src/pages/sets/") and rel.endswith(".astro"):
        return True
    if rel.startswith("src/content/sets/"):
        return True
    return False


def protect_canonical_and_urls(text: str) -> tuple[str, list[str]]:
    """
    Replace canonical URLs, markdown links, and href attributes that contain
    '90-seconds' with sentinel placeholders so the regex pass doesn't mangle them.
    Returns (protected_text, stash) where stash[i] is original for sentinel __PROT_i__.
    """
    stash: list[str] = []

    def stash_match(m: re.Match[str]) -> str:
        stash.append(m.group(0))
        return f"__PROT_{len(stash) - 1}__"

    # Protect frontmatter canonical: "...take-90-seconds..." lines
    text = re.sub(
        r'(?m)^canonical:\s*"[^"]*"',
        stash_match,
        text,
    )
    # Protect markdown links containing 90-seconds in URL: (/path/...-90-seconds...)
    text = re.sub(
        r"\(/[^)]*90-seconds[^)]*\)",
        stash_match,
        text,
    )
    # Protect href attributes with 90-seconds in URL
    text = re.sub(
        r'href="[^"]*90-seconds[^"]*"',
        stash_match,
        text,
    )
    # Protect raw slug references (e.g., blogs/.../glidelock-...-take-90-seconds...)
    text = re.sub(
        r"\b[a-z0-9/\-]*-take-90-seconds(?:-[a-z0-9]+)?\b",
        stash_match,
        text,
    )
    return text, stash


def restore_protected(text: str, stash: list[str]) -> str:
    for i, original in enumerate(stash):
        text = text.replace(f"__PROT_{i}__", original)
    return text


def normalize(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {"assembly-time": 0, "tool-free": 0, "Clik": 0, "other": 0}
    protected, stash = protect_canonical_and_urls(text)

    for pattern, repl, category in ASSEMBLY_RULES:
        def sub_fn(m: re.Match[str], _repl: str = repl, _cat: str = category) -> str:
            counts[_cat] += 1
            return _repl
        protected = pattern.sub(sub_fn, protected)

    # Clik check (report-only; canonical says it shouldn't appear at all)
    for _ in re.finditer(r"\bClik\b", protected):
        counts["Clik"] += 1

    restored = restore_protected(protected, stash)
    return restored, counts


def process_file(path: Path, totals: dict[str, int], modified_files: dict[str, list[str]]) -> None:
    if is_source_of_truth(path):
        return
    original = path.read_text(encoding="utf-8")
    new_text, counts = normalize(original)
    changed = sum(v for k, v in counts.items() if k != "Clik") > 0 and new_text != original
    for k, v in counts.items():
        totals[k] = totals.get(k, 0) + v
    if changed:
        path.write_text(new_text, encoding="utf-8")
        bucket = "blog" if "content/blog" in path.as_posix() else "pages"
        modified_files[bucket].append(path.relative_to(ROOT).as_posix())


def main() -> int:
    totals: dict[str, int] = {"assembly-time": 0, "tool-free": 0, "Clik": 0, "other": 0}
    modified: dict[str, list[str]] = {"blog": [], "pages": []}

    for md in sorted(BLOG_DIR.glob("*.md")):
        process_file(md, totals, modified)
    for astro in sorted(PAGES_DIR.glob("*.astro")):
        process_file(astro, totals, modified)

    print("=== Normalize Blog Copy — results ===")
    print(f"Blog files modified  ({len(modified['blog'])}):")
    for p in modified["blog"]:
        print(f"  - {p}")
    print(f"Page files modified  ({len(modified['pages'])}):")
    for p in modified["pages"]:
        print(f"  - {p}")
    print()
    print("Edit counts by category:")
    for k, v in totals.items():
        print(f"  {k:<15} {v}")
    if totals["Clik"] > 0:
        print("\nWARNING: 'Clik' appears somewhere in scope — investigate.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
