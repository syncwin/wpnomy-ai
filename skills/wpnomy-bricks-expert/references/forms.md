# Forms

Lead forms (contact, home evaluation, showing request) use the native Bricks `form` element: it has server handling, so it is an allowed builder-bound element under the policy. Every field and state is styled by classes only; labels and error states stay accessible. No custom HTML form substitute.

## Read first

1. Resolve the post and the form element.
2. `bricks/get-form-config` before editing an existing form.
3. `bricks/get-element-schema` `{ elementName: "form" }` for the controls and which actions this site offers.

## Fields

- Fields live in `settings.fields[]`; each has `type` plus its type keys. Types: `email`, `text`, `textarea`, `richtext`, `tel`, `number`, `url`, `image`, `gallery`, `checkbox`, `select`, `radio`, `file`, `datepicker`, `password`, `rememberme`, `html`, `hidden`.
- Checkbox, select and radio `options` are newline-separated; `valueLabelOptions` when the stored value differs from the label.
- `bricks/update-form-fields` **replaces the whole ordered array**: merge the change into the full current array and keep every existing field `id`.
- Placeholders in email and webhook content bind to the field **id**: `{{abc123}}`, `{{all_fields}}`, `{{referrer_url}}`; file fields `{{id:url}}` (or `name`, `type`, `size`, `id`). A field's custom `name` changes only the submitted input name. Keep ids stable when relabelling; avoid hyphens in placeholder names.
- Normal dynamic data (`{post_title}`) renders in subject, body, redirect URL and webhook content after field placeholders. `admin_email` is a recipient option, not a tag.

## Actions

- `bricks/update-form-actions` replaces the supplied action list and merges action settings; keep unrelated actions and their order.
- Actions run in stored order, except `redirect`, which always runs last. An error stops the rest, so validation-style actions go first.
- Built-in: `email`, `webhook`, `redirect`, `custom`, `login`, `registration`, `lost-password`, `reset-password`, `create-post`, `update-post`, `mailchimp`, `sendgrid`. `save-submission` appears only when Bricks > Settings > Form > Save submissions is on.
- Saving submissions needs both the site setting `saveFormSubmissions` (writable through `bricks/set-global-settings`) and the `save-submission` action on the form. Read with the paginated `bricks/list-form-submissions`.
- Per-action conditions: `settings.actionConditions` rows `{ action, conditions: [{ fieldId, compare, value? }], conditionsRelation: "and" | "or" }`. Keep existing rules.
- Webhook: 15 s timeout, no retry; errors recorded unless `webhookErrorIgnore`; without a template the payload keys are `form-field-<id>`.
- A custom action key works only if its `bricks/form/action/<key>` hook already exists on the site.
- Lead routing (CRM, Follow Up Boss) is a webhook or email action agreed with the operator; never invent an endpoint.

## Spam and delivery

- Honeypot: a `hidden` field with `isHoneypot: true`.
- reCAPTCHA v3 needs `enableRecaptcha` on the form and a global site key; keys alone protect nothing. Turnstile: `turnstileInitialization` (`viewport` or `interaction`; unset loads on page load), `turnstileViewportDistance` 0 to 5000 (default 300).
- Check keys with `bricks/list-credential-status`; never read their values.
- Email goes through `wp_mail()`. A successful handoff is not delivery: the site needs an SMTP plugin, a from-address on its own domain, and the provider's logs.

## Verify

- A configuration review is read-only. Never submit a production form to check layout: a submit sends email and webhooks.
- Functional tests go to an agreed test destination, from the front end, not the builder.
- Read back with `get-form-config`; check validation, error, success and deferred CAPTCHA states in a browser, by keyboard.
