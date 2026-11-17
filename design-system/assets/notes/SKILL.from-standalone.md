---
name: ipe-design
description: Use this skill to generate well-branded interfaces and assets for the Instituut voor Publieke Economie (IPE), either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the README.md file within this skill, and explore the other available files.
If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.
If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## Quick map
- `readme.md` — full brand guide: context, content fundamentals, visual foundations, iconography, index.
- `styles.css` — link this one file to get all tokens + fonts. It `@import`s `tokens/*.css`.
- `tokens/` — `colors.css`, `typography.css`, `spacing.css`, `fonts.css`.
- `components/` — React primitives (Button, Tag, Bullet/BulletList, MonoLabel, Logo, Card, StatCard, Input, Checkbox, Callout). Each has a `.prompt.md` with usage.
- `guidelines/` — foundation specimen cards (colour, type, spacing, brand).
- `templates/website/` — interactive website recreation (home, publications, article).
- `slides/` — sample PowerPoint-style slides (title, section, content, data, quote).
- `assets/logo/` — IPE logo (vertical + inverted) and the EMPN partner mark; `assets/fonts/` — DM Sans TTFs.

## Brand in one breath
Editorial, civic, confident. White + black do the work; **red `#d63f44`** is the single
hero accent; **beige `#f4ede3`** is the warm alt background; aqua/green/blue are data
accents. **DM Sans** everywhere, **DM Mono** for the logo, labels and figures (DM Serif
is never used). Rectilinear, asymmetric layouts; the **red square (▪)** is the bullet.
Dutch copy, sentence case, no emoji.
