import asyncio, os, sys, importlib.util
ROOT = "/home/user/aqdesignengine"
os.chdir(ROOT)
ENGINE_DIR = os.path.join(ROOT, "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout"); shp = load("shapes")

W, H = core.SIZES["feed"]
M = 64
A = core.ACCENTS  # pink,mint,lemon,tomato,sky,grape,teal

def rakhi_motif(cx, cy, size, accent, z=8, rot=0):
    """A rakhi medallion: starburst badge + center ring + two hanging tassel threads."""
    r = size/2
    d_star = shp.starburst(points=10, R=48, r=30)
    d_ring = shp.starburst(points=1,R=1,r=1) # unused placeholder
    tassel_len = size*0.42
    svg = f'''<svg viewBox="0 0 100 140" width="{size}" height="{size*1.4:.0f}" style="transform:rotate({rot}deg)">
      <line x1="50" y1="46" x2="50" y2="{46+tassel_len*0.36:.0f}" stroke="{core.__dict__["ROOT"] and "#0A0A0A"}" stroke-width="4"/>
      <path d="M38 {46+tassel_len*0.32:.0f} Q50 {46+tassel_len*0.55:.0f} 62 {46+tassel_len*0.32:.0f}" fill="none" stroke="#0A0A0A" stroke-width="4"/>
      <circle cx="38" cy="{46+tassel_len*0.55:.0f}" r="5" fill="{accent}" stroke="#0A0A0A" stroke-width="3"/>
      <circle cx="62" cy="{46+tassel_len*0.55:.0f}" r="5" fill="{accent}" stroke="#0A0A0A" stroke-width="3"/>
      <path d="{d_star}" fill="{accent}" stroke="#0A0A0A" stroke-width="6" stroke-linejoin="round" transform="translate(0,0)"/>
      <circle cx="50" cy="50" r="14" fill="#F4EFE0" stroke="#0A0A0A" stroke-width="5"/>
      <circle cx="50" cy="50" r="5" fill="{accent}"/>
    </svg>'''
    return f'<div style="position:absolute;top:{cy-r}px;left:{cx-r}px;width:{size}px;height:{size*1.4:.0f}px;z-index:{z};filter:drop-shadow(6px 6px 0 #0A0A0A)">{svg}</div>'

def wrist_band(cx, cy, w, accent, z=9, rot=0):
    """A tied wrist: forearm capsule + rakhi thread wrap + medallion + tassels."""
    h = w*0.62
    d_arm = shp.capsule(w=100, h=52)
    svg = f'''<svg viewBox="0 0 100 100" width="{w}" height="{h:.0f}" style="transform:rotate({rot}deg)">
      <path d="{d_arm}" fill="#F2C9A0" stroke="#0A0A0A" stroke-width="6" transform="translate(0,24)"/>
      <rect x="34" y="18" width="32" height="60" rx="10" fill="{accent}" stroke="#0A0A0A" stroke-width="5"/>
      <circle cx="50" cy="26" r="15" fill="#FFF6E6" stroke="#0A0A0A" stroke-width="5"/>
      <circle cx="50" cy="26" r="6" fill="{accent}"/>
      <path d="M40 26 Q30 40 34 58" fill="none" stroke="#0A0A0A" stroke-width="4"/>
      <path d="M60 26 Q70 40 66 58" fill="none" stroke="#0A0A0A" stroke-width="4"/>
      <circle cx="34" cy="60" r="4" fill="{accent}" stroke="#0A0A0A" stroke-width="2.5"/>
      <circle cx="66" cy="60" r="4" fill="{accent}" stroke="#0A0A0A" stroke-width="2.5"/>
    </svg>'''
    return f'<div style="position:absolute;top:{cy-h/2:.0f}px;left:{cx-w/2:.0f}px;width:{w}px;height:{h:.0f}px;z-index:{z};filter:drop-shadow(5px 5px 0 #0A0A0A)">{svg}</div>'

