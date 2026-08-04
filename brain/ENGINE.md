# AQ SOCIAL DESIGN ENGINE

Generates AquaTerra social collateral: **posters, carousels, stories** for @ngo.aquaterra. Audience: students 14–19, Kolkata. Voice: chaotic-good friend group, never boring NGO.

This folder **is** the generator. The samples you've seen came out of these files. Editing these files changes what gets generated — there is no separate "summary." Keep them current.

## THE ONE PRINCIPLE (read first)
**Every feature is a per-piece decision, chosen only when it serves that piece. NOTHING is enforced on every design.** Not dividers, not stat-rows, not doodles, not even spacing, not background geometry. Variety across pieces comes from making DIFFERENT choices — including subtraction. The engine offers a menu; it never force-feeds the whole menu. Force-feeding = boredom.

When building a piece, you DECIDE per layer what to include and what to leave out. A tidy divided stack and an asymmetric one-giant-focal piece with no dividers are both valid.

## DEFINITIONS
- **RHYTHM** = the felt pattern of emphasis and pause as the eye moves through a piece. Made by ANY of: size jumps (huge→tiny), spacing (tight cluster→big breath), repetition/echo, weight shifts, color beats, alignment changes. Even spacing is only ONE way; uneven/syncopated is often better. Rhythm can be one dominant focal with quiet around it, OR a run of repeated beats. Goal = intentional pattern by varied means — NOT a fixed band+divider template.
- **FRAMING** = how the composition is bounded and held: where edges, containers, breathing room sit. Decisions: full-bleed vs margin-framed; photo in hard border vs bleeding off-page; color block cropping type; negative space as frame; an element deliberately breaking the frame. Framing sets the stage; rhythm moves within it.

