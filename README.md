# AQ Design Engine

A portable, rule-based poster generator for **AQUATERRA** (youth-led NGO + ventures, Kolkata, est. 2021).
Produces on-brand 1080×1350 (and custom-canvas) Instagram posters as **direct outcomes of encoded
rules** — not improvisation — with a mandatory visual-review ("looking gate") loop. Designed to be
dropped into a Claude Code / agentic coding session and run independently of any prior context: the
operating manual, the reasoning behind every rule, and 44+ reference recreations are all in-repo.

## The one principle

Every poster must be a **direct outcome of the engine's rules**. If a piece's quality depends on
hand-editing one output, that is an **engine bug** — fix the rule, then regenerate. The "looking
gate" runs after every render, on the actual rendered PNG; each visual flaw caught by eye gets
converted into an automated check so the engine needs the eye less over time. See
[`CLAUDE.md`](CLAUDE.md) for the full protocol — read it first, it is the entry point.

## Claude Code skill

[`.claude/skills/aq-design-engine/SKILL.md`](.claude/skills/aq-design-engine/SKILL.md) is a
Claude Code skill wrapping this repo — it triggers automatically on AQ/AQUATERRA poster requests
and points into `CLAUDE.md` (the actual source of truth) rather than duplicating it. Drop the
`.claude/` folder into any Claude Code project root, or copy `aq-design-engine/` into
`~/.claude/skills/`, to make it available.

## Quick start

```bash
pip install -r requirements.txt
python -m playwright install chromium

# Workflow A — fresh generation from the archetype registry
python generate.py

# Workflow B — resume the long-running 44-poster recreation run (see CLAUDE.md §5)
python engine/runqueue.py next
```

## Two workflows

| | **A. Fresh generation** | **B. Reference recreation** |
|---|---|---|
| Goal | make a new on-brand AQ poster | reproduce a reference layout element-by-element |
| Entry point | `engine.generate(name, archetype, content, accent_idx)` | a bespoke script built directly on `core`/`build`/`doodles`/`shapes`/`layout` |
| Never routes through | — | `engine.py`'s ARCHETYPES registry |
| Tracked in | `out/<name>.png` | `out/versions/<slug>/vN.png`, logged in `brain/RECREATION_AUDIT.md` |

Both are gated by the looking gate and the static pre-render gate stack, and both feed the same
"encode the fix back into the engine" loop — see `CLAUDE.md` §8.

## Repo layout

- **`CLAUDE.md`** — the full operating manual (also mirrored as `AGENTS.md` for tools that read
  that convention instead). Read this first.
- **`engine/`** — the generation library:
  - `core.py` — brand tokens (colors, fonts, `SIZES`, `LOGO`, real photos), embedded as base64 so
    the engine has zero external asset dependencies at render time.
  - `build.py` — the HTML/CSS frame, element helpers, and the render+audit gate
    (`build.render()` auto-runs `css_var_check` + `same_as_bg_scan` on every render).
  - `doodles.py` — the 20-shape icon vocabulary. Instantiate ONLY via `doodles.stamp(kind, color,
    rot=, style=)` — 5 of the 20 are stroke-drawn and reject a `fill=` kwarg; `stamp()` resolves
    the correct kwarg by introspection instead of guessing.
  - `shapes.py` — parametric die-cut silhouettes (scallop, arch, wave-banner, blob, starburst,
    gear, capsule, shield, tag) + `sticker()`, the uniform die-cut halo/outline/shadow treatment,
    for when the fixed doodle pack doesn't match a reference's silhouette family.
  - `layout.py` — the static pre-render gate stack: `bounds_check`, `collision_check`,
    `invisible_color_check` / `same_as_bg_scan` / `invisible_craft_scan`, `css_var_check`,
    `dominance_check`, `star_text_width`, `collision_nudge`, and `preflight()` (bundles all of the
    zero-false-positive checks into one call + verdict).
  - `compare.py` — structural comparison between a reference JPG and a recreation PNG:
    occupancy, dispersion, detail, palette, and per-region coverage, returned as a directed
    critique (an instruction, not just a number) — see `brain/RECREATION_PROTOCOL.md`.
  - `runqueue.py` — the persistent state machine for the 44-poster recreation run
    (`brain/RECREATION_QUEUE.json`); `next` resumes the in-progress poster, `record` / `fail` log
    an outcome.
  - `engine.py` — Workflow A: the `ARCHETYPES` registry + encoded self-correction loop
    (density escalation, per-archetype fill floors, flat-dominance exemptions).
  - Supporting modules: `audit.py` (DOM margin/overlap gate), `preview.py` (pixel critique —
    dead-quadrant/sparse/crammed/flat), `ref_metrics.py` / `metrics.py`, `reconcile.py`
    (headless DOM measurement), `rhythm.py` (8px grid snap), `tex.py` (halftone/riso, photos
    only), `whitespace.py`, `vision.py` (safe doodle/chip placement on real photos), `archetypes.py`
    (geometry for pending archetypes).
