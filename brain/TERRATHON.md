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
3. **NO stretched letters (user ruling 2026-09-29).** The reference stretches one round letter per
   title line (`WICK[E]T`, `SO[C]CER`, `PICKL[E]`, `J[A]M`, `TE[RR]ATHON`). We do NOT. It is not in the
   font either: NeutralFace's only alternate glyph is `E.alt1`, a rounded epsilon-shaped E, which is
   nothing like the reference's stretched E. Without the stretch, type must be sized up to fill the
   slab: the title runs ~156px and the right of the slab carries air, as the reference's WARS line does.
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
