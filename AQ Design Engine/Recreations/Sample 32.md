# Sample 32

**Reference file:** `bf31ba491425433b3af84cb75022d1f9.jpg`

## Composition description & outcome

Reference: bf31ba491425433b3af84cb75022d1f9.jpg (2-panel: signpost + pattern-filled speech
bubbles; this recreation focuses on the speech-bubble half per established precedent since the
signpost mechanism was already realized in sample 8)
- Background: solid cream, no texture.
- Bold black headline "WHAT THEY SAY." top-left, ~x40-380,y30-70.
- 3 stacked speech-bubble cards, each a rounded rect with a distinct SVG pattern fill, a small
  tail triangle pointing down-left from the bottom edge, drop shadow, white bold quote text:
  - Bubble 1: sky-blue bg + purple diagonal-line pattern, ~x260-1220,y210-450, tail at
    bottom-left ~x290,y450-490. Quote: "Felt like I finally found my lane."
  - Bubble 2: green bg + pink crisscross/star-burst line pattern, ~x340-1220,y480-700, tail at
    bottom-left ~x360,y700-740. Quote: "No CV, just showed up and stayed."
  - Bubble 3: orange bg + yellow diagonal brush-stroke pattern, ~x260-1220,y740-960, tail at
    bottom-left ~x300,y960-1000. Quote: "My first drive turned into my whole crew."
- Small black oval "shadow" beneath the tail, bottom of the 3rd bubble.
- Small yellow/orange sparkle doodle, left margin, ~x60-150,y560-620.

v1 (out/versions/bf31ba491425433/v1.png) gaps vs this description:
- Real bug: the tail triangles use `border-top:24px solid var(--_c)` — an undefined CSS custom
  property — so the tails render invisible/broken (one bubble shows a stray malformed triangle
  artifact instead of a clean tail). All 3 cards read as plain rounded rects with no visible tail.
- Bottom half of canvas (~y1000-2600) is empty dead space — only the 3 bubbles + title + 2
  sparkles occupy the top ~40%, nothing fills below.
- Otherwise structure matches: 3 patterned bubbles with correct pattern styles (diagonal lines,
  crisscross, brush strokes), correct quote text, correct color per bubble.

**Sample 32 outcome**: DONE (v3, 2 iterations). v1 had a real bug: bubble tails used
`border-top:24px solid var(--_c)`, an undefined CSS variable, so tails never rendered. v2 fixed
the tail color (explicit per-bubble color) and added a 4th patterned bubble to fill the bottom
dead space — but a stray "artifact" turned out to be the sparkle doodle overlapping bubble 2's
corner, a real placement collision. v3 repositioned that sparkle clear of the card. Visually
verified: all 4 bubbles have clean visible tails, no collisions, patterns and quotes all present
and legible. No further iteration needed.

## Status
revisit-done — REVISITED (session 8, v1->v3): v1's bubble tails used an undefined CSS var (invisible). v2 fixed tail color + added a 4th bubble to fill the bottom gap, but a sparkle doodle collided with bubble 2's corner; v3 repositioned it. All 4 bubbles verified clean, no collisions.

## See also
- [[Recreations Index]]
- [[Doodle-badge dropped over text or shape]]
- [[var(--typo) undefined renders transparent]]
