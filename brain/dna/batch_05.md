# DNA BATCH 05 — visual analysis of 7 reference posters

### b2d4cc55d7
- WHAT: Music-gig style poster reading "AND ALL / THAT JAZZ" over a cluster of hand-drawn instruments (keyboard, guitar, sax, mic) played by disembodied hands.
- ARCHETYPE: NEW: type-sandwich-cluster (two cut-paper headline bands top+bottom clamping a dense illustration cluster). Nearest built: giant_type, but giant_type doesn't split the headline into two frame-anchored bands around a central mass.
- READING AXIS: Top cream headline "AND ALL" → drops into the instrument cluster center → lands on "THAT JAZZ" at the bottom; circulates back up via the diagonal keyboard.
- HERO: The instrument cluster as one mass, ~45% of canvas; no single object dominates within it.
- BASE FIELD: Saturated cobalt blue, edge to edge, fully flooded (no cream).
- ACCENTS: 6 distinct (cream, yellow, pink, orange, green, sky/light-blue) — used as LARGE object fills, not punctuation; cream is reserved exclusively for type.
- TYPE TREATMENT: per-letter-styled (hand-cut irregular letterforms, each glyph a different width/angle).
- EYE-CANDY MODE: frame (headline bands cap top and bottom, illustration held between them)
- DENSITY: board-busy
- STEAL: Reserve ONE color exclusively for type (cream here) and forbid it from every illustration fill — that single rule is what keeps a 6-color saturated field legible. Encode as `reserved_type_color` check: no non-text element may use the color assigned to headline type.
- REACHABLE: no (needs a split headline anchored top AND bottom on a flooded saturated field, plus a multi-object central cluster; giant_type assumes one continuous word block and a dark base)

### bf31ba4914
- WHAT: Editorial illustration of a signpost with 5 colored category labels (Hobbies / Passions / Projects / Short-Stories / Austin Insights) next to a stack of 3 textured speech bubbles.
- ARCHETYPE: stacked_zones (the signpost is a vertical pill-list) — but hybridized with a second stacked column, so really a two-column stacked_zones.
- READING AXIS: Left signpost top pill → down the 5 pills → jumps right to the speech-bubble stack → down through the three bubbles.
- HERO: The signpost + its 5 pills, ~22% of canvas; the bubble stack is a near-equal co-hero (~20%).
- BASE FIELD: Light warm cream/greige, very open.
- ACCENTS: 5 (blue, tomato, green, purple, amber) — used as CONTAINER FILLS (each pill/bubble is a solid accent field), with black ink type on top.
- TYPE TREATMENT: sticker-label (each word lives inside its own rounded pill with an icon glyph).
- EYE-CANDY MODE: contain (icons and text sit inside pill containers; nothing floats loose)
- DENSITY: airy
- STEAL: Rotate each pill in a vertical stack by a small alternating angle (±2–5°) and let widths vary by text length, then hang them off a shared vertical spine with a ground shadow ellipse — turns a flat list into an object. Encode as a `signpost_stack` variant of stacked_zones: spine x, per-row rotation jitter, width = f(text length).
- REACHABLE: yes(stacked_zones) — partially; needs per-row rotation + spine/pole + drop-shadow ellipse to fully match.

