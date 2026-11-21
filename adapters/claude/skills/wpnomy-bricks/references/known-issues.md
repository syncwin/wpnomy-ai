# Known issues

Checked on Bricks 2.4.5. Re-test on other versions before relying on a workaround.

## Contents
- Abilities that fail
- Running PHP as user 0

## Abilities that fail

- **`bricks/preview-html-css-page-import`** adds an svg signature to the result and then rejects it. Workaround: import with placeholders for the signed parts, then sign the elements with `Admin::process_elements_for_signature` (needs the PHP route below, so only with an explicit yes).
- **`bricks/upload-custom-icon`** rejects SVG files that are valid. Workaround: upload the file as normal media and use an `image` element, or add the icon in the builder UI. Tell the owner which icons were swapped.
- **`bricks/create-template`** rejects the svg signature, `user_id` and `time` keys. Strip them, create, then re-sign (see `templates-and-components.md`).

## Running PHP as user 0

`execute-php` runs as user 0, which has no capabilities, so abilities gated by Bricks code fail with a permission error.

1. Set an admin user for the request (`wp_set_current_user( <admin id> )`).
2. Reset `Bricks\Capabilities` `capabilities_set`. It is cached per request, so it still holds the user 0 result until you clear it.
3. Then call the gated code.

Only with an explicit yes for `execute-php`, as the main rules say.
