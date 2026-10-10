"""DISCO DIWALI "WHAT'S INSIDE THIS FOLDER" carousel (user, 2026-10-10), 5 slides, feed 1080x1350 + story 1080x1920.
Mechanism borrowed from a reference post: a desktop-UI parody. A context-menu pill (Cut / Copy / Paste / Replace...), a two-weight
title (bold + light), a pixel cursor sitting on a letter, a dropdown list card with one highlighted row, flat blue folders, and
three photos peeking out of a folder front. Dressed in TerraThon: black ground, orchid-bordered cream UI, StretchPro name,
kit shuriken, the DD disco ball / ticket / diya stickers, the user's three real Disco Diwali photos.
TEASER (user, 2026-10-10): tickets are NOT on sale yet and the user does not want them mentioned at all: no ticket copy, no ticket sticker, no link in bio.
Slides: 1 cover (the folder) / 2 dance.jpg / 3 decor.jpg / 4 group.jpg / 5 closer (Paste yourself into this folder).
NO date, venue or price printed anywhere (user: "do not mention date or anything"). Photos: engine/assets/terrathon/dd_photos/.
Adaptations: reference's brand handle -> @ngo.aquaterra; reference's stock selfies -> real DD photos; macOS blue folder -> TT blue.
Run: PYTHONIOENCODING=utf-8 python scratchpad/tt_dd_folder_carousel.py [story]   -> out/collaterals/dd_folder/
"""
import asyncio, base64, importlib.util, os, random, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B, W = tt.core, tt.B, tt.W
lay = tt.load("layout")
_s2 = importlib.util.spec_from_file_location("tt_dd_tickets", os.path.join(ROOT, "scratchpad", "tt_dd_tickets.py"))
ddm = importlib.util.module_from_spec(_s2); _s2.loader.exec_module(ddm)
GROUND, ORCHID, INK, WHITE, CTA_FILL, SLAB = tt.GROUND, tt.ORCHID, tt.INK, tt.WHITE, tt.CTA_FILL, tt.SLAB
GREEN, BLUE, LEMON = "#2FD284", "#0396FF", "#FFC700"
HL = "#BFE3FF"          # the highlighted-row blue of the reference
STORY = len(sys.argv) > 1 and sys.argv[1] == "story"
H = 1920 if STORY else 1350
DY = 230 if STORY else 0          # story: cluster shifts down off the Instagram top zone
FOOT = 270 if STORY else 0        # footer lift off the bottom edge
TOTAL = 5
DDP = "engine/assets/terrathon/dd_photos"
PH = {n: "data:image/jpeg;base64," + base64.b64encode(open(f"{DDP}/{n}.jpg", "rb").read()).decode() for n in ("dance", "decor", "group")}


def rb(x, y, w, h, deg):
    b = lay.rotated_bbox(x, y, w, h, deg)
    return tuple(b) if not isinstance(b, dict) else (b["x"], b["y"], b["w"], b["h"])


FOLDER_SVG = ('<svg width="{w}" height="{h}" viewBox="0 0 200 160" overflow="visible">'
              '<defs><linearGradient id="fg{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9BD0FF"/><stop offset="1" stop-color="' + BLUE + '"/></linearGradient>'
              '<linearGradient id="fb{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6FB6F5"/><stop offset="1" stop-color="#2C86E0"/></linearGradient></defs>'
              '<path d="M8,18 Q8,8 18,8 L72,8 Q80,8 85,15 L92,26 L182,26 Q192,26 192,36 L192,142 Q192,152 182,152 L18,152 Q8,152 8,142 Z" fill="url(#fb{k})" stroke="' + CTA_FILL + '" stroke-width="6" stroke-linejoin="round"/>'
              '<path d="M8,48 Q8,38 18,38 L182,38 Q192,38 192,48 L192,142 Q192,152 182,152 L18,152 Q8,152 8,142 Z" fill="url(#fg{k})" stroke="' + CTA_FILL + '" stroke-width="6" stroke-linejoin="round"/></svg>')

CURSOR = ('<svg width="{s}" height="{s2}" viewBox="0 0 13 21" shape-rendering="crispEdges"><polygon points="1,1 1,17 5,13 8,20 10.5,19 7.5,12.5 13,12.5" '
          'fill="' + HL + '" stroke="' + INK + '" stroke-width="1.4" stroke-linejoin="miter"/></svg>')


