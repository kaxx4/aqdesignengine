import asyncio, os, sys, importlib.util
ROOT = "/home/user/aqdesignengine"
os.chdir(ROOT)
ENGINE_DIR = os.path.join(ROOT, "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n, path=None):
    p = path or os.path.join(ENGINE_DIR, n+".py")
    s = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout"); shp = load("shapes")
# reuse the rakhi visual vocabulary built for the first carousel instead of rebuilding it
v1 = load("rakhi_v1", "/home/user/aqdesignengine/scratchpad/rakhi/gen_rakhi_v1.py")

W, H = core.SIZES["feed"]
M = 64
A = core.ACCENTS
SLUG = "raksha_bandhan_relatable_2026"

rakhi_motif = v1.rakhi_motif
wrist_band  = v1.wrist_band
person      = v1.person
headline    = v1.headline
body        = v1.body
eyebrow     = v1.eyebrow
logo        = v1.logo

def footer(dark=False, n="01"):
    c = "#FFFFFF" if dark else "var(--ink3)"
    return (f'<span style="position:absolute;bottom:52px;left:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:15px;letter-spacing:.06em;color:{c};z-index:20">@ngo.aquaterra</span>'
            f'<span style="position:absolute;bottom:52px;right:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:13px;letter-spacing:.06em;color:{c};z-index:20">{n}/03</span>')

def coin(cx, cy, size, accent, z=8, label="₹"):
    """A simple coin/UPI-transfer icon: ink-outlined circle with a rupee glyph — not a fake
    receipt/UI screenshot, just an iconographic mark (real-assets-only rule, CLAUDE.md §9)."""
    r = size/2
    svg = (f'<svg viewBox="0 0 100 100" width="{size}" height="{size}">'
           f'<circle cx="50" cy="50" r="42" fill="{accent}" stroke="#0A0A0A" stroke-width="7"/>'
           f'<text x="50" y="64" font-family="JetBrains Mono, monospace" font-weight="700" '
           f'font-size="42" text-anchor="middle" fill="#0A0A0A">{label}</text></svg>')
    return f'<div style="position:absolute;top:{cy-r:.0f}px;left:{cx-r:.0f}px;width:{size}px;height:{size}px;z-index:{z};filter:drop-shadow(5px 5px 0 #0A0A0A)">{svg}</div>'

def list_row(y, num_bg, icon_html, text, z=10):
    row = (f'<div style="position:absolute;top:{y}px;left:{M}px;width:{W-2*M}px;display:flex;'
           f'align-items:center;gap:22px;z-index:{z}">'
           f'<div style="flex:0 0 auto">{icon_html}</div>'
           f'<div style="font-family:var(--e);font-weight:400;font-size:26px;line-height:1.28;'
           f'color:var(--ink);flex:1">{text}</div></div>')
    return row

async def render_slide(name, html, elements, color_pairs, page_bg, expect_hero=True):
    outdir = f"out/versions/{SLUG}"
    os.makedirs(outdir, exist_ok=True)
    pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs, page_bg=page_bg, core=core, expect_hero=expect_hero)
    print(name, "preflight clean:", pf.get("clean"))
    out_png = f"{outdir}/{name}.png"
    await B.render(html, out_png, W, H, elements=elements, color_pairs=color_pairs, page_bg=page_bg, expect_hero=expect_hero)
    print("wrote", out_png)
    return out_png

