# House rules (every wpnomy expert skill)

Read this before any build, push or review. Each expert skill adds only what is specific to its plugin.

## Contents

1. Work types · 2. Fixed order · 3. Precedence · 4. Design system rules · 5. Black box policy and styling · 6. Missing or partial · 7. Hand-over checklist

## 1. Work types

Name the type first; it decides what changes and what is checked.

| Type | Changes | Check |
|---|---|---|
| New page, template or component | builder content only | front end at every breakpoint |
| Design system setup | variables, classes, fonts, breakpoints | every existing page still renders the same |
| Data model | field groups, post types, taxonomies | the edit screen and the front-end output |
| Migration between plugins | content plus design system | before/after render of each page |
| Review of existing work | nothing until the owner approves fixes | the hand-over checklist (§7) |

## 2. Fixed order (never skip or reorder)

1. **Plan.** A short checklist with context and examples goes to the owner; nothing starts until they approve. Approved plans run without asking again.
2. **Snapshot.** Before any write to a live site, save what will change (the plugin's own revisions or an export) so it can be undone.
3. **Build** through the plugin's own save functions or UI, never raw database writes, so revisions, caches and validation stay in step.
4. **Check the live front end**, not the editor or the saved data. A write that saves fine can still render wrong.
5. **Review** against §7, then report: what changed, what was verified, what was not.

## 3. Precedence

1. The owner's explicit instruction for this job.
2. These house rules.
3. The plugin's behaviour **as checked on the site** (installed version).
4. The plugin's official docs.
5. General knowledge.

If the site and the docs disagree, the site wins; record the version. If the owner's instruction conflicts with a house rule, name the rule and ask once.

## 4. Design system rules

These apply to block and page content (not to the plugin's own admin screens).

- **Variables only.** Every value is a design-system variable: `var(--token)`, sub-steps as `calc(var(--token) * n)`. Allowed literals: `0`, `1px`, `%`, unitless ratios, keywords. When the site uses the Atomic Framework (from Atomic Wireframe), its variable names are the source; otherwise use the site's own framework (Automatic.css, Core Framework, the builder's variables).
- **BEM classes only.** `block`, `block__element`, `block--modifier`. Element and modifier names say what they are (role, then a token or keyword: `card__text-spaced`, `split__box-first`), never a counter (`-2`). Atomic Framework blocks use the `awf-` prefix.
- **No inline styles, no `!important`, no bare tag selectors** (scope one with `:where()` or give the element a class).
- **Desktop-first by default** (max-width, base 1440px). The owner may switch to mobile-first; on a site with content, warn that existing pages can break and get a second confirmation first.

## 5. Black box policy and styling

The black box policy is `black-box-policy.md` (what to use, what never to use, the decision flow) and styling placement is `styling-and-code.md`; both sit next to this file. Before placing any element, ask: can the exact output HTML be described, can our classes and variables style every part, would it survive a copy to another builder as HTML plus classes? Any no means skip it, or log it as builder-bound with its output markup. Custom features only where the plugin has nothing like it, checked in the plugin itself on the site.

## 6. Missing or partial

- **Add-on missing** (for example a forms add-on): use the documented fallback in the expert skill and say so in the report; never install a plugin without the owner's approval.
- **Feature only partly available** (for example site-wide only): use it only if it changes nothing beyond the work at hand; otherwise use the fallback and say why.
- **Version differs from the one the skill was checked on:** re-check the step on the site before writing, and note the new version in the report.
- **No site access:** produce the plan and the exact output (HTML, classes, variables, data), marked unverified.

## 7. Hand-over checklist

Use the router's "Before handing back" list. Report each line PASS, FAIL or NOT RUN; a check that did not run is never PASS.

## 8. Cross-cutting rules (every expert)

- **Native first.** Use the plugin's own features first and check its official docs; write custom code only when nothing native exists.
- **Scratchpad after each task.** Close with a tight structured scratchpad (headings, lists, tables; nothing repeated) of what was done.
- **Scripts.** A skill that runs a bundled script copies it once per session into the working folder (for example `./tools/`) and runs it from there. Never put a `/root/.claude` or `~/.claude` path in a shell command.
- **Novamira PHP and text edits.** Never `preg_replace` with replacement text containing `$` figures (prices, amounts, `$1`-like digits); they are read as backreferences. Use `str_replace` or `preg_replace_callback`, then re-read the figures.
