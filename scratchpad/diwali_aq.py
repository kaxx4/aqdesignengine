"""AQ Diwali wish (feed 1080x1350). Workflow C bespoke build, no reference.
Mechanism: one hero (a flat ink-outlined diya, flame as the only lemon), a two-line
display headline, ONE serif accent word ("light"). Adaptation recorded: the engine has no
diya doodle, so it is drawn as flat SVG with the house craft layer (ink outline + hard shadow).
Department hue: content/brand piece, so tomato (the diya) carries the piece, lemon only the flame.
"""
import asyncio, os, sys, importlib.util
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine"); sys.path.insert(0, ENGINE_DIR)
def load(n, d=None):
    s = importlib.util.spec_from_file_location(n, os.path.join(d or ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); ds = load("diya_scene", os.path.join(os.getcwd(),"scratchpad")); B = load("build"); dd = load("doodles")
W, H = core.SIZES["feed"]; M = 64; A = core.ACCENTS
INK = core.INK; TOMATO = A[3]; LEMON = A[2]; SKY = A[4]; PINK = A[0]; MINT = A[1]; GRAPE = A[5]
elements = []

def doodle(kind, x, y, size, fill, rot=0, z=7):
    elements.append((f"dd_{kind}_{x}", x, y, size, size))
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;width:{size}px;height:{size}px;z-index:{z}">'
            f'{dd.stamp(kind, fill, rot=rot, style="clean")}</div>')

BG = "#0A0A0A"; CRM = "#F4EFE0"; MB = "#00E5A0"; TEALL = "#2FB5C0"
# Dark-ground adaptation (recorded; precedent: Disco Diwali). Brief: black ground, more blue + green.
# Outlines are cream (an ink outline on an ink field vanishes: CLAUDE.md sec 10 craft-layer row);
# hard shadow is teal. Deep teal-navy night keeps the bowl readable against black.
PAL = dict(ink=CRM, sw=7, hard=True, shadow="#0E7C86", night="#0B2C40", star=CRM, f1=SKY, f2=MB, f3=CRM,
  sand="#CFEFE3", sand2="#A9D9C8", hill="#14587A", bulb=LEMON, candle1=SKY, candle2=MB, skin="#B9744A",
  cloth1=SKY, cloth2=CRM, lantern_up=MB, tile="#BFE6F7", bal=TEALL, wall="#0E7C86", wall2="#0A6872",
  flower=CRM, lan1=MB, lan2=SKY, rim=A[6], rim_bead=CRM, ground_shadow="#10202A")
SC = 940/1040; SX, SY = 70, 96
art = f'<div style="position:absolute;left:{SX}px;top:{SY}px;width:940px;z-index:6">{ds.scene(PAL,"aq")}</div>'
elements += [("flame", SX+(380+20)*SC, SY+10*SC, 260*SC, 340*SC), ("bowl", SX+20*SC, SY+370*SC, 1000*SC, 450*SC)]
head = f'''
<div style="position:absolute;left:0;right:0;top:950px;text-align:center;font-family:var(--d);font-weight:900;font-size:122px;line-height:1;letter-spacing:.015em;color:#F4EFE0;text-transform:uppercase;z-index:8;white-space:nowrap">HAPPY DIWALI</div>
<div style="position:absolute;left:0;right:0;top:1100px;text-align:center;font-family:var(--e);font-size:42px;line-height:1.2;color:#F4EFE0;z-index:8;white-space:nowrap">may your home glow with <span style="font-family:var(--s);font-style:italic;font-size:58px;color:{MB}">light</span></div>
<div style="position:absolute;left:0;right:0;top:{H-86}px;text-align:center;font-family:var(--m);font-weight:700;font-size:20px;letter-spacing:.04em;color:#F4EFE0;z-index:20">FROM ALL OF US AT AQUATERRA &nbsp;·&nbsp; @NGO.AQUATERRA</div>
'''
elements += [("headline", 120, 950, 840, 122), ("sub", 240, 1100, 600, 70), ("footer", 160, H-86, 760, 26)]
dood = (doodle("sparkle", 130, 190, 110, SKY, 8) + doodle("star", 860, 170, 86, MB, -12) +
        doodle("burst", 100, 300, 96, A[6], 0) + doodle("plus", 930, 330, 60, SKY, 0) +
        doodle("sparkle", 800, 290, 56, TEALL, 10))
inner = f'<div style="position:absolute;inset:0;background:{BG}"></div><div style="position:absolute;left:{M}px;top:48px;background:{CRM};border-radius:999px;padding:8px 18px;z-index:20;height:48px;display:flex;align-items:center"><img src="{core.LOGO}" style="height:30px"></div>{art}{head}{dood}'
html = B.page(W, H, BG, inner, grain=False)
tp = [("headline", CRM, BG, 122, True), ("sub", CRM, BG, 42, False),
      ("accent", MB, BG, 58, False)]
async def main():
    await B.render(html, "out/diwali/aq_diwali_v7.png", W, H, elements=elements, text_pairs=tp,
                   page_bg=BG, expect_hero=True)
asyncio.run(main())
