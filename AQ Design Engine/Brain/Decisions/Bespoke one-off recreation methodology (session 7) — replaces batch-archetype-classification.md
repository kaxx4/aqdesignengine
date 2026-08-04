# Bespoke one-off recreation methodology (session 7) — replaces batch/archetype-classification

- CORRECTED APPROACH (user mandate): do NOT route the 44 reference_posters through engine.py's
  small ARCHETYPES registry or rotating content banks. Each reference is recreated individually,
  directly from engine/core.py + build.py + doodles.py + layout.py primitives, in its own
  bespoke script, varying the underlying composition mechanism each time. This is deliberately
  a WIDER decision space, not a classifier into ~5 buckets.
- New reusable primitives added: engine/layout.py — `cluster_positions()` (overlapping pile
  placement for a LOCAL group of badges/photos) and `quadrant_fill_check()` (flags canvas
  quadrants without real visual weight so a mid-layer filler gets added there).
- KEY LESSON (from sample 87525f70, 4 iterations): overlap and frame-filling are SEPARATE
  decisions. Cramming an overlapping cluster into one corner to "solve" overlap starves every
  other quadrant and makes dom_cov WORSE, not better (v1 0.686 -> v2 0.786 -> v3 0.833 vs
  target 0.455). The fix: keep overlap LOCAL to one sub-cluster, and independently ensure every
  other quadrant still gets its own element (per the existing LAYERING SYSTEM rule above).
- KEY LESSON: overlap_frac must never fully bury a badge's text — some minimum visible arc/label
  per badge is a hard constraint, not a nice-to-have.
- RENDERING GOTCHA (sample 2022ebef, session 8): a `position:absolute` child anchored with
  `bottom:Npx` inside a parent that has BOTH `transform:rotate()` AND `overflow:hidden` silently
  fails to paint once the child is wide enough (confirmed via isolated repro in Playwright/
  Chromium: identical SVG content at width 300 renders, the same content at width 760 vanishes
  completely, no error). This cost a full blank-card bug in the "FRIDAY 24TH" ransom-poster
  register. FIX: anchor such children with `top:Npx` instead of `bottom:Npx` — confirmed reliable
  regardless of width. Rule of thumb: never use `bottom` positioning for wide content inside a
  rotated + overflow:hidden card; always use `top`.

## See also
- [[Decisions Index]]
- [[Cramming a pile into one corner starves other quadrants]]
- [[06 The Bespoke Script]]
