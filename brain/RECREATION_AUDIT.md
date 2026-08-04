# Revisit pass — full visual composition audit (session 8)

Per user correction: one-line "structural reads" were too shallow and caused real misses
(e.g. sample 40's map outline shape was skipped entirely, leaving just floating labels on
flat color — the reference's core visual foundation was missed, not a minor detail).

## New per-sample protocol (mandatory from here on)
For each of the 44 samples, in order:
1. **Full composition description** — list EVERY visual layer before writing any code:
   - Background: literal color/gradient/texture, and any large background SHAPES (maps,
     silhouettes, terrain outlines, blobs) — not just "textured bg".
   - Foreground layers in z-order: what sits on what, what overlaps what.
   - Every distinct element: type, approximate size/proportion, color, rotation, position.
   - Do not summarize multiple distinct elements as one ("scattered decorations") — enumerate.
2. **Recreate** (v1) from that description, matching proportions.
3. **Visually compare** v1 against the reference side by side — check every item in the
   composition description is actually present and proportioned correctly. Missing a listed
   element = fail, not a style variation.
4. **Iterate** (v2, v3...) fixing gaps found in step 3. Tag each version with which gaps
   from the description it fixes.
5. Only mark done once the rendered image visibly contains everything in the composition
   description, or a deliberate/logged reason why an element was substituted (e.g. real-photo
   fabrication avoided).

## Status
Revisit tracker below. Each row: sample, whether the ORIGINAL recreation missed a structural
element, and revisit status.

| # | file | original miss | revisit status |
|---|------|---------------|-----------------|
| 40 | d375fd7dbcf69cfcaeef11a6be81b2b9.jpg | Skipped the hand-drawn coastline/map outline shape entirely -- recreation was just floating labels + route lines on flat blue, no actual landmass geometry | DONE (v2) — added the wobbly coastline silhouette w/ district-border lines, partial cropped-circle bleeding off right edge. Now contains every item in the composition description below. |
| 1 | 87525f70ad66d82bf7c9457ad6765a62.jpg | v1-v4 used generic AQ badges ("show up that's it" etc) that don't match this reference's ACTUAL sticker cluster at all -- wrong badge shapes, wrong count, wrong specific icons (crop-mark globe, paper airplane, bitten-globe, giant letter, curved-text circle, diecut hand sticker) | DONE (v5->v6, 2 iterations). v5 had all 10 elements but 3 were too weak to read (melon bite invisible, ray pattern didn't render, SHOW UP text hidden behind melon). v6 fixed all three: real bite notch, repeated triangle ray strip, repositioned A so vertical text clears the melon, added globe-in-palm to hand sticker. All 10 composition-description items now visibly present. |
| 2 | 091944e282ce11698315cf95a78615e2.jpg | v1 missing: outer white card frame w/ drop shadow on gray page bg; had inverted black/yellow-outline title card instead of solid yellow fill; no "this month"/"2026" nav row; schedule rows floated on cream with no black wrapping panel; label-pills were flat ink-black instead of colored; more-info and url bars were merged into one instead of separate | DONE (v2, 1 iteration). Rebuilt with: gray page bg + white outer card w/ shadow; solid yellow title card "our drives. this month." w/ 2 sparkles; two-segment nav row (white "this month" pill w/ arrow badge + pink "2026" pill); black panel wrapping all 5 rows, each w/ a colored date-pill AND a colored (non-black) label-pill cycling through accents; separate two-tone "more information" bar w/ seam sparkle; separate bordered "@ngo.aquaterra" url bar w/ arrow badge. Verified all elements visible in rendered v2.png. |
| 3 | 10f1b8a9789261fc73570521bf63db74.jpg | v1 was a plausible editorial register but missing 3 specific reference doodles (bee, red triple-chevron arrow cluster, bottom-right asterisk) and left too much dead space in the bottom half vs. the denser reference | DONE (v3, 2 iterations). v2 rebuilt full composition (scribble double-loop+arrow, dot, blue 3-finger+thumb hand w/ face doodles, sparkle, bee, headline stack HOW/ILLUSTRATION-on-yellow-band/ENHANCES, red triple-chevron+sparkle, YOUR-pill-w/-circle-arrow+BRAND, italic subtext, bottom-right asterisk) but v2 had a text collision (BRAND overlapping the pill's circle-arrow badge, off-canvas subtext/asterisk from loose vertical spacing). v3 fixed pill to a fixed width with BRAND positioned clear of it, and tightened all vertical spacing to fit within canvas with no off-canvas warnings. All 10 composition-description items now visibly present. |

## Sample 3 — full composition description (written BEFORE v2)
Canvas cream bg, no texture. Editorial register: thin black horizontal rule at top (~y6%) and
bottom (~y95%), with "02." far-left / studio name center / "@2025" far-right sitting just above
each rule (both top and bottom rows use this pattern, bottom swaps the center text for a tagline).
Z-order back-to-front:
1. Scribble doodle upper-left (~x10-35%,y15-33%): a hand-drawn double-loop squiggle (two
   overlapping circles) that trails up into a curved arrow pointing up-right, thin black stroke.
2. Tiny black circle/dot just below-left of the loop doodle (~x8%,y35%).
3. Blue solid 3-finger+thumb hand/mascot illustration, center-right (~x40-72%,y28-48%), each
   finger has a tiny doodled face (dot eyes + curved mouth), thin black linework detailing on
   palm, white circle at the wrist/base. Rotated slightly, overlapping the headline below it.
4. Small 4-point star/sparkle outline right of hand (~x63%,y26%), thin black stroke, no fill.
5. Bee doodle far-right (~x84-92%,y37-40%): tiny black-outlined bee w/ yellow/black striped
   abdomen and two wings, small scale.
6. Headline stack, left-aligned, giant bold black caps, 3 lines tight leading:
   - "HOW" (line 1, plain black)
   - "ILLUSTRATION" (line 2) on a yellow rectangular highlighter-marker band, rotated ~-3°,
     text black, band extends past text on both ends with hard-edge (marker-stroke look)
   - "ENHANCES" (line 3, plain black)
7. Triple red arrow/chevron doodle (~x68-80%,y58-65%), three small arrow chevrons stacked
   pointing down-left, positioned right of "ENHANCES", plus one more small star outline below-right
   of the arrows (~x83%,y64%).
8. Final line "YOUR" in a green rounded-pill highlight band containing a black filled circle
   badge with a white right-arrow icon inside it, then "BRAND" continues in plain black caps
   directly after the pill on the same baseline (~x8-88%,y72-80%).
9. Italic subtext line below headline block (~x8%,y85%): "Not just "cute" — illustration can
   elevate how people remember you."
10. Small asterisk doodle bottom-right (~x92%,y87%), thin black outline, above the bottom rule.
Overall: dense upper-2/3, headline block dominates lower-half-ish, only a modest gap between
subtext and bottom rule (not a large dead zone) — the v1 recreation left too much empty space
in the bottom half and was missing the bee, the red arrow-chevron cluster, and the bottom-right
asterisk.

## Sample 4 — full composition description (written BEFORE v2)
Canvas: light blue-gray graph-paper grid texture (fine square grid lines) across the FULL canvas,
no vignette. A tight, interlocking, isometric-3D cluster of chunky rounded-square "keycap" blocks
fills roughly the top 75% of the canvas, touching/overlapping in a diamond arrangement (each block
rotated to a diamond/isometric angle, NOT axis-aligned). Every block has TRUE 3D shading: a lighter
top face (the flat color) + a solid BLACK bottom/side face offset down-right ~14px giving genuine
chunky-3D keycap look (not just a drop shadow blur).
Z-order back-to-front, positions approximate (canvas ~510x640 ref, scale to 1080x1350):
1. Two small star/sparkle outline doodles, top-left cluster (~x5-30%,y3-13%), thin black stroke,
   one larger one smaller, both angled.
2. Cream/off-white rounded-square block, top-center (~x35-58%,y0-16%), containing a black-outlined
   envelope icon centered on it, thin purple/pink-gradient bottom edge.
3. Cream rounded-square block, upper-right of envelope (~x62-92%,y18-30%), containing black
   code-bracket icon "</>" style zigzag centered, tilted ~-15°.
4. Cream rounded-tall-rect "notification" block far upper-right (~x68-96%,y5-25%), small circle
   badge with "1" in top-right corner of it, thin orange-gradient bottom edge.
5. Letter block "O" — orange fill, black letter, upper-left-mid (~x10-30%,y20-38%).
6. Letter block "V" — lavender/purple-light fill, black letter, center (~x28-50%,y35-52%),
   overlapping O's bottom-right corner.
7. Letter block "E" — indigo/blue-purple fill, black letter, center-right of V (~x48-68%,y32-50%).
8. Letter block "R" — mint/teal-green fill, black letter, far right (~x68-92%,y28-46%).
9. Letter block "F" — sky-blue fill, black letter, lower-left (~x8-30%,y55-75%).
10. Letter block "L" — yellow/gold fill, black letter, center-bottom (~x26-48%,y58-78%), tallest/
    most-forward block (drop shadow largest), overlapping F.
11. Letter block "O" (2nd) — green fill, black letter, center-right-bottom (~x44-66%,y55-75%).
12. Letter block "W" — lavender fill, black letter, right (~x62-90%,y62-82%).
13. Black hand-pointing cursor/arrow icon, small, centered in the gap between the two letter rows
    (~x38-50%,y48-58%), overlapping the V/L blocks — reads as a UI cursor click indicator.
14. Cream hand-icon block (pointing finger / "tap" gesture), right side between rows
    (~x82-98%,y50-65%), black outline, no bright fill.
15. Cream chat-bubble block lower-left (~x5-32%,y77-90%), rounded rect with a small tail, three
    dot-circles inside representing "typing", thin purple-gradient bottom edge.
16. Cream pencil-icon block, diagonal, lower-right (~x50-88%,y82-96%), tilted ~-25°, pink eraser
    tip visible at the bottom-right end, thin black outline.
Overall palette: cream/off-white for the 6 non-letter accessory blocks, saturated flat colors
(orange, lavender, indigo, mint, sky-blue, gold, green) for the 8 letter blocks, all with true
black 3D offset undersides. v1's biggest misses: only 6 letters instead of 8 ("OVERFLOW" not
"SHOW UP"), blocks used flat drop-shadow instead of true isometric black side-faces, way too
loosely spaced with a large empty bottom half, and missing 5 of the 6 accessory icon blocks
(envelope, code-bracket, notification-tag, chat-dots, pencil) plus the cursor icon.

**Sample 4 outcome**: DONE (v3, 2 iterations). v1 had only 6 letters ("SHOW UP" not 8-letter
"OVERFLOW"), flat drop-shadow blocks instead of true isometric black-underside keycaps, and was
missing 5 of 6 accessory blocks + cursor. v2 rebuilt full composition with all 16 elements but the
pencil block's SVG rotated oddly (only the pink tip visible, body invisible) and the cursor icon
read as an ambiguous triangle. v3 fixed the pencil (rebuilt as a simple rect+triangle with explicit
transform-origin) and redrew the cursor as a proper white-outlined black pointer arrow. All 16
composition-description items now visibly present and correctly proportioned.

## Sample 5 — full composition description (written BEFORE v2)
NOTE: reference file is a 7-cell moodboard grid (different "PORTFOLIO" type treatments); per prior
session's judgment call, only the bottom-most cell (the ransom-note/cut-paper black panel) is
recreated as a single AQ poster, since that's the register that best fits AQ's ink/craft voice.
That panel's composition:
- Full-bleed solid black bg, no texture.
- Top label row (~y6-8%): "OCTOBER 2022 - 2023" far-left, "GRAPHIC DESIGN" center, small caps
  white/gray text, no rule line above/below it (unlike editorial samples).
- Giant ransom-note headline "PORTFOLIO" spanning ~y58-78%, x5-92%: EACH letter is its own separate
  white paper-cut card/tile with a JAGGED, IRREGULAR torn-paper silhouette (not a clean rounded
  rect) — corners nicked at random angles, some edges diagonal-cut, each tile independently
  rotated a few degrees +/-, tiles overlapping slightly at their touching edges. Letter glyph
  printed bold black serif-ish caps, roughly centered per tile.
  - 2nd tile ("O" of PORT) has a small dot-halftone texture patch visible in its corner.
  - One tile ("R" of FOLIO area) has a diagonal torn notch cut out of its top edge.
  - Right end of the word: two-three thin vertical white line accents (like a torn-paper fringe/
    barcode accent) just past the last letter tile.
- Bottom row (~y88-90%): "PERSONAL PROJECT" + "HIJGUIDE" stacked small caps, left-center; small
  red circular badge (app logo) bottom-right with tiny white platform-ID text next to it.
- No footer rule line, no dot-perforation row (that decorative dot row belongs to a DIFFERENT
  moodboard cell, not this one — v1 incorrectly borrowed it from elsewhere in the moodboard).
Overall: v1's biggest miss is that its letter tiles have plain straight/rounded edges (just
rotated rectangles), not the true jagged torn-paper silhouette that defines the ransom-note look,
and it included a dot-perforation decorative row that doesn't belong to this specific panel.

**Sample 5 outcome**: DONE (v3, 2 iterations). v1's letter tiles were plain rotated rounded-rects,
missing the true jagged torn-paper silhouette that defines the ransom-note look, and it included a
dot-perforation row borrowed from a different cell of the source moodboard that doesn't belong to
this panel. v2 rebuilt with genuine irregular clip-path tiles per letter (random jagged corners,
one diagonal notch, one dot-halftone texture patch, thin vertical fringe lines past the last
letter) but used the reference's literal word "PORTFOLIO" — v3 swapped the headline to "AQUATERRA"
(same letter count) to keep the recreation on-brand while preserving the exact torn-paper treatment.
All composition-description items now visibly present.

## Sample 6 — full composition description (written BEFORE v2)
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

## Sample 7 — full composition description (written BEFORE v2)
Full-bleed flat red/tomato bg w/ visible film-grain noise texture. Z-order back-to-front:
1. Top row small labels: "$100 / Cover Consumo" upper-left (2-line, bold+regular), "Caballero /
   In the DJ Booth" upper-right (2-line) — v1 substituted "FREE entry"/"DJ SET by aq crew" which
   is an acceptable content swap, that's fine.
2. Center wordmark stack: "WELCOME TO" small caps, then giant wobbly-baseline logotype "CLASSICO"
   (each letter independently rotated a few degrees, ransom-note style) in black, then "PENINSULA"
   small caps below.
3. THREE stacked white note-cards, each titled "THURSDAY 13TH" (v1: "FRIDAY 24TH" — fine swap),
   fanned out with slight rotation, each card's LOWER two-thirds contains a hand-drawn black-ink
   line illustration of two/three stylized cartoon figures dancing/wrestling together (loose
   scribbly figure-drawing style, arms flailing) — NOT blank white space. Each card shows a
   DIFFERENT snippet/pose of the dancing figures, layered so the topmost card's illustration is
   most visible.
4. Small illustrated objects scattered around/behind the cards (all bold-outline flat-color
   sticker-style illustrations):
   a. Upper-left: a drink-jug illustration with a label ("Jacob Elordi's Bath Water" joke label —
      substitute AQ-relevant joke label), teal liquid, black spigot/tap.
   b. Right of the cards: a gray disco-ball sphere with a few small white sparkle/star accents
      beside it.
   c. Left-middle, below jug: an orange cocktail glass with ice cubes and a striped straw.
   d. Right-middle: a martini glass with green olives and a red-striped straw.
   e. Lower-left: a black wine/liquor bottle with a white label + lightning-bolt-like logo mark.
   f. Lower-right: a large red/pink elephant-head illustration (ears + trunk + tusk), sticker-
      style with thick black outline, overlapping the envelope shape's bottom-right corner.
   g. A pink rubber-glove illustration upper-right area (near disco ball), fingers spread.
5. Large two-tone triangular "envelope-flap" shape at the bottom third: two triangles meeting at
   a center point (like an opened envelope), left triangle NAVY, right triangle LIGHT GRAY-BLUE,
   spanning the full width, with a small gold sparkle doodle and pink paw-print doodle sitting on
   top of it (v1 already has these two doodles — keep).
6. Bottom text block: "RESERVATIONS (+18)" bold, phone numbers below in regular weight (v1:
   "RSVP (open to all)" + handle — fine swap), small italic tagline bottom-left ("Conocer es no
   excederse" / v1: "show up is the only rule" — fine swap), two small sponsor-logo wordmarks
   bottom-right stacked ("Grupo Masai" + "Dobel Tequila" style logos — v1 substituted "WELFARE" /
   "CLIMATE" text labels, a reasonable AQ-brand swap for sponsor logos).
v1's biggest miss: the three stacked cards were completely BLANK (no dancing-figure illustration
inside any of them — the single most important visual content of the whole poster was missing),
and none of the 7 scattered object illustrations (jug, disco ball, cocktail, martini, bottle,
elephant, glove) were present — only globe/leaf/paw/thumbsup/sparkle doodles were used instead of
this reference's specific illustrated-object cast.

**Sample 7 outcome**: DONE (v3, 2 iterations). v1's three stacked cards were completely blank
(missing the dancing-figure illustration that's the poster's core content) and none of the 7
scattered object illustrations (jug, disco ball, cocktail, martini, bottle, elephant, glove) were
present. v2 added stick-figure line art inside each card plus all 7 objects, but the figures didn't
render at all — root-caused to a genuine Chromium rendering bug (not a content bug): an absolutely
positioned child anchored with `bottom` inside a `rotate()` + `overflow:hidden` parent silently
fails to paint once the child is wide enough (confirmed via isolated repro: identical circle SVG at
width 300 renders fine, same circle at width 760 vanishes; switching the anchor from `bottom` to
`top` fixes it regardless of width). v3 applied that fix. All composition-description items now
visibly present. Worth encoding as a standing engine rule: avoid `bottom`-anchored children in
rotated+overflow:hidden containers; prefer `top`.

## Sample 8 — full composition description (written BEFORE v2)
Reference is an isolated clip-art street-sign-pole illustration, no background/layout — flat
vector, thick black outlines throughout. Z-order bottom-to-top (pole base to top of signs):
1. Vertical gray metal pole, RIBBED/CORRUGATED texture (horizontal ridge lines running the full
   length), narrower than the signs, centered.
2. Near the bottom of the pole: a yellow rounded-square box containing a black pedestrian
   "walking person" icon (the WALK signal), mounted flush against the pole's left side.
3. Just above/right of that: a yellow rounded-square sign with a red circle-slash icon over a
   double-arrow, and small black text "NO STANDING ANYTIME" beneath the icon.
4. A 3-lamp traffic-light box (black rounded housing) mounted on the pole above the pedestrian
   signals, with THREE lit/yellow circular lamps stacked vertically inside it (not gray/off —
   all 3 rendered as bright yellow-gold circles, evenly spaced).
5. Street-sign arms fanning off the pole above the traffic light, each a black-outlined rounded
   rectangle sign attached perpendicular to the pole, rotated at a slight angle, casting a small
   drop shadow:
   a. Two BLACK signs with white bent-arrow glyph + "ONE WAY" text, stacked near the very top,
      angled slightly different directions (like a mini directional cluster).
   b. A green sign "BROADWAY" below those.
   c. A green sign "W 44 ST" below that, slightly different angle.
v1's biggest misses: the pole has no ribbed/corrugated texture (plain flat rectangle), the traffic
light's 3 lamps are rendered dark gray (unlit) instead of bright yellow/lit, and the pedestrian
WALK-signal box + "NO STANDING ANYTIME" sign are both completely absent — v1 only has a plain
pink square and a teal circle at the base instead of these two specific sign elements. The
4 fanning signs are a reasonable content-swap match (AQ program names instead of street names).

**Sample 8 outcome**: DONE (v2, 1 iteration). v1 had a plain flat pole (no ribbed texture), dark
gray unlit traffic-light lamps, and no pedestrian WALK-signal box or "NO STANDING ANYTIME" sign
(substituted with a generic pink square + thumbsup badge). v2 added corrugated pole texture via a
repeating-linear-gradient background, glowing lit-yellow lamps, a walking-person icon box, and a
red-slash/double-arrow "no standing" sign box with caption text. All composition-description items
now visibly present.

## Sample 9 — full composition description (written BEFORE v2)
Full-bleed white bg, no texture. Z-order back-to-front:
1. Small red square logo mark upper-left (~x6-16%,y3-11%) containing a black abstract 4-legged
   creature silhouette (like a stool/animal), thick black outline.
2. Top info row, 3 columns, small bold caps + regular caps text: "23 KATTENGASSE, BERLIN, DE /
   OPENING HOURS: 9AM-10PM" (left), "THE CASR OF DROM: ALL TOGETHER" (center), "SOFA MONSTER /
   CUBIC / LEG / SMILO / CUBIC" (right, a credits/cast list) — v1 substitutes AQ-relevant copy,
   fine swap.
3. Giant lowercase wordmark "dröm" (v1: "aquaterra"), 2-line stack, thick rounded-slab black
   sans, filling ~x6-95%,y28-58%. The umlaut dots over the "o" are SQUARE not round. A small
   circled-C copyright mark sits to the upper-right of the "m".
4. FIVE large Matisse-style blob-creature illustrations in a loose bento arrangement below the
   wordmark, each MUCH larger than a small icon (roughly 30-45% of canvas width each), thick
   black outline, flat single-color fill, occupying the full lower ~42% of the canvas height:
   a. Red lip/tongue-shaped blob (upper-left of the blob zone, ~x9-56%,y58-72%), with two
      white elongated "finger" shapes poking up from its top edge, and a black curvy line
      (like a smile/tongue crease) drawn across its lower half.
   b. Yellow paint-splat/flame-shaped blob (upper-right, ~x63-92%,y58-78%), jagged flame-like
      edges, with a thin drip/tail extending down from its bottom point.
   c. Blue 4-legged "sofa monster" blob (lower-left, ~x9-50%,y78-100%), a rounded body with
      FOUR thin leg shapes hanging down from the bottom, like a stool/creature silhouette.
   d. Solid purple/lavender square, small, lower-middle (~x56-73%,y85-100%).
   e. Green sock/boot-shaped blob, lower-right (~x80-95%,y82-100%), an L-shaped bent leg/sock
      silhouette.
v1's biggest miss: the 5 blobs were rendered as small GENERIC doodles (leaf, paw, globe,
thumbsup, plain square) at roughly 1/4 the reference's scale, clustered in the bottom-left corner
— completely missing the specific large creature-blob shapes (lip+fingers, flame/splat, 4-legged
monster, sock/leg) that are the visual heart of this composition, and leaving the whole lower-
middle and lower-right of the canvas as dead space instead of filled with big shapes.

