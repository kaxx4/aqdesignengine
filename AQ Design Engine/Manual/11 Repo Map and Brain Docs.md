# 11. Repo Map and Brain Docs

- `CLAUDE.md` — this manual (read on entry).
- `generate.py` — Workflow A entrypoint: edit `JOBS`, run `python generate.py`.
- `engine/` — the generation library:
  - `core.py` (brand tokens, fonts, photos, `SIZES`, `LOGO`, `GRAIN`) · `build.py` (`page`,
    `render`, element helpers, the render+audit gate) · `doodles.py` (icon vocabulary) ·
    `layout.py` (generalized pre-render checks + `preflight` — §7a) · `audit.py` (DOM margin/overlap
    gate) · `preview.py` (pixel critique) · `ref_metrics.py` / `metrics.py` (metric targets) ·
    `reconcile.py` (headless DOM measurement) · `rhythm.py` (8px snap) · `tex.py` (textures) ·
    `whitespace.py` · `engine.py` (Workflow A: ARCHETYPES + self-correction) · `archetypes.py`
    (geometry for pending archetypes).
- `brain/` — the full reasoning: `TASTE.md`, `VISUAL_REVIEW.md` (looking-gate protocol), `ENGINE.md`,
  `ENGINE_STATE.md`, `DECISIONS.md` (standing rulings + every encoded fix), `INSPIRATION.md`
  (reference teardowns), `RECREATION_AUDIT.md` (per-sample composition descriptions + outcomes),
  `RECREATION_PROGRESS.md` (44-row status table), `AUDIT.md`.
- `training_samples/reference_posters/` — the 44 references. `out/versions/<slug>/` — recreation
  iterations. `out/` — fresh generations. `sample_outputs/` — example engine outputs.

## See also
- [[Manual Index]]
- [[Decisions Index]]
- [[Recreations Index]]
- [[Bug Catalog Index]]

[[Manual Index]]
