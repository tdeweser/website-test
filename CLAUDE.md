# ipe.nl — website rebuild

Static rebuild of www.ipe.nl (Instituut voor Publieke Economie). Content lives in Markdown
(`content/`), is rendered by `scripts/build.py` into `public/`, and `public/` is committed and
served by Cloudflare Pages (`ipe-dza.pages.dev`, output directory `public`, no build command).
Read [README.md](README.md) and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) first.

## Working on this site

- Python: always use `.venv/Scripts/python` (deps in `requirements.txt`).
- Edit sources only: `content/`, `templates/`, `static/`, `scripts/`. Never hand-edit `public/`.
- After every change: `scripts/build.py`, then `scripts/check.py`, which must print OK. Commit
  sources **and** `public/` together.
- **No links to the old site.** Nothing in `public/` may point at ipe.nl, instituut-pe.nl or
  Squarespace (mailto `@ipe.nl` excepted). Download new images/PDFs into `static/media/` and
  link them as `/media/...`. `check.py` enforces this.
- **Look of the site (2026-11-17):** the site is being upgraded section by section.
  - *Redesigned* (modelled on the reference design at ipe-eta.vercel.app): the header, the
    footer (every page) and the homepage. Styles: `static/assets/css/chrome.css` (header,
    footer, buttons, tokens) and `home.css` (homepage only). DM Sans VF + DM Mono, colours
    red `#d63f44`, cream `#f4ede3`, ink `#141312`, navy `#1d3354`.
  - *Still the original ipe.nl look:* all other page bodies (`site.css`, measured from the old
    Squarespace site). Keep those faithful to the original until the user asks to redesign them.
  - The design system below applies to new designs and mock-ups.
- Hand-maintained (the scraper never overwrites them, `keep_local` in site.yml):
  the homepage `content/pages/home.md` (front matter = all texts and settings), the team page
  `content/pages/onze-mensen.md` and `content/people/people.yml` (everyone on the team page,
  grouped; `home: true` = also on the homepage). Portraits are round with a CSS-drawn red ring
  (`ui.portrait`); `ringed: true` marks photo files that already contain a ring.
- Listings show only `in_window: true` items (the 3-month window, `content/site.yml`).
  Non-article content (pages, events) is taken regardless of date.
- Shortcodes available in content: `listing()`, `authors()`, `archive()`, `map()`,
  `social_links()` (see docs/ARCHITECTURE.md).
- `scripts/scrape.py` overwrites `content/pages|highlights|events`, `content/people/authors.yml`
  and `static/media`. Don't re-run it after hand edits without the user's OK.
- Keep this site `noindex` (`content/site.yml`) until the user says it goes live.
- How to add content: [docs/CONTENT-GUIDE.md](docs/CONTENT-GUIDE.md). Deploy: [docs/DEPLOY.md](docs/DEPLOY.md).

## Design: use the IPE design system for new designs

Every new HTML design, mock-up or component made in this project follows the IPE
design system in [design-system/](design-system/) (the website itself mirrors the original
ipe.nl, see above). Before designing anything:

1. Read [design-system/README.md](design-system/README.md) — content
   fundamentals (tone, Dutch copy, boilerplate), visual foundations, iconography.
2. Read [design-system/assets/notes/CLAUDE.from-standalone.md](design-system/assets/notes/CLAUDE.from-standalone.md)
   — the fixed colour rules.
3. For a component, read its `.prompt.md` (usage) and `.jsx` (exact styling) in
   [design-system/components/](design-system/components/).
4. For a website page, look at [design-system/templates/website/](design-system/templates/website/)
   (Home, Publications, Article) as the reference layout.

When the README and the official brand guide disagree, the PDF wins:
[design-system/uploads/IPE-richtlijnen-huisstijl-oktober-2025-v21.pdf](design-system/uploads/IPE-richtlijnen-huisstijl-oktober-2025-v21.pdf).
Address and domain are the exception: use **ipe.nl** and **Plein 17, 2511 CS Den Haag**
(the PDF still shows the old ones).

### How to wire it into a page

- For a standalone mock-up, link `design-system/styles.css`. It loads the self-hosted
  DM Sans / DM Mono fonts and all tokens. (The website build also publishes it at
  `/assets/ds/styles.css`, used there only for the DM Sans fonts.)
- Use the CSS custom properties, never raw hex values: `var(--brand)`,
  `var(--surface-alt)`, `var(--font-mono)`, `var(--space-6)`, `var(--type-h1)` etc.
  (see [design-system/tokens/](design-system/tokens/)).
- The site is static HTML. Reproduce components as plain HTML + CSS using the
  styling in their `.jsx` files; only use React/Babel (`_ds_bundle.js`) for
  throwaway prototypes, not for production pages.
- Logos: use the PNGs in [design-system/assets/logo/](design-system/assets/logo/)
  rather than re-typesetting the wordmark.

### Non-negotiables

- **Palette is fixed to nine colours**: white `#ffffff`, black `#000000`,
  beige `#f4ede3`, text gray `#404040`, red `#d63f44` (hero accent),
  navy `#1d3354`, gray `#9f9f9f`, aqua `#4790b1`, green `#00843b`. Charts use only
  red and navy plus their `-l80/-l60/-l40/-d25/-d50` variants. No other colours.
- **Type**: DM Sans for everything; DM Mono for logo, labels, numbers and tables.
  Never DM Serif.
- **Bullets** are the small red square (▪), not round dots.
- **Layout** is asymmetric and editorial; the logo is never centred. Flat colour
  fields (white / beige / red), no gradients or textures. Small radii (2–10px);
  pills only for tags.
- **Copy** is Dutch, sentence case, no emoji. Institutional "wij" voice.
- **Icons**: Lucide (line icons) as a stand-in.
- `Tag` supports `red | navy | aqua | green | gray` — its `.d.ts` says `blue`,
  but the implementation uses `navy` (a `blue` tag silently falls back to red).

## Source of the design system

[design-system/](design-system/) is a copy of the organisation's
"IPE Design System" artifact (https://claude.ai/artifact/LBc7RZSkfVHFvNey8azUF2),
taken 2026-11-16. Left out: Word/PowerPoint/Excel templates, slide and print
templates, and extracted PDF page images. If the artifact is updated, re-pull the
changed files into `design-system/` instead of editing them here.
