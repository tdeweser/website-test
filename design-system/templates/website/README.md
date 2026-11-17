# Website UI kit — Instituut voor Publieke Economie

An interactive recreation of the IPE marketing/think-tank website, built on the
design-system components. Open `index.html` and click through:

- **Home** — hero ("Inhoud met impact"), featured report cover,
  a mono-figure stats strip, a recent-publications grid, and a themes / approach band
  on the beige alternative background.
- **Publications** — filterable index of reports & policy papers (filter by theme).
- **Article** — report detail with author/date metadata,
  callouts, DM Mono stat cards, and the red-bullet proposal list.

Navigate: header nav switches Home ↔ Publications; any publication card/row opens the
Article view.

## Files
- `index.html` — interactive shell + router.
- `parts.jsx` — `Icon` (Lucide), `Header`, `Footer`.
- `Home.jsx`, `Publications.jsx`, `Article.jsx` — screens.
- `data.js` — sample publications, themes and stats (fictional, on-brand).

## Notes
- Composes the DS primitives (`Button`, `Tag`, `MonoLabel`, `Card`, `StatCard`,
  `Callout`, `BulletList`, `Logo`) from `window.IPEDesignSystem_e09975`.
- Icons via **Lucide** (CDN) — a flagged substitute for the institute's
  project-chosen vector icons (see root readme → ICONOGRAPHY).
- This is an interpretation grounded in the brand guidelines (asymmetric layout,
  beige alt background, DM Mono labels/data) — no production site code or Figma
  was provided.
