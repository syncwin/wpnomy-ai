# Known issues and write fallbacks (Elementor V4)

Written from field feedback with little detail. Treat each item as a lead and verify on the site before relying on it.

## Contents
- Swapping an `e-image`
- Clearing the CSS cache
- When a rich save fails

## Swapping an `e-image`

- When you swap the picture in an `e-image`, update the attachment id, not only the URL. The URL alone can render the old size or a stale `srcset`. Verify on the site that the stored value holds the new id and that the rendered `img` uses the new file.
- Read the element back after the write and compare the id, URL and size with the attachment you meant to use.

## Clearing the CSS cache

- After writes through Novamira, V4 class and variable CSS may not appear until Elementor regenerates its CSS files. Clear the Elementor CSS cache and regenerate the files (Elementor, Tools, Regenerate CSS and Data, or the equivalent ability or WP-CLI command the site offers).
- Check the front end logged out after clearing. Any page cache or host cache in front of Elementor is cleared too. Verify on the site which cache layers exist.

## When a rich save fails

- If a save with rich or formatted text is rejected or comes back altered, fall back to `save_plain_text` for that field, then add the formatting with the element's own controls or classes. Verify on the site that the tool exists under that name, since the live tool list leads.
- Log each fallback in the scratchpad with the field it applied to.
