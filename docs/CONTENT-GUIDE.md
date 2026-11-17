# Content guide

All content is Markdown with a YAML header ("front matter") in `content/`. After any change:

```bash
.venv/Scripts/python scripts/build.py && .venv/Scripts/python scripts/check.py
```

Then commit **both** your change and the regenerated `public/` folder.

> Running `scripts/scrape.py` overwrites `content/pages`, `content/highlights`,
> `content/events`, `content/people/authors.yml` and `static/media`. Once you edit content by
> hand, stop re-scraping, or re-apply your edits afterwards.

## Writing rules

- Dutch, sentence case, no emoji. The institutional voice is "wij".
- The site copies the look of the original ipe.nl. Don't add new colours, fonts or styles in
  content; use the section themes and classes described below.
- Use the official boilerplate where an "about" line is needed (see
  `design-system/README.md`).

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
image: /media/img/my-image.jpg          # thumbnail (blog index, listings)
listing_image: /media/img/figure.png    # optional: listings use this when there is no image
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

## Homepage

The homepage is `content/pages/home.md`. All its texts and settings are in the front matter
(there is no body), and `templates/home.html` renders them. The scraper never overwrites
this file.

| Key | What it controls |
|---|---|
| `hero` | `title`, the part of the title to underline in red (`underline`), `lead`, `image`, `buttons` (`style: line` = outline button), `note` |
| `publications` | heading, "Naar het archief" link, which `categories` count as publications (newest `count` shown, whatever their age) and the `articles` row (newest listed items in that category) |
| `topics` | heading, intro, and the four topic cards (`title`, `text`, `image`, `url`) |
| `media` | heading, intro (Markdown links allowed) and the `tag` whose items fill the photo slider |
| `wordmark` | the two lines of the large photo-filled "Publieke Economie" and the photo |
| `values` | "Wij staan voor" heading, intro and rows |
| `people` | heading, text and link; the people are those with `home: true` in `content/people/people.yml` |
| `support` | "Bevalt onze inhoud?" photo, newsletter and donate texts and buttons (the QR code comes from the old site) |

## Edit a permanent page

Pages live in `content/pages/<name>.md`. Their structure:

```markdown
<section class="band theme-white-bold height-medium" markdown="1">

<div class="fe-row" markdown="1">

<div class="fe-cell" style="--c: 1 / 13" markdown="1">

## Left column (columns 1–12 of 24)

Text …

</div>

<div class="fe-cell" style="--c: 14 / 25" markdown="1">

Right column (columns 14–24)

</div>

</div>

{{ listing(tag="Wonen", limit=4, layout="carousel", meta1="cats", meta2="date", meta_pos="above-title") }}

</section>
```

Keep a blank line after every opening `<section>`/`<div … markdown="1">` and before its
closing tag. Otherwise the Markdown inside is not converted.

| Class | Effect |
|---|---|
| `theme-white`, `theme-white-bold` | white section; `-bold` makes headings red |
| `theme-light`, `theme-light-bold` | beige section |
| `theme-dark` | navy section, white text |
| `theme-bright` | red section, white text |
| `height-small` / `-medium` / `-large` | vertical padding of the section |
| `band--image` + `style="--band-image: url(/media/img/x.jpg); --overlay: .3"` | background photo |
| `<div class="block-bg">` | beige box around a block |
| `<div class="align-center">`, `text-large`, `text-small`, `text-white`, `text-accent` | text styling |

Buttons: `<p class="button-row align-left"><a class="button" href="/steun-ons/">Steun ons</a></p>`.
Collapsible Q&A: `<details class="accordion" markdown="1"><summary>Vraag</summary> … </details>`.

## Add a new page

1. Create `content/pages/<name>.md` with `title`, `url` (e.g. `/nieuw/`) and `layout: page`.
2. Add it to the menu in `content/site.yml → nav` if it should be there.

## People

**Team page and homepage.** `content/people/people.yml` lists everyone on "Onze mensen",
grouped in display order (Kernteam, Fellows, Raad van Advies, Bestuur). Per person:

```yaml
- name: Julia van Rijn
  role: Onderzoeker
  bullets: [Onderzoekt diverse onderwerpen …, …]
  links:
  - { title: LinkedIn, url: "https://www.linkedin.com/in/…" }
  photo: /media/img/julia-c3685704.png
  ringed: true   # the photo file already has a red ring baked in
  home: true     # also show under "De mensen achter IPE" on the homepage
```

Every photo is shown as a circle with a red ring, whatever its original shape. To add
someone, put a square-ish photo in `static/media/img/` and add an entry. Each person gets
an anchor on the team page (`/onze-mensen/#julia-van-rijn`). The page intro is in
`content/pages/onze-mensen.md`.

**Author cards** in articles come from `content/people/authors.yml` (`name`, `role`,
`email`, `photo`, `url`). The name must exactly match the tag used on articles.

## Navigation and footer

Edit `content/site.yml`. In `nav`, an entry with `url` is a plain link and an entry with
`items` is a dropdown folder; Home and English are left out of the header (the logo is
Home, English sits under the NL/EN picker, `languages`). `cta` is the red "Steun ons"
button. The footer uses `footer` (tagline, link columns, KvK/RSIN), `anbi_note`, `contact`
and `social`; its layout is in `templates/partials/footer.html`.
