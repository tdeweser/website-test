The IPE action button — rectilinear, DM Sans medium, red as the hero accent. Use for primary and secondary actions across product and marketing UI.

```jsx
<Button variant="primary" size="md">Lees het rapport</Button>
<Button variant="secondary" iconRight={<ArrowIcon />}>Meer weten</Button>
<Button variant="ghost" size="sm">Annuleren</Button>
```

Variants: `primary` (solid red), `secondary` (red outline, red text), `ghost` (quiet, neutral hover), `dark` (solid black). Sizes: `sm` / `md` / `lg`. Props: `iconLeft`, `iconRight`, `disabled`, `fullWidth`. Hover darkens red; press nudges down 1px. Keep labels in sentence case.
