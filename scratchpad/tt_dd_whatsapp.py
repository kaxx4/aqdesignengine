"""DISCO DIWALI + DISCO DASH WHATSAPP GRAPHICS (feed 4:5 1080x1350), user 2026-10-01. Two designs that sit beside the existing Rs. 550 ticket graphic (tt_dd_tickets_set.py wa):
`dash`  - DISCO DASH, the circuit: hero ticket + disco ball, the three rules as one slab, three pointer pills.
`combo` - WIN IT FREE OR BUY IT AT RS. 550: two cards (Disco Dash: first 5 finishers win free tickets / DD ticket stall: Rs. 550) under the disco ball.
Rules/facts only as the user gave them; no points target, no Disco Diwali date/venue (none supplied). Mini-Fete: 3rd + 4th Oct 2026, Turf XL, New Alipore.
Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_dd_whatsapp.py   ->  out/collaterals/disco_dash_whatsapp.png, out/collaterals/disco_diwali_win_or_buy_whatsapp.png
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
H, TOTAL = 1350, 1
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
    s.add(f'<img class="measure" data-tag="{tag}" src="{STK[slug]}" style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;transform:rotate({deg}deg);z-index:{z}">'); s.el(tag, x, y, size, size)


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
    out = []; BOT = H - 150; STAR_IGN = [("star_tl", "t1"), ("star_tr", "t1")]
    # ================= DISCO DASH =================
    s = Slide(1, 601); s.idx = 0
    ty = await s.title("DISCO DASH", "HYROX-STYLE CIRCUIT", big_w=730, sub_w=720, top=104)
    s.star("star_tl", 24, 70); s.star("star_tr", W - 24 - 104, 86)
    tk, tkh = ddm.ticket(560, "wt"); svg_sticker(s, "tkt", tk, 50, ty + 40, 560, tkh, -8, z=8)
    ball, bh = ddm.disco_ball(470, "wb"); svg_sticker(s, "ball", ball, W - 50 - 470, ty + 10, 470, bh, 6, z=6)
    sy = ty + 40 + max(tkh + 30, bh * .75) + 20; sh = 330
    slab(s, "slab", 84, sy, 912, sh)
    ign = rows_in(s, 84, sy, 912, sh, [("FINISH ALL 9 STATIONS", 50, INK), ("WITH MAXIMUM POINTS", 50, INK), ("FIRST 5 WIN FREE DISCO DIWALI TICKETS", 34, "#0E7C86")])
    py = sy + sh + 50
    for i, txt in enumerate(("9 STATIONS", "PLAY ANY GAME SOLO", "3 + 4 OCT, TURF XL")):
        w = (968 - 2 * 20) / 3; s.chip(f"p{i}", txt, 56 + i * (w + 20), py, w, deg=[-2, 1.5, -1.5][i], size=22)
    s.footer(cta="SEE YOU THERE"); out.append(("dash", s, ign + [("slab", "tkt"), ("slab", "ball"), ("tkt", "ball")] + STAR_IGN))
    # ================= WIN IT OR BUY IT =================
    s = Slide(1, 602); s.idx = 0
    ty = await s.title("DISCO DIWALI", "WIN YOUR TICKETS OR BUY THEM", big_w=700, sub_w=800, top=104)
    s.star("star_tl", 24, 70); s.star("star_tr", W - 24 - 104, 86)
    ball, bh = ddm.disco_ball(340, "cb"); svg_sticker(s, "ball", ball, (W - 340) / 2, ty + 6, 340, bh, 0, z=6)
    cy0 = ty + 6 + bh + 14; chh = min(580, BOT + 30 - cy0); cw_ = 470; ign = list(STAR_IGN)
    for i, (xx, chip, big, bpx, l1, l2, deg) in enumerate([(56, "WIN THEM FREE", "DISCO DASH", 40, "FINISH ALL 9 STATIONS WITH MAXIMUM POINTS", "FIRST 5 FINISHERS WIN", -1), (554, "OR BUY THEM", "RS. 550", 72, "AT THE DD TICKET STALL", "TURF XL, 3RD + 4TH OCT", 1)]):
        s.add(f'<div class="measure" data-tag="cd{i}" style="position:absolute;left:{xx}px;top:{cy0}px;width:{cw_}px;height:{chh}px;box-sizing:border-box;transform:rotate({deg}deg);border:6px solid {GREEN};border-radius:36px;background:#F3ECDE;z-index:6"></div>'); s.el(f"cd{i}", *rb(xx, cy0, cw_, chh, deg))
        s.add(f'<div class="measure" data-tag="ch{i}" style="position:absolute;left:{xx + 30}px;top:{cy0 + 34}px;background:{ORCHID};color:{INK};font-family:var(--d);font-weight:900;font-size:28px;line-height:1;padding:10px 20px 9px;border-radius:999px;white-space:nowrap;z-index:9">{chip}</div>'); s.el(f"ch{i}", xx + 30, cy0 + 34, 270, 50)
        s.add(f'<div class="measure" data-tag="bg{i}" style="position:absolute;left:{xx + 20}px;top:{cy0 + 112 + (84 - bpx) / 2}px;width:{cw_ - 40}px;text-align:center;color:{INK};font-family:StretchPro;-webkit-text-stroke:{tt.ST_STROKE * bpx}px {INK};letter-spacing:{tt.ST_LS}em;font-feature-settings:{tt.ST_FEAT};font-size:{bpx}px;line-height:1;white-space:nowrap;z-index:9">{big}</div>'); s.el(f"bg{i}", xx + 20, cy0 + 114 + (84 - bpx) / 2, cw_ - 40, bpx * .82)
        s.add(f'<div class="measure" data-tag="l{i}" style="position:absolute;left:{xx + 24}px;top:{cy0 + 218}px;width:{cw_ - 48}px;text-align:center;color:{INK};font-family:var(--d);font-weight:900;font-size:28px;line-height:1.1;z-index:9">{l1}</div>'); s.el(f"l{i}", xx + 24, cy0 + 218, cw_ - 48, 64)
        s.add(f'<div class="measure" data-tag="m{i}" style="position:absolute;left:{xx + 24}px;top:{cy0 + 304}px;width:{cw_ - 48}px;text-align:center;color:#0E7C86;font-family:var(--d);font-weight:900;font-size:28px;line-height:1.1;z-index:9">{l2}</div>'); s.el(f"m{i}", xx + 24, cy0 + 304, cw_ - 48, 34)
        ign += [(f"cd{i}", t) for t in (f"ch{i}", f"bg{i}", f"l{i}", f"m{i}")]
    for j, slug in enumerate(("darts", "headphones", "jenga")):
        sticker(s, f"gs{j}", slug, 56 + 24 + j * 138, cy0 + chh - 168, 140, [-5, 4, -4][j], z=9); ign.append(("cd0", f"gs{j}"))
    tk, tkh = ddm.ticket(360, "ct"); svg_sticker(s, "tkt", tk, 554 + 55, cy0 + chh - 200, 360, tkh, -7, z=9); ign.append(("cd1", "tkt"))
    ign += [("ball", "cd0"), ("ball", "cd1"), ("cd0", "cd1"), ("gs0", "gs1"), ("gs1", "gs2")]
    s.footer(cta="SEE YOU THERE"); out.append(("win_or_buy", s, ign))
    return out


async def main():
    res = await build(); os.makedirs("out/collaterals", exist_ok=True)
    text_pairs = [("head", WHITE, GROUND, 96, True), ("sub", ORCHID, GROUND, 50, True), ("chip", INK, CTA_FILL, 22, True), ("cta", INK, CTA_FILL, 30, True)]
    names = {"dash": "disco_dash_whatsapp.png", "win_or_buy": "disco_diwali_win_or_buy_whatsapp.png"}
    async with B.session():
        for name, s, ign in res:
            out = "out/collaterals/" + names[name]
            await B.render(s.html(), out, W, H, elements=s.els, text_pairs=text_pairs, containers=tuple(l for l, *_ in s.els if l.startswith("cd") or l == "slab"), page_bg=GROUND,
                           expect_hero=False, collision_ignore=set(map(tuple, ign)), margin=12)
            print("done", out)

asyncio.run(main())
