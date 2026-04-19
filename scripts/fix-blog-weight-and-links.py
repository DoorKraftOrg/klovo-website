#!/usr/bin/env python3
"""
Fix KLOVO blog content:
  1) Update KLOVO weight-capacity claims from "300 lbs per shelf" to "500 lbs per cabinet".
     Only touches lines that unambiguously describe KLOVO. Competitor capacity numbers
     and category-level statistics are preserved.
  2) Rewrite Shopify-era links (https://klovo.com/..., /collections/*, etc.) to the
     new Astro routes.

Idempotent — safe to run multiple times.
"""

from __future__ import annotations
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT / "src" / "content" / "blog"

# ---------------------------------------------------------------------------
# Weight-capacity replacements
# ---------------------------------------------------------------------------
# Each entry: (regex pattern, replacement). All applied with re.sub on the
# whole file. Patterns are written so they only match KLOVO-context lines —
# we use surrounding KLOVO-specific phrasing as anchors where needed.

# Generic literal swaps that are unambiguously KLOVO when they appear.
LITERAL_SWAPS = [
    # Headings / phrases mentioning "300 lb / 300-pound shelves" in KLOVO context
    ("Why 300 lb Weight-Capacity Shelves Change Everything for Heavy Gear",
     "Why 500 lb Per-Cabinet Capacity Changes Everything for Heavy Gear"),
    ("Why 300-Pound Shelves Change Everything: The Engineering Behind Capacity",
     "Why 500-Pound Per-Cabinet Capacity Changes Everything: The Engineering Behind It"),
    ("300 lb weight-capacity shelves transform what's possible:",
     "500 lb per-cabinet capacity transforms what's possible:"),
    # Headings inside comparison posts ("Shelf Capacity: 300 lb vs. ~100 lb")
    ("## 3\\. Shelf Capacity: 300 lb vs. \\~100 lb",
     "## 3\\. Cabinet Capacity: 500 lb per Cabinet vs. \\~100 lb Shelves"),
    ("## 3\\. Shelf Capacity: 300 lb Standard",
     "## 3\\. Cabinet Capacity: 500 lb per Cabinet Standard"),
    ("## Shelf Capacity: 300 lbs vs. 100–200 lbs",
     "## Cabinet Capacity: 500 lbs per Cabinet vs. 100–200 lbs per Shelf"),
    # KLOVO marketing line variants
    ("Every KLOVO shelf is rated for 300 lb.",
     "Every KLOVO cabinet is rated for 500 lb."),
    ("**Every KLOVO shelf is rated for 300 lb.**",
     "**Every KLOVO cabinet is rated for 500 lb.**"),
    ("**Every KLOVO shelf is rated for 300 lb**",
     "**Every KLOVO cabinet is rated for 500 lb**"),
    ("**Every KLOVO shelf is rated for 300 lb** as a baseline — not an upgrade. We made it standard so you never have to think about which shelf can hold what.",
     "**Every KLOVO cabinet is rated for 500 lb** as a baseline — not an upgrade. We made it standard so you never have to think about how much each cabinet can hold."),
]

# Regex-based KLOVO-context replacements.
# Each pattern is anchored by KLOVO phrasing nearby OR table-row context.
REGEX_SWAPS = [
    # Table rows: "| Shelf Capacity | 300 lbs | ..." or "| Fixed shelf capacity | 300 lbs | ..."
    (re.compile(r"\|\s*(?:Fixed s|S)helf [Cc]apacity\s*\|\s*300\s*lbs?\s*\|"),
     "| Cabinet Capacity | 500 lbs per cabinet |"),
    # "| Shelf capacity | ... | **300 lb** |" right-column KLOVO win row
    (re.compile(r"(\|\s*Shelf capacity\s*\|[^|]*\|\s*\*\*)300 lb(\*\*\s*\|)"),
     r"\g<1>500 lb per cabinet\g<2>"),
    # "| Shelf capacity | ~100 lb (Bold) | **300 lb standard** |"
    (re.compile(r"(\|\s*Shelf capacity\s*\|[^|]*\|\s*\*\*)300 lb standard(\*\*\s*\|)"),
     r"\g<1>500 lb per cabinet standard\g<2>"),
    # Tables: "| Cabinet Capacity"-style competitor cell with KLOVO 300 lbs
    (re.compile(r"\|\s*KLOVO Modular System\s*\|\s*\$1,200-\$2,000\s*\|\s*DIY\s*\|\s*300 lbs\s*\|"),
     "| KLOVO Modular System | $1,200-$2,000 | DIY | 500 lbs per cabinet |"),
    (re.compile(r"\|\s*1\s*\|\s*KLOVO\s*\|\s*\\~90 sec\s*\|\s*300 lb\s*\|"),
     "| 1 | KLOVO | \\~90 sec | 500 lb per cabinet |"),
]

