# Friction report — e7b32bd307aac4 ("Intake/Production/Review/Delivery" workflow-pile)

Final: `out/versions/e7b32bd307aac4/v11.png`, score 0.253 (accept line 0.16), 11 iterations.
Looking gate PASSED (full 26-element inventory present, correctly proportioned, no
collisions/off-canvas/invisible fills). Not accepted in the strict score<=0.16 sense, not
parked (this is a real single-frame poster, genuinely scorable). Logged via
`runqueue.py record e7b32bd307aac4 0.253 11 "..."` — status came back `attempted`, `NOT YET
(keep iterating)`. Honest verdict below. Top-3 friction points are flagged inline with
**FRICTION** and summarized at the end.

## Docs: wrong, stale, ambiguous, or missing a step

1. **CLAUDE.md's own bespoke-script template (Sec6) omits `shapes` entirely from the
   `load(...)` calls**, but the very next line and half the template's own commentary
   (`shapes.sticker()`, `shapes.SILHOUETTES`) assume it's loaded. Every real example script I
   found on disk (`gen_110a5730_v4.py`, etc.) adds `shapes = load("shapes")` themselves. Minor,
   but a literal copy-paste of Sec6 as printed does not run.

2. **RECREATION_PROTOCOL.md's "THE LOOP" and CLAUDE.md §5 disagree on file naming for the
   description step.** §5 step 1 says write the description "under a `## Sample N` heading" in
   `RECREATION_AUDIT.md`; the actual file's recent history (session 10c onward) uses
   `## Sample <hash>` or bare `## <hash>` headings once the corpus moved past the original 44
   (matches what my task brief asked for: `## e7b32bd307aac4`). The numbered-sample convention
   is stale for anything in the 30-reference 2026-09-19 addition; nothing in CLAUDE.md or the
   protocol says so explicitly, you have to infer it from the file's own recent tail.

3. **CLAUDE.md's `compare.py` section (§7c) describes `compare.report`/`compare.compare` well,
   but never says `report()` RETURNS a string instead of printing one.** `compare.report(ref,
   gen)` silently produces no output unless you `print()` it yourself — I ran it once with no
   output at all and had to `inspect.getsource` it to find out why. This is a real footgun for
   exactly the Sonnet/Haiku-without-Opus-judgment audience RECREATION_PROTOCOL.md says it's
   designed for: a silent no-op reads as "it worked, nothing to report," not as "you forgot a
   print."

4. **Nowhere does either doc mention that `layout.invisible_color_check`'s hard-fail threshold
   (40 RGB-distance units, euclidean) is essentially unclearable for a "paper card barely
   distinct from the page" pattern** — which is exactly what THIS reference's hero card is
   (I measured the reference's own card fill within ~0 distance of its own background). I found
   this out empirically: pure white against `core.CREAM` is only 36.6 units away, so ANY
   plausible near-white "paper" card fails the gate. **FRICTION 1.** See "Genuine gate
   conflict" below — this isn't just a documentation gap, it's a real unresolved tension between
   two independently-justified rules.

5. **`layout.preflight`'s printed `[preflight] ISSUES:` output for `collisions` prints raw
   overlap-area tuples `(label_a, label_b, ov_w, ov_h)` with no units/legend inline** — you have
   to already know `collision_check`'s signature to know the last two numbers are the overlap's
   width/height in px, not e.g. a distance or a percentage. Not wrong, just terse enough that a
   first-time reader (the Sonnet/Haiku audience) will misinterpret it.

6. **CLAUDE.md's bug catalog (§10) documents `reconcile.measure_dom`'s OVERSIZE-suppression
   fix as resolved, but I never actually exercised reconcile.py's hard checks directly** — I
   only saw its output pass through `build.render()`'s own internal call. It would help §7b if
   it said explicitly that a bespoke-script author never calls `reconcile.measure_dom` by name;
   it's invisible plumbing inside `render()`, and the printed lines it produces (`clipped`,
   `spilling`, etc., none of which fired for me) look exactly like `preflight`'s own advisory
   lines with no visual distinction in the console output about which module emitted them.

## scatter_solve / resolve_label_z — usable, or not?

