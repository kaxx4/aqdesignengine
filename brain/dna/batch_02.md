# DNA Batch 02 — visual analysis of 8 reference posters

### 29c6a85891
- WHAT: Celebration post — "'GLASSDOOR'S BEST PLACES TO WORK 2025 / WE WON" sticker pile.
- ARCHETYPE: NEW: sticker_pile_celebration (closest built = scatter_collage stub, but here the pile is a diagonal cascade of 2 type-blocks + satellite stickers)
- READING AXIS: green speech-bubble badge top-left → curled arrow sweeping right-down → "WE" black block → steps down-right to "WON" → small stickers (star, donut, capsule) last
- HERO: the two-line black "WE / WON" slab-type blocks, ~35% of canvas
- BASE FIELD: saturated color — flat kelly green with a halftone dot texture across the whole field
- ACCENTS: 6 (white, black, yellow, sky blue, purple, orange) — role: container fills + sticker bodies, not punctuation; color IS the composition
- TYPE TREATMENT: sticker-label
- EYE-CANDY MODE: direct (the big hand-drawn curled arrow physically routes the eye from badge to hero)
- DENSITY: board-busy
- STEAL: the hand-drawn curled arrow as an explicit reading-axis connector — an engine primitive `connector_arrow(from_bbox, to_bbox)` that draws a loopy ink arrow along the vector between two placed elements, auto-rotated, with a fat arrowhead at the destination.
- REACHABLE: no — needs diagonal two-block type cascade + a bbox-to-bbox arrow connector; giant_type gives one word centered, not a stepped pair with satellites.

### 3bb3f9582d
- WHAT: A "Design Project Brief" numbered checklist rendered as a photographed sheet of paper on a desk, with a FINAL sticky note.
- ARCHETYPE: NEW: desk_photo_mockup (a scatter_collage of paper artifacts, but shot in perspective on a dark surface)
- READING AXIS: "Design Project / Brief" headline top-center → orange FINAL sticky → the 01–07 numbered list left-to-right, top-to-bottom → the yellow portfolio sheet bleeding off right
- HERO: the white brief sheet itself, ~65% of canvas
- BASE FIELD: dark/ink — near-black matte desk surface, papers stacked on it
- ACCENTS: 6 (yellow, mint, blue, coral, pink, orange) — role: type color only, one hue per numbered item; the paper stays white
- TYPE TREATMENT: editorial-stack
- EYE-CANDY MODE: contain (everything sits inside paper containers; hand-marks — an underline and a hand-drawn oval around "Timeline" — annotate rather than decorate)
- DENSITY: medium
- STEAL: per-item accent rotation in a numbered list — each "NN / Label" pair gets the next color from ACCENTS in sequence, number in the same hue as its label, so a mono list reads as a rainbow index without any container fills. Plus: hand-drawn oval/underline as a "highlight one item" primitive.
- REACHABLE: partially — stacked_zones can do the numbered list, but no (missing: paper-sheet-on-dark-surface framing, rotation/perspective, sticky-note overlay, hand-annotation marks).

### 487e800350
- WHAT: A "plastic matters / how plastic are we?" editorial moodboard — a grid of rounded cards on black about plastic.
- ARCHETYPE: isometric_grid is wrong; closest = NEW: card_grid_board (rounded-rect module grid, mixed sizes, gutters, full-bleed black)
- READING AXIS: "No plastic bags" card top-left → blue "plastic matters" mega-card (true hero) → green lime "how plastic are we?" → the full-width lime ticker bar mid-page → bottom row of image/graphic cards
- HERO: the blue rounded card with "plastic matters" black condensed type + rubber duck, ~18% of canvas
- BASE FIELD: dark/ink — pure black gutters between all cards
- ACCENTS: 6+ (electric blue, acid lime, magenta, orange-red, purple, yellow) — role: large container fills, one saturated hue per card
- TYPE TREATMENT: clean-bold (heavy condensed grotesk), with a mono-technical sub-layer inside the definition card
- EYE-CANDY MODE: contain (every element lives inside a rounded-rect card) + one full-width ticker bar acting as a divider
- STEAL: the full-width lime "ticker bar" — a single-row rounded pill spanning margin-to-margin with mono/pixel type and small glyphs interleaved between words, used as a horizontal divider between two card rows. Mechanical: `ticker_bar(y, words[], glyphs[])` alternating word/glyph/word.
- DENSITY: board-busy
- REACHABLE: no — needs a rounded-card grid layout engine (variable row heights, consistent gutter, per-card fill) which no built archetype has.

