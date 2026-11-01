# JSON generation mode

V3 files are for changes to an existing V3 export only: V3 is maintain-only, and new pages are V4 or Bricks (black box policy, section 0).

Files only. Never claim anything is live.

## V4 is blocked

Do not generate V4 JSON until a verified V4 export from a real site is in hand. The atomic element schema, the property type wrapping, the Global Class id format and the variables payload are all new, and an invented shape imports as a broken or empty page.

If asked for a V4 file, say so plainly and offer two routes: build through Novamira instead, or supply one V4 export containing a heading, an image, a button, a Global Class and a Variable reference, after which this restriction lifts. V3 has no such gap.

## V3 envelope

Exactly these keys. Wrong keys fail the import with no useful error.

```json
{"content": [], "page_settings": [], "version": "0.4", "title": "<Page Name>", "type": "container"}
```

## V3 rules

- Containers only, `"elType": "container"`. Nested content containers carry `"isInner": true`.
- Every element gets a unique lowercase hex id of 7 or 8 characters. Accordion item entries use `_id`.
- Colours and fonts go through `__globals__`, referencing the target site's own global ids from its Export Kit. Never carry another site's ids across.
- Responsive padding on every top-level section, `isLinked: false`, with tablet and mobile values.
- Never invent a control key. Copy the key and its value shape from the site's own export.
- No media library ids from another site. Images use an empty id with a placeholder or supplied URL.
- Dynamic tags only where asked, and only in a format verified against a real export.

## Validate

1. JSON parses: `python3 -c "import json; json.load(open('file.json'))"`.
2. Envelope keys exact.
3. All ids unique. Any `items` array length matches its child container count.
4. Zero hardcoded colours, zero foreign media ids, zero control keys absent from the reference export.
5. Every heading in the brief present in the output.

## Deliver

Write to `/mnt/user-data/outputs/` as `<site>-<page-or-part>-elementor.json`, loop items as `<site>-loop-<name>-elementor.json`. Present with the import path, the ACF field groups that must already exist, and any display conditions to set by hand after import.
