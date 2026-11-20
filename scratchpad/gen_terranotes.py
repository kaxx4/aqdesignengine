"""TerraNotes logo (bespoke, Workflow C style, no reference to match).
Mechanism: AQ wordmark craft (thick ink outline + hard offset shadow + one shine) on a two-voice
lockup: TERRA in NeutralFace 900 (sky, the brand's blue) and *notes* in Instrument Serif italic
(lemon) stacked over its baseline, as in the working mark. Serif used for ONE word (§9).
Adaptations: leaves are the engine leaf doodle (mint); sparkles stand in for the contour-map pluses."""
import asyncio, os, sys, importlib.util
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ED = os.path.join(os.getcwd(), "engine"); sys.path.insert(0, ED)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ED, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles")
A = core.ACCENTS; SKY, MINT, LEMON, INK, CREAM = A[4], A[1], A[2], core.INK, core.CREAM

def lockup(W, H, ground, ol, shadow_c, scale=1.0, tag=True):
    cx = W/2
    S = scale
    t_size, n_size = 330*S, 400*S
    t_y, n_y = H*0.50, H*0.50 + 250*S
    sw_t, sw_n, off = 16*S, 18*S, 14*S
    def txt(x, y, size, fam, extra, fill, stroke, sw, dx=0, dy=0, idn=""):
        return (f'<text {idn} x="{x+dx}" y="{y+dy}" text-anchor="middle" font-family="{fam}" font-size="{size}" '
                f'{extra} fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" paint-order="stroke fill">')
    T = "TERRA"; N = "notes"
    tf = "font-weight=\"900\" letter-spacing=\"-6\""
    nf = "font-style=\"italic\" letter-spacing=\"-4\""
    svg = f'''<svg style="position:absolute;inset:0;z-index:6" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
    <defs>
      <clipPath id="tc">{txt(cx,t_y,t_size,"NeutralFace",tf,"#000","none",0)}{T}</text></clipPath>
      <clipPath id="nc">{txt(cx,n_y,n_size,"Instrument Serif",nf,"#000","none",0)}{N}</text></clipPath>
    </defs>
    {txt(cx,t_y,t_size,"NeutralFace",tf,shadow_c,shadow_c,sw_t,off,off)}{T}</text>
    {txt(cx,t_y,t_size,"NeutralFace",tf,SKY,ol,sw_t)}{T}</text>
    <g clip-path="url(#tc)"><polygon points="{cx-420*S},{t_y-260*S} {cx-300*S},{t_y-260*S} {cx-520*S},{t_y+20*S} {cx-640*S},{t_y+20*S}" fill="#fff" opacity=".35"/>
    <polygon points="{cx-250*S},{t_y-260*S} {cx-215*S},{t_y-260*S} {cx-435*S},{t_y+20*S} {cx-470*S},{t_y+20*S}" fill="#fff" opacity=".35"/></g>
    {txt(cx,n_y,n_size,"Instrument Serif",nf,shadow_c,shadow_c,sw_n,off,off)}{N}</text>
    {txt(cx,n_y,n_size,"Instrument Serif",nf,LEMON,ol,sw_n)}{N}</text>
    </svg>'''
    def d(kind, x, y, size, color, rot=0, z=4):
        return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;z-index:{z}">'
                f'{dd.stamp(kind, color, rot=rot)}</div>')
    parts = [f'<div style="position:absolute;inset:0;background:{ground}"></div>',
             d("leaf", cx-590*S, n_y-250*S, 210*S, MINT, rot=-8, z=9),
             d("leaf", cx+400*S, n_y-290*S, 230*S, MINT, rot=68, z=9),
             svg,
             d("sparkle", cx-720*S, t_y-330*S, 110*S, LEMON, rot=8, z=7),
             d("sparkle", cx+580*S, t_y-390*S, 80*S, ol if ground==CREAM else CREAM, rot=0, z=7),
             d("plus", cx+470*S, n_y+10*S, 70*S, SKY if ground==CREAM else CREAM, rot=0, z=7)]
    if tag:
        tc = core.on_cream(MINT, 26) if ground == CREAM else CREAM
        parts.append(f'<div style="position:absolute;left:0;right:0;top:{n_y+90*S}px;text-align:center;z-index:8;'
                     f'font-family:var(--m);font-weight:700;font-size:{30*S}px;letter-spacing:{10*S}px;color:{tc}">BY AQUATERRA</div>')
    return "".join(parts)

async def main():
    out = "out/terranotes"
    jobs = [("terranotes_logo_cream", 1500, 1000, CREAM, INK, INK, 1.0),
            ("terranotes_logo_sky",   1500, 1000, SKY,   INK, INK, 1.0)]
    async with B.session():
        for name, W, H, g, ol, sc, s in jobs:
            inner = lockup(W, H, g, ol, sc, s)
            if g == SKY:   # on sky, the wordmark's own fill would vanish: recolour TERRA cream
                inner = inner.replace(f'fill="{SKY}" stroke', f'fill="{CREAM}" stroke')
            await B.render(B.page(W, H, g, inner, grain=False), f"{out}/{name}.png", W, H, page_bg=g)
    print("done")
asyncio.run(main())
