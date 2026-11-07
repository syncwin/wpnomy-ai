---
name: wpnomy-elementor-atomic-expert
description: Build and edit Elementor V4 pages and theme builder parts with Atomic Elements, Variables, Global Classes, Components and Interactions, and install or extend the Atomic Framework design system on a site. Use when the target site or the supplied export is Elementor V4, when the user says V4, atomic, Global Classes, Variables, Components, design tokens or BEM, when they ask to map the Atomic Framework onto Elementor, when a V4 page needs a change, or when wpnomy routes here after the version question. Covers the token-to-variable mapping, the atomic widget coverage gap, BEM class naming in a flat namespace, and the CSS escalation order. Do NOT use for Elementor 3.x containers and classic widgets, which are wpnomy-elementor-classic-expert.
license: MIT
metadata:
  displayName: "WPnomy Elementor Atomic Expert"
  version: "0.1.8"
  author: "@wasimness"
  company: "SyncWin"
---

# WPnomy Elementor Atomic Expert (V4)

Reached from `wpnomy`, which owns intake, design standards, JSON delivery and handover. This file carries V4 build rules only.

Requires Elementor Core 3.29+ with the Atomic Editor activated, and is on by default from 4.x.

Open the router's build scratchpad at the start of every build and keep it current: intake, plan, decisions, builder-bound exceptions and verification.

## Pairs with

`elementor-build-page` for building through Novamira, and `elementor-convert-to-v4` when an existing V3 page is being moved across. Load them for the mechanics; the conventions here lead where they differ.

## Black box gate

Run before placing any element. Full statement: the router's `references/black-box-policy.md`.

| Allowed (primitives) | Div Block, Flexbox, Heading, Paragraph, Image, Button, SVG, Divider, with Global Classes and Variables |
|---|---|
| Allowed, builder-bound | Atomic Form, atomic Tabs, the atomic accordion when Elementor ships one (house default for FAQs), YouTube or video with a facade, Loop Grid for dynamic lists, Nav Menu, search, pagination, breadcrumbs, Components. Styled by classes only; each logged with its output markup |
| Never | Classic composite widgets (icon box, image box, CTA, pricing, testimonial, counter, progress, countdown, hero, social icons, star rating, author box, post info), add-on pack widgets, legacy Section, Column or Inner Section, motion and entrance effects, per-element hover effects, display conditions for responsive visibility, Text Editor holding layout markup |

1. Can the element's exact output HTML be described? 2. Can every part be styled by our classes and variables? 3. Would it survive a copy to another builder as HTML plus classes? Any no: skip it, or log it as a builder-bound exception.

Use Elementor's native features first (check the official Elementor docs); custom code only when nothing native exists. UI or functions that do not depend on Elementor go in one global place and power the whole site from there: FluentSnippets for functions, Elementor Code Snippets where relevant.

## Check the install first

Several capabilities ship as feature flags and are off by default on some installs. Confirm each before planning around it, and report anything missing rather than silently designing around it.

| Feature | Matters because |
|---|---|
| Global Classes | The whole class workflow depends on it |
| Variables, and Variables Manager | Without the Manager, variables can be consumed but not authored |
| Components | Without it there is no reusable layout primitive |
| V4 Custom CSS | Without it, per-element CSS is unavailable and code moves up the escalation order |

## Styling doctrine

This is where the Oxygen and Bricks workflow carries over, because V4 has the primitives for it.

**Variables are the tokens.** Colours, typography and sizes live as Variables. Read the site's existing set first and use it. Never hardcode a value a variable already expresses, and never create a near-duplicate because the existing name was not obvious.

**Classes carry the styling**, named in BEM: `block`, `block__element`, `block--modifier`. Style the class, not the element. Any class this plugin invents takes the site's class prefix, `<prefix>-` (router, Naming: ask first). An element styled locally is a one-off the next page cannot reuse.

