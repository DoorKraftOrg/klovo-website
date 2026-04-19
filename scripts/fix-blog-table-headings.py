#!/usr/bin/env python3
"""Fix blog markdown where headings are mashed with tables or paragraphs on one line.

Symptoms found after the Shopify port:
  "## Quick comparison table | Rank | Brand | ...."
  "| 10 | Monkey Bars | ... | Lifetime | ## Which should you buy?"
  "... | text. ### Interlocking Tiles"

Splits each case onto its own line with a blank line between heading and content.
Idempotent: running again does nothing once the pattern is absent.
"""
import re
import sys
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / "src" / "content" / "blog"

# Heading followed by pipe-table on same line: "## Title | a | b |"
RE_HEAD_TABLE = re.compile(r"^(#{1,6}\s+[^\n|]+?)\s+(\|[^\n]*\|\s*)$", re.MULTILINE)
# Table row (or any line) followed by a new heading: "... | text | ## Next"
RE_INLINE_HEAD = re.compile(r"([^\n])\s+(#{2,6}\s+)")


def fix(content: str) -> tuple[str, int]:
    changes = 0

    # 1) Split heading mashed with table header.
    def _split_head_table(m):
        nonlocal changes
        changes += 1
        return f"{m.group(1)}\n\n{m.group(2)}"

    content = RE_HEAD_TABLE.sub(_split_head_table, content)

    # 2) Walk line-by-line to split trailing "## Heading" off the end of any line.
    out_lines = []
    for line in content.split("\n"):
        # Skip YAML front-matter lines and fenced code markers untouched.
        if line.startswith("---") or line.startswith("```"):
            out_lines.append(line)
            continue
        # Only process if a heading marker appears mid-line, not at start.
        m = re.search(r"\s(#{2,6}\s[^\n]+)$", line)
        if m and not line.lstrip().startswith("#"):
            head = m.group(1)
            before = line[: m.start()].rstrip()
            out_lines.append(before)
            out_lines.append("")
            out_lines.append(head)
            changes += 1
        else:
            out_lines.append(line)
    content = "\n".join(out_lines)

    # 3) Ensure a blank line between a pipe-table block and a following heading.
    content = re.sub(r"(\|\s*)\n(#{2,6}\s)", r"\1\n\n\2", content)

    return content, changes


def main():
    total_files = 0
    total_changes = 0
    for md in sorted(BLOG_DIR.glob("*.md")):
        original = md.read_text()
        fixed, n = fix(original)
        if fixed != original:
            md.write_text(fixed)
            total_files += 1
            total_changes += n
            print(f"  {md.name}: {n} fixes")
    print(f"\nTotal: {total_files} files, {total_changes} edits")
    return 0


if __name__ == "__main__":
    sys.exit(main())
