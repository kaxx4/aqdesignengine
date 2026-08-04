# Sample 07

**Reference file:** `2022ebef4ffad554b42b3d6c5c6c914a.jpg`

## Composition description & outcome

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

## Status
revisit-done — REVISITED (session 8, v1->v3): v1's three stacked cards were completely blank (missing the dancing-figure illustration that's this poster's core content) and 7 scattered object illustrations (jug, disco ball, cocktail, martini, bottle, elephant, glove) were missing, replaced by generic gag doodles. v3 added stick-figure line art in all 3 cards plus all 7 objects, and fixed a genuine Chromium rendering bug along the way (bottom-anchored wide children inside rotate+overflow:hidden parents silently fail to paint — see brain/DECISIONS.md). All verified present.

## See also
- [[Recreations Index]]
- [[Wide bottom-anchored child in rotated overflow parent renders blank]]
