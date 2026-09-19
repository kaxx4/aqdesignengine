# CONTENT SYSTEM — the map of everything AQ's brain now covers

Status: **index + architecture, read this first when the task isn't a plain feed poster.**
This file doesn't introduce new rules; it says which doc owns which surface, what's actually
built vs. spec, and the one spine every surface routes through.

Origin: the engine (`CLAUDE.md`) was built for one output — 1080x1350 Instagram posters, as a
direct outcome of encoded rules. That principle (§1 there: never hand-tune, fix the rule) doesn't
change when the surface changes. This file exists because "extend the brain across LinkedIn,
Instagram ideation, voice, brochures, catalogs, everything" is a request to cover more *surfaces*
with that same principle, not to replace it with something looser per-surface.

---

## 1. THE SPINE (the part every surface shares, non-negotiable)

Every surface below — built or spec — routes through the same three layers before anything
renders or gets typed:

```
BRAND TOKENS (engine/core.py)      — colors, fonts, logo, real photos. The law. Never per-surface.
        |
VOICE_PROFILE (brain/VOICE.md §7)  — lane x audience x channel x intent -> register, banks, shape
        |
CRAFT / GATE STACK (CLAUDE.md §7)  — the looking gate + the encoded checks, scaled to the surface
```

A surface-specific doc (IDEATION, BROCHURE_CATALOG) is never allowed to invent a color, a font, a
voice rule, or a truth-ladder exception. If a surface seems to need one, that's a signal the spine
is missing something general, not that the surface gets a local escape hatch — same logic as
`CLAUDE.md` §8 ("fix the RULE, never the individual output"), one level up.

---

## 2. THE SURFACE MAP

| Surface | Owning doc | Status | Renders via |
|---|---|---|---|
| Feed poster (1080x1350) | `CLAUDE.md` (Workflow A + B) | **built** | `engine.py` archetypes / bespoke scripts |
| Story (1080x1920) | `CLAUDE.md` | **built** (same pipeline, `SIZES["story"]`) | same |
| Real-photo carousel | `CAROUSEL_PLAYBOOK.md` | **built** | bespoke scripts + `vision.py` |
| Instagram/LinkedIn post *ideas* | `IDEATION.md` | **spec** | n/a — feeds the surfaces above |
| Voice / copy, any surface | `VOICE.md` | **spec** | n/a — feeds every surface |
| LinkedIn text post | `IDEATION.md` §7 | **spec** | none yet (no canvas needed — text only) |
| One-pager / brochure / catalog / report / deck | `BROCHURE_CATALOG.md` | **spec** | would extend `build.py`/`core.py` to new `SIZES` + a PDF assembler |

Reading order for a new task: **this file** → the owning doc for the surface → `VOICE.md` for the
copy → `CLAUDE.md` §7 gate stack for what must pass before it ships.

---

## 3. WHAT'S ACTUALLY BUILT vs. WHAT'S SPEC, IN ONE LIST

Built and running today:
- The poster/story engine, both workflows, the full gate stack (`CLAUDE.md` §7).
- The real-photo carousel pipeline (`CAROUSEL_PLAYBOOK.md`, `vision.py`).
- 44/44 reference recreations (`RECREATION_PROGRESS.md`).

Specified, not encoded — written so a human can use them by hand *today*, and so a future session
knows exactly what to build and in what order if asked to encode them:
- `VOICE.md` — the lane x audience x channel x intent voice resolver.
- `IDEATION.md` — the pillar/post-type idea generator + rotation rule.
- `BROCHURE_CATALOG.md` — the multi-page print/PDF format spec.

**None of the three spec docs should be treated as "the engine already does this."** If a task
needs, say, an automatically-generated week of Instagram briefs, the honest answer today is "here
is the framework to apply by hand" (`IDEATION.md` §5, the brief generator, run manually), not "run
this command" — there is no command yet. Say so plainly rather than quietly hand-writing output
and calling it encoded.

**Grounding pass, 2026-08-26.** The three spec docs above started as first-principles rules; a
real content-ingestion pass (47 AQ/Shikshaq documents, ~105 real photos/designs, plus external
research into comparable content-strategy frameworks) has since grounded most of `VOICE.md` and
part of `IDEATION.md` in actual sourced material — see `AQ_FACTS.md` for the fact bank and
`DECISIONS.md`'s 2026-08-26 entry for what changed. This upgrades the docs from "plausible spec"
to "spec checked against real evidence," but does **not** change their build status — they are
still hand-applied, not encoded. Don't conflate "now grounded in reality" with "now automated."

---

## 4. BUILD ORDER, IF/WHEN ENCODING STARTS

Consolidates the "what encoding requires" sections scattered across the three spec docs into one
dependency-correct sequence, same spirit as `GENERATION_MAP.md`'s existing build order for
archetypes.

1. **Mechanical voice gates** (`VOICE.md` §11.3-5): banned-phrase scan, em-dash/emoji scan,
   number-provenance check. Cheapest, highest-value, zero dependencies on anything else here.