# Phrase-level KLOVO-context replacements (full-line / sentence-level).
# These are checked against the file as plain text; they must be unique
# enough to be safe.
PHRASE_SWAPS = [
    # custom-garage-cabinets-vs-pre-built.md tables / KLOVO-spec lines
    ("Shelf capacity: 300 lbs per shelf",
     "Cabinet capacity: 500 lbs per cabinet"),
    ("| Shelf Capacity | 300 lbs | 50 lbs per shelf (200 lbs total) | Varies by line |",
     "| Cabinet Capacity | 500 lbs per cabinet | 50 lbs per shelf (200 lbs total) | Varies by line |"),
    ("| Shelf Capacity | 300 lbs | 50 lbs per shelf | Varies by line |",
     "| Cabinet Capacity | 500 lbs per cabinet | 50 lbs per shelf | Varies by line |"),
    ("| Shelf Capacity | 300 lbs per fixed shelf | 75–100 lbs per shelf (varies by model) |",
     "| Cabinet Capacity | 500 lbs per cabinet | 75–100 lbs per shelf (varies by model) |"),
    ("You need heavy-duty shelves (300 lbs) for tools, equipment, and gear",
     "You need heavy-duty cabinets (500 lbs per cabinet) for tools, equipment, and gear"),
    ("you need heavy-duty 300 lb shelves for tools and equipment",
     "you need heavy-duty 500 lb per-cabinet capacity for tools and equipment"),

    # from-builder-to-homeowner...
    ("Each shelf holds up to 300 lbs, which means homeowners can load them with power tools, paint cans, and bulk storage without shelf sag or failure.",
     "Each cabinet holds up to 500 lbs, which means homeowners can load them with power tools, paint cans, and bulk storage without sag or failure."),
    ("Kitchen-grade TFL, 300 lb shelves, soft-close hardware",
     "Kitchen-grade TFL, 500 lb per-cabinet capacity, soft-close hardware"),

    # klovo-vs-seville-classics
    ("KLOVO's fixed shelves are rated to hold 300 pounds each — enough for heavy automotive supplies, full tool collections, and stacked storage bins without concern.",
     "KLOVO cabinets are rated to hold 500 pounds each — enough for heavy automotive supplies, full tool collections, and stacked storage bins without concern."),
    ("If you need heavy-duty 300 lb shelves for tools, equipment, and heavy storage.",
     "If you need heavy-duty 500 lb per-cabinet capacity for tools, equipment, and heavy storage."),
    ("KLOVO's 300 lb shelf rating significantly exceeds Seville Classics' 75–100 lb range.",
     "KLOVO's 500 lb per-cabinet rating significantly exceeds Seville Classics' 75–100 lb per-shelf range."),

    # glidelock-assembly-how-klovo-made...
    ("**300 lb shelf capacity.** Each fixed shelf supports 300 lbs of evenly distributed weight. The shelf-pin system uses hardened steel pins seated in reinforced bore holes. Adjustable shelves can be repositioned without any change in load rating.",
     "**500 lb per-cabinet capacity.** Each cabinet supports 500 lbs of evenly distributed weight across its shelves. The shelf-pin system uses hardened steel pins seated in reinforced bore holes. Adjustable shelves can be repositioned without any change in cabinet load rating."),
    ("Each KLOVO shelf holds up to 300 lbs of evenly distributed weight.",
     "Each KLOVO cabinet holds up to 500 lbs of evenly distributed weight."),

    # seasonal-garage-organization
    ("The 300 lb shelf capacity means you're not limited to lightweight bins — you can store heavy items like tile saws, pressure washers, and bulk supplies on any shelf without worrying about sagging or failure.",
     "The 500 lb per-cabinet capacity means you're not limited to lightweight bins — you can store heavy items like tile saws, pressure washers, and bulk supplies in any cabinet without worrying about sagging or failure."),
    ("Each cabinet holds up to 300 lbs per shelf, assembles in under 90 seconds with the GlideLock system",
     "Each cabinet holds up to 500 lbs, assembles in under 90 seconds with the GlideLock system"),

    # klovo-vs-newage
    ("300 lb shelves as standard, and a Made-in-Georgia",
     "500 lb per-cabinet capacity as standard, and a Made-in-Georgia"),
    ("KLOVO is generally **15–25% less per linear foot than NewAge Pro**, and roughly comparable to Bold while including soft-close and 300 lb shelves as standard.",
     "KLOVO is generally **15–25% less per linear foot than NewAge Pro**, and roughly comparable to Bold while including soft-close and 500 lb per-cabinet capacity as standard."),
    ("with soft-close and 300 lb shelves included as standard.",
     "with soft-close and 500 lb per-cabinet capacity included as standard."),
    ("soft-close and 300 lb shelves as standard rather than upgrades, and a domestically-made cabinet system that finishes a garage like a kitchen rather than a workshop.",
     "soft-close and 500 lb per-cabinet capacity as standard rather than upgrades, and a domestically-made cabinet system that finishes a garage like a kitchen rather than a workshop."),
    ("soft-close and 300 lb shelves as standard rather than upgrades, and a domestically-made cabinet system.",
     "soft-close and 500 lb per-cabinet capacity as standard rather than upgrades, and a domestically-made cabinet system."),

    # garage-organization-systems-the-ultimate / variant
    ("Heavy-duty weight capacity (premium cabinets like KLOVO hold 300 lbs per fixed shelf)",
     "Heavy-duty weight capacity (premium cabinets like KLOVO hold 500 lbs per cabinet)"),
    ("Heavy-duty weight capacity (premium cabinets like KLOVO hold 300 lbs per shelf)",
     "Heavy-duty weight capacity (premium cabinets like KLOVO hold 500 lbs per cabinet)"),
    ("**300 lb Shelf Capacity:** KLOVO fixed shelves hold twice what budget cabinets handle. Lawn mowers, heavy power tools, automotive fluids — no worries.",
     "**500 lb Per-Cabinet Capacity:** KLOVO cabinets hold far more than budget alternatives. Lawn mowers, heavy power tools, automotive fluids — no worries."),
    ("**300 lb Shelf Capacity:** KLOVO shelves hold twice what budget cabinets handle. This means you can store your lawn mower, heavy power tools, automotive fluids, and equipment without worry.",
     "**500 lb Per-Cabinet Capacity:** KLOVO cabinets hold far more than budget alternatives. This means you can store your lawn mower, heavy power tools, automotive fluids, and equipment without worry."),
    ("KLOVO 6-foot cabinet set: $1,052, premium TFL finish, 300 lb capacity, 90-second GlideLock assembly",
     "KLOVO 6-foot cabinet set: $1,052, premium TFL finish, 500 lb per-cabinet capacity, 90-second GlideLock assembly"),
    ("KLOVO 6-foot cabinet set: $1,052, premium finish, 300 lb capacity, 90-second assembly, lifetime design support",
     "KLOVO 6-foot cabinet set: $1,052, premium finish, 500 lb per-cabinet capacity, 90-second assembly, lifetime design support"),

    # why-kitchen-grade-cabinets
    ("KLOVO's fixed shelves are rated to 300 lbs each for exactly this reason.",
     "KLOVO cabinets are rated to 500 lbs each for exactly this reason."),
    ("| Fixed shelf rating | 300 lbs per shelf |",
     "| Cabinet capacity | 500 lbs per cabinet |"),
    ("KLOVO fixed shelves are rated to 300 lbs each. Adjustable shelves hold 60 lbs. Tall cabinet panels hold up to 400 lbs each, with total tall cabinet capacity reaching 1,000 lbs per unit.",
     "KLOVO cabinets are rated to 500 lbs each. Adjustable shelves hold 60 lbs. Tall cabinet panels hold up to 400 lbs each, with total tall cabinet capacity reaching 1,000 lbs per unit."),
    ("kitchen-grade TFL engineered wood, 1mm PVC edge-banding, 300 lb fixed shelves, patent-pending GlideLock assembly.",
     "kitchen-grade TFL engineered wood, 1mm PVC edge-banding, 500 lb per-cabinet capacity, patent-pending GlideLock assembly."),

    # small-garage-big-storage
    ("KLOVO wall cabinets mount securely to studs and each shelf supports up to 300 lbs.",
     "KLOVO wall cabinets mount securely to studs and each cabinet supports up to 500 lbs."),

    # glidelock-assembly-how-we-made-cabinet-assembly...
    ("300 lb shelves, moisture-resistant TFL finish, soft-close hardware.",
     "500 lb per-cabinet capacity, moisture-resistant TFL finish, soft-close hardware."),

    # entryway-mudroom 2026 — KLOVO contexts
    ("This construction method creates shelves with 300-pound capacity—double or triple the capacity of standard alternatives.",
     "This construction method gives KLOVO cabinets 500-pound capacity—several times the capacity of standard alternatives."),
    ("The 300-pound capacity also provides psychological benefit.",
     "The 500-pound per-cabinet capacity also provides psychological benefit."),
    ("| KLOVO Modular System | $1,200-$2,000 | DIY | 300 lbs | Excellent | High |",
     "| KLOVO Modular System | $1,200-$2,000 | DIY | 500 lbs per cabinet | Excellent | High |"),

    # entryway-mudroom 2027
    ("choosing shelves rated for 300 lbs ensures your system handles real-world use.",
     "choosing cabinets rated for 500 lbs ensures your system handles real-world use."),

    # made-in-america
    ("300 lb fixed shelf rating.",
     "500 lb per-cabinet capacity rating."),

    # klovo-vs-husky
    ("KLOVO delivers kitchen-grade materials, 300 lb shelves, and patent-pending GlideLock assembly. Here's the full head-to-head.",
     "KLOVO delivers kitchen-grade materials, 500 lb per-cabinet capacity, and patent-pending GlideLock assembly. Here's the full head-to-head."),
    ("KLOVO delivers kitchen-grade materials, 300 lb shelves, patent-pending GlideLock assembly, and domestic manufacturing at a premium-but-justified price.",
     "KLOVO delivers kitchen-grade materials, 500 lb per-cabinet capacity, patent-pending GlideLock assembly, and domestic manufacturing at a premium-but-justified price."),
    ("| **Fixed shelf capacity** | 300 lbs | 100–200 lbs (varies by line) |",
     "| **Cabinet capacity** | 500 lbs per cabinet | 100–200 lbs per shelf (varies by line) |"),
    ("## Shelf Capacity: 300 lbs vs. 100–200 lbs",
     "## Cabinet Capacity: 500 lbs per Cabinet vs. 100–200 lbs per Shelf"),
    ("KLOVO's fixed shelves are rated to 300 pounds each. Adjustable shelves hold 60 lbs.",
     "KLOVO cabinets are rated to 500 pounds each. Adjustable shelves hold 60 lbs."),
    ("KLOVO's 300 lb rating gives real headroom.",
     "KLOVO's 500 lb per-cabinet rating gives real headroom."),
    ("the 300 lb shelf rating, and modular expandability justify the price gap",
     "the 500 lb per-cabinet capacity, and modular expandability justify the price gap"),

    # best-garage-cabinets top 10
    ("**Shelf capacity:** 300 lb per shelf.", "**Cabinet capacity:** 500 lb per cabinet."),
    ("Shelves are rated to 300 lb, which is 2–3× the category average.",
     "Cabinets are rated to 500 lb, which is several times the category average."),
    ("| 1 | KLOVO | \\~90 sec | 300 lb | Kitchen-grade plywood | Lifetime |",
     "| 1 | KLOVO | \\~90 sec | 500 lb per cabinet | Kitchen-grade plywood | Lifetime |"),

    # 10-laundry-room-makeovers
    ("KLOVO's 300 lb shelves handle heavy detergent jugs and bulk supplies easily.",
     "KLOVO's 500 lb per-cabinet capacity handles heavy detergent jugs and bulk supplies easily."),
    ("The 300 lb shelves handle bulk dog food bags and heavy pet supply containers that would buckle lighter shelving.",
     "The 500 lb per-cabinet capacity handles bulk dog food bags and heavy pet supply containers that would buckle lighter shelving."),
    ("The 300 lb shelves store detergent, cleaning supplies, and linens that would otherwise crowd the closet interior.",
     "The 500 lb per-cabinet capacity stores detergent, cleaning supplies, and linens that would otherwise crowd the closet interior."),

    # laundry-room-cabinet-ideas-2026
    ("KLOVO cabinets feature 300-pound weight capacity shelves, supporting heavy detergent bottles, cleaning supplies, and laundry baskets without sagging.",
     "KLOVO cabinets feature 500-pound per-cabinet capacity, supporting heavy detergent bottles, cleaning supplies, and laundry baskets without sagging."),

    # true-cost-of-garage-cabinets-budget-breakdown
    ("| **Premium Modular** | $175–$360/ft | Kitchen-grade materials, 300 lb shelves, tool-free assembly |",
     "| **Premium Modular** | $175–$360/ft | Kitchen-grade materials, 500 lb per-cabinet capacity, tool-free assembly |"),
    ("* **300 lb shelf capacity** — Load up power tools, automotive parts, cases of paint, and heavy equipment. This is 4–6x the capacity of budget shelves.",
     "* **500 lb per-cabinet capacity** — Load up power tools, automotive parts, cases of paint, and heavy equipment. This is several times the capacity of budget cabinets."),
    ("but gives you 300 lb shelves (vs. 50 lb), kitchen-grade finish",
     "but gives you 500 lb per-cabinet capacity (vs. 50 lb shelves), kitchen-grade finish"),
    ("The 300 lb shelves and moisture-resistant finish will handle everything you throw at them.",
     "The 500 lb per-cabinet capacity and moisture-resistant finish will handle everything you throw at them."),
    ("The 300 lb shelves and moisture-resistant finish handle everything.",
     "The 500 lb per-cabinet capacity and moisture-resistant finish handle everything."),
    ("delivers kitchen-grade materials, 300 lb shelves, and genuine tool-free assembly",
     "delivers kitchen-grade materials, 500 lb per-cabinet capacity, and genuine tool-free assembly"),
    ("(KLOVO: 300 lb shelves, TFL finish, tool-free assembly)",
     "(KLOVO: 500 lb per-cabinet capacity, TFL finish, tool-free assembly)"),
    ("KLOVO cabinets include 300 lb shelves, soft-close hardware, and patent-pending GlideLock assembly as standard.",
     "KLOVO cabinets include 500 lb per-cabinet capacity, soft-close hardware, and patent-pending GlideLock assembly as standard."),

    # custom-garage-cabinets-vs-pre-built (long form)
    ("KLOVO sits squarely in this tier, offering kitchen-grade engineered wood with TFL (Thermally Fused Laminate) finish, 300 lb fixed shelves, and the patent-pending GlideLock assembly system",
     "KLOVO sits squarely in this tier, offering kitchen-grade engineered wood with TFL (Thermally Fused Laminate) finish, 500 lb per-cabinet capacity, and the patent-pending GlideLock assembly system"),
    ("KLOVO's fixed shelves hold 300 lbs each — more than most custom builders spec.",
     "KLOVO cabinets hold 500 lbs each — more than most custom builders spec."),
    ("The 300 lb shelf capacity alone puts KLOVO in a different performance class than budget options rated at 40–75 lbs per shelf.",
     "The 500 lb per-cabinet capacity alone puts KLOVO in a different performance class than budget options rated at 40–75 lbs per shelf."),

    # garage-cabinet-materials-compared (KLOVO column only — the third "300 lbs/shelf")
    ("* **300 lb shelf capacity:** Engineered wood with proper support handles serious loads. Plenty for most homeowners.",
     "* **500 lb per-cabinet capacity:** Engineered wood with proper support handles serious loads. Plenty for most homeowners."),
    ("| **Weight Capacity** | 300+ lbs/shelf | 300+ lbs/shelf | 300 lbs/shelf |",
     "| **Weight Capacity** | 300+ lbs/shelf | 300+ lbs/shelf | 500 lbs per cabinet |"),

    # the-complete-guide-to-diy-garage-cabinets
    ("KLOVO publishes 300 lbs per shelf distributed.",
     "KLOVO publishes 500 lbs per cabinet distributed."),

    # ----- HTML-wrapped variants in Shopify-port "long single-line" files -----
    # best-garage-cabinets (frontmatter description / blob — duplicate of body table row)
    ("|| 1 | KLOVO | \\~90 sec | 300 lb | Kitchen-grade plywood | Lifetime ||",
     "|| 1 | KLOVO | \\~90 sec | 500 lb per cabinet | Kitchen-grade plywood | Lifetime ||"),
    ("**Shelf capacity:** 300 lb per shelf.",
     "**Cabinet capacity:** 500 lb per cabinet."),
    # klovo-vs-gladiator HTML version
    ("<h2>3\\. Shelf Capacity: 300 lb vs. \\~100 lb</h2>",
     "<h2>3\\. Cabinet Capacity: 500 lb per Cabinet vs. \\~100 lb Shelves</h2>"),
    ("soft-close hardware, and 300 lb shelves as standard rather than upgrades.",
     "soft-close hardware, and 500 lb per-cabinet capacity as standard rather than upgrades."),
    ("<tr><td>Shelf capacity</td><td>\\~75–100 lb</td><td><strong>300 lb</strong></td></tr>",
     "<tr><td>Cabinet capacity</td><td>\\~75–100 lb per shelf</td><td><strong>500 lb per cabinet</strong></td></tr>"),
    # klovo-vs-newage HTML version
    ("<h2>3\\. Shelf Capacity: 300 lb Standard</h2>",
     "<h2>3\\. Cabinet Capacity: 500 lb per Cabinet Standard</h2>"),
    ("<p><strong>Every KLOVO shelf is rated for 300 lb</strong> as a baseline — not an upgrade. We made it standard so you never have to think about which shelf can hold what.</p>",
     "<p><strong>Every KLOVO cabinet is rated for 500 lb</strong> as a baseline — not an upgrade. We made it standard so you never have to think about how much each cabinet can hold.</p>"),
    ("<tr><td>Shelf capacity</td><td>\\~100 lb (Bold)</td><td><strong>300 lb standard</strong></td></tr>",
     "<tr><td>Cabinet capacity</td><td>\\~100 lb per shelf (Bold)</td><td><strong>500 lb per cabinet standard</strong></td></tr>"),
    # true-cost HTML version
    ("Kitchen-grade materials, 300 lb shelves, tool-free assembly</td>",
     "Kitchen-grade materials, 500 lb per-cabinet capacity, tool-free assembly</td>"),
    ("Every shelf holds <strong>300 lbs</strong>.",
     "Every cabinet holds <strong>500 lbs</strong>."),
    ("for premium modular systems like KLOVO (300 lb shelves, TFL finish, tool-free assembly)",
     "for premium modular systems like KLOVO (500 lb per-cabinet capacity, TFL finish, tool-free assembly)"),
    # rta-cabinets (KLOVO is named in the sentence)
    ("KLOVO modular cabinets ship flat, click together in under 90 seconds per cabinet, are rated for 300 lbs distributed per shelf, and use kitchen-grade construction sealed on all six sides.",
     "KLOVO modular cabinets ship flat, click together in under 90 seconds per cabinet, are rated for 500 lbs distributed per cabinet, and use kitchen-grade construction sealed on all six sides."),
    # klovo-vs-husky line 87
    ("The material quality, assembly ease, 300 lb shelf rating, and modular expandability justify the price gap, particularly for long-term use.",
     "The material quality, assembly ease, 500 lb per-cabinet capacity, and modular expandability justify the price gap, particularly for long-term use."),

    # ----- entryway-mudroom-2026 long-line variants -----
    # These are in KLOVO-positioning sections that were already updated in the
    # newer "2027" version. Apply the same updates to the 2026 long-line file.
    ("A 300-pound capacity shelf can handle winter boots for an entire family, sports equipment, and storage boxes without concern.",
     "A 500-pound per-cabinet capacity can handle winter boots for an entire family, sports equipment, and storage boxes without concern."),
    ("A 300-pound capacity shelf is particularly valuable in winter because it can safely store multiple pairs of heavy boots, winter sports equipment, and storage boxes containing off-season items.",
     "A 500-pound per-cabinet capacity is particularly valuable in winter because it can safely store multiple pairs of heavy boots, winter sports equipment, and storage boxes containing off-season items."),
    ("The 300-pound capacity means you can store heavy winter gear, sports equipment, and storage boxes without concern.",
     "The 500-pound per-cabinet capacity means you can store heavy winter gear, sports equipment, and storage boxes without concern."),
    ("The 300-pound shelf capacity means you're not limited in what you can store.",
     "The 500-pound per-cabinet capacity means you're not limited in what you can store."),
    ("A 300-pound shelf capacity means you can store heavy winter gear without concern.",
     "A 500-pound per-cabinet capacity means you can store heavy winter gear without concern."),
    # Internal link text — leave the URL alone (it's a different blog slug),
    # but fix the user-facing anchor text.
    ("[why shelf weight capacity actually matters and why 300 lbs changes everything]",
     "[why cabinet weight capacity actually matters and why 500 lbs per cabinet changes everything]"),

    # ----- garage-organization-systems-ultimate (line 27 long line) -----
    # Mid-range steel category line — leave alone (competitor category).
    # No KLOVO-specific 300 here.


    # how-to-plan-your-garage-storage (load number)
    ("A fully loaded KLOVO wall cabinet can weigh up to 350 lbs (50 lb cabinet + 300 lb shelf load).",
     "A fully loaded KLOVO wall cabinet can weigh up to 550 lbs (50 lb cabinet + 500 lb capacity load)."),
]


