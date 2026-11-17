# Content guide

All content is Markdown with a YAML header ("front matter") in `content/`. After any change:

```bash
.venv/Scripts/python scripts/build.py && .venv/Scripts/python scripts/check.py
```

Then commit **both** your change and the regenerated `public/` folder.

> Running `scripts/scrape.py` overwrites `content/pages`, `content/highlights`,
> `content/events`, `content/people/authors.yml` and `static/media`. Once you edit content by
> hand, stop re-scraping, or re-apply your edits afterwards.

## Writing rules (from the IPE design system)

- Dutch, sentence case, no emoji. The institutional voice is "wij".
- Bullets are the red square, which you get automatically with a Markdown `- ` list.
- Use the official boilerplate where an "about" line is needed (see
  `design-system/README.md`).
- Don't add colours or fonts. The styles come from the design-system tokens only.

## Add an article

Create `content/highlights/YYYY-MM-DD-<slug>.md`:

```markdown
---
title: Een betere vermogenswinstbelasting
url: /highlights/vermogenswinstbelasting/
date: 2026-10-22
in_window: true            # true = appears in listings
categories: [Artikel, Sociaal beleid en belastingen]
tags: [Vinzenz Ziesemer, Belastingen]
author: Vinzenz Ziesemer
featured: true             # optional: picked up by listings with featured=True
image: /media/img/my-image.jpg
excerpt: One or two sentences shown on cards and in the feed.
external_url: https://…    # optional, for media items: adds a "Bekijk bij de bron" button
---

Body in Markdown. Shortcodes such as {{ authors(["Vinzenz Ziesemer"]) }} work here.
```

| Field | Notes |
|---|---|
| `categories` | The **kind** (`Rapport`, `Policy paper`, `Artikel`, `Opinie`, `In de media`) is the card label. The **topic** (`Macro-economie`, `Sociaal beleid en belastingen`, `Europese Unie`, `Functioneren overheid`) drives "Lees ook". |
| `tags` | Subjects (`Wonen`, `Begrotingsbeleid`, …) and author names. Each gets a page at `/highlights/tag/<slug>/`, and topic pages filter on them. |
| `in_window` | Only `true` items appear in listings, the archive and the feed. |

Put images in `static/media/img/` and PDFs in `static/media/files/`, and link them as
`/media/img/…` and `/media/files/…`.

## Edit a permanent page

Pages live in `content/pages/<name>.md`. Their structure:

```markdown
<section class="band band--alt" markdown="1">      <!-- band, band--alt, band--dark, band--image -->

## Heading

Text …

<div class="cols" style="--cols: 1fr 1fr" markdown="1">
<div class="cols__cell" markdown="1">

Left column

</div>
<div class="cols__cell" markdown="1">

Right column

</div>
</div>

{{ listing(tag="Wonen", limit=4, layout="carousel") }}

</section>
```

Keep a blank line after every opening `<section>`/`<div … markdown="1">` and before its
closing tag. Otherwise the Markdown inside is not converted.

Buttons: `<p class="button-row"><a class="button" href="/steun-ons/">Steun ons</a></p>`.
Collapsible Q&A: `<details class="accordion" markdown="1"><summary>Vraag</summary> … </details>`.

## Add a new page

1. Create `content/pages/<name>.md` with `title`, `url` (e.g. `/nieuw/`) and `layout: page`.
2. Add it to the menu in `content/site.yml → nav` if it should be there.

## People

Author cards are in `content/people/authors.yml` (`name`, `role`, `email`, `photo`,
`url`). The name must exactly match the tag used on articles. The team page itself is
`content/pages/onze-mensen.md`.

## Navigation and footer

Edit `content/site.yml`: `nav`, `cta`, `contact`, `newsletter`, `social`, `footer_links`.
