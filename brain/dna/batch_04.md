# DNA BATCH 04 — visual teardown of 7 references

### 87525f70ad
- WHAT: A sticker-pack brand sheet for "flylane" — a wordmark surrounded by education/travel sticker objects (paper plane, globes, big letter A, pencil badge, fist holding a globe) with copy chips "WAY TO GO", "YOUR LANE, YOUR JOURNEY", "LEARN WITHOUT LIMITS", "READY FOR IT".
- ARCHETYPE: scatter_collage
- READING AXIS: the dark green "flylane" wordmark across the upper third → the giant orange/peach letter A at center → clockwise out to the badge, fist sticker, yellow card, then the plane/globe at top.
- HERO: the letter-A sticker block, ~18% of canvas; the wordmark is a close second at ~12% but reads first by contrast.
- BASE FIELD: light cream, completely flat, zero texture — every object floats on it.
- ACCENTS: 6 (dark green, pink/peach, lemon, orange, magenta/plum, bright green) used as LARGE container fills — each sticker is a solid accent field, not a punctuation dot.
- TYPE TREATMENT: sticker-label
- EYE-CANDY MODE: contain (every word lives inside a shape: badge ring, rounded card, letterform, speech-blob)
- DENSITY: board-busy
- STEAL: give every sticker a uniform white/pale "die-cut" halo stroke (~10-14px) plus a same-color hard drop shadow offset ~6px, so overlapping objects in a dense pile stay individually legible. Encode as a `sticker(el)` wrapper: halo stroke + offset shadow + random rot ±12°.
- REACHABLE: no (needs a pile/overlap placer with die-cut halo + z-order stacking; `cluster_positions` places but nothing renders the halo/shadow contract)

### 878f95ff7b
- WHAT: A multi-page graphic-designer portfolio deck (cover "PORTFOLIO", "TABLE OF CONTENTS" with numbered pills, "ABOUT Meeee!" bio page) shown as a stacked scroll.
- ARCHETYPE: stacked_zones (per page); the contents page specifically is a pill-list
- READING AXIS: per page — the multicolor headline word at top → the pill list / body block below-left → the illustrated object (envelope, polaroid) at right.
- HERO: the per-letter-colored headline ("PORTFOLIO" / "CONTENTS"), ~14% of each page.
- BASE FIELD: light cream, with oversized pale outline letterforms bleeding off the left/right edges as background texture.
- ACCENTS: 5 (red/pink, cobalt blue, orange, green, sky) as TYPE COLOR (per letter) and as container fills for the numbered pills.
- TYPE TREATMENT: per-letter-styled
- EYE-CANDY MODE: frame (sparkles, stars, squiggles ring the headline and the page corners) + hand-drawn oval outlines around labels
- DENSITY: medium
- STEAL: per-letter color + per-letter vertical jitter on the headline — cycle the accent array letter by letter, alternate baseline offset ±8px and rotation ±6°, so one word carries the whole palette. Encode as `rainbow_word(text, accents)`.
- REACHABLE: yes(stacked_zones for the pill list) — but the rainbow headline is not a capability today; the pill-list layer alone is reachable.

### 8988345ad4
- WHAT: "Sticker Kit" product slide (1/3) from Sand Studio — a pile of ~16 designer in-joke stickers on a grey card with @handle and "Buy Now →".
- ARCHETYPE: scatter_collage
- READING AXIS: the "HELLO, I'M / User Friendly" name badge at dead center → outward to "I ♥ MY JOB", the yellow note, the heart, the peace hands → up to the "Sticker Kit" title, out via "Buy Now →".
- HERO: the red name-badge sticker, ~9%; the pile as a whole reads as the hero mass (~45%).
- BASE FIELD: light neutral grey (near-white), flat, deliberately recessive so the pile pops.
- ACCENTS: 5 (cobalt, red, yellow, green, purple) as CONTAINER FILLS on individual stickers; the surrounding page has none — accents are entirely quarantined inside the pile.
- TYPE TREATMENT: sticker-label (with a script/serif accent inside a few stickers)
- EYE-CANDY MODE: contain
- DENSITY: board-busy (in the central 60%), airy margins
- STEAL: the "quarantined pile" rule — cluster ALL busy/colored content inside a centered ellipse ~60% of canvas, and keep a hard empty margin band top and bottom carrying only the title and the CTA. Encode as `pile_zone(cx,cy,rx,ry)` that rejects placements outside the ellipse plus a reserved top/bottom band.
- REACHABLE: no (needs radial-scatter-with-overlap inside an ellipse; radial_orbit places on a ring with no overlap and no z-stacking)

### a99a4af4ca
- WHAT: "Gift Guide Ideas for creatives" — a Black Friday product roundup: numbered orange dots tag 8 real objects (keyboard, mouse, plant, SSD, book, cutting mat) around a serif headline.
- READING AXIS: the big serif "GiftGuide / Ideas" at center → the numbered orange badges radiating out → the keyboard cluster bottom → the "→" next-slide arrow bottom-right.
- ARCHETYPE: radial_orbit (photo-object variant — headline core, product satellites)
- HERO: the two-line serif headline, ~20% of canvas.
- BASE FIELD: near-white with faint vertical pinstripe lines — a subtle paper/grid texture, not flat.
- ACCENTS: 1 (orange) — pure punctuation: number badges, one headline word, the pill CTA, the book cover. Everything else is greyscale.
- TYPE TREATMENT: editorial-stack (large serif headline stacked, with a light grey subordinate phrase riding the baseline)
- EYE-CANDY MODE: direct — dashed leader lines connect each numbered badge to its object.
- DENSITY: medium
- STEAL: the numbered-callout system — a small filled circle badge with a number, connected to its target by a short DASHED arc, placed on the outward side of the object. Encode `callout(n, target_bbox, angle)` that emits badge + dashed bezier and registers both bboxes for collision.
- REACHABLE: yes(radial_orbit) for the ring geometry — but the dashed leader lines and the mono-accent (single accent) discipline are missing.

