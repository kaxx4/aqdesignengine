# 12. Current State

- Workflow A: 3 archetypes fully self-correcting (`number_hero`, `radial_orbit`, `giant_type`);
  `stacked_zones` registered. Pending: 5 more (`diagonal_cascade`, `off_frame_bleed`,
  `scatter_collage`, `isometric_grid`, `corner_anchor`) — geometry exists in `engine/archetypes.py`,
  needs wiring into the self-correcting pipeline + looking gate.
- Workflow B: all 44 references processed (`brain/RECREATION_PROGRESS.md` all `revisit-done`).
- Gate stack: the §10 guards are encoded in `layout.py`; `preflight` bundles them; `css_var_check`
  auto-runs in `render`; `render(..., elements=…)` runs the full preflight at render time. Self-tests:
  `scratchpad/test_layout_rules.py` (21 assertions) + `scratchpad/test_collision_nudge.py` (9
  assertions), each reproduces a real historical bug.
- Collision auto-nudge is now encoded (§10) — no pending fix-rules remain from the §10 catalog.
- The looking gate is only as good as the checklist + the eye. It runs EVERY time; that is its value.
  **Keep converting each new visual catch into an encoded rule (§8).**

## See also
- [[Engine State]]
- [[Session Log]]

[[Manual Index]]
