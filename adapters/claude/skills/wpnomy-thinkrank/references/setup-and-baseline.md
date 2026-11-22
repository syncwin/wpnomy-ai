# Setup and the SEO baseline

## Contents
- First checks
- Baseline preset
- Sitemap, IndexNow and llms.txt

## First checks

1. `blog_public`: must be `1` on a live site. If it is `0`, per-type robots settings do nothing. Report it.
2. Fetch the live robots.txt and read it. Note any physical file that overrides the generated one.
3. Note any other active SEO plugin, and whether the theme or builder prints its own SEO tags (Bricks has its own SEO setting; see `rest-config.md`).
4. Back up the database before activation (export to a file outside the web root).

## Baseline preset

A brand-agnostic default. Apply it, then log each change away from it with a reason. Confirm any item that does not fit the site's business.

| Area | Setting |
|---|---|
| Indexing | `noindex` for internal search, author archives, date archives, blog tags, post formats and builder template taxonomies |
| Shop | Product categories indexed |
| Snippets | `max-snippet: -1` and `max-image-preview: large` |
| Sitemap | On, with images and featured images |
| Schema | Product schema on; shop archive schema off |
| Head | Generator tag removed |
| Links | External links open in a new tab |
| Instant indexing | IndexNow on for post, page and product (off by default) |
| llms.txt | On |

Apply the settings per entity through the matrix route (`rest-config.md`), not by guessing option names.

## Sitemap, IndexNow and llms.txt

- Before submitting a sitemap, scan it for demo or placeholder entries (slugs such as `demo-*` or `product-*`) and report them.
- The sitemap, schema and sitemap generate routes return 403 from PHP unless the REST nonce header is sent (`rest-config.md`). Without it, use the UI.
- `llms-txt/generate` needs `user_input` with `website_description`, `key_features`, `target_audience`, `business_type` and `technical_stack`. Ask the owner for these; never invent them.
- Auto delivery or disabling llms.txt can delete a physical `llms.txt` file. Copy it first.
