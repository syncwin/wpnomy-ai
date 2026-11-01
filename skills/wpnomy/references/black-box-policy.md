# Black Box Policy

The operator's workflow standard for every page-builder build. Mandatory for Elementor V4 and Bricks; Elementor V3 is maintain-only under it. Each build skill carries a short gate and its own allowed-element list; this file is the full statement. Where styles and code live is `styling-and-code.md`.

## Contents

0. House resolutions · 1. What "black box" means · 2. Do NOT use · 3. Exceptions · 4. DO use · 5. What to do instead · 6. Decision flow · 7. Why this matters for Atomic Wireframe

## 0. House resolutions

Decided by the operator on 6 Oct 2026 where the policy and the plugin met:

| Point | Resolution |
|---|---|
| Accordions and FAQs | The builder's **nested accordion** is the default (Bricks Accordion Nestable, the V4 atomic accordion when Elementor ships one), styled by classes only and marked builder-bound. `<details><summary>` is the alternative when a page needs zero builder JS. One FAQPage source per page: the accordion's FAQ schema switch stays off wherever the data plugin or the SEO plugin emits FAQPage. This overrides the "Accordion widget" row in section 5 |
| Elementor V3 | Maintain-only. No new V3 pages or parts. Existing V3 pages are edited in place under the V3 skill, and no banned widget in section 2 is added to them |
| HTML / Code element | Primitives first. `details`, `summary`, `dialog`, `ul`, `figure` and the like are built from Div or Block elements with a custom tag. The Code or HTML element is used only when no primitive can output the markup, with code execution enabled by the operator, and logged as builder-bound |
| Element styling (2.6) | Design (type, colour, spacing scale, borders, radius, shadows, states) never lives on an element. Placement one-offs (grid position, order, self-alignment, an instance's own background image, a scoped token override) may, through the element's native fields first and short element custom CSS second. Full ladder and promotion rules: `styling-and-code.md` |
| V3 widget on a V4 page | Last resort for a coverage gap that native HTML cannot fill, with the operator's yes, logged builder-bound with a revisit trigger. Never a widget banned in section 2 |
| Builder-bound log | Every exception in section 3 is written in the scratchpad's Exceptions table with the element, why HTML could not do it, and its documented output markup |

## 1. What "black box" means

A black box element is any builder element where one or more of these is true:

1. It outputs markup you did not write and cannot see or edit in the editor.
2. It ships its own CSS or JS that you cannot override through classes or variables.
3. Its settings are baked into the element (inline styles, per-widget panels) instead of living in a reusable class or token.
4. It cannot be copied cleanly to another builder, because the output depends on that builder's proprietary renderer.
5. It breaks the "one class system, one source of truth" rule. The styling lives in the widget, not in the framework.

**The test before using any element:**
- Can I describe the exact HTML it outputs?
- Can I style every part of it with my own classes and CSS variables?
- Would it survive a copy into another builder as plain HTML plus classes?

If any answer is no, it is a black box. Skip it, unless it earns an exception (section 3).

## 2. Do NOT use

### 2.1 Pre-styled "composite" widgets
These bundle content, layout, and styling into one opaque unit.
- Icon box, image box, info box, feature box, CTA box
- Pricing tables, price lists, flip boxes
- Testimonial, review, and team-member widgets
- Counters, progress bars, circle charts, countdown timers
- Hero or banner widgets, call-to-action widgets
- Social icons, share buttons, star ratings, author boxes, post-info widgets

**Why:** each one hides a wrapper structure and a stylesheet. You cannot restyle them with framework classes without fighting `!important` rules.

### 2.2 Third-party add-on packs
- Anything from Elementor add-on packs, Bricks add-ons, or Oxygen add-ons
- "Pro" widget bundles that add dozens of elements

**Why:** the vendor owns the markup, and the elements vanish if the plugin is deactivated or abandoned.

### 2.3 Legacy or non-atomic structure
- Elementor V3 Section, Column, and Inner Section (use V4 atomic elements only)
- Any element that adds hidden wrapper divs (`.elementor-widget-container`, `.brxe-*-inner`)
- Deprecated or "classic" containers

### 2.4 Builder-native effects and interactions where CSS can do it
- Builder animation panels, scroll effects, parallax, sticky or motion effects, entrance animations
- Hover effects configured per element
- Builder-native "show/hide" conditions used for responsive visibility (use CSS)

### 2.5 Shortcode and widget wrappers
- Generic shortcode elements, WordPress widget areas, "Text Editor" or WYSIWYG blobs holding layout markup

**Why:** unreviewable markup that the builder cannot manage or convert.

### 2.6 Per-element styling in general
- Typography, spacing, colours, borders, shadows set in the element panel instead of through classes

**Why:** this is the biggest black box of all. It turns the page into inline overrides and makes the class system pointless.

## 3. Exceptions (use only when HTML + CSS cannot do the job)

Use a builder-native element when it does something plain HTML cannot (server logic, dynamic data, or complex accessible JS). Even then, it must follow three conditions:
1. All visual styling is done with classes and variables, never the element panel.
2. The element's output markup is documented and predictable.
3. You note it as a "builder-bound" block, because it will not copy cleanly to other builders.

| Need | Allowed element | Condition |
|---|---|---|
| Dynamic lists | Query loop / Collection / Repeater | Style the loop item with classes only |
| Dynamic data | Dynamic data tags, ACF/meta fields | Output into plain elements |
| Forms with backend handling | The builder's form element, or a dedicated form plugin | Style fields by class; label and error states accessible |
| Navigation with mobile toggle | Nav / Nested nav element | Keep markup `<nav>` + `<ul>`; style by class |
| Real carousels (needs Swiper-grade touch, loop, a11y) | Nested slider element | Only if CSS scroll-snap is not enough |
| Maps, embeds, video with privacy mode | Map / Video element | Use lazy-load or facade |
| Commerce | Woo cart, checkout, product elements | No alternative exists |
| Templates and reuse | Component / Template / Slot | These are structure, not styling |
| Search, comments, pagination, breadcrumbs | Native element | Server-rendered output you cannot hand-write |

Rule of thumb: **functional black boxes are tolerated, visual black boxes are not.**

## 4. DO use (the primitive set)

These are thin wrappers around real HTML. You can predict the output, and they accept classes.

| Primitive | HTML it should output |
|---|---|
| Section / Container / Block / Div (tag selectable) | `section`, `div`, `header`, `main`, `footer`, `article`, `aside`, `nav` |
| Heading | `h1` to `h6` |
| Text / Basic text | `p`, `span` |
| Rich text | Only for long, editor-owned prose |
| Button / Link | `a` or `button` |
| Image | `img` (with width, height, alt, `loading`, `srcset`) |
| Icon / SVG | Inline `svg` |
| List | `ul`, `ol`, `li` |
| HTML / Code element | Any custom markup you author |
| Video | `video` or lazy iframe |
| Nested accordion / tabs (Bricks nested, Elementor V4 atomic) | Acceptable because they are composed from primitives you can class |

Per-builder preference:
- **Bricks:** Section, Container, Block, Div, Heading, Text Basic, Button, Image, Icon, SVG, Code, plus nested elements and Query.
- **Oxygen 6:** Section, Div, Heading, Text, Link, Image, HTML Code, Icon, Repeater.
- **Elementor V4:** atomic elements only (Div Block, Flexbox, Heading, Paragraph, Image, Button, SVG, Divider), with classes and variables.
- **Builderius:** HTML elements, containers, collections, templates.

## 5. What to do instead

| Instead of this widget | Do this |
|---|---|
| Accordion widget | `<details><summary>` (use `name=""` for exclusive groups). House default is the nested accordion (section 0) |
| Modal / popup builder | `<dialog>` or the Popover API (`popover` attribute) |
| Tabs widget | Radio-input pattern, or `<details name>` for simple cases; small vanilla JS for ARIA tabs |
| Simple carousel | CSS `scroll-snap` row with `overflow-x: auto` |
| Gallery / masonry | CSS Grid (or `columns`) with `<figure>` items |
| Icon box / feature box | Block (class) + inline SVG + Heading + Text |
| Pricing table | Grid of Blocks with classes, `<ul>` for features |
| Testimonial slider | Blockquote cards in a scroll-snap row |
| Counter / progress bar | `<progress>`, `<meter>`, or CSS counters; tiny JS only if animating |
| Countdown | A `<time>` element plus a tiny script |
| Tooltip | `popover` or CSS `anchor-positioning` / `title` |
| Parallax / scroll effects | CSS `animation-timeline: scroll()` or `view()` |
| Entrance animations | CSS classes plus an `IntersectionObserver` utility class |
| Responsive show/hide | Utility classes with media or container queries |
| Sticky header | `position: sticky` on the class |
| Social share / ratings | Plain links with inline SVG; JSON-LD for ratings |
| Button variants | One `.btn` class with modifier classes (`.btn--primary`) |
| Spacing and typography | Framework utility classes and CSS variables (tokens), never panel overrides |
| Colour / dark mode | CSS variables with `prefers-color-scheme` and a `data-theme` switch |

General rule: **semantic HTML first, CSS second, tiny vanilla JS third, a builder widget last.**

## 6. Decision flow

1. Can plain semantic HTML plus classes do it? **Use that.**
2. Does a native HTML feature cover it (`details`, `dialog`, `popover`, `scroll-snap`)? **Use that.**
3. Does it truly need server logic or dynamic data (query, form, commerce, nav)? **Use the builder-native functional element, styled by classes only, and mark it builder-bound.**
4. Needs real JS behaviour (complex slider, ARIA tabs)? **Use a nested or atomic element built from primitives, or a small script. Avoid the pre-styled widget.**
5. Otherwise: **don't add it.**

## 7. Why this matters for Atomic Wireframe

- Blocks in the library are plain HTML plus framework classes, so one copy works across Bricks, Oxygen 6, Elementor V4, and Builderius.
- Black-box widgets cannot be translated between builders, so they break the multi-format Copy menu.
- Class-based styling keeps the design system in one place, which makes global changes and dark mode work.
- Output stays lean, accessible, and indexable, which helps performance, SEO, and AEO.

**Rules for library blocks:**
- No element-panel styling.
- No add-on widgets.
- No composite widgets.
- Builder-bound functional elements are flagged and kept out of the "universal" set.
