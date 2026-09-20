# Judge 2 — recipe/canvas re-proportioning pass

Scope: the 7 slugs `stylebank.py validate` flagged under `recipe/canvas` on 2026-09-20:
`2af2568a52cc92`, `4939a628d6deb2`, `522f2d898b827f`, `62f8cc4d3c6135`, `b075bc30db0422`,
`d88c31285a237f`, `fa3e4affb80375`.

## What worked
Reading one reference image per `Read` call and writing its recipe immediately, before
opening the next, was easy to hold to and I didn't catch myself cross-attributing slugs.
`validate` and `crosscheck` are fast, cheap, and their pass/fail messages are unambiguous.

## Friction — real, not "it was fine"

### 1. `canvas_shift()` measures the WRONG aspect for `mockup` entries, and the schema says so itself
This is the big one. `stylebank.py`'s own `MEASURED_SCOPE` dict documents, for `kind: mockup`,
that `measured.*` describes **"THE PHOTOGRAPH — BACKDROP, DEVICE AND SHADOWS INCLUDED"**, and
explicitly tells the judge to crop the design out and measure THAT instead (`compare.crop`).
But `canvas_shift()` — the function `validate`'s `recipe/canvas` check runs — reads
`measured.aspect` straight off the bank entry with no branch for `kind`, so for a mockup it is
comparing the judged canvas against the aspect of the **whole photographed scene**, not the
aspect of the extracted screen/mechanism the recipe actually describes.

I hit this concretely on three of my seven slugs:
- `522f2d898b827f` — flagged as "1.018:1 ref judged story (0.562:1)". The 1.018 is the aspect of
  the two-phone photograph shown side by side. The actual mechanism (the RIGHT phone's screen,
  which is what the recipe describes) is a normal portrait phone screenshot, already close to
  story's 0.562. There is barely any real re-proportioning to write — the flag is measuring the
  wrong thing. (This is also the same slug CLAUDE.md §12 already flags as "PARKED... the score
  is NOT comparable to a same-aspect recreation" for exactly this reason — a precedent for the
  bug existed in the manual and nothing in the tooling used it.)
- `d88c31285a237f` — flagged as "1.333:1 ref judged story (0.562:1)". The 1.333 is five
  onboarding phone screens laid out in a row. The mechanism is ONE screen, which again is
  naturally close to story's proportions.
- `fa3e4affb80375` — flagged as "1.001:1 ref judged story (0.562:1)". The 1.001 is a single
  phone-on-a-yellow-backdrop photo; the `content_bbox` fraction of that same entry
  ([0.283,0.062]-[0.713,0.932]) implies a screen aspect of roughly 0.49 — again close to story,
  not square.

I wrote genuine re-proportioning language into all three recipes anyway (because the task asked
for it, and because "build straight to the canvas, don't stretch it to match a mismeasured
aspect" IS a legitimate instruction), but the underlying validate signal that sent me to these
three was partly noise. A judge who trusted the number at face value (rather than opening the
image) would invent a compression story that doesn't need to exist. **Suggested fix (not made —
out of scope): `canvas_shift()` should skip or downweight the check when `kind == "mockup"` and
no `crop` region is recorded, or `measure()` should store a separate `screen_aspect` from
`compare.crop` for mockups.**

The other four slugs (`2af2568a52cc92`, `4939a628d6deb2`, `62f8cc4d3c6135`, `b075bc30db0422`)
had a real, load-bearing aspect mismatch worth writing about — `2af2568a52cc92`'s `measured`
looks like it actually WAS taken from a crop (its content_bbox ratio is close to its stated
aspect), so that one behaved as documented.

### 2. `merge()` silently drops an entry that only supplies `recipe`, contradicting the task's own drop-file example
The task prompt says to write a drop-file shaped `{"<slug>": {"recipe": "..."}}`. But
`merge()`'s actual rule is:
```python
if not clean.get("mechanism") or not clean.get("recipe"):
    skipped.append((fn, slug)); continue
```
A drop-file with only `recipe` has no `mechanism`, so `clean.get("mechanism")` is falsy and the
whole entry is **silently skipped** — `merge()` doesn't error, it just doesn't fold it in, and
you only find out by reading the "SKIPPED" lines it prints (easy to miss if you don't pass
`verbose` output through, and the tool has no dry-run/plan mode to catch this before writing).
I caught this by reading `stylebank.py` source before running merge, not from any message the
tool gave me proactively. I worked around it by copying each entry's existing `mechanism` string
verbatim into my drop-file (unchanged) alongside the new `recipe`, since `update()` only touches
keys present in the drop-file and I didn't want to touch `kind`/`hero`/`canvas`/`tags`/`depts`.
**A judge who followed the task prompt's example literally would have every single one of their
recipe-only fixes vanish with no error, only a "SKIPPED" note buried in ~50 lines of merge output
from everyone else's drop-files landing in the same run.**

