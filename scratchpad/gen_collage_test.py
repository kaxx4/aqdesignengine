import asyncio, base64, os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build")
W, H = core.SIZES["feed"]; M = 48
A = core.ACCENTS
TEAL = A[6]

SRC = "scratchpad/carousel_sunderbans8/src_images"
def photo_b64(fname):
    with open(os.path.join(SRC, fname), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()

def logo_pill(x=M, y=40):
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;z-index:20;background:var(--bg);'
            f'border:3px solid var(--ink);border-radius:999px;padding:7px 14px 7px 10px;'
            f'box-shadow:4px 4px 0 var(--ink);display:flex;align-items:center">'
            f'<img src="{core.LOGO}" style="height:20px;display:block"></div>')

def category_tag(txt, accent, x_right=M, y=48):
    ink = core.text_on(accent)
    return (f'<span style="position:absolute;top:{y}px;right:{x_right}px;z-index:20;font-family:var(--m);'
            f'font-weight:700;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:{ink};'
            f'background:{accent};border:2.5px solid var(--ink);border-radius:999px;padding:6px 14px;'
            f'box-shadow:3px 3px 0 var(--ink)">{txt}</span>')

def footer(loc, date):
    return (f'<div style="position:absolute;bottom:36px;left:{M}px;z-index:20;font-family:var(--m);'
            f'font-weight:700;font-size:12px;letter-spacing:.05em;color:var(--ink)">@ngo.aquaterra'
            f'<span style="color:var(--ink3);font-weight:500;margin-left:12px">{loc} &middot; {date}</span></div>')

def tile(b64, x, y, w, h, rot=0, z=5):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'transform:rotate({rot}deg);border:5px solid var(--ink);box-shadow:6px 6px 0 rgba(10,10,10,.85);'
            f'overflow:hidden;z-index:{z};background:#000">'
            f'<img src="{b64}" style="width:100%;height:100%;object-fit:cover;display:block"></div>')

async def render_collage():
    imgs = {n: photo_b64(f"{n}.png") for n in ["main","img1","img2","img3","img4"]}
    inner = f'<div style="position:absolute;inset:0;background:var(--bg2)"></div>'
    # large hero tile top, three smaller tiles staggered below like snapshots on a desk
    inner += tile(imgs["main"], M, 130, W-2*M, 620, rot=0, z=4)
    tw = (W - 2*M - 2*24) / 3
    ty = 130 + 620 + 28
    th = 430
    inner += tile(imgs["img1"], M, ty, tw, th, rot=-2, z=5)
    inner += tile(imgs["img2"], M+tw+24, ty+14, tw, th, rot=1.5, z=6)
    inner += tile(imgs["img3"], M+2*(tw+24), ty, tw, th, rot=-1, z=5)
    inner += logo_pill()
    inner += category_tag("OUTREACH", TEAL)
    inner += footer("Sunderbans", "DEC 2025")
    html = B.page(W, H, "var(--bg2)", inner, grain=False)
    os.makedirs("out/versions/format_test", exist_ok=True)
    await B.render(html, "out/versions/format_test/collage_demo.png", W, H)

asyncio.run(render_collage())
print("done")
