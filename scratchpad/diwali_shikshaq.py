"""Shikshaq Diwali wish (feed 1080x1350). Shikshaq tokens from addons/shikshaq/src/tokens.mjs:
bone ground (never white), one saturated orange slab at radius 32, ink type on orange (white is 2.5:1),
indigo as the second accent, Archivo 800/400 headline pair. Copy carries no number or claim."""
import asyncio, base64, os
from playwright.async_api import async_playwright
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); AD = f"{R}/addons/shikshaq/assets"
b64 = lambda p: base64.b64encode(open(p, "rb").read()).decode()
arch = b64(f"{AD}/fonts/archivo-latin.woff2"); geist = b64(f"{AD}/fonts/geist-latin.woff2")
logo = b64(f"{AD}/shikshaq-logo.svg")
INK, BONE, OR, IND, TINT = "#1F1F1F", "#F9F5F1", "#FF8000", "#4351FF", "#EDEEFF"
diya = f'''<svg viewBox="0 0 400 290" width="640" height="464" style="overflow:visible">
<path d="M18 150 Q200 340 382 150 Z" fill="{IND}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
<ellipse cx="200" cy="150" rx="182" ry="20" fill="{BONE}" stroke="{INK}" stroke-width="8"/>
<g fill="{BONE}"><circle cx="110" cy="205" r="9"/><circle cx="160" cy="232" r="9"/><circle cx="200" cy="242" r="9"/><circle cx="240" cy="232" r="9"/><circle cx="290" cy="205" r="9"/></g>
<path d="M200 20 C150 70 140 112 200 142 C260 112 250 70 200 20 Z" fill="{OR}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
<path d="M200 76 C180 98 180 118 200 132 C220 118 220 98 200 76 Z" fill="#FFF4E8" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>
<g stroke="{INK}" stroke-width="8" stroke-linecap="round"><line x1="108" y1="62" x2="84" y2="44"/><line x1="292" y1="62" x2="316" y2="44"/><line x1="92" y1="112" x2="62" y2="110"/><line x1="308" y1="112" x2="338" y2="110"/></g></svg>'''
import importlib.util
sp=importlib.util.spec_from_file_location("ds",f"{R}/scratchpad/diya_scene.py"); ds=importlib.util.module_from_spec(sp); sp.loader.exec_module(ds)
PAL=dict(ink=INK, sw=6, hard=False, night="#2E3AD6", star="#F9F5F1", f1=OR, f2="#FFB259", f3="#FFF4E8", sand="#FCECDE", sand2="#F3D9BF",
  hill="#4351FF", bulb="#FFD27A", candle1=OR, candle2="#FFB259", skin="#C98A5B", cloth1=OR, cloth2=BONE, lantern_up="#FFB259",
  tile="#FFF4E8", bal="#FFB259", wall=OR, wall2="#E57300", flower=BONE, lan1="#34B268", lan2=IND, rim=OR, rim_bead=BONE, ground_shadow="#F0EAE2")
spark = lambda x,y,sz,c: f'<svg viewBox="-50 -50 100 100" width="{sz}" height="{sz}" style="position:absolute;left:{x}px;top:{y}px"><path d="M0 -48 Q6 -6 48 0 Q6 6 0 48 Q-6 6 -48 0 Q-6 -6 0 -48Z" fill="{c}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/></svg>'
sparks = spark(150,200,84,IND)+spark(880,180,64,OR)+spark(110,380,48,OR)+spark(930,340,52,IND)+spark(790,300,36,OR)
html = f'''<!doctype html><meta charset=utf-8><style>
@font-face{{font-family:A;src:url(data:font/woff2;base64,{arch});font-weight:100 900}}
@font-face{{font-family:G;src:url(data:font/woff2;base64,{geist});font-weight:100 900}}
*{{margin:0;box-sizing:border-box}}
.p{{width:1080px;height:1350px;background:{BONE};position:relative;overflow:hidden;font-family:G}}
.h{{position:absolute;left:0;right:0;top:930px;text-align:center;font-family:A;font-weight:800;font-size:132px;line-height:1;letter-spacing:-.035em;color:{INK};white-space:nowrap}}
.h span{{font-weight:400}}
.sub{{position:absolute;left:0;right:0;top:1076px;text-align:center;font-size:40px;line-height:1.25;color:#4A443E;font-weight:500}}
.sub b{{color:{IND};font-weight:700}}
.chip{{position:absolute;left:50%;transform:translateX(-50%);bottom:56px;background:{TINT};color:#2E3AD6;border-radius:999px;padding:16px 32px;font-weight:700;font-size:26px;white-space:nowrap}}
.sc{{position:absolute;left:70px;top:96px;width:940px}}
</style><div class=p>
<img src="data:image/svg+xml;base64,{logo}" style="position:absolute;left:64px;top:56px;height:84px">
<div class=sc>{ds.scene(PAL,"sq")}</div>{sparks}
<div class=h>Happy <span>Diwali</span></div>
<div class=sub>Wishing every student, parent<br>and teacher a <b>bright</b> one.</div>
<div class=chip>From all of us at Shikshaq</div></div>'''
async def main():
    os.makedirs(f"{R}/out/diwali", exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width":1080,"height":1350}, device_scale_factor=2)
        await pg.set_content(html); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
        m = await pg.evaluate("""()=>[...document.querySelectorAll('.h,.sub,.chip,.sc svg')].map(e=>{const r=e.getBoundingClientRect();return [e.tagName+'.'+(e.getAttribute('class')||''),Math.round(r.left),Math.round(r.top),Math.round(r.right),Math.round(r.bottom)]})""")
        print(m)
        await pg.screenshot(path=f"{R}/out/diwali/shikshaq_diwali_final.png"); await b.close()
asyncio.run(main())
