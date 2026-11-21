# Schema and JSON-LD

## Contents
- One source per node
- Adding or changing schema
- Retiring builder or custom JSON-LD
- Duplicate BreadcrumbList

## One source per node

Each schema type should come from one place. Choose ThinkRank as the source and remove the others.

## Adding or changing schema

- Use ThinkRank's schema filters, not a second plugin or hand-written script tags. Read the filter names in the plugin source on the site; they vary by version.
- Per-entity schema type and article type are set in the entity settings (`rest-config.md`).
- With Local SEO on, Organization and local-business nodes are split in 2.21.x. Check the output and merge by hand if the nodes should be one entity.

## Retiring builder or custom JSON-LD

1. List every JSON-LD source: ThinkRank, the builder, the theme, WooCommerce, snippets and custom code.
2. Fetch the rendered page and list each node by `@type`.
3. For each duplicate, keep ThinkRank's node and turn off the other source. Prefer a native setting on the builder element or the plugin over a snippet.
4. Remove only code this task identified, after a backup.
5. Re-fetch and check again.

**Verify with a regex that allows any attribute order:** `<script[^>]*ld\+json`. A regex that assumes `type` is the first attribute misses scripts.

## Duplicate BreadcrumbList

ThinkRank and WooCommerce can both print a `BreadcrumbList` on products. The native fix on Bricks: swap the `woocommerce-breadcrumbs` element (it prints the Woo schema) for the native `breadcrumbs` element.

- Keep the old settings and classes on the new element.
- Add `singularStructure` with `[{ postType: [product], showTaxonomy: true, taxonomy: product_cat, showParentTerms: true }]` (adjust to the site's taxonomy).
- The SEO plugin is then the only breadcrumb schema source.
- Prefer this native swap over a snippet.
