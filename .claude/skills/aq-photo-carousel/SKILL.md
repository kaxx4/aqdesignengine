---
name: aq-photo-carousel
description: Build AQUATERRA (AQ) real-photo Instagram carousels in batch from event photographs — sourcing them from public Google Drive folders and a project CSV/database export, picking frames by looking, rendering on-brand slides through the AQ engine, and backfilling the CSV's image columns. Use whenever the user asks for AQ carousels, event/workshop recap posts, "make carousels from these photos/this Drive folder/this CSV", or wants a project export's empty image columns filled from real photos. Complements the aq-design-engine skill, which covers single illustrated posters.
license: Internal AQUATERRA tool. Brand assets embedded in the engine (logo, fonts, photos) are AQUATERRA's own and are not licensed for reuse outside AQUATERRA work.
---

# AQ photo carousel — batch pipeline

For **real-photo carousels built from actual event photographs**: workshop recaps, camp trips,
field visits, distribution drives. For a single illustrated/archetype poster, use the
`aq-design-engine` skill instead — different code path, different rules.

**Read `CLAUDE.md` at the repo root first.** This skill is a pipeline on top of that manual, not a
replacement for it. §3 (looking gate), §8 (encoding fixes), §9 (brand constants) and §10 (bug
catalog) all apply unchanged. `reference/CAROUSEL_PLAYBOOK.md` in this skill is the per-slide
checklist and the accumulated failure list — **read it before the first render, not after.**

## The one thing that makes this pipeline work

Every stage is measured or looked at; nothing is assumed. Specifically: **a gate printing `CLEAN ✓`
is not evidence a slide is good.** The gates check what exists — they cannot see a doodle sitting
on a child's hair, a photo whose text reads backwards, a cover duplicated as the closer, or a slide
with no decoration at all. In this batch every one of those shipped past a clean gate and was caught
only by looking at the rendered PNG. Budget for that.

## Pipeline

### 1. Inventory before promising anything
Parse the export. Find the candidate events (date range, `objective`, etc.). For each, note the
photo source: existing image URLs in the row, and/or a `google_drive_link`.

`scripts/drive_fetch.py` lists and downloads a **public** Drive folder with no API key. Count
photos per event before deciding what is buildable:

```bash
python scripts/drive_fetch.py <folderId>
```

Report the honest count. A private folder returns a sign-in page and lists nothing — that is a
blocker to name, not to work around.

### 2. Download into per-event folders
`fetch_folder(folder_id, dest, cache)` → `carousel_<batch>/<slug>/src_images/00.jpg …`. The
thumbnail endpoint is used deliberately: it returns real JPEGs for HEIC sources, which the raw
download endpoint does not.

### 3. Pick frames by LOOKING
```bash
python scripts/contact_sheet.py carousel_<batch>/<slug>/src_images
```
Read the sheet, then choose by index. What to check while looking:

- **Portrait frames crop far better** to 1080×1350 than landscape (the sheet prints dimensions).
- **Cover and closer must be different moments** — consecutive frames of one group read as a
  duplicate.
- **Read any text visible inside the photo.** A card photographed with reverse-side ink bleeding
  through reads backwards on the slide.
- **Near-duplicates**: two frames a second apart are one frame. Prefer a shorter carousel.
- **Does the folder actually belong to this event?** Check filename dates against the row's date.
  A folder linked from three different rows cannot be honestly attributed to any of them.

### 4. Write the job
Copy `scripts/jobs.example.py`. Per event: `picks` (cover), `slides` (photo, caption, sticker),
optional `type_slides`, `seed`, `extra_exclude`.

**All copy comes from the row's own fields** — `key_statistic`, `short_summary`. Never invent a
number. Captions describe *the photo they sit on*, not a generic mood. The only generated
number allowed is the `NN / NN` index tag, which is true by construction.

### 5. Render
`scripts/build_carousel.py` holds the helper block (logo, tinted scrims, accent-rotating dots,
truthful index tag, sticker, vision-driven doodles, type slide). Point `ROOT` at the batch folder.

