#!/usr/bin/env python3
"""Port Shopify CMS pages to Astro pages for klovo.com."""
import json
import os
import re
from pathlib import Path

SOURCE = "/Users/sohamkhaitan/.claude/projects/-Users-sohamkhaitan-Library-CloudStorage-GoogleDrive-soham-khaitan-doorkraft-com-My-Drive-Claude-s-Folder-Website/4bf37981-7e33-4d06-bd58-47eaee758480/tool-results/toolu_016gdeHALFXWyxBzLbXzgRvt.json"
OUT_DIR = Path("/Users/sohamkhaitan/Library/CloudStorage/GoogleDrive-soham.khaitan@doorkraft.com/My Drive/Claude's Folder/Website/klovo-website/src/pages/pages")

HANDLES = [
    "garage-cabinets",
    "custom-garage-cabinets",
    "diy-garage-cabinets",
    "laundry-room-cabinets",
    "entryway-cabinets",
    "garage-organization-systems",
    "glidelock-assembly",
    "terms-of-service",
    "shipping-and-returns",
    "data-sharing-opt-out",
    "warranties-map-trade-partner-policies-clikclosets-trade-info",
]

TAG_RE = re.compile(r"<(p|h[1-6]|ul|ol|li|div|span|br|a|table|tr|td|th|strong|em|img|section|article)\b", re.I)

def looks_like_html(s: str) -> bool:
    return bool(TAG_RE.search(s or ""))

def strip_html(s: str) -> str:
    s = re.sub(r"\\([\\`*_{}\[\]()#+\-.!~|<>])", r"\1", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"&nbsp;", " ", s)
    s = re.sub(r"&amp;", "&", s)
    s = re.sub(r"&quot;", '"', s)
    s = re.sub(r"&#39;", "'", s)
    s = re.sub(r"&lt;", "<", s)
    s = re.sub(r"&gt;", ">", s)
    # Strip markdown syntax for descriptions
    s = re.sub(r"^#{1,6}\s+", "", s, flags=re.M)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"(?<!\w)_([^_\n]+)_(?!\w)", r"\1", s)
    s = re.sub(r"^\s*[-*]\s+", "", s, flags=re.M)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def make_description(body: str, title: str, limit: int = 155) -> str:
    text = strip_html(body) if body else ""
    if not text:
        return title
    if len(text) <= limit:
        return text
    cut = text[:limit]
    sp = cut.rfind(" ")
    if sp > 40:
        cut = cut[:sp]
    return cut.rstrip(",.;:-") + "..."

def rewrite_urls(s: str) -> str:
    s = s.replace("https://klovo.com/", "/")
    s = s.replace("http://klovo.com/", "/")
    s = s.replace("https://1zchxb-wz.myshopify.com/", "/")
    s = s.replace("http://1zchxb-wz.myshopify.com/", "/")
    return s

def _inline_md(s: str) -> str:
    # [text](url)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    # **bold**
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    # _italic_ (only when flanked by non-word on one side)
    s = re.sub(r"(?<!\w)_([^_\n]+)_(?!\w)", r"<em>\1</em>", s)
    return s

def plaintext_to_html(body: str) -> str:
    paras = re.split(r"\n\s*\n", body.strip())
    html_parts = []
    for p in paras:
        p = p.strip()
        if not p:
            continue
        # Horizontal rule
        if re.fullmatch(r"-{3,}", p):
            continue
        # Heading paragraph: starts with # markers. Split heading title from remainder.
        m_h = re.match(r"^(#{1,6})\s+(.+)$", p, re.S)
        if m_h:
            level = len(m_h.group(1))
            rest = m_h.group(2).strip()
            # First "line" of the heading — up to newline or first sentence-ending period
            mline = re.match(r"^([^\n.?!]+[.?!]?)(?:\s+(.*))?$", rest, re.S)
            if mline:
                title_txt = mline.group(1).strip().rstrip(".")
                remainder = (mline.group(2) or "").strip()
            else:
                title_txt = rest
                remainder = ""
            hlevel = min(level + 1, 6)
            html_parts.append(f"<h{hlevel}>{_inline_md(title_txt)}</h{hlevel}>")
            if remainder:
                html_parts.append(f"<p>{_inline_md(remainder)}</p>")
            continue
        lines = p.split("\n")
        # List block: all lines start with - or * or number.
        if all(re.match(r"^\s*([-*]|\d+\.)\s+", ln) for ln in lines):
            ordered = bool(re.match(r"^\s*\d+\.\s+", lines[0]))
            tag = "ol" if ordered else "ul"
            items = []
            for ln in lines:
                item = re.sub(r"^\s*([-*]|\d+\.)\s+", "", ln)
                items.append(f"<li>{_inline_md(item)}</li>")
            html_parts.append(f"<{tag}>" + "".join(items) + f"</{tag}>")
            continue
        # Mixed: join with <br>
        joined = "<br>".join(_inline_md(ln) for ln in lines)
        html_parts.append(f"<p>{joined}</p>")
    return "\n".join(html_parts)

