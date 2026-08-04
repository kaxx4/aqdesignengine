# Dead half the reference fills

**Seen in:** 15, 25, 30, 31, 39

**Encoded guard:** `preview.critique` dead_quadrant/sparse + "scale up before filler"

This failure class was caught by eye during the 44-sample Workflow B recreation pass and is now
guarded by an automated rule in `engine/layout.py` (or `engine/preview.py` / `engine/build.py` as
noted), per the "encode the fix" loop in [[08 Encoding A Fix]].

## Samples where this was seen
[[Sample 15]], [[Sample 25]], [[Sample 30]], [[Sample 31]], [[Sample 39]]

## See also
- [[10 The Bug Catalog]]
- [[Bug Catalog Index]]