```bash
PYTHONIOENCODING=utf-8 python -c "import asyncio,sys,importlib.util; sys.path.insert(0,'<batch>'); s=importlib.util.spec_from_file_location('bc','<batch>/build_carousel.py'); bc=importlib.util.module_from_spec(s); s.loader.exec_module(bc); from jobs import JOBS; asyncio.run(bc.build(JOBS['<slug>'],'v1'))"
```

Renders are slow (~10 s/slide). Batch them in the background; don't poll.

### 6. Look — montage first, then full size
```bash
python scripts/montage.py review.jpg <slug>:v1 <slug2>:v1 ...
```
Read the montage: it exposes cross-slide problems a single-PNG review hides. Then Read full-size
any slide the montage flags. Walk `reference/CAROUSEL_PLAYBOOK.md`'s per-slide checklist.

**Read the build output too, don't grep it for a guessed keyword.** `preflight` prints `ISSUES:`
followed by e.g. `collisions: [('accent_field','doodle3',58,58)]`. A real collision was missed in
this batch purely because the run was filtered for the wrong string.

### 7. Fix at the rule, re-render, look again
Per `CLAUDE.md` §8. A per-photo fix (an `extra_exclude` box) is legitimate when the alternative is
a global heuristic that would false-positive — but **measure the box off a render, never estimate
it.** An estimated box missed on the first try and the doodles landed on hair a second time.

### 8. Deliver + backfill
Export to a flat, posting-ordered folder (`01.png` = cover) with a README recording what was built,
what was skipped and why, and any data problems found.

`scripts/fill_images.py` backfills the export's `main_image` / `image_N` / `*_alt` / `label_N`
columns from the chosen photos. It **only fills empty cells**, stages files under their final
storage object names, writes a COALESCE-guarded idempotent `patch.sql`, and emits an uploader.
Verify `EXISTING CELLS OVERWRITTEN: 0` before handing it over.

## Hard rules specific to photo carousels

- **`vision.plan_spots` returning `[]` is silent death.** The slide renders with no craft layer and
  every gate passes because nothing exists to fail. Always use **`vision.plan_spots_relaxed()`**,
  which escalates `busy_pctl` and warns `starved`. Self-test: `scripts/test_vision_starve.py`.
- **Never exclude a full-width band.** `background_grid` keeps only free regions touching the top
  edge, so a full-width top band severs every candidate and starves the photo to nothing. Shape
  excludes like the UI — a logo box, a dots box.
- **Accent first, contrast second.** `pick_visible([accent, white, ink])` ranks by luminance delta
  and picks near-black ink on every bright wall; a thin dark stroke on textured concrete reads as
  dirt. Test the accent alone; fall back only on failure.
- **Every photo doodle needs a hard drop-shadow**, or it reads as a scuff on the photograph.
- **Hair is not background.** vision's skin veto cannot see it, so doodles land on heads with a
  clean gate. Tight portraits need a measured `extra_exclude`.
- **Photo-poor events get a type slide, not padding.** Never reuse a near-duplicate frame; never
  fabricate imagery (§9 real-assets-only). `render_type_slide()` sets the row's own statistic as
  the hero. Space that stack by the hero's *measured* line count, never a constant.
- **Don't whitelist a collision on a layout where nothing should overlap** — that is exactly what
  hides the real bug.
- **Large areas carry the palette; punctuation carries the contrast.** When biasing the palette
  (e.g. "more blue-green"), constrain the *large/structural* rotation — scrim tints, dots, index
  tag, type-slide field — and let small doodles keep a contrasting rung. Removing the contrast
  entirely turns a bias into a colour cast over the photographs.

## Judgement calls that are NOT yours to make

Surface these and stop; do not guess:

- A photo folder that can't be attributed to one event (shared across rows, or containing visibly
  different sessions).
- Publishing identifiable people — especially children — alongside sensitive subject matter.
- Duplicate rows in the export: say which to delete rather than filling both.

## Self-test

```bash
PYTHONIOENCODING=utf-8 python scripts/test_vision_starve.py   # 13 assertions, each a real bug
```
Plus the engine suites listed in `CLAUDE.md` §12 after touching `engine/`.

## Companion art piece

CLAUDE.md carries a standing rule: invoke `/canvas-design` once alongside any engine output to
produce a companion philosophy note + art piece. A batch does not waive it.
