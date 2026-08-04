import asyncio, base64, os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")
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

def scrim_bottom(h=520):
    return (f'<div style="position:absolute;bottom:0;left:0;right:0;height:{h}px;'
            f'background:linear-gradient(to top,rgba(0,0,0,.78),rgba(0,0,0,0));z-index:10"></div>')

def full_bleed_photo(b64):
    return f'<img src="{b64}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1">'

def micro_stat_tag(txt, top=48):
    # small mono stat tag, top-right, sits ABOVE the dots row on gallery slides -> place opposite side
    return (f'<span style="position:absolute;top:{top}px;left:{M}px;z-index:20;font-family:var(--m);'
            f'font-weight:700;font-size:13px;letter-spacing:.08em;color:{TEAL};background:rgba(10,10,10,.55);'
            f'border:1.5px solid {TEAL};border-radius:999px;padding:5px 12px;text-shadow:none">{txt}</span>')

async def render_cover_v2():
    photo = full_bleed_photo(photo_b64("main.png"))
    top_scrim = ('<div style="position:absolute;top:0;left:0;right:0;height:360px;'
                 'background:linear-gradient(to bottom,rgba(0,0,0,.6),rgba(0,0,0,0));z-index:9"></div>')
    bottom_scrim = scrim_bottom(700)
    eyebrow = (f'<div style="position:absolute;top:120px;left:{M}px;z-index:20;font-family:var(--m);'
               f'font-weight:700;font-size:15px;letter-spacing:.16em;text-transform:uppercase;color:{TEAL};'
               f'display:flex;align-items:center;gap:10px;text-shadow:0 2px 6px rgba(0,0,0,.5)">'
               f'<span style="width:10px;height:10px;border-radius:50%;background:{TEAL}"></span>SUNDARBANS &middot; DEC 2025</div>')
    headline = (f'<div style="position:absolute;bottom:150px;left:{M}px;right:{M}px;z-index:20;'
                f'font-family:var(--d);font-weight:900;font-size:88px;line-height:.92;text-transform:uppercase;'
                f'color:#FFFFFF;text-shadow:0 4px 14px rgba(0,0,0,.55)">SUNDERBANS<br>8.0</div>')
    inner = photo + top_scrim + bottom_scrim + logo_pill() + eyebrow + headline + footer()
    html = B.page(W, H, "var(--bg)", inner, grain=False)
    os.makedirs("out/versions/sunderbans8_carousel_v2", exist_ok=True)
    await B.render(html, "out/versions/sunderbans8_carousel_v2/1_cover.png", W, H)

async def render_gallery_v2(fname, out_name, page_index, total, caption, stat_tag):
    # pure photo — no caption, no stat tag. logo, progress dots, handle only.
    inner = full_bleed_photo(photo_b64(fname)) + scrim_bottom(260) + logo_pill() + dots(total, page_index)
    inner += footer()
    html = B.page(W, H, "var(--bg)", inner, grain=False)
    os.makedirs("out/versions/sunderbans8_carousel_v2", exist_ok=True)
    await B.render(html, f"out/versions/sunderbans8_carousel_v2/{out_name}.png", W, H)

async def render_impact_card():
    # closing plate: numbers as the sole visual subject, engraved-plate craft treatment
    bg = "#0D2E2B"
    def big_stat(num, label, accent, y):
        return (f'<div style="position:absolute;top:{y}px;left:{M}px;right:{M}px;z-index:20;'
                f'display:flex;align-items:baseline;gap:22px;border-bottom:2px solid rgba(244,239,224,.18);padding-bottom:26px">'
                f'<span style="font-family:var(--d);font-weight:900;font-size:96px;line-height:1;color:{accent}">{num}</span>'
                f'<span style="font-family:var(--e);font-weight:600;font-size:24px;color:var(--bg)">{label}</span></div>')
    # faint tide-line echo tying this card back to the companion piece's texture
    tide = "".join(
        f'<path d="M0,{y} Q270,{y-14} 540,{y} T1080,{y}" fill="none" stroke="{TEAL}" stroke-width="1.2" opacity="0.14"/>'
        for y in (330, 560, 790, 1020, 1180)
    )
    inner = f'<div style="position:absolute;inset:0;background:{bg}"></div>'
    inner += f'<svg width="{W}" height="{H}" style="position:absolute;inset:0;z-index:2">{tide}</svg>'
    inner += logo_pill()
    inner += (f'<div style="position:absolute;top:150px;left:{M}px;z-index:20;font-family:var(--m);'
              f'font-weight:700;font-size:14px;letter-spacing:.14em;text-transform:uppercase;color:{TEAL}">'
              f'the day, by the numbers</div>')
    inner += big_stat("120+", "medical checkups conducted", TEAL, 250)
    inner += big_stat("&#8377;25K+", "in medicine &amp; supplies donated", A[2], 405)
    inner += big_stat("15", "AquaTerra volunteers on ground", A[4], 560)
    inner += big_stat("4", "doctors who gave their day", A[0], 715)
    inner += (f'<div style="position:absolute;top:900px;left:{M}px;right:{M}px;z-index:20;'
              f'font-family:var(--s);font-style:italic;font-size:32px;color:var(--bg);opacity:.9">'
              f'not just numbers &mdash; a village that got seen.</div>')
    inner += (f'<div style="position:absolute;top:980px;left:{M}px;z-index:20;width:120px;height:3px;'
              f'background:{TEAL};opacity:.5"></div>')
    inner += footer()
    html = B.page(W, H, bg, inner, grain=True)
    os.makedirs("out/versions/sunderbans8_carousel_v2", exist_ok=True)
    await B.render(html, "out/versions/sunderbans8_carousel_v2/6_impact.png", W, H)

async def main():
    await render_cover_v2()
    slides = [
        ("img1.png", "Smiles powered by service", None),
        ("img2.png", "Gratitude that says everything", None),
        ("img3.png", "Learning nurtured with care", None),
        ("img4.png", "Small moments, lasting impact", None),
    ]
    total = len(slides) + 1
    for i, (fname, cap, tag) in enumerate(slides, start=1):
        await render_gallery_v2(fname, f"{i+1}_gallery{i}", i, total, cap, tag)
    await render_impact_card()
    print("done: v2 slides in out/versions/sunderbans8_carousel_v2/")

asyncio.run(main())
