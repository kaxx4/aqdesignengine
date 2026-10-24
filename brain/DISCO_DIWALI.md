# DISCO DIWALI FORMAT (v1, 2026-10-13)

The poster family for AQ's Disco Diwali charity party. Built as a FORMAT MODULE, `engine/discodiwali.py`, the same shape as `dispatch.py`: one skeleton, a validated content dict, a solved layout. Self-test: `scratchpad/test_discodiwali.py` (69 assertions). Operator quickstart is section 7.

Status: the 2026 announcement was recreated from its reference and accepted by the looking gate (`scratchpad/dd_announce.py`, v2). The module generalises it to five kinds, two canvases and three visual directions. Rules marked PROVEN were each caught by a render and fixed.

## 1. Facts supplied (the only source for copy)
- Disco Diwali 2026, "Masquerade Sangeet Edition", 10th November 2026, 4:30 PM onwards.
- "Ticket sales open soon", "More details to follow", CTA "Link in bio". All for charity.
- No venue, price or lineup has been supplied. The module has no field for them, so it cannot print one. (TerraThon notes carry Rs. 550 as UNCONFIRMED. It stays out until confirmed.)
- Earlier editions: 1.0 (Oct 2024), 2.0 (Oct 2025, clapperboard 22/10/25). See `AQ_FACTS.md`.

## 2. Assets (all supplied by the user; `engine/assets/disco_diwali/`)
| File | Role |
|---|---|
| `title_lockup.png` 2000x1382 RGBA | the hero: disco ball + DISCO + hand-lettered दिवाली, speckled off-white. It is lettering, never rebuild it from a font |
| `live_badge.png` 1061x1005 RGBA | ALL FOR CHARITY / LIVE / AQUATERRA card, top left. It is the AQ presence on this format |
| `mask.png` 2000x1514 RGBA | silver jewelled mask |
| `mask_copper.png` 1680x1278 RGBA | the same mask in copper, the classier colourway |
| `mask_red.svg` | a red satin mask DRAWN here (gold filigree, beaded trim, plume), for when no photo mask is wanted |
| `mask_stroked.png` | the silver mask with a red speckled die-cut stroke, built by `scratchpad/make_mask_stroke.py` from the mask's own alpha |
| `string_lights.png` | two sagging bulb strings |
| `bg_beaded_portrait.jpg`, `bg_beaded_landscape.jpg` | beaded celestial corner plates on black |
| `bg_diya_portrait.jpg`, `pattern_diya_navy.jpg` | navy and gold lotus-diya corner plate, and its source tile |
| `sparkles.png`, `grain.png` | full-frame overlays: gold dust, film grain with scratches |
| `red_carpet.png` | trapezoid runway with gold lines, for ticket posters |
| `sold_out_banner.png` | red grain banner with speckled SOLD OUT |
References: `training_samples/disco_diwali/ref_announce_2026.png`, `ref_announce_copper_diya.png`.
Still wanted: the navy diya LANDSCAPE plate (shown in chat, never reached the disk).

## 3. The skeleton (z-order, back to front)
ground black -> plate (corner clusters, centre left black on purpose) -> [carpet] -> string lights -> mask (IN FRONT of the lights) -> LIVE badge -> title lockup -> type stack or hero numeral -> [sold-out banner] -> gold sparkles (screen blend) -> film grain (screen blend).
Measured on the reference (`compare.geometry`): full-bleed, coverage 0.539, the quiet band sits between the title and the date block.

