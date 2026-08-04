# 5. Workflow B - Reference Recreation

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

## See also
- [[Recreations Index]]
- [[06 The Bespoke Script]]
- [[10 The Bug Catalog]]

[[Manual Index]]
