"""TerraThon STALL POSTERS, A4 PORTRAIT (user, 2026-10-02: "A4 posters for each game to be put at the stall, 5 unique posters for Disco Diwali ticket promotions, and one for the Disco Dash,
one cumulative PDF"). 14 pages: 01 Disco Dash circuit; 02-09 one per game (sticker on a cream plate, numbered badge, PLAY HERE, the Disco Dash rule card with a 1-8 station tracker);
10-14 five Disco Diwali ticket posters (hero disco ball / giant Rs. 550 + ticket / find us with the real DD photo / the night, two real DD photos / win them free at Disco Dash).
Built at 1080x1527 (A4 ratio) and rendered at 2x = 2160x3054 px (about 260 dpi on A4); the cumulative PDF is those PNGs placed at true A4 size (raster, not vector).
Facts only as the user gave them: 8 games (plank removed), finish all 8 with MAXIMUM points, FIRST 5 finishers win free Disco Diwali tickets, any game can be played solo, Disco Diwali tickets Rs. 550 at the DD stall at the
Mini-Fete (3rd + 4th Oct 2026, Turf XL, New Alipore), Disco Diwali is on 10th November (year assumed 2026; venue never supplied, not printed). No per-game rules or scoring (none supplied). HYROX-STYLE per the user.
PRINT: full-bleed black A4, no bleed marks (ask the printer for a bleed proof); the stickers are original artwork, the two DD photos are the user's own.
Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_stall_posters.py   ->  out/collaterals/stall_posters/NN_name.png + terrathon_stall_posters_A4.pdf
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
STORY = False     # 1080x1920 with Instagram UI zones clear (top ~250, bottom ~270)
H, TOTAL = 1527, 1
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


DDP = "engine/assets/terrathon/dd_photos"
PH = {n: b64(f"{DDP}/{n}.jpg", "image/jpeg") for n in ("decor", "group", "dance")}
_s2 = importlib.util.spec_from_file_location("tt_dd_tickets", os.path.join(ROOT, "scratchpad", "tt_dd_tickets.py")); ddm = importlib.util.module_from_spec(_s2); _s2.loader.exec_module(ddm)
GAMES = [("headphones", "GUESS THE SENTENCE", "WITH HEADPHONES"), ("cup_flip", "FLIP THE CUP", None), ("jenga", "JENGA", "WITH DARES"),
         ("darts", "DARTS", None), ("tongue", "TONGUE TWISTERS", None), ("pushup", "PUSH UP CHALLENGE", None),
         ("aim_cup", "AIM THE CUP", None), ("coin_drop", "COIN DROP", None)]
DK = "#0A0A0A"; TEAL = "#0E7C86"; DDATE = "DISCO DIWALI: 10TH NOVEMBER 2026"


def sticker(s, tag, slug, x, y, size, deg=0, z=7):
    s.add(f'<img class="measure" data-tag="{tag}" src="{STK[slug]}" style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;transform:rotate({deg}deg);z-index:{z}">'); s.el(tag, x, y, size, size)


def svg_sticker(s, tag, svg, x, y, w, h, deg=0, z=7):
    s.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;transform:rotate({deg}deg);z-index:{z}">{svg}</div>'); s.el(tag, x, y, w, h)


def slab(s, tag, x, y, w, h, deg=-1.25):
    s.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;transform:rotate({deg}deg);background:{SLAB};border:20px solid {ORCHID};border-radius:52px;z-index:8"></div>'); s.el(tag, *rb(x, y, w, h, deg))


def rows_in(s, sx, sy, sw, sh, rows, tag="row"):
    tot = sum(z for _, z, _c in rows) + (len(rows) - 1) * 20; y = sy + (sh - tot) / 2 - 4
    for i, (txt, z, col) in enumerate(rows):
        s.add(f'<div class="measure" data-tag="{tag}{i}" style="position:absolute;left:{sx + 36}px;width:{sw - 72}px;top:{y}px;text-align:center;color:{col};font-family:var(--d);font-weight:900;font-size:{z}px;line-height:1;white-space:nowrap;z-index:9">{txt}</div>'); s.el(f"{tag}{i}", sx + 36, y, sw - 72, z * .85); y += z + 20
    return [("slab", f"{tag}{i}") for i in range(len(rows))]


def tracker(s, y, active, tag="tracker", x_center=W / 2):
    d, g = 46, 12; tot = 8 * d + 7 * g; x0 = x_center - tot / 2; h = ""
    for i in range(8):
        on = i in active
        h += (f'<div style="position:absolute;left:{i * (d + g)}px;top:0;width:{d}px;height:{d}px;box-sizing:border-box;border-radius:50%;'
              f'background:{ORCHID if on else "transparent"};border:4px solid {ORCHID if on else DK};color:{DK};font-family:var(--d);font-weight:900;'
              f'font-size:22px;display:flex;align-items:center;justify-content:center;line-height:1">{i + 1}</div>')
    s.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x0}px;top:{y}px;width:{tot}px;height:{d}px;z-index:9">{h}</div>'); s.el(tag, x0, y, tot, d)
    return y + d


async def dash_poster():
    s = Slide(1, 701); s.idx = 0; BOT = H - 150
    ty = await s.title("DISCO DASH", "HYROX-STYLE CIRCUIT", big_w=760, sub_w=740, top=104)
    s.star("star_tl", 24, 70); s.star("star_tr", W - 24 - 104, 86)
    pw, px0 = 900, 90; py = ty + 8; ph = int(BOT + 60 - py - 360)
    s.add(f'<div class="measure" data-tag="plate" style="position:absolute;left:{px0}px;top:{py}px;width:{pw}px;height:{ph}px;box-sizing:border-box;transform:rotate(-1deg);background:#F3ECDE;border:16px solid {ORCHID};border-radius:56px;z-index:5"></div>'); s.el("plate", *rb(px0, py, pw, ph, -1))
    cell_w = (pw - 40) / 3; cell_h = (ph - 40) / 3; ss = min(cell_w - 10, cell_h - 6); ign = [("star_tl", "t1"), ("star_tr", "t1")]
    for i, (slug, *_r) in enumerate(GAMES):
        cx = px0 + 20 + (i % 3) * cell_w + (cell_w - ss) / 2 + (cell_w / 2 if i >= 6 else 0); cy = py + 20 + (i // 3) * cell_h + (cell_h - ss) / 2
        sticker(s, f"g{i}", slug, cx, cy, ss, [-4, 3, -3][i % 3], z=8)
        bd = 48; s.add(f'<div class="measure" data-tag="n{i}" style="position:absolute;left:{cx + 6}px;top:{cy + 6}px;width:{bd}px;height:{bd}px;box-sizing:border-box;border-radius:50%;background:{GREEN};border:4px solid {DK};display:flex;align-items:center;justify-content:center;color:{DK};font-family:var(--d);font-weight:900;font-size:24px;line-height:1;z-index:9">{i + 1}</div>'); s.el(f"n{i}", cx + 6, cy + 6, bd, bd)
        ign += [("plate", f"g{i}"), ("plate", f"n{i}"), (f"g{i}", f"n{i}")]
    yy = py + ph + 36
    s.chip("c1", "FINISH ALL 8 WITH MAXIMUM POINTS", (W - 940) / 2, yy, 940, deg=-1.5, size=36); ign.append(("plate", "c1"))
    s.text("l1", "FIRST 5 WIN FREE DISCO DIWALI TICKETS", 20, yy + 112, W - 40, 44, 900, WHITE)
    s.text("l2", "PLAY ANY GAME SOLO  |  3 + 4 OCT, TURF XL, NEW ALIPORE", 20, yy + 168, W - 40, 30, 400, CREAM_HALO)
    s.text("l3", DDATE, 20, yy + 214, W - 40, 36, 900, ORCHID)
    s.footer(cta="SEE YOU 3 + 4 OCT"); return ("01_disco_dash", s, ign)


async def game_poster(n):
    slug, name, sub = GAMES[n]; s = Slide(n + 2, 710 + n); s.idx = 0; BOT = H - 150
    ty = await s.title(name, f"STATION 0{n + 1} OF 08", big_w=min(900, 70 * len(name) + 120), sub_w=560, top=100)
    px0, pw, py = 110, 860, ty + 16; ph = 590
    s.add(f'<div class="measure" data-tag="plate" style="position:absolute;left:{px0}px;top:{py}px;width:{pw}px;height:{ph}px;box-sizing:border-box;transform:rotate(1deg);background:#F3ECDE;border:18px solid {ORCHID};border-radius:60px;z-index:5"></div>'); s.el("plate", *rb(px0, py, pw, ph, 1))
    ss = min(ph - 30, 700); sticker(s, "stk", slug, px0 + (pw - ss) / 2, py + (ph - ss) / 2 - (24 if sub else 0), ss, [-4, 3, -3, 4, -4, 3, -3, 4][n], z=8)
    bd = 150; bx, by = px0 - 46, py - 38
    s.add(f'<div class="measure" data-tag="badge" style="position:absolute;left:{bx}px;top:{by}px;width:{bd}px;height:{bd}px;box-sizing:border-box;border-radius:50%;background:{GREEN};border:8px solid {DK};display:flex;align-items:center;justify-content:center;color:{DK};font-family:var(--d);font-weight:900;font-size:72px;line-height:1;z-index:10">0{n + 1}</div>'); s.el("badge", bx, by, bd, bd)
    ign = [("plate", "stk"), ("plate", "badge"), ("badge", "stk"), ("star_bl", "plate"), ("star_br", "plate"), ("star_br", "stk"), ("star_bl", "stk"), ("star_bl", "play"), ("star_br", "play")]
    if sub: s.chip("sub", sub, (W - 660) / 2, py + ph - 48, 660, deg=-2, size=40); ign += [("plate", "sub"), ("sub", "stk")]
    y2 = py + ph + 60 + (10 if sub else 0)
    s.chip("play", "PLAY HERE", (W - 560) / 2, y2, 560, deg=-2, size=56)
    s.star("star_bl", 70, y2 - 6, 112, z=10); s.star("star_br", W - 70 - 112, y2 + 4, 112, z=10)
    cy_ = y2 + 56 + 40 + 56; chh = 280
    s.add(f'<div class="measure" data-tag="card" style="position:absolute;left:70px;top:{cy_}px;width:940px;height:{chh}px;box-sizing:border-box;border:6px solid {GREEN};border-radius:36px;background:#F3ECDE;z-index:6"></div>'); s.el("card", 70, cy_, 940, chh)
    s.add(f'<div class="measure" data-tag="ch" style="position:absolute;left:{(W - 380) / 2}px;top:{cy_ + 22}px;width:380px;text-align:center;background:{ORCHID};color:{DK};font-family:var(--d);font-weight:900;font-size:28px;line-height:1;padding:9px 0 8px;border-radius:999px;z-index:9">PART OF DISCO DASH</div>'); s.el("ch", (W - 380) / 2, cy_ + 22, 380, 46)
    s.text("c1", "FINISH ALL 8 STATIONS WITH MAXIMUM POINTS", 80, cy_ + 86, 920, 32, 900, DK, z=9)
    s.text("c2", "FIRST 5 WIN FREE DISCO DIWALI TICKETS", 80, cy_ + 132, 920, 32, 900, TEAL, z=9)
    tracker(s, cy_ + 196, {n})
    ign += [("card", t) for t in ("ch", "c1", "c2", "tracker")] + [("play", "card"), ("ch", "c1")]
    s.footer(cta="DISCO DIWALI: 10TH NOV"); return (f"{n + 2:02d}_{slug}", s, ign)


async def dd_posters():
    out = []; BOT = H - 150; SI = [("star_tl", "t1"), ("star_tr", "t1")]
    s = Slide(10, 801); s.idx = 0   # 10: hero disco ball + price slab
    ty = await s.title("DISCO DIWALI", "GET YOUR TICKETS", big_w=800, sub_w=700, top=104)
    s.star("star_tl", 24, 70); s.star("star_tr", W - 24 - 104, 86)
    bw = 700; ball, bh = ddm.disco_ball(bw, "p1"); svg_sticker(s, "ball", ball, (W - bw) / 2, ty + 10, bw, bh)
    sy = ty + 10 + bh + 30; sh = BOT - sy + 20; slab(s, "slab", 100, sy, 880, sh)
    ign = rows_in(s, 100, sy, 880, sh, [("RS. 550", 110, INK), ("AT THE DD TICKET STALL, TURF XL", 30, TEAL), ("3RD + 4TH OCT, MINI-FETE", 30, INK), (DDATE, 30, INK)])
    s.footer(cta="DD TICKET STALL"); out.append(("10_dd_hero_ball", s, ign + [("slab", "ball")] + SI))
    s = Slide(11, 802); s.idx = 0   # 11: giant price + ticket
    ty = await s.title("RS. 550", "DISCO DIWALI TICKETS", big_w=740, sub_w=800, top=104)
    s.star("star_tl", 24, 70); s.star("star_tr", W - 24 - 104, 86)
    tw_ = 900; tk, tkh = ddm.ticket(tw_, "p2"); svg_sticker(s, "tkt", tk, (W - tw_) / 2, ty + 40, tw_, tkh, -7)
    dy_ = ty + 40 + tkh + 90; dw = 330; dya, dyh = ddm.diya(dw, "p2d"); svg_sticker(s, "diya", dya, 70, dy_, dw, dyh, -6)
    s.text("w1", "AT THE DD TICKET STALL", 430, dy_ + 20, 600, 38, 900, WHITE, align="left"); s.text("w2", "TURF XL, NEW ALIPORE", 430, dy_ + 80, 600, 34, 400, WHITE, align="left")
    s.text("w3", "3RD + 4TH OCT", 430, dy_ + 130, 600, 36, 900, ORCHID, align="left"); s.text("w4", "DISCO DIWALI: 10TH NOV", 430, dy_ + 186, 600, 36, 900, WHITE, align="left")
    s.footer(cta="DD TICKET STALL"); out.append(("11_dd_giant_ticket", s, SI + [("tkt", "t3")]))
    s = Slide(12, 803); s.idx = 0   # 12: find us (real DD photo)
    ty = await s.title("FIND US", "AT TERRATHON CRICKET", big_w=620, sub_w=860, top=104)
    s.star("star_tl", 24, 70); s.star("star_tr", W - 24 - 104, 86)
    fh = int((BOT - ty) * 0.52); s.frame("frame", PH["decor"], 90, ty + 20, 900, fh, -2, "50% 55%")
    py_ = ty + 20 + fh + 50
    s.chip("c1", "DD TICKET STALL", 120, py_, 560, deg=-2, size=36)
    s.text("v1", "TURF XL, NEW ALIPORE", 40, py_ + 120, W - 80, 52, 900, WHITE); s.text("v2", "3RD + 4TH OCT", 40, py_ + 188, W - 80, 46, 900, ORCHID)
    s.text("v3", "RS. 550", 40, py_ + 252, W - 80, 54, 900, WHITE); s.text("v4", "DISCO DIWALI: 10TH NOVEMBER", 40, py_ + 326, W - 80, 40, 900, ORCHID)
    s.footer(cta="DD TICKET STALL"); out.append(("12_dd_find_us", s, SI + [("frame", "c1")]))
    s = Slide(13, 804); s.idx = 0   # 13: the night (two real DD photos)
    ty = await s.title("DISCO DIWALI", "BE THERE", big_w=700, sub_w=420, top=104)
    s.star("star_tl", 24, 70); s.star("star_tr", W - 24 - 104, 86)
    fh = int((BOT - ty) * 0.62)
    s.frame("f1", PH["dance"], 50, ty + 30, 560, fh, -4, "50% 45%", z=4); s.frame("f2", PH["group"], 470, ty + 30 + fh * 0.30, 560, int(fh * 0.78), 3.5, "50% 40%", z=5)
    dya, dyh = ddm.diya(260, "p4d"); svg_sticker(s, "diya", dya, 70, ty + 30 + fh - 40, 260, dyh, -8, z=9)
    s.chip("c1", "10TH NOV  |  TICKETS RS. 550", 200, ty + 30 + fh + 90, 760, deg=-2, size=38)
    s.text("v1", "AT THE DD STALL, TURF XL, 3RD + 4TH OCT", 20, ty + 30 + fh + 210, W - 40, 34, 400, WHITE)
    s.footer(cta="DD TICKET STALL"); out.append(("13_dd_the_night", s, SI + [("f1", "f2"), ("f1", "diya"), ("f2", "diya"), ("f2", "c1"), ("f1", "c1"), ("diya", "c1"), ("f2", "star_tr"), ("f2", "v1"), ("c1", "v1"), ("diya", "v1")]))
    s = Slide(14, 805); s.idx = 0   # 14: win them free at Disco Dash
    ty = await s.title("WANT THEM FREE?", "WIN THEM AT DISCO DASH", big_w=700, sub_w=780, top=104)
    s.star("star_tl", 24, 70); s.star("star_tr", W - 24 - 104, 86)
    tk, tkh = ddm.ticket(520, "p5"); svg_sticker(s, "tkt", tk, 40, ty + 30, 520, tkh, -9)
    ball, bh = ddm.disco_ball(440, "p5b"); svg_sticker(s, "ball", ball, W - 40 - 440, ty + 20, 440, bh, 6)
    sy = ty + 30 + max(tkh, bh) + 60; sh = 420; slab(s, "slab", 84, sy, 912, sh)
    ign = rows_in(s, 84, sy, 912, sh, [("FIRST 5 TO FINISH ALL 8", 46, INK), ("MINI-FETE GAMES WIN", 46, INK), ("FREE DISCO DIWALI TICKETS", 36, TEAL), ("DISCO DIWALI IS ON 10TH NOVEMBER", 28, INK)])
    s.chip("c1", "OR BUY AT RS. 550", 220, sy + sh + 60, 640, deg=-2, size=40)
    s.footer(cta="DD TICKET STALL"); out.append(("14_dd_win_free", s, ign + [("slab", "tkt"), ("slab", "ball"), ("star_tl", "t1"), ("star_tr", "t1"), ("tkt", "ball")]))
    return out


async def main():
    res = [await dash_poster()] + [await game_poster(n) for n in range(8)] + await dd_posters()
    outdir = "out/collaterals/stall_posters"; os.makedirs(outdir, exist_ok=True)
    text_pairs = [("head", WHITE, GROUND, 96, True), ("sub", ORCHID, GROUND, 50, True), ("chip", INK, CTA_FILL, 36, True), ("cta", INK, CTA_FILL, 30, True)]
    files = []
    async with B.session():
        for name, s, ign in res:
            out = f"{outdir}/{name}.png"
            await B.render(s.html(), out, W, H, elements=s.els, text_pairs=text_pairs, containers=("slab", "plate", "card"), page_bg=GROUND, expect_hero=False,
                           collision_ignore=set(map(tuple, ign)), margin=12, crop_tags=("frame", "f1", "f2"))
            files.append(out); print("done", out)
    from PIL import Image
    ims = [Image.open(f).convert("RGB") for f in files]; w_in = 8.2677
    ims[0].save("out/collaterals/terrathon_stall_posters_A4.pdf", save_all=True, append_images=ims[1:], resolution=ims[0].size[0] / w_in)
    print("pdf pages:", len(ims), "px", ims[0].size)

asyncio.run(main())
