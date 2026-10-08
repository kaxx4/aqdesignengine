"""Disco Diwali stall call, IG story 1080x1920. Workflow C, bespoke.
Style: no drawn bank style fits (bank pick needed product photos, none are real AQ assets);
built from the sticker-card mechanism. Adaptation: dept colour events=sky is the hero hue,
Diwali warmth (lemon/tomato/pink) as supporting cards. Date/venue omitted: not supplied."""
import asyncio, os, sys, importlib.util
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine"); sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")
W, H = core.SIZES["story"]; M = 64
A = core.ACCENTS
SKY = core.accent_for("events")
els = []
def doodle(kind, x, y, size, fill, rot=0, z=7):
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;width:{size}px;height:{size}px;z-index:{z}">'
            f'{dd.stamp(kind, fill, rot=rot)}</div>')

parts = [f'<div style="position:absolute;inset:0;background:var(--bg)"></div>']
parts.append(B.logo(y=110)); els.append(("logo", M, 110, 160, 32))
parts.append(B.eyebrow("DISCO DIWALI · STALL CALL", core.on_cream(A[3], 18), 200)); els.append(("eyebrow", M, 200, 520, 24))

# headline
parts.append(f'<div style="position:absolute;top:290px;left:{M}px;font-family:var(--d);font-weight:900;font-size:210px;line-height:.9;color:var(--ink);text-transform:uppercase;z-index:6">WANT A</div>')
els.append(("h1", M, 300, 640, 190))
slab = (f'<div style="position:absolute;top:500px;left:{M}px;width:700px;height:330px;background:{SKY};border:5px solid var(--ink);'
        f'border-radius:32px;box-shadow:10px 10px 0 var(--ink);transform:rotate(-3deg);z-index:5"></div>')
parts.append(slab); els.append(("slab", M, 500, 700, 330))
parts.append(f'<div style="position:absolute;top:490px;left:{M+40}px;font-family:var(--s);font-style:italic;font-size:340px;line-height:1;color:var(--ink);transform:rotate(-3deg);z-index:6">stall</div>')
els.append(("stall", M+40, 520, 560, 290))
parts.append(f'<div style="position:absolute;top:870px;left:{M}px;font-family:var(--d);font-weight:900;font-size:96px;line-height:.95;color:var(--ink);text-transform:uppercase;z-index:6">AT OUR DIWALI?</div>')
els.append(("h3", M, 880, 800, 90))
parts.append(doodle("sparkle", 800, 330, 170, A[2], rot=12)); els.append(("spark", 800, 330, 170, 170))
parts.append(doodle("star", 790, 590, 120, A[0], rot=-10)); els.append(("star", 790, 590, 120, 120))

# cards
cards = [("FOOD & DRINKS", "snacks, sweets, sips", A[3], "leaf", M, 1030, -2),
         ("GAMES", "make people compete", A[5], "lightning", M+488, 1070, 2),
         ("MERCH & CRAFTS", "diyas, jewellery, thrift", A[2], "heart", M, 1330, 2),
         ("SOMETHING ELSE", "surprise us", A[0], "burst", M+488, 1370, -2)]
CW, CH = 464, 250
for lab, sub, col, d, x, y, rot in cards:
    fg = core.text_on(col)
    parts.append(f'<div style="position:absolute;top:{y}px;left:{x}px;width:{CW}px;height:{CH}px;background:{col};border:5px solid var(--ink);'
                 f'border-radius:32px;box-shadow:8px 8px 0 var(--ink);transform:rotate({rot}deg);z-index:6;overflow:hidden">'
                 f'<div style="position:absolute;right:14px;top:14px;width:110px;height:110px">{dd.stamp(d, "#FFFFFF" if False else core.INK)}</div>'
                 f'<div style="position:absolute;left:24px;bottom:56px;font-family:var(--d);font-weight:900;font-size:44px;line-height:1;color:{fg};text-transform:uppercase;white-space:nowrap">{lab}</div>'
                 f'<div style="position:absolute;left:24px;bottom:20px;font-family:var(--e);font-weight:600;font-size:24px;color:{fg};white-space:nowrap">{sub}</div></div>')
    els.append((f"card_{lab[:4]}", x, y, CW, CH))

# CTA
parts.append(f'<div style="position:absolute;top:1650px;left:{M}px;width:952px;height:96px;background:var(--ink);border-radius:999px;box-shadow:6px 6px 0 {SKY};'
             f'display:flex;align-items:center;justify-content:center;gap:16px;z-index:8">'
             f'<span style="font-family:var(--d);font-weight:900;font-size:40px;color:var(--bg);text-transform:uppercase;letter-spacing:.01em">DM US TO GET A SPOT</span>'
             f'<span style="font-family:var(--m);font-weight:700;font-size:22px;color:{core.on_dark(SKY,22)}">@ngo.aquaterra</span></div>')
els.append(("cta", M, 1650, 952, 96))

html = B.page(W, H, "var(--bg)", "".join(parts), grain=False)
text_pairs = [("h1", core.INK, "var(--bg)", 210, True), ("stall", core.INK, SKY, 340, False),
              ("h3", core.INK, "var(--bg)", 96, True),
              ("eyebrow", core.on_cream(A[3], 18), "var(--bg)", 18, True)]
async def main():
    await B.render(html, "out/versions/disco_stalls/v1.png", W, H, elements=els, text_pairs=text_pairs,
                   containers=("slab",), page_bg="var(--bg)", expect_hero=True)
asyncio.run(main())
