---
name: wpnomy-builderius-expert
description: Build and edit Builderius templates, components and global settings under the house black box policy, and map Atomic Framework variables, classes and breakpoints into Builderius. Use when the site runs Builderius or Builderius PRO, when the user says Builderius, Builderius template, Builderius component, HtmlElement, global CSS, CSS variables panel, Builderius breakpoints, commit, publish, or pastes Builderius copied elements, or when the wpnomy router sends Builderius work here. Covers the HtmlElement module, global settings commits through GraphQL, variables in global CSS, breakpoints, components, publishing safely and front-end checks. Not for Bricks, Oxygen or Elementor.
license: MIT
metadata:
  displayName: WPnomy Builderius Expert
  version: 0.1.1
  author: "@wasimness"
  company: SyncWin
---

# WPnomy Builderius Expert

Checked on Builderius 1.4-beta with Builderius PRO 1.4-beta. On another version, re-check each step on the site first.

**Needs:** `${CLAUDE_PLUGIN_ROOT}/skills/wpnomy/references/house-rules.md` (read it first). Site access through Novamira (or another way to run PHP). Pasting into the Builderius editor needs the owner's sign-in, so the owner does that step.

## 1. How Builderius stores things

- **Versioned, like git.** Templates and the global settings set have branches and commits (post types `builderius_template`, `builderius_component`, `builderius_sett_set`, `builderius_branch`, `builderius_commit`, `builderius_release`). Every change is a new commit, so history and undo come free.
- **GraphQL API** at the REST route `POST /wp/v2/builderius` with body `{ "queries": [ { "name", "query", "variables" } ] }`. From PHP, call it with `rest_do_request()` as a signed-in user who can edit Builderius.
- **Publishing is separate and global.** Publishing makes every template and setting live at once, so an automatic publish can take someone's unfinished work live. Commit without publishing (`autopublish: false`) and let the owner publish.

## 2. Global settings (breakpoints, global CSS)

Read the active commit:

```graphql
{ global_settings_sets(technology: html) { active_branch { id active_commit { content_config } } } }
```

`content_config` is JSON; settings sit in `template.settings` as `{ name, value }` rows (for example `breakpoints` and the global CSS). Change only the rows you own, keep the rest, and write a new commit:

```graphql
mutation($input: BuilderiusCreateCommitInput!, $publish: Boolean) {
  createCommit(input: $input, autopublish: $publish) { commit { name } }
}
```

with `input = { branch_id, description, serialized_content_config }` and `publish = false` unless the owner asked to publish. A result without `errors` and with `createCommit` means Builderius accepted it.

**Before writing,** save the whole `content_config` so a restore can commit it back.

## 3. Variables and classes

- **Variables** go in the global CSS as one clearly marked `:root { ... }` block. That is where Builderius keeps its own global CSS variables, and its CSS variables panel lists them. Never touch the rest of the global CSS.
- **Classes:** Builderius styles any valid selector in its UI (classes, attributes, combinators, pseudo-classes). Use BEM classes; put `:hover`, descendants and `@media` in the class's own rules.
- **Builderius CSS Framework** is optional. When the site uses the Atomic Framework or another framework, don't load both for the same job.
- **Heading sizes (custom feature):** Builderius sizes headings only site-wide in its global styles. Size library headings through their classes instead, so other pages don't change.

## 4. Elements

Builderius has one native module that takes any tag: **`HtmlElement`**, with `tag`, `tagClass`, `tagId`, `htmlAttribute`, raw `content` and `%local%` CSS. The library maps to it one-to-one with no fallback, so nothing needs to be a black box. Use it for every primitive (section, div, heading, text, button, link, image, list, svg). Loops, forms and other builder-bound parts follow house rules §5.

## 5. Copy and paste

Builderius's Copy writes `{ modules, indexes, template, version, source: "builderiusCopiedElements" }`, and Ctrl/Cmd+V in the editor reads it back. When generating it:

- Put CSS in a `style` element.
- Break up Builderius template delimiters in content (`{{ }}`, `[[[`, `[%`, `[^`), or Builderius will try to parse them.
- Treat the format as unverified until one real paste in the editor works; until then, hand over HTML plus classes.

## 6. Breakpoints

Breakpoints are the `breakpoints` row of the global settings. Push the project's whole breakpoint setup relative to the base, keep a copy of the rows you replaced, and on Remove put them back. Desktop-first by default (house rules §4).

## 7. Components and templates

Global components support nesting, conditional display and custom properties. Build a repeated part once as a component; a part it cannot express exactly stays plain `HtmlElement`s. For content types like blog posts, design the layout as a Builderius template and keep the content in the WordPress editor.

## 8. Check

1. Read the settings back and confirm the new commit holds your change.
2. After the owner publishes, load the front end at the base and at every breakpoint.
3. Run the router's hand-over checklist (house rules §7).

Next: report to the owner, then the router's scratchpad.

## Scratchpad

End with the scratchpad: every request with its status (done, partly done, in progress, failed, not started, needs you), then the commits made (not published unless asked), what was verified on the site and what was not, and the Builderius version checked.