### 4c6df2b479
- WHAT: A Saigon bar's weekly events board — six event cards (Tanoshii Park, Hiphop Night, Beer Bông, Thursday Funny, Ladies Night) with a hotline footer.
- ARCHETYPE: NEW: card_grid_board (same family as 487e; here a masonry of 6 event cards on black)
- READING AXIS: top mono eyebrow row (MERSHE / SAIGON / PRESENTS) → big blue Tanoshii card upper-left → yellow BEER BÔNG card right (the loudest) → smaller cards downward → footer hotline strip
- HERO: the yellow "BEER BÔNG" card with daisy cluster, ~24% of canvas
- BASE FIELD: dark/ink — black, cards float on it with generous gutters
- ACCENTS: 5 (blue, red, yellow, teal, purple) — role: large container fills, one per card; cream used as a neutral card
- TYPE TREATMENT: clean-bold
- EYE-CANDY MODE: contain, plus one motif repeated as a sticker (the asterisk-flower badge) that straddles card edges and stitches the grid together
- DENSITY: board-busy
- STEAL: a single repeated brand glyph (here the asterisk-flower) placed as a circular badge STRADDLING the boundary of two adjacent cards — it breaks the grid deliberately and unifies the board. Rule: after laying a card grid, place 2–3 instances of one doodle centered on card seams, z-above all cards.
- REACHABLE: no — needs the masonry card-grid engine + eyebrow/footer rails.

### 502e07d0eb
- WHAT: A collage of real road signs (STOP, DETOUR, ONE WAY, ROUTE 66, DEAD END, "Main Street Moments") — no headline, purely a sign pile.
- ARCHETYPE: scatter_collage (stub) — genuinely this one, an object pile with no type layer of its own
- READING AXIS: no single entry — the eye lands on the red STOP octagon (only red), then wanders outward through the yellow diamonds; a scan pattern, not an axis
- HERO: the STOP sign, only ~7% of canvas — deliberately NO dominant element
- BASE FIELD: light — flat pale grey, cut-out objects float on it with soft drop shadows
- ACCENTS: 5 (yellow, red, orange, green, blue) — role: object-intrinsic color, not applied; yellow dominates by object frequency
- TYPE TREATMENT: sticker-label (all type lives inside the sign objects)
- EYE-CANDY MODE: juxtapose (objects placed for shape rhyme — diamonds vs octagons vs shields — with rotation variance ±20°)
- DENSITY: board-busy
- STEAL: rotation-jitter + shape-family alternation in a scatter fill — place objects on a loose 4-column jitter grid, each rotated random ±18°, and never allow two same-silhouette shapes adjacent. That's a concrete `scatter_pack(objects, cols, rot_jitter, silhouette_key)` rule.
- REACHABLE: no — no built archetype makes a hero-less object pile; `dominance_check` would actively flag this layout as failing, so it needs an opt-out.

### 51010a5e1a
- WHAT: "the community for social media marketers." — a brand hero statement for plm, set as one giant serif paragraph.
- ARCHETYPE: giant_type (closest built), extended with floating UI-chip satellites
- READING AXIS: dead center on "community" (the pink highlight bar) → reads down the serif stack → the chips/emoji orbiting it are picked up second
- HERO: the 4-line serif type block, ~45% of canvas
- BASE FIELD: light — off-white paper with a fine grid/graph-paper rule
- ACCENTS: 4 (pink highlight, lime green tag, baby blue tag, plus small object colors) — role: punctuation, ~10% coverage, used as highlighter bars and tag fills behind/around type
- TYPE TREATMENT: serif-accent (a whole display serif at hero scale, mixed weights/italic in the wordmark)
- EYE-CANDY MODE: letterform-integrated (cherries, disco ball, lightning, cash sit ON the letterforms; speech-bubble tags with tails point at specific words; two cursor arrows imply hover)
- DENSITY: medium
- STEAL: the "annotated headline" move — attach small rounded speech-bubble tags with tails ANCHORED to specific words in the headline (tail tip touching the glyph), plus one flat translucent highlighter bar sitting behind a single word. Mechanical: `annotate_word(word_bbox, label, side)` emitting a tag + tail vector.
- REACHABLE: yes(giant_type) for the type mass — but the word-anchored tag/tail + highlighter-behind-one-word layer would need adding.

