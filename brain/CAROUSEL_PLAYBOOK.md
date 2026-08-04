# PHOTO CAROUSEL PLAYBOOK — real-photo Workflow B, batch-of-many mode

Origin: `scratchpad/gen_sunderbans8_carousel_v1..v6.py` (session 2026-07-23). This is the
reference implementation for any future real-photo carousel (event recaps, camp trips, field
visits — anything built from actual AQ photos rather than illustrated archetypes). Read this
BEFORE starting a new carousel; copy v6's helper block wholesale rather than re-deriving it.

This exists because the next ask is 20-30 of these in a batch, not one-offs. Everything below is
either (a) a helper that must not be re-invented per-post, or (b) a mistake this session made once,
fixed, and should never re-occur.

## The helper block (copy verbatim from `gen_sunderbans8_carousel_v6.py`)
- `logo_pill()` — **bare logo, no pill/border/background.** 56px height, `drop-shadow(0 2px 6px
  rgba(0,0,0,.5))` for legibility against any photo tone. (Earlier iteration had it boxed in a
  cream pill — removed on request; a drop-shadow alone is enough contrast on real photos.)
- `dots(n, active, accent)` — carousel position dots; the ACTIVE dot takes that slide's rotating
  accent color, not a fixed white. Threads the one recurring UI element through the accent rotation.
- `scrim_bottom(h, tint)` / `scrim_top(h, tint)` — black gradient + an optional faint accent-color
  wash (`{tint}4D` fading to transparent) layered underneath. Gives every slide's dark band a hint
  of that slide's color instead of reading flat black across a 20-30 post batch.
- `sticker(txt, accent, x, y, rot)` — the mono-label pill chip (ink border, offset shadow — same
  craft language as `build.chip()`).
- `index_tag(page_index, total, accent)` — small "01 / 05" pill in the scrim corner. **This is the
  only numeric claim allowed to be invented-looking** because it's literally true (real carousel
  position) — never repurpose this slot for a fabricated stat.
- `filler_set(spots, slide_seed)` + `VOCAB` (16 doodles) + `ACCENT_ORDER` (7-accent rotation) +
  `SIZES` — the systematic variety engine. `spots` is the only hand-picked input (photo-dependent
  free-zone anchors); kind/color/size/rotation are ALL derived from `slide_seed` so no two slides
  reach for the same 3 doodles out of habit. `connector()` draws a dashed line between the first two
  spots per slide — ties the scatter into a small constellation, purely decorative, zero collision
  risk since it lives inside the same pre-verified empty zone.
- **No `frame_border()`.** It was tried (10px ink border around the whole canvas) and pulled on
  request — reads as a "boxed screenshot," not a poster, on full-bleed real photos. Do not re-add
  it to this carousel style. (It may still suit an illustrated/flat-vector archetype — that's a
  Workflow A question, not this playbook's.)

## Per-slide checklist (do this for every one of the 20-30 posts, every slide)
1. **Look at the photo first.** Identify the genuinely empty zone (sky, wall, ceiling) — this is
   the only manual step, because it's the one thing that depends on actual photo content.
2. **Estimate the face/subject bbox** in script-space (photo is `W×H` = 1080×1350, PNG output is
   2x that). Keep every filler, sticker, and index tag OUTSIDE that bbox — not just "near it."
   A chip that touches hair or a shoulder edge still reads as a collision at 1:1 zoom.
3. **Check margin, not just face-clearance.** A sticker chip is ~120-200px wide depending on text
   length; placed within ~150px of the right/bottom canvas edge it WILL clip (`FREE CHECK` instead
   of `FREE CHECKUP` was this exact bug). If the only clear zone is edge-adjacent, drop the sticker
   into the bottom scrim band instead (guaranteed dark, guaranteed full-width, zero subject risk)
   rather than fighting for space in a cluttered sky pocket.
4. **Don't stack fillers where they were already dense.** The Sunderbans sky (img1/img2) ended up
   crowded (5-6 doodles in one small pocket) because `filler_set` was handed too many spots for how
   little clear sky the photo actually had. Count the real free area first; 3-4 fillers reads as
   "constellation," 6+ in a small pocket reads as clutter.
5. **Sticker copy must describe THIS photo, not a generic mood-word.** "Every plate, every form" on
   a photo with neither plates nor forms visible was a real miss — the caption should survive
   someone comparing it side-by-side against the actual image. Prefer echoing/complementing an
   existing caption over duplicating it verbatim.
6. **Never let a sticker/tag invent a fact.** "day 1/8" implied an 8-day itinerary nothing
   established — swapped for the truthful, derivable "01 / 05" carousel-position tag. If a number
   isn't literally knowable from the shoot, don't put it in a chip.
7. Render → `Read` the PNG → walk this checklist against what you SEE, not what the code intended.
   The static preflight gate (`CLEAN ✓`) only catches off-canvas/undefined-var/named collisions in
   the manually-maintained bbox list — it does NOT know a chip sits on a face, because faces aren't
   tracked as elements. That check is only ever caught by looking.

## Batch-of-many operating notes (for the 20-30 run)
- **One slug per event/post**, versioned the normal way (`out/versions/<slug>/vN/`). Don't reuse
  `slide_seed` values in a way that makes every post's rotation identical — vary the STARTING
  `slide_seed` per post (e.g. seed the first slide of post N at `N` instead of always `0`/`1`) so
  batch output doesn't visually repeat the same doodle-kind/accent pairing across posts even though
  each individual post is internally systematic.
- Keep the source photos for each post in its own `scratchpad/carousel_<slug>/src_images/` folder,
  mirroring this session's `scratchpad/carousel_sunderbans8/`.
- Every post still owes the full looking gate (`brain/VISUAL_REVIEW.md`) AND the standing
  `/canvas-design` companion-art rule (CLAUDE.md preamble) — batch size does not waive either.
- If a NEW general failure class turns up during the batch (not covered by the checklist above),
  stop and add it here per CLAUDE.md §8 before continuing — that is what keeps the 30th post better
  than the 1st, instead of just as error-prone.
