# Starry Night throwback carousel (9 slides, 1080x1350 feed, rendered at 2x)

Final PNGs: `final/01.png` ... `final/09.png`, in posting order. Build: `build_carousel.py` (copy of the skill pipeline with the fixes listed below), `jobs.py`, `prep_src.py` (4:5 crops of the chosen frames), `run.py`, `montage.py`. Renders per round: `slides/v1`..`slides/v4` (v4 is final).

## Slides (source frame and caption)
| # | Edition | Source file (Drive) | Caption on slide |
|---|---|---|---|
| 01 cover | Dec 2024 | `DSC_9928.jpg` (Starry nights 23/12/24) | title STARRY NIGHT, "December 2024 and Starry Night 2.0, one more time under the lights" |
| 02 | Dec 2024 | `IMG_6812.JPG` | star lights hung in daylight over an empty court, the night still to come (sticker: STARRY NIGHT 2024) |
| 03 | Dec 2024 | `IMG_6816.JPG` | the tree up, the tables dressed, the sky going gold behind the net |
| 04 | Dec 2024 | `IMG_0373.JPG` | friends on the turf in front of the tree, the AquaTerra neon glowing behind them |
| 05 | Dec 2024 | `DSC_9791.jpg` | a stall under the net after dark, with a hand-lettered sign: "get your lip balms pierced!" |
| 06 | Dec 2025 | Stalls/Photos `IMG_20251226_171956.jpg` | string lights overhead, stalls along the walls, people already walking the floor (sticker: STARRY NIGHT 2.0) |
| 07 | Dec 2025 | Group/Photography `IMG_9917.JPG` | two friends under a ceiling of fairy lights and hanging stars |
| 08 | Dec 2025 | DJ/Photos `IMG_9944.JPG` | the DJ at the decks, with the AquaTerra globe on the banner behind him |
| 09 closer | Dec 2025 | Candids/Photos `IMG_2841.JPG` | hands up under the hanging stars, the whole floor lit blue (sticker: HANDS UP) |

Tag text is truthful by construction: `NN / 09` is the real position. Footer: `@ngo.aquaterra . Starry Night . DEC 2024` on 2024 slides, `DEC 2025` on 2025 slides, `DEC 2024 + DEC 2025` on the cover. No statistics, prices or vendor claims anywhere. The only transcribed in-photo text is the hand-lettered sign on slide 05 (read from the photo: "GET YOUR LIP BALMS PIERCED!").

## Date-label assumptions
- 2024: folder is named "Starry nights 23/12/24", with phone/WhatsApp filenames stamped 20241223. Used "DEC 2024".
- 2025: the Starry Night 2.0 folder's phone files are stamped `20251226` and the user called it Dec 2025. Used "DEC 2025". Nothing more precise is printed (no day).

## Sources reviewed and not used
- `Merry Miracles 2025` (18Aqj5exyeBMLVPz_19BdCtnqk13zLY06): NOT used, per instruction. It holds December 2025 Pather Sathi session folders, a different event.
- Starry Night 2.0 root also holds `Digi Cam`, `Odd Affair`, `YORS` subfolders (Odd Affair / YORS look like other segments of the evening; I did not open them). `.MOV`/video and `.dng` files ignored. `DSC_9930` is over the connector's 10 MB download limit and could not be fetched.
- 2024 folder: 49 pro `DSC_` frames plus phone images. I looked at ~16 and picked 5. Skipped `DSC_9791` neighbours as near-duplicates; I did not view the stall price-list frames and printed no prices.
- Skipped on purpose after viewing: `IMG_9855/9955` (IMG_9955: two adults in front of the lights, good but a second DJ-area frame), `IMG_9964` (four young women, face-forward), `IMG_9862`, `IMG_9832`, `IMG_9813`, `IMG_2847`, `IMG_2855`, `IMG_0340/0358/0412`, `DSC_9803`, `DSC_9734/9777/9871/9882/9895/9915/9945`. Reasons: duplicate mood, prominent faces of probable minors, or weaker light.

## Frames where a child may be identifiable (YOUR DECISION; no consent record)
Nobody is labelled as a minor in the folders. Judging by looks only:
- `07` (IMG_9917): two girls, tight close-up, faces fill the frame. Highest risk, appear to be teenagers.
- `04` (IMG_0373): group of five on the turf, faces clear. May include teens.
- `09` (IMG_2841): the boy on shoulders is clear and smiling; looks teen/young adult. Crowd faces are blurred/dark.
- `01` cover (DSC_9928): DJ and two bystanders (one holding a phone over his face) clear; DJ looks adult.
- `05` (DSC_9791): the stall vendor is clearly shown, looks adult.
- `08` (IMG_9944): the DJ (looks adult) with partly visible people behind.
- `02`, `03`, `06`: no identifiable faces at size, only distant figures.
If any of 07/04/09 is a problem, swap in a non-face frame (e.g. a decor or stall shot from Decor/Stalls) and rebuild; the pipeline is a one-line edit in `jobs.py`.

## Rule-level fixes made to the pipeline (copy in this folder only; skill file untouched)
1. Bottom scrim held darker longer (and taller): the stock ramp left the caption unreadable over pale trousers/tables (v1).
2. Sticker raised above the scrim: it sat under it and `measure_dom` reported it BURIED.
3. Index tag/dots offset: the cover is slide 1, so photo slide k is `k+1 / N`, not `k / N` (v1 said 01/09 on slide 2).
4. Doodle colour: tries the rest of the accent wheel before falling back to ink (a black blob on a pale sky in v1).
5. Connector line is skipped if it would cross an excluded region (it ran through the DJ's face in v2).
6. Inactive carousel dots made visible on a pale sky (3 of 9 vanished on slide 03).
7. `manual_spots` option for frames where `vision.plan_spots_relaxed` starves (netted sky, faces filling frame): positions read off a render, local luminance measured.
`extra_exclude` boxes in `jobs.py` were measured off the v1 renders. A `[vision] starved` warning fired on 03 and was handled by manual spots.

## Looking gate
Montages and every slide read at full size across v1-v4. Remaining known notes: advisory `BURIED img` on the cover (the logo/title scrim stack, visible in the PNG); `OVERSIZE` advisories are doodle bboxes under-reported by <=11px (cosmetic, no collision). Preflight ISSUES: none on any slide.

## Suggested Instagram caption (AquaTerra voice, verified facts only)


```
starry night, again. 

december 2024: the first Starry Night, our Christmas carnival fundraiser. december 2025: Starry Night 2.0. same lights, new faces on the floor.

swipe for the tree, the stalls, the DJ booth and a very loud dance floor.

run by students, for the people we do this for. see you under the lights.

LINK IN BIO
```
Check before posting: "run by students" and the fundraiser framing come from AQ_FACTS (events fund the work; students earn the money they deploy); no date, venue, ticket price or amount is claimed. Drop "LINK IN BIO" if there is no live link. No em dashes used.

## Outstanding
The standing `/canvas-design` companion art piece (CLAUDE.md) was NOT run here, per instruction: the parent session owns it.
