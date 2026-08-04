# Sample 36

**Reference file:** `ce6fdd94f81b3e6018bc80724ae4508e.jpg`

## Composition description & outcome

Reference: ce6fdd94f81b3e6018bc80724ae4508e.jpg ("ThriftHaus" event/brand moodboard)
- Background: solid black, no texture.
- Blue card, top-left: "AN EVENING WITH" bold caps + "ThriftHaus" italic serif wordmark,
  ~x55-365,y230-420.
- Pink oval "THRIFTHAUS" small tag + yellow circle "TH" mark, overlapping blue card's right
  edge, ~x185-345,y285-330.
- Orange/red card, top-right: small paragraph body text (justified caps), ~x360-645,y285-435.
- Purple cloud-shaped blob badge "TH" (large scalloped edge), top-right corner, ~x565-690,y230-355.
- Green sun/starburst icon (circle + radiating lines), right of purple blob, ~x570-670,y390-450.
- "20% OFF EVERYTHING" — "20%" in pink oval tag + "OFF EVERYTHING" bold black caps, left-mid,
  ~x55-365,y490-580.
- Small yellow cap/hat doodle icon, above "OFF", ~x120-175,y475-505.
- Small photo of folded jeans on white bg, ~x260-360,y495-565.
- Photo panel, right side: blue sky + green hill, 3 pairs of jeans hanging (product shot),
  "ThriftHaus" italic wordmark overlay, black outline flower doodle bottom-left, black outline
  squiggle/loop doodle, small price-tag card ("size 4, slim skinny, $30" + circular logo stamp)
  bottom-right — ~x360-690,y450-720.
- Photo, bottom-left: woman in overalls, arms raised, outdoor sky/field — ~x55-360,y610-850.
  Small yellow speech-bubble "TH" tag overlapping top-left corner of photo.
- Orange loop/coil squiggle doodle, bottom-left margin, ~x25-140,y800-870.
- Green pill tag "THRIFTHAUS" small, ~x310-430,y755-790.
- Yellow rotated tag "THANK YOU" bold black caps, ~x260-450,y755-810.
- Pink oval "THRIFTHAUS" large, bottom-right, ~x480-690,y775-840.
- Overall: dense collage cluster occupies roughly the top 80% of canvas (y230-870 of ~1100px),
  bottom ~20% is empty black margin.

v1 (out/versions/ce6fdd94f81b3e/v1.png) gaps vs this description:
- Real bug: the orange card's body text overflows behind/gets visually cut off by the purple
  "AQ" blob badge overlapping its right edge ("...OF TH", "WEL...", "...T...ONLY" all clipped
  by the badge sitting on top) — text is illegible where the badge overlaps.
- Real bug: the bottom-left photo's caption text "STANDING STEADFAST FOR THE ONES WHO NEED US
  MOST" is clipped at the photo's bottom edge — second line cut off.
- Structural swaps (real AQ photos instead of literal thrift-store product shots, AQ program
  copy instead of ThriftHaus copy) are acceptable per real-assets-only rule — keep.
- Missing decorative doodles: no flower, no squiggle-loop on the photo panel, no sun icon, no
  small jean/tag photo — but these were swapped for real-asset equivalents already (badges,
  zigzag) which is an acceptable simplification; the 2 clipping bugs are the real fails.

**Sample 36 outcome**: DONE (v2, 1 iteration). v1 had two real bugs: the orange card's body
text ran underneath and was clipped by the purple "AQ" badge, and the bottom-left photo's
baked-in caption ("standing steadfast for the ones who need us most") was cropped off at the
container's bottom edge because the container height didn't match the photo's true aspect
ratio. v2 narrowed the orange card's text column to end before the badge, and resized the photo
container to the photo's actual aspect ratio so the full caption is visible. Visually verified:
both cards fully legible, all composition elements present. No further iteration needed.

## Status
revisit-done — REVISITED (session 8, v1->v2): v1 had 2 real bugs -- orange card text clipped by the AQ badge, and photo1's baked-in caption cropped off by a mismatched container aspect ratio. v2 fixed both. All verified present and legible.

## See also
- [[Recreations Index]]
- (none logged)
