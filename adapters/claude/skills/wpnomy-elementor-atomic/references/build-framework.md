# Build the Atomic Framework CSS and Variable manifest

Turn an Atomic Framework token export into CSS plus an Elementor Variable manifest by hand. This is the same logic as the maintainer's `dev/wpnomy-elementor-atomic/scripts/build_framework.py`, written so Claude can do it with Read, Grep and Write. Nothing generated is hand-edited afterwards: a new framework version is a re-run of this recipe.

Outputs live in `../assets/`: `atomic-framework.css.md` (the CSS, in a fenced block), `variables-manifest.json`, and `report.txt.md` (the report, in a fenced block). Copy a fenced block's content out unchanged when installing.

## 1. Read the export

Read the tokens JSON. It has `meta` (`version`, `rootFontSize`, `remBase`, `darkModeSelector`), `categories` (`id`, `name`) and `variables[]` (`name`, `value`, optional `darkValue`, `category`, `type`, `layer`). A lighter export may carry only name, value, id and category; infer the rest below.

**Refuse unsafe input.** The export becomes CSS. Stop and report the offending names if any token name does not match `^[A-Za-z0-9_-]+$`, or any `value` or `darkValue` contains `{`, `}`, `;`, `<`, `>`, `/*`, `*/` or `@import`.

## 2. CSS file

Header comment: `/* Atomic Framework <version or "(version not in export)">. <count> tokens. Generated from the framework export, do not hand-edit. */`

If `rootFontSize` is set, add the comment block that says html needs that font size so 1rem equals `remBase` (default `10px`), and that the computed value must be verified on a rendered page because a body font-size does nothing for rem, then `html { font-size: <rootFontSize>; }`. If it is not set, add a comment that the export carries no root font size and the rem base must be confirmed before install.

Then `:root { ... }`: categories in first-seen order; per category a comment `/* <category name> */`, one line `  --<name>: <value>;` per token, then a blank line. If any token has a `darkValue`, add a second block using `darkModeSelector` (default `[data-theme="dark"]`) holding only tokens whose `darkValue` differs from `value`, grouped the same way. The shipped sample is `../assets/atomic-framework.css.md`.

## 3. Classify each token

**Type** (use the export's `type` if present, else infer in this order, on the name and the trimmed value):

1. Name starts `font-` and does not end `weight` or `size`: `font`.
2. Name starts `shadow-` and the value has a space: `shadow`.
3. Name starts `transition`: `transition`.
4. Name ends `line-height`: `string`.
5. Name ends `font-weight` or `weight`: `number`.
6. Value starts `#`, `oklch`, `rgb`, `hsl`, `lab`, `lch` or `color(`: `color`.
7. Value contains `color-mix(`, or starts `var(` and the name contains `color` or starts `bg-`, `on-` or `border`: `color`.
8. Value is `0`, contains a number followed by px, rem, em, %, vw, vh, ch, ex or fr, or starts `clamp(`: `size`.
9. Value is a bare number: `number`. Otherwise `string`.

**Layer**: the export's `layer` if present; else `molecule` when the value contains `var(`, `color-mix(`, `calc(`, `min(` or `max(` and does not contain `clamp(`; else `atom`.

**Elementor type and mode**:

- `color`: literal value (starts `#` or a colour function) registers as `color`, mode `mirror`. A derived value stays CSS only, reason "derived value; a colour variable holds a literal".
- `font`: value `inherit`, `initial`, `unset`, `revert` or empty needs a site value (type `font`, mode `site`, note "ships as a keyword; set the site's real family at install"). Otherwise registers as `font`, mode `mirror`.
- `size`: registers as `size`, mode `reference`, with value `var(--<name>)`.
- Any other type: CSS only, reason "no Elementor Variable type for '<type>'".

## 4. Manifest JSON

`{framework_version, source_export (file name), token_names_prefixed (first token name matches ^[a-z]{2,4}-), registers[], needs_site_value[], css_only[]}`. Each entry has `label` (the name), `token` (`--<name>`), `category` (category name), `layer`, `source_type`. Registered entries add `type`, `value` (colour and font carry the literal; size carries `var(--<name>)`) and `mode`. Needs-site entries add `type`, `value: null`, `mode: "site"`, `note`. CSS-only entries add `reason`. Indent with two spaces. The shipped sample is `../assets/variables-manifest.json`.

## 5. Report

Lines: `Atomic Framework <version> source <file>`; `<n> tokens: <r> register, <s> need a site value, <c> stay in CSS.`; `Dark values in export: yes|no. Root font size in export: <value or not specified>.`; blank; `Register: <count> <type>, ...` (types alphabetical); the reference-mode count and the mirror-mode count lines; the "Need a site value before registering" list, then "CSS only" with the name padded to 24 characters and the reason; and, when dark values exist, "Dark mode is CSS only: Elementor Variables have no dark variant." The shipped sample is `../assets/report.txt.md`.

## 6. Check

Both shipped export shapes (`atomic-framework-tokens.json`, `atomic-framework-bricks-light.json`) classify identically. After a re-run, diff the new manifest against the old one and tell the user which tokens moved between register, site-value and CSS-only.