# ============================= SLIDE 1 — HOOK =============================
async def slide1():
    accent = A[5]  # grape
    els = []
    bg_div = '<div style="position:absolute;inset:0;background:var(--ink)"></div>'
    els.append((0,0,W,H))
    strip = f'<div style="position:absolute;top:0;left:0;width:{W}px;height:14px;background:{accent};z-index:5"></div>'
    els.append((0,0,W,14))
    lg = f'<img src="{core.LOGO}" style="position:absolute;top:56px;left:{M}px;height:30px;z-index:22;background:var(--bg);padding:6px 10px;border-radius:10px">'
    els.append((M,56,160,44))
    eb = eyebrow("REAL TALK", accent, 130)
    els.append((M,130,240,24))
    hl = headline("RAKHI HITS<br>DIFFERENT WHEN<br>YOU'RE BOTH BROKE.", 178, 68, "#FFFFFF", lh=1.02)
    els.append((M,178,W-2*M,320))
    sub = body("...and living off different mess food 🧵<br><br>no one tells you growing up means rakhi stops being about tying a thread and starts being about:",
                520, 28, "#D8D4C4", w=580)
    els.append((M,520,580,220))
    hero = rakhi_motif(870, 990, 260, accent, z=8)
    els.append((870-130,990-130,260,364))
    ring1 = f'<div style="position:absolute;top:850px;left:64px;width:150px;height:150px;border-radius:50%;border:12px solid {A[4]};opacity:.85;z-index:3"></div>'
    els.append((64,850,150,150))
    coin1 = coin(330, 900, 110, A[2], z=7)
    els.append((330-55,900-55,110,110))
    wb1 = wrist_band(230, 1150, 260, A[0], z=8, rot=-8)
    els.append((230-130,1150-81,260,161))
    star1 = f'<div style="position:absolute;top:1090px;left:520px;width:90px;height:90px;z-index:6">{dd.stamp("star", A[0], rot=-12, style="clean")}</div>'
    els.append((520,1090,90,90))
    dots1 = f'<div style="position:absolute;top:1060px;left:660px;width:100px;height:100px;z-index:6">{dd.stamp("dots", A[2], rot=0, style="clean")}</div>'
    els.append((660,1060,100,100))
    ftr = footer(dark=True, n="01")
    els.append((M,H-70,300,20))
    inner = "".join([bg_div, strip, lg, eb, hl, sub, ring1, coin1, star1, dots1, wb1, hero, ftr])
    html = B.page(W, H, "var(--ink)", inner, grain=True)
    color_pairs = [("ring1", A[4], "var(--ink)"), ("rakhi_medallion", accent, "var(--ink)"), ("coin", A[2], "var(--ink)")]
    return await render_slide("v1_s1", html, els, color_pairs, "var(--ink)")

# ============================= SLIDE 2 — THE LIST =============================
async def slide2():
    accent = A[3]  # tomato
    els = []
    bg_div = '<div style="position:absolute;inset:0;background:var(--bg)"></div>'
    els.append((0,0,W,H))
    strip = f'<div style="position:absolute;top:0;left:0;width:{W}px;height:14px;background:{accent};z-index:5"></div>'
    els.append((0,0,W,14))
    lg = logo(); els.append((M,56,140,32))
    eb = eyebrow("IT LOOKS LIKE THIS NOW", accent, 106)
    els.append((M,106,420,24))
    hl = headline("GROWING-UP<br>RAKHI, RANKED.", 170, 62, "var(--ink)", lh=1.0)
    els.append((M,170,W-2*M,150))

    def icon_div(x, y, size, kind, accent2):
        if kind == "coin":
            return coin(x+size/2, y+size/2, size, accent2, z=11)
        return f'<div style="position:absolute;top:{y}px;left:{x}px;width:{size}px;height:{size}px;z-index:11;filter:drop-shadow(4px 4px 0 #0A0A0A)">{dd.stamp(kind, accent2, rot=0, style="clean")}</div>'

    rows_y = [400, 560, 720, 880]
    row_h = 138
    items = [
        (A[2], "coin", "your sibling UPI-ing you ₹500 mid-semester because you “forgot” to budget"),
        (A[4], "lightning", "them knowing exactly which prof to blame when you're spiralling about grades"),
        (A[0], "speech", "the group chat that sends memes instead of “good morning” texts"),
        (A[5], "arrow", "still fighting over whose turn it is to call mom back"),
    ]
    row_html = []
    for i, ((ac, kind, txt), y) in enumerate(zip(items, rows_y)):
        icon = icon_div(M, y, 72, kind, ac)
        els.append((M, y, 72, 72))
        row = list_row(y+6, ac, "", txt, z=10)
        # replace the empty icon slot with the rendered icon at fixed left, text offset instead
        row = (f'<div style="position:absolute;top:{y}px;left:{M+96}px;width:{W-2*M-96}px;'
               f'font-family:var(--e);font-weight:400;font-size:25px;line-height:1.3;color:var(--ink);z-index:10">{txt}</div>')
        els.append((M+96, y, W-2*M-96, 80))
        row_html.append(icon); row_html.append(row)
        if i < 3:
            div = f'<div style="position:absolute;top:{y+row_h-8}px;left:{M}px;width:{W-2*M}px;height:2px;background:var(--ink);opacity:.15;z-index:9"></div>'
            els.append((M, y+row_h-8, W-2*M, 2))
            row_html.append(div)

    rk_top = rakhi_motif(920, 300, 120, accent, z=8, rot=8)
    els.append((920-60,300-60,120,168))
    wb1 = wrist_band(230, 1160, 240, accent, z=8, rot=6)
    els.append((230-120,1160-74,240,149))
    rk_bot = rakhi_motif(650, 1200, 150, A[6], z=9, rot=-6)
    els.append((650-75,1200-75,150,210))
    zig1 = f'<div style="position:absolute;top:1080px;left:490px;width:150px;height:75px;z-index:6">{dd.stamp("zigzag", A[5], rot=0, style="clean")}</div>'
    els.append((490,1080,150,75))
    dots = f'<div style="position:absolute;top:1140px;left:870px;width:110px;height:110px;z-index:6">{dd.stamp("dots", A[6], rot=0, style="clean")}</div>'
    els.append((870,1140,110,110))
    ftr = footer(dark=False, n="02")
    els.append((M,H-70,300,20))
    inner = "".join([bg_div, strip, lg, eb, hl] + row_html + [dots, zig1, wb1, rk_bot, rk_top, ftr])
    html = B.page(W, H, "var(--bg)", inner, grain=True)
    color_pairs = [("rakhi_medallion", accent, "var(--bg)")]
    return await render_slide("v1_s2", html, els, color_pairs, "var(--bg)", expect_hero=False)

