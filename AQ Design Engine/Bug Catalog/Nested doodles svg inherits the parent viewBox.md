# Nested doodles svg inherits the parent viewBox

**Seen in:** friendship_day carousel (2026-08-02), slide 06 (`art_door`)

**Encoded guard:** none possible — this is a **discipline rule**, not a checkable condition

## The failure

A bespoke illustration drew its own art inside a `viewBox="0 0 400 400"` SVG, then reached for an
existing doodle to finish it:

```python
f'<g transform="translate(292,20) scale(.72)">{dd.heart(fill=PINK)}</g>'
```

The expectation was a 120-unit heart at 0.72× ≈ **86 units**. What rendered was ~**288 units** —
a heart three times too large that bled off its panel *and* off the canvas edge.

## The mechanism

Every builder in `doodles.py` returns a bare `<svg viewBox="0 0 120 120">` with **no width or
height attribute**. An inner `<svg>` without explicit dimensions resolves to **100% of the parent
viewport** — 400 units here, not its own 120. The `scale(.72)` then applied to 400, not to 120.

The `viewBox` controls the inner coordinate system. It does **not** set the rendered size.

## The rule

**Inside a bespoke art SVG, inline the path. Never nest a `doodles.py` builder.**

`doodle()` at the HTML layer — the doodle in its own absolutely-positioned `<div>` with explicit
`width`/`height` — is the only supported way to use the pack, because the div supplies the
dimensions the inner `<svg>` lacks.

```python
# WRONG — inside an art <svg>
f'<g transform="scale(.72)">{dd.heart(fill=PINK)}</g>'

# RIGHT — inline the path, explicit coordinates
f'<g transform="translate(300,26) scale(.62)"><path d="M60 104 C20 76 ..." '
f'fill="{PINK}" stroke="{INK}" stroke-width="9"/></g>'
```

## Why no automated guard

The bug is invisible to static analysis: the markup is valid, the transform is valid, and the
resulting size depends on the *parent's* viewBox at render time. It would only be catchable by a
post-render DOM measurement (`reconcile.probe`) against an expected bbox nobody declares. Cheaper
to never write it. Related discipline entry: [[Stale bbox tuple hides a real off-canvas or collision]].

## See also
- [[10 The Bug Catalog]]
- [[Bug Catalog Index]]
- [[Element clips off-canvas]]
- [[06 The Bespoke Script]]
