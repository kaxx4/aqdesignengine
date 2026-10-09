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

## Round-4 rulings (user, 2026-10-09)
- Review-count deliverables: KEEP AS WRITTEN (user's call; the legal/policy risk is recorded above and was not acted on).
- Event framing: one night. 'all days / five days / all events / all event locations' rewritten to 'on the night' / 'at the venue'.
- Exclusivity funnel REMOVED. Replaced by slide 17 "Numbers, by touchpoint" (Instagram 5K+ followers, 4.3L views/30d, 21.7K and 9.3K post views, WhatsApp 3,162 members, 2000+ student database, 18 schools, 5M+ impressions). All figures from the source deck; the post-view numbers come from the poster screenshots.
- Age chart: a true PIE of the audience demographic (Class 9-10 29%, 11-12 45%, college 26%; sums to 100). Volunteer network (1.5K+) is a separate stat tile, NOT a slice. This reverses the earlier 4-slice choice after the user said "i basically want a pie chart of the demographic"; flagged for confirmation.
- Kids reached unified to 4000+ (source had 3.5K+ and 4000+). Flagged.

## Haiku persona panel on v2 (8 reviewers, 2026-10-09; run per the user's "remember to run the haiku persona test"; re-run on every derived deck and brochure)
Roles: founder, finance head, legal/risk, Gen Z intern, marketing manager, brand director, restaurant GM (stall view), events buyer. Cohesion 7-8/10 from all; clarity of ask 3-4/10 from all; 6 of 8 would not proceed as drafted.
Agreed (7-8 of 8): no price/slots/deadline; no venue and a tentative date; attendance story (600+ expected vs 350+ in the 2024 edition vs "thousands" on two slides); review-count deliverables; 2000+ student database = minors' data; child photos without a consent line; unattributed quotes and logos (Red Bull, Raymond, POLICE, a Tipco stall shown beside a Hydration slot).
New from this panel: "every net rupee" / "all proceeds" / "raised" are three bases and Rs22.5L+ is gross; 80G is a donation tax benefit while sponsorship is a GST invoice, and the deck shows both; tier names drift (Media sponsor vs Media partner; Cafe sponsor vs Cafe partner) and the flowchart implies a hierarchy no slide states; "5M+ impressions" is undated and unit-mismatched against 4.3L views/30 days; Classes 6-8 are in the target market but absent from the age data; 1.5K volunteers read as audience; entity named "NGO" on one slide and "welfare charitable trust" on another.
Fixed from the panel: "2.5T tons" typo; poster white-strip crops; Paradox card year (I had written 2025 with no source; now "Paradox 3.0"); cover date chip now says tentative.
Judged inaccurate or already handled: slide-number slips by two reviewers; "text at 12px" (contact-sheet downscale, real size is 24-27px).

## Round-5 changes (user, 2026-10-09): "very visual, prove it is recurring, more splash of colour"
Source of the idea: the Rever deck was won on full-slide pictures that showed this is a recurring series. Applied: deckkit tone grounds (`slide(tone="green|lemon|blue")`); 36 slides now (was 30). New recurrence run after the proof slide: 11 "Not a one-off" (green, all six posters), 12 "Disco Diwali, again" (lemon: 2024 poster, 2025 photo, 2026 you-are-here), 13 "Starry Night, twice" (blue: 550+ both years, Rs3L to Rs6.7L), 14 Summer Sunset photos (June 2026, from engine/assets/img/events/summer-aq-turns-five), 15 Disco Diwali 2025 photos (clapperboard reads 22/10/25), 16 TerraThon sports photos (captions inferred from the throwback folder).
Also: map replaced by a visual community overview (18 school chips + 3 photos); Cafe partner, Food partner and the Cafe category sponsor removed everywhere (user: "not a category"); the flowchart stays (Hydration + Fashion under Associate); partners slide is now Education + Media; in-kind is Media / Stationery / Gift.
Derived claims to confirm: "Six flagship events" (the six cards), "Same crowd size, more than double the funds" (550+ and 550+; Rs3L to Rs6.7L = 2.2x), "Disco Diwali, again" 2024 / 2025 / 2026.

## Haiku panel round 2 on v3 (8 reviewers; 36 slides)
Cohesion 7-8/10 again. Clarity of ask still 3/10 from all eight (no price, venue or firm date). Recurrence proof: "yes/partly" 8 of 8; slide 13 (Starry Night twice) named strongest by 4. New findings:
- DATA GAPS (need the user): Disco Diwali 2025 has 500 entries but NO funds figure, so it drops out of the 9/10 totals and the "again" slide; Paradox card has no date; Summer Sunset has no funds; "raised" is not defined as gross or net (Rs22.5L+ is the sum of the cards).
- "500 entries" vs "350+ guests" vs "footfall" vs "attendees" are four words for attendance. Pick one term.
- Slides 3/20 say classes 6-12 but the survey pie covers 9-12.
- Legal: slide 6 (adult with identifiable children) is the riskiest photo; 2000+ student database = minors' data (DPDP Act); review counts; "every one of them for charity" on slide 11 overreaches because Summer Sunset shows no proceeds.
- Brand director: the photo-led recurrence slides "helped the look, hurt trust". RECORDED, NOT ACTED ON: the user's direction is that pictures are the biggest strength and the deck must be more visual.
Fixed from round 2: neon-sign crops (35/36); slide 12 highlight and 2026 card; slides 9/10/11 no longer show the same six flyers (10 now uses event photos); ~4 duplicated photos swapped; reach-tile labels enlarged.
Lesson: a `swap(start, end, new)` helper in a patch script deleted a block of slides when the end marker was defined before the start. Restored from git; assert start < end in any such patch.

## Derived decks and brochures built (2026-10-09)
`python scratchpad/gen_sponsor_deck.py --deck sponsors_cold|sponsors_warm|stalls_cold|stalls_warm [--text] [slide numbers]` -> `out/decks/<deck>/` (36 / 26 / 20 / 14 slides + PDF). One slide library, four ORDER lists; warm decks drop the "who is AQ" intro and open on a thank-you + the past-sponsor wall and quotes (user: warm = generic returning-partner recap, no new facts); stalls decks add "Your stall, in one page" and "Fees and terms, on request" (user: stall pricing/terms are shared later, so no figures anywhere).
`python scratchpad/gen_brochures.py` -> `out/decks/brochures/{sponsors,stalls}_trifold_{outside,inside}.png` + a 2-page PDF each. A4 landscape letter-fold, 3369x2382 px, PDF stamped to 297x210 mm. NO bleed, NO CMYK: confirm with the printer. Print double-sided, flip on the short edge. User ruling: both brochures are trifolds (one per audience).

## Haiku panel on the derived pieces (9 reviewers, 2026-10-09) and fixes
Sponsors warm (returning marketer 4/3/5/8 on warm/ask/credibility/cohesion; design intern 6/4/6/5): asked for the ask to come earlier, fewer repeats, a real "your 2025 activation" recap. DONE: warm order now cover, thanks, logo wall, quotes, this-year, offer-in-one-page, proof... NOT DONE (no data): a per-sponsor recap of what was delivered and reached.
Stalls cold (GM 4/6/8/4 and legal 6/3/8/4): both say they would only reply if a venue and a fee band were shown. Fees are withheld by the user's ruling, so the deck cannot show a band; recorded as the main conversion risk of the stalls decks. Legal wants a compliance statement (FSSAI per food vendor, alcohol policy, fire NOC, noise, insurance) and a safeguarding statement for a minor-heavy audience: NOT in the deck, needs AQ facts.
Stalls warm (returning stall 5/3/5/7; intern 7/5/4/6): fixed the three empty step cards (now numbered steps plus a photo strip with a real "call or message us" step), the "JOIN US" slide (now "Book your stall"), the stat-bar inconsistency on the series slide (one stat per card), chip colours on the run of show (single ink chip), photo repeats, "trade through the night" vs 10:30 PM close.
Brochures: print designer scored print-readiness 3/10: no bleed, 288 dpi raster, flap same width as panels, 100K black, small grey labels, white text on blue. DONE: a PRINT build with 3mm+ bleed, crop marks, fold ticks, 300 dpi (`*_trifold_PRINT.pdf`, 3722x2694), labels raised to ~8pt and darker, blue chips use ink text (measured via core.text_on: ink 6:1 beats white on that blue), contact panel top half filled with a photo, flap photos de-duplicated, "five of our six flagship events" on the proof panel, "600+ expected" (was "600+ guests"), a plain-text QR URL printed beside the QR (source asset decodes to https://www.instagram.com/ngo.aquaterra/). NOT DONE: vector type (the print PDF wraps 300 dpi PNGs, so type is raster), CMYK/rich black, a narrower flap and score lines (printer template governs), a fee band (withheld by ruling), a domain email instead of gmail (user's contact, not mine to change).
Cross-deck: "600+" is now "expected" everywhere (cover chips, flagship, glance); "five of six" qualified on the proof slide; tiny labels raised to 16px.