# ============================= SLIDE 3 — PLOT TWIST + CLOSE =============================
async def slide3():
    accent = A[6]  # teal
    els = []
    bg_div = '<div style="position:absolute;inset:0;background:var(--ink)"></div>'
    els.append((0,0,W,H))
    strip = f'<div style="position:absolute;top:0;left:0;width:{W}px;height:14px;background:{accent};z-index:5"></div>'
    els.append((0,0,W,14))
    lg = f'<img src="{core.LOGO}" style="position:absolute;top:56px;left:{M}px;height:30px;z-index:22;background:var(--bg);padding:6px 10px;border-radius:10px">'
    els.append((M,56,160,44))
    eb = eyebrow("PLOT TWIST", accent, 130)
    els.append((M,130,220,24))
    hl = headline("IT WAS NEVER<br>ABOUT PROTECTION.", 178, 62, "#FFFFFF", lh=1.02)
    els.append((M,178,W-2*M,150))
    sub = body("it's about the one person who's seen every unhinged version of you — finals-week you, "
               "heartbreak you, 3-months-into-a-new-personality you — and still picks up the phone.",
               350, 27, "#D8D4C4", w=580)
    els.append((M,350,580,150))
    p1 = person(870, 620, 220, A[0], z=6, flip=True)
    els.append((870-110,620-149,220,297))
    rk = rakhi_motif(760, 900, 150, accent, z=9)
    els.append((760-75,900-75,150,210))
    close = (f'<div style="position:absolute;top:1000px;left:{M}px;width:{W-2*M}px;font-family:var(--e);'
             f'font-weight:600;font-size:29px;line-height:1.35;color:{accent};z-index:12">'
             f'happy rakhi to the sibling who’s basically your <span style="font-family:var(--s);'
             f'font-style:italic;color:{A[2]}">unpaid therapist</span>, hype person, and emergency '
             f'contact — rolled into one 🫡</div>')
    els.append((M,1000,W-2*M,220))
    star1 = f'<div style="position:absolute;top:70px;left:850px;width:100px;height:100px;z-index:6">{dd.stamp("sparkle", A[2], rot=10, style="clean")}</div>'
    els.append((850,70,100,100))
    dots = f'<div style="position:absolute;top:1210px;left:130px;width:100px;height:100px;z-index:6">{dd.stamp("dots", A[0], rot=0, style="clean")}</div>'
    els.append((130,1210,100,100))
    ftr = footer(dark=True, n="03")
    els.append((M,H-70,300,20))
    inner = "".join([bg_div, strip, lg, eb, hl, sub, star1, p1, rk, close, dots, ftr])
    html = B.page(W, H, "var(--ink)", inner, grain=True)
    color_pairs = [("rakhi_medallion", accent, "var(--ink)")]
    return await render_slide("v1_s3", html, els, color_pairs, "var(--ink)")

async def main():
    await slide1()
    await slide2()
    await slide3()

if __name__ == "__main__":
    asyncio.run(main())
