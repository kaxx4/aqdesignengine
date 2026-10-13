# DISCO DIWALI FORMAT (draft v0, 2026-10-13)

Status: assets filed, reference described and measured, no build yet. Rules below are READ OFF the one reference, not yet proven by iteration. Mark each rule "proven" only after a recreation passes the looking gate.

## 1. Facts supplied by the reference (the only source for copy)
- Disco Diwali 2026, "Masquerade Sangeet Edition", 10th November 2026, 4:30 PM onwards.
- "Ticket sales open soon", "More details soon", CTA "Link in bio". All for charity.
- No venue, price or lineup is shown. Do not add one. (TerraThon notes carry Rs. 550 as UNCONFIRMED.)

## 2. Asset inventory
Filed in `engine/assets/disco_diwali/`:
| File | What | Notes |
|---|---|---|
| `mask.png` 2000x1514 RGBA | silver and gold jewelled masquerade mask, eyes cut out (transparent) | hero object; place top right, bleeds off the right edge |
| `string_lights.png` 2000x662 RGBA | two sagging warm-yellow bulb strings | drape from the top edge across the mask |
| `bg_beaded_portrait.jpg` 1600x2000 | beaded celestial embroidery (stars, planets, moons, rockets, sun) in four corner clusters, black centre | feed ground; centre is empty on purpose, that is the type zone |
| `bg_beaded_landscape.jpg` 2000x1610 | same family, landscape | LinkedIn / landscape cuts |
Filed in `training_samples/disco_diwali/`: `ref_announce_2026.png` (1200x1500).

NOT YET ON DISK (shown in chat, no file received): LIVE "ALL FOR CHARITY" badge, the DISCO + दिवाली title lockup with disco ball, the gold sparkle overlay, the film-grain/glitch texture. All four are needed. The Devanagari title is hand-lettered, not a font, so it cannot be rebuilt faithfully without the file.

## 3. Reference teardown (ref_announce_2026.png, 4:5)
Measured (`compare.geometry`): full-bleed, coverage 0.539, centroid (0.510, 0.446). Row 4 of the occupancy grid is the quiet band (0.04 to 0.19 in the middle columns): the gap between the title and the date block.

Z-order, back to front:
1. Black ground with film grain and scratch glitch lines.
2. Beaded celestial clusters, all four corners, densest bottom-left and top-right, faded toward the centre.
3. Gold sparkle dots scattered over the whole canvas.
4. Mask, top right, about 0.55 of canvas width, bleeding off the right edge, rotated slightly clockwise.
5. String lights draped across the top, running behind and through the mask's eye holes.
6. LIVE badge, top left, rounded square (about 0.25 of width), thin gold border, grey card fill.
7. Title lockup: disco ball sitting on the top curve of the दि, "DISCO" in a geometric sans tilted about -10 degrees, "दिवाली" in a heavy brush Devanagari with a long swept headline bar. Speckled off-white, about 0.9 of canvas width. Hero.
8. "MASQUERADE SANGEET" bold, "EDITION" regular, centred under the title.
9. Date block, three centred lines, bold grotesque, off-white: date (largest), clock emoji + time, "TICKET SALES OPEN SOON".
10. "MORE DETAILS SOON" small, then "LINK IN BIO" in a thin-gold-bordered black pill at the bottom.

## 4. Format rules, inferred (unproven)
1. Ink ground only. Never cream. The beaded plates are the pattern, so no doodle field is added on top.
2. Corner-cluster principle: pattern lives in the corners and fades to black in the middle. The centre is reserved for type.
3. One hero: the title lockup. The mask is the second voice and must not touch the title.
4. Silver, gold and white only for type and objects. Colour comes from the beaded art itself. No AQ accents.
5. Type is off-white, bold grotesque, UPPERCASE, centred, three weights of emphasis at most. Not NeutralFace by default: the reference grotesque is a wide geometric sans, so measure and pick.
6. AQ presence is the LIVE badge top left, not the cream-ground logo.
7. Grain and scratch texture over everything, full-frame, low alpha.

## 5. Conflicts with CLAUDE.md to resolve (decisions, not yet made)
- Ground: CLAUDE.md section 9 says cream, never white. This format is ink. Precedent: dark-ground pieces exist (`core.on_dark`).
- Palette: no AQ accents. Needs a recorded exception.
- Fonts: wide geometric sans plus a hand-lettered Devanagari asset, outside `core.FONTS`.
- Grain texture: section 9 says halftone only on photos and "faint wash is dirt". The film grain here is photographic texture on a dark ground, which is a different job, but `wash_scan` may flag it.

## 6. Plan (extensive system)
1. Receive the four missing files.
2. Recreate the 2026 announcement (Workflow B), iterate to a matched looking gate.
3. Encode what generalises (ground, corner clusters, type scale, badge placement).
4. Derive the set from one skeleton: story 1080x1920, tickets-open, lineup, countdown (T-7, T-3, T-1), thank-you, LinkedIn landscape using the landscape plate.
5. Companion art piece per CLAUDE.md standing rule, at the session level.
