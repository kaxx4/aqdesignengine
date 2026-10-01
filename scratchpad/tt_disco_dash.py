"""TerraThon x DISCO DASH: a HYROX-STYLE CIRCUIT of the nine Mini-Fete games, played to WIN FREE DISCO DIWALI TICKETS (user, 2026-10-01). Formats: a single static post, a 5-slide
carousel (cover with the kit's carnival sticker, stations 01-03 / 04-06 / 07-09 as cards with the improved game stickers, how-to-win closer), each in FEED 1080x1350 and STORY 1080x1920.
Rules as the user gave them: finish all nine with MAXIMUM POINTS; the FIRST 5 to finish win free Disco Diwali tickets (in total, not per day); each game can also be played on its own.
The user did not give a numeric points target ("maximum points") or per-game scoring, so none is printed. The Disco Diwali event's own date/venue were never supplied, so only the Mini-Fete's
(3rd + 4th Oct 2026, Turf XL, New Alipore, open to all) is printed. "Hyrox" is a third-party brand; used only as "HYROX-STYLE" at the user's request (confirm before posting).
Sticker art: scratchpad/tt_minigame_stickers.py (nine redrawn game icons); ticket and disco ball come from scratchpad/tt_dd_tickets.py (the die-cut SVG kit already used for the Rs. 550 graphic).
Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_disco_dash.py [story]
"""
import asyncio, base64, importlib.util, os, random, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B, W = tt.core, tt.B, tt.W
lay = tt.load("layout")
GROUND, ORCHID, CREAM_HALO, INK, WHITE, CTA_FILL, SLAB = tt.GROUND, tt.ORCHID, tt.CREAM_HALO, tt.INK, tt.WHITE, tt.CTA_FILL, tt.SLAB
GREEN = "#2FD284"
import sys
STORY = "story" in sys.argv[1:]     # 1080x1920 with Instagram UI zones clear (top ~250, bottom ~270)
H, TOTAL = (1920 if STORY else 1350), 5
OY = 200 if STORY else 0          # content drop below the top UI zone
EXTRA = 130 if STORY else 0       # extra vertical room spent on bigger frames and rows
FOOT = 270 if STORY else 0        # footer lift off the bottom edge
A = "engine/assets/terrathon/minigames"


def b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


STK = {n: b64(f"{A}/{n}.svg", "image/svg+xml") for n in ("headphones", "cup_flip", "jenga", "darts", "tongue", "pushup", "plank", "aim_cup", "coin_drop")}


def rb(x, y, w, h, deg):
    b = lay.rotated_bbox(x, y, w, h, deg)
    return tuple(b) if not isinstance(b, dict) else (b["x"], b["y"], b["w"], b["h"])


