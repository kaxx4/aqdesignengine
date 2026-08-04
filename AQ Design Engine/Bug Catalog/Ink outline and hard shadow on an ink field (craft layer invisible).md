# Ink outline and hard shadow on an ink field (craft layer invisible)

**Seen in:** friendship_day carousel (2026-08-02), slides 01 + 08

**Encoded guard:** `layout.invisible_craft_scan` — ADVISORY, wired into `layout.preflight`

## The failure

On the two ink-based slides, every element carried `border:7px solid var(--ink)` plus
`box-shadow:12px 12px 0 var(--ink)` against an ink page. The entire AQ craft layer — "thick ink
outlines · hard-offset ink shadows" from [[09 Brand Constants]] — deleted itself.

The slides still rendered. They passed `css_var_check`, passed `same_as_bg_scan`, and `preflight`
reported **CLEAN ✓**. They simply looked flat and cheap next to the cream slides. Caught by the
[[03 The Looking Gate|looking gate]] only.

## Why every existing guard missed it

[[Shape fill equals page bg (invisible)]] is guarded by `same_as_bg_scan`, which inspects
`background:` declarations. The craft layer does not live in `background:` — it lives in `border:`
and `box-shadow:`, and **nothing checked those properties at all**. This is the same failure shape
as the showcase5b invisible bubble: an entire property family sitting outside every gate's field
of view.

## The fix (the rule, not the patch)

**Outline colour is a per-slide token, not a constant.** Cream outline on an ink field, ink
outline on a cream field. In the carousel this became a single helper threaded through every
furniture function (punch box, chip, sticker, dots):

```python
def outline_of(dark):
    return CREAM if dark else INK
```

See [[Outline colour is a per-slide token, not a constant]].

## Why the guard is ADVISORY and never a hard fail

An element's true backing surface is **not knowable from the HTML alone**. A cream-bordered chip
sitting on an accent panel over a cream page resolves as "border == page bg" and would
false-positive. Per [[08 Encoding A Fix]] step 4, a noisy check in the hard-fail set trains people
to ignore warnings, which is worse than no check. So it reports and never flips `clean`.

## Self-test

`scratchpad/test_invisible_craft.py` — 11 assertions, including an explicit assertion that the
check does **not** flip `preflight`'s `clean` flag.

## See also
- [[10 The Bug Catalog]]
- [[Bug Catalog Index]]
- [[Shape fill equals page bg (invisible)]]
- [[Text stroke approx equals bg (invisible outline)]]
- [[Outline colour is a per-slide token, not a constant]]
