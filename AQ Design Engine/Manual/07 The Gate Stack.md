# 7. The Gate Stack

Three tiers. Run the cheap static ones BEFORE render, the pixel/DOM ones AFTER.

### 7a. Static, pre-render — `engine/layout.py` (the tuple-list world the bespoke scripts live in)
`audit.py`'s DOM gate only sees elements tagged `.measure`; bespoke scripts hand-maintain
`(x,y,w,h)` tuple lists, so these run on THAT list:
- `bounds_check(W,H,elements)` → elements clipping off-canvas (feed is 1080×1350, not taller).
- `collision_check(elements, min_overlap=12, ignore_pairs=…)` → any two elements really overlapping
  (doodle over text, badge over shape). Accepts `(x,y,w,h)` or `(label,x,y,w,h)`; echoes labels.
- `invisible_color_check(pairs, page_bg, core)` → any fill/stroke whose resolved color ≈ the
  surface behind it (the "drawn but invisible" bug). Resolves `var(--token)`; skips gradients/named.
- `css_var_check(html, core)` → `var(--typo)` referenced but never defined (renders transparent).
- `dominance_check(elements, W, H, min_hero_frac=0.12)` → **opt-in**; flags "no element reaches hero
  scale" for layouts that should have one dominant element.
- `star_text_width(diameter)` → helper: the width to constrain text to so it fits a star's waist.
- `antipattern_scan(html)` → **manual only** (not in the auto gate — false-positives on normal
  footers). Call by hand when chasing a blank card (the rotate+overflow:hidden+bottom gotcha).
- **`preflight(W,H,elements,html,color_pairs,page_bg,core,expect_hero=…)`** → runs all the
  zero-false-positive checks above at once, returns `{'clean': bool, ...}`, prints one verdict.
  `under_filled_quadrants` is included but ADVISORY (its threshold is noisy — trust the pixel
  critique for density). **This is the standing pre-render call.**
- Also: `quadrant_fill_check` (advisory density) and `cluster_positions` (overlapping-pile
  placement) and `pick_fill_mode` (solid-dominant fill picker) — legacy helpers, still valid.

**Auto-enforcement:** `build.render()` ALWAYS runs `css_var_check` (undefined var is unambiguously a
bug). If you pass `render(html, out, W, H, elements=…, color_pairs=…, page_bg=…, expect_hero=…)`, it
also runs the full `preflight` at render time for free.

### 7b. DOM structural — `engine/audit.py` & `engine/reconcile.py`
- `audit.audit(html, name)` (runs inside `build.render`) → margin breaches + real overlaps between
  `.measure`-tagged DOM elements, with whitelisted by-design overlaps (tags-on-hero, sign piles…).
- `reconcile.probe(...)` → measures rendered DOM extents when you cannot see the image: overflow,
  off-canvas, text-wider-than-container.

### 7c. Pixel / metric — `engine/preview.py` & `engine/ref_metrics.py`
- `preview.critique(png)` / `preview.report(png, name)` → `dead_quadrant`, `sparse`, `crammed`,
  `flat`, `flat_dominant`, `uniform`; returns fill, contrast, per-quadrant fill. The headless
  proxy for the looking gate — run it every render, but it is NOT a substitute for actually looking.
- `ref_metrics.analyze(png)` → `dom_cov`, `mean_sat`, `contrast`, `ink`, `vdr` (visual dominance
  ratio). **Reference targets:** contrast ≈ .26, ink ≈ .11, sat ≈ .31, dom_cov ≈ .46, VDR 0.06–0.20
  (one clear hero; <0.05 = no hero, >0.22 = headline swallows the piece). Treat these like the
  collision auditor — a piece should land within ~0.1 per axis before you call it done.
  (Caveat: flat-vector recreations read low on `vdr` vs. gradient/photo references — a known metric
  limitation, not a visual bug.)

## See also
- [[10 The Bug Catalog]]
- [[08 Encoding A Fix]]

[[Manual Index]]
