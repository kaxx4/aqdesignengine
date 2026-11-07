"""DISCO DIWALI A3 PRINT SIGNAGE, LANDSCAPE (2026-11-04): one A3 sign per stall, from the user's Summer Sunset welcome-sign reference, in Disco Diwali branding.

v2 (user, 2026-11-04): horizontal, no photo in the background, no cream "brought to you by" pill ("doesn't match the Disco Diwali branding").
Ground is the brand's own beaded celestial plate (engine/assets/disco_diwali/bg_beaded_landscape.jpg) with string lights, gold dust and grain.
Left: the stall's logo (or photo) in the gold circle with its copper sticker on the corner. Right: the stall name (measured to fit the column),
its type, the Disco Diwali lockup. Foot: a gold-ruled "BROUGHT TO YOU BY TEAM AQUATERRA" credit line, the brand's own rule device. The LIVE badge
(which carries the AquaTerra mark) sits top left.

Canvas 1527 x 1080 is A3 landscape (420 x 297 mm) in CSS px; rendered at scale 3.25 = 4963 x 3510 px, 300 dpi at A3. Output: PNG + an A3 PDF.
sRGB, no bleed, no crop marks (brain/BROCHURE_CATALOG.md print caveats).

Run: PYTHONIOENCODING=utf-8 STALL=kulfi python scratchpad/dd_a3_print.py      (STALL=all renders every stall)
"""
import asyncio, base64, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B = dd.B; core = dd.core
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dd_photo_bg as PB, dd_copper as CP, dd_ground as G   # noqa: E402

W, H, SCALE = 1527, 1080, 3.25
OUT = os.path.join(ROOT, "out", "discodiwali", "print_a3")
EV = os.path.join(ROOT, "engine", "assets", "img", "events")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"


def _png(path):
    return "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()


# slug: (name, tagline, circle content, circle fill, logo inset %, ground photo, ground focus, dim, sticker fn, sticker rot, headline px)
STALLS = {
    "kulfi":    ("Bombay|Kulfi", "Food stall", "bombay-kulfi/01_bombay-kulfi-logo.png", "#FFFFFF", 8, "bombay-kulfi/02_kulfi-sticks-yellow-board.jpg", "50% 50%", .52, "kulfi", 12, 116),
    "artily":   ("Artily", "Beverage partner", "artily/01_artily-logo.png", "#FFFFFF", 3, "artily/02_artily-blue-drink-pour.jpg", "50% 50%", .52, "cup", 10, 165),
    "subway":   ("Subway", "Food stall", "subway/01_subway-logo.png", "#0C8A42", 0, "subway/02_subway-sub-in-basket.jpg", "50% 50%", .52, "sub", -12, 165),
    "pizzahut": ("Pizza|Hut", "Food stall", "pizza-hut/01_pizza-hut-logo.png", "#FFFFFF", 0, "pizza-hut/02_pizza-hut-pizza-top-down.jpg", "50% 50%", .52, "slice_", 14, 165),
    "cravella": ("Crave’lla", "Food stall", "cravella/01_cravella-logo.png", "#5F2327", 0, "cravella/02_cravella-brownies.jpg", "50% 0%", .52, "brownie", -8, 150),
    "zaairah":  ("Zaairah", "Food stall", "zaairah/01_zaairah-logo.png", "#000000", 0, "zaairah/02_zaairah-pasta-plate.jpg", "50% 50%", .52, "cloche", 8, 165),
    "meetcute": ("Meet|Cute", "Food stall", "meet-cute/01_meet-cute-logo.png", "#FFFAF0", 0, "meet-cute/02_meet-cute-pasta-fork.jpg", "50% 50%", .34, "mug", 10, 150),
    "artstop":  ("The|ArtStop", "Jewellery stall", "the-artstop/01_the-artstop-logo.png", "#4C1815", 0, "the-artstop/02_the-artstop-lip-charms.jpg", "50% 50%", .52, "heart", 10, 112),
    "nandu":    ("Nandu|Jee", "Food stall", "nandu-jee/01_nandu-jee-googly-eyes.jpg", None, 0, "14_04", "50% 30%", .62, "samosa", 8, 165),
    "photobooth": ("Photo|Booth", "Activity", "photobooth/01_photobooth-set-crop.jpg", None, 0, "", "", 0, "camera", 10, 165),
    "gajra":    ("Gajra &amp;|Jhumka", "Jewellery stall", "gajra-jhumka/01_gajre-board-crop.jpg", None, 0, "", "", 0, "jhumka", 10, 165),
    "unbasic":  ("Unbasic", "Clothing stall", "unbasic/01_unbasic-logo.png", "#000000", 6, "", "", 0, "tee", 10, 165),
    "eloza":    ("Eloza", "Jewellery &amp; crochet stall", "eloza/01_eloza-logo.png", "#F4F1E9", 5, "", "", 0, "bloom", 10, 165),
    "mod":      ("Mad Over|Donuts", "Food stall", "mad-over-donuts/01_mod-logo.png", "#F26B2A", 0, "", "", 0, "donut", 10, 165),
    "periodsim": ("Period Pain|Simulator", "Activity", "period-pain-simulator/01_period-sim-electrodes-crop.jpg", None, 0, "", "", 0, "bolt", -10, 165),
    "puchka":   ("Puchka", "Food stall", "puchka/01_puchka-plates-crop.jpg", None, 0, "14_04", "50% 30%", .62, "samosa", -10, 165),
}


