"""TerraThon MINI-FETE MINI GAMES carousel (11 slides, feed 1080x1350), built from STICKERS because there are no photos (user, 2026-10-01). Nine hand-drawn flat stickers
(scratchpad/tt_minigame_stickers.py -> engine/assets/terrathon/minigames/*.svg, original artwork in the kit's die-cut style). v2 (user: "a separate slide for all the games and the first slide
may not include all the stickers"): cover with FOUR of the nine + "swipe to see all 9", then ONE SLIDE PER GAME (big sticker on a cream plate, numbered badge, game name), then the closer.
The nine games are exactly the user's list: guess the sentence with headphones, flip the cup, Jenga with dares, darts, tongue twisters, push up challenge, plank challenge, aim the cup, coin drop.
NO rules, prizes, scoring, entry fees or timings are printed (none were supplied); the only extra words restate the game's own name ("with headphones", "with dares").
Event facts (copy pack): Mini-Fete 3rd and 4th Oct 2026, Turf XL, New Alipore, open to all.
Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_minigames_carousel.py   ->  out/collaterals/minigames/slide_NN.png
"""
import asyncio, base64, importlib.util, os, random, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B, W = tt.core, tt.B, tt.W
lay = tt.load("layout")
GROUND, ORCHID, CREAM_HALO, INK, WHITE, CTA_FILL, SLAB = tt.GROUND, tt.ORCHID, tt.CREAM_HALO, tt.INK, tt.WHITE, tt.CTA_FILL, tt.SLAB
GREEN = "#2FD284"
import sys
STORY = "story" in sys.argv[1:]     # 1080x1920 with Instagram UI zones clear (top ~250, bottom ~270)
H, TOTAL = (1920 if STORY else 1350), 11
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


GAMES = [("headphones", "GUESS THE SENTENCE", "WITH HEADPHONES"), ("cup_flip", "FLIP THE CUP", None), ("jenga", "JENGA", "WITH DARES"),
         ("darts", "DARTS", None), ("tongue", "TONGUE TWISTERS", None), ("pushup", "PUSH UP CHALLENGE", None),
         ("plank", "PLANK CHALLENGE", None), ("aim_cup", "AIM THE CUP", None), ("coin_drop", "COIN DROP", None)]


def sticker(s, tag, slug, x, y, size, deg=0, z=7):
    s.add(f'<img class="measure" data-tag="{tag}" src="{STK[slug]}" style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;transform:rotate({deg}deg);z-index:{z}">')
    s.el(tag, x, y, size, size)


