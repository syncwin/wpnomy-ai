# Binding: getting a field onto a page

The field already exists. This is how its value reaches the rendered page. For designing the field itself, read `schema.md`.

## Dynamic tag or shortcode

Two mechanisms, two jobs.

A dynamic tag is a native Elementor hook. At render it calls the field function directly and hands the value to the element, with no wrapping markup and no string parsing.

A shortcode is a placeholder inside text. WordPress runs the whole block through `do_shortcode()`, a regex pass that scans, queries, swaps and continues. Slightly slower, far more flexible inside a sentence.

**Use a dynamic tag** when the value stands alone: a heading, a standalone figure, a button label, an image source, a link. When a block, column or section must hide itself on an empty field, because Elementor evaluates the empty tag before rendering the container and prevents the gap a shortcode would leave behind. When filling a primitive inside a component or loop item: a heading, an image, a link, a figure. When mapping core metadata: post date, author, featured image, taxonomy terms, anything feeding SEO schema.

**Use a shortcode** when the value sits mid-sentence and an editor needs to write the paragraph naturally. When one block needs several variables, because splitting a sentence across widgets to place two numbers is layout fragmentation. When the text is long-form rich content, disclaimers or documentation. When platform independence matters, since shortcodes survive a move to Gutenberg, Bricks or headless and dynamic tags do not.

## Banned: the Before and After settings

Never build a sentence out of a dynamic tag's Before and After fields. Four reasons, all of which surface later rather than at build time.

Editors lose the sentence. It is split across hidden sidebar inputs and cannot be read or edited on the canvas.

Translation breaks. WPML, Polylang and Weglot see three disconnected fragments, and word order differs between languages, so the sentence is often untranslatable rather than merely awkward.

Formatting is gone. No italics, no inline link, no rich text. Raw HTML in a narrow sidebar input is the only option.

It does not migrate. Text buried in widget metadata does not export cleanly to another builder or to blocks, and reappears as missing phrases scattered through the layout.

Replace it with a shortcode inside the text, or a dynamic tag on its own element.

## Efficiency

**Always pass `post_id` on options-page shortcodes:** `[acf field="phone" post_id="options"]`. Without it WordPress burns queries guessing the loop context, and inside a global template it often guesses wrong.

**Keep a page under roughly 15 to 20 shortcodes.** Each runs a regex pass, and hundreds show up as TTFB.

**Leave no stray brackets in static text.** WordPress still scans the block.

## V4 and ACF

Read this before planning a dynamic V4 page.

Elementor's documented list of dynamic tags supported by V4 atomic elements covers WordPress and WooCommerce, Archive, Author, Comments, Post and Site groups, including **Post Custom Field** and **Request Parameter**. It does not list the ACF-specific tag groups that exist for V3 widgets.

So on a V4 page:

1. Verify in the editor which tags the target atomic element actually offers. Do not assume parity with V3.
2. Post Custom Field reaches a plain ACF value and is the primary route.
3. For anything it cannot express, use a shortcode in a Paragraph element.
4. Where a V3 ACF tag is genuinely required, build that part with a V3 widget only with the operator's yes, and log it with a revisit trigger (black box policy, section 0).

Record the route chosen for each dynamic value in the scratchpad. This is the part most likely to change as V4 matures, and the record is what makes the eventual swap a small job.

## Repeating content

Repeaters, relationships and post loops render through the Loop Builder, never hand-built markup that happens to match today's content.

- Build the loop item template first, then point the Loop Grid or Loop Carousel at it.
- Design the item visually rather than coding it from scratch.
- Map it to ACF fields, the custom post type, or a custom query as the source requires.
- Keep the loop item self-contained. It must not depend on the layout of the archive it appears in.

## Always

- Set a fallback on every dynamic tag that offers one.
- Test on two real records, one complete and one with fields left empty. A preview loaded on the most complete post hides every missing-value bug.
- Match field type to element. An image field in an image element, a URL field in a link control, never forced into text.

## When a field renders blank

Check the render path before assuming the data is wrong. Read the raw stored value first. A correct value can sit behind a disabled snippet, a cached page, a tag reading the wrong key, or a code path that does not execute in preview mode at all. Confirm on the published page before treating empty preview output as a bug.