**`resolve_label_z`: genuinely usable, used for real, and it caught a real bug.** I built the
pile's z-order by hand (matching the reference's own visual depth ordering) and fed
`resolve_label_z` each object's (label, LABEL box, initial z). On v1-v5 it correctly reported
`bookphoto` as **unresolved** — its own top strip (the part I declared as its "label", i.e. the
part that must stay visible so the photo itself isn't fully swallowed) was buried under
Aa/Au and couldn't be fixed by raising z alone. That result was the exact signal that told me
the WHOLE lower cluster (book photo + Aa + Au + ribbed rect + Approved) needed to move down as
a group to open the "gap above the pile" the reference actually has — not something I would
have caught from `collision_check` (irrelevant here, overlap is the design) or from the score
critique (which never once mentioned this in its top-3 lines). Once I re-measured that
cluster's real position off the reference crop and moved it, `resolve_label_z` came back with
**zero unresolved** from v6 onward. That is the tool doing exactly its documented job.

**`scatter_solve`: evaluated, NOT used, and I don't think it could have been used here.**
It solves "find A legal layout" (random search against overlap/protect/keep-out constraints),
with no notion of a TARGET position. For Workflow B, the goal is to match a SPECIFIC
reference's arrangement — feeding it my 11 pile objects' sizes would have returned SOME
non-colliding-enough layout, but there is no way to bias it toward the reference's actual
composition beyond the crude `zones` parameter (which biases toward a region, not a point, and
is shared across all items in a call, not per-item). Using it here would have produced a
plausible-looking pile that does NOT match the reference — the opposite of what a recreation
needs. I hand-placed every pile object instead, using bboxes measured directly off
`compare.geometry`'s occupancy grid and, more usefully, off direct pixel crops of the reference
(`scratchpad/_ref_pile_full.png` etc.) when the fractional occupancy grid was too coarse to
resolve individual object edges. **This is worth stating plainly in RECREATION_PROTOCOL.md or
CLAUDE.md §10: `scatter_solve` is a Workflow-A/C authoring tool (compose a NEW pile), not a
Workflow-B recreation tool (reproduce a SPECIFIC pile).** The task brief's framing ("for a pile,
scatter_solve places against protected text and keep-out zones instead of hand-typed
coordinates") reads as if it should replace hand-placement in Workflow B, and it can't, for a
structural reason, not a skill-issue reason.

## APIs that surprised me

- `compare.report()` returns a string, doesn't print (see doc friction #3 above).
- `layout.rotated_bbox(x,y,w,h,deg)` — worked exactly as documented and caught a real bug on
  the first render: my swing tag's hand-padded bbox (`x-6,y-4,w+16,h+16`) still ran the rotated
  footprint 22px past the canvas edge (`off_canvas: [(7, 1006, 466, 196, 166)]`). Recomputing
  with `rotated_bbox` and choosing a position/size whose ROTATED box (not the CSS box) clears
  the canvas fixed it permanently. This is the one CLAUDE.md §10 catalog entry that fired on
  literally the first render, exactly as advertised.
- `layout.preflight`'s `collision_ignore` pairs are checked against the LABELS you pass in
  `elements` (`(label, x, y, w, h)` tuples), NOT against any `data-tag` in the HTML — but
  `render()`'s own separate audit pass prints `IGNORE PAIRS NAME NO data-tag IN THE DOM` for
  every one of my ignore-pair labels, on every single render, because I never bothered adding
  matching `data-tag="..."` attributes to most of my divs. This is advisory/harmless (my
  `elements` list already carries the labels `collision_check` needs), but the warning fires
  unconditionally and looks alarming the first time — CLAUDE.md doesn't mention that
  `collision_ignore` and `data-tag` are two SEPARATE label namespaces serving two DIFFERENT
  gates (`layout.collision_check` vs whatever DOM-tag-based check `render()` runs internally).
  **FRICTION 2.**
- `shapes.lighten(hex, frac)` is not documented in CLAUDE.md's brand-constants section at all
  (§9 lists `text_on`, `on_cream`, `ink_of`, `outline_of`, `hard_shadow`, `keyline` — no
  `lighten`); I found it by `dir(shapes)`. Small thing, but §9 claims to be the "source of
  truth" for the craft-scale helpers and this one is missing.
- `invisible_color_check`'s default `thresh=40` and `content_mask`'s default `tol=46` in
  `compare.py` are independently-chosen, undocumented-as-related constants that turn out to
  matter together for exactly the "near-invisible card" pattern (see below). Nothing in either
  file's docstring cross-references the other.

## Where the SCORE disagreed with my EYE (both directions, with numbers)

**Score said "fine", eye said "broken":** none in this session — every render that passed
`preflight` and looked wrong to me also scored worse than a fixed version, which is
reassuring. But see the next point, which is closer to "silent" than "wrong":

**Score was silent about a real defect (eye caught it, score never flagged it):** v1-v10 used
`core.PHOTOS['edu']` for the right-mid buttercup bleed panel. That photo carries a baked-in
caption ("CREATING MOMENTS ETCHED IN THEIR HEARTS FOREVER") in its own bottom band, which
rendered CLIPPED AND ILLEGIBLE across the bottom of the small triangular panel on v10.png —
plainly wrong to the eye, a real "text off its shape" legibility failure per CLAUDE.md §3.
`compare.compare()` never once flagged it across 10 renders; its critique list has no
"illegible text" or "unintended caption" axis, only occupancy/detail/palette. Fixing it (an
oversized top-anchored `background-size` crop, same fix already applied once to
`core.PHOTOS['food']` on the book-photo tile — I had literally already solved this exact bug
class earlier in the SAME session and still missed the second occurrence until a direct
visual look at v10.png) made the numeric score **worse** by 0.006 (0.247 -> 0.253), because it
slightly reduced the "content" pixel count in that grid cell, moving it further from the
reference's own (also-miscounted, since the reference doesn't have this exact defect) value
there. Kept the fix; it is unambiguously correct despite the score regression. **FRICTION 3 —
this is the single clearest evidence in the whole session that "do not accept on score alone"
is not a formality: a genuinely broken element (illegible baked-in text) can score BETTER than
the fixed version.**

