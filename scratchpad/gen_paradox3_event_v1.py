"""PARADOX 3.0 (2025) highlights in the AQ EVENT style (black ground, gold flecks, full-bleed photo fading to black,
mint mono step chip, one marked/ringed accent per headline, mono footer). Workflow C, bespoke. Feed 1080x1350 + story 1080x1920.
Reuses the helper block of gen_why_we_do_v1.py and photo_full of gen_events_vibe_v1.py (same event series look).
No stats or dates (none sourced); captions describe each photo.
Landscape photos are cover-cropped with a measured focal point (the natural-aspect variant left a dead black middle).
"""
import os, sys, asyncio, io, base64
_HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(_HERE, "gen_why_we_do_v1.py")).read().split("# ====================== CAROUSEL")[0])
_ev = open(os.path.join(_HERE, "gen_events_vibe_v1.py")).read().splitlines()
_s = next(i for i, l in enumerate(_ev) if l.startswith("def step_chip")); _e = next(i for i, l in enumerate(_ev) if l.startswith("async def type_slide"))
exec("\n".join(_ev[_s:_e]))
from PIL import Image
OUT = "out/paradox3_event"; os.makedirs(OUT, exist_ok=True)
SRC = "scratchpad/carousel_2026/paradox_3_2025/src_images/"
def pimg(path, maxw=1500):
    im = Image.open(path).convert("RGB")
    if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), im.height / im.width
COVER_FILE = SRC + "cover.jpg"   # the separate cover photo; slides 02-06 render without it until it is supplied
P = {n: pimg(SRC + f"{n}.jpg")[0] for n in (25, 26, 27, 28, 29)}
SLIDES = [  # name, photo, pos, natural_r, chip, lines, sub, cta
 ("02_huddle", P[25], "36% 50%", None, "THE HUDDLE", [("EVERYONE HAS", "EVERYONE HAS"), ("A POINT.", mark("A POINT."))], ["a huddle mid-argument, hands everywhere."], None),
 ("03_committee", P[27], "50% 40%", None, "THE COMMITTEE", [("PLACARDS UP,", "PLACARDS UP,"), ("SMILES ON.", ring("SMILES ON."))], ["name cards in hand, sunglasses out."], None),
 ("04_placard", P[29], "52% 55%", None, "HANDS UP", [("RAISE IT", "RAISE IT"), ("HIGH.", mark("HIGH."))], ["a placard up and laptops open."], None),
 ("05_court", P[26], "45% 55%", None, "OFF THE FLOOR", [("PAPERS IN HAND,", "PAPERS IN HAND,"), ("ON THE COURT.", ring("ON THE COURT."))], ["sheets read over at the basket, in the sun."], None),
 ("06_close", P[28], "45% 55%", None, "SEE YOU NEXT TIME", [("PARADOX 3.0", "PARADOX 3.0"), ("2025.", mark("2025."))], ["mid-air, no net."], "follow @ngo.aquaterra"),
]
if os.path.exists(COVER_FILE):
    SLIDES.insert(0, ("01_cover", pimg(COVER_FILE)[0], "58% 50%", None, "2025", [("PARADOX 3.0", "PARADOX 3.0"), ("2025", mark("2025"))], ["one event. a lot of voices."], None))
async def main():
    async with B.session():
        for fmt, (W, H, size) in dict(story=(1080, 1920, 112), feed=(1080, 1350, 100)).items():
            for name, src, pos, nr, chip, lines, sub, cta in SLIDES:
                if fmt == "feed" and not name.startswith("01_"): continue   # feed size is for the cover only
                if fmt == "feed" and not name.startswith("01_"): continue   # feed size is for the cover only
                global OUT
                await photo_full(f"{fmt}_{name}", W, H, src, pos, chip, lines, sub, hash(name) % 90, size=size, natural_r=nr, cta=cta)
asyncio.run(main())
