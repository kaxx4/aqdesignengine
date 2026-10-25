"""FOOTBALL FUNDRAISER 2024 highlights in the AQ EVENT style (black ground, gold flecks, full-bleed photo fading to black,
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
OUT = "out/football24_event"; os.makedirs(OUT, exist_ok=True)
SRC = "scratchpad/carousel_2026/football_fundraiser_2024/src_images/"
def pimg(path, maxw=1500):
    im = Image.open(path).convert("RGB")
    if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), im.height / im.width
COVER_FILE = SRC + "cover.jpg"   # the separate cover photo; slides render without it until it is supplied
# 67.jpg (signs with MILF/DILF jokes) is deliberately NOT used: not suitable for a public NGO page
P = {n: pimg(SRC + f"{n}.jpg")[0] for n in (68, 69, 70, 71)}
NAT_TOP, NAT_GH = 0, 300
NAT = {}
SLIDES = [  # name, photo, pos, natural_r, chip, lines, sub, cta
 ("02_kick", P[68], "50% 50%", None, "KICK OFF", [("BALL AT", "BALL AT"), ("THEIR FEET.", mark("THEIR FEET."))], ["two players, one red ball, full focus."], None),
 ("03_match", P[70], "55% 50%", None, "GAME ON", [("GAME ON,", "GAME ON,"), ("BAREFOOT AND ALL.", ring("BAREFOOT AND ALL."))], ["a scramble for the ball at dusk."], None),
 ("04_hug", P[69], "50% 40%", None, "FULL TIME", [("GROUP HUG,", "GROUP HUG,"), ("NO REFEREE.", mark("NO REFEREE."))], ["five friends and a camera, after the match."], None),
 ("05_close", P[71], "50% 40%", None, "SEE YOU NEXT TIME", [("FOOTBALL", "FOOTBALL"), ("FUNDRAISER 2024.", mark("FUNDRAISER 2024."))], ["under the aquaterra banner."], "follow @ngo.aquaterra"),
]
if os.path.exists(COVER_FILE):
    SLIDES.insert(0, ("01_cover", pimg(COVER_FILE)[0], "55% 30%", None, "2024", [("FOOTBALL", "FOOTBALL"), ("FUNDRAISER", mark("FUNDRAISER"))], ["a pitch, a crowd and a cause."], None))
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
