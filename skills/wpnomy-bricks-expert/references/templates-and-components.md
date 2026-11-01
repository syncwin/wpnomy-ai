# Components, templates, navigation, nestables, popups and interactions

## Contents

Components · Templates and conditions · Headers and footers · Navigation and mega menus · Nestables · Popups and modals · Interactions

## Components

A component is structure, not styling (policy section 3). Use one for structure repeated on more than one page or template: proof strip, CTA band, author box, FAQ block, card types, listing strip, source line. Shared styling alone is a class.

- Read `bricks/list-components` first. Labels are unique (`bricks_conflict_duplicate_component_name`) and carry the library id: `CTA Band (CTA-02)`. Always write a short `desc`.
- Build the subtree once on a page, then `bricks/extract-component-from-elements` `{ postId, rootElementId, label, category, desc }`. It rewrites ids, swaps the subtree for an instance and snapshots a revision; `properties` and `variants` start empty. Never copy-paste a subtree (duplicate ids).
- `bricks/create-component` accepts nested or flat elements and regenerates ids; `connections` may use the input ids and are remapped.
- Properties: `{ id, label, type, connections: { "<elementId>": ["<controlKey>"] }, default, desc, group, options, multiple, replace }`. Types: `text`, `editor`, `icon`, `image`, `image-gallery`, `link`, `select`, `toggle`, `query`, `class`. An unconnected property does nothing.
- Variants by class: a `class` property connected to `_cssGlobalClasses`, named `options` whose `value` is an array of class ids, `replace: true` for true variants. The instance stores the option `id`.
- A toggle property connected to "Hide element" removes the element from the DOM.
- Instance: `{ "cid": "<componentId>", "properties": { ... }, "slotChildren": { "<slotElementId>": [ ...children ] } }`. Slots are real `slot` elements, keyed by their id; keep slot ids stable.
- Nested component property pass-through: `"properties": { "label": "parent:cid_<outerRootId>:prop_<propId>" }`. No guard against circular nesting.
- Editing one existing component: the `resolve-agent-file` and `commit-agent-file` route. `bricks/update-component` replaces the whole tree and needs `expectedDesignSystemVersion` plus the full `expectedComponentDigest`; removing a slot needs `allowSlotOrphans: true`.
- Readback with `bricks/get-component`: `_version` present, every `connections` key a surviving element id, every `slotChildren` key a real slot, nested property keys exist.
- Delete only with a yes: `get-component` digest, `get-design-context({ includeUsage: true })` for `usedOnPosts`, then `bricks/delete-component` with `expectedDesignSystemVersion`, `expectedComponentDigest`, `expectedUsageCount` and `allowOrphans: true`. A `component_usage_count_mismatch` may mean hidden references; never retry with the returned count. Orphaned instances render as "missing component".
- Dynamic tags inside a component resolve where the instance sits. Query filters and their target loops stay at page or template level, never inside a component. Classes and variables a component uses must exist on any site it is moved to.

## Templates and conditions

Types: `header`, `footer`, `content` (single), `archive`, `search`, `error` (404), `section` (inserted with a Template element, never self-rendering), `popup`, `password_protection`.

`bricks/set-template-conditions` `{ templateId, conditions: [...] }` replaces the list. Shapes:

| Target | Condition |
|---|---|
| Whole site | `{ "main": "any" }` (never `entireWebsite`) |
| Front page | `{ "main": "frontpage" }` |
| A post type's singles | `{ "main": "postType", "postType": ["city"] }` |
| A post type archive | `{ "main": "archiveType", "archiveType": ["postType"], "archivePostTypes": ["project"] }` |
| Terms | `{ "main": "terms", "terms": ["category::5"] }` (`taxonomy::id`; `archiveTerms` also accepts `taxonomy::all`) |
| Specific pages | `{ "main": "ids", "ids": [42] }` |
| Search results | `{ "main": "search" }` (never `any`: all body templates are scored together) |
| 404 | `{ "main": "error" }` |
| Hooked section | `{ "main": "any", "hookName": "...", "hookPriority": 10 }` (section templates only; `hook` is stored as `any`) |

- Several conditions are OR; there is no AND. Empty conditions mean the template never renders except as a narrow fallback; never rely on that.
- Highest score wins: `ids` 10, `frontpage` 9, child pages, assigned terms, specific archives, author, date, search and error 8, a post type or all CPT archives 7, `archiveType: any` 3, `any` 2; `password_protection` adds 100. Equal scores depend on order: never rely on a tie.
- A `content` template on `any` takes over every singular page. A post type with `has_archive` off has no archive URL. A taxonomy or post type slug change is not migrated in saved conditions.
- Template settings through `bricks/set-template-settings`; read back with `bricks/get-template` or `bricks/get-template-settings`. Duplicate a template with `bricks/duplicate-post`.
- Write every template's conditions into the scratchpad in plain language, with the expected winner per URL type.

## Headers and footers

- Bricks wraps a header template in `<header>` and a footer in `<footer>`. The root is a `section` or `block`, never tagged `header` or `footer` (double landmark).
- Element writes route by template type automatically (header to `_bricks_page_header_2`, footer to `_bricks_page_footer_2`). Never pass an area. An empty `get-page-elements` after a header write means routing failed: stop.
- Baseline: one header and one footer on `{ "main": "any" }`. A page-specific header is a header template on `{ "main": "ids" }`. No matching header template means no header.
- Sticky: `position: sticky` on the header class (policy), not the template's sticky panel.
- A loop inside a header or footer turns on "Disable query merge".