### 3. Schema is silent on how many sentences a re-proportioning addition should cost against the 3-5 sentence budget
`RECIPE_RULE` caps a recipe at 3-5 sentences and demands it state a restraint. Several of my
flagged entries already had 4-5 sentences of legitimate content before I added anything, so
"add the re-proportioning" and "stay under 5 sentences" were in direct tension — I ended up
merging existing sentences with semicolons to make room (e.g. `4939a628d6deb2`,
`522f2d898b827f`, `62f8cc4d3c6135`, `b075bc30db0422` all needed a trim-and-merge pass, not a
pure append). The schema doesn't say whether the re-proportioning instruction is allowed to be
its own bullet outside the 3-5 sentence count, or must compete with the original content for
the same budget. I assumed the latter (single unified recipe, still 3-5 sentences total) as the
more defensible reading, but a second judge could reasonably have appended a 6th/7th sentence
instead and produced recipes that read as instruction-dumps.

### 4. `_REPROP_WORDS` is a hidden acceptance list, not part of the visible schema/contract
`validate()`'s pass/fail for "did the recipe mention re-proportioning" is a keyword substring
match against `_REPROP_WORDS` (`compress`, `re-proportion`, `landscape`, `portrait`, `wider`,
`taller`, `side by side`, `stack`, `aspect`, `squar`, `column`, `row of`, `band`, …), invisible
unless you read the source. I wrote physically concrete instructions that happened to use words
like "portrait", "stack", "column", "side by side" naturally, so I passed on the first try, but
this is luck as much as design — a recipe could give a perfectly correct, concrete
re-proportioning instruction ("let the ribbons sweep top-to-bottom instead of crossing
side-to-side") and still fail the automated check if it phrased the compression without hitting
one of these exact substrings. `schema` (the documented contract) should either surface this
list or the check should be semantic rather than lexical.

### 5. `crosscheck` gave no feedback tied to my edits
`crosscheck` only reports contradictions against `measured.ground_rgb`/luminance — none of my
edits touched `kind`/`ground`-adjacent fields, so it printed a clean bill with zero signal either
way about whether my new recipe text was reasonable. That's expected given what the function
does, but worth naming: neither `validate` nor `crosscheck` can tell you whether a
re-proportioning recipe is *actually correct* for the reference image, only whether it exists
and doesn't contradict ground colour. The only real check is a human reading the image next to
the words, same as the rest of this engine's "the looking gate is the only real gate" philosophy
(CLAUDE.md §3) — it's just not automated here, and validate's clean pass can read as more
assurance than it is.

## Entries where I think a judged field might be wrong (not changed, just reporting)
None of the `kind`/`canvas`/`hero` judgments on these 7 struck me as wrong once I actually saw
the images — `mockup` is right for all the phone/tablet/device shots, `sheet` is right for the
three-panel jazz poster, and the canvas choices (feed/linkedin/story) all make sense for the
kind of use each mechanism would actually see on Instagram/LinkedIn. My only real reservation is
the *measurement* used to flag `522f2d898b827f`, `d88c31285a237f`, and `fa3e4affb80375` (see
friction item 1 above) — that's a tooling gap, not a bad judgment call by whoever set `canvas`.

## Where I was unsure / what I'd have needed
- For `522f2d898b827f`, `d88c31285a237f`, `fa3e4affb80375`: whether to write a "real" heavy
  compression story to satisfy the keyword check, or to write the honest "there isn't much
  compression here, the flag is measuring the wrong crop" story. I chose honesty + a short
  concrete instruction (extend density into the extra run, don't stretch), which is both
  correct and happens to satisfy the checker, but I'd have wanted a documented way to say
  "this flag is a measurement artifact, not a missing instruction" without it looking evasive.
- For `b075bc30db0422` (three-panel sheet → linkedin banner): the reference shows exactly three
  crops; I decided the honest linkedin-shaped answer is TWO panels, not a squeezed three,
  because a third full-height column genuinely does not fit a 628px-tall frame at a legible
  size. I'd have liked a stated policy on whether a "sheet" mechanism's item-count is itself a
  free variable when re-proportioning, or whether it's meant to be preserved and only the crop
  tightness varies.

## Summary
- Recipes rewritten: 7 (all 7 flagged slugs).
- `validate`: clean (`all judged entries conform to the schema`).
- `crosscheck`: clean (`no judgment contradicts its measured ground`).
- Top 3 friction points: (1) `canvas_shift()` uses the whole-photograph aspect for `mockup`
  entries even though the schema itself says that field describes the photograph, not the
  design, producing 3/7 flags that were largely measurement artifacts; (2) `merge()` silently
  skips a drop-file entry that omits `mechanism`, which is exactly the shape the task prompt's
  own example tells you to write; (3) the 3-5 sentence recipe budget and the re-proportioning
  requirement compete for the same room with no guidance on how to resolve that, requiring a
  trim-and-merge rewrite rather than a clean append on 4 of the 7 entries.
