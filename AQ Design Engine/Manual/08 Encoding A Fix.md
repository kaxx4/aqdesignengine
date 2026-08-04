# 8. Encoding A Fix

When the looking gate (or a recreation) surfaces a flaw that is a GENERAL class — not unique to one
poster — you do NOT just fix the one output. You:

1. **Locate the right layer.**
   - A composition/self-correction rule → `engine/engine.py` (`RULES`, `ARCHETYPE_PROFILES`, or the
     archetype function).
   - A generalized pre-render check usable by any build → `engine/layout.py` (that's where the whole
     §10 catalog lives, because bespoke scripts import it and bypass the DOM audit).
   - A brand token / asset → `engine/core.py`.
2. **Write the check/rule** so it operates on inputs a build already has (an element list, the HTML
   string, a color pair) and returns issues (empty == pass). Skip anything it can't resolve rather
   than guessing (e.g. `invisible_color_check` ignores gradients, never assumes).
3. **Prove it with a self-test** that reproduces the exact historical bug. See
   `scratchpad/test_layout_rules.py` — 21 assertions, each reconstructs a real failure (sample 21's
   invisible badge, 32's undefined var, 26's collision, 44's overflowing star). A rule you can't
   demonstrate catching its bug is not done.
4. **Wire it into the gate** — add it to `preflight` if it's zero-false-positive; auto-run it in
   `build.render()` only if it can NEVER false-positive (an undefined var qualifies; the blank-card
   heuristic does not — that stays a manual diagnostic). A noisy check in the auto-gate trains
   people to ignore warnings; that is worse than no check.
5. **Document it** in `brain/DECISIONS.md` (the why + the sample it came from) and update this file's
   §10 + §12. Then regenerate the affected pieces from the new rule.

This loop is the entire point of the engine: every session should leave the ruleset stronger, so the
eye is needed less next time.

## See also
- [[10 The Bug Catalog]]
- [[Decisions Index]]

[[Manual Index]]
