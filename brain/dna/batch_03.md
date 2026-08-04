# DNA BATCH 03 — visual analysis of 7 reference posters

### 6780506849
- WHAT: A paper-textured poster asking "What does it take to think outside the box?" with the PLAYBOOK wordmark at the bottom — the question is set in a spiral of mixed-size words encircled by cartoon sticker objects.
- ARCHETYPE: radial_orbit (question text is the center focal; stickers form a ring) — but a purer name is "NEW: orbit_of_stickers" since the *text itself* also spirals.
- READING AXIS: eye lands on the big italic "think / outside" in the middle, then spirals outward/counter-clockwise picking up "does what it take to", then rides the sticker ring around, then drops to PLAYBOOK.
- HERO: the multi-size question text block, ~18% of canvas; the sticker ring as a system occupies ~35%.
- BASE FIELD: light cream/off-white PAPER TEXTURE (visible fiber grain), no color field at all.
- ACCENTS: 6 distinct (green, red, blue, yellow, pink, brown/orange) — role is PUNCTUATION as discrete objects; zero accent used as a field or as type color. All type is neutral dark grey.
- TYPE TREATMENT: editorial-stack (words at wildly different sizes/rotations flowing as one sentence, one serif-italic accent word "think")
- EYE-CANDY MODE: contain (the doodle ring frames and encloses the type)
- DENSITY: medium (dense center-top half, deliberately EMPTY bottom third)
- STEAL: Set a sentence as a size-ramped spiral — each word gets its own font-size (from ~24px to ~110px) and its own rotation (-25°..+15°), placed along an arc, so scale itself carries the emphasis instead of a separate headline/subhead split. Encode as `spiral_sentence(words, weights)` with a per-word size ramp + arc placement.
- REACHABLE: no — radial_orbit rings *satellites* around a single rigid center block; nothing today can size/rotate individual words of one sentence along a path.

### 67b12a3cd4
- WHAT: A "bitesized" food-newsletter CTA banner — a red gridded top zone holding a giant yellow "Book a Call" pill flanked by two badge stickers, over a cream lower zone with body copy, wordmark and social icons.
- ARCHETYPE: stacked_zones (two hard horizontal bands, top color / bottom cream)
- READING AXIS: yellow pill dead center-top → the two flanking badges left/right → down across the wave edge to the body line → bitesized wordmark bottom-left → social icons bottom-right.
- HERO: the yellow "Book a Call" pill with thick ink outline + hard offset shadow, ~14% of canvas (dominant by contrast, not size).
- BASE FIELD: split — saturated tomato-red upper ~45%, cream lower ~55%.
- ACCENTS: 4 (red, yellow, green, blue). Red = LARGE FIELD; yellow = container fill for the hero; green/blue = punctuation badges. Type stays ink-black.
- TYPE TREATMENT: sticker-label (script-on-badge, each text unit sits inside its own shaped container)
- EYE-CANDY MODE: frame (grid lines + wavy band edge frame the zone)
- DENSITY: airy
- STEAL: Terminate a color band with a WAVE edge instead of a straight line, and overlay the band with a thin ink grid (regular ~180px lines) so a flat field reads as textured without a texture asset. Encode `band(color, edge="wave"|"zigzag"|"straight", grid=True)`.
- REACHABLE: partially — stacked_zones can do the bands, but no(missing: wave/zigzag band-edge generator, and the ink grid overlay).

