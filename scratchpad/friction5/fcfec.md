# Friction log — cfec9bd415fff2 (flat-lay cutting-mat desk scene)

Final: `out/versions/cfec9bd415fff2/v10.png`, script `scratchpad/gen_cfec9bd_v4.py`,
canvas `li_square` (1080x1080). **Score 0.158** (accept line 0.16), 7 iterations
(v4-v10; v1-v3 pre-existing from session 8, orphaned script). No BLOCKING critique.
Looking gate passed against the full Sample-37 inventory (already in
`brain/RECREATION_AUDIT.md`) — presence, relative size, and arrangement all checked,
not just presence. Honest verdict: a real, clean convergence, not a score-chased one —
the last fix (see below) was a genuine bug, found by looking at the render next to the
reference and refusing to trust the metric's own explanation for the gap.

## Top 3 friction points

1. **The queue's own state was actively misleading, and nothing detects that.**
   `RECREATION_QUEUE.json` had this slug at `score: 0.27, iters: 2, note: "showcase5f;
   small-text rule validated - detail 0.88-1.29 all five"`. That note describes
   `scratchpad/gen_showcase5f.py`'s `flat_lay()` function — a generic "kit checklist"
   card (headline "what to bring", a gear/mug/tag/pen/AQ sticker row) that renders to
   `out/showcase5/27_flat_lay.png` and has nothing to do with this reference's actual
   cutting-mat desk scene. `out/versions/cfec9bd415fff2/v1-v3.png` (the ACTUAL
   recreation, matching `brain/RECREATION_AUDIT.md`'s `## Sample 37` inventory almost
   exactly) were last modified July 14-15, untouched since. The 0.27 in the queue was,
   as far as I can tell, computed against the wrong file entirely — the showcase
   script's comment header just happens to say `27 cfec9bd415  flat-lay tableau` (it's
   item #27 in a batch of 44 archetype demos, numbered to loosely match the queue, not
   an actual recreation attempt). Nothing in `runqueue.py` or the queue schema records
   WHICH FILE a score came from, so this is silently unfalsifiable from the JSON alone
   — I only caught it because the note's content ("small-text rule", "detail 0.88-1.29
   all five") didn't match anything about a desk scene, and `git log`/file mtimes
   confirmed `out/versions/cfec9bd415fff2/` predates the queue's 2026-09-19 `init`.
   **Suggested fix**: `record()` should take (or auto-derive) the actual PNG path it
   scored and store it in the entry, so a future session can sanity-check a suspicious
   note against the file instead of re-deriving provenance from mtimes and prose.

2. **A systematic double-offset bug survived 6 iterations because the region-critique
   decision table has no row for "your coordinates are wrong."** Every one of this
   script's 11 placed elements had `MAT_Y0` added twice: once inside the `loc()`
   helper (which already returns an absolute canvas position — `MAT_Y0 + fy0*MAT_H`),
   and again at every call site (`at(x, MAT_Y0 + y, ...)`). X-coordinates were correct
   (`loc()`'s x output used directly, no re-add) — only Y was wrong, and identically
   wrong on all 11 elements, which is exactly what made it invisible: everything
   shifted down together by a constant 138px, so relative spacing, collisions, and
   containment all still looked "clean." `compare.report`'s region critiques (v4
   through v9) kept pointing at over-filled cells near the bottom and under-filled
   ones near the top, and RECREATION_PROTOCOL's decision table says to treat that as
   scale/position/shape problems on individual elements — which sent me tuning
   padding, rotation, notch size, and cluster spacing for 6 iterations (v4->v9,
   0.282->0.183) when the actual bug was a single copy-pasted `MAT_Y0 +` prefix. I
   only found it by grepping my own script for the pattern after a v9 crop
   (`compare.crop`) showed the yellow triangle hanging off the mat's bottom-right edge
   into open background — a symptom specific enough that "everything is 138px too low"
   was the only explanation that fit. **This is a real gap in the protocol**: the
   decision table (CLAUDE.md's own §7/RECREATION_PROTOCOL's table) has no branch for
   "the region deltas are a coherent constant-offset pattern, not a size/shape/count
   problem" — worth adding a row like *"multiple region critiques on the SAME side of
   the composition, at roughly the SAME magnitude, across otherwise-unrelated
   elements -> suspect a shared coordinate bug before touching any individual
   element."*

