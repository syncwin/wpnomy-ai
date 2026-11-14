# wpnomy agent guide

WPnomy Claude plugin (plugin slug `wpnomy`): WordPress builds under one house black box policy, one skill per builder or data plugin.

**Structure (single branch, `main`):** the shipped plugin is `adapters/claude/` (`.claude-plugin/plugin.json`, `skills/wpnomy` router and `skills/wpnomy-<tool>` for acf, bricks, builderius, elementor-atomic, elementor-classic, metabox and oxygen, `evals/` with `router/cases.json`, `prompts/`, assets with the icon, plus copies of README, CHANGELOG, LICENSE, CREDITS, PUBLIC-SAFETY, `.gitignore`, `.public-safety-allow`). The root keeps `.claude-plugin/marketplace.json` (source `./adapters/claude`), the same docs, `dev/` (Python maintainer tools, not shipped), `docs/assets/` (SVG icon source), `.github/` (CI and the release workflow). Edit the docs in both places and keep the copies identical.

## Commands
- Maintainer tools (not shipped; each has a recipe in the skill's `references/`): `dev/wpnomy-acf/scripts/acf_validate.py <file-or-dir>`, `dev/wpnomy-bricks/scripts/aw_to_bricks.py <project.json> -o plan.json`, `dev/wpnomy-elementor-atomic/scripts/build_framework.py <tokens.json> -o <outdir>`. The scripts read the asset copies in their own `dev/<skill>/assets/`; keep those identical to the skill's `assets/` files.
- Directory gate: `python <aiaddon>/dev/aiaddon-review/scripts/validate_extension.py adapters/claude --strict --target directory --require-meta author,company`; router: `route_check.py adapters/claude`; secrets: `scan_secrets.py . --history` (false positives only in `.public-safety-allow`)
- Validate: `claude plugin validate adapters/claude --strict` and `claude plugin validate . --strict`
- Evals (real model calls): `claude plugin eval adapters/claude --trust-plugin --ablation none --scaffold --allow-tools Read Glob Grep Skill -j 4 --no-publish`. Rebuild cases with the owner's local `plugin-evals/regen_evals.py` (not in this repo). Write results outside the repo; the packager includes repo files.

## Workflow
1. Read the skill or script you change, plus its neighbours.
2. Make the smallest change; run the closest check, then the full gate.
3. Update `CHANGELOG.md` for behavior changes; log ideas in `IMPROVEMENTS.md`.

## Rules
- **Directory compliance:** the shipped plugin has no hooks, no scripts or other non-text files, and text-only frontmatter. Script-like features are recipes in `skills/*/references/`; `dev/` is maintainer tooling only.
- **Never publish secrets or private data** (keys, tokens, personal contact data, client names, internal URLs, local paths); the secret and public-safety scans block every commit and release.
- Run the closest check and the full gate before committing. Never delete or weaken tests or evals. Report failed, skipped or timed-out runs honestly; NOT RUN is never a pass.
- Follow neighbouring files. Keep each `SKILL.md` under 500 lines; move detail into `references/`.
- On release, bump `version` in `adapters/claude/.claude-plugin/plugin.json` and the plugin entry in `.claude-plugin/marketplace.json` together (skills carry no `metadata` block); add a `CHANGELOG.md` entry per behavior change (root and `adapters/claude/` copies). Release: push a `v<version>` tag; `release-plugin.yml` builds `wpnomy.plugin`.
- No commits, pushes or PRs unless asked. Work on a branch and open a PR; never push to main.
- No new dependencies without asking (scripts stay on the Python standard library).
- Never commit secrets. Never pick names or slugs without user confirmation.
- Skills are named `wpnomy-<tool>`; the router is `wpnomy`. Keep the black box policy once, in the router skill.
- Pin any GitHub Action to a full commit SHA with the version in a comment; give each job least permissions.
- `evals/results/` is git-ignored.

## Model routing
Opus plans, decides, writes self-contained briefs with a report word limit, and reviews every result. Haiku for search, reading and mechanical edits. Sonnet for coding, tests and multi-step work. Do 1-2 tool calls inline.

## Docs
README.md, CHANGELOG.md, CREDITS.md, PUBLIC-SAFETY.md; ideas and feedback in `IMPROVEMENTS.md`.
