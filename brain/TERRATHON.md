# TERRATHON: the design system (started 2026-09-29)

TerraThon is AQ's multi-sport and gaming fest, **2nd to 4th October 2026**. The user supplied
the full suite: three event posters (each in a `LINK IN THE BIO` and a `LINK BELOW` variant), one
umbrella "registration open" poster, and the sticker kit. Everything below is measured from those files.

| Event | Sport | Dates | Venue | Fee | Pool (winner + runners up) |
|---|---|---|---|---|---|
| **Wicket Wars** | cricket | 3rd and 4th | Turf XL | Rs. 2,100 per team of 8 | Rs. 7,500 (4,500 + 3,000) |
| **Soccer Storm** | FIFA (console) | 3rd | Battleground Gaming | Rs. 350 | Rs. 2,500 (1,500 + 1,000) |
| **PickleJam** | pickleball | 2nd | 11:11 Pick A Court | Rs. 750 per team of 2 | Rs. 5,000 (3,000 + 2,000) |
| **TerraThon** (umbrella) | all three | 2nd to 4th | none | none | "Prizes totalling Rs. 15,000" = 7,500 + 2,500 + 5,000 |

The umbrella reads `SPOTS FILLING FAST / REGISTRATION NOW!!` with the `!!` in red. Every number
in the suite reconciles, so a brief validator can enforce that pool = winner + runners up and
that the umbrella total = the sum of the events.

Files: `training_samples/terrathon/` (references, 1620x2025 RGBA) and
`engine/assets/terrathon/` (stickers: `shuriken smiley flower basketball controller cricket_set pickleball_set aq_live`).

## 1. This is a FORMAT, not four posters

The three event posters share one skeleton to the pixel: same star positions, slab position and tilt,
header block and footer. Only the hero, title, numbers and CTA change. That makes TerraThon a
**format module** (like `engine/dispatch.py`), not a Workflow B target. Recreation is how we
learned the constants. The deliverable is `engine/terrathon.py`: brief in, poster out.

## 2. The skeleton (proven on all three events by `scratchpad/tt_events.py`: **0.039 / 0.073 / 0.082**)

Coordinates are reference px on a 1600x2000 canvas; the engine builds on feed 1080x1350 (scale 0.675).

| Layer (back to front) | What | Position |
|---|---|---|
| Ground | pure `#000`, sparse white flecks | full bleed |
| Shuriken x4 | one identical blue sprite, **never rotated**, ~150px | (1346,257) (163,484) (1343,813) (28,1010); the last sits ON the slab corner |
| Hero sticker | the sport's real sticker, ~747px wide, bottom hidden by the slab | visible top-left (432,484) |
| Slab | white `#F9F9F9`, 28px orchid border, radius ~70, tilt **-1.25 deg** | x 70..1542, y 1095..1601 |
| Title | event name, 2 lines, NeutralFace Bold ~156px, line-height .9; subtitle `A <SPORT> TOURNAMENT` ~88px | inside the slab, left |
| Header | `PRIZE POOL:` (regular 113px), `RS. N` (bold 113px, winged-money emoji), two prize lines (50px) | centred at x=800, y 104..445 |
| Fest tag | white pill, 9px orchid border, `TERRATHON` bold 46px | (1198,78) 377x120 |
| Info | calendar + date, pin + venue at 49px, then fee lines | y 1650..1855 |
| Footer | AQ logo bottom-left, CTA pill bottom-right (cream `#F5EEE1`, orchid border) | y 1880..1985 |

## 3. Rules learned

1. **Weight pairing: label light, value bold**, in ONE family. NeutralFace 400 for labels
   (`PRIZE POOL:`, `WINNER`, `PARTICIPATION FEE`, `FOR A`), NeutralFace 900 for values. The reference's
   header matched NeutralFace at a constant 0.757 ratio on every line, so the face is NeutralFace.
2. **The hero is tucked, not placed.** The slab overlaps the sticker's bottom edge. The sticker file
   is the full object; the slab decides how much shows.
