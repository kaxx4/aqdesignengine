# BROCHURES, CATALOGS & PDFs — the multi-page, print-adjacent format spec

Status: **specification, not yet encoded.** Same posture as `VOICE.md` and `IDEATION.md`. Nothing
below runs. The engine today (`engine/build.py`, `engine/core.py`) renders exactly one canvas at a
time via Playwright, to one of three fixed pixel sizes (`core.SIZES`: feed/story/square). Every
format in this doc is **multi-page**, which the current pipeline has never done — this is a real
architecture extension, not a content-only one, so §5 is longer than the equivalent section in
the other two docs.

---

## 1. WHY THIS IS A DIFFERENT PROBLEM FROM A POSTER

A poster is one composition, one looking-gate pass, one file. A brochure is **N compositions that
must read as one system** — same margins, same grid, same type scale, same accent logic, page
after page — plus a cover and a back that do different jobs than the interior pages. The single
hardest new failure mode this format introduces, that a poster literally cannot have:

> **Page 4 looking like it came from a different piece than page 1.**

Everything in §3-4 exists to prevent that one failure, the same way the whole gate stack in
`CLAUDE.md` §7 exists to prevent "this one element is wrong" — just promoted one level, from
element-consistency-within-a-page to page-consistency-within-a-document.

---

## 2. THE FORMATS

| Format | Pages | Primary audience (VOICE.md §4) | Job |
|---|---|---|---|
| **one-pager** | 1 (front only, or front+back) | corporate/CSR, schools/parents, government | leave-behind after a meeting; the "what is AQ" answer in one look |
| **tri-fold brochure** | 1 sheet, 3 panels each side (6 panels total) | general followers, volunteers, schools | physical handout at events, recruitment drives, stalls |
| **program catalog** | 8-16 | donors, corporate/CSR, partners | one spread per lane (`VOICE.md` §3) — the full menu of what AQ runs |
| **annual / impact report** | 12-24 | donors, corporate/CSR, government | the year in counted numbers, per the truth ladder (`VOICE.md` §2) |
| **partnership deck (PDF)** | 6-10 | corporate/CSR specifically | the pitch: what AQ offers, what documented delivery looks like |

All five share one page-grid system (§3) and one page-role vocabulary (§4). They differ only in
page count and which page roles they use — a one-pager is a catalog with exactly a cover-role page
and nothing else; a tri-fold is six panels that map to cover/interior/back roles folded physically.

---

## 3. THE PAGE-GRID SYSTEM (the thing that stops page drift)

**Canvas sizes to add to `core.SIZES`** (print-safe at 300dpi, sRGB — see §6 caveat):

```python
SIZES = {
    "feed": (1080,1350), "story": (1080,1920), "square": (1080,1080),   # existing
    "a4_portrait":  (2480, 3508),   # brochure interior pages, one-pager, catalog
    "a4_landscape": (3508, 2480),   # tri-fold panel sheet (before fold-cutting into 3)
    "letter_portrait": (2550, 3300),  # US-audience variant, same role as a4_portrait
}
```

**One shared grid, every page, every format:**
- Margin `M = 120px` at these sizes (proportionally larger than the poster's `M = 64` at 1080px,
  because print is read closer and a 64px margin at 2480px reads as edge-to-edge).
