# Klovo Shopify → Astro Content Audit

Source of truth: Shopify store `1zchxb-wz.myshopify.com` (customer-facing domain `klovo.com`). Pulled via Admin GraphQL on 2026-04-19.

---

## Summary

| Bucket | Count | Action |
|---|---|---|
| Blog articles — published | 34 | Port all 1:1 to `/blogs/news/{slug}` |
| Blog articles — unpublished | 1 | Skip (draft) |
| Shopify pages — already on Astro | 8 | 301 redirect old `/pages/{handle}` → existing Astro path |
| Shopify pages — SEO landing pages | 6 | Flag for decision: port as real pages or redirect |
| Shopify pages — legal/policy | 2 | Port content to Astro (terms, shipping) |
| Shopify pages — internal/unpublished | 7 | Skip |
| Shopify pages — misc | 9 | Catch-all redirect to `/` |

---

## 1. Blog Articles (`/blogs/news/*`) — 34 published, 1 draft

Every URL below is currently indexed. **Recommendation: port all 34 URLs 1:1 to preserve SEO.** Duplicates (marked 🔁) look like re-publishes of the same content — port both URLs but set the newer one as `rel="canonical"` during content migration. Final dedup/consolidation is a separate cleanup pass.

| # | Handle | Title | Published | Dup of |
|---|---|---|---|---|
| 1 | `5-ways-to-set-up-your-ultimate-gaming-space` | 5 Ways to Set Up Your Ultimate Gaming Space | 2026-04-01 | |
| 2 | `glidelock-assembly-how-we-made-cabinet-assembly-take-90-seconds` | GlideLock Assembly: 90-Second Cabinet Assembly | 2026-04-03 | |
| 3 | `klovo-vs-gladiator-garage-cabinets-an-honest-side-by-side-comparison` | KLOVO vs. Gladiator | 2026-04-07 | |
| 4 | `klovo-vs-newage-products-premium-garage-cabinets-compared` | KLOVO vs. NewAge Products | 2026-04-07 | |
| 5 | `true-cost-of-garage-cabinets-budget-breakdown` | True Cost of Garage Cabinets | 2026-04-07 | |
| 6 | `garage-organization-systems-ultimate-buyers-guide-2026` | Garage Organization Systems Buyer's Guide | 2026-04-07 | |
| 7 | `custom-garage-cabinets-vs-pre-built` | Custom vs. Pre-Built | 2026-04-07 | |
| 8 | `klovo-vs-husky-garage-cabinets-which-is-worth-your-money` | KLOVO vs. Husky | 2026-04-07 | |
| 9 | `why-kitchen-grade-cabinets-belong-in-your-garage` | Kitchen-Grade Cabinets in Your Garage | 2026-04-07 | |
| 10 | `klovo-vs-gladiator-garage-cabinets-an-honest-side-by-side-comparison-1` | KLOVO vs. Gladiator | 2026-04-07 | 🔁 #3 |
| 11 | `klovo-vs-newage-products-premium-garage-cabinets-compared-1` | KLOVO vs. NewAge | 2026-04-07 | 🔁 #4 |
| 12 | `the-true-cost-of-garage-cabinets-budget-breakdown-for-every-size` | True Cost of Garage Cabinets | 2026-04-07 | 🔁 #5 |
| 13 | `made-in-america-the-klovo-story` | Made in America: KLOVO Story | 2026-04-07 | |
| 14 | `glidelock-assembly-how-we-made-cabinet-assembly-take-90-seconds-1` | GlideLock Assembly | 2026-04-07 | 🔁 #2 |
| 15 | `garage-organization-systems-the-ultimate-buyers-guide-2026` | Garage Organization Systems Guide | 2026-04-07 | 🔁 #6 |
| 16 | `the-complete-guide-to-diy-garage-cabinets-2026` | DIY Garage Cabinets Complete Guide | 2026-04-08 | |
| 17 | `rta-cabinets-explained-what-ready-to-assemble-actually-means-in-2026` | RTA Cabinets Explained | 2026-04-08 | |
| 18 | `5-garage-cabinet-layouts-for-every-garage-size-1-car-to-3-car` | 5 Garage Cabinet Layouts | 2026-04-08 | |
| 19 | `mudroom-to-wow-room-entryway-storage-before-amp-after` | Mudroom to Wow Room | 2026-04-08 | |
| 20 | `best-garage-cabinets-2026-top-10-reviewed-honest-ranking` | Best Garage Cabinets 2026: Top 10 | 2026-04-09 | |
| 21 | `entryway-mudroom-storage-solutions-that-actually-work-in-2026` | Entryway & Mudroom Storage Solutions | 2026-04-09 | |
| 22 | `laundry-room-cabinet-ideas-transform-your-space-on-a-budget-in-2026` | Laundry Room Cabinet Ideas | 2026-04-09 | |
| 23 | `garage-cabinet-materials-compared-steel-vs-wood-vs-engineered-wood-2026-guide` | Garage Cabinet Materials Compared | 2026-04-09 | |
| 24 | `entryway-mudroom-storage-solutions-that-actually-work-in-2027` | Entryway & Mudroom Storage Solutions | 2026-04-09 | 🔁 #21 |
| 25 | `laundry-room-cabinet-ideas-transform-your-space-on-a-budget-in-2027` | Laundry Room Cabinet Ideas | 2026-04-09 | 🔁 #22 |
| 26 | `custom-garage-cabinets-vs-pre-built-what-every-homeowner-should-know-2026-guide` | Custom vs. Pre-Built Guide | 2026-04-10 | 🔁 #7 |
| 27 | `klovo-vs-seville-classics-garage-cabinets-which-modular-system-is-worth-your-money-2026` | KLOVO vs. Seville Classics | 2026-04-10 | |
| 28 | `10-laundry-room-makeovers-using-modular-cabinets-real-transformations-and-what-they-cost-2026` | 10 Laundry Room Makeovers | 2026-04-10 | |
| 29 | `glidelock-assembly-how-klovo-made-garage-cabinet-assembly-take-90-seconds` | GlideLock Assembly (Klovo) | 2026-04-10 | 🔁 #2 |
| 30 | `small-garage-big-storage-maximizing-space-under-200-square-feet` | Small Garage, Big Storage | 2026-04-10 | |
| 31 | `how-to-plan-your-garage-storage-a-step-by-step-measurement-guide` | Plan Your Garage Storage | 2026-04-10 | |
| 32 | `seasonal-garage-organization-spring-cleaning-your-garage-the-right-way-in-2026` | Seasonal Garage Organization | 2026-04-10 | |
| 33 | `from-builder-to-homeowner-why-contractors-choose-klovo-garage-cabinets` | Why Contractors Choose KLOVO | 2026-04-10 | |
| 34 | `garage-flooring-cabinets-the-complete-garage-makeover-guide-for-2026` | Garage Flooring + Cabinets Makeover | 2026-04-10 | |
| — | `why-shelf-weight-capacity-actually-matters-and-why-300-lbs-changes-everything` | Why Shelf Weight Capacity Matters | *draft* | skip |

