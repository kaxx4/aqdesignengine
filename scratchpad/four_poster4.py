"""Four-company Diwali poster as a BENTO: full black grain-textured ground, rounded tiles with hairline edges:
title tile, the recreated sparkler illustration in a tall art tile, four company tiles (logo + 'Visit us at' + link,
each with an accent taken from the illustration), a wish tile and a 'from' tile. Tokens: radius 32, 16px gaps, 40px margin."""
import asyncio, os, sys, base64, importlib.util, random, math
os.environ["SPARKLER_HAND"] = "black"
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
def company(i, logo, site, color, note=None):
    y = y_art + i * (CO_H + G)
    return (f'<div class="tile" style="left:{M+ART_W+G}px;top:{y:.0f}px;width:{COL_W}px;height:{CO_H:.0f}px;padding:22px 26px;display:flex;flex-direction:column;justify-content:space-between">'
            f'<div style="display:flex;align-items:center;justify-content:space-between"><div class=logo style="position:relative;z-index:2;min-height:64px;display:flex;align-items:center">{logo}</div><span style="width:16px;height:16px;border-radius:50%;background:{color};flex:none"></span></div>'
            f'{_co_deco(i)}<div style="position:relative;z-index:2"><div style="font-family:var(--m);font-weight:700;font-size:14px;letter-spacing:.14em;color:{MUTED}">{"NOW BUILDING" if note else "VISIT US AT"}</div>'
            f'<div class=chk data-n="{note or site}" style="margin-top:5px;font-size:23px;font-weight:700;color:{CREAM};white-space:nowrap">{note or site}</div></div></div>')
def _star(x, y, sz, c): return f'<path transform="translate({x} {y})" d="M0 -{sz} Q2 -2 {sz} 0 Q2 2 0 {sz} Q-2 2 -{sz} 0 Q-2 -2 0 -{sz}Z" fill="{c}"/>'
def _dots(ds): return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x, y, r, c in ds)
def _svg(w, h, inner, z=1): return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="position:absolute;left:0;top:0;z-index:{z}">{inner}</svg>'
def _wish_deco():
    L = [sr.ribbon([(30, 126), (50, 108), (72, 114), (92, 94), (116, 88)], 10, sr.BLUE, sr.BLUEL),
         sr.loop([(46, 40), (60, 30), (80, 36), (80, 56), (64, 68), (50, 60)], sr.LG, 7),
         sr.band([(80, 150), (104, 134), (134, 126)], [2, 8, 2], sr.LAV, sr.LAVL, side=-1),
         sr.band([(968, 136), (944, 118), (914, 106), (892, 84)], [2, 9, 12, 2], sr.RED, sr.PINKL, side=-1, c2frac=.5),
         sr.loop([(900, 36), (914, 26), (934, 32), (934, 52), (918, 64), (904, 56)], sr.SALMON, 7),
         sr.ribbon([(962, 40), (948, 56), (960, 70), (946, 90)], 10, sr.DG),
         _dots([(20, 80, 6, sr.LAVL), (130, 40, 5, "#F5A02A"), (120, 150, 4, sr.LAVL), (984, 100, 7, sr.LAVL), (868, 140, 5, "#F5A02A"), (880, 20, 4, sr.LAVL)]),
         _star(150, 100, 11, YEL), _star(858, 100, 12, YEL), _star(28, 150, 8, CREAM), _star(978, 28, 9, CREAM)]
    return _svg(1000, 168, "".join(L))
wish_deco = _wish_deco()
def _title_deco():
    L = [sr.ribbon([(806, 30), (828, 40), (848, 32), (872, 42)], 9, sr.BLUE, sr.BLUEL), sr.loop([(950, 22), (964, 12), (984, 18), (984, 38), (968, 50), (954, 42)], sr.LG, 7),
         sr.band([(930, 172), (960, 160), (990, 138)], [2, 9, 2], sr.RED, sr.PINKL, side=-1), sr.band([(790, 150), (826, 164), (872, 172)], [2, 8, 2], sr.LAV, sr.LAVL, side=1),
         _dots([(800, 100, 6, sr.LAVL), (968, 96, 6, "#F5A02A"), (930, 150, 4, sr.LAVL), (800, 60, 4, "#F5A02A")]), _star(792, 128, 9, YEL)]
    return _svg(1000, 190, "".join(L))
