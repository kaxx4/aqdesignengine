"""RECREATION — 17c7de5509caae, iteration 3. Grid starts higher (fixes row-1 under-fill) and
three tiles get ONE small restrained sticker each (fixes DETAIL TOO LOW without dot-pattern
clutter — the lesson from 11e7d9a3ff6761 earlier this session: cheap texture that makes flat
fields look busy is worse than accepting a lower detail score)."""
import asyncio, os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join("engine", n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); sh = load("shapes"); dd = load("doodles"); lay = load("layout")

W, H = core.SIZES["feed"]; M = 64
A = core.ACCENTS
CREAM = "var(--bg)"

def at(x, y, w, h, inner, z=6, rot=0):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'z-index:{z};transform:rotate({rot}deg)">{inner}</div>')

def logo():
    return f'<img src="{core.LOGO}" style="position:absolute;top:52px;left:{M}px;height:40px;z-index:60">'

def footer():
    return (f'<span style="position:absolute;bottom:52px;left:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:14px;letter-spacing:.06em;color:var(--ink);z-index:60">@ngo.aquaterra</span>')

def eyebrow(txt, color="var(--ink)"):
    return (f'<span style="position:absolute;top:64px;right:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:14px;letter-spacing:.14em;text-transform:uppercase;color:{color};z-index:60">{txt}</span>')

def mono(txt, size=13, color="var(--ink)", ls=".1em"):
    return f'<span style="font-family:var(--m);font-weight:700;font-size:{size}px;letter-spacing:{ls};color:{color}">{txt}</span>'

els = []
def E(label, x, y, w, h): els.append((label, x, y, w, h))

# grid raised from y=150 to y=64 -- closes the row-1 under-fill compare.py flagged
GY = 118   # leaves a real header band; logo/eyebrow now tracked below
tiles = [
    (0, GY, 360, 300, A[0], "SHOW UP", "d", 54, "#FFF"),
    (360, GY, 360, 300, "#0A0A0A", "show up", "s", 62, A[2]),
    (720, GY, 360, 300, A[4], "SHOW<br>UP", "d", 48, "#0A0A0A"),
    (0, GY + 300, 540, 280, A[2], "show up", "e", 56, "#0A0A0A"),
    (540, GY + 300, 540, 280, A[5], "SHOW UP", "m", 34, "#FFF"),
    (0, GY + 580, 360, 300, A[6], "SHOW<br>UP", "d", 50, "#FFF"),
    (360, GY + 580, 720, 300, A[3], "show up.", "s", 74, "#FFF"),
]
fam = {"d": "var(--d)", "s": "var(--s)", "e": "var(--e)", "m": "var(--m)"}
# one small restrained sticker on 3 of the 7 tiles -- real, richer silhouettes, not a texture wash
STICKERS = {0: ("star", A[2], 46, 300, 60), 4: ("heart", A[0], 40, 960, 570), 6: ("sparkle", "#FFFFFF", 44, 1000, 900)}
els_html = ""
for i, (x, y, w, h, bg, txt, f, fs, fg) in enumerate(tiles):
    ital = "font-style:italic;" if f == "s" else ""
    els_html += at(x, y, w, h,
        f'<div style="width:100%;height:100%;background:{bg};display:flex;align-items:center;'
        f'justify-content:center;border:2px solid rgba(10,10,10,.35);box-sizing:border-box">'
        f'<div style="font-family:{fam[f]};{ital}font-weight:900;font-size:{fs}px;line-height:.92;'
        f'color:{fg};text-align:center;letter-spacing:{".08em" if f=="m" else "0"}">{txt}</div></div>', z=10)
    E(f"tile{i}", x, y, w, h)
    els_html += at(x + 12, y + 12, 46, 30,
        f'<div style="width:100%;height:100%;background:{CREAM};border:2px solid #0A0A0A;'
        f'display:flex;align-items:center;justify-content:center">{mono(f"{i+1:02d}", 12)}</div>', z=20)
    if i in STICKERS:
        kind, col, sz, sx, sy = STICKERS[i]
        els_html += at(sx, sy, sz, sz, dd.stamp(kind, col, rot=8), z=25)
        E(f"sticker{i}", sx, sy, sz, sz)

SY = GY + 880
strip = (f'<div style="position:absolute;top:{SY}px;left:0;right:0;height:120px;background:#0A0A0A;'
         f'display:flex;align-items:center;justify-content:space-between;padding:0 {M}px;z-index:22">'
         + mono("SEVEN WAYS", 20, "#FFF") + mono("ONE ASK", 20, A[2])
         + mono("AQUATERRA", 20, "#FFF") + "</div>")
E("strip", 0, SY, W, 120)

E("logo", M, 52, 240, 40)
E("eyebrow", 780, 64, 260, 20)
inner = (f'<div style="position:absolute;inset:0;background:{CREAM}"></div>'
         + els_html + strip + logo() + footer() + eyebrow("AQ &middot; TYPE STUDY"))
html = B.page(W, H, CREAM, inner, grain=True)
pf = lay.preflight(W, H, els, html=html, page_bg=CREAM, core=core,
                    collision_ignore={frozenset({"tile4", "sticker4"}), frozenset({"tile6", "sticker6"}),
                                      frozenset({"tile0", "sticker0"})})

async def main():
    out = "out/versions/17c7de5509caae/v3.png"
    await B.render(html, out, W, H)
    print("wrote", out, "| clean =", pf.get("clean"))
asyncio.run(main())