**Score was noisy/inconsistent in a way that cost real iteration time:** individual grid-cell
fixes did not compose. Concretely:
- Widening the bottom-mid chair panel from 144x38 to 267x68 fixed `row 11/11 col 7/9`
  (0.58->~0) but the wider panel's extra area pushed the OVERALL score from 0.267 to 0.300 —
  net worse, because the extra area inflated `area_ratio` (1.193->1.281) more than the local
  fix helped. I had to revert to a narrower box (190x50) that fixed the SAME cell without the
  area penalty, purely by trial (three attempted sizes: 267x68 too big, 190x68 still worse
  than baseline once repositioned, 190x50 finally net-neutral-to-positive).
- Extending the ribbed-rect's height from 70 to 112px fixed `row 8/11 col 5/9`
  (delta 0.64 -> ~0) but pushed `row 8/11 col 6/9` from delta 0.09 to 0.82 (a WORSE new
  problem), because this build represents the ribbed rect as a plain rectangle while the
  reference's actual shape is a diagonal/tapered wedge — there is no single rectangular bbox
  that matches the reference's footprint in both columns at once. Net score: 0.247 (without
  the extension) vs 0.258 (with it) — reverted, logged as a named residual gap rather than
  chased further.
This is a real, reproducible limitation: `compare.py`'s 9x11 grid rewards LOCAL shape fidelity
that a rectangular clip-path fundamentally cannot deliver for organic reference shapes, and the
scalar SCORE aggregates cells in a way that doesn't guarantee "fix one cell, score improves" —
sometimes fixing the worst-reported cell makes the total worse. RECREATION_PROTOCOL.md's
decision table treats each critique line as an independent action item ("do exactly what it
says"); in practice for this reference, two of the top-3 critique lines were in direct tension
with each other and satisfying both was not possible with the axis-aligned-bbox tool this
build uses.

## Which §7 checks I used, and which I only found by reading source

**Used as documented, from CLAUDE.md alone:** `layout.preflight` (with `elements`, `html`,
`color_pairs`, `page_bg`, `expect_hero`, `collision_ignore`), `layout.resolve_label_z`,
`layout.rotated_bbox`, `compare.geometry`, `compare.compare`, `B.session()` +
`B.render(..., elements=, color_pairs=, page_bg=, expect_hero=, collision_ignore=)`.

**Found only by reading source / trial, not fully clear from the docs:**
- `compare.report()`'s return-not-print behavior (had to `inspect.getsource`).
- `layout.preflight`'s exact ADVISORY vs HARD-FAIL set — CLAUDE.md §7a lists each check's
  category prose-style scattered across many bullet points; I had to read `preflight`'s own
  source (`ADVISORY = {...}`) to get a single authoritative list, since the prose descriptions
  for `under_filled_quadrants`, `invisible_craft`, `faint_wash`, `double_rotation`,
  `cascade_hidden`, `occluded` are spread across 5 different catalog rows plus the function's
  own docstring, none of which cross-reference each other by name consistently.
- `invisible_color_check`'s exact distance formula and default threshold (had to read source
  to compute what fill values would clear the gate — CLAUDE.md just says "≈40" without units
  or formula, which I needed precisely to search for a passing colour).
- `content_mask`'s `tol=46` and its interaction with `invisible_color_check`'s `thresh=40`
  (the genuine gate conflict below) — found only by reading `compare.py`'s source after
  noticing the numbers were suspiciously close.

**Never fired, so I can't say whether they'd have caught something real:** `wash_scan`,
`invisible_craft_scan`, `double_rotation_scan`, `cascade_peek_check`, `occlusion_check`
(I never called this one directly — `resolve_label_z` uses it internally), `antipattern_scan`
(never called manually — nothing suggested a blank-card symptom).

## The genuine gate conflict (the highest-value finding from this session)

