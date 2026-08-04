"""Proof sheet for engine/shapes.py — renders every parametric silhouette with the uniform
sticker treatment so the looking gate can verify the paths actually draw correctly."""
import asyncio, os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join("engine", n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); S = load("shapes")

W, H = 1080, 1350
A = core.ACCENTS

items = [
    ("scallop",     S.scallop(12),            A[0], S.label("YOU GOT<tspan x='50' dy='16'>THIS!</tspan>", 13, 44)),
    ("arch",        S.arch(),                 A[2], S.label("UPLIFT", 12, 44) + S.label("EACH OTHER", 10, 66)),
    ("wave_banner", S.wave_banner(100, 44, 1.5, 7), A[5], ""),
    ("blob",        S.blob(3, 8),             A[3], ""),
    ("starburst",   S.starburst(11),          A[2], S.label("NEW", 14, 56)),
    ("gear",        S.gear(9),                A[0], ""),
    ("capsule",     S.capsule(100, 40),       A[4], ""),
    ("shield",      S.shield(),               A[6], ""),
    ("tag",         S.tag(100, 44),           A[1], ""),
    ("ring+arctext", S.scallop(20, 44),       A[6], S.text_on_arc("GO TEAM! GO TEAM! ", 30, 11)),
]

cells = []
cols, cw, ch = 3, 320, 300
for i, (name, d, fill, inner) in enumerate(items):
    r, c = divmod(i, cols)
    x, y = 60 + c * cw, 200 + r * ch
    svg = S.sticker(d, fill, size=200, halo=True, shadow=(i % 3 == 0), inner=inner)
    cells.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:200px;height:200px">{svg}</div>')
    cells.append(f'<div style="position:absolute;left:{x}px;top:{y+205}px;width:200px;'
                 f'font-family:var(--m);font-size:15px;color:var(--ink);text-align:center">{name}</div>')

head = ('<div style="position:absolute;top:70px;left:60px;font-family:var(--d);font-weight:900;'
        'font-size:52px;color:var(--ink)">SHAPES PROOF SHEET</div>')
inner = f'<div style="position:absolute;inset:0;background:var(--bg)"></div>{head}' + "".join(cells)
html = B.page(W, H, "var(--bg)", inner, grain=False)

async def main():
    os.makedirs("scratchpad/proof", exist_ok=True)
    await B.render(html, "scratchpad/proof/shapes_sheet.png", W, H)
    print("done")
asyncio.run(main())
