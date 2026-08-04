import asyncio, base64, os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build")
W, H = core.SIZES["feed"]; M = 64
A = core.ACCENTS  # pink,mint,lemon,tomato,sky,grape,teal
CAT_COLOR = {"Workshop": A[4], "Distribution Drive": A[1], "Distribution Workshop": A[1],
             "Feeding dogs": A[3], "Stalls": A[5]}

SRC = "scratchpad/format_test/src_images"
def photo_b64(fname):
    with open(os.path.join(SRC, fname), "rb") as f:
        ext = "jpeg" if fname.endswith("jpg") or fname.endswith("jpeg") else "png"
        return f"data:image/{ext};base64," + base64.b64encode(f.read()).decode()

def logo_pill(x=M, y=48):
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;z-index:20;background:var(--bg);'
            f'border:3px solid var(--ink);border-radius:999px;padding:8px 16px 8px 12px;'
            f'box-shadow:4px 4px 0 var(--ink);display:flex;align-items:center">'
            f'<img src="{core.LOGO}" style="height:22px;display:block"></div>')

def category_tag(txt, accent, x_right=M, y=58):
    ink = core.text_on(accent)
    return (f'<span style="position:absolute;top:{y}px;right:{x_right}px;z-index:20;font-family:var(--m);'
            f'font-weight:700;font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:{ink};'
            f'background:{accent};border:2.5px solid var(--ink);border-radius:999px;padding:7px 16px;'
            f'box-shadow:3px 3px 0 var(--ink)">{txt}</span>')

def location_tag(loc, date):
    return (f'<div style="position:absolute;bottom:100px;left:{M}px;z-index:20;font-family:var(--m);'
            f'font-weight:500;font-size:13px;letter-spacing:.04em;color:#FFFFFF;text-shadow:0 2px 6px rgba(0,0,0,.6)">'
            f'{loc} &middot; {date}</div>')

def footer(txt="@ngo.aquaterra"):
    return (f'<span style="position:absolute;bottom:56px;left:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:13px;letter-spacing:.06em;color:#FFFFFF;z-index:20;text-shadow:0 2px 6px rgba(0,0,0,.5)">{txt}</span>')

def scrim_bottom(h=340):
    return (f'<div style="position:absolute;bottom:0;left:0;right:0;height:{h}px;'
            f'background:linear-gradient(to top,rgba(0,0,0,.7),rgba(0,0,0,0));z-index:10"></div>')

def full_bleed_photo(b64, focus="center 30%"):
    return f'<img src="{b64}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;object-position:{focus};z-index:1">'

async def render_moment_card(fname, category, loc, date, out_name, focus="center 25%"):
    accent = CAT_COLOR.get(category, A[6])
    inner = full_bleed_photo(photo_b64(fname), focus)
    inner += scrim_bottom(320)
    inner += logo_pill()
    inner += category_tag(category, accent)
    inner += location_tag(loc, date)
    # location_tag sits directly above footer; nudge location up a bit so footer has clean room
    inner += footer()
    html = B.page(W, H, "var(--bg)", inner, grain=False)
    os.makedirs("out/versions/format_test", exist_ok=True)
    await B.render(html, f"out/versions/format_test/{out_name}.png", W, H)

async def main():
    await render_moment_card("teach_eng.jpg", "Workshop", "Ektara Foundation", "APR 2026", "moment_teach_eng", focus="center 20%")
    await render_moment_card("digital_safety.png", "Workshop", "Pather Saathi", "MAY 2026", "moment_digital_safety", focus="center 15%")
    print("done")
asyncio.run(main())