class Slide:
    def __init__(self, idx, seed):
        self.idx, self.els, self.parts = idx, [], []
        rnd = random.Random(seed)
        specks = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.6, .8, 1, 1.3, 1.9]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(520))
        self.parts += [f'<style>{tt.FONT_CSS}</style>', f'<div style="position:absolute;inset:0;background:{GROUND}"></div>',
                       f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">{specks}</svg>']

    def el(self, l, x, y, w, h): self.els.append((l, x, y, w, h))
    def add(self, html): self.parts.append(html)

    async def title(self, big, sub, big_w=780, sub_w=800, top=100):
        top += OY
        big = re.sub(r'([A-Z])(?=\1)', '\\1\u200c', big).replace("'", "\u2019")   # ZWNJ stops StretchPro's doubled-letter ligature (LL, EE) from stretching
        m = await B.measure_text([dict(text=big, font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT),
                                  dict(text=sub, font="SigmarOne", size=50, weight=400, letter_spacing=f"{tt.SG_LS}em")], extra_css=tt.FONT_CSS)
        tpx = 100 * big_w / m[0]["text_w"]; spx = 50 * min(1.0, sub_w / m[1]["text_w"])
        self.text("t1", "TERRATHON MINI-FETE", (W - 700) / 2, top - 52, 700, 38, 400, CREAM_HALO)
        self.add(f'<div class="measure" data-tag="t2" style="position:absolute;left:{(W - big_w - 20) / 2}px;width:{big_w + 20}px;top:{top}px;text-align:center;color:{WHITE};font-family:StretchPro;-webkit-text-stroke:{tt.ST_STROKE * tpx}px {WHITE};'
                 f'letter-spacing:{tt.ST_LS}em;font-feature-settings:{tt.ST_FEAT};font-size:{tpx}px;line-height:1;white-space:nowrap;z-index:6">{big}</div>')
        self.el("t2", (W - big_w) / 2, top + 4, big_w, tpx * .82)
        sy = top + tpx * 1.05
        self.add(f'<div class="measure" data-tag="t3" style="position:absolute;left:{(W - sub_w - 20) / 2}px;width:{sub_w + 20}px;top:{sy}px;text-align:center;color:{ORCHID};font-family:SigmarOne;'
                 f'-webkit-text-stroke:{tt.SG_STROKE * spx}px {ORCHID};letter-spacing:{tt.SG_LS}em;font-size:{spx}px;line-height:1;white-space:nowrap;z-index:6">{sub}</div>')
        self.el("t3", (W - sub_w) / 2, sy + 2, sub_w, spx * .82)
        return sy + spx + 20

    def text(self, tag, txt, x, y, w, size, weight=400, color=WHITE, align="center", z=6):
        self.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;text-align:{align};color:{color};font-family:var(--d);font-weight:{weight};font-size:{size}px;line-height:1.05;white-space:nowrap;z-index:{z}">{txt}</div>')
        self.el(tag, x, y, w, size * .85)

    def star(self, tag, x, y, size=104, z=8):
        im, src = tt.crop_to_alpha("shuriken.png"); hh = size * im.height / im.width
        self.add(f'<img src="{src}" class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{hh}px;z-index:{z}">'); self.el(tag, x, y, size, hh)

    def logo_badge(self, tag, x, y, size, ring=10, z=9):
        self.add(f'<img class="measure" data-tag="{tag}" src="{LOGO}" style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;border-radius:50%;box-sizing:border-box;border:{ring}px solid {ORCHID};z-index:{z}">'); self.el(tag, x, y, size, size)

    def chip(self, tag, txt, x, y, w, deg=-3, size=40, z=9):
        h = size + 40
        self.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;transform:rotate({deg}deg);border:6px solid {ORCHID};border-radius:999px;'
                 f'background:{CTA_FILL};display:flex;align-items:center;justify-content:center;white-space:nowrap;font-family:var(--d);font-weight:900;font-size:{size}px;line-height:1;color:{INK};z-index:{z}">{txt}</div>')
        self.el(tag, *rb(x, y, w, h, deg))

    def frame(self, tag, src, x, y, w, h, deg, pos="50% 50%", z=4):
        self.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;transform:rotate({deg}deg);border:12px solid {ORCHID};border-radius:44px;overflow:hidden;background:#111;z-index:{z}">'
                 f'<img src="{src}" style="width:100%;height:100%;object-fit:cover;object-position:{pos};display:block"></div>'); self.el(tag, *rb(x, y, w, h, deg))

    def box(self, tag, x, y, w, h, inner, pad="16px 22px"):
        self.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;border:6px solid {GREEN};border-radius:32px;background:{CTA_FILL};'
                 f'padding:{pad};color:{INK};font-family:var(--d);z-index:6;overflow:hidden">{inner}</div>'); self.el(tag, x, y, w, h)

    def footer(self, cta=None):
        ly = H - FOOT - 27 - 56
        self.add(f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:27px;top:{ly}px;height:56px;z-index:9">'); self.el("logo", 27, ly, 320, 56)
        if cta:
            cw, chh = 480, 70; cx, cy = W - 27 - cw, H - FOOT - 13 - chh; self.el("cta", cx, cy, cw, chh)
            self.add(f'<div class="measure" data-tag="cta" style="position:absolute;left:{cx}px;top:{cy}px;width:{cw}px;height:{chh}px;box-sizing:border-box;border:6px solid {ORCHID};border-radius:999px;background:{CTA_FILL};'
                     f'display:flex;align-items:center;justify-content:center;z-index:9;font-family:var(--d);font-weight:900;font-size:30px;color:{INK}">{cta}</div>')
        else:
            tw, th = 150, 50; tx, ty = W - 27 - tw, H - FOOT - 27 - th; self.el("idx", tx, ty, tw, th)
            self.add(f'<div class="measure" data-tag="idx" style="position:absolute;left:{tx}px;top:{ty}px;width:{tw}px;height:{th}px;box-sizing:border-box;border:5px solid {ORCHID};border-radius:999px;background:{CTA_FILL};'
                     f'display:flex;align-items:center;justify-content:center;z-index:9;font-family:var(--d);font-weight:900;font-size:26px;color:{INK}">{self.idx:02d} / {TOTAL:02d}</div>')

    def html(self): return B.page(W, H, GROUND, "".join(self.parts), grain=False)


def head_row(chip, price=None, price_px=40):
    p = (f'<div style="background:{GREEN};color:{INK};font-weight:900;font-size:{price_px}px;line-height:1;padding:9px 20px 8px;border-radius:999px;white-space:nowrap">{price}</div>' if price else "")
    return (f'<div style="display:flex;align-items:center;justify-content:space-between;gap:16px"><div style="background:{ORCHID};color:{INK};font-weight:900;font-size:30px;line-height:1;padding:9px 20px 8px;border-radius:999px;white-space:nowrap">{chip}</div>{p}</div>')


def rows_html(rows, rh, size, price_col=False):
    out = ""
    for i, r in enumerate(rows):
        name, price = (r if isinstance(r, tuple) else (r, None))
        sep = f"border-top:3px solid rgba(10,10,10,.22);" if i else ""
        pr = (f'<div style="font-weight:900;font-size:{size}px;white-space:nowrap">{price}</div>' if price else "")
        out += f'<div style="height:{rh}px;{sep}display:flex;align-items:center;justify-content:space-between;gap:14px;font-size:{size}px;line-height:1.08;font-weight:400"><div>{name}</div>{pr}</div>'
    return out


_s2 = importlib.util.spec_from_file_location("tt_dd_tickets", os.path.join(ROOT, "scratchpad", "tt_dd_tickets.py")); ddm = importlib.util.module_from_spec(_s2); _s2.loader.exec_module(ddm)
GAMES = [("headphones", "GUESS THE SENTENCE", "WITH HEADPHONES"), ("cup_flip", "FLIP THE CUP", None), ("jenga", "JENGA", "WITH DARES"),
         ("darts", "DARTS", None), ("tongue", "TONGUE TWISTERS", None), ("pushup", "PUSH UP CHALLENGE", None),
         ("plank", "PLANK CHALLENGE", None), ("aim_cup", "AIM THE CUP", None), ("coin_drop", "COIN DROP", None)]
DK = "#0A0A0A"


def sticker(s, tag, slug, x, y, size, deg=0, z=7):
    s.add(f'<img class="measure" data-tag="{tag}" src="{STK[slug]}" style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;transform:rotate({deg}deg);z-index:{z}">')
    s.el(tag, x, y, size, size)


def svg_sticker(s, tag, svg, x, y, w, h, deg=0, z=7):
    s.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;transform:rotate({deg}deg);z-index:{z}">{svg}</div>'); s.el(tag, x, y, w, h)


def tracker(s, y, active, tag="tracker"):
    d, g = 46, 12; tot = 9 * d + 8 * g; x0 = (W - tot) / 2; h = ""
    for i in range(9):
        on = i in active
        h += (f'<div style="position:absolute;left:{x0 + i * (d + g) - x0}px;top:0;width:{d}px;height:{d}px;box-sizing:border-box;border-radius:50%;'
              f'background:{ORCHID if on else "transparent"};border:4px solid {ORCHID if on else CREAM_HALO};color:{INK if on else CREAM_HALO};font-family:var(--d);font-weight:900;'
              f'font-size:22px;display:flex;align-items:center;justify-content:center;line-height:1">{i + 1}</div>')
    s.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x0}px;top:{y}px;width:{tot}px;height:{d}px;z-index:7">{h}</div>'); s.el(tag, x0, y, tot, d)
    return y + d


