# Sample 27

**Reference file:** `a99a4af4caa8fcca981b3e5efca87fcf.jpg`

## Composition description & outcome

Reference: a99a4af4caa8fcca981b3e5efca87fcf.jpg ("Gift Guide Ideas for creatives")
- Background: flat off-white/light gray, faint vertical hairline grid stripes across whole
  canvas (subtle paper-ruled texture), ~7 vertical lines evenly spaced.
- Top-left: "BLACK FRIDAY" bold small-caps + "2025" gray beneath — ~x40-190,y75-105.
- 8 numbered orange circle badges (white bold number, ~40px dia), each connected by a short
  orange DASHED arc/line to its physical object, positioned as follows:
  1. badge near keyboard, bottom-left area ~x210-260,y735-775, dashed line curving up to keyboard.
  2. badge near mouse, mid-left ~x75-125,y480-520, dashed line down to mouse.
  3. badge near grid/mousepad card, lower-mid ~x505-555,y580-620, dashed line to grid card corner.
  4. badge near orange book, upper-right ~x630-680,y265-305, dashed line down-left to book corner.
  5. badge near power-bank object, upper-left ~x175-220,y235-275, dashed line to power bank.
  6. badge near plant pot, top-center ~x300-350,y110-150, dashed line down to plant.
  7. badge near orange donut/ring object, top-center-right ~x475-520,y280-320, dashed line to donut.
  8. badge near Figma sticky-notes, right side ~x630-675,y545-585, dashed line to notes stack.
- Physical objects (photoreal product shots), scattered/overlapping in a loose arc above and
  around the headline:
  - Small black power-bank (Samsung branded) ~x175-330,y235-320, slight rotation.
  - Terracotta plant pot with succulent ~x255-500,y140-360, upright, largest hero object.
  - Orange donut-shaped object (desk toy/pillow) ~x420-655,y255-355, rotation ~-8deg.
  - Orange hardcover book "dieter rams" (Phaidon) ~x565-680,y255-410, rotated ~+8deg (tilted
    right edge up), partially behind headline "Guide".
  - Dark wireless mouse ~x75-215,y480-600, angled diagonally.
  - White mechanical keyboard ~x170-500,y590-720, angled, in front of headline baseline.
  - Gray isometric grid/graph-paper mousepad/card ~x420-660,y565-735, tucked behind keyboard's
    right edge.
  - Small Figma-branded sticky-note stack (2 colored notes with Figma logo) ~x600-670,y565-625,
    tucked at the mousepad's top-right corner.
- Giant serif wordmark headline, stacked/overlapping, mixed color:
  - "Gift" (dark brown/black serif, huge) ~x105-380,y365-500.
  - "Guide" (same style, overlapping to the right) ~x330-660,y365-500.
  - "Ideas" (bold orange serif, below-left, overlapping "Gift") ~x105-390,y480-590.
  - "for creatives" (thin gray sans, small, right of "Ideas") ~x400-660,y520-565.
- Small pill badge "@ Vasil Enev" (orange outline, orange text, small circular avatar icon) —
  ~x105-260,y600-630, sits just under "Ideas".
- Orange rounded-pill CTA "◅ share it with friends" — ~x300-560,y735-775, bottom of the cluster,
  overlapping badge 1.
- Bottom footer row: "GIFT / RESOURCES" bottom-left (2-line bold caps), "2025 / NOVEMBER"
  bottom-center-left (2-line), black circle arrow-button bottom-right — ~y880-910.

v1 (out/versions/a99a4af4caa8fc/v1.png) gaps vs this description:
- Only 6 numbered badges/objects present (globe, leaf, paw, thumbsup, thumbsup, globe) — missing
  items 7 and 8 entirely (no donut/ring object, no Figma-sticky-notes object). Real miss, not
  a style swap.
- No dashed connector lines/arcs from any badge to its object — reference's dashed-arc mechanism
  was skipped entirely (noted in progress tracker as an acceptable simplification, but revisit
  protocol requires re-evaluating this as a real missing element since it's a distinct visual
  detail called out in the description, not just decoration).
- Doodle-vocabulary swaps (globe/leaf/paw/thumbsup for power-bank/plant/grid-card/book) are
  acceptable since engine/doodles.py has no photoreal product icons — keep.
- "@ Vasil Enev" credit tag concept covered acceptably by "@ngo.aquaterra" pill — keep.
- Headline/CTA/footer structure matches well.

**Sample 27 outcome**: DONE (v3, 2 iterations). v1 had only 6 of 8 numbered items and no dashed
connector lines from badges to objects. v2 added item 7 (ring/donut doodle) and item 8 (Figma
sticky-note stack) plus dashed SVG connector arcs for all 8 badges, but badge 7 was placed
directly on top of item 3's paw object (real placement bug — badge and ring were positioned
inside the paw's bounding box). v3 repositioned ring7+badge7 into a clear gap near the headline.
Visually verified: all 8 numbered items present, each with a visible dashed connector, no
overlapping collisions. No further iteration needed.

## Status
revisit-done — REVISITED (session 8, v1->v3): v1 had only 6 of 8 numbered items and no dashed connector lines. v2 added items 7-8 and dashed connectors but badge 7 collided with the paw object; v3 repositioned it clear. All 8 items + connectors verified present.

## See also
- [[Recreations Index]]
- [[Doodle-badge dropped over text or shape]]