- **`brain/`** — the reasoning behind every rule: `TASTE.md`, `VISUAL_REVIEW.md` (the looking-gate
  protocol), `RECREATION_PROTOCOL.md` (the convergent decision-table loop for Workflow B),
  `DECISIONS.md` (every standing ruling, chronological), `ENGINE_STATE.md`, `VISUAL_DNA.md`,
  `RECREATION_AUDIT.md` / `RECREATION_PROGRESS.md` (per-poster write-ups + status),
  `CAROUSEL_PLAYBOOK.md`, `INSPIRATION.md`, `SESSION_LOG.md`, `dna/` (per-batch teardowns).
- **`AQ Design Engine/`** — an Obsidian vault mirroring `brain/` + `CLAUDE.md` as an atomized,
  cross-linked note network (Bug Catalog, Decisions, Manual, Recreations) — open the folder
  directly as an Obsidian vault to navigate it.
- **`training_samples/reference_posters/`** — the 44 reference posters the engine was trained
  against.
- **`sample_outputs/`** — example fresh-generation output.
- **`scratchpad/`** — bespoke Workflow B build scripts (`gen_*.py`) and the engine self-test
  suites (`test_*.py`); rendered output is intentionally not tracked here (see `.gitignore`).

## Self-tests

Every gate in `layout.py` and `doodles.py` is proven against a reconstruction of the real
historical bug it exists to catch — not just a synthetic case.

```bash
PYTHONIOENCODING=utf-8 python scratchpad/test_layout_rules.py     # 28 assertions
PYTHONIOENCODING=utf-8 python scratchpad/test_collision_nudge.py  #  9 assertions
PYTHONIOENCODING=utf-8 python scratchpad/test_invisible_craft.py  # 11 assertions
PYTHONIOENCODING=utf-8 python scratchpad/test_doodle_stamp.py     # 25 assertions
```

Run these before trusting the gate stack after any change to `engine/layout.py` or
`engine/doodles.py`.

## Brand constants (source of truth: `engine/core.py`)

- **Colors** — cream `#F4EFE0` base (never white), ink `#0A0A0A` (never `#000`, never navy for
  "dark"). 7 accents (`core.ACCENTS`): pink `#FF4D8C` · mint `#1B8A5A` · lemon `#FFC700` ·
  tomato `#FF4D2E` · sky `#3DA9FC` · grape `#7E5BFF` · teal `#0E7C86`. Used as punctuation
  (~30% of a piece), never a flooded field.
- **Fonts** (embedded) — NeutralFace 900 uppercase (display), Eina01 (body), Instrument Serif
  italic (≤1 accent word per piece), JetBrains Mono (labels/eyebrows).
- **Real assets only** — never fabricate stats, screenshots, QR codes, or stock imagery. Real
  AQ photos (`core.PHOTOS`), a flat SVG illustration, or a real CTA substitute for anything a
  reference used a fake asset for.

## License / usage

Internal tool for AQUATERRA. Brand assets (logo, real photos) embedded in `engine/core.py` are
AQUATERRA's own and are not licensed for reuse outside this project.
