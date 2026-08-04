# Sample 26

**Reference file:** `8988345ad4963ec66e5754c8c5441f56.jpg`

## Composition description & outcome

Reference: 8988345ad4963ec66e5754c8c5441f56.jpg ("Sticker Kit")
- Background: flat light gray (#E9E8E6-ish), no texture.
- Top-left: "Sticker Kit" header text, large bold sans, dark gray, ~y40-70.
- Top-right: dark pill badge "1/3" (page counter), rounded, gray fill white text, ~x670-730,y30-65.
- Sticker cluster (loosely piled, overlapping, varied rotation), roughly z-ordered top-to-bottom
  as physically stacked (later listed = higher z / on top):
  1. Googly-eyes rounded-square sticker (white bg, black border, two black-ringed eyes with
     black pupils) — top-left area, ~x110-210,y195-280, slight white drop-shadow/outline (sticker
     die-cut look), rotation ~-5deg.
  2. Blue oval sticker "anti-social but / user-friendly" (cursive italic 2nd line) — royal blue
     fill, white text, ~x225-470,y135-235, rotated ~+8deg, positioned overlapping/behind eyes.
  3. White rect sticker "Out of Office" bold black text with small corner selection-handle marks
     (crop-tool style corner brackets, purple) — ~x160-390,y255-310, rotation ~-3deg, sits atop
     the blue oval's bottom edge.
  4. Orange/red flame emoji-style sticker (flat orange flame shape, white die-cut outline) —
     ~x415-480,y225-300, rotation ~+3deg, sits to the right of Out-of-Office tag.
  5. Blue globe/world sticker (circular, blue grid-line globe icon with googly eyes on it,
     black outline) — ~x510-610,y210-345, rotation 0.
  6. Red heart sticker with white "⌘" (command-key) symbol cut into center — ~x120-270,y330-460,
     rotation ~-8deg, sits behind/below Out-of-Office and flame.
  7. Red rect nametag sticker "HELLO, I'M" (small label) + "User Friendly" (large cursive
     signature) — white/red bg card, ~x270-520,y325-450, rotation ~-2deg, overlaps heart's
     right edge.
  8. Green peace-sign hand sticker (2-finger V, cartoon hand, black outline, light green skin
     tone) — ~x535-635,y335-450, rotation ~+10deg, to the right of nametag card.
  9. "I ❤️ MY JOB" text lockup (bold black sans + small red heart glyph) — ~x500-635,y480-565,
     no card/background, sits directly on the gray bg beneath globe/peace-hand.
  10. Purple peace-sign hand sticker — smaller, ~x90-175,y430-520, rotation ~-6deg, left side,
      below heart.
  11. Circular badge "Sand Studio & Co." with curved text along the badge's own circumference
      arcing around a smaller inset badge — off-white circle, black outline, black text,
      ~x290-460,y460-635, rotation slight.
  12. Cursor/arrow icon (small black filled cursor-pointer shape) — ~x95-130,y550-590, sits at
      the edge of the "Designer" pill.
  13. White pill sticker "Designer" (black outline, black bold text) — ~x115-275,y590-635,
      rotation ~-4deg, overlaps cursor icon's tail.
  14. Light-green oval sticker "Professional / Instance Detacher" (cursive + bold 2-line text)
      — ~x185-360,y635-715, rotation ~-3deg, bottom-left cluster.
  15. Yellow rounded-rect sticker "Please / Detach with care" + small keyboard-shortcut glyph
      row ("\ ⌘ B") — ~x420-675,y620-735, rotation ~+2deg, bottom-right.
  16. Dark teal peace-sign hand sticker — ~x390-460,y690-770, rotation ~-8deg, bottom-center,
      overlapping the green oval's right edge and yellow card's left edge.
- Footer row: "@sandstudio.co" bottom-left (small gray text), "Buy Now →" bottom-right (bold
  black text + arrow glyph) — ~y850, both sit on flat gray bg, no cards.
- Overall density: cluster occupies roughly the vertical middle 70% of canvas (y130-770 of a
  ~910px-tall image), quite tightly packed/overlapping with almost no gaps between stickers;
  header and footer are the only elements outside the cluster.

v1 (out/versions/8988345ad4963e/v1.png) gaps vs this description:
- Bottom half of canvas (~y1900-2700 at full 2160x2700 res) is completely empty — the reference's
  cluster fills much closer to the bottom edge relative to canvas height. v1 stops around y1650.
- Missing: googly-eyes sticker box, flame/fire sticker, cursor/arrow icon near the Designer pill.
- Heart sticker in v1 is a plain flat heart with no cutout symbol (reference has a white ⌘
  symbol cut into the heart's center) — acceptable minor simplification but should add a symbol
  for fidelity.
- Real bug (noted in progress tracker): the purple "thumbsup" doodle is placed ON TOP of the
  "...EER" pill, covering most of its text ("volunteer" reads as just "EER") — a genuine
  z-order/placement collision, not a style choice.
- Reference has 3 peace-sign hands (green/purple/teal); v1 substitutes 3 thumbsup icons in the
  same slots — acceptable doodle-vocabulary swap (peace-sign not in engine/doodles.py), keep.

**Sample 26 outcome**: DONE (v2, 1 iteration). v1 gaps: bottom half of canvas empty, missing
googly-eyes sticker, missing flame sticker, missing cursor/arrow icon, plain heart with no
cutout symbol, and a real z-order bug where the purple thumbsup doodle covered most of the
"volunteer" pill's text. v2 fixed the collision (repositioned the hand doodle clear of the
pill), added the googly-eyes sticker box, a flame-shaped accent, a small cursor triangle beside
the pill, a ⌘ symbol cut into the heart, and a new lower sticker cluster (circle badge, tag,
star, extra hand) filling the bottom half to match the reference's fuller vertical density.
Visually verified: all composition-description items present, "volunteer" pill fully legible,
no further iteration needed.

## Status
revisit-done — REVISITED (session 8, v1->v2): v1 had a real collision (thumbsup covering "volunteer" pill text), missing googly-eyes/flame/cursor stickers, plain heart with no cutout, and empty bottom half. v2 fixed the collision, added all missing stickers, and filled the bottom half with a new cluster. All verified present.

## See also
- [[Recreations Index]]
- [[Doodle-badge dropped over text or shape]]
