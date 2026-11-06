---
name: wpnomy-bricks-expert
description: Build and edit Bricks Builder pages, templates, components, forms and design systems under the house black box policy, and map the Atomic Framework from the Atomic Wireframe plugin into Bricks global variables, theme styles, breakpoints and BEM global classes. Use when the target site runs the Bricks theme, when the user says Bricks, Bricks template, global class, Bricks component, query loop, query filter, Bricks form, nav nested, mega menu, Bricks dynamic data or conditions, when Atomic Wireframe tokens or blocks need to reach Bricks, or when wpnomy routes here after the builder question. Covers the ability call order through Novamira, the writes that save fine and render wrong, ACF binding, media for migrations, and front-end verification. Do NOT use for Elementor work.
license: MIT
metadata:
  displayName: "WPnomy Bricks Expert"
  version: "0.1.7"
  author: "@wasimness"
  company: "SyncWin"
---

# WPnomy Bricks Expert

Reached from `wpnomy`, which owns intake, design standards, handover and the scratchpad. This file carries the Bricks build rules. Fill the scratchpad's **Bricks canon** block, not the Elementor one.

Built for Bricks 2.4 with its Abilities API, called through Novamira's `mcp-adapter-execute-ability` with slash names (`bricks/get-design-context`). Many enabled abilities are dispatcher-only and never appear as direct tools: a missing tool is not a disabled ability; check `bricks/list-ability-status` with `abilityNames`. Runtime reads beat every example in these files: when a live schema or readback disagrees with a rule here, follow the site and log the difference.

## Precedence

1. **This plugin** decides conventions, naming, design and safety.
2. **The official Bricks skills (Codeer, v0.1.1)** are distilled into `references/`. They are not installed; this skill carries what matters from them.
3. **Novamira Pro's Bricks skills** (`bricks-build-page`, `bricks-element-gotchas`, `bricks-nestables`, `bricks-components`, `bricks-page-settings`) are a fallback for mechanics only. Load one with `novamira/skill-get` when a mechanic is missing here, and say which rule here overrode it.

## The design source

The **Atomic Wireframe** plugin holds the site's design: the 80-token Atomic Framework, the fluid scales, root font size, breakpoints, the class prefix and per-class renames, a 139-block BEM library and saved pages. Read it with `atomic-wireframe/get-project`. It is the source of truth; Bricks is where it is realised.

- Never change an Atomic Wireframe project (tokens, settings, classes, pages) without an explicit yes. Its design is the user's product.
- Never let Bricks regenerate a scale the framework owns. Details in `references/design-system.md`.
- If the plugin is absent, ask for a framework export before inventing any token.

## Black box gate

Every element passes this gate before it is placed. Full statement: the router's `references/black-box-policy.md`.

| | Bricks elements |
|---|---|
| **Primitives (use)** | `section`, `container`, `block`, `div` (tag or custom tag), `heading`, `text-basic`, `button`, `text-link`, `image`, `icon`, `svg`, `list`; `text` (Rich Text) only for long editor-owned prose or a field that returns HTML |
| **Builder-bound (allowed, classes only, logged)** | Query loops, `form`, `nav-nested` with `dropdown` and `offcanvas`, Accordion Nestable (house default for FAQs), Tabs Nestable, `slider-nested` only where `scroll-snap` cannot do it, `video` with a facade, `map`, search, pagination, breadcrumbs, post comments, components, templates, slots |
| **Never** | Composite elements (icon box, image box, alert, pricing tables, testimonials, team members, counter, progress bar, pie chart, countdown, social icons, rating, post meta and post taxonomy as styled widgets, logo carousels), Bricks add-on packs, design styling set on an element (type, colour, spacing, borders, shadows, states), interaction or animation panels where CSS can do it, element conditions for responsive visibility, `shortcode` and `wordpress` widget elements holding layout |

The three questions: can the exact output HTML be described, can every part be styled by our classes and variables, would it survive a copy to another builder as HTML plus classes. Any no: skip it or log it as builder-bound in the scratchpad with its output markup.

## Doctrine

**What to build** follows the policy's decision flow: semantic HTML from primitives first; a native HTML feature (`details`/`summary`, `dialog`, `popover`, `scroll-snap`, `position: sticky`) built from `div` or `block` with `tag: "custom"`, `customTag` and `_attributes`; a builder-native functional element (loop, form, nav, nestable, filter) only for server logic or dynamic data, logged builder-bound; a component for any structure used twice.

**Where styling and code go** follows the router's `references/styling-and-code.md`. In Bricks terms:

| Ladder step | Bricks |
|---|---|
| Tokens | Global variables (`var(--space-m)`) |
| Class native fields | The global class's style controls (`_typography`, `_padding`, `_background`, `_border`, `_gap`...), with breakpoint and pseudo suffixes (`_padding:bp768`, `_background:hover`) |
| Class custom CSS | The class's own custom CSS, selector `.md-block` |
| Component | Bricks component, `class` property with options and `replace: true` for variants |
| Element native fields (placement only) | Placement controls as the live element schema names them (`_order`, `_alignSelf`, `_gridItemJustifySelf`, `_zIndex`, `_aspectRatio`, `_position` with `_top`...), and this instance's own background image |
| Element custom CSS, short (placement only) | `_cssCustom` as a full rule with the persisted selector: `#brxe-<id>` on a page element, `.brxe-<id>` inside a component, the custom id if `_cssId` is set (`%root%` is the editor's shorthand for the same). Grid placement with no field and scoped token overrides go here: `#brxe-<id> {\n  grid-column: span 2;\n  --card-cols: 4;\n}` |
| FluentSnippets | Utility sets, the dark-mode block, `@keyframes`, vanilla JS scoped to a `js-` class, PHP hooks (`bricks/posts/query_vars`, echo allow-list). Never Bricks Settings custom code or child-theme files for new work |

Rules that follow:

- No literal except `0`, `1px` hairlines, `100%` and `auto`: every value is a variable.
- Design (type, colour, spacing scale, borders, radius, shadows, states) is never set on an element. A second use of any element-level style promotes it to a modifier class.
- No inline `style` attributes. Library markup that carries one becomes a class.
- Interactions only where no CSS or native HTML route exists (popup opener, offcanvas toggle, load more), because each adds inline `data-interactions` JSON and its own JS. Hover and focus are class pseudo states.
- Element conditions are render logic (a missing field, a user state), never styling and never responsive visibility.
- Never `!important`. Fix the cascade order instead (see `references/elements-and-pages.md`).
- Class prefix is `<prefix>` (router, Naming: ask first, site code only as the default), read from the Atomic Wireframe project's `classPrefix` every run; never assume it.
- `js-` hook classes go in the element's plain `_cssClasses`, not as global classes.
- The Code element and `execute-php` only with an explicit yes.

## Workflow

**0. First run on a site.** Run the Bricks audit in `references/verify.md`. Read-only. Record the canon.

**1. Read before writing.** `bricks/get-design-context` (summary), `atomic-wireframe/get-project`, `bricks/list-breakpoints`, `bricks/list-templates`, and `bricks/find-post` plus `bricks/get-page-structure` for an existing page. Mark each resource the brief needs as exists, missing or ambiguous. Reuse what exists; never create a second class, variable or component for something already there under another name.

**2. Plan.** Section plan in the scratchpad: element tree, classes, component instances, dynamic sources, conditions. Get agreement before any write.

**3. Design system first.** Variables, theme style, breakpoints, fonts, then classes, then components. Content after. Template conditions and menus last. Destructive steps last within each tier. Load `references/design-system.md` and `references/bem-classes.md`.

**4. Build.** Load `references/elements-and-pages.md` for trees, imports and media; `references/templates-and-components.md` for components, templates, navigation, nestables, popups and interactions; `references/dynamic-data.md` when any value comes from ACF, a loop, a filter or a condition; `references/forms.md` for any form.

**5. Verify.** Load `references/verify.md` and run the gate. A save is not a result.

## Write safety

- Ask which environment the site is and confirm it against what the connector reports. On production every change is proposed first and applied one at a time.
- Global data (variables, classes, palettes, theme styles, breakpoints, settings, menus) has **no revisions**. Before changing any of it on a site with content, export a transfer package (`bricks/list-transfer-items`, `bricks/export-transfer-package`) and keep the zip.
- `bricks/set-page-elements` replaces the whole tree. To add a section, use `bricks/add-element` with `parentId` and `position`. `bricks/update-component` also replaces the whole tree.
- Every global write needs fresh ownership values from one read. On a stale-ownership or digest error, re-read and rebase. Never resend the same payload and never build ownership from `get-design-context.version`.
- On any `bricks_*` validation error, fix the shape. Do not retry unchanged.
- A disabled ability (`bricks_ability_disabled`) is final. Report it; never route around it with `execute-php`.
- Deletes, publishes and overwrites need an explicit yes. Report-only requests authorise no fixes.
- Never edit, deactivate or update Novamira or Novamira Pro.

## Delivery

Two methods, chosen at intake:

| Method | Output |
|---|---|
| Novamira direct | Writes through abilities, verified on the front end |
| Files | Bricks clipboard JSON for a section (`source: "bricksCopiedElements"`, pasted on the canvas with cross-site copy and paste on), or a transfer package zip for a set of templates, classes and variables |

A clipboard file carries its `globalClasses` with names matching the target site's existing classes, so the paste reuses them. Never ship element ids or class ids from another site as if they exist on the target.

## References

| Read when | File |
|---|---|
| Tokens, palette, theme styles, fonts, breakpoints, root font size | `references/design-system.md` |
| Naming, creating or applying any class | `references/bem-classes.md` |
| Element trees, custom tags, write routes, Atomic Wireframe blocks to Bricks, media and migration assets | `references/elements-and-pages.md` |
| Components, templates and conditions, headers and footers, navigation and mega menus, nestables, popups, interactions | `references/templates-and-components.md` |
| ACF values, query loops, global queries, query filters, element conditions, hide on empty | `references/dynamic-data.md` |
| Any form (contact, home evaluation, lead capture) | `references/forms.md` |
| First run on a site, verifying any write, handing back | `references/verify.md` |

## Before handing back

- [ ] Black box gate passed; every builder-bound element logged with its output markup.
- [ ] Styling ladder followed: element-level styles are placement one-offs only, each logged; nothing used twice left on an element.
- [ ] Every value reads a variable. `bricks/render-elements` shows `var(--...)` in the output, not a raw value.
- [ ] Classes follow `references/bem-classes.md`, carry the project prefix, and none duplicates an existing one.
- [ ] Repeated sections are component instances, not copies.
- [ ] Header and footer roots carry no `header` or `footer` tag (Bricks wraps them).
- [ ] Every template and theme style has conditions, and the winner is the intended one.
- [ ] Every dynamic tag previewed with `bricks/preview-dynamic-tag` and `unknownTags` empty.
- [ ] Every bound block hides on an empty value, tested on a complete and a sparse record.
- [ ] Checked logged out on the front end at every Bricks breakpoint. CSS regenerated if CSS loading is set to files.
- [ ] Transfer package exported before any global change on a site with content.
- [ ] Scratchpad complete, including every condition in plain language.
