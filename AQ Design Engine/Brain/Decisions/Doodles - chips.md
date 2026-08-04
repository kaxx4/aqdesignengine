# Doodles / chips

- Doodle pack = 20 shapes, clean + rough(hand-drawn) styles, incl. AQ-specific globe/leaf/paw/tree. Auto-generated SVG, any color/rotation/size.
- Use FEWER, intentional (2–3), not sprayed.
- Snarky chips = dry lowercase one-liner asides in accent pills (ink outline, hard shadow, slight tilt). A valid device to fill space + carry voice.


## Always instantiate via `dd.stamp()` (2026-08-03)

Never call `doodles.PACK` entries by hand, and never hand-roll
`try: fn(fill=..) except TypeError: fn(rot=rot)`. Five doodles (`ring`, `arrow`, `squiggle`,
`zigzag`, `spiral`) are stroke-drawn and reject `fill=`, so that pattern silently discarded the
requested colour and rendered their hard-coded default. `dd.stamp(kind, colour, rot=, style=)`
resolves the right kwarg by introspection. Full write-up:
[[Stroke-drawn doodles silently discard the requested colour]].

## See also
- [[Decisions Index]]
- (no direct cross-link identified)
