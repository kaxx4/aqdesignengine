# Element clips off-canvas

**Seen in:** 6, 9, 10

**Encoded guard:** `layout.bounds_check`

This failure class was caught by eye during the 44-sample Workflow B recreation pass and is now
guarded by an automated rule in `engine/layout.py` (or `engine/preview.py` / `engine/build.py` as
noted), per the "encode the fix" loop in [[08 Encoding A Fix]].

## Samples where this was seen
[[Sample 06]], [[Sample 09]], [[Sample 10]]

## See also
- [[10 The Bug Catalog]]
- [[Bug Catalog Index]]
