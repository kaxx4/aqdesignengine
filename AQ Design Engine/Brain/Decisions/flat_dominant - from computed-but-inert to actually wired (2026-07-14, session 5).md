# flat_dominant: from computed-but-inert to actually wired (2026-07-14, session 5)

Cross-sample finding: a 44-sample batch (out/versions/) showed dom_cov running +0.13 to +0.24 over
target across ALL FOUR archetypes — every composition reads more uniform/flat than its reference.
Three attempts, in order, with honest measurement at each step (never claimed success without
re-measuring the full batch):
1. Tightened preview.py's flat_dominant threshold .60→.52. Regenerated all 44: **zero effect**,
   byte-identical output. Root cause: `flat_dominant` was never included in `arch_ok` (engine.py's
   pass/fail gate) — only fill/contrast/quads were — so it never influenced generation, only reporting.
2. Added `flat_dominant` to the density-escalation trigger (alongside sparse/dead_quadrant). Regenerated
   all 44: **still zero effect**. Root cause: `arch_ok` was already True at iteration 0 for most pieces
   (fill/contrast/quads alone were satisfied), so `generate()` broke out of the loop before ever
   reaching the escalation branch — flat_dominant flagged, but nothing was listening.
3. Added flat_dominant as an actual condition of `arch_ok` itself (a piece with an over-dominant field
   is no longer "ok" regardless of fill/contrast/quads) — this is what finally gives it teeth: pieces
   now can't exit early with a flat field, so they proceed to real density escalation.
   Regenerated all 44: mean error 0.85→0.838. 8/44 improved, 2/44 worsened (now flagged NEEDS-LOOK
   where they weren't before — density escalation ran out at max_density without fully fixing it,
   which is honest and correct: it should surface as needing a look, not silently ship), 34/44
   unchanged (already had healthy dom_cov, gate correctly left them alone).
LESSON: a numeric check that's computed but not wired into the actual pass/fail decision is decoration,
not a rule — verify by re-measuring after EVERY change, because "I added a check" and "the check does
something" are different claims. Two of three attempts here were confirmed inert before the real fix.

## See also
- [[Decisions Index]]
- [[One flat color floods the field]]
