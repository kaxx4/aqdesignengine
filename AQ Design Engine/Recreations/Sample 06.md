# Sample 06

**Reference file:** `1d518d2bc5d3dd93934dbea4cf14984d.jpg`

## Composition description & outcome

Canvas light gray-cream bg, no texture. Z-order back-to-front:
1. Top-left small caps wordmark "LINKEDIST" (→ recreate as "AQUATERRA"), plain black, small.
2. Top-right pill button: white rounded-pill outline w/ black border containing a right-arrow.
3. Headline, 2 lines, bold black sans, left-aligned (~x8-88%,y13-24%): "October at [Linkedist in
   blue] — what a month" followed by a small lightning-bolt emoji/glyph at the end of line 2.
4. Large white rounded-rect calendar CARD (~x13-88%,y30-75%), drop shadow, containing:
   - "October 2025" bold black title top-left of card, small "Today" pill button w/ left/right
     chevron arrows top-right of card.
   - 7-column weekday header row (Sun-Sat), thin gray text, grid of date numbers below in a
     7-col x 5-row month grid, thin hairline gridlines between cells.
   - A small red-filled circle badge over date "28" (top-left, prior month, grayed) — like a
     "today" indicator badge.
   - A small party-popper emoji/glyph in the Friday column near date 3.
   - Two small red pushpin/map-pin icon accents placed directly on TWO different date cells
     (approx over "22" and "27") marking event days.
5. SIX polaroid photo cards overlapping/bleeding out of the calendar card edges, each: white photo
   border, thick colored inner border-frame (rotates through pink, blue, purple, gold, +2 more),
   a real photo image, small bold caption label bottom of the polaroid, each rotated a few degrees,
   drop shadow, layered on top of and slightly beyond the calendar edges:
   a. Blue-framed polaroid, upper-left area, group workshop photo, caption "Workshop for TEVA"
      (partially — actually caption sits as separate handwritten annotation, not on polaroid).
   b. Pink-framed polaroid, upper-right, on-stage conference photo w/ "STARTUPFAIR" banner text
      visible in photo, no caption chip.
   c. Pink/red-framed polaroid, right side below b, portrait photo, caption chip "Promotion" in
      pink pill overlapping the bottom of the photo.
   d. Blue-framed polaroid, lower-left, audience/conference-room photo, no caption.
   e. Pink-framed polaroid, center-lower, phone/app screenshot photo "LinkedIn Growth Tactics"
      flyer, small calendar-icon graphic visible inside the photo.
   f. Blue-framed polaroid, center-bottom (frontmost/largest shadow), dark navy app-ad screenshot
      "Black Friday is coming!" w/ small CTA button visible inside the photo.
6. Handwritten-style cursive/marker annotation labels with curved connector arrows pointing from
   label text to specific polaroids/dates: "Workshop for TEVA" (pointing down-right to blue
   polaroid a), "Liutauras" (pointing up-left to polaroid c's name label), "LIMA" (pointing
   up-right to polaroid e).
7. Several autumn maple-leaf illustrations (orange/red/rust, 2-3 tone gradient per leaf, detailed
   vein lines) clustered in TWO groups: upper-left cluster (2-3 leaves stacked, near polaroid a)
   and lower-left cluster (2-3 leaves stacked, below polaroid d) — richer and more numerous than
   simple single-leaf doodles.
8. Bottom row: two black pill tags "HIGHLIGHTS" + "OCTOBER" bottom-left, black pill page-counter
   "01/07" bottom-right.
v1's biggest misses: only 4 polaroids instead of 6, no pushpin icons on calendar dates, no
handwritten-annotation arrows connecting labels to polaroids/dates, leaf doodles were 2 lone simple
shapes instead of two richer multi-leaf clusters, no lightning-bolt glyph in headline, no
red "today" circle badge or party-popper accent on the calendar grid.

**Sample 6 outcome**: DONE (v4, 3 iterations). v1 had only 4 of 6 polaroids, no pushpins, no
handwritten-annotation arrows, sparse 2-leaf doodles instead of two rich clusters, and no
lightning-bolt/party-popper/red-badge calendar accents. v2 added all of these but v2/v3 had a bug
where a moved annotation's on-canvas text position wasn't matched by its bounds_check bbox, so
bounds_check silently missed that "liutauras" was rendering 170px off the right edge of the canvas
(invisible). v4 fixed the coordinate/bbox mismatch and repositioned the note to sit on-canvas next
to the Promotion polaroid. All 8 composition-description items now visibly present.

## Status
revisit-done — REVISITED (session 8, v1->v4): v1 had only 4 of 6 polaroids, no pushpins on calendar dates, no handwritten-annotation arrows, sparse leaf doodles, no lightning-bolt/party-popper/red-badge accents. v4 rebuilt with all 6 polaroids, 2 pushpins, 3 annotated arrows, 2 rich leaf clusters, and all calendar accents; fixed an off-canvas annotation bug along the way. All verified present.

## See also
- [[Recreations Index]]
- [[Element clips off-canvas]]
- [[Stale bbox tuple hides a real off-canvas or collision]]
