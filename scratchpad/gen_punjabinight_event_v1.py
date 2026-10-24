"""PUNJABI NIGHT 2025 highlights in the AQ EVENT style (black ground, gold flecks, full-bleed photo fading to black,
mint mono step chip, one marked/ringed accent per headline, mono footer). Workflow C, bespoke. Feed 1080x1350 + story 1080x1920.
Reuses the helper block of gen_why_we_do_v1.py and photo_full of gen_events_vibe_v1.py (same event series look).
400+ guests and Jun 2025 come from brain/SPONSORSHIP_DECKS.md; captions describe each photo.
Landscape photos are cover-cropped with a measured focal point (the natural-aspect variant left a dead black middle).
"""
import os, sys, asyncio, io, base64
_HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(_HERE, "gen_why_we_do_v1.py")).read().split("# ====================== CAROUSEL")[0])
_ev = open(os.path.join(_HERE, "gen_events_vibe_v1.py")).read().splitlines()
_s = next(i for i, l in enumerate(_ev) if l.startswith("def step_chip")); _e = next(i for i, l in enumerate(_ev) if l.startswith("async def type_slide"))
exec("\n".join(_ev[_s:_e]))
from PIL import Image
OUT = "out/punjabi_night_event"; os.makedirs(OUT, exist_ok=True)
SRC = "scratchpad/carousel_2026/punjabi_night_2025/src_images/"
def pimg(path, maxw=1500):
    im = Image.open(path).convert("RGB")
    if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), im.height / im.width
COVER_FILE = SRC + "cover.jpg"   # the separate cover photo; slides 02-06 render without it until it is supplied
P = {n: pimg(SRC + f"{n}.jpg")[0] for n in (19, 20, 21, 22, 23)}
SLIDES = [  # name, photo, pos, natural_r, chip, lines, sub, cta
 ("02_dhol", P[22], "50% 50%", None, "DHOL ON", [("DHOL ON.", "DHOL ON."), ("FEET UP.", mark("FEET UP."))], ["two drums, sunglasses and a lot of dancing."], None),
 ("03_deck", P[23], "50% 40%", None, "ON THE DECKS", [("POINTING BACK", "POINTING BACK"), ("AT THE CROWD.", ring("AT THE CROWD."))], ["behind the console, headphones round the neck."], None),
 ("04_floor", P[19], "50% 60%", None, "ON THE FLOOR", [("FLOOR FULL,", "FLOOR FULL,"), ("LIGHTS LOW.", mark("LIGHTS LOW."))], ["silver balloons overhead, green and amber light."], None),
 ("05_spray", P[20], "50% 45%", None, "SPRAY IT", [("SPRAY CAN,", "SPRAY CAN,"), ("NO RULES.", ring("NO RULES."))], ["a white tee, a can of colour, one steady hand."], None),
 ("06_close", P[21], "70% 55%", None, "SEE YOU NEXT TIME", [("400+ GUESTS.", "400+ GUESTS."), ("ONE SELFIE.", mark("ONE SELFIE."))], ["punjabi night, 2025."], "follow @ngo.aquaterra"),
]
if os.path.exists(COVER_FILE):
    SLIDES.insert(0, ("01_cover", pimg(COVER_FILE)[0], "50% 40%", None, "JUN 2025", [("PUNJABI NIGHT", "PUNJABI NIGHT"), ("2025", mark("2025"))], ["one night. a lot of dhol."], None))
async def main():
    async with B.session():
        for fmt, (W, H, size) in dict(story=(1080, 1920, 112), feed=(1080, 1350, 100)).items():
            for name, src, pos, nr, chip, lines, sub, cta in SLIDES:
                if fmt == "feed" and not name.startswith("01_"): continue   # feed size is for the cover only
                global OUT
                await photo_full(f"{fmt}_{name}", W, H, src, pos, chip, lines, sub, hash(name) % 90, size=size, natural_r=nr, cta=cta)
asyncio.run(main())
