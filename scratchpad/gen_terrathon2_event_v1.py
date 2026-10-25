"""TERRATHON 2.0 (2025) highlights in the AQ EVENT style (black ground, gold flecks, full-bleed photo fading to black,
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
exec("\n".join(_ev[_s:_e]).replace("gh = 680 if natural_r", "gh = 300 if natural_r"))   # shorter fade so a held sign stays readable
from PIL import Image
OUT = "out/terrathon2_event"; os.makedirs(OUT, exist_ok=True)
SRC = "scratchpad/carousel_2026/terrathon_2_2025/src_images/"
def pimg(path, maxw=1500):
    im = Image.open(path).convert("RGB")
    if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), im.height / im.width
COVER_FILE = SRC + "cover.jpg"   # the separate cover photo; slides 02-06 render without it until it is supplied
P = {n: pimg(SRC + f"{n}.jpg")[0] for n in (31, 32, 33, 34, 35)}
SLIDES = [  # name, photo, pos, natural_r, chip, lines, sub, cta
 ("02_pitch", P[31], "50% 50%", None, "ON THE PITCH", [("EYES ON", "EYES ON"), ("THE BALL.", mark("THE BALL."))], ["bat out, fielder ready, a yellow ball mid-air."], None),
 ("03_court", P[34], "55% 50%", None, "FULL COURT", [("DRIBBLE,", "DRIBBLE,"), ("DEFEND.", mark("DEFEND."))], ["a ball in play under the tin roof."], None),
 # 04_rim dropped: dark frame, and the headline hides the players at the foot of the picture
 ("05_sign", P[33], "", 1600 / 1200, "THE CHEER SQUAD", [("THEY SAY", "THEY SAY"), ("SHOOTERS SHOOT.", mark("SHOOTERS SHOOT."))], ["a hand-painted sign, held up courtside."], None),
 ("06_close", P[35], "40% 50%", None, "SEE YOU NEXT TIME", [("TERRATHON 2.0", "TERRATHON 2.0"), ("2025.", mark("2025."))], ["game on. see you at the next one."], "follow @ngo.aquaterra"),
]
if os.path.exists(COVER_FILE):
    SLIDES.insert(0, ("01_cover", pimg(COVER_FILE)[0], "55% 50%", None, "2025", [("TERRATHON 2.0", "TERRATHON 2.0"), ("2025", mark("2025"))], ["cricket, basketball, teams out."], None))
async def main():
    async with B.session():
        for fmt, (W, H, size) in dict(story=(1080, 1920, 112), feed=(1080, 1350, 100)).items():
            for name, src, pos, nr, chip, lines, sub, cta in SLIDES:
                if fmt == "feed" and not name.startswith("01_"): continue   # feed size is for the cover only
                if fmt == "feed" and not name.startswith("01_"): continue   # feed size is for the cover only
                global OUT
                await photo_full(f"{fmt}_{name}", W, H, src, pos, chip, lines, sub, hash(name) % 90, size=size, natural_r=nr, cta=cta)
asyncio.run(main())