3. **The top-3-line critique in `compare.report` hid the real pattern; only the full
   grid diff explained it.** v6 and v7 both got "row10/11, col1/9" over-fill critiques
   and I fixed the wrong mechanism twice (padding, then rotation) because the printed
   critique only shows the 3 worst cells, not the shape of the error. Calling
   `compare._grid_occupancy` directly on both images (undocumented — I found it by
   reading `engine/compare.py`, not from any doc) showed the reference's entire left
   column runs LOWER than mine at a near-constant ~0.2-0.25 offset through the middle
   of the mat, and specifically COLLAPSES near the bottom-left corner (ref 0.11 vs
   mine 0.57-0.61) — i.e. the reference's bottom-left corner is SPARSE/OPEN, not
   padded-wide-with-orange the way I'd built it. That's the opposite mental model from
   what the top-3 critique text ("REGION OVER-filled... you have X") suggests on its
   own, since "over-filled" reads as "you have too much stuff," not "your shape is
   fundamentally backwards at this corner." I'd suggest `compare.report`'s docstring
   (or RECREATION_PROTOCOL) point at `_grid_occupancy` explicitly as a step-4b
   diagnostic before iterating on a stubborn region critique — it exists, it's the
   right tool, and nothing surfaces it.

## Where docs were wrong / stale / ambiguous

- **CLAUDE.md §5 step 0's canvas assumption is implicit and wrong for this slug.**
  Nothing in §5 or RECREATION_PROTOCOL.md tells you to check the reference's *aspect
  ratio* against the canvas before building — Workflow B's template (§6) hardcodes
  `W, H = core.SIZES["feed"]` with no caveat. `compare.report` DOES catch this (the
  `ASPECT MISMATCH` warning), but only *after* you've already built and rendered on
  the wrong canvas. Step 0 (`compare.geometry`) doesn't print the reference's raw
  pixel aspect at all, only fractional bbox/margins — I had to separately open the
  file in PIL to get `(1000, 750)`. Suggest `compare.geometry` print the source
  image's raw `(W, H)` and flag if it's >25% off every `core.SIZES` entry, mirroring
  the aspect-gap warning `compare.compare()` already has for two RENDERED images.
- **The style bank's `canvas: 'linkedin'` field was a load-bearing fact nothing
  pointed me to.** I only found it by manually inspecting `STYLE_BANK.json` for this
  slug on a hunch after the aspect-mismatch warning. RECREATION_PROTOCOL.md's step 0
  says to run `compare.geometry` but never mentions cross-checking `STYLE_BANK.json`
  for a `kind`/`canvas` hint, even though `stylebank.py`'s own `MEASURED_SCOPE`/
  `canvas_shift` machinery (CLAUDE.md §10's table) exists for exactly this. Worth a
  one-line addition to RECREATION_PROTOCOL step 0: "also check
  `STYLE_BANK.json[slug]['canvas']` — if it's not `feed`/absent, don't default to
  `feed`."
- **RECREATION_AUDIT.md's existing `## Sample 37` entry says "DONE (v3, 2
  iterations)"** and `RECREATION_PROGRESS.md` row 37 says `revisit-done` — both
  written before `compare.py`/the aspect-mismatch check existed, both now
  contradicted by `compare.report` scoring v3 at 0.664 (mostly aspect distortion, but
  even accounting for that, v3 was never actually measured against anything). Neither
  doc has a mechanism for "this was marked done under an older, weaker gate, and needs
  re-verification under the new one" other than a human/agent noticing by hand. This
  is the second time in the same file family I've now seen "done" not mean "still
  passes the current gate" (the runqueue docstring documents an analogous problem for
  `in_progress` vs `attempted`).

## API surprises