**Sample 9 outcome**: DONE (v3, 2 iterations). v1's 5 blobs were generic small doodles (leaf, paw,
globe, thumbsup, plain square) at roughly 1/4 the reference's scale. v2 rebuilt with 5 large custom
SVG blob-creatures (red lip w/ 2 white fingers + smile-crease, yellow flame/splat w/ drip tail,
blue 4-legged sofa-monster, purple square, green sock/boot-leg) but the first sizing pass put all 5
shapes off-canvas (extending 30-260px past H=1350). v3 rescaled the hero wordmark down and
compressed the blob grid to fit two rows within the canvas with no off-canvas warnings. All 5
composition-description blob shapes now visibly present at proper scale.

## Sample 10 — full composition description (written BEFORE v2)
Full-bleed mint-green bg with a fine dot-grid texture. Z-order back-to-front:
1. Top card: a white SPEECH-BUBBLE shape with a THICK BLACK OFFSET SHADOW duplicate behind it —
   critically, the card's outline is NOT a plain rounded rect: it has small jagged rectangular
   notches cut into its top-left corner and bottom-left edge (like a torn/tabbed speech-bubble
   tail), 2-line bold black caps headline text inside ("'GLASSDOOR'S / BEST PLACES TO WORK" —
   v1 substitutes "AQUATERRA'S 1,200 VOLUNTEERS", fine swap), rotated slightly.
2. Yellow oval/pill badge "2025" overlapping the card's top-right corner, small black bold text,
   thin black outline.
3. A hand-drawn black squiggle-arrow connector: starts as a DOUBLE OVERLAPPING LOOP (like a
   scribbled loop-de-loop) then curves down-right into a clean arrow with arrowhead, connecting
   the card to the banner below — v1's arrow is a single smooth curve with NO loop, missing the
   signature loop-de-loop start.
4. Two overlapping black rectangular banner strips (diagonal, stacked with a slight vertical
   gap/overlap at the left, wider at the right), each containing giant bold white caps text
   ("WE" / "WON" — v1: "SHOW UP." / "THAT'S IT.", fine swap).
5. A light-blue jagged 8-point starburst badge sitting ON the seam between the two banners
   (upper-right-ish), containing a black hand-wave/raised-hand icon silhouette (v1 substitutes a
   thumbsup silhouette — reasonably close, acceptable swap).
6. A purple/lavender speech-bubble-tail chip attached to the right end of the second banner,
   containing a horizontal row of 7 small yellow dot-circles (like a "counting/tally" motif) —
   v1 has NO equivalent chip at all, just a small unrelated sparkle.
7. A small yellow star/badge shape overlapping the bottom-left corner of the second banner —
   v1 has no equivalent (has a globe icon instead, positioned separately below, not overlapping).
8. A partial donut/pie-chart shape (orange outer ring + blue inner wedge segments) peeking from
   behind the bottom-left corner of the second banner, mostly cropped/cut off by the banner edge —
   v1 has NO donut/pie shape at all.
9. Small circular profile-icon placeholder bottom-left corner of canvas (v1: omits, uses handle
   text instead — acceptable brand-consistency swap).
v1's biggest misses: the info card lacks the speech-bubble tail notches (plain rounded rect
instead), the connector arrow lacks its signature double-loop scribble start, and THREE distinct
accent elements are missing entirely — the purple dot-tally chip, the yellow star badge, and the
orange/blue donut-chart peeking from the banner corner.

**Sample 10 outcome**: DONE (v3, 2 iterations). v1's info card was a plain rounded rect (missing
the speech-bubble tail notches), the connector arrow was a single smooth curve (missing the
signature double-loop scribble start), and three accent elements were completely absent: the
purple dot-tally chip, the yellow star badge, and the orange/blue donut-chart peeking from the
banner corner. v2 added all of these but the dot-chip and a sparkle landed off-canvas; v3 fixed
both positions. All composition-description items now visibly present.

## Sample 11 — full composition description (written BEFORE v2)
Full-bleed solid black bg. Z-order back-to-front:
1. Left peeking document stack, mostly off-canvas-left, only right edge visible (~x0-8%): a
   dotted-circle icon top-left corner, a thin green squiggle mark below it, a colored strip
   (orange band, then blue band, then pink band stacked), small caption text fragment
   "...ng, Web Des..." and 3 small colored dot bullets (gray, pink, black) stacked vertically.
2. Right peeking document, partially off-canvas-right (~x88-100%,y42-100%): a light-gray card
   tilted, header text "2020 Port..." in dark gray, and below it an ORANGE card filled with a
   white isometric/triangle line-pattern graphic.
3. Front-and-center white card (the main "brief" doc), large, slightly rotated, drop shadow,
   containing: thin black horizontal rule near top, bold black 2-line headline ("Design Project"
   black + "Brief" in blue — v1: "DRIVE BRIEF. THIS MONTH." fine content swap), second thin rule
   below headline, then a 3-COLUMN numbered list (not 2-column): column1 "01 Context" (orange,
   underlined green accent below "Context"), "03 Visual References" (pink); column2 "02 Audience"
   (green), "04 Timeline" (blue, hand-drawn gray ellipse circling this specific item), column3
   "03 Goals" (orange, partially cropped by the right-peeking doc), "05 Spec" (orange, also
   cropped) — plus "06 Deliverables" (green) and "07 Budget" (orange) in a lower row. A green
   solid triangle shape peeks from behind the card's bottom-right area.
4. Yellow sticky-note "FINAL" (v1: "approved", fine swap) with a folded/dog-eared bottom-right
   corner, handwritten-style italic text with underline, positioned overlapping the TOP-LEFT of
   the white card — must sit BELOW/behind the headline text baseline, not overlapping the actual
   headline letters (v1's sticky-note currently overlaps and partially obscures "DRIVE BRIEF").
v1's biggest misses: only ONE peeking document (left blue card) instead of TWO (missing the right
gray/orange isometric-pattern document entirely), the left stack has no dotted-circle icon, no
colored dot bullets, and no partial caption text, no green triangle peeking from the card's
bottom-right, the list is 2-column instead of 3-column, and the sticky note directly overlaps and
obscures headline text instead of sitting cleanly above/beside it. The card is also much taller
than the reference's, leaving a large dead white area in the lower half.

**Sample 11 outcome**: DONE (v2, 1 iteration). v1 was missing the right peeking gray/orange
isometric-pattern document entirely, the left stack lacked the dotted-circle icon/colored dot
bullets/caption text, there was no green triangle peeking from the card's bottom-right, the list
was 2-column instead of 3-column, and the sticky note directly overlapped the headline text. v2
added the right document, dot-bullets/icon/caption on the left stack, the green triangle, switched
to a 3-column list, and repositioned the sticky note clear of the headline; also shrank the card
to reduce dead space. All composition-description items now visibly present.

## Sample 12 — full composition description (written BEFORE v2)
Full-bleed black bg. Bento grid of ~11 cells across 3 rows, each cell a rounded-rect with its own
fill/content — critically, EVERY cell has something inside it (photo, graphic, or text), none are
flat empty color blocks. Z-order back-to-front, row by row:
Row 1 (~y13-36%): 4 cells —
  a. White cell: "NO [globe emoji] plastic bags" stacked text over 3 gray oval bg bands, with a
     small flesh-tone BABY-DOLL FIGURE breaking out/overlapping the cell's bottom-right corner.
  b. Small photo cell: a ventriloquist-dummy puppet face photo with 2 small blue teardrop emoji
     accents.
  c. Black-bordered lime-outline cell: "noun" label pill top, definition paragraph text below,
     decorated with squiggly blue and pink liquid-blob line-doodles in the corners.
  d. (below b+c, taller) Blue cell: giant black lowercase "plastic matters" 2-line text, with a
     rubber-duck emoji + small star sparkles breaking out/overlapping its top-right corner.
