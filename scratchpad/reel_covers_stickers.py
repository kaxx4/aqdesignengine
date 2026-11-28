"""Reel covers (1080x1920) from two supplied photos: the photo full bleed, nothing else but four copper stickers, one in each corner.
No text, logo or branding on the cover. Stickers sit in the corners of the 4:5 grid crop (y 285..1635) so they survive the profile-grid crop.
Cover A (crowd): heart / star / diya / calendar.  Cover B (tree): star / diya / heart / pin.  Sticker art: sample_outputs/disco_diwali_stickers/ (rotation baked in, no drop shadow in the PNG; one is added here).
CONSENT: the crowd photo shows apparent minors and there is no consent record. Check before posting.
Run: PYTHONIOENCODING=utf-8 python scratchpad/reel_covers_stickers.py"""
import asyncio, base64, importlib.util, io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ED = os.path.join(ROOT, "engine"); sys.path.insert(0, ED)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ED, n + ".py")); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
B = load("build")
from PIL import Image
W, H = 1080, 1920; SAFE_T, SAFE_B, EDGE = 285, 1635, 28
OUT = os.path.join(ROOT, "out", "reel_covers")
def uri(img):
    b = io.BytesIO(); img.save(b, "PNG" if img.mode == "RGBA" else "JPEG", **({} if img.mode == "RGBA" else {"quality": 92}))
    return f"data:image/{'png' if img.mode == 'RGBA' else 'jpeg'};base64," + base64.b64encode(b.getvalue()).decode()
def photo(name):
    im = Image.open(os.path.join(ROOT, "training_samples", "reel_cover_photos", name)).convert("RGB")
    if im.width > 1800: im = im.resize((1800, round(im.height * 1800 / im.width)), Image.LANCZOS)
    return uri(im)
def sticker(name, w):
    im = Image.open(os.path.join(ROOT, "sample_outputs", "disco_diwali_stickers", name)).convert("RGBA")
    h = round(im.height * w / im.width); return uri(im.resize((700, round(im.height * 700 / im.width)), Image.LANCZOS)), h
def corners(spec, w_of):
    """spec: names for TL, TR, BL, BR. Returns html + element boxes; each sticker hugs its corner of the safe frame."""
    html, els = "", []
    for pos, name in zip(("tl", "tr", "bl", "br"), spec):
        w = w_of[name]; u, h = sticker(f"copper_{name}.png", w)
        x = EDGE if pos[1] == "l" else W - EDGE - w
        y = SAFE_T if pos[0] == "t" else SAFE_B - h
        tag = f"s_{pos}"
        html += f'<img data-tag="{tag}" src="{u}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;z-index:20;filter:drop-shadow(0 12px 18px rgba(0,0,0,.6))">'
        els.append((tag, x, y, w, h))
    return html, els
SIZES = {"heart": 330, "star": 270, "diya": 320, "calendar": 290, "pin": 230}
def cover(img, pos, spec):
    ph = (f'<img data-tag="photo" src="{photo(img)}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;object-position:{pos};filter:contrast(1.05) saturate(1.05) brightness(1.04)">')
    s, els = corners(spec, SIZES)
    return ph + s, els
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        for name, args in (("cover_a_crowd", ("crowd_dance.jpg", "70% 50%", ("heart", "star", "diya", "calendar"))),
                           ("cover_b_tree", ("tree_gifts.jpg", "27% 50%", ("star", "diya", "heart", "pin")))):
            inner, els = cover(*args)
            await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, name + ".png"), W, H, elements=els, bleed_tags=("photo",), crop_tags=("photo",), page_bg="#000")
            Image.open(os.path.join(OUT, name + ".png")).convert("RGB").resize((W, H), Image.LANCZOS).save(os.path.join(OUT, name + ".jpg"), quality=90)
    print("done ->", OUT)
asyncio.run(main())