### abb2ab5d11
- WHAT: A Kaohsiung jazz festival poster — "jazz / spring / show" set in bouncing letters among cut-paper shapes, with bilingual date/venue lines.
- ARCHETYPE: NEW: word-scatter-field (the three headline words are themselves scattered across the canvas as three separate anchors, shapes filling the gaps between them)
- READING AXIS: "jazz" top-left → the lavender hexagon date block top-center → "spring" mid-right → "show" bottom-left → the Chinese title bottom-right, closing the Z.
- HERO: no single hero — the three headline words plus the red flower blob share it; the red flower is the largest single object at ~7%.
- BASE FIELD: light cream/off-white, flat.
- ACCENTS: 7 (red, cobalt, green, magenta, yellow, lavender, ice blue) as LARGE FIELDS — the shapes are the color, the type is near-black.
- TYPE TREATMENT: per-letter-styled (each letter individually rotated/baseline-shifted along an implied arc)
- EYE-CANDY MODE: juxtapose (shapes sit beside and between the words, never inside or behind them — almost zero overlap)
- DENSITY: board-busy but airy — high object count, generous gaps.
- STEAL: bouncing-baseline word setting — set a word letter-by-letter along a shallow sine, each glyph rotated ±15° and vertically offset by sin(i), so a single word reads as hand-placed. Pair with a rule that shapes may touch but never overlap type. Encode `bounce_word()` + a type-exclusion halo in collision_check.
- REACHABLE: no (needs per-letter transform along a curve, and a "shapes fill negative space between word anchors" placer)

### abd472f264
- WHAT: A moody "My Confession" journal collage — a die-cut bubble title over a grass photo, with scattered white note cards ("OH GOD", "12.37 AM", "Here I'm", "Am I Going To Give Up Now?") and a free-font QR corner.
- ARCHETYPE: scatter_collage (photo-backed variant)
- READING AXIS: the white bubble-letter "My confession" title at top → down-left into the "OH GOD" card → the cascade of tilted cards stepping down-right → the QR block bottom-left.
- HERO: the title lockup, ~16%; the card cascade is the mass.
- BASE FIELD: a real photograph (grass/car, desaturated, cool) — the only dark-ish field in the batch, and the cards read as paper on top.
- ACCENTS: 3 (red, cobalt blue, yellow-green) as small punctuation — tomato dots, a blue checker patch, star bursts; the cards themselves stay white.
- TYPE TREATMENT: clean-bold (tight grotesk on white cards) with one bubble/outline display lockup
- EYE-CANDY MODE: frame (the title's thick white outline frames it against the photo) + contain (each text block on its own card)
- DENSITY: board-busy
- STEAL: white paper cards over a photo base — each text block gets an opaque near-white rect at ±3-7° rotation with a soft drop shadow, so type NEVER sits directly on the photo. Encode as `paper_card(text, rot)` and a rule: text over a photo layer must be inside a card or a scrim.
- REACHABLE: no (needs a photo base field with rotated opaque cards + shadows stacked over it; current archetypes never composite type-cards onto a photo)

### b075bc30db
- WHAT: An "ALL THAT JAZZ / International Jazz Day 4/30" poster series shown as three panels — flat sax, trumpet and double-bass shapes over a green blob with a piano-key edge.
- ARCHETYPE: off_frame_bleed
- READING AXIS: the "ALL THAT JAZZ" headline top-center → straight down the trumpet/bass diagonal → the "4/30 INTERNATIONAL JAZZ DAY" tag bottom-right.
- HERO: the instrument cluster, ~45% of the panel — the blue double bass alone ~20%.
- BASE FIELD: plain white, flat; the green blob is a large mid-ground field, not the base.
- ACCENTS: 4 (green, blue, yellow, orange) as LARGE FIELDS — instruments are solid accent silhouettes with no outline.
- TYPE TREATMENT: clean-bold (grotesk caps) with the italic "Jazz" as a serif-ish accent word
- EYE-CANDY MODE: letterform-integrated — the headline sits ON the green blob and the piano keys run along the blob's lower edge as a texture band.
- DENSITY: medium
- STEAL: crop the hero shapes at the canvas edge — the sax and bass run off the left/right/bottom margins, and the green field bleeds off the top. Encode an `off_frame(el, edge, bleed_frac=0.15..0.3)` helper AND a bounds_check exemption list so intentional bleed isn't flagged as an off-canvas bug.
- REACHABLE: no (bounds_check actively forbids the very move that defines this piece; needs an opt-in bleed whitelist)

---
## CROSS-BATCH NOTE
4 of 7 are collage/scatter pieces the engine cannot build. The single highest-leverage missing
capability is a **sticker/card primitive** (halo stroke + offset shadow + rotation + z-order) plus a
**pile placer** (overlap allowed, confined to a zone, with reserved title/CTA bands). Those two
unlock 87525f70, 8988345a and abd472f2 at once. Second is an **intentional-bleed exemption** in
`bounds_check`, without which off_frame_bleed can never pass the gate.
