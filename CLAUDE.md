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

> **SCOPE (clarified 2026-09-20).** This rule binds the SESSION, not every delegated sub-task. If
> you are a subagent working a narrow brief with a fixed output list, build what you were asked for
> and say in your report that the companion piece is outstanding — do not widen your own scope to
> produce one. The session that dispatched you owns it. (A Sonnet agent hit this exact conflict and
> correctly flagged it instead of guessing; that is the right move, and now it has an answer.)

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

**C. FRESH POSTER, BESPOKE BUILD (the common case, added session 10e).** Workflow A is
limited to the four registered archetypes, which `brain/VISUAL_DNA.md` measured as
reaching only ~6 of the 44 original references. Most real briefs therefore want B's
*construction method* (bespoke script from the primitives) for A's *purpose* (new
content, no reference to match). That is a third path and it now has an entry point:

```bash
python design.py "126 return visits to one partner in Kolkata"   # draws a style
python design.py "sign-ups open" --dept events --canvas story
python design.py --list                                          # what the bank knows
```

`design.py` draws a STYLE from `brain/STYLE_BANK.json` — all 74 references, each with
MEASURED fields (coverage, ground, palette, bbox, taken from the pixels) and JUDGED
fields (mechanism, hero, and a `recipe` written as build instructions). The draw is
educated-random: filtered by what you know, weighted so a judged style with a written
recipe beats an unjudged one, and it never returns empty — it relaxes filters one at a
time and reports which. It prints a BRIEF; it does not render. You still build it as a
bespoke script and the looking gate (§3) still runs on the PNG.

Workflow C's checklist is Workflow B's minus the reference-matching steps: measure the
chosen style's reference (`compare.geometry`), build to its proportions, render, LOOK.

### WHEN THE STYLE AND THE BRAND DISAGREE — the precedence ladder
A drawn style is a *reference someone judged*, not a specification, and it will
sometimes ask for something §9 forbids. Both of these came up on the first real
Workflow C builds and both were resolved correctly from first principles — which
means every builder was re-deriving them. They are rules now:

1. **A HARD BRAND RULE BEATS THE RECIPE, always.** `core.accent_for(dept)` is semantic,
   contrast is measured, Instrument Serif is ≤1 accent word, the ground is cream not
   white, real assets only. A recipe saying "set the whole headline in serif caps"
   loses to §9; take the *mechanism* (serif carries the voice) and express it the
   brand's way (one italic accent word).
2. **A recipe's COUNT is a target, not a ceiling.** "Restraint: exactly four colours"
   means *this piece is disciplined about colour*, and a fifth that arrives because
   the department hue is fixed by rule has not broken the restraint. Keep the spirit
   — no free-for-all — and say in the script's docstring which number you exceeded
   and why.
3. **The mechanism is the part you must not drop.** Everything else is negotiable.
   If honouring a brand rule would destroy the mechanism, you have drawn the wrong
   style for this brief: re-draw with a different seed rather than build a piece whose
   whole reason for existing has been adapted away.
4. **Record every adaptation** in the bespoke script's docstring, the same way
   Workflow B's step 4 distinguishes an acceptable adaptation from a real miss. §5's
   list applies here too: swapping literal brand copy for AQ program names, using a
   real AQ photo or flat SVG where the reference used stock, substituting an engine
   doodle for an icon the engine lacks — all acceptable. A missing mechanism, a
   collision, an invisible element, a dead half — still failures.

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

0. **MEASURE THE REFERENCE FIRST.** `compare.geometry(ref_path)` → content bbox, margins,
   vertical ratio, centroid, occupancy grid. Paste the numbers into the description and
   BUILD TO THEM.
   **IF THE REFERENCE IS A MOCKUP** (phones/devices/print/a scene), crop the chosen screen
   FIRST: `compare.crop(ref, x0,y0,x1,y1, out)` → then measure and score against the CROP.
   Scoring a full-bleed poster against a photo of four phones on grey measures the grey.
   Expect the crop to carry some bezel; a few "MISSING COLOUR near-black" critiques are
   that bezel, not a missing element. The written inventory catches missing ELEMENTS; it is unreliable for
   PROPORTIONS, and a wrong proportion there propagates straight into the build.

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
# Repo root from THIS FILE's location — never an absolute path. A hardcoded root
# has broken something three times now (the self-tests twice, and this template).
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")
# shapes/tex are NOT optional extras — they are where badges, silhouettes and every
# texture live (§9). The template used to load only the four above, so an agent that
# needed a starburst and a checkerboard found them by running `wc -l engine/*.py`.
shapes = load("shapes"); tex = load("tex")     # sticker/fit_font/ink_mark · the 15 textures
vis = load("vision")                           # ONLY for real-photo pieces (plan_spots)
W, H = core.SIZES["feed"]; M = 64          # feed canvas is 1080x1350 — NEVER assume taller
                                           # M=64 matches build.py's own margin constant and
                                           # ~10 of the 14 recent bespoke scripts. The template
                                           # said 48 and nothing else did.
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

# ---- DECLARE WHAT THE GATE CANNOT INFER ------------------------------------------
# Each of these is OPT-IN and simply never fires unless you pass it. They are not
# extras: every one exists because a poster shipped broken without it. Declare the
# ones your piece actually has and delete the rest.

# SHAPES whose fill could vanish into what is behind them:  (label, fill[, surface])
color_pairs = [("hero_bg", A[4], "var(--bg)")]

# TYPE, against the surface it sits ON:  (label, text, surface[, size_px[, bold]])
# Different question from color_pairs — that asks "is it the same colour", this asks
# "can it be read". White on a pale card is a big distance AND 1.44:1. HARD FAIL.
text_pairs = [("headline", core.INK, "var(--bg)", 96, True),
              ("label",    core.on_cream(A[4], 16), "var(--bg)", 16, True)]

# CONTAINERS — a card/slab/panel that HOLDS things. Anything wholly inside one is
# contained, not colliding. Beats hand-listing an ignore pair per child. The label
# must be one you actually put in `elements`, or the check says so and holds nothing.
# ⚠ FILL THIS IN the moment your piece has a panel, card or slab with things ON it.
#   Leaving it empty makes every child of that panel report as a collision with it —
#   five false collisions on the first build that had a full-bleed panel, and the
#   author went reading layout.py to find out why.
containers = ()          # e.g. ("panel", "card") — each must also be in `elements`

# TAGS THAT BLEED OFF THE CANVAS ON PURPOSE. Full-bleed is a real AQ move and
# bounds_check is a HARD FAIL, so without this a design whose MECHANISM is the bleed
# can never report clean and you learn to read past a failing verdict.
bleed_tags = ()          # e.g. ("pill",) for a field that runs off both edges

# ONE SENTENCE split across several boxes, in the order it is meant to be READ.
# This example is the CORRECT placement — a clean diagonal stagger:
reading_order = [("chip1", 48, 672, 520, 80), ("chip2", 300, 772, 520, 80),
                 ("chip3", 552, 872, 520, 80)]
