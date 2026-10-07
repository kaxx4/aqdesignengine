# Campaign: "Shikshaq is where you find your tutor"

The whole four-week campaign as code. Every asset is a spec in `catalog3a.mjs` and `catalog3b.mjs` rendered by the panel-stack engine in `stack.mjs`, gated on the
DOM it actually drew. Nothing is hand-edited. A weak asset is a missing rule: fix the look or the gate, then rebuild.

```
npm run campaign              build everything (about two minutes): 240 images, sheets, phone and WhatsApp previews, all text
npm run campaign -- --family=faq          one family      (--only=FQ1,FQ2 for named assets)
npm run campaign:test         36 assertions, each one a failure this build actually hit
npm run campaign:wire         pull the Supabase export into the gated slots (see below)
npm run campaign:final        refuses to finish while any slot still holds placeholder data
npm run lookbook              one sample of every look on every canvas
```

Output is `out/campaign-what-is-shikshaq/` (git-ignored): one folder per family, `_sheets/` contact sheets, `_phones/` story frames with the
story chrome drawn over them, `wa-preview/` each WhatsApp push as a chat, `texts/` (schedule, captions with alt text, WhatsApp pushes,
volunteer answers, reel scripts) and `manifest.json` (every asset, its post, audience and status).

## Wiring the data (tomorrow)
1. Run the queries in `queries.sql` against the Shikshaq project (read-only) and save each result as JSON in `campaign/import/`.
2. Put the approved tutors in `import/tutors.json`: `[{"name","subject","quote","photo","approved":true}]`. A tutor with `approved` false stays a DRAFT.
3. `npm run campaign:wire`, then `npm run campaign:final`.

Until then the 21 gated assets (reviews, Meet a tutor, the Reviews cover) render with a red DRAFT band and the build will not call them final.
`data.json` holds real people's words and is git-ignored; `data.template.json` is the committed placeholder. Reviews are quoted exactly and carry their
source id. By default the reviewer shows as an initial (`--attribution=first` to show a first name) because the authors are school students.

## What each part owns
| File | Owns |
|---|---|
| `catalog3a.mjs`, `catalog3b.mjs`, `catalog.mjs` | every visible word, every asset (240), its family, post and audience |
| `stack.mjs`, `kit3.mjs`, `wsticker.mjs`, `looks.mjs` | the panel-stack engine (23 panel types), the icon and mascot kit, the WhatsApp sticker look. They hold no copy |
| `characters.mjs`, `looks-core.mjs` | the site's blob family plus the sun and X-lobe shapes; canvas geometry |
| `validate-campaign.mjs` | the copy gate: no dash, no digit without a fact, no "connects families", no "verified", the charity rule |
| `renderer.mjs` + `../src/render.mjs` | one browser, the DOM gate, and the story safe zone (top 250, bottom 340) |
| `plan.mjs`, `wa.mjs`, `captions.mjs` | the four-week calendar, the 30 WhatsApp pushes with their replies, the captions |
| `resolve.mjs`, `wire-data.mjs`, `queries.sql` | data binding. Missing data becomes a visible draft, never invented copy |

The shared engine change this build needed: `src/render.mjs` exports `gate()` and now takes a story safe zone, and its CLIPPED-Y tolerance scales with font
size (tight display leading overflows its line box by design). `src/kit.mjs`'s fit script got the same proportional tolerance.
