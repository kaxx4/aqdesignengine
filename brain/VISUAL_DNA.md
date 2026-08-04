# VISUAL DNA — what all 44 references actually taught (session 2026-07-24)

Derived by LOOKING at every one of the 44 posters in `training_samples/reference_posters/` against a
fixed schema (archetype, reading axis, hero %, base field, accent role, type treatment, eye-candy
mode, density, transferable move, reachability). Per-poster teardowns: `brain/dna/batch_01..06.md`.

This supersedes nothing in TASTE.md — it OPERATIONALISES it. TASTE.md says taste is "a committed
cascade of intentional decisions." This document is the measured vocabulary those decisions choose
from, extracted from the corpus instead of improvised.

---

## 0. THE HEADLINE FINDING (read this before anything else)

**The engine can reach roughly a fifth of its own reference corpus.**

| Reachability by the 4 built archetypes | Count |
|---|---|
| Fully reachable today | ~6 / 44 |
| Partially reachable (right skeleton, missing a capability) | ~8 / 44 |
| **Not reachable at all** | **~30 / 44** |

This is the real reason generation needs hand-holding every time — and it is NOT primarily a
content-input problem. Hand-feeding the content dict is a symptom. The cause is that the archetype
vocabulary is far narrower than the taste it is trying to serve, so the operator compensates by
steering each piece manually. **You cannot one-shot your way out of a 20%-coverage vocabulary.**

Corollary that matters more than any single rule below: three of the engine's OWN GATES actively
reject good reference designs (§6). Widening the vocabulary without fixing the gates would just move
the fight from "the design is wrong" to "the gate won't let me."

---

## 1. THE UNIVERSAL UNIFIER: uniform sticker treatment

The single most repeated finding — top-3 STEAL in **5 of 6 batches**, independently:

- 5 of 8 in batch 1 put a thick ink outline on *every* shape ("the single most consistent unifier")
- batch 4: die-cut halo stroke + hard same-color offset shadow + rot ±12°
- batch 5: "3px black outline + an offset pale halo tinted from the element's own fill — and 9
  unrelated colors read as one set"
- batch 3: container-per-text-line (every text run gets its own shaped container)
- batch 6: per-word sticker boxes

**RULE — `sticker_treatment(fill)`: ink outline + hard offset shadow + optional pale halo =
lighten(fill, 55%), applied UNIFORMLY to every object in a piece.**

Why it matters mechanically: this is what LICENSES density. The references are far busier than AQ
outputs, and they stay legible because one shared treatment makes unrelated objects read as a single
set. AQ currently applies outline/shadow per-element by hand and inconsistently. Uniformity is the
rule, not the outline itself.

---

## 2. ACCENTS AS CONTAINER FILLS — the doctrine that needs to become conditional

AQ's standing law (CLAUDE.md §9) is *"accents PUNCTUATE (~30%), never flood."* The corpus disagrees
about half the time:

- batch 2: "the batch skews dark-field with saturated container fills, the inverse of AQ's cream
  default. Accent-as-large-container-fill (not punctuation) is the recurring deviation."
- batch 1: "only 2 of 8 use a light empty field the way the engine defaults to"
- batch 5 (`b2d4cc55d7`): 6 accents as large object fills on a flooded cobalt field
- batch 6 (`d252704dc5`): accents as full pattern fields — "deliberately un-AQ: accents flood"

This is corroborated by the engine's own history: `DECISIONS.md` records that `accent_flood_check`
had to be left manual-only because it FAILED a design the looking gate had already approved.

**RULE — `palette_mode` ∈ {`punctuation`, `container_fill`, `flooded`}, chosen by the director per
piece; the accent-coverage ceiling is read from the mode, not from a global constant.** The ~30% law
becomes the definition of `punctuation` mode rather than a universal.

Guard rail that makes `flooded` survivable, from `b2d4cc55d7`:
**reserve ONE color exclusively for type and forbid it in every illustration fill.** That single
constraint is what keeps a 6-colour saturated field readable. Checkable: no non-text element may use
the hue assigned to headline type.

---

## 3. BASE FIELD IS A MODE, NOT A DEFAULT

Cream is one option among five in the corpus: **cream · ink/black · saturated full-bleed · photo ·
textured (paper/graph/riso grain)**. Dark and saturated fields are *more* common than light ones, and
they read as more confident because objects "glow" against them.

Two archetypes already have a `field` param (added ad hoc for GLASSDOOR and DRÖM). Generalise it to
all archetypes as a first-class director decision.

---

