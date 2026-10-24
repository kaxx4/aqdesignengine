"""DISCO DIWALI 2.0 (2025) highlights in the AQ EVENT style (black ground, gold flecks, full-bleed photo fading to black,
mint mono step chip, one marked/ringed accent per headline, mono footer). Workflow C, bespoke. Feed 1080x1350 + story 1080x1920.
Reuses the helper block of gen_why_we_do_v1.py and photo_full of gen_events_vibe_v1.py (same event series look).
No stats or dates beyond the event name and year (none sourced); captions describe each photo.
Landscape photos are cover-cropped with a measured focal point (the natural-aspect variant left a dead black middle).
"""
import os, sys, asyncio, io, base64
_HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(_HERE, "gen_why_we_do_v1.py")).read().split("# ====================== CAROUSEL")[0])
_ev = open(os.path.join(_HERE, "gen_events_vibe_v1.py")).read().splitlines()
_s = next(i for i, l in enumerate(_ev) if l.startswith("def step_chip")); _e = next(i for i, l in enumerate(_ev) if l.startswith("async def type_slide"))
exec("\n".join(_ev[_s:_e]))
from PIL import Image
OUT = "out/disco_diwali_event"; os.makedirs(OUT, exist_ok=True)
SRC = "scratchpad/carousel_2026/disco_diwali_2_2025/src_images/"
def pimg(path, maxw=1500):
    im = Image.open(path).convert("RGB")
    if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), im.height / im.width
COVER_FILE = SRC + "cover.jpg"   # the separate cover photo; slides 02-06 render without it until it is supplied
P = {n: pimg(SRC + f"{n}.jpg")[0] for n in (13, 14, 15, 16, 17)}
SLIDES = [  # name, photo, pos, natural_r, chip, lines, sub, cta
 ("02_booth", P[14], "52% 55%", None, "THE BOOTH", [("LIGHTS, CAMERA,", "LIGHTS, CAMERA,"), ("DISCO DIWALI.", mark("DISCO DIWALI."))], ["a hollywood set, balloons and a red carpet."], None),
 ("03_floor", P[15], "48% 60%", None, "ON THE FLOOR", [("HANDS UP.", "HANDS UP."), ("LIGHTS DOWN.", ring("LIGHTS DOWN."))], ["playing cards hung overhead, blue light everywhere."], None),
 ("04_hug", P[13], "50% 40%", None, "THE HUGS", [("TWO OUTFITS,", "TWO OUTFITS,"), ("ONE HUG.", mark("ONE HUG."))], ["under a wall of playing-card suits."], None),
 ("05_rooftop", P[16], "55% 40%", None, "ROOFTOP", [("DRESSED UP,", "DRESSED UP,"), ("GLOWING.", ring("GLOWING."))], ["fairy lights and three big smiles."], None),
 ("06_close", P[17], "45% 40%", None, "SEE YOU NEXT TIME", [("WRISTBANDS ON.", "WRISTBANDS ON."), ("PHONES OUT.", mark("PHONES OUT."))], ["disco diwali 2.0, 2025."], "follow @ngo.aquaterra"),
]
if os.path.exists(COVER_FILE):
    SLIDES.insert(0, ("01_cover", pimg(COVER_FILE)[0], "60% 50%", None, "DIWALI 2025", [("DISCO DIWALI", "DISCO DIWALI"), ("2.0", mark("2.0"))], ["one night. a whole lot of glitter."], None))
async def main():
    async with B.session():
        for fmt, (W, H, size) in dict(story=(1080, 1920, 112)).items():
            for name, src, pos, nr, chip, lines, sub, cta in SLIDES:
                global OUT
                await photo_full(f"{fmt}_{name}", W, H, src, pos, chip, lines, sub, hash(name) % 90, size=size, natural_r=nr, cta=cta)
asyncio.run(main())