class Slide:
    def __init__(self, idx, seed):
        self.idx, self.els, self.parts, self.ign = idx, [], [], []
        rnd = random.Random(seed)
        specks = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.6, .8, 1, 1.3, 1.9]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(520))
        self.parts += [f'<style>{tt.FONT_CSS}</style>', f'<div style="position:absolute;inset:0;background:{GROUND}"></div>',
                       f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">{specks}</svg>']

    def el(self, l, x, y, w, h): self.els.append((l, x, y, w, h))
    def add(self, html): self.parts.append(html)
    def allow(self, *labels):
        for i in range(len(labels)):
            for j in range(i + 1, len(labels)): self.ign.append((labels[i], labels[j]))

    def star(self, tag, x, y, size=104, z=8):
        im, src = tt.crop_to_alpha("shuriken.png"); hh = size * im.height / im.width
        self.add(f'<img src="{src}" class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{hh}px;z-index:{z}">'); self.el(tag, x, y, size, hh)

    def folder(self, tag, x, y, w, k, z=5, deg=0):
        h = w * 0.8
        self.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({deg}deg);z-index:{z}">{FOLDER_SVG.format(w=w, h=h, k=k)}</div>'); self.el(tag, *rb(x, y, w, h, deg))

    def cursor(self, tag, x, y, s=52, z=12):
        self.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;z-index:{z}">{CURSOR.format(s=s, s2=s * 21 / 13)}</div>'); self.el(tag, x, y, s, s * 21 / 13)

    def menu(self, tag, items, x, y, w, hi=None, size=34, tail=True, z=10):
        """The context-menu pill. items: list of labels; hi: index of the highlighted one."""
        h = 78
        cells = ""
        for i, t in enumerate(items):
            on = (i == hi)
            bg = f"background:{HL};" if on else ""
            sep = f"border-left:3px solid rgba(10,10,10,.14);" if i else ""
            fx = 1.45 if i == len(items) - 1 else 1
            cells += (f'<div style="flex:{fx};height:100%;display:flex;align-items:center;justify-content:center;{bg}{sep}font-family:var(--d);font-weight:400;font-size:{size}px;color:{INK};white-space:nowrap">{t}</div>')
        tl = (f'<div style="position:absolute;left:72px;bottom:-24px;width:0;height:0;border-left:20px solid transparent;border-right:20px solid transparent;border-top:24px solid {ORCHID}"></div>'
              f'<div style="position:absolute;left:78px;bottom:-14px;width:0;height:0;border-left:14px solid transparent;border-right:14px solid transparent;border-top:16px solid {CTA_FILL}"></div>') if tail else ""
        self.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;border:6px solid {ORCHID};border-radius:24px;background:{CTA_FILL};'
                 f'display:flex;overflow:hidden;z-index:{z}">{cells}</div>' + (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z}">{tl}</div>' if tail else ""))
        self.el(tag, x, y, w, h + (24 if tail else 0))

    def listcard(self, tag, rows, x, y, w, rh=84, size=36, hi=0, z=9):
        h = rh * len(rows) + 12
        out = ""
        for i, t in enumerate(rows):
            bg = f"background:{HL};" if i == hi else ""
            sep = "" if i == 0 else f"border-top:3px solid rgba(10,10,10,.16);"
            out += f'<div style="height:{rh}px;display:flex;align-items:center;padding:0 22px;{bg}{sep}font-family:var(--d);font-weight:400;font-size:{size}px;color:{INK};white-space:nowrap">{t}</div>'
        self.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;border:6px solid {ORCHID};border-radius:28px;background:{CTA_FILL};'
                 f'padding:0;overflow:hidden;z-index:{z}">{out}</div>'); self.el(tag, x, y, w, h)

    def text(self, tag, txt, x, y, w, size, weight=400, color=WHITE, align="left", z=6, h=None):
        self.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;text-align:{align};color:{color};font-family:var(--d);font-weight:{weight};font-size:{size}px;line-height:1.05;white-space:nowrap;z-index:{z}">{txt}</div>')
        self.el(tag, x, y, w, h or size * .85)

    def footer(self, cta=None):
        ly = H - FOOT - 27 - 56
        self.add(f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:27px;top:{ly}px;height:56px;z-index:9">'); self.el("logo", 27, ly, 320, 56)
        cw, chh = (480, 70) if cta else (150, 50)
        cx, cy = W - 27 - cw, (H - FOOT - 13 - chh) if cta else (H - FOOT - 27 - chh)
        self.el("cta", cx, cy, cw, chh)
        lab = cta or f"{self.idx:02d} / {TOTAL:02d}"
        self.add(f'<div class="measure" data-tag="cta" style="position:absolute;left:{cx}px;top:{cy}px;width:{cw}px;height:{chh}px;box-sizing:border-box;border:6px solid {ORCHID};border-radius:999px;background:{CTA_FILL};'
                 f'display:flex;align-items:center;justify-content:center;z-index:9;font-family:var(--d);font-weight:900;font-size:{30 if cta else 26}px;color:{INK}">{lab}</div>')

    async def title(self, l1, l2, y, w1=900, w2=800, cursor_on_l2=True):
        """Two-weight title (bold NeutralFace + StretchPro name). Returns the y below it."""
        m = await B.measure_text([dict(text=l1, font="d", size=100, weight=900), dict(text=l2, font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT)], extra_css=tt.FONT_CSS)
        p1 = 100 * w1 / m[0]["text_w"]; p2 = 100 * w2 / m[1]["text_w"]
        x1, x2 = (W - w1) / 2, (W - w2) / 2
        self.add(f'<div class="measure" data-tag="t1" style="position:absolute;left:{x1 - 10}px;width:{w1 + 20}px;top:{y}px;text-align:center;color:{WHITE};font-family:var(--d);font-weight:900;font-size:{p1}px;line-height:1;white-space:nowrap;z-index:6">{l1}</div>')
        self.el("t1", x1, y + p1 * .08, w1, p1 * .8)
        y2 = y + p1 * 1.08
        self.add(f'<div class="measure" data-tag="t2" style="position:absolute;left:{x2 - 10}px;width:{w2 + 20}px;top:{y2}px;text-align:center;color:{ORCHID};font-family:StretchPro;-webkit-text-stroke:{tt.ST_STROKE * p2}px {ORCHID};'
                 f'letter-spacing:{tt.ST_LS}em;font-feature-settings:{tt.ST_FEAT};font-size:{p2}px;line-height:1;white-space:nowrap;z-index:6">{l2}</div>')
        self.el("t2", x2, y2 + p2 * .08, w2, p2 * .8)
        return y2 + p2 * 1.0, (x2, y2, p2)

    def html(self): return B.page(W, H, GROUND, "".join(self.parts), grain=False)


def photo_card(s, tag, key, x, y, w, h, deg, pos="50% 50%", z=4):
    s.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;transform:rotate({deg}deg);background:{CTA_FILL};padding:12px;border:6px solid {ORCHID};border-radius:14px;z-index:{z}">'
          f'<img src="{PH[key]}" style="width:100%;height:100%;object-fit:cover;object-position:{pos};display:block;border-radius:4px"></div>'); s.el(tag, *rb(x, y, w, h, deg))


