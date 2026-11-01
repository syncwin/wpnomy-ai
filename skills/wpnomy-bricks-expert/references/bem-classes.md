# BEM global classes

The naming follows the Atomic Wireframe block library, which is the house reference for how classes are written. The prefix replaces the library's `awf-`.

## The prefix

- Read `classPrefix` from `atomic-wireframe/get-project` every run. The library's `awf-btn` exports as `<prefix>-btn`.
- It is the site's own short code, lowercase kebab-case (for example `md`). A missing or malformed prefix is a question, not a value to use.
- Per-class renames (`class_renames`) from the project apply on top. Use the renamed name exactly.
- Classes already on a site under another convention are matched when editing that old work, and never adopted for new work.

## Anatomy

| Part | Form | Library examples |
|---|---|---|
| Block | `<prefix>-<block>` | `btn`, `card`, `section`, `stat-grid`, `faq`, `footer` |
| Element | `<block>__<element>` | `section__head`, `section__title`, `footer__bottom`, `faq__question` |
| Modifier | `<block>--<modifier>` or `<block>__<element>--<modifier>` | `btn--primary`, `card--flat`, `section__head--tight` |
| State | `is-<state>`, unprefixed | `is-active`, `is-featured`, `is-on` |
| Utility | `<prefix>-<utility>` | `bg-surface`, `bg-accent` |

Rules the library follows, which the build follows too:

- **Kebab case, nouns for blocks.** A block names the thing (`plan-card`), never its look (`blue-box`).
- **One element level.** `card__title`, never `card__body__title`. A nested part that needs its own parts is its own block.
- **A modifier never stands alone.** The element carries `btn btn--primary`, and the modifier sets only what differs.
- **Modifier families are consistent.** Tone: `--primary`, `--secondary`, `--ghost`. Density: `--tight`, `--loose`, `--flush`. Size: `--sm`, `--lg`. Layout counts and ratios: `card-grid--3`, `split--60-40`, `stat-grid--4`.
- **States are styled only with their block.** `.pill.is-active`, never `.is-active` alone. States are set by an interaction, a condition or the element's own behaviour, not by hand.
- **Utilities are rare and single-purpose.** A surface or background switch, nothing that mixes layout and colour.
- **A name is never reused for a different pattern.** The library split `list-head` from `section__head` because one name doing two layouts broke both. Check the existing class list before naming.
- **No bare inner classes.** A few library atoms style unprefixed children (`.checkbox .box`, `.toggle .knob`, `.track`, `.dot`). In Bricks these become proper elements: `<prefix>-checkbox__box`, `<prefix>-toggle__knob`.
- **Every value reads a token.** The library CSS still carries some literal sizes (`padding:1.25rem`, `gap:2.5rem`, `max-width:560px`). When porting a rule into Bricks, map each literal to the nearest token (`space-m`, `space-xl`, `max-width-s`) and log the mapping. Never carry the literal.

## Layout primitives

These carry structure, so pages stay shallow:

| Class | Role |
|---|---|
| `section` | Vertical rhythm (`space-xl`), modifiers for tight and flush |
| `container` | Site width (`container-width`) and side gutter (`space-l`) |
| `section__head` | Centred intro: eyebrow, title, description, capped width |
| `split` with `--50-50`, `--60-40`, `--40-60`, `--70-30`, `--30-70` | Two-column grid |
| `card-grid` with `--2`, `--3`, `--4` | Card grid; the base owns the responsive collapse |
| `stat-grid`, `split-stack`, `media-row` | Specific repeaters |

In Bricks, a `section` element plus its Bricks `container` already does part of this. Use the class on the Bricks element of the same role rather than adding a wrapper div for it.

## Styling a class in Bricks

1. **Look first.** `bricks/list-global-classes` (or `get-design-context`). Names are unique site-wide; `btn` and `button` are the same resource.
2. **Native controls first.** Class settings use the element-setting shape: `_padding`, `_typography`, `_background`, `_border`, `_gap`, with values from variables. Responsive values use the breakpoint key suffix (`_padding:bp768`); hover and focus use pseudo suffixes (`_background:hover`).
3. **Class custom CSS for the rest.** Compound states (`.md-pill.is-active`), `:focus-visible` rings with the framework's two-band ring, `color-mix()` borders, `:not()`. Selector is the class itself; never an element id.
4. **Mobile-first.** The unsuffixed value is the smallest screen. The library's few `max-width` media queries are rewritten as min-width values on the matching breakpoint key.
5. **Check the modifier wins.** Bricks writes each class as a single selector. If a modifier loses to its base on the front end, move that rule into the modifier's custom CSS as `.<block>.<block>--<mod>`, as the library does. Never `!important`.
6. **Render before committing in bulk.** `bricks/render-elements` with one element carrying the class shows the emitted CSS.

Creating several classes at once: `bricks/batch-create-global-classes` with `expectedOwnership` from a fresh `list-global-classes`. A single `create-global-class` needs none. Updates and deletes need the target's `itemOwnership` and `lockOwnership`.

Do not pre-create modifiers the build does not use. Do not paste the whole library CSS into the site: unused rules are dead weight, and styles outside the class manager are invisible to the next editor.

## Applying classes

- Elements reference classes by **id** in `_cssGlobalClasses`, never by name. Resolve names to ids from the class list.
- Element-level styles on a classed element are placement one-offs only, logged in the scratchpad; the second use becomes a modifier (router, `styling-and-code.md`).
- A component exposes a class choice through a `class` property with named options and `replace: true` for true variants (see `templates-and-components.md`).
- Script and interaction hooks use a plain `js-` class (`js-faq-toggle`) in the element's `_cssClasses`, never a global class and never an element id, because ids change on duplication.

## Auditing

`bricks/audit-design-system` (read-only) with `scope` `all`, `orphans`, `unused`, `theme-styles` or `palettes`, and `skipPostScan: true` for a fast pass. Errors are orphan class, variable and component references, which render wrong; "unused" is bounded evidence, not proof. It does not find naming drift or two classes doing one job; check those by reading the list against this file. Report; do not fix without a yes.
