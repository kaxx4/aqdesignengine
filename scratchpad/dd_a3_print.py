"""DISCO DIWALI A3 PRINT SIGNAGE (2026-11-04): one A3 sign per stall, from the user's Summer Sunset welcome-sign reference, rebuilt in Disco Diwali branding.

Reference mechanism kept: a big hero identity in the middle, decorative stickers in the corners, the event mark, and a "BROUGHT TO YOU BY TEAM AQUATERRA"
pill carrying the AQ logo at the foot. Adapted: the beach emoji / palms become the Disco Diwali kit (event photo ground, string lights, LIVE badge, copper
sticker); the hero is the stall (its logo in the gold circle + its name), the same skeleton as the stall Instagram posts so the signs and posts match.

Canvas 1080 x 1527 is A3 portrait (297 x 420 mm) in CSS px; rendered at scale 3.25 = 3510 x 4963 px, i.e. 300 dpi at A3. Output: PNG + an A3 PDF.
sRGB, no bleed, no crop marks (see brain/BROCHURE_CATALOG.md print caveats).

Run: PYTHONIOENCODING=utf-8 STALL=kulfi python scratchpad/dd_a3_print.py      (STALL=all renders every stall)
"""
import asyncio, base64, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B = dd.B; core = dd.core
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dd_photo_bg as PB, dd_copper as CP   # noqa: E402

W, H, SCALE = 1080, 1527, 3.25
OUT = os.path.join(ROOT, "out", "discodiwali", "print_a3")
EV = os.path.join(ROOT, "engine", "assets", "img", "events")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"


def _png(path):
    return "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()


# slug: (name, tagline, circle content, circle fill, logo inset %, ground photo, ground focus, dim, sticker fn, sticker rot, headline px)
STALLS = {
    "kulfi":    ("Bombay Kulfi", "Food stall", "bombay-kulfi/01_bombay-kulfi-logo.png", "#FFFFFF", 8, "bombay-kulfi/02_kulfi-sticks-yellow-board.jpg", "50% 50%", .52, "kulfi", 12, 116),
    "artily":   ("Artily", "Beverage stall", "artily/01_artily-logo.png", "#FFFFFF", 3, "artily/02_artily-blue-drink-pour.jpg", "50% 50%", .52, "cup", 10, 165),
    "subway":   ("Subway", "Food stall", "subway/01_subway-logo.png", "#0C8A42", 0, "subway/02_subway-sub-in-basket.jpg", "50% 50%", .52, "sub", -12, 165),
    "pizzahut": ("Pizza Hut", "Food stall", "pizza-hut/01_pizza-hut-logo.png", "#FFFFFF", 0, "pizza-hut/02_pizza-hut-pizza-top-down.jpg", "50% 50%", .52, "slice_", 14, 165),
    "cravella": ("Crave&rsquo;lla", "Food stall", "cravella/01_cravella-logo.png", "#5F2327", 0, "cravella/02_cravella-brownies.jpg", "50% 0%", .52, "brownie", -8, 150),
    "zaairah":  ("Zaairah", "Food stall", "zaairah/01_zaairah-logo.png", "#000000", 0, "zaairah/02_zaairah-pasta-plate.jpg", "50% 50%", .52, "cloche", 8, 165),
    "meetcute": ("Meet Cute", "Food stall", "meet-cute/01_meet-cute-logo.png", "#FFFAF0", 0, "meet-cute/02_meet-cute-pasta-fork.jpg", "50% 50%", .34, "mug", 10, 150),
    "artstop":  ("The ArtStop", "Jewellery stall", "the-artstop/01_the-artstop-logo.png", "#4C1815", 0, "the-artstop/02_the-artstop-lip-charms.jpg", "50% 50%", .52, "heart", 10, 112),
    "nandu":    ("Nandu Jee", "Food stall", "nandu-jee/01_nandu-jee-googly-eyes.jpg", None, 0, "14_04", "50% 30%", .62, "samosa", 8, 165),
    "puchka":   ("Puchka", "Food stall", "puchka/01_puchka-plates-crop.jpg", None, 0, "14_04", "50% 30%", .62, "samosa", -10, 165),
}


def circle(src, fill, inset):
    if fill is None:   # a photo, not a logo: fill the circle
        return f'<img src="{dd.photo_uri(os.path.join(EV, src))}" style="width:100%;height:100%;object-fit:cover;filter:contrast(1.06) saturate(1.05)">'
    return (f'<div style="position:absolute;inset:0;background:{fill}"></div>'
            f'<img src="{_png(os.path.join(EV, src))}" style="position:absolute;left:{inset}%;top:{inset}%;width:{100 - 2 * inset}%;height:{100 - 2 * inset}%;object-fit:contain">')


