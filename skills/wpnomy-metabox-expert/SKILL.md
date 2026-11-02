---
name: wpnomy-metabox-expert
description: Plan and build Meta Box data models (field groups, custom post types, taxonomies, settings pages, relationships and custom tables) and connect the fields to Bricks, Oxygen 6, Builderius or Elementor without black boxes. Use when the site runs Meta Box or Meta Box AIO, when the user says Meta Box, metabox, rwmb_meta, rwmb_meta_boxes, MB Builder, MB Custom Table, MB Views, MB Relationships, MB Blocks, MB Settings Page, Meta Box abilities, custom fields with Meta Box, moving from ACF to Meta Box, or asks whether to use Meta Box or ACF, or when the wpnomy router sends Meta Box work here. Not for ACF itself (wpnomy-acf-expert) or for page layout (the builder's expert skill).
license: MIT
metadata:
  displayName: WPnomy Meta Box Expert
  version: 0.1.3
  author: "@wasimness"
  company: SyncWin
---

# WPnomy Meta Box Expert

Checked on Meta Box AIO 3.13.1 (Meta Box core 5.15.3) with Bricks 2.4.4. On another version, re-check each step on the site first.

**Needs:** `${CLAUDE_PLUGIN_ROOT}/skills/wpnomy/references/house-rules.md` (read it first; work type "Data model"). Site access to check versions and the edit screens. Layout work goes to the builder's expert skill.

## 1. Confirm the stack

Record the Meta Box core version (`RWMB_VER`) and which extensions are on. In Meta Box AIO they are listed in the `meta_box_aio` option (`extensions`): for example `meta-box-builder`, `mb-custom-post-type`, `mb-custom-table`, `mb-relationships`, `mb-views`, `mb-blocks`, `mb-settings-page`, `meta-box-group`, `meta-box-conditional-logic`, `mb-term-meta`, `mb-user-meta`, `mb-acf-migration`, `mb-elementor-integrator`. Use only what is on; never turn on an extension or install a plugin without the owner's approval.

Definitions made in the UI are posts: `meta-box` (field groups), `mb-post-type`, `mb-taxonomy`, `mb-relationship`, `mb-views`, `mb-settings-page`.

## 2. Write through the official abilities first

Meta Box registers WordPress abilities (Abilities API), so an MCP client such as Novamira can call them directly. Prefer them over PHP or database writes: they validate input and save the same way the UI does.

| Area | Abilities (`meta-box/…`) |
|---|---|
| Post types | `get-post-types`, `create-post-type` (`title`, `settings`), `update-post-type` (`id`; settings are merged), `delete-post-type` |
| Taxonomies | `get-taxonomies`, `create-taxonomy`, `update-taxonomy`, `delete-taxonomy` |
| Field groups | `list-field-groups`, `get-field-group` (`id`), `create-field-group` (`title`, `slug`, `fields`, `settings`), `update-field-group`, `delete-field-group` |
| Fields | `list-fields`, `get-field`, `create-field` (`field_group_id`, `field`), `update-field` (`field_id`; changing `field.id` renames the field), `delete-field`, `move-field` (`before` / `after`) |
| Values | `get-field-value-format` (call first to learn the value shape, including clone and multiple), `get-field-value`, `update-field-value`, `delete-field-value` (`field_id`, `object_id`, `object_type`) |

- Every `delete-*` ability is destructive (`force` deletes permanently instead of trashing): snapshot first and confirm with the owner each time.
- Renaming a field with `update-field` does not move stored values; treat it as a migration.
- Post and term content abilities for a single post type or taxonomy exist only after "Enable abilities" is turned on in that post type's or taxonomy's Features settings.
- Read results back with the matching `get-*` ability.

## 3. Choose where the definition lives

| Choice | Use when | Note |
|---|---|---|
| **MB Builder** (UI, or the abilities above) | the owner or a client edits fields in wp-admin | export the field group JSON into the repo or a FluentSnippets backup |
| **Code** (`rwmb_meta_boxes` filter) | fields must be versioned with a plugin or theme | site-side code goes in FluentSnippets, plugin code in its repo |

Never define the same field group in both. Field IDs are permanent once content exists: renaming one orphans the stored data.

## 4. Field groups in code

```php
add_filter( 'rwmb_meta_boxes', function ( $meta_boxes ) {
	$meta_boxes[] = [
		'title'      => __( 'Event details', 'text-domain' ),
		'id'         => 'event_details',
		'post_types' => [ 'event' ],
		'fields'     => [
			[ 'id' => 'event_date', 'name' => __( 'Date', 'text-domain' ), 'type' => 'date' ],
			[ 'id' => 'event_venue', 'name' => __( 'Venue', 'text-domain' ), 'type' => 'text' ],
		],
	];
	return $meta_boxes;
} );
```

- Field IDs: lowercase snake_case, prefixed by the group's purpose, never by a counter.
- Every visible string goes through `__()` with the project's text domain.
- Prefer native field types; use `custom_html` only with a recorded reason.

## 5. Reading values

- `rwmb_meta( $field_id, $args, $object_id )`. `$args` takes `size` for images, `object_type` (`term`, `setting`, `user`) for non-post data, and `storage_type` + `table` for custom tables. `$object_id` is the post, term or user ID, or the option name for a settings page.
- `rwmb_get_value()` returns the stored value (a select's key); `rwmb_the_value()` returns display HTML (a select's label). `rwmb_meta()` acts like `rwmb_the_value()` for oEmbed and map fields and like `rwmb_get_value()` otherwise.
- Escape on output (`esc_html`, `esc_url`, `wp_kses_post`).

## 6. Custom tables (MB Custom Table)

Use custom tables for many records or for fields queried often.

- Create the table with `MetaBox\CustomTable\API::create( $table, $columns, $keys )` on plugin activation (or `init`). Don't define `ID`; the extension adds it. Column names equal field IDs, one column per field.
- Point the field group at it: `'storage_type' => 'custom_table', 'table' => 'my_table'`. In MB Builder, add these as custom attributes on the group's Settings tab.
- Read with the same `storage_type` and `table` passed to `rwmb_meta()` or `[rwmb_meta]`.

Limits to tell the owner before choosing it:

- `WP_Query` meta queries don't work; query the table for IDs, then use `post__in`.
- Group fields are one serialized column; you can't query their sub-fields with SQL.
- Indexing `TEXT`/`LONGTEXT` columns needs a prefix length.
- Custom models have no permalinks or front-end templates.
- Limited compatibility with MB Relationships and MB Views.

## 7. Output on the front end (no black boxes)

Apply house rules §5 to the output, not just the layout:

- **Builders first.** Bind fields through the builder's native dynamic data; the builder's expert skill owns the layout.
  - **Bricks:** native Meta Box provider; tags look like `{mb_<post type>_<field id>}`. Pick the exact tag from Bricks' dynamic data list instead of typing it.
  - **Oxygen 6:** native Meta Box fields (`MetaboxField` and its checkbox, file, gallery, group, image, map, oEmbed, post, taxonomy, user and video variants).
  - **Elementor:** through the `mb-elementor-integrator` extension when it is on.
  - **Builderius:** not checked yet; confirm on the site before relying on it.
- **MB Views** (Twig templates) only when no builder handles it; its markup must still be plain elements with BEM classes and variables.
- **MB Blocks** for editor blocks: describe the exact output HTML first (house rules §5 questions).
- **Never** use `[rwmb_meta]` shortcodes or MB Views output to hold layout inside a builder; bind the data to native elements.

## 8. Meta Box or ACF

| Need | Lean to |
|---|---|
| Custom tables, very many records | Meta Box (MB Custom Table) |
| Relationships stored both ways in their own table | Meta Box (MB Relationships) |
| Fields in a plugin's code, versioned | either; Meta Box's `rwmb_meta_boxes` array is plain PHP |
| The builder only supports one natively | that one |
| The client already knows one | that one |

State the reason in one line. Moving data between them is a migration (house rules §1): use Meta Box's own `mb-acf-migration` extension (or `mb-toolset-migration` from Toolset) when it is on, snapshot first, map every field ID and type, and check every edit screen and front-end output after.

## 9. Check

1. Open the edit screen for each post type, term or settings page: the fields appear, save and reload.
2. Load a front-end page that shows each field.
3. For custom tables, confirm the rows were written (`SELECT` by ID).
4. Run the router's hand-over checklist (house rules §7).

Next: hand layout to the builder's expert skill, or report to the owner and finish with the router's scratchpad.

## Scratchpad

End with the scratchpad: every request with its status (done, partly done, in progress, failed, not started, needs you), then the field groups, tables and bindings changed, what was verified on the site and what was not, and the Meta Box version and extensions checked.
