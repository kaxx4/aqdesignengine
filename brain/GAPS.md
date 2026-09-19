# GAPS — open questions and unknowns, tracked centrally

Status: first-class open-questions log, adopted 2026-08-26 on the recommendation of an external
research pass (see `DECISIONS.md`'s 2026-08-26 entry) into how a comparable multi-doc "brain"
system prevents open questions from getting silently dropped when a session ends. Before this
file, open questions lived only inline at the bottom of `VOICE.md`, `IDEATION.md`, and
`BROCHURE_CATALOG.md` — easy to lose track of as the brain folder grows. Those inline sections
stay (removing them would break in-context reading), but this file is now the canonical, scannable
list. When a question resolves, move it to "RESOLVED" with the answer and the date, don't delete
it — the resolution is itself useful history.

Format per entry: **[status]** question — source doc — why it matters.

---

## OPEN

1. **[open]** Does AQ want a shared idea backlog (a running list of "next 20 post ideas" a human
   can glance at and reorder), or should the eventual `next_brief()` always generate on demand,
   one at a time? — `IDEATION.md` §9.3 — changes whether the eventual ledger needs a queue file
   (like `brain/RECREATION_QUEUE.json`) or stays a pure function.
2. **[open]** Who approves content before it actually publishes? `VOICE.md`/`IDEATION.md` generate
   briefs and copy; neither says anything about the human review step before something posts. —
   `IDEATION.md` §9.2 — worth a one-line standing rule once decided, the way `CLAUDE.md`'s header
   carries the recreation-run standing rule.
3. **[open]** LinkedIn, WhatsApp, and email have zero precedent in the ingested corpus — every
   channel rule for those three in `VOICE.md` §5 is invented, not derived. If AQ already has real
   copy on those surfaces somewhere not yet ingested, it should drive the rules instead. —
   `VOICE.md` §12.4
4. **[open]** Sentence case on LinkedIn — allowed as a legibility concession in `VOICE.md` §5. No
   real precedent found either way. — `VOICE.md` §12.6
5. **[open]** Shikshaq now has a confirmed, distinct visual system (black bg, orange/blue neon
   accents, chat-bubble mockup format — see `AQ_FACTS.md` §10) that `engine/core.py` does not
   encode at all — the poster engine currently has exactly one brand system (AQUATERRA's
   cream/ink/7-accent tokens). Does Shikshaq content need its own `core.py`-equivalent token set,
   or does it stay a manual/bespoke treatment indefinitely? This is a real, shipped gap, not
   speculative scope — `AQ_FACTS.md` §10, `CONTENT_SYSTEM.md` §2.
6. **[open]** ROOTS (the apparel venture, ~10% of org revenue, "Made to give back") has real
   product photography in the ingested corpus (kraft-paper tags, flat-lay merchandise shots) but
   no confirmed brand-voice register of its own yet — is it voiced like general AQUATERRA content,
   or does "apparel that's more of a voice rather than fashion" imply its own register? —
   `AQ_FACTS.md` §11.
7. **[open]** The 100% "100% profit → drives" line already used in `generate.py`'s existing
   `roots`/`community` JOBS content wasn't independently verified against a source document in
   this ingestion pass — worth confirming against a real ROOTS financial figure next time that
   archetype is touched, rather than assuming the existing copy is exact. — `AQ_FACTS.md` §11.
8. **[open]** Cadence and format-mix targets are now real (`AQ_FACTS.md` §12: 3-5 feed posts/week,
   60% carousel / 25% reel / 15% static, 80% proof / 20% philosophy) but nothing enforces them —
   `IDEATION.md`'s rotation rule (§4) checks pillar/post-type/lane repetition; it does not yet
   check format-mix or weekly volume against these real targets. Worth folding in if/when
   `IdeaLedger` gets built (`IDEATION.md` §8.1).
9. **[open]** No cross-post "cannibalization" check exists — `IDEATION.md`'s rotation rule (§4)
   prevents the same hook/format repeating, but nothing checks whether a *new* topic overlaps an
   *existing* one enough to compete with it (a pattern surfaced by external research into a
   comparable content-ops system — see `DECISIONS.md` 2026-08-26). Distinct problem from
   repetition; not yet addressed anywhere in this brain.
10. **[open]** No "refresh due" mechanism exists for facts. `AQ_FACTS.md` states a refresh
    discipline (12 months from source date) but nothing checks or flags it automatically — a
    number could get pulled from that file two years stale with no warning. Same external-research
    origin as #9.
11. **[open]** Which brochure/catalog/report format is actually wanted first, and is it print or
    PDF-only? — `BROCHURE_CATALOG.md` §8.1-2 — changes whether the print-safety caveats (bleed,
    CMYK, fold lines) are live risks or irrelevant, and which format should be the proof-of-concept.
12. **[open]** Does the program catalog need to stay in sync with a real, changing list of AQ's
    active lanes/ventures? Lanes have already changed once in this session (ROOTS and Shikshaq
    surfaced as distinct from the original guess) — a static catalog would drift the same way the
    old copy banks did. — `BROCHURE_CATALOG.md` §8.3.

## RESOLVED

- ~~Is there a real donor/individual-giving program to model a "donors" audience on?~~ **Resolved
  2026-08-26, NO.** `AquaTerra_Revenue_Streams.md` states explicitly: 0% of revenue from
  donations, ~90% from fundraising events, ~10% from startups (ROOTS). "AquaTerra does not raise
  money separately from its activities." The real institutional-funding channel is corporate CSR
  partnership (see next). `VOICE.md` §4's old "donors" row has been superseded accordingly.
- ~~Which lane taxonomy is real — the six drive-types in `generate.py` or the six departments in
  `RECREATION_AUDIT.md`?~~ **Resolved 2026-08-26, neither fully — real facts sourced instead.**
  `AQ_FACTS.md` §1-11 is now the sourced lane/fact bank; it surfaces two lanes neither prior list
  had cleanly separated: ROOTS (a revenue venture, not welfare "clothes/kits") and Shikshaq (a
  fully distinct sub-brand, not an education sub-lane).
- ~~Is Shikshaq a separate voice or a sub-lane of education?~~ **Resolved 2026-08-26, separate.**
  Confirmed on three grounds in `AQ_FACTS.md` §10: a distinct audience (tutors/teachers) the base
  voice system never modeled, a distinct shipped visual system, and real published headline voice
  sharper/funnier than the AQUATERRA-proper default. (Its own visual-system encoding remains open
  — see #5 above.)
- ~~Does AQ have a real corporate/CSR register to ground `VOICE.md`'s invented corporate audience
  row?~~ **Resolved 2026-08-26, yes** — the real Emami Foundation CSR proposal
  (`AquaTerra_Emami_CSR_Proposal_Revised.docx`), which validates the invented register almost
  exactly (formal, zero snark, compliance/metrics-forward) rather than contradicting it.
- ~~What's a real posting cadence / format mix?~~ **Resolved 2026-08-26.** AQ's own 2026 Virality
  Plan states it directly: 3-5 feed posts/week minimum, 60% carousels / 25% reels / 15% static,
  80% proof / 20% philosophy content mix. See `AQ_FACTS.md` §12.

## See also
`CONTENT_SYSTEM.md` §6 (node map) · `AQ_FACTS.md` (the fact bank several resolutions above cite) ·
`VOICE.md` §12 and `IDEATION.md` §9 (the inline versions this file consolidates) ·
`BROCHURE_CATALOG.md` §8 (its open questions, not yet touched by this ingestion pass).
