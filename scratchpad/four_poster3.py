"""Cohesive four-company Diwali poster built on the recreated sparkler illustration, in its own palette
(pink, yellow, green, coral, lavender, blue on black). The art sits full-width at the bottom and fades up into an
extended black header band that carries the title, small logos and the web addresses, plus a few matching shapes
so the band reads as part of the same picture. Branding stays small, as the references do."""
import asyncio, os, sys, base64, importlib.util, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, f"{ROOT}/engine")
import core
sp = importlib.util.spec_from_file_location("sr", f"{ROOT}/scratchpad/sparkler_recreate.py"); sr = importlib.util.module_from_spec(sp); sp.loader.exec_module(sr)
b64 = lambda p: base64.b64encode(open(p, "rb").read()).decode()
W, H, BAND = 1080, 1350, 270; ART = H - BAND
CO = f"{ROOT}/scratchpad/co"
ARCH = b64(f"{ROOT}/addons/shikshaq/assets/fonts/archivo-latin.woff2")
YEL, CREAM, INK = "#FBBE0E", "#F4EFE0", sr.INK
# ---- header-band decorations (poster coords), kept to the right/middle so type stays clear
rnd = random.Random(21); band = []
for _ in range(160):
    band.append(f'<circle cx="{rnd.uniform(0,W):.1f}" cy="{rnd.uniform(0,BAND+40):.1f}" r="{rnd.choice([.7,1,1.3,1.8])}" fill="#d8d4c4" opacity="{rnd.uniform(.25,.7):.2f}"/>')
band += [sr.ribbon([(836, 78), (858, 96), (886, 90), (912, 114), (938, 122)], 11, sr.BLUE, sr.BLUEL),
         sr.loop([(966, 62), (982, 52), (1002, 58), (1002, 78), (986, 92), (970, 84)], sr.LG, 7),
         sr.band([(1010, 112), (1040, 128), (1075, 146), (1100, 172)], [2, 9, 13, 10], sr.RED, sr.PINKL, side=-1, c2frac=.5),
         sr.band([(700, 280), (740, 268), (790, 254)], [3, 9, 2], sr.LAV, sr.LAVL, side=-1),
         sr.loop([(560, 262), (574, 254), (592, 258), (592, 276), (576, 284), (562, 278)], sr.SALMON, 7),
         sr.ribbon([(840, 258), (856, 270), (846, 284), (864, 296)], 10, sr.DG),
         sr.band([(930, 272), (970, 258), (1010, 236)], [3, 8, 2], sr.RED, sr.PINKL, side=-1)]
for x, y, r, c in [(830, 150, 7, sr.LAVL), (1042, 214, 8, sr.LAVL), (815, 60, 5, "#F5A02A"), (1050, 86, 6, "#F5A02A"), (655, 266, 4, sr.LAVL), (1030, 260, 5, "#F5A02A"), (770, 268, 5, "#F5A02A")]:
    band.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>')
band_svg = (f'<svg width="{W}" height="{BAND+60}" viewBox="0 0 {W} {BAND+60}" style="position:absolute;left:0;top:0;z-index:2">'
            f'<defs><filter id="rfb" x="-3%" y="-3%" width="106%" height="106%"><feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="3" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3.2" xChannelSelector="R" yChannelSelector="G"/></filter></defs>'
            f'<g filter="url(#rfb)">{"".join(band)}</g></svg>')
art_svg = sr.svg.replace('width="736" height="736"', f'width="{W}" height="{W}"', 1)
sh = f'<img src="data:image/svg+xml;base64,{b64(ROOT+"/addons/shikshaq/assets/shikshaq-logo.svg")}" style="height:30px">'
pill = lambda i: f'<span style="background:{CREAM};border-radius:999px;padding:5px 13px;display:inline-flex;align-items:center">{i}</span>'
logos = (pill(f'<img src="{core.LOGO}" style="height:22px">') + pill(sh) + f'<img src="data:image/png;base64,{b64(CO+"/mk_logo_crop.png")}" style="height:38px">' +
         f'<img src="data:image/svg+xml;base64,{b64(CO+"/ek_icon.svg")}" style="height:38px">')
html = f'''<!doctype html><meta charset=utf-8><style>{core.FONTS}{core.ROOT}
@font-face{{font-family:AR;src:url(data:font/woff2;base64,{ARCH});font-weight:100 900}}
*{{margin:0;box-sizing:border-box}}
.p{{width:{W}px;height:{H}px;background:{INK};position:relative;overflow:hidden;font-family:AR;color:{CREAM}}}
.art{{position:absolute;left:0;top:{BAND}px;width:{W}px;height:{W}px;z-index:1;-webkit-mask-image:linear-gradient(to bottom,transparent 0,#000 110px);mask-image:linear-gradient(to bottom,transparent 0,#000 110px)}}
.chk{{position:absolute;z-index:12;white-space:nowrap}}
</style><div class=p>
<div class=art>{art_svg}</div>{band_svg}
<div style="position:absolute;left:40px;right:40px;top:36px;height:2px;background:{CREAM};z-index:12"></div>
<div class=chk data-n=title style="left:40px;top:58px;font-weight:800;font-size:104px;line-height:1;letter-spacing:-.03em;color:{YEL}">HAPPY DIWALI</div>
<div class=chk data-n=sub style="left:42px;top:176px;font-weight:800;font-size:27px;line-height:1;letter-spacing:-.005em">AQ · SHIKSHAQ · MK CYCLES · EKAVYA</div>
<div class=chk data-n=logos style="right:40px;top:170px;display:flex;align-items:center;gap:14px">{logos}</div>
<div class=chk data-n=urls style="left:42px;top:222px;font-family:var(--m);font-weight:700;font-size:14.5px;letter-spacing:.05em;color:#a39e8c">VISIT US AT  NGOAQUATERRA.COM · SHIKSHAQ.IN · MKCYCLES.IN · EKAVYAVYAPAAR.VERCEL.APP</div>
</div>'''
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        await pg.set_content(html); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(600)
        m = await pg.evaluate("""()=>[...document.querySelectorAll('.chk')].map(e=>{const r=e.getBoundingClientRect();return [e.dataset.n,Math.round(r.left),Math.round(r.top),Math.round(r.right),Math.round(r.bottom)]})""")
        await pg.screenshot(path=f"{ROOT}/out/four/poster3_final.png"); await b.close()
    print(m, "| margins ok" if all(x[1] >= 38 and x[3] <= W - 38 for x in m) else "| OUT OF MARGIN")
asyncio.run(main())
