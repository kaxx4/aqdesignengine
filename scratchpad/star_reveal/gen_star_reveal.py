"""Star-reveal carousel (Workflow C, bespoke). Reference: IG DeXUGacmThK slide 1 — a blue
field with a small star that shows a photo; the star grows slide to slide.

MECHANISM: the photo is ONE full-canvas layer that never moves or scales. A 5-point star
clip-path on that layer reveals it. Only the star radius changes per slide.
ADAPTATIONS (recorded per section 2 ladder): electric blue -> AQ sky A[4] (user directive);
footer text is INK, not white, because core.text_on measures white on sky at <2.6:1;
star centre sits on the sign's wordmark rather than the reference's right-of-centre so a
small star shows readable content; real uploaded AQ photo replaces the crowd stock image.
"""
import asyncio, os, sys, base64, io, importlib.util, math
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine"); sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build")
from PIL import Image
W, H = core.SIZES["feed"]; M = 64
BLUE = core.ACCENTS[4]
HERE = os.path.dirname(os.path.abspath(__file__))
im = Image.open(os.path.join(HERE, "in/photo_juice.jpg")); im.thumbnail((1620, 2160))
buf = io.BytesIO(); im.save(buf, "JPEG", quality=90)
PHOTO = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

_iw, _ih = Image.open(os.path.join(HERE, "in/photo_juice.jpg")).size
PW, PH = W, round(W * _ih / _iw)            # photo at cover width: 1080x1440
PY = -(PH - H) // 2                            # fixed crop, identical on every slide
CX, CY = 620, 860                              # star centre on the cup, identical on every slide
N = 12
RADII = [round(170*(1800/170)**(k/(N-2))) for k in range(N-1)] + [None]   # geometric growth; None = fully revealed

def star(cx, cy, R, r_ratio=0.382):
    pts = []
    for i in range(10):
        a = -math.pi/2 + i*math.pi/5
        r = R if i % 2 == 0 else R*r_ratio
        pts.append(f"{cx+r*math.cos(a):.1f}px {cy+r*math.sin(a):.1f}px")
    return "polygon(" + ",".join(pts) + ")"

ink = core.text_on(BLUE)
def slide(i, R):
    clip = "" if R is None else f"clip-path:{star(CX, CY - PY, R)};"
    photo = (f'<img data-tag="photo" src="{PHOTO}" style="position:absolute;left:0;top:{PY}px;'
             f'width:{PW}px;height:{PH}px;z-index:3;{clip}">')
    logo = (f'<div data-tag="logo" style="position:absolute;top:48px;left:{M}px;z-index:20;background:{core.CREAM};'
            f'border:3px solid var(--ink);border-radius:999px;padding:8px 18px;box-shadow:4px 4px 0 var(--ink)">'
            f'<img src="{core.LOGO}" style="height:30px;display:block"></div>')
    cue = ""
    if i == 0:
        cue = (f'<div data-tag="cue" style="position:absolute;left:0;width:{W}px;bottom:150px;text-align:center;z-index:20;'
               f'font-family:var(--d);font-weight:900;text-transform:uppercase;font-size:34px;letter-spacing:.04em;color:{ink}">'
               f'Hold down the dots and scroll</div>'
               f'<svg data-tag="arrow" style="position:absolute;left:{W/2-28}px;bottom:52px;z-index:20" width="56" height="86" viewBox="0 0 56 86" fill="none" '
               f'stroke="{ink}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><path d="M28 4V80M4 56L28 80L52 56"/></svg>')
    return B.page(W, H, BLUE, photo + logo + cue, grain=True)

async def main():
    out = "out/star_reveal"; os.makedirs(out, exist_ok=True)
    async with B.session():
        for i, R in enumerate(RADII):
            els = [("logo", M, 48, 250, 54)]
            if i == 0: els += [("cue", 0, H-150-44, W, 44), ("arrow", W//2-28, H-52-86, 56, 86)]
            await B.render(slide(i, R), f"{out}/slide{i+1}.png", W, H, elements=els,
                           text_pairs=[("cue", ink, BLUE, 34, True)] if i == 0 else None,
                           bleed_tags=("photo",), crop_tags=("photo",), page_bg=BLUE)
    print("done")
asyncio.run(main())