## 4. Rules
1. **Ink ground only**, never cream. A recorded exception to CLAUDE.md sec 9; this format has its own palette: silver, gold, off-white, plus the mask's own colour. No `core.ACCENTS`. PROVEN.
2. **One hero**: the title lockup. A countdown numeral or date numeral REPLACES the info stack, never the title. PROVEN (countdown, save-the-date).
3. **The pattern lives in the corners and fades to black in the centre.** The centre is the type zone. The plate is never tiled across it.
4. **The carpet ALWAYS fades into black** toward its narrow end (user directive 2026-10-13). A hard-edged slab is a defect. Encoded as a mask gradient, asserted in the self-test.
5. **Type is off-white, bold, uppercase, centred**, with a text stroke for weight. The reference uses a wide geometric sans that is not in `core.FONTS`; Eina stands in, and the match is close.
6. **Type is measured on what the reader sees.** The first build shrank the clock line to illegible because the width estimate counted the clock's SVG markup as letters. PROVEN, asserted.
7. **A declared box must be as tall as the glyphs.** A numeral boxed at 74% of its drawn height "collided" with its label and hid a real 4px overlap. PROVEN, asserted.
8. **A taller canvas stacks two plates**, the second flipped and faded in, because cropping a 4:5 plate to 9:16 leaves a dead black middle. Extra height goes to TOP 15%, TITLE 62%, INFO 100%, so the CTA stays bottom-anchored. PROVEN.
9. **The title, mask and type never touch.** Intentional tucks (subtitle into the title's left notch) are declared as collision-ignore pairs, filtered to the labels that exist in that kind.
10. **The mask is always in front of the string lights** (user, 2026-10-13). Lights sit at z 5, mask at z 6; asserted in the self-test.
11. **Text budget: the more of the canvas a photo owns, the less copy it carries.** `typo="minimal"` keeps the title, one foil date line and the CTA; `typo="whisper"` keeps the title and one mono line. Both lighten the dim layer so more photo shows, and add a bottom shade so the remaining line still reads. Use them whenever the photo is the full background.
12. **Nothing is invented.** A price, venue or lineup is printed only if a field exists and the caller supplies it. A missing or unknown field raises with the field named.

## 5. Visual directions (the `style` and `mask` options)
| Direction | Call | Character |
|---|---|---|
| Silver and sequins | `style="plate"`, `mask="asset"` | the reference. Busy, jewelled, string lights on |
| **Copper and diya** | `style="diya"`, `mask="copper"` | **the classier direction (user, 2026-10-13).** Navy and gold lotus-diya corners, copper mask, no string lights. Quiet and warm |
| Stroked mask, plain ink | `style="stroke"`, `mask="asset"` | silver mask with a red speckled die-cut stroke on a plain black ground; the type does all the work |
| Photo + soft plate | `style="photo"`, `mask="copper"`, `typo=` editorial / foil / outline / vertical / stack / minimal / whisper | a real photo behind the SCREEN-blended soft diya plate; seven type treatments. Foil and outline are the strongest |
| Red satin mask | `style="stroke"`, `mask="red"` | a mask drawn from scratch. Works, but reads flatter than the photographed masks. Fallback only |

### Photo teasers (kinds `teaser_full`, `teaser_arch`, `teaser_trio`)
Real event photos from `engine/assets/img/events/unsorted-2026-10-07/` (by NN prefix, e.g. `"03"`) in the branding: a full-bleed photo sunk into ink under the title, a gold-edged arch window, or three tilted print frames. All three work on feed and story. **Consent caveat: several photos show minors and none has a consent record. Check before any public post.**

### Layout presets (`layout=` on `style="photo"` announce)
`classic` (title centred, mask top right) · `mask_hero` (a huge mask bleeding off the right edge, title lower) · `title_hero` (the lockup bleeds wide, mask shrinks to a corner accent) · `mask_behind` (the mask sits BEHIND the title, which overprints it). The edition lines are placed relative to the lockup's real bottom, so every preset keeps the notch tuck. `mask_tilt=` and `mask_scale=` override a preset. Batches: `scratchpad/dd_variations.py` (12 posters across direction, type, photo, mask) and `scratchpad/dd_layouts.py` (8 posters across layout). JPEG samples are in `sample_outputs/disco_diwali/` (never commit the 2x PNGs: ~8 MB each).

### Launch pack (kinds `story_launch`, `wa_poster`, `wa_dp`) — `scratchpad/dd_launch_pack.py`
- **Ten stories** (1080x1920), each a different photo, type treatment and layout, ALL carrying the launch post's information (LIVE badge, edition, date, time, ticket-sales status, "more details to follow"). **No CTA pill**: a link-sticker zone is declared as the element `linkzone` (640x165 at y=1505), with a small "LINK IN BIO" cue above it. The zone ends 250px above the bottom edge (Instagram's reply bar) and nothing enters it; the top 200px is left clear of Instagram's profile bar.
- **WhatsApp poster** (1080x1350): the same information as a 4:5, no pill and no "link in bio" (there is no link to point at).
- **WhatsApp group DP** (1080x1080): WhatsApp crops to a CIRCLE r=540, so every box is asserted to sit inside it (title, a small mask, the date and edition; no LIVE badge, it would be cropped and unreadable at DP size). `whatsapp_dp_circle_preview.*` shows the crop.
- **All launch-pack type is NeutralFace** (user, 2026-10-13, who supplied `neutral-face.zip`): `Poster.neutralise()` re-sets the serif, mono and Eina lines in `--d`, forces uppercase and maps weights to the two cuts (400 Regular, 700 Bold). The zip's cuts are the same face as `engine/assets/fonts/NeutralFace*.otf` (Bold identical; Regular differs by ~2px a line), so the engine file was NOT replaced: that would shift every existing recreation.
- **ONE mask placement for every story** (user, 2026-10-13, reference `story_01`): the classic position (left 254 / top 60 / width 832 on the 1080 canvas, untilted). `story_launch` ignores `layout=`, `mask_tilt=` and `mask_scale=`, because the layout presets move the mask and the title together; the silver mask is fitted to the copper mask's measured footprint. Asserted in the self-test.
- **Stories carry no date or time** (user, 2026-10-13): `date` and `time` are optional on `story_launch`; without them the status is the hero line.
- Story type is scaled 1.14x (a story is read at a third of a feed's size) and the info lines spread with it, anchored just above the date. Lines tucked under the lockup (`sub1`, `sub2`) and the cue keep their size.
- `stack` abbreviates the month as NOV (10 NOV 2026); every other treatment prints NOVEMBER.
- JPEG deliverables (1080 wide): `sample_outputs/disco_diwali_launch/`.

### BULK STORIES: the approved design (user, 2026-10-13: "perf, this is the design for bulk stories")
Use kind `story_ref` (`scratchpad/dd_bulk_stories.py`), never `story_launch`, for any batch of stories. It is the remake of the user's reference story, built from measured positions: LIVE badge top left, copper mask top right, ball-free title lockup (`title_lockup_noball.png`), "MASQUERADE SANGEET" 40px bold with a white regular "EDITION" 38px, "TICKET SALES OPEN SOON" 52px, "MORE DETAILS TO FOLLOW" 38px, and a soft gold-edged "LINK IN BIO" pill. Photo runs edge to edge (no diya plate), all type NeutralFace white with a thin black border, no date or time. Only the photo changes between stories. Open questions: the reference's own photo is not in the repo (photo 05 stands in), and the pill sits where an Instagram link sticker would go.

### Carousel: "window stack" (2026-10-14) — `scratchpad/dd_window_carousel.py`
Five 4:5 slides from a user inspo (tilted search windows stacked, one photo each). Bespoke script on the Poster primitives, not a registered kind. Cover and CTA keep the lockup as hero; slides 02-04 make the photo stack the hero (R2 bends there). Title bar reads DISCO DIWALI - MASQUERADE SANGEET EDITION (supplied facts only); the one search field says LINK IN BIO. Lessons: CSS `perspective` makes a window's top edge draw ~12% WIDER than its declared width, so declare narrower; the long title needs a window >= ~830px or a shorter per-window title (it spilled past a 640px window and no gate caught it); size body type off the well, not the window. Photos carry the standing consent caveat. JPEGs and the companion art piece: `sample_outputs/disco_diwali_carousel/`.

### Carousel: "callout frames" (2026-10-14) — `scratchpad/dd_callout_carousel.py`
Four 4:5 slides from a second user inspo (dimmed full-bleed night photo, gold-bordered close-ups, hairlines to corner-bracket reticles). Cover and CTA keep the lockup as hero; 02-03 make the framed photos the hero. Label is MASQUERADE SANGEET EDITION (supplied), no date, time or location. Photos: `engine/assets/img/events/disco-diwali-hall-2026-10-14/`. Lesson: pick the background photo for what it looks like at 60% brightness AFTER the navy grade, not before: an extreme close-up (a neck and ear) made a poor ground, and a very dark frame needed a 1.2 brightness lift. JPEGs and companion: `sample_outputs/disco_diwali_callout/`.

### CAROUSEL: "captcha" (`scratchpad/dd_carousel_captcha.py`, JPEGs in `sample_outputs/disco_diwali_captcha/`)
Four 1080x1350 slides on the approved diya ground (user, 2026-10-14, "i want this blue effect": black, navy and gold lotus-diya corners fading to black, string lights; not the beam recipe), from a user inspo (a "Choose everything related to..." verification card over a party photo): 1 the COVER (title lockup, copper mask, LIVE badge, a full captcha-card hook: blue header VERIFY YOU'RE A DISCO DIWALI HUMAN, a checkbox with a spinner, a SWIPE button), 2 the card with nine real event photos, 3 the same card with all nine ticked and the button reading VERIFIED, 4 ALL FOR CHARITY with the edition line and the LINK IN BIO pill (no date or time anywhere in the carousel, user 2026-10-14). Adaptations: the card is a design device (no reCAPTCHA marks, real photos, our button); the inspo's "best parties in the city" became "Related to Disco Diwali" because the claim cannot be backed; the header keeps the inspo's blue as the recognisable mechanism. No price, venue or lineup. Photo consent caveat applies (nine event photos, several show apparent minors).

### Location reveal poster (2026-10-19) — `scratchpad/dd_location_reveal.py`, JPEGs in `sample_outputs/disco_diwali_location/`
Feed 1080x1350 and story 1080x1920 from a user inspo (a tilted rounded map card lying on the ground with round map buttons and a pin avatar). The map is the USER'S OWN screenshot (`engine/assets/disco_diwali/map_60_chowringhee.jpg`), never redrawn, so no street label is ours; the "3D" and compass buttons are drawn here with no Apple or Google marks. Facts printed, all supplied by the user: venue "60, Chowringhee Banquets" and the address "60, Chowringhee Road, Bishop Lefroy Rd, Kolkata, West Bengal 700020". No date or time (user choice), no price, no lineup. Layout (user, 2026-10-19: no pill, lockup in the footer like the reference chat slide, mask back on the card, no edition line): LIVE badge top left, the map card with the copper mask lying across its top-right corner (the placement the user preferred over a top-right mask), the reveal copy (the venue, the address, then a plain bold line ON THE ROOFTOP; the event is on a rooftop, user 2026-10-19). Three earlier wordings were tried and rejected by eye (THE ROOFTOP AT above the venue, a gold ROOFTOP pill, and a callout on the map pin); `dd_location_reveal.py` keeps them behind the `ROOFTOP=` switch (default `below`), then the DISCO DIWALI lockup WITH its ball as a small footer mark. No LINK IN BIO pill, no MASQUERADE SANGEET EDITION line, no LOCATION REVEAL label. The map card is 960px wide (a tilted box ~995px), the hero. The inspo's Memoji pin avatar is not used; the red venue pin in the screenshot carries the pointing. Lessons: size the feed stack from the room left (the first build ended at y=1432 on a 1350 canvas, caught by the gate); a headline at the story's full size sat 50px from the edge, so 90px. The "Turf XL, New Alipore" in the TerraThon scripts is where the ticket STALL is, not the event venue.

### Date + time reveal poster (2026-10-19) — `scratchpad/dd_date_reveal.py`, JPEGs in `sample_outputs/disco_diwali_date/`
Feed 1080x1350 and story 1080x1920 from a user inspo (a headline over a photo with a calendar-event card floating under it). The headline teases (BLOCK YOUR CALENDAR, then TWO DAYS AFTER DIWALI / ONE DAY BEFORE BHAI DOOJ, supplied by the user 2026-10-19. UNVERIFIED AGAINST A KOLKATA PANCHANG: Diwali 2026 is Sunday 8 November, but several web sources list Bhai Dooj on 10 November, which would make the event day itself Bhai Dooj; Bengal's Bhai Phota may fall a day later. Confirm before posting) and a drawn white calendar card reveals: "Tue, 10 Nov 2026" (the weekday is DERIVED from the supplied date), hour lines 4, 5 and 6 PM, and one periwinkle event block (DISCO DIWALI, MASQUERADE SANGEET EDITION, 4:30 PM ONWARDS) that starts half way between the 4 and 5 PM lines and runs off the card's bottom edge, because the supplied time has no end. The card is a drawn UI device, not a screenshot (no Google or Apple marks); the periwinkle exists only as the calendar's own colour. Same family as the location poster: diya ground, string lights, LIVE badge, copper mask across the card's top-right corner, the lockup with its ball as a footer mark, no pill. No venue, price or lineup. Lesson: a 3-hour calendar card needs a half-hour offset, not a guessed pixel, to make "4:30" read right.

### Carousel cover (2026-10-19) — `scratchpad/dd_cover.py`, JPEG in `sample_outputs/disco_diwali_cover/`
Cover for the three-slide set (ALL FOR CHARITY, date reveal, location reveal), v4. History: v1 calm lockup (rejected, "make it fun"), v2 IT'S HAPPENING. over the three real slides fanned like cards (LIKED, but it leaked the date and the location), v3 the cards removed (rejected, "i liked the one before"). v4 keeps v2's composition and hides the secrets: the ALL FOR CHARITY card is shown as is, the date card and the location card are BLURRED (22px, darkened, scaled up so no edge text survives) behind a big "?". Checked by eye at full size: no date, map or text survives. Headline IT'S HAPPENING. is the user's brief expressed as copy, a claim of nothing but the event existing. Lessons: a teaser must be checked for what it LEAKS, not just what it shows; when a user rejects a change they asked for, the thing they liked was the composition, so keep it and fix only the offending element. **Story cut (2026-10-19):** `dd_cover.py` now renders both `cover.png` (1080x1350) and `story.png` (1080x1920) from one `build(H)`: second plate flipped and faded in (format rule 8), LIVE badge and lockup moved below Instagram's top 200px, cards 370x462, headline 108/148px so HAPPENING. keeps ~40px side margins, last element ends at y=1650 (reply bar zone starts at 1670). JPEGs: `sample_outputs/disco_diwali_cover/{cover,story}.jpg`.

### ALL FOR CHARITY poster, matched to the carousel (2026-10-19) — `scratchpad/dd_charity.py`, JPEGs in `sample_outputs/disco_diwali_charity/`
Feed and story. The earlier charity slide was a block inside `dd_carousel_captcha.py` (a different carousel) and did not match the date and location posters, so it was rebuilt on their skeleton: small LIVE badge top left, ALL FOR CHARITY headline with the edition line under it, the lockup (with its ball) as a footer mark, no pill, no link. **No card on this slide (user, 2026-10-19)**: a first version put the LIVE badge on a white card with the mask on its corner; the user asked for no cards, so the copper mask became the hero, then **ALL FOR CHARITY must be the highlight (user, 2026-10-19)**: the headline is now the hero at 205px (~960px wide, near full frame width) and the mask supports from the top-right corner at the poster_ref position, smaller (visible 520x342). A slide's hero is whatever the user names, not whatever is the largest asset. Lesson: `live_badge.png` is SEMI-TRANSPARENT over black, so on a white card it washes to grey and its white text nearly vanishes (it needs an opaque black tile); at its native small size on the diya ground it is fine, which is how every other poster uses it. The cover's first card reads this file. Only supplied facts: ALL FOR CHARITY and the edition.

### WhatsApp "reveal is tomorrow" poster (2026-10-19) — `scratchpad/dd_wa_reveal.py`, JPEG in `sample_outputs/disco_diwali_wa_reveal/`
1080x1350, built from the carousel cover (`dd_cover.py`): lockup with ball, LIVE badge, the three fanned cards (ALL FOR CHARITY slide as is, date and location slides blurred behind "?"), the edition line, and the headline THE REVEAL IS TOMORROW. The cover's SWIPE pill is dropped (nothing to swipe on WhatsApp) and the cards are slightly bigger. It prints NO date and NO location: they are what tomorrow reveals. "Tomorrow" is the user's own statement and no calendar date is asserted, so the poster is only valid the day before the reveal. The `CLIPPED img` notes in the render log are intentional (the blurred slides are scaled 1.15x inside their cards so no edge text survives). Post this the day before the reveal, then retire it.

### Carousel photo backgrounds (2026-10-20) — `scratchpad/dd_photo_bg.py`
User: "use a photo in the bg of the carousel", then "remove the blue diya lamp texture". The four carousel posters (cover, charity, date, location, feed and story) now sit on a real event photo instead of the diya plate: the photo graded dark (contrast 1.08), a navy-to-black scrim (heavier top and bottom so type reads), the string lights, gold dust and film grain. The navy diya texture is OFF (`plate_opacity=0`; the helper can still screen it in, and each script's `BG=diya` env restores the old ground). Frames, chosen for atmosphere with small or turned faces: cover `14_04` (hall, purple chandelier ceiling), charity `07_03` (red-drape entrance), date `14_07` (purple hall), location `07_12` (dark hall, star balloons). A first location frame (`07_09`, the courtyard crowd) read as the backs of heads and was swapped. The cover's blurred cards read the exported slide JPEGs, so re-render the slides and export them BEFORE the cover. Consent caveat applies: event photos show people, several apparent minors, with no consent record. The WhatsApp reveal-tomorrow poster still uses the diya ground.

### Copper stickers instead of the repeated mask (2026-10-20) — `scratchpad/dd_copper.py`, texture `engine/assets/disco_diwali/copper_texture.jpg`
User: "use different stickers instead of the mask again and again, create something of your own of the same red copper metal style", then "make the sticker look like the mask". The carousel slides no longer all carry the mask: charity gets a HEART, date a CALENDAR (first a four-point sparkle star), location a map PIN (first a DIYA lamp), each on the corner where the mask sat. The user then asked for "a sticker for calendar and location pin" and for ALL the stickers as PNG: `scratchpad/dd_sticker_export.py` renders heart, star, diya, calendar and pin as transparent PNGs (3x, NO drop shadow so they sit on any ground, trimmed to content) into `sample_outputs/disco_diwali_stickers/copper_*.png`. Bug caught on the way: the calendar's gem gradient id was defined only inside the pin's defs, so the calendar's gem rendered as an empty ring until it got its own. Lesson: v1 drew the metal as flat vector gradients with drawn scrolls, glitter and a gem, and it read as cartoon next to the photographed mask; a vector can imitate the colour but not the surface. v2 BORROWS the surface: `copper_texture.jpg` is a patch cut from `mask_copper.png` (its beaded filigree, region 215..535 x 395..555 of the 1680x1278 asset), mirror-tiled to 1024x512, clipped into each new silhouette with a pearl-bead rim like the mask's own edge, a dark inner edge, a diagonal glint and a drop shadow. The diya flame is drawn. Rotation is baked into each SVG. The mirror tiling makes a visible kaleidoscope symmetry at close range; a second patch (D, 230..520 x 340..470) is a candidate for a less symmetric look. The cover has no mask, so it needed no sticker; its first card shows the new charity slide. The reveal-tomorrow WhatsApp poster is unchanged.

### Standing rule: a different background every time (user, 2026-10-24)
Every new Disco Diwali poster gets a background photo no earlier poster used. Before picking, check the table: photo ref (`14_NN` hall set, `07_NN` unsorted set, see `scratchpad/dd_photo_bg.py`) -> poster. Used so far: 14_01 gajra & jhumka; 14_04 charms (v2), 07_09 bedazzling diyas; 07_12 cosmic experience and DIY mask & touch up station; 07_03 live dhol; 14_09 crochet stand; 14_06 gajra & jhumka (rejected, faces); 14_07 masquerade experience; 07_05 nails/press-ons/face glitter; 07_08 period pain stimulator; 07_13 photobooth; 14_03 sponsor invite story; 14_08 nails stall call; 14_05 puchka stall (07_11 rejected, faces); 07_06 charms (rejected). Prefer frames with backs of heads or ceilings behind the headline, never a large close face.

## 6. Conflicts with CLAUDE.md and how they were resolved (precedence ladder, sec 2)
- Ground, palette and fonts differ from the AQ house style. Resolved as a format exception, like TerraThon. The format wins inside `discodiwali.py` only.
- Film grain over a dark ground is photographic texture with a job to do, not a faint patterned wash. `wash_scan` did not flag it.
- Real-assets-only rule honoured: every image is supplied. The one drawn asset, `mask_red.svg`, is flat vector art, not a fabricated photo.

## 7. Operator quickstart
```python
import asyncio, discodiwali as dd            # run from engine/ or put engine/ on sys.path
asyncio.run(dd.render_poster("announce", dict(edition="Masquerade Sangeet Edition", date="10th November, 2026",
    time="4:30 PM Onwards", status="Ticket sales open soon", cta="Link in bio"),
    "feed", "out/discodiwali/announce.png", style="diya", mask="copper"))
```
Teaser demo set: `out/discodiwali/teasers/`. Kinds and their required fields are in `REQUIRED`. `days_to_go("2026-11-10")` derives a countdown from the date. `python engine/discodiwali.py` renders the whole demo set to `out/discodiwali/`.
Always LOOK at the PNG before it ships (CLAUDE.md sec 3).

## 8. Open items
- Navy diya landscape plate (for LinkedIn). A LinkedIn kind is not built yet.
- A lineup / performers kind, once a lineup is supplied.
- Eina vs the reference's wide grotesque: identify the real face and add it if it can be licensed.
- Consent for any real event photos before a recap kind (see `engine/assets/img/events/README.md`).
