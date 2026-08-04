# 6. The Bespoke Script

Copy this into the scratchpad as `gen_<slug8>_vN.py`. It is the exact shape used for all 44
recreations, updated to call the standing gate (§7).

```python
import asyncio, os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")
W, H = core.SIZES["feed"]; M = 48          # feed canvas is 1080x1350 — NEVER assume taller
A = core.ACCENTS                            # A[0..6]: pink,mint,lemon,tomato,sky,grape,teal
elements = []                               # keep a bbox (x,y,w,h) per placed element, IN SYNC

# doodle() helper: most doodles take (fill, rot); some also style="rough"/"clean"; globe takes no fill
def doodle(kind, x, y, size, fill, rot=0, z=7):
    fn = getattr(dd, kind)
    try: inner = fn(fill=fill, rot=rot)
    except TypeError: inner = fn(rot=rot)
    return f'<div style="position:absolute;top:{y}px;left:{x}px;width:{size}px;height:{size}px;z-index:{z}">{inner}</div>'

# --- build each element as an absolutely-positioned div/svg, and APPEND ITS TRUE BBOX ---
# CRITICAL: when you move an element's CSS x/y, update its elements.append((x,y,w,h)) too.
# A stale bbox makes bounds_check/collision_check silently miss real bugs (sample 6).
hero = doodle("globe", 270, 540, 520, A[4])           # heroes fill a real fraction of the frame
elements.append((270, 540, 520, 520))
# ... every other element, each with a matching elements.append(...) ...

footer = f'<span style="position:absolute;bottom:52px;left:{M}px;font-family:var(--m);font-weight:700;font-size:13px;color:var(--ink);z-index:20">@ngo.aquaterra</span>'
elements.append((M, H-70, 300, 20))

# --- assemble, GATE, render ---
inner = "".join([f'<div style="position:absolute;inset:0;background:var(--bg)"></div>', hero, footer])
html = B.page(W, H, "var(--bg)", inner, grain=False)   # grain=True adds photo-grain overlay

# color_pairs: (label, fill) or (label, fill, surface) for every shape whose fill could vanish
color_pairs = [("hero_bg", A[4], "var(--bg)")]

# ONE gate call before render. clean==False means a real bug — fix before rendering.
pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs,
                   page_bg="var(--bg)", core=core, expect_hero=True)

async def main():
    slug = "8988345ad4963e"                              # first ~14 chars of the reference hash
    os.makedirs(f"out/versions/{slug}", exist_ok=True)
    await B.render(html, f"out/versions/{slug}/v2.png", W, H)  # css_var_check auto-runs here
    print("done")
asyncio.run(main())
```
Run with `PYTHONIOENCODING=utf-8 python gen_<slug8>_vN.py` (the utf-8 flag matters for the ✓/⚠
glyphs on Windows). Then **Read the rendered PNG and run the looking gate (§3).**

## See also
- [[05 Workflow B - Reference Recreation]]
- [[07 The Gate Stack]]

[[Manual Index]]
