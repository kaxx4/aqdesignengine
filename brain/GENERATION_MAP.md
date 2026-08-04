# GENERATION MAP — the architecture for a long-term autonomous content generator

Goal: `oneshot(brief)` produces a finished, on-brand AQ piece with no per-piece steering, and keeps
doing so across hundreds of posts without collapsing into a template.

Read `brain/VISUAL_DNA.md` first — it establishes WHY this order is mandatory. Short version: the
engine currently reaches ~20% of its own reference corpus, so automating decisions today would just
produce fast, confident repetition. Vocabulary before autonomy.

---

## THE PIPELINE

```
BRIEF                      the ONLY human input. Thin: a topic, optionally an intent.
  |                        e.g. {"topic": "sunderbans medical camp", "intent": "recruit/warm"}
  v
[1] DIRECTOR               TASTE.md's decision cascade, as code.
  |                        intent -> archetype -> base_field -> palette_mode -> type_treatment
  |                                -> eyecandy_mode -> density seed
  |                        Every choice CONSTRAINS the next (a cascade, not 6 independent rolls).
  |                        Consults the LEDGER to force departure from recent pieces.
  |                        OUT: a committed SPEC.
  v
[2] COPYWRITER             spec + brief -> content dict (kicker/number/label/chips/band/body).
  |                        Combinatorial + ledger-deduped, in AQ voice.
  v
[3] COMPOSER               ARCHETYPES[spec.archetype](content, spec)
  |                        + craft layer: uniform sticker_treatment on every object
  |                        + word-level type layer (VISUAL_DNA §4)
  |                        + density via edge-cropped mass / ghost-type (VISUAL_DNA §5)
  |                        PHOTO PIECES: placement comes from vision.plan_spots(), never hand coords
  v
[4] GATE                   preflight, reading the archetype's INTENT PROFILE
  |                        (allow_bleed / allow_occlusion / heroless_ok / palette ceiling)
  v
[5] RENDER + CRITIQUE      Playwright -> preview.critique -> encoded self-correction loop
  v
[6] LOOKING GATE           the one irreducible human/LLM step. Never self-certified.
  v
[7] LEDGER WRITE           archetype, accents, phrases, skeleton -> so the NEXT call departs.
```

---

## THE FOUR LAYERS THAT DON'T EXIST YET

### [1] DIRECTOR — `engine/director.py`
Encodes the TASTE.md cascade. Today steps 1–5 of that cascade are hand-fed via `JOBS`; that is the
literal definition of "not autonomous."

```
decide(brief, ledger) -> spec {
    archetype, base_field, palette_mode, accent_idx, type_treatment,
    eyecandy_mode, density_seed, intent_profile
}
```
Rules it must encode:
- **intent → archetype affinity** (a stat-led brief wants `number_hero`; a roster/list wants
  `card_grid_board` or `stacked_zones`; a single defiant line wants `giant_type`).
- **TASTE.md test B, mechanised:** if the chosen archetype OR reading axis matches either of the last
  two ledger entries, force the next-best candidate. "Two pieces in a row sharing a skeleton =
  failure" becomes a hard constraint, not an aspiration.
- **cascade coupling:** `base_field` constrains `palette_mode` (a flooded field can't also run
  container-fill accents), which constrains `type_treatment` (reserved type colour, VISUAL_DNA §2).

### [2] COPYWRITER — `engine/copy.py`
`ENGINE_STATE.md` already records the failure this fixes: the content banks hold 4 and 10 entries, so
"exact wording repeats across the 44 batch samples." A generator that repeats its copy every ~10
posts is not a long-term generator.

Needs to be **combinatorial, not a bank**: slot grammars per archetype (kicker / hero / label /
chips / band / body), filled from brief nouns + AQ voice patterns, with the ledger rejecting any
phrase used in the last N pieces. Hard rule inherited from CLAUDE.md §9: never fabricate a stat — a
number must come from the brief or be omitted.

### [4] VISION — `engine/vision.py` ✅ **BUILT THIS SESSION**
Removes the last manual step in photo carousels. See "Built" below.

### [5] LEDGER — `engine/ledger.py` + `brain/GENERATION_LEDGER.json`
Append-only record per generation: archetype, base_field, palette_mode, accent_idx, copy phrases,
reading axis, output path. Read by the director (variety) and copywriter (dedupe).

