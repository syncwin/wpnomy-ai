# Changelog

## 0.0.1 (2026-11-01)

First release as wpnomy (renamed and extended from a private predecessor).

### Added
- `wpnomy-oxygen-expert`: Oxygen 6 native elements, variables and collections, selectors, components, fixed and custom breakpoints, paste format, form fallback, dynamic data, Oxygen Doctor check (checked on Oxygen 6.2.1).
- `wpnomy-builderius-expert`: HtmlElement module, global settings commits through GraphQL, variables in global CSS, breakpoints, components, safe publishing (checked on Builderius 1.4-beta).
- `wpnomy-metabox-expert`: Meta Box's official abilities, field groups, custom tables, builder bindings, Meta Box or ACF (checked on Meta Box AIO 3.13.1 with Bricks 2.4.4).
- `skills/wpnomy/references/house-rules.md`: work types, fixed order, precedence, design-system values, missing add-ons.
- Behavior tests in `evals/` for the three new skills.

### Changed
- Every skill renamed to `wpnomy-<plugin>-expert`; router renamed to `wpnomy` and now routes Oxygen 6, Builderius and Meta Box.
- Class prefix is the site's own code (`<prefix>-`, from the Atomic Wireframe project's `classPrefix`), with no company part.
- ACF expert: shorter description, Oxygen 6 and Builderius binding, link to the house rules and to the Meta Box comparison.
- Author @wasimness, company SyncWin, MIT license.

### Removed
- Client names and the scope rule for an external Elementor workflow.
