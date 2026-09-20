import asyncio, os, sys, importlib.util
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
B = load("build")
shapes = load("shapes")

async def main():
    items = [
        dict(text="LABS", font="d", weight=900, size=40, transform="uppercase"),
    ]
    res = await B.measure_text(items, 1080, 1080)
    for it, r in zip(items, res):
        print(it["text"], "size", it["size"], "->", r)
    mw, ma = res[0]["glyph_w"], 40
    for badge_size in (180, 210, 230, 260):
        box, fits = shapes.fit_font(mw, ma, "burst", badge_size)
        avail = shapes.inner_width("burst", badge_size)
        print("burst size", badge_size, "avail_px", round(avail,1), "-> box", round(box,2), "fits", fits, "~px", round(box*badge_size/100,1))

asyncio.run(main())
