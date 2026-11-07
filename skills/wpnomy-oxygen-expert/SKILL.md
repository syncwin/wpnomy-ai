---
name: wpnomy-oxygen-expert
description: Build and edit Oxygen 6 pages, templates, headers, footers, components and design systems under the house black box policy, and map Atomic Framework variables, classes and breakpoints into Oxygen. Use when the site runs Oxygen 6 (the Oxygen plugin on the Breakdance engine), when the user says Oxygen, Oxygen 6, Oxygen template, Oxygen component, Oxygen variables, selectors, custom breakpoints, Breakdance Elements for Oxygen, Breakdance Forms, Oxygen Doctor, or pastes Oxygen JSON, or when the wpnomy router sends Oxygen work here. Covers native elements, variables and collections, selectors and classes, components, breakpoints, dynamic data from ACF or Meta Box, the form fallback, and front-end checks. Not for Oxygen Classic (4.x), Breakdance itself, Bricks or Elementor.
license: MIT
metadata:
  displayName: "WPnomy Oxygen Expert"
  version: "0.1.8"
  author: "@wasimness"
  company: "SyncWin"
---

# WPnomy Oxygen Expert

Checked on Oxygen 6.2.1 with Breakdance Elements for Oxygen 1.1.0 and Breakdance Forms for Oxygen 1.1.0. On another version, re-check each step on the site first.

**Needs:** `${CLAUDE_PLUGIN_ROOT}/skills/wpnomy/references/house-rules.md` (read it first; it holds the order, the black box policy and the checklist). Site access through Novamira (or another way to run PHP and open the builder). Without site access, deliver the plan and exact output marked unverified.

## 1. Confirm the stack

Run on the site and record the result:

```php
defined('BREAKDANCE_MODE') && BREAKDANCE_MODE === 'oxygen'   // Oxygen 6, not Breakdance or Oxygen Classic
function_exists('\Breakdance\Variables\saveVariables')      // variables API present
```

Also note whether Breakdance Elements for Oxygen (the `EssentialElements\*` pack) and Breakdance Forms are active. Their absence changes §5 and §7.

## 2. Native elements (use these)

Oxygen's own elements are `OxygenElements\*`:

| Need | Element | Notes |
|---|---|---|
| section, div, any tag | `Container` | any tag through `settings.advanced.tag` |
| linked box | `ContainerLink` | URL in `content.content.url` |
| heading, paragraph, span, `<button>` | `Text` | renders HTML; a paragraph with links stays one Text |
| link | `TextLink` | URL in `content.content.url` |
| long editor prose | `RichText` | only for owner-edited prose |
| image | `Image` | from a URL: `content.image.from: url`, set both alt keys (Oxygen reads `alt == 'custom'` for URL images too) |
| icon, svg | `SvgIcon` | |
| video | `Html5Video`, `oEmbed` | builder-bound; use a facade |
| loops | `PostsLoop`, `DynamicDataLoop`, `TermLoopBuilder` | builder-bound |
| reusable part | `Component` | see §4 |
| template slot | `TemplateContentArea` | |
| raw code | `HtmlCode`, `CssCode`, `JavaScriptCode`, `PhpCode` | only with a recorded reason |

Classes and attributes go in `settings.advanced.classes` and `settings.advanced.attributes`.

**Never:** the `EssentialElements\*` composites from Breakdance Elements for Oxygen (icon box, pricing table, testimonials, counters, sliders, social icons, logo list, and so on), `Shortcode`, `ContainerShortcode` and `WpWidget` holding layout. The site already hides the Breakdance duplicates of the primitives (`EssentialElements\Section`, `Div`, `Heading`, `Text`, `TextLink`, `WrapperLink`, `Icon`, `RichText`, `CodeBlock`, `Image2`) through the `oxygen_builder_hidden_elements` option; keep them hidden.

## 3. Design system

