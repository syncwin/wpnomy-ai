# Dynamic data, loops, filters and conditions

## Contents

Which route · Tags · Query loops · Global queries · Query filters · Element conditions · Test records

Field design belongs to `wpnomy-acf-expert`, and so does the choice between a bound value and a shortcode. This file is how a chosen value reaches a Bricks page.

## Which route

| Value | Route |
|---|---|
| A single value: heading, figure, label, link, image | Bricks dynamic tag bound to the ACF field or options field |
| A value inside a sentence | The data plugin's shortcode inside a `text` element. Never build a sentence from text before and after a tag |
| Rows: repeater, relationship, post type | A query loop |
| Long rich text from a field | `text` (Rich Text) with the tag, never `text-basic` with `tag: "p"` |

No figure, phone, address, credential or date is typed into an element.

## Tags

- Syntax: `{tag}`, `{tag:modifier}`, `{tag:modifier:arg}`, chained with colons. The pipe is only for `array_value|key` (`{acf_link:array_value|url}`).
- ACF fields by field **name**: `{acf_<name>}`. A tag resolves only where its field group is assigned.
- Options-page fields, relationship outputs and select values have their own forms. Do not write them from memory.
- `{cf_<meta_key>}` reads any post meta. Modifiers: `:plain`, `:raw`, `:value` (a select's stored value), date formats (`{post_date:M j, Y}`), `:array_value|key`. Never a `|upper` style pipe.
- Parser keys `@fallback`, `@sanitize` and `@key` exist; there is no `@post_id`, `@term_id` or `@user_id` override. Preview a specific record by passing `postId`.
- An ACF Relationship or Post Object field returns ids: loop over it with a Posts loop whose include is set to the field's dynamic data. Writing `{acf_rel}` into text prints ids.
- `[render_dynamic_data content="..."]` renders Bricks tags outside Bricks output.

The sequence, every time, before a tag goes into an element:

1. `bricks/list-dynamic-data-tags` with a `postId` of the target type. Copy the exact tag.
2. `bricks/preview-dynamic-tag` with `{ tag, postId, context: "text" }`.
3. `unknownTags` not empty means the tag prints as literal text on the live site. Stop and fix it.
4. `isEmpty: true` is either missing data or the wrong context. Preview on a record known to have the value.

Preview cannot simulate repeater rows, terms or users. Those are verified in the real loop on the front end.

## Query loops

- The loop goes on a `section`, `container`, `block` or `div` with `hasLoop: true` and a `query`. **The looping element is the repeated item.** The grid that lays out the cards goes on its non-looping parent; a grid on the loop element makes one grid per card.
- Get the `objectType` from `bricks/list-query-loop-types`. ACF repeater, relationship and flexible content loops use exact runtime keys; never guess one from a field label.
- Query shape: `{ "objectType": "post", "postType": ["city"], "posts_per_page": 12, "orderby": "...", "order": "ASC", "meta_query": [...], "tax_query": [...] }`. `query: null` and a query without `objectType` are rejected.
- Inside a loop, tags resolve against the current row or post. Terms loops: `{term_id}`, `{term_name}`, `{term_url}`, `{term_description}`, `{term_meta:key}`. Users loops: `{wp_user_display_name}` and the like. Array loops: `{query_array @key:'name'}`.
- Media is not an object type: a Posts loop on `attachment`, with `{post_id}` as the image source (`{featured_image}` does not work there).
- Include or exclude through dynamic data needs the loop's post type to match the field's referenced type, or the loop returns nothing silently.
- Random order with pagination needs a non-zero `randomSeedTtl` (default 60 minutes).
- Never loop a Template element inside another loop; wrap the content in a block.
- Nested loops do not inherit the outer context automatically.
- Load more: an interaction `{ "trigger": "click", "action": "loadMore", "loadMoreQuery": "<queryElementId>" }`.
- Custom query logic goes in the `bricks/posts/query_vars` hook in a FluentSnippets PHP snippet (`<prefix>-query-vars`), scoped by its `$element_id` argument (the 6-character id), keeping existing `meta_query` and `tax_query`. Never Custom Query PHP in the builder.
- `cacheQueryLoops` keeps results for one minute and helps only with a persistent object cache.
- Posts loops: add `ID` as a secondary orderby; only one main-query loop per page; turn on "Disable query merge" in headers, footers and sidebars.
- Pagination, load more and filters rely on loop markers: the server adds a `data-brx-loop-start` attribute to the loop wrapper and front-end JS turns it into a `<!--brx-loop-start-<queryId>-->` comment. Check both (page source and live DOM). An optimiser that strips or rewrites either breaks them silently.
- Empty loop checklist: saved; query valid; post type matches; children visible; tags loop-aware; markers intact; no `bricks/query/run` filter emptying it.

## Global queries

- `bricks/create-global-query` `{ label, category?, query }`; `category` is an id from `bricks/create-global-query-category` `{ name }`.
- `bricks/update-global-query` `{ queryId, label?, category?, query? }`; passing `query` replaces the whole settings object.
- Bind with `bricks/update-element` `settings: { query: { id: "<globalQueryId>" } }`; inline args are then ignored.
- `bricks/delete-global-query` does not unlink consumers: they fall back to their local query or render empty. Clear references first.
- Never hard-code a post id in a global query; use `{post_id}` or the hook.

## Query filters

For listings and projects. Builder-bound (server logic), styled by classes only.

- Turn on `enableQueryFilters` in global settings first.
- Elements: `filter-checkbox`, `filter-radio`, `filter-select`, `filter-range`, `filter-search`, `filter-datepicker`, `filter-submit` (`filterButtonType` apply or reset), `filter-active-filters`.
- **Every filter, Active Filters included, needs its own `filterQueryId`** (the target loop element's id), or it silently does nothing. Quick fix `bricks/set-filter-target-query`; full config `bricks/update-filter-element`; read with `bricks/list-query-filters` and `bricks/get-filter-element`.
- Sources in `filterSource`: `taxonomy` (`filterTaxonomy`, term include and exclude, order), `wpField`, `customField` (`sourceFieldType`, `customFieldKey`, for ACF meta).
- Checkbox, radio, select, range and datepicker read the index table. Reindex after bulk imports, after adding a filter on an existing field, or after changing field structure (`bricks/reindex-filters`, then confirm with `list-query-filters`). Serialized or array ACF values need the `bricks/query_filters/custom_field_index_rows` hook to expand.
- Nested loops and `bricks/query/run` loops need the `useQueryFilter` opt-in on the query element.
- Keep filters and their loop together at page or template level. Duplicating a section or component changes the loop id and breaks the link.
- Search filters run `LIKE` on title and content: slow on large sets.
- Verify after the AJAX result: expected records, empty state, changed selection, pagination.

## Element conditions

`settings._conditions` is an array of OR groups, each an array of AND items: `{ key, compare, value }`, with real booleans and integer ids. Operators: `==`, `!=`, `>=`, `<=`, `>`, `<`, `contains`, `contains_not`, `empty`, `empty_not`. Write them with `bricks/update-element-conditions`, which replaces the set, validates and keeps a revision. Never save `[[]]`, which is always true. Template condition shapes (`{ main: ... }`) never go here.

**Hide on empty** is required for every bound element (house rule). A missing figure hides its row; it never shows a blank or a zero.

| Case | Condition on the wrapper |
|---|---|
| A field | `[[{ "key": "dynamic_data", "dynamic_data": "{acf_<name>}", "compare": "empty_not" }]]` |
| A loop | `[[{ "key": "dynamic_data", "dynamic_data": "{query_results_count:<loopElementId>}", "compare": ">", "value": "0" }]]` on the loop's parent, with the raw 6-character id |

Conditions are render logic only: never styling and never responsive visibility (a utility class does that, policy 2.4). They remove markup; they do not secure it. Anything that must not reach a visitor is a capability or data question, not a condition. Conditions on the loop count are not re-run after AJAX filtering.

## Test records

Every template is checked logged out against one complete record and one sparse record before it is used. Most template defects are missing-value defects, and the complete record hides all of them.
