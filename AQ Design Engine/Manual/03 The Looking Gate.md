# 3. The Looking Gate

Numeric/metric checks are PROXIES. They pass pieces that are visually broken (text off its shape,
dead corners, flat fields, invisible elements). **The only reliable check is LOOKING at the
rendered PNG.** Full protocol: `brain/VISUAL_REVIEW.md`.

**Critical sequencing:** the looking gate runs AFTER the PNG is rendered, on the image you can
actually see — never on a disk path you assume is correct. In Claude Code: after every render,
`Read` the PNG (it displays visually) and review it. Wire this into the loop so it happens EVERY
iteration, automatically.

**Review against every principle**, and for each failure write "[element] — what's wrong — the fix":
- **Legibility** — every word readable; nothing clipped by a shape edge or another element.
- **Hierarchy** — one clear hero; the eye knows where to land first.
- **Balance** — no dead quadrant; weight distributed, not dumped in one corner.
- **Rhythm / flow** — spacing between bands/clusters is intentional, not an accidental gap.
- **Contrast / color** — dark type on light field; accents punctuate (~30%), never flood.
- **Craft / depth** — outlines, offset shadows, one hero-shine; not flat matte everywhere.
- **Density** — board-level busy but audited clean; no collisions.

**When you can't see (view tool down / headless):** use `engine/reconcile.py` (measures element
extents in the rendered DOM — catches overflow, off-canvas, margin breach, text-wider-than-
container) and `engine/preview.py` (catches sparse, crammed, dead-quadrant, flat, flat_dominant,
uniform from the pixels). **NEVER fabricate a visual review.** If you can't see it and can't measure
it, say so.

## See also
- [[Visual Review]]
- [[07 The Gate Stack]]

[[Manual Index]]
