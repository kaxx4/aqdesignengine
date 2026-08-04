import asyncio, os, sys, base64, importlib.util

os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)

def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout"); T = load("tex")

W, H = 1080, 1440
M = 64
A = core.ACCENTS  # pink,mint,lemon,tomato,sky,grape,teal

def snap(v): return round(v / 8) * 8

def b64_img(path, mime="image/png"):
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()

def chip(txt, accent, x, y, rot=0):
    fg = "#0A0A0A" if accent in core.INK_ON else "#fff"
    return (f'<div style="position:absolute;top:{snap(y)}px;left:{snap(x)}px;background:{accent};color:{fg};'
            f'font-family:var(--m);font-weight:700;font-size:17px;letter-spacing:.05em;text-transform:uppercase;'
            f'padding:10px 18px;border-radius:999px;border:3px solid var(--ink);box-shadow:4px 4px 0 var(--ink);'
            f'transform:rotate({rot}deg);z-index:14;white-space:nowrap">{txt}</div>')

def doodle(kind, x, y, size, accent, rot=0, z=15):
    fn = getattr(dd, kind, dd.star)
    try: inner = fn(fill=accent, rot=rot)
    except TypeError:
        try: inner = fn(stroke=accent, rot=rot)
        except TypeError: inner = fn(rot=rot)
    return f'<div style="position:absolute;top:{snap(y)}px;left:{snap(x)}px;width:{size}px;height:{size}px;z-index:{z}">{inner}</div>'

yamal_uri = b64_img("scratchpad/Screenshot 2026-07-18 115448.png")
messi_uri = b64_img("scratchpad/Screenshot 2026-07-18 115500.png")

esp_accent = A[3]   # tomato — reads closest to Spain's red
arg_accent = A[4]   # sky — Argentina's sky blue
badge_accent = A[2] # lemon, punchy VS badge

frame_w = W - 2 * M
yamal_y, yamal_h = 128, 508
messi_y, messi_h = yamal_y + yamal_h + 26, 508
panel_y = messi_y + messi_h + 26
panel_h = H - panel_y - M

