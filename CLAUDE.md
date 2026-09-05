# AQ POSTER ENGINE — OPERATING MANUAL (read this first)

You are operating the AQUATERRA (AQ) poster engine. It produces on-brand AQ Instagram posters
(1080×1350) that are DIRECT OUTCOMES OF ENCODED RULES — not improvisation. This manual is
exhaustive on purpose: by the end of it you can (A) generate a fresh poster, and (B) recreate /
"train against" any reference poster the way the whole `training_samples/` set was done — every
poster, multiple iterations, side-by-side visual comparison, and every fix written back into the
engine so it never has to be caught by eye again.

**STANDING RULE — AUTO-RESUME THE RECREATION RUN (user directive, 2026-07-24):** there is a
long-running, multi-session task: recreate all 44 reference posters to ≥80–90% visual match. It is
expected to outlive any single context window and must resume **with no user intervention**.

> **On entering this repo, if the user has not given you a different task, run:**
> ```bash
> python engine/runqueue.py next
> ```
> That prints the exact poster to work on (resuming any interrupted one first). Then follow
> `brain/RECREATION_PROTOCOL.md` — it is a mechanical loop with a decision table, designed to run on
> Sonnet/Haiku without Opus-grade visual judgment. Record every outcome with
> `python engine/runqueue.py record <slug> <score> <iters> "<note>"` so the next window resumes cleanly.
> State lives in `brain/RECREATION_QUEUE.json`. Never restart the run from scratch; never skip a
> poster silently — park blockers with `runqueue.py fail`.

**STANDING RULE — companion art piece (user directive, 2026-07-18):** every time this engine is
used to produce output (Workflow A generation, Workflow B recreation, or any other run of
`engine.generate` / a bespoke script), also invoke the `/canvas-design` skill once alongside it to
produce a companion design-philosophy (.md) + art piece (.pdf/.png). This is independent of the
poster's own gate stack (§7) and looking gate (§3) — it does not replace or block them, it runs in
addition. Do this automatically; do not wait to be asked each time.

---

## 0. TABLE OF CONTENTS
1. THE ONE PRINCIPLE
2. TWO WORKFLOWS (fresh generation vs. reference recreation)
3. THE LOOKING GATE (mandatory in both workflows)
4. WORKFLOW A — generate a fresh poster
5. WORKFLOW B — recreate / "train against" a reference poster
6. THE BESPOKE SCRIPT (annotated template you copy for Workflow B)
7. THE GATE STACK (what every checker catches, and when to run it)
8. ENCODING A FIX BACK INTO THE ENGINE (the heart of "training")
9. BRAND CONSTANTS & VOCABULARY (colors, fonts, doodles, photos, sizes)
10. THE BUG CATALOG (every recurring failure → its encoded guard)
11. REPO MAP & BRAIN DOCS
12. CURRENT STATE / WHAT'S PENDING

---

## 1. THE ONE PRINCIPLE (non-negotiable)
Every design must be produced by the engine's encoded rules. **If a poster's quality depends on
you hand-editing an individual output, that is an ENGINE BUG.** Fix the RULE, then regenerate —
never patch one file and move on. Taste = a committed cascade of intentional decisions that cohere
+ subtraction. NOT accumulation, NOT randomness across absorbed references. (Full reasoning:
`brain/TASTE.md`.)

Corollary that governs everything below: **every visual flaw you catch by eye is a rule you haven't
written yet.** The looking gate (§3) exists to find flaws; §8 exists to convert each one into an
automated check so the next generation can't reproduce it. Over time, dependence on the eye shrinks.

---

## 2. TWO WORKFLOWS
There are exactly two ways to make a poster, and they use different code paths. Do not mix them.

| | **A. Fresh generation** | **B. Reference recreation ("training")** |
|---|---|---|
| Goal | make a NEW AQ poster for real content | reproduce a specific reference layout, learn from the gap |
| Code path | `engine.generate(...)` (the ARCHETYPES registry in `engine/engine.py`) | a **bespoke script** built directly from `core`+`build`+`doodles`+`layout` primitives — **never** `engine.py`'s ARCHETYPES |
| Input | intent + archetype + content dict + accent index | a full written composition description of the reference |
| Output | `out/<name>.png` | `out/versions/<slug>/vN.png` (versioned, iterated) |
| Ends when | looking gate passes | render matches the reference element-by-element; outcome logged |

