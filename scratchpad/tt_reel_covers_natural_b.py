"""TerraThon REEL COVERS, 20 DIFFERENT PHOTOS (TerraThon recap + past pickleball + past FIFA), TEXTLESS natural-colour (no tint) cut: 20 covers in the 'NO CAPTION NEEDED' look (greyscale photo multiplied by one accent), no headline, no pill; logo, sponsor strip and stickers stay, 1080x1920, six layout families, real event photos only (engine/assets/terrathon/recap_photos/).
Photo key: 01 group selfie · 02 cricket lineup (white kits) · 03 marigold mirror dome · 04 Disco Diwali stall · 05 WE LOVE AQ frame · 06/07 cricket groups.
SAFE BAND: Instagram's profile grid crops a 9:16 cover to the centre 3:4, so ~240px top and bottom are cut there. Every headline, sticker and the sponsor strip
sits inside y 285..1635; only photo and ground bleed past it.
FACTS: copy is a hook line or describes what is visible. The only facts printed are TerraThon 2026 and "2ND TO 4TH OCT" (brain/TERRATHON.md) and Disco Diwali
10 Nov (user, 2026-10-01). No scores, winners, counts or names. Run: python scratchpad/tt_reel_covers.py [only-number ...]"""
import asyncio, base64, importlib.util, io, os, random, sys, itertools
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B, W = tt.core, tt.B, tt.W
from PIL import Image
H = 1920
GROUND, ORCHID, CREAM, INK, WHITE, SLAB = "#000000", tt.ORCHID, tt.CREAM_HALO, tt.INK, tt.WHITE, tt.SLAB
GREEN, BLUE = "#2FD284", "#0396FF"
PH = "engine/assets/terrathon/recap_photos"
OUT = "out/collaterals/terrathon_reel_covers_natural_b"

_pi = Image.open("engine/assets/terrathon/partners/partner_strip.png").convert("RGBA"); _pi = _pi.resize((1600, round(1600 * _pi.height / _pi.width)))
_b = io.BytesIO(); _pi.save(_b, "PNG"); STRIP = "data:image/png;base64," + base64.b64encode(_b.getvalue()).decode()

TT = "engine/assets/terrathon"
PHOTOS = {  # batch 2: the photos not used in the first 20
    "P1": "throwback/IMG_6012.jpg", "P5": "throwback/IMG_6048.jpg", "P8": "throwback/IMG_6060.jpg", "P10": "throwback/IMG_6085.jpg",
    "F14": "throwback_fifa/IMG_3791.jpg", "F15": "throwback_fifa/IMG_3796.jpg", "F16": "throwback_fifa/IMG_3802.jpg", "F20": "throwback_fifa/IMG_5875.jpg",
    "LOT": "lottery.jpg", "BOOTH": "photobooth.jpg",
}
def photo_uri(n):
    im = Image.open(f"{TT}/{PHOTOS[n]}").convert("RGB")
    if im.width > 1700: im = im.resize((1700, int(im.height * 1700 / im.width)))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=90); return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

LAND = {"F14", "F16", "LOT"}          # landscape photos: shown as a full-width duotone band that fades into the flat accent, so nobody is cropped out
S = ["shuriken", "aq_live", "flower", "smiley", "controller", "cricket_set", "pickleball_set", "basketball", "carnival"]
# (photo, focus, accent, [two stickers])
COVERS = [
    ("P1", "50% 55%", ORCHID, ['pickleball_set', 'shuriken']),
    ("F14", "50% 55%", ORCHID, ['controller', 'shuriken']),
    ("BOOTH", "50% 55%", ORCHID, ['smiley', 'aq_live']),
    ("P5", "50% 55%", ORCHID, ['shuriken', 'pickleball_set']),
    ("LOT", "50% 55%", ORCHID, ['flower', 'shuriken']),
    ("F15", "50% 55%", ORCHID, ['controller', 'flower']),
    ("P8", "50% 55%", ORCHID, ['pickleball_set', 'smiley']),
    ("F16", "50% 55%", ORCHID, ['shuriken', 'controller']),
    ("P10", "50% 55%", ORCHID, ['aq_live', 'pickleball_set']),
    ("F20", "50% 55%", ORCHID, ['controller', 'shuriken']),
]

