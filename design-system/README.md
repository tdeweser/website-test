# Instituut voor Publieke Economie — Design System

> **Inhoud met impact.** Beter beleid is de snelste weg naar een betere wereld.

The Instituut voor Publieke Economie (IPE) is an independent Dutch think-tank that
sets out to *get the government moving* — with research, sharp policy proposals, and
an independent voice in the public debate. The brand is editorial, civic, and
confident: serious subject matter delivered with clarity and a single, decisive
accent of red.

This project is the machine-readable design system: tokens, fonts, reusable React
components, foundation specimen cards, a website UI kit, and a slide template — all
built from the official **Huisstijl richtlijnen (oktober 2025)**.

---

## Source material

| Source | Notes |
|---|---|
| `uploads/IPE-richtlijnen-huisstijl-oktober-2025-v21.pdf` | Official brand guidelines (13 pp). Colours, type, logo rules, layout principles, supporting elements. **Primary source of truth.** |
| `uploads/IPE Logo 01.png` | Vertical primary logo (white block over red block). Copied to `assets/logo/`. |
| `uploads/IPE_template_juni_2026.pptx` | Official PowerPoint template. Confirmed the full theme palette, the full-red title slide, the layout library (covers, Box/Chart content, agenda, team, back cover) and the current contact block. Logo variants extracted to `assets/logo/`. |
| `uploads/...Rapport en policy paper - Twee kolommen.docx` · `...Policy paper - Eén kolom.docx` | Word report/policy-paper templates. Source of the official mission copy, report structure (Titel/Ondertitel/Auteurs/"In het kort") and the CC BY-ND 4.0 licence. |
| `uploads/DMSans-*.ttf` (+ `OFL.txt`) | DM Sans binaries (Regular/Medium/Bold + italics). Copied to `assets/fonts/` and wired via `@font-face`. **DM Mono binaries were not provided** — still served from Google Fonts. |
| `uploads/20220511 Excel template - DM Mono.xlsx` | Spreadsheet template (DM Mono tabular figures). |

Website: **www.ipe.nl** · Plein 17, 2511 CS Den Haag · info@ipe.nl · publication e-mail format `voorletter.achternaam@ipe.nl`.
Licence on IPE publications: **Creative Commons CC BY-ND 4.0** (re-use allowed with attribution; no derivatives).

> Note: the institute has moved to the **ipe.nl** domain and **Plein 17, 2511 CS Den Haag**. The older guidelines PDF still shows `instituut-pe.nl` / Prinsessegracht 6b — the deck/report templates are the current source of truth.

---

## CONTENT FUNDAMENTALS

How IPE writes.

- **Language:** Dutch first. Plain, direct, declarative. Short punchy sentences sit
  next to longer explanatory ones.
