# SHIKSHAQ: the design language, as an engine format

**Read this whenever the ask names Shikshaq.** "Design a poster, story, page, carousel, deck slide or
screen for Shikshaq" means this document and `engine/shikshaq.py`, not AQ's palette, fonts, doodles or
craft layer. Shikshaq is a second brand on the AQ rails. The two share a cream-ish ground and nothing else.

Evidence tags: `[F]` fact read from code or measured in a real browser, `[V]` the site's own stated rule,
`[I]` my inference, `[?]` uncertain. Where the site's docs and code disagree, the code wins.

Provenance. Source snapshot: Shikshaq repo commit `766e43b` (2026-11-26), vendored in
`engine/assets/shikshaq/source/` and `brain/shikshaq_source/`. Live screens: `training_samples/shikshaq/`
(34 images, 390px and 1280px, read 2026-11-27 from `shikshaqkanitest`, the owner's test deployment, which
runs the same code against the same Supabase data; shikshaq.in itself sits behind a Vercel bot checkpoint
and was not scraped).

---

## 0. THE ROUTE (what to do when the ask names Shikshaq)

| The ask | Path | Notes |
|---|---|---|
| A page, landing page, screen, site section | `engine/shikshaq.py` section builders + `sk.doc(kind="page")` | start from `scratchpad/shik_landing_example.py` |
| A feed poster, story, square | `engine/shikshaq.py` `sk.poster([...])` + `sk.doc(kind="poster")` | start from `scratchpad/shik_poster_example.py`, or `python engine/shikshaq.py scaffold poster <name>` |
| The WEEKLY three-post Instagram plan with captions | `addons/shikshaq/` (Node) | planner, ledger rotation, caption gates. Its tokens were synced to this module on 2026-11-27 |
| A carousel from real photos | `brain/CAROUSEL_PLAYBOOK.md` for the mechanics, but ONLY this module's tokens, fonts, panels | AQ's logo treatment, doodles and photo scrims do not apply |
| A CAROUSEL (5 slides, 1080x1350) | `sk.poster` per slide + `sk.render_carousel` | start from `scratchpad/shik_carousel_exam_practice.py`; `sk.slide_header`, `sk.index_tag`, `sk.swipe_arrow`, a contact sheet of every slide |
| Remaking another brand's poster in this language | keep the MECHANISM, rebuild it from the builders with Shikshaq content | worked examples: `scratchpad/shik_remakes.py` (a chat bubble, a tabbed teaser card, a flipped scene) |
| A deck (16:9 slides) | not built | use this module's tokens and panel grammar; say so |

Never route Shikshaq through `engine.generate`, `core.ACCENTS`, `core.LOGO`, `doodles.py`, `shapes.sticker`
or `build.page`. Those are AQ. A pink star on a Shikshaq poster is the failure this document exists to prevent.

Every Shikshaq output goes through the gate (section 7) and the looking gate (`CLAUDE.md` section 3). Both.

## 1. THE ONE PARAGRAPH

A warm bone page (`#F9F5F1`) carrying stacks of 30px-rounded panels that touch with zero gap, separated
by fill alone. Saturated slabs (orange, indigo) arrive every few panels. One heavy display face (Archivo)
in mixed weights carries the voice, a quiet face (Geist) carries the body. Two MODES (teachers = orange,
papers = indigo) re-theme a whole page. Every subject has a tint from one formula. A mascot with
pointer-tracking eyes gives the brand a face. Depth is a hairline ring plus a crisp 1px drop. The skeleton
is crisp where people compare things and loud where they arrive, finish or get stuck. `[F]`

## 2. THE PRINCIPLES (the same list the gate and the builders enforce)

1. **Crisp skeleton, loud moments.** `[V]` Grids of comparable items stay calm (no tilt, tape, grain,
   thick outline). Hero, empty states, success, 404, footer and posters get character.
2. **Fill is the separator.** `[F]` Panels differ by fill, gap 0, 30px radius. No divider lines.
3. **Two modes, one switch.** `[F]` Teachers orange, papers indigo. A piece chooses a mode by what it is about.
4. **One primary action, at most two accents per viewport.** `[V]`
5. **Mixed weight is the headline device.** `[F]` 400 for the setup, 800 for the payoff, one family, one size.
6. **Category colour is data.** `[F]` `sk.subject_palette()`; never hand-pick a subject colour.
7. **Honest by construction.** `[F]` Every number traces to `sk.FACTS`. Empty states say what is true. No dashes in copy.

