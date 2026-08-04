---
name: aq-design-engine
description: Generate or recreate AQUATERRA (AQ) branded Instagram posters using the rule-based AQ Design Engine. Use this skill whenever the user asks to make an AQ / AQUATERRA poster, carousel, or social graphic, or to "train" the engine against a reference design, or mentions the AQ Poster Engine / AQ Design Engine repo. Produces on-brand output as a direct outcome of encoded rules, never freehand — and every visual flaw caught gets written back into the engine as a permanent rule.
license: Internal AQUATERRA tool. Brand assets embedded in the engine (logo, real photos) are AQUATERRA's own and are not licensed for reuse outside AQUATERRA work.
---

# AQ Design Engine

You are operating a **rule-based** poster generator, not a freehand design tool. The engine's own
operating manual — `CLAUDE.md` at the repo root — is the actual source of truth and is exhaustive
on purpose. **This skill file is a map into that manual, not a replacement for it.** Always read
`CLAUDE.md` in full at the start of a session before generating or recreating anything; it changes
as rules get encoded, so a cached memory of it will drift stale.

Repo: https://github.com/kaxx4/aqdesignengine — clone or locate the local checkout first if it
isn't already the working directory. Nothing in this engine works without the actual `engine/`
Python modules and the embedded brand assets in `engine/core.py`.

## The one non-negotiable principle

**Every poster must be a direct outcome of the engine's rules.** If a piece's quality depends on
hand-editing one output, that is an ENGINE BUG — fix the rule, then regenerate. Never patch a
single PNG and move on. See `CLAUDE.md` §1.

## Orientation — read these, in this order, before doing anything

1. `CLAUDE.md` — the full manual. Sections 1–3 (principle, workflows, looking gate) are mandatory
   context for every task; sections 4–12 are reference, read the ones relevant to the task at hand.
2. `brain/DECISIONS.md` — every standing ruling, chronological. Skim the tail for the most recent.
3. `brain/RECREATION_QUEUE.json` (via `python engine/runqueue.py next`) — if there's a long-running
   recreation task in progress and the user hasn't given a different task, this is what to resume.
4. The Obsidian vault at `AQ Design Engine/` mirrors `brain/` as cross-linked notes — useful for
   tracing *why* a rule exists (Bug Catalog, Decisions) when `CLAUDE.md`'s summary isn't enough.

## Two workflows — do not mix them

**A. Fresh generation** — a new poster for real content. Code path: `engine.generate(name,
archetype, content, accent_idx)` from `engine/engine.py`'s `ARCHETYPES` registry. Edit `JOBS` in
`generate.py`, run `python generate.py`. Full protocol: `CLAUDE.md` §4.

**B. Reference recreation ("training")** — reproduce a specific reference poster element-by-
element. A **bespoke script** built directly from `engine/core.py` + `build.py` + `doodles.py` +
`shapes.py` + `layout.py` primitives — **never** through `engine.py`'s ARCHETYPES. Full protocol:
`CLAUDE.md` §5–6 and `brain/RECREATION_PROTOCOL.md` (the mechanical decision-table loop — use this
one, it replaces "iterate until it looks right" with measurement + a fixed table, and is designed
to converge without Opus-grade visual judgment).

If the user's ask doesn't specify, ask which workflow they mean before writing code — the two
produce different artifacts in different places and are not interchangeable.

## The looking gate is mandatory, every time, both workflows

Numeric/metric checks are proxies; they pass pieces that are visually broken. **The only reliable
check is looking at the actual rendered PNG.** After every render: use the Read tool on the PNG (it
displays visually) and review against every principle in `CLAUDE.md` §3 (legibility, hierarchy,
balance, rhythm, contrast, craft, density). Never fabricate a visual review — if you genuinely
cannot see the image, say so and fall back to `engine/reconcile.py` + `engine/preview.py`.

## When you catch a visual flaw

Do not hand-edit the PNG. Do not patch just that one poster. Follow `CLAUDE.md` §8:

1. Locate the right layer — composition rule → `engine/engine.py`; generalized pre-render check →
   `engine/layout.py`; brand token/asset → `engine/core.py`.
2. Write the check/rule so it operates on inputs a build already has, returns issues (empty =
   pass), and skips what it can't resolve rather than guessing.
3. Prove it with a self-test that reconstructs the exact historical bug — see
   `scratchpad/test_layout_rules.py` for the pattern (28 assertions, each one a real prior
   failure). **A rule you can't demonstrate catching its bug is not done.**
4. Wire it into `layout.preflight()` only if it is zero-false-positive; otherwise it stays a manual
   diagnostic (see `invisible_craft_scan`'s advisory status for why a noisy hard-fail is worse than
   no check).