# ---------------------------------------------------------------------------
# Link rewrites — KLOVO-owned URLs only.
# ---------------------------------------------------------------------------
# Order matters: more specific patterns first.
LINK_SWAPS = [
    # Absolute klovo.com → relative
    ("https://www.klovo.com/blogs/news/", "/blogs/news/"),
    ("https://klovo.com/blogs/news/", "/blogs/news/"),
    # Shopify-only "/blog/<slug>" → "/blogs/news/<slug>"
    ("https://klovo.com/blog/klovo-vs-gladiator",
     "/blogs/news/klovo-vs-gladiator-garage-cabinets-an-honest-side-by-side-comparison"),
    ("https://klovo.com/blog/klovo-vs-newage",
     "/blogs/news/klovo-vs-newage-products-premium-garage-cabinets-compared"),
    ("https://klovo.com/blog/klovo-vs-husky",
     "/blogs/news/klovo-vs-husky-garage-cabinets-which-is-worth-your-money"),
    ("https://klovo.com/blog/custom-garage-cabinets-vs-pre-built",
     "/blogs/news/custom-garage-cabinets-vs-pre-built"),
    ("https://klovo.com/blogs/diy-garage-cabinets-guide",
     "/blogs/news/the-complete-guide-to-diy-garage-cabinets-2026"),
    # Shopify /collections/* → /sets/
    ("https://klovo.com/collections/kits-bundles", "/sets/"),
    ("https://klovo.com/collections/garage-cabinet-sets", "/sets/"),
    ("https://klovo.com/collections/all", "/sets/"),
    ("/collections/all", "/sets/"),
    ("/collections/kits-bundles", "/sets/"),
    ("/collections/garage-cabinet-sets", "/sets/"),
    # Pages — these exist as ported Astro pages under /pages/*
    ("https://klovo.com/pages/", "/pages/"),
    # Bare klovo.com homepage references
    ("](https://klovo.com)", "](/)"),
    ("](https://www.klovo.com)", "](/)"),
]


