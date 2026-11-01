# Styling and code placement

The one ladder for where a style or a piece of code lives, on Elementor V4 and Bricks. The black box policy decides **what** gets built; this file decides **where its styling and code go**. Each build skill keeps only a short map of these steps to its own controls. Elementor V3 edits keep the V3 doctrine (globals, no classes) and use step 7 for anything large.

## Contents

The principle · Reuse first · The ladder · Element level: what is allowed · Promotion rules · FluentSnippets rules · CSS standards · Logging

## The principle

Design lives in tokens and classes; placement can live on an instance. Typography, colour, spacing scale, borders, radius, shadows and states are design: they always live in variables and classes, so one change updates every page. Where one element sits inside one parent (grid area, order, self-alignment, a one-off offset, its own background image) is placement: it may live on that element, because no other element shares it. This is how the policy's section 2.6 ("no per-element styling instead of classes") is applied.

## Reuse first

Before styling anything, look in this order and stop at the first hit:

1. An existing **component** that already is this structure: place an instance, set its properties.
2. An existing **class or modifier** that already is this look: apply it.
3. An existing **token** for every value: never a literal except `0`, `1px` hairlines, `100%` and `auto`.

Only then create something new, at the lowest step of the ladder that can hold it.

## The ladder

| Step | Where | Use it for |
|---|---|---|
| 1 | **Tokens** (variables from the Atomic Framework) | Every value. Never a near-duplicate token for one section |
| 2 | **Class, native style fields** (the builder's controls on a global class) | All design: type, colour, spacing, border, radius, shadow, layout of the block, hover and focus states, responsive values |
| 3 | **Class custom CSS** (the class's own CSS field) | What no field expresses, still reusable: compound states (`.block.is-active`), `:focus-visible` rings, `color-mix()`, container queries, `:has()`, scroll-driven animation |
| 4 | **Component** (with properties, and a `class` property for variants) | Structure used more than once. Styling stays in the classes inside it |
| 5 | **Element, native style fields** | Placement one-offs only (see below), values from tokens |
| 6 | **Element custom CSS, short** | A placement one-off no field expresses: one rule, up to about 10 declarations, tokens only, no `@keyframes`, no `@font-face` |
| 7 | **FluentSnippets** | Anything large, site-wide or shared across builders: utility sets, the dark-mode block, `@keyframes`, small vanilla JS, PHP hooks (query vars, echo allow-list, filters). Data goes in the AuraKeyRealty Data plugin, never a snippet |

Not used for new work: the builder's global custom-code areas (Bricks Settings custom code, Elementor site-wide Custom Code) and child-theme files, because code split across several places is code nobody finds. Existing code found there is moved to FluentSnippets when that area is next touched, with a yes. One exception: design-system foundation CSS the editor itself must render while you build (the Atomic Framework token layer on Elementor V4: its `:root` block and the dark block generated with it) stays in Elementor's site-wide custom CSS, because a snippet that loads only on the front end leaves the editor unstyled.

## Element level: what is allowed

| Allowed on an element (steps 5 and 6) | Never on an element (always a class) |
|---|---|
| `grid-column`, `grid-row`, `order`, `align-self`, `justify-self` | Font family, size, weight, line height, colour |
| A one-off offset or `z-index` for overlap in this layout | Padding, margin or gap that follows the spacing scale |
| This instance's own background image or `object-position` | Background colour, border, radius, shadow |
| `aspect-ratio` or a max width for this one media slot | Hover, focus and active states |
| A token override scoped to this instance (`--card-cols: 4`) | Anything responsive that other elements also need |

When unsure, it is design, and it goes on a class.

## Promotion rules

DRY is enforced by promotion, not by hoping:

- The same element-level style appears on a **second** element: it becomes a modifier class, and both elements use it.
- The same structure appears on a **second** page or template: it becomes a component.
- Element custom CSS grows past one short rule, or needs a media query beyond one breakpoint: it becomes a class (step 2 or 3).
- Class custom CSS is needed by **more than one** class, or by markup the builder does not own: it moves to one FluentSnippets snippet.
- A snippet's rule turns out to style one block: it moves back onto that block's class.

## FluentSnippets rules

- One snippet per concern, named `<prefix>-<purpose>` (`md-utilities`, `md-dark-mode`, `md-query-vars`), with a header comment: what it does, where it applies, who added it and when.
- Load only where needed: FluentSnippets' location and condition settings scope CSS and JS to the pages, post types or templates that use them. Site-wide only when every page needs it.
- CSS reads tokens only and stays flat and low-specificity (one class deep where possible); JS is vanilla, deferred, and scoped to a `js-` class.
- PHP snippets follow WordPress coding and security standards (sanitize input, escape output, capability checks) and are tested on staging before live.
- Back up the snippet before changing it on a live site; one snippet change at a time, verified on the front end.

## CSS standards

From the WordPress CSS coding standards, applied at every step:

- Flat, low-specificity selectors; never `!important`, never an ID selector except the builder's own element selector at step 6.
- `rem` and tokens for type and spacing; unitless line height.
- Logical properties (`margin-inline`, `padding-block`, `inset-inline-start`) so a right-to-left language never needs a second stylesheet.
- One declaration per line; group by display and position, box model, colour and type, then the rest.
- Mobile-first: the base value is the smallest screen; wider breakpoints layer up.

## Logging

Every step 5, 6 and 7 use is a line in the scratchpad: the element or snippet, what it does, and why a lower step could not hold it. Steps 1 to 4 need no log. A build with many element-level lines is a signal that a class or component is missing.
