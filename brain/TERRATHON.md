# TERRATHON: the design system (session started 2026-09-29)

TerraThon is AQ's multi-sport and gaming fest, **3rd and 4th October 2026**, with per-event
posters. Confirmed events so far: **Wicket Wars** (cricket, Turf XL, 3rd and 4th) and **Soccer
Storm** (FIFA, Battleground Gaming, 3rd). The sticker pack also carries basketball and pickleball
objects, so those events probably exist. That is inference, not fact, until the user confirms.

Reference set: `training_samples/terrathon/` (4 posters, 1600x2000 = 4:5, plus `aq_live_sticker.png`).
Each event has two variants that differ ONLY in the CTA pill: `LINK IN THE BIO` vs `LINK BELOW`.

## 1. What this is: a FORMAT, not four one-off posters

Wicket Wars and Soccer Storm share one skeleton to the pixel: the same star positions, the same
slab position and tilt, the same header block. Only the hero sticker, the title, and the
numbers and venue change. That makes TerraThon a **format module** in the sense of
`engine/dispatch.py` (CLAUDE.md §10, session 10g), not a Workflow B recreation target. The right
end state is `engine/terrathon.py`: validate a brief, solve the layout from measured content,
and take content as the only hand-input. Recreating the two references is the way we learn the
constants. It is not the deliverable.

## 2. The skeleton (fractions of the canvas; measured, `compare.geometry`)

| Layer (back to front) | What | Position |
|---|---|---|
| Ground | pure `#000`, fine white speckle grain | full bleed |
| Shuriken x4 | blue 4-point star, cream halo, ~7% wide, each rotated differently | top-right (0.89, 0.16), upper-left (0.15, 0.28), right-mid (0.88, 0.44), lower-left (0.06, 0.53) tucked under the slab corner |
| Hero sticker | one die-cut sport object, green fill, cream halo, 45-55% of canvas height | centred (~0.5, 0.36), **its bottom is hidden behind the slab** |
| Slab | white rounded rectangle, ~2% orchid border, tilted about -1.5 deg | x 0.05..0.96, y 0.54..0.80 |
| Title | event name in extended black display, 2 lines, then subtitle `A <SPORT> TOURNAMENT` | inside slab, left-aligned |
| Header | `PRIZE POOL:` light, `RS. N` heavy with winged-money emoji, two prize lines | top centre-left, y 0.05..0.23 |
| Fest tag | white pill, orchid border, `TERRATHON` | top-right, y 0.04..0.10 |
| Info | calendar + date, pin + venue, then fee line | y 0.82..0.93 |
| Footer | AQ logo bottom-left, CTA pill bottom-right (cream fill, orchid border) | y 0.94..0.99 |

Measured: content bbox spans x 0.013..0.987, coverage 0.43 to 0.47, centroid (0.52, 0.57).
Two posters, same skeleton, so the centroid barely moves (0.577 vs 0.566 vertically).

## 3. The rules this teaches

1. **Weight pairing: label light, value bold.** `PRIZE POOL:` is light and `RS. 7,500` is heavy.
   `WINNER:` is light and `RS.4,500` is bold. `PARTICIPATION FEE` is light and `RS. 2,100` is bold.
   `FOR A` is light and `TEAM OF 8` is bold. The value is always the heavier word. This is the
   whole hierarchy of the info areas, with no colour or size change needed.
2. **The hero is tucked, not placed.** The slab overlaps the sticker's bottom edge. It reads as
   an object standing in a tray. Never float the hero clear of the slab.
3. **One stretched glyph per title line.** A round letter (E, A, C, O) is scaled horizontally
   3 to 4x into a capsule (`WICK[E]T`, `W[A]RS`, `SO[C]CER`, `ST[O]RM`). It is a signature, and it
   needs a `type_stretch` primitive. The engine has none.
4. **Constant furniture, variable hero.** The four shuriken never move between events. They are
   the series' fingerprint. Only the hero, the title and the numbers change.
5. **Every sticker gets the same die-cut treatment**: cream halo (`#F3ECDE`), no ink outline, flat fill,
   rough hand-cut edge (`shapes.sticker` produces a smooth halo, so it needs an edge-roughening step).
6. **Emoji are used as icons** (winged money, medals, calendar, pin). They are raster glyphs, not
   engine doodles. See the decision list below.
7. **Numbers add up, and that is checkable.** 4,500 + 3,000 = 7,500 and 1,500 + 1,000 = 2,500.
   A brief validator should reject a prize split that does not sum to the pool.

## 4. Palette (sampled from the pixels)

| Role | Reference | Nearest AQ token | Gap |
|---|---|---|---|
| Ground | `#000000` | `core.INK` `#0A0A0A` | negligible |
| Hero green | `#2FD284` | `--mintbright` `#00E5A0`, `ACCENTS[1]` mint `#1B8A5A` | neither; it sits between them |
| Slab border, pill borders, CTA border | `#DE68F0` (orchid) | `ACCENTS[0]` pink `#FF4D8C`, `ACCENTS[5]` grape `#7E5BFF` | **no orchid in the palette** |
| Star blue | about `#0396FF` (sticker pack) | `ACCENTS[4]` sky `#3DA9FC` | close but more saturated |
| Halo | `#F3ECDE` | `CREAM` `#F4EFE0` | match |
| Slab fill and text | `#F9F9F9` / `#F5F5F5` | `PAPER` `#FFFFFF` | near-white, not cream |

Proportions on the black ground: black 61 to 64%, near-white 15 to 16%, green 4 to 7%, orchid 4%.

## 5. Open decisions (need the user)

1. **Palette:** the sticker pack (orchid, bright green, saturated blue) is not the AQ accent
   set. Does TerraThon carry its own tokens (`core.TERRATHON_*`) as a sub-brand, or should we
   snap to `ACCENTS`? Snapping loses the orchid, which is the strongest thing on the page.
2. **The calendar emoji reads `JUL 17`** on posters dated 3rd and 4th October. That is the
   emoji's fixed artwork, not a date. It is wrong on the live posters. Replace it with a drawn
   date chip or an emoji that shows no date.
3. **Subtitle face** (`A CRICKET TOURNAMENT`) is a chunky display slab that is not one of the four
   AQ fonts. Is it a licensed font we can embed, or should we substitute NeutralFace?
4. **Real assets:** the sticker pack (smiley, flower, basketball, pickleball, controller, cricket
   set) must exist as files in the repo. Images pasted into a chat mid-turn were not persisted.

## 6. Build plan

1. Ingest the sticker pack to `assets/terrathon/` and measure each (bbox, halo width, fill).
2. Workflow B on `wicket_wars_bio` (bespoke script, v1 to converge) to learn the constants.
3. Encode `type_stretch` and rough-edge halo as primitives (CLAUDE.md §8), with a self-test.
4. `engine/terrathon.py`: brief in (event, sport hero, numbers, venue, CTA), poster out, with a
   validator (prize split sums, date range formatted, fee text).
5. Same module drives the rest of the lifecycle (teaser, results, thank-you), which the
   messaging skill already defines as a chain.
6. Companion `/canvas-design` piece per the standing rule (outstanding).
