# First-run site audit

Run once per site, the first time any skill in this plugin touches it. Read-only. Record the result in the scratchpad so later runs skip it.

Two purposes: learn the site canon so the build uses what exists, and spot settings that make Elementor work worse than it needs to.

## Read these

Through Novamira, in this order. None of them write.

| Call | Gives you |
|---|---|
| `novamira/elementor-check-setup` | Core and Pro versions, whether the V4 atomic runtime, style schema, Global Classes, Variables and Interactions are available, container width, active breakpoints |
| `novamira/elementor-list-variables` | Every V4 Variable with id, label, type, value |
| `novamira/elementor-list-global-classes` | Every Global Class and its variants |
| `novamira/elementor-list-v3-styles` | System and custom Global Colors and Typography |
| `novamira/elementor-list-dynamic-tags` | Which dynamic tags exist on this install, including whether ACF groups are present |
| `novamira/acf-check-setup` | ACF edition, version, whether post types, taxonomies and options pages are manageable |
| `novamira/acf-list-fieldgroups` | Field groups, their source (db, json or php) and whether they are editable |
| `novamira/get-active-design` | Whether a Novamira design is active and who holds authority |
| Active kit `custom_css` | Any existing CSS variable layer, which the build must not collide with |
| Theme base font settings | The computed `html` font size, which decides whether rem-based tokens are safe |

## What to look for

**A CSS variable layer already in the kit.** If `custom_css` on the active kit defines tokens, that is the site's existing design layer. Reconcile with it or namespace around it. Two token systems styling the same page is the failure this check exists to prevent.

**Duplicate variables.** Two variables holding the same value usually means one was created because the other was hard to find. Report it; do not silently consolidate, because both may be referenced.

**A font variable holding something that is not a family.** `inherit` is valid CSS and invalid as a variable value.

**Global Classes that do not follow one convention.** Mixed naming across existing classes tells you which convention the site actually uses, which matters more than the one this plugin prefers.

**Breakpoints.** Build to the ones that are active. A site running only desktop, tablet and mobile has no laptop or widescreen override to write.

**Container width.** A very large value means section width is being controlled somewhere else, usually per page. Find where before adding a third mechanism.

**Root font size against any rem-based token set.** Themes commonly set the base size on `body`, which does nothing for rem. Check the computed value on `html`.

**Competing templates.** Two theme builder parts of the same type whose conditions overlap. One wins and the other silently does not render.

## Optimizations worth checking

Each of these is a setting, not a rebuild, and each has a plausible reason someone turned it the wrong way. Report what you find; change nothing.

| Setting | Why it matters |
|---|---|
| Elementor performance features: improved asset loading, optimized DOM output, element caching, lazy loading | Off by default on older installs. Turning them on is usually the largest single win available, and each can break a page that depended on the old output, so they go on one at a time with a render check. |
| Font loading method for Google fonts | Remote loading blocks render. Local or swap is usually right. |
| Unused Elementor elements, in Element Manager | Widgets never used on the site still register assets. |
| An optimizer stripping query strings from static resources | Elementor versions its per-page CSS with `?ver=`. Strip it and a returning visitor keeps the old CSS after every edit, so the page renders unstyled and only for some people. This one is worth checking on any site behind a host-level optimizer. |
| Page cache, object cache and the builder's own caches | Elementor keeps CSS and element caches separate from any page cache plugin. Forgetting one is the usual reason an update looks like it did not apply. |
| Post revisions retained | Elementor stores a revision per save, and a long-lived page accumulates thousands of rows. |

## Go-live purchase check (stores)

Check a purchase without placing an order, through the Store API:

1. `GET` the cart (send the `Nonce` and `Cart-Token` headers).
2. `POST cart/add-item` with a real product.
3. `POST cart/update-customer` with a real local address.
4. Read the totals, `shipping_rates` and `payment_methods`.

A missing carrier rate or payment method shows up here. Report it; fix nothing without a yes. Remove the test cart item afterwards.

## WooCommerce go-live checks

