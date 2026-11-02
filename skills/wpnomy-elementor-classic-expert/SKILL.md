---
name: wpnomy-elementor-classic-expert
description: 'Maintain and edit existing Elementor V3 pages and theme builder parts: flexbox and grid containers, classic widgets, Global Colors and Global Fonts. Maintain-only: new pages are built in V4 or Bricks. Use when an existing Elementor 3.x page, part or export needs a change, when the user says V3, classic, containers or widgets about existing work, or when wpnomy routes here after the version question. Covers container structure, semantic HTML tags, responsive control keys, the control traps that fail silently, and the classless globals-only styling doctrine V3 requires. Do NOT use for Atomic Elements, Global Classes, Variables or Components, which are wpnomy-elementor-atomic-expert.'
license: MIT
metadata:
  displayName: "WPnomy Elementor Classic Expert"
  version: "0.1.4"
  author: "@wasimness"
  company: "SyncWin"
---

# WPnomy Elementor Classic Expert (V3)

V3 rules only; shared intake and handover live in the `wpnomy` router.

**Maintain-only.** V3 is kept for editing pages and parts that already exist in V3. No new V3 page, template or part is started; new work goes to `wpnomy-elementor-atomic-expert` or `wpnomy-bricks-expert`, and a request for a new V3 build is answered with that routing. Never convert or partly migrate an existing V3 page unless asked.

**Black box gate on edits.** The router's `references/black-box-policy.md` applies to anything added: no composite widget (icon box, image box, CTA, pricing, testimonial, counter, progress bar, countdown, hero, social icons, star rating, author box, post info), no add-on pack widget, no legacy Section, Column or Inner Section, no animation, motion, parallax or entrance effect panels, and no Text Editor holding layout markup. Where an edit needs one of these, raise it: the fix is usually a V4 rebuild of that section, not a new black box on the V3 page. The V3 styling doctrine below stays for the existing page, because V3 has no class system to move to. Code too large for page-level custom CSS, and any script or PHP, goes in FluentSnippets per the router's `styling-and-code.md`, step 7.

Open the router's build scratchpad at the start of every edit and log each change, exception and verification in it.

## Pairs with

`elementor-build-page` for building through Novamira, and `kadence-build-page` where the work reaches theme settings rather than the page. Use them for mechanics only (router, Novamira skills).

## Styling doctrine

V3 has no real class system and no native variables. Forcing a framework workflow onto it produces per-widget CSS nobody can maintain, so V3 builds are classless and use Elementor's own system as designed.

| Do | Don't |
|---|---|
| Pick colours from Global Colors only | Type or paste a hex into any colour control |
| Pick typography from Global Fonts only | Set font family, size or weight per widget |
| Control spacing with container padding and gap | Use margins for spacing that padding or gap owns |
| Reuse the spacing values already on the site | Introduce a new spacing value for one section |
| Use native controls throughout | Write custom CSS or classes for anything native controls and globals can do |

If a needed colour or font is not in the globals, stop and ask. A one-off hex is the exact failure this rule prevents.

Exception: a data table or similar block that genuinely needs markup lives in an HTML widget (see Widgets), styled in page-level custom CSS with `<prefix>-` classes and confined to that block.

The Atomic Framework does not apply here. It depends on V4 Variables and Classes, and a V3 page cannot read them. Do not import its CSS onto a V3 page to get around the doctrine above.

## Structure

- Flexbox containers for every layout. Grid containers where the layout is genuinely a grid. Never legacy sections and columns.
- Nested containers carry `isInner`.
- Semantic HTML tag on every container: `section`, `article`, `header`, `footer`, `aside`, `nav`, `main`. `div` only where nothing else is correct.
- Name every container in the Navigator for its role. An unnamed tree is unmaintainable.
- Keep nesting shallow: wrapper, row, children. Reaching for a fourth level usually means a gap or align setting was missed.
- Widths in percentages with tablet and mobile overrides. Every multi-column row stacks to full width on mobile.
- Responsive values use the `_tablet` and `_mobile` suffixes.

## Control traps

Each of these fails silently rather than erroring, which is why they are worth memorising.

| Trap | Correct form |
|---|---|
| Widget custom width | `_element_width: initial` plus `_element_custom_width`. There is no `custom` value |
| Container width | `width` only applies when `content_width: full` |
| Spacing keys | Containers use `margin` and `padding`. Widgets use `_margin` and `_padding` |
| CSS class keys | Containers use `css_classes`. Widgets use `_css_classes`. The widget key on a container does nothing |
| Batch edits | Change the elements tree and save once. Per-element saves time out past roughly forty elements |

## Widgets

Prefer native. For an accordion or FAQ, use the Nested Accordion widget (the house default). One FAQPage source per page: leave its FAQ schema off wherever the data plugin or the SEO plugin emits FAQPage.

Reserve the HTML widget for markup no native widget can produce. Put its styling in page-level custom CSS rather than inline, and prefix any class `<prefix>-` (router Naming: ask first) so it cannot collide with theme or plugin classes.

## Direct-write notes

When building through Novamira rather than emitting JSON, after any direct meta write: flush the object cache, delete `_elementor_css`, regenerate the post CSS, and run it twice, because the object cache serves stale page settings on the first pass.

Clear every cache layer after a change (router `references/site-audit.md`, caches row).
