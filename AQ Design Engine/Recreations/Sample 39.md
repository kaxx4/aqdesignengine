# Sample 39

**Reference file:** `d2add78f901cbf3b892742fb5669ea47.jpg`

## Composition description & outcome

Reference: d2add78f901cbf3b892742fb5669ea47.jpg (full laptop-mockup website screenshot; picked
the green "statement band with inline pill-labels" section per established single-mechanism
precedent)
- Green solid band, edge-to-edge, ~y880-1145 of the full page screenshot.
- Giant black bold caps sentence wrapping 3 lines, with small white-outlined pill-label chips
  inserted mid-sentence at word-scale (not full-line-height), each a rounded rect with dark
  bg + bold caps label: "Explore", "Discover", "A Global", "Experience", "Begins", "at Your",
  "Next", "Meal" — 8 total pill chips scattered inline within the sentence flow.
- 4th line: "AWAITS!" in bold orange italic, larger scale than the black text above it.
- Overall: the green band is compact relative to its text — text fills the band edge-to-edge
  top-to-bottom with almost no vertical padding above/below the paragraph.

v1 (out/versions/d2add78f901cbf/v1.png) gaps vs this description:
- Content swap (AQ program names for literal site copy: welfare/climate/no cv/show up for
  explore/discover/etc.) — acceptable, count is close (4 pills vs reference's 8, fewer but
  still present as the core mechanism).
- Real proportion gap: v1 has a large empty gap (~y900-1750) between the "AWAITS!" line and the
  black "CHOOSE YOUR LANE" CTA band at the very bottom — the green band itself is far taller
  than its text content, unlike the reference's compact, text-filled band. This was flagged as
  fixed in the original pass ("cta_band never appended, fixed to v2") but the CTA band's
  presence didn't address the real gap: the green band's vertical padding is still oversized
  relative to reference proportion.

**Sample 39 outcome**: DONE (v2, 1 iteration). v1 (post earlier cta_band fix) still had a large
~410px dead gap between the "AWAITS!" line and the bottom CTA band, unlike the reference's
compact, text-filled band. v2 enlarged the headline text, tightened its vertical position, and
added a small "welfare • climate • education" caption row to close the gap. Visually verified:
statement sentence with inline pill labels, italic "awaits!" line, caption row, and CTA band all
present with no dead space. No further iteration needed.

## Status
revisit-done — REVISITED (session 8, v1->v2): even after the earlier cta_band fix, a real ~410px dead gap remained before the CTA band. v2 enlarged the headline and added a caption row to close it. All verified present, no dead space.

## See also
- [[Recreations Index]]
- [[Dead half the reference fills]]