## 3. TOKENS (`sk.C`, proven against the site by `sk.verify_tokens()`)

Ground `[F]`: page `#F9F5F1` · card `#FCFAF7` · muted `#F0EAE2` · hairline `#E7DFD5` · panel (near-black) `#1B1A18`.
Text `[F]`: ink `#1F1F1F` · prose `#4A443E` · secondary `#6F675F` · tertiary `#776F67` (4.55:1 on page).

| | Teachers | Papers |
|---|---|---|
| action | `#FF8000` | `#4351FF` |
| tint | `#FFF4E8` | `#EDEEFF` |
| deep (text on tint) | `#A35200` | `#2E3AD6` |
| text ON the fill | **ink** (6.5:1) | white |

Fixed: WhatsApp `#25D366` on `#0B3D1F` (the only green CTA on the site), mint `#E3F7EC` / `#34B268`, peach `#FCECDE`.
Radii: slab 30, photo well 24, card 20, tile 13, control 12, pill full. Type: Archivo (wght 100 to 900, wdth 62 to 125)
for display, Geist for body (body weight 500, meta 400). Tracking on headings -0.045em to -0.055em, line-height about 0.96.

**Subject palette** `[F]`: `tint = hsl(h s 93%)`, `solid = hsl(h s l)`, `text = hsl(h 45 26%)`, `meta = hsl(h 28 34%)`.
**Badge text is MEASURED, not read from the spec's "dark" flag**: white if it clears 4.5:1, else whichever of
ink or white is higher. Consequence: Science and Geography greens, Maths orange, English teal and History ochre
take INK; Commerce, Computer and Hindi take white. (The first demo build hand-typed white on the Chemistry
tile. It was wrong, white is 2.72:1 there. The generator is right.) `sk.palette_from_key()` (the site's `paletteFromKey`) gives a decorative, stable colour to a thing with no subject (a paper cover).

**Depth** `[F]`: `--ring` is `0 1px 2px rgb(ink/.12), 0 0 0 1px rgb(ink/.08)`. A tinted card carries NO ring and NO
shadow (the tint carries it); a neutral card carries the ring. Saturated fills get a darker edge of their own hue.
**Motion** `[F]`: press .97 (.94 small, .99 card) in 150ms on `cubic-bezier(.23,1,.32,1)`, hover lift 2px on fine
pointers only, transform and opacity only, ambient loops desktop only, reduced motion removes movement.

## 4. LAYOUT GRAMMAR

- **The bento stack** `[F]`: a page is a vertical stack of 30px panels, gap 0. Live home order: bone, peach, lavender,
  bone x4, indigo, orange, peach, bone x3, dark footer. Saturation every few panels.
- **Saturated seams (S10)** `[F]` `[I]`: the design docs say two saturated fills never touch. The LIVE home puts
  indigo directly on orange once. Encoded: at most ONE orange/indigo seam per page, never the same hue twice
  (gate: `SAME-HUE`, `SATURATED-SEAMS`).
- **The first panel runs under the nav** `[F]`. The nav is three floating pills: a dark desktop pill (60px), a cream
  mobile pill with a hamburger, and a dark bottom pill whose active tab expands in the mode colour.
- **Hero formula** `[F]`: eyebrow, mixed-weight H1 with an inline avatar chip, live-count pills, mode toggle, ONE dominant
  search, quick chips; on desktop two fork panels (peach teachers, lavender papers) with mascots. `sk.hero()`.
- **Footer** `[F]`: dark slab, rounded top, a sentence with highlighted phrases, link pills, small print, then a giant
  `shikshaq` wordmark (Archivo, wdth 125) clipped by the slab edge. `sk.footer()`.
- **Posters** `[I]`: a column of rounded panels on bone with a 24px outer margin and a 64px radius (the site's 30px scaled
  to a 1080px canvas). Top panel bone with a mixed-weight headline, a saturated slab below with real content, ONE tilted
  sticker, ONE mascot. `sk.poster()`.

## 5. COMPONENT AND SECTION BUILDERS (all in `engine/shikshaq.py`)

Primitives: `icon`, `mascot` (orange awake, indigo asleep), `blob` (five moods, fixed colours, each with a documented
use: rough = error, meh = zero results, fine = neutral empty, good = confirmation, great = success), `logo` (white on
dark only, never recoloured), `sticker` (tilt -9 to 9, one per card, a third of a grid at most, never on a face), `mark`
(marker highlight), `eyebrow`, `numbered_heading`, `cat_tile`, `board_row`, `cover`, `stat`, `pill`, `chip`.
Sections: `nav`, `hero`, `fork`, `category_section`, `papers_slab`, `steps_slab`, `stats_section`, `eyes_section`,
`footer`, `poster`, `doc`. The CHARACTER SET (16 school objects, section 5a): `character(name, size, rot)`, `character_ok(name, ground)`, `CHARACTERS`, `CHAR_PALETTE`. Poster furniture: `sun` and `lobe` (the campaign's burst and four-lobe, ported from
`addons/shikshaq/campaign/characters.mjs`), `pchip` (a poster-scale chip, tilt -9 to 9), `swipe_arrow`, `index_tag`,
`slide_header`. Positioning: `art()` for DECORATIVE svg (marked `data-art`, the gate keeps it off the words) and `place()` for
TEXT-bearing objects (a chip, a badge). Mixing them up is the commonest misuse: a chip wrapped in `art()` reads as art on its own
words. Compose them; do not re-derive them.

Rules inside the builders: ink on orange, never white. Chips never tilt. Buttons are pills at 44px. Eyebrow and ordinal
labels use the TERTIARY text colour, not the site's quaternary (see section 9, deviation D2).

## 5a. THE CHARACTER SET (16 school objects; the owner approved the first four and asked for the rest, 2026-11-27)

`sk.character(name, size=160, rot=None)` returns an inline svg (decorative, `data-art`). The 16: pencil, star, kulhad (chai cup), warning,
book, backpack, ruler, calculator, clock, bulb, globe, trophy, notebook, cap, flask, compass. Each has a note on what it MEANS in
`sk.CHARACTERS` (a trophy is a milestone, never a claim about results). The review sheet is `scratchpad/shik_characters_sheet.py`.

The system, so a seventeenth follows it: a flat body, two ink dots (r 3.4, 12 apart) and one round-capped mouth (3.4), no outline, no
gradient, no shadow; COLOUR only from `sk.CHAR_PALETTE` (the site's own colours: blob moods, the burst yellow, subject solids, brand
orange and indigo, the warm neutrals; the test fails any other hex); a tilt of its own in `CHARACTERS`; the warning sign carries a mark
(a sign, not a creature). They are shapes, not mascots: no names, no stories. The orange mascot, the blobs, the burst and the lobe stay
the brand's characters; these are props for a scene.

**Ground safety is measured, not guessed.** `sk.character_ok(name, ground)` compares the character's silhouette colour with the ground
(floor 1.5:1). The review sheet shows it as a red ring. Known losses: the terracotta cup on orange; the ink calculator and cap on the dark
panel; the yellow pencil, bulb, trophy and warning on mint; the teal star on orange. Every character holds on bone, which is the default.

## 6. PAGE ARCHETYPES (panel sequences)

Landing: hero (+ forks) > category mosaic + board rows > indigo papers slab > orange steps slab > tinted stats > eyes
panel > dark footer. Directory list: back link, mixed-weight H1 with a live count, mode toggle, search, Filters button
with an applied-count badge, removable chips, cards with a cross-sell card inserted after the fourth; desktop adds a left
filter rail. Teacher detail: dark header block with photo, name and chips, a label/value grid, a mint panel holding the
honesty line and the WhatsApp button, reviews on peach. Reader: dark chrome, a cream sheet, question cards, a gate card at
question three, an orange cross-sell. Taxonomy landing: one templated fold (category icon tile, mixed-weight H1) then the
directory list. Index rows (subjects, schools): numbered H1 then rows with a letter tile. Apply: marker-highlighted promise,
a tilted sticker, one dark CTA, a 2x2 of tinted value cards. Auth: orange top half, dark bottom half. FAQ: numbered H1,
search, chips, accordion cards. 404: the numeral in the hairline colour at 132px, a voice line in the product's metaphor,
three stacked actions. Reference screens for every one are in `training_samples/shikshaq/`.

## 7. THE GATE (`sk.render` / `sk.session().render`, measured on the rendered DOM)

HARD failures: `OVERFLOW-X` (page wider than its viewport; names the widest elements and the fix), `CONTRAST` (WCAG per
element against the surface painted behind it, 4.5:1, 3:1 for large), `CLIPPED` (text sliced by an overflow:hidden
ancestor), `OFF-CANVAS` (posters), `COLLISION` (text on text, measured on GLYPH boxes, not block boxes), `ART-ON-TEXT` (a
mascot or `[data-art]` landing on words), `TAP-TARGET` (anything `data-tap` under 44px), `TINY-TEXT` (under 11px on a page,
20px on a poster), `SAME-HUE`, `SATURATED-SEAMS`, `FONT-FALLBACK` (every word is Archivo or Geist and whichever is used
loaded), `DASH`.
Also hard: `TEXT-COVERED` (a line of type partly painted over by an unrelated opaque object: the paint stack is walked at 9 points
per line), and `ART-ON-TEXT` ignores art that is covered by an opaque panel above it (a mascot peeking from behind a bubble).
Measuring rules: text is boxed PER LINE (a paragraph's union box counts the air beside a short last line); text inside a TILTED
group is compared in the group's own frame (the axis-aligned box of a rotated line over-reports).
INFO (printed every time, never silent): `ACCENT-DISPLAY`, the one orange seam.

Declaring intent, never silencing: `data-accent-display` (the site's heavy orange payoff, section 9 D1), `data-crop` (a
deliberate clip, like the footer wordmark), `data-bleed`, `data-deco` (ignore), `data-lowcontrast`, `data-tiny`, `data-font-ok`.

Copy: `sk.copy_gate(strings)` is a HARD gate on dashes, unprovable superlatives, unsourced social proof, brand-voice
clichés, and any digit that does not trace to `sk.FACTS` (class numerals in context and years pass). It WARNS when
`FACTS.asOf` is more than 14 days old: re-read the live counts before publishing.

Then LOOK at the PNG. The numeric gates passed posters that were visibly wrong while this module was built (a mascot
over a line of copy was invisible to the text-collision check until `ART-ON-TEXT` existed).

## 8. HOW TO DESIGN SOMETHING NEW FOR SHIKSHAQ (the loop)

1. Name the job: a parent reaching a teacher, or a student reading a paper. That chooses the MODE.
2. Take the facts you need from `sk.FACTS`. If the figure is missing or older than 14 days, ask for it or read the live
   site; never write a plausible number. **The paper count is ASKED EACH TIME** (D5): ask which of 655 or 661, then
   `sk.confirm("papers", N)`. Note `FACTS.known_inconsistencies` before using any count.
3. `python engine/shikshaq.py scaffold poster|page <name>`, or copy a worked example. Compose from the builders.
4. Copy through `copy_gate`. Render. Read every gate line. Fix the cause in the builder or stylesheet if it is a class of
   bug (`CLAUDE.md` section 8), not the one output.
5. Open the PNG and look: legibility, hierarchy, balance, rhythm, contrast, craft, density (`CLAUDE.md` section 3).
6. Companion art piece (`CLAUDE.md` standing rule) when the session produced engine output.

## 9. DEVIATIONS FROM THE SITE AND OPEN DECISIONS (do not "fix" these silently)

- **D1 (RULED 2026-11-27: allow it, declared and reported).** The site's signature heavy orange payoff on bone (`#FF8000` on `#FCFAF7`) measures
  **2.42:1**, under the 3:1 large-text floor. The live hero does it at 29px on mobile and 58px on desktop. The engine
  allows it ONLY when declared with `data-accent-display`, only at 28px or more and bold, and prints it on every render.
  The compliant alternative is `--orange-deep` (`#A35200`), which looks brown; the owner chose to keep the site's look.
- **D2 (RULED 2026-11-27: keep the darker grey).** The site's quaternary text `#8A8279` (labels, ordinals) is 3.49:1 and the site records it as "a
  small step under the floor". The engine uses tertiary `#776F67` (4.55:1) for eyebrows and ordinals, visually near-identical.
- **D3 (deliberate).** Small label text on an indigo or orange slab is solid white or full ink, not a translucent tint, which
  measured 3.5:1 and 3.8:1.
- **D4 (fact).** `brand-deep` is `hsl(30 100% 32%)` = `#A35200`. The site's comment says `#A35100`, and the Node addon carried
  `#B35900` from before the 32% change (the addon was synced to `#A35200` on 2026-11-27, as was its secondary text `#6F675F`). The engine computes it from the HSL, which is what renders.
- **D5 (RULED 2026-11-27: ask each time).** Paper counts disagree between surfaces: 655 (home hero, About, Auth) vs 661 (Browse
  cross-sell). The engine hardcodes NEITHER: `sk.need("papers")` raises, naming the question, until `sk.confirm("papers", N)` (or
  `SHIKSHAQ_PAPERS=N`) records the owner's answer for that run. Copy containing 655 or 661 fails `copy_gate` as an UNCONFIRMED count.
- **D6 (info).** The site's design docs call the thick-outline `.sticker` a core device, but it ships almost nowhere. The
  shipped sticker is a tilted pill. Thick outlines survive mainly on empty-state icon tiles. Do not carry AQ's outline and hard
  shadow into Shikshaq.

## 10. BUG CATALOG (flaws found while learning and building this, each now a check or a default)

| Failure | Guard |
|---|---|
| A page 425px wide in a 390px viewport: a horizontal scroller inside a grid cell forced the column open | gate `OVERFLOW-X` names the culprits; the section builders put `min-width:0` on grid items |
| The Node addon's token copy drifted from the site (old text ramp, old orange-deep) | `verify_tokens()` recomputes from the vendored source; the test breaks a token on purpose to prove it bites |
| A mascot landing on a headline passed every text check (art is not text) | `ART-ON-TEXT` |
| An ordinal beside a padded block heading read as a text collision | collision and clip checks use GLYPH boxes (a Range over the element's own text nodes) |
| A font that a page never uses never loads, so a naive "fonts loaded" check false-failed | `FONT-FALLBACK` checks only the faces actually used, and rejects any off-brand face |
| Hand-typed white on a Chemistry tile (2.72:1) | `cat_tile()` uses the measured badge colour |
| A "Search" pill stretched and lost its icon because `.search span{flex:1}` matched the pill | the placeholder carries its own class |
| `poster()` panels did not carry their fill class, so label colours did not switch on indigo | the class rides along |
| The scaffold shipped without `data-accent-display` and failed its own gate | the test EXECUTES every scaffold as shipped |
| `<i>` used as a button element rendered its label italic | `.pill` sets `font-style:normal` |
| Counts disagreed between surfaces and one was quietly picked | recorded in `FACTS.known_inconsistencies`, and the paper count is ASKED EACH TIME (`need`/`confirm`) |
| A pill sat on the last line of a paragraph and the gate said CLEAN | `TEXT-COVERED` walks the paint stack under each text line |
| The "Free" sticker on the desktop fork was hidden under the nav pill (invisible by eye in the first demo build; found by `TEXT-COVERED`) | the first panels reserve the nav's 72px INSIDE the panel, like the live site's `NavReserve` |
| A paragraph's union box counted the empty space beside its short last line, so a tick beside it "collided" | per-LINE boxes |
| Lines of a tilted card read as colliding with each other (the axis-aligned box of a rotated line) | in-plane comparison in the tilted group's own frame; a real overlap there still fails |
| A mascot peeking from behind an opaque panel read as landing on the text above it | the gate walks the paint stack and skips art that is covered |
| A chip wrapped in the decorative-art helper read as art landing on its own words | `place()` for text-bearing objects, `art()` for decoration |
| `100% free!` failed only as an untraceable number: `\b` never matches after `%`, so the superlative rule never fired | `(?<![\w.])100\s*%` |

## 11. REFRESHING THE SNAPSHOT

When the site changes: re-copy `src/index.css`, `tailwind.config.ts`, `src/lib/subject-palette.ts` and the `ui/` components
named in `engine/assets/shikshaq/source/` from the Shikshaq repo, run `python engine/shikshaq.py selftest`. It names every
drifted token. Update `sk.C`, the `PAIRS` map if a variable was renamed, and `FACTS` (re-read the live counts, set `asOf`).
Then `python scratchpad/test_shikshaq.py` (155 assertions).

## 12. NOT VERIFIED `[?]`

shikshaq.in itself (the test deployment may lag it), signed-in screens (dashboards, checker, HOD desk, admin, games),
real-device performance, the exact EyesPanel blink and gyro behaviour (the engine's eyes follow the pointer only), the bottom
navigation pill (specified here, not built), a 16:9 deck (the carousel path is built, the deck is not), whether the blur on later teacher cards for signed-out visitors is a deliberate gate.
