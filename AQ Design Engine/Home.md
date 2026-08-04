# AQ Design Engine — Vault

This vault reorganizes the AQ Poster Engine's documentation (`CLAUDE.md` + `brain/`) into an
atomized, cross-linked note network. It exists to make the engine's design rules easier to
navigate and edit in Obsidian than as a handful of giant source files. Nothing here changes the
engine itself — the source files in the repo remain the single source of truth.

## Manual
The 12-section operating manual (from `CLAUDE.md`): the one principle, the two workflows, the
looking gate, and everything needed to generate or recreate a poster.
→ [[Manual Index]]

## Brain
The reasoning docs: taste, engine state, the visual-review protocol, inspiration teardowns, the
session log, and the full standing-decisions log (split into atomic entries).
→ [[Brain/Decisions/Decisions Index|Decisions Index]] · see also [[Engine]], [[Audit]], [[Inspiration]], and the other individual notes under `Brain/`

## Bug Catalog
Every recurring visual failure class caught during the 44-sample recreation pass, each now
guarded by an encoded rule in `engine/layout.py`.
→ [[Bug Catalog Index]]

## Recreations
The 44 reference-poster recreations ("training" pass) — one note per sample, each with its full
composition description and outcome.
→ [[Recreations Index]]
