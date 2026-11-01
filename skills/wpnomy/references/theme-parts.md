# Theme parts and display conditions

Two halves of one question: where a template applies, and what appears inside it once it does.

## Theme builder parts

A part is not a page. It renders inside other content, usually many times, against records whose shape varies.

| Part | Built against | The thing that breaks it |
|---|---|---|
| Header, footer | Every page | A layout that assumes the hero below it, or a transparent state that only works on one page |
| Single | One record of a post type | Fields left empty on some records |
| Archive | A query that can return nothing | No empty state, and no thought about page 2 |
| Loop item | One record, inside a grid it cannot see | Styling tuned to the archive it was first placed in |
| Popup, off-canvas | A trigger | A trigger that never fires, or fires everywhere |

Rules that follow from that:

**Build the loop item first, then the grid.** The reverse means styling the item through the grid's preview, which bakes in assumptions about column width.

**Keep a part self-contained.** It must not depend on the page it lands in. A header that needs the page below it to supply top padding is broken on the one page that does not.

**Test against a sparse record and an empty query**, not the best-populated one. Most template defects are missing-value defects, and a preview on a complete record hides every one.

**Check what the part replaces.** Assigning a single template takes over every record matched by its condition, including ones nobody looked at.

**One part, one job.** Two headers with a condition each beats one header with visibility rules inside it, because the condition is visible in the Theme Builder list and the internal rules are not.

## Display conditions

Two different mechanisms with the same name. Using the wrong one is the usual mistake.

| | Template conditions | Element conditions |
|---|---|---|
| Set on | A theme builder part | A container or widget |
| Answers | Which content this template renders for | Whether this block appears at all |
| Lives in | The Theme Builder, visible in the list | The element's own settings, invisible until you open it |

**Template conditions decide reach.** Include broadly, then exclude, rather than listing every inclusion. `Singular / Posts` minus one category is maintainable; twelve individual post rules is not, because nobody updates it when post thirteen arrives.

Order matters: a more specific condition beats a broader one. Two parts of the same type competing for the same URL is a defect, not a preference. Check the list after adding one.

**Element conditions decide visibility.** Use them for a block that should not exist for some visitors or some records: a badge that only applies to featured listings, a section that depends on an optional field.

**An empty dynamic tag already hides its container.** Elementor evaluates the tag before rendering, so an ACF-driven block with a dynamic tag needs no condition to disappear when the field is blank. Adding one is a second mechanism for a job already done, and it will eventually disagree with the first.

**A true/false field switches visibility, not content.** If two variants of a block both need to exist, that is two blocks with opposite conditions, not one block whose contents change.

**Conditions hide, they do not secure.** Conditioned content can still be in the response. Anything that must not reach a visitor is a capability check, not a display condition.

## Recording them

Write every condition into the scratchpad in plain language, one line each, naming the part or element and what the condition says. Conditions are the least discoverable thing on a site: they are invisible in the page, invisible on the front end, and the next person finds them by opening elements one at a time.
