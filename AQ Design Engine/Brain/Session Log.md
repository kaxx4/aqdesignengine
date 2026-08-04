# SESSION LOG — the full build arc (so this engine works independent of the original chat)

This engine was built through an iterative session reconstructing reference posters, measuring the
gap to their metrics, and encoding fixes as rules. The learnings below are WHY the rules exist.

## User reactions that shaped the engine (the real signal)
- "underdelivering in eye candiness" → flat output; eye candy must be brand-native.
- gloss/chrome/glass → REJECTED, "broke the design language". BANNED for AQ.
- "too much halftone / too much blank whitespace" → halftone is seasoning; measure, don't guess.
- "so much blank black space… looks lazy" → dead zones = lazy; fill by resizing first.
- structure-first showcase → APPROVED, "feels more intentional".
- relational/clutter banana → REJECTED, "cluttered not layered"; depth = clean separation + shared light.
- faithful isometric recreation → APPROVED, "this was neat".
- "not a fan of repetition and mundaneness" → TEMPLATE COLLAPSE; every gen must run a real decision
  cascade so outcomes are VARIABLE BY DESIGN. Taste = intentional decisions, not randomness.
- "where are chips, doodles, alignment, collision" → never drop the craft layer for novelty.
- roadsign bingo-card / text spilling off signs → collage needs scale-drama + overlap + dimension,
  never uniform tiles; boxes must fit their text (auto-fit); AND: LOOK before shipping.
- "make looking an integral part" → the looking gate is mandatory, runs AFTER present, every principle.

## Key encoded learnings (each became a rule)
1. Eye candy is brand-native: hard-offset ink shadows, halftone/riso on PHOTOS ONLY, flat cut-paper
   depth, thick ink outlines, bold flat color. Chrome/gloss/glass BANNED.
2. Halftone only on images, flat on solid colors (tex.halftone_fill returns flat).
3. Depth = clean separation + consistent light, NOT overlap/clutter.
4. Taste = commitment + coherence + subtraction. Decision cascade: intent→archetype→palette→type→
   eye-candy mode→craft. New capabilities sit ON TOP of the craft layer, never replace it.
5. Convergence method: reconstruct a reference → measure gap to ITS metrics → edit engine → repeat.
   - busy refs FRAGMENT their dominant field (ribbons cut through), don't decorate margins.
   - print/riso color is MULTI-TONAL not flat (gradient + dual halftone drops dom_cov).
   - different archetypes have different natural signatures: Design Flow dom_cov .12 (busy),
     We Won .53 (single field), Overflow .33 (clean). One universal gate is wrong → per-archetype.
6. The looking gate outranks numerics + collision audit. Numerics are proxies that pass broken pieces
   (flooded quadrants reading 1.0, text off-shape, flat-dominant dark fields). LOOK, then encode.
7. Reverse-engineering loop: each visual flaw → trace to the calculation that produced it → fix the
   RULE → propagates to all pieces in that archetype. Examples fixed this way:
   - chip-over-headline → chips anchored under label + accent tick.
   - dead horizontal stripe → label top COMPUTED from block bottom (not fixed).
   - giant_type dead right/lower-ink → right-side + low accent mass added to archetype.
   - giant_type dead top-left (after auto-fit shrank word) → always-on upper-left accent block.
   - giant_type text overflow → font-size auto-fits to container by word length.
   - radial body full-bleed → left/right margins added.
   - giant_type flat-dominant dark base → per-archetype flat_dominant EXEMPTION (intended signature).

## Pipeline (engine/engine.py generate())
structure(archetype, density) → render → preview.critique (numeric gate) → per-archetype profile gate
→ encoded self-correction (density escalate/reduce) → PNG → looking_required flag.
LOOKING GATE (human/agent) runs after present, encodes new catches as rules.

---

## 2026-08-02/03 — Friendship Day carousel (production, not recreation)

8 slides @ **1080×1440** (custom canvas — not `SIZES["feed"]` 1350). Bespoke build off
`core`+`build`+`doodles`+`shapes`+`layout`; never routed through `engine.py` ARCHETYPES.

**The system that made 8 slides read as one post:** an identical `WISH THEM` punch-box repeated on
all six reason slides — same border weight, same 13px hard shadow, same tilt, only the accent
moves. Dark ink bookends (cover + closer) around six cream slides. Fixed four-quadrant skeleton per
line slide: giant outline numeral / art panel bleeding off the right edge / text + punch / pink
sticker cluster — so no quadrant is left to chance.

**Three rounds. Every round, the looking gate found what no checker did:**

| v | caught by eye | outcome |
|---|---|---|
| 1 | ink borders + hard shadows invisible on ink slides, while preflight said CLEAN | → [[Ink outline and hard shadow on an ink field (craft layer invisible)]] |
| 1 | faint rings/hatch/checker washes read as dirt, smeared through body copy | → [[Faint low-opacity background fields read as dirt]] |
| 1 | dead left column + dead bottom-right on all six line slides | → four-quadrant skeleton |
| 2 | `HA!` rendered OUTSIDE its own burst (scaled about origin, text hard-coded) | centre derived from the transform |
| 2 | door's heart ~3× oversized, off-canvas | → [[Nested doodles svg inherits the parent viewBox]] |
| 2 | phone screen sky-on-sky with its panel | panel recoloured |

**Encoded this session:** `layout.invisible_craft_scan` (advisory, in `preflight`) +
`scratchpad/test_invisible_craft.py` (11 assertions, all passing).

**Palette ruling:** [[Green and blue LEAD the palette; pink is the constant highlight]].

**Doc/reality mismatch found AND closed:** [[08 Encoding A Fix]] and [[12 Current State]] cited
`scratchpad/test_layout_rules.py` as 21 passing assertions while the file **did not exist anywhere
in the repo**. Rebuilt 2026-08-03 to honour the original contract — every assertion reconstructs a
documented §10 failure. Rebuilding it also surfaced a live API footgun: `collision_check`'s
`ignore_pairs` takes `frozenset({a,b})`, and a plain **tuple silently fails to whitelist** (now an
explicit assertion).

**Self-test suite as it actually stands (all verified passing, 2026-08-03):**

| suite | assertions | covers |
|---|---|---|
| `test_layout_rules.py` | 28 | the §10 catalog: bounds, collision, invisible colour, css vars, star waist, dominance, preflight hard-vs-advisory |
| `test_doodle_stamp.py` | 25 | stroke-drawn doodles silently discarding colour |
| `test_invisible_craft.py` | 11 | ink outline/shadow on an ink field |
| `test_collision_nudge.py` | 9 | auto-nudge separation |

**Standing lesson: if a doc cites a test, open it before repeating the claim.** A cited-but-absent
suite is worse than no suite — it buys unearned confidence in the whole gate stack.

## See also
- [[12 Current State]]
- [[Decisions Index]]

[[Home]]