`layout.invisible_color_check` (hard fail, `preflight`) and `compare.content_mask` (the
scorer's definition of "painted content") both use a raw RGB-distance-from-background
threshold, independently chosen (40 and 46), to decide whether a fill "counts." For a design
whose actual mechanism is "a card that's ALMOST the same colour as the page, distinguished
only by a drop shadow" — which is exactly what this reference's hero card is; I measured its
real pixels at effectively 0 distance from its own field — **there is no card fill that can
simultaneously (a) clear the engine's hard-fail gate and (b) avoid being counted as scored
"content" the reference itself doesn't have.** I verified this isn't hypothetical: a control
render with the card fill reverted to literal `core.CREAM` (script preserved as
`scratchpad/_test_cardbg_same.py`, NOT part of the accepted build, and it correctly FAILS
`preflight`) scored 0.425 vs. the accepted build's 0.463 at that point in the session — a real
9-point score improvement from violating the hard gate, confirming the card fill genuinely
does inflate the score gap, just not by as much as I first guessed. I kept the hard-gate-
passing version (per CLAUDE.md §1: never violate an encoded rule to chase a score) and
documented the conflict in `brain/RECREATION_AUDIT.md` rather than silently working around it.
**This is a real, reusable finding for whoever owns the gate stack next:** either
`invisible_color_check`'s threshold needs a documented exception for "shadow-differentiated,
same-hue" cards (the engine already has a per-element craft-layer concept for outlines via
`outline_of()` — an analogous "this element's separation comes from shadow, not colour"
declaration would resolve it cleanly), or `content_mask` needs to weight shadow-adjacent flat
regions differently, or this is simply an accepted, permanent gap between the two gates that
should be written into CLAUDE.md §7/§10 so the next agent doesn't re-discover it by trial.

## Iteration times / what I had to guess

- Each `python scratchpad/gen_e7b32bd3_vN.py` run (inside `B.session()`) took 3.5-5.5 seconds
  end to end (render + preflight + save), consistent with CLAUDE.md's claimed ~1.9s/poster
  inside a session plus the Python interpreter/import overhead of loading 5 engine modules via
  `importlib` each run (`core`, `build`, `doodles`, `layout`, `shapes`) — no separate
  measurement of render-only time was taken since the whole script's wall time was already
  fast enough not to matter across 11 iterations.
- What I had to guess vs. measure: I initially GUESSED every pile-object bbox by eye from a
  550x510 crop of the reference (`scratchpad/_crop_pile.png`) for v1-v5, which got the right
  elements in roughly the right neighborhood but was off by 30-90px on several objects (book
  photo height was guessed at 290px, measured-off-crop reality was 222px; ribbed rect was
  guessed at various widths/heights across FOUR different attempts before landing near the
  reference's actual footprint, and even then the shape's true taper was never fully resolved
  — see the genuine rectangle-vs-wedge limitation above). The single highest-leverage action
  in the whole session was switching from "eyeball the crop" to "read `compare.compare()`'s
  worst-3-grid-cells, then crop exactly that pixel region and measure it directly" — that's
  what took the score from 0.463 to 0.247 across v5-v10. `compare.geometry`'s 9x11 occupancy
  grid (run once, step 0) was too coarse on its own to resolve pile-internal object boundaries
  (its cells are ~133x57px, bigger than several individual pile objects); it was useful for the
  ambient bleed panels' large-scale placement but not for the dense pile's internal geometry.

## Verdict

Structurally faithful: all 26 inventoried elements present, correctly proportioned, passing
the looking gate and every hard-fail static/DOM check. Score 0.253, above the 0.16 accept
line, entirely attributable to (a) a resolved-but-real card-colour gate conflict and (b) a
rectangular-clip-path limitation for the reference's organic bleed-panel wedges that showed
genuine diminishing/negative returns under further iteration (confirmed by explicit revert
experiments, not assumption). Logged honestly via `runqueue.py record`, not force-accepted.

## Top 3 friction points (recap)

1. **`invisible_color_check` (hard fail) vs `content_mask` (scoring) structurally conflict for
   any "shadow-differentiated, same-hue-as-background" design** — a real, reference-confirmed
   pattern, not an edge case. No fill satisfies both. Undocumented anywhere in CLAUDE.md.
2. **`collision_ignore` labels and DOM `data-tag` attributes are two separate namespaces that
   LOOK like the same mechanism** — `render()` prints a scary-looking "NO data-tag IN THE DOM"
   warning every time you use plain-label ignore pairs (which is the only mechanism CLAUDE.md's
   own §6 template actually demonstrates), with no doc note that this is expected/harmless.
3. **The score does not reward fixing the worst-reported critique** for shapes this build's
   primitives can't represent exactly (rectangular bbox vs. organic wedge) — two of
   `compare.compare()`'s own top-3 critique lines were in direct, verified tension (fixing one
   cell provably breaks another), which contradicts RECREATION_PROTOCOL's per-line decision
   table framing of "do exactly what it says" as if each critique were independently
   actionable.
