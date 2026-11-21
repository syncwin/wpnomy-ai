# Checks and known issues

## Contents
- Checks
- Known ThinkRank 2.21.x issues

## Checks

Run on the rendered front end, logged out.

1. `blog_public` is `1`; robots.txt reads as intended.
2. `<title>` and meta description on a post, a page, a product, a category and the front page.
3. Robots meta on each entity type matches the baseline.
4. Canonical and Open Graph tags present once.
5. JSON-LD: list the `@type` of every node with `<script[^>]*ld\+json`. No duplicates, and `BreadcrumbList` appears once.
6. Sitemap index loads; no demo or placeholder URLs; excluded types absent.
7. llms.txt loads and holds the owner's facts.
8. No PHP fatal on the home page, a post, a page, an archive and the shop (see the first issue below).
9. On a store: cart, checkout and `wp-json` return 200 after each activation.

## Known ThinkRank 2.21.x issues

| Issue | Handling |
|---|---|
| Fatal error in `SEO_Manager::apply_post_robots_override` when `get_the_ID()` is false | Check archives and non-post views for a fatal; report it to the plugin author; do not patch plugin files |
| content_blocks import converts only Rank Math FAQ blocks, not Yoast's | Rebuild Yoast FAQ blocks by hand |
| The Yoast move misses post-type noindex and sitemap exclusions | Redo both by hand |
| Auto delivery or disabling llms.txt deletes a physical file | Copy the file first |
| With Local SEO on, Organization and local-business nodes are split | Check output; merge by hand |
| The posts page ignores per-page SEO and social fields | Set titles through templates or accept the gap |
| No URL-pattern robots setting and no archive title or description templates | Use the matrix per entity; report the limit |
| `schema/settings`, `sitemap/settings` and generate return 403 from PHP without the nonce header | Send the header (`rest-config.md`) or use the UI |
