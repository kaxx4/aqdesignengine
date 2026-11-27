---
name: shikshaq-design
description: Design anything for SHIKSHAQ (shikshaq.in, the Kolkata tuition-teacher directory and past-paper library) in its own design language: posters, Instagram feed or story art, landing pages, site sections and screens, carousels, slides. Use whenever the user's ask names Shikshaq or Shikshak in any spelling, or says to design for the tuition-teacher or past-papers site. This is NOT the AQ brand; AQ's palette, fonts, doodles and craft layer must not be used. Routes to engine/shikshaq.py, brain/SHIKSHAQ.md and the measured gate.
license: Internal AQUATERRA tool. The Shikshaq wordmark, fonts and source snapshots are vendored from the Shikshaq repository for use on Shikshaq work.
---

# Shikshaq design

**Shikshaq is a second brand on the AQ rails, not AQ.** Warm bone ground, a heavy display face in mixed weights, two modes
(teachers = orange, papers = indigo), a tinted palette per subject, depth as a hairline ring. None of AQ's pink, doodles,
thick outlines or hard offset shadows apply. Using them is the failure this skill exists to prevent.

## Do this, in order

1. Read `brain/SHIKSHAQ.md` in full. It is the operator doc (the route table, tokens, layout grammar, page archetypes,
   the gate, deviations and open decisions). It changes as rules are encoded; do not work from memory.
2. Pick the path from its section 0:
   - page / screen / section: `engine/shikshaq.py` section builders, start from `scratchpad/shik_landing_example.py`
   - poster / story / square: `sk.poster([...])`, start from `scratchpad/shik_poster_example.py`, or
     `python engine/shikshaq.py scaffold poster|page <name>` (a starter that already passes the gate)
   - the weekly three-post Instagram plan: `addons/shikshaq/` (Node)
3. Use `sk.FACTS` for every number. If a figure is missing or older than 14 days, read the live site (or ask) and update
   `FACTS`; never write a plausible number. Check `FACTS.known_inconsistencies` first.
4. Run the copy through `sk.copy_gate`, render through `sk.render` (the measured gate), fix what it names.
5. **Look at the PNG** (the Read tool shows it). The numeric gate passed visibly wrong posters during the build.
6. If the flaw is a general class, encode it as a rule in `engine/shikshaq.py` plus an assertion in
   `scratchpad/test_shikshaq.py` (80 assertions), and note it in `brain/SHIKSHAQ.md` section 10. Never patch one output.

## Hard rules (each is checked, not hoped for)

Ink, not white, on orange. Subject colour only from `sk.subject_palette()` (badge text is MEASURED). Fill separates panels,
30px radius, gap 0. At most one orange/indigo seam, never the same hue twice. No dashes in copy. Every number traces to a
fact. 44px tap targets, 4.5:1 text contrast measured on the real surface, no horizontal overflow, Archivo and Geist only.
Heavy orange display type on bone is allowed ONLY when declared (`data-accent-display`) and is reported every time (open
decision D1 in `brain/SHIKSHAQ.md`).

## Do not

Route Shikshaq through `engine.generate`, `core.ACCENTS`, `core.LOGO`, `doodles.py`, `shapes.sticker` or `build.page`. Recolour
the logo (it goes white on dark only). Put a sticker on a teacher's face, tilt a chip, or put texture or a thick outline inside a
grid of comparable items. Scrape shikshaq.in past its bot checkpoint (read the owner's test deployment through the connected
Vercel account, or ask).

The AQ repo's standing companion-art rule (`CLAUDE.md`) still binds the session when engine output is produced.
