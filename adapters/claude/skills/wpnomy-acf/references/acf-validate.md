# ACF JSON validation recipe

Check ACF JSON by hand before handover. This is the same set of checks the maintainer's `dev/wpnomy-acf/scripts/acf_validate.py` runs, written so Claude can do them with Read, Grep and Write. No script is needed or shipped.

## Inputs

One or more ACF export files, or every `*.json` in a folder. Read each file. A file holds one object or a list of objects. Report a non-object entry as an error. Report a file that is not valid JSON as an error and skip it.

## Result

Errors block handover. Warnings never block. Finish with one line: `<n> file(s), <n> key(s). <n> error(s), <n> warning(s).` Print warnings first, then errors, each as `<file or file[index]>: <message>`.

## Object checks

1. Collect every object `key` across all files. A key used twice is an error: `object key '<key>' already used in <file>`. Field keys join the same pool (see field checks).
2. A **field group** is an object with a `fields` property or a `key` starting `group_`. Errors: no `title`, no `location` rules, no `fields`.
3. A **post type** has a `key` starting `post_type_`. Error when `post_type` is empty. Error when the slug is longer than 20 characters (the register_post_type limit).
4. A **taxonomy** has a `key` starting `taxonomy_`. Error when `taxonomy` is empty. Error when the slug is longer than 32 characters (the register_taxonomy limit). Warning when `object_type` is empty: the taxonomy is attached to no post type.
5. An **options page** has a `key` starting `ui_options_page_`. Errors: no `page_title`, no `menu_slug`.

## Field checks

Walk `fields`, then recurse into each field's `sub_fields` and into each flexible content layout's `sub_fields` (`layouts` may be a list or an object keyed by layout id; treat an object as its values). Label nested fields `parent > child`. Field names are unique per group: the set is shared across the whole group including nested fields.

For every field:

- Not an object: error.
- `key` missing: error. `key` already seen anywhere (group keys, object keys, other fields): error naming where it was first used. `key` not starting `field_`: error. When it does start `field_` and a `name` exists but `key` is not exactly `field_<name>`: warning.
- `name` missing: error. A `name` already used in the same group: error.
- `type` missing: error.
- Any of these flags set to a JSON boolean is an error, because ACF stores them as 0 or 1: `required`, `active`, `allow_null`, `multiple`, `ui`, `disabled`, `readonly`, `wrapper_required`, `hierarchical`, `public`, `show_in_rest`, `allow_in_bindings`, `media_upload`, `delay`.
- Each key of `choices` containing a space or any uppercase letter: warning, the choice value looks like a label, not a slug.
- `type` is `repeater` or `group` with no `sub_fields`: error. `type` is `flexible_content` with no `layouts`: error.

## Conditional logic

Gather every `conditional_logic` rule on every field (including nested and layout fields). `conditional_logic` is a list of groups, each a list of rules; each rule's `field` is a field key. Error for each rule whose `field` is not among the collected keys: `<field name>: conditional logic points at '<key>', which does not exist`.

## Parity

Run on the same input, this recipe and the script report the same errors and warnings. Check with a sample that has one failure per rule above.
