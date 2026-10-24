"""STARRY NIGHT 2.0 highlights in the AQ EVENT style (black ground, gold flecks, full-bleed photo fading to black,
mint mono step chip, one marked/ringed accent per headline, mono footer). Workflow C, bespoke. Feed 1080x1350 + story 1080x1920.
Reuses the helper block of gen_why_we_do_v1.py and photo_full of gen_events_vibe_v1.py (same event series look).
Facts used (brain/SPONSORSHIP_DECKS.md, scratchpad/gen_rever_deck.py): Starry Night 2.0, 26 December, Sky Turf, DJ Rajiv, 550+ guests.
Landscape photos are cover-cropped with a measured focal point (the natural-aspect variant left a dead black middle).
"""
import os, sys, asyncio, io, base64
_HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(_HERE, "gen_why_we_do_v1.py")).read().split("# ====================== CAROUSEL")[0])
_ev = open(os.path.join(_HERE, "gen_events_vibe_v1.py")).read().splitlines()
_s = next(i for i, l in enumerate(_ev) if l.startswith("def step_chip")); _e = next(i for i, l in enumerate(_ev) if l.startswith("async def type_slide"))
exec("\n".join(_ev[_s:_e]))
from PIL import Image
OUT = "out/starry2_event"; os.makedirs(OUT, exist_ok=True)
SRC = "scratchpad/carousel_2026/starry_night_2/src_images/"
def pimg(path, maxw=1500):
    im = Image.open(path).convert("RGB")
    if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), im.height / im.width
GREEN, GR = pimg(SRC + "00.jpg"); FRIENDS, FR = pimg(SRC + "01.jpg"); SQUAD, SR = pimg(SRC + "02.jpg")
DJ, DR = pimg(SRC + "03.jpg"); CROWD, CR = pimg(SRC + "04.jpg"); COVER, COR = pimg(SRC + "05.jpg")

SLIDES = [  # name, photo, pos, natural_r, chip, lines, sub, cta
 ("01_cover", COVER, "50% 35%", None, "26 DEC · SKY TURF", [("STARRY NIGHT", "STARRY NIGHT"), ("2.0", mark("2.0"))], ["one night. one sky of lights."], None),
 ("02_floor", GREEN, "50% 30%", None, "ON THE FLOOR", [("HANDS UP.", "HANDS UP."), ("NO NOTES.", ring("NO NOTES."))], ["the whole floor, on its feet."], None),
 ("03_squad", SQUAD, "45% 40%", None, "THE SQUAD", [("FRONT ROW,", "FRONT ROW,"), ("ALL SMILES.", mark("ALL SMILES."))], ["fairy lights behind, wristbands on."], None),
 ("04_deck", DJ, "60% 50%", None, "ON THE DECKS", [("DJ RAJIV", "DJ RAJIV"), ("RAN THE NIGHT.", mark("RAN THE NIGHT."))], ["the stars hung above the dance floor."], None),
 ("05_crew", FRIENDS, "48% 50%", None, "THE CREW", [("FRIENDS,", "FRIENDS,"), ("ONE FRAME.", ring("ONE FRAME."))], ["caught between songs."], None),
 ("06_close", CROWD, "50% 40%", None, "SEE YOU NEXT TIME", [("550+ GUESTS.", "550+ GUESTS."), ("ONE SKY.", mark("ONE SKY."))], ["starry night 2.0, 26 december."], "follow @ngo.aquaterra"),
]
async def main():
    async with B.session():
        for fmt, (W, H, size) in dict(feed=(1080, 1350, 100), story=(1080, 1920, 112)).items():
            for name, src, pos, nr, chip, lines, sub, cta in SLIDES:
                global OUT
                await photo_full(f"{fmt}_{name}", W, H, src, pos, chip, lines, sub, hash(name) % 90, size=size, natural_r=nr, cta=cta)
asyncio.run(main())