Both workflows are gated by §3 (looking) and §7 (the automated checks). Both feed §8 (encode fixes).

---

## 3. THE LOOKING GATE (mandatory — this is where quality is actually enforced)
Numeric/metric checks are PROXIES. They pass pieces that are visually broken (text off its shape,
dead corners, flat fields, invisible elements). **The only reliable check is LOOKING at the
rendered PNG.** Full protocol: `brain/VISUAL_REVIEW.md`.

**Critical sequencing:** the looking gate runs AFTER the PNG is rendered, on the image you can
actually see — never on a disk path you assume is correct. In Claude Code: after every render,
`Read` the PNG (it displays visually) and review it. Wire this into the loop so it happens EVERY
iteration, automatically.

**Review against every principle**, and for each failure write "[element] — what's wrong — the fix":
- **Legibility** — every word readable; nothing clipped by a shape edge or another element.
- **Hierarchy** — one clear hero; the eye knows where to land first.
- **Balance** — no dead quadrant; weight distributed, not dumped in one corner.
- **Rhythm / flow** — spacing between bands/clusters is intentional, not an accidental gap.
- **Contrast / color** — dark type on light field; accents punctuate (~30%), never flood.
- **Craft / depth** — outlines, offset shadows, one hero-shine; not flat matte everywhere.
- **Density** — board-level busy but audited clean; no collisions.

**When you can't see (view tool down / headless):** use `engine/reconcile.py` (measures element
extents in the rendered DOM — catches overflow, off-canvas, margin breach, text-wider-than-
container) and `engine/preview.py` (catches sparse, crammed, dead-quadrant, flat, flat_dominant,
uniform from the pixels). **NEVER fabricate a visual review.** If you can't see it and can't measure
it, say so.

---

## 4. WORKFLOW A — GENERATE A FRESH POSTER
1. **Choose INTENT** — what the piece is for + the ONE feeling it should carry.
2. **Choose an ARCHETYPE** that serves it. Fully self-correcting today: `number_hero`,
   `radial_orbit`, `giant_type`. Also registered: `stacked_zones`. (More are pending — see §12.)
3. **Provide CONTENT** (a dict) + an accent index (0–6, indexes `core.ACCENTS`). This dict is your
   ONLY hand-input. See `generate.py`'s `JOBS` list for real, copyable examples per archetype.
4. **Call** `engine.generate(name, archetype, content, accent_idx)`. The engine then, BY RULE:
   `structure → render (Playwright) → numeric gate (preview.critique) → per-archetype gate
   (ARCHETYPE_PROFILES) → encoded self-correction (density escalation) → writes PNG to out/`.
5. **RUN THE LOOKING GATE** (§3). Always. Nothing ships unseen.
6. If a visual flaw survived the numeric gates, **encode the fix as a rule** (§8) and regenerate —
   do not hand-edit the PNG or the one output.

To run: edit `JOBS` in `generate.py`, then `python generate.py` from the repo root.

### The encoded self-correction loop (do not hand-tune)
- `sparse` / `dead-quadrant` + fill < floor → escalate `density` (bigger hero, accent blocks, band,
  corner filler).
