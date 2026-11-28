"""TerraNotes v3 (bespoke). Mechanism taken from the two nostalgia references: a serif lowercase
wordmark STRADDLING the edge between a textured paper field and a dark block, so the same word
is ink on the paper half and cream on the dark half. Edge colour strips (ref 2) use AQ accents.
Adaptations: no stock/child photo (real-assets rule + logo should not depend on a portrait): the
dark block is ink with grain and a warm glow; Instrument Serif regular (not italic) carries the
ONE serif word; paper texture = tex.paper_fibre + tex.grain on cream, not white."""
import asyncio, os, sys, importlib.util
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ED = os.path.join(os.getcwd(), "engine"); sys.path.insert(0, ED)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ED, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); tex = load("tex")
A = core.ACCENTS; SKY, MINT, LEMON, TOMATO, GRAPE, INK, CREAM = A[4], A[1], A[2], A[3], A[5], core.INK, core.CREAM
W, H = 1500, 1040; LINE = 640; BL = 800; FS = 640; X = 60

def word(color, top_off):
    return (f'<div style="position:absolute;left:{X}px;top:{BL-FS*0.82+top_off}px;font-family:var(--s);font-size:{FS}px;'
            f'line-height:1;letter-spacing:-14px;color:{color};white-space:nowrap">notes</div>')

def build():
    paper = (f'<div style="position:absolute;inset:0;background:{CREAM}"></div>'
             f'<div style="position:absolute;inset:0;{tex.paper_fibre(0.03)}"></div>'
             f'<div style="position:absolute;inset:0;{tex.grain(0.22,0.7,3,300)};mix-blend-mode:multiply"></div>'
             f'<div style="position:absolute;left:0;top:0;width:{W}px;height:{LINE}px;'
             f'background:radial-gradient(ellipse 60% 70% at 80% 10%,{LEMON}33,transparent 70%)"></div>')
    dark = (f'<div style="position:absolute;left:40px;top:{LINE}px;width:{W-80}px;height:{H-LINE}px;background:{INK};overflow:hidden">'
            f'<div style="position:absolute;inset:0;background:radial-gradient(ellipse 45% 55% at 78% 100%,{TOMATO}88,{LEMON}33 45%,transparent 75%)"></div>'
            f'<div style="position:absolute;inset:0;background:radial-gradient(ellipse 30% 40% at 12% 30%,{MINT}33,transparent 70%)"></div>'
            + "".join(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;border-radius:50%;'
                      f'background:{c};filter:blur({s*0.28}px);opacity:{o}"></div>'
                      for x,y,s,c,o in [(1010,170,46,LEMON,.95),(830,255,30,LEMON,.8),(1180,290,22,TOMATO,.9),(520,150,26,LEMON,.7)]) +
            f'<div style="position:absolute;inset:0;{tex.grain(0.35,0.8,2,240)};mix-blend-mode:screen;opacity:.5"></div></div>')
    strips = "".join(f'<div style="position:absolute;left:0;top:{y}px;width:14px;height:{h}px;background:{c}"></div>'
                     for y,h,c in [(0,210,GRAPE),(210,210,LEMON),(420,220,SKY),(LINE,300,MINT),(LINE+300,H-LINE-300,TOMATO)])
    top_half = (f'<div style="position:absolute;left:0;top:0;width:{W}px;height:{LINE}px;overflow:hidden;z-index:5">{word(INK,0)}</div>')
    bot_half = (f'<div style="position:absolute;left:0;top:{LINE}px;width:{W}px;height:{H-LINE}px;overflow:hidden;z-index:5">'
                f'<div style="position:absolute;left:0;top:{-LINE}px;width:{W}px;height:{H}px">{word(CREAM,0)}</div></div>')
    terra = (f'<div id="terra" style="position:absolute;left:{X+8}px;top:150px;z-index:6;font-family:var(--e);font-weight:600;'
             f'font-size:170px;line-height:1;letter-spacing:-6px;color:{INK}">terra</div>')
    leaf = (f'<svg width="120" height="120" viewBox="0 0 120 120" style="position:absolute;left:{X+8+322}px;top:150px;z-index:6;overflow:visible">'
            f'<path d="M58 112 C58 84 60 62 66 40" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>'
            f'<path d="M62 70 C36 70 18 52 16 28 C42 28 60 44 62 70 Z" fill="{MINT}" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/>'
            f'<path d="M64 52 C70 26 90 10 112 10 C112 36 94 54 64 52 Z" fill="{MINT}" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/></svg>')
    credit = (f'<div style="position:absolute;right:{W-1452}px;top:60px;z-index:6;writing-mode:vertical-rl;font-family:var(--m);'
              f'font-weight:700;font-size:20px;letter-spacing:7px;color:{core.on_cream(MINT,20)}">a magazine by aquaterra</div>')
    return paper + dark + strips + top_half + bot_half + terra + leaf + credit

async def main():
    async with B.session():
        await B.render(B.page(W, H, CREAM, build(), grain=False), "out/terranotes/terranotes_v3_editorial.png", W, H, page_bg=CREAM)
asyncio.run(main()); print("done")