---

## 2. Shopify Pages (`/pages/*`)

### 2a. Already-equivalent pages — redirect only

| Old `/pages/{handle}` | New path on Astro | Notes |
|---|---|---|
| `/pages/about` | `/about` | |
| `/pages/contact` | `/contact` | Shopify body is empty anyway |
| `/pages/warranty` | `/warranty` | |
| `/pages/assembly` | `/assembly` | |
| `/pages/where-to-buy` | `/where-to-buy` | |
| `/pages/frequently-asked-questions` | `/faq` | |
| `/pages/retailers` | `/for-retailers` | |
| `/pages/how-it-works` | `/assembly` | already redirected in `astro.config.mjs` at root `/how-it-works/` — extend to `/pages/how-it-works` too |

### 2b. SEO landing pages — decision needed

These have real indexable content and drove search traffic. Three options per page: (A) port 1:1 as an Astro page, (B) redirect to closest equivalent blog post, (C) redirect to `/`.

| Old URL | Title | Suggested action |
|---|---|---|
| `/pages/garage-cabinets` | Garage Cabinets | **B** → `/sets/` (product hub) |
| `/pages/custom-garage-cabinets` | Custom Garage Cabinets | **B** → `/blogs/news/custom-garage-cabinets-vs-pre-built` |
| `/pages/diy-garage-cabinets` | DIY Garage Cabinets | **B** → `/blogs/news/the-complete-guide-to-diy-garage-cabinets-2026` |
| `/pages/laundry-room-cabinets` | Laundry Room Cabinets | **B** → `/blogs/news/laundry-room-cabinet-ideas-transform-your-space-on-a-budget-in-2026` |
| `/pages/entryway-cabinets` | Entryway & Mudroom Cabinets | **B** → `/blogs/news/entryway-mudroom-storage-solutions-that-actually-work-in-2026` |
| `/pages/garage-organization-systems` | Garage Organization Systems | **B** → `/blogs/news/garage-organization-systems-ultimate-buyers-guide-2026` |
| `/pages/glidelock-assembly` | GlideLock Assembly System | **B** → `/blogs/news/glidelock-assembly-how-we-made-cabinet-assembly-take-90-seconds` |

