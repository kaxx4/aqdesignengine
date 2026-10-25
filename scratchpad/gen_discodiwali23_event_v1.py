"""DISCO DIWALI 2023 highlights in the AQ EVENT style (black ground, gold flecks, full-bleed photo fading to black,
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
exec("\n".join(_ev[_s:_e]).replace("gh = 680 if natural_r", "gh = NAT_GH if natural_r")
     .replace("left:0;top:0;width:{W}px;height:auto", "left:0;top:{NAT_TOP}px;width:{W}px;height:auto")
     .replace("top:{ph - gh}px", "top:{ph + (NAT_TOP if natural_r else 0) - gh}px")
     .replace("top:{ph - 3}px", "top:{ph + (NAT_TOP if natural_r else 0) - 3}px"))   # NAT_TOP slides a natural-aspect photo up; NAT_GH is its fade height
NAT_TOP, NAT_GH = 0, 300
NAT = {"04_rim": (-160, 140)}   # rim frame: the players sit at the foot of the picture, so lift it clear of the headline
from PIL import Image
OUT = "out/discodiwali23_event"; os.makedirs(OUT, exist_ok=True)
SRC = "scratchpad/carousel_2026/disco_diwali_2023/src_images/"
def pimg(path, maxw=1500):
    im = Image.open(path).convert("RGB")
    if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), im.height / im.width
COVER_FILE = SRC + "cover.jpg"   # the separate cover photo; slides render without it until it is supplied
P = {n: pimg(SRC + f"{n}.jpg")[0] for n in (86, 87, 88, 89, 90)}
NAT_TOP, NAT_GH = 0, 300
NAT = {}
SLIDES = [  # name, photo, pos, natural_r, chip, lines, sub, cta
 ("02_floor", P[86], "50% 60%", None, "THE FLOOR", [("FLOOR FILLING", "FLOOR FILLING"), ("UP.", mark("UP."))], ["string lights overhead, the crowd in kurtas and lehengas."], None),
 ("03_red", P[87], "40% 55%", None, "RED LIGHT", [("RED LIGHT,", "RED LIGHT,"), ("GOOD COMPANY.", ring("GOOD COMPANY."))], ["friends crowded in under the lights."], None),
 ("04_globe", P[88], "50% 55%", None, "MARIGOLDS", [("TWO FRIENDS,", "TWO FRIENDS,"), ("ONE GLOBE.", mark("ONE GLOBE."))], ["marigolds behind, the aquaterra globe in hand."], None),
 ("05_hug", P[89], "40% 50%", None, "THE HUG", [("THE BIG", "THE BIG"), ("HUG.", ring("HUG."))], ["a hug under the string lights."], None),
 ("06_close", P[90], "50% 82%", None, "SEE YOU NEXT TIME", [("DISCO DIWALI", "DISCO DIWALI"), ("2023.", mark("2023."))], ["the crew, under the banner."], "follow @ngo.aquaterra"),
]
if os.path.exists(COVER_FILE):
    SLIDES.insert(0, ("01_cover", pimg(COVER_FILE)[0], "50% 40%", None, "DIWALI 2023", [("DISCO DIWALI", "DISCO DIWALI"), ("2023", mark("2023"))], ["one night. a whole lot of glitter."], None))
async def main():
    async with B.session():
        for fmt, (W, H, size) in dict(story=(1080, 1920, 112), feed=(1080, 1350, 100)).items():
            for name, src, pos, nr, chip, lines, sub, cta in SLIDES:
                global NAT_TOP, NAT_GH; NAT_TOP, NAT_GH = NAT.get(name, (0, 300))
                if fmt == "feed" and not name.startswith("01_"): continue   # feed size is for the cover only
                if fmt == "feed" and not name.startswith("01_"): continue   # feed size is for the cover only
                global OUT
                await photo_full(f"{fmt}_{name}", W, H, src, pos, chip, lines, sub, hash(name) % 90, size=size, natural_r=nr, cta=cta)
asyncio.run(main())