async def build():
    slides = []
    BOT = H - FOOT - 150
    # ---- 1 COVER: four of the nine, a swipe cue ----
    s = Slide(1, 81)
    ty = await s.title("MINI GAMES", "9 OF THEM, 2 DAYS", big_w=730, sub_w=700, top=104)
    s.star("star_tl", 24, 70 + OY); s.star("star_tr", W - 24 - 104, 86 + OY)
    area = BOT - ty - 110; size = min(420, area / 2 + 30)
    pos = [("darts", 70, ty + 20, -5), ("headphones", W - 70 - size, ty + 50, 5), ("jenga", 90, ty + 40 + size * 0.85, 4), ("cup_flip", W - 90 - size, ty + 20 + size * 0.95, -4)]
    for i, (slug, x, y, d) in enumerate(pos): sticker(s, f"stk{i}", slug, x, y, size, d)
    cw = 640; cy = BOT - 20
    s.chip("swipe", "SWIPE TO SEE ALL 9", (W - cw) / 2, cy - 30, cw, deg=-2, size=40)
    s.footer(); slides.append((s,) + tuple((f"stk{i}", f"stk{j}") for i in range(4) for j in range(i + 1, 4)) + (("swipe", "stk2"), ("swipe", "stk3")))
    # ---- 2-10 ONE SLIDE PER GAME ----
    for n, (slug, name, sub) in enumerate(GAMES):
        s = Slide(n + 2, 90 + n)
        ty = await s.title(name, f"GAME 0{n + 1} OF 09", big_w=min(760, 130 * len(name)), sub_w=520, top=96)
        s.star("star_tl", 24, 60 + OY); s.star("star_tr", W - 24 - 104, 74 + OY)
        px, pw = 110, 860; py = 350; ph = BOT - py - 20      # fixed plate on every game slide so the deck stays steady
        s.add(f'<div class="measure" data-tag="slab" style="position:absolute;left:{px}px;top:{py}px;width:{pw}px;height:{ph}px;box-sizing:border-box;transform:rotate(1deg);background:#F3ECDE;border:18px solid {ORCHID};border-radius:60px;z-index:5"></div>')
        s.el("slab", *rb(px, py, pw, ph, 1))
        ss = min(ph - 40, 780); sticker(s, "stk", slug, px + (pw - ss) / 2, py + (ph - ss) / 2 - (24 if sub else 0), ss, [-4, 3, -3, 4, -4, 3, -3, 4, -3][n], z=8)
        bd = 150; bx, by = px - 46, py - 38
        s.add(f'<div class="measure" data-tag="badge" style="position:absolute;left:{bx}px;top:{by}px;width:{bd}px;height:{bd}px;box-sizing:border-box;border-radius:50%;background:{GREEN};border:8px solid {INK};display:flex;align-items:center;justify-content:center;color:{INK};font-family:var(--d);font-weight:900;font-size:72px;line-height:1;z-index:10">0{n + 1}</div>'); s.el("badge", bx, by, bd, bd)
        ign = [("slab", "stk"), ("slab", "badge"), ("badge", "stk"), ("star_tl", "badge"), ("star_tl", "t1")]
        if sub:
            s.chip("chip", sub, (W - 640) / 2, py + ph - 52, 640, deg=-2, size=40); ign += [("slab", "chip"), ("chip", "stk")]
        s.footer(); slides.append((s,) + tuple(ign))
    # ---- 11 CLOSER ----
    s = Slide(11, 86)
    ty = await s.title("SEE YOU THERE", "AT THE MINI-FETE", big_w=730, sub_w=640, top=96)
    s.star("star_tl", 24, 60 + OY); s.star("star_tr", W - 24 - 104, 74 + OY)
    row1 = ["headphones", "darts", "aim_cup"]; row2 = ["jenga", "pushup", "coin_drop"]
    sz = 250; y1 = ty + 6
    for i, slug in enumerate(row1): sticker(s, f"a{i}", slug, 70 + i * 300, y1, sz, [-5, 4, -4][i])
    sx, sy, sw, sh = 84, y1 + sz + 24, 912, 290
    s.add(f'<div class="measure" data-tag="slab" style="position:absolute;left:{sx}px;top:{sy}px;width:{sw}px;height:{sh}px;box-sizing:border-box;transform:rotate(-1.25deg);background:{SLAB};border:20px solid {ORCHID};border-radius:52px;z-index:8"></div>')
    s.el("slab", *rb(sx, sy, sw, sh, -1.25))
    rows = [("SAT 3 + SUN 4 OCT, 2026", 52), ("TURF XL, NEW ALIPORE", 52), ("OPEN TO ALL", 44)]
    tot = sum(z for _, z in rows) + 2 * 20; ty2 = sy + (sh - tot) / 2 - 4
    for i, (txt, z) in enumerate(rows):
        s.add(f'<div class="measure" data-tag="row{i}" style="position:absolute;left:{sx + 40}px;width:{sw - 80}px;top:{ty2}px;text-align:center;color:{INK};font-family:var(--d);font-weight:900;font-size:{z}px;line-height:1;white-space:nowrap;z-index:9">{txt}</div>')
        s.el(f"row{i}", sx + 40, ty2, sw - 80, z * .85); ty2 += z + 20
    y2 = sy + sh + 24
    for i, slug in enumerate(row2): sticker(s, f"b{i}", slug, 70 + i * 300, y2, sz, [4, -5, 5][i])
    s.footer(cta="SEE YOU 3 + 4 OCT")
    slides.append((s,) + tuple(("slab", f"row{i}") for i in range(3)) + (("slab", "a0"), ("slab", "a1"), ("slab", "a2"), ("slab", "b0"), ("slab", "b1"), ("slab", "b2")))
    return slides


async def main():
    slides = await build()
    outdir = "out/collaterals/minigames"; os.makedirs(outdir, exist_ok=True)
    text_pairs = [("head", WHITE, GROUND, 96, True), ("sub", ORCHID, GROUND, 50, True), ("chip", INK, CTA_FILL, 40, True), ("badge", INK, GREEN, 72, True), ("idx", INK, CTA_FILL, 26, True), ("cta", INK, CTA_FILL, 30, True)]
    async with B.session():
        for s, *ign in slides:
            out = f"{outdir}/slide_{s.idx:02d}.png"
            await B.render(s.html(), out, W, H, elements=s.els, text_pairs=text_pairs, containers=("slab",), page_bg=GROUND,
                           expect_hero=False, collision_ignore=set(map(tuple, ign)), margin=12)
            print("done", out)

asyncio.run(main())
