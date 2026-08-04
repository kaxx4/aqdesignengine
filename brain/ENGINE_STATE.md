# AQ ENGINE — current encoded state (single source of truth for what's RULE vs still-manual)

## ENTRY POINT
engine.py → generate(name, archetype, content, accent_idx) → runs full self-correcting pipeline.
Everything a design needs comes from encoded RULES, not LLM improvisation. Inputs (archetype, content,
accent) are choices; all CORRECTION is rule-driven.

## PIPELINE STAGES (encoded)
1. Structure: ARCHETYPES[archetype](content, accent, density) — grid-snapped, rule-built elements.
2. Render (Playwright @2x).
3. Numeric gate: preview.critique() — fill, contrast, quadrant balance, uniformity.
4. Per-archetype gate: ARCHETYPE_PROFILES[archetype] (fill_min, max_density) — different geometries,
   different natural density.
5. ENCODED self-correction: sparse/dead-quadrant → escalate density (bigger hero, accent blocks,
   footer band, corner mass); crammed → reduce. Loops to profile max. NO hand-editing.
6. LOOKING GATE (VISUAL_REVIEW.md): operator LLM VIEWS the png, scores every principle, fixes RULES
   if a visual problem isn't caught by numerics. Hard requirement; nothing ships unseen.

## ENCODED RULES (in engine.py RULES + ARCHETYPE_PROFILES)
- reference targets (contrast .26, ink .11, sat .31, dom_cov .46)
- gates: fill 0.34-0.82 (per-archetype override), contrast>0.22, every quadrant>0.12
- craft constants: 6px ink shadow, 4px ink outline, snap-8 grid
- halftone: photos only (flat on solids) — enforced in tex.py
- type scale floors by role; accent rotation (punctuation only)
- snark bank (voice); chip/doodle/logo/meta/footer built from R_ helpers (identical everywhere)

## ARCHETYPES ENCODED (self-correcting)
- number_hero ✓ (density 0-3: number size, accent block width, footer band, corner; NEW: `field`
  param — "cream" default or "accent" for a single saturated dominant field, textured via
  tex.halftone_gradient, for reference signatures like GLASSDOOR "WE WON" that a cream-only base
  structurally could not reach. See brain/DECISIONS.md "accent-flood field mode".)
- radial_orbit ✓ (density 0-4: focal size, orbit size, corner; airier floor 0.26) — FIXED this session:
  the density>=2 corner-mass circle was positioned `left:-60px` (deliberately bled off-canvas) which
  read as stray/disconnected debris (no orbit line, no label) rather than an intentional bleed. Clamped
  to `left:0px` + reduced to 220px so its full bounding box stays on-canvas. Verified by regenerating
  community.png and pixel-cropping the bottom-left corner — circle now renders fully, no clipping.
- giant_type ✓ (dark ink base is an intentional signature, exempt from flat_dominant; NEW: `field`
  param mirrors number_hero — "ink" default or "cream" for a light-dominant giant-word signature like
  DRÖM, where the word is the only major ink mass against a huge light field.)
