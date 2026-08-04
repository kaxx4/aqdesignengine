# Stroke-drawn doodles silently discard the requested colour

**Seen in:** friendship_day carousel (2026-08-03) — and, retroactively, **every bespoke script ever
written**, including the template in [[06 The Bespoke Script]] itself

**Encoded guard:** `doodles.stamp()` — the colour-correct entry point

## The failure

The standard doodle helper — copied verbatim into every bespoke script from the §6 template:

```python
try:    inner = fn(fill=fill, rot=rot)
except TypeError: inner = fn(rot=rot)      # <-- SILENTLY DROPS THE COLOUR
```

Five doodles are **stroke-drawn, not filled**, so their colour kwarg is `stroke`, not `fill`:

| doodle | colour arg | hard-coded default it fell back to |
|---|---|---|
| `ring` | `stroke` | grape `#7E5BFF` |
| `arrow` | `stroke` | tomato `#FF4D2E` |
| `squiggle` | `stroke` | grape `#7E5BFF` |
| `zigzag` | `stroke` | teal `#0E7C86` |
| `spiral` | `stroke` | pink `#FF4D8C` |

For those five, `fill=` raised `TypeError`, the `except` branch ran, and the doodle rendered in its
**hard-coded default colour**. The requested accent was accepted and thrown away with no error.

Caught on a slide where a `PINK` arrow rendered **tomato orange** against a mint/sky palette — the
one warm colour in a piece that was supposed to have exactly one, and it was the wrong warm colour.
Retroactively this means a "pink zigzag" has been coming out teal, and a "mint ring" grape, on
posters going back to the beginning.

## Why it went unnoticed for so long

`spiral`'s default is pink `#FF4D8C` — which is the most-requested accent — so the single most
common stroke doodle usually *looked* correct by coincidence. And nothing errors: the fallback is
a legitimate call that returns valid SVG. Only a palette with a deliberately narrow colour rule
(green/blue lead, exactly one warm highlight — see
[[Green and blue LEAD the palette; pink is the constant highlight]]) made the wrong colour obvious.

## The fix

```python
inner = dd.stamp(kind, colour, rot=rot, style="clean")
```

`stamp()` resolves the correct kwarg by **introspection** (`inspect.signature`) instead of guessing,
using a `COLOR_ARG` map built at import time. A colour is either genuinely applied, or the doodle
truly has none (`globe`, whose colours are intrinsic to the AQ mark). Never silently wrong.

**Rule: never call `doodles.PACK` entries by hand.** `dd.stamp()` is the only supported entry point.
The §6 template and the §9 vocabulary line have both been corrected.

## Self-test

`scratchpad/test_doodle_stamp.py` — 25 assertions. The first four **reproduce the old bug** by
running the historical helper shape and asserting the wrong colour comes out.

## See also
- [[10 The Bug Catalog]]
- [[Bug Catalog Index]]
- [[06 The Bespoke Script]]
- [[Doodles - chips]]
- [[Color]]
