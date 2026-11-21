# Moving off Yoast

## Contents
- Order
- What the move misses
- After the move

## Order

1. Back up the database and note which Yoast settings and per-post data exist.
2. Save the live head and the sitemap URLs before the move, as a "before" record.
3. Run ThinkRank's import for Yoast data. Do not leave both plugins live longer than the import needs.
4. Deactivate Yoast only after the import is checked. Deactivate, do not delete, until the checks pass.

## What the move misses

ThinkRank 2.21.x does not carry everything across. Check each by hand and redo it in ThinkRank.

- Post-type `noindex` settings.
- Sitemap exclusions.
- FAQ blocks from Yoast: the content_blocks import converts only Rank Math FAQ blocks, so Yoast FAQ blocks stay as they were.
- Title and description for a static front page, which need the post meta `_thinkrank_seo_title` (see `rest-config.md`).

## After the move

- Compare the new head and sitemaps with the "before" record.
- Check redirects Yoast managed, if any.
- Check schema for duplicates (`schema.md`), because builder and custom JSON-LD often outlive the old plugin.
