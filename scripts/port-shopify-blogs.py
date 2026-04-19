#!/usr/bin/env python3
"""Port Shopify blog articles into Astro content collection for klovo.com."""
import json
import os
import re
from urllib.parse import urlparse

SRC = "/Users/sohamkhaitan/.claude/projects/-Users-sohamkhaitan-Library-CloudStorage-GoogleDrive-soham-khaitan-doorkraft-com-My-Drive-Claude-s-Folder-Website/4bf37981-7e33-4d06-bd58-47eaee758480/tool-results/mcp-f06646b4-a207-46ca-9315-6334be97df91-shopify_api_request_beta-1776638693783.txt"
SITE = "/Users/sohamkhaitan/Library/CloudStorage/GoogleDrive-soham.khaitan@doorkraft.com/My Drive/Claude's Folder/Website/klovo-website"
BLOG_DIR = os.path.join(SITE, "src", "content", "blog")
MANIFEST = os.path.join(SITE, "scripts", "blog-image-manifest.json")

CANONICALS = {
    "klovo-vs-gladiator-garage-cabinets-an-honest-side-by-side-comparison-1": "https://www.klovo.com/blogs/news/klovo-vs-gladiator-garage-cabinets-an-honest-side-by-side-comparison",
    "klovo-vs-newage-products-premium-garage-cabinets-compared-1": "https://www.klovo.com/blogs/news/klovo-vs-newage-products-premium-garage-cabinets-compared",
    "the-true-cost-of-garage-cabinets-budget-breakdown-for-every-size": "https://www.klovo.com/blogs/news/true-cost-of-garage-cabinets-budget-breakdown",
    "glidelock-assembly-how-we-made-cabinet-assembly-take-90-seconds-1": "https://www.klovo.com/blogs/news/glidelock-assembly-how-we-made-cabinet-assembly-take-90-seconds",
    "garage-organization-systems-the-ultimate-buyers-guide-2026": "https://www.klovo.com/blogs/news/garage-organization-systems-ultimate-buyers-guide-2026",
    "entryway-mudroom-storage-solutions-that-actually-work-in-2027": "https://www.klovo.com/blogs/news/entryway-mudroom-storage-solutions-that-actually-work-in-2026",
    "laundry-room-cabinet-ideas-transform-your-space-on-a-budget-in-2027": "https://www.klovo.com/blogs/news/laundry-room-cabinet-ideas-transform-your-space-on-a-budget-in-2026",
    "custom-garage-cabinets-vs-pre-built-what-every-homeowner-should-know-2026-guide": "https://www.klovo.com/blogs/news/custom-garage-cabinets-vs-pre-built",
    "glidelock-assembly-how-klovo-made-garage-cabinet-assembly-take-90-seconds": "https://www.klovo.com/blogs/news/glidelock-assembly-how-we-made-cabinet-assembly-take-90-seconds",
}

def yaml_escape(s):
    if s is None:
        return ""
    # Strip control chars (except newline/tab, which we also strip for frontmatter strings)
    s = "".join(ch for ch in s if ch == " " or ch == "\t" or ch >= " ")
    s = s.replace("\t", " ")
    # escape backslash then quote
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return s

def strip_html(html):
    if not html:
        return ""
    # remove tags
    text = re.sub(r"<[^>]+>", " ", html)
    # unescape common entities
    text = (text.replace("&nbsp;", " ")
                .replace("&amp;", "&")
                .replace("&quot;", '"')
                .replace("&#39;", "'")
                .replace("&apos;", "'")
                .replace("&lt;", "<")
                .replace("&gt;", ">"))
    text = re.sub(r"\s+", " ", text).strip()
    return text

def make_description(summary, body):
    if summary and summary.strip():
        return summary.strip()
    txt = strip_html(body)
    if len(txt) <= 150:
        return txt
    cut = txt[:150]
    # end on word boundary
    sp = cut.rfind(" ")
    if sp > 80:
        cut = cut[:sp]
    return cut.rstrip(" ,.;:-") + "..."

SHOPIFY_CDN_RE = re.compile(r'(<img[^>]*\bsrc=")(https?://cdn\.shopify\.com/[^"]+)(")', re.IGNORECASE)
# Internal link rewrites
LINK_PATTERNS = [
    (re.compile(r'https?://(?:www\.)?klovo\.com/blogs/news/'), '/blogs/news/'),
    (re.compile(r'https?://1zchxb-wz\.myshopify\.com/blogs/news/'), '/blogs/news/'),
]