# The same three at x=48 / x=560 / x=48 would HARD FAIL as a column trap: chips 1
# and 3 share a left edge, so the eye reads them as a column and the sentence scans
# "chip1 -> chip3 -> chip2". That shipped once (out/session10f/c1_v3.png) and two
# rounds of iteration did not catch it, because nothing about it is measurable in a
# pixel histogram.

# ONE gate call before render. clean==False means a real bug — fix before rendering.
# (You can skip this entirely and let render() do it — see the render call below.)
pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs,
                   text_pairs=text_pairs, containers=containers,
                   reading_order=reading_order, bleed_tags=bleed_tags,
                   page_bg="var(--bg)", core=core, expect_hero=True)

async def main():
    slug = "8988345ad4963e"                              # first ~14 chars of the reference hash
    os.makedirs(f"out/versions/{slug}", exist_ok=True)
    # ALWAYS pass elements= (and the rest). Without it you get css_var_check and
    # nothing else: reconcile_boxes never runs, so an element you built but forgot to
    # elements.append() is invisible to EVERY check. That exact omission put a lemon
    # star on top of the words "SIGN-UPS OPEN NOW" while preflight printed CLEAN
    # (out/session10f/c2_v3.png). The template used to show the short call.
    #
    # render() forwards EVERY preflight option, so this one call is the whole gate:
    # the static checks, the DOM measurement (clipped / oversize / off-canvas /
    # buried), and the declared-vs-drawn reconciliation. Calling preflight by hand
    # and then rendering without elements= is the failure mode this replaced.
    await B.render(html, f"out/versions/{slug}/v2.png", W, H,
                   elements=elements, color_pairs=color_pairs,
                   text_pairs=text_pairs, containers=containers,
                   reading_order=reading_order, bleed_tags=bleed_tags,
                   page_bg="var(--bg)", expect_hero=True)
    print("done")
asyncio.run(main())
```
**Rendering more than one piece? Hold ONE browser open.** `render()` used to cost 16.8s a poster
(two chromium cold starts + 2.7s of blind sleeps); it is now 1.9s inside a session:
```python
async with B.session():
    for html, out in jobs:
        await B.render(html, out, W, H, elements=els)   # elements= also runs the bbox reconciliation