- `crammed` → reduce density.
- `flat_dominant` (>~52% one color) → break up the field — UNLESS the archetype is exempt (e.g.
  `giant_type`'s dark base is an intended signature; see `ARCHETYPE_PROFILES`).
Each archetype has its OWN fill floor + max density in `ARCHETYPE_PROFILES`: geometries breathe
differently (radial is airier than number_hero; giant_type's dark base is dominant on purpose).

### Supporting palette rotates WITH the hero accent
`generate()` picks one hero accent per call (`accent_idx`); every secondary color (chips, ticks,
doodles) is DERIVED from that choice, so different accent indices produce genuinely different color
relationships — not the same palette recolored. (History: this was a real bug, fixed session 6.)

---

## 5. WORKFLOW B — RECREATE / "TRAIN AGAINST" A REFERENCE POSTER
This is the exact protocol used to process all 44 references in `training_samples/reference_posters/`,
tracked in `brain/RECREATION_PROGRESS.md` (a 44-row status table) and `brain/RECREATION_AUDIT.md`
(the full write-ups). Work **one reference per session/turn** — do not batch.

**The 6 steps, in order, no skipping:**

1. **Full composition description BEFORE any code.** `Read` the reference `.jpg` and write a
   complete description into `brain/RECREATION_AUDIT.md` under a `## Sample N` heading. Enumerate
   EVERY background texture/shape, every layer in z-order, every distinct element with approximate
   size / color / rotation / position. **Do not summarize multiple elements as one** ("a few
   stickers" hides misses). This written list is your acceptance checklist for step 4.

2. **Build the bespoke script** in the scratchpad, using `engine/core.py` + `build.py` +
   `doodles.py` + `layout.py` primitives DIRECTLY. **Never route through `engine.py`'s ARCHETYPES**
   — Workflow B is a deliberately wider decision space than the ~4 archetype buckets. Use the
   template in §6.

3. **Render** as `vN.png` in that reference's `out/versions/<slug>/` folder, incrementing the
   version number (v1 → v2 → v3…). The slug is the first ~14 chars of the reference's filename hash.

4. **Look, side-by-side.** `Read` the reference AND your render. Walk your step-1 checklist item by
   item: is each listed element present, and proportioned correctly? **A missing listed element is
   a FAIL requiring another iteration — not an acceptable variation.** Distinguish honestly:
   - *Acceptable adaptation* — swapping the reference's literal brand copy for AQ program names;
     using a flat SVG illustration or a real AQ photo where the reference used stock/fake imagery
     (the real-assets-only rule, §9); substituting an engine doodle for an icon the engine lacks.
   - *Real miss* — a whole element/motif absent; a collision; an invisible element; wrong
     proportion of the hero; a dead half the reference fills. These fail.

5. **Iterate (v+1)** fixing each gap found, then re-render and re-check. Repeat until it genuinely
   matches. (Most took 1–3 iterations; the worst needed a full rebuild.)

6. **Log the outcome** in `brain/RECREATION_AUDIT.md` (iteration count + exactly what was fixed),
   and flip that row in `brain/RECREATION_PROGRESS.md` to `revisit-done` with a one-line note.

**The meta-step that makes this "training," not just copying:** whenever a fix in step 5 is a
GENERAL class of bug (not specific to this one poster), stop and encode it as a rule per §8 before
moving on. That is how the bug catalog in §10 was built — each entry is a flaw caught by eye once,
then permanently guarded so it's caught by rule forever after.

**Multi-slide references** (moodboards, pitch decks, website screenshots): pick ONE slide/mechanism
and recreate it as a single 1080×1350 poster. Established precedent; don't try to cram a whole deck.

**Real-photo carousels** (event recaps, camp trips, field visits — built from actual AQ photos, not
illustrated archetypes): read `brain/CAROUSEL_PLAYBOOK.md` FIRST. It has the reusable helper block
(logo treatment, tinted scrims, accent-rotating dots, the systematic doodle-variety engine, the
truthful index tag) and the per-slide face/margin/collision checklist distilled from the Sunderbans
8.0 batch session — copy it rather than re-deriving any of it, especially when producing many of
these in one batch.

---

## 6. THE BESPOKE SCRIPT (annotated template for Workflow B)
Copy this into the scratchpad as `gen_<slug8>_vN.py`. It is the exact shape used for all 44
recreations, updated to call the standing gate (§7).

```python
import asyncio, os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")
W, H = core.SIZES["feed"]; M = 48          # feed canvas is 1080x1350 — NEVER assume taller
A = core.ACCENTS                            # A[0..6]: pink,mint,lemon,tomato,sky,grape,teal
elements = []                               # keep a bbox (x,y,w,h) per placed element, IN SYNC

# doodle() helper — ALWAYS via dd.stamp(). Do NOT hand-roll `try: fn(fill=..) except TypeError`:
# 5 doodles (ring, arrow, squiggle, zigzag, spiral) are STROKE-drawn and reject `fill=`, so that
# pattern silently discarded the colour and rendered their hard-coded default (a pink arrow came
# out tomato). stamp() resolves the right kwarg by introspection. See §10.
def doodle(kind, x, y, size, fill, rot=0, z=7, style="clean"):
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;width:{size}px;height:{size}px;'
            f'z-index:{z}">{dd.stamp(kind, fill, rot=rot, style=style)}</div>')

# --- build each element as an absolutely-positioned div/svg, and APPEND ITS TRUE BBOX ---
# CRITICAL: when you move an element's CSS x/y, update its elements.append((x,y,w,h)) too.
# A stale bbox makes bounds_check/collision_check silently miss real bugs (sample 6).
hero = doodle("globe", 270, 540, 520, A[4])           # heroes fill a real fraction of the frame
elements.append((270, 540, 520, 520))
# ... every other element, each with a matching elements.append(...) ...

footer = f'<span style="position:absolute;bottom:52px;left:{M}px;font-family:var(--m);font-weight:700;font-size:13px;color:var(--ink);z-index:20">@ngo.aquaterra</span>'
elements.append((M, H-70, 300, 20))

# --- assemble, GATE, render ---
inner = "".join([f'<div style="position:absolute;inset:0;background:var(--bg)"></div>', hero, footer])
html = B.page(W, H, "var(--bg)", inner, grain=False)   # grain=True adds photo-grain overlay

# color_pairs: (label, fill) or (label, fill, surface) for every shape whose fill could vanish
color_pairs = [("hero_bg", A[4], "var(--bg)")]

# ONE gate call before render. clean==False means a real bug — fix before rendering.
pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs,
                   page_bg="var(--bg)", core=core, expect_hero=True)

async def main():
    slug = "8988345ad4963e"                              # first ~14 chars of the reference hash
    os.makedirs(f"out/versions/{slug}", exist_ok=True)
    await B.render(html, f"out/versions/{slug}/v2.png", W, H)  # css_var_check auto-runs here
    print("done")
asyncio.run(main())
```
Run with `PYTHONIOENCODING=utf-8 python gen_<slug8>_vN.py` (the utf-8 flag matters for the ✓/⚠
glyphs on Windows). Then **Read the rendered PNG and run the looking gate (§3).**

---

## 7. THE GATE STACK (what each checker catches, and when)
Three tiers. Run the cheap static ones BEFORE render, the pixel/DOM ones AFTER.

### 7a. Static, pre-render — `engine/layout.py` (the tuple-list world the bespoke scripts live in)
`audit.py`'s DOM gate only sees elements tagged `.measure`; bespoke scripts hand-maintain
`(x,y,w,h)` tuple lists, so these run on THAT list:
- `bounds_check(W,H,elements)` → elements clipping off-canvas (feed is 1080×1350, not taller).
- `collision_check(elements, min_overlap=12, ignore_pairs=…)` → any two elements really overlapping
  (doodle over text, badge over shape). Accepts `(x,y,w,h)` or `(label,x,y,w,h)`; echoes labels.
- `invisible_color_check(pairs, page_bg, core)` → any fill/stroke whose resolved color ≈ the
  surface behind it (the "drawn but invisible" bug). Resolves `var(--token)`; skips gradients/named.
- `css_var_check(html, core)` → `var(--typo)` referenced but never defined (renders transparent).
- `dominance_check(elements, W, H, min_hero_frac=0.12)` → **opt-in**; flags "no element reaches hero
  scale" for layouts that should have one dominant element.
- `star_text_width(diameter)` → helper: the width to constrain text to so it fits a star's waist.
- `antipattern_scan(html)` → **manual only** (not in the auto gate — false-positives on normal
  footers). Call by hand when chasing a blank card (the rotate+overflow:hidden+bottom gotcha).
- **`preflight(W,H,elements,html,color_pairs,page_bg,core,expect_hero=…)`** → runs all the
  zero-false-positive checks above at once, returns `{'clean': bool, ...}`, prints one verdict.
  `under_filled_quadrants` is included but ADVISORY (its threshold is noisy — trust the pixel
  critique for density). **This is the standing pre-render call.**
- Also: `quadrant_fill_check` (advisory density) and `cluster_positions` (overlapping-pile
  placement) and `pick_fill_mode` (solid-dominant fill picker) — legacy helpers, still valid.

**Auto-enforcement:** `build.render()` ALWAYS runs `css_var_check` (undefined var is unambiguously a
bug). If you pass `render(html, out, W, H, elements=…, color_pairs=…, page_bg=…, expect_hero=…)`, it
also runs the full `preflight` at render time for free.

### 7b. DOM structural — `engine/audit.py` & `engine/reconcile.py`
- `audit.audit(html, name)` (runs inside `build.render`) → margin breaches + real overlaps between
  `.measure`-tagged DOM elements, with whitelisted by-design overlaps (tags-on-hero, sign piles…).
- `reconcile.probe(...)` → measures rendered DOM extents when you cannot see the image: overflow,
  off-canvas, text-wider-than-container.

### 7c. Pixel / metric — `engine/preview.py` & `engine/ref_metrics.py`
- `preview.critique(png)` / `preview.report(png, name)` → `dead_quadrant`, `sparse`, `crammed`,
  `flat`, `flat_dominant`, `uniform`; returns fill, contrast, per-quadrant fill. The headless
  proxy for the looking gate — run it every render, but it is NOT a substitute for actually looking.
- `ref_metrics.analyze(png)` → `dom_cov`, `mean_sat`, `contrast`, `ink`, `vdr` (visual dominance
  ratio). **Reference targets:** contrast ≈ .26, ink ≈ .11, sat ≈ .31, dom_cov ≈ .46, VDR 0.06–0.20
  (one clear hero; <0.05 = no hero, >0.22 = headline swallows the piece). Treat these like the
  collision auditor — a piece should land within ~0.1 per axis before you call it done.
  (Caveat: flat-vector recreations read low on `vdr` vs. gradient/photo references — a known metric
  limitation, not a visual bug.)

---

## 8. ENCODING A FIX BACK INTO THE ENGINE (the heart of "training")
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

---

## 9. BRAND CONSTANTS & VOCABULARY (`engine/core.py` is the source of truth)
**Colors** — bg cream `#F4EFE0` (NEVER white) · ink `#0A0A0A`. Accents (`core.ACCENTS`, index them
by `A[i]`), used as PUNCTUATION only (~30% of the piece, never a flooded field):
`A[0]` pink `#FF4D8C` · `A[1]` mint `#1B8A5A` · `A[2]` lemon `#FFC700` · `A[3]` tomato `#FF4D2E` ·
`A[4]` sky `#3DA9FC` · `A[5]` grape `#7E5BFF` · `A[6]` teal `#0E7C86`. (Also `--mintbright #00E5A0`.)

**Fonts** (embedded, referenced as CSS vars): `--d` NeutralFace 900 UPPERCASE (display/headlines) ·
`--e` Eina lowercase (body) · `--s` Instrument Serif italic (≤1 accent word per piece) · `--m`
JetBrains Mono (labels/eyebrows/footer). Headlines UPPERCASE, body lowercase, numbers can be heroes.

**Doodles** (`engine/doodles.py`, call via the `doodle()` helper): `star sparkle circle ring
thumbsup heart arrow squiggle zigzag burst plus lightning spiral dots speech cross globe leaf paw
tree`. Call ONLY via `dd.stamp(kind, color, rot=, style=)` — 5 are stroke-drawn and reject `fill=`; `globe` has no colour arg at all. Vary SIZES
(mix 60px and 160px, not all ~90px) and place only in measured free zones.

**Real photos** (`core.PHOTOS`, base64-embedded — the ONLY real imagery): `food` (food
distribution), `edu` (education Sundarban), `diwali` (fundraising), `xmas` (Christmas Khidirpur).

**Canvas sizes** (`core.SIZES`): `feed` (1080,1350) — the default · `story` (1080,1920) · `square`
(1080,1080).

**Logo** — `core.LOGO`, the real colored wordmark, top-left every slide (a pill on dark/photo
backgrounds; NEVER white-inverted).

**Real-assets-only rule (hard):** never fabricate stats, UI screenshots, QR codes, or stock/photo
imagery. If a reference used a fake asset, substitute a real AQ photo, a flat SVG illustration, or a
real CTA — and note the swap as an acceptable adaptation.

**Craft layer (always on):** thick ink outlines · hard-offset ink shadows · one hero-shine per piece
· halftone ONLY on photos (flat on solid colors) · 8px grid snap · snarky voice chips in dead zones ·
fill space by SCALING existing elements UP before adding filler doodles (filler is the last resort).

---

## 10. THE BUG CATALOG (every recurring failure → its encoded guard)
Each row is a flaw caught by eye during the 44-sample pass, now guarded by rule. Full stories in
`brain/DECISIONS.md`.

| Failure class | Seen in (samples) | Encoded guard |
|---|---|---|
| Element clips off-canvas | 6, 9, 10 | `layout.bounds_check` |
| Doodle/badge dropped over text or shape | 26, 27, 32 | `layout.collision_check` |
| Shape fill == page bg → invisible | 21 | `layout.invisible_color_check` |
| Text stroke ≈ bg → invisible outline | 24 | `layout.invisible_color_check` |
| `var(--typo)` → element renders transparent | 32 | `layout.css_var_check` (auto in `render`) |
| Text overflows a star/burst's narrow waist | 19, 44 | `layout.star_text_width` |
| Hero scaled far too small vs. reference | 42 | `layout.dominance_check` (opt-in) |
| Wide `bottom:`-anchored child in rotated overflow parent renders BLANK | 7 | `layout.antipattern_scan` (manual) + rule: anchor wide content with `top:` |
| Stale bbox tuple hides a real off-canvas/collision | 6 | discipline: update `elements.append` whenever you move CSS |
| Dead half the reference fills | 15, 25, 30, 31, 39 | `preview.critique` dead_quadrant/sparse + "scale up before filler" |
| One flat color floods the field | (batch) | `preview.critique` flat_dominant (>52%) |
| Cramming a pile into one corner starves other quadrants | 87525f70 | `layout.quadrant_fill_check` (overlap LOCAL, fill GLOBAL) |
| Fill == page bg → element invisible, and the opt-in check never ran | showcase5b | **`layout.same_as_bg_scan` (AUTO in `build.render` when `page_bg` passed)** |
| Recreation strays while metrics say "converged" (global scalars are structure-blind) | c42f94a09f | `engine/compare.py` — occupancy/dispersion/detail/palette/region + directed critique |
| Detailed reference sticker → flat geometric blob (silhouette collapse) | c42f94a09f | `engine/shapes.py` parametric silhouettes + uniform `sticker()` treatment |
| Stacked plates spaced by a guessed constant clip their own text | showcase5b | rule: space stacks by ELEMENT HEIGHT + a real gap, never a constant |
| A module in `engine/` shadowing a stdlib name breaks every bespoke script | `queue.py` | rule: never name an `engine/` module after a stdlib module (sys.path is prepended) |
| Composition systematically under-filled vs the corpus | 15-poster batch | `compare.py` area ratio + `brain/VISUAL_DNA.md` §5a (per-base-field density targets) |
| Ink outline + hard shadow on an INK field → whole craft layer invisible | friendship_day | **`layout.invisible_craft_scan` (advisory, in `preflight`)** + rule: outline colour is a per-slide token (`outline_of(dark)`), never a constant |
| `doodles.py` builder nested inside a bespoke art `<svg>` → inherits the PARENT viewBox, renders ~3x oversized and off-canvas | friendship_day | rule: inline the path inside art SVGs; only ever call `doodle()` at the HTML layer in its own div |
| Faint (.13–.26 opacity) rings/hatch/checker "fields" read as dirt and smear through body copy | friendship_day | rule: decoration is SOLID + ink-outlined + hard-shadowed, never a low-opacity wash |
| `try: fn(fill=..) except TypeError` **silently discards the colour** for the 5 stroke-drawn doodles (ring/arrow/squiggle/zigzag/spiral) → they render their hard-coded default | friendship_day | **`doodles.stamp()`** resolves the colour kwarg by introspection; §6 template updated. Self-test: `scratchpad/test_doodle_stamp.py` |
| `vision.plan_spots` returns `[]` on a dense photo → slide renders with **NO craft layer at all**, and every gate still prints CLEAN because nothing exists to fail | 2026 workshop batch | **`vision.plan_spots_relaxed()`** — escalating busy_pctl ladder + explicit `starved` warning. Self-test: `scratchpad/test_vision_starve.py` |
| Full-width top exclude band severs every free region from the top edge `background_grid` requires → photo starved to `free_fraction` 0.004 | 2026 workshop batch | rule: shape excludes like the UI (logo box, dots box), never as a full-width stripe. Covered by the same self-test |
| `pick_visible([accent, white, ink])` ranks by luminance delta → picks near-black ink on every bright wall; thin dark stroke on texture reads as **dirt** | 2026 workshop batch | rule: test the accent ALONE against local luminance, fall back only on failure; + `drop-shadow` on every photo doodle (`CAROUSEL_PLAYBOOK` 10-11) |
| Dark smooth **hair** scores as low-busy background → doodle lands on a child's head, gate says CLEAN | 2026 workshop batch | rule: per-photo `extra_exclude` box on tight portraits, **measured off a render, never estimated** (`CAROUSEL_PLAYBOOK` 12) |
| `giant_type`'s `leftmass` (its only TL-quadrant shape) never scaled with `density` while `rightmass`/`lowmass` did, AND its profile capped `max_density` at 1 — one escalation step, applied to shapes that couldn't use it, left cream-field pieces stuck NEEDS-LOOK (`sparse`+TL/TR<0.17) with no headroom | teachers_day | `leftmass` now scales with density; `max_density` 1→2; new `midmass` density≥2 tier fills the collision-safe window beside the title box. Self-test: `scratchpad/test_giant_type_density_escalation.py` |

Collision AUTO-nudge is encoded: `layout.collision_nudge` repositions the later-placed element of a
colliding pair away from the earlier (anchor) one, opt-in via `preflight(..., auto_nudge=True)`.
Self-test: `scratchpad/test_collision_nudge.py`. (Session 9; see `brain/DECISIONS.md`.)

---

## 11. REPO MAP & BRAIN DOCS
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
  `RECREATION_PROGRESS.md` (44-row status table), `AUDIT.md`, `CAROUSEL_PLAYBOOK.md` (real-photo
  carousel helper block + per-slide collision/margin checklist, for batch runs of many carousels),
  **`VISUAL_DNA.md`** (what all 44 references taught — the measured design vocabulary + the honest
  corpus-coverage audit; read before adding any archetype or gate), **`GENERATION_MAP.md`** (the
  architecture + dependency-ordered build plan for autonomous one-shot generation), `dna/batch_01..06.md`
  (per-poster teardowns behind VISUAL_DNA).
- `training_samples/reference_posters/` — the 44 references. `out/versions/<slug>/` — recreation
  iterations. `out/` — fresh generations. `sample_outputs/` — example engine outputs.

---

## 12. CURRENT STATE / WHAT'S PENDING (honest — full detail in `brain/ENGINE_STATE.md`)
- Workflow A: 3 archetypes fully self-correcting (`number_hero`, `radial_orbit`, `giant_type`);
  `stacked_zones` registered. Pending: 5 more (`diagonal_cascade`, `off_frame_bleed`,
  `scatter_collage`, `isometric_grid`, `corner_anchor`) — geometry exists in `engine/archetypes.py`,
  needs wiring into the self-correcting pipeline + looking gate.
- Workflow B: all 44 references processed (`brain/RECREATION_PROGRESS.md` all `revisit-done`).
- Gate stack: the §10 guards are encoded in `layout.py`; `preflight` bundles them; `css_var_check`
  auto-runs in `render`; `render(..., elements=…)` runs the full preflight at render time.
  **Self-tests (all passing, verified 2026-08-03) — each assertion reproduces a real historical bug:**
  `test_layout_rules.py` (28) · `test_collision_nudge.py` (9) · `test_invisible_craft.py` (11) ·
  `test_doodle_stamp.py` (25) · `test_vision_starve.py` (13, added 2026-08-07) ·
  `test_giant_type_density_escalation.py` (9, added 2026-09-05), all in `scratchpad/`. Run them
  before trusting the gate stack.
  (`test_layout_rules.py` had been cited here as 21 assertions while missing from disk entirely;
  rebuilt 2026-08-03 — if a doc cites a test, open it before repeating the claim.)
- Collision auto-nudge is now encoded (§10) — no pending fix-rules remain from the §10 catalog.
- The looking gate is only as good as the checklist + the eye. It runs EVERY time; that is its value.
  **Keep converting each new visual catch into an encoded rule (§8).**
- **CORPUS COVERAGE (measured 2026-07-24, `brain/VISUAL_DNA.md`): the 4 built archetypes can reach
  only ~6 of the 44 references fully, ~8 partially — ~30 are unreachable.** This, not content input,
  is the real reason generation needs per-piece steering. Three gates (`bounds_check`,
  `collision_check`, `dominance_check`) actively REJECT legitimate reference designs and need
  per-archetype intent profiles before any new archetype is added. Build order in
  `brain/GENERATION_MAP.md` — gates → primitives → archetypes → ledger → director → copywriter.
- `engine/vision.py` (NEW) makes photo pieces one-shot: it measures a photo and returns safe doodle/
  chip placements automatically, so "find the empty zone" and "don't land on a face" are now RULES,
  not eye-judgment. Use `vision.plan_spots()` in place of hand-picked coordinates in any real-photo
  build; `CAROUSEL_PLAYBOOK.md`'s manual spot-picking step is superseded by it.
