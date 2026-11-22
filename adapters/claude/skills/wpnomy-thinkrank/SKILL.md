---
name: wpnomy-thinkrank
description: Use when setting up or configuring the ThinkRank SEO plugin, moving a site off Yoast, adding or fixing schema and JSON-LD, or setting meta titles, robots, sitemaps and llms.txt. Use when the user says ThinkRank, SEO plugin, moving from Yoast, move off Yoast, schema, JSON-LD, breadcrumb schema, llms.txt, sitemap, robots, meta titles or IndexNow, or when the wpnomy router sends SEO plugin work here. Covers the first checks, a brand-agnostic SEO baseline, the Yoast move and what it misses, schema through ThinkRank filters, retiring builder or custom JSON-LD, REST configuration from PHP, a checks list and known 2.21.x issues. Not for content writing, keyword research or page layout.
license: MIT
---

# WPnomy ThinkRank Expert

Reached from `wpnomy`. Checked on ThinkRank 2.21.x. On another version, re-check each step on the site first and follow the site where it disagrees.

**Needs:** `${CLAUDE_PLUGIN_ROOT}/skills/wpnomy/references/house-rules.md` (read it first). Site access through Novamira. Writing copy, the wording of titles and page layout go elsewhere: this skill sets up the plugin and its output.

## Rules

- Native first: ThinkRank's own settings, then its REST routes, then its filters. Custom code only when none of these can do it, placed per the router's `references/styling-and-code.md`.
- Production: back up first, propose each change, apply one at a time, verify on the rendered page. Never claim a change is live until the front end shows it.
- Nothing is hardcoded to a brand. Business facts (name, type, audience) come from the owner or the site; ask when unknown.
- Never leave two SEO plugins live together without the move plan in `references/moving-off-yoast.md`.

## Workflow

1. **First checks.** Read `blog_public` and the live robots.txt before any per-type robots setting. A site set to discourage search engines makes every other setting pointless. Report it; change it only with a yes.
2. **Set up.** Apply the baseline as a preset, one group at a time. `references/setup-and-baseline.md`.
3. **Move off Yoast** when the site has it. `references/moving-off-yoast.md`.
4. **Schema and JSON-LD.** Extend through ThinkRank filters, retire builder or custom JSON-LD. `references/schema.md`.
5. **Configure.** From PHP through REST, or in the UI where PHP gets a 403. `references/rest-config.md`.
6. **Verify.** Run the checks in `references/checks-and-known-issues.md` and report what was not covered.

## References

| Read when | File |
|---|---|
| First checks, baseline preset, sitemap, llms.txt, IndexNow | `references/setup-and-baseline.md` |
| The site runs Yoast | `references/moving-off-yoast.md` |
| Schema nodes, builder or custom JSON-LD, breadcrumbs | `references/schema.md` |
| Writing settings through REST from Novamira PHP, titles and templates | `references/rest-config.md` |
| Verification checks, ThinkRank 2.21.x bugs and gaps | `references/checks-and-known-issues.md` |

## Before handing back

- [ ] `blog_public` and robots.txt checked and reported first.
- [ ] Backup taken; undo path stated.
- [ ] Baseline applied group by group; each deviation logged with its reason.
- [ ] If Yoast was replaced: the gaps list in `references/moving-off-yoast.md` was checked by hand.
- [ ] One source for each schema type: no duplicate `BreadcrumbList` or other node.
- [ ] Rendered titles checked on a post, a page, a product or archive and the front page.
- [ ] Sitemap, robots.txt and llms.txt loaded and read.
- [ ] Scratchpad complete.
