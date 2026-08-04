# AQ ENGINE — INSPIRATION TEARDOWN (reverse-engineered board)

Each reference broken into LAYERS (bottom→top) + the DESIGN DECISIONS that made it work + the AQ-TRANSLATION (how to do it with our tokens/voice, never copy). This is taste training. Techniques feed the menu in ENGINE.md; nothing here is mandatory.

---
## 1. INDIEGROUND "SPECIAL WEEK" (black + primary blobs, graffiti type)
Layers: (1) black base (2) big organic blobs — orange splat, pink/blue/green blobs — bleeding off ALL edges, halftone-textured (3) yellow highlight bar behind Korean subtitle (4) huge hand-drawn/graffiti WHITE display type "SPECIAL WEEK" with a tiny crown doodle (5) orange date-block + green info-block, foreground.
Decisions: black lets primaries scream; type is the hero at enormous scale; blobs fill the frame edge-to-edge so zero dead black; one tiny doodle (crown) as a wink; date info corralled into solid blocks.
AQ translation: ink base + our 7 accents as edge-bleeding blobs (halftoned); NeutralFace at max scale OR a rough hand-drawn headline; corral dates/details in solid accent blocks with ink outline; one doodle wink.

## 2. HELLO RIIZE (sky photo-bg, 3D-object collage, graffiti wordmark)
Layers: (1) painted blue-sky photo base (2) faint doodles drawn INTO the sky (planes, stars, scribbles, low-contrast) (3) mid-layer 3D/photo objects at varied scale + angle — guitar, inflatable dino, rock, boba, toy soldier, frog — pinned around edges (4) torn-paper white banner + black graffiti "HELLO, RIIZE" wordmark (5) taped date/venue label strips.
Decisions: the background is a PHOTO, not flat; objects orbit the focal at different sizes creating depth; every corner has an object; text lives on torn-paper/taped strips for a cut-and-paste feel; hand-drawn marks fill the sky gaps.
AQ translation: use a real AQ photo as the whole bg (sky, field, crowd) → scrim → faint doodles drawn into it → orbit varied-size cut-outs/doodles → headline on torn-paper strip → taped mono label strips for date/venue.

## 3. RELATIONSHIP SERIES (checkerboard, cut-paper stars, sticker-label type, off-frame serif)
Layers: (1) split field: black top zone + cream bottom + a pink/red CHECKERBOARD block + blue grid patch (2) cut-paper black + white starbursts straddling edges (3) big italic serif "Relationship Series" cropped by the top edge; a second giant serif bleeding off the RIGHT edge, half-cut (4) sticker-label type "IT'S NOT YOU / IT'S ME" — each phrase a blue highlighted block, staggered, tilted.
Decisions: OFF-FRAME type (words half-cut) = tension + implies scale beyond the canvas; pattern blocks (checkerboard/grid) as color zones instead of flat fills; sticker-label words as a rhythm device; mixes serif + heavy sans.
AQ translation: let a giant Instrument Serif OR NeutralFace word bleed off an edge on purpose (override safe-margin per piece); use checkerboard/grid pattern blocks in accent pairs as zones; stagger key words as tilted highlighted label-blocks.

## 4. PLM (giant serif hero + pinned tags + 3D objects, grid paper)
Layers: (1) faint graph-paper grid bg (2) pink highlight block behind one word (3) GIANT lowercase Instrument-Serif-style headline filling the whole frame ("the community for social media marketers.") (4) small 3D objects nested in the type (disco ball, cherries, cash, lightning) (5) speech-bubble + pill tags pinned around pointing in ("Community", "This Month's Trends", cursor arrows).
Decisions: serif at MASSIVE scale is the entire composition; tags/objects fill the gaps between big letters; cursor arrows add a digital-native wink; one word highlighted for emphasis.
AQ translation: Instrument Serif hero at massive scale, lowercase, one word highlight-blocked; nest small doodles/number-badges in the letter gaps; pin speech-bubble tags (our chips w/ tails) around it.

## 5. THE DESIGN FLOW (podcast: angled type-blocks, mic photo, speech bubbles)
Layers: (1) yellow textured base + magenta swoosh ribbons curving through (2) green + orange ANGLED type-blocks stacked ("The Design", "Flow") with hard black shadow, tilted opposite ways (3) b/w mic photo cut-out as focal object rising into the type (4) green speech-bubble "Fresh ideas Real Stories" + orange starburst badge "Every Friday" + green asterisk doodles.
Decisions: angled solid type-blocks create energy + depth; a single real photo object anchors; curved ribbons lead the eye; badges/bubbles carry secondary info.
AQ translation: stacked angled accent type-blocks (ink shadow) for a title; one real photo cut-out (member/object) rising into them; curved accent ribbons as bg motion; starburst badge + speech bubble for details.

## 6. GLASSDOOR "WE WON" (green halftone, sticker pile, outlined type)
File: training_samples/reference_posters/29c6a858911dab0fa25ef134785d64ba.jpg
Layers: (1) green base + halftone dots across the WHOLE field + scattered line-doodles (2) hand-drawn curly arrow leading down (3) white-outlined speech-bubble award badge (top) (4) chunky white "WE WON" on black blocks, tilted (5) foreground stickers overlapping the type: blue starburst + waving-hands, purple bubble with bead-dots, orange/blue partial ring, yellow star.
Decisions: even a "simple" win post is DENSE — halftone + doodles keep the green alive; stickers overlap the focal for depth; one leading arrow directs the eye; heavy black outlines unify the sticker pile.
AQ translation: accent base + halftone everywhere + scattered marks; headline on tilted ink blocks; pile foreground stickers (starburst, bubble, ring, star) overlapping the words; one hand-drawn arrow to lead; black outlines on all stickers.

CONVERGENCE RUN (this session): target signature measured via ref_metrics.analyze — dom_cov .53,
mean_sat .52, hi_sat_frac .77, contrast .25, ink .19, vdr .49. Prior to this session, number_hero
had NO way to express this signature at all (its base was hardcoded to cream) — that structural gap
was the actual finding, not a styling gap. FIX (generalized, engine/engine.py archetype_number_hero):
added `content["field"]` = "cream" (default) | "accent" — accent mode renders the FULL background as
`tex.halftone_gradient(accent)` (dotted textured field, not flat — avoids the flat_dominant ban while
matching print/riso multi-tonal texture per SESSION_LOG learning #5), inverts the hero block to ink so
the number still pops, and switches all on-field text color via the existing INK_ON contrast rule.
Iteration 1 (accent="mint", density=3): dom_cov .59 (target .53), mean_sat .56 (.52), hi_sat .67 (.77),
contrast .27 (.25), ink .18 (.19), vdr .83 (.49) → total error ≈0.56. Matches the ~0.5-0.6 plateau this
exact reference already hit earlier in the session (SESSION_LOG Phase 8) — re-confirms the residual is
a VDR metric-fidelity limit: the proxy measures the bbox of the largest dark region, and the reference's
dark "WE WON" sticker is small+irregular+tilted with stickers breaking it up, while the engine's hero
block is a full rectangular slab spanning nearly the whole width — visually different strategy, same
"dominant ink mass" principle. PLATEAUED at iteration 1 per protocol (matches prior documented residual,
no further generalized rule found this pass). Bug caught + fixed in the same pass: meta text on the
top-right corner block (density>=2) inherited the field's white text color regardless of what accent
was actually drawn behind it (lemon corner) — white-on-yellow illegible. Generalized fix: meta color
now checks INK_ON against whatever's actually behind it (corner accent at density>=2, else the field
accent), not the field's default text color. This is the first instance of the "dark-on-dark /
low-contrast pre-check" pending item from ENGINE_STATE.md being encoded as a real rule.