def circle(src, fill, inset):
    if src.startswith("cp:"):   # no logo or photo supplied: a large copper sticker drawn for this stall, on a near-black disc
        return (f'<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 40%,#2A1410 0%,{fill} 70%)"></div>'
                f'<div style="position:absolute;left:14%;top:14%;width:72%;height:72%">{getattr(CP, src[3:])(round(580 * .72), 0, u=src[3:4] + "C")}</div>')
    if fill is None:   # a photo, not a logo: fill the circle
        return f'<img src="{dd.photo_uri(os.path.join(EV, src))}" style="width:100%;height:100%;object-fit:cover;filter:contrast(1.06) saturate(1.05)">'
    return (f'<div style="position:absolute;inset:0;background:{fill}"></div>'
            f'<img src="{_png(os.path.join(EV, src))}" style="position:absolute;left:{inset}%;top:{inset}%;width:{100 - 2 * inset}%;height:{100 - 2 * inset}%;object-fit:contain">')


def ground():
    return G.ground(dd, W, H)          # the blue diya ground (user, 2026-11-07), shared by every A3 sign: scratchpad/dd_ground.py


COL_X, COL_W = 820, 640          # the right-hand text column


async def fit_name(lines, cap=170):
    m = await B.measure_text([dict(text=t.upper().replace("&AMP;", "&"), font="d", size=100, weight=700) for t in lines], W=W, H=H)
    widest = max(r["text_w"] for r in m)
    return min(cap, int(100 * (COL_W - 20) / widest))