V4 Global Classes are a flat namespace with no descendant selectors. BEM is built for exactly that, so it fits, but context has to live in the class name rather than a parent selector. A `card__title` that differs inside two blocks needs two class names, not a nested rule.

**Design never lives on an element.** Typography, spacing, colour, border, shadow and states live in classes and variables. An element's own style controls hold placement one-offs only (router, `styling-and-code.md`), and a second use becomes a modifier class.

## The Atomic Framework

The house design system, maintained separately as a product: 72 tokens across Colors, Typography, Spacing, Layout and Effects, in OKLCH, fluid by `clamp()`, with a dark variant. Token names pass through exactly as the framework writes them.

Read `references/atomic-framework.md` before installing it, extending it, or mapping any token onto a V4 Variable. A new framework version is a re-run of `scripts/build_framework.py` against the new tokens JSON, never a hand edit of the generated files.

One rule worth carrying even if nothing else is read: the framework needs `html { font-size: 62.5% }` so that `1rem` is `10px`. Without it every rem value renders 1.6 times too large, and nothing errors.

## Styling and code placement

The router's `references/styling-and-code.md` is the ladder. In V4 terms:

| Ladder step | Elementor V4 |
|---|---|
| Tokens | Variables (and the framework CSS layer for tokens V4 cannot hold) |
| Class native fields | The Global Class's style tab, per breakpoint and per state |
| Class custom CSS | V4 Custom CSS on the class (compound states, `:focus-visible` rings, `color-mix()`, container queries, scroll-driven animation) |
| Component | Elementor Component exposing only the properties that vary |
| Element native fields (placement only) | The element's local style controls: order, self-alignment, grid placement, position offset, z-index, aspect ratio, its own background image |
| Element custom CSS, short (placement only) | V4 Custom CSS on the element, one short rule |
| FluentSnippets | Utility sets, `@keyframes`, small vanilla JS, PHP hooks. The framework `:root` layer is the one exception: it stays in Elementor's site-wide CSS so the editor renders it |

Display Conditions are server-side render logic only (a missing field, a user state), never responsive visibility, which is a utility class.

## Components

Use before writing code, for any layout that repeats.

1. Lay out the section with native atomic elements.
2. Create a Component from the container.
3. Expose only the properties that should vary per instance, typically text and image sources.
4. Keep the core layout and styling controlled globally, inside the component.

A component whose every property is exposed is a template with extra steps. Expose the minimum. Reference: `elementor.com/help/components-2/`

## Atomic elements and the coverage gap

Available atomic elements include Div Block, Flexbox, Heading, Paragraph, Button, Image, SVG, YouTube, Tabs and the Atomic Form set, with CSS Grid supported.

Some classic widgets have no atomic equivalent yet, accordions, galleries and carousels among them. Follow the policy's decision flow before reaching for one:

- **Native HTML first.** Gallery: a CSS grid of `figure` items. Carousel: a `scroll-snap` row. Modal: `dialog` or `popover`. Accordion with no atomic accordion yet: `details` and `summary` (the house default nested accordion only exists in V4 once Elementor ships it). Built from atomic elements where the tag control allows, otherwise an HTML element holding authored markup styled by the framework classes, logged as builder-bound.
- **A classic V3 widget on a V4 page is the last resort**: it cannot take a Global Class or a Variable, so it breaks the one-class-system rule. Use one only under the policy's section 0 rule (operator's yes, logged with a revisit trigger), and replace it when the atomic element ships.

## Structure

Flexbox where the layout is a flex context, Div Block where it is a plain wrapper. Semantic HTML tag on every structural element. Valid heading outline. Nested links only where the pattern genuinely calls for it, since an anchor inside an anchor is invalid markup.

Element states and responsive values are set per breakpoint and per state in the style tabs. Respect the site's own breakpoints and never introduce a new one.

## Version boundary

A V4 page is a V4 page. Do not convert existing V3 production pages to V4 and do not partially migrate one. Mixed pages are acceptable only where the coverage gap forces it.