def person(cx, cy, size, shirt, z=6, flip=False, arm_up=True):
    """Simple friendly character: head + body + one raised tying arm (arm drawn in the
    body-fill color path, but rendered as its own opaque stroke ON TOP so it always shows —
    the earlier version buried the arm under the head/body paint order)."""
    w = size; h = size*1.35
    fl = " scaleX(-1)" if flip else ""
    arm = (f'<path d="M78 58 Q100 26 112 16" fill="none" stroke="{shirt}" stroke-width="18" stroke-linecap="round"/>'
           f'<path d="M78 58 Q100 26 112 16" fill="none" stroke="#0A0A0A" stroke-width="18" stroke-linecap="round" stroke-dasharray="0" opacity="0"/>'
           f'<circle cx="112" cy="16" r="11" fill="#F2C9A0" stroke="#0A0A0A" stroke-width="5"/>') if arm_up else ""
    svg = f'''<svg viewBox="0 0 130 160" width="{w}" height="{h:.0f}" style="transform:{fl};overflow:visible">
      <path d="M20 158 C20 100 30 70 60 70 C90 70 100 100 100 158 Z" fill="{shirt}" stroke="#0A0A0A" stroke-width="7"/>
      {arm}
      <circle cx="60" cy="42" r="34" fill="#F2C9A0" stroke="#0A0A0A" stroke-width="7"/>
      <circle cx="48" cy="40" r="4" fill="#0A0A0A"/>
      <circle cx="72" cy="40" r="4" fill="#0A0A0A"/>
      <path d="M48 54 Q60 62 72 54" fill="none" stroke="#0A0A0A" stroke-width="4" stroke-linecap="round"/>
      <path d="M28 26 Q60 2 92 26 Q92 10 60 8 Q28 10 28 26 Z" fill="#0A0A0A"/>
    </svg>'''
    return f'<div style="position:absolute;top:{cy-h/2:.0f}px;left:{cx-w/2:.0f}px;width:{w}px;height:{h:.0f}px;z-index:{z};overflow:visible">{svg}</div>'

def headline(txt, y, size, color, z=15, w=None, lh=0.94, align="left"):
    ww = w or (W-2*M)
    ta = "left" if align=="left" else align
    return (f'<div style="position:absolute;top:{y}px;left:{M}px;width:{ww}px;font-family:var(--d);'
            f'font-weight:900;text-transform:uppercase;font-size:{size}px;line-height:{lh};color:{color};'
            f'z-index:{z};text-align:{ta}">{txt}</div>')

def body(txt, y, size, color, z=14, w=None):
    ww = w or (W-2*M)
    return (f'<div style="position:absolute;top:{y}px;left:{M}px;width:{ww}px;font-family:var(--e);'
            f'font-weight:400;font-size:{size}px;line-height:1.35;color:{color};z-index:{z}">{txt}</div>')

def footer(dark=False):
    c = "#FFFFFF" if dark else "var(--ink3)"
    return (f'<span style="position:absolute;bottom:52px;left:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:15px;letter-spacing:.06em;color:{c};z-index:20">@ngo.aquaterra</span>'
            f'<span style="position:absolute;bottom:52px;right:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:13px;letter-spacing:.06em;color:{c};z-index:20">01/04</span>')

def page_no(n, dark=False):
    c = "#FFFFFF" if dark else "var(--ink3)"
    return f'<span style="position:absolute;bottom:52px;right:{M}px;font-family:var(--m);font-weight:700;font-size:13px;letter-spacing:.06em;color:{c};z-index:20">{n}/04</span>'

def eyebrow(txt, color, y=64):
    return (f'<div style="position:absolute;top:{y}px;left:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:16px;letter-spacing:.14em;text-transform:uppercase;color:{color};z-index:20;'
            f'display:flex;align-items:center;gap:10px"><span style="width:11px;height:11px;border-radius:50%;'
            f'background:{color}"></span>{txt}</div>')

def logo():
    return f'<img src="{core.LOGO}" style="position:absolute;top:56px;left:{M}px;height:30px;z-index:22">'

async def render_slide(name, html, elements, color_pairs, page_bg, expect_hero=True):
    slug = "raksha_bandhan_2026"
    outdir = f"out/versions/{slug}"
    os.makedirs(outdir, exist_ok=True)
    pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs, page_bg=page_bg, core=core, expect_hero=expect_hero)
    print(name, "preflight clean:", pf.get("clean"))
    if not pf.get("clean"):
        print(pf)
    out_png = f"{outdir}/{name}.png"
    await B.render(html, out_png, W, H, elements=elements, color_pairs=color_pairs, page_bg=page_bg, expect_hero=expect_hero)
    print("wrote", out_png)
    return out_png

