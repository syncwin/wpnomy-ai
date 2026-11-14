# Atomic Wireframe to Bricks plan recipe

Map an Atomic Wireframe project onto Bricks payloads by hand. This is the same logic as the maintainer's `dev/wpnomy-bricks/scripts/aw_to_bricks.py`, written so Claude can do it with Read, Grep and Write. It writes nothing to any site. The naming and rem rebasing follow the plugin's own "Bricks JSON" export.

Read `../assets/atomic-framework-ids.json` first. It holds `tokens` (framework token name to id and layer), `categories` (rows with an `id`), `defaultBaseSettings` (per category `naming` values, for example `afwtyp` and `afwsp`) and `source` (the framework version).

## 1. Read the project

Accept either shape, saved as JSON. If the top level is an object with an object `data`, use `data`.

- **Envelope** (has `variables`): tokens come from `variables[]` as name, value, `darkValue`, category, layer, type, id. Settings from `settings`; breakpoints from `breakpoints`; strategy from `breakpointStrategy`; prefix from `settings.classPrefix`; renames from `classRenames`; base settings from `baseSettings`.
- **get-project ability result** (has `tokens`): tokens from `tokens[]` as name, value, `dark_value`, category, type; layer and id come from the ids asset by name. Settings from `settings`; `breakpoints`; `breakpoint_strategy`; prefix from `class_prefix` or `settings.classPrefix`; renames from `class_renames`. Base settings come from the ids asset.

No tokens: stop and say "No tokens found. Call atomic-wireframe/get-project with parts including \"tokens\"."

Settings used: `rootFontSize` (default `100%`) and `variablePrefix` (default empty).

## 2. Warnings so far

- Framework tokens in the ids asset but absent from the project: warn with the count and names: read every category, or confirm they were removed on purpose.
- Project tokens not in the ids asset: warn "Tokens not in Atomic Framework 2.2.0": they get generated ids, check the framework version.
- A token `font-heading` whose value is `inherit`: warn to set the site's heading family in Atomic Wireframe before building.

## 3. Names

For each token name apply, in order:

1. If it starts `text-` and the base setting `afwtyp.naming` is set and not `text`, replace the `text` part with that naming.
2. Else if it starts `space-` and `afwsp.naming` is set and not `space`, replace the `space` part with that naming.
3. If `variablePrefix` is non-empty, prepend `<prefix>-`.

This is the rename map (original name to exported name).

## 4. Values

For every value: first rewrite each `var(--name)` using the rename map (names not in the map stay). Then, only when `rootFontSize` is `62.5%`, multiply every number before `rem` by 1.6 and round to 4 decimals, dropping trailing zeros (`1.25rem` becomes `2rem`).

## 5. Outputs (one JSON plan)

- `variables`: one row per token, `{name: <exported name>, value: <rewritten value>, category}`. Bricks assigns ids and upserts by name.
- `categories`: the ids-asset categories whose id is used by at least one token. No `scale` key.
- `darkCss`: for tokens with a dark value whose layer is `atom` or unknown, a block `[data-theme="dark"] { --<exported name>: <rewritten dark value>; ... }`, two-space indented, one line per token. Empty string when none.
- `themeStyle`: `{label: "Root", conditions: [{main: "any"}], settings: {typography: {...}}}` where `typographyHtml` is `rootFontSize`, `typographyBody` is font-family `var(--font-body)`, font-size `var(--text-m)`, line-height `var(--text-line-height)`, font-weight `var(--text-font-weight)`, color `var(--text-color)`; `typographyHeadings` is font-family `var(--font-heading)`, font-weight `var(--heading-font-weight)`, line-height `var(--heading-line-height)`, color `var(--heading-color)`; and `typographyHeadingH1` to `typographyHeadingH6` each `{font-size: var(--h1)}` to `var(--h6)`. Every `var()` name goes through the rename map. Add `themeStyleNote`: typography keys match the bundled schema; read the live schema for link, button and container keys before adding them.
- `breakpoints`: enabled breakpoints sorted by `px` ascending, each `{key: id, label: "<name> (<px>px)", width: px}`; the first also has `base: true`.
- `classPrefix` and `classRenames`: the project's values.
- `source`: `{rootFontSize, variablePrefix, tokenCount, framework}` where framework is the ids asset `source`.
- `warnings`: the list below.

## 6. Breakpoint, root and prefix warnings

- Strategy other than mobile-first (unset counts as mobile-first): "Project breakpoint strategy is <x>; this plan assumes mobile-first. Ask before mapping."
- More than 5 enabled breakpoints: each adds a responsive column to every Bricks control; confirm all are needed.
- Base breakpoint 360px or less: mobile-first base styles already cover small phones; consider disabling it.
- Any breakpoints: replacing Bricks' default keys needs `allowRemovedBreakpoints: true` after reviewing the usage evidence; after set-breakpoints, stop unless list-breakpoints reads back `isMobileFirst: true`.
- Root `62.5%`: every rem value was multiplied by 1.6; the Root theme style must set html font-size to 62.5% or every size renders 1.6x too small.
- Prefix set but not lowercase kebab-case (`^[a-z][a-z0-9]*(-[a-z0-9]+)*$`): ask before using it. No prefix: classes would export as `awf-`, ask for the prefix.

## 7. Hand back

Write the plan to a file the user can open (for example `plan.json` in the working folder), read the warnings back to the user, and apply nothing to the site until they agree. Use the plan rows with `bricks/set-global-variable-categories`, `bricks/set-global-variables`, `bricks/create-theme-style` and `bricks/set-breakpoints`.
