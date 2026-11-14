# Intake: screenshot, mockup, or existing JSON

## From a screenshot or mockup

Transcribe before designing. Build a table of section, layout, elements, content, notes. Confirm it, then build from the table.

**Never read values off the image.** A screenshot gives proportion and intent, not pixels. Spacing maps to the site's existing scale, colour to an existing global or variable, type size to an existing font style. If the mockup needs something the system cannot express, say so and ask whether to extend the system or adjust the design. Adding a token silently is how a design system dies.

| Extract | Ignore |
|---|---|
| Section order and hierarchy | Exact pixel measurements |
| Column structure and proportion | Screenshot colour values, compressed and shifted |
| Which elements are which, and their state | Placeholder copy, unless confirmed final |
| Repeating patterns that should become a component or class | Fonts guessed by eye |

Where the mockup shows one instance of something that clearly repeats, flag it as a component or BEM block before building it three times. Ask about what the image cannot show: hover and focus states, empty states, other breakpoints, what is dynamic, where links go.

## From an existing Elementor JSON

1. Parse the whole element tree and inventory what exists before touching anything.
2. Change only what was asked.
3. Preserve every untouched element and its id. Do not delete and rebuild an element to change one setting.
4. Do not restructure, restyle or tidy anything outside the request.
5. Note anything wrong but out of scope in the scratchpad and report it rather than fixing it silently.

Read the file's own conventions first: global ids, class names, spacing values. Match them. An edit introducing a second convention is worse than the flaw it fixed.