title_deco = _title_deco()
def _co_deco(i):
    """small sector icons in the illustration's flat style, kept inside x 214..334, y 88..156 (clear of logo + text)"""
    L = []
    if i == 0:   # AquaTerra: globe with a sprout (environment / NGO)
        L = [f'<circle cx="274" cy="124" r="30" fill="{sr.BLUE}"/>',
             sr.blob([(256, 108), (270, 102), (282, 108), (278, 120), (266, 126), (256, 120)], sr.LG),
             sr.blob([(280, 128), (292, 124), (298, 134), (290, 146), (280, 142)], sr.DG),
             f'<path d="M244 124 Q274 114 304 124 M274 94 Q262 124 274 154" fill="none" stroke="{sr.BLUEL}" stroke-width="2.5" opacity=".8"/>',
             f'<path d="M274 94 L274 76" stroke="{sr.DG}" stroke-width="5" stroke-linecap="round"/>',
             sr.band([(274, 80), (262, 68), (248, 66)], [1, 8, 2], sr.LG, sr.DG, side=-1), sr.band([(274, 76), (288, 62), (304, 60)], [1, 8, 2], sr.LG, sr.DG, side=1),
             _dots([(220, 112, 4, sr.LAVL), (322, 100, 4, "#F5A02A")]), _star(316, 140, 8, YEL)]
    elif i == 1: # Shikshaq: open book + pencil (education)
        L = [f'<path d="M232 140 L274 132 L274 100 L232 106 Z" fill="{sr.LAV}"/>', f'<path d="M316 140 L274 132 L274 100 L316 106 Z" fill="{sr.LAVL}"/>',
             f'<path d="M232 106 L274 100 L316 106" fill="none" stroke="{CREAM}" stroke-width="3" stroke-linejoin="round"/>',
             "".join(f'<line x1="240" y1="{112+i_*8}" x2="268" y2="{108+i_*8}" stroke="{CREAM}" stroke-width="2.4" stroke-linecap="round"/><line x1="280" y1="{108+i_*8}" x2="308" y2="{112+i_*8}" stroke="{sr.LAV}" stroke-width="2.4" stroke-linecap="round"/>' for i_ in range(3)),
             f'<g transform="rotate(38 308 90)"><rect x="302" y="62" width="12" height="52" rx="2" fill="{YEL}"/><path d="M302 114 L314 114 L308 126 Z" fill="{sr.PINKL}"/><rect x="302" y="62" width="12" height="9" fill="{sr.RED}"/></g>',
             _dots([(222, 92, 4, sr.LAVL), (326, 140, 4, "#F5A02A")]), _star(240, 80, 8, CREAM)]
    elif i == 2: # MK Cycles: bicycle wheel + gear (cycles)
        cx, cy = 262, 118
        L = [f'<circle cx="{cx}" cy="{cy}" r="32" fill="none" stroke="{sr.RED}" stroke-width="6"/>', f'<circle cx="{cx}" cy="{cy}" r="26" fill="none" stroke="{sr.PINKL}" stroke-width="2"/>',
             "".join(f'<line x1="{cx}" y1="{cy}" x2="{cx+27*math.cos(math.radians(a_*30)):.1f}" y2="{cy+27*math.sin(math.radians(a_*30)):.1f}" stroke="{CREAM}" stroke-width="1.8"/>' for a_ in range(12)),
             f'<circle cx="{cx}" cy="{cy}" r="5" fill="{YEL}"/>']
        gx, gy = 316, 134
        g = "M" + " L".join(f"{gx+(15 if k%2==0 else 11)*math.cos(math.radians(k*22.5)):.1f} {gy+(15 if k%2==0 else 11)*math.sin(math.radians(k*22.5)):.1f}" for k in range(16)) + "Z"
        L += [f'<path d="{g}" fill="{YEL}"/>', f'<circle cx="{gx}" cy="{gy}" r="5" fill="{TILE}"/>', _dots([(318, 96, 4, "#F5A02A"), (222, 98, 4, sr.LAVL)])]
    else:        # Ekavya: building frame + crane (real estate)
        L = ['<g transform="translate(2 20)">'] + [f'<rect x="236" y="96" width="62" height="58" fill="none" stroke="{sr.BLUE}" stroke-width="4"/>',
             "".join(f'<line x1="236" y1="{96+k*19.3:.1f}" x2="298" y2="{96+k*19.3:.1f}" stroke="{sr.BLUE}" stroke-width="3.5"/>' for k in (1, 2)),
             "".join(f'<line x1="{236+k*20.7:.1f}" y1="96" x2="{236+k*20.7:.1f}" y2="154" stroke="{sr.BLUE}" stroke-width="3.5"/>' for k in (1, 2)),
             f'<rect x="258" y="136" width="14" height="12" fill="{YEL}"/><rect x="278" y="117" width="14" height="12" fill="{YEL}"/><rect x="240" y="117" width="14" height="12" fill="{sr.PINKL}"/>',
             f'<path d="M300 154 L300 74 M300 74 L240 74 M300 74 L322 74" stroke="{sr.RED}" stroke-width="5" stroke-linecap="round"/><path d="M252 74 L252 90" stroke="{CREAM}" stroke-width="2"/><path d="M300 74 L322 94" stroke="{sr.RED}" stroke-width="2.5"/>',
             _dots([(222, 82, 4, sr.LAVL), (326, 132, 4, "#F5A02A")]), _star(326, 108, 8, YEL)] + ['</g>']
    return _svg(344, 208, "".join(L))

