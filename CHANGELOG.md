# Changelog

## 0.1.4 (2026-11-02)

### Changed
- Class prefix is asked for once per site (usually the user's company or brand code plus the site code) and recorded in the site canon; the site's short code is only the default when no prefix is given. No SyncWin prefix is built in any more.

## 0.1.3 (2026-11-02)

- Plugin icon (`assets/icon.png`, `assets/icon.svg`).

## 0.1.2 (2026-11-02)

### Changed
- Marketplace renamed to `syncwin-wpnomy`, matching the other SyncWin plugins (`syncwin-<plugin>`).

## 0.1.1 (2026-11-02)

### Changed
- Display name is now WPnomy (plugin, skills, README); slugs and skill names are unchanged.
- README lists every command (`/wpnomy:wpnomy` and each expert) and the marketplace install for claude.ai, desktop and mobile.

## 0.1.0 (2026-11-01)

First release as wpnomy (renamed and extended from a private predecessor).

### Added
- `wpnomy-oxygen-expert`: Oxygen 6 native elements, variables and collections, selectors, components, fixed and custom breakpoints, paste format, form fallback, dynamic data, Oxygen Doctor check (checked on Oxygen 6.2.1).
- `wpnomy-builderius-expert`: HtmlElement module, global settings commits through GraphQL, variables in global CSS, breakpoints, components, safe publishing (checked on Builderius 1.4-beta).
- `wpnomy-metabox-expert`: Meta Box's official abilities, field groups, custom tables, builder bindings, Meta Box or ACF (checked on Meta Box AIO 3.13.1 with Bricks 2.4.4).
- `skills/wpnomy/references/house-rules.md`: work types, fixed order, precedence, design-system values, missing add-ons.
- Behavior tests in `evals/` for the three new skills.

### Changed
- Every skill renamed to `wpnomy-<plugin>-expert`; router renamed to `wpnomy` and now routes Oxygen 6, Builderius and Meta Box.
- Class prefix is company plus site code, `sw-<site>-` (`sw` for SyncWin), read from the Atomic Wireframe project's `classPrefix`; helper variables use `sw-`.
- ACF expert: shorter description, Oxygen 6 and Builderius binding, link to the house rules and to the Meta Box comparison.
- Author @wasimness, company SyncWin, MIT license.

### Removed
- Client names and the scope rule for an external Elementor workflow.