```
**And MEASURE text before you size anything around it** — `B.measure_text([...])` returns the layout
box (`h`, flow the next element off this), the content box (`ink_h`), and the TRUE painted glyph box
(`glyph_w`/`glyph_h`, size collision bboxes off this). Every layout bug in session 10 was a guessed
text dimension.

Run with `PYTHONIOENCODING=utf-8 python gen_<slug8>_vN.py` (the utf-8 flag matters for the ✓/⚠
glyphs on Windows). Then **Read the rendered PNG and run the looking gate (§3).**

---

## 7. THE GATE STACK (what each checker catches, and when)
Three tiers. Run the cheap static ones BEFORE render, the pixel/DOM ones AFTER.

### 7a. Static, pre-render — `engine/layout.py` (the tuple-list world the bespoke scripts live in)
`audit.py`'s DOM gate only sees elements tagged `.measure`; bespoke scripts hand-maintain
`(x,y,w,h)` tuple lists, so these run on THAT list:
- `bounds_check(W,H,elements)` → elements clipping off-canvas (feed is 1080×1350, not taller).
- `collision_check(elements, min_overlap=12, ignore_pairs=…)` — `ignore_pairs` takes PAIRS
  in any shape (`('a','b')`, `{'a','b'}`, `frozenset({'a','b'})`); anything that is not a pair is
  now reported rather than silently ignored → any two elements really overlapping
  (doodle over text, badge over shape). Accepts `(x,y,w,h)` or `(label,x,y,w,h)`; echoes labels.
- `text_contrast_check(text_pairs, page_bg, core)` → TYPE that does not clear its WCAG
  floor against the surface behind it. The legibility half `invisible_color_check` never
  covered: same inputs, different question — distance says "is it there", contrast says
  "can it be read". White on a light lavender card is a large DISTANCE and **1.44:1**.
  Honours the large-text split (>=24px bold -> 3.0). HARD FAIL via `preflight(text_pairs=…)`.
- `collision_check(..., containers=("card","slab"))` → declare the furniture ONCE instead of
  hand-listing an ignore pair per child. Explicit on purpose: a doodle dropped entirely
  inside a headline's bbox is containment too, and that is the bug the check exists for.
- `img_src_check(html)` → an `<img>` with an empty or missing src. Auto in `preflight` with `html=`.
- `double_rotation_scan(html)` → **advisory**; an element rotated by BOTH its wrapper and itself
  draws at the SUM. `doodles.stamp(rot=)` and `shapes.sticker(rot=)` bake the angle in, so a
  rotated wrapper doubles it. Counter-rotation is legal and reports a sum near zero — that is the
  tell. Auto in `preflight` with `html=`.
- **`bleed_tags=("pill",)`** → tags that leave the canvas ON PURPOSE. `bounds_check` is a hard
  fail, so without this a design whose MECHANISM is the bleed can never report clean. Accepted by
  `preflight` and `render`, and passed on to `measure_dom`'s own off-canvas exemption.
- `reading_order_check(parts)` → one SENTENCE split across placed boxes must scan in its own
  order. Catches an INVERSION and the COLUMN TRAP (parts 1 and 3 left-aligned with 2 between
  them, so they read as a column). HARD FAIL via `preflight(reading_order=[…])`.
- `invisible_color_check(pairs, page_bg, core)` → any fill/stroke whose resolved color ≈ the
  surface behind it (the "drawn but invisible" bug). Resolves `var(--token)`; skips gradients/named.
- `css_var_check(html, core)` → `var(--typo)` referenced but never defined (renders transparent).
- `dominance_check(elements, W, H, min_hero_frac=0.12)` → **opt-in**; flags "no element reaches hero
  scale" for layouts that should have one dominant element.
- `contains_check(pairs)` → content that does not fit the shape it belongs to (label vs. its pill,
  headline vs. its band). **HARD FAIL.** Prefer NESTING the child in the shape's div where you can —
  the browser then enforces it and `measure_dom` reports it for free; use this for what nesting can't say.
- `rotated_bbox(x,y,w,h,deg)` → the axis-aligned box a rotated element ACTUALLY occupies.
- `resolve_label_z(items)` → re-stack an overlapping pile so every object's own LABEL stays
  readable. Returns `(new_z, unresolved)`; `unresolved` means those labels must MOVE, not
  restack — two label boxes on the same spot cannot both be on top.
- `occlusion_check(items)` → **advisory**; an element buried behind higher-z elements.
- `fit_block(available_h, lines, …)` → the size at which a block fits the room left.
- **`scatter_solve(items, W, H, protect=…, keep_out=…)`** → SOLVES a pile's placement
  against protected text, keep-out bands and pairwise overlap. Use it instead of typing
  coordinates for anything more than ~3 loose objects. Returns `(placements, unplaced)`.
- `wash_scan(html,W,H)` → **advisory**; large patterned decoration at low alpha (the 'dirt' defect).
- `star_text_width(diameter)` → helper: the width to constrain text to so it fits a star's waist.
- `antipattern_scan(html)` → **manual only** (not in the auto gate — false-positives on normal
  footers). Call by hand when chasing a blank card (the rotate+overflow:hidden+bottom gotcha).
- **`preflight(W,H,elements,html,color_pairs,page_bg,core,expect_hero=…)`** → runs all the
  zero-false-positive checks above at once, returns `{'clean': bool, ...}`, prints one verdict.
  `under_filled_quadrants` is included but ADVISORY and is NOT PRINTED when it flags all four
  quadrants — a check that fires on every composition carries no signal (verified across the
  session-10 batches). Trust the pixel critique for density. **This is the standing pre-render call.**
- Also: `quadrant_fill_check` (advisory density) and `cluster_positions` (overlapping-pile
  placement) and `pick_fill_mode` (solid-dominant fill picker) — legacy helpers, still valid.

**Auto-enforcement:** `build.render()` ALWAYS runs `css_var_check` (undefined var is unambiguously a
bug). If you pass `render(html, out, W, H, elements=…, color_pairs=…, page_bg=…, expect_hero=…)`, it
also runs the full `preflight` at render time for free.

### 7b. DOM structural — `engine/audit.py` & `engine/reconcile.py`
- `audit.audit(html, name)` (runs inside `build.render`) → margin breaches + real overlaps between
  `.measure`-tagged DOM elements, with whitelisted by-design overlaps (tags-on-hero, sign piles…).
- **`reconcile.measure_dom(page,W,H)` → AUTO-RUNS in `build.render()` on every render.**
  NOTE ON `OVERSIZE`: a headline at the house's own tight line-height (<1) ALWAYS paints past
  its line box, so this used to print on every hero numeral even when the author had correctly
  used `measure_text()['ink_h']` for the bbox. It is now suppressed when the element list you
  passed already declares a box that covers the real extent — so if you still see it, the
  declared box really is too small. Measures the
  real DOM: `clipped` (characters lost), `spilling` (content exceeds a declared size), `off_canvas`,
  plus `boxes` (true extents). This is the ONLY check that sees what hand-written tuples cannot.
- **`reconcile.reconcile_boxes(boxes, elements)` → advisory**, auto-run when `render(..., elements=…)`:
  declared tuples vs. what was drawn — `under_reported` and `untracked`.
- `reconcile.probe(...)` → the legacy Workflow-A-only driver. Prefer `measure_dom`.
- **`measure_dom` also reports `invisible_fill` (auto).** An element whose own opaque background
  is the same colour as the first opaque thing painted BEHIND it. This replaced
  `layout.same_as_bg_scan` in the auto gate, which compared every fill to the PAGE ground and so
  called a cream badge on a full-bleed teal panel invisible on every render. A static scan cannot
  know an element's real backing surface; the browser can. The static one stays as a manual
  diagnostic.
- **`measure_dom` also reports `buried_text` (ADVISORY, auto).** Type that is painted,
  laid out, correctly coloured, inside its box and on the canvas — and invisible, because
  something OPAQUE is in front of it. Catches the z-index trap (an explicit `z-index` on a
  sibling paints above `z-index:auto` whatever the DOM order) and anything else that puts a
  solid object over a word. It walks `elementsFromPoint` and counts only an element with a
  real background as blocking, because `elementFromPoint` alone reports GEOMETRIC stacking:
  a headline at a tight line-height hit-tests ABOVE its own border box and "covers" things
  it does not hide. A repeated-card deck legitimately hides its back copies' text and will
  report here — that is what a deck IS, so this stays advisory.


### 7c. Pixel / metric — `engine/preview.py` & `engine/ref_metrics.py`
- `preview.critique(png)` / `preview.report(png, name)` → `dead_quadrant`, `sparse`, `crammed`,
  `flat`, `flat_dominant`, `uniform`; returns fill, contrast, per-quadrant fill. The headless
  proxy for the looking gate — run it every render, but it is NOT a substitute for actually looking.
- **`compare.crop(path, x0,y0,x1,y1)`** → cut one screen/region out of a MOCKUP reference so a
  single-mechanism recreation can be scored against something honest. Coordinates are canvas
  fractions. Caveat: a crop and a full-res render differ in resolution AND often in aspect —
  run a control (score the render against a downscaled copy of ITSELF) before believing a
  detail-ratio gap is real. On 522f2d89 the control returned 1.12x against a measured 2.49x,
  so most of that gap was genuine, not an artifact.
- **`compare.geometry(path)`** → MEASURE a reference before describing it: content bbox,
  margins, vertical ratio, centroid, coverage and a 9x11 occupancy grid, all as canvas
  fractions. **Run this as step 0 of any recreation.** An eyeballed proportion in the
  written inventory is a confident wrong instruction to the build (sample 3d846c78).
- `ref_metrics.analyze(png)` → `dom_cov`, `mean_sat`, `contrast`, `ink`, `vdr` (visual dominance
  ratio). **Reference targets:** contrast ≈ .26, ink ≈ .11, sat ≈ .31, dom_cov ≈ .46, VDR 0.06–0.20
  (one clear hero; <0.05 = no hero, >0.22 = headline swallows the piece). Treat these like the
  collision auditor — a piece should land within ~0.1 per axis before you call it done.
  (Caveat: flat-vector recreations read low on `vdr` vs. gradient/photo references — a known metric
  limitation, not a visual bug.)
  **SECOND CAVEAT, the opposite direction (session 10f): `vdr` and `ink` INVERT on a dark-ground
  piece.** Their dark-pixel heuristic cannot tell "headline ink" from "the page's own ink ground",
  so a correct dark-ground story measured `vdr = 0.99` against a documented target of 0.06–0.20.
  Do not chase these two numbers on a dark ground; the rest of `analyze()` still reads normally.

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
**Colors** — bg cream `#F4EFE0` (NEVER white) · ink `#0A0A0A`.
⚠ **`PAPER` (#FFFFFF) and `CREAM` (#F4EFE0) are 1.15:1 apart** — a white card on the cream page is
very nearly invisible as a FILL and reads ONLY by its outline or its hard shadow. `invisible_color_check`
flags that pair, correctly; it is not a false positive, it is the two tokens telling you they cannot
carry a figure/ground relationship on their own. Give the card its craft layer, or change one of them. Accents (`core.ACCENTS`, index them
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
(1080,1080) · `linkedin` (1200,628) · `li_square` (1200,1200). LinkedIn crops portrait hard in-feed,
so AQ's LinkedIn art is landscape or square — never 4:5.

**Contrast is MEASURED, never assumed** (all added session 10, from the live site's `tokens.css`):
- `core.text_on(fill)` — the correct text colour ON a fill, decided by computing both candidates.
  (It used to read a hand-kept set and returned white on pink at **3.14:1, failing AA**; ink is 6.31:1.)
- **`core.on_dark(accent, size_px)` — the same decision on the INK ground, which is where about a
  third of the style bank lives.** Measured on `#0A0A0A`: teal is **4.00:1 and FAILS** small type
  (it gets tinted to a lighter partner); mint and grape sit at 4.55:1 and just pass. If you are
  typing a hex value for type on a dark field, you have skipped this.
- `core.on_ground(accent, ground, size_px)` — the general form. It picks the direction by MEASURING
  the ground (darken on light, lighten on dark) instead of assuming, and falls back to whichever
  neutral actually wins there. `on_cream` and `on_dark` both delegate to it. Before it existed,
  `on_cream(accent, 16, ground=INK)` — which that signature openly invites — returned **ink on ink,
  1.00:1, invisible**, because its only fallback darkened.
- `core.lit_of(accent)` — the computed lightened partner, mirroring `ink_of`. It walks the accent
  toward paper in 5% steps and stops at the first value that clears the floor, so the department
  hue survives.
- `core.on_cream(accent, size_px)` — accent type on the page ground. **Accents may shout but may not
  whisper:** a 500px mint numeral on cream is 3.78:1 and passes the large-text floor; a 20px mint
  label is the same 3.78:1 and fails, so it swaps to the darkened partner.
- `core.ink_of(accent)` — that darkened partner. NO raw accent clears 4.5:1 as small type on cream.
- `core.accent_for(dept)` — **department colour is semantic, not a rotation index**: welfare=mint,
  events=sky, labs=lemon, ops=teal, content=grape, matching what the website teaches.
- `core.outline_of(surface)` · `core.hard_shadow(size)` · `core.keyline(ring_bg)` · `core.RADII`
  (32/22/14/pill) — the craft scales, shared with the site.

**Stickers** — ⚠ `shapes.sticker()` renders a SQUARE `size`×`size` svg whatever the silhouette
inside it looks like, so declare `(label, x, y, size, size)` in `elements` — always. Declaring a
wide tag's apparent 220×150 earns a correct `OVERSIZE` report and a collision check that has been
lied to. Its `rot=` is BAKED IN; do not also rotate the wrapping div or the angle applies twice
(`layout.double_rotation_scan` catches that). `doodles.stamp()` behaves identically.
Build every badge with `shapes.sticker()` and fit its label with
`shapes.fit_font(measured_w, measured_at, kind, size)`. ⚠ `shapes.label(size=)` is in BOX
units (0–100), NOT px: inside a 206px badge a 13 renders at 27px. `fit_font` returns box
units and reports `fits=False` when a label simply cannot fit that silhouette — split it
over lines or grow the badge; never ship 5pt type.

**Textures** (`engine/tex.py`) — texture belongs INSIDE a shape that has an edge, at full contrast:
`grain` `paper_fibre` `stripes` `crosshatch` `dot_grid` `grid_lines` `checkerboard` `rays`
`concentric` `duotone` `photo_ink` `tape` `torn` `cutpaper` `riso_offset`. A faint patterned wash is
not texture, it is dirt — `layout.wash_scan` reports it.

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
| Stale bbox tuple hides a real off-canvas/collision | 6 | **`reconcile.reconcile_boxes` (AUTO in `build.render` when `elements=` passed)** — compares declared tuples against what the browser DREW; reports `under_reported` + `untracked`. Was the catalog's only "discipline" row |
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
| Repeated-card "deck" offset points toward the frontmost copy instead of away from it → back cards nest fully inside it, cascade reads as one flat card | `2022ebef4ffad5` | `layout.cascade_peek_check` (advisory, opt-in via `preflight(..., cascade_stacks=[...])`) + rule: offset direction must point away from where the front copy already covers |
| `text_on()` returned WHITE on pink/mint/tomato/grape — white on pink is **3.14:1, fails AA**; ink is 6.31:1 | whole corpus (found session 10 by reading the live site's `tokens.css`) | **`core.text_on()` now MEASURES** both candidates and returns the winner — right for any colour, not a table that can drift. Self-test: `scratchpad/test_brand_truth.py` |
| Accent-coloured SMALL type on cream — no accent clears 4.5:1 there (best teal 4.30, worst lemon 1.36) | whole corpus | **`core.ink_of()` / `core.on_cream(accent, size_px)`** — accents may shout (display sizes clear the 3:1 large-text floor) but may not whisper |
| Department hue picked by arbitrary `accent_idx`, so a welfare poster could come out grape | Workflow A | **`core.accent_for(dept)`** — welfare=mint, events=sky, labs=lemon, ops=teal, content=grape, matching the site |
| Text sized by GUESS: label wider than its pill ("PLANTAT"), headline taller than its band | session 10 batch v1, all 3 pieces | **`build.measure_text()`** (ask the font: layout / content / TRUE PAINTED glyph box) + **`layout.contains_check`** (HARD FAIL). Preferred fix is structural — NEST the label in the shape's div and the browser enforces it |
| Rotated element's real footprint is bigger than its CSS size — a 168px sticker at -9° draws **192px** | session 10 (found by `reconcile_boxes`) | **`layout.rotated_bbox(x,y,w,h,deg)`** — error peaks at +41% at 45° |
| Clipped / oversize / off-canvas text invisible to every static gate | session 10 | **`reconcile.measure_dom` (AUTO in `build.render`)** — the check already existed but was welded inside Workflow-A-only `probe()`; extracted and wired |
| Faint patterned decoration at .05–.34 alpha reads as dirt and smears body copy | friendship_day | **`layout.wash_scan` (advisory, in `preflight`)** — the rule existed in this table with no encoded guard until session 10 |
| `tape()`/craft object in cream on a cream page, or floating with nothing under it | session 10 | rule: a craft object must contrast its ground AND be holding something down |
| Sticker label sized independently of the silhouette holding it — `PATHER SATHI` ran out of both ends of its capsule | motifs v1 | **`shapes.fit_font` / `inner_width`** — a per-family usable-width fraction, fitted from a MEASURED label. Generalises `layout.star_text_width`, which solved this for stars only |
| **UNIT TRAP:** `shapes.label(size=13)` is BOX units (0–100), so inside a 206px sticker it renders at 27px | motifs v1 | `fit_font` returns BOX units, so the caller never does the conversion that went wrong |
| Element placed *behind* another so completely that it reads as a smear, not as depth | motifs v1–v5 | **`layout.occlusion_check`** (advisory) — the general form of `cascade_peek_check`. Caveat documented: a text bbox is mostly air, so it over-reports against type |
| Headline size picked by eye, wraps to one more line than planned, pushes body copy onto the footer | motifs v2 | **`layout.fit_block`** — solve the size from the room that remains. And ALWAYS check `measure_text()['lines']` against the planned line count |
| A multi-line headline declared as ONE bbox: ~60% air, so collision and occlusion checks both become meaningless | motifs v3 | rule: declare a headline as PER-LINE boxes — `KEEP` is 420px wide, not 952 |
| `box-sizing:border-box` means a border eats the content width — every pill in a 28-pill field clipped by 5–6px | motifs v3 | rule: add `2*border` when sizing a box to its measured content. Caught by `reconcile.measure_dom`, invisible to the eye |
| Ten objects hand-placed by coordinate; each fix trades one collision for another (six versions) | motifs v1–v6 | **`layout.scatter_solve`** — constraint placement against protected text, keep-out zones and pairwise overlap. The vector twin of `vision.plan_spots`; returns what it could NOT place rather than dumping it |
| Depth sought by putting badges BEHIND type, which hides their own labels | motifs v6 | rule: in a sticker pile every badge sits in FRONT; depth comes from badge-on-badge overlap, and the type reads because badges land in its gaps |
| A child positioned outside its `overflow:hidden` container — a line of copy sliced off a slab edge. **Scored 0.147, INSIDE the accept gate**; only the eye saw it | 77e7bb34 | **`reconcile.measure_dom` clipped-by-parent** (auto). Excludes the page root `.p`, so deliberate full-bleed stays the `off_canvas` check's job |
| `reconcile._SEL` measured only DIRECT children of `.p`, so NESTING — which the house style recommends — hid elements from the gate entirely | 77e7bb34 | selector widened to every positioned descendant |
| A proportion EYEBALLED into the step-1 written description became a confident wrong instruction: "grid sits high, 2:1 black below" vs a measured 1.05:1. Cost a scoring regression (0.180 → 0.405, IoU 0.87 → 0.60) | 3d846c78 | **`compare.geometry(path)`** — measure the reference's bbox, margins, vertical ratio, centroid and occupancy BEFORE writing the description |
| A drawn mark given the die-cut sticker treatment stops reading as ink | 3d846c78 | **`shapes.ink_mark()`** — flat fill, no halo/outline/shadow. `sticker()` stays for badges |
| An asterisk drawn as wedges radiating from a shared hub reads as a vector sparkle, not a brush mark | 3d846c78 | **`shapes.brush_asterisk()`** — strokes pulled THROUGH the centre, tapered at both ends, bowed, crossing |
| A bitmap motif had no representation at all — any smooth builder destroys the pixel character | 77e7bb34 | **`shapes.pixel_art()` + `AQ_PIXELS`** (drop/leaf/sprout/wave) |
| One object in a deliberately overlapping pile covers ANOTHER'S LABEL. `collision_check` is silent (the overlap IS the design) and `occlusion_check` measures whole objects, so a capsule 60% visible reads fine when the hidden 40% is exactly the words | 522f2d89 | **`layout.resolve_label_z`** — protect the LABEL box, not the object. Raises the buried one just clear; reports `unresolved` when no stacking can fix it |
| A mockup reference (phones on a backdrop) is unscorable — comparing a poster to a picture of three phones on grey measures the grey, so every mockup recreation was parked with NO number | ~1/3 of the corpus | **`compare.crop(path, x0,y0,x1,y1)`** — cut the chosen screen and score against that |

| A style brief printed the reference image's `coverage`/`centroid`/`content_bbox` under "build to THESE numbers" — but that image is a single design in your frame for only **25 of 74** entries. The other 49 measure a 12-up sticker sheet, a photo of a phone on a table, or a whole page scroll | style bank, session 10f | **`stylebank.MEASURED_SCOPE`** (what a non-poster's fractions really describe + what to do instead) and **`stylebank.canvas_shift()`** (an explicit RE-PROPORTION block naming what transfers and what does not) |
| `CANVAS_RULE` told judges a re-proportioned mechanism "should then say how" in the recipe. Nothing checked, so 7 of the 17 cross-aspect entries never mention the frame | style bank, session 10f | **`stylebank.validate()`** reports them as `recipe/canvas`; hard violations are separable via `validate(advisory=False)` |
| **`on_cream(accent, 16, ground=INK)` returned `#0A0A0A` ON `#0A0A0A`** — 1.00:1, invisible. The `ground=` parameter invited the call, but the only fallback (`ink_of`) DARKENS, so on a dark ground it walked the wrong way and fell through to a hardcoded `else INK` | whole dark-ground corpus (~1/3 of the bank) | **`core.on_ground()`** picks the direction BY MEASURING the ground and falls back to `text_on(ground)`, never a fixed INK · **`core.lit_of()`**, the computed mirror of `ink_of` · **`core.on_dark()`** as the named entry point |
| One sentence split across three chips placed at x=48 / x=560 / x=48: chips 1 and 3 share a left edge, so they read as a COLUMN and the copy scans "showing → and again → up again". Everything legible, nothing colliding, no dead quadrant, pixel critique happy. **A Sonnet agent iterated the piece twice, fixed the quadrant the metrics named, and never saw this** | c1_v3, session 10f | **`layout.reading_order_check(parts)`** — INVERSION + COLUMN TRAP, opt-in via `preflight(..., reading_order=[...])`, HARD FAIL when asked |
| The section 6 template's render call omitted `elements=`, so `reconcile_boxes` never ran and an element built-but-never-`append`ed was invisible to EVERY check — a lemon star landed on the words "SIGN-UPS OPEN NOW" while preflight printed CLEAN | c2_v3, session 10f | template fixed to the full call; see section 6 |
| An `ignore_pairs` entry naming a label that is not in `elements` — the author thought about the overlap but never declared the object | c2_v3, session 10f | **`layout.collision_check`** reports ignore pairs naming undeclared labels |
| A test file accumulated THREE `ALL {N} ASSERTIONS PASSED` banners; a run dying at assertion 19 still printed "ALL 18 ASSERTIONS PASSED" first, so grepping for the pass string read a failure as a success | `test_stylebank.py`, session 10f | rule: exactly ONE pass banner, at the end of the file |

| `measure_text()` had no `font-style`, and its canvas TextMetrics call left the style out of the font shorthand — so every Instrument Serif string, whose ONLY brand use is italic, measured **10.7% narrow** and bled off-canvas | session 10f, agent c3 | **`build.measure_text(style=)`**, defaulting to italic for the `'s'` token |
| Type painted, laid out, correctly coloured, inside its box and on canvas — and invisible, because a sibling with an explicit `z-index` buries an element with `z-index:auto` regardless of DOM order. preflight CLEAN, render CLEAN, Playwright `is_visible()` **True** | session 10f, agent c1 | **`reconcile.measure_dom` → `buried_text`** (advisory, auto). Walks `elementsFromPoint` and counts only an OPAQUE element as blocking — `elementFromPoint` reports geometric stacking, and a tight line-height hit-tests above its own box, which made v1 of this check flag visible text |
| Text declared honestly in `color_pairs` as white-on-lavender: `invisible_color_check` passed it (distance is large) while the pair is **1.44:1** and unreadable | session 10f, `110a5730` v4 | **`layout.text_contrast_check`** — HARD FAIL in `preflight(text_pairs=…)`, honours the WCAG large-text split, and reports what `core.text_on()` would have chosen |
| Every child of a card had to be hand-listed in `collision_ignore`; a forgotten pair looks exactly like a real bug | session 10f, agent r1 | **`collision_check(..., containers=(…))`** — containment is not collision, declared explicitly because a doodle inside a headline's bbox is containment too |
| A hardcoded repo root reached **50 Python files**, `AGENTS.md` and a second copy of the manual in the vault — 10e fixed one of three documents. Then 17 more named the CURRENT root, the same bomb with a newer address | five occurrences, session 10f | full sweep to a self-locating root + **`scratchpad/test_repo_hygiene.py`**, which also forbids a second pass banner in any test file |
| `build.render()` forwarded four of `preflight`'s options and silently dropped the rest, so a script needing `cascade_stacks` called preflight by hand and then rendered WITHOUT `elements=` — disabling `suppress_handled` and `reconcile_boxes` too | session 10f, agent c2 | `render()` now forwards every preflight option |
| `stylebank.canvas_shift` fired on a mockup's WHOLE-PHOTO aspect and stated a precise ratio that was not true of the design inside it | session 10f, judging agent | `canvas_shift` returns None for any kind in `MEASURED_SCOPE`; those already get the crop-first warning |
| `stylebank.merge()` required `mechanism` AND `recipe` IN THE DROP-FILE, so a partial update ("a better recipe for an entry you already judged") was silently skipped | session 10f, judging agent | completeness is now checked on the MERGED RESULT, not the drop-file |

| `shapes.sticker()` renders a SQUARE `size`x`size` svg whatever the silhouette looks like, and nothing said so — a wide cloud declared as 220x150 got a correct OVERSIZE report and a collision check that had been lied to | session 10f, agent c2 | docstring states it; declare `(label, x, y, size, size)` always |
| `doodles.stamp(rot=)` / `shapes.sticker(rot=)` BAKE the angle into their own svg. Rotating the wrapping div too draws at the SUM — a star meant for 10° drew at 20°, and `rotated_bbox` (computed for 10°) under-reported the footprint by what looks like rounding | session 10f, agent c2 | **`layout.double_rotation_scan(html)`** (advisory, in `preflight`). Counter-rotation is legal and reports a SUM OF ZERO, which is the tell |
| Two overlap checkers that did not cooperate: `collision_ignore` silenced `layout.collision_check` while `audit.py`'s DOM check kept printing the same overlaps from a closed `SKIP_PAIRS` vocabulary no caller could reach. The only thing that worked was DOM nesting, found by reading source | session 10f, agent c3 | `audit.audit(ignore_pairs=, margin=)`, forwarded by `render()` — ONE declaration now silences both. A gate nobody can silence is a gate everybody scrolls past |
| `audit.py` carried its own `M=64`, a second hardcoded margin in a different file from `build.py`'s `M=64` — agreeing by coincidence of two literals, not because one reads the other | session 10f, agent c3 | `audit.audit(margin=)`, and `render()` passes `build.M` |
| `stylebank._REPROP_WORDS` was a hidden acceptance list: a recipe could fail the canvas check with no way to see why | session 10f, judging agent | `RECIPE_RULE` now PRINTS the enforced tuple (derived, not retyped — the first draft of this fix drifted immediately, "square" vs "squar") |
| `AGENTS.md` was a full second copy of this manual, frozen before session 10: `M = 48`, the render call that disables the measured tier, "all 44 processed" against a 74-item queue, and no knowledge of `measure_text`, `measure_dom`, the style bank or Workflow C. A harness reading it by convention got a confident, authoritative, four-sessions-stale manual | session 10f | `AGENTS.md` is now a pointer to this file. `test_repo_hygiene.py` asserts it stays one |

| A cross-aspect score read as a quality number: a 0.275 phone crop against a 0.5625 story canvas scored 0.534 against a 0.16 accept line while the looking gate found every element present. Discovering that took a control run the builder had to think of | session 10f, agent r1 | **`compare.compare()` now WARNS on an aspect gap >25%** and names the control to run · `compare.aspect_gap()` |
| Workflow C had no ruling for "the drawn style's recipe conflicts with a hard brand rule" (a reference set entirely in serif vs. §9's ≤1 accent word) or "the recipe's colour count vs. the fixed department hue". Both were re-derived from first principles by every builder | session 10f, agent c1 | **§2's precedence ladder** — hard brand rule beats recipe; a recipe's count is a target not a ceiling; the mechanism is the part you may not drop; record every adaptation |

| `same_as_bg_scan` AUTO-RAN and compared every fill to the PAGE ground — so a cream badge on a full-bleed teal panel got "FILL SAME AS PAGE BG (element invisible)" on every single render. Its docstring claimed zero-false-positive. **Two independent agents reported it**, which makes it a spec defect: a static scan cannot know an element's real backing surface, and most AQ posters layer | session 10f, agents c3 and g3 | **`reconcile.measure_dom` → `invisible_fill`** asks the browser what is actually painted underneath. The static scan no longer auto-runs and stays a manual diagnostic |

| **`build.render()` hardcoded `html=None` in its internal preflight**, so `css_var_check`, `img_src_check`, `invisible_craft_scan`, `wash_scan` and `double_rotation_scan` NEVER ran through the documented convenience path — while §6 claimed that one call was the whole gate | session 10f, agent g1 | `render()` passes the html. Its own `css_var_check` now runs only when there is no element list, so nothing is reported twice |
| A design whose MECHANISM is bleeding off both edges printed a wall of `OFF-CANVAS`, and `bounds_check` is a HARD FAIL — so a correct full-bleed build could never report clean, which teaches you to read past a failing verdict | session 10f, agent g1 | `preflight(..., bleed_tags=("pill",))` and `render(..., bleed_tags=…)`. `measure_dom` always had it; nothing above exposed it |

| **A MEASURED field was wrong.** `compare._bg_color` took the modal quantized colour of every pixel, assuming the ground is the largest flat area. On a dense poster it is not: a warm-yellow RISO-TEXTURED field scatters across buckets while solid black type lands in one, so black won and the bank recorded `ground: dark [0,0,0]` for a plainly yellow reference. `design.py` would have briefed a dark piece from it. Blurring first only moved the answer to the largest green plate | session 10f, agent g2 | **`_bg_color` samples the EDGE RING**, because the ground is whatever the design has not covered. 8 of 74 entries changed; the two other `poster` changes were verified by eye as corrections, one is a wash |
| `cross_check` excluded only `mockup` from its ground comparison — the same reasoning covers every kind in `MEASURED_SCOPE`, and it surfaced the moment the ground sampler got accurate enough to read a sheet's dark backdrop correctly | session 10f | excludes all of `MEASURED_SCOPE` |
| `audit.audit(ignore_pairs=)` matches the DOM's `data-tag` while `layout.collision_check` matches the caller's element LABELS — two namespaces behind one argument, so three plates sharing `data-tag="plate"` had the tuple-level ignore work and the DOM-level one silently miss, in the same render call | session 10f, agent g2 (a regression introduced earlier the same session) | `audit` reports ignore pairs matching no `data-tag`, and lists the tags that do exist |

| `buried_text` required EVERY sampled point to be covered, so a plate label with its bottom half sliced off by an overlapping sibling passed with 2 of 5 points clear — and shipped, "SINCE 2021" cut through the middle of its letters. You cannot read the top half of a word | session 10f, g2_v6 | a **3x3 grid** instead of the 5-point X (judging "is half of this covered" needs vertical resolution), reported at a 60% majority — a corner tuck is 1/9 and stays silent |
| "Size it oversize, then clip it with `overflow:hidden`" is a real technique, and `CLIPPED` fired on a visually correct render. The agent worked around its own gate rather than ship a render whose log reads as broken | session 10f, agent g4 | `render(..., crop_tags=("photo","frame"))`, honoured for the container and the child. A DIFFERENT element's accidental clip still fires |
| `core.on_dark` / `on_ground` / `lit_of` existed but were absent from §9 — the section a brief about dark-ground contrast points you at | session 10f, agent g4 | added to §9 with the measured facts (teal 4.00:1 FAILS on ink; mint and grape just pass) |
| `ref_metrics.vdr` and `ink` INVERT on a dark ground — their dark-pixel heuristic cannot tell headline ink from the page's own ink ground, so a correct dark story measured `vdr 0.99` against a 0.06–0.20 target | session 10f, agent g4 | documented in §7c as a second caveat, in the opposite direction from the one already there |

| **The standing auto-resume rule was jammed.** `record()` wrote status `in_progress` whenever a score missed the accept line, so "attempted, did not converge" and "a session is working on this right now" became the same value. `nxt()` resumes in-progress work first and returns the FIRST such entry — so with **36 of them, every new window got the same stuck poster** and the 26 never-touched references were unreachable through the documented entry point. The run sat at 3 done of 74 while 36 had been worked. All 36 carried a score; not one was a real interruption | session 10f | **`runqueue._status()`** derives `attempted` from the data (derived, not migrated — four agents were writing to the JSON at the time), `record()` stores it going forward, and `nxt()` now prefers untouched work then falls back to the attempt CLOSEST to converging. Self-test: `scratchpad/test_runqueue.py` |
| `runqueue.py`'s own docstring told you to run `python engine/queue.py` — a file that does not exist and must not, since a module named `queue.py` in `engine/` shadows the stdlib and broke every bespoke script once already (this same table) | session 10f | every command in it names the real file; the self-test asserts it |

| **No primitive for a flowing BAND** — 12 of the 74 styles call for one (a winding ribbon, a swooping arrow-band, a wavy torn panel edge). A recreation had to hand-write a Catmull-Rom generator from scratch, and every future reference with the motif would hit the same wall | session 10f, agent f80cb | **`shapes.ribbon(points, width=, taper=, closed=)`** — a thick band through control points, with a documented limit: a bend tighter than its own half-width pinches the inner edge |
| `compare.report()` RETURNED its text and printed nothing, while RECREATION_PROTOCOL step 3 is literally `python -c "...compare.report(ref, gen)"` followed by "This prints SCORE + a directed critique list". The documented measure step produced total silence | session 10f, agent f80cb | it prints by default; `echo=False` for a caller that wants the string |
| A persistent `MISSING COLOUR dark/ink` on EVERY version of a recreation whose render was full of that exact black: `_match_palette` is strictly 1:1, and JPEG noise had split the reference's flat black across two adjacent quantization buckets, so the second could never match | session 10f, agent f80cb | **`compare._merge_near`** folds near-duplicates first, at a tolerance READ FROM the quantization step — a guessed 30 missed the real 32 by one unit and the false positive survived the first fix |
| The decision table's `REGION under/over-filled` remedies assume a missing or mis-scaled element. When the cause is a WRONG SHAPE FAMILY they actively misdirect — a ribbon with the right colour, width, endpoints and bbox but a smooth diagonal where the reference hooks burned **3 of 6 iterations** adding filler because the table said to | session 10f, `80cb7ed71a8cc9` | a new row plus "WHEN THE REGION ROWS ARE LYING TO YOU" in `RECREATION_PROTOCOL.md`: the tell is an over-filled cell BESIDE an under-filled one with balanced totals |
| `buried_text` keyed on "has own text", so a buried IMAGE was invisible to it — a fade layer above `build.logo()`'s hardcoded `z-index:20` made the wordmark vanish completely with every gate clean | session 10f, agent f62f8 | an `<img>`/`<svg>`, or anything tagged `logo`, now counts as content |
| `audit.py`'s `BLEED` and `MARGIN_OK` were closed vocabularies baked into that file, so a script with a deliberately bleeding element could not tell that gate — an agent dropped elements from it rather than live with permanent noise, ending with DOM coverage on 4 of 7 | session 10f, agents f80cb + f62f8 | `audit.audit(bleed_tags=)`, forwarded by `render` — ONE declaration now reaches `preflight`, `audit` and `measure_dom` |
| `PAPER` (#FFFFFF) and `CREAM` (#F4EFE0) are **1.15:1** apart, so a white card on the cream page reads only by its outline. `invisible_color_check` flags the pair, correctly — but nothing said so, and it looked like a false positive | session 10f, agent f62f8 | stated in §9: the two tokens cannot carry a figure/ground relationship without a craft layer |

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
- **`brain/CONTENT_SYSTEM.md`** — the hub doc for everything beyond a single poster: which doc owns
  which surface (Instagram, LinkedIn, brochures/catalogs/PDFs), what's built vs. spec, the shared
  build order, and the node map (§6) tying every brain doc together bidirectionally. **Start here**
  for any task that isn't a plain feed-poster generation. It indexes:
  - **`brain/VOICE.md`** — the full voice system: lane x audience x channel x intent, a truth
    ladder for numbers, a do-not-say list, worked examples. Supersedes the old 4-line voice note
    in `DECISIONS.md`. Spec only (§11 there scopes what encoding it requires) — apply it by hand
    until `engine/copy.py` exists.
  - **`brain/IDEATION.md`** — the Instagram/LinkedIn post-idea engine: content pillars, a
    post-type taxonomy, hook formulas, a rotation rule against repetition, and a brief-generator
    that resolves a raw event into a full brief via `VOICE.md` §7. Spec only.
  - **`brain/BROCHURE_CATALOG.md`** — spec for one-pagers, tri-fold brochures, program catalogs,
    impact reports and partnership decks: new multi-page canvas sizes, a shared page-grid system,
    five page roles, and the render-pipeline extension (PDF assembly) this would need. Spec only,
    with explicit print-safety caveats (sRGB vs. CMYK, no bleed/fold marks yet) — read before
    treating any output as print-ready.
  - **`brain/AQ_FACTS.md`** — the sourced fact/fingerprint bank behind `VOICE.md`'s truth ladder,
    built 2026-08-26 from a real ingestion of 47 AQ/Shikshaq documents and ~105 photos/designs
    (CSR proposal, org strategy briefs, Shikshaq UX research, published posts). Pull real numbers
    from here; never invent a plausible-sounding one.
  - **`brain/GAPS.md`** — the first-class, centrally-tracked open-questions log for the whole
    content system (voice, ideation, brochures). Check here before assuming a question is
    unresolved — several were answered by the 2026-08-26 ingestion.
- `training_samples/reference_posters/` — the 44 references. `out/versions/<slug>/` — recreation
  iterations. `out/` — fresh generations. `sample_outputs/` — example engine outputs.

---

## 12. CURRENT STATE / WHAT'S PENDING (honest — full detail in `brain/ENGINE_STATE.md`)
- Workflow A: 3 archetypes fully self-correcting (`number_hero`, `radial_orbit`, `giant_type`);
  `stacked_zones` registered. Pending: 5 more (`diagonal_cascade`, `off_frame_bleed`,
  `scatter_collage`, `isometric_grid`, `corner_anchor`) — geometry exists in `engine/archetypes.py`,
  needs wiring into the self-correcting pipeline + looking gate.
- Workflow B: the original 44 are processed (`brain/RECREATION_PROGRESS.md`). **30 NEW
  references were added 2026-09-19 (`runqueue.py init`, queue now 74).** Accepted so far
  from the new set: `3d846c781bd059` (0.123, 3 iters), `77e7bb34144e08` (0.11, 2 iters).
  PARKED: `522f2d898b827f` (0.619, 4 iters) — a phone screen recreated on AQ story;
  the looking gate passes and the mechanism is faithful, but the score is NOT
  comparable to a same-aspect recreation. Recorded as parked, not accepted.
  **A recreation is NOT done at an accepting score** — 77e7bb34 v1 scored 0.147, inside
  the gate, while a whole line of copy was sliced off its slab. The looking gate is what
  caught it; compare.py cannot see a missing line of copy.
- Gate stack: the §10 guards are encoded in `layout.py`; `preflight` bundles them; `css_var_check`
  auto-runs in `render`; `render(..., elements=…)` runs the full preflight at render time.
  **Session 10 added a MEASURED tier** — `reconcile.measure_dom` auto-runs on every render (clipped /
  oversize / off-canvas, from the real DOM) and `reconcile_boxes` reconciles declared tuples against
  what was drawn. This closes the gap that let three posters pass the whole static stack while
  visibly broken: static checks can only ever verify what the author TYPED.
  **Render is ~9x faster** (16.81s → 1.86s/poster in a `B.session()`), output verified pixel-identical.
  **Self-tests (all passing, verified 2026-08-03) — each assertion reproduces a real historical bug:**
  `test_layout_rules.py` (76) · `test_collision_nudge.py` (9) · `test_invisible_craft.py` (11) ·
  `test_doodle_stamp.py` (25) · `test_vision_starve.py` (13) · **`test_brand_truth.py` (34) ·
  `test_texture.py` (25) · `test_measured_layout.py` (32) · `test_placement.py` (30) ·
  `test_recreation.py` (47) ·
  `test_stylebank.py` (64) · `test_buried_text.py` (24) · `test_repo_hygiene.py` (28) · `test_runqueue.py` (16)** —
  **435 assertions total, all verified passing 2026-09-20**. `test_repo_hygiene.py`
  EXECUTES the §6 template and requires it to pass its own gate — the copy-paste
  skeleton carried a dead path for months precisely because nobody ever ran it.. All in `scratchpad/`.
  Run them before trusting the gate stack.
  (`test_layout_rules.py` had been cited here as 21 assertions while missing from disk entirely;
  rebuilt 2026-08-03 — if a doc cites a test, open it before repeating the claim. Verified again
  2026-09-03: its `os.chdir` still pointed at the project's pre-move folder, so despite being on
  disk it had silently never actually run since the repo relocated — fixed, now genuinely 31/31.)
- Collision auto-nudge is now encoded (§10) — no pending fix-rules remain from the §10 catalog.
- **OPEN DECISION (session 10):** the live site's ops/teal is `#12909C`; the engine's canon teal is
  `#0E7C86`. Recorded as `core.DEPT_SITE_TEAL` rather than reconciled, because changing `ACCENTS[6]`
  restyles all 44 recreations. Someone should decide which one wins.
- **Motifs built from the 2026-09 reference dump** (`scratchpad/gen_motifs_v6.py`, output in
  `out/session10b/`): sticker swarm (badges in the gaps of a headline), staggered bleed rows
  (a full-canvas field of named pills), duotone photo (two-plate riso that keeps faces), and
  notched interlocking slabs. These are worked examples, NOT registered archetypes — the
  Workflow A registry is still the same four.
- **Real content source:** `welfare_projects_rows.csv` (558 logged welfare projects, 2021–2026) is
  the first real dataset wired into generation. Counted figures: 558 projects · 291 workshops ·
  126 returns to Pather Sathi · 3,756 volunteer TURNOUTS (not unique volunteers — the qualifier
  travels with the number, `VOICE.md` §2). Worked examples: `scratchpad/gen_csv_batch_v5.py`,
  output in `out/session10/`.
- The looking gate is only as good as the checklist + the eye. It runs EVERY time; that is its value.
  **Keep converting each new visual catch into an encoded rule (§8).**
- **STYLE BANK BRIEFS NOW STATE WHICH FRAME THEIR NUMBERS ARE IN (session 10f).** Only
  **25 of 74** entries are a same-frame `poster` whose measured fractions are build
  targets; 45 are a sheet/mockup/asset/carousel measuring something that is not a
  composition, and 17 are judged onto a canvas >25% from their own aspect. `brief()`
  prints a RE-PROPORTION block and a MEASURED_SCOPE warning accordingly.
  **7 recipes still owe a re-proportioning sentence** — `python engine/stylebank.py validate`
  names them.
- **STYLE BANK (new, session 10e): `brain/STYLE_BANK.json` holds all 74 references as
  usable STYLES — measured fields from the pixels, judged fields from eyes, all 74 judged.**
  `python design.py "<subject>"` draws one educated-random and prints a build brief; see
  Workflow C in §2. `stylebank.py schema` is the judging contract (it lives in the module,
  not in a prompt); `stylebank.py crosscheck` catches a judgment written about the wrong
  image by comparing its claimed ground against the measured one.
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
