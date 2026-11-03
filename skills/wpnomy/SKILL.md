---
name: wpnomy
description: Entry point for every WordPress build with the house black box policy, on any site. Use whenever the user asks to build, design, rebuild, restyle or extend a page, template, header, footer, single, archive, loop item or component in Bricks, Elementor (V4 or V3), Oxygen 6 or Builderius; attaches a mockup or screenshot and wants it built in a page builder; uploads a builder export and wants changes; asks about global classes, variables, components, breakpoints, query loops, the Atomic Framework or Atomic Wireframe; or needs custom fields, post types or taxonomies with ACF or Meta Box and their values on a page. Trigger even when they never name the builder but mention their page builder, a template import or building on staging. Routes to wpnomy-bricks-expert, wpnomy-elementor-atomic-expert (V4), wpnomy-elementor-classic-expert (V3 edits), wpnomy-oxygen-expert, wpnomy-builderius-expert, wpnomy-acf-expert and wpnomy-metabox-expert.
license: MIT
metadata:
  displayName: "WPnomy"
  version: "0.1.5"
  author: "@wasimness"
  company: "SyncWin"
---

# WPnomy: Router

Routes between the expert skills and owns everything they share: intake, design standards, JSON delivery, handover. Carries no version-specific build rules of its own.

**Production.** Ask which environment the target site is before any write, and confirm it against what the connector actually reports rather than what the request assumed. On production, every change is proposed first and applied one at a time.

## Routing

| Work | Skill |
|---|---|
| Edits to existing Elementor 3.x pages (maintain-only: no new V3 builds) | `wpnomy-elementor-classic-expert` |
| Elementor V4 Atomic Elements, Variables, Classes, Components, and the Atomic Framework | `wpnomy-elementor-atomic-expert` |
| Bricks pages, templates, components, global classes and variables, and the Atomic Framework in Bricks | `wpnomy-bricks-expert` |
| Oxygen 6 pages, templates, components, variables, selectors and breakpoints | `wpnomy-oxygen-expert` |
| Builderius templates, components and global settings (commits, breakpoints, global CSS) | `wpnomy-builderius-expert` |
| ACF schemas, and any ACF value reaching a page | `wpnomy-acf-expert` |
| Meta Box field groups, post types, taxonomies, custom tables, and any Meta Box value reaching a page | `wpnomy-metabox-expert` |

Load one build skill, plus the ACF or Meta Box skill only when the page is dynamic. A static V3 page never loads the V4, Bricks or ACF file, and a Bricks build never loads an Elementor file.

## Black box policy (mandatory)

Every build on every builder follows `references/black-box-policy.md`: semantic HTML first, CSS second, tiny vanilla JS third, a builder widget last; no composite widgets, no add-on packs, no element-panel styling; functional builder elements only when HTML cannot do the job, styled by classes and logged as builder-bound. Each build skill carries its own gate and allowed-element list. Read the policy in full on the first build of a session, and whenever an element is not on the build skill's allowed list.

New pages and parts are built in Elementor V4 or Bricks. Elementor V3 is maintain-only.

## Step 0. First run on a site

The first time any skill here touches a site, run the audit in `references/site-audit.md` (Elementor sites) or the Bricks skill's `references/verify.md` (Bricks sites). It is read-only, it fills the scratchpad's site canon, and it produces a list of recommended Elementor and backend optimizations.

Recommend only. Implement nothing without explicit approval, one item at a time. Record the result so later runs skip this step.

## Step 1. Define the build

Ask in one message and wait. Skip anything already answered.

1. **Builder: Bricks, Elementor V4, Oxygen 6, Builderius, or an edit to an existing Elementor V3 page?** New work is never V3. Confirm against the connector rather than the request: an active Bricks theme means Bricks; `BREAKDANCE_MODE === 'oxygen'` means Oxygen 6; active Builderius means Builderius. For Elementor, if unsure, ask them to check Elementor > Editor > Settings > Atomic Editor.
2. **Page type: static, or dynamic (ACF or Meta Box)?**
3. **Existing design?** If yes, ask for the mockup or screenshot. If no, ask concisely for required sections, components, layout and direction.
4. **Build method: generate a file for manual import (Elementor JSON, or Bricks clipboard JSON or transfer package), or build directly on a named site through Novamira MCP?**

**Version lock.** When the user supplies an Elementor JSON and asks for changes, keep its version. V3 stays V3, V4 stays V4. Change only on an explicit instruction. A site never changes builder inside a build.

## Step 2. Gather inputs

| Always | When applicable |
|---|---|
| Design mockup or direction | ACF field names and types, and shortcodes already in use |
| Required sections, components, layout | Elementor Export Kit for the target site |
| Target site, staging or production | An existing export to pattern against |

**Inspect every supplied file before building.** Read the Export Kit and any export for global colours, global fonts, V4 Variables, existing Global Classes, breakpoints, container width and reusable components. Anything already on the site is reused, never re-created under a new name.

**Stop rules.** Never build on assumed globals, assumed variable names or assumed ACF field names. Ask.

**Novamira's own skills.** Load them with `novamira/skill-get` for the mechanics of talking to the install. Each build skill names the ones it pairs with. The rest are general WordPress work outside this plugin's scope:

