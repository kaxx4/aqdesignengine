"""Shikshaq Diwali wish, sparkler direction (feed 1080x1350). Idea from a user-supplied reference
(deep-blue dotted ground, halftone starburst on a sparkler); drawn from scratch in Shikshaq tokens:
indigo ground, orange/peach starburst, bone type (bone on indigo 5.5:1). Logo sits on a bone pill."""
import asyncio, base64, math, os
from playwright.async_api import async_playwright
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); AD = f"{R}/addons/shikshaq/assets"
b64 = lambda p: base64.b64encode(open(p, "rb").read()).decode()
arch = b64(f"{AD}/fonts/archivo-latin.woff2"); geist = b64(f"{AD}/fonts/geist-latin.woff2"); logo = b64(f"{AD}/shikshaq-logo.svg")
INK, BONE, OR, IND, DEEP, TINT = "#1F1F1F", "#F9F5F1", "#FF8000", "#4351FF", "#2E3AD6", "#EDEEFF"
CX, CY = 470, 500
radii = [330,140,255,135,345,150,250,125,305,145,275,135,320,150,262,138]
def star(scale):
    pts=[]
    for i,r in enumerate(radii):
        a=math.radians(-90+i*22.5+6); pts.append(f"{CX+r*scale*math.cos(a):.1f},{CY+r*scale*math.sin(a):.1f}")
    return " ".join(pts)
def core():
    pts=[]
    for i in range(8):
        r=118 if i%2==0 else 30; a=math.radians(-90+i*45+10); pts.append(f"{CX+r*math.cos(a):.1f},{CY+r*math.sin(a):.1f}")
    return " ".join(pts)
rays=[(-60,360,420),(-18,380,455),(30,375,430),(165,372,400),(205,368,425),(100,365,420),(-120,372,425)]
rayssvg="".join(f'<line x1="{CX+a*math.cos(math.radians(t)):.0f}" y1="{CY+a*math.sin(math.radians(t)):.0f}" x2="{CX+b*math.cos(math.radians(t)):.0f}" y2="{CY+b*math.sin(math.radians(t)):.0f}" stroke="#FFD27A" stroke-width="10" stroke-linecap="round"/>' for t,a,b in rays)
def wstar(x,y,s):
    p=[]
    for i in range(10):
        r=s if i%2==0 else s*.42; a=math.radians(-90+i*36); p.append(f"{x+r*math.cos(a):.1f},{y+r*math.sin(a):.1f}")
    return f'<polygon points="{" ".join(p)}" fill="{BONE}"/>'
stars="".join(wstar(*t) for t in [(420,120,22),(780,150,24),(125,430,24),(960,620,22),(135,740,22),(500,930,22),(930,300,16)])
art=f'''<svg viewBox="0 0 1080 1100" width="1080" height="1100" style="position:absolute;left:-64px;top:-80px">
<defs><pattern id="dots" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(30)"><circle cx="7" cy="7" r="3.1" fill="#C95F00"/></pattern>
<pattern id="dots2" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(30)"><circle cx="7" cy="7" r="2.6" fill="#FF8000"/></pattern></defs>
{rayssvg}{stars}
<polygon points="{star(1)}" fill="{OR}" stroke-linejoin="round"/><polygon points="{star(1)}" fill="url(#dots)"/>
<polygon points="{star(.68)}" fill="#FFB259"/><polygon points="{star(.68)}" fill="url(#dots2)"/>
<polygon points="{star(.4)}" fill="#FFF4E8"/>
<polygon points="{core()}" fill="#FFD27A" stroke-linejoin="round"/>
<line x1="{CX}" y1="{CY}" x2="{CX+250}" y2="{CY+330}" stroke="{BONE}" stroke-width="40" stroke-linecap="round"/>
<line x1="{CX+252}" y1="{CY+334}" x2="{CX+345}" y2="{CY+470}" stroke="{BONE}" stroke-width="5" stroke-linecap="round"/></svg>'''
html=f'''<!doctype html><meta charset=utf-8><style>
@font-face{{font-family:A;src:url(data:font/woff2;base64,{arch});font-weight:100 900}}
@font-face{{font-family:G;src:url(data:font/woff2;base64,{geist});font-weight:100 900}}
*{{margin:0;box-sizing:border-box}}
.p{{width:1080px;height:1350px;background:{BONE};position:relative;overflow:hidden;font-family:G;color:{INK}}}
.slab{{position:absolute;left:64px;right:64px;top:150px;height:740px;background:{IND};border-radius:32px;overflow:hidden}}
.dots{{position:absolute;inset:0;background-image:radial-gradient({DEEP} 2.4px,transparent 2.6px);background-size:16px 16px}}
.h{{position:absolute;left:0;right:0;top:925px;text-align:center;font-family:A;font-weight:800;font-size:132px;line-height:1;letter-spacing:-.035em;white-space:nowrap}}
.h span{{font-weight:400}}
.sub{{position:absolute;left:0;right:0;top:1076px;text-align:center;font-size:38px;line-height:1.25;font-weight:500;color:#4A443E}}
.sub b{{color:{IND};font-weight:700}}
.chip{{position:absolute;left:50%;transform:translateX(-50%);bottom:56px;background:{TINT};color:{DEEP};border-radius:999px;padding:14px 30px;font-weight:700;font-size:25px;white-space:nowrap}}
.logo{{position:absolute;left:64px;top:48px;background:{BONE};border-radius:999px;padding:10px 22px;height:64px;display:flex;align-items:center}}
</style><div class=p>
<img src="data:image/svg+xml;base64,{logo}" style="position:absolute;left:64px;top:44px;height:84px">
<div class=slab><div class=dots></div>{art}</div>
<div class=h>Happy <span>Diwali</span></div>
<div class=sub>Wishing every student, parent<br>and teacher a <b>bright</b> one.</div>
<div class=chip>From all of us at Shikshaq</div></div>'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={"width":1080,"height":1350},device_scale_factor=2)
        await pg.set_content(html); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
        print(await pg.evaluate("""()=>[...document.querySelectorAll('.h,.sub,.chip,.slab')].map(e=>{const r=e.getBoundingClientRect();return [e.className,Math.round(r.left),Math.round(r.top),Math.round(r.right),Math.round(r.bottom)]})"""))
        await pg.screenshot(path=f"{R}/out/diwali/shikshaq_sparkler_final.png"); await b.close()
asyncio.run(main())