async def cover(i, spec_):
    ph, focus, acc, stk = spec_
    els = []
    def el(l, x, y, w, h): els.append((l, x, y, w, h))
    parts = [f'<style>{tt.FONT_CSS}</style>']
    def sticker(name, label, x, y, w, z=12, rot=0):
        im, src = tt.crop_to_alpha(name + ".png"); h = w * im.height / im.width; el(label, x, y, w, h)
        r = f"transform:rotate({rot}deg);" if rot else ""
        return f'<img src="{src}" class="measure" data-tag="{label}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z};{r}filter:drop-shadow(0 6px 10px rgba(0,0,0,.45))">'
    def chrome():
        p = [f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:44px;top:300px;height:58px;z-index:20;filter:drop-shadow(0 2px 6px rgba(0,0,0,.55))">']; el("logo", 44, 300, 330, 58)
        sw = 760; sh = round(sw * 322 / 2000); sx = (W - sw) // 2; sy = 1470
        p.append(f'<img class="measure" data-tag="sponsors" src="{STRIP}" style="position:absolute;left:{sx}px;top:{sy}px;width:{sw}px;height:{sh}px;z-index:20">'); el("sponsors", sx, sy, sw, sh)
        return "".join(p)
    photo_css = f"object-position:{focus};filter:none;display:block"
    parts.append(f'<div style="position:absolute;inset:0;background:#0A0A0A"></div>')
    if ph in LAND:
        by, bh = 380, 1060                       # band is ~1080 wide, so the 1.08:1 photo is almost uncropped
        mask = "linear-gradient(180deg,transparent 0%,#000 14%,#000 86%,transparent 100%)"
        parts.append(f'<div style="position:absolute;left:0;top:{by}px;width:{W}px;height:{bh}px;z-index:1;-webkit-mask-image:{mask};mask-image:{mask}"><img src="{photo_uri(ph)}" style="width:100%;height:100%;object-fit:cover;{photo_css}"></div>')
        spots = [(740, 330, 260, 8), (30, 1230, 240, -8)]
    else:
        parts.append(f'<div style="position:absolute;inset:0;z-index:1;background:#000"><img src="{photo_uri(ph)}" style="width:100%;height:100%;object-fit:cover;{photo_css}"></div>')
        parts.append(f'<div style="position:absolute;inset:0;z-index:3;background:linear-gradient(180deg,rgba(0,0,0,.3),rgba(0,0,0,0) 30%,rgba(0,0,0,0) 55%,rgba(0,0,0,.7))"></div>')
        spots = [(40, 420, 300, -8), (760, 1130, 260, 8)]
    for k, nme in enumerate(stk):
        x, y, w_, rot = spots[k]
        parts.append(sticker(nme, f"stk{k}", x, y, 130 if nme == "shuriken" else w_, 11, rot))
    parts.append(chrome())
    html = B.page(W, H, "#0A0A0A", "".join(parts), grain=False)
    labels = [e[0] for e in els]
    ign = {frozenset(p) for p in itertools.combinations(labels, 2)}
    ign = {tuple(sorted(p)) for p in ign} | {tuple(p) for p in ign}
    cname = {ORCHID: "orchid", GREEN: "green", BLUE: "blue"}[acc]
    out = f"{OUT}/{i:02d}_{ph}.png"
    await B.render(html, out, W, H, elements=els, text_pairs=[], page_bg="#0A0A0A", margin=12, collision_ignore=ign)
    return out

async def main(only):
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        for i, c in enumerate(COVERS, 1):
            if only and i not in only: continue
            print(await cover(i, c))
    print("done")
asyncio.run(main({int(a) for a in sys.argv[1:]}))
