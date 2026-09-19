"""23bb507f6ec978 v3 — full rebuild (v1-2 script lost).
Reference: a dense NYC-signpost sticker illustration — 2 angled black "ONE WAY" arrow signs up
top, 2 street-name signs (green/blue) below them, a big 3-lamp traffic light mid-pole, a walk-signal
box and a red no-standing box at the bottom, all tightly overlapping one central grey pole, filling
~85% of the frame with almost no cream margin.

v2 critique (compare.py): area 0.756x (under-filled, not yet blocking), bbox IoU only 0.511 (the
signs are spread thin down a tall pole instead of clustered tight like the reference), region
under-filled at the center column (rows 3/6/7 of 11), missing red/pink + teal + muted blue-purple
accents. Score 0.324, no blocking critique fired but IoU/region gaps are real.
Fixes here: same sign set but pulled into a tight overlapping cluster (arms cross the pole, ends
overlap each other's corners like a real signpost), pole shortened, traffic light enlarged with a
visible red accent, an explicit teal sign added, margins tightened.
"""
import asyncio, os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\Code\AquaTerra\AQ_CODEBASE")
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join("engine", n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); S = load("shapes"); dd = load("doodles"); lay = load("layout")

W, H = core.SIZES["feed"]; M = 64
A = core.ACCENTS
CREAM = "var(--bg)"
elements = []

def at(x, y, w, h, inner, z=6, rot=0):
    elements.append((x, y, w, h))
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'z-index:{z};transform:rotate({rot}deg);transform-origin:0 50%">{inner}</div>')

logo = f'<img src="{core.LOGO}" style="position:absolute;top:52px;left:{M}px;height:38px;z-index:80">'
title = (f'<div style="position:absolute;top:150px;left:0;right:0;text-align:center;z-index:70;'
         f'font-family:var(--d);font-weight:900;font-size:76px;text-transform:uppercase;'
         f'color:var(--ink)">PICK A LANE.</div>')
elements.append((M, 52, 140, 40)); elements.append((240, 150, 600, 100))

POLE_X = 540
pole = at(POLE_X - 11, 380, 22, 900,
          f'<div style="width:100%;height:100%;background:repeating-linear-gradient(to bottom,'
          f'#8A8F95 0 8px,#6E7378 8px 16px);border:3px solid #0A0A0A;border-radius:4px"></div>', z=1)

def sign(text, fill, w, h, fs=30):
    return (f'<div style="width:100%;height:100%;background:{fill};border:5px solid #0A0A0A;'
            f'border-radius:6px;box-shadow:7px 7px 0 rgba(0,0,0,.4);display:flex;align-items:center;'
            f'justify-content:center;font-family:var(--m);font-weight:800;font-size:{fs}px;'
            f'letter-spacing:.03em;color:{core.text_on(fill)};text-align:center;padding:0 10px;'
            f'box-sizing:border-box;text-transform:uppercase">{text}</div>')

def arrow_sign(text, w, h, point="right"):
    tri = "0 0,100% 50%,0 100%" if point == "right" else "100% 0,0 50%,100% 100%"
    pad_l = "0 34px 0 14px" if point == "right" else "0 14px 0 34px"
    arrow_div = (f'<div style="position:absolute;{"right" if point=="right" else "left"}:0;top:0;'
                 f'width:26px;height:100%;background:#F4EFE0;clip-path:polygon({tri})"></div>')
    return (f'<div style="width:100%;height:100%;background:#0A0A0A;border:5px solid #0A0A0A;'
            f'border-radius:4px;box-shadow:7px 7px 0 rgba(0,0,0,.4);position:relative;'
            f'display:flex;align-items:center;justify-content:center;font-family:var(--m);'
            f'font-weight:800;font-size:20px;letter-spacing:.05em;color:#F4EFE0;text-transform:'
            f'uppercase;padding:{pad_l};box-sizing:border-box;white-space:nowrap">{text}{arrow_div}</div>')

signs = []
# two angled "ONE WAY"-style arrow signs, top, overlapping the pole and each other
signs.append(at(POLE_X - 34, 400, 300, 68, arrow_sign("GIVE BACK", 300, 68, "right"), z=20, rot=-9))
signs.append(at(POLE_X - 300, 452, 300, 68, arrow_sign("SHOW UP", 300, 68, "left"), z=19, rot=6))
# street-name signs, tightly stacked, overlapping the arrows and each other
signs.append(at(POLE_X - 40, 520, 360, 78, sign("WELFARE", A[4], 360, 78), z=18, rot=-4))
signs.append(at(POLE_X - 330, 566, 340, 78, sign("CLIMATE", "#0E7C86", 340, 78), z=17, rot=5))
signs.append(at(POLE_X - 20, 630, 380, 78, sign("EDUCATION", A[5], 380, 78), z=16, rot=-6))
signs.append(at(POLE_X - 350, 676, 320, 78, sign("RECRUIT", A[2], 320, 78), z=15, rot=4))