5. Document it — a row in `CLAUDE.md` §10's bug catalog, an entry in `brain/DECISIONS.md`, and (if
   the repo's Obsidian vault is present) a linked note under `AQ Design Engine/Bug Catalog/`.

This loop is the entire point of the engine. Skipping step 5 means the next session re-discovers
the same bug from zero.

## Hard rules worth repeating (full detail in CLAUDE.md, these are the ones people forget)

- **Doodles:** instantiate ONLY via `doodles.stamp(kind, color, rot=, style=)`. Never hand-roll
  `try: fn(fill=...) except TypeError: fn(rot=...)` — 5 of the 20 doodles are stroke-drawn and
  reject `fill=`, so that pattern silently discards the requested colour and renders the doodle's
  hard-coded default instead. No error is raised. This shipped unnoticed in every bespoke script
  for a long time; `stamp()` exists specifically to make it impossible again.
- **Outline/shadow colour is a per-field token, not a constant.** "Ink outline" means ink on a
  *light* field. On a dark field the outline must flip to cream, or the entire craft layer
  (thick ink outlines, hard-offset shadows) renders invisible while every gate reports clean.
- **Never nest a `doodles.py` builder inside a bespoke art `<svg>`.** An inner `<svg>` without
  explicit width/height inherits the *parent's* viewBox, not its own — a doodle nested this way
  renders 2–3× oversized and bleeds off-canvas. Inline the path instead; only call `doodle()`/
  `stamp()` at the HTML layer, in its own div.
- **Decoration is solid, ink-outlined, and hard-shadowed — never a low-opacity wash.** Faint
  rings/hatch/checker fields at ~15–25% opacity read as dirt or a dirty scan, not design, even
  though they raise density metrics.
- **Real assets only.** Never fabricate stats, screenshots, QR codes, or stock imagery. Swap for a
  real AQ photo (`core.PHOTOS`), a flat SVG illustration, or a real CTA, and note it as an
  acceptable adaptation, not a miss.
- **Multi-slide references** (moodboards, decks, screenshots) — pick ONE mechanism and recreate it
  as a single poster; do not try to cram the whole board in. Note also: `engine/compare.py` scores
  against the *whole* reference image regardless, so a moodboard reference will show a structurally
  high score even when the single-mechanism choice is correct per `CLAUDE.md` §5 — this is a known
  metric limitation, not necessarily a real gap. Say so explicitly if it applies, don't chase the
  number past the point it stops meaning anything.
- **Preserve every bespoke Workflow-B script.** Copy it into `out/versions/<slug>/` alongside the
  PNG, not just `scratchpad/` — scratchpad scripts have been lost between sessions before, forcing
  a blind rebuild from the PNG alone.

## Self-tests — run before trusting the gate stack

```bash
PYTHONIOENCODING=utf-8 python scratchpad/test_layout_rules.py     # bounds/collision/invisible-color/etc.
PYTHONIOENCODING=utf-8 python scratchpad/test_collision_nudge.py  # auto-nudge separation
PYTHONIOENCODING=utf-8 python scratchpad/test_invisible_craft.py  # outline/shadow-on-matching-field
PYTHONIOENCODING=utf-8 python scratchpad/test_doodle_stamp.py     # doodle colour kwarg resolution
```

Run these after any change to `engine/layout.py` or `engine/doodles.py`, and add a new assertion
whenever step 5 above adds a rule.

## Brand constants (full detail: `engine/core.py`, `CLAUDE.md` §9)

Cream `#F4EFE0` base (never white) · ink `#0A0A0A` (never `#000`, never navy for "dark") · 7
accents used as punctuation (~30% of a piece, never flooded): pink `#FF4D8C` · mint `#1B8A5A` ·
lemon `#FFC700` · tomato `#FF4D2E` · sky `#3DA9FC` · grape `#7E5BFF` · teal `#0E7C86`. Fonts:
NeutralFace 900 uppercase (display), Eina01 (body, lowercase), Instrument Serif italic (≤1 accent
word per piece), JetBrains Mono (labels/eyebrows/footer). Canvas: `core.SIZES` has `feed`
(1080×1350, default), `story` (1080×1920), `square` (1080×1080) — custom canvases are also valid
(a carousel used 1080×1440), just pass explicit dimensions rather than assuming feed.

## Companion art piece (standing rule, if the user's setup includes it)

If a `/canvas-design`-style skill is available in this session, invoke it once alongside any
poster output (fresh generation or recreation) to produce a companion design-philosophy note +
art piece. This runs in addition to, never instead of, the gate stack and looking gate above.
