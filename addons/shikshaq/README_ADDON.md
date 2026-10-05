# Shikshaq addon (vendored)

A second brand on the AQ engine's rails: Shikshaq's design language, a weekly three-post planner, copy and layout gates. Node, self-contained, no dependency on the Python engine.

Source of truth is `Shikshaq/marketing` (kept local, never pushed to the Shikshaq repo by owner instruction). This copy is for AQ-side reference and reuse. If both change, diff before trusting either.

Run: `cd addons/shikshaq && npm install && node run-week.mjs --dry`.
The token self-test compares against Shikshaq's `src/index.css`; point `SHIKSHAQ_REPO` at a checkout to run it, otherwise that part is skipped.

Ideas worth lifting into AQ proper: the per-element WCAG measurement and text-on-text collision gate in `src/render.mjs`, the fact-traceability copy gate in `src/validate.mjs`, and the ledger-based rotation in `src/brain.mjs`.
