# Configuring through REST from PHP

Validated on ThinkRank 2.21.2 with `rest_do_request` run from Novamira PHP.

## Contents
- Nonce header
- Routes
- Titles and templates
- Builder SEO off

## Nonce header

Send `X-WP-Nonce: wp_create_nonce('wp_rest')`, as an admin user (the Bricks `known-issues.md` explains the user 0 problem). Without it the route returns 403 "Invalid security token". With it, `sitemap/settings`, `schema/settings` and `sitemap/generate` work from PHP. If a route still returns 403, set the option in the UI and report it.

## Routes

| Route | Use |
|---|---|
| `global-seo/matrix` POST | `{ entity, settings: { sitemap_include, robots_meta_enabled, robots_meta } }` per entity |
| `instant-indexing/settings` | IndexNow, off by default |
| `woocommerce/settings` | Shop options |
| `sitemap/settings`, `schema/settings`, `sitemap/generate` | Need the nonce header |
| `llms-txt/generate` | Needs `user_input` (see `setup-and-baseline.md`) |

Read each setting back after a write.

## Titles and templates

Nothing changes in the rendered title until per-entity templates are stored. The separator setting alone did not change the `<title>` on a Bricks page, because the separator still came from WordPress core. Check who owns the title.

Store templates with `\ThinkRank\SEO\Content_Type_Settings::update_entity_settings( $key, $patch )`, which merges.

- Post types `post`, `page`, `product`: `title`, `description`, `schema_type`, `article_type`, `archive_title`. For `product`, `archive_title` is the shop title.
- Taxonomies, key `taxonomy:<tax>`: `title` and `description`, with `%term%`, `%sep%`, `%sitename%` and `%term_description%`.
- A static front page needs the post meta `_thinkrank_seo_title`.

## Builder SEO off

When Bricks is the builder, its own SEO output must be off (`bricks_global_settings.disableSeo`), or it competes with ThinkRank. Change it only with a yes and read it back.
