# Build Scratchpad

Copy at the start of every run, fill as you go, deliver with the build.
Save as `<site>-<page-or-part>-build-scratchpad.md`.

## Build definition

| | |
|---|---|
| Site | |
| Staging or production | |
| Builder | Elementor V3 / Elementor V4 / Bricks |
| Page type | Static / ACF-powered |
| What is being built | Page / header / footer / single / archive / loop item |
| Build method | File (Elementor JSON, Bricks clipboard or transfer package) / Novamira direct |
| Design input | Mockup / screenshot / brief / existing JSON |
| Date | |

## Site canon

Everything the build uses comes from here.

| Asset | Values found | Source |
|---|---|---|
| Global colours or Colour Variables | | |
| Global fonts or Font Variables | | |
| Size Variables | | |
| Existing Global Classes | | |
| Existing Components | | |
| Breakpoints | | |
| Container width | | |
| Spacing scale in use | | |
| Existing CSS variable layer in the kit | | |
| Computed `html` font size | | |

**V4 only.** Feature flags checked: Global Classes ☐ Variables ☐ Variables Manager ☐ Components ☐ V4 Custom CSS ☐

Atomic Framework installed ☐ · `html` computed font-size verified at 62.5% ☐
Variable route: **A reference mode** ☐ / **B mirror mode** ☐ · Size Variables accept `clamp()` ☐
Brand colours contrast-checked, light and dark ☐

**Bricks canon.** Bricks version ☐ · Abilities API on ☐ · disabled abilities listed ☐ · CSS loading: inline / files ☐

| Bricks asset | Values found | Source |
|---|---|---|
| Atomic Wireframe project (id, title) | | `atomic-wireframe/get-project` |
| Class prefix and renames | | project |
| Root font size (project / Root theme style / computed `html`) | | |
| Breakpoints (project / Bricks, mobile-first read back) | | |
| Variables and categories (count, any without the framework) | | |
| Palette entries | | |
| Theme styles and their conditions | | |
| Global classes (count, prefix conformance) | | |
| Components | | |
| Templates and conditions | | |
| Global queries, custom fonts | | |
| ACF and data plugin tags present | | `list-dynamic-data-tags` |

`aw_to_bricks.py` plan generated ☐ · warnings read to the user ☐ · transfer package exported before global writes ☐

**First-run audit:** run ☐ / previously run ☐ · Environment confirmed against the connector: staging ☐ production ☐

**Palette source:** existing site palette ☐ · supplied by user ☐ · grayscale placeholder ☐
Atom mapping signed off ☐

**Recommended optimizations (recommend only, never auto-apply):**

| Finding | Fix | Risk | Approved |
|---|---|---|---|

**Missing or not supplied:**

## ACF fields in play

Field names and types only. Field design belongs to `wpnomy-acf-expert`.

| Field | Type | Where it renders | Binding route | Fallback |
|---|---|---|---|---|

Route is one of: dynamic tag, Post Custom Field tag, shortcode, Loop Builder, V3 widget exception.

Schema work this run: none ☐ · JSON generated ☐ · written via Novamira ☐ · validator run and clean ☐

## Section plan

Agreed before building.

| # | Section | Layout | Elements | Content source | Dynamic | Classes or components |
|---|---|---|---|---|---|---|

## Screenshot transcription

Delete unless a mockup was the input.

| # | Section | Layout | Elements | Content | Notes |
|---|---|---|---|---|---|

Questions the image could not answer, and their answers:

## Decisions

| Decision | Reason |
|---|---|

## Exceptions logged

| Exception | Where | Reason | Revisit when |
|---|---|---|---|

Every builder-bound element (black box policy, section 3) goes here with its documented output markup. Typical: a nested accordion, form, nav or query loop (builder-bound); a V3 classic widget on a V4 page for a coverage gap, with the operator's yes; mirror mode drift risk; on Bricks, a library literal mapped to the nearest token, or a modifier moved to compound custom CSS. Element-level styles and code outside the builder have their own tables below.

## Element-level styles

Placement one-offs only (`styling-and-code.md`, steps 5 and 6). A row that repeats is a missing modifier class.

| Element | Property | Why no class holds it |
|---|---|---|

## Code placed outside the builder

FluentSnippets by default (`<prefix>-<purpose>`), plus the V4 framework layer in Elementor's site-wide CSS.

| What | Where it lives | What it does |
|---|---|---|

## Out of scope, noticed anyway

Reported, not fixed.

## Verification

Mirrors the router's handover checklist.

| Check | Result |
|---|---|
| Every colour, font and size resolves to a global or variable | |
| Every ACF value bound, nothing pasted as static text | |
| Semantic tags set, heading outline valid, one H1 or none | |
| Checked on the published URL at every site breakpoint | |
| Dynamic content tested on a complete record | |
| Dynamic content tested on a sparse record | |
| Display conditions set | |
| Brief headings diffed against the build | |
| Contrast checked against the palette | |
| Keyboard order and focus states checked | |

Breakpoints actually tested:

## Display conditions set

| Part or element | Condition, in plain language |
|---|---|

## Handover

**Built:**

**Skipped, and why:**

**Needs a decision from you:**

**Next steps:**
