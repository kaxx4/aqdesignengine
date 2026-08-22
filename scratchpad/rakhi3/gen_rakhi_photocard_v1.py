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
v1 = load("rakhi_v1", "/home/user/aqdesignengine/scratchpad/rakhi/gen_rakhi_v1.py")

W, H = core.SIZES["feed"]
M = 64
A = core.ACCENTS
SLUG = "raksha_bandhan_photocard_2026"

rakhi_motif = v1.rakhi_motif
wrist_band  = v1.wrist_band
headline    = v1.headline
body        = v1.body
eyebrow     = v1.eyebrow
logo        = v1.logo

def footer(dark=False, n="00"):
    c = "#FFFFFF" if dark else "var(--ink3)"
    return (f'<span style="position:absolute;bottom:52px;left:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:15px;letter-spacing:.06em;color:{c};z-index:20">@ngo.aquaterra</span>'
            f'<span style="position:absolute;bottom:52px;right:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:13px;letter-spacing:.06em;color:{c};z-index:20">{n}/04</span>')

async def render_slide(name, html, elements, color_pairs, page_bg, expect_hero=True):
    outdir = f"out/versions/{SLUG}"
    os.makedirs(outdir, exist_ok=True)
    pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs, page_bg=page_bg, core=core, expect_hero=expect_hero)
    print(name, "preflight clean:", pf.get("clean"))
    out_png = f"{outdir}/{name}.png"
    await B.render(html, out_png, W, H, elements=elements, color_pairs=color_pairs, page_bg=page_bg, expect_hero=expect_hero)
    print("wrote", out_png)
    return out_png

# ============================= SLIDE 0 — COVER (no photo) =============================
async def slide0():
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
    hl = headline("RAKHI HITS<br>DIFFERENT WHEN<br>YOU'RE BOTH BROKE<br>AND IN DIFFERENT<br>CITIES.", 178, 62, "#FFFFFF", lh=1.05)
    els.append((M,178,W-2*M,540))
    hero = rakhi_motif(830, 1080, 260, accent, z=8)
    els.append((830-130,1080-130,260,364))
    ring1 = f'<div style="position:absolute;top:880px;left:64px;width:150px;height:150px;border-radius:50%;border:12px solid {A[4]};opacity:.85;z-index:3"></div>'
    els.append((64,880,150,150))
    star1 = f'<div style="position:absolute;top:1080px;left:150px;width:100px;height:100px;z-index:6">{dd.stamp("star", A[0], rot=-12, style="clean")}</div>'
    els.append((150,1080,100,100))
    dots1 = f'<div style="position:absolute;top:1180px;left:340px;width:100px;height:100px;z-index:6">{dd.stamp("dots", A[2], rot=0, style="clean")}</div>'
    els.append((340,1180,100,100))
    ftr = footer(dark=True, n="00")
    els.append((M,H-70,300,20))
    inner = "".join([bg_div, strip, lg, eb, hl, ring1, star1, dots1, hero, ftr])
    html = B.page(W, H, "var(--ink)", inner, grain=True)
    color_pairs = [("ring1", A[4], "var(--ink)"), ("rakhi_medallion", accent, "var(--ink)")]
    return await render_slide("v1_s0", html, els, color_pairs, "var(--ink)")

async def main():
    await slide0()

if __name__ == "__main__":
    asyncio.run(main())