def filename_from_url(url):
    path = urlparse(url).path
    name = path.rsplit("/", 1)[-1]
    return name or "image"

def process_body(body, handle, image_records, seen_urls):
    if not body:
        return ""
    # Rewrite internal links
    new = body
    for pat, repl in LINK_PATTERNS:
        new = pat.sub(repl, new)

    # Rewrite cdn images
    def img_sub(m):
        prefix, url, suffix = m.group(1), m.group(2), m.group(3)
        clean_url = url.split("?")[0]
        fn = filename_from_url(clean_url)
        local = f"/images/blog/{handle}/{fn}"
        if url not in seen_urls:
            seen_urls.add(url)
            image_records.append({
                "article_handle": handle,
                "original_url": url,
                "local_path": f"public/images/blog/{handle}/{fn}",
            })
        return f"{prefix}{local}{suffix}"
    new = SHOPIFY_CDN_RE.sub(img_sub, new)
    return new

def main():
    with open(SRC, "r", encoding="utf-8") as f:
        raw = f.read()
    data = json.loads(raw)
    results = data.get("results", [])

    os.makedirs(BLOG_DIR, exist_ok=True)

    written = 0
    skipped = []
    issues = []
    image_records = []

    for art in results:
        handle = art.get("handle")
        if not handle:
            issues.append(f"missing handle: title={art.get('title')!r}")
            continue
        if not art.get("isPublished", False):
            skipped.append(handle)
            continue

        title = art.get("title") or handle
        published = art.get("publishedAt") or ""
        # author: could be author_name, or nested author.name, or just author (string)
        author = art.get("author_name")
        if not author:
            a = art.get("author")
            if isinstance(a, dict):
                author = a.get("name")
            elif isinstance(a, str):
                author = a
        if not author:
            author = "Klovo Team"

        tags = art.get("tags") or []
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]

        summary = art.get("summary") or ""
        body = art.get("body") or ""
        if not body:
            issues.append(f"empty body: {handle}")

        # image
        image_url = art.get("image_url")
        if not image_url:
            img = art.get("image")
            if isinstance(img, dict):
                image_url = img.get("url")
        image_alt = art.get("image_alt") or art.get("image_altText")
        if not image_alt:
            img = art.get("image")
            if isinstance(img, dict):
                image_alt = img.get("altText") or img.get("alt")

        seen_urls = set()
        # hero image first so it's in manifest even if not referenced in body
        hero_local = None
        if image_url:
            clean = image_url.split("?")[0]
            fn = filename_from_url(clean)
            hero_local = f"/images/blog/{handle}/{fn}"
            seen_urls.add(image_url)
            image_records.append({
                "article_handle": handle,
                "original_url": image_url,
                "local_path": f"public/images/blog/{handle}/{fn}",
            })

        new_body = process_body(body, handle, image_records, seen_urls)

        description = make_description(summary, new_body)

        # Build frontmatter
        lines = ["---"]
        lines.append(f'title: "{yaml_escape(title)}"')
        lines.append(f'description: "{yaml_escape(description)}"')
        if published:
            lines.append(f"date: {published}")
        lines.append(f'author: "{yaml_escape(author)}"')
        if hero_local:
            lines.append(f'image: "{hero_local}"')
            if image_alt:
                lines.append(f'imageAlt: "{yaml_escape(image_alt)}"')
        # tags
        if tags:
            tag_items = ", ".join(f'"{yaml_escape(t)}"' for t in tags)
            lines.append(f"tags: [{tag_items}]")
        else:
            lines.append("tags: []")
        if handle in CANONICALS:
            lines.append(f'canonical: "{CANONICALS[handle]}"')
        lines.append("---")
        lines.append("")
        lines.append(new_body)

        out_path = os.path.join(BLOG_DIR, f"{handle}.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        written += 1

    # Manifest
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump({"images": image_records}, f, indent=2)

    unique_urls = {r["original_url"] for r in image_records}

    print(f"Articles in source: {len(results)}")
    print(f"Markdown files written: {written}")
    print(f"Skipped (unpublished): {len(skipped)} -> {skipped}")
    print(f"Total image entries in manifest: {len(image_records)}")
    print(f"Unique image URLs: {len(unique_urls)}")
    if issues:
        print("Issues:")
        for i in issues:
            print(" -", i)

if __name__ == "__main__":
    main()