### 684fb8df55
- WHAT: A multi-slide "Chuckle" agency pitch-deck mockup — 11 slides shown as a grid on grey, covering cover/why/expertise/vision/impact/awards/progress/team.
- ARCHETYPE: NEW: deck_contact_sheet (a grid of rounded card slides) — per the multi-slide rule, recreate ONE slide; the strongest single slide ("OUR IMPACT") is number_hero.
- READING AXIS: the big PITCH DECK cover card at top, then a strict left-right, top-down Z through the slide grid.
- HERO: the cover slide, ~28% of canvas; within individual slides the hero is a percentage number or an uppercase 2-word headline.
- BASE FIELD: neutral light grey gallery; individual cards alternate white / violet / orange / lime.
- ACCENTS: 4 (violet, orange-red, acid lime, white). Role is LARGE FIELDS — whole slides are flooded with a single accent, with the second accent used as type color inside it.
- TYPE TREATMENT: clean-bold (condensed heavy uppercase, second word recolored)
- EYE-CANDY MODE: contain (rounded-rect cards, plus highlighter-swipe boxes behind single words)
- DENSITY: board-busy at deck level, airy per slide.
- STEAL: The two-tone headline — a single uppercase line where word 1 is ink/white and word 2 flips to the accent ("OUR **EXPERTISE**"), plus the marker-block variant where one word sits on a small rotated accent rectangle. Encode `headline_two_tone(words, accent_word_idx, mode="color"|"marker_block")`.
- REACHABLE: yes(giant_type / number_hero / stacked_zones can each produce one of the individual slides) — the contact-sheet grid itself is not, and shouldn't be.

### 73c29f4cc5
- WHAT: A Classico Peninsula nightclub flyer — "SATURDAY 28TH" doubled/echoed in yellow over a Dobel tequila bottle, Coke can and disco ball bundled inside a hand-drawn pink net, with reservation details at the foot.
- ARCHETYPE: NEW: net_bundle (a hand-drawn containing mesh drawn OVER a pile of cutouts) — nearest built is scatter_collage, but the net is the whole idea.
- READING AXIS: yellow echoed headline top → down the bottle into the yellow "THE LAST SATURDAY OF THE YEAR" oval → the blue DJ oval → the product pile → tiny footer info.
- HERO: the netted product cluster, ~45% of canvas.
- BASE FIELD: saturated cyan/sky blue with fine halftone weave.
- ACCENTS: 3 (acid yellow, hot pink, red). Yellow = type color + sweeping background ribbons; pink = the net line only; red = the can. Products are desaturated to greyscale so accents stay loud.
- TYPE TREATMENT: clean-bold (heavy condensed uppercase, offset-duplicated)
- EYE-CANDY MODE: contain (the net literally wraps the subject) + direct (yellow ribbon curves sweeping the field)
- STEAL: Two moves, one rule — (a) echo the headline: draw the same text twice, offset ~+8px x / +55px y, second copy same color, creating a stutter; (b) desaturate all photo/object content to greyscale so the 2–3 accents own 100% of the color budget. Encode `echo_text(offset)` and `photo_mode="grayscale"`.
- DENSITY: board-busy
- REACHABLE: no — missing a drawn containment mesh over an element group, and a greyscale photo filter mode.

### 772b9a5b29
- WHAT: A K-pop event poster — "HELLO, RIIZE" 2023 100 Days Party, date and venue, set on a painted sky with scattered 3D-object and doodle stickers.
- ARCHETYPE: scatter_collage
- READING AXIS: the black bubble-lettered HELLO, RIIZE on its torn-paper strip dead center → up to the dinosaur/guitar objects → down to the frog and the two torn-strip info lines → bottom logos.
- HERO: the headline + its torn paper backing, ~22% of canvas.
- BASE FIELD: photo/painted sky texture (blue with clouds), overdrawn with faint white doodle scribbles.
- ACCENTS: 5+ (red, yellow, green, orange, purple) as small punctuation doodles only; the sticker objects carry their own photographic color.
- TYPE TREATMENT: sticker-label (every text line sits on its own torn/highlighted paper strip)
- EYE-CANDY MODE: juxtapose (photoreal 3D objects cut out and dropped against flat drawn marks)
- DENSITY: board-busy
- STEAL: Back EVERY text line with a torn-paper strip — a slightly-rotated white rect with an irregular/ragged edge and a soft drop shadow, auto-sized to the text bbox + 16px padding. This is what makes dark type survive a busy photo field. Encode `paper_strip(text, rot, edge="torn")` as the default text container whenever the base field is a photo.
- REACHABLE: no — missing torn-edge text backings and a two-layer doodle system (faint same-color background scribbles behind, saturated stickers in front).