## THE 6 LAYERS (build bottom-up; each layer's features are OPTIONAL per piece)
0. **CANVAS** — size (feed 1080×1350 / story 1080×1920 / square 1080×1080); base (cream #F4EFE0 / ink #0A0A0A / one accent flood); texture (grain almost always; + optional halftone/color-wash). Never flat white.
1. **STRUCTURE / FRAMING** — pick the dominant move + framing: photo-hero, type-hero, big-number, torn/diagonal split, quote-card, meme, chip-scatter, manifesto-list, row-rhythm stack, focal-portrait. ONE move leads.
2. **PHOTO** — none / full-bleed / cut-out-tilted-framed / in-a-shape. Real assets only. Chunky white+ink border + hard shadow when framed. Scrim when text overlaps.
3. **TYPE** — headline NeutralFace 900 UPPERCASE; ≤1 Instrument Serif italic accent word; body Eina lowercase (short); labels JetBrains Mono UPPERCASE. Numbers can be heroes. Clear size cadence.
4. **ELEMENTS (energy)** — OPTIONAL: doodles (0–3, clean/rough, AQ-specific globe/leaf/paw/tree for fingerprint), snarky chips (dry lowercase asides in accent pills), micro-chips, stickers, dividers/rules, corner marks, background geometry. Use FEWER, intentional. Skip entirely on dense pieces.
5. **BRAND FURNITURE** — logo (bare colored wordmark, NO pill, light zones only; on dark pieces put it in a light top-bar/footer). handle. soft CTA. ≥1 fingerprint (real number/name/project).

## RHYTHM & FRAMING AS A MENU (not a rule)
`rhythm.py` offers an even-cadence band engine — use it WHEN a piece wants an even beat. Do NOT use it every time. Other rhythm tools: one giant focal + quiet space; syncopated/uneven gaps; repeated echo beats; a single color doing the pulsing. Dividers (`rule()`) are ONE optional way to mark a beat — reach for them occasionally, not by default.

## COLOR
7 accents, FREE rotation per piece (not category-locked — that's the website's rule, not social's). One accent leads per piece; teal #0E7C86 is the 7th, canon. Ink text on lemon/sky/mint-bright; white on the rest. No gradients. ~90% cream+ink / accents for the rest.

## VOICE (see brand memory for full banned list)
Lowercase, dry, Hinglish ok, honest-as-warmth, never preachy. Soft CTAs only. No em dashes. No emojis on graphics (use ★/doodles). First names/handles only. ≥1 real fingerprint per piece.

## PIPELINE (every piece)
`author a spec` → `html_from_spec` → **`render()` runs `audit.py` (overlap + margin gate)** → if issues, fix placement (use `measure_free()` to find REAL gaps) → re-audit → ship. Never ship with overlaps. Intended overlaps (chip-on-photo) are whitelisted in audit.py.


## EXPANDED TECHNIQUE MENU (from board teardown — see INSPIRATION.md for the full breakdown)
All OPTIONAL, per-piece. Pick a few that serve the piece; never all.
- FRAMING: object-as-frame · map/diagram-as-layout · off-frame/bleed type (override safe-margin on purpose) · torn-paper note · signpost-pole · rounded-card container · two-zone color split.
- BACKGROUNDS (never flat): photo-bg+scrim · halftone everywhere · organic blobs edge-to-edge · pattern blocks (checkerboard/grid) · line-doodles drawn into the air · risograph grain · floating primary geometric shapes.
- TYPE: sticker-label staggered words · giant-serif hero · graffiti/marker display · angled solid type-blocks · numbered index · off-frame giant word · script/wave wordmark · repeating-text tape ribbon.
- FILL/ENERGY: varied-size doodle orbit · marker-scribble loops · speech-bubble tags w/ tails · starburst option badges · scalloped brand stickers · sticker-pile overlap on focal · repeated accent-shape motif · confetti bits · one leading hand-drawn arrow · big outline character bleeding off-edge.


## DESIGN REGISTERS (pick ONE per piece — this is how we get variety without chaos)
AQ flexes across registers; choosing a different one each time IS the variety strategy:
- (a) CLEAN-EDITORIAL: ruled header/footer, 1-2 accents, big sans headline w/ highlighter-block keyword, sparse doodles, one illustration. (carousels, credible content)
- (b) LOUD-SCRAPBOOK: maximal, per-letter multicolor bouncy type, marker annotations everywhere, faint bg letters, nothing empty. (youth-energy hype)
- (c) BENTO-GRID: multiple items as rounded cards on ink base, ONE recurring motif as glue, halftone photos, condensed headlines. (multi-event "this week at AQ")
- (d) STICKER-KIT: varied-font sticker pile (script/mono/keycap/name-badge) on neutral cream, unified by white cut-outline. (voice/phrase posts)
- (e) Y2K-EDGY: acid accents + pixel font + chrome 3D on ink, bento cards. (events like Disco Diwali)
- (f) MATISSE CUT-PAPER: flat organic shapes, NO black outlines, hand-cut irregular letters, type-sandwich or scattered-word framing. Warm, artsy, human. (welfare/community warmth, arts). A softer alt to heavy-outline sticker style.
Also: tonal sticker coloring (2-3 shades of ONE hue) reads more designed than all-rainbow — use it.

## CAROUSEL BLUEPRINT (from Chuckle deck; the scaffold for multi-slide)
- Rounded-card slide frames, consistent across slides = cohesion.
- ALTERNATE full-accent slides and cream/white slides = rhythm across the deck.
- One highlighter-block keyword per headline (clashing accent).
- Retro/real photos in rounded white frames; sticker-logo slap on slides; big accent-square stats.
- First slide = scroll-stopper (loud); interior = readable; last = CTA/recruit.

## TYPE-HERO VOCABULARY (vary per piece so headlines never repeat)
marker-lowercase · per-letter-multicolor-bouncy · ransom/patchwork · puffy-3D-bubble · glossy-script-sticker w/ crop-marks · baseline-chaos overlap · liquify/warp · squished-heavy-condensed · wide-tracked bubbly · highlighter-block keyword · pixel/8-bit accent · words nested between big letters · isometric-3D-keycap letters.


## EVENT/PARTY PLAYBOOK (Classico/Mershe/Brewdowner cluster — for Disco Diwali, Paradox, Starry Nights)
ink or one-flat-accent base · fanned tilted flyer-stack OR bento cards · oval/scalloped stamp callouts for key info · gag/humor objects for personality · echoed/offset title for motion · themed motif as glue (music notes, flowers) · duotone-tint photo cut-outs · mono meta in corners · 3-color discipline even when loud.

## SCHEDULE DEVICE (from Events Calendar ref — directly usable for AQ drive/event lists)
Rounded pill-row stack on ink: rounded display header card → "IN <MONTH>" pill row → stack of date-rows, each = colored number-pill + colored label-pill (per-row accent pair) → footer split-pill + URL/CTA + star gap-fillers. Super clean + fun for "this month's drives/events."

## MORE FRAMING/TYPE OPTIONS (round-3 adds)
Framing: net/string container drawn over object cluster · envelope-spilling-flyers reveal · themed cut-out pile (ONE theme unifies chaos) · type-sandwich (title top+bottom around center art) · scattered-word all-over balance · single-hero-illustration + whitespace (a valid CALM register — not everything must be maximal).
Type: ghosted repeat-word bg (texture + branding at once) · echoed/offset duplicate title (motion) · hand-cut paper letters · overlapping-flat-shape multiply color-mixing.
Principle: a THEME unifies a chaotic pile — pick ONE per collage. Duotone-tinting photo cut-outs unifies a busy piece.

## THE ANTI-EMPTY DEPTH LAW (learned: pieces kept reading "too empty")
Every dense piece = 4–5 stacked layers, and the BACKGROUND is never plain:
1. active background (texture/pattern/blobs/photo + faint line-doodles drawn into the air across the WHOLE field)
2. mid-layer objects at VARIED sizes (mix ~60px and ~160px, not uniform) filling every dead zone
3. gap-filler marks in every negative-space patch (scan all quadrants; no dead patch > ~200px)
4. focal (headline / sticker-label type)
5. foreground stickers/bubbles overlapping even the focal
Background-layer shapes/marks may sit BEHIND text (low z-index, not audited). Foreground doodles/chips/bubbles MUST dodge text (tagged .measure, audited). NEXT ENGINE UPGRADE: auto-place fillers in measured free zones so density isn't manual whack-a-mole.

## FILES
- `core.py` — tokens, fonts, real assets, sizes. The raw materials.
- `build.py` — the generator vocabulary + render/audit gate + measure_free.
- `rhythm.py` — optional even-cadence engine + `snap()`.
- `doodles.py` — 20-shape pack (clean/rough + globe/leaf/paw/tree).
- `audit.py` — overlap + margin auditor (the gate); whitelists intended overlaps.
- `pieces.py` — the authored piece specs (each a small function). ADD new piece types here.
- `assets/` — fonts, real logo, real photos.
- `DECISIONS.md` — running log of every standing ruling. Read it before generating.

## LAYER 4.5 — EYE CANDY (BRAND-NATIVE richness — adaptive, never imported)
CRITICAL: eye candy must be expressed through AQ's OWN visual language, NOT generic design tricks. AQ is FLAT bold color + THICK ink outlines + cream/ink base + hand-drawn energy + print texture. Chrome gradients, glossy speculars, glassmorphism, soft blurred shadows, 3D-extrude-with-light = WRONG, they break AQ's identity. Do NOT use them.

AQ's richness comes from MORE OF WHAT AQ ALREADY IS:
- DEPTH via HARD-OFFSET INK SHADOW (flat, chunky) — not soft/glossy drop-shadows. And via LAYERED FLAT CUT-PAPER stacking (offset flat copies), not 3D light models.
- TEXTURE via HALFTONE dots inside fills + GRAIN + RISO grit — not gradient-mesh sheen.
- LIFT via THICK BLACK OUTLINES doing the work — not speculars/highlights.
- ENERGY via per-letter color, marker scribbles, doodle density, more flat elements — AQ's "more" is more flat stuff + texture, never gloss.
- PUNCH via BOLD FLAT COLOR CONTRAST (e.g. neon-on-ink, accent-on-cream) — not chrome.
- SHIMMER via hand-drawn INK sparks/stars — not white glassy glints.

THE EYE-CANDY PASS (run after composing, all brand-native):
1. Give the focal + key stickers HARD ink offset shadow (6px) + thick outline. 2. Put halftone/grain INSIDE flat fills (no dead-flat). 3. Add layered cut-paper depth to 1-2 hero shapes. 4. One BOLD-COLOR-CONTRAST hero (not a chrome object). 5. Sprinkle hand-drawn ink sparks + doodles in gaps. If it looks glossy/3D/SaaS, it's off-brand — flatten back to ink+halftone.
Helpers (finish.py, all brand-native): grain_layer, halftone_in, sticker, cutpaper_stack, hardshadow_text, rich_panel, spark.

## EYE CANDY IS MODE-CONDITIONAL (from "Architecture of Attraction" analysis)
CORE PRINCIPLE: eye candy is a STRUCTURAL ASSET deployed differently per mode, never a global "make it richer" dial. The rule is CONTROLLED IMBALANCE — decoration deviates from the rigid grid, then RESOLVES back into a structured unit. Structure (ACC) = skeleton; eye candy = muscle/skin; the tension between them is the delight. Uncontrolled decoration = cognitive overload + distrust.

FIVE DEPLOYMENT MODES (pick per piece; each gives decoration a specific JOB):
1. GRID-GOVERNED POP (events: Disco Diwali, Starry, Paradox): rigid grid holds text/dates; eye candy (halftone, bursts, lightning, jagged lines) deployed as FRAMING ELEMENTS that CONTAIN a zone — "everything inside this border is the same chaotic zone." Decoration frames text, doesn't spread across whole design. Convey NO info itself.
2. MINIMALISM FILTER (ventures, credible: ShikshAq, About, process): grid IS the hero; extreme negative-space management; decoration reduced to functional enhancement + ONE accent color reserved for CTA only. Negative space is structural MATERIAL that gives content weight. (This is the Functional Saturation rule made visual.)
3. TYPOGRAPHIC ARCHITECTURE (headlines, brand: milestone, myth, stat): hierarchy set BEFORE images; decoration applied to LETTERFORMS themselves (color-in-letters, pop outline, non-linear paths, per-letter treatment). The word becomes an illustration. Each letter = a contained, modular graphic asset.
4. DATA NARRATIVE (schedules, timelines, recaps): grid NON-NEGOTIABLE, data aligns perfectly; decoration ONLY as directional cues — colored flags per type, connecting arrows/lines showing flow, icons as bullets. Flair DIRECTS movement + highlights the date, never replaces or distracts from the data point.
5. COMPOSITIONAL ASSEMBLAGE (collage, moodboard, "this week", scrapbook): implied Z-pattern reading flow; elements in groups drawing the eye across; delight comes from JUXTAPOSITION (realistic object next to abstract doodle) + overlapping + varying scale for depth. Every element = a "discovered artifact" arranged into a story. NOTE: this mode often has NO single shine-hero — density of equal-weight elements IS the effect (confirmed by corpus: maximal-collage pieces run one_shine_hero=false).

KEY CORRECTIONS this locks in:
- "Every piece needs ONE hero" is register-dependent — TRUE for modes 1-4, often FALSE for mode 5 (assemblage), where equal-weight density is the point.
- Eye candy must FRAME/CONTAIN/DIRECT, not just fill. Ask "what structural JOB does this decoration do?" before adding it.
- Controlled Imbalance: place a big playful element OFF-center, then re-establish balance with a structured block below/beside it. Never random.

## EYE CANDY IS RELATIONAL, NOT ADDITIVE (the real unlock)
The recurring "eye candy still feels flat" problem is NOT solved by adding more techniques/stickers/textures. Richness comes from how elements RELATE to each other physically. Three relational qualities:
1. DEPTH LAYERING / OCCLUSION: elements deliberately tuck BEHIND and IN FRONT of each other (sticker corner slides under headline; badge covers a photo edge; number sits half-behind a block). Intentional overlap = real depth. FLAT = everything on one plane. NB: accidental collision (my 15K over its own label) is the failure mode — overlap must be DESIGNED (big element clearly in front, small clearly behind, with a shadow/outline selling the layer order).
2. SCALE DRAMA BETWEEN NEIGHBORS: put a HUGE element right next to a TINY one. Even weighting = boring. The violent size contrast between adjacent elements IS the eye candy. (ref: giant Q keycap beside tiny letters; 300px number beside 14px label.)
3. REACTIVE PLACEMENT: elements ENGAGE neighbors — an arrow points AT something, a sticker sits ON a corner, text WRAPS an object, a doodle leans AGAINST a letter. Decorations must not float independently in their own zone; they must acknowledge what's next to them.

RULE: after composing + eye-candy pass, do a RELATIONAL pass — (a) pick 2-3 element pairs and make one clearly overlap the other with correct z-order + shadow selling the depth; (b) ensure at least one violent scale jump between neighbors; (c) make every decoration point at / sit on / lean against something real. If elements only float in separate zones, it will read flat no matter how textured.

## MANDATORY PREVIEW STEP (never ship an image without self-reviewing it first)
The collision auditor only catches overlaps + margins. It does NOT catch compositional basics that make a piece look wrong: dead quadrants, sparseness, over-cramming, bingo-card uniformity, flatness. These slipped through repeatedly (roadsign bingo-card, giantserif dead-right-half).
RULE: after EVERY render, run preview.critique() BEFORE showing the user. It flags:
- dead_quadrant: a quarter of the canvas nearly empty → spread elements there
- sparse (fill<0.32): scale elements up / add mass (NOT just filler — resize first)
- crammed (fill>0.85): remove/shrink
- flat (contrast<0.20): add dark type / bolder color
- uniform: even grid spacing+size → vary scale + add overlap (kills bingo-card look)
If any flag fires, FIX and re-render before showing. Target: fill 0.45-0.75, contrast >0.22, all 4 quadrants >0.12, non-uniform.