| Skill | Use it for |
|---|---|
| `gutenberg-edit-content` | Content in the block editor rather than a builder |
| `custom-theme-build` | A coded child theme or page template instead of builder output |
| `kadence-build-page` | Kadence theme settings, palette, header and footer chrome |
| `yoast-integration` | SEO titles, meta, canonicals, indexing, redirects |
| `form-model-schema`, `form-model-migration` | Contact form schemas and moving between form plugins |
| `content-model-migration` | Moving a field schema between modelling plugins |
| `novamira-design` | Capturing or applying the site's saved design direction |
| `novamira-feedback` | Reporting a genuine Novamira bug, only on the user's request |
| `skill-creator` (Novamira's) | Authoring a Novamira-side skill stored in WordPress |
| `bricks-build-page` and its companions (Novamira Pro) | Fallback mechanics for Bricks only; `wpnomy-bricks-expert` names when |

**When they collide, this plugin leads.** Where a Novamira skill and a rule here disagree on a convention, a naming scheme or a design decision, follow the rule here and say which one was overridden. Use their mechanics, keep our standards.

**Design authority.** `novamira/get-active-design` reports who owns visual decisions. The Atomic Framework leads wherever it defines a value. Take from an active Novamira design only what the framework has no value for, and never let it override a framework token. If the design reports `ask`, say that the framework is leading rather than leaving it open.

## Step 3. Plan, then build

Write the section-by-section plan into the scratchpad and get agreement before generating JSON or writing to a site. Each section: layout, elements, content source, anything dynamic.

## Working file

Copy `assets/build-scratchpad.md` at the start of every run and keep it current. It is the intake record, plan, decision log and handover report in one file, and it ships with the build.

## References

| Read when | File |
|---|---|
| Any build: work types, fixed order, precedence, design-system values, missing add-ons | `references/house-rules.md` |
| The input is a screenshot, mockup, or an existing JSON export | `references/intake.md` |
| Making any layout, UX or accessibility decision | `references/design-standards.md` |
| Build method is a JSON file rather than Novamira | `references/json-mode.md` |
| First run on this site | `references/site-audit.md` |
| Building a header, footer, single, archive, loop item or popup, or setting any display condition | `references/theme-parts.md` |
| Choosing any element, or any element not on the build skill's allowed list | `references/black-box-policy.md` |
| Deciding where a style or a piece of code goes | `references/styling-and-code.md` |

## Rules every build skill inherits

**Decision flow.** The black box policy's section 6 decides what gets built: plain semantic HTML with classes, then a native HTML feature (`details`, `dialog`, `popover`, `scroll-snap`), then a builder functional element styled by classes and marked builder-bound, then a nested or atomic element or a small script, otherwise nothing.

**Styling and code placement.** `references/styling-and-code.md` decides where every style and piece of code lives on V4 and Bricks: design in tokens and classes, placement one-offs on elements, large or site-wide code in FluentSnippets, with promotion rules that keep it DRY.

**Version independence.** V3, V4 and Bricks implementations stay separate. Never migrate, merge or alter an existing production implementation unless explicitly asked. The V4 path exists to support gradual adoption without putting live pages at risk.

**Research before implementing.** If any element, control, tag or behaviour is unfamiliar, research it before writing anything. V4 moves fast and the feature set at build time may differ from what these files describe. Reference set: `elementor.com/help/build-with-the-editor/v4-editor/`, `elementor.com/help/components-2/`, `developers.elementor.com/`; for Bricks, the live `bricks/get-element-schema` first, then `academy.bricksbuilder.io`. If uncertainty remains, ask for details or a documentation link. Never guess a control name, a tag format or a schema shape.

**Naming.** Atomic Framework token names pass through exactly as the framework writes them; the framework owns its namespace and nothing here renames it. **Class prefix: ask first.** Every BEM class this plugin invents, on any builder, is `<prefix>-<block>`. The prefix belongs to whoever owns the work, so it is settled per site, in this order: (1) the Atomic Wireframe project's `classPrefix`, or the prefix already recorded in the scratchpad's site canon; (2) otherwise ask once, before creating any class: "Which class prefix should new classes use on this site? Usually your company or brand code plus the site's short code, for example `acme-md`. Leave it empty to use the site's short code alone."; (3) only when the answer is empty, default to the site's short code (`md-card__title`). Record the answer in the site canon so later runs reuse it. Never assume a prefix from memory or carry one from another site, client or employer. The site code names the brand or person, never the domain, so a domain move changes no class. A component or class carried to another site is renamed to that site's prefix on the way in. State classes (`is-<state>`, always paired with their block) and `js-` hook classes stay unprefixed. Helper variables and FluentSnippets names use the same prefix (`<prefix>-<purpose>`, `styling-and-code.md`). An existing site's own older prefix is matched when editing that old work and never adopted for new work.

**Never claim a change is live** until it is verified on the rendered page. Code outside the builder goes only where `references/styling-and-code.md` puts it, and every snippet is logged in the scratchpad.

## Before handing back

- [ ] Black box gate passed: no banned element, every builder-bound element logged with its output markup.
- [ ] Only variables: literals limited to `0`, `1px`, `%`, unitless ratios and keywords; no inline styles, `!important` or bare tag selectors.
- [ ] BEM class names only, none counter-named.
- [ ] Snapshot taken before any write; undo path stated.
- [ ] `styling-and-code.md` followed, its promotion rules applied, element-level styles and snippets logged.
- [ ] Every colour, font and size resolves to a variable (V4, Bricks) or a global (V3 edits). Nothing hardcoded.
- [ ] Every ACF value is bound, never pasted as static text.
- [ ] Semantic HTML tags set. Heading outline valid. One H1 or none.
- [ ] Checked at every breakpoint the site defines, on the published URL, not the editor preview.
- [ ] Dynamic content tested on a complete record and on a sparse one.
- [ ] Display conditions set and written down in plain language.
- [ ] Every item in the brief is present. Diff the brief's headings against the build.
- [ ] Scratchpad complete and delivered.

Never report a build as done because it saved. Load the front end first.