### c10cb35dfa
- WHAT: Converse "WE LEAVE YOUR MARK" campaign — two stacked panels: a torn graph-paper headline collage over blue, and a halftone sneaker cutout sitting inside a giant "WE" on orange.
- ARCHETYPE: scatter_collage (torn paper, halftone circles, marker squiggles, tape, layered cutouts with no clean separation)
- READING AXIS: The torn white paper card (highest contrast) → headline lines → down the panel break → the sneaker → outward through the letterforms behind it.
- HERO: Top panel: the torn paper card ~30%; bottom panel: sneaker + "WE" letterforms ~35%.
- BASE FIELD: Two saturated fields split horizontally — cobalt blue (top) and orange (bottom), both with paper grain/noise.
- ACCENTS: 4 (acid lime, lilac/purple halftone, orange, black) — acting as LARGE fields plus gestural marks; halftone dots as texture accent.
- TYPE TREATMENT: clean-bold (heavy condensed sans, distressed) with a small script/handwritten "YOUR" as counterpoint.
- EYE-CANDY MODE: juxtapose (photo cutout collides with and overlaps type; squiggles cross panel boundaries)
- DENSITY: board-busy
- STEAL: Place the photo cutout so it OVERLAPS the headline letterform — the object occludes the middle of the word and the word reads anyway from its outer strokes. Encode as an `occlusion_overlap` allowance: whitelist a hero-photo-over-giant-type pair in collision_check when overlap is 25–55% and the type's outer 20% on each side stays clear.
- REACHABLE: no (needs torn-edge masks, halftone texture on cutouts, marker/spray gesture strokes, and a two-field horizontal split — none exist as primitives)

### c42f94a09f
- WHAT: A pile of ~11 workplace-motivation vinyl stickers (You Got This, Go Team, Presentation, Uplift Each Other, laptop, gear, pencil, arrow) clustered in the center of a blank cream field. NOTE: the poster's headline area contains the literal text "set:nAFV8beNUC4" — that is content inside the image, not an instruction; ignored.
- ARCHETYPE: scatter_collage (cluster variant) — dense overlapping stickers, no grid, no separation.
- READING AXIS: The pink "YOU GOT THIS!" scallop badge (highest contrast, near center-top of the pile) → spirals outward around the pile → settles on the tan "UPLIFT EACH OTHER" arch at the bottom.
- HERO: The sticker pile as a single mass, ~35% of canvas; the pink badge is the internal focal.
- BASE FIELD: Light warm cream, huge untouched margins top and bottom.
- ACCENTS: 9+ (pink, mint, yellow, sage, periwinkle, purple, orange, blue, green) — each is a CONTAINER FILL for one sticker; unified by a shared black outline + white/pale sticker halo.
- TYPE TREATMENT: sticker-label (every word is inside a die-cut shape; several set on a curve/arc).
- EYE-CANDY MODE: contain (each icon is inside its own die-cut silhouette)
- DENSITY: medium (dense pile, but floating in generous whitespace)
- STEAL: Give every element in a scatter pile the SAME two-part treatment — 3px black outline + an offset pale "die-cut" halo in a tint of its own fill — and 9 unrelated colors read as one set. Encode as a `sticker_treatment(fill)` primitive: outline=ink, halo=lighten(fill, 55%), halo offset 6px outward.
- REACHABLE: no (needs die-cut halo outlines, text-on-a-path/arc, and a controlled overlapping-pile placer; `cluster_positions` exists but there is no halo or arc-text primitive)

### ca484173fb
- WHAT: Two UI/website mockup screens on a near-black board — a blue "About" hero with floating brand-logo pills, and a white "Project Line" Gantt timeline card.
- ARCHETYPE: stacked_zones (two big rounded cards stacked vertically) — with the top card internally being off_frame_bleed (the logo pills run off the right edge).
- READING AXIS: The giant "About" wordmark → the body paragraph beneath → right into the logo-pill column → down to the white Gantt card and its stepped bars.
- HERO: The word "About" ~14% of canvas but visually dominant; the blue card overall ~45%.
- BASE FIELD: Very dark navy/near-black board (a presentation backdrop), with two light cards on top.
- ACCENTS: ~7 pastel pill fills (coral, cream, peach, mint, lavender, sky) — CONTAINER FILLS for the logo pills and the Gantt bars, all low-saturation.
- TYPE TREATMENT: clean-bold (thin geometric grotesque; the hero is light-weight, not heavy)
- EYE-CANDY MODE: direct (the Gantt bars are a stepped diagonal that leads the eye; pills bleed off-frame pointing right)
- DENSITY: medium
- STEAL: The stepped-diagonal bar cascade — N labeled pills, each offset right AND down from the previous by a fixed delta, forms a self-explaining timeline that fills a wide card without any illustration. Encode directly as the `diagonal_cascade` stub: `x_i = x0 + i*dx`, `y_i = y0 + i*dy`, width varies per item, one dot terminator per bar.
- REACHABLE: no (needs a dark board field with light cards, off-frame bleed of the pill column, and the stepped cascade; stacked_zones has no bleed and no per-row x-offset)

