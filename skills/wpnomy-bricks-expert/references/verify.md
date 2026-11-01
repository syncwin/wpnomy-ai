# First-run audit and verification

## First run on a Bricks site

Read-only. Fills the scratchpad's Bricks canon. Recommends; implements nothing.

| Call | Gives you |
|---|---|
| `bricks/get-mcp-version` | Bricks, abilities and WordPress versions; disabled ability count |
| `bricks/list-ability-status` with `includeDisabled: true` | Which abilities an admin turned off. Plan around them |
| `bricks/get-system-information` | Theme and child theme, active plugins, permalinks, memory, CSS loading (present on Bricks 2.4.2, not in the official skills; if absent, `bricks/get-global-settings` for `cssLoading` plus Novamira's site info) |
| `novamira/bricks-check-setup` | Licence, post types Bricks may edit, CSS folder state, render probe |
| `bricks/get-design-context` (summary) | Palettes, classes, theme styles, components, variables, breakpoints |
| `bricks/get-style-manager`, `bricks/list-theme-styles` | Root size, fluid range, theme style conditions |
| `bricks/list-templates`, `bricks/list-components`, `bricks/list-global-queries`, `bricks/list-custom-fonts` | What already exists |
| `atomic-wireframe/list-projects`, `atomic-wireframe/get-project` | The design source, its prefix, root size and breakpoints |
| `bricks/list-dynamic-data-tags` on a real post | Whether ACF and the data plugin's tags are present |
| `novamira/get-active-design` | Whether a Novamira design claims authority. The framework leads; record what it reports |

### Look for

- **Design source missing or still default.** No Atomic Wireframe project, or atoms still grayscale.
- **Two token systems.** Variables or a CSS variable block already on the site that the framework would duplicate.
- **Breakpoint mismatch.** Bricks desktop-first defaults against a mobile-first project. Switching paradigm on a site with content orphans every responsive value; on an empty site it is free.
- **Root size mismatch.** Project at 62.5% while Bricks has no root theme style.
- **Template contention.** Two templates of one type whose conditions overlap.
- **Classes without a convention** or without the project prefix.

### Settings worth reporting

| Setting | Why |
|---|---|
| CSS loading inline | External files cache across pages; the house speed budget asks for them. Needs a writable `uploads/bricks/css` folder |
| Permalinks plain | Changes every URL. Set before content exists, never after |
| WP memory limit low (40M) | Large pages and imports fail on save |
| Post types Bricks may edit | A custom post type left off cannot get a template built for it |
| Google Fonts on | Remote loading; the house standard self-hosts at most two families |
| Bricks Abilities and `execute-php` enabled on production | Turn off what the site does not need once the build is done |
| `postTypes` (post types Bricks may edit) | `city`, `project` and every CPT with a template must be included |
| `enableQueryFilters`, `saveFormSubmissions` | Needed only when filters or saved submissions are planned |
| `elementAttsAsNeeded`, `disableBricksCascadeLayer` | Bricks output and cascade switches; read their schema descriptions before recommending either, since they can break `#brxe-` selectors |
| `disableSkipLinks` | Keep skip links on |
| Optimiser stripping or rewriting `data-brx-loop-start` attributes or `brx-loop-start` comments | Breaks loop pagination, load more and filters |
| Page and object cache | A change that looks unapplied is usually a cache |

Each finding goes in the scratchpad with what it fixes and what it risks. One approval covers one item.

### Settings: how to read and write

`bricks/list-settings-schema`, then `bricks/get-global-settings`, then `bricks/set-global-settings` `{ settings: { key: value } }` as a partial merge; never round-trip the whole blob. `cssLoading` is `""` (inline) or `"file"`. Excluded keys return `bricks_setting_excluded`, which is final: `license*`, `apiKey*`, `apiSecretKey*`, `executeCodeEnabled`, `executeCodeCapabilities`, `codeSignaturesLocked`, `codeExecutionMode`, `htmlExecutionMode`, template passwords. Unknown keys return `bricks_setting_unknown`. Breakpoints, Style Manager, pseudo-classes and roles have their own abilities. PHP abilities need `BRICKS_ENABLE_PHP_ABILITIES`, global code execution, unlocked signatures and an operator's admin session; signatures are regenerated only in the admin UI. Re-read the schema on each Bricks version.

## After every write

Read the mutation result first: target, persisted values, anything normalised or omitted. A `revisionId` proves a save, not a result.

| Wrote | Read back with |
|---|---|
| Elements | `bricks/get-page-elements` (ids present, settings as sent) |
| Element conditions | `bricks/get-element-conditions` |
| Interactions | `bricks/get-element-interactions`, reading `effectiveInteractions` (class interactions stack) |
| Template or conditions | `bricks/get-template` |
| Variables | `bricks/list-global-variables` (values as strings, OKLCH intact) |
| Classes | `bricks/list-global-classes` |
| Theme style | `bricks/get-theme-styles` with the id (conditions present) |
| Component | `bricks/get-component` (`_version` present, connections point at surviving ids, slot keys real) |
| Breakpoints | `bricks/list-breakpoints` (`isMobileFirst` as intended) |
| Form | `bricks/get-form-config` |
| Filters after reindex | `bricks/list-query-filters` |
| Menu | `bricks/get-nav-menu` |

`list-*` results are paginated: on `hasMore: true`, scope the readback to the written id.

Black box and ladder check on every write: no banned element; no design control on any element; every element-level style is a logged placement one-off; every builder-bound element logged.

Silent failures to suspect: success with the old state (a save filter vetoed it); an id missing from the readback (wrong post or area); a theme style with no effect (no conditions); a template not rendering (outscored); an element still showing (another OR group); a renamed variable still emitted (references not swept).

## Front-end gate

1. If CSS loading is files and globals changed, `bricks/regenerate-css-files`.
2. Open the page logged out. `bricks/find-post` returns the builder URL, not the permalink; `create-post` returns the permalink, otherwise resolve it from WordPress. Drafts are checked through an authenticated preview; never publish to test, and never submit a production form.
3. Check at every Bricks breakpoint width and just either side of each.
4. Computed `html` font size matches the project root.
5. Variables resolve: no unstyled block, no raw tag text, no literal `{acf_...}`.
6. Keyboard: menus, accordions, tabs, `details`, `dialog` and popups: initial, open and closed states, activation by keyboard, focus moving in and returning, ARIA correct.
7. Loops and filters after their AJAX result, not just on load.
8. Complete and sparse records for every template.
9. Console free of errors.

Without a browser, `bricks/render-elements` is the fallback evidence. Say which checks it could not cover.

Never report a build as done because it saved. Report what was verified, and name what was not.

## Restore and clean up

- Restore from a transfer package: `bricks/inspect-transfer-package` `{ zipBase64 }` returns `zipHash`; then `bricks/import-transfer-package` `{ zipBase64, expectedZipHash, types, items: { <type>: [ids] }, conflictMode: "skip" }`. `items` is required for every type (`["all"]` for breakpoints); `replace` needs `allowOverwrite: true`; the custom-code settings tab cannot be imported; `importImages: true` is opt-in; split large packages.
- After a migration: `bricks/list-orphaned-elements`, then `bricks/cleanup-orphaned-elements` with `dryRun: true`, then a yes, then `dryRun: false`. It sweeps the whole site.
- A success that shows the old state means a `bricks/save_*` filter vetoed the save. An empty `get-page-elements` after a header write means area routing failed: stop.