Read-only. Report each finding; change nothing without a yes.

- **Weight and size.** Compare the store's weight unit with the product values (for example `0.6` in a `g` store is almost certainly wrong). List products with missing dimensions.
- **Shipping zones.** List each zone and its methods. A zone with no method, or a customer address that matches no zone, gives no rate.
- **In-request cart test.** In one PHP request, load the cart (`wc_load_cart()`), set the shipping location with `WC()->customer->set_shipping_location()` and call `calculate_shipping()`. Add an `http_response` filter to capture the carrier API reply. Cart loops in one request can reuse a stale tax location, so test each address in a new request.
- **Local pickup plus a national courier.** Use a postcode zone (a postcode prefix such as `123*`) ordered above the country zone, holding pickup and the courier. The country zone gets the courier only.
- **Shipping plugin prerequisites (Shiprocket as the example).** Rates need the merchant link (the plugin's signup button fills `integration_id`), realtime rates on, and a verified account with a pickup address and wallet. Until then the API answers "pincode not serviceable". The fallback rate shows only when the zone has no other method. It may add no tax on shipping, so check the tax on live courier rates once active.
- **Razorpay.** The plugin (woo-razorpay 4.x) creates its own webhook at `admin-post.php?action=rzp_wc_webhook`, not the old `?wc-api=razorpay` route. Verify server-side with the plugin's SDK (`$api->request->request('GET','webhooks')`) before asking anyone to add one by hand.
- **Native tax classes (GST as the example).** Standard and Reduced classes, with per-class rows for the store state (CGST then SGST, by priority) and a blank-state IGST row at priority 1 so the specific state wins. Rates by price band change by law: confirm current rules with the owner. Test with `WC_Tax::find_rates()`. Idea for a later brand-agnostic add-on: a FluentSnippets filter on `woocommerce_product_get_tax_class` (and the variation filter) that picks the class from the live price, with settings for the threshold, the classes and excluded categories. Create the snippet with `Helper::createSnippet()`, then set `@status: published` and call `cacheSnippetIndex()`. A workflow plugin cannot do this, since it reacts to events and does not filter prices.
- **Email body font.** A Times or empty `woocommerce_email_font_family` makes body text serif under the MailPoet WooCommerce template. Count `font-family:` in an `EmailPreview` render. MailPoet's `woocommerce.brandingColor` is both the heading bar and the link colour, so keep it dark.

## Email checks

- **Which mailer sends.** Hook `wp_mail_failed` and send a test. After deactivating a mailer plugin, test in a new request, since the old one can linger in the current request.
- **Free mail plans** (for example a free hosted mailbox tier) often have no SMTP. Do not plan on them as the sender.
- **MailPoet Sending Service.** When active, it can send all site emails (`send_transactional_emails`) once FluentSMTP is off.
- **MailPoet automations from templates.** Create with `CreateAutomationFromTemplateController::createAutomation('<slug>')` and edit step args through `AutomationStorage`. The email itself is only created when "Edit content" is opened in the UI (choose the Classic editor). Then edit its JSON body, activate with `setStatus('active')` plus `AutomationValidator`, and check with `SendPreviewController::sendPreview()`. The WooCommerce template (`wc_transactional`) and the confirmation email are JSON bodies you edit by walking `content.blocks`.
- **Logos.** SVG does not render in Gmail or Outlook. Use PNG. A PNG on a solid light rounded plate stays readable in dark mode. Server Imagick often lacks the SVG delegate, so render with a local headless browser.
- **Vector check.** An uploaded `.svg` may only wrap a base64 PNG (`<image xlink:href="data:image/png...`). That is not a vector: ask for a true vector or trace the alpha channel.

## Reporting

Write the findings into the scratchpad's site canon table. Then list recommended optimizations separately, each with what it fixes and what it risks.

**Recommend only. Implement nothing without explicit approval, one item at a time.** A settings change on a production site is exactly the kind of small edit that looks safe and is not. If the user approves one item, do that item and report it; do not carry the approval to the next.
