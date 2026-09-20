"""25d39cb69b3684 v4 — scale-up + reflow pass on top of v3 (script lost, rebuilt from the render).
Reference (`dröm` furniture-brand poster): a giant lowercase wordmark spanning near the full canvas
width, sitting directly above a row of 5-6 flat die-cut blob "furniture creature" objects in a wide
4:1 size range, packed edge to edge with almost no cream margin.

v3 critique (compare.py): CONTENT TOO SMALL (0.67x, BLOCKING), CENTROID OFF (shift right/down),
region under-filled top-right (row7/col8) and bottom-left (row10/col2), one region over-filled
mid-right. v3 already had the right silhouette set (bean/mouth blob, table/hippo-leg blob, tree
blob, square, boot blob) and right colors -- it was just built too small and too centered-left.
Fix: same 5 objects, scaled ~1.5x into a genuinely edge-to-edge 4:1 range, wordmark widened to span
margin-to-margin like the reference, whole composition shifted right/down to fix centroid, and a
small top-right credit block added to fill the row7/col8 gap (the reference's own device list).
"""
import asyncio, os, sys, importlib.util
# Repo root from THIS FILE's location. A hardcoded root has broken this repo
# five times; the last fix just swapped in a NEW absolute path.
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join("engine", n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); S = load("shapes"); dd = load("doodles"); lay = load("layout")

W, H = core.SIZES["feed"]; M = 56
A = core.ACCENTS
CREAM = "var(--bg)"
elements = []

def at(x, y, w, h, inner, z=6, rot=0):
    elements.append((x, y, w, h))
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'z-index:{z};transform:rotate({rot}deg)">{inner}</div>')

badge = at(56, 52, 76, 76,
           f'<div style="width:100%;height:100%;background:{A[3]};border-radius:6px;display:flex;'
           f'align-items:center;justify-content:center;font-size:34px">👍</div>', z=30)

info_l = (f'<div style="position:absolute;top:160px;left:{M}px;font-family:var(--m);font-weight:700;'
          f'font-size:15px;line-height:1.55;color:var(--ink);z-index:30">kolkata, india<br>'
          f'open drives:<br>all year round</div>')
info_c = (f'<div style="position:absolute;top:160px;left:0;right:0;text-align:center;font-family:'
          f'var(--m);font-weight:700;font-size:15px;line-height:1.55;color:var(--ink);z-index:30">'
          f'the state of aq:<br>everyone, together</div>')
info_r = (f'<div style="position:absolute;top:160px;right:{M}px;text-align:right;font-family:var(--m);'
          f'font-weight:700;font-size:15px;line-height:1.55;color:var(--ink);z-index:30">'
          f'welfare / climate<br>education / recruit<br>events / shikshaq</div>')
elements.append((M, 160, 220, 80)); elements.append((430, 160, 220, 80))
elements.append((W - M - 220, 160, 220, 80))

word = (f'<div style="position:absolute;top:280px;left:{M}px;right:{M}px;font-family:var(--d);'
        f'font-weight:900;font-size:200px;line-height:.86;letter-spacing:-.02em;'
        f'text-transform:lowercase;color:var(--ink);z-index:20">aqua<br>terra</div>')
elements.append((M, 280, W - 2 * M, 460))

blobs = [
    (S.blob(2, 8), A[3], 40, 720, 480, 0),
    (S.blob(9, 7), A[4], 30, 920, 300, 0),
    (S.blob(6, 9), A[2], 600, 700, 420, 0),
    (S.blob(4, 5), A[5], 480, 1000, 230, 0),
    (S.blob(11, 8), A[1], 860, 790, 190, -8),
]
blob_els = []
for d, f, x, y, sz, r in blobs:
    blob_els.append(at(x, y, sz, sz,
        f'<div style="width:{sz}px;height:{sz}px">{S.sticker(d, f, size=sz, halo=False, sw=8)}</div>',
        z=10, rot=r))

footer = f'<span style="position:absolute;bottom:56px;left:{M}px;font-family:var(--m);font-weight:700;font-size:14px;letter-spacing:.06em;color:var(--ink);z-index:60">@ngo.aquaterra</span>'
elements.append((M, H - 76, 260, 20))

inner = (f'<div style="position:absolute;inset:0;background:{CREAM}"></div>'
         + badge + info_l + info_c + info_r + word + "".join(blob_els) + footer)
html = B.page(W, H, CREAM, inner, grain=True)

color_pairs = [("field", CREAM, CREAM)]
pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs, page_bg=CREAM, core=core,
                   expect_hero=True, auto_nudge=False)

async def main():
    slug = "25d39cb69b3684"
    os.makedirs(f"out/versions/{slug}", exist_ok=True)
    await B.render(html, f"out/versions/{slug}/v4.png", W, H)
    print("done")
asyncio.run(main())
