# 4. Workflow A - Fresh Generation

1. **Choose INTENT** — what the piece is for + the ONE feeling it should carry.
2. **Choose an ARCHETYPE** that serves it. Fully self-correcting today: `number_hero`,
   `radial_orbit`, `giant_type`. Also registered: `stacked_zones`. (More are pending — see §12.)
3. **Provide CONTENT** (a dict) + an accent index (0–6, indexes `core.ACCENTS`). This dict is your
   ONLY hand-input. See `generate.py`'s `JOBS` list for real, copyable examples per archetype.
4. **Call** `engine.generate(name, archetype, content, accent_idx)`. The engine then, BY RULE:
   `structure → render (Playwright) → numeric gate (preview.critique) → per-archetype gate
   (ARCHETYPE_PROFILES) → encoded self-correction (density escalation) → writes PNG to out/`.
5. **RUN THE LOOKING GATE** (§3). Always. Nothing ships unseen.
6. If a visual flaw survived the numeric gates, **encode the fix as a rule** (§8) and regenerate —
   do not hand-edit the PNG or the one output.

To run: edit `JOBS` in `generate.py`, then `python generate.py` from the repo root.

### The encoded self-correction loop (do not hand-tune)
- `sparse` / `dead-quadrant` + fill < floor → escalate `density` (bigger hero, accent blocks, band,
  corner filler).
- `crammed` → reduce density.
- `flat_dominant` (>~52% one color) → break up the field — UNLESS the archetype is exempt (e.g.
  `giant_type`'s dark base is an intended signature; see `ARCHETYPE_PROFILES`).
Each archetype has its OWN fill floor + max density in `ARCHETYPE_PROFILES`: geometries breathe
differently (radial is airier than number_hero; giant_type's dark base is dominant on purpose).

### Supporting palette rotates WITH the hero accent
`generate()` picks one hero accent per call (`accent_idx`); every secondary color (chips, ticks,
doodles) is DERIVED from that choice, so different accent indices produce genuinely different color
relationships — not the same palette recolored. (History: this was a real bug, fixed session 6.)

## See also
- [[07 The Gate Stack]]
- [[10 The Bug Catalog]]
- [[Engine State]]

[[Manual Index]]