### 2c. Legal / policy — port content to Astro

| Old URL | Action |
|---|---|
| `/pages/terms-of-service` | Port body HTML → new `/legal/terms` Astro page, then 301 old URL |
| `/pages/shipping-and-returns` | Port body HTML → new `/legal/shipping-and-returns`, then 301 old URL |
| `/pages/data-sharing-opt-out` | Port body HTML → new `/legal/privacy-choices`, then 301 old URL |
| `/pages/warranties-map-trade-partner-policies-clikclosets-trade-info` | 301 → `/warranty` (or port separately if trade program lives on) |

### 2d. Trade / pro — decision needed

| Old URL | Status | Suggested |
|---|---|---|
| `/pages/pro` | published | redirect → `/for-retailers` |
| `/pages/plan` | published | redirect → `/` (unless there's a plan tool page) |
| `/pages/dealers` | published | redirect → `/where-to-buy` |
| `/pages/builders` | published | redirect → `/for-retailers` |
| `/pages/trade` | published (form) | port if the trade registration form is still active; else redirect `/contact` |
| `/pages/rendering` | published (Magicplan) | redirect `/` |
| `/pages/configurator` | published | redirect `/sets/` |

### 2e. Unpublished — skip (don't redirect, Google never indexed)

- `/pages/clikclosets-brochure-2025`
- `/pages/trade-partners-info-page`
- `/pages/about-technology`
- `/pages/map`
- `/pages/retail`
- `/pages/trade-1`

### 2f. Catch-all fallback

Anything else under `/pages/*` → `/` (301 permanent).

---

## 3. Notion SEO backlog cross-check

Not yet pulled — waiting to port the blog first, then I'll diff the Notion "Done" column against the ported handles to flag any tracked-but-not-published items for you.

---

## 4. Implementation plan (what I'll do next, once you green-light)

1. **Create blog infrastructure** — `src/pages/blogs/news/[slug].astro`, `src/pages/blogs/news/index.astro` (listing), `src/pages/blog.astro` → redirect to `/blogs/news` (or double-route).
2. **Port 34 articles** → `src/content/blog/{handle}.md` with frontmatter (title, description, date, image, author) + body HTML. Extend schema to optionally include `tags` and `canonical` (for duplicates).
3. **Download images** → `public/images/blog/{handle}/*` and rewrite `<img src>` paths.
4. **Port 3 legal pages** as real Astro pages.
5. **Add all redirects** to `astro.config.mjs` `redirects:` block.
6. **Build + preview** → spot-check 5 posts, verify 301s on 3 page URLs.
7. **Cross-check Notion** and report drift.

---

## 5. Open decisions for Soham before step 2

1. Duplicates in blog table (rows #10, 11, 12, 14, 15, 24, 25, 26, 29) — port all 9 or consolidate now and 301 the -1 variants to the canonical slug? Default: **port all** for safety.
2. Section 2b (SEO landing pages) — are the B→blog redirects OK, or do any need to stay as dedicated Astro pages?
3. Section 2d (trade pages) — is `/pages/trade` form still in use? If yes, it needs to be ported, not redirected.
4. Where should legal pages live — `/legal/*` (my default) or top-level `/terms`, `/shipping-returns`, `/privacy-choices`?
