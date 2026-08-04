# VISUAL REVIEW — the LOOKING gate (mandatory engine stage, not optional, not numeric)

## WHY THIS EXISTS
Numerics are PROXIES. fill%, contrast-std, quadrant-balance approximate principles but cannot SEE:
- text spilling off its container / illegible on wrong background
- a headline that's technically big but visually swallowed
- rhythm that reads as monotonous despite "passing" spacing math
- a focal point the eye doesn't actually land on first
- color that clashes or an accent that disappears
- crowding that math reads as "balanced fill"
Every principle the engine is trained on FAILS silently if no one LOOKS. So looking is a required stage.

## CRITICAL: WHERE THE LOOKING GATE RUNS
The view tool on a raw disk path may NOT render. The looking gate runs AFTER present_files, on the
images made visible IN THE CHAT. Correct flow:
  generate → numeric gates → self-correct → PRESENT_FILES → LOOK at the presented in-chat images
  → review every principle → if FAIL: encode the fix as a RULE in engine.py → regenerate → present → look again.
Never review a disk path before presenting. Never ship before looking at the presented image.

## THE PROTOCOL
STEP 1 — RENDER, then VIEW the actual PNG with the view tool. Non-negotiable. Never ship unseen.
STEP 2 — SCORE against EVERY principle below, precisely, from what I SEE (not what I intended):
STEP 3 — CONSOLIDATE into a verdict: PASS or specific FIX-LIST with element + problem + fix.
STEP 4 — If any principle fails, FIX and re-render, then LOOK AGAIN. Loop until visual PASS.
STEP 5 — Only a visually-reviewed PASS may be shown to the user.

## THE PRINCIPLE CHECKLIST (judge each from the image, precisely)
LEGIBILITY
  □ Every text element fully inside its container? (no spill onto background)
  □ Every text on a background it contrasts with? (no white-on-cream, dark-on-dark)
  □ All text readable at thumbnail size? (IG feed = small)
  □ No text clipped, cut off, or overlapping into illegibility?
HIERARCHY
  □ Does the eye land on the intended focal FIRST? (not just "biggest by math")
  □ Clear 1st / 2nd / 3rd read order? Or does everything compete?
  □ Is the hero actually dominant visually, or swallowed by busy neighbors?
BALANCE & COMPOSITION
  □ Weight distributed, or lopsided/tipping to one side/corner?
  □ Any dead quadrant the eye skips?
  □ Any crowded pocket where elements collide visually (even if not pixel-overlapping)?
RHYTHM & FLOW
  □ Does spacing feel intentional (varied, syncopated) or monotonous (bingo-card)?
  □ Does the eye MOVE through the piece, or stall?
  □ Scale variation present, or everything mid-sized and even?
CONTRAST & COLOR
  □ Enough dark/bold to anchor? Or washed-out and flat?
  □ Accents punctuating, or flooding / disappearing?
  □ Any color clash or muddy combination?
  □ Does it read as ON-BRAND AQ (flat bold + ink outlines + cream), not generic?
CRAFT & DEPTH
  □ Shadows/outlines consistent (shared light logic)?
  □ Overlaps intentional and clean, or accidental collisions?
  □ Halftone only on photos, flat on solids?
  □ Does it look DESIGNED (committed) or ASSEMBLED (accumulated)?
DENSITY
  □ Frame filled but breathing? Or sparse-and-lazy / crammed-and-noisy?
  □ Negative space active (framing/ghost) or dead holes?

## OUTPUT FORMAT (what LOOKING produces — consolidated, precise, per-element)
For each fail: "[element] — [what I SEE wrong] — [specific fix]"
e.g. "BOOKS sign — white text spills onto cream bg, half-invisible — size box to text, keep word inside"
e.g. "overall — all signs same size, reads as bingo-card — make one sign 2x others, overlap two"
Then: overall verdict + the ONE biggest visual problem to fix first.

## RULE
This LOOKING gate outranks the numeric preview and the collision audit. A piece can pass both and still
FAIL looking — and looking wins. Numerics pre-filter; the eye decides. Nothing ships unseen.

## See also
- [[03 The Looking Gate]]

[[Home]]
