# Design standards

The bar: sleek, responsive, accessible, scalable, organised, clean, efficient, no fluff. User experience outranks visual ambition whenever the two pull apart.

## Layout

Two-column rhythm is the workhorse. Full-width single-column sections are earned, by tables, FAQs, stat grids and short section intros; two full-width text-only sections back to back read as a document, not a page.

Alternate image sides across consecutive splits and track it while building.

Pair sibling topics side by side in one section instead of stacking them as two. This is the single biggest lift over a naive build.

In a split, the heading lives inside its column, left-aligned at the top of the text column. A lone centred heading floating above a split looks unresolved; centred headings belong to genuinely full-width sections.

A dark treatment is a panel, not wallpaper: a rounded inner container on a light section, reserved for the one or two most decision-critical blocks and the closing CTA.

Vary without churning. No more than two consecutive sections sharing a pattern, and no using every pattern once to prove range.

## Rhythm

Section-to-section gap is a deliberate value on the section's own padding, never a blank spacer element.

The last item in any repeated group gets no trailing border or margin, because a divider under nothing reads as a bug.

Cap running text width. Full-width body copy on a wide screen reads as unfinished.

To centre a block while keeping its content left-aligned, box and centre the parent and leave the content alone.

## Typography

Title Case headings unless it reads badly.

A hero H1 is the largest, boldest thing on the page. A timid one against a heroic mockup is a defect, not a preference.

A line mixing bold and plain text is one element with inline strong, not two elements that drift apart on wrap.

## Tables

Native table widgets squeeze multi-column data into unreadable cells below full desktop width, so build data tables as markup.

- Scrollable bordered wrapper, standard table inside. Horizontal scroll on the wrapper, never the page body.
- A change or trend cell renders as a pill, not coloured plain text.
- Below the mobile breakpoint, hide the header row visually using clip rather than display none so it stays accessible, and stack each row as label and value pairs.
- Every colour resolves to a global or a variable first.

## Accessibility

WCAG 2.2 AA is the working bar, built to the highest practical standard without degrading the experience.

- Valid heading outline. One H1 or none where the theme supplies it.
- Landmarks through semantic tags.
- Colour contrast checked against the site's palette rather than eyeballed. A failing brand pairing is raised, not shipped.
- Visible focus states on every interactive element.
- Alt text on every meaningful image, empty alt on decorative ones.
- Keyboard reachable in a sensible order, with disclosure and tab patterns using native or Elementor-native markup so keyboard and screen reader behaviour come free.
- Never colour alone to carry meaning.

## CTAs

Point every CTA at the destination that keeps the visitor moving through the site. A generic CTA aimed at a dead end where a better internal link exists is a defect.

A closing CTA meant to echo the hero reuses the hero's exact tokens, not similar ones, so a palette change carries through.
