# Bundled the encoded rules into one gate + auto-enforcement (goal: raise generation confidence)

Extended the session-8 hardening from individual checks to a UNIFORM gate, because the pass showed
bugs slipped through when each build called only a SUBSET of checks by hand. New in engine/layout.py:
- `dominance_check(elements,W,H,min_hero_frac=0.12)` — static cousin of metrics.VDR. Flags "no
  element reaches hero scale" for layouts that are MEANT to have one dominant element (sample 42's
  mic became a too-small globe). Opt-in (scatter collages legitimately have no hero).
- `antipattern_scan(html,wide_px=480)` — MANUAL diagnostic for the rotate+overflow:hidden+bottom
  blank-card gotcha. Precision-tuned to fire on WIDE bottom-anchored elements only (width is the
  real trigger per the original repro), but still can't be told apart from a normal full-width
  footer without nesting analysis, so it is NOT in the auto gate — call it by hand when chasing a
  blank card.
- `preflight(W,H,elements,html,color_pairs,page_bg,core,expect_hero=...)` — ONE call that runs every
  zero-false-positive static check (bounds + collision + invisible-color + undefined-var, plus opt-in
  hero) and returns {'clean':bool,...}. quadrant fill is reported but ADVISORY (its inverted
  threshold is noisy; the post-render pixel critique judges density better). Recommended standing
  usage: call preflight before render in every new bespoke build.
AUTO-ENFORCEMENT: engine/build.py `render()` now runs `css_var_check` on EVERY render automatically
(zero false positives; an undefined var is always an invisible-element bug). Confirmed it fires on a
bad var even when audit.py reports CLEAN. antipattern is deliberately NOT auto-run (footer false
positives would train people to ignore warnings). All checks covered by scratchpad/test_layout_rules.py
(21 assertions, each reproducing a real historical bug). This is the "convert every visual catch into
an encoded rule" mandate discharged for the whole 44-sample pass: the catchable classes now gate by
rule, shrinking dependence on the looking gate.

## See also
- [[Decisions Index]]
- [[Doodle-badge dropped over text or shape]]
- [[var(--typo) undefined renders transparent]]
- [[Hero scaled far too small vs the reference]]
- [[06 The Bespoke Script]]
- [[03 The Looking Gate]]
- [[07 The Gate Stack]]
