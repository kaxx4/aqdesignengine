# Sample 42

**Reference file:** `eaad68d6305fbaca52c0a830906bc783.jpg`

## Composition description & outcome

Reference: eaad68d6305fbaca52c0a830906bc783.jpg ("The Design Flow" podcast cover)
- Background: solid yellow, faint orange grid-line texture across whole canvas.
- Pink thick ribbon/squiggle arc, weaving behind the title blocks and down to the mic, ~x0-620,y230-800.
- Orange small tag "The" (skewed rect), top-left, ~x130-410,y50-140.
- Green skewed rect "Design" (large bold black text), ~x90-660,y75-235.
  - Black drop-shadow offset layer behind (visible as thin black band under green block).
- Orange skewed rect "Flow" (large bold black text), below Design, ~x130-600,y225-370.
  - Black drop-shadow layer beneath, visible as a triangle/wedge at the bottom-left corner.
- Green 6-point asterisk/sparkle, left margin, ~x25-80,y240-300.
- Green 6-point asterisk/sparkle, right side, ~x625-670,y325-370.
- Large photoreal vintage microphone (silver, grille texture), center, dominant hero element
  filling roughly the bottom 55% of canvas, ~x265-560,y370-750 — the single largest element.
- Green speech-bubble "Fresh ideas / Real Stories" with a small tail pointing down-left toward
  the mic, right-mid, ~x460-670,y440-570.
- Orange 12-point starburst badge "Every Friday" (bold black 2-line text), bottom-left,
  ~x75-250,y565-700.

v1 (out/versions/eaad68d6305fbb/v1.png) gaps vs this description:
- Doodle-vocabulary swap (globe for mic hero, green rect for speech bubble) already reviewed —
  acceptable per real-assets-only rule since engine/doodles.py has no microphone icon.
- Real proportion gap: the reference's mic hero fills ~55% of canvas height and dominates the
  lower half; v1's globe substitute is far smaller (~15% of canvas height), leaving a large
  empty area between the globe and the "EVERY WEEK" badge (~y1200-1750 in script coords) that
  the reference does not have — reference's hero fills that space edge-to-edge.
- Missing: the speech-bubble tail shape on the "REAL DRIVES. REAL TEENS." rect (reference has a
  visible tail pointing toward the hero) — v1's rect is a plain box with no tail.
- 2 sparkle asterisks present and well-positioned — matches.

**Sample 42 outcome**: DONE (v2, 1 iteration). v1's hero doodle (globe, substituting for the
reference's mic) was far too small relative to the reference's dominant hero proportion,
leaving a large dead gap above the "EVERY WEEK" badge; the speech-bubble rect also had no tail.
v2 enlarged the hero to ~40% of canvas height/width and repositioned the starburst badge clear
of it, and added a triangular tail to the speech-bubble rect. Visually verified: all elements
present, proportions much closer to the reference, no collisions. No further iteration needed.

## Status
revisit-done — REVISITED (session 8, v1->v2): hero doodle was far too small vs. the reference's dominant mic proportion, leaving a dead gap; speech bubble had no tail. v2 enlarged the hero and added the tail. All verified present.

## See also
- [[Recreations Index]]
- [[Hero scaled far too small vs the reference]]
