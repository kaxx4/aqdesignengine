"""TerraNotes masthead v2 (bespoke). Editorial, not sticker: lowercase Eina 600 'terra' + large
Instrument Serif italic 'notes' tucked up under it (as in the working mark), hairline leaf sprout,
hairline rule + mono credit. Adaptation recorded: the AQ heavy outline/hard-shadow craft layer is
DROPPED on the user's request (magazine, elegant); the serif carries ONE word (§9)."""
import asyncio, os, sys, importlib.util
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ED = os.path.join(os.getcwd(), "engine"); sys.path.insert(0, ED)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ED, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build")
A = core.ACCENTS; SKY, MINT, LEMON, GRAPE, INK, CREAM = A[4], A[1], A[2], A[5], core.INK, core.CREAM

def leaf_pair(c, line, size):
    # fine-line sprout: two leaves on a curved stem
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 120 120" style="position:absolute;overflow:visible">'
            f'<path d="M58 112 C58 84 60 62 66 40" fill="none" stroke="{line}" stroke-width="2.6" stroke-linecap="round"/>'
            f'<path d="M62 70 C36 70 18 52 16 28 C42 28 60 44 62 70 Z" fill="{c}" stroke="{line}" stroke-width="2.6" stroke-linejoin="round"/>'
            f'<path d="M64 52 C70 26 90 10 112 10 C112 36 94 54 64 52 Z" fill="{c}" stroke="{line}" stroke-width="2.6" stroke-linejoin="round"/>'
            f'<path d="M62 70 C48 62 34 50 22 34 M64 52 C80 40 94 26 108 14" fill="none" stroke="{line}" stroke-width="1.6" stroke-linecap="round" opacity=".7"/></svg>')

def masthead(W, H, ground, t_col, n_col, leaf_c, line, tag_col, spark):
    cx = W/2
    t = (f'<div style="position:absolute;left:0;right:0;top:{H*0.20}px;text-align:center;z-index:5;font-family:var(--e);'
         f'font-weight:600;font-size:400px;line-height:1;letter-spacing:-14px;color:{t_col}">terra</div>')
    n = (f'<div style="position:absolute;left:0;right:0;top:{H*0.20+235}px;text-align:center;z-index:6;font-family:var(--s);'
         f'font-style:italic;font-size:430px;line-height:1;letter-spacing:-6px;color:{n_col}">notes</div>')
    lf = f'<div style="position:absolute;left:{cx+372}px;top:{H*0.20-42}px;z-index:7">{leaf_pair(leaf_c, line, 150)}</div>'
    rule = (f'<div style="position:absolute;left:{cx-330}px;width:660px;top:{H*0.20+672}px;height:2px;background:{line};opacity:.55;z-index:5"></div>'
            f'<div style="position:absolute;left:0;right:0;top:{H*0.20+699}px;text-align:center;z-index:5;font-family:var(--m);'
            f'font-weight:500;font-size:24px;letter-spacing:11px;color:{tag_col}">A MAGAZINE BY AQUATERRA</div>')
    sp = (f'<svg width="46" height="46" viewBox="-23 -23 46 46" style="position:absolute;left:{cx+560}px;top:{H*0.20+390}px;z-index:7">'
          f'<path d="M0 -22 C2 -6 6 -2 22 0 C6 2 2 6 0 22 C-2 6 -6 2 -22 0 C-6 -2 -2 -6 0 -22Z" fill="{spark}"/></svg>')
    return f'<div style="position:absolute;inset:0;background:{ground}"></div>' + t + n + lf + rule + sp

async def main():
    W, H = 1500, 1200; out = "out/terranotes"
    jobs = [("terranotes_v2_cream", CREAM, INK, GRAPE, MINT, INK, core.INK3 if hasattr(core,"INK3") else "#5A5A55", LEMON),
            ("terranotes_v2_ink",   INK, CREAM, LEMON, MINT, CREAM, CREAM, LEMON),
            ("terranotes_v2_sky",   SKY, CREAM, INK, MINT, INK, INK, CREAM)]
    async with B.session():
        for name, g, tc, nc, lc, ln, tg, sp in jobs:
            html = B.page(W, H, g, masthead(W, H, g, tc, nc, lc, ln, tg, sp), grain=False)
            await B.render(html, f"{out}/{name}.png", W, H, page_bg=g)
asyncio.run(main()); print("done")