def transform(text: str) -> tuple[str, int, int]:
    weight_count = 0
    link_count = 0

    new_text = text

    # Literal weight swaps
    for old, new in LITERAL_SWAPS:
        if old in new_text:
            n = new_text.count(old)
            new_text = new_text.replace(old, new)
            weight_count += n

    # Phrase weight swaps
    for old, new in PHRASE_SWAPS:
        if old in new_text:
            n = new_text.count(old)
            new_text = new_text.replace(old, new)
            weight_count += n

    # Regex weight swaps
    for pattern, repl in REGEX_SWAPS:
        new_text, n = pattern.subn(repl, new_text)
        weight_count += n

    # Link rewrites
    for old, new in LINK_SWAPS:
        if old in new_text:
            n = new_text.count(old)
            new_text = new_text.replace(old, new)
            link_count += n

    return new_text, weight_count, link_count


def main() -> None:
    files = sorted(BLOG_DIR.glob("*.md"))
    modified = 0
    total_weight = 0
    total_links = 0

    for f in files:
        original = f.read_text(encoding="utf-8")
        new_text, w, l = transform(original)
        if new_text != original:
            f.write_text(new_text, encoding="utf-8")
            modified += 1
            print(f"  modified: {f.name}  weight={w}  links={l}")
            total_weight += w
            total_links += l

    print()
    print(f"Files scanned:    {len(files)}")
    print(f"Files modified:   {modified}")
    print(f"Weight rewrites:  {total_weight}")
    print(f"Link rewrites:    {total_links}")


if __name__ == "__main__":
    main()