def escape_for_template_literal(s: str) -> str:
    # Order matters: backslash first, then backtick, then ${
    s = s.replace("\\", "\\\\")
    s = s.replace("`", "\\`")
    s = s.replace("${", "\\${")
    return s

def escape_js_string_dq(s: str) -> str:
    s = s.replace("\\", "\\\\")
    s = s.replace('"', "&quot;")
    return s

def unescape_md(s: str) -> str:
    # Unescape common backslash-escaped markdown chars seen in source data
    return re.sub(r"\\([\\`*_{}\[\]()#+\-.!~|<>])", r"\1", s)

def looks_like_single_line_md(s: str) -> bool:
    # If few newlines but many markdown heading markers, it's mangled md on one line
    lines = s.count("\n")
    hashes = len(re.findall(r"(?:^|\s)#{2,4}\s+", s))
    return lines < 3 and hashes >= 2

def resplit_single_line_md(s: str) -> str:
    # Strip stray "-##" bullet-header combos that appear in mangled source
    s = re.sub(r"\|\s*-#{1,6}\s+", " ## ", s)
    s = re.sub(r"(?<=\s)-(?=#{1,6}\s+)", "", s)
    # Insert double newlines before markdown headings and horizontal rules
    s = re.sub(r"\s+(?=#{1,6}\s+)", "\n\n", s)
    s = re.sub(r"\s+---\s+", "\n\n", s)
    # Break before bullet lists
    s = re.sub(r"(?<=[.!?])\s+(?=-\s+\*\*)", "\n\n", s)
    return s

def build_body_html(body: str) -> str:
    if not body or not body.strip():
        return '<p>This page is coming soon. <a href="/contact">Contact us</a> for info.</p>'
    body = unescape_md(body)
    body = rewrite_urls(body)
    if looks_like_html(body):
        return body
    body = resplit_single_line_md(body)
    return plaintext_to_html(body)

TEMPLATE = """---
import BaseLayout from '../../layouts/BaseLayout.astro';

const title = "{title}";
const description = "{description}";
---

<BaseLayout title={{title}} description={{description}}>
  <article class="max-w-3xl mx-auto px-4 sm:px-6 py-12">
    <h1 class="text-3xl sm:text-4xl font-bold mb-8">{{title}}</h1>
    <div class="prose prose-lg max-w-none shopify-body" set:html={{`{body}`}} />
  </article>
</BaseLayout>

<style is:global>
  .shopify-body h2 {{ font-size: 1.75rem; font-weight: 700; margin-top: 2rem; margin-bottom: 1rem; }}
  .shopify-body h3 {{ font-size: 1.35rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.75rem; }}
  .shopify-body p {{ margin-bottom: 1rem; line-height: 1.75; }}
  .shopify-body ul, .shopify-body ol {{ margin-left: 1.5rem; margin-bottom: 1rem; }}
  .shopify-body ul {{ list-style: disc; }}
  .shopify-body ol {{ list-style: decimal; }}
  .shopify-body li {{ margin-bottom: 0.35rem; }}
  .shopify-body a {{ color: #0057ff; text-decoration: underline; }}
  .shopify-body table {{ width: 100%; border-collapse: collapse; margin: 1.5rem 0; }}
  .shopify-body th, .shopify-body td {{ border: 1px solid #e5e7eb; padding: 0.5rem 0.75rem; text-align: left; }}
  .shopify-body th {{ background: #f9fafb; font-weight: 600; }}
</style>
"""

def main():
    with open(SOURCE, "r") as f:
        outer = json.load(f)
    if isinstance(outer, list):
        text = outer[0]["text"]
    else:
        text = outer["text"]
    data = json.loads(text)
    results = data["results"]
    by_handle = {r["handle"]: r for r in results}

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    report = []
    for handle in HANDLES:
        page = by_handle.get(handle)
        if not page:
            report.append((handle, "MISSING", 0))
            continue
        title = page.get("title") or handle
        body = page.get("body") or ""
        if not body.strip():
            btype = "empty"
        elif looks_like_html(body):
            btype = "html"
        else:
            btype = "plaintext"

        body_html = build_body_html(body)
        body_escaped = escape_for_template_literal(body_html)
        description = make_description(body, title)

        out = TEMPLATE.format(
            title=escape_js_string_dq(title),
            description=escape_js_string_dq(description),
            body=body_escaped,
        )
        (OUT_DIR / f"{handle}.astro").write_text(out)
        report.append((handle, btype, len(body)))

    print("\nReport:")
    for h, t, n in report:
        print(f"  {h}: {t} ({n} chars)")

if __name__ == "__main__":
    main()
