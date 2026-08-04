# Wide bottom-anchored child in rotated overflow parent renders blank

**Seen in:** 7

**Encoded guard:** `layout.antipattern_scan` (manual) + rule: anchor wide content with `top:`

This failure class was caught by eye during the 44-sample Workflow B recreation pass and is now
guarded by an automated rule in `engine/layout.py` (or `engine/preview.py` / `engine/build.py` as
noted), per the "encode the fix" loop in [[08 Encoding A Fix]].

## Samples where this was seen
[[Sample 07]]

## See also
- [[10 The Bug Catalog]]
- [[Bug Catalog Index]]
