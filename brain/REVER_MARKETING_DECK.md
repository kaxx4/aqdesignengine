# REVER x Disco Diwali 2026: the marketing deck (built 2026-10-13, formal revision same day)

The companion to the 29-slide partnership proposal. Audience: Rever (cafe, our Exclusive Food and Location Partner). Job: show Rever exactly how AquaTerra will market it, before, on and after the event. 14 slides, 1920x1080, PDF.

Run: `python scratchpad/rever_marketing_assets.py` once (crops), then `PYTHONIOENCODING=utf-8 python scratchpad/gen_rever_marketing_deck.py [slide numbers]` -> `out/decks/rever_marketing/` (PNGs + `rever_marketing_deck.pdf`). Needs `pip install playwright==1.56.0`. Every number lives in the `FACTS` dict at the top of the deck script. Edit, rerun.

## Rulings (user, 2026-10-13)
- "Forever" was a typo for Rever. Audience is Rever, TerraThon branding (so it re-uses the proposal deck's system: black ground, shuriken, orchid-bordered slabs, StretchPro / Sigmar One, die-cut stickers).
- Channels: Instagram (reels, posts, stories, collabs; follows, reach, views, shares, likes), WhatsApp (community, broadcasts, school outreach), 18+ schools.
- No prices slide. Contact: Pratyaksh Singhania.
- Content plan, verbatim from the user: before (location drop post, sponsor mention post, blueprint post, location showcase reel, menu post, fun menu reels, and many more), on the day (decor going up reel, registration started and a full run through the location, fun reels in general), after (decor dump, favourite menu item reel, location reviews reel, thank-you post, podcast with the owner).
- Output: PDF from a script, not an editable file.

## Round 2 (user, 2026-10-13)
- **Formal register.** Applied once in the override block at the top of `gen_rever_marketing_deck.py`, not per slide: no tilted cards, 6px keylines and 20px corners (was 10px and 34px), NeutralFace only (the StretchPro numerals and Sigmar One sub-lines are gone), no stickers inside cards (they stay on the cover, the closing slide's disco ball and the shuriken), headlines as plain statements, square-cornered pills.
- **"And many more"** now closes the before AND the on-the-day plans.
- **Approval line**, in the user's words: "every content plan will be approved by Rever first before being shot". It is a pill on all three content-plan slides, a requirement and its own pill on slide 13, a step on the calendar and on the closing slide.
- **Proof-of-reach screenshots: built conditionally, not shown.** Neither source deck contains an Instagram Insights screenshot (all 65 pages read), so none can be cut from them, and one must never be mocked up (real-assets-only rule). Drop real screenshots into `engine/assets/rever_marketing/proof/` (or set `REVER_PROOF_DIR`; up to 3, file-name order), edit `proof_captions` and `proof_note` in `FACTS`, and rerun: a "Proof of reach" slide appears after the reach slide and the deck becomes 15 slides.
- Source line on the reach slide reads "Figures supplied by Team AquaTerra", because I cannot say where 1.11M+ originated.

## Slides
1 cover · 2 plan at a glance (Instagram / WhatsApp / schools) · 3 who sees it · 4 Instagram formats + what we track · 5 reach numbers (6 proof of reach, only with real screenshots) · 6 WhatsApp · 7 the 18+ school network · 8 photo break · 9 calendar (sign-off to the week after) · 10 before · 11 on the day · 12 after · 13 what we need from Rever · 14 next steps and contact.

## Where the two source decks disagreed, and what this deck uses
| Figure | Sponsors cold | Rever deck | Used here |
|---|---|---|---|
| Disco Diwali 2025 raised | Rs 4.5L+ | Rs 4.3 lakh | not shown (no funds slide) |
| Student volunteers | 1.5K+ | 1,800+ | not shown |
| Schools | 18 | 25+ | **18+** (user's words) |
| WhatsApp | 3,162 across groups | 1,800+ community | **1,800+** (what Rever has already seen) |
| Impressions | 5M+ lifetime | 1.11M+ last few events | **1.11M+** |
| Instagram | 5K+ followers, 4.3L views / 30 days, 21.7K and 9.3K post views | not stated | all from the cold deck |
Open: the two decks still contradict each other on funds, volunteers, schools and WhatsApp. Pick one source of truth before either goes to a third party.

## Adaptations and judgement calls (CLAUDE.md sec 2 rule 4)
- "spam" (WhatsApp) read as "broadcasts".
- No Rever food or venue photos exist in the repo and food imagery may not be invented, so the menu items and food are stickers.
- Photos: Disco Diwali 2025 images from the repo plus crops cut from the two PDFs by `rever_marketing_assets.py`. The PDFs are flat (one JPEG per page, no embedded photos), so "extraction" means page rasters plus crops. Output is git-ignored (identifiable minors, partner logos).
- "Reach and views summary" and "assets handover" on the after slides come from the proposal deck, not the user's list.
- Slide 13 ("what we need") is inferred from the plan: shoot access, the menu and Rever's handle, approvals, a contact and the owner's time for the podcast. Confirm.
- Slide 3 age band "16-19" and "how they find things" are carried over from the proposal deck.
- The 2025 photo on slide 8 and the 300 to 350 guest cap are from the proposal deck (cap ruled by the user 2026-10-08).

## Gate notes
Static gate CLEAN on all 14 slides. Round 2 renders printed no layout issues. Every slide was read as an image after its last change, except that slides 9 to 12 were read before two kicker-text-only edits. Every slide was read as a PNG after its last change.

## New files
`scratchpad/gen_rever_marketing_deck.py`, `scratchpad/rever_marketing_assets.py`, `scratchpad/rever_marketing_stickers.py` (six new die-cut stickers: mic, chat, school, eye, plane, follow; no text, no third-party logos).