## Navigation and mega menus

Builder-bound: navigation needs the mobile toggle. Markup stays `nav` plus `ul`, styled by class.

- New headers use `nav-nested`. Its direct child is a wrapper (typically `block` with `tag: "ul"`) whose `settings._hidden._cssClasses` contains the token `brx-nav-nested-items`. Links and dropdowns go inside it. Each `dropdown` needs a **direct** child with `_hidden._cssClasses` containing `brx-dropdown-content`. On Bricks 2.4.2 and later, read `nestableChildren` from `bricks/get-element-schema` for `nav-nested` and `dropdown`, allocate fresh ids, and never replace saved content with defaults. A `missing_navigation_scaffold` error is fixed by adding or moving only the wrapper. Our own classes go beside those tokens, never replacing them.
- Use `nav-menu` (a WordPress menu) only when the client must edit menus in Appearance > Menus. Menu edits: `bricks/list-nav-menus`, `bricks/get-nav-menu`, then `bricks/save-nav-menu` (omitted items are kept). Removals only through `bricks/delete-nav-menu-items` with explicit ids or `bricks/delete-nav-menu`, keeping the returned `beforeDelete`. Menus have no revisions.
- Mega panel, native: `dropdown` with `megaMenu: true`, optional `megaMenuSelector` (width and position anchor, default body), `megaMenuSelectorVertical`, and a deliberate `toggleOn` (`click`, `hover` or `both`). Panel children are not wrapped in `li`; on mobile the panel becomes static inside the drawer.
- Mega panel from a WordPress menu: a `section` template with `status: "publish"`; `save-nav-menu` item `bricksOptions: { megaMenuTemplateId }` (top-level items only); the header `nav-menu` with `menu`, `megaMenu: true` and `megaMenuToggleOn`. Never build the panel as a header or footer template.
- Off-canvas drawers are the `offcanvas` element, toggled by an interaction with `action: "toggleOffCanvas"` and `offCanvasSelector`.
- Verify: readback of the header and the menu; in a browser, the desktop open state and width, hover and click, keyboard focus, Escape and outside close, the mobile drawer and the current-item state.

## Nestables

Assemble the whole widget in memory and insert it once; children do not auto-populate. Bricks' structural class tokens drive its styling, ARIA and JS pairing: never remove them, and add our classes beside them.

- **Accordion Nestable** (house default for FAQs, builder-bound). Each item is a title block and a content block; questions are `h3`. Bricks handles `aria-expanded` and keyboard support; never add them by hand. Option names differ between sources (`accordionOneAtATime` in the official prose, `independentToggle`, `expandItem` and `faqSchema` in the schema): read the live schema and copy a valid instance. One FAQPage source per page: `faqSchema` stays off wherever the data plugin or the SEO plugin emits FAQPage.
- **Tabs Nestable**: `openTab` is a 0-based string. Structure, with titles and panes in matching order and count, and content only inside panes:

```text
tabs-nested (openTab: "0")
  block (_hidden._cssClasses: "tab-menu")
    div (_hidden._cssClasses: "tab-title")   x N
  block (_hidden._cssClasses: "tab-content")
    block (_hidden._cssClasses: "tab-pane")  x N
```

- **Slider Nested** only where `scroll-snap` cannot do the job. A loop goes on one child slide block, never on the widget.
- For any nestable in a loop, the loop sits on the child item wrapper.

## Popups and modals

Policy first: a modal is a native `dialog` or the Popover API (see `elements-and-pages.md`). A Bricks popup is builder-bound and used only when it needs what those cannot do (frequency limits, AJAX content).

- A popup is a `popup` template. Without matching display conditions it is not in the DOM and nothing can open it, `bricksOpenPopup` included.
- Opener: interaction `{ "trigger": "click", "action": "show", "target": "popup", "templateId": <id> }`. There is no `openPopup` action.
- Settings through `bricks/update-popup-settings`: `popupCloseOn` (one of `backdrop`, `esc`, `none`), `popupBodyScroll`, `popupAjax`, the `popupLimit*` frequency keys, template interactions `showPopup` and `hidePopup`. Default z-index 10000 (`popupZindex`). Read with `bricks/list-popups` and `bricks/get-popup-config`.
- A form in a popup needs a success state or close behaviour.

## Interactions

Only where CSS and native HTML have no route: a popup opener, an off-canvas toggle, load more. Each one ships inline `data-interactions` JSON.

- Write with `bricks/update-element-interactions` (replaces the element's rows, generates ids); read with `bricks/get-element-interactions`, checking `effectiveInteractions`, because class interactions stack with element ones.
- Row: `{ id?, trigger, action, target: "self" | "custom" | "popup", targetSelector?, templateId? }`. Actions include `show`, `hide`, `toggleOffCanvas` (`offCanvasSelector`), `loadMore` (`loadMoreQuery: "<queryElementId>"`), `setAttribute`, `toggleAttribute`, `scrollTo` and `javascript` (`jsFunction` naming a `window` function, `jsFunctionArgs` rows with ids; no inline JS).
- Target by a `js-` class, never `#brxe-<id>`: duplication and `_cssId` change ids. Use `runOnce` inside loops.
- Hover, focus and entrance effects are CSS on the class, never an interaction.