html = f'''<!doctype html><meta charset=utf-8><style>{core.FONTS}{core.ROOT}
@font-face{{font-family:AR;src:url(data:font/woff2;base64,{ARCH});font-weight:100 900}}
*{{margin:0;box-sizing:border-box}}
.p{{width:{W}px;height:{H}px;background:{INK};position:relative;overflow:hidden;font-family:AR;color:{CREAM}}}
.tile{{position:absolute;background:{TILE};border:1px solid {EDGE};border-radius:{R}px;overflow:hidden;z-index:5}}
.gr{{position:absolute;inset:0;background:url(data:image/png;base64,{GRAIN}) center/cover;mix-blend-mode:screen;opacity:.6;z-index:30;pointer-events:none}}
</style><div class=p>
<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0;z-index:1">{dust}</svg>
<div class="tile" style="left:{M}px;top:{M}px;width:{CW}px;height:{T_H}px;padding:0 36px;display:flex;align-items:center;justify-content:space-between">{title_deco}
  <div><div style="font-family:var(--m);font-weight:700;font-size:15px;letter-spacing:.2em;color:{MUTED};margin-bottom:6px">DIWALI GREETINGS</div>
  <div style="display:flex;align-items:baseline;gap:22px;white-space:nowrap" class=chk data-n=title>
    <span style="font-family:var(--s);font-style:italic;font-weight:400;font-size:124px;line-height:1;color:{CREAM};letter-spacing:-.01em">Happy</span>
    <span style="font-weight:800;font-size:122px;line-height:1;letter-spacing:-.035em;color:{YEL};text-shadow:5px 5px 0 {sr.RED}">DIWALI</span></div></div>
  <svg width="86" height="86" viewBox="-50 -50 100 100" style="position:relative;z-index:2">{"".join(f'<line x1="{14*math.cos(math.radians(i*15)):.1f}" y1="{14*math.sin(math.radians(i*15)):.1f}" x2="{(46 if i%2==0 else 36)*math.cos(math.radians(i*15)):.1f}" y2="{(46 if i%2==0 else 36)*math.sin(math.radians(i*15)):.1f}" stroke="{CREAM}" stroke-width="3" stroke-linecap="round"/>' for i in range(24))}</svg>
</div>
<div class="tile" style="left:{M}px;top:{y_art}px;width:{ART_W}px;height:{ART_H}px"><div style="position:absolute;left:-120px;top:0;width:880px;height:880px">{art_svg}</div></div>
{company(0, aq_logo, "www.ngoaquaterra.com", AQC)}{company(1, sh_logo, "www.shikshaq.in", SHC)}{company(2, mk_logo, "mkcycles.in", MKC)}{company(3, ek_logo, "", EKC, note="in South Kolkata")}
<div class="tile" style="left:{M}px;top:{y_r3}px;width:{CW}px;height:{R3_H}px;display:flex;align-items:center;justify-content:center">
  {wish_deco}
  <div class=chk data-n=wish style="position:relative;z-index:2;text-align:center;white-space:nowrap">
    <div style="display:flex;align-items:baseline;justify-content:center;gap:18px;line-height:1">
      <span style="font-family:var(--s);font-style:italic;font-size:64px;color:{CREAM}">Wishing you</span>
      <span style="font-weight:800;font-size:56px;letter-spacing:-.03em;color:{YEL};text-shadow:3px 3px 0 {sr.RED}">LIGHT</span>
      <span style="font-family:var(--s);font-style:italic;font-size:52px;color:{MUTED}">&amp;</span>
      <span style="font-weight:800;font-size:56px;letter-spacing:-.03em;color:#EE84C2;text-shadow:3px 3px 0 {sr.DG}">LOVE</span></div>
    <div style="margin-top:12px;font-family:var(--s);font-style:italic;font-size:40px;line-height:1;color:{CREAM};opacity:.92">and a bright year ahead</div></div></div>
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
