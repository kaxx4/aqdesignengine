"""Four-company Diwali poster as a BENTO: full black grain-textured ground, rounded tiles with hairline edges:
title tile, the recreated sparkler illustration in a tall art tile, four company tiles (logo + 'Visit us at' + link,
each with an accent taken from the illustration), a wish tile and a 'from' tile. Tokens: radius 32, 16px gaps, 40px margin."""
import asyncio, os, sys, base64, importlib.util, random, math
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, f"{ROOT}/engine")
import core
sp = importlib.util.spec_from_file_location("sr", f"{ROOT}/scratchpad/sparkler_recreate.py"); sr = importlib.util.module_from_spec(sp); sp.loader.exec_module(sr)
b64 = lambda p: base64.b64encode(open(p, "rb").read()).decode()
W, H, M, G, R = 1080, 1350, 40, 16, 32
CO = f"{ROOT}/scratchpad/co"
ARCH = b64(f"{ROOT}/addons/shikshaq/assets/fonts/archivo-latin.woff2"); GRAIN = b64(f"{ROOT}/engine/assets/disco_diwali/grain.png")
YEL, CREAM, INK, TILE, EDGE, MUTED = "#FBBE0E", "#F4EFE0", "#0a0a0c", "#131316", "rgba(244,239,224,.14)", "#a39e8c"
AQC, SHC, MKC, EKC = sr.DG, sr.LAV, sr.RED, sr.BLUE
# geometry
CW = W - 2 * M                                  # 1000
T_H, ART_H, R3_H = 190, 880, 168
ART_W = 640; COL_W = CW - ART_W - G             # 344
y_art = M + T_H + G; y_r3 = y_art + ART_H + G
CO_H = (ART_H - 3 * G) / 4
# dust texture across the ground
rnd = random.Random(3); dust = "".join(f'<circle cx="{rnd.uniform(0,W):.1f}" cy="{rnd.uniform(0,H):.1f}" r="{rnd.choice([.6,.8,1,1.3,1.7])}" fill="#d8d4c4" opacity="{rnd.uniform(.12,.45):.2f}"/>' for _ in range(700))
art_svg = sr.svg.replace('width="736" height="736"', 'width="880" height="880"', 1)
sh_logo = f'<span style="background:{CREAM};border-radius:999px;padding:4px 18px;display:inline-flex"><img src="data:image/svg+xml;base64,{b64(ROOT+"/addons/shikshaq/assets/shikshaq-logo.svg")}" style="height:46px"></span>'
aq_logo = f'<span style="background:{CREAM};border-radius:999px;padding:8px 20px;display:inline-flex"><img src="{core.LOGO}" style="height:34px"></span>'
mk_logo = f'<img src="data:image/png;base64,{b64(CO+"/mk_logo_crop.png")}" style="height:62px">'
ek_logo = (f'<span style="display:inline-flex;align-items:center;gap:12px"><img src="data:image/svg+xml;base64,{b64(CO+"/ek_icon.svg")}" style="height:54px">'
           f'<span style="font-weight:800;font-size:24px;letter-spacing:.12em">EKAVYA VYAPAAR</span></span>')
def company(i, logo, site, color):
    y = y_art + i * (CO_H + G)
    return (f'<div class="tile" style="left:{M+ART_W+G}px;top:{y:.0f}px;width:{COL_W}px;height:{CO_H:.0f}px;padding:22px 26px;display:flex;flex-direction:column;justify-content:space-between">'
            f'<div style="display:flex;align-items:center;justify-content:space-between"><div class=logo style="min-height:64px;display:flex;align-items:center">{logo}</div><span style="width:16px;height:16px;border-radius:50%;background:{color};flex:none"></span></div>'
            f'<div><div style="font-family:var(--m);font-weight:700;font-size:14px;letter-spacing:.14em;color:{MUTED}">VISIT US AT</div>'
            f'<div class=chk data-n="{site}" style="margin-top:5px;font-size:23px;font-weight:700;color:{CREAM};white-space:nowrap">{site}</div></div></div>')