- stacked_zones ✓ NEW THIS SESSION (density 0-2: row height, footer band). Top-down pill-row list
  archetype — accent title card + kicker chips + an ink container of colored index-chip/label-pill
  rows. Matches the EVENTS-CALENDAR-style references that NONE of the other 3 archetypes could ever
  reach (they're all single-focal geometries; this is a genuinely different reading axis). First-pass
  convergence error ≈0.345 against R3-10 (better than either prior per-sample convergence run) — see
  INSPIRATION.md R3-10 entry for full detail. This is the first of the 5 remaining archetype stubs in
  archetypes.py (diagonal_cascade, off_frame_bleed, scatter_collage, isometric_grid, corner_anchor
  still pending) to get wired into the real self-correcting pipeline.

## TEMPLATE-LEVEL FIX (session 5): flat_dominant now actually gates generation
Cross-archetype finding from the 44-sample batch: dom_cov ran +0.13 to +0.24 over target on EVERY
archetype — a shared-rule bug, not a per-sample one. Root-caused through 3 measured iterations (see
brain/DECISIONS.md "flat_dominant: from computed-but-inert to actually wired" for the full story):
`flat_dominant` was computed by preview.critique() but never included in engine.generate()'s pass/fail
gate (`arch_ok`), so it silently did nothing for the whole life of the engine so far. Now included in
`arch_ok` (with the existing exempt_flat/field=="accent" carve-outs preserved). Re-ran the full 44-sample
batch after the real fix: mean error 0.85→0.838 (8 improved, 2 correctly now flagged NEEDS-LOOK instead
of silently shipping flat, 34 unchanged/already-healthy). This is a genuine template-level improvement —
every future generation across all 4 archetypes benefits, not just the samples in this batch.

## FULL-BATCH v1 PASS (session 5) — every reference sample regenerated
Ran batch_versions.py: writes a v1 recreation for EVERY file in training_samples/reference_posters/
into out/versions/<slug>/v1.png (44/44 done, none skipped). Numeric error (vs the 5-metric convergence
sum used throughout this session) across all 44: mean 0.85, median 0.742, min 0.135, max 1.96 — much
higher on average than the hand-picked deep-convergence samples (0.3-0.6), because these are single-pass
heuristic-content generations with no iteration, exactly as expected for a first full-coverage sweep.
- Best v1s (error <0.3): bf31ba4914 (.135), abb2ab5d11 (.261), 29c6a85891 (.265 — the already-converged
  "We Won" sample), b075bc30db (.27) — mostly number_hero/giant_type hitting archetype-appropriate refs.
- Worst v1s (error >1.3): b2d4cc55d7 (1.96), ffc106f26f (1.83), cfec9bd415 (1.69), 67805068 (1.55),
  e9d82bbdf0 (1.46), d375fd7dbc (1.44), a99a4af4ca (1.39), 1d518d2bc5 (1.35 — DRÖM, already tracked).
  Diagnosed the worst (b2d4cc55d7): target has vdr≈0.99, ink≈0.62 — near-full-canvas dense dark/colorful
  connected mass. This is a STRUCTURAL ceiling: no current archetype (all built around clean separation +
  a light cream/dark-ink base with accents as punctuation) can ever produce that signature. Needs
  scatter_collage (dense overlapping cards/objects, no clean-separation constraint) — confirmed candidate
  for the next new-archetype build, same pattern as stacked_zones unlocking the calendar-style refs.
- This full sweep is intentionally SHALLOW (v1 per sample, heuristic content, no per-sample iteration).
  Deep convergence (v2/v3+, rule diagnosis, targeted fixes) continues selectively on top of this baseline
  — see the sample-specific entries below and in INSPIRATION.md.

## REFERENCE-CONVERGENCE LOG (brain/INSPIRATION.md has full detail per sample)
- Sample #6 GLASSDOOR "WE WON" (29c6a858911dab0fa25ef134785d64ba.jpg): PLATEAUED, total error ≈0.56
  (dom_cov/mean_sat/ink/contrast all within ~0.05 of target; residual driven by vdr proxy — a bbox-
  crudeness limit, not a design gap, per SESSION_LOG's own caveat that some residuals are metric-
  fidelity limits). Unlocked the `field="accent"` capability above and caught+fixed a real meta-text
  contrast bug (white text inherited over the lemon corner block regardless of what was actually
  behind it) — this is the first encoded instance of the "dark-on-dark contrast pre-check" pending item.
- Sample R2-1 DRÖM (1d518d2bc5d3dd93934dbea4cf14984d.jpg): PLATEAUED at iteration 1. Unlocked
  giant_type's `field="cream"` mode (mirror of number_hero's fix). Caught+fixed a second instance of
  the same bug class: a text color hardcoded against the OLD base's contrast (lemon payoff line, fine
  on ink/illegible on cream). Residual: mean_sat/hi_sat_frac run ~.14 hot because the scattered accent
  masses are larger/more saturated than DRÖM's actual objects — real, traceable, not yet fixed (would
  need a size/saturation cap on leftmass/rightmass/lowmass when field=="cream"); vdr gap is a proxy
  artifact (thin cursive word barely registers on the dark-mask bbox method either reference-side or
  ours) not chased further.
- STANDING PRINCIPLE now proven twice: check for a hardcoded dominant-field color FIRST before treating
  a metric gap as a styling problem — it may be a structural ceiling, not a tuning issue. And: every
  field-mode addition must re-audit ALL text colors in the archetype, not just the obvious ones — both
  sessions this pass missed one hidden text color on the first attempt, only caught by looking.