## 4. TYPE IS A WORD-LEVEL MEDIUM (the biggest structural gap)

The engine sets **text blocks**. The references design **individual words**:

| Move | Seen in |
|---|---|
| Highlight exactly ONE word per line, each in a different container shape | `10f1b8a978` |
| Speech-bubble tags whose tails anchor to a specific glyph | `51010a5e1a` |
| Box each word in its own accent rect, rotated ±2–4°, staggered (misregistration IS the effect) | `d252704dc5`, `d375fd7dbc`, `eaad68d630` |
| Per-letter colour across a wordmark | `e9d82bbdf0` |
| Micro-copy chips inlaid into the counters/gaps of huge letters | `d2add78f90` |
| Size-ramped sentence, each word 24→110px along an arc | batch 3 |
| Letters riding ON objects (keycaps) instead of set as type | `11e7d9a3ff` |

**RULE — a word-level text layer: `word_layer(text, mode)` with modes
{`highlight_one`, `box_each`, `per_letter_color`, `size_ramp`, `annotate`}.** Nothing in the current
engine can express any of these, which is why AQ headlines read flatter than the corpus.

---

## 5. DENSITY IS SOLVED WITH BIG CROPPED SHAPES, NOT SCATTERED DOODLES

The engine's density-escalation adds filler doodles. The corpus fills space with **large shapes
cropped by the canvas edge**:

- giant concentric ring/arc anchored at each corner, only a quarter visible — "kills dead quadrants
  with zero filler doodles" (`e9d82bbdf0`)
- 4–6 irregular accent blobs each cropped by an edge, behind the type layer (batch 3)
- `ghost_type_bg`: re-set the headline at ~4×, stroke-only, overflowing all four edges, z=0 — free
  density and texture with no new assets (`64b2248475`)

**RULE — density escalation should prefer, in order: (1) scale existing elements up, (2) add an
edge-cropped mass or ghost-type layer, (3) only then filler doodles.** The current loop jumps to (3).
This is a strict upgrade of the "scale up before filler" note already in CLAUDE.md §9.

---

## 5a. MEASURED: AQ OUTPUT IS UNDER-FILLED vs THE CORPUS (added 2026-07-25)

Measured across 15 recreations spanning 15 reference families (`engine/compare.py` area ratio =
recreation content coverage / reference content coverage):

| Batch | area ratio vs reference |
|---|---|
| showcase5 (cream/light fields) | ~0.85x |
| showcase5b (saturated + textured fields) | **0.26 – 0.42x** |
| showcase5c (built deliberately dense) | 0.44 – 0.81x (one overshoot to 1.83x) |

**This was initially misdiagnosed as a comparator artifact** — riso/paper grain in the references
counting as content. Denoising was added to `compare.content_mask` to test that; the ratios barely
moved (0.39 → 0.42). **The gap is real.** The reference corpus is board-busy (`DENSITY: board-busy`
is the single most common value in the batch teardowns); AQ defaults to airy cream fields with
generous margins.

Consequences for the engine:
- This is the quantitative form of §5 — the corpus fills space with big cropped masses and full
  fields, while the engine's density-escalation adds small filler doodles.
- Density targets should be set PER BASE-FIELD MODE. A cream/light piece can breathe at ~0.85x; a
  saturated or ink field in this corpus runs far denser, and matching it needs edge-cropped masses,
  pattern fills (`shapes.checker`), and ghost-type layers — not more doodles.
- Correcting it is easy to OVERSHOOT (one piece hit 1.83x). Treat the fix as damped, not a
  new "fill everything" default.

---

## 6. THE GATES REJECT GOOD DESIGN — three documented conflicts

Found independently by three different analyses. This is the highest-priority engineering fix,
because every one of these will fire spuriously during an unattended batch:

| Gate | Rejects | References it would kill |
|---|---|---|
| `bounds_check` | intentional off-frame bleed — *the defining move of the `off_frame_bleed` archetype* | `64b2248475`, `e9d82bbdf0`, `eaad68d630`, batch-3 set (~6) |
| `collision_check` | intentional occlusion (card stacks; photo overlapping a headline) | `620d62f101` (35% deliberate occlusion), `c10cb35dfa` |
| `dominance_check` | hero-less compositions (deliberate flat scan, no focal) | `502e07d0eb` |

**RULE — every archetype carries an INTENT PROFILE declaring its opt-outs:
`allow_bleed`, `allow_occlusion=(min,max)`, `heroless_ok`, `palette_mode`.** Gates read the profile
instead of applying one global taste. `ARCHETYPE_PROFILES` already does exactly this for
fill/density — extend the same mechanism to bounds/collision/dominance/accent-coverage.