3. **The stretched letters are a REAL FONT, not a distortion (found 2026-09-29).** The user ruled "do not stretch the font" (never `scaleX` a
   glyph), then supplied the actual face: **StretchPro** (`engine/assets/fonts/StretchPro.otf`, Fontself, **licence: "Free For Personal Use"**, flag
   before public/commercial use). It is a LIGATURE font: a doubled letter (`EE`, `EEE`, `EEEE`, `AA`, `AAA`, `CC`, `OO`, `RR`, ...) becomes ONE natively
   stretched glyph. Verified against the references by specimen render: `WICKEEET`, `WAARS`, `STOORM`, `PICKLEEJAAM`, `MINI-FEETE`; `SOCCER` (the natural
   `CC`) and `TERRATHON` (the natural `RR`) stretch on their own. Titles are set in StretchPro, uppercase, spelled with the doubled letter. The
   subtitle face is **Sigmar One** ("use sparingly", per the user; open licence, file not yet supplied). Everything else stays NeutralFace.
   **Done:** all four posters re-rendered with StretchPro titles and a Sigmar One subtitle (`scratchpad/tt_events.py`, `tt_minifete.py`); scores
   0.036 / 0.051 / 0.060 / 0.053 (after the stroke and tracking pass), all under the 0.16 accept line (the metric cannot see a font change; the eye check carries it).
   Sizing: the longer title line is fitted to 940 ref px (events), `TERRATHON` to 760 and `MINI-FEETE` to 1000 (mini-fete), measured with
   `build.measure_text(..., extra_css=)` because a face outside `core.FONTS` measures wrong otherwise. Title spellings: `WICKEET` / `WAARS`,
   `PICKLEE` / `JAAM`, `SOCCER` / `STOORM`, `TERRATHON`, `MINI-FEETE`. NOT copied: the references' titles look ~1.3x taller than StretchPro's natural
   proportions (the designer scaled them vertically); we keep natural proportions per the user's no-distortion ruling.
   **Stroke and tracking (user, 2026-09-29):** in the references StretchPro and Sigmar One have a stroke around the letters and tighter kerning.
   Measured: reference letter gaps are 1-4px where plain rendering gives 9-15px (StretchPro) and ~8px vs ~9px at a larger cap (Sigmar One); the NeutralFace
   lines already matched to ~1px. Applied: StretchPro `-webkit-text-stroke 0.04em` + `letter-spacing -0.045em`; Sigmar One stroke `0.03em` + `-0.01em`;
   NeutralFace unchanged. **TRAP: any non-zero `letter-spacing` switches the stretch ligatures OFF** (`WICKEET` silently renders as two ordinary E's), so StretchPro
   text MUST also carry `font-feature-settings:'liga' 1,'dlig' 1` (and so must its measurement: `measure_text(features=)`).
   Sigmar One: OFL, `engine/assets/fonts/SigmarOne-Regular.woff2` (fetched from the npm package `@fontsource/sigmar-one`); the user said to use it SPARINGLY
   (subtitle and the sport name on promo stories only).
4. **Constant furniture.** The four stars never move or rotate between events.
5. **One die-cut treatment**: cream halo, no ink outline, flat fill, hand-cut rough edge. The rough
   edge is in the supplied PNGs. `shapes.sticker()` cannot reproduce it, so stickers are ASSETS,
   never redrawn.
6. **Subtitle fits, never crowds.** Full size (88px) unless the sport name is long; then it shrinks to a
   1265px maximum width (`A PICKLEBALL TOURNAMENT` ran to within 25px of the slab border at 88px). Found by
   the looking gate, not by any metric, and encoded as `SUB_MAX_W` in the builder.
6b. **Info rows are measured, then centred on x=800.** Icon + date, an 80px gap, pin + venue form one group;
   the fee block sits below. With ONE fee line the rows shift down (date +16px, fee +10px in 1600 space);
   with two lines they sit high. Per-event offsets live in `EVENTS`.
6c. **Sprites sit at native size** (x 1600/1620): every sticker in the kit is 1:1 in the 1620px design, so
   an event only needs the visible top-left of its hero, not a scale.
6d. **Tight margins are a series trait**: logo 27px and CTA 13px from the canvas edge on 1080x1350.
   `build.render(margin=12)` now says so (see the engine fixes below).
7. **Numbers reconcile** (table above). Validate before rendering.
8. **The calendar is drawn, without a date.** The reference's calendar emoji is fixed artwork that reads
   `JUL 17` beside `3RD OCTOBER`. That is wrong on the live posters. Do not copy it.

## 4. Palette: TerraThon's own tokens (user ruling: own colours)

| Token | Hex | Used for |
|---|---|---|
| ground | `#000000` | canvas |
| orchid | `#DE68F0` | slab border, pill borders |
| green | `#2FD284` | hero stickers |
| blue | `#0396FF` family | shuriken, smiley/flower/basketball rings |
| halo | `#F3ECDE` | sticker die-cut halo |
| slab | `#F9F9F9` | slab, pill fill |
| cta | `#F5EEE1` | CTA pill fill |

These are not `core.ACCENTS`, and they do not go through `accent_for(dept)`. To implement as
`core.TERRATHON` when the module is written.

## 5. Sticker kit

`shuriken` (furniture, all posters) · `cricket_set` (bat + ball) · `pickleball_set` (paddle + ball) ·
`controller` (FIFA) · `basketball`, `smiley`, `flower` (purple/blue: reserved for other events or fillers;
not used by any supplied poster yet) · `aq_live` (a blue/white/black burst reading `AQUATERRA LIVE`, a
separate live-coverage badge, not on the event posters) · **`carnival`** (1750x2000, real alpha: a pre-composed
PILE, not a single object: blue palm tree over a green smiling flower, a purple heart holding a green
shuriken, and a blue star-eyed smiley, all in the same cream die-cut halo).

The kit shows a colour rule: the **character stickers recolour** (smiley and flower are purple with a blue
ring in the pack, but green-flower / blue-smiley / purple-heart inside `carnival`), while the **sport
objects are always green** and the shuriken is always blue. Palm blue is `#0090F8`, close to the shuriken
family. 

## 5b. The MINI-FETE (the carnival; a marketing stunt for Disco Diwali passes)

The carnival pile is the hero of the **TerraThon Mini-Fete**: a stunt at the fest (3rd and 4th October, Turf XL,
New Alipore, open to all) with mini-games, competitions and stalls, whose job is to sell **Disco Diwali passes**.
Reference: `training_samples/terrathon/mini_fete_stunt.png`. Built by `scratchpad/tt_minifete.py`, **0.047**, gate clean.

It shares the visual system but NOT the event skeleton, so it is its own layout:
- no prize block and no TERRATHON pill; the header is a two-line ask, `CHANCE TO BUY / DISCO DIWALI PASSES`
- hero: `carnival` at 0.535 of native, visible top-left (420, 335), bottom hidden by the slab
- slab text is **centred** (event slabs are left-aligned) in three tiers: `TERRATHON` / `MINI-FETE` / `MINI-GAMES | COMPETITIONS`
- one info row (calendar, date, venue; no pin), then a three-line bold body, CTA `OPEN TO ALL`
- the fourth star sits on the slab's bottom-RIGHT corner at 0.9 scale (5px from the right edge; events: bottom-left)
- header type is set to the reference's cap heights with tracking solved to its widths; body lines are 57px bold

Reference inconsistencies kept as given but flagged: `MINI-GAMES` (slab) vs `MINIGAMES` (body).

## 5c. Content facts supplied by the user (real; never invent alternatives)

- **WhatsApp group (CTA for the carnival carousel and its stories):** https://chat.whatsapp.com/Jke9ZHypTP90HhSnyHl3ai?s=sh&p=a&mlu=4&ilr=4 (given 2026-09-29).
  Instagram cannot carry a clickable link in a feed image, so the slide CTA reads "link in bio" or "link below" (as the event posters do);
  the real link goes in the caption or bio. A QR made from THIS link is a real asset (unlike a fabricated one) and is allowed on the WhatsApp graphic.
- **Calendar (from the user, 2026-09-29):** carnival days are Sat 3 and Sun 4 Oct; sports registrations close Thu 1 Oct.

## 5d. The party-invite carousel structure (`training_samples/terrathon/summer_sunset_carousel_template.png`)

The user shared an 8-slide "Event Poster" frame from the Summer Sunset (AQ's 5th anniversary party) all-you-need-to-know carousel,
4:5 portrait. It is NOT the Paradox template (that is still not in the repo). It teaches the info-slide grammar of a party invite:

| # | Slide | Mechanism |
|---|---|---|
| 1 | Cover | "Everything you would want to know about" + the event logo-type |
| 2 | Artist | circular portrait, `MUSIC BY` + name, supporting acts below |
| 3 | Venue map | a real floor plan on the page, `GATES OPEN AT 5PM` under it |
| 4 | Schedule + parking | white pill rows (time chip + act), then a red no-parking note |
| 5 | Food | 3x3 grid of circular partner logos |
| 6-7 | Rules and guidelines | dark rounded panel of numbered fine print, split over two slides |
| 8 | See you tomorrow | event logo-type, pin + venue, clock + time |

Visual system there: sand ground, illustrated palms and a beach/wave footer with the logo on every slide. That is Summer Sunset's look,
not TerraThon's. The STRUCTURE transfers to the Friday "all you need to know" post; the look would be TerraThon's (black ground, slab, stickers).
Two craft notes: the rules panel's fine print is unreadable at feed size (split it further or raise the size), and slides 5 and 3 depend
on real assets (partner logos, an actual floor plan) that cannot be invented.

## 5e. The marketing-points carousel: Paradox "13 reasons why" (`training_samples/terrathon/paradox_13_reasons_template.png`)

The user's template for the Tuesday carousel (TerraThon/Carnival marketing points, "reusing the Paradox template"). The screenshot shows the cover and
five point slides of a longer run; the 6th is cut off. 4:5 stories/posts. Grammar:

| Slide | Mechanism |
|---|---|
| Cover | big red numeral (`13`), `REASONS WHY YOU SHOULD ATTEND`, event logo-type, then a strip: date, venue pin, clock, `LINK IN THE BIO` pill |
| Point slide | circular photo (a real photo of the thing), red display headline (`NANDU JEE`, `POLAROID`, `CUTEST DECOR`, `PRESS-ONS`, `CHARMS BAR`), one snarky two-part tagline in black |
| Artist slide | same as a point slide, headline `MUSIC BY` + name, supporting acts under it |
| Every slide | title-sponsor strip at the top (`Realmark`, `TITLE SPONSOR`); footer `LIMITED SPOTS, REGISTER NOW!` above AQ logo (left) and Paradox logo (right) |

Voice pairs (headline / tagline): `NANDU JEE / SERVING CHAOS AND CRAVINGS (ON THE HOUSE)`, `POLAROID / BECAUSE PHONES DIE, MEMORIES DON'T`,
`PRESS-ONS / WALK IN EMPTY-HANDED. LEAVE LOOKING FRESH.` Each tagline is one benefit plus one wink, in capitals. Look: sand upper half, blue wave lower half, green palms
in both top corners. Every point slide depends on a REAL photo in its circle and, on this template, a sponsor logo and a Paradox logo: none can be invented.
Open questions before building: does the carnival carry a title sponsor, and which footer brand (TerraThon, Paradox or neither)?

## 5f. Partner logos (`engine/assets/terrathon/partners/`)

Real logos supplied by the user, one file each, used as-is (never redrawn): **`cravella.png`** (508x508 circular mark: plum ground, cream ring, a
bow drawing, script wordmark `crave'lla`, handle `@cravella_kolkata`). Spelling for copy: **Crave'lla** (handle `cravella_kolkata`).
**Seen but NOT on disk (inline images only, no file):** the Artily logo (black wordmark `ARTILY` with the line `ARTISANAL BEVERAGES`, so Artily sells
**artisanal beverages** by its own logo) and the CRFTD logo (blocky red `CRFTD` wordmark with a small star on a cream ground, an opaque square, so it would be a tile,
not a floating mark). Neither may be redrawn: real files are required. (A wrong `artily.png` that was a duplicate of the Cravella file was committed and removed the same day.)
Confirmed by the user (2026-09-29): **Artily = boba**; **Crave'lla = desserts and brownies**; a **photobooth** is on site; **no title-sponsor strip** on the carnival carousel.
Still awaited: the Artily and CRFTD files, and what the CRFTD orders are.

## 5g. Promotion-story templates (user, 2026-09-29: "sample story templates")

The user's screenshot shows the sports PROMOTION STORY template, 1080x1920: a full-bleed real photo of the sport at its venue (8 variants each
for PICKLEBALL, FIFA, CRICKET) under a dark scrim, the prize block top-right (`PRIZE POOL:` / `RS. N` / winner / runners up, small white),
blue shuriken on the left and right edges, and at the bottom a white card with a GREEN outline holding a small `TERRATHON` tag chip, the sport name in
Sigmar One (`PICKLEBALL`, `FIFA`, `CRICKET`), then the info lines (date and venue, participation fee, team size), and the AQ logo under it.
Note the card outline is GREEN here, not the orchid of the feed posters. Source photos are required as FILES (only the screenshot exists so far).

## 5h. Collaterals built (2026-09-29): builders and what each needs

| Item | Builder | Status |
|---|---|---|
| Event posters, Mini-Fete post | `tt_events.py`, `tt_minifete.py` | done |
| Disco Diwali ticket sale, Rs. 550, at the carnival (stickers-first: disco ball, diya, ticket; feed only) | `tt_dd_tickets.py` -> `out/collaterals/dd_tickets_550_carnival.png` | done, gate clean. **Price 550 is from the user's second message (first said 55); confirm.** No DD date/venue shown (not supplied). Story cut not built. Companion: `tt_companion_facet_ledger.py` |
| 7-reasons carousel (feed + story), "all you need to know" deck (feed + story) | `tt_carousel.py reasons know` | done, stickers in the circles |
| 10 sports promo stories (3 cards x 3 sports + umbrella) | `tt_promo.py`, `tt_umbrella.py` | done |
| Single-slide WhatsApp graphic + verified QR | `tt_wa_graphic.py` | done |
| Photo promotion stories, day stories | `tt_promo_photo.py` | template done; drop photos in `engine/assets/terrathon/promo_photos/<sport>/` and `day_photos/` |
| Copy pack (captions, WhatsApp, reel briefs, Q&A) | `brain/TERRATHON_COPY_PACK.md` | drafted |
| Companion art plate | `tt_companion_halo_field.py` | done (`brain/companion/`) |
| Schedule post (feed + story) | `tt_schedule.py [story]`, data in `brain/TERRATHON_SCHEDULE.md` | done |
| Throwback carousels (pickleball, FIFA), 7 slides each | `tt_throwback.py pickleball\|fifa`, photos in `engine/assets/terrathon/throwback*/` | done |
| Crave'lla stall signage (A4 landscape, PDF + 300dpi PNG): Crave'lla logo + name, "our dessert partner", AQ LIVE sticker, AQ logo, TerraThon look | `tt_partner_sign.py cravella|artily|crftd` | done; full-bleed black, no bleed/crop marks |
| Disco Diwali ticket stall signage (A4 landscape, PDF + 300dpi PNG): user's three DD photos in tilted frames, DISCO DIWALI / TICKET STALL / LIMITED TICKETS ON SALE | `tt_dd_sign.py`, photos in `engine/assets/terrathon/dd_photos/` | done; NO price printed (Rs. 550 unconfirmed) |
| Lottery stall signage (A4 landscape, PDF + 300dpi PNG): user's jar photo, LOTTERY / TRY YOUR LUCK | `tt_lottery_sign.py`, photo `engine/assets/terrathon/lottery.jpg` | done; no prize/price/rules printed (not supplied) |
| Photobooth stall signage (A4 landscape, PDF + 300dpi PNG): user's photo of the printed AQUATERRA strips, PHOTO BOOTH / STRIKE A POSE | `tt_photobooth_sign.py`, photo `engine/assets/terrathon/photobooth.jpg` | done; faces visible in the strips (flagged); no price/hours printed |
| CRFTD stall signage (A4 landscape, PDF + 300dpi PNG): CRFTD logo in a circle (no photos), CRFTD / OUR JERSEY PARTNER / T-SHIRT ORDERS TAKEN HERE (NOT DIY; no pre-printed-tees line on the sign) | `tt_crftd_stall_sign.py` | done; no prices printed |
| Crave'lla A4 menu card (single page, PDF + 300dpi PNG, TerraThon branding: black ground, green cards, orchid chips) | `tt_cravella_menu.py` | done; full-bleed black, no bleed/crop marks |
| Crave'lla carousel REMAKE (5 slides, feed + story): cover, meet the stall (slab), FINAL menu on one slide, cookie-tin feature, closer. Supersedes the 6-slide version below | `tt_cravella2.py [story]` -> `out/collaterals/cravella_stall_v2/`, `stories/cravella2_story_NN.png` | done |
| Crave'lla stall carousel (6 slides: our dessert partner intro + FINAL menu, 2026-10-01), logo and photos from the user | `tt_cravella.py`, assets in `engine/assets/terrathon/partners/cravella/` | done; ACAI spelled as such (user wrote "Asscai") |
| Rules cover (opener for the three rules posts; swipe order 02 PickleJam, 03 Wicket Wars, 04 Soccer Storm) | `tt_rules_cover.py` | done |
| Rules posts (cricket, pickleball, FIFA), green boxes on black | `tt_rules_cricket.py cricket\|pickleball\|fifa` (copy condensed from the site's rules pages; clauses omitted are listed in the config comments) | done |
| Certificates: Winner, Runner Up (full black ground) and Participant (white paper), A4 landscape, PNG + PDF, one layout, three colourways; single signatory Kanishk Agarwal, Co-Founder and Trustee | `tt_certificate.py` | done (rev 2). Modelled on the Paradox certificate set. Fillable: `--name`, `--event`. Rank (1ST / 2ND) is set at 46px; AQ LIVE sticker replaces the logo; sport and character stickers from the kit. Wordmark tracking is +0.012em, not the poster's -0.045em (the thick outline fuses E and the stretched R otherwise). Signature line is blank on purpose. On black, outlines go cream and hard shadows take the variant accent. Winner = solid orchid keyline + gold seal; runner up = blue keyline + silver seal; participant = green seal |
| Video, welfare-impact numbers | none | not possible / blocked |

## 6. Reference defects (do not copy)

1. `SOCCER STORM` subtitle reads **`A FIFA TOURNMENT`** (missing A). Set correctly here.
2. `soccer_storm_bio.png` has **no TERRATHON pill**; the other five event posters do. Treated as an
   omission in the source design, so the pill is part of the series. Scored against `soccer_storm_below.png`.
3. The calendar emoji (`JUL 17`) on every event poster.

## 7. What is still open

1. **Logo lockup.** The reference logo has a bigger globe and a narrower, quieter wordmark than
   `core.LOGO`. Fit by width for now (475px). If the user has the TerraThon lockup file, use it.
2. **Emoji.** Noto Color Emoji stands in for the reference's Apple set (💸 🥇 🥈 📍). Acceptable adaptation.
3. **Paper grain on the slab** (the reference has a fine speckle) is not yet reproduced.
4. **Subtitle face.** Set in NeutralFace Bold per user ruling; the reference's chunky slab face is not used.
5. **Other events.** Basketball, smiley and flower stickers exist with no poster. Ask before assuming.

## 8. Build plan

1. Done: Wicket Wars 0.039, PickleJam 0.073, Soccer Storm 0.082, all gate-clean, one builder (`scratchpad/tt_events.py`,
   output `out/versions/terrathon_<event>/v2.png`). The skeleton IS constant: PickleJam and Soccer Storm needed only
   data, one subtitle rule, and per-event row offsets.
3. The umbrella poster is a different layout (three heroes fanned, prize total, a red alert line).
   Recreate it after the three events.
4. Then `engine/terrathon.py`: brief in (event, sport, dates, venue, fee, prize split, CTA), validator,
   solver, poster out. Same brief drives the messaging chain via the `aq-event-messaging` skill.
5. Companion `/canvas-design` piece per the standing rule (outstanding).