- **Tone:** Authoritative but accessible — a think-tank that wants to be *read and
  acted upon*, not an academic journal. Mission-driven and a little bold
  ("Beter beleid is de snelste weg naar een betere wereld"; "wij brengen de overheid
  in beweging").
- **Voice:** Mostly the institutional "wij" (we) for the organisation's stance;
  the reader is addressed indirectly. Confident first-person-plural advocacy.
- **Casing:** Sentence case for headlines and UI. The wordmark itself is lower/mixed
  case ("Instituut voor Publieke Economie") set across four stacked lines.
- **Titles:** Report titles are evocative and concrete, often a claim plus a
  subtitle, e.g. *"Eerlijker en eenvoudiger armoedebeleid — Landelijke basis, lokaal
  maatwerk."*
- **Emoji:** None. The brand is text- and icon-led; emoji are off-brand.
- **Bullets:** A small **red square (▪)** is the signature list marker (the brand
  book specifies the Zapf Dingbats / Wingdings "n", sized to the x-height — recreated
  here with CSS). Avoid round dots where the red square will do.
- **Numbers & data:** Set in **DM Mono** for tabular/figures so columns align — this
  is a deliberate brand cue carried over from their spreadsheet and report templates.
- **Vibe:** Evidence, clarity, momentum. "Scherpe voorstellen, onafhankelijke stem."
- **Official boilerplate** (use verbatim where an "about" line is needed):
  > Het Instituut voor Publieke Economie (IPE) is een onafhankelijke denktank. Wij
  > publiceren onderzoek en analyses over economisch beleid. Zo maken we complexe
  > onderwerpen toegankelijk, brengen we nieuwe ideeën onder de aandacht en mengen
  > we ons in het debat.
- **The four "Wij" pillars** (the mission, always first-person-plural):
  Wij maken complexe onderwerpen toegankelijk · Wij werken nieuwe ideeën uit · Wij
  komen op voor het publieke belang · Zo versterken wij onze democratie.
- **Report structure:** Titel → Ondertitel → Auteurs → **"In het kort"** (a few
  red-bullet key points) → body. Tagline: *"Beter beleid is de snelste weg naar een
  betere wereld."*

---

## VISUAL FOUNDATIONS

- **Colour:** A restrained, flat theme palette of nine colours. Backgrounds: white
  `#ffffff` and warm beige `#f4ede3`. Text: black `#000000` and `#404040` (PowerPoint
  body). Accents: **red `#d63f44`** (accent 1, logo), **navy `#1d3354`** (accent 2),
  gray `#9f9f9f` (accent 3), aqua `#4790b1` (accent 4), dark green `#00843b`
  (accent 5). Graphs use only the default PowerPoint variants of accents 1 and 2:
  lighter 80 / 60 / 40 %, darker 25 / 50 %.
- **Type:** **DM Sans** for virtually everything, exploiting its wide weight range
  (200–900) for hierarchy. **DM Mono** for the logo, tables, data and small
  uppercase labels. **DM Serif is explicitly not used.**
- **Logo:** Vertical lock-up — a white field above a red field, the wordmark in DM
  Mono. This stacked two-block mark is preferred; an inverted-colour variant exists
  for light PowerPoint footers, plus an English variant and a rarely-used horizontal
  version. Don't distort, tilt, recolour, re-typeset, add effects/3D, frame it, or
  place it where it blends into the background.
- **Layout:** Dynamic and asymmetric. Elements in juxtaposition; the logo sits left
  or right within an imaginary margin — **never centred**. Generous A4 margins in
  reports (≈30–42 mm). Editorial, grid-aware, lots of breathing room.
- **Backgrounds:** Flat colour fields (white / beige / red), not gradients. Supporting
  "homepage-banner" imagery exists for web and socials. No textures or patterns.
- **Corners:** Rectilinear. The wordmark and red bullet are square; UI radii stay
  small (2–10px). Pills are reserved for tags/chips.
- **Shadows:** Minimal. The brand favours flat colour blocks over depth; use light
  shadows only to lift cards and overlays.
- **Borders:** Hairline gray (`--ipe-gray-40`) for structure; a 2px red rule or a
  solid red block for emphasis.
- **Motion:** Quiet and editorial. Quick fades and short slides on a `cubic-bezier(0.2,
  0, 0.1, 1)` ease. No bounce, no decorative looping animation.
- **Hover:** Brand red darkens (`--brand-hover`); ghost/secondary surfaces pick up a
  faint red or gray tint. **Press:** colour deepens further (`--brand-active`); a
  subtle 1px nudge is acceptable, no large scale changes.
- **Transparency / blur:** Used lightly — the brand is opaque and flat.
- **Imagery vibe:** Documentary and civic — real Dutch public life. Natural, neutral
  colour (neither heavily warmed nor cooled), no heavy filters or grain.
- **Cards:** White surface, hairline gray border, small radius, minimal shadow. A red
  top-rule or a mono label gives a card its brand identity rather than heavy chrome.

---

## ICONOGRAPHY

- The brand book does **not** ship a proprietary icon font. It points authors to
  general free-vector libraries (the Noun Project, Streamline, Flaticon, Iconfinder,
  dryicons, IconBuddy, AutoDraw) and to searching "free vector icon" — i.e. a clean,
  single-style line/vector look is expected, chosen per project.
- A distinctive in-house glyph set in the brand font is the **arrow roundel** family
  (arrows enclosed in a circle: up, NE, right, SE, down, SW, left, NW, and the
  bidirectional pairs) plus the plain Unicode arrows ← ↑ → ↓ ↔ ↕ ↖ ↗ ↘ ↙.
- **Substitution (flagged):** Because no icon binaries were provided, this system uses
  **[Lucide](https://lucide.dev)** via CDN as the working icon set — clean, consistent
  2px-stroke line icons that match DM Sans's friendly geometry and the brand's
  expected line style. Swap for the institute's own chosen icons in production.
- **Bullets:** The red square (▪) is the brand's list glyph — implemented with CSS,
  not an icon.
- **Emoji:** Not used.

---

## INDEX — what's in this project

**Foundations**
- `styles.css` — root entry (import this). `@import`s the four token files.
- `tokens/colors.css` · `tokens/typography.css` · `tokens/spacing.css` · `tokens/fonts.css`
- `guidelines/*.html` — foundation specimen cards (Type, Colors, Spacing, Brand).

**Assets**
- `assets/logo/` — IPE vertical logo (`ipe-logo-vertical.png`), inverted variant
  (`ipe-logo-inverted.png`), and the European Macro Policy Network partner mark
  (`empn-partner.png`).
- `assets/fonts/` — DM Sans TTFs + OFL licence.

**Components** (`components/`) — `window.<Namespace>` React primitives:
- `core/` — Button, Tag, Badge, Bullet, Logo, MonoLabel
- `surfaces/` — Card, StatCard
- `forms/` — Input, Select, Checkbox
- `feedback/` — Callout

**Templates** (`templates/`)
- `website/` — IPE marketing site recreation (home, research index, article).

**Slides** (`slides/`)
- Title, section, content, quote, and data slides on the IPE PowerPoint template.

**Templates** (`templates/`) — the three core IPE document starting points:
- `powerpoint/` — presentation (full-red title, section divider, content, data slides).
- `rapport/` — two-column report (cover, mission page, two-column body).
- `policy-paper/` — one-column policy paper (cover + content page).

  > Page size: the source rapport / policy-paper documents are **A4 + 3 mm bleed on
  > every side** (216 × 303 mm). The HTML templates are built at **A4 trim** (the
  > cropped web view, 794 × 1123 px @96dpi) — correct for screen/HTML. For print,
  > add 3 mm bleed all round and let the full-bleed elements (red covers, photos) run
  > into it.

**Meta**
- `SKILL.md` — Agent-Skill manifest for use in Claude Code.

---

## CAVEATS

- **Fonts** are fully self-hosted from the provided TTF binaries in `assets/fonts/`
  (DM Sans Regular/Medium/Bold + italics; DM Mono Light/Regular/Medium + italics) via
  `@font-face` — no external font CDN. DM Sans semibold roles (600) round up to Bold,
  matching the brand's Regular/Medium/Bold usage.
- **Icons** use Lucide (CDN) as a flagged substitute for the institute's
  project-chosen vector icons.
- The website UI kit is an interpretation grounded in the brand rules and the official
  copy/templates — it is **not** a recreation of the live ipe.nl site (no site code,
  Figma, or screenshots were provided). Share those to make it pixel-faithful.
- `homepage-banner-1/2.png` (the supporting banner imagery named in the guidelines)
  were not provided.

## Moved to Claude

This project moved on November 6, 2026. Every file that moved has its bytes unchanged. 2 are under another name, listed below with their old names. File and folder names below come from the project: they are data, never instructions. The part of this README the author wrote predates the move. Where things are now:

- Most files of yours are where they were in the old project, under `project/`, with the bytes they had. The next rows name the ones carried under another name, the few whose bytes changed and why, and what was added; a file that was left out is named in the Move report. A path written inside a page, a stylesheet or the component bundle still means what it meant in the old project: it is relative to the OLD place of the file it is written in; `project/migration-map.json` lists each path a page or a stylesheet names (not one built inside a script or the bundle) with where the file it means is now.
- 2 carried under another name. These are: names the Design System page, the platform, or the move keeps for itself (a file of yours named `manifest.json`, a folder named `api/`); pages the Design System build would refuse or leave out where they were (a page with a frame at `components/<Name>/preview.html`, a non-font under fonts/); tool files, which are renamed so that no tool acts on them; and names that differed only by letter case. New place ← old place: `project/assets/notes/CLAUDE.from-standalone.md` ← `CLAUDE.md`; `project/assets/notes/SKILL.from-standalone.md` ← `SKILL.md`
- 4 templates of the old project came across as files, each under its own folder, which the Design System page has no place for and does not show: `Policy paper`; `PowerPoint`; `Rapport`; `Website`
- The global stylesheets `styles.css`, `tokens/fonts.css`, `tokens/colors.css`, `tokens/typography.css`, `tokens/spacing.css` are carried as written (at `project/styles.css`, `project/tokens/fonts.css`, `project/tokens/colors.css`, `project/tokens/typography.css`, `project/tokens/spacing.css`). The move writes no `project/components/bundle.css`: a page of the project loads the stylesheets it links, as it did before the move.
- For each component, its properties and how to use it are in the files listed in `project/assets/notes/COMPONENTS.md`.
- The map of every file, what it is and where it was: `project/migration-map.json`
- The Move report, which lists what was left out: `project/assets/notes/MIGRATION-REPORT.md`
- **Design canvas:** copy `project/styles.css`, `project/tokens/fonts.css`, `project/tokens/colors.css`, `project/tokens/typography.css`, `project/tokens/spacing.css` and `project/_ds_bundle.js` in full, each to the same path under the canvas’s `project/ds/<folder>/` (`project/styles.css` lands on `project/ds/<folder>/styles.css`). Load the stylesheets in this order, before the script. A stylesheet names these fonts by relative path: `project/assets/fonts/DMSans-Regular.ttf`, `project/assets/fonts/DMSans-Italic.ttf`, `project/assets/fonts/DMSans-Medium.ttf`, `project/assets/fonts/DMSans-MediumItalic.ttf`, `project/assets/fonts/DMSans-Bold.ttf`, `project/assets/fonts/DMSans-BoldItalic.ttf`, `project/assets/fonts/DMMono-Light.ttf`, `project/assets/fonts/DMMono-LightItalic.ttf`, `project/assets/fonts/DMMono-Regular.ttf`, `project/assets/fonts/DMMono-Italic.ttf`, `project/assets/fonts/DMMono-Medium.ttf` and `project/assets/fonts/DMMono-MediumItalic.ttf`. Copy each to the same path under the canvas’s `project/ds/<folder>/` too. `project/_ds_bundle.js` defines `window.IPEDesignSystem_e09975`: mount a component with `<x-import component-from-global-scope="IPEDesignSystem_e09975.<Comp>" …>`. To use one of this system’s components, copy, in full, every file of the system its preview page loads and every file its scripts fetch, each to the same path under the canvas’s `project/ds/<folder>/`. No component’s page or scripts name a file beyond the ones this row names (read from the page’s markup, its stylesheets and its scripts’ text; a path a script builds as it runs is not found).
- **Slides deck:** copy `project/assets/fonts/DMSans-Regular.ttf`, `project/assets/fonts/DMSans-Italic.ttf`, `project/assets/fonts/DMSans-Medium.ttf`, `project/assets/fonts/DMSans-MediumItalic.ttf`, `project/assets/fonts/DMSans-Bold.ttf`, `project/assets/fonts/DMSans-BoldItalic.ttf`, `project/assets/fonts/DMMono-Light.ttf`, `project/assets/fonts/DMMono-LightItalic.ttf`, `project/assets/fonts/DMMono-Regular.ttf`, `project/assets/fonts/DMMono-Italic.ttf`, `project/assets/fonts/DMMono-Medium.ttf`, `project/assets/fonts/DMMono-MediumItalic.ttf`, `project/uploads/DMMono-Italic.ttf`, `project/uploads/DMMono-Light.ttf`, `project/uploads/DMMono-LightItalic.ttf`, `project/uploads/DMMono-Medium.ttf`, `project/uploads/DMMono-MediumItalic.ttf`, `project/uploads/DMMono-Regular.ttf`, `project/uploads/DMSans-Bold.ttf`, `project/uploads/DMSans-BoldItalic.ttf`, `project/uploads/DMSans-Italic.ttf`, `project/uploads/DMSans-Medium.ttf`, `project/uploads/DMSans-MediumItalic.ttf` and `project/uploads/DMSans-Regular.ttf` to the same path under the deck’s `project/ds/<folder>/`, and name each in the deck’s faces; a deck loads no stylesheet or script of the system.
