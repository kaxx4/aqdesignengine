# Sample 30

**Reference file:** `b075bc30db04223fc1086b86d92ba2b4.jpg`

## Composition description & outcome

Reference: b075bc30db04223fc1086b86d92ba2b4.jpg ("All That Jazz" — 3-panel triptych, recreating
ONE panel per established precedent, the fullest/middle panel)
- Background: solid white, with a large flat green organic mountain/blob shape covering the top
  ~40% of canvas (jagged zigzag bottom edge), ~x0-W,y0-380.
- Black bold headline "ALL THAT / Jazz" (2 lines, mixed case — "ALL THAT" caps, "Jazz" mixed-case
  cursive-ish), top-left overlapping the green blob, ~x15-220,y10-100.
- White piano-key strip (vertical black-outlined rectangles alternating black keys), spanning
  full width along the bottom edge of the green blob, ~x0-290,y70-220 (only visible in the
  middle panel's crop — keys emerge from under the green shape).
- Yellow trumpet/saxophone silhouette (bent horn shape), left side, ~x0-90,y110-290, partially
  cropped by panel edge.
- Orange trumpet illustration (flat color, bell + valves + mouthpiece), center-left, lower-mid,
  ~x100-220,y150-290, overlapping the blue double-bass shape.
- Blue double-bass/violin silhouette (large, rounded body + neck), center-right, ~x150-280,y60-290.
- Small light-blue hexagon/pentagon accent, left-mid ~x30-55,y195-215.
- Date "4/30" bold black, bottom-left, ~x15-60,y245-265.
- Caption "INTERNATIONAL JAZZ DAY" small bold caps, bottom-left below date, ~x15-95,y270-280.
- Panel divider: thick black vertical bars separate the 3 repeated panels (not part of a single
  poster — triptych framing, not recreated here per established single-panel precedent).

v1 (out/versions/b075bc30db0422/v1.png) gaps vs this description:
- Real bug (flagged in original pass): "SHOW UP, SHOW UP." headline's 2nd line visually
  overlaps/sits flush against the piano-key strip with insufficient gap — needs vertical
  separation.
- Bottom half of canvas (~y1300-2400) is completely empty dead space — reference's compact
  panel has much tighter vertical density relative to canvas height; v1's 3 doodles (globe,
  leaf, thumbsup — acceptable swaps for sax/trumpet/bass) are clustered in the upper-middle
  with nothing below.
- Doodle-vocabulary swap (globe/leaf/thumbsup for trumpet/sax/bass) already reviewed as
  acceptable since engine/doodles.py has no music-instrument icons — keep, but instrument
  shapes could be approximated with SVG for closer fidelity; will keep swap since revisit
  priority is structural completeness not asset fidelity.

**Sample 30 outcome**: DONE (v2, 1 iteration). v1 had a real bug (headline's 2nd line touching
the piano-key strip) and a real gap between the instrument-doodle cluster and the bottom meta
row. v2 pushed the piano keys down and tightened headline line-height to clear the collision,
and added an orange "join the drive" CTA band to fill the gap. Visually verified: green blob,
piano keys, headline, 3 instrument-doodle substitutes, date, caption, and new CTA band all
present with no overlaps. No further iteration needed.

## Status
revisit-done — REVISITED (session 8, v1->v2): v1 had a real headline/piano-key collision and a real gap above the footer. v2 fixed the collision and added a CTA band to fill the gap. All verified present.

## See also
- [[Recreations Index]]
- [[Dead half the reference fills]]