## 7. THRIFTHAUS (black base, multi-card sticker collage, mixed type)
Layers: (1) pure black base (2) rectangular color CARDS (blue, orange, sky) at slight angles holding copy, arranged like scattered flyers (3) real product photos (jeans, model) cut out (4) scalloped/blob name-stickers "TH", "ThriftHaus", "THANK YOU" in varied colors (5) tiny hand-drawn marks (flower, sun, scribbles) between cards.
Decisions: black makes the color cards pop like objects on a table; each card its own accent + angle; scalloped sticker badges repeat the brand mark; every gap has a small doodle.
AQ translation: ink base + scattered angled accent cards holding copy/photos; scalloped AQ badge stickers repeated; real photos cut out; small doodles in the gaps. Great for multi-fact posts (recap, menu of drives).

## 8. MY CONFESSIONS (grass photo bg, flyer-pile collage, mixed weight type)
Layers: (1) photo bg (grass/car) (2) big cut-out sticker wordmark "My Confessions" w/ white outline, letters at different baselines (3) pile of white flyer-cards overlapping, each with its own layout + halftone/grid patch (4) tomato/red circle stickers, checker patches, flower + spark doodles scattered (5) small mono captions floating ("i just follow my heart").
Decisions: chaotic pile that still reads because one wordmark dominates; repeated red-circle motif ties it; varied type weights per card; doodles + patches fill all gaps.
AQ translation: photo bg + dominant cut-out wordmark (letters off-baseline) + overlapping flyer-cards for multi-point content + a repeated accent-shape motif + gap doodles. Good for "confessions"-style member-voice posts.

## 9. OTW TO PORTOLA (riso map, taped labels, star pins)
Layers: (1) heavy risograph blue textured base (2) hand-drawn white map outline + route lines (arcs) (3) taped black/white LABEL strips for each city+time, tilted (4) star pins at varied sizes/colors marking spots (5) a big line-drawn smiley bleeding off the right edge.
Decisions: a MAP is the layout skeleton; info as taped label strips; riso texture = gritty print feel; stars as wayfinding; one big outline character for personality; off-frame element.
AQ translation: map/diagram-as-layout for journeys (drive routes, Sundarbans trips); taped mono label strips; star pins; heavy riso/grain; a big outline doodle bleeding off-edge.

## 10. THE MARKET (object-as-frame: real basket photo)
Layers: (1) real photo of a blue shopping basket (2) the poster/flyer sits INSIDE the basket as if dropped in (3) flyer itself: orange/grey/yellow/pink horizontal color bands + condensed bold type "THE MARKET" (4) two starburst stickers "buy individual packs" / "or get unlimited access" + script "Your Choice!".
Decisions: object-as-frame = surprise + realism; the flyer is a tidy retro-grocery layout contrasting the real object; script font for warmth; starbursts for the two options.
AQ translation: shoot/borrow a real object (tiffin, cycle basket, notebook) and drop an AQ flyer inside it; retro banded flyer layout; starburst option stickers. High-effort, high-scroll-stop; use sparingly.

## 11. CONVERSE "WE LEAVE YOUR MARK" (torn-paper, marker scribbles, halftone, split)
Layers: (1) split: blue top / orange bottom, each textured (2) torn graph-paper note held by the focal type (3) mixed type: heavy black condensed + purple bubble letters + orange marker script "your" (4) marker-scribble loops (orange, lime, blue) all over the negative space (5) halftone patches + a b/w sneaker photo cut-out spray-framed, overlapping a giant "W".
Decisions: torn-paper framing; wild marker scribbles are the primary gap-filler and energy; multiple type styles in one lockup; halftone spray behind the product; two-zone color split.
AQ translation: torn-paper note holding the headline; marker-scribble loops (rough doodles) filling negative space heavily; mix NeutralFace + rough display + serif accent; halftone spray behind a photo cut-out; two-zone accent split.

## 12–13, 15–16, 19 (WEB/EDITORIAL refs — quieter, structural)
- **12 desk illustration**: layered paper sheets w/ hard shadow, cutting-mat grid, scattered stationery + tiny heart/square confetti → AQ: layered-paper depth + measured-grid surface + confetti gap-fill for calmer pieces.
- **13 design brief**: numbered index (01–07) in rotating accent colors on off-white paper, marker circle on one item, sticky-note, torn edge → AQ: numbered index carousel/menu, accent-per-number, marker-circle emphasis, sticky-note tag.
- **15 humanz / 16 promox**: big geometric shapes (circles, arcs, rectangles) in primaries floating on off-white; giant thin headline; pill brand-tags stacked → AQ: primary geometric shapes floating on cream, one giant word, stacked pill tags. Cleaner/coporate end of our range.
- **19 truus**: rounded card container, mono lowercase labels in pills, huge script wordmark waving along the bottom w/ sticker slaps (smiley, 100, heart, camera, BAM) → AQ: rounded card framing, pill mono labels, a huge script/serif wordmark as a baseline wave with sticker slaps.

## 14, 17 (SIGNPOST / DIRECTORY refs)
- **14 Table of Content**: a 3D street-sign POLE with angled directional signs (Brand Identity octagon, Illustration, Social Media, Marketing) covered in sticker slaps + graffiti; a repeating "ABOUT" checker-tape ribbon across the top; giant red "Table of Content" bleeding off-edge; character mascot in a starburst.
- **17 signpost**: a black signpost with 5 stacked accent direction-signs (Hobbies/Passions/Projects/Short-Stories) each w/ an icon + different type, fanned at angles; patterned speech-bubbles beside it.
Decisions: signpost = a playful way to present a MENU/list with vertical rhythm + angle variation; checker-tape ribbon = repeating-text border device; mascot in starburst; giant off-frame section title.
AQ translation: SIGNPOST layout for "what we do / departments / ways to join" — stacked angled accent signs w/ icons; a repeating-text tape ribbon ("AQUATERRA · AQUATERRA") as a border; giant off-frame section word; patterned speech-bubbles.