elements = [
    ("kicker", M, 56, 380, 24),
    ("index_chip", W - M - 210, 44, 210, 40),
    ("yamal_frame", M, yamal_y, frame_w, yamal_h),
    ("messi_frame", M, messi_y, frame_w, messi_h),
    ("vs_badge", W // 2 - 62, yamal_y + yamal_h - 62, 124, 124),
    ("panel", M, panel_y, frame_w, panel_h),
]
color_pairs = [
    ("panel", "var(--ink)", "var(--bg)"),
    ("yamal_chip", esp_accent, "var(--ink)"),
    ("messi_chip", arg_accent, "var(--ink)"),
    ("vs_badge_bg", badge_accent, "var(--bg)"),
]

def photo_wrap(src, tint, object_pos="50% 50%"):
    # riso_photo_wrap hardcodes object-position:center, which is wrong for a portrait-oriented
    # source (664x852) forced into a wide landscape frame (952x508): center-crop only shows the
    # torso, the face is above the crop window. Same halftone/tint treatment, custom crop anchor.
    return (f'<div style="position:relative;width:100%;height:100%;overflow:hidden">'
            f'<img src="{src}" style="width:100%;height:100%;object-fit:cover;object-position:{object_pos};'
            f'filter:grayscale(1) contrast(1.2) brightness(1.05)">'
            f'<div style="position:absolute;inset:0;background:{tint};mix-blend-mode:multiply;opacity:.55"></div>'
            f'<div style="position:absolute;inset:0;background-image:radial-gradient(#00000055 1.2px,transparent 1.6px);'
            f'background-size:5px 5px;mix-blend-mode:multiply;opacity:.4"></div></div>')

yamal_photo = photo_wrap(yamal_uri, esp_accent + "40", object_pos="50% 12%")
messi_photo = photo_wrap(messi_uri, arg_accent + "40", object_pos="50% 30%")

panel_content = "".join([
    f'<div style="font-family:var(--d);font-weight:900;font-size:52px;line-height:1.02;'
    f'text-transform:uppercase;color:{badge_accent}">pov: you\'re facing a guy<br>older than your dad</div>',
    f'<div style="font-family:var(--m);font-weight:700;font-size:16px;letter-spacing:.03em;color:var(--bg);'
    f'opacity:.8">messi, born 1987. yamal, born 2007. 20 years apart &mdash; and he\'s still doing this.</div>',
])

inner = "".join([
    f'<div style="position:absolute;inset:0;background:var(--bg)"></div>',
    f'<span style="position:absolute;top:56px;left:{M}px;font-family:var(--m);font-weight:700;font-size:14px;'
    f'letter-spacing:.14em;text-transform:uppercase;color:var(--ink);z-index:20">threat assessment &middot; final</span>',
    f'<div style="position:absolute;top:44px;right:{M}px;background:var(--ink);color:var(--bg);'
    f'font-family:var(--m);font-weight:700;font-size:15px;letter-spacing:.06em;padding:8px 16px;'
    f'border-radius:999px;z-index:20">20 YEAR AGE GAP</div>',

    # Yamal frame
    f'<div style="position:absolute;left:{M}px;top:{yamal_y}px;width:{frame_w}px;height:{yamal_h}px;'
    f'border-radius:24px;border:6px solid var(--ink);box-shadow:10px 10px 0 var(--ink);overflow:hidden;z-index:4">{yamal_photo}</div>',
    chip("lamine yamal, 17 &middot; &quot;the new kid&quot;", esp_accent, M + 24, yamal_y + yamal_h - 64, rot=-1.5),
    doodle("star", M + frame_w - 66, yamal_y - 30, 76, badge_accent, rot=-10, z=16),

    # Messi frame
    f'<div style="position:absolute;left:{M}px;top:{messi_y}px;width:{frame_w}px;height:{messi_h}px;'
    f'border-radius:24px;border:6px solid var(--ink);box-shadow:10px 10px 0 var(--ink);overflow:hidden;z-index:4">{messi_photo}</div>',
    chip("lionel messi &middot; age 37 &middot; &quot;still here&quot;", arg_accent, M + 24, messi_y + messi_h - 60, rot=1.5),

    # VS badge at the seam
    f'<div style="position:absolute;left:{W//2-62}px;top:{yamal_y+yamal_h-62}px;width:124px;height:124px;'
    f'border-radius:50%;background:{badge_accent};border:6px solid var(--ink);box-shadow:6px 6px 0 var(--ink);'
    f'display:flex;align-items:center;justify-content:center;z-index:10">'
    f'<span style="font-family:var(--d);font-weight:900;font-size:34px;color:#0A0A0A">VS</span></div>',

    # bottom ink panel — headline
    f'<div style="position:absolute;left:{M}px;top:{panel_y}px;width:{frame_w}px;height:{panel_h}px;'
    f'background:var(--ink);border-radius:24px;box-shadow:10px 10px 0 rgba(10,10,10,0.28);z-index:4;'
    f'display:flex;flex-direction:column;justify-content:center;gap:16px;padding:36px;box-sizing:border-box">{panel_content}</div>',
    doodle("burst", M + frame_w - 90, panel_y + panel_h - 90, 66, esp_accent, rot=8, z=12),
])

html = B.page(W, H, "var(--bg)", inner, grain=True)

async def main():
    pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs,
                        page_bg="var(--bg)", core=core, expect_hero=True,
                        collision_ignore=frozenset({
                            frozenset({"panel", "vs_badge"}),
                            frozenset({"yamal_frame", "vs_badge"}),
                            frozenset({"messi_frame", "vs_badge"}),
                        }))
    os.makedirs("out", exist_ok=True)
    out = "out/torch_meme_yamal_messi.png"
    await B.render(html, out, W, H)
    print(f"clean={pf['clean']} -> {out}")

asyncio.run(main())