- **`compare.report()` DOES print by default** (the RECREATION_PROTOCOL doc's own
  `## Sample N` notes elsewhere worried about this being silent — it isn't, in the
  current `engine/compare.py`; `echo=True` is the default). No issue here, just
  confirming for the next session since another agent's friction log apparently
  flagged the opposite at some point (`compare.report()`'s docstring change is
  mentioned in CLAUDE.md's bug catalog under `80cb7ed71a8cc9`).
- **`compare._grid_occupancy` is private (underscore) but is the single most useful
  diagnostic for a stuck region critique** — more useful than `compare.report`'s own
  printed critique lines, which only surface the top-3 deltas by magnitude and lose
  the pattern across the full 9x11 grid. It's not mentioned by name in
  RECREATION_PROTOCOL.md or CLAUDE.md §7c at all.
- **`layout.preflight`/`build.render`'s `collisions` list has no way to say "this pair
  overlaps by design and I know it."** I declared `containers=("mat",)` to silence the
  (correct, expected) collisions between the mat and everything sitting on it, but the
  reference deliberately has the note card overlapping the pencil, the mug edging the
  eraser, and the eraser edging the red circle — none of which are container
  relationships (nothing "holds" the other), so every one of them still prints in the
  `collisions` advisory list on every render, 15 lines of it, identically, every
  iteration. `collision_ignore`/`ignore_pairs` would silence these one at a time, but
  for a genuinely-overlapping "pile" composition (which CLAUDE.md's own bug catalog
  says is a real, intended AQ mechanism — "reference piles overlap, the engine's
  instinct to separate is wrong here") there's no single declaration like
  `allow_occlusion=True` for "this whole composition is a pile, stop treating overlap
  as suspect." I ended up just reading past the same 15-line block every render.
- **The mat's own `clip-path` notch fix (v8) had no engine primitive to reach for.**
  CLAUDE.md's shapes/doodles vocabulary (scallop, arch, wave_banner, blob, starburst,
  gear, capsule, shield, tag, ribbon) has nothing for "a rectangle with 2 opposite
  corners cut on a diagonal" — I wrote a raw CSS `clip-path: polygon(...)` by hand.
  Given how common a "peeking second layer" motif seems to be in this corpus (this is
  at least the 2nd-3rd reference using it, per CLAUDE.md's own recipe language: "a
  second mat colour peeking out from behind one edge for depth"), a
  `shapes.corner_notch(w, h, notch)` or similar returning the clip-path string might
  be worth promoting out of one-off scripts.
- **`B.render()`'s auto-run static gate reports `CLIPPED div: width 1064px inside a
  1058px box`** on every single iteration from v4 onward, unchanged by any of my
  edits to the actual layout. I never tracked down which specific div this refers to
  (the message doesn't name the element/label), and since the rendered PNG never
  showed clipped text anywhere I could see, I could not tell whether this is a real
  bug in my HTML (something with `box-sizing` off by the border width, per CLAUDE.md's
  own bug catalog row about `border-box` eating declared width) or an artifact of
  `core.LOGO`'s wordmark image / `B.page()`'s own chrome. Would help if this warning
  named the element the way every other check in the gate stack does.

## Where score and eye disagreed

- **v9 -> v10, score moved 0.183 -> 0.158 (14% relative improvement) from a fix that
  is invisible in a quick glance at the two renders side by side** — both look like
  "the same composition, slightly shifted." The eye alone would likely have rated v9
  as "done, ship it" (nothing overlaps badly, nothing is unreadable, no dead
  quadrant) — it took the SCORE'S insistence that something was still off, plus one
  targeted crop of the one place a rotated/rotated-past-its-container element (the
  yellow triangle) made the systematic offset externally visible, to catch a bug that
  the looking gate on its own would have missed for an 11th iteration. This is the
  inverse of the usual worry in this codebase (score passing while the eye catches a
  real miss) — here the score was right and more sensitive than a casual look.
- **Conversely, the residual `row10/11 col1/9` delta (0.41, reference 0.09) that
  remains in the ACCEPTED v10** looks like nothing at all by eye — cropping that exact
  cell shows a thin, plausible orange sliver at the mat's bottom-left corner, not
  visibly "wrong." I believe this residual is a genuine but minor geometry mismatch
  (my diagonal notch is a straight cut; the reference's corner may be a slightly
  different curve/taper) rather than a missing element, and chasing it further past
  the 0.16 accept line looked like exactly the "diminishing-returns, tune one more
  parameter" trap CLAUDE.md warns about (§1: "taste is a committed cascade of
  intentional decisions... not accumulation").

## Which §7 checks were used, and how each was found

- `compare.geometry` (step 0) — found via RECREATION_PROTOCOL.md directly, used as
  instructed.
- `compare.report` (wraps `compare.compare`) — found via RECREATION_PROTOCOL.md,
  used every iteration.
- `compare.crop` — found via RECREATION_PROTOCOL.md's MOCKUPS section and CLAUDE.md
  §7c; used repeatedly (8+ calls) for side-by-side corner/region diagnosis — this was
  the single most useful tool in this whole session, more than the numeric score
  itself for deciding WHAT to change.
- `compare._grid_occupancy` — **found only by reading `engine/compare.py` source**,
  not documented anywhere in CLAUDE.md or RECREATION_PROTOCOL.md by name. This is the
  biggest doc gap of the session (see friction point 3 above).
- `layout.preflight` / `build.render(..., elements=, color_pairs=, text_pairs=,
  containers=, page_bg=, expect_hero=)` — found via CLAUDE.md §6's template, used as
  documented. `containers=("mat",)` matches §7a's description exactly.
- `bounds_check`, `collision_check`, `css_var_check`, `img_src_check`,
  `double_rotation_scan` — all auto-run through `preflight`/`render`, never called by
  hand; matches CLAUDE.md's claim that `render(..., elements=...)` is "the whole
  gate."
- `reconcile.measure_dom` / `reconcile_boxes` — auto-run, surfaced the
  `BBOX UNDER-REPORTS` and `UNTRACKED` advisories; read about these in CLAUDE.md §7b,
  did not need to call directly.
- Did **not** use: `dominance_check` (no single hero — the note card is the largest
  element but the composition is a pile, not `expect_hero`-shaped), `reading_order`
  (no split sentence in this piece), `cascade_stacks` (no repeated-card deck),
  `scatter_solve` (positions came from measured reference fractions, not a solver —
  matches the documented scope note that `scatter_solve` is for AUTHORING, not
  recreation).

## Iteration times / what had to be guessed

- Each `python scratchpad/gen_cfec9bd_v4.py` run (render + full preflight +
  `reconcile_boxes`) took roughly 2-4 seconds wall-clock — consistent with CLAUDE.md's
  claim of ~1.9s/poster in a session, plus my script's own SVG-heavy HTML generation.
  `compare.report` calls were near-instant (<1s). The actual time cost of this task
  was almost entirely spent on: (a) reading crops and reasoning about geometry by eye
  between iterations, and (b) the ~30-40 minutes lost to the double-Y-offset bug
  across v4-v9 before I thought to grep my own source for the pattern.
- **Had to guess**: the reference's exact mat pixel bbox (`x60-930,y60-680`) — this
  came from the PRE-EXISTING `## Sample 37` audit text (itself described as
  "approximate," ~x60-930 not exact pixels), not from a fresh measurement. I did not
  re-derive this from scratch since the existing inventory was already thorough and
  matched what I saw on re-reading the reference image directly.
- **Had to guess**: the exact geometry of the reference's double-layer "peek"
  mechanism (rotation vs. notch vs. simple offset) — this took 4 of the 7 iterations
  (v4, v5-v7 rotation attempts, v8 notch fix) to reverse-engineer correctly from the
  grid-occupancy data rather than from a stated rule anywhere. Nothing in CLAUDE.md's
  vocabulary section names this mechanism, despite it recurring across the corpus per
  the style bank's own recipe text ("a second mat colour peeking out from behind one
  edge for depth").
- **Did not need to guess** (measured directly via PIL, not eyeballed): mat green
  color (`(34,129,89)`, matched to `core.ACCENTS[1]` mint almost exactly), background
  navy (`~(66,88,146)`), orange under-layer/mug color
  (`(239,91,61)`, matched to `core.ACCENTS[3]` tomato).
