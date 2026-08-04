# AUTO-FILLER built (autofill.py) — automates measure-then-place

- density_map(png): 9x12 grid fill-ratio, returns (grid, fill_score, dead_cells) + ASCII density map for debugging.
- dead_zones_merged(dead): greedy 2D empty-rectangle finder (merges free cells right+down into blocks).
- autofill_piece(build_fn,name): render -> measure -> if score<0.62, place up to 5 varied filler doodles into biggest dead rectangles (measured => collision-free, no audit needed) -> re-render. Returns final score.
- Fillers rotate through accents + doodle types (star/sparkle/burst/heart/plus).
CAVEAT: auto-placed doodles are a SAFETY NET for genuine dead zones, NOT a substitute for good composition. Per calibration rule, prefer scaling existing elements first; use autofill to catch leftover holes. Trigger threshold + filler size/count are tunable.

## See also
- [[Decisions Index]]
- [[Doodle-badge dropped over text or shape]]