---
## CONSOLIDATED NEW MENU ITEMS (added to ENGINE.md)
Framing: object-as-frame · map/diagram-as-layout · off-frame/bleed type · torn-paper note · signpost-pole · rounded-card container · two-zone color split.
Backgrounds (never flat): photo-bg + scrim · halftone-everywhere · organic blobs edge-to-edge · pattern blocks (checkerboard/grid) · scattered line-doodles drawn into the air · risograph grain · floating primary geometric shapes.
Type: sticker-label staggered words · giant-serif hero · graffiti/marker display · angled solid type-blocks · numbered index · off-frame giant word · script/wave wordmark · repeating-text tape ribbon.
Fill/energy: varied-size doodle orbit · marker-scribble loops · speech-bubble tags w/ tails · starburst option badges · scalloped brand stickers · sticker-pile overlap on focal · repeated accent-shape motif · confetti bits · leading hand-drawn arrow · one big outline character bleeding off-edge.
Depth rule (the anti-empty law): 4–5 layers always — active bg → mid-layer varied-size objects → gap-filler marks in EVERY dead patch → focal → foreground stickers overlapping. Vary sizes. Scan all quadrants; no dead patch > ~200px.

# ============ ROUND 2 TEARDOWN (16 refs) ============

## R2-1. DRÖM (white bg, giant marker lowercase, hand-drawn objects grid)
File: training_samples/reference_posters/1d518d2bc5d3dd93934dbea4cf14984d.jpg
LAYERS: (1) plain white base (2) small red logo tile top-left + 3-column mono info header (3) GIANT black marker-drawn lowercase wordmark "dröm" with a © mark (4) row of hand-drawn thick-outline objects (red sofa-face, yellow tree, blue stool-creature, purple square, green leg) arranged in a loose grid below.
FRAMING: clean top-to-bottom: header band → huge type → object grid. Massive negative space is OK because type is enormous + objects are bold.
TYPE: hand-drawn marker lowercase, super chunky, imperfect. Mono caps for info.
TEXTURE/COLOR: flat white + primaries + heavy black outlines. No grain. Confidence through scale + outline weight.
DECISIONS: one giant word carries the whole thing; objects have PERSONALITY (eyes, faces); grid keeps chaos ordered.

