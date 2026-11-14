# Elements, imports and media

## Contents

Element trees · Primitives and their output · Native HTML patterns · Settings an element may carry · Cascade · Write routes · Atomic Wireframe blocks to Bricks · Media and migration assets

## Element trees

A Bricks content area is a flat array. Each element: `id` (exactly 6 characters; the front end renders `id="brxe-<id>"` unless `_cssId` is set), `name`, `parent` (`0` for a root), `children` (ids), `settings`, optional `label` (the Structure panel name, never the id). Nested input (`{ name, settings, children }`) may omit ids; Bricks generates them. Never invent semantic ids like `hero`.

Before writing an element whose settings are not covered here, read `bricks/get-element-schema` `{ elementName }` (dispatcher-only on most servers). Never guess a control key. Unbalanced `{` or `}` in a non-code setting is rejected at write time.

## Primitives and their output

| Need | Element | Output and notes |
|---|---|---|
| Page band | `section` | `<section>`. Never a section inside a section |
| Site-width wrapper | `container` | Width from the Root theme style, bound to `container-width`. Never a container inside a container |
| Full-width flex wrapper | `block` | Tag selectable |
| Anything else structural | `div` | `tag` for `article`, `aside`, `nav`, `ul`, `ol`, `li`, `figure`, `blockquote`; `tag: "custom"` plus `customTag` for anything else |
| Heading | `heading` | `tag` h1 to h6 (default h3: always set it). One H1 per page |
| Short text | `text-basic` | Default tag is `div`: set `tag: "p"` or `"span"`. Never for HTML from a field |
| Long editor-owned prose, or a field returning HTML | `text` (Rich Text) | Always renders a wrapper div (no tag control). Policy: only for long prose |
| Call to action | `button` | Default tag `span` with a link; styled by `btn` classes only. Reset the theme style's button defaults to tokens so classes do not fight them |
| Inline link | `text-link` | |
| Image | `image` | Default root is `figure`; set `tag: "div"` when a figure is wrong. Local media id, alt, `loading: "eager"` on the LCP image only |
| Icon, inline SVG | `icon`, `svg` | |

Bricks wraps header templates in `<header>`, footer templates in `<footer>` and page content in `<main>` itself. Never tag a root `header`, `footer` or `main`.

## Native HTML patterns

The policy's step 2. Built from primitives, no Code element:

| Pattern | Build |
|---|---|
| Disclosure (non-FAQ) | `div` `tag: "custom"`, `customTag: "details"`; first child `text-basic` or `div` with `customTag: "summary"`. Exclusive group: `_attributes: [{ "name": "name", "value": "group-id" }]` on each `details` |
| Modal | `div` with `customTag: "dialog"`, opened by a `button` with `popovertarget` or a 3-line script; or the Popover API (`popover` attribute on the panel) |
| Carousel | A `div` row with a class using `scroll-snap-type` and `overflow-x: auto`; children are cards |
| Sticky header | `position: sticky` on the header class |

The official skills do not document these custom tags, so the first use on a site is verified, and the result recorded in the scratchpad:
1. The live `div` and `block` schema offers `custom` in `tag`.
2. The readback keeps `customTag` (a `bricks/allowed_html_tags` filter may strip unknown tags).
3. `bricks/render-elements` and the front end show the real element.
4. How a valueless attribute (`popover`, `open`) is emitted, and what default CSS Bricks puts on `.brxe-div` and `.brxe-block` (flex display can break `details`).

`popovertarget` needs a stable id: set `_cssId` on the target and point at that, never at `brxe-<id>` (duplication changes it). A `_cssId` also replaces the rendered `brxe-` id.

The HTML importer does not map `details`, `summary` or `dialog`; build these natively, never through an import.

## Settings an element may carry

Content, structure and the placement one-offs below: `tag`, `customTag`, `text`, `link`, `image`, `altText`, `loading`, `_cssGlobalClasses` (global class **ids**), `_cssClasses` (plain classes, for `js-` hooks), `_cssId`, `_attributes` (`[{ id?, name, value }]`, for `aria-*`, `role`, `popover`, `name`, `data-*`), loop settings, `_conditions`, and on the rare allowed element `_interactions`.

