# Outline colour is a per-slide token, not a constant

**Session:** friendship_day carousel, 2026-08-02

## The ruling

The AQ craft layer specifies "thick **ink** outlines · hard-offset **ink** shadows"
([[09 Brand Constants]]). Read literally — ink, always — that rule **destroys itself on a dark
field**, because ink on ink is nothing.

The constant was never the *colour*. The constant is the **contrast**. Restated:

> Outline colour is a per-slide token derived from the field: **cream outline on an ink field,
> ink outline on a cream field.** The weight, the offset, and the hardness never change.

## Implementation shape

One helper, threaded through every piece of furniture that carries craft — punch box, chip,
sticker, position dots, panel:

```python
def outline_of(dark):
    return CREAM if dark else INK
```

Every call site takes `dark` and asks for its outline rather than hard-coding `var(--ink)`. This
is cheap to apply and impossible to forget once the furniture functions require the argument.

## Why this matters beyond one carousel

Any piece mixing light and dark fields hits this — and mixed-field sets are becoming normal
(dark bookends around cream content is now a standing carousel rhythm). Hard-coding ink was safe
only while every poster was cream.

## The guard

`layout.invisible_craft_scan`, advisory, inside `layout.preflight`. Deliberately not a hard fail:
an element's real backing surface is unknowable from HTML, so a cream-bordered chip on an accent
panel would false-positive, and per [[08 Encoding A Fix]] step 4 a noisy hard-fail is worse than no
check. Self-test: `scratchpad/test_invisible_craft.py`, 11 assertions.

Full failure write-up: [[Ink outline and hard shadow on an ink field (craft layer invisible)]].

## See also
- [[Decisions Index]]
- [[Color]]
- [[Logo]]
- [[07 The Gate Stack]]
