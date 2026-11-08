"""Shared kit for the four-company Diwali set: grainy 'spray' gradient shapes on black (idea from two user references:
a sparkler hand with flowing leaves, and a Bontan poster of a hand + spiky stars + orbs). Drawn from scratch.
spray(): fills a shape with colour c1 and overlays colour c2 through a noise-thresholded gradient mask, which is what
gives the gritty stipple fade instead of a smooth blend."""
import math, os, sys, base64, asyncio
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{ROOT}/engine")
import core
W, H = 1080, 1350
_n = [0]
def _id(p): _n[0] += 1; return f"{p}{_n[0]}"
DEFS = ['<filter id="spk" filterUnits="userSpaceOnUse" x="-50" y="-50" width="1200" height="1500" color-interpolation-filters="sRGB">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed="4" result="t"/>'
        '<feColorMatrix in="t" type="matrix" values="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 1" result="g"/>'
        '<feComposite in="SourceGraphic" in2="g" operator="arithmetic" k1="0" k2="1" k3="2.6" k4="-1.3" result="s"/>'
        '<feComponentTransfer in="s"><feFuncR type="linear" slope="12" intercept="-6"/><feFuncG type="linear" slope="12" intercept="-6"/><feFuncB type="linear" slope="12" intercept="-6"/></feComponentTransfer></filter>']
def spray(d, c1, c2, g, stroke=None, bbox=(0, 0, W, H), extra=""):
    """d: path data. g=(x1,y1,x2,y2) gradient: c2 appears toward (x2,y2) as speckle that thickens to solid."""
    gid, mid = _id("g"), _id("m"); x, y, w, h = bbox
    DEFS.append(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{g[0]}" y1="{g[1]}" x2="{g[2]}" y2="{g[3]}"><stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#fff"/></linearGradient>'
                f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="{x}" y="{y}" width="{w}" height="{h}"><g filter="url(#spk)"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{gid})"/></g></mask>')
    return f'<path d="{d}" fill="{c1}" {extra}/><path d="{d}" fill="{c2}" mask="url(#{mid})" {extra}/>'
def flat(d, c, extra=""): return f'<path d="{d}" fill="{c}" {extra}/>'
def star(cx, cy, R, r, n, rot=0, pinch=.28):
    pts = []
    for i in range(n * 2):
        a = math.radians(rot - 90 + i * 180 / n); rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(1, len(pts) + 1):
        p = pts[i % len(pts)]; q = pts[i - 1]
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        cx2, cy2 = mx + (cx - mx) * pinch, my + (cy - my) * pinch
        d += f" Q{cx2:.1f} {cy2:.1f} {p[0]:.1f} {p[1]:.1f}"
    return d + "Z"
def circle(cx, cy, r): return f"M{cx-r} {cy} a{r} {r} 0 1 0 {2*r} 0 a{r} {r} 0 1 0 {-2*r} 0Z"
def leaf(x, y, ang, L, w, bend=0):
    a = math.radians(ang); tx, ty = x + L * math.cos(a), y + L * math.sin(a)
    nx, ny = -math.sin(a), math.cos(a); mx, my = (x + tx) / 2, (y + ty) / 2
    c1 = (mx + nx * (w + bend), my + ny * (w + bend)); c2 = (mx - nx * (w - bend), my - ny * (w - bend))
    return f"M{x:.1f} {y:.1f} Q{c1[0]:.1f} {c1[1]:.1f} {tx:.1f} {ty:.1f} Q{c2[0]:.1f} {c2[1]:.1f} {x:.1f} {y:.1f}Z", (x, y, tx, ty)
def sparkle4(cx, cy, s, rot=0): return star(cx, cy, s, s * .16, 4, rot, pinch=.0)
ARCH = base64.b64encode(open(f"{ROOT}/addons/shikshaq/assets/fonts/archivo-latin.woff2", "rb").read()).decode()
GRAIN = base64.b64encode(open(f"{ROOT}/engine/assets/disco_diwali/grain.png", "rb").read()).decode()
def page(art_svg, body, bg="#0A0A0A"):
    return (f'<!doctype html><meta charset=utf-8><style>{core.FONTS}{core.ROOT}'
            f'@font-face{{font-family:AR;src:url(data:font/woff2;base64,{ARCH});font-weight:100 900}}'
            f'*{{margin:0;box-sizing:border-box}}.p{{width:{W}px;height:{H}px;background:{bg};position:relative;overflow:hidden;color:#F4EFE0;font-family:AR}}'
            f'.gr{{position:absolute;inset:0;background:url(data:image/png;base64,{GRAIN}) center/cover;mix-blend-mode:screen;opacity:.55;z-index:30;pointer-events:none}}</style>'
            f'<div class=p><svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute;left:0;top:0;z-index:2"><defs>{"".join(DEFS)}</defs>{art_svg}</svg>{body}<div class=gr></div></div>')
async def shoot(html, out, check=".chk"):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        await pg.set_content(html); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(600)
        m = await pg.evaluate(f"""()=>[...document.querySelectorAll('{check}')].map(e=>{{const r=e.getBoundingClientRect();return [e.dataset.n||e.className,Math.round(r.left),Math.round(r.top),Math.round(r.right),Math.round(r.bottom)]}})""")
        await pg.screenshot(path=out); await b.close()
    bad = [x for x in m if x[1] < 40 or x[3] > W - 40 or x[4] > H - 30]
    print(os.path.basename(out), "boxes", m, "| OUT OF MARGIN:" if bad else "| margins ok", bad or "")