html = f'''<!doctype html><meta charset=utf-8><style>{core.FONTS}{core.ROOT}
@font-face{{font-family:AR;src:url(data:font/woff2;base64,{ARCH});font-weight:100 900}}
*{{margin:0;box-sizing:border-box}}
.p{{width:{W}px;height:{H}px;background:{INK};position:relative;overflow:hidden;font-family:AR;color:{CREAM}}}
.tile{{position:absolute;background:{TILE};border:1px solid {EDGE};border-radius:{R}px;overflow:hidden;z-index:5}}
.gr{{position:absolute;inset:0;background:url(data:image/png;base64,{GRAIN}) center/cover;mix-blend-mode:screen;opacity:.6;z-index:30;pointer-events:none}}
</style><div class=p>
<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0;z-index:1">{dust}</svg>
<div class="tile" style="left:{M}px;top:{M}px;width:{CW}px;height:{T_H}px;padding:0 36px;display:flex;align-items:center;justify-content:space-between">
  <div><div style="font-family:var(--m);font-weight:700;font-size:15px;letter-spacing:.2em;color:{MUTED};margin-bottom:6px">DIWALI GREETINGS</div>
  <div class=chk data-n=title style="font-weight:800;font-size:112px;line-height:1;letter-spacing:-.03em;color:{YEL};white-space:nowrap">HAPPY DIWALI</div></div>
  <svg width="86" height="86" viewBox="-50 -50 100 100">{"".join(f'<line x1="{14*math.cos(math.radians(i*15)):.1f}" y1="{14*math.sin(math.radians(i*15)):.1f}" x2="{(46 if i%2==0 else 36)*math.cos(math.radians(i*15)):.1f}" y2="{(46 if i%2==0 else 36)*math.sin(math.radians(i*15)):.1f}" stroke="{CREAM}" stroke-width="3" stroke-linecap="round"/>' for i in range(24))}</svg>
</div>
<div class="tile" style="left:{M}px;top:{y_art}px;width:{ART_W}px;height:{ART_H}px"><div style="position:absolute;left:-120px;top:0;width:880px;height:880px">{art_svg}</div></div>
{company(0, aq_logo, "www.ngoaquaterra.com", AQC)}{company(1, sh_logo, "www.shikshaq.in", SHC)}{company(2, mk_logo, "mkcycles.in", MKC)}{company(3, ek_logo, "ekavyavyapaar.vercel.app", EKC)}
<div class="tile" style="left:{M}px;top:{y_r3}px;width:{ART_W}px;height:{R3_H}px;padding:0 34px;display:flex;align-items:center">
  <div class=chk data-n=wish style="font-size:38px;font-weight:700;line-height:1.18;letter-spacing:-.01em;color:{CREAM}">Wishing you light, love<br>and a bright year ahead</div></div>
<div class="tile" style="left:{M+ART_W+G}px;top:{y_r3}px;width:{COL_W}px;height:{R3_H}px;padding:20px 26px;display:flex;flex-direction:column;justify-content:center">
  <div style="font-family:var(--m);font-weight:700;font-size:14px;letter-spacing:.14em;color:{MUTED};margin-bottom:8px">FROM</div>
  <div class=chk data-n=from style="font-size:22px;font-weight:800;line-height:1.32;letter-spacing:.01em">
    <span style="color:{AQC}">●</span> AQ &nbsp;<span style="color:{SHC}">●</span> SHIKSHAQ<br><span style="color:{MKC}">●</span> MK CYCLES &nbsp;<span style="color:{EKC}">●</span> EKAVYA</div></div>
<div class=gr></div></div>'''
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        await pg.set_content(html); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(700)
        # every text box must sit inside its tile with padding
        bad = await pg.evaluate("""()=>{const out=[];for(const e of document.querySelectorAll('.chk')){const t=e.closest('.tile').getBoundingClientRect(),r=e.getBoundingClientRect();
          if(r.right>t.right-16||r.left<t.left+16||r.bottom>t.bottom-8||r.top<t.top+8)out.push([e.dataset.n,Math.round(r.left-t.left),Math.round(t.right-r.right)])}
          for(const e of document.querySelectorAll('.logo')){const t=e.closest('.tile').getBoundingClientRect(),r=e.firstElementChild.getBoundingClientRect();if(r.right>t.right-50)out.push(['logo',Math.round(t.right-r.right)])}return out}""")
        await pg.screenshot(path=f"{ROOT}/out/four/bento_final.png"); await b.close()
    print("text/tile fit:", "ok" if not bad else bad)
asyncio.run(main())