async def build():
    out = []
    BOT = H - FOOT - 150
    # ================= SINGLE STATIC POST =================
    s = Slide(1, 301); s.idx = 0
    ty = await s.title("DISCO DASH", "HYROX-STYLE CIRCUIT", big_w=730, sub_w=720, top=104)
    s.star("star_tl", 24, 70 + OY); s.star("star_tr", W - 24 - 104, 86 + OY)
    pw, px0 = 900, 90; py = ty + 8; ph = int(BOT + 70 - py - 230)
    s.add(f'<div class="measure" data-tag="plate" style="position:absolute;left:{px0}px;top:{py}px;width:{pw}px;height:{ph}px;box-sizing:border-box;transform:rotate(-1deg);background:#F3ECDE;border:16px solid {ORCHID};border-radius:56px;z-index:5"></div>'); s.el("plate", *rb(px0, py, pw, ph, -1))
    cell_w = (pw - 40) / 3; cell_h = (ph - 40) / 3; ss = min(cell_w - 10, cell_h - 6)
    ign = [("star_tl", "t1"), ("star_tr", "t1")]
    for i, (slug, *_r) in enumerate(GAMES):
        cx = px0 + 20 + (i % 3) * cell_w + (cell_w - ss) / 2; cy = py + 20 + (i // 3) * cell_h + (cell_h - ss) / 2
        sticker(s, f"g{i}", slug, cx, cy, ss, [-4, 3, -3][i % 3], z=8)
        bd = 44; s.add(f'<div class="measure" data-tag="n{i}" style="position:absolute;left:{cx + 6}px;top:{cy + 6}px;width:{bd}px;height:{bd}px;box-sizing:border-box;border-radius:50%;background:{GREEN};border:4px solid {DK};display:flex;align-items:center;justify-content:center;color:{DK};font-family:var(--d);font-weight:900;font-size:22px;line-height:1;z-index:9">{i + 1}</div>'); s.el(f"n{i}", cx + 6, cy + 6, bd, bd)
        ign += [("plate", f"g{i}"), ("plate", f"n{i}"), (f"g{i}", f"n{i}")]
    yy = py + ph + (34 if STORY else 22)
    s.chip("c1", "FINISH ALL 9 WITH MAXIMUM POINTS", (W - 940) / 2, yy, 940, deg=-1.5, size=34); ign += [("plate", "c1")]
    s.text("l1", "FIRST 5 WIN FREE DISCO DIWALI TICKETS", 20, yy + 104, W - 40, 40, 900, WHITE)
    s.text("l2", "OR PLAY ANY GAME SOLO", 20, yy + 154, W - 40, 30, 400, CREAM_HALO)
    s.footer(cta="SEE YOU 3 + 4 OCT"); out.append(("single", s, ign))
    # ================= CAROUSEL =================
    # ---- 1 COVER ----
    s = Slide(1, 311)
    ty = await s.title("DISCO DASH", "HYROX-STYLE CIRCUIT", big_w=730, sub_w=720, top=104)
    s.star("star_tl", 24, 70 + OY); s.star("star_tr", W - 24 - 104, 86 + OY)
    im, src = tt.crop_to_alpha("carnival.png"); chh = BOT - ty - 290; cww = chh * im.width / im.height; cx0 = (W - cww) / 2; cy0 = ty + 20
    s.add(f'<img class="measure" data-tag="carnival" src="{src}" style="position:absolute;left:{cx0}px;top:{cy0}px;width:{cww}px;height:{chh}px;transform:rotate(-4deg);z-index:7">'); s.el("carnival", *rb(cx0, cy0, cww, chh, -4))
    ly = cy0 + chh + 40
    s.text("w1", "9 STATIONS. FINISH ALL.", 20, ly, W - 40, 50, 900, WHITE)
    s.text("w2", "FIRST 5 WIN FREE DISCO DIWALI TICKETS", 20, ly + 64, W - 40, 38, 900, ORCHID)
    s.chip("swipe", "SWIPE FOR THE 9 STATIONS", (W - 760) / 2, ly + 118, 760, deg=-2, size=34)
    s.footer(); out.append(("c1", s, [("star_tl", "t1"), ("star_tr", "t1"), ("swipe", "w2")]))
    # ---- 2-4 STATIONS ----
    for k in range(3):
        s = Slide(k + 2, 312 + k)
        ty = await s.title("DISCO DASH", f"STATIONS 0{3 * k + 1} TO 0{3 * k + 3}", big_w=730, sub_w=640, top=96)
        s.star("star_tl", 24, 60 + OY); s.star("star_tr", W - 24 - 104, 74 + OY)
        yb = tracker(s, ty + 4, {3 * k, 3 * k + 1, 3 * k + 2})
        gap = 38; y0 = yb + 34; ch = (BOT + 20 - y0 - 2 * gap) / 3; ign = [("star_tl", "t1"), ("star_tr", "t1")]
        for r in range(3):
            n = 3 * k + r; slug, name, sub = GAMES[n]
            y = y0 + r * (ch + gap); x = 56; cw = 968
            s.add(f'<div class="measure" data-tag="card{r}" style="position:absolute;left:{x}px;top:{y}px;width:{cw}px;height:{ch}px;box-sizing:border-box;border:6px solid {GREEN};border-radius:34px;background:#F3ECDE;z-index:6"></div>'); s.el(f"card{r}", x, y, cw, ch)
            ss = min(ch - 4, 250); sticker(s, f"stk{r}", slug, x + 14, y + (ch - ss) / 2, ss, [-4, 3, -3][r], z=8)
            bd = 104; bx = x + cw - 28 - bd; by = y + (ch - bd) / 2
            s.add(f'<div class="measure" data-tag="bdg{r}" style="position:absolute;left:{bx}px;top:{by}px;width:{bd}px;height:{bd}px;box-sizing:border-box;border-radius:50%;background:{ORCHID};border:6px solid {DK};display:flex;align-items:center;justify-content:center;color:{DK};font-family:var(--d);font-weight:900;font-size:48px;line-height:1;z-index:9">0{n + 1}</div>'); s.el(f"bdg{r}", bx, by, bd, bd)
            tx = x + 14 + ss + 20; tw_ = bx - 18 - tx
            nsz = int(min(52, tw_ / (len(name) * 0.74))); nh = nsz * 1.02; ny = y + (ch - nh - (46 if sub else 0)) / 2
            s.add(f'<div class="measure" data-tag="nm{r}" style="position:absolute;left:{tx}px;top:{ny}px;width:{tw_}px;color:{INK};font-family:var(--d);font-weight:900;font-size:{nsz}px;line-height:1.02;white-space:nowrap;z-index:9">{name}</div>'); s.el(f"nm{r}", tx, ny, tw_, nh)
            if sub: s.add(f'<div class="measure" data-tag="sb{r}" style="position:absolute;left:{tx}px;top:{ny + nh + 8}px;width:{tw_}px;color:{INK};font-family:var(--d);font-weight:400;font-size:34px;line-height:1;white-space:nowrap;z-index:9">{sub}</div>'); s.el(f"sb{r}", tx, ny + nh + 8, tw_, 34)
            ign += [(f"card{r}", t) for t in (f"stk{r}", f"bdg{r}", f"nm{r}", f"sb{r}")]
            if r < 2:   # a dotted link to the next station
                for d in range(3): s.add(f'<div style="position:absolute;left:{bx + bd / 2 - 5}px;top:{y + ch + 6 + d * 10}px;width:10px;height:10px;border-radius:50%;background:{ORCHID};z-index:7"></div>')
        if k == 0: s.chip("start", "START", 330, y0 - 34, 190, deg=-4, size=28); ign += [("card0", "start")]
        if k == 2: s.chip("fin", "FINISH", 790, y0 + 2 * (ch + gap) - 30, 220, deg=4, size=28); ign += [("card2", "fin"), ("fin", "bdg2")]
        s.footer(); out.append((f"c{k + 2}", s, ign))
    # ---- 5 HOW TO WIN ----
    s = Slide(5, 316)
    ty = await s.title("HOW TO WIN", "DISCO DASH", big_w=700, sub_w=520, top=96)
    s.star("star_tl", 24, 60 + OY); s.star("star_tr", W - 24 - 104, 74 + OY)
    sx, sy, sw, sh = 84, ty + 14, 912, 380 + (EXTRA // 4)
    s.add(f'<div class="measure" data-tag="slab" style="position:absolute;left:{sx}px;top:{sy}px;width:{sw}px;height:{sh}px;box-sizing:border-box;transform:rotate(-1.25deg);background:{SLAB};border:20px solid {ORCHID};border-radius:52px;z-index:8"></div>'); s.el("slab", *rb(sx, sy, sw, sh, -1.25))
    rows = [("FINISH ALL 9 STATIONS", 50, INK), ("WITH MAXIMUM POINTS", 50, INK), ("FIRST 5 WIN FREE DISCO DIWALI TICKETS", 34, "#0E7C86")]
    tot = sum(z for _, z, _c in rows) + 2 * 22; ty2 = sy + (sh - tot) / 2 - 4
    for i, (txt, z, col) in enumerate(rows):
        s.add(f'<div class="measure" data-tag="row{i}" style="position:absolute;left:{sx + 36}px;width:{sw - 72}px;top:{ty2}px;text-align:center;color:{col};font-family:var(--d);font-weight:900;font-size:{z}px;line-height:1;white-space:nowrap;z-index:9">{txt}</div>'); s.el(f"row{i}", sx + 36, ty2, sw - 72, z * .85); ty2 += z + 22
    ign = [("slab", f"row{i}") for i in range(3)]
    ry = sy + sh + 40 + (EXTRA / 3)
    tk, tkh = ddm.ticket(320, "tkA"); svg_sticker(s, "tkt", tk, 40, ry + 30, 320, tkh, -8)
    ball, bh = ddm.disco_ball(290, "dbA"); svg_sticker(s, "ball", ball, W - 40 - 290, ry - 10, 290, bh, 6)
    s.chip("solo", "OR PLAY ANY GAME SOLO", 340, ry + 78, 400, deg=-2, size=24)
    ly = ry + max(tkh, bh) + 60 + (EXTRA // 4)
    s.text("d1", "SAT 3 + SUN 4 OCT, 2026", 20, ly, W - 40, 54, 900, WHITE)
    s.text("d2", "TURF XL, NEW ALIPORE", 20, ly + 68, W - 40, 42, 400, WHITE)
    s.footer(cta="SEE YOU 3 + 4 OCT"); out.append(("c5", s, ign + [("slab", "tkt"), ("slab", "ball"), ("tkt", "solo"), ("ball", "solo"), ("star_tl", "t1"), ("star_tr", "t1")]))
    return out


async def main():
    res = await build()
    outdir = "out/collaterals/stories" if STORY else "out/collaterals/disco_dash"; os.makedirs(outdir, exist_ok=True)
    text_pairs = [("head", WHITE, GROUND, 96, True), ("sub", ORCHID, GROUND, 50, True), ("chip", INK, CTA_FILL, 34, True), ("idx", INK, CTA_FILL, 26, True), ("cta", INK, CTA_FILL, 30, True)]
    async with B.session():
        for name, s, ign in res:
            out = f"{outdir}/disco_dash_{'story_' if STORY else ''}{name}.png"
            await B.render(s.html(), out, W, H, elements=s.els, text_pairs=text_pairs, containers=tuple(l for l, *_ in s.els if l.startswith("card") or l in ("slab", "plate")), page_bg=GROUND,
                           expect_hero=False, collision_ignore=set(map(tuple, ign)), margin=12)
            print("done", out)

asyncio.run(main())