Style controls on an element are for placement one-offs only (the router's `styling-and-code.md`, steps 5 and 6): `_order`, `_alignSelf`, `_gridItemJustifySelf`, `_zIndex`, `_aspectRatio`, `_position` offsets, this instance's background image, and a short `_cssCustom` rule for grid placement or a scoped token override. Design controls (`_typography`, `_padding`, `_margin`, `_gap`, `_background` colour, `_border`, `_boxShadow`, hover states) are never set on an element; they live in a global class. A second element needing the same placement gets a modifier class instead.

Link object: `{ type: "internal", postId }` or `{ type: "external", url, newTab }`; `dynamic` and `media` types also exist. Empty link objects are rejected.

Class custom CSS is a full rule using the class selector (`.md-pill.is-active { ... }`), with `\n` newlines.

## Cascade

Later wins at equal specificity: global variables, theme styles, utility classes, global classes, palette colour vars, page CSS, header, content, footer, popup, template CSS, Settings custom code. Solve a conflict by moving the rule to the right layer, never `!important`. FluentSnippets CSS sits wherever its location setting puts it (usually the head, so before Bricks' own CSS): keep snippet rules flat and one class deep so they never depend on load order.

## Write routes

| Situation | Route |
|---|---|
| Small exact edit to existing text, a variable value or a class leaf | `bricks/commit-exact-site-edits` with `expectedValue` (or `allowBlindWrite: true` only when the user named the exact target and wants it replaced). On component elements it edits only `role` and `aria-*` attributes |
| Edit whose target needs finding | `bricks/checkout-site-edit-map` `{ targets: [{ scope: "page", postId }], elementIds? }`, then `bricks/commit-site-edit-plan` with the returned `selectionRef` and one stable idempotency key; `responseFormat: "summary"` |
| Structural edit to one known resource, such as one component | `bricks/resolve-agent-file` `{ scope, query, resourceKinds? }`, then `bricks/commit-agent-file` with one key, following its `editingContract` |
| Add a section to an existing page | `bricks/add-element` `{ postId, parentId ("0" for root), position (zero-based), element: <nested subtree> }`, built in memory and inserted once |
| Settings on several elements | `bricks/batch-update-elements` |
| Empty page or template body from finished markup | `bricks/commit-html-css-page-import` (below) |
| Two to 25 coordinated resources | One site changeset: preview once, apply with the same token and key; done only on `committed`. Stop on `failed_before_commit`, `partial_commit` or `manual_recovery`, re-read and re-plan. More than 25: split into valid batches |
| Replace a whole page | `bricks/set-page-elements`, only when replacing everything is the intent. Never send just a fragment |

Each element write returns a `revisionId`; `bricks/list-revisions` and `bricks/restore-revision` are the rollback (present on Bricks 2.4.2, checked on the staging site 6 Oct 2026, though not in the official skills; confirm with `bricks/list-ability-status` on other sites, otherwise restore in the builder UI). Global data rolls back from a transfer package.

## Atomic Wireframe blocks to Bricks

The library is the starting point for sections. Library blocks are already plain HTML plus framework classes, which is what the policy wants.

**Prepare the markup** from `atomic-wireframe/get-block`:
1. Apply the project prefix and renames to every class.
2. Remove the `awf` scope class; the Root theme style does its job.
3. Turn every inline `style` into a class rule. Nothing reaches the site as an inline style or an element style.
4. Map placeholders (`placeholder--image`, `--logo`, `--avatar`) to real `image` elements with media, or leave the slot for the content stage.
5. Pull out anything the converter cannot carry (accordions, tabs, sliders, forms, `details`, `dialog`): those are built natively afterwards.

**Empty page.** One call, no version, context or converter pre-calls: `bricks/commit-html-css-page-import` with the page identifier, `html` (no `<main>`, no site header or footer), `css` (only the rules for the classes the block uses, rewritten per `bem-classes.md`), `documentPurpose: "page-content"` (`"template-content"` for the inside of an empty header or footer template), `replaceExisting: false`, a new `idempotencyKey`, and options:

```json
{ "source_root_font_size_px": 16, "target_root_font_size_px": 10 }
```

The library CSS is written on a 16px root and a 62.5% Bricks site is 10px, so the converter rescales. Pass both values, or a normalisation warning fires. If the CSS was already rebased (for example with values from the `aw-to-bricks.md` plan), pass `10` and `10`. Never both rescale and pre-rebase. Media-query widths are never rescaled.

Result handling:
- `autoApplied: true` needs `committed: true` and `transactionState: "committed"`.
- `nextAction: "review_warnings"`: review, then `bricks/apply-html-css-page-import` with the returned **`previewToken`**, the same `idempotencyKey` and `acknowledgeWarnings: true`.
- On errors or policy violations: fix the source and use a **new** key.
- Always read `partial` and `omittedElements`. The importer drops elements it cannot author, with their descendants, and still reports success. A partial import is not complete.

For "no new globals" work, use the native-only profile `{ "preserve_html_defaults": false, "custom_css_policy": "forbid", "global_resource_policy": "forbid_creates" }`. Never weaken a profile to make a preview pass.

**Existing page.** Convert with `bricks/convert-html-css-to-bricks-data` (read-only), then check `rem_normalization`, `code_sensitive_elements`, `code_sensitive_write_blocked` and `requires_execute_code`. A blocked write is rewritten and reconverted, never persisted unchanged. Create new classes with `bricks/batch-create-global-classes` (`dryRun: true`, then fresh ownership and `dryRun: false`), keeping the converter's class ids so `_cssGlobalClasses` stay valid; reuse existing classes. Insert with `add-element`.

Converter hints: `<div class="brxe-container">` becomes a Container, `<div class="brxe-block">` a Block, `<a class="brxe-button">` a Button (a plain `<a>` is a Text Link). `.brx-*` and `.brxe-*` are reserved and never imported as classes.

Converter limits: static only. `@keyframes` goes to page CSS, `@font-face` to custom fonts, `@supports` is dropped, `:has()`, `:is()` and `:where()` are stored as written. Broad selectors (`*`, `body`, bare tags) and `table`, `pre`, `code`, `iframe`, `canvas` become Code fallbacks, which the policy does not want: keep broad rules in the theme style, and rebuild tables from `div` primitives with custom tags (`table`, `thead`, `tbody`, `tr`, `th`, `td`), verified like the other custom tags. Rich Text holds a table only inside editor-owned prose. Bricks resets user-agent heading and paragraph styles, so the theme style and classes must set them. Split large HTML by section.

**Clipboard (for a human paste).** Atomic Wireframe's Copy > Bricks Builder produces clipboard JSON. It keeps inline styles as attributes and relies on pasting the library CSS, so it is for wireframes only, never production.

## Media and migration assets

- Search before uploading: `bricks/find-media` `{ query, mimeType: "image/" }`, compact for broad searches.
- Upload: `bricks/upload-media` `{ filename, base64, title, alt }`. The extension must be WordPress-allowed and within the upload limit. URL sideloading only for public http(s) sources: never localhost, private, link-local, metadata, credentialed or file URLs.
- Image element:

```json
{ "name": "image", "settings": {
    "image": { "id": 123, "url": "...", "filename": "hero.jpg", "size": "large", "full": "..." },
    "altText": "...", "loading": "eager" } }
```

Choose `size` from the `sizes` the upload returns. Never lazy-load the LCP image.
- Empty alt only for decorative images. Page-specific alt goes on the element, because the attachment's alt is shared by every use.
- **Migration rule.** For the rebuild of an existing site: take images from the backup, upload each, replace every source URL with the attachment's `id`, `url`, `filename` and `size`, then verify the rendered images use local URLs with `srcset`. Never leave a source-site URL in a final element.
- Documents: the native `file` element (`source: "file"`, `file: { id, url }`).
- Galleries: a CSS grid of `figure` items (policy). Read the `image-gallery` schema only if a native gallery is ever approved.
- Custom SVG icons: `bricks/list-icon-sets`, `bricks/list-custom-icons`, then the live schemas of `bricks/create-custom-icon-set` and `bricks/upload-custom-icon`. Sanitisation may change the SVG; verify it.
- Delete only uploads this task created and nothing uses: `bricks/delete-media` `{ attachmentId }`, with a yes.