- FULL LOOKING-GATE PASS COMPLETED (this session) on all 44 generated samples in out/converge/ (see
  batch_converge.py at repo root — maps every reference file to a best-fit archetype via ref_metrics
  heuristics, generates through the real engine.generate() pipeline, no hand-tuning). Reviewed all 44
  individually against the full principle checklist (legibility, hierarchy, balance, contrast, craft,
  density). Result: 43/44 clean on first full-batch look; the 1 defect found (radial_orbit focal-number
  overflow, sample 05/index 5, "1.2K") was fixed as an encoded rule (see radial_orbit auto-fit note
  above) and the ENTIRE batch was regenerated and re-reviewed clean. No other legibility, contrast,
  craft-layer, or off-canvas issues found across number_hero (12 samples: cream/accent fields, 3
  accent rotations), giant_type (21 samples: cream/ink fields), radial_orbit (11 samples). Known,
  accepted limitation: GIANT_WORDS/NUMBER_STATS content banks are small (4 and 10 entries) so exact
  wording repeats across the 44 batch samples — this is a content-variety gap in the demo script
  batch_converge.py, not an engine defect; the engine itself renders each repeat correctly with
  different accents/fields/densities.
- Remaining 42 reference samples: not yet run through the deeper reference-convergence loop (metric
  gap measurement vs the specific reference, iterative rule tuning toward that reference's signature —
  see the sample #6/R2-1 entries above). The 44-sample batch above is a BROADER but SHALLOWER pass
  (archetype-fit + looking gate only, no per-sample metric convergence). Filenames are NOT mapped to
  INSPIRATION.md teardown numbers except #6 and R2-1 (now recorded). Mapping the rest is prerequisite
  work before continuing the loop — teardowns exist but the file<->teardown correspondence was lost
  from the original chat session. Partial mapping recorded in passing this cycle (not yet run):
  487e8003509b031fab66b15b992c50c5.jpg = R2-12 DIRTYBARN x GRAZIA "plastic matters" (busy bento/collage,
  archetype not encoded); 51010a5e1a5625cd72aa26fed559bc1b.jpg = R3-5 road-sign sticker sheet (collage,
  not encoded); 620d62f101b97c666749fa48d17d26c8.jpg = R3-3 CLASSICO greatest nights (tilted flyer-stack
  collage, not encoded); 091944e282ce11698315cf95a78615e2.jpg = R3-10 events calendar (pill-row stack,
  stacked_zones-ish, not encoded); 502e07d0ebae6cb98924795f0df95826.jpg = editorial big-serif-stack
  ("pltm", grid paper bg) — not yet matched to any named teardown, resembles the quieter web/editorial
  group (#12-13,15-16,19) but is its own layout (paragraph-scale stacked serif, not one giant word);
  3bb3f9582d5cac37437cb9e049cf5c4a.jpg = a moodboard/polaroid-pile photo (black bg, "Design Project
  Brief" doc + portfolio polaroids) — no existing teardown, not yet classified. All five of these need
  either a new archetype (bento/collage/stacked-pill-row) or don't fit the current 3 encoded archetypes
  at all — deferred until the collage/stacked-zones archetypes are wired.

## STILL MANUAL / PENDING (honest)
- 4 of 8 archetypes wired into self-correction (number_hero, radial_orbit, giant_type, stacked_zones).
  Remaining: diagonal_cascade, off_frame_bleed, scatter_collage, isometric_grid, corner_anchor — these
  would cover the busy/collage references (DIRTYBARN x GRAZIA, road-sign sticker sheet, CLASSICO
  flyer-stacks, OVERFLOW isometric keycaps) that no current archetype can reach.
- Fix-rules cover sparse/crammed/dead-quadrant. Now also covers one contrast-vs-actual-background case
  (number_hero meta/corner) and one text-overflow case (radial_orbit focal number auto-fits by
  character count now — found generating a 44-sample batch pass: "1.2K" (4 chars) spilled past the
  focal circle edge because font-size was fixed for 3-char numbers like "534". Still to encode
  generally: flatness (add ink), uniformity (vary scale + overlap), and text-overflow in the OTHER
  archetypes (only radial_orbit's focal number is auto-fit so far — number_hero's hero number and
  giant_type's word already had auto-fit from earlier session work, chips/labels do not yet).
- Looking gate runs when view tool is available; when down, engine flags looking_required and will
  NOT self-certify.
- Collision auto-fix not yet rule-encoded (audit detects; fix still needs a rule, e.g. auto-nudge).

## PRINCIPLE
If any output quality depends on LLM judgment rather than an encoded rule, that's a bug in the ENGINE.
Fix the rule here, never the individual output.
