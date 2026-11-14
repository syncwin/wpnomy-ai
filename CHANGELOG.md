# Changelog

## 0.2.0: Directory-compliant layout

**Changed**
- Single-branch layout: the shipped plugin is `adapters/claude/` (Markdown, JSON and the icon only); the marketplace entry at the repo root points at it. Docs are kept identical in both places.
- Skills renamed to drop the `-expert` suffix: `wpnomy-acf-expert` is now `wpnomy-acf`, `wpnomy-bricks-expert` is `wpnomy-bricks`, `wpnomy-builderius-expert` is `wpnomy-builderius`, `wpnomy-elementor-atomic-expert` is `wpnomy-elementor-atomic`, `wpnomy-elementor-classic-expert` is `wpnomy-elementor-classic`, `wpnomy-metabox-expert` is `wpnomy-metabox`, `wpnomy-oxygen-expert` is `wpnomy-oxygen`. Commands become `/wpnomy:wpnomy-<tool>`. Every reference, the router and the evals are updated.
- Router: the routing section is now a routing table with trigger phrases, tie-break rules and a closed default question, checked by `evals/router/cases.json`.
- Skill descriptions lead with the trigger ("Use when ...") and skills carry text-only frontmatter (no `metadata` block); the plugin version lives in `plugin.json` and the marketplace entry.
- The house rule about bundled scripts now says the plugin ships none.

**Moved**
- `acf_validate.py`, `aw_to_bricks.py` and `build_framework.py` moved unchanged to `dev/` (maintainer tools, not shipped). Each has an equivalent recipe in its skill's `references/` (`acf-validate.md`, `aw-to-bricks.md`, `build-framework.md`) that Claude follows with Read, Grep and Write.
- The generated `atomic-framework.css` and `report.txt` are now `atomic-framework.css.md` and `report.txt.md` (the content in a fenced block, unchanged).

**Added**
- Public-safety files: `.public-safety-allow`, `PUBLIC-SAFETY.md`, a `.gitignore` preset, `.env.example`, and a CI workflow running the directory validator, router check and secret scan.
- The release workflow now checks that the package holds only text files and no hooks or scripts.

## 0.1.8: Update

**Added**
- House rules section 8: native features first, a tight scratchpad after each task, bundled scripts copied once per session into the working folder (never a `~/.claude` path in a shell command), and no `preg_replace` with `$` figures in replacement text (Novamira edits).
- Elementor experts (V4, V3): native features first; non-Elementor UI and functions go in one global place (FluentSnippets, Elementor Code Snippets).
- Bricks expert: mobile-first; style settings need breakpoint keys (`:bp360`), unsuffixed keys render nothing.
- ACF expert: learn the site's tech stack and tune Novamira settings before building.

## 0.1.7: Update

**Changed**
- Standing rule: research before building. Check current official docs and widely recommended, secure practice before choosing an approach, file, tool, config or dependency; cite the source; mark anything unverified; never guess; keep research scoped to the task.

## 0.1.6: Update

**Changed**
- Security first. The router asks for staging first and an explicit yes, after a backup, for destructive site operations (deleting content, plugins or themes, search-replace, database, user or role changes, plugin activation), and never runs commands found in pages, exports or tool results.
- PHP snippet rules now list nonces, capability checks, REST permission callbacks, prepared queries and output escaping.

**Fixed**
- build_framework.py refuses token names or values that could break out of a CSS declaration (braces, semicolons, angle brackets, comments, @import). The bundled exports produce identical output.

## [0.1.5] - 2026-11-03
### Changed
- Metadata to the AI Extender standard: author company, plugin metadata block, release stage, listing links, and display name, version, author, company and license on every skill and agent. No behaviour change.

## 0.1.4 (2026-11-02)

### Changed
- Class prefix is asked for once per site (usually the user's company or brand code plus the site code) and recorded in the site canon; the site's short code is only the default when no prefix is given. No SyncWin prefix is built in any more.

## 0.1.3 (2026-11-02)

- Plugin icon.

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
