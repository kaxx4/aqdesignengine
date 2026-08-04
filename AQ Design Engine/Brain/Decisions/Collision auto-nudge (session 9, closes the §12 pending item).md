# Collision auto-nudge (session 9, closes the §12 pending item)

- `layout.collision_check` detected collisions (samples 26/27/32) but reposition stayed manual —
  the last item in the §10 bug catalog marked "detection done, reposition still manual."
- Added `layout.collision_nudge(elements, W, H, ...)`: for each colliding pair it pushes the
  LATER-placed element directly away from the earlier one (center-to-center vector, step-wise),
  re-checking after every step, capped at `max_iters`. Earlier elements (hero, background bands —
  placed first in a bespoke script's append order) act as anchors and never move; later badges/
  doodles/chips move. Degenerate identical-center case nudges along a fixed diagonal instead of
  dividing by zero. Never pushes a repositioned element off-canvas (stays within `margin`..`W/H -
  margin`) — bounds_check still owns off-canvas detection, this only owns un-colliding.
- Wired into `preflight(..., auto_nudge=True)` (opt-in, default False so existing bespoke scripts
  are unaffected): if collisions are found, elements are nudged before the rest of the gate runs,
  and the repositioned list comes back as `r['nudged_elements']` for the caller to adopt. Any pair
  it can't separate within the canvas still fails `clean` via `r['collisions']` — auto-nudge fixes
  cramped placement, it does not silently paper over a genuinely too-small canvas.
- Self-test: `scratchpad/test_collision_nudge.py` (9 assertions) — reproduces the sample-26
  thumbsup-over-pill collision, confirms it resolves, confirms the anchor element doesn't move,
  confirms on-canvas containment, confirms the identical-center edge case terminates, and confirms
  the `preflight(auto_nudge=True)` wiring end-to-end. All passing.

## See also
- [[Decisions Index]]
- [[Doodle-badge dropped over text or shape]]
- [[Element clips off-canvas]]
- [[06 The Bespoke Script]]
- [[07 The Gate Stack]]
