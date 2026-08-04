import asyncio, base64, os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")
W, H = core.SIZES["feed"]; M = 64
A = core.ACCENTS  # pink,mint,lemon,tomato,sky,grape,teal
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

def dots(n, active, x_right=M):
    out = f'<div style="position:absolute;top:58px;right:{x_right}px;z-index:20;display:flex;gap:8px">'
    for i in range(n):
        c = "#FFFFFF" if i == active else "rgba(255,255,255,.35)"
        b = "border:2px solid var(--ink);" if i == active else ""
        out += f'<span style="width:9px;height:9px;border-radius:50%;background:{c};{b}"></span>'
    return out + "</div>"

def footer(txt="@ngo.aquaterra", dark=True):
    c = "#FFFFFF" if dark else "var(--ink)"
    sh = "text-shadow:0 2px 6px rgba(0,0,0,.5);" if dark else ""
    return (f'<span style="position:absolute;bottom:52px;left:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:13px;letter-spacing:.06em;color:{c};z-index:20;{sh}">{txt}</span>')

def scrim(pos="bottom", h=520):
    grad = "to top" if pos == "bottom" else "to bottom"
    side = f"bottom:0" if pos == "bottom" else "top:0"
    return (f'<div style="position:absolute;{side};left:0;right:0;height:{h}px;'
            f'background:linear-gradient(to {"top" if pos=="bottom" else "bottom"},rgba(0,0,0,.75),rgba(0,0,0,0));z-index:10"></div>')

def full_bleed_photo(b64):
    return f'<img src="{b64}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1">'

async def render_slide(inner_extra, out_name, page_index, total, caption=None, caption_align="left"):
    parts = []
    parts.append(inner_extra["photo"])
    parts.append(scrim("bottom", 480))
    parts.append(logo_pill())
    parts.append(dots(total, page_index))
    if caption:
        align_css = "left" if caption_align == "left" else "right"
        parts.append(
            f'<div style="position:absolute;bottom:118px;left:{M}px;right:{M}px;z-index:20;'
            f'font-family:var(--s);font-style:italic;font-size:36px;line-height:1.15;color:#FFFFFF;'
            f'text-shadow:0 2px 10px rgba(0,0,0,.55)">{caption}</div>'
        )
    parts.append(footer())
    inner = "".join(parts)
    html = B.page(W, H, "var(--bg)", inner, grain=False)
    os.makedirs("out/versions/sunderbans8_carousel", exist_ok=True)
    await B.render(html, f"out/versions/sunderbans8_carousel/{out_name}.png", W, H)

async def render_cover():
    photo = full_bleed_photo(photo_b64("main.png"))
    top_scrim = ('<div style="position:absolute;top:0;left:0;right:0;height:340px;'
                 'background:linear-gradient(to bottom,rgba(0,0,0,.55),rgba(0,0,0,0));z-index:9"></div>')
    bottom_scrim = scrim("bottom", 620)
    eyebrow = (f'<div style="position:absolute;top:120px;left:{M}px;z-index:20;font-family:var(--m);'
               f'font-weight:700;font-size:15px;letter-spacing:.16em;text-transform:uppercase;color:{TEAL};'
               f'display:flex;align-items:center;gap:10px;text-shadow:0 2px 6px rgba(0,0,0,.5)">'
               f'<span style="width:10px;height:10px;border-radius:50%;background:{TEAL}"></span>SUNDARBANS &middot; DEC 2025</div>')
    headline = (f'<div style="position:absolute;bottom:210px;left:{M}px;right:{M}px;z-index:20;'
                f'font-family:var(--d);font-weight:900;font-size:88px;line-height:.92;text-transform:uppercase;'
                f'color:#FFFFFF;text-shadow:0 4px 14px rgba(0,0,0,.55)">SUNDERBANS<br>8.0</div>')
    stat_chip = (f'<span style="position:absolute;bottom:150px;left:{M}px;z-index:20;background:{TEAL};color:#fff;'
                 f'font-family:var(--e);font-weight:600;font-size:19px;padding:9px 18px;border-radius:999px;'
                 f'border:3px solid var(--ink);box-shadow:4px 4px 0 var(--ink)">120+ checkups &middot; a day of care</span>')
    inner = photo + top_scrim + bottom_scrim + logo_pill() + eyebrow + headline + stat_chip + footer()
    html = B.page(W, H, "var(--bg)", inner, grain=False)
    os.makedirs("out/versions/sunderbans8_carousel", exist_ok=True)
    await B.render(html, "out/versions/sunderbans8_carousel/1_cover.png", W, H)

async def main():
    await render_cover()
    slides = [
        ("img1.png", "Smiles powered by service"),
        ("img2.png", "Gratitude that says everything"),
        ("img3.png", "Learning nurtured with care"),
        ("img4.png", "Small moments, lasting impact"),
    ]
    total = len(slides) + 1
    for i, (fname, cap) in enumerate(slides, start=1):
        await render_slide({"photo": full_bleed_photo(photo_b64(fname))},
                            f"{i+1}_gallery{i}", i, total, caption=cap)
    print("done: 5 slides in out/versions/sunderbans8_carousel/")

asyncio.run(main())