This is the component that makes the engine *long-term* rather than merely *automatic*. Without it,
autonomy and repetition are the same thing.

---

## BUILD ORDER (dependency-correct — do not reorder)

| # | Work | Why it must come first |
|---|---|---|
| 1 | **Gate intent profiles** (VISUAL_DNA §6) | Until gates carry per-archetype intent, every new archetype fights `bounds_check` / `collision_check` / `dominance_check`. Blocks everything downstream. |
| 2 | **Shared primitives** — `sticker_treatment`, `off_frame`, `connector`, `word_layer`, `layered_sheet`, `ticker_bar`, `stitch_stickers` | Every new archetype composes from these; building archetypes first means writing them 4×. |
| 3 | **4 archetypes** — `card_grid_board`, `sticker_pile`, `photo_card_stack`, `diagonal_cascade` | Takes corpus coverage ~20% → ~60%. `diagonal_cascade`'s spec is already fully derived from `ca484173fb`. |
| 4 | **Ledger** | Director and copywriter both depend on it. |
| 5 | **Director** | Needs a vocabulary worth choosing from (3) and memory to vary against (4). |
| 6 | **Copywriter** | Needs the spec from (5) to know which slots to fill. |
| 7 | **`oneshot(brief)`** + batch proof + looking gate on every output | The integration. |

---

## STATUS

**Built this session**
- `engine/vision.py` — automatic placement intelligence for photo pieces. Replaces hand-picked
  free-zone coordinates, which caused every face-collision and edge-clip in the Sunderbans batch.
  - `analyze()` — per-cell edge-energy + variance + skin-fraction + luminance map (PIL/numpy only).
  - `background_grid()` — the key idea: **topology, not brightness, separates background from
    subject.** Pure flatness is not enough — measured on the Sunderbans photos it happily chose
    luminance-4–33 spots, i.e. the volunteers' black hoodies, which are perfectly flat. Real
    background runs off the edge of the frame; a subject is a flat island enclosed by busy pixels.
    So only free components touching the top edge (or a side edge while sitting in the upper frame)
    qualify. The bottom edge never qualifies — in these photos it is always foreground.
  - `plan_spots()` — ranks by clearance, spreads picks (kills the "6 doodles crammed in one sky
    pocket" failure), derives SIZE from real clearance (natural 60/90px variety instead of a guessed
    constant), applies a **vertically-aware clearance floor** (3 cells up top where it's sky, 4 lower
    down where a "gap" is usually just space between two people), and ends with a **pixel-level skin
    veto** on the padded footprint to catch faces smaller than a grid cell.
  - `best_band()` — encodes "if the sky is too cluttered, put the chip in the scrim band" as a
    measurement rather than a judgement call.
  - `pick_visible()` — generalises `layout.invisible_color_check` from "vs the page bg" to "vs the
    actual pixels behind this element," the photo case the old check could never handle.
  - Validated by rendering placement overlays and LOOKING at them (`scratchpad/vision_debug.py`),
    iterating through three real defects: dark-clothing false positives → topology fix; doodles in
    the narrow sliver beside a face → clearance floor; over-conservatism (1–2 spots) → 30px grid.
  - **Known limitation, deliberately conservative:** background enclosed by foreground (e.g. the
    Sunderbans sunset sky framed by pillars and trees) fails the border test and is skipped. False
    negatives cost a placement; false positives cost a doodle on someone's face. Wrong in the cheap
    direction on purpose.

- `brain/VISUAL_DNA.md` + `brain/dna/batch_01..06.md` — all 44 references analysed.

**Not built** — layers 1, 2, 5 above, plus build-order items 1–3 and 7.

---

## THE STANDING PRINCIPLE

`ENGINE_STATE.md` already says it: *"If any output quality depends on LLM judgment rather than an
encoded rule, that's a bug in the ENGINE."* This map is the list of judgments still being made by
hand. Each one closed is one fewer reason a generation needs supervision.

The looking gate (step 6) is the deliberate exception and stays forever — but per VISUAL_DNA it
should be catching *taste* questions, not "the chip is on someone's face." That class is now a rule.