**Variables.** Oxygen stores them in the options `oxygen_variables_json_string` and `oxygen_variables_collections_json_string`. Read with `\Breakdance\Variables\getVariables()` and `getVariablesCollections()`. Write only through `\Breakdance\Variables\saveVariables( $json )` with `{ "variables": [...], "collections": [...] }`, so the write becomes an Oxygen revision. `saveVariables()` returns nothing, so read the variables back and compare. Use one collection per Atomic Framework category (the test site uses Colors, Typography, Spacing, Layout, Effects). Push only the types `color`, `font_family` and `text`; a `font_family` value is the custom font id from `\Breakdance\Fonts\resolveFontFamilyToSlug()`.

**Classes (selectors).** Oxygen references selectors by id, and a paste cannot create them. For pasted blocks, keep plain class names on the elements and style them with one `CssCode` element that carries the token scope and the block CSS. Create real selectors in the Selectors panel only when the owner wants them editable there.

**Global settings** live in `oxygen_global_settings_json_string` (read with `\Breakdance\Data\get_global_settings_array()`). Global colours and fonts exist only when Breakdance Elements for Oxygen is active.

**Fonts.** Bundled fonts become Oxygen custom fonts with the woff2 files in the media library, so they keep working without other plugins; each face needs `id`, `weight` and `fileName`.

## 4. Components and templates

- Components are the `oxygen_block` post type (labelled Component). Templates, headers, footers and popups are `oxygen_template`, `oxygen_header`, `oxygen_footer` and `breakdance_popup`.
- Build a repeated part once as a Component and place it with the `Component` element. Component properties feed values through dynamic data (`OxyComponentField`).
- A part a component cannot express exactly stays plain elements (house rules §5).

## 5. Breakpoints

Oxygen's five built-in breakpoints are fixed in code and must not be edited:

| id | Label | max-width |
|---|---|---|
| `breakpoint_base` | Desktop | (base) |
| `breakpoint_tablet_landscape` | Tablet Landscape | 1119 |
| `breakpoint_tablet_portrait` | Tablet Portrait | 1023 |
| `breakpoint_phone_landscape` | Phone Landscape | 767 |
| `breakpoint_phone_portrait` | Phone Portrait | 479 |

Add other project widths as custom breakpoints in Preferences → Custom Breakpoints. They are saved in the `preferences` global option (`\Breakdance\Data\get_global_option('preferences')` / `set_global_option`); keep every other preference intact. Each row needs `id` (lowercase, `[a-z0-9_]`), `label`, `defaultPreviewWidth`, and `minWidth` (above the base) or `maxWidth` (px − 1, below the base). Skip widths equal to a built-in one. Overlapping custom breakpoints give unpredictable CSS.

## 6. Paste format

Oxygen's clipboard is `{ "element": [...] }` (a tree; ids are renumbered on paste). Generate it, paste it through Oxygen's own paste handler in the builder, save, then check the front end. Never emit a native format you have not verified with a real paste; fall back to HTML in an `HtmlCode` element and say so.

## 7. Forms (custom feature)

Breakdance Forms' Form Builder is a composite and cannot hold library fields or classes. Build fields as a `Container` with a `Text` label and the `<input>`/`<textarea>` in `HtmlCode`; log the form as builder-bound. Keep this fallback even when Breakdance Forms is active.

## 8. Dynamic data

Oxygen reads ACF, Meta Box and Toolset fields natively (`AcfField`, `MetaboxField`, `ToolsetField` families, plus post, term, author, user and WooCommerce fields). Bind fields through dynamic data, never through `PhpCode` or shortcodes. Field setup belongs to `wpnomy-acf-expert` or `wpnomy-metabox-expert`.

## 9. Check

1. Open the Oxygen builder once after any push: **Oxygen Doctor** reports data it rejects.
2. Load the front end at the base and at every breakpoint; compare with the plan.
3. Run the router's hand-over checklist (house rules §7).

Next: report to the owner, then the router's scratchpad.

## Scratchpad

End with the scratchpad: every request with its status (done, partly done, in progress, failed, not started, needs you), then what changed, what was verified on the site and what was not, and the Oxygen version checked.
