# Klovo Website

Astro 4 site for klovo.com — garage cabinet systems. Auto-deploys to Vercel from `main`.

## Stack
- Astro 4 App Router, Tailwind, TypeScript
- Content: `src/content/blog/` (blog), `src/pages/pages/` (SEO/legal), `src/content/sets/` (products)
- Repo: `github.com/DoorKraftOrg/klovo-website`, branch `main`
- Preview: Claude-Preview MCP `klovo-dev` on port 4321

## Critical brand rules
- Weight: **"500 lbs per cabinet"** — never per shelf
- Tools: **"almost tool-free"** — 4 screws still required for back panel runners
- Assembly: **"about 2–3 minutes per cabinet"** — never "90 seconds"
- Connector: **GlideLock** (patent-pending)
- Brand: **Klovo** only — never "Clik" or "Clik Closets"

## URL patterns (never break these)
- Blog: `/blogs/news/{slug}` — never `/blog/`
- Products: `/sets/{slug}` — never `/collections/` or `/products/`
- SEO pages: `/pages/{handle}`

## SEO backlog
- Notion DB: `8fa3a3dd-72e8-4bc6-85a9-271eb1041b8e`
- Strategy plan: `~/.claude/plans/streamed-sparking-diffie.md`

## Do NOT read automatically
- `node_modules/`, `dist/`, `.git/`
- `src/content/blog/*.md` in bulk — read individually when needed
