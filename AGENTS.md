# wpnomy agent guide

WPnomy Claude plugin (plugin slug `wpnomy`): WordPress builds under one house black box policy, one expert skill per builder or data plugin.

**Structure:** `skills/wpnomy` (router), `skills/wpnomy-<tool>-expert` (Bricks, Elementor V4/V3, Oxygen 6, Builderius, ACF, Meta Box), `evals/`, `prompts/`. `eval-legacy-tmp/` and `dist/` are untracked scratch.

## Commands
- Validate ACF output: `python3 skills/wpnomy-acf-expert/scripts/acf_validate.py <file-or-dir>`
- Other scripts: `skills/wpnomy-bricks-expert/scripts/aw_to_bricks.py`, `skills/wpnomy-elementor-atomic-expert/scripts/build_framework.py`
- Validate: `claude plugin validate . --strict`
- Evals (real model calls): `claude plugin eval . --trust-plugin --ablation none --scaffold --allow-tools Read Glob Grep Skill -j 4 --no-publish`. Rebuild cases with `python A:\Automation\plugin-evals\regen_evals.py <plugin> <router> <fixture ids>`. Write results outside the repo (`D:\SyncWin\AI Outputs\<plugin>\eval-results`); the packager includes repo files.

## Workflow
1. Read the skill or script you change, plus its neighbours.
2. Make the smallest change; run the closest check, then the full gate.
3. Update `CHANGELOG.md` for behavior changes; log ideas in `IMPROVEMENTS.md`.
4. Branch, commit, open a PR; never push to main.

## Rules
- Run the closest check and the full gate before committing. Never delete or weaken tests or evals. Report failed, skipped or timed-out runs honestly; NOT RUN is never a pass.
- Follow neighbouring files. Keep each `SKILL.md` under 500 lines; move detail into `references/`.
- On release, bump `version` in `.claude-plugin/plugin.json` and every skill's `metadata.version` together; add a `CHANGELOG.md` entry per behavior change.
- No commits, pushes or PRs unless asked. Work on a branch and open a PR; never push to main.
- No new dependencies without asking (scripts stay on the Python standard library).
- Never commit secrets. Never pick names or slugs without user confirmation.
- Skills are named `wpnomy-<tool>-expert`. Keep the black box policy once, in the router skill.
- `evals/results/` is git-ignored.

## Model routing
Opus plans, decides, writes self-contained briefs with a report word limit, and reviews every result. Haiku for search, reading and mechanical edits. Sonnet for coding, tests and multi-step work. Do 1-2 tool calls inline.

## Docs
README.md, CHANGELOG.md, CREDITS.md; ideas and feedback in `IMPROVEMENTS.md`.
