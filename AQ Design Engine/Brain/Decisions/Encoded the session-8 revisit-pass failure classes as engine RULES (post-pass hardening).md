# Encoded the session-8 revisit-pass failure classes as engine RULES (post-pass hardening)

After the full 44-sample revisit pass, the same handful of bug classes had recurred as one-off
scratchpad fixes. Per THE ONE PRINCIPLE (fix the RULE, not one output), these are now encoded as
generalized checks in engine/layout.py — the module the bespoke scripts already import. They live
here (not audit.py) because the bespoke one-off scripts BYPASS audit.py's DOM gate: audit.py only
sees `.measure` DOM elements, while the bespoke scripts hand-maintain (x,y,w,h) tuple lists. The
guards therefore have to operate in that tuple/HTML-string world.

- `collision_check(elements, min_overlap=12, ignore_pairs=...)` — pairwise bbox overlap on the
  manual element list (tuple-world twin of audit.py's OVERLAP check). Catches the collision class
  that hit samples 26 (thumbsup over the "volunteer" pill), 27 (badge 7 inside the paw), 32
  (sparkle over a speech bubble). bounds_check missed all three because nothing left the canvas.
  Accepts (x,y,w,h) or (label,x,y,w,h); echoes labels back so you know WHICH two collide.
- `invisible_color_check(pairs, page_bg, core, thresh=40)` — flags any fill/stroke whose resolved
  color is within RGB-distance `thresh` of the surface behind it. Catches the "shape is drawn but
  invisible" class: sample 21 (oval badge bg == page bg) and sample 24 (near-black stroke on a
  black page). Resolves var(--token) against core.ROOT; skips unresolvable colors (named/gradient/
  rgba) rather than guessing.
- `css_var_check(html, core)` — returns CSS custom-property names referenced via var() but never
  defined (inline or in core.ROOT). Catches sample 32's `var(--_c)` typo that made every
  speech-bubble tail render transparent/invisible.
- `star_text_width(diameter, waist_frac=0.42)` — a star/burst badge's usable text band is its
  narrow horizontal waist, not its bounding box; text sized to the box overflows the points and is
  clipped by the clip-path (samples 19 and 44). Constrain the inner text element to this width.

All four are covered by a passing self-test (scratchpad/test_layout_rules.py) where each assertion
reproduces the exact historical bug it guards against. Recommended usage in any new bespoke build:
call collision_check + bounds_check + quadrant_fill_check together right before render, and run
invisible_color_check on every (fill,surface) pair + css_var_check on the final HTML string.

## See also
- [[Decisions Index]]
- [[Doodle-badge dropped over text or shape]]
- [[var(--typo) undefined renders transparent]]
- [[Shape fill equals page bg (invisible)]]
- [[Text overflows a star or burst's narrow waist]]
- [[Element clips off-canvas]]
- [[Cramming a pile into one corner starves other quadrants]]
- [[06 The Bespoke Script]]
