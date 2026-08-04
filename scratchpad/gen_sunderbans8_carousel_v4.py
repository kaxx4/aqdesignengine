import asyncio, base64, os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles")
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
            f'background:linear-gradient(to top,rgba(0,0,0,.72),rgba(0,0,0,0));z-index:10"></div>')

def full_bleed_photo(b64):
    return f'<img src="{b64}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1">'

def filler(kind, x, y, size, fill, rot=0, opacity=0.92, z=8):
    fn = getattr(dd, kind)
    try: inner = fn(fill=fill, rot=rot, style="clean")
    except TypeError: inner = fn(rot=rot, style="clean")
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;'
            f'opacity:{opacity};z-index:{z}">{inner}</div>')

def caption(txt):
    # small, quiet, grounded — a tick mark (not a caption bar) so it reads as an annotation, not a headline
    return (f'<div style="position:absolute;bottom:100px;left:{M}px;right:{M}px;z-index:20;'
            f'display:flex;align-items:flex-start;gap:12px">'
            f'<span style="width:18px;height:3px;background:{TEAL};margin-top:11px;flex:none"></span>'
            f'<span style="font-family:var(--e);font-weight:500;font-size:19px;line-height:1.35;'
            f'color:rgba(255,255,255,.94);text-shadow:0 2px 6px rgba(0,0,0,.45);max-width:820px">{txt}</span></div>')

async def render_cover():
    photo = full_bleed_photo(photo_b64("main.png"))
    top_scrim = ('<div style="position:absolute;top:0;left:0;right:0;height:340px;'
                 'background:linear-gradient(to bottom,rgba(0,0,0,.55),rgba(0,0,0,0));z-index:9"></div>')
    bottom_scrim = scrim_bottom(500)
    eyebrow = (f'<div style="position:absolute;top:120px;left:{M}px;z-index:20;font-family:var(--m);'
               f'font-weight:700;font-size:15px;letter-spacing:.16em;text-transform:uppercase;color:{TEAL};'
               f'display:flex;align-items:center;gap:10px;text-shadow:0 2px 6px rgba(0,0,0,.5)">'
               f'<span style="width:10px;height:10px;border-radius:50%;background:{TEAL}"></span>SUNDARBANS &middot; DEC 2025</div>')
    headline = (f'<div style="position:absolute;bottom:230px;left:{M}px;right:{M}px;z-index:20;'
                f'font-family:var(--d);font-weight:900;font-size:84px;line-height:.92;text-transform:uppercase;'
                f'color:#FFFFFF;text-shadow:0 4px 14px rgba(0,0,0,.55)">SUNDERBANS<br>8.0</div>')
    subhead = (f'<div style="position:absolute;bottom:150px;left:{M}px;right:{M}px;z-index:20;'
               f'display:flex;align-items:flex-start;gap:12px">'
               f'<span style="width:18px;height:3px;background:{TEAL};margin-top:11px;flex:none"></span>'
               f'<span style="font-family:var(--e);font-weight:500;font-size:20px;line-height:1.35;'
               f'color:rgba(255,255,255,.94);text-shadow:0 2px 6px rgba(0,0,0,.45);max-width:820px">'
               f'volunteers and doctors ran a day of free checkups for the village</span></div>')
    # negative space: open sky top-right, clear of the eyebrow/logo and the sign structure
    fillers = (filler("sparkle", 890, 140, 52, "#FFFFFF", rot=-8) +
               filler("circle", 970, 250, 24, TEAL) +
               filler("star", 800, 320, 36, A[2], rot=10) +
               filler("plus", 990, 370, 26, A[0], rot=-12))
    inner = photo + top_scrim + bottom_scrim + logo_pill() + eyebrow + headline + subhead + fillers + footer("Sunderbans", "DEC 2025")
    html = B.page(W, H, "var(--bg)", inner, grain=False)
    os.makedirs("out/versions/sunderbans8_carousel_v4", exist_ok=True)
    await B.render(html, "out/versions/sunderbans8_carousel_v4/1_cover.png", W, H)

async def render_slide(fname, page_index, total, out_name, cap, fillers=""):
    inner = full_bleed_photo(photo_b64(fname))
    # only pull the scrim in when a caption needs it — a caption-free slide should breathe as pure photo
    inner += scrim_bottom(280 if cap else 170)
    inner += logo_pill()
    inner += dots(total, page_index)
    inner += fillers
    if cap:
        inner += caption(cap)
    inner += footer("Sunderbans", "DEC 2025")
    html = B.page(W, H, "var(--bg)", inner, grain=False)
    os.makedirs("out/versions/sunderbans8_carousel_v4", exist_ok=True)
    await B.render(html, f"out/versions/sunderbans8_carousel_v4/{out_name}.png", W, H)

async def main():
    await render_cover()
    # not every slide needs a line — only where it adds something the photo alone doesn't say.
    # the group-of-kids and the smiling-man photos speak for themselves; skip captions there.
    slides = [
        # img1: open blue sky upper-right, clear of the dots row and the woman/boys below
        ("img1.png", None,
         filler("star", 850, 250, 46, TEAL, rot=12) +
         filler("circle", 950, 410, 28, A[0]) +
         filler("plus", 740, 170, 24, A[2], rot=-10) +
         filler("sparkle", 940, 550, 34, A[5], rot=15)),
        # img2: weathered teal wall, empty upper-right above her shoulder
        ("img2.png", "logging patient details by hand, one form at a time",
         filler("plus", 900, 210, 38, A[2], rot=-15) +
         filler("ring", 770, 370, 42, A[3]) +
         filler("circle", 980, 470, 22, A[5])),
        # img3: bright window light upper-right, above the kids
        ("img3.png", "a drawing break while the queue moves",
         filler("circle", 870, 170, 32, A[2]) +
         filler("star", 960, 330, 26, A[4], rot=8) +
         filler("plus", 900, 460, 20, A[0], rot=20)),
        # img4: dark corrugated roof/rafters, wide open top band
        ("img4.png", None,
         filler("ring", 130, 190, 48, "#F4EFE0") +
         filler("plus", 400, 110, 28, A[4], rot=-8) +
         filler("circle", 600, 270, 24, A[0]) +
         filler("star", 850, 340, 30, A[2], rot=14)),
    ]
    total = len(slides) + 1
    for i, (fname, cap, fill) in enumerate(slides, start=1):
        await render_slide(fname, i, total, f"{i+1}_slide", cap, fillers=fill)
    print("done: 5-slide carousel, captions only where they earn their place")

asyncio.run(main())
