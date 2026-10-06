"""TerraThon DISCO DIWALI teaser, ONE feed poster (1080x1350) with all five of the user's photos, promoting @aquaterra.live (user, 2026-10-06).
Collage of five tilted orchid frames (two rows), disco ball sticker at the join, title SOMETHING SHINY / IS ON THE WAY, handle slab. No dates, venue or price (user ruling same day). Photos git-ignored (people).
Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_dd_follow_poster.py -> out/collaterals/dd_follow_poster.png
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
DDP = "engine/assets/terrathon/dd_photos"


def b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


FP = "engine/assets/terrathon/follow_photos"
PH = {n: b64(f"{FP}/{n}.jpg", "image/jpeg") for n in ("dance", "duo", "boxes", "night", "crew")}


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
        self.text("t1", "TERRATHON", (W - 700) / 2, top - 52, 700, 38, 400, CREAM_HALO)
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
DK = "#0A0A0A"


def svg_sticker(s, tag, svg, x, y, w, h, deg=0, z=7):
    s.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;transform:rotate({deg}deg);z-index:{z}">{svg}</div>'); s.el(tag, x, y, w, h)


def slab(s, tag, x, y, w, h, deg=-1.25):
    s.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;transform:rotate({deg}deg);background:{SLAB};border:20px solid {ORCHID};border-radius:52px;z-index:8"></div>'); s.el(tag, *rb(x, y, w, h, deg))


def rows_in(s, sx, sy, sw, sh, rows, tag="row"):
    tot = sum(z for _, z, _c in rows) + (len(rows) - 1) * 20; y = sy + (sh - tot) / 2 - 4
    for i, (txt, z, col) in enumerate(rows):
        s.add(f'<div class="measure" data-tag="{tag}{i}" style="position:absolute;left:{sx + 36}px;width:{sw - 72}px;top:{y}px;text-align:center;color:{col};font-family:var(--d);font-weight:900;font-size:{z}px;line-height:1;white-space:nowrap;z-index:9">{txt}</div>'); s.el(f"{tag}{i}", sx + 36, y, sw - 72, z * .85); y += z + 20
    return [("slab", f"{tag}{i}") for i in range(len(rows))]



HANDLE = "@AQUATERRA.LIVE"
async def main():
    s = Slide(1, 701)
    ty = await s.title("SOMETHING SHINY", "IS ON THE WAY", big_w=700, sub_w=640, top=96)
    s.star("star_tl", 24, 60); s.star("star_tr", W - 24 - 104, 76)
    y0 = ty + 10
    s.frame("f1", PH["dance"], 40, y0, 350, 430, -3, "50% 55%", z=4)
    s.frame("f2", PH["boxes"], 375, y0 - 6, 330, 440, 2, "50% 45%", z=5)
    s.frame("f3", PH["duo"], 700, y0 + 10, 340, 430, -2, "50% 30%", z=4)
    y1 = y0 + 410
    s.frame("f4", PH["crew"], 40, y1, 540, 360, 2.5, "35% 40%", z=6)
    s.frame("f5", PH["night"], 560, y1 + 10, 480, 360, -3, "50% 65%", z=5)
    bw = 230; ball, bh = ddm.disco_ball(bw, "bp"); svg_sticker(s, "ball", ball, 425, y1 - 120, bw, bh, 8, z=10)
    sy = y1 + 395; slab(s, "slab", 110, sy, 860, 120)
    ign = rows_in(s, 110, sy, 860, 120, [("FOLLOW " + HANDLE, 46, INK)])
    s.footer(cta="FOLLOW ALONG")
    ig = ign + [(a, b) for a in ("f1", "f2", "f3", "f4", "f5", "ball") for b in ("f1", "f2", "f3", "f4", "f5", "ball") if a < b] + [("f2", "star_tr"), ("f3", "star_tr"), ("f1", "star_tl"), ("slab", "f4"), ("slab", "f5")]
    text_pairs = [("head", WHITE, GROUND, 96, True), ("sub", ORCHID, GROUND, 50, True), ("cta", INK, CTA_FILL, 30, True)]
    os.makedirs("out/collaterals", exist_ok=True)
    async with B.session():
        await B.render(s.html(), "out/collaterals/dd_follow_poster.png", W, H, elements=s.els, text_pairs=text_pairs, containers=("slab",), page_bg=GROUND, expect_hero=False,
                       collision_ignore=set(map(tuple, ig)), margin=12, crop_tags=("frame", "f1", "f2", "f3", "f4", "f5"))
asyncio.run(main())
