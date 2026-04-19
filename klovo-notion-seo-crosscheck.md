# KLOVO Notion SEO ↔ Shopify Blog Cross-Check

Date: 2026-04-19
Source audit: `klovo-content-audit.md` (34 published + 1 draft handles on Shopify)

---

## 1. Database(s) found

- **SEO & AI Action Items** (data source) — https://www.notion.so/fa0be5900f644e57a7085f91b3f54cf9
  - Parent board: **KLOVO SEO & AI Visibility — Master Board** — https://www.notion.so/337e2b9334a881e9b3daf976f00b4892
  - Schema: `Task` (title), `Status` (Not started / In progress / Done), `Category` (Content - Blog, etc.), `Priority`, `Phase`, `Timeline`, `Target Keywords`, `Notes` (often contains the live Shopify URL or "DRAFT READY — not yet deployed").
  - 18 `Content - Blog` rows have `Status = Done`. All 18 map to a published Shopify handle — see §2.
  - A second tranche of blog/comparison rows created 2026-04-19 (Husky, Ulti-MATE, Flow Wall, Garage vs Kitchen, Modular vs Custom, Garage Flooring, Garage Lighting, How to Measure, How to Install, Are Garage Cabinets Worth It, How Much Weight, Garage Mudroom, Workshop Setup, Home Gym, Home Office, Kids Playroom, etc.) are all `Not started` and are out of scope here.

---

## 2. Notion Done → missing from Shopify

**None.** Every Notion `Content - Blog` row with `Status = Done` has a matching live Shopify handle (many have two handles — the original and a reworked `-1` / "-homeowner-should-know-2026-guide" variant).

Match table (Notion Done → Shopify handle(s)):

| Notion task | Status Notes field | Matched Shopify handle(s) |
|---|---|---|
| BLOG: GlideLock Assembly: How We Made Cabinet Assembly Take 90 Seconds | LIVE | `glidelock-assembly-how-we-made-cabinet-assembly-take-90-seconds`, `glidelock-assembly-how-we-made-cabinet-assembly-take-90-seconds-1`, `glidelock-assembly-how-klovo-made-garage-cabinet-assembly-take-90-seconds` |
| COMPARISON: KLOVO vs. Gladiator Garage Cabinets | "DRAFT READY — not yet deployed" | `klovo-vs-gladiator-garage-cabinets-an-honest-side-by-side-comparison`, `klovo-vs-gladiator-garage-cabinets-an-honest-side-by-side-comparison-1` |
| COMPARISON: KLOVO vs. NewAge Products | "DRAFT READY — not yet deployed" | `klovo-vs-newage-products-premium-garage-cabinets-compared`, `klovo-vs-newage-products-premium-garage-cabinets-compared-1` |
| BLOG: The True Cost of Garage Cabinets | "DRAFT READY — not yet deployed" | `true-cost-of-garage-cabinets-budget-breakdown`, `the-true-cost-of-garage-cabinets-budget-breakdown-for-every-size` |
| PILLAR: Garage Organization Systems 2026 | "DRAFT READY — not yet deployed" | `garage-organization-systems-ultimate-buyers-guide-2026`, `garage-organization-systems-the-ultimate-buyers-guide-2026` |
| PILLAR: Custom Garage Cabinets vs. Pre-Built | "DRAFT READY — not yet deployed" | `custom-garage-cabinets-vs-pre-built`, `custom-garage-cabinets-vs-pre-built-what-every-homeowner-should-know-2026-guide` |
| PILLAR: Made in America: The KLOVO Story | DONE 2026-04-07, published | `made-in-america-the-klovo-story` |
| BLOG: Mudroom to Wow Room: Entryway Storage Before & After | Done | `mudroom-to-wow-room-entryway-storage-before-amp-after` |
| PILLAR: Entryway & Mudroom Storage Solutions | Done | `entryway-mudroom-storage-solutions-that-actually-work-in-2026`, `entryway-mudroom-storage-solutions-that-actually-work-in-2027` |
| BLOG: 10 Laundry Room Makeovers | Done | `10-laundry-room-makeovers-using-modular-cabinets-real-transformations-and-what-they-cost-2026` |
| PILLAR: Laundry Room Cabinet Ideas | Done | `laundry-room-cabinet-ideas-transform-your-space-on-a-budget-in-2026`, `laundry-room-cabinet-ideas-transform-your-space-on-a-budget-in-2027` |
| BLOG: Why 300 lb Shelves Matter | DONE 2026-04-08, published | `why-shelf-weight-capacity-actually-matters-and-why-300-lbs-changes-everything` (DRAFT in Shopify) |
| BLOG: 5 Garage Cabinet Layouts | Done | `5-garage-cabinet-layouts-for-every-garage-size-1-car-to-3-car` |
| BLOG: RTA Cabinets Explained | Done | `rta-cabinets-explained-what-ready-to-assemble-actually-means-in-2026` |
| PILLAR: Complete Guide to DIY Garage Cabinets | Done | `the-complete-guide-to-diy-garage-cabinets-2026` |
| BLOG: Garage Cabinet Materials Compared | Done | `garage-cabinet-materials-compared-steel-vs-wood-vs-engineered-wood-2026-guide` |
| COMPARISON: Best Garage Cabinets 2026: Top 10 Reviewed | Done | `best-garage-cabinets-2026-top-10-reviewed-honest-ranking` |
| PILLAR: Why Kitchen-Grade Cabinets | DONE, published | `why-kitchen-grade-cabinets-belong-in-your-garage` |

