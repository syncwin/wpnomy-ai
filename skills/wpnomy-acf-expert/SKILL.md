---
name: wpnomy-acf-expert
description: Design ACF schemas and bind ACF data into pages. Plans and generates importable ACF JSON (custom post types, taxonomies, field groups, options pages, repeaters, flexible content, clone and relationship fields) or writes them live through Novamira, then wires the fields into Bricks, Elementor, Oxygen 6 or Builderius. Use whenever the user mentions ACF, Advanced Custom Fields, acf-json, a field group, a CPT, a custom taxonomy, an options page, a repeater or flexible content; asks what fields or post types a site needs; asks for a field plan, schema or importable JSON; or asks how to show a custom field on a page or why one renders blank. Use it even without the word ACF when the request is about structuring WordPress content into fields on an ACF site. For Meta Box sites use wpnomy-metabox-expert.
license: MIT
metadata:
  displayName: "WPnomy ACF Expert"
  version: "0.1.6"
  author: "@wasimness"
  company: "SyncWin"
---

# WPnomy ACF Expert

Two jobs, in order: decide what the schema should be, then get its values onto a page.

| Job | Read |
|---|---|
| Designing a schema, generating or validating ACF JSON, writing objects to a site | `references/schema.md` |
| Getting an existing field onto a page | `references/binding.md` |

On a Bricks site, `references/binding.md` still decides the route (bound value or shortcode); the Bricks mechanics (tag preview, query loops, hide-on-empty conditions) are in `wpnomy-bricks-expert`'s `references/dynamic-data.md`.

On Oxygen 6, bind through Oxygen's native ACF dynamic data (`AcfField` family, see `wpnomy-oxygen-expert`); on Builderius, confirm its ACF support in the builder on the site first (`wpnomy-builderius-expert`). Build rules for every job: `${CLAUDE_PLUGIN_ROOT}/skills/wpnomy/references/house-rules.md`. Choosing between ACF and Meta Box: `wpnomy-metabox-expert` §"Meta Box or ACF".

Use ACF's native capabilities first. Do not rebuild in code what ACF already does.

## Delivery model

The same two routes the Elementor skills use. Ask which, and never assume.

**JSON files to import.** One file per object plus a combined array, written to the output directory. The user imports through ACF, Tools, Import, or drops the per-object files into the theme's `acf-json/`. Nothing is live.

**Direct on the site through Novamira.** Novamira's `acf-*` abilities create and edit field groups, post types, taxonomies and options pages in place, and read and write values. Check `novamira/acf-check-setup` first: managing post types, taxonomies and options pages through abilities needs ACF Pro 6.5 or later.

Either route, the schema rules in `references/schema.md` are the same. The route changes where the output lands, not what it says.

## Pairs with (Novamira skills, load with `novamira/skill-get`)

| Skill | Use it for |
|---|---|
| `acf-integration` | The discover, read, modify, write workflow and consent semantics for complex types |
| `dynamic-data-binding` | Binding a field into a builder widget, and the silent-failure patterns when one does not resolve |
| `content-model-schema` | Describing a schema in plugin-agnostic terms, for auditing or replicating it |
| `content-model-migration` | Moving a schema off ACF or onto it |

Load them for the mechanics. The schema decisions and house conventions here lead where they differ.

## Rules that apply to both jobs

**Read before writing.** On an existing site, list what is there and reuse existing keys verbatim. A changed key orphans every value already saved against it, silently, because ACF simply stops finding them.

**Never write on assumption.** If a field name, type or location is not confirmed, ask.

**Refuse php-sourced objects.** A field group registered in code cannot be edited through the API. Say so rather than producing an edit that appears to work.

**Field-group edits replace the fields array.** Any field absent from the payload is removed. Send the whole array, every time.

**Complex writes replace, not merge.** Repeaters, flexible content, galleries, clones and groups overwrite their entire previous content on write. Treat every one as destructive and confirm first.

**Permalinks are not reversible by apology.** See the permalink rule in `references/schema.md` before any post type or taxonomy change on a site with live URLs.

## Scratchpad

End with the router's scratchpad (`assets/build-scratchpad.md` in the wpnomy skill): every request with its status, the schema objects and bindings changed, and what was verified on the front end.