# traffic light — big, 3 lamps, red one clearly lit (adds the missing red/pink accent + detail)
tl_w, tl_h = 190, 300
tl = at(POLE_X - tl_w // 2, 760, tl_w, tl_h,
        f'<div style="width:100%;height:100%;background:#0A0A0A;border:5px solid #0A0A0A;'
        f'border-radius:20px;box-shadow:8px 8px 0 rgba(0,0,0,.4);position:relative">'
        + "".join(
            f'<div style="position:absolute;left:50%;top:{18+i*94}px;width:120px;height:120px;'
            f'transform:translateX(-50%);border-radius:50%;background:{c};'
            f'box-shadow:0 0 26px {glow}"></div>'
            for i, (c, glow) in enumerate([("#3A2A00", "transparent"), ("#3A2A00", "transparent"),
                                            (A[3], "rgba(255,77,46,.85)")])
        ) + '</div>', z=25)

walk = at(POLE_X - 220, 1080, 170, 170,
          f'<div style="width:100%;height:100%;background:#0A0A0A;border:5px solid #0A0A0A;'
          f'border-radius:14px;box-shadow:7px 7px 0 rgba(0,0,0,.4);display:flex;align-items:center;'
          f'justify-content:center">'
          f'<svg width="90" height="90" viewBox="0 0 100 100"><g fill="{A[3]}">'
          f'<circle cx="50" cy="18" r="12"/><path d="M50 32 L30 46 L38 52 L46 44 L46 60 L30 88 '
          f'L40 94 L54 68 L60 94 L70 88 L60 55 L70 60 L78 50 L62 40 L54 32 Z"/></g></svg></div>', z=24, rot=3)

nostand = at(POLE_X + 60, 1100, 170, 170,
             f'<div style="width:100%;height:100%;background:{A[2]};border:5px solid #0A0A0A;'
             f'border-radius:14px;box-shadow:7px 7px 0 rgba(0,0,0,.4);display:flex;flex-direction:'
             f'column;align-items:center;justify-content:center;gap:6px">'
             f'<svg width="80" height="46" viewBox="0 0 100 60"><line x1="10" y1="30" x2="90" y2="30" '
             f'stroke="#0A0A0A" stroke-width="7"/><path d="M10 30 L26 20 M10 30 L26 40" fill="none" '
             f'stroke="#0A0A0A" stroke-width="7" stroke-linecap="round"/>'
             f'<path d="M90 30 L74 20 M90 30 L74 40" fill="none" stroke="#0A0A0A" stroke-width="7" '
             f'stroke-linecap="round"/><line x1="6" y1="6" x2="94" y2="54" stroke="{A[3]}" '
             f'stroke-width="8"/></svg>'
             f'<div style="font-family:var(--m);font-weight:800;font-size:12px;color:#0A0A0A;'
             f'text-align:center;line-height:1.1">NO STANDING<br>ANY TIME</div></div>', z=24, rot=-3)

base = at(POLE_X - 30, 1240, 60, 60,
          f'<div style="width:100%;height:100%;background:#6E7378;border:5px solid #0A0A0A;'
          f'border-radius:8px"></div>', z=2)

footer = (f'<span style="position:absolute;bottom:70px;left:{M}px;font-family:var(--m);font-weight:700;'
          f'font-size:14px;letter-spacing:.06em;color:var(--ink);z-index:60">@ngo.aquaterra</span>')
caption = (f'<div style="position:absolute;top:290px;left:0;right:0;text-align:center;'
           f'font-family:var(--s);font-style:italic;font-size:28px;color:var(--ink);opacity:.75;'
           f'z-index:60">every sign leads back to the same drive.</div>')
elements.append((M, 1280, 260, 20)); elements.append((360, 290, 360, 40))

inner = (f'<div style="position:absolute;inset:0;background:{CREAM}"></div>'
         + pole + base + "".join(signs) + tl + walk + nostand
         + title + logo + footer + caption)
html = B.page(W, H, CREAM, inner, grain=True)

color_pairs = [("field", CREAM, CREAM)]
pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs, page_bg=CREAM, core=core,
                   expect_hero=False, auto_nudge=False)

async def main():
    slug = "23bb507f6ec978"
    os.makedirs(f"out/versions/{slug}", exist_ok=True)
    await B.render(html, f"out/versions/{slug}/v3.png", W, H)
    print("done")
asyncio.run(main())
