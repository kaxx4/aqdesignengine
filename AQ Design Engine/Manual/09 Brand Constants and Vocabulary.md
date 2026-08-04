# 9. Brand Constants and Vocabulary

**Colors** — bg cream `#F4EFE0` (NEVER white) · ink `#0A0A0A`. Accents (`core.ACCENTS`, index them
by `A[i]`), used as PUNCTUATION only (~30% of the piece, never a flooded field):
`A[0]` pink `#FF4D8C` · `A[1]` mint `#1B8A5A` · `A[2]` lemon `#FFC700` · `A[3]` tomato `#FF4D2E` ·
`A[4]` sky `#3DA9FC` · `A[5]` grape `#7E5BFF` · `A[6]` teal `#0E7C86`. (Also `--mintbright #00E5A0`.)

**Fonts** (embedded, referenced as CSS vars): `--d` NeutralFace 900 UPPERCASE (display/headlines) ·
`--e` Eina lowercase (body) · `--s` Instrument Serif italic (≤1 accent word per piece) · `--m`
JetBrains Mono (labels/eyebrows/footer). Headlines UPPERCASE, body lowercase, numbers can be heroes.

**Doodles** (`engine/doodles.py`, call via the `doodle()` helper): `star sparkle circle ring
thumbsup heart arrow squiggle zigzag burst plus lightning spiral dots speech cross globe leaf paw
tree`. Most take `(fill, rot, style="clean"|"rough", seed)`; `globe` takes no `fill`. Vary SIZES
(mix 60px and 160px, not all ~90px) and place only in measured free zones.

**Real photos** (`core.PHOTOS`, base64-embedded — the ONLY real imagery): `food` (food
distribution), `edu` (education Sundarban), `diwali` (fundraising), `xmas` (Christmas Khidirpur).

**Canvas sizes** (`core.SIZES`): `feed` (1080,1350) — the default · `story` (1080,1920) · `square`
(1080,1080).

**Logo** — `core.LOGO`, the real colored wordmark, top-left every slide (a pill on dark/photo
backgrounds; NEVER white-inverted).

**Real-assets-only rule (hard):** never fabricate stats, UI screenshots, QR codes, or stock/photo
imagery. If a reference used a fake asset, substitute a real AQ photo, a flat SVG illustration, or a
real CTA — and note the swap as an acceptable adaptation.

**Craft layer (always on):** thick ink outlines · hard-offset ink shadows · one hero-shine per piece
· halftone ONLY on photos (flat on solid colors) · 8px grid snap · snarky voice chips in dead zones ·
fill space by SCALING existing elements UP before adding filler doodles (filler is the last resort).

## See also
- [[10 The Bug Catalog]]

[[Manual Index]]
