# Design system: Atomic Framework into Bricks

The Atomic Wireframe plugin owns the design. Bricks receives it. Nothing in Bricks is designed by hand where the framework already has a value.

## Contents

Read the source · What goes where · Root font size · Order of writes · Ownership and conflict rules · Breakpoints · Fonts · Checks · Dark mode · Changing a token later · Existing token layers

## Read the source

1. `atomic-wireframe/list-projects`, then `atomic-wireframe/get-project` with no `parts` filter. Save the result as JSON in the working folder.
2. Follow `aw-to-bricks.md` in this folder on the saved JSON and write the result to `plan.json`. It writes nothing to the site. It produces the variable rows, categories, the Root theme style payload, breakpoint rows, the dark-mode block and the class prefix, with the plugin's own naming and rem rebasing.
3. Read every warning in `plan.json` to the user before writing. They are decisions, not notes.

If the project's eight colour atoms are still the grayscale defaults (`primary` is `oklch(25% 0 0)`), the brand has not been set. Stop and ask for the approved palette. Grayscale is a placeholder, never a launch value.

## What goes where

| Framework | Bricks | Why |
|---|---|---|
| All 80 tokens | Global variables in five categories (Colors, Typography, Spacing, Layout, Effects), names bare as the framework writes them | One source. Bricks emits `--name`; every class reads `var(--name)` |
| Fluid type and space scales | Static variables, categories with **no** `scale` config | The framework is the only scale generator. A Bricks `scale` config regenerates those variables on any root-size, screen-width or import change |
| Colour atoms | Variables only. **No palette entries for them** | A palette colour with `raw: "var(--name)"` emits that variable in a later CSS bucket than global variables, so a palette entry pointing at a variable of the same name makes `--primary: var(--primary)`, a cyclic value that kills the colour. Styling is class-only, so the builder colour picker is not needed |
| Root font size, body and heading type | One theme style, `Root`, conditions `[{ "main": "any" }]` | Theme styles with no conditions do nothing |
| Breakpoints | Bricks breakpoints, mobile-first, keys from the project (`bp768`) | Matches the framework's own media queries |
| Dark values | The `[data-theme="dark"]` block, only if the site ships dark mode | Bricks variables hold one value |
| Class prefix and renames | Global class names | See `bem-classes.md` |

Never `bricks/commit-site-foundation` on a framework site: it builds its own palette, scales and templates, and it refuses non-greenfield state anyway. Never Bricks' `generate-scale-variables` or `generate-color-shades` on framework tokens.

If a site already has a palette in use, leave it; do not add atoms to it. If the default palette's colours are unused, report them; delete only with a yes.

## Root font size

