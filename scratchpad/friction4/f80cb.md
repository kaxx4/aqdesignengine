# Friction report — recreating 80cb7ed71a8cc9 ("A WORLD OF PURE IMAGINATION.")

Slug `80cb7ed71a8cc9`, judged canvas `linkedin` (1200x628). Final: `v5`, score 0.243,
5 real iterations (+1 discarded regression, v6). Full write-up in
`brain/RECREATION_AUDIT.md` under `## 80cb7ed71a8cc9`. Scripts + PNGs for every
version preserved in `out/versions/80cb7ed71a8cc9/`.

## Verdict up front

Looking gate: PASSED cleanly. Every element in the step-1 inventory (cream ground, the
full-bleed wavy ribbon, the red sparkle-with-face, the yellow flower, the 3-line headline,
the Portuguese subhead) is present, correctly proportioned, non-colliding, non-invisible.
Score: 0.243, above the 0.16 accept line. I recorded it honestly as `attempted` (not
`done`) via `runqueue.py record`, not `fail` — this is a real poster, not a mockup, and I
do not believe the gap is a real content miss (see below). This is exactly the kind of
score-vs-eye disagreement CLAUDE.md §12 already documents in the other direction (77e7bb34
scored 0.147, inside the gate, while a whole line of copy was sliced off) — here the eye
says match, the number says not-quite, and I'm reporting both rather than picking one.

## CLAUDE.md / RECREATION_PROTOCOL — wrong, stale, ambiguous, or missing a step

1. **§6's template line "5 waypoints read off the reference" doesn't exist as a technique
   at all — there is no ribbon/snake/wavy-band entry in `shapes.SILHOUETTES`.** For a
   reference whose dominant element is a long flowing multi-bend band (not a badge/sticker),
   neither `doodles.py`'s 20 fixed stamps nor `shapes.py`'s 9 parametric silhouettes apply.
   I had to hand-write a Catmull-Rom-through-waypoints path generator from scratch inside
   the bespoke script. This is a real, recurring gap: any reference with a ribbon, river,
   cable, or snake motif (a plausible category — this corpus already has one) hits the same
   wall. Worth a `shapes.py` addition (e.g. `wavy_stroke(waypoints, width)`), since the
   Catmull-Rom-to-bezier math is generic and I'd be surprised if this is the only poster
   that needs it.
2. **RECREATION_PROTOCOL.md's decision table has no entry for "the reference's shape family
   itself is more complex than a smooth curve."** My v2-v4 iterations plateaued at
   score 0.246-0.256 because a sparse waypoint list, no matter how precisely each point was
   pixel-measured, gets smoothed by Catmull-Rom into a shallow diagonal — it structurally
   cannot produce the reference's actual geometry (a quarter-turn into a flat run, then a
   TIGHT ~180-degree hook). None of the table's rows (`DETAIL TOO LOW`, `TOO DISPERSED`,
   `REGION UNDER/OVER-filled`) name this failure mode; `REGION under/over-filled`'s
   prescribed action ("an element from your inventory is missing or too small there... only
   add filler as a last resort") sent me looking for a MISSING ELEMENT for two iterations
   before I zoomed into the actual pixels and found it was a WRONG CURVE SHAPE on an
   already-present element. A row like "your shape's curvature doesn't match the
   reference's — zoom into a crop of just that element before adjusting coordinates" would
   have saved real iterations.
3. **Step 0's `compare.geometry` is silent about aspect.** The reference is 1199x675
   (1.776:1); the judged canvas is `linkedin` 1200x628 (1.911:1) — a real, if small,
   mismatch the task brief didn't flag and `compare.geometry` doesn't either (it just
   reports fractions against whatever image you hand it). I worked through whether this
   mismatch was distorting the score (see `compare.py` section below) — it turned out to be
   a smaller effect than I first suspected, but the manual only prints its aspect-mismatch
   warning inside `compare()` itself, not at the `compare.geometry()` step-0 stage, so I had
   to discover the discrepancy by hand rather than being told about it before I started
   building.
4. **§6's template still says "M=64" as if it's universal; this canvas has almost no
   established margin convention** (feed/story have ~10 recreated posters using M=64;
   linkedin has essentially none in this corpus yet). Not wrong, just worth flagging that
   the convention is being extrapolated from a different aspect ratio, not verified for
   this one.

## APIs that surprised me

1. **`compare.report()` returns a string, it does not print one**, despite
   RECREATION_PROTOCOL.md's own usage line: `python -c "...compare.report(ref, gen)"` reads
   like a print statement and produces silent, empty output. `compare.compare()` (the dict
   form) is likewise silent. You have to know to wrap it in `print(...)`. Cost me one dead
   command before I noticed.
2. **`layout.preflight`'s `collision_ignore` and `render()`'s DOM-level `audit.audit`
   ignore-pairs are two unrelated namespaces that both read from the SAME parameter.**
   `layout.collision_check` matches your tuple LABELS; `audit.audit` (invoked inside
   `render()`) matches DOM `data-tag` attributes on elements carrying `class="measure"`.
   My `ribbon`/`star`/`flower` SVGs have `data-tag` but not `class="measure"` (added
   deliberately — see next point), so every render printed:
   `IGNORE PAIRS NAME NO data-tag IN THE DOM: ['flower', 'ribbon', 'star'] — this gate
   matches data-tag, while layout.collision_check matches your element LABELS.` on every
   single run, forever, even after everything else was clean. It's diagnosed as
   informational rather than a failure, but it's permanent noise for any build that (like
   mine) intentionally excludes some elements from the DOM-level margin/overlap gate. The
   code comment at `engine/audit.py:58-65` says this confusion has already been "found by
   reading this source" by a previous agent (session 10f, agent c3) — it recurred for me
   independently, which suggests the fix belongs in the tool (e.g. accept ignore-pairs by
   either label or data-tag, or only warn once) rather than in tribal knowledge.
