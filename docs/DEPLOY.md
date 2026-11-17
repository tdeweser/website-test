# Deployment

The site is hosted on **Cloudflare Pages**, project `ipe-dza`, deploying the GitHub repo
`tdeweser/website-test` from branch `main`. Preview URL: https://ipe-dza.pages.dev

## Cloudflare settings

Workers & Pages → **ipe-dza** → Settings → Build → Build configuration:

| Setting | Value |
|---|---|
| Framework preset | None |
| Build command | *(empty)*. The site is built locally and `public/` is committed. |
| Build output directory | `public` |
| Root directory | *(empty)* |

Every push to `main` deploys automatically, usually within a minute.

## Publishing a change

```bash
.venv/Scripts/python scripts/build.py
.venv/Scripts/python scripts/check.py     # must print OK
git add -A
git commit -m "Describe the change"
git push
```

## Search engines

While `noindex: true` in `content/site.yml`, the build writes:

- `public/_headers`: `X-Robots-Tag: noindex, nofollow` on every response (Cloudflare
  Pages applies `_headers` automatically);
- `public/robots.txt`: `Disallow: /`;
- a `<meta name="robots" content="noindex, nofollow">` tag on every page.

This keeps the test copy from competing with www.ipe.nl. When this site goes live on the real
domain, set `noindex: false`, set `base_url` to the real address, rebuild and push.