# ============================= SLIDE 1 — HOOK =============================
async def slide1():
    accent = A[6]  # teal
    elements = []
    els = elements
    bg_div = '<div style="position:absolute;inset:0;background:var(--bg)"></div>'
    els.append((0,0,W,H))
    lg = logo(); els.append((M,56,140,32))
    eb = eyebrow("RAKSHA BANDHAN", accent, 106); els.append((M,106,300,24))
    hl = headline("IT ISN'T JUST<br>ABOUT BLOOD.", 190, 92, "var(--ink)"); els.append((M,190,W-2*M,220))
    sub = body("it's about the bonds we build <span style=\"font-family:var(--s);font-style:italic;color:%s\">here.</span>" % accent, 430, 30, "var(--ink3)", w=560)
    els.append((M,430,560,90))
    # hero rakhi motif, large, right side
    hero = rakhi_motif(770, 900, 300, accent, z=8)
    els.append((770-150, 900-150, 300, 420))
    ring1 = f'<div style="position:absolute;top:150px;left:820px;width:180px;height:180px;border-radius:50%;border:12px solid {A[0]};opacity:.9;z-index:3"></div>'
    els.append((820,150,180,180))
    dotgrid = f'<div style="position:absolute;top:760px;left:70px;width:132px;height:132px;z-index:6">{dd.stamp("dots", A[2], rot=0, style="clean")}</div>'
    els.append((70,760,132,132))
    star1 = f'<div style="position:absolute;top:990px;left:130px;width:110px;height:110px;z-index:6">{dd.stamp("star", A[0], rot=-14, style="clean")}</div>'
    els.append((130,990,110,110))
    heart1 = f'<div style="position:absolute;top:920px;left:790px;width:0px;height:0px"></div>'
    strip = f'<div style="position:absolute;top:0px;left:0px;width:{W}px;height:14px;background:{accent};z-index:5"></div>'
    els.append((0,0,W,14))
    ftr = footer(dark=False)
    els.append((M,H-70,300,20))
    pgno = page_no(1)
    els.append((W-M-60,H-70,60,20))
    inner = "".join([bg_div, strip, lg, eb, hl, sub, ring1, dotgrid, star1, hero, ftr, pgno])
    html = B.page(W, H, "var(--bg)", inner, grain=True)
    color_pairs = [("ring1", A[0], "var(--bg)"), ("rakhi_medallion", accent, "var(--bg)")]
    return await render_slide("v1_s1", html, els, color_pairs, "var(--bg)")

# ============================= SLIDE 2 — SENIORS =============================
async def slide2():
    accent = A[0]  # pink
    els = []
    bg_div = '<div style="position:absolute;inset:0;background:var(--ink)"></div>'
    els.append((0,0,W,H))
    strip = f'<div style="position:absolute;top:0px;left:0px;width:{W}px;height:14px;background:{accent};z-index:5"></div>'
    els.append((0,0,W,14))
    lg = f'<img src="{core.LOGO}" style="position:absolute;top:56px;left:{M}px;height:30px;z-index:22;background:var(--bg);padding:6px 10px;border-radius:10px">'
    els.append((M,56,160,44))
    eb = eyebrow("TO EVERY SENIOR", accent, 130)
    els.append((M,130,320,24))
    hl = headline("WHO'S GUIDED US.", 178, 76, "#FFFFFF")
    els.append((M,178,W-2*M,180))
    sub = body("the ones who showed us the way, one step at a time — this thread's for you.", 400, 27, "#D8D4C4", w=520)
    els.append((M,400,520,80))
    # two characters: senior (right, taller) tying rakhi on junior's (left) wrist
    p1 = person(330, 940, 260, A[4], z=6, flip=False)
    els.append((330-130,940-176,260,352))
    p2 = person(700, 900, 300, A[2], z=7, flip=True)
    els.append((700-150,900-203,300,405))
    rk = rakhi_motif(500, 760, 170, accent, z=10)
    els.append((500-85,760-85,170,238))
    ring1 = f'<div style="position:absolute;top:640px;left:130px;width:150px;height:150px;border-radius:50%;border:12px solid {A[5]};opacity:.85;z-index:3"></div>'
    els.append((130,640,150,150))
    burst1 = f'<div style="position:absolute;top:200px;left:840px;width:120px;height:120px;z-index:6">{dd.stamp("burst", A[2], rot=8, style="clean")}</div>'
    els.append((840,200,120,120))
    ftr = footer(dark=True)
    els.append((M,H-70,300,20))
    pgno = page_no(2, dark=True)
    els.append((W-M-60,H-70,60,20))
    inner = "".join([bg_div, strip, lg, eb, hl, sub, ring1, burst1, p1, p2, rk, ftr, pgno])
    html = B.page(W, H, "var(--ink)", inner, grain=True)
    color_pairs = [("ring1", A[5], "var(--ink)"), ("rakhi_medallion", accent, "var(--ink)")]
    return await render_slide("v1_s2", html, els, color_pairs, "var(--ink)")

