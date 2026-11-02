# Atomic Framework on Elementor V4

## Contents

- [Names and prefixes](#names-and-prefixes)
- [Migrating a site's existing token layer](#migrating-a-sites-existing-token-layer)
- [The two layers](#the-two-layers)
- [What a V4 Variable can hold](#what-a-v4-variable-can-hold)
- [The mapping](#the-mapping)
- [Colour sourcing](#colour-sourcing)
- [The rem trap](#the-rem-trap)
- [Install on a site](#install-on-a-site)
- [Naming and BEM](#naming-and-bem)
- [Using tokens while building](#using-tokens-while-building)
- [Extending the framework](#extending-the-framework)
- [Failure modes](#failure-modes)

Atomic Framework 2.0.0 tokens export: 72 tokens, rem already written for a 62.5% root. The Bricks skill reads the newer Atomic Wireframe project instead (80 tokens, rem on a 16px root, rebased by `aw_to_bricks.py`): the two sources differ and are never mixed. Five categories, two layers, OKLCH colour, fluid `clamp()` sizing, `[data-theme="dark"]` variant, WCAG AA/AAA targets.

Maintained separately as a product. This skill consumes a version of it, never edits one.

| File | What it is |
|---|---|
| `assets/atomic-framework-tokens.json` | The product, full export. The only file a new version replaces. |
| `assets/atomic-framework-bricks-light.json` | A second export shape, kept as a fixture so the generator is tested against both. |
| `scripts/build_framework.py` | Generates everything below. |
| `assets/atomic-framework.css` | Generated. The `:root` block, plus a dark block when the export carries dark values. |
| `assets/variables-manifest.json` | Generated. Every token that registers as an Elementor Variable, plus the ones needing a site value and the ones staying in CSS. |
| `assets/report.txt` | Generated. The same split, readable. |

**A new framework version is a re-run, not an edit.** Drop the new export into `assets/`, run `python3 scripts/build_framework.py assets/<export>.json -o assets`, and re-apply. Never hand-edit the generated files: the next version overwrites them.

The generator reads either export shape. The full one carries `meta`, `type`, `layer` and `darkValue`; the lighter one carries only name, value, id and category, and everything missing is inferred from the value. Both classify identically, which is what the second fixture is for.

## Names and prefixes

**Token names pass through exactly as the framework writes them.** The framework owns its own namespace. If a future version prefixes its names, the prefix flows through; nothing here adds one. The manifest reports `token_names_prefixed` so the install step knows which it is dealing with.

Anything this plugin invents that is not a framework token takes the house prefix: classes and wrappers `<prefix>-` (the prefix from the router's Naming rule), helper variables the same prefix. The router's naming rule is the full statement.

Bare framework names are short and can collide with a theme or another plugin's variables. That is what the first-run audit checks for, and what the migration below resolves when a site already has its own layer.

## Migrating a site's existing token layer

A site with its own variables, typically a `--<brand>-*` block in the kit CSS, is retired onto the framework rather than run alongside it. Two systems on one page means neither is canonical and the next edit picks the wrong one.

1. **Map before deleting.** List every existing token and the framework token that replaces it. A brand navy maps to `primary`; a wash maps to `bg-surface`; a hairline maps to `border-color`. Anything with no framework equivalent is either a site-specific value, which becomes a `<prefix>-` variable outside the framework block, or a sign the framework needs the token, which is a product change.
2. **Alias, do not cut.** Redefine each old token as the framework one: `--bh-navy: var(--primary);`. Every existing page keeps rendering while nothing has been edited yet.
3. **Migrate consumers**, page by page, from the old name to the framework name.
4. **Delete the alias block** only once nothing references it. Search the kit CSS, page-level CSS, every template and every HTML widget before deleting; a token used in one widget on one page fails silently and only there.

Keep the alias block for a full review cycle. It costs a few lines and it is the difference between a reversible migration and a hunt.

## The two layers

**Atoms** are configured per site: eight colours, three font families, the raw scales. Changing an atom is how a site gets its brand.

**Molecules** derive from atoms through `color-mix()` and `var()`. Hovers, muted foregrounds, shadows, the heading scale. They self-adapt, which is the point: set `--primary` and every hover, shadow seed and derived surface follows.

**Never configure a molecule directly.** A hardcoded `--primary-hover` stops tracking `--primary`, and the two drift on the next rebrand, silently, because both values are present and both format correctly.

## What a V4 Variable can hold

Three types, and they do not have equal reach. Verified against a live Elementor 4.2 install.

| Type | Accepts | Consequence |
|---|---|---|
| Size | A CSS dimension (`24px`, `1.5rem`) **or a CSS expression**: `clamp()`, `calc()`, `min()`, `max()`, `var(--token)` | Every fluid token registers directly, and can be authored as a reference to the CSS layer |
| Color | A hex value | A token whose value is `var()` or `color-mix()` has nowhere to live |
| Font | A family name | `inherit` is valid CSS and invalid here |

V4 Variables also have no dark-mode variant, so every `darkValue` comes from CSS regardless.

That asymmetry sets the architecture. **The `:root` block is canonical.** Size variables reference it safely. Colour variables cannot, so the eight colour atoms register as hex literals and are treated as a generated mirror: a colour changed in the CSS is changed in the variable in the same pass, never one alone.

## The mapping

47 of 72 tokens register as V4 Variables, one (`font-heading`) needs a site value, 24 stay in CSS. The generator produces this split; the table is here so the shape is readable without running it.

| Category | Registers | Type | Stays in CSS |
|---|---|---|---|
| Colors | 8 atoms: `primary`, `secondary`, `accent`, `text-color`, `heading-color`, `bg-body`, `bg-surface`, `border-color` | Color, as hex | 6 molecules: `on-accent`, `muted-foreground`, `surface-muted`, and the three `*-hover`. All `var()` or `color-mix()` |
| Typography | 2 families, 8 `text-*`, 6 heading sizes | Font, Size | `font-heading` (ships as `inherit`, not a family name), `text-line-height`, `heading-line-height` (`calc()` strings, no matching type), `text-font-weight`, `heading-font-weight` (numbers) |
| Spacing | 8 `space-*` | Size | none |
| Layout | 6 widths | Size | none |
| Effects | 7 `radius-*`, `focus-ring-width`, `focus-ring-offset` | Size | `shadow-color` (a `var()`), 5 `shadow-*`, 2 transitions, 5 `z-*`, `focus-ring-color` |

The manifest carries the right value per token: `var(--<name>)` for the 37 sizes, which resolve as expressions and keep one source of truth, and a literal for the 10 that cannot reference.

`font-heading` ships as `inherit`, which is valid CSS and not a family name. It is listed under `needs_site_value`: register it with the site's real heading family, or the body family where the design uses one typeface. Leaving it unregistered means the heading font is the one thing a designer cannot pick from the variable list.

## Colour sourcing

**On an existing site, the site's palette wins.** Read the existing V4 Colour Variables and V3 Global Colors first, map them onto the eight atoms, and put those values in the framework CSS. The framework supplies structure; the site supplies colour. Never install the shipped grayscale over a site that already has a palette.

Propose the atom mapping and get sign-off before writing it. Mapping a palette onto semantic atoms is a design decision, and palettes rarely line up one to one. A site whose "Accent" holds the same value as its "Primary" has no real accent, and choosing one changes how every derived hover and badge reads.

**On a new site, ask for the palette.** Only when none is supplied does the shipped grayscale stand, and say plainly that it is a placeholder.

Either way, check contrast on the real values before building. The shipped defaults are AAA against `bg-body` in both modes; a brand colour dropped into `--primary` carries none of that guarantee.

## The rem trap

The fluid scales are in rem and assume `html { font-size: 62.5% }`, so `1rem` is `10px`.

Themes commonly set a base size on `body` instead, which does nothing for rem. If `html` stays at the browser default, every `clamp()` renders 1.6 times too large and nothing errors. Kadence in particular stores a base font size that applies to `body`.

Check the **computed** font size on `html` on a rendered page. Do not read it off a stylesheet: the value that matters is whatever wins after the theme, the builder and any optimizer have had their say. If it is not 62.5%, either add that rule as part of the install or convert the scales to px before registering anything.

## Install on a site

1. Run the first-run site audit. If the kit already carries a CSS variable layer, migrate it (see above) before adding a second one.
2. Map the site's palette onto the eight colour atoms, and the real font families onto the three font tokens. Get sign-off.
3. Put the generated framework CSS (the `:root` token layer and its `[data-theme="dark"]` block, one generated file) in Elementor's site-wide custom CSS (Site Settings > Custom CSS). This is the one exception to FluentSnippets (router, `styling-and-code.md`): the editor must render the tokens while you build. Never Elementor Custom Code.
4. Verify the computed `html` font size.
5. Register the variables from `assets/variables-manifest.json`: the `registers` list as-is, and each `needs_site_value` entry with the site's real value. Reuse any variable that already exists rather than creating a near-duplicate.
6. Check contrast in both modes.

Dark mode ships in the CSS. Toggling it needs `data-theme="dark"` on the html element from whatever switch the site uses, which is outside this skill.

## Naming and BEM

Token names and class names are separate namespaces and must not blur. Tokens describe values. Classes describe components, carry no framework prefix, and take the house prefix: `md-hero`, `md-hero__title`, `md-card--featured`.

Classes consume tokens. A class sets `padding: var(--space-l)`, never a number.

Flat namespace: see the skill's Styling doctrine.

Where a site's existing classes follow a different convention, say so and let the user choose. Two conventions in one class list is worse than the wrong one applied consistently.

## Using tokens while building

- Every spacing decision is a `space-*` token. A raw value means the scale was not consulted.
- Every heading uses its matching `h1` to `h6` size token, not a `text-*` token picked by eye.
- Body copy is `text-m`. `text-xs` and `text-s` are for captions, labels and legal text.
- Interactive elements take `transition` and the focus-ring trio, so focus states stay consistent and visible without a per-component decision.
- Surfaces use `bg-surface` and `border-color`, not a lightened brand colour.
- Shadows come from the scale. A custom shadow does not adapt in dark mode, where the framework swaps to darker, larger values.

## Extending the framework

Adding a token is a change to the product, not a page decision. It goes into the tokens JSON and the CSS is regenerated, and it takes the same atom-or-molecule treatment: if it can derive from an existing atom, it is a molecule and derives.

Raise it before adding, and raise it as a framework change so it reaches the version that is maintained separately. A token added only to a site's copy is lost on the next version drop, which is the whole reason for the prefix and the generator.

A value that is genuinely site-specific rather than framework-level is not a framework token. It is a `<prefix>-` variable or a class, kept outside the framework block.

## Failure modes

**The 62.5% root is missing.** Everything renders 1.6 times too large and nothing errors. Check this first whenever a V4 build looks oversized.

**A second token layer already exists.** The kit CSS defines its own variables and the framework adds a parallel set. Both work, neither is canonical, and the next edit picks the wrong one. Migrate rather than coexist.

**A bare token name collided.** Framework names are short and unprefixed. A theme defining its own `--primary` at a more specific selector wins, and the framework value silently does not apply.

**A generated file was hand-edited.** The next version drop silently reverts it.

**A molecule was set directly.** The site rebrands and the hover colours stay on the old palette.

**Colour mirror drift.** The CSS was edited and the colour variables were not. The editor picker and the front end disagree, and the picker is the one lying.

**A brand colour broke contrast.** The defaults were AAA, the brand values are not, and nothing in the framework catches it.

**`color-mix()` or OKLCH unsupported.** Both are current-browser features. On a browser matrix that predates them the derived colours resolve to nothing and surfaces render transparent. Raise it rather than work around it silently.