def svg_sticker(s, tag, svg, x, y, w, h, deg=0, z=7):
    s.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;transform:rotate({deg}deg);z-index:{z}">{svg}</div>'); s.el(tag, *rb(x, y, w, h, deg))


async def build():
    out = []
    # ---------------- 1 COVER ----------------
    s = Slide(1, 501)
    s.menu("menu", ["Cut", "Copy", "Paste", "Replace... ▶"], 60, 70 + DY * .5, 760, hi=None)
    s.star("star_tr", W - 24 - 104, 60 + DY * .5)
    ty0 = 250 + DY * .6
    yb, (x2, y2, p2) = await s.title("WHAT’S INSIDE", "DISCO DIWALI", ty0, w1=900, w2=780)
    s.cursor("cur", x2 + 540, y2 + p2 * .55)
    # dropdown list + side folder (reference: right-middle card, left-middle folder)
    ly = yb + 70
    s.folder("fold", 56, ly + 40, 250, "a", z=5)
    s.listcard("list", ["Disco ball energy", "Dance floor chaos", "Your people, dressed up"], 380, ly, 640, hi=0)
    # photos peeking from a folder front
    pt = ly + 330
    ph_h = 360
    bot = H - FOOT - 120                               # folder front bottom
    ftop = pt + ph_h - 120                             # folder front top: hides the photos' lower edge
    photo_card(s, "p_l", "decor", 70, pt + 40, 300, ph_h - 60, -4, "30% 50%", z=4)
    photo_card(s, "p_r", "group", 720, pt + 40, 300, ph_h - 60, 4, "55% 50%", z=4)
    photo_card(s, "p_c", "dance", 300, pt - 10, 480, ph_h - 10, 0, "55% 50%", z=5)
    s.add(f'<div class="measure" data-tag="ffront" style="position:absolute;left:50px;top:{ftop}px;width:{W - 100}px;height:{bot - ftop}px;box-sizing:border-box;border:6px solid {CTA_FILL};border-radius:44px;'
          f'background:linear-gradient(180deg,#9BD0FF,{BLUE});z-index:8;display:flex;align-items:center;justify-content:center;font-family:var(--d);font-weight:900;font-size:34px;color:{INK}">@ngo.aquaterra</div>')
    s.el("ffront", 50, ftop, W - 100, bot - ftop)
    s.footer()
    s.allow("t1", "t2"); s.allow("t2", "cur"); s.allow("list", "fold")
    for p in ("p_l", "p_c", "p_r"): s.allow(p, "ffront")
    s.allow("p_l", "p_c"); s.allow("p_c", "p_r"); s.allow("t2", "star_tr")
    out.append(("1", s)); cover_dims = (ftop, bot)
    # ---------------- 2-4 FILE WINDOWS ----------------
    files = [("2", "dance", "dance.jpg", "DANCE FLOOR", "ZERO SKILL REQUIRED", "50% 40%", ["Open", "Copy", "Share", "Replace... ▶"], 2),
             ("3", "decor", "decor.jpg", "DISCO DECOR", "BALLS, BLOCKS AND A CASSETTE", "50% 60%", ["Open", "Copy", "Share", "Replace... ▶"], 2),
             ("4", "group", "group.jpg", "YOUR PEOPLE", "DRESSED IN THEIR BEST", "50% 45%", ["Open", "Copy", "Share", "Replace... ▶"], 2)]
    for n, key, fname, bold, light, pos, items, hi in files:
        s = Slide(int(n), 510 + int(n))
        s.menu("menu", items, 60, 70 + DY * .5, 760, hi=hi)
        s.star("star_tr", W - 24 - 104, 60 + DY * .5)
        wx, wy, ww = 70, 230 + DY * .6, 940
        bar = 74; ph = 720 if not STORY else 900
        wh = bar + ph + 6
        s.add(f'<div class="measure" data-tag="win" style="position:absolute;left:{wx}px;top:{wy}px;width:{ww}px;height:{wh}px;box-sizing:border-box;border:6px solid {ORCHID};border-radius:30px;background:{CTA_FILL};overflow:hidden;transform:rotate(-1deg);z-index:6">'
              f'<div style="height:{bar}px;display:flex;align-items:center;padding:0 24px;gap:12px;border-bottom:4px solid rgba(10,10,10,.18);background:#E9E1D2">'
              f'<div style="width:22px;height:22px;border-radius:50%;background:{ORCHID}"></div><div style="width:22px;height:22px;border-radius:50%;background:{LEMON}"></div><div style="width:22px;height:22px;border-radius:50%;background:{GREEN}"></div>'
              f'<div style="margin-left:18px;font-family:var(--d);font-weight:900;font-size:32px;color:{INK}">{fname}</div></div>'
              f'<img src="{PH[key]}" style="width:100%;height:{ph - 6}px;object-fit:cover;object-position:{pos};display:block"></div>')
        s.el("win", *rb(wx, wy, ww, wh, -1))
        s.cursor("cur", wx + ww - 250, wy + wh - 200, z=12)
        by = wy + wh + 40
        s.text("h1", bold, 70, by, 760, 84, 900, WHITE)
        s.text("h2", light, 70, by + 92, 780, 44, 400, WHITE)
        s.folder("fold", W - 60 - 150, by + 10, 150, f"b{n}", z=5)
        s.footer(); s.allow("win", "cur"); s.allow("star_tr", "menu"); out.append((n, s))
    # ---------------- 5 CLOSER ----------------
    s = Slide(5, 505)
    s.menu("menu", ["Cut", "Copy", "Paste", "Replace... ▶"], 60, 70 + DY * .5, 760, hi=2)
    s.star("star_tr", W - 24 - 104, 60 + DY * .5)
    yb, (x2, y2, p2) = await s.title("PASTE YOURSELF", "INTO THIS FOLDER", 250 + DY * .6, w1=900, w2=900)
    s.cursor("cur", x2 + 470, y2 + p2 * .55)
    ty = yb + 40
    ball, bh = ddm.disco_ball(380, "b5"); svg_sticker(s, "ball", ball, W - 60 - 380, ty, 380, bh, 6)
    tk, tkh = ddm.diya(340, "d5"); svg_sticker(s, "tkt", tk, 170, ty + 50, 340, tkh, -8)
    ly = ty + max(bh, tkh + 80) + 50
    s.listcard("list", ["Save this folder", "Send it to your people", "More soon"], 190, ly, 700, hi=0)
    s.footer(cta="STAY TUNED"); s.allow("t2", "cur"); s.allow("ball", "tkt"); s.allow("t2", "star_tr")
    out.append(("5", s))
    return out


async def main():
    res = await build()
    outdir = "out/collaterals/dd_folder" + ("_story" if STORY else ""); os.makedirs(outdir, exist_ok=True)
    text_pairs = [("head", WHITE, GROUND, 96, True), ("name", ORCHID, GROUND, 96, True), ("ui", INK, CTA_FILL, 34, False), ("cta", INK, CTA_FILL, 30, True)]
    async with B.session():
        for name, s in res:
            out = f"{outdir}/dd_folder_{name}.png"
            await B.render(s.html(), out, W, H, elements=s.els, text_pairs=text_pairs, containers=("win", "ffront"), page_bg=GROUND, expect_hero=False,
                           collision_ignore=set(map(tuple, s.ign)), margin=12, crop_tags=("win", "p_l", "p_c", "p_r"))
            print("done", out)

asyncio.run(main())
