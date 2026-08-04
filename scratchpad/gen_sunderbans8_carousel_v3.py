import asyncio, base64, os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build")
W, H = core.SIZES["feed"]; M = 64
A = core.ACCENTS
TEAL = A[6]

SRC = "scratchpad/carousel_sunderbans8/src_images"
def photo_b64(fname):
    with open(os.path.join(SRC, fname), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()

def logo_pill(x=M, y=48):
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;z-index:20;background:var(--bg);'
            f'border:3px solid var(--ink);border-radius:999px;padding:8px 16px 8px 12px;'
            f'box-shadow:4px 4px 0 var(--ink);display:flex;align-items:center">'
            f'<img src="{core.LOGO}" style="height:22px;display:block"></div>')

def category_tag(txt, accent=TEAL, x_right=M, y=58):
    ink = core.text_on(accent)
    return (f'<span style="position:absolute;top:{y}px;right:{x_right}px;z-index:20;font-family:var(--m);'
            f'font-weight:700;font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:{ink};'
            f'background:{accent};border:2.5px solid var(--ink);border-radius:999px;padding:7px 16px;'
            f'box-shadow:3px 3px 0 var(--ink)">{txt}</span>')

def dots(n, active, x_right=M, y=112):
    out = f'<div style="position:absolute;top:{y}px;right:{x_right}px;z-index:20;display:flex;gap:8px">'
    for i in range(n):
        c = "#FFFFFF" if i == active else "rgba(255,255,255,.35)"
        b = "border:2px solid var(--ink);" if i == active else ""
        out += f'<span style="width:9px;height:9px;border-radius:50%;background:{c};{b}"></span>'
    return out + "</div>"

def footer(loc, date):
    return (f'<div style="position:absolute;bottom:52px;left:{M}px;z-index:20;font-family:var(--m);'
            f'font-weight:700;font-size:13px;letter-spacing:.06em;color:#FFFFFF;text-shadow:0 2px 6px rgba(0,0,0,.5)">'
            f'@ngo.aquaterra <span style="opacity:.75;font-weight:500">&middot; {loc} &middot; {date}</span></div>')

def scrim_bottom(h=260):
    return (f'<div style="position:absolute;bottom:0;left:0;right:0;height:{h}px;'
            f'background:linear-gradient(to top,rgba(0,0,0,.68),rgba(0,0,0,0));z-index:10"></div>')

def full_bleed_photo(b64):
    return f'<img src="{b64}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1">'

async def render_slide(fname, page_index, total, out_name, category_slide=False):
    inner = full_bleed_photo(photo_b64(fname))
    inner += scrim_bottom(260)
    inner += logo_pill()
    if category_slide:
        inner += category_tag("OUTREACH")
    else:
        inner += dots(total, page_index)
    inner += footer("Sunderbans", "DEC 2025")
    html = B.page(W, H, "var(--bg)", inner, grain=False)
    os.makedirs("out/versions/sunderbans8_carousel_v3", exist_ok=True)
    await B.render(html, f"out/versions/sunderbans8_carousel_v3/{out_name}.png", W, H)

async def main():
    slides = ["main.png", "img1.png", "img2.png", "img3.png", "img4.png"]
    total = len(slides)
    for i, fname in enumerate(slides):
        await render_slide(fname, i, total, f"{i+1}_slide", category_slide=(i == 0))
    print("done: 5-slide carousel, no captions, no stats")

asyncio.run(main())
