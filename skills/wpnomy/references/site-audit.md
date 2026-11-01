# First-run site audit

Run once per site, the first time any skill in this plugin touches it. Read-only. Record the result in the scratchpad so later runs skip it.

Two purposes: learn the site canon so the build uses what exists, and spot settings that make Elementor work worse than it needs to.

## Read these

Through Novamira, in this order. None of them write.

| Call | Gives you |
|---|---|
| `novamira/elementor-check-setup` | Core and Pro versions, whether the V4 atomic runtime, style schema, Global Classes, Variables and Interactions are available, container width, active breakpoints |
| `novamira/elementor-list-variables` | Every V4 Variable with id, label, type, value |
| `novamira/elementor-list-global-classes` | Every Global Class and its variants |
| `novamira/elementor-list-v3-styles` | System and custom Global Colors and Typography |
| `novamira/elementor-list-dynamic-tags` | Which dynamic tags exist on this install, including whether ACF groups are present |
| `novamira/acf-check-setup` | ACF edition, version, whether post types, taxonomies and options pages are manageable |
| `novamira/acf-list-fieldgroups` | Field groups, their source (db, json or php) and whether they are editable |
| `novamira/get-active-design` | Whether a Novamira design is active and who holds authority |
| Active kit `custom_css` | Any existing CSS variable layer, which the build must not collide with |
| Theme base font settings | The computed `html` font size, which decides whether rem-based tokens are safe |

## What to look for

**A CSS variable layer already in the kit.** If `custom_css` on the active kit defines tokens, that is the site's existing design layer. Reconcile with it or namespace around it. Two token systems styling the same page is the failure this check exists to prevent.

**Duplicate variables.** Two variables holding the same value usually means one was created because the other was hard to find. Report it; do not silently consolidate, because both may be referenced.

**A font variable holding something that is not a family.** `inherit` is valid CSS and invalid as a variable value.

**Global Classes that do not follow one convention.** Mixed naming across existing classes tells you which convention the site actually uses, which matters more than the one this plugin prefers.

**Breakpoints.** Build to the ones that are active. A site running only desktop, tablet and mobile has no laptop or widescreen override to write.

**Container width.** A very large value means section width is being controlled somewhere else, usually per page. Find where before adding a third mechanism.

**Root font size against any rem-based token set.** Themes commonly set the base size on `body`, which does nothing for rem. Check the computed value on `html`.

**Competing templates.** Two theme builder parts of the same type whose conditions overlap. One wins and the other silently does not render.

## Optimizations worth checking

Each of these is a setting, not a rebuild, and each has a plausible reason someone turned it the wrong way. Report what you find; change nothing.

| Setting | Why it matters |
|---|---|
| Elementor performance features: improved asset loading, optimized DOM output, element caching, lazy loading | Off by default on older installs. Turning them on is usually the largest single win available, and each can break a page that depended on the old output, so they go on one at a time with a render check. |
| Font loading method for Google fonts | Remote loading blocks render. Local or swap is usually right. |
| Unused Elementor elements, in Element Manager | Widgets never used on the site still register assets. |
| An optimizer stripping query strings from static resources | Elementor versions its per-page CSS with `?ver=`. Strip it and a returning visitor keeps the old CSS after every edit, so the page renders unstyled and only for some people. This one is worth checking on any site behind a host-level optimizer. |
| Page cache, object cache and the builder's own caches | Elementor keeps CSS and element caches separate from any page cache plugin. Forgetting one is the usual reason an update looks like it did not apply. |
| Post revisions retained | Elementor stores a revision per save, and a long-lived page accumulates thousands of rows. |

## Reporting

Write the findings into the scratchpad's site canon table. Then list recommended optimizations separately, each with what it fixes and what it risks.

**Recommend only. Implement nothing without explicit approval, one item at a time.** A settings change on a production site is exactly the kind of small edit that looks safe and is not. If the user approves one item, do that item and report it; do not carry the approval to the next.
