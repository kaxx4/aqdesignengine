# Doodle-badge dropped over text or shape

**Seen in:** 26, 27, 32

**Encoded guard:** `layout.collision_check`

This failure class was caught by eye during the 44-sample Workflow B recreation pass and is now
guarded by an automated rule in `engine/layout.py` (or `engine/preview.py` / `engine/build.py` as
noted), per the "encode the fix" loop in [[08 Encoding A Fix]].

## Samples where this was seen
[[Sample 26]], [[Sample 27]], [[Sample 32]]

## See also
- [[10 The Bug Catalog]]
- [[Bug Catalog Index]]


## Update — collision auto-nudge (session 9)
Collision AUTO-nudge is now encoded: `layout.collision_nudge` repositions the later-placed
element of a colliding pair away from the earlier (anchor) one, opt-in via
`preflight(..., auto_nudge=True)`. Self-test: `scratchpad/test_collision_nudge.py`. See
[[Collision auto-nudge (session 9)]] in the Decisions log for the full story.