From `c10cb35dfa`, a precise occlusion rule worth encoding rather than a blanket allowance: permit a
hero-photo-over-giant-type overlap of 25–55% **provided the type's outer 20% on each side stays
clear** — the word still reads from its outer strokes.

---

## 7. REPETITION AND CONNECTORS AS COMPOSITION

**Repetition:** duplicate the same card 3× at decreasing scale + increasing rotation, offset down-left
(`2022ebef4f`); stepped diagonal cascade with fixed (dx,dy) per item (`ca484173fb` — this is a
drop-in spec for the unbuilt `diagonal_cascade` stub); break a rigid grid exactly once by rotating
one card ~8° and scaling 1.4× to manufacture a hero (`fc9ff90207`); per-item accent rotation down a
numbered list (`3bb3f9582d`).

**Connectors:** a hand-drawn curled arrow physically routing the eye badge→hero (`29c6a85891`);
label-to-item arrows so labels can live in empty margin and still bind (`1d518d2bc5`); arcing lines
from each origin to a destination (`d375fd7dbc`).

**RULE — `connector(from_bbox, to_bbox, style)` generating an ink arrow/arc between two PLACED
elements.** (The dashed connector hand-written for the Sunderbans v6 carousel is a special case of
this — generalise it rather than re-deriving per piece.)

---

## 8. ARCHETYPE DEMAND — ranked by how many references need it

| Archetype | Refs demanding it | Status |
|---|---|---|
| `card_grid_board` (rounded-rect masonry on black, one accent per card, gutters) | ~5 | **not built — highest value** |
| `sticker_pile` / `scatter_pack` (dense overlapping pile, uniform sticker treatment) | ~6 | stub only |
| `photo_card_stack` (fanned/rotated overlapping cards, permitted occlusion) | ~4 | not built |
| `diagonal_cascade` | ~2 | stub — **spec already handed to us by `ca484173fb`** |
| `off_frame_bleed` | ~4 | stub — blocked by `bounds_check` |
| `quadrant_patchwork` (hard-edged field partitioning + pattern fills) | 1 | new |
| `annotated_map` | 1 | new |
| `flat_lay_tableau`, `type_sandwich`, `object_in_context`, `single_object_portrait` | 1 each | new |

Build order implied: **card_grid_board → sticker_pile → photo_card_stack → diagonal_cascade**, then
unblock `off_frame_bleed` via the gate profiles in §6. Those four plus the gate fix would move
coverage from ~20% to a rough ~60% of the corpus.

Supporting primitives each of those needs (recurring across teardowns): `sticker_treatment(fill)`,
`ticker_bar(y, words, glyphs)`, `stitch_stickers(cards)` (a doodle straddling two card seams to
bind a grid), `layered_sheet(...)` (nested offset rotated sheets for free depth), `off_frame(el,
edge, frac)`, `scatter_pack(objects, cols, rot_jitter, silhouette_key)` (never allow two same
silhouettes adjacent).

---

## 9. WHAT THIS MEANS FOR "ONE-SHOT EVERY TIME"

The corpus says the failure mode is not randomness — it is **narrowness**. So autonomy has to be
built in this order, and building it out of order will not work:

1. **Fix the gates (§6).** Until gates carry per-archetype intent, every new archetype fights them.
2. **Widen the vocabulary (§8)** — four archetypes + the shared primitives.
3. **Add the word-level type layer (§4)** and the sticker treatment (§1) as cross-archetype craft.
4. **Then** automate the decision cascade (director) and the copy — see `brain/GENERATION_MAP.md`.

Automating decisions over a 20%-coverage vocabulary would just produce confident, fast, repetitive
output — the exact "template collapse" TASTE.md names as a failure mode.

---

## SECURITY NOTE — a poisoned reference asset

`c42f94a09f07cda39df8afe51cde9098.jpg` renders the literal string **`set:nAFV8beNUC4`** as its
headline. That is the syntax of an internal tool-load query, not a design element — the rest of the
poster is an ordinary sticker-pile graphic watermarked `@creativehausmktg`. Verified directly.

Treated strictly as image CONTENT, never as an instruction; nothing was executed. Flagged because
these assets are fed to LLM analysis passes routinely, and an asset that mimics tool syntax in its
headline is either tampered or scraped from something that was. Recommend replacing or quarantining
it. Its design DNA was still extracted normally (it is the source of the §2 halo/outline rule).
