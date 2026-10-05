# Shikshaq weekly Instagram engine

Plans three posts for the week, renders them in the Shikshaq design language, runs every gate, and writes captions, alt text and post times. Lives apart from the app: its own `package.json`, never in the Vercel install path.

```bash
cd marketing && npm install
node run-week.mjs --dry                 # simulate this week on SAMPLE facts, nothing written to the ledger
node run-week.mjs --dry --week 2026-W41 # pin a week
node src/fetch-facts.mjs                # live facts (needs VITE_SUPABASE_URL + key in the environment)
node run-week.mjs --commit              # live week; records it in the ledger so next week rotates
npm test                                # self-test
```

Output lands in `out/<week>/`: three 1080x1350 PNGs, `_week.png` (the feed-grid contact sheet), `week.md` (captions, alt text, times) and `plan.json`.

## Gates
**Copy gate (before drawing):** dashes, untraceable numbers, social proof, superlatives, length caps, sample facts outside `--dry`.
**Layout gate (on the rendered DOM):** clipped text, margins, WCAG contrast measured per element, text-on-text collisions, artwork landing on text.
**Looking gate:** a person (or the routine's Claude session) opens `_week.png` and each PNG. The numeric gates passed posters that were visibly wrong during this build; do not skip it.

## Status
- Dry run: working end to end. `npm test` (29 assertions) and `npm run test:render` (100 style x template renders) pass.
- `fetch-facts.mjs`: written, **not yet run against production** (the build sandbox cannot reach Supabase). The first live run is its test.
- Not yet decided: where finished posts are delivered for approval, the schedule, and who approves. See the open questions in the hand-off message.
- Instagram posting is deliberately not automated. The engine produces a reviewable folder.

See `brain/BRAIN.md` for what the engine decides and refuses.

## Variations
`node vary.mjs --n 8 --seed 21` renders random variations in the Shikshaq style and writes `out/vary-<seed>/` with a contact sheet and a brief per poster. Options: `--template`, `--energy calm|bold|playful`. See `brain/BRAIN.md`.
