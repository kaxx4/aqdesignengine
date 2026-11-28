# Disco Diwali 3.0 carousels (Nov 2026)

Two real-photo carousels built with the `aq-photo-carousel` pipeline. Final slides are in `final_jpg/<name>/NN.jpg` (01 = cover), 2160x2700 (1080x1350 at 2x), JPEG q92. The lossless 2x PNGs were rendered to `final/` and are not committed (size). Source photos are not committed either (consent): `jobs.py` names each frame by its Drive folder and file position. Source folder: the "Disco Diwali 3.0" Drive folder.

## 1. dd26_stalls (8 slides)
| # | Source | Caption on slide |
|---|---|---|
| 01 cover | Gajra jhumka `00` | title THE STALLS OF DD 3.0; "donuts, kulfi, jhumkas, crochet and more, all under one roof at Disco Diwali 3.0" |
| 02 | MOD `02` | the Mad Over Donuts sign, glowing over a dark counter |
| 03 | Chetan Kala `00` | crochet flowers and plush toys under a marigold garland, Chetan Kala |
| 04 | Unbasic `01` | beaded cherries, stars and jellyfish laid out on black cloth, Unbasic |
| 05 | Meet cute `01` | noodles, momos and spices lined up in trays at Meet Cute |
| 06 | Bedazzling `04` | rows of clay diyas beside sheets of gem stickers |
| 07 | Eloza `01` | bracelets and rings laid out on pink and cream trays, Eloza |
| 08 closer | Bombay kulfi `00` | a smile behind the Bombay Kulfi counter |

Stall names are read off the signs in the photos (MOD, Chetan Kala, Meet Cute, Bombay Kulfi, Eloza, Unbasic). Price lists visible in some frames are not printed.

## 2. dd26_groups (7 slides)
| # | Source | Caption on slide |
|---|---|---|
| 01 cover | Cravella `06` | title THE PEOPLE OF DD 3.0; "pairs, trios and packs of friends, caught at Disco Diwali 3.0" |
| 02 | DSLR `28` | two friends leaning in at the Eloza stall |
| 03 | Eloza `00` | three thumbs up under the marigold garlands at Eloza |
| 04 | DSLR `40` | a hug, mid-laugh, against the coloured wall |
| 05 | Nandu jee `00` | the Nandu Jee food stall pair, peace sign up |
| 06 | DSLR `17` | heads down together over the table, kurtas and stoles on |
| 07 closer | DSLR `27` | backs to the camera under the fairy lights, red, teal and pink kurtas |

## Your decision needed: faces and consent
Several people in both sets look like teenagers, and no folder carries a consent record (the DD notes in `brain/DISCO_DIWALI.md` say the same about the earlier photo set). Judged by appearance only:
- **Groups 01, 02, 04, 06, 07** show people who may be minors. 02 and 04 are tight faces. 07 is backs only and the safest.
- **Stalls 03 and 08** show adult stall holders. No other stall slide has an identifiable face.
If any should go, swap the frame in `jobs.py` and re-run `run.py`.

## Thin spots in the Drive folder
- The DJ, Decor and Sania cam folders are almost entirely the DJ, so they gave no group shots. Groups come from the DSLR set and from stall-owner photos.
- Empty or unreadable: Period Pain Simulator, puchka, pizza hut, subway, Photobooth (both), Digicam, Meta Glasses, Exposure/Photos. Four stall images failed to download (artily `00`, bombay kulfi `03` and `04`, unbasic `03`). Those stalls are therefore thin or missing: **Period Pain Simulator, puchka, pizza hut and subway have no slide.**

## Dates
"DISCO DIWALI 3.0 / NOV 2026" comes from the folder name and file dates. Nothing else is claimed.

## Build notes
- Builder: `build_carousel.py` here is a copy of the skill's, with rule-level fixes since written back into `.claude/skills/aq-photo-carousel/` (sticker under scrim, eyebrow contrast, cover scrim and exclusions, `spots_override`). See playbook items 20 to 24.
- Hair exclusions measured off v1 renders on a 100px grid: `hug.jpg`, `huddle.jpg`. Vision starved on `kulfi.jpg`, `hug.jpg`, `huddle.jpg`, so doodles there are hand-placed on measured wall areas. `trio.jpg` (the groups cover) carries one doodle only, by design: the cover keeps its title block clear.
- Advisories left: BURIED on the cover image (a scrim over a photo, visible in the PNG) and OVERSIZE on doodle boxes (under-reported by up to 11px, no collisions).

## Suggested captions (facts from the Drive folder only)
Stalls:
```
the stalls of Disco Diwali 3.0.

donuts, kulfi, jhumkas, crochet, beaded pins, diyas, bracelets and a lot of momos. swipe through.

LINK IN BIO
```
Groups:
```
the people of Disco Diwali 3.0.

pairs, trios and packs of friends. tag yourself.

LINK IN BIO
```
