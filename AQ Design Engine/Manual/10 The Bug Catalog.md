# 10. The Bug Catalog

Each row is a flaw caught by eye during the 44-sample pass, now guarded by rule. Full stories in
`brain/DECISIONS.md`.

| Failure class | Seen in (samples) | Encoded guard |
|---|---|---|
| Element clips off-canvas | 6, 9, 10 | `layout.bounds_check` |
| Doodle/badge dropped over text or shape | 26, 27, 32 | `layout.collision_check` |
| Shape fill == page bg → invisible | 21 | `layout.invisible_color_check` |
| Text stroke ≈ bg → invisible outline | 24 | `layout.invisible_color_check` |
| `var(--typo)` → element renders transparent | 32 | `layout.css_var_check` (auto in `render`) |
| Text overflows a star/burst's narrow waist | 19, 44 | `layout.star_text_width` |
| Hero scaled far too small vs. reference | 42 | `layout.dominance_check` (opt-in) |
| Wide `bottom:`-anchored child in rotated overflow parent renders BLANK | 7 | `layout.antipattern_scan` (manual) + rule: anchor wide content with `top:` |
| Stale bbox tuple hides a real off-canvas/collision | 6 | discipline: update `elements.append` whenever you move CSS |
| Dead half the reference fills | 15, 25, 30, 31, 39 | `preview.critique` dead_quadrant/sparse + "scale up before filler" |
| One flat color floods the field | (batch) | `preview.critique` flat_dominant (>52%) |
| Cramming a pile into one corner starves other quadrants | 87525f70 | `layout.quadrant_fill_check` (overlap LOCAL, fill GLOBAL) |

Collision AUTO-nudge is encoded: `layout.collision_nudge` repositions the later-placed element of a
colliding pair away from the earlier (anchor) one, opt-in via `preflight(..., auto_nudge=True)`.
Self-test: `scratchpad/test_collision_nudge.py`. (Session 9; see `brain/DECISIONS.md`.)

## See also
- [[Bug Catalog Index]]
- [[Decisions Index]]

[[Manual Index]]