def sign(slug, hs):
    name, tag, src, fill, inset, bg, focus, dim, stk, rot, _ = STALLS[slug]
    lines = name.split("|")
    parts, els = [ground()], []
    # LIVE badge, top left
    bx, by, bw = 48, 44, 170
    parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:{bx}px;top:{by}px;width:{bw}px;z-index:20">')
    els.append(("badge", bx, by, bw, round(bw * 1005 / 1061)))
    # the stall circle, left half
    d = 600; cx, cy0 = 150, 230
    parts.append(f'<div data-tag="circle" style="position:absolute;left:{cx}px;top:{cy0}px;width:{d}px;height:{d}px;border-radius:50%;overflow:hidden;border:10px solid {dd.GOLD};'
                 f'box-sizing:border-box;z-index:10;box-shadow:0 16px 44px rgba(0,0,0,.7)">{circle(src, fill, inset)}</div>')
    els.append(("circle", cx, cy0, d, d))
    # copper sticker on the circle's top-right corner
    ss = 260; mx, my = cx + d - 200, cy0 - 120
    parts.append(f'<div data-tag="sticker" style="position:absolute;left:{mx}px;top:{my}px;z-index:12">{getattr(CP, stk)(ss, rot)}</div>'); els.append(("sticker", mx, my, ss, ss))
    # right column: name lines, type, lockup -- stacked, centred on the circle's centre line
    lh = round(hs * 1.0); gap1, tsz, gap2 = 22, (56 if len(tag) <= 18 else 34), 44
    vw = 300; t = vw / 1717; vh = round(991 * t)
    total = len(lines) * lh + (len(lines) - 1) * 8 + gap1 + tsz + gap2 + vh
    y = cy0 + d // 2 - total // 2
    def line(tg, txt, top, size, h, stroke=True):
        parts.append(f'<div data-tag="{tg}" style="position:absolute;left:{COL_X}px;width:{COL_W}px;top:{top}px;text-align:center;font-family:var(--d);font-weight:700;font-size:{size}px;line-height:1;'
                     f'text-transform:uppercase;white-space:nowrap;{STROKE if stroke else "color:#fff;"}z-index:20">{txt}</div>'); els.append((tg, COL_X, top, COL_W, h))
    for i, txt in enumerate(lines):
        line(f"head{i}", txt, y, hs, lh); y += lh + 8
    y += gap1 - 8
    line("tag1", tag, y, tsz, tsz, stroke=False); y += tsz + gap2
    vx = COL_X + (COL_W - vw) // 2
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(y - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">')
    els.append(("title", vx, y, vw, vh))
    # credit line: gold rules either side, the brand's rule device (discodiwali.py), not a pill
    fy = H - 92
    rule = f'<span style="display:inline-block;width:150px;height:2px;background:{dd.GOLD};vertical-align:middle"></span>'
    parts.append(f'<div data-tag="credit" style="position:absolute;left:0;width:{W}px;top:{fy}px;text-align:center;font-family:var(--d);font-weight:700;font-size:28px;line-height:1;'
                 f'letter-spacing:.12em;text-transform:uppercase;color:#fff;text-shadow:0 2px 10px #000,0 0 4px #000;z-index:20;white-space:nowrap">'
                 f'{rule}<span style="margin:0 26px;vertical-align:middle">Brought to you by Team AquaTerra</span>{rule}</div>')
    els.append(("credit", 380, fy, W - 760, 30))
    return "".join(parts), els, y + vh, fy


async def main():
    which = os.environ.get("STALL", "kulfi")
    slugs = list(STALLS) if which == "all" else which.split(",")
    os.makedirs(OUT, exist_ok=True)
    from PIL import Image
    async with B.session(scale=SCALE):
        for s in slugs:
            hs = await fit_name(STALLS[s][0].split("|"))
            inner, els, lockup_end, credit_top = sign(s, hs)
            print(f"[{s}] name {hs}px, lockup ends y={lockup_end}, credit at y={credit_top}")
            png = os.path.join(OUT, f"{s}_a3.png")
            await B.render(B.page(W, H, "#000", inner, grain=False), png, W, H, elements=els, bleed_tags=("plate",), crop_tags=("plate", "circle"),
                           page_bg="#000", collision_ignore=[("circle", "sticker")],
                           text_pairs=[("head", "#fff", "#000", 120, True), ("tag", "#fff", "#000", 56, True), ("credit", "#fff", "#000", 28, True)])
            im = Image.open(png).convert("RGB")
            print(f"[{s}] {im.size[0]}x{im.size[1]} px")
            im.save(os.path.join(OUT, f"{s}_a3.pdf"), "PDF", resolution=300)
    print("a3 done ->", OUT)
asyncio.run(main())
