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
    return (f'<img src="{core.LOGO}" style="position:absolute;top:{y}px;left:{x}px;z-index:20;'
            f'height:56px;display:block;filter:drop-shadow(0 2px 6px rgba(0,0,0,.5))">')

# dots now pick up the slide's own rotating accent on the active dot — a small thread
# tying the one recurring UI element to each slide's color instead of always plain white
def dots(n, active, accent="#FFFFFF", x_right=M, y=112):
    out = f'<div style="position:absolute;top:{y}px;right:{x_right}px;z-index:20;display:flex;gap:8px">'
    for i in range(n):
        c = accent if i == active else "rgba(255,255,255,.35)"
        b = "border:2px solid var(--ink);" if i == active else ""
        out += f'<span style="width:9px;height:9px;border-radius:50%;background:{c};{b}"></span>'
    return out + "</div>"

def footer(loc, date):
    return (f'<div style="position:absolute;bottom:52px;left:{M}px;z-index:20;font-family:var(--m);'
            f'font-weight:700;font-size:13px;letter-spacing:.06em;color:#FFFFFF;text-shadow:0 2px 6px rgba(0,0,0,.5)">'
            f'@ngo.aquaterra <span style="opacity:.75;font-weight:500">&middot; {loc} &middot; {date}</span></div>')

# scrim now takes an optional accent tint — a faint colored wash under the black,
# so the gradient itself carries that slide's color instead of always reading as flat black
def scrim_bottom(h=260, tint=None):
    layers = 'linear-gradient(to top,rgba(0,0,0,.72),rgba(0,0,0,0))'
    if tint: layers = f'linear-gradient(to top,{tint}4D,transparent 65%), ' + layers
    return f'<div style="position:absolute;bottom:0;left:0;right:0;height:{h}px;background:{layers};z-index:10"></div>'

def scrim_top(h=340, tint=None):
    layers = 'linear-gradient(to bottom,rgba(0,0,0,.55),rgba(0,0,0,0))'
    if tint: layers = f'linear-gradient(to bottom,{tint}40,transparent 65%), ' + layers
    return f'<div style="position:absolute;top:0;left:0;right:0;height:{h}px;background:{layers};z-index:9"></div>'

def full_bleed_photo(b64):
    return f'<img src="{b64}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1">'

# thick ink outline framing the whole slide — the brand's craft-layer rule, previously
# absent on this carousel (full-bleed photos had zero outline treatment)
def frame_border(width=10):
    return (f'<div style="position:absolute;inset:0;border:{width}px solid var(--ink);'
            f'z-index:25;pointer-events:none;box-sizing:border-box"></div>')

def caption(txt):
    return (f'<div style="position:absolute;bottom:100px;left:{M}px;right:{M}px;z-index:20;'
            f'display:flex;align-items:flex-start;gap:12px">'
            f'<span style="width:18px;height:3px;background:{TEAL};margin-top:11px;flex:none"></span>'
            f'<span style="font-family:var(--e);font-weight:500;font-size:19px;line-height:1.35;'
            f'color:rgba(255,255,255,.94);text-shadow:0 2px 6px rgba(0,0,0,.45);max-width:820px">{txt}</span></div>')

def sticker(txt, accent, x, y, rot=-4):
    ink = core.text_on(accent)
    return (f'<span style="position:absolute;left:{x}px;top:{y}px;z-index:9;transform:rotate({rot}deg);'
            f'font-family:var(--m);font-weight:700;font-size:13px;letter-spacing:.08em;text-transform:uppercase;'
            f'color:{ink};background:{accent};border:2.5px solid var(--ink);border-radius:999px;'
            f'padding:6px 14px;box-shadow:3px 3px 0 var(--ink);white-space:nowrap">{txt}</span>')

# small truthful index tag — real carousel position (never a fabricated stat), sits in the
# always-dark scrim band so it never risks landing on a face
def index_tag(page_index, total, accent):
    txt = f"{page_index:02d} / {total:02d}"
    ink = core.text_on(accent)
    return (f'<span style="position:absolute;bottom:140px;right:{M}px;z-index:20;font-family:var(--m);'
            f'font-weight:700;font-size:12px;letter-spacing:.08em;color:{ink};background:{accent};'
            f'border:2px solid var(--ink);border-radius:999px;padding:5px 12px;'
            f'box-shadow:2px 2px 0 var(--ink)">{txt}</span>')

def one(kind, x, y, size, fill, rot=0, opacity=0.94, z=8):
    fn = getattr(dd, kind)
    try: inner = fn(fill=fill, rot=rot, style="clean")
    except TypeError: inner = fn(rot=rot, style="clean")
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;'
            f'opacity:{opacity};z-index:{z}">{inner}</div>')

# a dashed connector between two doodles in the same free zone — reads as a composed
# constellation instead of scattered icons, drawn behind the doodles/text (z=7)
def connector(x1, y1, x2, y2, color, opacity=0.5):
    cx1, cy1 = x1 + 15, y1 + 15
    cx2, cy2 = x2 + 15, y2 + 15
    return (f'<svg style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;z-index:7;pointer-events:none">'
            f'<line x1="{cx1}" y1="{cy1}" x2="{cx2}" y2="{cy2}" stroke="{color}" stroke-width="2.5" '
            f'stroke-dasharray="2 8" stroke-linecap="round" opacity="{opacity}"/></svg>')

