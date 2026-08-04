# Sample 24

**Reference file:** `841552212f857b7ca02fafe6dfc5d879.jpg`

## Composition description & outcome

Full-bleed black bg w/ subtle halftone texture. Z-order back-to-front:
1. Jagged orange/red textured burst shape bleeding off the top-right corner.
2. Pink triangle peeking from left edge (mid-canvas) and blue triangle peeking from bottom-right
   corner, both behind the headline/schedule box.
3. Two logo marks top-left (v1: single AQ logo, fine simplification).
4. Yellow ribbon banner "Coming Soon" small italic script + bold caps subtitle line UNDER it in
   the SAME yellow band (v1: "COMING SOON" only, missing the second line of Korean/subtitle text
   inside the band — though v1's single-line content is an acceptable simplification, not a hard
   fail since the ribbon device itself is present).
5. Giant BUBBLE-OUTLINE headline (white fill, thick black outline stroke on each letter, NOT flat
   solid white) "SPECiAL" with a small crown emoji sitting on the "i", small yellow subtitle text
   directly below in a different script, then "Week" continuing the bubble-outline style — v1's
   headline ("SHOW UP WEEK") is FLAT SOLID WHITE with no outline/stroke at all, missing the
   signature bubble-letter treatment entirely, and has no small subtitle line between the two
   headline words.
6. Two small white 4-point sparkle/star doodles flanking the headline area — v1 has ZERO stars.
7. Orange/red schedule box (2-line white/black bold text, "PART1"/"PART2" dates) — v1 matches this.
8. Green speech-bubble-shaped CTA (3-line text) — v1 uses a plain rounded rect, not a speech-
   bubble shape (missing the pointer/tail), a minor miss.
9. Yellow squiggle ribbon bottom-right — v1 uses a thin teal zigzag line instead of a thick yellow
   ribbon-squiggle, a color/weight mismatch.
v1's biggest misses: the headline has no bubble-outline stroke treatment (flat solid white
instead), zero sparkle-star doodles anywhere, no subtitle line between the two headline words, and
a large dead gap in the middle third of the canvas between the headline and the schedule box.

**Sample 24 outcome**: DONE (v3, 2 iterations). v1's headline was flat solid white with no
outline/stroke, had zero sparkle-star doodles, no subtitle line, and a large dead gap between the
headline and schedule box. v2 added a bubble-outline stroke via `-webkit-text-stroke`, 2 stars, a
subtitle line, a speech-bubble tail, and moved the schedule box up to close the gap — but the
stroke color was set to `var(--ink)` (near-black) against a black background, making it invisible.
v3 fixed the stroke color to a bright yellow accent so the bubble-outline is clearly visible. All
composition-description items now visibly present.

## Status
revisit-done — REVISITED (session 8, v1->v3): v1's headline was flat solid (no bubble-outline stroke), had no stars/subtitle, and a dead mid-canvas gap. v3 added the bubble-outline (after fixing an invisible-stroke-color bug), stars, subtitle, and closed the gap. All verified present.

## See also
- [[Recreations Index]]
- [[Text stroke approx equals bg (invisible outline)]]