### 620d62f101
- WHAT: Nightclub event flyer — "The Greatest Nights Only In CLASSICO, 11.12.25 Thursday", with reservations footer.
- ARCHETYPE: NEW: photo_card_stack (a fanned stack of 4 rotated rectangular cards — scatter_collage's cousin but ordered, overlapping, and tilted on one axis)
- READING AXIS: red card headline top-left → down through the overlapping yellow/blue/photo cards → the red ellipse "THURSDAY 11TH" → footer reservations
- HERO: the tilted red card, ~28% of canvas
- BASE FIELD: dark/ink — full black, high-contrast; cards are the only light
- ACCENTS: 4 (red, yellow, sky-blue photo, orange) — role: large container fills, each card one flat hue
- TYPE TREATMENT: clean-bold (tight grotesk caps), with one serif-italic accent word ("PARTIES", "THURSDAY")
- EYE-CANDY MODE: juxtapose + frame (ellipse and scalloped-badge shapes stamped over the card stack; deliberate occlusion — "BAD IDEAS MAKE GREAT NIGHTS" is half-hidden behind the red card and that's the point)
- DENSITY: board-busy
- STEAL: intentional partial occlusion — allow a later card to cover ~35% of an earlier card's text and DON'T fix it; the engine's collision_check needs an `allow_occlusion` class for stacked cards, plus a rule that each card in a stack rotates by a stepped amount (e.g. -6°, +3°, -2°, +5°) rather than random.
- REACHABLE: no — collision_check would reject this layout outright; needs an occlusion-permitted stack primitive.

### 64b2248475
- WHAT: "Brewdowner Sundowner, Coffee Rave Party" — a headphones/cassette collage gig poster.
- ARCHETYPE: off_frame_bleed (stub) — giant ghost word "COFFEE BREW" bleeding off all four edges behind the object
- READING AXIS: the black-and-yellow headphones dead center → yellow lightning bolts → the torn-paper banner headline at bottom → the ghost background type read last
- HERO: the headphones + cassette cut-out object, ~40% of canvas
- BASE FIELD: saturated color — periwinkle blue, filled with oversized white outline display type cropped by every edge
- ACCENTS: 2 (yellow, black) — role: punctuation (bolts, music notes) and the object's own duotone treatment
- TYPE TREATMENT: per-letter-styled (the torn-banner headline is stencil-condensed with rough inked texture; the background type is a separate outline layer)
- EYE-CANDY MODE: frame (bolts and music notes radiate outward from the hero as a halo, framing it)
- DENSITY: medium
- STEAL: the background-as-cropped-outline-type layer — set the headline word a second time at ~4x size, white outline only (no fill), rotated 0°, deliberately overflowing all four canvas edges, z-index below everything. Free density + texture with zero new assets. Mechanical: `ghost_type_bg(word, scale=4.0, stroke_only=True, z=0)`.
- REACHABLE: partially — giant_type does big type but not as a cropped no-fill background layer under a hero object; no(missing: stroke-only overflowing type layer + duotone photo cutout hero).

## Cross-batch observations
- 3 of 8 are card/module grids on black (487e, 4c6d, and 620d as its tilted cousin) — a `card_grid_board` archetype is the single highest-value addition from this batch.
- Only 2 of 8 use a light base field; the batch skews dark-field with saturated container fills, which is the inverse of AQ's cream default. Accent-as-large-container-fill (not punctuation) is the recurring deviation.
- Two posters (502e, 620d) would FAIL the current gate stack (dominance_check, collision_check) despite being good design — the gates need documented opt-outs for hero-less scatter and permitted-occlusion stacks.