The Atomic Wireframe project writes rem on a 16px root (the V4 skill's older 2.0.0 export is already on 62.5%; never mix the two sources). A project set to `62.5%` exports every rem multiplied by 1.6, and the script does the same. The two must match:

- Root theme style `settings.typography.typographyHtml` is the project's `rootFontSize` as a plain string (`"62.5%"`). Body, headings and H1 to H6 are property maps (`typographyBody: { "font-family": "var(--font-body)", ... }`).
- Check the computed `html` font size on the front end after the theme style is live.
- Changing the root size later rescales the whole site. It is a site decision, asked for, never a fix.
- Bricks Style Manager (`bricks/get-style-manager`) stores a root size and fluid range for Bricks' own generator, and is resolved before theme styles. Leave it unset on a framework site, or set it to the same values. `set-style-manager` replaces the whole option: read it and keep unrelated keys.

## Order of writes

Each step is a separate, verified write. Fresh ownership from one read before each.

1. **Back up** if the site has any content: `bricks/list-transfer-items`, then `bricks/export-transfer-package` for variables, classes, palettes, theme styles and breakpoints. Global data has no revisions.
2. **Check for scale-prefix collisions.** `bricks/get-design-context`: if any existing variable category carries a `scale` config whose prefix is `text-` or `space-`, it blocks hand-authored values for that prefix. Report it; do not write.
3. **Categories.** `bricks/list-global-variables`, then `bricks/set-global-variable-categories` with the full list (it replaces the list; keep existing categories and their opaque fields), passing `expectedOwnership` (category ownership) and `expectedVariableOwnership` from that one read. Re-read, and if Bricks stored different category ids than the plan's (`afwclr` and the rest), rewrite each variable row's `category` to the stored id.
4. **Variables.** `bricks/set-global-variables` with rows `{ name, value, category: "<categoryId>" }` from `plan.json`, plus `expectedVariableOwnership` and `expectedCategoryOwnership` from one fresh read. Unknown keys are rejected. It upserts by name: an existing name with a different value is a conflict to report, never overwrite.
5. **Root theme style.** Read the live theme-style schema for link, button and container keys, then `bricks/create-theme-style` with `{ label: "Root", conditions: [{ "main": "any" }], settings: <plan.themeStyle.settings> }`. Then bind links, buttons and container width to variables (`container-width`). Read back with `bricks/get-theme-styles` and the id.
6. **Breakpoints** (below).
7. **Fonts** (below).
8. **CSS.** If CSS loading is files, `bricks/regenerate-css-files`.

## Ownership and conflict rules

- Every global write takes ownership values copied from one fresh read. On a stale-ownership error, re-read and rebase; never resend the stale payload.
- Variables: delete with `bricks/delete-global-variable` passing the row's `itemOwnership` and `allowOrphans: true`; it returns `beforeDelete`. Names are unique (`bricks_conflict_duplicate_global_variable_name`).
- Theme styles: update and delete take `itemOwnership` from `get-theme-styles({ style: id })`; deleting a style with settings or conditions needs `acknowledgeStyleRemoval: true`. Only the highest-scoring matching style applies unless `themeStylesLoadingMethod` loads all matches.
- Palettes, if ever touched: chain each response's `ownership` into the next call, never parallel; deleting a colour that other CSS references needs `allowOrphans: true`.
- Pseudo-classes: `bricks/list-pseudo-classes`, then `bricks/set-pseudo-classes` with `expectedOwnership`; removing one needs `allowRemovedPseudoClasses: true`. Pseudo suffixes take one colon (`:hover`), never `::hover`.

## Breakpoints

1. `bricks/list-breakpoints` for `breakpointOwnership` and `globalSettingsOwnership`.
2. `bricks/set-breakpoints` with the full row list from `plan.json` (rows `{ key, label, width, base? }`, exactly one `base: true`), `expectedOwnership`, `customEnabled: true` with `expectedGlobalSettingsOwnership`. Replacing Bricks' default keys (`desktop`, `tablet_portrait`, `mobile_landscape`, `mobile_portrait`) removes them, so the write also needs `allowRemovedBreakpoints: true` after the returned usage evidence is reviewed.
3. Read back with `bricks/list-breakpoints`. **Stop unless `isMobileFirst` is `true`.** The writer sorts rows before saving, so the readback, not the request, is the contract.
4. Run `bricks/regenerate-css-files` if CSS loading is files.

On a site with content, switching paradigm orphans every responsive value stored under the old keys (they stay on elements, never deleted). Never reuse an old key for a different width: its stored settings merge silently. On an empty site the switch is free.

## Fonts

Self-hosted, at most two families. Call order:

1. `bricks/upload-custom-font-file` `{ filename: "inter-tight-400.woff2", content: "<base64>" }` returns `{ attachmentId, url, format, bytes }`. Formats woff2, woff, ttf, otf, eot; 8 MB decoded. Never `upload-media` for fonts.
2. `bricks/create-custom-font` `{ family }` returns the font id.
3. `bricks/update-custom-font` `{ fontId, fontFaces: { "400": { "woff2": <attachmentId> }, "700": { "woff2": <id> }, "400italic": [...] } }`. `fontFaces` replaces the whole map: send every face each time.

Output uses `font-display: swap`. Turning Google Fonts off (`disableGoogleFonts`) is writable only if `bricks/list-settings-schema` shows the key; otherwise it is an operator click in Bricks settings. `font-body` in the framework must name the uploaded family.

## Checks before moving on

- `bricks/render-elements` on one heading using a class that reads `var(--text-m)`: the output shows the variable, not a number.
- OKLCH and `color-mix()` values survive the round trip: read the variables back and compare strings.
- Clamp values render at the narrowest and widest breakpoints without inverting.
- `muted-foreground` against `bg-body` and every `on-*` pair still pass WCAG AA after the brand colours land. The framework's AA claim holds for its defaults, not for a new palette.

## Dark mode

Off unless the brief asks. If asked, the framework's `[data-theme="dark"]` block from `plan.json` goes in one place only (a FluentSnippets snippet, `<prefix>-dark-mode`), and the toggle that sets `data-theme` is a decision to raise. Never two dark-mode mechanisms.

## Changing a token later

To change it: edit the project in Atomic Wireframe (after a yes), redo the plan with `aw-to-bricks.md`, then update only the changed rows. Renaming a variable does not update `var(--old)` anywhere: sweep classes, theme styles, components and every document (`bricks/checkout-site-repository` with cursors, recording any coverage limit) before a rename, or do not rename.

## Existing token layers

A site already carrying its own variables, palette or classes is reconciled before anything is imported: list them, map each to its framework equivalent, alias old names to framework tokens, move consumers page by page, and delete the alias only when nothing references it. Report duplicates; never consolidate silently.