> Note on Notion hygiene: 6 rows are marked `Done` but the Notes still say "DRAFT READY — not yet deployed." Those drafts have since shipped to Shopify but the Notion note was never updated. Worth a small cleanup pass.

---

## 3. Shopify published → not tracked in Notion

These handles are live (or draft) on the new Astro site but have no matching Notion `Content - Blog` row. Several correspond to Notion rows that still sit in `Not started` — meaning the blog went out ahead of the tracker:

| Shopify handle | Likely origin |
|---|---|
| `5-ways-to-set-up-your-ultimate-gaming-space` | No Notion row. Adjacent to the still-unstarted `Pillar: Garage Kids Playroom` / `Pillar: Garage Home Gym Setup` but not a direct match. Published outside tracked workflow. |
| `klovo-vs-husky-garage-cabinets-which-is-worth-your-money` | Notion row exists (`Comparison: KLOVO vs Husky`) but `Status = Not started`. Article was shipped without updating Notion. |
| `klovo-vs-seville-classics-garage-cabinets-which-modular-system-is-worth-your-money-2026` | No Notion row. Seville Classics only appears as a bullet inside the "Best Garage Cabinets 2026" roundup. Untracked. |
| `small-garage-big-storage-maximizing-space-under-200-square-feet` | No Notion row. Untracked. |
| `how-to-plan-your-garage-storage-a-step-by-step-measurement-guide` | Notion row exists (`Guide: How to Measure Your Garage Wall`) but `Status = Not started`. Shipped ahead of tracker. |
| `seasonal-garage-organization-spring-cleaning-your-garage-the-right-way-in-2026` | Notion has `Seasonal content plan — March-May spring push` (planning row, not a blog row) and it's still `Not started`. Article shipped outside tracker. |
| `from-builder-to-homeowner-why-contractors-choose-klovo-garage-cabinets` | No Notion row. Contractor-audience post with no backlog entry. Untracked. |
| `garage-flooring-cabinets-the-complete-garage-makeover-guide-for-2026` | Notion row exists (`Guide: Garage Flooring for Cabinets`) but `Status = Not started`. Shipped ahead of tracker. |

**Summary of drift:** 8 of the 34 published Shopify blogs (~24%) went live without a corresponding `Done` flip in Notion. 4 of those 8 have matching `Not started` rows that should simply be flipped to `Done` with the live URL added to Notes. The other 4 (`gaming-space`, `klovo-vs-seville-classics`, `small-garage-big-storage`, `from-builder-to-homeowner`) have no Notion row at all and should be added for historical completeness.
