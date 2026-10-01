"""DISCO DASH PROMO STORIES (user, 2026-10-01: "disco diwali and disco dash promotions in all enticing forms for stories and whatsapp"). Five 1080x1920 story designs, each a different
hook for the same circuit: 1 can-you-finish-all-8 (sticker plate), 2 the prize (giant ticket + disco ball), 3 the eight stations (named tiles), 4 how to win (three steps), 5 see you at the dash.
Rules are only what the user gave: finish all 8 with MAXIMUM points, FIRST 5 finishers (in total) win free Disco Diwali tickets, any game can also be played solo. No numeric points target, no
per-game scoring, no Disco Diwali date/venue printed (none supplied). Mini-Fete facts: 3rd + 4th Oct 2026, Turf XL, New Alipore. "HYROX" appears only as HYROX-STYLE.
Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_disco_dash_promo.py
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
STORY = True     # 1080x1920 with Instagram UI zones clear (top ~250, bottom ~270)
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
         ("aim_cup", "AIM THE CUP", None), ("coin_drop", "COIN DROP", None)]
DK = "#0A0A0A"


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


async def build():
    out = []; BOT = H - FOOT - 150; STAR_IGN = [("star_tl", "t1"), ("star_tr", "t1")]
    # ---- 1 CAN YOU FINISH ALL 9? ----
    s = Slide(1, 501); ty = await s.title("CAN YOU FINISH ALL 8?", "DISCO DASH", big_w=740, sub_w=520, top=104)
    s.star("star_tl", 24, 70 + OY); s.star("star_tr", W - 24 - 104, 86 + OY)
    pw, px0, py = 900, 90, ty + 10; ph = BOT - py - 190
    s.add(f'<div class="measure" data-tag="plate" style="position:absolute;left:{px0}px;top:{py}px;width:{pw}px;height:{ph}px;box-sizing:border-box;transform:rotate(1deg);background:#F3ECDE;border:16px solid {ORCHID};border-radius:56px;z-index:5"></div>'); s.el("plate", *rb(px0, py, pw, ph, 1))
    cw_, chh = (pw - 40) / 3, (ph - 40) / 3; ss = min(cw_ - 10, chh - 6); ign = list(STAR_IGN)
    for i, (slug, *_r) in enumerate(GAMES):
        cx = px0 + 20 + (i % 3) * cw_ + (cw_ - ss) / 2 + (cw_ / 2 if i >= 6 else 0); cy = py + 20 + (i // 3) * chh + (chh - ss) / 2; sticker(s, f"g{i}", slug, cx, cy, ss, [-4, 3, -3][i % 3], z=8); ign.append(("plate", f"g{i}"))
    s.chip("c1", "FIRST 5 WIN FREE DISCO DIWALI TICKETS", (W - 960) / 2, py + ph + 40, 960, deg=-1.5, size=30); ign.append(("plate", "c1"))
    s.footer(cta="SEE YOU 3 + 4 OCT"); out.append(("1", s, ign))
    # ---- 2 THE PRIZE ----
    s = Slide(2, 502); ty = await s.title("FREE TICKETS", "FOR THE FIRST 5 TO FINISH", big_w=700, sub_w=760, top=104)
    s.star("star_tl", 24, 70 + OY); s.star("star_tr", W - 24 - 104, 86 + OY)
    ball, bh = ddm.disco_ball(560, "pb"); svg_sticker(s, "ball", ball, W - 40 - 560, ty + 10, 560, bh, 5, z=6)
    tk, tkh = ddm.ticket(780, "pt"); svg_sticker(s, "tkt", tk, 40, ty + bh * 0.55, 780, tkh, -8, z=8)
    sy = ty + bh * 0.55 + tkh + 70
    s.chip("c1", "DISCO DIWALI TICKETS", 130, sy, 820, deg=-2, size=44)
    s.text("w1", "WIN THEM AT DISCO DASH", 40, sy + 130, W - 80, 48, 900, WHITE); s.text("w2", "THE MINI-FETE CIRCUIT, 3RD + 4TH OCT", 40, sy + 196, W - 80, 32, 400, CREAM_HALO)
    s.footer(cta="SEE YOU 3 + 4 OCT"); out.append(("2", s, STAR_IGN + [("ball", "tkt"), ("tkt", "c1"), ("ball", "c1")]))
    # ---- 3 THE NINE STATIONS ----
    s = Slide(3, 503); ty = await s.title("8 STATIONS", "ONE CIRCUIT", big_w=640, sub_w=520, top=104)
    s.star("star_tl", 24, 70 + OY); s.star("star_tr", W - 24 - 104, 86 + OY)
    gap = 22; tw_, th_ = (968 - 2 * gap) / 3, (BOT + 20 - ty - 14 - 2 * gap) / 3; ign = list(STAR_IGN)
    for i, (slug, name, sub) in enumerate(GAMES):
        x = 56 + (i % 3) * (tw_ + gap) + ((tw_ + gap) / 2 if i >= 6 else 0); y = ty + 14 + (i // 3) * (th_ + gap)
        s.add(f'<div class="measure" data-tag="tile{i}" style="position:absolute;left:{x}px;top:{y}px;width:{tw_}px;height:{th_}px;box-sizing:border-box;border:6px solid {GREEN};border-radius:30px;background:#F3ECDE;z-index:6"></div>'); s.el(f"tile{i}", x, y, tw_, th_)
        ss = min(tw_ - 40, th_ - 120); sticker(s, f"k{i}", slug, x + (tw_ - ss) / 2, y + 10, ss, [-4, 3, -3][i % 3], z=8)
        s.add(f'<div class="measure" data-tag="tn{i}" style="position:absolute;left:{x + 8}px;top:{y + th_ - 98}px;width:{tw_ - 16}px;height:84px;display:flex;align-items:center;justify-content:center;text-align:center;color:{INK};font-family:var(--d);font-weight:900;font-size:26px;line-height:1.05;z-index:9"><span>{i + 1}. {name}</span></div>'); s.el(f"tn{i}", x + 8, y + th_ - 98, tw_ - 16, 60)
        ign += [(f"tile{i}", f"k{i}"), (f"tile{i}", f"tn{i}")]
    s.footer(); out.append(("3", s, ign))
    # ---- 4 HOW TO WIN ----
    s = Slide(4, 504); ty = await s.title("HOW TO WIN", "DISCO DASH", big_w=700, sub_w=520, top=104)
    s.star("star_tl", 24, 70 + OY); s.star("star_tr", W - 24 - 104, 86 + OY)
    steps = [("1", "FINISH ALL 8 STATIONS", None), ("2", "WITH MAXIMUM POINTS", None), ("3", "BE ONE OF THE FIRST 5", "WIN FREE DISCO DIWALI TICKETS")]
    gap = 34; chh = (BOT - ty - 100 - 2 * gap) / 3; ign = list(STAR_IGN)
    for i, (n, a, b) in enumerate(steps):
        y = ty + 24 + i * (chh + gap); x = 70; cw_ = 940
        s.add(f'<div class="measure" data-tag="card{i}" style="position:absolute;left:{x}px;top:{y}px;width:{cw_}px;height:{chh}px;box-sizing:border-box;border:6px solid {GREEN};border-radius:36px;background:#F3ECDE;z-index:6"></div>'); s.el(f"card{i}", x, y, cw_, chh)
        bd = min(150, chh - 40); s.add(f'<div class="measure" data-tag="bd{i}" style="position:absolute;left:{x + 28}px;top:{y + (chh - bd) / 2}px;width:{bd}px;height:{bd}px;box-sizing:border-box;border-radius:50%;background:{ORCHID};border:7px solid {DK};display:flex;align-items:center;justify-content:center;color:{DK};font-family:var(--d);font-weight:900;font-size:{int(bd * .5)}px;line-height:1;z-index:9">{n}</div>'); s.el(f"bd{i}", x + 28, y + (chh - bd) / 2, bd, bd)
        tx = x + 28 + bd + 30; tw2 = x + cw_ - 24 - tx
        s.add(f'<div class="measure" data-tag="tx{i}" style="position:absolute;left:{tx}px;top:{y + (chh - (110 if b else 56)) / 2}px;width:{tw2}px;color:{INK};font-family:var(--d);font-weight:900;font-size:{int(min(44, tw2 / (len(a) * .74)))}px;line-height:1.05;white-space:nowrap;z-index:9">{a}</div>'); s.el(f"tx{i}", tx, y + (chh - (110 if b else 56)) / 2, tw2, 48)
        if b: s.add(f'<div class="measure" data-tag="tb{i}" style="position:absolute;left:{tx}px;top:{y + (chh - 110) / 2 + 62}px;width:{tw2}px;color:#0E7C86;font-family:var(--d);font-weight:900;font-size:{int(min(34, tw2 / (len(b) * .74)))}px;line-height:1;white-space:nowrap;z-index:9">{b}</div>'); s.el(f"tb{i}", tx, y + (chh - 110) / 2 + 62, tw2, 34)
        ign += [(f"card{i}", t) for t in (f"bd{i}", f"tx{i}", f"tb{i}")]
    s.chip("c1", "OR PLAY ANY GAME SOLO", 250, ty + 24 + 3 * chh + 2 * gap + 36, 580, deg=-2, size=30)
    s.footer(cta="SEE YOU 3 + 4 OCT"); out.append(("4", s, ign + [("card2", "c1")]))
    # ---- 5 SEE YOU AT THE DASH ----
    s = Slide(5, 505); ty = await s.title("SEE YOU AT THE DASH", "HYROX-STYLE CIRCUIT", big_w=800, sub_w=720, top=104)
    s.star("star_tl", 24, 70 + OY); s.star("star_tr", W - 24 - 104, 86 + OY)
    im, src = tt.crop_to_alpha("carnival.png"); chh = BOT - ty - 400; cww = chh * im.width / im.height; cx0 = (W - cww) / 2; cy0 = ty + 10
    s.add(f'<img class="measure" data-tag="carnival" src="{src}" style="position:absolute;left:{cx0}px;top:{cy0}px;width:{cww}px;height:{chh}px;transform:rotate(4deg);z-index:7">'); s.el("carnival", *rb(cx0, cy0, cww, chh, 4))
    ly = cy0 + chh + 50
    s.text("d1", "SAT 3 + SUN 4 OCT, 2026", 20, ly, W - 40, 54, 900, WHITE); s.text("d2", "TURF XL, NEW ALIPORE", 20, ly + 70, W - 40, 42, 400, WHITE)
    s.chip("c1", "FIRST 5 FINISHERS WIN FREE TICKETS", (W - 900) / 2, ly + 150, 900, deg=-1.5, size=32)
    s.footer(cta="SEE YOU 3 + 4 OCT"); out.append(("5", s, STAR_IGN))
    return out


async def main():
    res = await build(); outdir = "out/collaterals/stories"; os.makedirs(outdir, exist_ok=True)
    text_pairs = [("head", WHITE, GROUND, 96, True), ("sub", ORCHID, GROUND, 50, True), ("chip", INK, CTA_FILL, 32, True), ("idx", INK, CTA_FILL, 26, True), ("cta", INK, CTA_FILL, 30, True)]
    async with B.session():
        for name, s, ign in res:
            out = f"{outdir}/disco_dash_promo_story_{name}.png"
            await B.render(s.html(), out, W, H, elements=s.els, text_pairs=text_pairs, containers=tuple(l for l, *_ in s.els if l.startswith(("card", "tile")) or l in ("slab", "plate")), page_bg=GROUND,
                           expect_hero=False, collision_ignore=set(map(tuple, ign)), margin=12)
            print("done", out)

asyncio.run(main())
