# DISCO DIWALI FORMAT (v1, 2026-10-13)

The poster family for AQ's Disco Diwali charity party. Built as a FORMAT MODULE, `engine/discodiwali.py`, the same shape as `dispatch.py`: one skeleton, a validated content dict, a solved layout. Self-test: `scratchpad/test_discodiwali.py` (53 assertions). Operator quickstart is section 7.

Status: the 2026 announcement was recreated from its reference and accepted by the looking gate (`scratchpad/dd_announce.py`, v2). The module generalises it to five kinds, two canvases and three visual directions. Rules marked PROVEN were each caught by a render and fixed.

## 1. Facts supplied (the only source for copy)
- Disco Diwali 2026, "Masquerade Sangeet Edition", 10th November 2026, 4:30 PM onwards.
- "Ticket sales open soon", "More details soon", CTA "Link in bio". All for charity.
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
