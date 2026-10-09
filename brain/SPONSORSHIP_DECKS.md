# Sponsorship + stalls decks and brochures (started 2026-10-09)

Brief (user): rebuild the Disco Diwali sponsorship deck from zero as a cohesive system, then derive **four decks** (sponsors cold, sponsors warm, stalls cold, stalls warm) and **two printable A4 brochures** (bifold / trifold). Same visual DNA as the original deck but rounded frames, tidier, more photos, rhythm. NOT TerraThon; TerraThon/Diwali die-cut stickers allowed as sparing accents.

## Rulings so far (user)
- Language: the *softer, cleaner* AQ variant (cream, paper cards on a keyline + soft shadow, 28px photo frames).
- Cold vs warm: ONE slide library. Warm drops the "who is AQ" intro, adds a "what you got last time" recap, re-orders and re-tones. One generic recap for returning partners.
- Output: PDF. Build order: sponsors cold first (master), then derive the rest.
- Numbers: 5K+ followers; projects shown as "112 in 2025 / 500+ since 2021"; age pie = Classes 9-10, 11-12, college, volunteer network (1.5K+ vs 1,810 respondents, percentages only; footnoted as approximate); "Our Numbers" bar chart replaced by an exclusivity funnel (2,500+ asked, 500 entered, 419 paid + the four ticket-price phases); school map rebuilt as vector with a numbered legend.
- Stalls pricing/terms: shared later with interested stalls, not in the deck.

## Build
- `engine/deckkit.py`: scaffold, tokens, 1 icon set, donut/funnel/hbars/map, `logo_uri` (trims margins), photo frames.
- `scratchpad/gen_sponsor_deck.py`: the sponsors-cold master (31 slides) -> `out/decks/sponsors_cold/` (git-ignored).
- `scratchpad/deck_assets.py` (extract rasters + vector logos from the source PDF), `deck_map_trace.py` (vectorise the school map), `deck_sheet.py` (contact sheets).
- PRIVATE, git-ignored (repo is PUBLIC; assets include identifiable school children, third-party logos, a named contact): `engine/assets/sponsorship/`, `training_samples/sponsorship_deck/`, `scratchpad/sponsorship_private/` (map.json, facts.json), `out/decks/`.
- Container needs `pip install playwright==1.56.0` (matches the pre-installed chromium-1194) and `opencv-python-headless` for the map trace.

## Source facts corrected in the rebuild
- Event cards re-read at full resolution (small-text reads were wrong): Starry Night Dec 2024 550+ / Rs3L; Disco Diwali Oct 2024 350+ / Rs1.7L; Paradox 1000+ / Rs8.9L; Punjabi Night Jun 2025 400+ / Rs2.2L; Starry Night 2.0 Dec 2025 550+ / Rs6.7L; Summer Sunset Jun 2026 500+ / funds blank in source.
- Run of show re-sorted chronologically (source listed 5:30 PM before 4:00 PM).
- Ticket phases 136+132+110+41 = 419 paid; 500 entered leaves 81 unexplained.

## Persona stress test (6 reviewers, sonnet; scores out of 10, v1 deck)
Cohesion 8/10 from all six. Clarity of ask 3-4/10 from all buyers: **no prices, no venue, no firm date**. Recurring findings:
1. Review-count deliverables (Google/Zomato/Swiggy) read as bought reviews; policy + legal risk (legal, cafe, media, finance all flag it; same finding as the Rever panel).
2. Attendance does not reconcile: 600+ (cover/flagship) vs 500 entered / 419 paid vs 350+ in 2024.
3. Pie mixes survey respondents with the volunteer network (legal, finance, media, Gen Z all flag it).
4. "all days / five days / all 15 events" vs a single-evening event.
5. 3.5K+ kids reached (vision) vs 4000+ (impact) in the source.
6. Registration: `AAFTT2300ME20251` is labelled Darpan in the source but its format matches an 80G/12A approval number. Relabelled "Registration no." pending the user.
7. Photos of children in school uniform in a commercial pitch; no consent statement.
8. Testimonials/logos unattributed; "2000+ student database" = minors' data.
9. Offer comes too late (fixed: slide 3 "the offer in one page"); tier structure shows three overlapping ladders (flowchart implies a hierarchy that does not exist).

## Open items needing the user (nothing invented)
Price per tier + slots left + payment deadline; venue and firm date; share of proceeds to charity; one attendance definition; review-count wording; single-night vs multi-day wording; 3.5K vs 4000+ kids; real 80G/12A/Darpan numbers; consent for child photos; named, permissioned testimonials; Summer Sunset funds; a second (adult) contact.