VOCAB = ["star","sparkle","circle","ring","plus","zigzag","burst","lightning",
         "spiral","dots","speech","cross","squiggle","leaf","thumbsup","heart"]
ACCENT_ORDER = [4,0,2,5,3,1,6]  # sky,pink,lemon,grape,tomato,mint,teal
SIZES = [26,34,44,60,80]

def slide_accent(seed):
    return A[ACCENT_ORDER[seed % len(ACCENT_ORDER)]]

def filler_set(spots, slide_seed, count=None):
    if count is None: count = len(spots)
    html = ""
    for i in range(count):
        x, y = spots[i]
        kind = VOCAB[(slide_seed * 3 + i * 5) % len(VOCAB)]
        accent = A[ACCENT_ORDER[(slide_seed + i) % len(ACCENT_ORDER)]]
        size = SIZES[(slide_seed + i * 2) % len(SIZES)]
        rot = ((slide_seed * 37 + i * 53) % 60) - 30
        fillcolor = "#FFFFFF" if kind == "ring" else accent
        html += one(kind, x, y, size, fillcolor, rot=rot)
    # thread the first two spots together with a dashed line in this slide's accent —
    # purely decorative, lives inside the same zone already proven clear of faces
    if len(spots) >= 2:
        html += connector(spots[0][0], spots[0][1], spots[1][0], spots[1][1], slide_accent(slide_seed))
    return html

async def render_cover():
    accent = TEAL
    photo = full_bleed_photo(photo_b64("main.png"))
    top_scrim = scrim_top(340, tint=accent)
    bottom_scrim = scrim_bottom(500, tint=accent)
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
    fillers = filler_set([(880,130),(970,235),(795,300),(1000,375),(870,440)], slide_seed=0)
    stickers = sticker("the full squad", A[2], 850, 555, rot=-6)
    inner = (photo + top_scrim + bottom_scrim + logo_pill() + eyebrow + headline + subhead
             + fillers + stickers + footer("Sunderbans", "DEC 2025"))
    html = B.page(W, H, "var(--bg)", inner, grain=False)
    os.makedirs("out/versions/sunderbans8_carousel_v6", exist_ok=True)
    await B.render(html, "out/versions/sunderbans8_carousel_v6/1_cover.png", W, H)

async def render_slide(fname, page_index, total, out_name, cap, spots, slide_seed,
                        sticker_txt=None, sticker_pos=None, sticker_accent_idx=1):
    accent = slide_accent(slide_seed)
    inner = full_bleed_photo(photo_b64(fname))
    inner += scrim_bottom(280 if cap else 170, tint=accent)
    inner += logo_pill()
    inner += dots(total, page_index, accent=accent)
    inner += filler_set(spots, slide_seed)
    if sticker_txt:
        sx, sy = sticker_pos
        inner += sticker(sticker_txt, A[sticker_accent_idx], sx, sy)
    inner += index_tag(page_index, total, accent)
    if cap:
        inner += caption(cap)
    inner += footer("Sunderbans", "DEC 2025")
    html = B.page(W, H, "var(--bg)", inner, grain=False)
    os.makedirs("out/versions/sunderbans8_carousel_v6", exist_ok=True)
    await B.render(html, f"out/versions/sunderbans8_carousel_v6/{out_name}.png", W, H)

async def main():
    await render_cover()
    slides = [
        dict(fname="img1.png", cap=None,
             spots=[(840,220),(945,150),(730,175),(970,430),(880,560),(1010,300)],
             slide_seed=1, sticker_txt="free checkup", sticker_pos=(64,1180), sticker_accent_idx=6),
        dict(fname="img2.png", cap="logging patient details by hand, one form at a time",
             spots=[(890,190),(760,350),(970,450),(830,270),(1000,140)],
             slide_seed=2, sticker_txt="form by form", sticker_pos=(820,600), sticker_accent_idx=0),
        dict(fname="img3.png", cap="a drawing break while the queue moves",
             spots=[(860,150),(955,300),(890,430),(760,220),(1020,410)],
             slide_seed=3, sticker_txt="crayons in the queue", sticker_pos=(860,210), sticker_accent_idx=2),
        dict(fname="img4.png", cap=None,
             spots=[(120,170),(390,100),(590,250),(830,320),(970,150),(240,320)],
             slide_seed=4, sticker_txt="next in line", sticker_pos=(120,420), sticker_accent_idx=5),
    ]
    total = len(slides) + 1
    for i, s in enumerate(slides, start=1):
        await render_slide(s["fname"], i, total, f"{i+1}_slide", s["cap"], s["spots"], s["slide_seed"],
                            s["sticker_txt"], s["sticker_pos"], s["sticker_accent_idx"])
    print("done: v6 — ink frame, tinted scrims, accent-matched dots, connector lines, truthful index tags")

asyncio.run(main())