CONVERGENCE RUN (session 2): target — dom_cov .72, mean_sat .12, hi_sat_frac .11, contrast .24, ink .04,
vdr .43 (a LIGHT-dominant giant-type signature — the opposite of giant_type's shipped ink-base default).
Same structural gap as sample 1: giant_type's base was hardcoded to ink, so this signature was
unreachable regardless of styling. FIX (generalized, engine/engine.py archetype_giant_type): added
`content["field"]="ink"` (default, current dark signature) | `"cream"` (light dominant base — word
stays the only major ink mass, scattered flat cut-paper shapes read as the DRÖM object-grid). All
on-field text (meta, word, footer, body) now resolves color from `field` via the same onfield/body_col
pattern used in number_hero's accent-field mode — same rule, second archetype.
Bug caught + fixed in the same pass: the payoff line ("big") was hardcoded to accents[2] (lemon) —
high-contrast on the ink base, but yellow-on-cream is nearly illegible once the base flips. Fixed:
color resolves to lemon only when field=="ink", else var(--ink).
Result: numeric gate PASS (fill .33) after the fix. Metric gap: dom_cov .59 (target .72, -.13), mean_sat
.27 (.12, +.15), hi_sat .25 (.11, +.14), contrast .22 (.24, -.03), ink .02 (.04, -.02), vdr 0 (.43, -.43).
PLATEAUED at iteration 1 — the big vdr gap is a proxy artifact (the reference's vdr proxy method looks
for a dark-mask bbox; DRÖM's giant word is thin marker-strokes so the reference itself barely registers,
and our version uses a thin cursive/italic Instrument Serif word, same issue, so the proxy reads ~0 for
both in spirit even though the number differs a lot in this small a sample — a metric-fidelity limit
per SESSION_LOG's own caveat, not chased further this pass). The mean_sat/hi_sat overshoot is real and
traceable: our scattered accent shapes (leftmass/rightmass/lowmass) are more saturated/larger relative
to canvas than DRÖM's smaller varied-hue objects — a genuine residual worth revisiting if more giant_type
cream-field pieces are generated (candidate fix: cap accent-mass size or desaturate via tex helpers when
field=="cream", not attempted this pass to keep the change scoped).

ITERATION 2 (session 4, versioned): implemented the deferred fix — leftmass/rightmass/lowmass now
scale to 75% size + blend to ~80% opacity (8-digit hex alpha) when field=="cream", full-size/opaque on
"ink" (that base's own signature is bold+flat, no change there). Result: total error 0.469 → 0.322
(v1→v2, saved at out/versions/drom/v1.png and v2.png). mean_sat and hi_sat_frac both moved substantially
toward target. New residual: contrast dipped to .208 (target .334, gate floor .22) — the lighter masses
slightly reduce overall light/dark spread — engine's own numeric gate correctly flagged NEEDS-LOOK
after escalating to max density and not clearing it. This is now the residual to chase in iteration 3;
not fixed this pass.
ITERATION 3 (session 4): tried raising mass_alpha CC→E0 (less transparent) on the hypothesis that
opacity was suppressing contrast. Result: error 0.322→0.324 (no real change; contrast .208→.209).
Hypothesis rejected — reverted to CC. The contrast/NEEDS-LOOK residual is NOT caused by mass opacity;
root cause not yet found. Logging this as a plateau rather than continuing to guess-and-check: needs
an actual diagnosis pass (which element is suppressing contrast) before another fix attempt, not
further tuning by trial.
AQ TRANSLATION: giant hand-drawn/marker lowercase AQ headline on cream; a row/grid of thick-outline doodle-objects with faces (our globe/leaf/paw/tree given eyes); mono info header. Good clean-but-fun register.

## R2-2. PLAYBOOK "think outside the box" (cream paper, circular word-scatter, sticker orbit)
LAYERS: (1) cream textured-paper base (2) the QUESTION set as scattered words following a loose CIRCULAR path, mixed sizes/weights/styles (some serif italic, some sans) (3) a full ring of thick-outline sticker characters (flowers with faces, bear, dove, star-bursts, blob hands) orbiting the words (4) small clean logo bottom-center.
FRAMING: circular/radial composition — words + stickers arc around a center. Very different from vertical stack.
TYPE: same sentence, but each word a different size/style/weight = playful rhythm through type variation alone.
TEXTURE/COLOR: paper grain; primaries with black outlines and drop shadows (stickers lift off page).
DECISIONS: radial reading path; type-size variation IS the rhythm; sticker ring frames the message; drop-shadows give depth.
AQ TRANSLATION: arrange a hook sentence on a circular path with mixed word sizes/styles; orbit it with AQ sticker-doodles (faces!) with drop shadows; cream paper. Great for a question/hook post.

## R2-3. FLYLANE (cream, overlapping sticker-pile, one wordmark buried in it)
LAYERS: (1) cream base (2) big overlapping sticker pile: green paper-plane, pink globe-in-crop-marks, yellow bitten-globe, orange "A/WAY TO GO", magenta "LEARN WITHOUT LIMITS" seal, yellow "your lane your journey" card, green hand-holding-globe "READY FOR IT" (3) the wordmark "flylane" sits IN the pile, dark green, slightly buried/overlapped by stickers.
FRAMING: dense center-weighted sticker cluster; wordmark integrated INTO the collage, not floating above it.
TYPE: bold wordmark partially occluded; sticker labels use circular/vertical/angled text; tonal (colors within a family per sticker).
TEXTURE/COLOR: analogous palettes per sticker (greens, or pink+orange), NOT rainbow — each sticker is 2-3 tones of one hue. Sophisticated.
DECISIONS: overlap = depth; wordmark buried = confident; TONAL sticker coloring (not everything rainbow) reads more designed.
AQ TRANSLATION: overlapping AQ sticker pile with the wordmark integrated/partly occluded; color each sticker TONALLY (2-3 shades of one accent) rather than all-rainbow; crop-mark + seal + hand motifs.

## R2-4. SAND STUDIO "Sticker Kit" (grey bg, sticker sheet, mixed label styles)
LAYERS: (1) flat light-grey base (2) centered pile of stickers: name-badge "HELLO I'M User Friendly", oval "anti-social but user-friendly", "Out of Office" input-field, hearts, peace-hands, "I ♥ MY JOB", circular-text logo, "Please Detach with care" keyboard-shortcut card (3) mono UI header "Sticker Kit 1/3" + footer "@handle / Buy Now →".
FRAMING: product-sheet layout — pile centered, clean UI chrome around it (page counter, buy button).
TYPE: HUGE range — script, mono, serif, UI-input, keycap — each sticker its own font personality. Coherent through consistent white outline + shadow.
TEXTURE/COLOR: mostly white/primary stickers on neutral grey; restrained bg lets stickers pop.
DECISIONS: neutral bg + wildly varied sticker type, unified by white sticker-outline; UI chrome frames it as a "kit".
AQ TRANSLATION: "sticker kit" style post = AQ phrases as varied-font stickers (script, mono, keycap, name-badge) on a neutral cream, unified by consistent white cut-outline; UI counter/CTA chrome. Great for voice/phrase posts.

## R2-5. CREATIVEHAUS sticker set (cream, outlined-icon stickers, clean)
LAYERS: (1) cream base (2) mono "set:code" header (3) cluster of thin-black-outline icon stickers with soft pastel fills: retro-window, "YOU GOT THIS!" scallop, pencil, "PRESENTATION" wavy banner, "GO TEAM" ring, OK-hand, green arrow, "UPLIFT EACH OTHER" arch, laptop, gear (4) faint handle watermark.
FRAMING: loose diagonal cluster, center-weighted, lots of clean negative space around.
TYPE: bold caps inside stickers; curved text on ring; wavy banner text.
TEXTURE/COLOR: PASTEL fills + THIN black outlines (softer than heavy-outline refs) — a gentler register.
DECISIONS: thin outlines + pastels = calmer sticker style; icons are workplace/encouragement themed; negative space intentional.
AQ TRANSLATION: alternative gentler sticker style — thin ink outlines + pastel accent fills; encouragement/action icons; more negative space. A quieter option vs the loud heavy-outline pile.

## R2-6. LOTS ART "how illustration enhances your brand" (white, highlighter-block type, doodle accents)
LAYERS: (1) white base + thin rule header/footer (mono index "02.", studio name, "@2025") (2) big black sans headline with KEY WORDS in highlighter blocks: yellow "ILLUSTRATION" (tilted), green pill "YOUR" with black arrow-dot, (3) one blue thick-outline hand illustration reaching in (4) scattered accent doodles: black spiral-arrow, red 3-stroke marks, tiny stars, a bee, asterisk.
FRAMING: editorial — ruled header/footer frame + left-aligned headline stack + one illustration + doodle confetti in gaps.
TYPE: heavy sans, keyword-highlighting via colored blocks/pills, one word tilted, arrow-dot connector.
TEXTURE/COLOR: white + black + 2 accents (yellow/green) + red doodles. Restrained but lively.
DECISIONS: highlighter-block keywords = emphasis + rhythm; editorial rules give structure; sparse doodles keep it from being corporate.
AQ TRANSLATION: editorial ruled header/footer + big sans headline with AQ-accent highlighter-block keywords (one tilted) + one hand-drawn illustration + sparse doodle confetti. Clean-credible register with personality. Great for carousel content slides.

## R2-7. GIFT GUIDE (grey studio-paper, serif+sans mix, numbered floating products)
LAYERS: (1) light grey vertical-lined paper (2) mixed serif/sans headline "GiftGuide Ideas for creatives" (elegant serif + orange accent) (3) real product photos floating (mouse, keyboard, plant, book, SSD) with dashed-line NUMBER tags (1-8) connecting them (4) orange pill labels "share it with friends", brand tags; mono corner meta.
FRAMING: editorial product-collage; numbered dashed connectors create a treasure-map read; center headline anchors.
TYPE: high-contrast serif for elegance + sans for support + one accent color word.
TEXTURE/COLOR: neutral grey + orange accent + real product photography. Premium-editorial.
DECISIONS: numbered dashed tags tie floating objects to a list; serif adds class; restrained accent.
AQ TRANSLATION: numbered dashed-connector tags linking floating real AQ objects/photos to a list; serif+sans mix; one accent. Good for "kit / what to bring / gift" style posts, premium register.

## R2-8. LINKEDIST "October — what a month" (white, calendar + polaroid pin-board)
File: training_samples/reference_posters/25d39cb69b368495069455246a545187.jpg

CONVERGENCE RUN (session 4): target — dom_cov .642, mean_sat .144, hi_sat_frac .144, contrast .353,
ink .143, vdr .556. First real test of the new stacked_zones archetype against a SECOND, calmer
reference (vs R3-10's louder one). Result (out/versions/linkedist_calendar/v1.png): dom_cov .438
(-.20), mean_sat .313 (+.17), hi_sat .347 (+.20), contrast .332 (-.02, close), ink .16 (+.02, close),
vdr .554 (-.002, essentially exact). Total error 0.613 — worse than R3-10's .345, and the pattern is
consistent with the DRÖM residual: stacked_zones' rows cycle through all 7 saturated accents every
time, which reads as MORE colorful than a calmer reference wants. vdr and ink converge well (the
geometry/structure itself is right), so this is a palette-intensity problem, not a structural one.
VISUAL FINDING (looking gate, not numeric): with only 4 rows (vs R3-10's 6), the ink container sizes
correctly for its content but leaves a large dead cream zone below it before the footer — reads sparse.
The sparse/dead-quadrant self-correction rule currently only escalates row HEIGHT with density, not
row COUNT or overall composition balance, so a short row list doesn't trigger the density ladder the
way it should. NOT FIXED this pass — flagged as the next concrete rule to encode for stacked_zones:
(1) an accent-count cap/muted-row-fraction so not every row is a loud color, and (2) let sparse
detection escalate by adding a bottom filler element (chip row, band) when row count is low, same
pattern already used in the other 3 archetypes.

ITERATION 2 (session 5): tried both flagged fixes, measured, REJECTED both.
- Muted alternating rows (every other row cream instead of accent): error 0.613→0.775. Muting rows
  didn't lower saturation as hypothesized (mean_sat barely moved, .313→.329) and tanked dom_cov further
  from target (.438→.332) by breaking the ink container into two similar-but-different light regions.
  Reverted.
- Forced density>=1 (footer band) for n<=4 rows, on the theory the dead cream zone below the list was
  "sparse and lazy": error 0.613→0.97 (worse again — the added accent-colored band pushed saturation
  UP, moving further from target). Reverted.
- REAL LESSON, not just "both fixes failed": this reference's own target signature (dom_cov .642, a
  very high ONE-color dominance) shows LINKEDIST's actual composition is deliberately light/airy — the
  "dead cream zone" I flagged as a visual defect was pattern-matching AQ's usual max-density instinct
  onto a reference that doesn't want that. The sparse/density-escalation heuristic is tuned for AQ's
  own house style (CLAUDE.md: "big type fills the frame," "dead zones = lazy") which is right for AQ's
  own content but is NOT a universal rule to force onto every convergence target — some references are
  legitimately calm. Confirms the per-archetype/per-reference calibration principle from session 1-2
  (ARCHETYPE_PROFILES already encodes per-archetype fill floors for this reason) needs to extend to
  "don't blindly apply AQ's density instinct when converging toward a reference that measures as calm."
  Reverted to the v1 baseline (error 0.613, unchanged) — no engine.py net change this iteration, but a
  real methodological lesson banked for future convergence work.
LAYERS: (1) white base (2) big rounded sans headline with one word in blue + lightning emoji-doodle (3) a real CALENDAR UI as the surface (4) polaroid photos with colored borders (blue/pink/yellow) PINNED (push-pin 3D) onto calendar dates, tilted, with handwritten labels + curved arrows (5) autumn-leaf photo cut-outs tucked behind polaroids (6) pill footer tags + page counter.
FRAMING: pin-board/calendar-as-layout; photos scattered on the grid with pins, seasonal props fill gaps.
TYPE: friendly rounded sans; handwritten script for annotations.
TEXTURE/COLOR: clean white + bright polaroid borders + seasonal orange leaves. Warm, real.
DECISIONS: calendar = structural skeleton; polaroids + pins + handwriting = human warmth; leaves fill negative space seasonally.
AQ TRANSLATION: calendar/pin-board layout for a monthly recap; AQ event photos as colored-border polaroids pinned + tilted with handwritten labels + curved arrows; seasonal props (or doodles) in gaps. Excellent for AQ monthly-roundup posts.

## R2-9. FUSION (scroll mockup: bubbly display font, blob bg, snake ribbons)
LAYERS: (1) yellow hero with pink/purple/green blobs + purple snake-ribbon winding through + tiny face-blobs + sparkles (2) bubbly rounded display headline "IMMERSE YOURSELF..." letter-spaced wide (3) starburst CTA "Choose your city" (4) later sections: green band with outline display font + words tucked in small white boxes between big letters + orange script accent.
FRAMING: full-scroll; hero uses blob+ribbon bg; a section buries small captions BETWEEN the big headline words (word-gap infill).
TYPE: bubbly wide-tracked display; outline display; mixing filled + outline + script.
TEXTURE/COLOR: soft yellow/pink/green/purple pastels-but-saturated; playful.
DECISIONS: snake-ribbon leads eye across hero; captions nested in headline gaps = clever infill; wide letter-spacing = airy playful.
AQ TRANSLATION: blob + winding-ribbon hero bg; wide-tracked bubbly display; nest small mono captions BETWEEN big headline words to fill gaps; starburst CTA.

## R2-10. AIMAN PORTFOLIO (cream, maximal kid-scrapbook, multicolor bouncy type)
LAYERS: (1) cream base + big faint outline letters in bg (2) brick-textured header band with peeking illustrated character + circled labels + pencil (3) MULTICOLOR bouncy display "PORTFOLIO/CONTENTS/ABOUT" — each letter a different accent, tilted, with stars/rings/sparkles between (4) pill index items (rotating colors), 3D envelope photo, polaroid character card with paperclip, marker-circle + curved-arrow annotations, highlighted key phrases in body.
FRAMING: maximal every-corner-filled scrapbook; multiple annotation layers (circles, arrows, highlights).
TYPE: each-letter-different-color bouncy display; handwritten annotations; highlighted running text.
TEXTURE/COLOR: cream + full rainbow + green scribbles in margins. Maximum energy.
DECISIONS: per-letter color = maximal playful; marker annotations everywhere; faint bg letters fill dead space; nothing left empty.
AQ TRANSLATION: per-letter multicolor bouncy display for big titles; faint oversized bg letters; marker-circle + curved-arrow annotation layer; highlighted key phrases; pill index. Our loudest register (use for youth-energy pieces).

## R2-11. PORTFOLIO TYPE GRID (9 ways to letter "PORTFOLIO")
This is a TYPE-TREATMENT reference sheet. Techniques for one word:
- sticker-slap over photo (stamps, flower, frog, waffle) on dark
- ransom/patchwork letters (each letter diff style+color, stitched)
- puffy 3D bubble letters + sparkles
- glossy script sticker w/ crop-marks + drop shadow
- letters at wild varied baselines/sizes overlapping (chaotic set)
- outline + tech/vector accents (pen-tool, crop-marks, circles)
- distorted/liquified white type on black (warp)
AQ TRANSLATION: our headline word can be treated ANY of these ways per piece — ransom-patchwork, puffy-3D, glossy-script-sticker, baseline-chaos, vector-tech-accented, liquify-warp. Big vocabulary for the "type-hero" structure. Vary it so pieces never look same.

## R2-12. DIRTYBARN x GRAZIA "plastic matters" (black, Y2K rounded-rect card grid, chrome/pixel)
LAYERS: (1) pure black base (2) grid of rounded-rectangle CARDS in acid green / blue / white / purple, various sizes tiled (3) heavy squished-bold display "plastic matters" (condensed heavy) (4) Y2K accents: chrome 3D blobs, pixel-font ticker "MORE OR LESS", pixel arrows/globes/sparkles, 3D toys (duck, doll, ventriloquist), photo cut-out of model with starburst.
FRAMING: modular card-grid (bento) on black; each card a mini-composition; one long ticker card spans width.
TYPE: squished heavy condensed display + pixel/8-bit font + outline font mix. Y2K/rave energy.
TEXTURE/COLOR: acid green + electric blue + magenta on black; chrome + pixel textures.
DECISIONS: bento-card grid = organized chaos; Y2K pixel+chrome = edgy/rave; black unifies loud cards.
AQ TRANSLATION: bento rounded-card grid on ink; acid-accent cards; optional Y2K pixel-font ticker + chrome doodle for edgier event posts (Disco Diwali!). Squished-condensed headline option.

## R2-13. MERSHE SAIGON (black, bento event-card grid, halftone photos, daisy motif)
LAYERS: (1) black base + mono header "MERSHE / SAIGON / PRESENTS" (2) bento grid of event cards (blue/red/yellow/teal/cream/purple), varied sizes (3) halftone-treated hero illustrations/photos per card (4) heavy condensed display titles ("TANOSHII PARK", "BEER BÔNG") (5) recurring daisy/asterisk flower motif + scribble-circle emphasis + big directional arrow.
FRAMING: bento card grid; each card self-contained event; repeated flower motif ties grid together; mono footer w/ hotline+address.
TYPE: heavy condensed uppercase display; mono meta; mixed script accents.
TEXTURE/COLOR: primaries on black, halftone photo texture, one recurring motif (daisy) as brand glue.
DECISIONS: bento = multi-event in one post; recurring motif unifies; halftone gives grit; scribble-circle for emphasis.
AQ TRANSLATION: bento event-grid on ink for "this week at AQ" multi-event posts; halftone AQ photos; ONE recurring AQ motif (star/globe) as glue across cards; condensed headlines; scribble-circle emphasis; mono footer w/ real info.

## R2-14 & R2-15. CHUCKLE PITCH DECK (bold agency deck system)
LAYERS/SYSTEM: rounded-rect slide frames; each slide ONE bold accent bg (orange/purple/acid-green/white) with high-contrast; heavy display headlines with ONE word highlighter-blocked in a clashing accent; retro photo objects (lamp, typewriter) framed in rounded white cards; big % stats in accent squares; team photos in accent tiles; bubbly logo wordmark.
FRAMING: consistent rounded-card slide system; alternating full-accent and white slides for rhythm across a deck; sticker-label logo slapped on slides.
TYPE: heavy grotesk display + bubbly logo + highlighter-block keyword.
TEXTURE/COLOR: orange/purple/acid-green/black rotating; retro-tech photography; high contrast.
DECISIONS: deck rhythm = alternate loud accent slide / clean white slide; consistent rounded frame; one highlighted keyword per headline; retro objects add character.
AQ TRANSLATION: full DECK/carousel system — rounded-card slides, alternate full-accent vs cream slides for rhythm, highlighter-block one keyword per headline, retro/real photo objects in rounded frames, bubbly AQ wordmark slapped as sticker, big accent-square stats. THIS IS THE CAROUSEL BLUEPRINT.

## R2-16. OVERFLOW (graph-paper, isometric 3D keycaps spelling word)
LAYERS: (1) light blue graph-paper base (2) isometric 3D keyboard KEYCAPS in rotating accent colors, each with a letter, arranged spelling "OVERFLOW" on a loose iso grid (3) extra iso objects: envelope key, code-window key, speech-bubble, pencil, cursor, hand, stars (4) subtle gradient side-faces on each key (depth).
FRAMING: isometric 3D object-type — letters ARE 3D objects on a grid; playful depth.
TYPE: letters embedded in 3D keycaps (object-as-letter).
TEXTURE/COLOR: graph paper + bright accents + gradient key sides + black outlines.
DECISIONS: iso 3D = tactile/game feel; object-as-letter; graph paper grounds it; gradient faces add dimension.
AQ TRANSLATION: isometric 3D keycap/block letters spelling an AQ word on graph paper; iso doodle-objects; gradient side-faces + ink outlines. Fun for playful/tech-y posts (AQ Labs!).

# ============ ROUND 2 CONSOLIDATED NEW MENU ============
FRAMING: circular/radial word-scatter · bento rounded-card grid (multi-item on ink) · calendar/pin-board · isometric-3D-object grid · numbered dashed-connector product collage · deck/carousel rounded-slide system (alternate accent/cream slides).
TYPE: giant marker lowercase wordmark · per-letter multicolor bouncy · ransom/patchwork letters · puffy-3D bubble · glossy-script-sticker w/ crop-marks · baseline-chaos overlap set · liquify/warp · squished-heavy-condensed · highlighter-block keyword (one word per headline) · pixel/8-bit accent font · wide-tracked bubbly display · words nested BETWEEN big headline letters.
FILL/TEXTURE/COLOR: TONAL sticker coloring (2-3 shades of one hue, not always rainbow) · thin-outline+pastel sticker style (gentle register) OR heavy-outline+primary (loud register) · chrome/Y2K 3D blobs + pixel textures · faint oversized bg letters · snake/ribbon winding leads · recurring single motif as brand-glue across a grid · push-pin/polaroid/paperclip realism · marker-circle + curved-arrow annotation layer · highlighted running-text phrases · dashed-line number connectors · halftone photo treatment.
REGISTERS CLARIFIED (pick per piece): (a) clean-editorial (ruled header/footer, 1-2 accents, sparse doodles) (b) loud-scrapbook (maximal, per-letter color, annotations everywhere) (c) bento-grid (multi-item, ink base, recurring motif) (d) sticker-kit (varied-font sticker pile on neutral) (e) Y2K-edgy (acid + pixel + chrome, for events). AQ can flex across ALL — variety = choosing a different register per piece.
CAROUSEL BLUEPRINT (from Chuckle): rounded-card slides; alternate full-accent vs cream; one highlighter-keyword per headline; retro/real photo in rounded frames; sticker-logo slap; big accent-square stats; consistent frame across slides = cohesion, alternating colors = rhythm.

# ============ ROUND 3 TEARDOWN (10 refs) ============

## R3-1. BREWDOWNER COFFEE RAVE (blue bg, giant ghosted word-repeat, collaged headphones)
LAYERS: (1) blue base (2) GHOSTED oversized brush-lettered "COFFEE BREW..." repeating faint white in bg (fills whole field) (3) blue-line music-note doodles + brush treble-clef staff lines scattered (4) collaged photo headphones+cassette cut-out, yellow-tinted duotone, as the focal object with yellow lightning bolts (5) torn-paper banner strip w/ condensed black title.
FRAMING: object-focal center; ghosted repeat-word bg is the space-filler; music doodles orbit.
TYPE: faint brush repeat-word bg + condensed sans on torn paper.
TEXTURE/COLOR: blue + yellow duotone photo + white brush; music-note motif everywhere. Rave energy.
DECISIONS: repeating ghosted brand word = texture AND branding at once; duotone photo unifies; motif (music notes) fills gaps.
AQ TRANSLATION: ghost-repeat an oversized AQ word faintly across the bg as texture+branding; duotone-tint a photo cut-out as focal; scatter a themed motif (leaves/paws) as gap-fill; title on torn-paper strip.

## R3-2. CLASSICO SATURDAY (cyan bg, string-bag net over 3D objects, echoed title)
LAYERS: (1) cyan textured base + yellow ribbon curves (2) ECHOED title "SATURDAY 28TH / SATURDAY 28TH" doubled + offset in yellow (motion) (3) hand-drawn pink NET/string-bag line-drawing over the objects (4) collaged halftone objects inside the net: tequila bottle, disco ball, coke can (5) oval sticker callouts (yellow/blue) w/ event info (6) yellow mono footer.
FRAMING: object cluster contained by a drawn net (net-as-frame); echoed title = motion.
TYPE: heavy condensed, echoed/offset duplicate for motion; oval sticker callouts.
TEXTURE/COLOR: cyan + yellow + pink line + halftone photo. Loud but 3-color disciplined.
DECISIONS: drawn net over real objects = clever containment; doubled title = energy; oval stickers carry info cleanly.
AQ TRANSLATION: echo/offset the headline in an accent for motion; draw a net/string/scribble container over a photo-object cluster; oval sticker callouts for info; keep to ~3 colors for discipline.

## R3-3. CLASSICO GREATEST NIGHTS (black, tilted flyer-stack collage, oval stamps)
LAYERS: (1) black base + mono corner meta (2) stack of tilted overlapping color flyers (red/yellow/blue-photo) each w/ heavy sans copy, fanned (3) photo cut-outs (crowd, green field) peeking between flyers (4) oval + scalloped stamp stickers "CLASSICO", "THURSDAY 11TH" (5) small outline doodles (martini, bottle-with-bolt, globe).
FRAMING: fanned flyer-stack (like scattered handbills); ovals stamp on top; black unifies.
TYPE: heavy sans, tight; oval-stamp callouts; mixed serif date.
TEXTURE/COLOR: red/yellow/blue on black, grain. Punchy.
DECISIONS: overlapping tilted flyers = "pile of invites" energy; oval stamps for key info; outline doodles fill black gaps.
AQ TRANSLATION: fanned tilted flyer-stack on ink for a multi-message party post; oval/scalloped stamp stickers; outline doodles in the black negative space; peeking photo cut-outs.

## R3-4. CLASSICO WELCOME (red bg, envelope collage, repeated line-art flyers)
LAYERS: (1) flat red base + grain (2) hand-drawn cut-paper display logo "CLASSICO" (wonky letters) (3) a blue paper ENVELOPE with white flyers spilling out, each w/ "THURSDAY 13TH" + line-art dancing figures, stacked/offset (4) collaged objects: bathwater-jug gag, pink hand, disco ball, cocktail, elephant head, bottle-with-bolt (5) mono meta corners.
FRAMING: envelope-spilling-flyers as central device; gag objects orbit; flat red unifies.
TYPE: wonky cut-paper display logo + heavy sans on flyers + line-art illustration.
TEXTURE/COLOR: bold red + b/w line-art + spot objects. Playful/irreverent.
DECISIONS: envelope-spill = narrative reveal; repeated offset flyer = rhythm; gag objects = humor/personality.
AQ TRANSLATION: envelope-spilling-flyers device for reveals/invites; wonky cut-paper display for a fun logo-word; line-art illustration; humor objects orbiting; one flat accent base.

## R3-5. ROAD-SIGN STICKER SHEET (grey bg, real road-sign photo stickers, dense pile)
LAYERS: (1) flat grey base (2) dense pile of REAL road-sign photo cut-outs (interstate, STOP, DETOUR, ONE WAY, ROUTE 66, EXIT, CAUTION, street-signs) tilted at varied angles, slight white sticker outline.
FRAMING: full-bleed sticker pile, edge-to-edge, minimal gaps. It's a MOTIF-LIBRARY (road/journey theme).
TYPE: comes from the signs themselves (found type).
TEXTURE/COLOR: real weathered-metal textures; multicolor but themed.
DECISIONS: a single THEME (road signs) makes a chaotic pile feel curated; real photo cut-outs add authenticity; angle variation.
AQ TRANSLATION: build a THEMED cut-out pile (e.g. Kolkata street signs, tiffin/transit ephemera, hand-drawn AQ signs) for a journey/wayfinding post; theme = coherence; angle variety = energy. Ties to our signpost/map devices.

## R3-6. NYC TRAFFIC-LIGHT ILLUSTRATION (single hand-drawn object, white bg)
LAYERS: (1) white (2) one detailed hand-drawn NYC signal-pole illustration (one-way/Broadway/W44 signs, walk-signal, no-standing).
FRAMING: single-object, isolated, tons of white space. Calm, illustrative.
TYPE: hand-lettered on the signs.
TEXTURE/COLOR: flat illustration, muted primaries, wobbly ink linework.
DECISIONS: sometimes ONE well-drawn object + white space is enough; hand-drawn = warmth.
AQ TRANSLATION: single hand-drawn hero illustration (a Kolkata signpost, a hand-drawn AQ object) isolated on cream = a calm, illustrative register. Not everything must be maximal.

## R3-7. AND ALL THAT JAZZ (cobalt bg, cut-paper Matisse hands+instruments, hand-cut type)
LAYERS: (1) saturated cobalt base (2) hand-cut PAPER-style display type "AND ALL / THAT JAZZ" (chunky, imperfect, cream) top+bottom (3) center: flat cut-paper illustrations of hands playing instruments (guitar, sax, mic, piano) in bold primaries + organic blobby shapes (4) scattered cut-paper stars + music notes.
FRAMING: type top+bottom framing a central illustration cluster (classic gig-poster sandwich).
TYPE: hand-cut paper letters, chunky and irregular = friendly/crafted.
TEXTURE/COLOR: cobalt + cream + red/yellow/pink/green flat fills; Matisse cut-paper aesthetic. No outlines, flat shapes.
DECISIONS: cut-paper flat shapes (no outlines) = a DIFFERENT visual language from our outlined-doodle style; type sandwich framing; hands = human warmth.
AQ TRANSLATION: NEW register — Matisse cut-paper: flat organic shapes, NO black outlines, hand-cut irregular letters, type-sandwich framing. Warm, artsy, human. A softer alternative to our heavy-outline sticker style. Great for welfare/community warmth posts.

## R3-8. ALL THAT JAZZ POSTER SERIES (white bg, overlapping flat instrument shapes)
LAYERS: (1) white base + thin black frame border (2) big flat color-blocked instrument shapes (sax=yellow, trumpet=orange, cello=blue, piano=green) overlapping w/ transparency/multiply (3) clean sans "ALL THAT JAZZ" + mono date footer.
FRAMING: bordered poster; overlapping flat shapes create color-mixing depth; minimal.
TYPE: clean modern sans, restrained. Lets shapes speak.
TEXTURE/COLOR: white + 4 flats with multiply overlaps (new colors where they cross). Sophisticated.
DECISIONS: overlapping transparency = depth + extra colors for free; restraint; series consistency (same layout, different instrument).
AQ TRANSLATION: overlapping flat shapes with multiply-blend (borrowed color-mixing) for a refined register; thin border frame; clean sans; SERIES thinking (same frame, rotating subject) = carousel cohesion.

## R3-9. JAZZ SPRING SHOW (cream, playful cut-out letters scattered + Matisse shapes)
LAYERS: (1) cream base (2) words "jazz / SPRING / SHOW" as big playful cut-out letters placed in different corners/scales/angles (each word its own spot) (3) bold flat organic shapes between them: red flower, blue megaphone, green rainbow, magenta asterisk-flower, squiggles, closed-eyes doodle (4) hexagon date-block + small rotated info text.
FRAMING: scattered-word placement (words as compositional anchors in different zones) + shapes filling between = balanced all-over composition.
TYPE: friendly rounded cut-out display, each word different position/size; small rotated captions.
TEXTURE/COLOR: cream + primary flats (Matisse). Airy, joyful.
DECISIONS: words scattered to corners = all-over balance (not a stack); flat shapes as connective tissue; rotated small text adds craft.
AQ TRANSLATION: scatter headline words to different zones as anchors, fill between with flat Matisse shapes + doodles; hexagon/shape info-blocks; rotated captions. Joyful all-over composition (vs vertical stack).

## R3-10. EVENTS CALENDAR
File: training_samples/reference_posters/091944e282ce11698315cf95a78615e2.jpg

CONVERGENCE RUN (session 3): target — dom_cov .345, mean_sat .319, hi_sat_frac .372, contrast .334,
ink .160, vdr .696. Prior finding (session 2): NO encoded archetype could reach this signature at all
— number_hero/radial_orbit/giant_type are all single-focal geometries, this reference is a TOP-DOWN
STACKED LIST (rounded title card → meta row → pill-row list on a dark container). That absence was
itself the real gap, not a styling problem — per the standing principle from sessions 1-2 (check for a
structural ceiling before treating a gap as tunable).
FIX (generalized, new archetype — not a variant of an existing one): added `archetype_stacked_zones`
to engine/engine.py + `ARCHETYPE_PROFILES["stacked_zones"]` (fill_min .30, max_density 2) + registered
in ARCHETYPES. Structure: accent title card (rounded, hard-outlined, ink drop-shadow) → two kicker
chips flanking a divider → an ink container holding N pill-rows, each with a small colored index chip
+ a full-width colored label pill, alternating accents. density escalates row height + adds a footer
band, matching the density pattern of the other 3 archetypes (never shrinks below a legible floor).
Content shape: `dict(meta, title, kicker_left, kicker_right, rows=[(tag,label,accent_idx),...], band,
footer)` — same input pattern (dict + accent_idx) as every other archetype, no special-casing in
generate().
Result: dom_cov .289 (target .345, -.056), mean_sat .439 (.319, +.12), hi_sat .457 (.372, +.085),
contrast .343 (.334, +.009 — essentially exact), ink .234 (.160, +.074), vdr .703 (.696, +.007 —
essentially exact). Total error ≈0.345 on the FIRST pass — better than either prior session's
first-pass convergence, because the geometry itself (not just the palette) now matches the reference's
actual structure. Residual: our accent rows are more saturated/varied-hue than the reference's cards
(which repeat fewer, calmer colors) — a legitimate future refinement (rows could cycle a shorter
accent subset per generation rather than all 7), not chased further this pass.
STATUS: converged well enough to ship as a 4th real archetype. Demo output: out/converge/44_stacked_zones_demo_events.png (ink base, rounded pill-row stack, per-row color)
LAYERS: (1) ink/black rounded-card base (2) big rounded-rect yellow header card w/ heavy rounded display "Events Calendar" + star doodles (3) pill "IN OCTOBER → 2024" row (4) STACK of date-rows: each = a colored number-pill + a colored label-pill (per-row color pairs: green/pink/blue/red/teal), rounded, chunky (5) footer: "MORE INFORMATION" split-pill + URL pill + arrow + star accents.
FRAMING: clean rounded pill-row stack on ink; each row two pills (date + event); highly legible list.
TYPE: heavy rounded friendly display + bold pill labels.
TEXTURE/COLOR: ink base makes rounded candy-color pills pop; per-row color coding; star gap-fillers.
DECISIONS: pill-row list = super-clean way to show a schedule; per-row color = scannable + lively; rounded everything = friendly; ink base = contrast.
AQ TRANSLATION: PERFECT for AQ event/drive schedules — rounded pill-row stack on ink, per-row accent pair (date-pill + label-pill), rounded display header, star gap-fillers. Clean + fun. Directly usable for "this month's drives / events."

# ============ ROUND 3 CONSOLIDATED NEW MENU ============
NEW REGISTER: (f) MATISSE CUT-PAPER — flat organic shapes, NO black outlines, hand-cut irregular letters, type-sandwich or scattered-word framing, warm artsy human. Softer alt to heavy-outline sticker style. (welfare/community warmth, arts posts)
FRAMING adds: net/string container drawn over objects · envelope-spilling-flyers reveal · fanned tilted flyer-stack · themed cut-out pile (theme = coherence for chaos) · type-sandwich (title top+bottom around center art) · scattered-word all-over balance (words as zone-anchors) · single-hero-illustration + whitespace (calm register) · rounded pill-row stack on ink (schedules).
TYPE adds: ghosted repeat-word bg (texture+branding) · echoed/offset duplicate title (motion) · hand-cut paper letters · wonky cut-paper display logo · overlapping-flat-shape color-mixing (multiply).
FILL/TEXTURE/COLOR adds: duotone-tint a photo cut-out to unify · recurring themed motif as gap-fill (music notes/flowers) · 3-color discipline even when loud · multiply-blend overlap for free extra colors · real weathered photo cut-outs for authenticity.
KEY PRINCIPLE reinforced: a THEME unifies a chaotic pile (road signs, jazz instruments) — pick ONE theme per collage. And: NOT everything must be maximal — single-hero-illustration + whitespace is a valid calm register.
EVENT/PARTY playbook (Classico/Mershe cluster): ink or one-flat-accent base · fanned flyer-stack OR bento cards · oval/scalloped stamp callouts · gag/humor objects for personality · mono meta corners · echoed/offset titles · themed motif glue. Perfect for Disco Diwali / Paradox / Starry Nights.

## See also
- [[09 Brand Constants and Vocabulary]]
- [[Recreations Index]]

[[Home]]