Row 1.5: lime-green cell "006 / how [flower emoji] plastic [are] -> we? / graziaesthetica ... 
  dirtybarn" small caption row bottom.
Row 2 (~y53-59%): full-width lime pixel-font divider band: "MORE [pink pixel-chevrons] OR [black
  star] LESS [pink circle-O] " — v1 has "MORE * DRIVES * LESS * TALK" (fine content swap) but
  should be in a PIXELATED/monospace block font style with small pixel-art icon accents between
  words, not plain bold sans with unicode stars.
Row 3 (~y61-92%): 4 cells —
  e. Orange cell: white jagged starburst-outline shape + a real photo of a person (hand on face)
     bleeding out over the bottom edge, plus white squiggly line-doodles in the corners.
  f. Purple cell: a bold white JAGGED PIXEL-STYLE "W" squiggle/zigzag line drawn across it,
     photo/pattern bleeding from the bottom (v1's purple cell is flat empty — miss).
  g. Cream cell: black starburst-outline + small heart icon centered.
  h. Pink/magenta cell: yellow 3D-emoji-style smiley face centered.
Row 4: bottom-right wide cell — black bg w/ lime border: globe icon + purple arrow + 3 pink
  sparkles, then pink pixel-font "DIRTYBARN" + green pixel-font "GRAZIA" brand credits below —
  v1 has NO equivalent cell at all (replaced with plain footer text).
v1's biggest misses: two cells (teal, purple) are completely flat/empty with no content at all —
every cell in the reference has a shape or graphic; the "noun"-equivalent cell has no border/
liquid-blob decorations; there are no breakout sticker elements overlapping cell edges (baby doll,
duck, sparkles); the purple cell lacks its signature jagged squiggle line; and there's no
bottom-right brand-credits cell (globe+arrow+sparkles+two brand names).

**Sample 12 outcome**: DONE (v2, 1 iteration). v1 had two completely flat/empty cells (teal,
purple) with no content, no breakout sticker elements overlapping cell edges, no border/liquid-
blob decoration on the definition cell, and no bottom-right brand-credits cell. v2 filled every
cell (photo in the teal slot, jagged zigzag squiggle in the purple slot), added a baby-doll-figure
breakout under the white cell, a duck+sparkles breakout over the blue cell, liquid-blob squiggle
doodles + lime border on the definition cell, and a bordered credits cell with globe/arrow/sparkle
+ brand text. All composition-description items now visibly present.

## Sample 13 — full composition description (written BEFORE v2)
Full-bleed black bg. Top masthead row: "MERSHE" / "SAIGON" / "PRESENTS" small bold caps, 3-column
(v1: "AQUATERRA"/"KOLKATA"/"PRESENTS", fine swap). Below, a bento grid of 6 event cards, EVERY
card containing a real photo/illustration, not flat color — filling nearly the FULL canvas height
(cards extend close to the bottom credit row, no large dead zone):
1. Blue card (top-left, tall): palm-tree/skate-park illustrated scene (3 characters sitting on
   steps with a boombox, retro cartoon style) filling the top 2/3 of the card, small caption
   "MERSHE X TECHNO" top-right, headline "TANOSHII PARK" + date/time bottom, a circular badge
   (brand mark in a ring) overlapping the card's bottom-right corner.
2. Red card (top-right): halftone-textured photo of a person mid-dance-move, small clover/flower
   accent glyphs, caption text top-right, headline "HIPHOP NIGHT" bottom-left.
3. Yellow card (below red, taller): giant black headline "BEER BÔNG", small clover glyphs top-
   right, "Every Saturday" label, several large white daisy-flower illustrations (each with a
   simple smiley face inside) clustered on the right side/bottom, a black diagonal arrow, prize/
   copy text bottom-left, circular badge overlapping bottom-right corner.
4. Teal/cream split card (below blue): "thursday funny" headline on teal left half, cream right
   half containing an illustrated staircase with a character sitting on a step + a daisy-flower
   illustration with a face, small clover glyph, caption text below headline.
5. Cream/tan card (bottom-left): bold black+yellow headline "BORN * BÔNG / GIÁ 60 CÀNH" (price
   callout), small clover glyph between words.
6. Purple/gradient card (bottom-right, wide): faded photo of a person visible through the
   gradient overlay, script-style "LADIES NIGHT" headline, "SUNDAY NIGHT" label, 3 columns of
   small perk text at the bottom.
Bottom row: 3 small clover glyphs + "HOTLINE: ..." left, address text center, all small caps.
v1's biggest misses: ALL SIX cards are flat solid-color blocks with only text — none contain any
photo, illustration, or flower/character graphic — and the whole bottom third of the canvas
(below the last row of cards) is empty dead space, unlike the reference where cards fill almost
the entire canvas height right down to the credit row.

**Sample 13 outcome**: DONE (v2, 1 iteration). v1's six cards were all flat solid-color blocks
with text only — no photo, illustration, or flower/character graphics anywhere — and the bottom
third of the canvas was empty dead space. v2 added a real photo to the blue and red cards, 3
daisy-flower illustrations (SVG, with face variants) to the yellow card, a staircase-illustration
+ daisy to the teal/cream card, a faded photo + gradient to the purple card, and enlarged all
cards so the grid fills down to the credit row with no dead zone. Minor cosmetic note: the "food"
photo asset has baked-in caption text that shows faintly behind the FOOD DRIVE label — not a
missing composition element, just a minor asset overlap. All composition-description items now
visibly present.

## Sample 14 — full composition description (written BEFORE v2)
Light gray-white bg. A DENSE scatter-collage of ~20 road-sign clip-art stickers, packed nearly
EDGE-TO-EDGE with overlapping corners and almost no visible background gaps between them (true
collage density, not evenly-spaced scattering). Sign types present, enumerated individually:
1. Interstate shield badge ("195"/red-white-blue), 2. orange "DETOUR" arrow rect, 3. white
diamond w/ black curvy-road icon (no text, icon only), 4. red octagon "STOP", 5. yellow diamond
w/ black U-turn arrow icon, 6. worn yellow diamond "DEAD END", 7. white/red triangle w/ truck-
on-slope icon, 8. tan/black "ONE WAY" arrow rect, 9. gray shield "ROUTE US 66", 10. green street-
sign cross-pole ("Main Street"/"Moments" on a real pole graphic), 11. yellow diamond w/ traffic-
light icon (3 colored dots), 12. dark red arrow-shaped "EXIT WAY OUT" sign, 13. blue circle w/
white straight-arrow icon, 14. yellow diamond "CAUTION", 15. worn yellow diamond w/ curvy-road
icon, 16. white rect w/ black fork-arrow icon (straight+right), 17. orange diamond "ROAD WORK
AHEAD", 18. white "ROUTE 66" shield (small), 19. small orange "DETOUR" arrow, 20. green highway
sign "75 SOUTH Atlanta", 21. white/black "ONE WAY" arrow rect (2nd instance, vertical).
v1's biggest miss: only ~15 signs placed with LARGE visible gaps of bare background between them
(nowhere near the reference's edge-to-edge packed density), and v1's signs are almost entirely
TEXT-ONLY badges (words like "no excuses", "one lane all in") — missing the reference's icon-only
sign variety: curvy-road icon, U-turn arrow icon, traffic-light dots icon, straight-arrow circle,
fork-arrow sign — roughly half the reference collage is pure iconography with no words at all,
and v1 has none of that.

**Sample 14 outcome**: DONE (v4, 3 iterations). v1 had only ~15 signs with large visible gaps
(not the reference's edge-to-edge collage density) and every sign was text-only, missing the
reference's icon-only sign variety. v2 added 5 icon-only signs (curvy-road, U-turn, traffic-light,
fork-arrow, straight-arrow circle) to increase density and variety, but the fork-icon plate
rendered invisible (dark icon on dark bg) and collided visually with the yield diamond. v3-v4
fixed the icon color contrast and repositioned the yield diamond and fork plate to clear the
overlap and stay on-canvas. All composition-description sign types now visibly present with much
tighter, more collage-like density.

## Sample 15 — full composition description (written BEFORE v2)
Fine grid-paper bg (cream, thin gray gridlines). Top bar: back-chevron + serif italic wordmark
"plm." top-left, 3 icons (list/hamburger, search, plus) top-right. Below, a giant mixed-serif
headline spanning 5 lines from ~y26% to ~y88% of the canvas (fills most of the vertical space,
NOT concentrated in the top half): "the" (italic serif) / "community" (bold serif, on a pink
highlighter band) / "for social" (italic serif) / "media" (bold serif) / "marketers." (bold
italic serif). Five speech-bubble/pill tag callouts positioned around and overlapping the
headline at different heights spanning the full vertical range of the headline block (not
clustered only near the top): green tag "Courses, Resources And Membership" (upper, pointing down
into "the"), white pill "Community" w/ pink dot + cursor icon (mid-upper, overlapping "community"
y-descender), white pill "This Month's Trends" w/ pink dot (middle, left side, level with
"media"), white tag "The Home Of Simple Strategy And Supportive Community" (middle, right side,
level with "media"), blue tag "plm." w/ cursor icon (lower, pointing up into "marketers."). Small
emoji/icon accents scattered at different heights: cherries (upper-right, by "community"),
disco-ball (upper-left, by "community"), lightning bolt (middle-right, by "social"), flying-
money emoji (lower-left, by "marketers."). Bottom ~10% of canvas is empty margin only — the
reference's dense content genuinely extends down through ~88% of the canvas height.
v1's biggest miss: the whole composition (headline + all tags/icons) is compressed into roughly
the TOP HALF of the canvas (ending around y=1140 of 1350), leaving a large, unintentional empty
dead zone in the bottom half — unlike the reference where the tag callouts are staggered at
different heights all the way down through 88% of the canvas height, and there is no equivalent
of the reference's bottom-most "plm." tag sitting low and close to the last headline line.

**Sample 15 outcome**: DONE (v2, 1 iteration). v1 compressed the whole composition into the top
half of the canvas (ending ~y1140 of 1350), leaving a large unintentional dead zone below, and had
only 4 tags all clustered near the top. v2 stretched the headline to 5 lines spanning ~19-62% of
canvas height, added a 5th tag, and re-staggered all 5 tags + 5 decorative icons across the full
vertical range down to the "aq." tag near y1160, matching the reference's full-height density.
All composition-description items now visibly present.

## Sample 16 — full composition description (written BEFORE v2)
Full-bleed black bg. Z-order back-to-front:
1. Top row: "$100 / Cover Consumo" left, script logotype "CLASSICO" + "PENINSULA" center, "Whatever
   / Dance the night" right (v1: "FREE entry"/"AQUATERRA"/"DJ SET by aq crew", fine content swap).
2. Card stack occupying roughly y17-83% of canvas (NOT just the bottom third — cards start high,
   right below the top row, with minimal gap):
   a. Red card (topmost-left, largest): headline "THE GREATEST NIGHTS ONLY IN" + white oval
      "CLASSICO" badge + date "11.12.25 / THURSDAY" + second headline "COLD NIGHTS, FUNNY DRINKS,
      BAD DECISIONS" + small martini-glass icon bottom-right of the card.
   b. Yellow card (behind/right of red, partially covered): "BAD IDEAS MAKE GREAT NIGHTS" bold
      black text.
   c. Orange scalloped/flower-shaped badge (top-right of the yellow card, overlapping its corner):
      black lightning-bolt icon centered.
   d. Blue-sky/green-grass photo card (lower-right, behind other cards' edge): "...ONLY CARE ABOUT
      GOOD PARTIES" text + a white hand-drawn globe/circle doodle.
   e. Concert/crowd photo card (lower-left): real photo of a crowd with stage lighting.
   f. Yellow rect tag "CLASSY NIGHTSS" overlapping the bottom of the photo card.
   g. Red oval tag "THURSDAY 11TH" bottom-right, overlapping the photo/blue-card boundary.
3. Bottom-left: white outline bottle-icon w/ lightning-bolt label.
4. Bottom text row: "RESERVATIONS (+18)" + phone numbers left, small italic tagline below, two
   sponsor-style wordmarks bottom-right (v1: "@ngo.aquaterra" handle, fine swap) — CRITICALLY this
   footer text must NOT overlap/collide with the card stack above it.
v1's biggest misses: (1) the entire top ~55% of the canvas (y150-950) is empty dead space — the
card stack doesn't start until very low, unlike the reference where cards begin right below the
top row; (2) the footer "@ngo.aquaterra" / "climate . education" text directly overlaps and is
rendered illegible UNDER/THROUGH the front orange card; (3) the white "AQUATERRA" pill badge
overlaps the "JOINING" headline text, making both illegible; (4) missing cards/elements entirely:
no yellow "BAD IDEAS" card content readable, no orange scalloped lightning badge, no blue-sky photo
card with globe doodle, no "CLASSY NIGHTSS" tag, no "THURSDAY 11TH" oval tag, no bottle icon,
and the crowd-photo card is cut off/bleeding off the bottom edge of the canvas instead of being
fully contained. This sample was flagged in its original log as having real defects the numeric
gates missed — the revisit pass confirms and must fix all of them, not just re-verify.

**Sample 16 outcome**: DONE (v4, 3 iterations). v1 had a dead top half, footer text colliding
illegibly with the front card, an "AQUATERRA" pill overlapping "JOINING" text, a cut-off photo
card, and 6 entirely missing elements (yellow card content, scalloped lightning badge, blue/green
photo card, "classy nightss" tag, "thursday 11th" oval, bottle icon). v2 fully rebuilt the
composition with all elements present and cards starting right below the top row (no dead zone),
but v3 still had the "classy nightss" tag and bottle icon overlapping the footer text. v4 repositioned
both clear of the footer. All composition-description items now visibly present with no
text-legibility collisions.

## Sample 17 — full composition description (written BEFORE v2)
Full-bleed sky-blue field, no texture. Z-order back-to-front:
1. Ghosted repeat-word background: giant slightly-darker-blue outline caps text wrapping around
   ALL FOUR EDGES of the canvas like a border frame — "COFFEE" along the top, continuing down the
   right edge, "RAVE"/"PARTY" along the bottom, continuing up the left edge — not just one corner.
2. Two sheet-music staff fragments (5 thin horizontal blue lines + a few music notes drawn ON the
   staff), one fragment top-left corner, one fragment bottom-right corner, each with a small
   treble-clef-like squiggle.
3. Large central hero: a 3D-rendered pair of over-ear headphones (dark olive/black textured) with
   a cassette tape clipped where the earcup would be, occupying roughly the center 55% of canvas
   width, y8-58% — v1 substitutes a flat black vinyl-record/globe icon which reads as a totally
   different object (record vs headphones+cassette); needs a headphones-recognizable silhouette
   instead, even in flat-illustration style.
4. FIVE yellow lightning-bolt icons scattered around the headphones at different scales/rotations
   (not just 2), thick black outline.
5. SIX yellow music-note icons (mix of single eighth-notes and a couple of connected/beamed pairs)
   scattered around the headphones and lower-canvas — v1 has ZERO music-note icons, only star/
   sparkle doodles (wrong icon family entirely).
6. Torn/jagged-edge paper banner ribbon crossing the lower-middle third, rotated slightly, bold
   black condensed caps headline text ("BREWDOWNER SUNDOWNER, COFFEE RAVE PARTY" — v1: "SATURDAY
   SHOWUP, WELFARE DRIVE PARTY", fine content swap) — v1's banner has a plain straight-edge
   rectangle, not the reference's torn/jagged paper-edge silhouette.
v1's biggest misses: (a) the hero object is a vinyl/globe icon, not recognizable as headphones+
cassette; (b) zero music-note icons anywhere (reference has 6, a signature motif); (c) ghost-text
background only appears in the top-left corner instead of framing all four edges; (d) no sheet-
music staff-line fragments; (e) banner has clean rectangular edges instead of torn-paper edges;
(f) bottom third of canvas is empty dead space.

**Sample 17 outcome**: DONE (v2, 1 iteration). v1's hero was a flat vinyl/globe icon (unrelated to
headphones+cassette), had zero music-note icons, ghost-text only in one corner instead of framing
all 4 edges, no sheet-music staff lines, a clean-edge (not torn) banner, and an empty bottom third.
v2 rebuilt with a flat-illustration headphones+cassette hero, 6 music notes, 5 lightning bolts,
4-edge ghost-text frame, 2 staff-line fragments, and a jagged torn-paper banner. All composition-
description items now visibly present.

## Sample 18 — full composition description (written BEFORE v2)
Grainy paper-texture cream bg. A TIGHT ring/wreath of ~15 colorful character/shape doodles
interspersed with question-phrase words, forming a dense loop (not loosely scattered dots) around
a center multi-line answer phrase, occupying roughly the middle 65% of canvas height:
Doodles enumerated: green flower-burst (smiley), red 4-point star, green squiggle, blue flower
(face), yellow diamond/sparkle, yellow rounded-blob w/ two eyes, pink flower w/ face, green snake/
leg shape, pink dog/animal lying down, green flower-burst (2nd), brown teddy-bear+bunny character,
white bird, blue diamond/sparkle (2nd), brown flower (smiley), blue rounded-square block, cream
banana/bone shape w/ small flower face, yellow ribbon/M-shape (x2 stacked), blue swirl/ribbon,
red starburst (jagged), yellow corrugated/accordion shape. Each doodle has a thick black outline
and a drop-shadow offset (consistent "sticker" style).
Question-phrase words woven INTO the ring gaps, italic gray serif: "What" / "does" / "it" / "take"
/ "to" — small, at the ring's outer edge, upper-left arc.
Center answer, large mixed-weight serif, 3 lines, left-aligned within the ring's inner space:
"think" (italic) / "outside" (bold) / "the box?" (mixed: "the" small bold, "box" large bold, "?"
separate) — v1 uses a single short line "SHOW UP." in one weight/size, missing the multi-line
mixed-typography treatment.
Below the ring: "PLAYBOOK" 2-line bold sans-serif wordmark + small thumbsup emoji beside it
(v1: "AQUATERRA" + sparkle, fine swap).
v1's biggest misses: only ~9 doodles/words loosely scattered with large gaps between them instead
of a tight, dense ~15-element wreath (the ring reads as sparse dots, not a wreath); the center
answer is a single short plain-weight line instead of a 3-line mixed-serif/mixed-weight phrase;
overall doodle variety is far narrower (v1 reuses globe/leaf/paw/sparkle 2-3x each) vs the
reference's ~15 genuinely distinct character shapes.

**Sample 18 outcome**: DONE (v3, 2 iterations). v1 had only ~9 doodles/words loosely scattered
with large gaps (reusing globe/leaf/paw/sparkle repeatedly) and a single-line plain-weight center
answer, unlike the reference's tight ~15-doodle wreath and 3-line mixed-typography phrase. v2
rebuilt with 15 genuinely varied doodles (leaf, star, squiggle, heart x2, burst, circle, paw, plus,
dots, ring, zigzag, lightning, thumbsup) tightly wreathed and a 3-line "think / OUTSIDE / the BOX?"
mixed-weight center phrase, but one doodle landed off-canvas; v3 fixed the position. All
composition-description items now visibly present with proper wreath density.

## Sample 19 — full composition description (written BEFORE v2)
Top ~48% of canvas: red/tomato checker-grid (thin black gridlines) band with a WAVY/SCALLOPED
bottom edge (not a straight cut) transitioning to cream below. On the grid: green rotated ticket-
shape tag "RESERVE Your Seat!" upper-left, large yellow pill button "Book a Call" center (bold
script-style italic text, underlined), blue jagged starburst badge upper-right with white script
"Sale!" text FULLY CONTAINED inside the starburst (not clipped/spilling past its points — v1's
star text overflows past the star's edges and is illegible, a hard legibility fail).
Bottom ~52% cream section: two-line bold caps body copy, then a giant lowercase wordmark
("bitesized" — v1: "aquaterra", fine swap) with a small mascot/badge character to its right
(circular face icon w/ cap, peace-sign hand, drumstick — v1 substitutes a plain thumbsup-in-circle
badge, a reasonable simplified swap), and TWO small social-icon glyphs (X/twitter logo + Instagram
camera-outline logo) bottom-right — v1 has neither icon, only a text handle.
v1's biggest misses: (1) the star badge's "show up" text overflows past the star points and reads
as "how ur" — illegible, must be resized/repositioned to stay fully inside the star; (2) the two
social-media icon glyphs (X, Instagram) are completely absent; (3) roughly the bottom third of the
canvas (below the wordmark row) is empty dead space with no additional content, unlike a fully
composed poster.

**Sample 19 outcome**: DONE (v3, 2 iterations). v1's star badge text overflowed past the star's
points ("show up" read as "how ur", illegible), the X/Instagram social icons were missing
(replaced with a text handle), and the bottom third was empty dead space. v2 enlarged the star and
shrank/repositioned its text to sit fully inside the points, added real X and Instagram glyph
icons, and added a teal info strip with a leaf doodle to fill the bottom space, but the star and
strip needed repositioning to stay on-canvas; v3 fixed both. All composition-description items
now visibly present and legible.

## Sample 20 — full composition description (written BEFORE re-check)
NOTE: reference file is a 9-slide pitch-deck moodboard; per prior session's judgment call, only
the cover-slide mechanism was recreated as a single AQ poster (a reasonable synthesis, not a
literal multi-slide copy). Cover-slide composition: full-bleed rounded-corner photo (desk scene),
"Date Presented / 12 June 2024" small caps top-left on the photo, brand logo pill top-right on the
photo, a white rounded card overlapping the LOWER portion of the photo (card is slightly rotated in
the reference, giving a casual pinned-photo feel) containing giant bold black caps title text
("PITCH DECK" / v1: "IMPACT REPORT.", fine swap). Below the card (from a DIFFERENT slide of the
deck, the "OUR IMPACT" slide, synthesized in): 2-3 stat badges in a row, each a solid-color
rounded-rect containing a giant bold stat number + small caption ("85%", "78%" in the reference's
impact slide — v1 uses "85%", "1.2K", "470", a reasonable content substitution combining stats
from multiple deck slides into one row).
Checked against the render: full-bleed photo present, date/logo present, white title card present
(v1's card is axis-aligned/unrotated rather than slightly tilted — a very minor style difference,
not a missing element), 3 stat badges present with real numbers and captions. All key structural
elements are present and correctly proportioned; this recreation already matches well.
**Sample 20 outcome**: CONFIRMED DONE (v1, no rebuild needed). Re-checked against the full
composition description above — every listed element is present and correctly proportioned. Only
a very minor style delta (card rotation) that doesn't rise to a missing-element fail. No iteration
required.

## Sample 21 — full composition description (written BEFORE v2)
Full-bleed sky-blue bg. Z-order back-to-front:
1. Yellow ribbon/squiggle accent lines (3-4, thick, curved) bleeding off canvas edges, scattered
   behind everything.
2. Small italic script logotype "CLASSICO Peninsula" top-center (v1: "aquaterra presents", fine
   swap).
3. Doubled/echoed headline "SATURDAY 28TH" x2 stacked (yellow behind, outline/black in front,
   slightly offset) — v1 matches this well.
4. A TIGHT WOVEN NET/MESH (like a string produce-bag) — pink/red criss-crossing lines that
   CONVERGE at a narrow point top and bottom and BULGE outward in the middle, genuinely wrapping
   around and containing the object cluster like a bag — v1's red lines are a loose scattered
   crosshatch with no converging bag silhouette, they just cross randomly behind the objects
   rather than visually enclosing them.
5. Inside the net: a bottle (dark, tequila-style label), a disco-ball sphere, a soda cup with straw
   — v1 substitutes flat doodle icons (ring, leaf, thumbsup) for these, a reasonable style
   abstraction given the "real assets only" rule, acceptable.
6. TWO oval callout badges overlapping the net, at different heights: yellow oval "THE LAST
   SATURDAY OF THE YEAR" (upper, over the bottle), blue oval "DJS PLAYING HERNANIB ATALO" (lower-
   middle, over the disco ball) — v1 has only ONE oval badge ("LAST DRIVE OF THE YEAR"), missing
   the second oval entirely.
7. Bottom-left: "RESERVATIONS +18" bold + phone numbers + price line; bottom-right: two sponsor
   wordmarks (v1: "hosted by aq crew" + "free entry" + handle, fine swap).
v1's biggest misses: (a) the net/mesh lines are a loose scattered crosshatch, not a converging
bag-silhouette net that visually wraps the object cluster; (b) only one of the two oval callout
badges is present — the second ("DJS PLAYING...") is missing entirely.

**Sample 21 outcome**: DONE (v2, 1 iteration). v1's second oval badge ("hosted by aq crew") was
rendered with a background color identical to the page background, making it functionally
invisible — only its white text showed, floating with no visible shape (a real bug, not a style
choice). The net-mesh lines were also a loose random crosshatch instead of a converging bag
silhouette. v2 fixed the badge's background color to a visible accent, and reshaped the net lines
to converge to a narrow point top and bottom with a bulge in the middle, matching the reference's
wrapped-bag look. All composition-description items now visibly present.

## Sample 22 — full composition description (written BEFORE v2)
Sky-blue gradient bg WITH visible white cloud texture/shapes throughout (not a flat gradient —
v1's bg has no clouds at all). Z-order back-to-front:
1. Cloud texture: soft white blob shapes scattered across the whole bg.
2. ~6-7 thin blue-line CHALK-STYLE doodle sketches scattered in the gaps (an amp/mascot character,
   a spiky 4-point star x2, a small poodle silhouette, a lightning bolt, a heart, a UFO) — v1 has
   only 2 tiny doodles (a small star + a squiggle), missing the amp mascot, poodle, lightning,
   heart, and UFO chalk sketches entirely.
3. ~8 real-object toy/item cutouts mounted on white circular drop-shadowed discs, scattered around
   the headline (guitar, dinosaur toy, rock/gem, frog toy, 2 boba-tea cups, nutcracker toy, plus
   one more) — v1 has only 4 discs (globe, paw, leaf, thumbsup doodle icons — a reasonable content
   swap given real-photo-object restrictions, but the COUNT is roughly half the reference's ~8).
4. Torn-paper strip banners: kicker "2023 RIIZE 100 DAYS PARTY" (v1: "AQ 100 DAYS PARTY", fine
   swap), bubble-letter bold headline "HELLO, RIIZE" on a larger white strip (v1: "HELLO, SHOW
   UP.", fine swap), date strip "2023.12.17 (SUN) 2PM/7PM" (v1 matches format), yellow venue strip
   "KWANGWOON UNIVERSITY, DONGHAE ARTS CENTER" (v1: "AQUATERRA HQ, KOLKATA", fine swap).
5. TWO small logo/brand marks bottom-center (v1 has none — only a bottom-left handle text, missing
   the centered logo-mark pair entirely).
v1's biggest misses: no cloud texture in the background (flat gradient instead), only 2 of ~7
chalk-doodle sketches present (missing amp mascot, poodle, lightning, heart, UFO), only 4 of ~8
disc-mounted object icons (half the reference's density), and the two bottom-center logo marks are
completely absent.

**Sample 22 outcome**: DONE (v2, 1 iteration). v1 had a flat gradient bg (no clouds), only 2 of ~7
chalk-doodle sketches, only 4 of ~8 disc-mounted object icons, and no bottom-center logo marks. v2
added blurred cloud shapes, 2 more disc-mounted icons (star, heart), 3 more chalk doodles
(speech-bubble, spiral, cross), and two small logo-mark chips bottom-center. All composition-
description items now visibly present.

## Sample 23 — full composition description (written BEFORE v2)
Periwinkle-blue outer bg, framed rounded-corner card inset from the edges. Cream nav strip top of
card: bold caps "work" left, italic cursive wordmark center, WhatsApp-style phone-icon glyph FULLY
VISIBLE top-right (v1's equivalent icon is clipped/cut off at the card's right edge, only a
fragment "2" visible — a real rendering bug, not a style choice). Blue body below: 3 pill-labeled
info blocks in a row ("looking for a job?" / "office" / "contact", each with a bold 2-line answer
+ "Google Maps" link under the office block) — v1 matches this structurally. A row of THREE small
social-icon glyphs (LinkedIn, Instagram, TikTok) below the contact block — v1 has NONE, missing
entirely. Small disclaimer italic line under the contact email. Giant cream cursive wordmark
"truus" spanning the bottom of the card, with SIX small sticker/doodle accents pinned across and
along the wordmark: orange starburst "BAM", blue circle smiley, pink heart w/ sparkle accents,
green hand-heart-gesture sticker, pink "100" emoji sticker, black camera-with-crown sticker — v1
has only 4 generic doodle icons (globe, thumbsup, leaf, sparkle) pinned on its wordmark, missing
2 of the 6 and using generic AQ icons instead of the varied sticker types. Small black "credits"
pill bottom-right corner (v1 matches this).
v1's biggest misses: (a) the phone/WhatsApp icon top-right of the nav is clipped by the card edge,
only a fragment visible — a real bug; (b) the row of 3 social-media icon glyphs (LinkedIn,
Instagram, TikTok) is completely absent; (c) only 4 of the reference's 6 sticker accents are
present on the wordmark.

**Sample 23 outcome**: DONE (v2, 1 iteration). v1's phone icon was clipped at the nav's right edge
(only a fragment visible), the 3 social icons were completely absent, and only 4 of 6 sticker
accents were present on the wordmark. v2 wrapped the phone icon in a proper circular badge with
padding so it renders fully, added a 3-icon social row (LinkedIn/Instagram/TikTok placeholders),
and added 2 more stickers (burst, heart) to reach 6. All composition-description items now visibly
present.

## Sample 24 — full composition description (written BEFORE v2)
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

## Sample 25 — full composition description (written BEFORE v2)
NOTE: reference is one slide ("table of contents") from a multi-slide portfolio-deck moodboard;
prior session correctly picked this slide's mechanism to recreate as a single AQ poster. Cream bg.
Z-order back-to-front:
1. Small caps label "TABLE OF" top-center, oval outline decoration nearby (v1 omits the oval).
2. Giant rainbow-per-letter bold rounded title "CONTENTS" (v1: "AQUATERRA", fine swap), each
   letter a different accent color, with a squiggly underline beneath part of the word and small
   star/sparkle accents woven between letters — v1's title has no underline squiggle and no
   inter-letter sparkles, only 2 large corner sparkles far from the title.
3. A big star OUTLINE shape (not filled) upper-right near the title, plus 2-3 additional small
   sparkle accents scattered near the title (upper-left small star, small blue diamond sparkle) —
   v1 only has 2 sparkles total, positioned as corner bookends rather than woven around the title.
4. Eight colored pill-tag buttons ("01."–"08." + labels) scattered in a loose arc, each a different
   accent color, rotated a few degrees — v1 matches this well (8 pills present, good color variety).
5. Pink envelope illustration below the pills: a V-notch envelope body, with a WHITE LETTER/CARD
   shape peeking out from the top opening (partially visible triangle of white paper) — v1's
   envelope is a solid pink V-shape with NO white letter peeking out, missing this detail.
6. A thick green squiggle/wavy divider line near the bottom of the slide — v1 has no such divider
   at all, and the bottom half of the canvas (below the envelope) is empty dead space.
v1's biggest misses: no squiggle underline or inter-letter sparkles on the title, no star-outline
accent, no white letter peeking from the envelope, no green squiggle divider, and the bottom half
of the canvas (roughly y1300-2700) is empty with nothing placed there at all.

**Sample 25 outcome**: DONE (v2, 1 iteration). v1 was missing: squiggle underline beneath the
title, star-outline accent + inter-letter sparkles woven near the title (only 2 corner-bookend
sparkles present), a white letter peeking out of the envelope's V-notch opening, a green squiggle
divider, and had a completely empty bottom half of the canvas (~y1300-2700). v2 added: a pink
squiggle SVG underline under the title; a black star-outline polygon plus 2 extra small sparkles
woven near the title (4 sparkles total, varied color/rotation); a white clip-path triangle
positioned behind the envelope so it peeks through the V-notch opening; a green squiggle-divider
SVG spanning the canvas width; and a new lower section with bold headline "every lane, one
drive." filling the previously-dead bottom half. Visually verified against the render: all 8
composition items present and correctly proportioned — title with rainbow letters, "table of"
label, squiggle underline, star-outline + 4 sparkles, 8 colored pills, envelope with visible
white letter peek, green squiggle divider, and the new bottom section. No further iteration
needed.

## Sample 26 — full composition description (written BEFORE v2)
Reference: 8988345ad4963ec66e5754c8c5441f56.jpg ("Sticker Kit")
- Background: flat light gray (#E9E8E6-ish), no texture.
- Top-left: "Sticker Kit" header text, large bold sans, dark gray, ~y40-70.
- Top-right: dark pill badge "1/3" (page counter), rounded, gray fill white text, ~x670-730,y30-65.
- Sticker cluster (loosely piled, overlapping, varied rotation), roughly z-ordered top-to-bottom
  as physically stacked (later listed = higher z / on top):
  1. Googly-eyes rounded-square sticker (white bg, black border, two black-ringed eyes with
     black pupils) — top-left area, ~x110-210,y195-280, slight white drop-shadow/outline (sticker
     die-cut look), rotation ~-5deg.
  2. Blue oval sticker "anti-social but / user-friendly" (cursive italic 2nd line) — royal blue
     fill, white text, ~x225-470,y135-235, rotated ~+8deg, positioned overlapping/behind eyes.
  3. White rect sticker "Out of Office" bold black text with small corner selection-handle marks
     (crop-tool style corner brackets, purple) — ~x160-390,y255-310, rotation ~-3deg, sits atop
     the blue oval's bottom edge.
  4. Orange/red flame emoji-style sticker (flat orange flame shape, white die-cut outline) —
     ~x415-480,y225-300, rotation ~+3deg, sits to the right of Out-of-Office tag.
  5. Blue globe/world sticker (circular, blue grid-line globe icon with googly eyes on it,
     black outline) — ~x510-610,y210-345, rotation 0.
  6. Red heart sticker with white "⌘" (command-key) symbol cut into center — ~x120-270,y330-460,
     rotation ~-8deg, sits behind/below Out-of-Office and flame.
  7. Red rect nametag sticker "HELLO, I'M" (small label) + "User Friendly" (large cursive
     signature) — white/red bg card, ~x270-520,y325-450, rotation ~-2deg, overlaps heart's
     right edge.
  8. Green peace-sign hand sticker (2-finger V, cartoon hand, black outline, light green skin
     tone) — ~x535-635,y335-450, rotation ~+10deg, to the right of nametag card.
  9. "I ❤️ MY JOB" text lockup (bold black sans + small red heart glyph) — ~x500-635,y480-565,
     no card/background, sits directly on the gray bg beneath globe/peace-hand.
  10. Purple peace-sign hand sticker — smaller, ~x90-175,y430-520, rotation ~-6deg, left side,
      below heart.
  11. Circular badge "Sand Studio & Co." with curved text along the badge's own circumference
      arcing around a smaller inset badge — off-white circle, black outline, black text,
      ~x290-460,y460-635, rotation slight.
  12. Cursor/arrow icon (small black filled cursor-pointer shape) — ~x95-130,y550-590, sits at
      the edge of the "Designer" pill.
  13. White pill sticker "Designer" (black outline, black bold text) — ~x115-275,y590-635,
      rotation ~-4deg, overlaps cursor icon's tail.
  14. Light-green oval sticker "Professional / Instance Detacher" (cursive + bold 2-line text)
      — ~x185-360,y635-715, rotation ~-3deg, bottom-left cluster.
  15. Yellow rounded-rect sticker "Please / Detach with care" + small keyboard-shortcut glyph
      row ("\ ⌘ B") — ~x420-675,y620-735, rotation ~+2deg, bottom-right.
  16. Dark teal peace-sign hand sticker — ~x390-460,y690-770, rotation ~-8deg, bottom-center,
      overlapping the green oval's right edge and yellow card's left edge.
- Footer row: "@sandstudio.co" bottom-left (small gray text), "Buy Now →" bottom-right (bold
  black text + arrow glyph) — ~y850, both sit on flat gray bg, no cards.
- Overall density: cluster occupies roughly the vertical middle 70% of canvas (y130-770 of a
  ~910px-tall image), quite tightly packed/overlapping with almost no gaps between stickers;
  header and footer are the only elements outside the cluster.

v1 (out/versions/8988345ad4963e/v1.png) gaps vs this description:
- Bottom half of canvas (~y1900-2700 at full 2160x2700 res) is completely empty — the reference's
  cluster fills much closer to the bottom edge relative to canvas height. v1 stops around y1650.
- Missing: googly-eyes sticker box, flame/fire sticker, cursor/arrow icon near the Designer pill.
- Heart sticker in v1 is a plain flat heart with no cutout symbol (reference has a white ⌘
  symbol cut into the heart's center) — acceptable minor simplification but should add a symbol
  for fidelity.
- Real bug (noted in progress tracker): the purple "thumbsup" doodle is placed ON TOP of the
  "...EER" pill, covering most of its text ("volunteer" reads as just "EER") — a genuine
  z-order/placement collision, not a style choice.
- Reference has 3 peace-sign hands (green/purple/teal); v1 substitutes 3 thumbsup icons in the
  same slots — acceptable doodle-vocabulary swap (peace-sign not in engine/doodles.py), keep.

**Sample 26 outcome**: DONE (v2, 1 iteration). v1 gaps: bottom half of canvas empty, missing
googly-eyes sticker, missing flame sticker, missing cursor/arrow icon, plain heart with no
cutout symbol, and a real z-order bug where the purple thumbsup doodle covered most of the
"volunteer" pill's text. v2 fixed the collision (repositioned the hand doodle clear of the
pill), added the googly-eyes sticker box, a flame-shaped accent, a small cursor triangle beside
the pill, a ⌘ symbol cut into the heart, and a new lower sticker cluster (circle badge, tag,
star, extra hand) filling the bottom half to match the reference's fuller vertical density.
Visually verified: all composition-description items present, "volunteer" pill fully legible,
no further iteration needed.

## Sample 27 — full composition description (written BEFORE v2)
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

## Sample 28 — full composition description (written BEFORE v2)
Reference: abb2ab5d1194e22f4dfbda71dcd98d9f.jpg ("jazz Spring Show" poster, Matisse cut-paper style)
- Background: solid off-white/cream, no texture.
- Scattered bold word-fragments at varied scale/rotation/color, layered as the dominant
  structure (not a single headline block):
  - "jazz" — huge, dark navy, top-left, slight skew, ~x40-290,y15-130.
  - "Spring" — huge, dark navy, mid-right diagonal cursive-ish sans, ~x380-720,y440-650,
    rotated so it reads diagonally down-right.
  - "SHOW" — huge, dark navy bold caps, lower-left, ~x30-330,y690-820.
  - Small caption block top-left under "jazz": 2 lines Chinese small text, ~x150-330,y150-200.
  - Small caption block top-right: 2-3 lines mixed Chinese/English small text (artist credits),
    ~x480-720,y50-140.
  - Purple/lavender hexagon date-card: "27-28 / January 2023 / 16:00 START", ~x385-545,y195-350.
  - "FREE ADMISSION 自由參加 @ 1F, Wave Towers 音浪塔一樓" small caption, left-mid, ~x30-320,y460-505.
  - "爵對有春" (large Chinese title chars), bottom-right, bold navy, ~x430-720,y940-1010.
- Organic Matisse-blob shapes (flat single-color cutout flowers/splats), scattered, varied
  rotation, z-order interleaved with the word fragments:
  - Yellow 5-petal flower, top-right corner, ~x585-720,y10-100, rotation ~+15deg.
  - Pink squiggle/ribbon double-curve, top-center, ~x365-475,y40-105.
  - Red 6-petal flower (large hero blob), left-mid, ~x25-260,y150-330, rotation slight.
  - Small light-blue hexagon, left, ~x25-90,y360-410, partially behind red flower.
  - Green wavy ribbon/arrow shape connecting red flower to hexagon date-card, ~x230-400,y270-360.
  - Green squiggly "S" ribbon blob (large), right side, ~x555-720,y250-390.
  - Yellow thin wavy squiggle line, right side below green ribbon, ~x635-715,y365-455.
  - Small navy megaphone icon (bullhorn, pointing left), left-mid, ~x30-230,y470-560.
  - Small pale-blue hexagon outline/fill, left, repeated motif, ~x30-90,y360-410 (see above).
  - Navy "eyelash" doodle (curved lash marks + dot), center, ~x360-450,y620-660.
  - Small navy hexagon w/ blue dot inside, center-left, ~x190-250,y790-840.
  - Yellow 4-line "speed lines"/hatch mark cluster, lower-mid, ~x510-565,y850-900.
  - Large magenta/pink starburst (8-point jagged star) with small light-blue flower center,
    bottom-right, ~x480-720,y660-820.
  - Green wifi-signal arc icon (concentric quarter-arcs + dot), bottom-left, ~x30-190,y660-780.
- Footer: two small logo marks bottom-left (music-center logo + jazz-records logo), ~y960-1010.
- Overall density: shapes and word-fragments overlap tightly with almost no empty gaps across
  the full canvas height; nothing below y1010 of the ~1035px reference is truly dead space.

v1 (out/versions/abb2ab5d1194e2/v1.png) gaps vs this description:
- Large dead zones: y200-870 in the right/center area is nearly empty (only 3 small shapes:
  hexagon date-card, zigzag squiggle, pink star+DRIVE), and y1400-1750 between DAY and the
  arrow/caption row is empty. Reference has near-zero dead space; v1 is much sparser overall.
- Missing doodle vocabulary present in reference: no megaphone icon, no wifi-signal-arc icon,
  no eyelash doodle, no small hexagon+dot motif, no speed-line hatch cluster.
- Word-fragment scatter (AQ/DRIVE/DAY/SHOW UP) is a reasonable structural echo of
  jazz/Spring/SHOW but v1 has only 4 words vs reference's tighter interleaving of word+blob
  layers — needs more blob variety and tighter spacing to match density.

**Sample 28 outcome**: DONE (v3, 2 iterations). v1 had large dead zones (y200-870 and
y1400-1750 nearly empty) and was missing the megaphone icon, wifi-signal-arc icon, eyelash
doodle, and hexagon+dot motif from the reference's dense blob/word scatter. v2 added a pink
squiggle ribbon, green wifi-arc SVG, a proper megaphone SVG shape, an eyelash SVG doodle, a
hexagon+dot motif, and a yellow speed-line cluster — but the hexagon+dot used CSS
clip-path+border which doesn't render a clean outline in Chromium (rendered as broken bracket
shapes). v3 fixed it with an SVG polygon outline instead. Visually verified: all listed
composition elements present, density now closely matches the reference's near-zero-dead-space
scatter. No further iteration needed.

## Sample 29 — full composition description (written BEFORE v2)
Reference: abd472f264528c60d34cd7bce0e17617.jpg ("My Confessions" scrapbook)
- Background: real photo (grassy outdoor scene, car visible, blurred), covers roughly top 30%
  of canvas, rest of canvas is white/light card area.
- Giant bubble-outline sticker title "My confessions" (2 stacked lines, black outline + white
  fill, playful hand-drawn wobble font), overlapping the photo/white boundary, ~x60-650,y15-250,
  large dominant hero element, slight rotation per-word.
- Small caption text top-right on photo: "i just follow my heart" — thin white sans, ~x480-660,y85-100.
- Small caption text below title on white area: "i got a lot of demon..." — thin gray sans,
  ~x330-660,y255-270.
- Yellow 6-point starburst/sparkle sticker — left side, ~x60-140,y230-290, rotation slight.
- Small coffee-cup icon graphic (white outline, tan fill), top-right on photo, ~x630-680,y135-210.
- White daisy-flower doodle (5 white rounded petals, small), left side, ~x25-95,y495-560.
- Green quatrefoil/loading-icon badge (circular, green arrows), ~x350-430,y495-565, rotated.
- Blue 4-petal flower/asterisk small icon (repeated ~2x as inline emoji-style accents inside
  card text, e.g. "N💠T" and "💠FTEN") — ~x220-250,y540-570 and ~x430-460,y540-570.
- Multiple red tomato stickers (flat red circle w/ green star-shaped stem/leaf on top), varied
  sizes, scattered across the right-side photo-collage card and lower area:
  - Half-tomato (cut cross-section) top-right of a card ~x395-470,y295-350.
  - 3 tomatoes varied size top-right card ~x475-670,y285-420.
  - 2 small tomatoes lower-left of same card ~x395-500,y480-545.
  - 1 tomato bottom-center overlapping cards ~x330-400,y690-750.
- Speech-bubble tag "IS THIS ME? OR NOT?" — blue rounded rect, white text, ~x330-420,y295-360,
  rotated slightly, sits on top-left corner of the tomato-collage card.
- 6+ white note-cards with black bold headline + smaller gray body text, drop-shadow, slight
  rotation each, scattered/overlapping in a loose grid (not a clean 2-col grid — reference's
  cards vary in width/position more than a grid):
  - "OH GOD" card (headline) + blurred grid/photo body + small italic caption below.
  - "IS THIS ME? OR NOT?" speech bubble (separate small element, not a full card).
  - Tomato/confession-text card (mostly filled with tomato stickers + tiny paragraph text).
  - "Y'KNOW, I'M NOT LIKE THIS OFTEN" card + "JUST SOMETIMES" sub-line + blue-flower accents.
  - "12:37 AM" card + small paragraph body text.
  - "free font" bold label + QR code square (black/white) — bottom-left, distinct from other
    cards, no drop-shadow card background, sits directly on white bg.
  - Blue checkered/gingham pattern card fragment, partially visible bottom-left ~x330-460,y660-740.
  - "Am I Going To Give Up Now?" card, bottom, partially cut off at canvas edge.
  - "Here I'm" card, bottom-right, partially cut off.
- Overall: reference is a dense, overlapping scrapbook collage with NO clean grid — cards
  overlap each other's corners, stickers overlap card edges, nothing sits in isolated boxes.

v1 (out/versions/abd472f264528c/v1.png) gaps vs this description:
- Missing signature repeated motif: NO tomato stickers anywhere (reference has ~7 tomatoes
  across multiple cards — a distinctive, repeated visual signature, not a minor detail).
  Real miss, not an acceptable style swap since doodles.py could still produce a red+green
  circle-with-stem shape via inline SVG.
- Missing daisy-flower doodle (v1 substitutes an abstract leaf shape — a doodle vocabulary
  swap, borderline acceptable but the reference's specific white daisy is a recognizable icon).
- Missing green quatrefoil/circular-arrow badge, missing small caption texts ("i just follow my
  heart", "i got a lot of demon"), missing coffee-cup icon.
- v1's 6 cards sit in a clean 2-column grid with even gaps — reference's cards overlap messily
  with no visible grid; this is a real structural difference but was already accepted in the
  original pass as a legible simplification. Given the revisit protocol's stricter bar, will
  add slight overlap/rotation per-card to better match the scrapbook feel, plus add the missing
  tomato stickers and captions.
- QR code swap for "join a lane" pill was already reviewed and is an acceptable real-asset-only
  substitution — keep.

**Sample 29 outcome**: DONE (v2, 1 iteration). v1 was missing the reference's signature repeated
tomato-sticker motif entirely, plus the daisy-flower doodle (substituted with an abstract leaf),
the green quatrefoil badge, and the two small photo captions ("i just follow my heart", "i got a
lot of demon energy"). v2 added inline SVG tomato stickers (5, scattered across the card
cluster), an SVG daisy doodle, an SVG quatrefoil badge, and both captions. Visually verified:
all composition-description items present and proportioned reasonably; card layout retains its
clean-grid simplification from v1 (previously accepted), tomatoes now supply the collage's
signature texture. No further iteration needed.

## Sample 30 — full composition description (written BEFORE v2)
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

## Sample 31 — full composition description (written BEFORE v2)
Reference: b2d4cc55d7fdbbc7294249e7c4d48b27.jpg ("And All That Jazz")
- Background: solid royal blue, no texture.
- Cream bubble-outline headline "AND ALL" — top-center, wavy hand-drawn caps font, ~x90-620,y70-220.
- Cream bubble-outline headline "THAT JAZZ" — bottom-center, same font, ~x60-650,y730-870.
- Center illustration cluster (flat-color hands playing instruments, thick black-less flat
  shapes, tightly packed, minimal gaps), roughly ~x60-670,y225-720:
  - Blue 4-point star (top-left of cluster) ~x75-190,y225-320.
  - Yellow piano keyboard (diagonal, pink+green key accents) with 2 cream cartoon hands playing
    it ~x60-390,y230-450.
  - Red 6-point star (center-top) ~x400-500,y230-320.
  - Small orange 4-point star (center, below red star) ~x440-500,y390-450.
  - Green microphone (mic head + cream hand gripping handle) + yellow curly cable — top-right
    ~x570-680,y230-450.
  - Orange/yellow guitar (body + neck + blue cartoon hand on neck + cream hand strumming) —
    center, diagonal, overlapping piano's bottom-right corner ~x180-450,y270-670.
  - Red music note (small, filled) — left of guitar body ~x100-160,y480-560.
  - Yellow music note (small, filled) — center, between guitar and saxophone ~x330-390,y480-580.
  - Blue/orange saxophone (body + bell + cream/orange hands on keys) — right side, ~x400-670,y440-720.
  - Small orange star (bottom, between guitar and sax) ~x300-350,y650-700.
- Overall density: the illustration cluster is very tightly packed with almost no gaps between
  elements — occupies the full ~500px middle band edge-to-edge; only ~100-150px of clear space
  separates the cluster from each headline.

v1 (out/versions/b2d4cc55d7fdbb/v1.png) gaps vs this description:
- Doodle-vocabulary swap (globe/thumbsup/paw/leaf/sparkles for piano+hands/guitar+hands/
  mic+hand/saxophone+hands) already reviewed as acceptable since engine/doodles.py has no
  hand-drawn instrument icons — keep.
- Real structural gap: v1's cluster occupies only ~y280-1210 loosely spaced with visible empty
  areas between icons, and there's an oversized empty gap (~y1210-1670) between the cluster and
  "SHOW UP." that the reference does not have (reference keeps ~100-150px separation only).
  Needs tightening: pull "SHOW UP." up closer to the cluster to match the reference's tight
  vertical rhythm.
- v1 has 8 decorative elements (globe, thumbsup, paw, leaf, 4 sparkles) vs reference's 9
  illustration groups — close enough in count, acceptable.

**Sample 31 outcome**: DONE (v2, 1 iteration). v1 had an oversized gap (~250px) between the
doodle cluster and the "SHOW UP." headline versus the reference's tight ~100-150px rhythm. v2
pulled the headline up, added a heart doodle and an extra sparkle to bring the cluster closer to
the reference's 9-element density. Visually verified: both headlines, 5-icon cluster, and 5
sparkles/stars present, spacing now matches the reference's tight vertical rhythm. No further
iteration needed.

## Sample 32 — full composition description (written BEFORE v2)
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

## Sample 33 — full composition description (written BEFORE v2)
Reference: c10cb35dfa09cdaa54d4d9911add468c.jpg (Converse ad, 2-panel: torn-notebook-paper card
+ typographic shoe panel; recreating the torn-notebook-paper mechanism per established
single-mechanism precedent)
- Background (top panel): solid blue, with several texture/decoration layers behind the card:
  - Orange felt-marker scribble "m"-shape mark, top-left corner, ~x230-330,y60-130.
  - Gray/black halftone-dot torn paper shape, top-left, partially off-canvas ~x0-140,y0-160.
  - Purple/lavender halftone-dot circle, top-right corner, large, ~x1080-1200,y0-180 (partially
    off-canvas).
  - Orange "3"-shaped coil/spiral squiggle, left edge, ~x0-110,y330-500, partially off-canvas.
  - Lime-green looping coil/ribbon shape, bottom-right of the card, ~x870-1150,y380-580.
- Torn notebook-paper card (grid-paper texture, jagged torn top edge with circular hole-punch
  notches along the tear), ~x150-1040,y150-520, drop shadow.
  - Headline "WE LEAVE" (black bold caps) ~x220-810,y230-310.
  - "your" (small orange italic, underlined) + "MARK" (large lavender bold caps, yellow drop
    shadow/offset) — second line, ~x220-870,y340-430.
  - Black spiral/swirl doodle, immediately right of "MARK", ~x850-960,y270-350.
  - "CONVERSE" wordmark + arrow-star logo, small, black, bottom of card ~x220-720,y460-500.
- Overall: card sits on the blue background with the decorative scribbles/coils/halftone visible
  only in the margins around the card (not overlapping it).

v1 (out/versions/c10cb35dfa09cd/v1.png) gaps vs this description:
- Content swap (AQUATERRA wordmark + arrow for CONVERSE + logo, "our" for "your", added a black
  CTA band "every drive leaves a mark on this city.") — acceptable brand adaptation, keep.
- Missing: the black spiral/swirl doodle beside "MARK" — a distinct, recognizable decorative
  element in the reference, absent in v1. Real miss.
- Missing: orange scribble "m" mark and orange coil/spiral squiggle (v1 has only 2 teal zigzags,
  not matching the reference's specific scribble/coil shapes) — partial doodle-vocabulary swap,
  but the spiral specifically is easy to add via inline SVG and should not be dropped.
- Missing: lime-green looping coil near the card's edge — v1 has none.
- Halftone dot corner present in v1 (yellow, top-right) approximates the reference's dot-texture
  corners reasonably — keep.

**Sample 33 outcome**: DONE (v2, 1 iteration). v1 was missing the black spiral/swirl doodle
beside "MARK", the orange felt-marker "m" scribble mark, and the lime-green looping coil near
the card's edge — all distinct decorative elements called out in the reference. v2 added all
three via inline SVG (the orange coil intentionally bleeds off the left edge, matching the
reference's own edge-bleeding decoration). Visually verified: all composition-description items
present and correctly positioned. No further iteration needed.

## Sample 34 — full composition description (written BEFORE v2)
Reference: c42f94a09f07cda39df8afe51cde9098.jpg ("set:nAFV8beNUC4" sticker set)
- Background: flat cream, no texture.
- Top-center: "set:nAFV8beNUC4" bold black label, ~x400-820,y120-165.
- 9 sticker illustrations scattered in a loose cluster, each with thick black outline + flat
  color fill + soft drop-shadow "sticker" halo:
  1. Browser/window icon (mint outline box with title-bar dots/icons at top, empty white body) —
     top-left, ~x195-420,y425-600, slight rotation.
  2. Pink scalloped-blob "YOU GOT THIS!" badge (wavy sticker-cut edge, bold black text 3 lines)
     — top-center, ~x445-680,y385-620.
  3. Orange pencil illustration (diagonal, eraser+ferrule+wood+tip detail) — top-right,
     ~x705-895,y430-560, rotated ~+35deg.
  4. Yellow party-horn/cone icon (striped cone + confetti shapes: triangle, circle, diamond) —
     left-mid, ~x330-560,y590-690, rotated.
  5. Purple wavy ribbon "PRESENTATION" (curved banner shape, bold black text following the curve)
     — right-mid, ~x695-985,y560-700.
  6. Green ring/donut "GO TEAM! GO TEAM!" (circular text repeating around a thick ring) —
     left, ~x225-520,y675-880.
  7. Blue hand "snap"/finger-snap doodle (cartoon hand with motion lines) — center,
     ~x520-730,y645-800.
  8. Tan arch-shaped "UPLIFT EACH OTHER" badge with 2 small face icons inside (smiley square +
     smiley hexagon, stacked) — center-bottom, ~x495-665,y800-1120.
  9. Green upward arrow (bent, hand-drawn zigzag arrow) — bottom-left, ~x310-460,y900-1010.
  10. Blue laptop illustration (screen+keyboard, flat color) — bottom-center-right,
      ~x650-850,y815-990.
  11. Pink gear/cog icon (thick outline, circular) — bottom-right, ~x805-965,y875-1040.
- Bottom: small gray handle "@CREATIVEHAUSMKTG" centered, ~y1385.
- Overall: cluster occupies the vertical middle ~40% of canvas (y385-1120), large empty margins
  above (y165-385) and below (y1120-1385) — a deliberately sparse "sticker sheet" layout.

v1 (out/versions/c42f94a09f07cd/v1.png) gaps vs this description:
- Missing 6 of 11 reference stickers: browser/window icon, pencil illustration, party-horn/cone
  icon, hand-snap doodle, laptop illustration, gear/cog icon. v1 only has 5 sticker equivalents
  (blob, ribbon, ring, arrow, arch) plus 2 substituted AQ doodles (thumbsup, globe-badge) = 7
  total vs reference's 11. Real miss — over half the sticker set is absent, not just a style swap.
- "RECRUIT" ribbon substitutes "PRESENTATION" (content swap, acceptable), "GO TEAM, GO TEAM"
  ring matches well, arrow/arch/blob all present and well-matched.
- Vast empty top/bottom margins already match the reference's deliberately sparse sticker-sheet
  layout — NOT a bug, keep as is.

**Sample 34 outcome**: DONE (v2, 1 iteration). v1 had only 5 of the reference's 11 stickers
(plus 2 unrelated substitutes), missing the browser/window icon, pencil illustration,
party-horn/confetti icon, hand-snap doodle, laptop, and gear — over half the sticker set. v2
added all 6 via inline SVG/CSS (a proper 8-tooth gear replacing the earlier globe-in-circle
badge that didn't read as a gear). Visually verified: all 11 composition-description stickers
present, minor intentional overlaps consistent with the reference's own sticker-pile style. No
further iteration needed.

## Sample 35 — full composition description (written BEFORE v2)
Reference: ca484173fb52871d5f058102020b036c.jpg (SaaS website mockup: "About" hero + "Project
Line" gantt card)
- Outer frame: black/near-black border margin around the whole canvas.
- Top panel: solid royal-blue rounded card, ~x40-1160,y55-710.
  - Small white text "Promox Saas Website" top-left ~x60-170,y65-80.
  - Small white text "Promox." top-center ~x420-465,y65-80.
  - Small white ".04" top-right corner ~x1130-1150,y70-80.
  - Partial white circle decoration, left edge, half off-canvas ~x30-90,y155-205.
  - Giant white/light-blue wordmark "About" ~x60-700,y360-560.
  - 3-line body paragraph, white/light text, ~x60-680,y580-655.
  - 8 colored rounded-pill company badges (logo + name), scattered in a loose diagonal stack,
    rotated at varied angles, right side, partially bleeding off the right edge:
    1. Red "Airbnb" pill, top ~x905-1150,y75-150.
    2. White "Microsoft" pill ~x800-965,y175-220.
    3. Yellow "Goldman Sachs" pill (partially cut at right edge) ~x1010-1160,y175-235.
    4. White "Apple" pill ~x785-990,y240-330.
    5. Lavender "PepsiCo" pill (partially cut) ~x1005-1160,y280-330.
    6. Blue "Google" pill ~x825-1055,y365-435.
    7. Peach "Bank of America" pill ~x785-1105,y490-565.
    8. Green "Netflix" pill ~x800-1000,y600-670.
    9. Lavender "Amazon" pill (mostly cut off at right edge) ~x1090-1160,y615-670.
- Bottom panel: solid white rounded card, ~x40-1155,y715-1345.
  - "/ Project Line" bold black heading (slash prefix) ~x125-400,y765-815.
  - 4 column headers "Week-1/2/3/4" ~x100-1075,y885-910.
  - Faint vertical grid divider lines between week columns.
  - Day labels row "Sun Mon Tue Wed Thu Fri Sat" ~x100-1100,y955-975.
  - 4 staggered horizontal gantt bars (rounded pill, colored, white icon-chip + label left, white
    circle "handle" right), each starting further right and ending further right than the one
    above (true diagonal cascade, not just left-indent):
    - Blue "Research" bar, shortest, ~x100-330,y1035-1080.
    - Green "Strategy" bar, ~x170-545,y1105-1155.
    - Peach "UX Design" bar, ~x420-795,y1195-1245.
    - Purple "UI Design" bar, ~x670-1045,y1275-1320.

v1 (out/versions/ca484173fb5287/v1.png) gaps vs this description:
- Missing the partial white circle decoration on the blue panel's left edge.
- Pill badges: v1 has 6 program-name pills (WELFARE/CLIMATE/EDUCATION/RECRUIT/SHIKSHAQ/EVENTS)
  vs reference's 8 company badges — acceptable content swap (AQ programs vs literal company
  logos, real-assets-only rule), count is close enough.
- Gantt bars: v1's 4 bars (FOOD DRIVE/TREE PLANTATION/HEALTH CHECKUP/CLOTHING DRIVE) already
  cascade with increasing start-indent, reasonably matching the reference's staggered rhythm —
  acceptable, though v1's bars all extend to nearly the same right edge rather than each ending
  at a distinct point like the reference — minor proportion difference, not a structural miss.
- This sample was previously flagged as the tightest per-axis metric match (all deltas <0.1) —
  revisit confirms the structure holds; only the white circle decoration is a genuine miss.

**Sample 35 outcome**: DONE (v2, 1 iteration). v1 was already the tightest per-axis metric
match from the original pass; the revisit found one genuine miss — the partial white circle
decoration bleeding off the blue panel's left edge, present in the reference. v2 added it.
Visually verified: hero headline, body copy, 6 program pills, white circle accent, and the
4-bar staggered gantt chart with week/day labels all present and proportioned correctly. No
further iteration needed.

## Sample 36 — full composition description (written BEFORE v2)
Reference: ce6fdd94f81b3e6018bc80724ae4508e.jpg ("ThriftHaus" event/brand moodboard)
- Background: solid black, no texture.
- Blue card, top-left: "AN EVENING WITH" bold caps + "ThriftHaus" italic serif wordmark,
  ~x55-365,y230-420.
- Pink oval "THRIFTHAUS" small tag + yellow circle "TH" mark, overlapping blue card's right
  edge, ~x185-345,y285-330.
- Orange/red card, top-right: small paragraph body text (justified caps), ~x360-645,y285-435.
- Purple cloud-shaped blob badge "TH" (large scalloped edge), top-right corner, ~x565-690,y230-355.
- Green sun/starburst icon (circle + radiating lines), right of purple blob, ~x570-670,y390-450.
- "20% OFF EVERYTHING" — "20%" in pink oval tag + "OFF EVERYTHING" bold black caps, left-mid,
  ~x55-365,y490-580.
- Small yellow cap/hat doodle icon, above "OFF", ~x120-175,y475-505.
- Small photo of folded jeans on white bg, ~x260-360,y495-565.
- Photo panel, right side: blue sky + green hill, 3 pairs of jeans hanging (product shot),
  "ThriftHaus" italic wordmark overlay, black outline flower doodle bottom-left, black outline
  squiggle/loop doodle, small price-tag card ("size 4, slim skinny, $30" + circular logo stamp)
  bottom-right — ~x360-690,y450-720.
- Photo, bottom-left: woman in overalls, arms raised, outdoor sky/field — ~x55-360,y610-850.
  Small yellow speech-bubble "TH" tag overlapping top-left corner of photo.
- Orange loop/coil squiggle doodle, bottom-left margin, ~x25-140,y800-870.
- Green pill tag "THRIFTHAUS" small, ~x310-430,y755-790.
- Yellow rotated tag "THANK YOU" bold black caps, ~x260-450,y755-810.
- Pink oval "THRIFTHAUS" large, bottom-right, ~x480-690,y775-840.
- Overall: dense collage cluster occupies roughly the top 80% of canvas (y230-870 of ~1100px),
  bottom ~20% is empty black margin.

v1 (out/versions/ce6fdd94f81b3e/v1.png) gaps vs this description:
- Real bug: the orange card's body text overflows behind/gets visually cut off by the purple
  "AQ" blob badge overlapping its right edge ("...OF TH", "WEL...", "...T...ONLY" all clipped
  by the badge sitting on top) — text is illegible where the badge overlaps.
- Real bug: the bottom-left photo's caption text "STANDING STEADFAST FOR THE ONES WHO NEED US
  MOST" is clipped at the photo's bottom edge — second line cut off.
- Structural swaps (real AQ photos instead of literal thrift-store product shots, AQ program
  copy instead of ThriftHaus copy) are acceptable per real-assets-only rule — keep.
- Missing decorative doodles: no flower, no squiggle-loop on the photo panel, no sun icon, no
  small jean/tag photo — but these were swapped for real-asset equivalents already (badges,
  zigzag) which is an acceptable simplification; the 2 clipping bugs are the real fails.

**Sample 36 outcome**: DONE (v2, 1 iteration). v1 had two real bugs: the orange card's body
text ran underneath and was clipped by the purple "AQ" badge, and the bottom-left photo's
baked-in caption ("standing steadfast for the ones who need us most") was cropped off at the
container's bottom edge because the container height didn't match the photo's true aspect
ratio. v2 narrowed the orange card's text column to end before the badge, and resized the photo
container to the photo's actual aspect ratio so the full caption is visible. Visually verified:
both cards fully legible, all composition elements present. No further iteration needed.

## Sample 37 — full composition description (written BEFORE v2)
Reference: cfec9bd415fff2e8fc3ebd264932e783.jpg (flat-lay desk-scene illustration)
- Background: navy-blue speckled/dotted texture, full canvas.
- Double-layered cutting mat: an orange rect peeking out from behind (top-right and bottom-left
  corners visible, offset ~15px), with the green cutting-mat on top, ~x60-930,y60-680.
- Green mat surface: white grid lines, plus a ruler scale — numbers "1" through "13" printed
  along the left edge, small tick marks along the top edge, white inner border/frame line
  inset slightly from the mat's edge.
- Small green crown/leaf glyph, top-center above the mat, ~x365-400,y40-55.
- White filled circle, small, top of mat ~x300-340,y65-100.
- Yellow heart shape, top-center, ~x345-390,y95-135.
- Red/orange diamond (rotated square), top-left area, ~x285-335,y135-175.
- Torn/cut notecard (pink-to-green gradient wash), rotated, occupies center-left of mat,
  ~x175-635,y150-495. Cursive squiggle "doodle writing" in green/blue marker scrawled across
  it (illegible scribble, not real text) + small orange flower-face doodle top-right corner
  of the card.
- Yellow pencil (two-tone: yellow barrel + graphite tip + pink eraser band), diagonal, bottom-
  left corner of card, ~x195-355,y380-620.
- Orange mug with tea bag string+tag, white-to-green gradient coffee/tea surface, 2 small
  bubble/steam dots, ~x635-800,y130-330.
- Blue-and-pink two-tone eraser, ~x745-885,y310-410.
- Red/orange circle badge (small, plain), ~x730-815,y375-440.
- Pink diamond sticker with black heart + 2 small teal dots, bottom-center, ~x510-610,y525-620.
- Yellow set-square/triangle ruler (with small ruler holes along the hypotenuse edge), bottom-
  right, ~x670-930,y445-635.
- Overall: mat is densely packed with the note card + 8 small object/doodle accents; almost no
  empty green mat space is visible.

v1 (out/versions/cfec9bd415fff2/v1.png) gaps vs this description:
- Missing the ruler tick-mark/number scale (1-13) along the mat's edges — a defining structural
  detail of a cutting mat, entirely absent in v1.
- Missing the double-layered mat (orange peeking from behind) — v1's mat sits directly on the
  dotted bg with no offset second layer.
- Missing: mug/tea illustration, eraser, red circle badge, 2 diamonds, pink heart-diamond
  sticker — v1 has only 2 shape accents (red arch blob, purple rect) vs reference's ~8 distinct
  small objects/doodles. Real miss — v1's mat area reads sparse where reference is dense.
  ("thumbsup" and "leaf" doodles substitute acceptably for hand-drawn heart/flower doodles, but
  don't cover the missing count.)
- Pencil present in v1 (plain yellow bar) vs reference's detailed two-tone pencil with tip —
  acceptable simplification given engine doodle limits, but could be improved with inline SVG.
- Content swap ("plan your next drive here." for illegible scribble text) is an acceptable
  adaptation.
- Metric note from original pass (vdr diverges due to flat-vector vs gradient-photo rendering)
  reconfirmed as a structural metric limitation, not a visual bug — not chased further.

**Sample 37 outcome**: DONE (v3, 2 iterations). v1 was missing the ruler tick-mark/number
scale, the double-layered mat effect, and most small objects (mug, eraser, red circle, 2
diamonds, heart sticker) — only ~2 of ~8 accents were present. v2 added all missing elements
(numbered ruler 1-13, SVG mug+tea-tag, 2-tone eraser, red circle, 2 diamonds, heart-diamond
sticker, improved 2-tone pencil, dotted-edge triangle) but the double-layer mat only peeked out
as a thin sliver at the bottom (uniform padding instead of a diagonal offset). v3 fixed the
offset so the orange under-layer peeks at the left and bottom edges, matching the reference's
corner-peek effect. Visually verified: all composition-description items present. The
originally-noted vdr metric divergence (flat-vector vs gradient-photo reference) remains a
structural metric limitation, not a visual defect. No further iteration needed.

## Sample 38 — full composition description (written BEFORE v2)
Reference: d252704dc5e5f32f202f854401f845fe.jpg ("Relationship Series" split-panel type-sandwich)
- Top panel: solid black, ~y0-745.
  - Giant cream italic serif headline "Relationship / Series" ~x40-980,y110-460.
  - Highlighter-box words "IT'S NOT" (light-blue bg, cream text) + "YOU" (cream bg, black text)
    staggered/overlapping at slight rotation ~x30-1170,y460-680.
  - Second highlighter row "IT'S" (blue) + "ME" (blue) ~x140-780,y680-830.
  - Cream 8-point starburst, top-right corner, partially bleeding off-canvas ~x1000-1200,y100-330.
  - Right edge: vertical stripe column (pink/blue diagonal stripes) ~x1030-1090,y0-745, AND a
    blue/lavender checkerboard block behind/overlapping the starburst ~x1090-1200,y0-330.
- Bottom panel: solid cream, ~y745-1200(crop).
  - Thin blue grid/checker vertical strip along the far-left edge ~x0-35,y745-1200.
  - Red/pink checkerboard block, left side ~x35-490,y745-1200 (bleeds off bottom edge).
  - Black 10-point starburst, overlapping the checkerboard's right edge ~x330-520,y940-1130.
  - Giant black bold serif body text "Becoming the person YOU are called to be in
    relationship..." bleeding off the right AND bottom edges ~x600-1200,y790-1200+.

v1 (out/versions/d252704dc5e5f3/v1.png) gaps vs this description:
- Content swap ("drive series." / "show up. that's it." / "becoming the volunteer you're
  called to be in this city.") for the reference's literal copy — acceptable brand adaptation.
- Missing: the blue/lavender checkerboard block behind the top-right starburst — v1 has only
  the diagonal stripe column, no checkerboard layer.
- Missing: the thin blue grid/checker strip along the bottom panel's far-left edge — v1's
  bottom panel starts directly with the pink/orange checkerboard block, no blue strip before it.
- Structure otherwise matches well: black top panel with italic headline + staggered highlight
  boxes + starburst + stripe edge; cream bottom panel with checkerboard + black starburst +
  giant bled-off body text.

**Sample 38 outcome**: DONE (v2, 1 iteration). This was already one of the strongest structural
matches from the original pass; the revisit found 2 genuine misses — the blue/lavender
checkerboard block behind the top-right starburst, and the thin blue grid/checker strip along
the bottom panel's left edge. v2 added both. Visually verified: black panel with italic
headline, staggered highlight boxes, starburst + stripe + checkerboard corner, and cream panel
with left checker strip, checkerboard block, black starburst, and bled-off body text all
present. No further iteration needed.

## Sample 39 — full composition description (written BEFORE v2)
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

## Sample 41 — full composition description (written BEFORE v2)
Reference: e9d82bbdf040cf13b8d261baa678f1e3.jpg ("Google in humanz" brand-site landing hero)
- Background: flat off-white/lavender-white, no texture.
- Top-left: red ring/arc (partial circle, thick stroke), bleeding off top-left corner, ~x0-95,y0-100.
- Below it: solid red rect, partially off-canvas left edge, ~x0-90,y150-185.
- Top-center: small solid yellow rect, ~x280-320,y15-70.
- Top-right nav: "Templates / Personal / About us" thin gray text row + black rounded pill
  button "Font" ~x455-680,y45-60.
- Giant multicolor per-letter wordmark "Google" (each letter a different brand color: blue,
  red, yellow, blue, green, red) + small "1" superscript, ~x175-460,y210-290.
- Black rounded pill "Let's go / It's plato" (2-line white text), right of "Google", ~x460-630,y215-285.
- Blue paint-splash/swirl icon (abstract liquid blob shape), right of the pill, ~x555-630,y210-290.
- Yellow "S"-shaped squiggle/ribbon doodle, left-center, ~x115-190,y300-390.
- Phone-mockup card (white, black outline, rounded corners) with a small profile-card UI
  (teal icon + 2 text lines) inside, ~x155-300,y285-410.
- Megaphone icon (yellow horn + red gripping hand + green confetti burst), overlapping the
  phone's right edge, ~x270-340,y290-350.
- "¡Come back!" bold black text + 2 small pill buttons (red "Now!" + blue "Star"), right of
  megaphone, ~x310-450,y325-375.
- Black arrow cursor icon, pointing up-left, ~x450-500,y350-400.
- "in" (large black text) continuing the sentence, far right, ~x500-555,y320-380.
- "humanz" giant black bold word, bottom line, with "nz" underlined, ~x175-475,y395-475.
- Solid blue rect, right of "humanz", ~x525-590,y425-465.
- Small caption row "Nuevo torneo / Game Evaluation" with tiny icon, below phone ~x175-260,y460-480.
- "Log in / Full coverage list" gray caption text + "20 / 25" + PlayStore icon+text, ~x175-355,y505-525.
- Bottom-right: 3 overlapping ring/circle shapes (blue ring, yellow ring, white filled circle
  behind), large, bleeding off the bottom-right corner, ~x480-730,y490-730.
- Bottom-left: "ALL RIGHTS RESERVED" small gray caps text, ~x15-95,y695-715.
- Bottom-center: small solid green rect, ~x215-380,y715-730.

v1 (out/versions/e9d82bbdf040cf/v1.png) gaps vs this description:
- Missing: yellow squiggle "S" doodle (left-center), missing megaphone icon (substituted with a
  plain curved arrow — acceptable swap but the megaphone's confetti-burst detail is lost),
  missing top-center small yellow rect, missing bottom-center small green rect, missing the
  white filled circle layer behind the blue/yellow rings (v1 only has 2 rings, not 3 layers).
- Content/nav swap ("drives/about/join" for "templates/personal/about us/Font") is acceptable.
- Structure otherwise matches very closely: multicolor wordmark, black pill, phone mockup,
  come-back card, arrow cursor, "20/25" stat, bottom-right ring cluster, footer credit — already
  flagged as one of the closest scale matches in the original pass.

**Sample 41 outcome**: DONE (v2, 1 iteration). v1 was already one of the closest scale matches;
the revisit found real gaps: missing yellow squiggle "S" doodle, missing top-center yellow rect,
missing bottom-center green rect, and only 2 ring layers instead of the reference's 3 (no white
filled circle behind the blue/yellow rings). v2 added all four. Visually verified: multicolor
wordmark, black pill, phone mockup, arrow-cursor, stat row, and full ring cluster all present
and proportioned correctly. No further iteration needed.

## Sample 42 — full composition description (written BEFORE v2)
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

## Sample 43 — full composition description (written BEFORE v2)
Reference: fc9ff902078e2044e28b7356e3015f71.jpg ("Chuckle" pitch-deck template marketplace
listing; picked the cover-slide mechanism per established single-mechanism precedent)
- Background: flat off-white/light gray, no texture.
- Giant bubble-outline wordmark "CHUCKLE" (orange fill, black outline, playful rounded font with
  a small decorative swirl/loop accent on the "C"), top-left, ~x40-620,y60-160.
- Subtitle "Pitch Deck Presentation Template" thin black serif/sans, below wordmark, ~x40-680,y175-210.
- Small white rounded-square Figma icon badge (black outline), ~x45-160,y225-290.
- Purple rounded pill "12 Total Asset" (white bold text), right of Figma badge, ~x175-460,y225-285.
- Tilted photoreal "pitch deck" polaroid card (white photo-frame border, slight rotation),
  center, ~x260-1030,y280-770: desk photo (red lamp, keyboard, plant) with a small red
  "CHUCKLE" corner tag (top-right) and bold black "PITCH DECK" caption overlay (bottom).
- Behind the polaroid, other deck-slide thumbnails peek out (green "the power of art..." slide,
  purple stats card) partially visible at the polaroid's edges — a stacked-deck depth effect.

v1 (out/versions/fc9ff902078e20/v1.png) gaps vs this description:
- Content swap ("AQUATERRA." for "CHUCKLE", "volunteer toolkit template" for "Pitch Deck
  Presentation Template", globe icon for Figma icon, "12 REAL DRIVES" for "12 Total Asset",
  real field-kit photo for the stock desk photo, "FIELD KIT"/"AQUATERRA" tags for "PITCH
  DECK"/"CHUCKLE" tags) — all acceptable adaptations per real-assets-only rule.
- The wordmark's decorative swirl accent (on the "C") is absent in v1's plain text wordmark —
  a minor missing detail, not a structural miss since the swirl is a font-specific flourish
  rather than a separate compositional element.
- The yellow tilted card behind the photo approximates the reference's "stacked deck peeking
  behind the polaroid" effect reasonably — acceptable simplification (single card vs 2 peeking
  slides).
- Bottom color-strip rows (welfare/climate/education/recruit) are an added density-fill below
  the cover mechanism, not present in the reference's cover crop itself — but since the
  reference's full page continues with colorful card rows below the cover, this is a reasonable
  continuation of the page's own visual language, not a fabrication.
- Structure otherwise matches very closely — already flagged as one of the strongest
  recreations in the original pass; revisit confirms no real missing elements.

**Sample 43 outcome**: DONE (v1, 0 iterations — re-checked, no rebuild needed). Re-viewed
against a full composition description of the reference's cover-slide mechanism (bubble
wordmark, subtitle, Figma-icon badge, "12 Total Asset" pill, tilted polaroid photo card with
corner tag + caption overlay). All elements confirmed present with acceptable content
adaptations; only the wordmark's decorative swirl flourish is missing, a minor font detail, not
a structural element. Already one of the strongest recreations in the batch.

## Sample 44 — full composition description (written BEFORE v2)
Reference: ffc106f26f584a842250c4235bcd368e.jpg (vintage-ad poster photographed inside a
shopping basket — perspective/basket framing skipped per real-assets-only precedent; recreating
just the poster content at full scale)
- Orange band, top: "NEW AT" bold black caps, ~y0-155.
- White band: "CHURCH GOODS" bold black caps + thin horizontal rules either side, ~y155-215.
- Yellow body band: "THE" (medium bold) + "MARKET" (giant bold, dominant), black, ~y215-620.
  - Blue 6-point starburst badge, left, overlapping "THE/MARKET" boundary, with cursive black
    text "Buy individual packs" fully contained within the star's points, ~x330-620,y590-720.
  - Green 6-point starburst badge, right, cursive black text "or get unlimited access" fully
    contained within the star, ~x600-870,y590-720.
- Pink band, bottom: cursive black script "Your Choice!", ~y880-990.

v1 (out/versions/ffc106f26f584a/v1.png) gaps vs this description:
- Real bug (flagged in original pass, confirmed on revisit): both star badges' text ("no cv
  needed", "just show up") is clipped by the star's own points — the text box is wider than the
  star shape's visible horizontal band, so words are cut off at the star's left/right edges in
  both badges. Reference keeps text fully inside the star's silhouette (smaller text, narrower
  wrap). This is a real legibility fail, not an acceptable variation.
- Otherwise structure matches closely: orange/white header bands, giant yellow "THE DRIVE."
  headline, pink script closing band, real-assets-only basket-photo skip — all as noted
  previously.

**Sample 44 outcome**: DONE (v2, 1 iteration). v1 had a real bug (previously noted as "minor"
but confirmed as a genuine legibility fail on revisit): both star badges' text overflowed past
the star's points because the text span had no width constraint. v2 fixed it by constraining
each span's width to the star's narrow visible waist and reducing font size slightly, so the
text wraps to 2 lines fully inside the star silhouette. Visually verified: both badges fully
legible, all other elements (header bands, giant "THE DRIVE." headline, pink script closing
band) present and matching the reference's proportions. No further iteration needed.

**ALL 44 SAMPLES NOW REVISIT-DONE.** The strict revisit pass over brain/RECREATION_AUDIT.md is
complete: every sample has a full pre-code composition description, a rebuilt/verified script
using engine/core.py+build.py+doodles.py+layout.py directly, a rendered PNG actually viewed and
checked item-by-item against its composition description, and an iteration where gaps were
found. brain/RECREATION_PROGRESS.md rows 1-44 all show "revisit-done" (or the original "done"
for samples 1/40 which were already covered pre-window and re-confirmed in this pass where
touched). Stopping condition met.

## Sample 40 — full composition description (written BEFORE v2)
- Background: solid dark-navy-to-blue, vertical-lines paper texture/grain overlay across whole canvas.
- Mid-ground SHAPE (the part v1 missed): a large white-outlined, hand-drawn wobbly coastline
  silhouette (west coast USA: WA/OR/CA), filled slightly lighter blue than the bg, occupying
  roughly the left 65% of the canvas width, full canvas height, with visible state-border lines
  inside it (thin white lines dividing WA/OR/CA/NV).
- On top of the coastline shape: 6 star pins (5-point, various fills: black, gray, navy-blue,
  gold [largest, the hub], pink, red) at city locations, roughly top-to-bottom matching city order.
- Thin curved line "routes" connecting the gold hub star to each other star (mix of black ink
  lines and one pink/red line), drawn as connector arcs, NOT straight lines.
- Tape-strip labels (alternating light-gray/paper and black bg, rotated few degrees) pinned next
  to each star: city name in one strip, "~N hours" travel time in an adjacent/stacked strip.
- ONE big diagonal tape-strip headline ("OTW TO PORTOLA") crossing the center-left, rotated ~-8°,
  light paper background, black bold condensed type, layered on TOP of the coastline and routes.
- Right edge: a large partial white-outline smiley-face circle illustration, mostly cropped off
  the right edge of canvas (only ~35% of it visible), sitting behind/at same layer as the coastline
  edge, bleeding off frame intentionally.
- No AQ logo/footer in the reference (it's a personal travel meme format) but we keep our own
  small handle per brand consistency.

## Sample 1 — full composition description (written BEFORE rebuild)
Canvas ~1000x1500 portrait, flat cream bg, no texture. A tight PILE of ~9 overlapping sticker
elements plus one wordmark and one giant letter, roughly filling the top 85% of the frame,
bottom ~15% empty cream. Z-order back-to-front approximately:
1. Pink rounded-square badge, upper-center-right (~x 46-78%, y 10-27% of canvas), containing a
   dark-green outlined globe/grid-sphere icon centered inside it, PLUS 4 dark-green corner
   "camera focus bracket" marks (small arrow-corner shapes) positioned at each corner of the
   badge, overlapping its edges. Whole badge rotated ~0-3°.
2. Green solid paper-airplane silhouette, upper-left (~x 9-39%, y 15-33%), pointing up-right,
   rotated ~-20°, solid dark-green fill, no outline detail.
3. Large italic/rounded-bold wordmark "flylane" in dark green with a lighter-green thin offset
   outline (like a drop shadow duplicate), diagonal rotation ~-10°, spanning roughly x 28-88%,
   y 27-43% — sits ON TOP of the paper airplane and partly on top of the lime melon-globe below.
4. Lime/pale-yellow "melon-globe" icon: a circle with globe-style grid lines, WITH A BITE taken
   out of its upper-right edge (like a bitten fruit), dark-green outline, positioned left-mid
   (~x 6-39%, y 36-60%).
5. Giant bold letter "A", coral/salmon-pink fill with a thick orange outline/offset, positioned
   center (~x 34-70%, y 40-68%), overlapping the melon-globe, the yellow travel card, and the
   purple circle below it.
6. Small caps text "WAY TO GO" in coral, rotated ~75° (near-vertical), running up the left
   diagonal stroke of the giant "A", nested inside/overlapping it.
7. Yellow/tan rounded-square card, upper-right of the "A" (~x 63-96%, y 36-58%), with a
   light-ray/fold triangle pattern fanning from the top edge, and two-line pale-yellow caption
   text at the bottom of the card, rotated ~4°.
8. Purple/magenta filled circle badge, lower-left (~x 6-46%, y 63-86%), with a pencil-tip icon
   centered inside (salmon triangular tip + purple faceted shaft), and small caps text curving
   AROUND the rim of the circle (following the circle's curvature, not straight), cream/pink
   color, thin inset cream ring border near the circle's edge.
9. Green solid hand-icon (fingers spread, reaching/holding), with a small globe-outline shape
   sitting in the palm, positioned bottom-center (~x 57-79%, y 68-86%) — this hand AND the
   adjacent caption are a single die-cut sticker with a white outline border around the whole
   combined shape.
10. Two-line bold caps caption text, bottom-right (~x 73-95%, y 79-86%), same white die-cut
    outline as the hand icon (they read as one sticker unit).
Overall palette: cream bg, dark forest green, lime/pale-yellow, coral/salmon, orange, tan/yellow,
purple/magenta, pink. Nothing photographic — all flat vector icon/type work.


---

# SHOWCASE RUN — 2026-07-25 (15 posters, new tooling)

First run under `brain/RECREATION_PROTOCOL.md` using `engine/compare.py` (structural measurement)
and `engine/shapes.py` (parametric silhouettes + uniform sticker treatment).
Outputs: `out/showcase5/`. Scripts: `scratchpad/gen_showcase5{,b,c}.py`.
Acceptance is score <=0.16 with no blocking critique — **none reached acceptance yet**; all are
logged `in_progress` in `brain/RECREATION_QUEUE.json`.

| # | slug | family | score | area | detail | blocking left |
|---|---|---|---|---|---|---|
| 01 | c42f94a09f07cd | sticker pile | 0.246 | 0.91x | 0.76x | none |
| 02 | 091944e282ce11 | events calendar | 0.328 | 0.91x | 0.74x | none |
| 03 | 25d39cb69b3684 | giant type + blobs | 0.392 | 0.82x | 0.92x | none |
| 04 | 29c6a858911dab | celebration slabs | 0.382 | 0.87x | 1.13x | none |
| 05 | bf31ba49142543 | signpost stack | 0.435 | 1.39x | 1.10x | none (over-corrected) |
| 06 | 64b2248475fe76 | ghost-type bleed | 0.775 | 0.42x | — | content-too-small |
| 07 | 487e8003509b03 | card grid board | 0.451 | 1.24x | 0.48x | detail-too-low |
| 08 | d375fd7dbcf69c | annotated map | 0.782 | 0.30x | — | content-too-small |
| 09 | eaad68d6305fba | slab banners | 0.951 | 0.35x | — | content-too-small |
| 10 | 502e07d0ebae6c | hero-less scatter | 0.746 | 0.26x | — | content-too-small |
| 11 | 11e7d9a3ff6761 | isometric keycaps | 0.545 | 0.44x | 0.83x | content-too-small |
| 12 | 1d518d2bc5d3dd | photo scatter (real AQ photos) | 0.641 | 1.83x | 0.71x | detail-too-low |
| 13 | 2022ebef4ffad5 | card deck repetition | 0.424 | 0.68x | 0.53x | detail, content |
| 14 | b2d4cc55d7fdbb | type sandwich | 0.442 | 0.61x | 1.25x | content-too-small |
| 15 | d252704dc5e5f3 | quadrant patchwork | 0.444 | 0.81x | 0.56x | detail-too-low |

## What the looking gate caught that NO metric did
- **04**: the connector arrow ran under the enlarged "WE" slab, reading as an artifact crossing the
  glyph. Repositioned into open field.
- **09**: slab stack spaced 130px with ~130px-tall slabs — each slab clipped the text above it.
  AND the speech bubble was filled with the page-field accent, so it rendered as an empty outline.
  The second one became an encoded auto-gate (`layout.same_as_bg_scan`).
- **07**: a seam sticker overlaps the ticker-bar text; another clips the right canvas edge.
- **15**: footer sits white-on-checkerboard (poor contrast); the cream quadrant is under-used; and
  unlike the reference, no type actually straddles the field seam.

## Standing gaps for the next pass
1. `DETAIL TOO LOW` is the most persistent blocking critique — interior linework (`hatch`,
   `motion_lines`) is still too thin vs reference interiors. Highest-value next lever.
2. Under-fill correction over-shot twice (05 at 1.39x, 12 at 1.83x) — damp it.
3. None of the 15 is at the 0.16 acceptance bar; they are structurally ~80%, not 90%.