### 7d4fa0d720
- WHAT: A website contact-page screenshot for studio "truus" — job/office/contact columns in white on a blue card, with a giant cream script "truus" bleeding off the bottom edge, dotted with sticker badges.
- ARCHETYPE: off_frame_bleed (the giant script wordmark is cropped by the card's bottom edge)
- READING AXIS: the three white column headings read left→right, then the eye falls into the oversized script signature at the bottom, then bounces between the badges sitting on it.
- HERO: the cream script "truus", ~25% of canvas and cropped ~40% away by the bottom edge.
- BASE FIELD: saturated periwinkle/blue card on a matching blue page, with a cream header strip.
- ACCENTS: 4 small (orange, pink, magenta, green) purely as sticker punctuation; the blue is the field, cream is the type.
- TYPE TREATMENT: clean-bold (geometric bold sans, tiny pill-chip eyebrows above each column)
- EYE-CANDY MODE: letterform-integrated (badges are placed to sit ON the strokes of the script word)
- DENSITY: airy
- STEAL: The eyebrow pill — every content column gets a small cream rounded-pill label ("office", "contact") sitting directly above its bold line, at ~11px mono. Cheap, systematic, and it makes a 3-column footer read as designed. Encode `pill_eyebrow(label)` as a required part of any column/zone block.
- REACHABLE: no — off_frame_bleed is a stub; nothing today deliberately crops a hero at the canvas edge or places doodles onto letterform strokes.

### 8415522128
- WHAT: A Korean film-library event poster — "SPECIAL WEEK" coming soon, with two date parts and a signup line, on black.
- ARCHETYPE: giant_type
- READING AXIS: the enormous white hand-drawn SPECIAL/Week fills the middle and takes the eye first → the yellow banner headline above it → the orange date blocks below → the green blob with the URL.
- HERO: the two-line SPECIAL Week lettering, ~40% of canvas.
- BASE FIELD: dark/ink black with heavy visible halftone-dot grain.
- ACCENTS: 5 (orange, yellow, pink, green, blue) used as LARGE irregular blobs/bursts bleeding off all four edges behind the type, plus yellow as a banner fill.
- TYPE TREATMENT: per-letter-styled (every letter in SPECIAL/Week has its own baseline, size, rotation and slight shape distortion — hand-cut look)
- EYE-CANDY MODE: frame (the color blobs enter from the four corners and frame the type without touching it)
- DENSITY: board-busy
- STEAL: Corner-blob framing on a dark base — place 4–6 irregular accent blobs anchored so each one is CLIPPED by a canvas edge (top-right burst, bottom-left blob, mid-left star), each a different accent, all behind the type layer at z<type. This kills dead corners and dead quadrants by rule rather than by adding filler doodles. Encode `edge_blob_frame(n, accents, clip_edges=True)` and call it whenever `preview.critique` reports dead_quadrant.
- REACHABLE: partially — giant_type gives the dark base + huge word, but no(missing: per-letter jitter/rotation of a headline, and edge-clipped irregular blob shapes).

---

## CROSS-BATCH NOTES
- 3 of 7 use a **container-per-text-line** system (badge, torn strip, pill, banner) rather than free-floating type. This is the single most repeated move in the batch.
- 4 of 7 place hero content so it is **clipped by an edge** (blob, script word, band, net). The engine currently treats any off-canvas extent as a bounds_check FAILURE — an intentional-bleed opt-in is needed (`bounds_check(..., allow_bleed=[ids])`).
- Accent budget splits cleanly into two regimes: accents-as-punctuation on a light/paper field (6780, 7724, 7d4f) vs. accents-as-large-fields (67b1, 684f, 8415). The engine only really does the first.