# ============================= SLIDE 3 — BATCHMATES =============================
async def slide3():
    accent = A[4]  # sky
    els = []
    bg_div = '<div style="position:absolute;inset:0;background:var(--bg)"></div>'
    els.append((0,0,W,H))
    strip = f'<div style="position:absolute;top:0px;left:0px;width:{W}px;height:14px;background:{accent};z-index:5"></div>'
    els.append((0,0,W,14))
    lg = logo(); els.append((M,56,140,32))
    eb = eyebrow("TO EVERY BATCHMATE", accent, 106)
    els.append((M,106,360,24))
    hl = headline("WHO'S HAD<br>OUR BACK.", 186, 92, "var(--ink)")
    els.append((M,186,W-2*M,220))
    sub = body("side by side through every deadline, every win — that's a bond worth tying.", 430, 30, "var(--ink3)", w=560)
    els.append((M,430,560,90))
    # two wrist bands tied together, side by side, lower half
    wb1 = wrist_band(360, 940, 260, A[5], z=8, rot=-8)
    els.append((360-130,940-81,260,161))
    wb2 = wrist_band(680, 980, 260, A[6], z=9, rot=10)
    els.append((680-130,980-81,260,161))
    rk = rakhi_motif(520, 800, 150, accent, z=11)
    els.append((520-75,800-75,150,210))
    zig = f'<div style="position:absolute;top:640px;left:120px;width:180px;height:90px;z-index:6">{dd.stamp("zigzag", A[3], rot=0, style="clean")}</div>'
    els.append((120,640,180,90))
    sparkle1 = f'<div style="position:absolute;top:700px;left:850px;width:110px;height:110px;z-index:6">{dd.stamp("sparkle", A[0], rot=12, style="clean")}</div>'
    els.append((850,700,110,110))
    dotgrid = f'<div style="position:absolute;top:1000px;left:840px;width:110px;height:110px;z-index:6">{dd.stamp("dots", A[2], rot=0, style="clean")}</div>'
    els.append((840,1000,110,110))
    ftr = footer(dark=False)
    els.append((M,H-70,300,20))
    pgno = page_no(3)
    els.append((W-M-60,H-70,60,20))
    inner = "".join([bg_div, strip, lg, eb, hl, sub, zig, sparkle1, dotgrid, wb1, wb2, rk, ftr, pgno])
    html = B.page(W, H, "var(--bg)", inner, grain=True)
    color_pairs = [("rakhi_medallion", accent, "var(--bg)")]
    return await render_slide("v1_s3", html, els, color_pairs, "var(--bg)")

# ============================= SLIDE 4 — JUNIORS + CLOSE =============================
async def slide4():
    accent = A[2]  # lemon
    els = []
    bg_div = '<div style="position:absolute;inset:0;background:var(--ink)"></div>'
    els.append((0,0,W,H))
    strip = f'<div style="position:absolute;top:0px;left:0px;width:{W}px;height:14px;background:{accent};z-index:5"></div>'
    els.append((0,0,W,14))
    lg = f'<img src="{core.LOGO}" style="position:absolute;top:56px;left:{M}px;height:30px;z-index:22;background:var(--bg);padding:6px 10px;border-radius:10px">'
    els.append((M,56,160,44))
    eb = eyebrow("AND EVERY JUNIOR", accent, 130)
    els.append((M,130,340,24))
    hl = headline("WHO'S BECOME<br>FAMILY.", 178, 84, "#FFFFFF")
    els.append((M,178,W-2*M,210))
    hero = headline("HAPPY<br>RAKSHABANDHAN", 620, 96, accent, w=W-2*M)
    els.append((M,620,W-2*M,230))
    sub = body("from all of us at AQUATERRA — thank you for being family.", 900, 27, "#D8D4C4", w=560)
    els.append((M,900,560,60))
    p1 = person(830, 500, 230, A[0], z=6, flip=True)
    els.append((830-115,500-155,230,311))
    rk1 = rakhi_motif(150, 1040, 160, accent, z=8, rot=-10)
    els.append((150-80,1040-80,160,224))
    rk2 = rakhi_motif(880, 1080, 130, A[0], z=8, rot=14)
    els.append((880-65,1080-65,130,182))
    ring1 = f'<div style="position:absolute;top:70px;left:830px;width:150px;height:150px;border-radius:50%;border:12px solid {A[6]};opacity:.85;z-index:3"></div>'
    els.append((830,70,150,150))
    star1 = f'<div style="position:absolute;top:980px;left:70px;width:90px;height:90px;z-index:6">{dd.stamp("star", A[4], rot=-10, style="clean")}</div>'
    els.append((70,980,90,90))
    ftr = footer(dark=True)
    els.append((M,H-70,300,20))
    pgno = page_no(4, dark=True)
    els.append((W-M-60,H-70,60,20))
    inner = "".join([bg_div, strip, lg, eb, hl, ring1, p1, hero, sub, star1, rk1, rk2, ftr, pgno])
    html = B.page(W, H, "var(--ink)", inner, grain=True)
    color_pairs = [("ring1", A[6], "var(--ink)"), ("rakhi_medallion1", accent, "var(--ink)"), ("rakhi_medallion2", A[0], "var(--ink)")]
    return await render_slide("v1_s4", html, els, color_pairs, "var(--ink)")

async def main():
    await slide1()
    await slide2()
    await slide3()
    await slide4()

if __name__ == "__main__":
    asyncio.run(main())