3. **`audit.py`'s `MARGIN_OK`/`BLEED` tag whitelist is a closed, hardcoded vocabulary**
   (`{"num"}` and `{"note","key","flyer","we","won","tb","title","body"}`) that a bespoke
   script cannot extend for the margin check specifically — `render()`'s own `bleed_tags`
   parameter only reaches `reconcile.measure_dom`'s off-canvas check, not `audit.audit`'s
   margin check. My ribbon legitimately bleeds off all four edges by design (per the
   reference itself, confirmed by `compare.geometry`'s content bbox), and my star sits
   deliberately close to the top edge. The only way to avoid a wall of false "MARGIN
   breaches safe area" warnings was to NOT give those three elements `class="measure"` at
   all — which means they also don't get `audit.audit`'s overlap check, a real reduction in
   gate coverage that a bespoke script has no clean way around. (I still ran full coverage
   on them through `layout.preflight`'s tuple-based `bounds_check`/`collision_check`, which
   IS extensible via `bleed_tags`/`collision_ignore` — so nothing went unchecked, but two
   different gates in the same call ended up covering different subsets of elements for a
   reason that has nothing to do with the elements themselves.)
4. **A redundant same-color background div is flagged as a bug, not a no-op.**
   `B.page(W,H,bg,inner)` already paints `.p{background:bg}`; adding
   `<div style="position:absolute;inset:0;background:var(--bg)">` on top of it (copied out
   of habit from an earlier template) is completely harmless — but
   `reconcile.measure_dom`'s `invisible_fill` scan (auto-run inside `render()`) correctly
   reports it: `its background rgb(244, 239, 224) is the same as the 'p' painted directly
   behind it ... the shape is drawn and cannot be seen`. Technically true, technically
   useless as a warning (nothing WAS hidden — the div contributes nothing whether it's
   there or not), and it reads exactly like the genuine "invisible badge" bug class this
   check exists to catch. Removed the div rather than chase it; worth noting since the
   fastest way to "clean" the render() log for a first-time bespoke author is to just not
   copy that line from old scripts, which the current §6 template does not point out.
5. **`compare.py`'s analysis frame is a hardcoded 4:5 portrait, `SIZE = (540, 675)`,
   regardless of the actual judged canvas.** Both the reference and every render get
   resized (non-uniformly, aspect-distorting) into this fixed frame before any metric is
   computed. I initially suspected this was the main cause of my plateaued score, since my
   render (1200x628, 1.911:1) and the reference (1199x675, 1.776:1) get stretched
   differently (mine +7.5% vertically, the reference 0%) on the way into that frame. On
   closer analysis this turned out to be mostly harmless AS LONG AS you scale your
   composition from source-fraction (as `compare.geometry` reports it) rather than from
   raw source pixels — which the recreation protocol already tells you to do — because the
   two resize factors cancel out for anything placed by fraction. But it took real
   dead-end investigation time to work that out, and it is a genuine sharp edge for anyone
   scoring a non-4:5 canvas (`linkedin`, `story`, `li_square` are all valid `core.SIZES`)
   who places even one element by an absolute pixel guess instead of a measured fraction.
6. **`compare._match_palette`'s greedy, non-reusable 1:1 matching produces a
   deterministic false-positive `MISSING COLOUR` on ink black whenever the reference is a
   JPEG.** Diagnosed exactly (numbers in `brain/RECREATION_AUDIT.md`): the reference's
   compression noise splits one visual black into two adjacent 32-wide quantization
   buckets (`(32,0,0)@11.1%` and `(0,0,0)@5.4%`); my clean SVG/CSS render produces one
   consolidated bucket (`(0,0,0)@18.4%`). The reference's MORE common near-black bucket is
   processed first (palettes are matched in `Counter.most_common()` order) and claims my
   only near-black candidate, leaving the reference's LESS common near-black bucket
   unmatched — even though the render plainly has more total near-black ink than the
   reference does. This fired identically on every one of my 6 versions regardless of any
   content change, which is itself a signal it's a matching artifact, not a per-version
   content signal. A JPEG reference with any solid dark colour will hit this.

## Score vs. eye

- **v1 -> v2**: score 0.391 -> 0.246 (eye agreed: v1's ribbon path was visibly, obviously
  too far right; v2 looked like the reference).
- **v2 -> v3 -> v4**: score 0.246 -> 0.251 -> 0.256, essentially flat/slightly worse, while
  the eye kept reading the ribbon shape as progressively "more correct" (v4 in particular
  fixed `area_ratio` to a near-perfect 1.007 for zero score benefit and one real
  regression). This is the clearest disagreement in this run: three iterations of genuine,
  measured, defensible improvement produced no score movement, because the actual defect
  (wrong CURVE FAMILY — a rounded hook approximated as a diagonal) wasn't something any of
  those three iterations addressed; they were all still perfecting the wrong curve.
- **v5**: score 0.243 (best), and by eye a substantially better match than v3/v4 — the
  ribbon now has a real hook, not a smoothed diagonal. The score moved far less than the
  visual improvement warranted, which is the coarse-grid sensitivity described above: a
  108px-wide element threading a 9x11 grid produces large fractional deltas for what are,
  by eye, small positional differences, because a whole grid cell (133x57px canvas-space)
  can flip between ~0 and ~1 coverage depending on whether the ribbon's centerline happens
  to cross it, independent of how faithful the overall shape is.
- **v6**: score 0.335 (worse), and by eye ALSO worse (the hook visibly clipped into the
  top-right corner and a lower band disappeared) — score and eye agreed here, which is
  useful confirmation that the metric isn't simply noise; it tracks real regressions, just
  compresses real improvements into very little dynamic range for this particular shape
  family.
- **Every version**: `MISSING COLOUR dark/ink` printed identically regardless of visible
  ink coverage (see above) — score disagreed with the eye in a way I could fully explain
  and attribute to the tool, not the render.

## §7 gate-stack usage

Used, and confirmed working as documented:
- `layout.bounds_check` / `collision_check` (via `preflight`) — caught the real
  star/headline collision on v1 before any render.
- `layout.invisible_color_check` (via `preflight`'s `color_pairs`) — ran clean every time
  (ink/tomato/lemon/grape all sufficiently different from cream); never fired, so I can't
  confirm it would catch a real defect on this build, only that it didn't false-positive.
- `layout.css_var_check` (auto, via `render()`) — never fired; all `var(--...)` refs
  resolved.
- `layout.dominance_check` (opt-in, `expect_hero=True`) — passed; the ribbon's bbox clears
  `min_hero_frac`.
- `reconcile.measure_dom` (auto in `render()`) — this is what caught the redundant
  background div (`invisible_fill`) and would have caught clipped/spilling text had my
  `measure_text()`-derived boxes been wrong; they weren't, so no clipped/spilling ever
  printed.
- `reconcile.reconcile_boxes` (auto when `elements=` passed to `render()`) — never printed
  anything, meaning my hand-computed ribbon bbox (via a 400-sample-per-segment numeric
  bezier walk, since the shape isn't a rectangle) matched what the browser actually drew,
  closely enough not to trip `under_reported`/`untracked`.
- `audit.audit` (DOM margin/overlap, inside `render()`) — ran, but only checked
  `headline_l1..3` and `subhead` (the only elements I gave `class="measure"`; see API
  friction #3 above for why the ribbon/star/flower were deliberately excluded from it).

Found only by reading source, not by CLAUDE.md/RECREATION_PROTOCOL:
- That `audit.audit`'s DOM-level gate requires `class="measure"`, separate from
  `data-tag` — CLAUDE.md's §6 template and §7b's description don't mention this
  requirement; I found it by reading `engine/audit.py`'s `_BOXES_JS`/`_NEST_JS` selectors
  (`.measure`) after wondering why my ignore-pairs warning kept firing.
- That `MARGIN_OK`/`BLEED` in `audit.py` are closed, hardcoded sets with no
  per-call extension point (unlike `reconcile.measure_dom`'s `bleed_tags`, which IS a
  parameter). Found by reading the module top, not documented in §7b.
- `compare.py`'s `SIZE = (540, 675)` hardcoded analysis frame — not mentioned anywhere in
  §7c's description of `compare.py`; found by reading `_load()` after suspecting an
  aspect-related score artifact.
- That `_palette`'s bucketing (`// 32 * 32`) plus `_match_palette`'s greedy, non-reusable
  matching can double-count/miss a single visual color split across JPEG noise — found by
  directly calling `compare._palette()` on both images and comparing the bucket lists by
  hand; nothing in §7c or RECREATION_PROTOCOL.md flags this as a known limitation the way
  the "flat-vector recreations read low on vdr" caveat already does for `ref_metrics`.

## Timing / what I had to guess

- Step 0 (`compare.geometry`) + reading the reference + writing the step-1 inventory:
  ~10 min, mostly manual crop-and-look (there is no automated element-enumeration tool;
  CLAUDE.md is explicit that this has to be done by eye, which is correct, but it is the
  single most time-consuming step for a 4-element-but-geometrically-complex poster).
- v1: ~12 min (build + 3 real gate-caught bugs fixed pre-render + first look + first
  score). v2: ~5 min (re-measure ribbon centerline from pixels). v3: ~4 min (denser
  waypoints, no visible/score benefit). v4: ~3 min (false lead, reverted). v5: ~8 min
  (zoomed crops, rebuilt hook geometry — the one iteration that needed genuine new
  investigation rather than parameter tweaking). v6: ~3 min (regression, discarded).
  Total: ~45 min build/iterate + ~10 min step-0/1 + this report.
- What I had to guess vs. measure: the ribbon's exact waypoints were PIXEL-SCANNED
  (`np.where` on a color-distance mask, not eyeballed) from v2 onward — this was the
  single highest-leverage thing I did, and the manual doesn't currently suggest it
  (CLAUDE.md/RECREATION_PROTOCOL's guidance is "measure bbox/margins/centroid via
  `compare.geometry`", which is necessary but not sufficient for a shape whose SILHOUETTE,
  not just its bounding box, is the thing being judged). The star/flower sizes and the
  headline's vertical anchor (relative to the star, not absolute) were measured via crop
  pixel bounds and `B.measure_text()` respectively — not guessed. The one thing I did NOT
  measure and can't verify without the original design file: the reference's exact
  swash-font used for "A WORLD / OF PURE / IMAGINATION." — substituted with AQ's own
  NeutralFace 900 per the real-assets/no-fabrication spirit, noted as an acceptable
  adaptation in `brain/RECREATION_AUDIT.md`.

## Top 3 friction points

1. **No engine primitive for a long flowing multi-bend ribbon/band** — every reference
   with this motif (there is at least one, this one) requires hand-rolling a Catmull-Rom
   path generator from scratch in the bespoke script, and a sparse/eyeballed waypoint list
   silently degrades into a "smoothed diagonal" that looks plausible but scores badly for
   reasons the decision table doesn't name (see #2 below).
2. **The decision table has no row for "your curve's SHAPE FAMILY is wrong" as distinct
   from "wrong scale/position/dispersion/missing element."** I spent 3 of my 6 iterations
   (v2-v4) treating a hook-vs-diagonal shape mismatch as a coordinate-precision problem
   before zooming into raw pixels revealed it was a category mismatch. `REGION
   under/over-filled`'s prescribed remedy ("check your inventory, add filler as last
   resort") actively pointed away from the real fix.
3. **Two unrelated ignore-pair/tag-whitelist systems (`layout.collision_check`'s label
   matching vs. `audit.audit`'s `class="measure"` + `data-tag` matching, plus `audit.py`'s
   closed `MARGIN_OK`/`BLEED` vocabulary) mean a bespoke script cannot get full,
   consistent gate coverage on elements that are BOTH intentionally bleeding/overlapping
   AND worth checking for real bugs** — you either accept permanent "ghost tag" warning
   noise, or drop those elements out of the DOM-level gate entirely. I chose the latter,
   which is defensible but means `audit.audit` covered 4 of my 7 elements, silently.
