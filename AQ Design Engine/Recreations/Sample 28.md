# Sample 28

**Reference file:** `abb2ab5d1194e22f4dfbda71dcd98d9f.jpg`

## Composition description & outcome

Reference: abb2ab5d1194e22f4dfbda71dcd98d9f.jpg ("jazz Spring Show" poster, Matisse cut-paper style)
- Background: solid off-white/cream, no texture.
- Scattered bold word-fragments at varied scale/rotation/color, layered as the dominant
  structure (not a single headline block):
  - "jazz" — huge, dark navy, top-left, slight skew, ~x40-290,y15-130.
  - "Spring" — huge, dark navy, mid-right diagonal cursive-ish sans, ~x380-720,y440-650,
    rotated so it reads diagonally down-right.
  - "SHOW" — huge, dark navy bold caps, lower-left, ~x30-330,y690-820.
  - Small caption block top-left under "jazz": 2 lines Chinese small text, ~x150-330,y150-200.
  - Small caption block top-right: 2-3 lines mixed Chinese/English small text (artist credits),
    ~x480-720,y50-140.
  - Purple/lavender hexagon date-card: "27-28 / January 2023 / 16:00 START", ~x385-545,y195-350.
  - "FREE ADMISSION 自由參加 @ 1F, Wave Towers 音浪塔一樓" small caption, left-mid, ~x30-320,y460-505.
  - "爵對有春" (large Chinese title chars), bottom-right, bold navy, ~x430-720,y940-1010.
- Organic Matisse-blob shapes (flat single-color cutout flowers/splats), scattered, varied
  rotation, z-order interleaved with the word fragments:
  - Yellow 5-petal flower, top-right corner, ~x585-720,y10-100, rotation ~+15deg.
  - Pink squiggle/ribbon double-curve, top-center, ~x365-475,y40-105.
  - Red 6-petal flower (large hero blob), left-mid, ~x25-260,y150-330, rotation slight.
  - Small light-blue hexagon, left, ~x25-90,y360-410, partially behind red flower.
  - Green wavy ribbon/arrow shape connecting red flower to hexagon date-card, ~x230-400,y270-360.
  - Green squiggly "S" ribbon blob (large), right side, ~x555-720,y250-390.
  - Yellow thin wavy squiggle line, right side below green ribbon, ~x635-715,y365-455.
  - Small navy megaphone icon (bullhorn, pointing left), left-mid, ~x30-230,y470-560.
  - Small pale-blue hexagon outline/fill, left, repeated motif, ~x30-90,y360-410 (see above).
  - Navy "eyelash" doodle (curved lash marks + dot), center, ~x360-450,y620-660.
  - Small navy hexagon w/ blue dot inside, center-left, ~x190-250,y790-840.
  - Yellow 4-line "speed lines"/hatch mark cluster, lower-mid, ~x510-565,y850-900.
  - Large magenta/pink starburst (8-point jagged star) with small light-blue flower center,
    bottom-right, ~x480-720,y660-820.
  - Green wifi-signal arc icon (concentric quarter-arcs + dot), bottom-left, ~x30-190,y660-780.
- Footer: two small logo marks bottom-left (music-center logo + jazz-records logo), ~y960-1010.
- Overall density: shapes and word-fragments overlap tightly with almost no empty gaps across
  the full canvas height; nothing below y1010 of the ~1035px reference is truly dead space.

v1 (out/versions/abb2ab5d1194e2/v1.png) gaps vs this description:
- Large dead zones: y200-870 in the right/center area is nearly empty (only 3 small shapes:
  hexagon date-card, zigzag squiggle, pink star+DRIVE), and y1400-1750 between DAY and the
  arrow/caption row is empty. Reference has near-zero dead space; v1 is much sparser overall.
- Missing doodle vocabulary present in reference: no megaphone icon, no wifi-signal-arc icon,
  no eyelash doodle, no small hexagon+dot motif, no speed-line hatch cluster.
- Word-fragment scatter (AQ/DRIVE/DAY/SHOW UP) is a reasonable structural echo of
  jazz/Spring/SHOW but v1 has only 4 words vs reference's tighter interleaving of word+blob
  layers — needs more blob variety and tighter spacing to match density.

**Sample 28 outcome**: DONE (v3, 2 iterations). v1 had large dead zones (y200-870 and
y1400-1750 nearly empty) and was missing the megaphone icon, wifi-signal-arc icon, eyelash
doodle, and hexagon+dot motif from the reference's dense blob/word scatter. v2 added a pink
squiggle ribbon, green wifi-arc SVG, a proper megaphone SVG shape, an eyelash SVG doodle, a
hexagon+dot motif, and a yellow speed-line cluster — but the hexagon+dot used CSS
clip-path+border which doesn't render a clean outline in Chromium (rendered as broken bracket
shapes). v3 fixed it with an SVG polygon outline instead. Visually verified: all listed
composition elements present, density now closely matches the reference's near-zero-dead-space
scatter. No further iteration needed.

## Status
revisit-done — REVISITED (session 8, v1->v3): v1 had large dead zones and was missing megaphone/wifi-arc/eyelash/hexagon-dot doodles present in the reference's dense scatter. v2 added all of these (fixing a clip-path+border rendering bug for the hexagon in v3). Density now matches reference closely, all verified present.

## See also
- [[Recreations Index]]
- (none logged)
