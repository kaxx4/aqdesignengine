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