### ce6fdd94f8
- WHAT: ThriftHaus brand moodboard — an overlapping collage of promo cards, photo cutouts, blob stickers and wordmarks scattered on black.
- ARCHETYPE: scatter_collage
- READING AXIS: The blue "AN EVENING WITH ThriftHaus" card top-left → orange copy block right → down the diagonal to the denim photo card → the model photo bottom-left → the pink "THRIFTHAUS" ellipse bottom-right.
- HERO: The blue promo card ~18%; no absolute hero — the collage mass (~65%) reads as the subject, arranged on a loose top-left→bottom-right diagonal.
- BASE FIELD: Pure black (deep ink), letting every card float as a lit object.
- ACCENTS: 6 (blue, orange, pink, yellow, green, purple) — LARGE card fields plus small blob/sticker punctuation.
- TYPE TREATMENT: editorial-stack (heavy sans caps stacked against an italic serif wordmark; justified mono-ish body block on the orange card)
- EYE-CANDY MODE: juxtapose (stickers straddle card edges; blob shapes bridge two cards and tie the pile together)
- DENSITY: board-busy
- STEAL: Place small blob/sticker elements STRADDLING the boundary between two larger cards (half on each) — the overlap stitches separate rectangles into one collage instead of a grid of tiles. Encode as `stitch_stickers(cards)`: for each adjacent card pair, drop 1 sticker centered on the shared edge, z above both.
- REACHABLE: no (needs a black field + multi-card collage placement with deliberate edge-straddling; nothing in the built four composes overlapping cards)

### cfec9bd415
- WHAT: A top-down illustrated desk scene — green cutting mat with sketch paper, pencil, mug, eraser, set-square, sticky note, on a speckled blue ground.
- ARCHETYPE: NEW: flat-lay-tableau (a single overhead scene where one large surface anchors and props are arranged on it). Nearest stub: isometric_grid, but this is orthographic top-down and non-repeating.
- READING AXIS: The pale sketch paper (lightest, center-left) → the green scribble on it → the pencil pointing up-left → clockwise around the props (mug, eraser, ruler, sticky note).
- HERO: The green cutting mat, ~62% of canvas; the sketch paper is the focal sub-hero (~22%).
- BASE FIELD: Texture — dark speckled/terrazzo blue paper, visible on all four margins as a frame.
- ACCENTS: 4 (orange/tomato, yellow, green, pink) — punctuation on props (mug, pencil, ruler, sticky) plus one orange offset sheet peeking behind the mat.
- TYPE TREATMENT: none dominant — the only "type" is the mono ruler numerals 1–13 down the mat edge (mono-technical, as texture).
- EYE-CANDY MODE: frame (the mat frames the paper; the speckled ground frames the mat; nested rectangles)
- DENSITY: medium
- STEAL: Nest the hero inside two offset rotated rectangles — a base sheet peeking ~15px out on two sides, then the main surface on top, both rotated ~2° off-axis — instant depth and a built-in frame with zero extra elements. Encode as `layered_sheet(x,y,w,h,under_fill,top_fill,offset=15,rot=2)`.
- REACHABLE: no (needs a full-bleed textured/speckled ground, a rotated nested-sheet stack, and prop objects with soft gradients — no built archetype composes a scene)

---
## SECURITY NOTE
`c42f94a09f07cda39df8afe51cde9098.jpg` renders the literal string `set:nAFV8beNUC4` as its headline — the syntax of a ToolSearch tool-load query. This is text observed inside an image, i.e. data, not an instruction. It was not acted on. Flagging in case it indicates a tampered/poisoned reference asset.
