# wpnomy

**Author:** @wasimness · **Company:** SyncWin · **Version:** 0.0.1 · **License:** MIT · **Home:** https://wpnomy.com/

Claude skills for building WordPress sites the right way from the start. One expert skill per plugin, all under one house black box policy: native elements, Atomic Framework variables, BEM classes, the plugin's own component mechanism, and a front-end check before anything is called done.

## Skills

| Skill | For |
|---|---|
| `wpnomy` | Router: intake, house rules, black box policy, styling placement, hand-over checklist |
| `wpnomy-bricks-expert` | Bricks pages, templates, components, global classes and variables, forms, query loops |
| `wpnomy-elementor-atomic-expert` | Elementor V4 Atomic Elements, Variables, Global Classes, Components, the Atomic Framework |
| `wpnomy-elementor-classic-expert` | Edits to existing Elementor V3 pages (maintain-only) |
| `wpnomy-oxygen-expert` | Oxygen 6 elements, variables, selectors, components, breakpoints |
| `wpnomy-builderius-expert` | Builderius templates, components, global settings commits, breakpoints |
| `wpnomy-acf-expert` | ACF schemas, importable JSON, binding ACF values into pages |
| `wpnomy-metabox-expert` | Meta Box field groups, post types, custom tables, official abilities, bindings |

Start with `/wpnomy` and describe the job; it routes to the right expert.

## Install

- **Claude Code:** add the plugin from its folder or marketplace (`claude plugin install wpnomy@<marketplace>`), then run `/wpnomy`.
- **Claude desktop / Cowork:** upload `wpnomy v0.0.1.plugin` in the app's plugin settings.
- **Undo:** uninstall the plugin from the same place.

Site work runs through Novamira (MCP connector or CLI). Without site access the skills deliver the plan and exact output, marked unverified.

## House rules in one place

- `skills/wpnomy/references/house-rules.md`: work types, fixed order, precedence, design-system values, missing add-ons.
- `skills/wpnomy/references/black-box-policy.md`: what to use, what never to use.
- `skills/wpnomy/references/styling-and-code.md`: where every style and piece of code lives.

Class names use the site's own prefix (`<prefix>-block__element`), read from the Atomic Wireframe project's `classPrefix` or the site canon.

## Tests

Behavior tests live in `evals/` (`claude plugin eval . --judge-model sonnet`). Each run makes real model calls.

## Support

Issues: https://github.com/syncwin/wpnomy-ai/issues · Email: support@syncwin.com
