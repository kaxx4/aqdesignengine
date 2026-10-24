"""MERRY MIRACLES 2025 highlights in the AQ EVENT style (black ground, gold flecks, full-bleed photo fading to black,
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
OUT = "out/merry_miracles_event"; os.makedirs(OUT, exist_ok=True)
SRC = "scratchpad/carousel_2026/merry_miracles_2025/src_images/"
def pimg(path, maxw=1500):
    im = Image.open(path).convert("RGB")
    if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), im.height / im.width
HAS12 = os.path.exists(SRC + "12.jpg")   # the piggyback cover; falls back to the kids' stockings frame
P = {n: pimg(SRC + f"{n}.jpg")[0] for n in (7, 8, 9, 10, 11) + ((12,) if HAS12 else ())}
SLIDES = [  # name, photo, pos, natural_r, chip, lines, sub, cta
 ("01_cover", P[12 if HAS12 else 9], "50% 25%" if HAS12 else "42% 50%", None, "CHRISTMAS 2025", [("MERRY MIRACLES", "MERRY MIRACLES"), ("2025", mark("2025"))], ["a christmas of small gifts and big hugs."], None),
 ("02_stockings", P[9], "42% 50%", None, "CRAFT TIME", [("STOCKINGS UP.", "STOCKINGS UP."), ("ALL SMILES.", mark("ALL SMILES."))], ["paper stockings, held as high as they go."], None),
 ("03_floor", P[10], "58% 55%", None, "ON THE FLOOR", [("COTTON, GLUE,", "COTTON, GLUE,"), ("SANTA HATS.", ring("SANTA HATS."))], ["paper plates, red card and a lot of cotton."], None),
 ("04_door", P[7], "50% 40%", None, "AT THE DOOR", [("A GIFT,", "A GIFT,"), ("A SMILE.", mark("A SMILE."))], ["handed over at the door, one home at a time."], None),
 ("05_doorway", P[8], "50% 55%", None, "DOOR TO DOOR", [("KNOCK, KNOCK.", "KNOCK, KNOCK."), ("MERRY CHRISTMAS.", ring("MERRY CHRISTMAS."))], ["a gift passed across a festive doorway."], None),
 ("06_close", P[11], "50% 35%", None, "SEE YOU NEXT TIME", [("SMALL GIFT.", "SMALL GIFT."), ("BIG MIRACLE.", mark("BIG MIRACLE."))], ["merry miracles 2025."], "follow @ngo.aquaterra"),
]
if not HAS12: SLIDES = [s for s in SLIDES if not s[0].startswith("02_")]
async def main():
    async with B.session():
        for fmt, (W, H, size) in dict(feed=(1080, 1350, 100), story=(1080, 1920, 112)).items():
            for name, src, pos, nr, chip, lines, sub, cta in SLIDES:
                global OUT
                await photo_full(f"{fmt}_{name}", W, H, src, pos, chip, lines, sub, hash(name) % 90, size=size, natural_r=nr, cta=cta)
asyncio.run(main())