def sign(slug):
    name, tag, src, fill, inset, bg, focus, dim, stk, rot, hs = STALLS[slug]
    bgref = bg if "_" in bg and "/" not in bg else os.path.join(EV, bg)
    parts, els = [PB.photo_ground(dd, W, H, bgref, focus, dim=dim)], []
    # LIVE badge, top left (no Instagram bars on paper, so it sits at the margin)
    bx, by, bw = 48, 48, 180
    parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:{bx}px;top:{by}px;width:{bw}px;z-index:20">')
    els.append(("badge", bx, by, bw, round(bw * 1005 / 1061)))
    # the stall circle
    d = 640; cx, cy0 = (W - d) // 2, 190
    parts.append(f'<div data-tag="circle" style="position:absolute;left:{cx}px;top:{cy0}px;width:{d}px;height:{d}px;border-radius:50%;overflow:hidden;border:10px solid {dd.GOLD};'
                 f'box-sizing:border-box;z-index:10;box-shadow:0 16px 44px rgba(0,0,0,.6)">{circle(src, fill, inset)}</div>')
    els.append(("circle", cx, cy0, d, d))
    # copper sticker on the circle's top-right
    ss = 300; mx, my = 1040 - ss, 40
    parts.append(f'<div data-tag="sticker" style="position:absolute;left:{mx}px;top:{my}px;z-index:12">{getattr(CP, stk)(ss, rot)}</div>'); els.append(("sticker", mx, my, ss, ss))
    # name + tagline
    def line(t, txt, top, size, h, stroke=True):
        parts.append(f'<div data-tag="{t}" style="position:absolute;left:0;width:{W}px;top:{top}px;text-align:center;font-family:var(--d);font-weight:700;font-size:{size}px;line-height:1;'
                     f'text-transform:uppercase;white-space:nowrap;{STROKE if stroke else "color:#fff;"}z-index:20">{txt}</div>'); els.append((t, 40, top, 1000, h))
    hy = cy0 + d + 34
    line("head", name, hy, hs, hs)
    t1 = hy + hs + 18
    line("tag1", tag, t1, 58, 62, stroke=False)
    # footer lockup, with ball
    y = t1 + 62 + 40
    vw = 300; t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(y - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">')
    els.append(("title", vx, y, vw, vh))
    # BROUGHT TO YOU BY TEAM AQUATERRA pill (the reference's footer), AQ wordmark on a cream pill (logo rule: never white-inverted)
    pw, ph = 760, 128; px, py = (W - pw) // 2, H - 48 - ph
    lw = 300; lh = round(lw * 225 / 1332)
    parts.append(f'<div data-tag="pill" style="position:absolute;left:{px}px;top:{py}px;width:{pw}px;height:{ph}px;box-sizing:border-box;border-radius:{ph // 2}px;'
                 f'background:#F7EFE0;border:6px solid {dd.GOLD};box-shadow:0 10px 30px rgba(0,0,0,.55);z-index:20;display:flex;align-items:center;justify-content:center;gap:34px">'
                 f'<img src="{core.LOGO}" style="width:{lw}px;height:{lh}px;display:block">'
                 f'<div style="font-family:var(--d);font-weight:700;font-size:28px;line-height:1.08;text-transform:uppercase;color:#0A0A0A">Brought to you<br>by Team AquaTerra</div></div>')
    els.append(("pill", px, py, pw, ph))
    return "".join(parts), els, y + vh, py


async def main():
    which = os.environ.get("STALL", "kulfi")
    slugs = list(STALLS) if which == "all" else which.split(",")
    os.makedirs(OUT, exist_ok=True)
    from PIL import Image
    async with B.session(scale=SCALE):
        for s in slugs:
            inner, els, lockup_end, pill_top = sign(s)
            print(f"[{s}] lockup ends y={lockup_end}, pill starts y={pill_top} (gap {pill_top - lockup_end})")
            png = os.path.join(OUT, f"{s}_a3.png")
            await B.render(B.page(W, H, "#000", inner, grain=False), png, W, H, elements=els, bleed_tags=("plate",), crop_tags=("plate", "circle"),
                           page_bg="#000", collision_ignore=[("circle", "sticker"), ("circle", "head")],
                           text_pairs=[("head", "#fff", "#000", 112, True), ("tag", "#fff", "#000", 58, True), ("pill", "#0A0A0A", "#F7EFE0", 28, True)])
            im = Image.open(png).convert("RGB")
            print(f"[{s}] {im.size[0]}x{im.size[1]} px")
            im.save(os.path.join(OUT, f"{s}_a3.pdf"), "PDF", resolution=300)
    print("a3 done ->", OUT)
asyncio.run(main())