2. **`VOICE_PROFILE` resolver** (`VOICE.md` §11.1): pure function, no text generation, trivially
   testable. Everything downstream needs this.
3. **LinkedIn text posts** (`IDEATION.md` §8.5): cheapest *new surface* to encode — no canvas, no
   Playwright, just the resolver + `IDEATION.md` §7's structure. Good first real output of the
   voice system.
4. **`IdeaLedger` + `next_brief()`** (`IDEATION.md` §8.1-2): needs #2. Should share one ledger file
   with the visual ledger `GENERATION_MAP.md` §[5] already specs — not two separate systems
   tracking "what have we already made."
5. **Brochure `SIZES` + grid reuse** (`BROCHURE_CATALOG.md` §5, first bullet): zero risk, pure
   constant extension of `core.py`/`build.py`. Can happen any time, independent of 1-4.
6. **One-pager end to end, by hand** (`BROCHURE_CATALOG.md` §5): the proof of concept, mirrors how
   Workflow B always starts with one bespoke script before a pattern gets extracted.
7. **PDF assembler + `spread_coherence_check`** (`BROCHURE_CATALOG.md` §5): only after #6 proves
   the single-page path works.

Nothing above is scheduled — this is a dependency graph, not a sprint plan. Pull whichever piece
is actually needed next.

---

## 5. STANDING RULES THIS FILE INHERITS AND DOES NOT RELAX

From `CLAUDE.md` header, unchanged, apply to every surface in §2:
- The recreation-run auto-resume standing rule.
- The companion-art-piece rule (`/canvas-design` alongside every generation run).

From `MEMORY.md`:
- `aqdesignengine` is a **public repo** — no AQ event photos of children in any commit, on any
  surface, including brochure/catalog mockups that might use placeholder imagery.

From `VOICE.md` §1, restated because it's the rule most likely to get lost when a new surface
feels like it deserves an exception: **never guilt-trip, never savior-frame, never fabricate a
number.** Every surface in §2, however formal or however new, is bound by these without exception.

---

## 6. NODE MAP — this is the hub, not a leaf

Every doc below links back here and to its neighbors. Follow any edge; you should never dead-end.

```
                              CLAUDE.md (poster engine manual, §11 repo map)
                                    |
                          CONTENT_SYSTEM.md  ←── you are here, the hub
                          /        |         \
                  VOICE.md   IDEATION.md   BROCHURE_CATALOG.md
                   (spine)    (uses VOICE     (uses VOICE §7 +
                       \       §7 resolver,     grid/craft reuse
                        \      feeds posters/    from build.py/core.py)
                         \     stories/carousels
                          \    /            \
                       CAROUSEL_PLAYBOOK.md   GENERATION_MAP.md
                       (built carousel        (archetype build order;
                        pipeline VOICE/        IDEATION §5a maps post-
                        IDEATION feed into)     types onto its archetypes)
                              \                /
                          TASTE.md ←── ENGINE.md / ENGINE_STATE.md
                       (decision cascade;    (craft constants,
                        VOICE §7's precedence  gate targets — the
                        rule mirrors this)      spine's other half)
                                    |
                              DECISIONS.md
                        (every encoded fix, old and new —
                         VOICE/IDEATION/BROCHURE additions
                         log here going forward, §8 rule)
```

- **Upstream (read before this file):** `CLAUDE.md` — the operating manual this whole system
  extends; §1's "fix the rule, never the output" is the principle every doc here inherits.
- **Downstream (this file points to):** `VOICE.md`, `IDEATION.md`, `BROCHURE_CATALOG.md` — the
  three spec docs it indexes.
- **Sideways (shared machinery):** `TASTE.md` (the decision-cascade `VOICE.md` §7's precedence
  rule is a direct instance of), `GENERATION_MAP.md` (the archetype build-order `IDEATION.md` §5a
  maps post-types onto, and the ledger `IDEATION.md` §8.1 shares rather than duplicates),
  `CAROUSEL_PLAYBOOK.md` (the one surface where voice + ideation already feed a built pipeline —
  read it to see the spine working end to end today).
- **Where fixes land:** `DECISIONS.md` — per `CLAUDE.md` §8, any general fix discovered while using
  VOICE/IDEATION/BROCHURE gets logged there, dated, same as every poster-engine fix. This file
  doesn't get its own decisions log; it shares the one that already exists.
- **Evidence spine, added 2026-08-26:** `AQ_FACTS.md` — the sourced fact/fingerprint bank behind
  `VOICE.md`'s truth ladder and `IDEATION.md` §10, built from a real ingestion pass over 47
  AQ/Shikshaq documents and ~105 photos/designs. Every real number and quote in `VOICE.md` and
  `IDEATION.md` traces back to this file; extend it, don't duplicate it, when new real material
  shows up.
- **Open questions, added 2026-08-26:** `GAPS.md` — the first-class, centrally-tracked version of
  what used to be inline "open questions" sections at the bottom of each spec doc (those sections
  still exist for in-context reading, but `GAPS.md` is now canonical). Adopted from external
  research into how a comparable multi-doc brain system prevents unresolved threads from silently
  dropping between sessions.
