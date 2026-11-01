# Schema: deciding and generating

Objects, fields and the JSON that creates them. For getting a value onto a page, read `binding.md`.

## Contents

- [Intake](#intake)
- [Plan before generating](#plan-before-generating)
- [Naming and keys](#naming-and-keys)
- [Field rules](#field-rules)
- [Generating JSON](#generating-json)
- [Writing directly through Novamira](#writing-directly-through-novamira)
- [Validate](#validate)
- [The permalink rule](#the-permalink-rule)
- [PHP](#php)
- [Hand over](#hand-over)

## Intake

Ask these in one message, then wait. Skip anything already answered, and state the default you used for anything left unanswered rather than asking twice.

1. **What is being built, in one sentence, and who edits it?** The editor's skill level decides how much instruction text each field carries.
2. **What objects do you think you need?** Post types, taxonomies, field groups, options pages. A rough answer is fine. If they do not know, planning is part of this job, not a prerequisite for starting it.
3. **Does any of this already exist?** If yes, get the current export or read the site. Existing keys are reused verbatim, never regenerated.
4. **ACF version, Pro or free?** Default target is ACF Pro 6.8 or later. Repeater, flexible content, clone, gallery and options pages are Pro only. On free, say which requested fields are unavailable rather than emitting JSON that fails quietly on import.
5. **Are there live URLs that must keep working?** Only matters when a post type or taxonomy is involved. See the permalink rule.
6. **Delivery: JSON files, or write to the site through Novamira?**

## Plan before generating

Do this even when handed a finished field list, because the most valuable output is often a field they do not need. Present the plan, get a yes, then generate. Fifty fields the user rewrites is worse than one round trip.

**Core WordPress before ACF.** Title, excerpt, featured image, author, menu order and the term relationship are already free, already indexed, already understood by every plugin. A `hero_image` field beside an unused featured image is a bug waiting to happen.

**Taxonomy when someone browses or filters by it, field when it is a fact shown once.** A filter built on a checkbox needs a slow meta query on a serialised value and has no archive URL. That decision is expensive to reverse once content exists.

**Nothing stored twice.** If a value can be derived from another field, a term, or the post itself, derive it. Two sources of one truth means one of them goes stale.

Say what you removed and why, in the plan. A field that comes back next quarter as a fresh idea costs more than the sentence explaining why it went.

## Naming and keys

**Keys are readable and match the name.** `field_avg_price` for a field named `avg_price`, `group_community_page`, `post_type_community`, `taxonomy_home_type`. ACF's own UI cannot do this, so generating the JSON is the only place it can be done, which is much of the point of doing it here.

**No instance-specific value in a key.** A key stays generic so the group exports unchanged into another site.

**Field order in the array is the order the editor sees.** Order it as the workflow runs, not as the fields occurred to you.

## Field rules

**Helpful field instructions where an editor could misread the field**, written for the person filling it in. "The average sale price for the quarter, all home types. Enter the number only" beats "Average price". Genuinely self-evident fields can leave it empty.

**Flat fields for flat data. Repeaters for genuinely repeating rows. Flexible content only when the row shape itself varies.**

**Store the raw value.** Never a pre-formatted display string. Format at read time, so one rule formats it everywhere.

**Percentages as the percentage number.** A fraction where a percentage is expected renders wrong silently.

**Property names and value types exactly as ACF writes them.** ACF is tolerant on import and then behaves oddly later. `required` is `0` or `1`, never `true`.

**Every options page gets a real title.** A blank one is invisible in the admin list and in search.

## Generating JSON

One file per object, named for its key:

```
acf-json/
  post_type_<slug>.json
  taxonomy_<slug>.json
  ui_options_page_<slug>.json
  group_<slug>.json
  acf-export-<date>.json      # the combined array, for the Tools screen
```

Default is both: per-object files for `acf-json/`, plus the combined array for the import screen.

## Writing directly through Novamira

The same schema, applied in place instead of handed over.

| Step | Ability |
|---|---|
| Confirm the runtime | `novamira/acf-check-setup` |
| See what exists | `novamira/acf-list-fieldgroups`, `acf-list-post-types`, `acf-list-taxonomies`, `acf-list-options-pages` |
| Read one object in full | `novamira/acf-get-fieldgroup-schema`, `acf-get-post-type`, `acf-get-taxonomy`, `acf-get-options-page` |
| Create or edit | the matching `acf-create-*` and `acf-edit-*` abilities |
| Read and write values | `novamira/acf-read-values`, `acf-write-values` |

Four traps worth carrying:

**The fields array replaces.** `acf-edit-fieldgroup` patches top-level keys but replaces `fields[]` wholesale. Send every field, every time, or the missing ones are deleted.

**Complex values replace too.** Repeater, flexible content, gallery, clone and group writes take an explicit consent wrapper because the write overwrites the field's entire previous content. Confirm before every one.

**`acf/save_post` does not fire.** Writes go through `update_field()`, so `acf/update_value` runs and anything hanging off the admin save does not. If a taxonomy term, a derived field or a cache purge depends on that hook, it will not happen; do it explicitly.

**An options page's menu slug is not its post id.** Values live under the page's `post_id`, which defaults to the shared `options` store. Passing the menu slug as the target reads and writes the wrong place, and returns plausible empty results rather than an error.

Also worth knowing: `get_field()` returns a field's default for values never written, so a fresh post can look pre-populated when nothing has been saved.

## Validate

Run before handing anything over:

```bash
python3 scripts/acf_validate.py <output-dir-or-file>
```

It checks key uniqueness across every file, keys that do not match their field name, conditional logic that points at a key which does not exist, boolean flags written as `true`/`false` instead of `0`/`1`, duplicate field names inside one group, empty repeaters and flexible content, choice values that are labels rather than slugs, and slug length limits.

Errors block the handover. Fix and re-run. Do not paraphrase what it said.

## The permalink rule

When a post type or taxonomy would change URLs that already exist and rank, **stop and say so rather than guessing the rewrite rules.** Emit the object with a note naming the risk, and ask for confirmation that every current URL still returns 200 after import, verified against live URLs rather than assumed from the setting.

Registering a post type with the wrong rewrite silently 404s a page that used to rank, and nobody notices for weeks.

A slug change on a site that already has content orphans that content too: the posts stay in the database under a post type that is no longer registered.

## PHP

JSON and abilities only, unless the user asks for PHP. Some things are simply not expressible in a schema, and it is honest to say so at handover rather than shipping something that half works: publish gates and validation, dynamic choices loaded from another source, terms assigned on save, and anything that renders.

Where the site owns custom PHP through a snippets plugin, that is where it goes. Never register post types, taxonomies or fields in code on a site where ACF owns them. Splitting the source of truth between code and the plugin UI produces broken slugs, labels and capabilities the next time anyone touches either side.

## Hand over

Three lines, plus the files:

1. What to import and how, or what was written and where.
2. What the user still has to decide, named. Choices you invented, values left blank, fields you were not confident about.
3. Anything that needs PHP to actually work.
