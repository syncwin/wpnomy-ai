# WPnomy

**Author:** @wasimness · **Company:** SyncWin · **Version:** 0.2.0 · **License:** MIT · **Home:** https://wpnomy.com/

**Download:** [wpnomy.plugin](https://github.com/syncwin/wpnomy-ai/releases/latest/download/wpnomy.plugin) (always the latest release)

Claude skills for building WordPress sites the right way from the start. One expert skill per plugin, all under one house black box policy: native elements, Atomic Framework variables, BEM classes, the plugin's own component mechanism, and a front-end check before anything is called done.

## Skills

| Skill | For |
|---|---|
| `wpnomy` | Router: intake, house rules, black box policy, styling placement, hand-over checklist |
| `wpnomy-bricks` | Bricks pages, templates, components, global classes and variables, forms, query loops |
| `wpnomy-elementor-atomic` | Elementor V4 Atomic Elements, Variables, Global Classes, Components, the Atomic Framework |
| `wpnomy-elementor-classic` | Edits to existing Elementor V3 pages (maintain-only) |
| `wpnomy-oxygen` | Oxygen 6 elements, variables, selectors, components, breakpoints |
| `wpnomy-builderius` | Builderius templates, components, global settings commits, breakpoints |
| `wpnomy-acf` | ACF schemas, importable JSON, binding ACF values into pages |
| `wpnomy-metabox` | Meta Box field groups, post types, custom tables, official abilities, bindings |

## Commands

Start with the router and describe the job; it sends the work to the right expert. Each expert can also be called directly.

| Command | Use it for |
|---|---|
| `/wpnomy:wpnomy` | Any WordPress build: intake, routing, house rules |
| `/wpnomy:wpnomy-bricks` | Bricks |
| `/wpnomy:wpnomy-elementor-atomic` | Elementor V4 |
| `/wpnomy:wpnomy-elementor-classic` | Elementor V3 edits |
| `/wpnomy:wpnomy-oxygen` | Oxygen 6 |
| `/wpnomy:wpnomy-builderius` | Builderius |
| `/wpnomy:wpnomy-acf` | ACF |
| `/wpnomy:wpnomy-metabox` | Meta Box |

Example: `/wpnomy:wpnomy add an Event post type with date and venue using Meta Box and show it on the single event template in Bricks`

## Install

- **claude.ai, desktop app, mobile (auto-updates):** Settings → Customize → Plugins → Add → Add marketplace → `syncwin/wpnomy-ai`, then install WPnomy.
- **Claude Code terminal:** `claude plugin marketplace add syncwin/wpnomy-ai`, then `claude plugin install wpnomy@syncwin-wpnomy`.
- **Undo:** uninstall the plugin from the same place.

Site work runs through Novamira (MCP connector or CLI). Without site access the skills deliver the plan and exact output, marked unverified.

## House rules in one place

- `adapters/claude/skills/wpnomy/references/house-rules.md`: work types, fixed order, precedence, design-system values, missing add-ons.
- `adapters/claude/skills/wpnomy/references/black-box-policy.md`: what to use, what never to use.
- `adapters/claude/skills/wpnomy/references/styling-and-code.md`: where every style and piece of code lives.

Class names use your own prefix (`<prefix>-block__element`). WPnomy asks for it once per site (usually your company or brand code plus the site's short code, like `acme-md`), reads it from the Atomic Wireframe project's `classPrefix` when set, and falls back to the site's short code only when you leave it empty.

## Tests

Behavior tests live in `adapters/claude/evals/` (`claude plugin eval adapters/claude --judge-model sonnet`). Each run makes real model calls. Maintainer scripts live in `dev/` and are not part of the plugin; the plugin itself ships only Markdown and JSON, and each script has an equivalent recipe in the skill's `references/` folder.

## Support

Issues: https://github.com/syncwin/wpnomy-ai/issues · Email: support@syncwin.com