- 12-column grid, same `colspan()` logic `build.py` already has (`_colw`, `colspan`), just
  recomputed at the new `W`. **Reuse the function, don't reimplement it** — this is exactly the
  kind of primitive `GENERATION_MAP.md` §[Build order #2] calls out as "build once, compose N
  times."
- Type scale is the poster's `RULES["fs"]` (`engine.py`) scaled by the same ratio as the canvas
  (2480/1080 ≈ 2.3x), not re-chosen per page. A headline that's 140px on a poster is ~320px on an
  a4_portrait page. **Never eyeball a print type scale separately from the poster's — that IS
  the page-drift failure mode from §1, just inside a single document instead of across two.**
- Accent rotation, doodle vocabulary, chip/shadow/outline craft constants: **identical to
  `CLAUDE.md` §9 and §7's `RULES`, unchanged.** A brochure is not a chance to invent new brand
  language; it's the same brand at a different size.

**Per-document constants, fixed once at the top of the build script and used on every page:**
- one hero accent (not re-picked per page — `VOICE.md`'s "supporting palette rotates with the
  hero" rule, from `engine.py`'s `A = lambda off: ...` pattern, applies at the *document* level
  here, not per-page)
- one type treatment (per `TASTE.md`'s decision cascade — pick one, commit for the whole document)
- one margin, one column count, one baseline grid

---

## 4. PAGE ROLES (every page in every format is one of these five)

### COVER
- Logo (real wordmark, `CLAUDE.md` §9 rule: bare, never white-inverted, pill only on dark/photo).
- One hero: a real AQ photo (`core.PHOTOS` or a supplied one) or one large illustrated doodle/hero
  shape, never both competing.
- One headline, ≤6 words, `VOICE.md` register resolved for the document's audience.
- One fingerprint line if the format is stats-led (impact report, catalog) — a single real number,
  not a wall of them; the wall belongs on interior pages.
- **No CTA on the cover.** The cover's only job is to earn the next page.

### INTERIOR — CONTENT SPREAD
- The workhorse page. One clear subject per spread (one lane, one milestone, one story).
- Grid: 2-column (text + photo/doodle) or 3-column (three short items, e.g. three lanes per
  spread in a catalog) — pick per spread based on the content, not forced uniform, but **the
  margin and baseline never move.**
- Every lane entry that appears in a catalog spread follows `VOICE.md` §8 exactly: lane name
  (display type), one doodle, one proof detail, one fingerprint number, done. This section of
  this doc is close to a direct restatement of that table on purpose — the catalog's whole
  interior is that table, laid out.

### INTERIOR — STATS SPREAD
- For impact reports specifically. A grid of `number_hero`-style stat blocks (reuse the poster
  archetype's number treatment, don't invent a new one), each with a truth-ladder tier attached
  (`VOICE.md` §2) — and the tier's qualifier travels with the number onto the page. "534 drives"
  on a stats spread needs "in 2025" in the same type block if that's the scope, at whatever size
  keeps it legible but present. **A stats spread with an unqualified scoped number is the print
  equivalent of the "day 1/8" fabrication failure** — it's not literally invented, but it will be
  read as a bigger claim than it is, which is the same harm the truth ladder exists to prevent.

### INTERIOR — PEOPLE SPREAD
- Volunteer/doctor/partner spotlights, per `VOICE.md` §6's gratitude intent: name and role, never
  abstraction, first names/handles only.

### BACK
- Contact: handle, one real channel (not all of them — pick the one right for the audience:
  a corporate deck's back page has an email/contact person, not an Instagram handle).
- One soft CTA (`VOICE.md` §1.12 — never a pressure line, doubly true in a leave-behind document
  someone will read alone, with no algorithm forcing urgency).
- Logo again, small.

---

## 5. THE RENDER PIPELINE EXTENSION NEEDED

This is genuinely new engineering, scoped here for sign-off before anyone builds it, per
`CLAUDE.md` §8's "locate the right layer" step.

1. **Per-page render is unchanged**: `build.page(W, H, bg, inner, grain=...)` then
   `build.render(html, out_png, W, H, elements=..., color_pairs=..., page_bg=...)` — same call
   shape as a poster, just at the new `SIZES` entries. Nothing here is new.
2. **New: a document assembler.** N page PNGs → one PDF. Two real options:
   - `img2pdf` (new dependency, ~one function, lossless PNG→PDF embed, no re-encoding, no CMYK
     conversion attempted) — **recommended**, matches the engine's existing "minimal dependencies,
     deterministic output" posture (`requirements.txt` today: playwright, Pillow, numpy, scipy).
   - Playwright's own `page.pdf()` — renders HTML directly to PDF per page, then merge. More
     moving parts (would need a PDF-merge dependency too, e.g. `pypdf`) for no real benefit here
     since every page is already a flat raster composition, not text that needs to reflow.
   - **Do not reach for `reportlab` or a full PDF-authoring library.** The engine's whole model is
     "render a styled HTML/CSS page to a raster, gate it, ship it" — a PDF-authoring library would
     mean maintaining layout logic in two different systems (HTML/CSS for posters, a PDF API for
     documents) for the same brand. `img2pdf` keeps exactly one layout system.
3. **New: a document-level gate**, run after all pages pass their individual `preflight()`:
   - `spread_coherence_check(pages)` — the margin, column x-positions, and type-scale ratio must
     match across every page. This is the direct encoding of §1's "page 4 looks like a different
     piece" failure. Zero-false-positive by construction (it's comparing numbers the build script
     already computed once and reused, per §3) — auto-gateable like `css_var_check`.
   - `qualifier_travel_check(page_text, brief)` — extends the eventual `number_provenance_check`
     from `VOICE.md` §11.5: for any *scoped*-tier number, confirm its qualifier phrase appears in
     the same page's text. This is the print-specific instance of that same gate.
4. **New: a page-role validator** — every page in the document must map to one of §4's five roles;
   a page with no assigned role is the print equivalent of an archetype-less poster and should
   fail the same way `dominance_check` flags "no element reaches hero scale" (`layout.py`).

**Build order, if this gets greenlit:** the `SIZES` entries + reused grid math (§3) first (zero
risk, pure extension of existing constants) → single one-pager end to end, by hand, as the proof
of concept (mirrors how Workflow B always starts with one bespoke script before any pattern gets
extracted) → `img2pdf` assembler → `spread_coherence_check` → then the catalog/report formats,
which are just more pages of the same primitives.

---

## 6. PRINT-SAFETY CAVEATS (read before anyone actually prints one of these)

- **Color: this pipeline is sRGB, not CMYK.** `core.py`'s hex tokens (`--pink:#FF4D8C` etc.) are
  screen colors. A digital PDF (viewed on-screen, or run through a modern inkjet office printer)
  will look right. A **commercial offset print run** will shift saturated accents, especially
  `--tomato` and `--pink` — sRGB-to-CMYK conversion is not something this engine attempts, and
  claiming print-accuracy without it would be a real problem the first time someone runs 500
  brochures through a print shop. If AQ needs true offset-print fidelity, that's a separate,
  scoped piece of work (a CMYK-safe sub-palette), not assumed here.
- **No bleed/trim marks.** These pages render edge-to-edge at the stated pixel size with no bleed
  margin. Fine for a home/office printer or a digital PDF. A commercial print shop will ask for
  3mm bleed + crop marks, which is a `SIZES` variant to add later (larger canvas, content inset by
  the bleed amount), not something to bolt on ad hoc per job.
- **Fold lines are not drawn.** The tri-fold's 3-panel layout needs to know exactly where the
  physical folds fall (a standard tri-fold is NOT three equal panels — the inner fold panel is
  slightly narrower so it tucks cleanly). This is a real, specific measurement to get from
  whatever print vendor is used, not something to guess at build time.
- **These caveats are why this doc is a spec and not a build.** A brochure that looks right on
  screen and wrong in hand is worse than not building it, per `CLAUDE.md` §1's own principle:
  a flaw caught by eye that isn't caught here yet is a rule not yet written.

---

## 7. HOW THIS CONNECTS TO IDEATION AND VOICE

- A catalog's interior spreads are `VOICE.md` §8 (fingerprint per lane) directly laid out —
  no new copy rules, just a new canvas.
- An impact report's stats spreads are `intent: recap/report` (`VOICE.md` §6) at whatever
  `audience` the report targets, run once per stat instead of once per poster.
- A partnership deck is the **corporate/CSR** audience row (`VOICE.md` §4) end to end — register
  ceiling 1, no snark, lead with documentation. It's the single closest thing in this whole content
  system to a sales document, and the closest to the sector boilerplate in `VOICE.md` §9 needing
  active resistance ("we deliver measurable impact" is exactly the kind of line this format will
  be tempted to reach for and exactly what §9 bans).
- `IDEATION.md`'s PROOF and TRANSPARENCY pillars are naturally the ones that graduate from a
  single Instagram post into an annual-report page once there's enough of them — a print document
  is often just several ideation-doc posts, laid out together with a shared grid, which is why
  building §3's grid system reuses the poster's primitives rather than a parallel set.

---

## 8. OPEN QUESTIONS

1. **Does AQ actually print these, or are they PDF-only (email attachments, WhatsApp shares,
   downloadable from a link)?** Changes whether §6's bleed/CMYK caveats are live risks or
   irrelevant. If PDF-only, this is a much smaller build (no fold-line, no bleed, no CMYK concern
   at all) and should be scoped down accordingly before §5's build order starts.
2. **Which format is actually wanted first?** The one-pager is the cheapest to prove the whole
   pipeline on (§5's build-order already assumes this) but if the real near-term need is the
   annual report or the partnership deck, the proof-of-concept should be that format instead —
   no sense proving the pipeline on a format nobody asked for.
3. **Does the program catalog need to be kept in sync with a real, changing list of AQ's active
   lanes?** If lanes get added/retired over time, the catalog either needs a single source of
   truth to build from (ideally `VOICE.md` §3's lane table itself) or it will drift the same way
   the copy banks did (`ENGINE_STATE.md`'s repeat-wording finding) — structurally, not just
   tonally.

---

## 9. SEE ALSO — this file's place in the tree

- **Hub:** `CONTENT_SYSTEM.md` — this file is one of the three docs it indexes; §4 there places
  the `SIZES`/grid extension and the one-pager proof-of-concept as steps 5-7 of the shared build
  order.
- **Reuses, never reinvents:** `engine/core.py` (tokens, fonts, `LOGO`, `PHOTOS`) and
  `engine/build.py` (`colspan`/`_colw`, `page()`, `render()`) — §3 above is explicit that the grid
  math and type scale are the poster's, recomputed at a new `W`, not a parallel system. Same
  reuse posture as `CAROUSEL_PLAYBOOK.md`'s helper block for carousels.
- **Gate stack lineage:** §5's `spread_coherence_check` and `qualifier_travel_check` are proposed
  as siblings to the existing `CLAUDE.md` §7a checks (`css_var_check`, `same_as_bg_scan`) — same
  "zero false positive → auto-gate" bar `CLAUDE.md` §8.4 sets before anything joins `preflight()`.
- **Copy for every spread** resolves through `VOICE.md` §7, same as any other surface; §4's
  per-lane catalog entries are `VOICE.md` §8's fingerprint table, laid out on paper instead of
  a single poster.
- **Fixes discovered while using this file** log in `DECISIONS.md`, per `CLAUDE.md` §8.
