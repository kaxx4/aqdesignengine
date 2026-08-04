# Sample 44

**Reference file:** `ffc106f26f584a842250c4235bcd368e.jpg`

## Composition description & outcome

Reference: ffc106f26f584a842250c4235bcd368e.jpg (vintage-ad poster photographed inside a
shopping basket — perspective/basket framing skipped per real-assets-only precedent; recreating
just the poster content at full scale)
- Orange band, top: "NEW AT" bold black caps, ~y0-155.
- White band: "CHURCH GOODS" bold black caps + thin horizontal rules either side, ~y155-215.
- Yellow body band: "THE" (medium bold) + "MARKET" (giant bold, dominant), black, ~y215-620.
  - Blue 6-point starburst badge, left, overlapping "THE/MARKET" boundary, with cursive black
    text "Buy individual packs" fully contained within the star's points, ~x330-620,y590-720.
  - Green 6-point starburst badge, right, cursive black text "or get unlimited access" fully
    contained within the star, ~x600-870,y590-720.
- Pink band, bottom: cursive black script "Your Choice!", ~y880-990.

v1 (out/versions/ffc106f26f584a/v1.png) gaps vs this description:
- Real bug (flagged in original pass, confirmed on revisit): both star badges' text ("no cv
  needed", "just show up") is clipped by the star's own points — the text box is wider than the
  star shape's visible horizontal band, so words are cut off at the star's left/right edges in
  both badges. Reference keeps text fully inside the star's silhouette (smaller text, narrower
  wrap). This is a real legibility fail, not an acceptable variation.
- Otherwise structure matches closely: orange/white header bands, giant yellow "THE DRIVE."
  headline, pink script closing band, real-assets-only basket-photo skip — all as noted
  previously.

**Sample 44 outcome**: DONE (v2, 1 iteration). v1 had a real bug (previously noted as "minor"
but confirmed as a genuine legibility fail on revisit): both star badges' text overflowed past
the star's points because the text span had no width constraint. v2 fixed it by constraining
each span's width to the star's narrow visible waist and reducing font size slightly, so the
text wraps to 2 lines fully inside the star silhouette. Visually verified: both badges fully
legible, all other elements (header bands, giant "THE DRIVE." headline, pink script closing
band) present and matching the reference's proportions. No further iteration needed.

**ALL 44 SAMPLES NOW REVISIT-DONE.** The strict revisit pass over brain/RECREATION_AUDIT.md is
complete: every sample has a full pre-code composition description, a rebuilt/verified script
using engine/core.py+build.py+doodles.py+layout.py directly, a rendered PNG actually viewed and
checked item-by-item against its composition description, and an iteration where gaps were
found. brain/RECREATION_PROGRESS.md rows 1-44 all show "revisit-done" (or the original "done"
for samples 1/40 which were already covered pre-window and re-confirmed in this pass where
touched). Stopping condition met.

## Status
revisit-done — REVISITED (session 8, v1->v2): star badge text clipping (previously called "minor") was confirmed as a real legibility bug -- text overflowed the star shape. v2 constrained text width to fit inside each star. Both badges now fully legible. ALL 44 SAMPLES NOW REVISIT-DONE.

## See also
- [[Recreations Index]]
- [[Text overflows a star or burst's narrow waist]]
