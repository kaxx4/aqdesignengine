# The marketing brain

What the weekly engine believes, so a person can argue with it and change it in one place.

## The one job
A Kolkata parent reaches the right teacher. A student reads the right paper. Every post is judged against whether it moves someone toward one of those two taps. Everything else is decoration.

## What it decides each week (all in `src/brain.mjs`, all deterministic)
1. **Season** from the calendar month (`brain/calendar.json`). Seasons tilt which tip themes win. They never create a claim. The calendar is an approximation: check board date sheets and Puja dates before relying on a specific day.
2. **Five slots** (`brain/pillars.json`): Mon papers, Tue tips, Wed trust, Thu teachers, Sat papers. One template per slot, so a week never repeats a layout.
3. **Copy** from a bank. An entry is eligible only if every fact it needs exists. It is scored by season fit, minus a penalty for being used in the last eight weeks (`brain/ledger.json`), plus a seeded tiebreak.
4. **Subject** featured by least recent use, so eight subjects rotate evenly instead of Maths forever.
5. **Accent** (orange, indigo, mint) rotates, never the same colour on consecutive posts.
6. **Caption, hashtags, alt text, post time** assembled from the chosen copy.

## What it refuses to do (`src/validate.mjs`, hard failures)
- Em or en dashes (site rule).
- Any digit that does not trace to a fact: a count, a free-question number, a paper's class or year.
- Social proof it cannot source: "thousands", "trusted by", "most popular", "everyone".
- Unprovable superlatives: "best teacher", "guaranteed", "100%".
- Sample figures outside `--dry`.
- Headlines over 40 characters, captions over 900, more than 8 hashtags.

## The truth ladder for numbers
Live query (`site_counts`) beats a recorded figure beats nothing. If a fact is missing, copy that needs it is skipped, not softened. A count is never rounded up.

## Design rules it follows (from VISUAL_LANGUAGE.md and DESIGN_SYSTEM.md)
Warm bone ground, never white. Saturated slabs at radius 32, punctuating the page. Subject colour comes from the eight-subject generator, copied exactly. Weight-400 plus weight-800 headline pair, tight tracking. Tilted overhanging stickers, one per card at most. Blob mascots in the site palette. At most two saturated fills per poster.

One deliberate deviation: type on a saturated subject colour uses whichever of ink or white measures higher, because white on the Science and Geography greens is 2.7:1 and fails even the large-text floor. The site's contract already made the same call for orange.

## How to teach it something
A weak post is a missing rule, not a one-off edit. Add the check to `validate.mjs` (copy) or the `gate()` in `render.mjs` (layout), prove it in `selftest.mjs`, then regenerate. New copy goes in `pillars.json`; the validator polices it.

## Decisions confirmed with the owner (2026-10-05)
- **Visual fidelity: loose.** The bento-board (tiles, blob characters, tall headline column, peeking eyes) is an occasional layout, one week in three on the Friday slot, not the house default. Stay inside Shikshaq tokens.
- **Caption voice: warm, plain, local.** Short, honest, says what happens next. No jokes that need an emoji to land.
- **Cadence:** three posts a week, Mon, Wed, Fri at 19:30 IST, planned on Sunday evening.
- **Delivery:** the routine posts the PNGs and captions into the session chat. Nothing is pushed to the Shikshaq repo and nothing is posted to Instagram automatically.

## Random variations (learned from the AQ engine)
`node vary.mjs --n 8 --seed 21` draws variations, and the weekly plan draws a style per post the same way. What was taken from AQ's `stylebank.pick` and `design.py`:
- **Educated random, not uniform.** Each style in `brain/style_bank.json` has a base weight, a judged mechanism and a written recipe. A style used in the last six weeks is drawn less often. A style built for one template is favoured on that template.
- **Every filter narrows and falls back.** An over-specified request relaxes one filter at a time and reports which, so a draw never returns nothing.
- **Seeded.** The same seed reproduces the same draw.
- **Hard brand rules beat the recipe.** Accent colour is semantic per pillar (papers indigo, teachers orange, tips mint), exactly like AQ's `accent_for(dept)`. Styles vary ground, CTA form, corner radius, mascot kit, mirroring, tile order and sticker tilt, never the accent, the palette family or the contrast floor.
- **Rejection, not hope.** `vary.mjs` renders every draw, runs the layout gate, and discards failures with the reason, instead of showing you a broken poster.
- **Matrix test.** `npm run test:render` renders every style on every template it allows (100 renders). It found a mint step card invisible on a mint-tinted page, which the default style never hits. Fix: tinted cards get a hairline ring whenever the ground is not bone.
- **Gates borrowed from AQ.** `INVISIBLE-FILL` (colour distance between a fill and what is painted behind it, ring or shadow exempt) came from `reconcile.invisible_fill`.

Add a style by appending to `style_bank.json` with a mechanism and recipe, then run `npm run test:render`.
