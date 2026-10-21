"""DISCO DIWALI "WANT A STALL AT OUR DIWALI?" story (1080x1920), AQ house cream style, rebuilt from the user's reference (2026-10-21, "like this").

Workflow B-style bespoke build (core+build+doodles primitives). Reference crop measured at 923x1640, scaled x1.17 to the 1080 canvas.
Copy is the reference's own, supplied by the user: eyebrow DISCO DIWALI . STALL CALL, headline (user copy, 2026-10-21: "its your last chance to put up a stall at disco diwali, dont miss it") LAST CHANCE / TO PUT UP A / stall / AT DISCO DIWALI + "don't miss it", three categories
(GAMES make people compete / MERCH & CRAFTS diyas, jewellery, thrift / SOMETHING ELSE surprise us), CTA DM US TO GET A SPOT @ngo.aquaterra.
NO deadline (user, 2026-10-21). Adaptations: department colours follow the reference (blue tag, purple, lemon, pink) which are all core.ACCENTS; pill label uses core.on_dark.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_stall_call_cream.py"""
import asyncio, os, sys, importlib.util
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine"); sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py")); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")
W, H = core.SIZES["story"]; M = 64
A = core.ACCENTS; INK = core.INK
els = []; parts = []
def doodle(kind, x, y, size, fill, z=8):
    return (f'<div data-tag="doodle" style="position:absolute;top:{y}px;left:{x}px;width:{size}px;height:{size}px;z-index:{z}">{dd.stamp(kind, fill)}</div>')
SH = f"box-shadow:9px 9px 0 {INK};"

parts.append('<div style="position:absolute;inset:0;background:var(--bg)"></div>')
parts.append(B.logo(y=104)); els.append(("logo", M, 104, 190, 32))
tomato = core.on_cream(A[3], 19)
parts.append(f'<div data-tag="eyebrow" style="position:absolute;top:202px;left:{M}px;font-family:var(--m);font-weight:700;font-size:19px;letter-spacing:.14em;text-transform:uppercase;color:{tomato};display:flex;align-items:center;gap:10px;z-index:6"><span style="width:12px;height:12px;border-radius:50%;background:{A[3]}"></span>Disco Diwali &middot; Last call</div>')
els.append(("eyebrow", M, 202, 420, 24))

def head(tag, txt, top, size, h):
    parts.append(f'<div data-tag="{tag}" style="position:absolute;left:{M - 6}px;top:{top}px;font-family:var(--d);font-weight:900;font-size:{size}px;line-height:1;text-transform:uppercase;white-space:nowrap;letter-spacing:-.02em;color:var(--ink);z-index:6">{txt}</div>')
    els.append((tag, M, top, 930, h))
head("h1a", "Last chance", 248, 124, 124)
head("h1b", "to put up a", 248 + 114, 124, 124)
# blue tag holding the serif accent word (the ONE Instrument Serif word)
tx, ty, tw, th = 59, 524, 719, 357
parts.append(f'<div data-tag="tag" style="position:absolute;left:{tx}px;top:{ty}px;width:{tw}px;height:{th}px;background:{A[4]};border:5px solid {INK};border-radius:{core.RADII["outer"]}px;{SH}transform:rotate(-1.5deg);z-index:5">'
             f'<span data-tag="tagword" style="position:absolute;left:40px;top:0;height:100%;display:flex;align-items:center;font-family:var(--s);font-style:italic;font-size:340px;line-height:1;color:{INK};white-space:nowrap">stall</span></div>')
els += [("tag", tx, ty - 20, tw + 10, 395), ("tagword", tx + 30, ty - 20, 540, 395)]
parts.append(doodle("sparkle", 840, 586, 170, A[2])); els.append(("spark", 840, 586, 170, 170))
parts.append(doodle("star", 880, 776, 100, A[0])); els.append(("star", 880, 776, 100, 100))
head("h2", "At Disco Diwali", 922, 96, 96)
parts.append(f'<div data-tag="dmi" style="position:absolute;left:{M}px;top:1026px;font-family:var(--e);font-weight:700;font-size:34px;line-height:1;color:{core.on_cream(A[3], 34)};z-index:6">don\'t miss it</div>'); els.append(("dmi", M, 1026, 230, 36))

def card(tag, x, y, w, h, fill, rot, title, sub, icon, icon_fill, isz):
    fg = core.text_on(fill)
    parts.append(f'<div data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{fill};border:5px solid {INK};border-radius:{core.RADII["outer"]}px;{SH}transform:rotate({rot}deg);z-index:5">'
                 f'<div data-tag="{tag}_t" style="position:absolute;left:26px;bottom:24px;color:{fg}"><div style="font-family:var(--d);font-weight:900;font-size:40px;line-height:1;text-transform:uppercase;letter-spacing:-.01em">{title}</div>'
                 f'<div style="font-family:var(--e);font-weight:500;font-size:25px;line-height:1.2;margin-top:6px;text-transform:lowercase">{sub}</div></div>'
                 f'<div data-tag="{tag}_i" style="position:absolute;right:26px;top:22px;width:{isz}px;height:{isz}px">{dd.stamp(icon, icon_fill)}</div></div>')
    els.extend([(tag, x, y, w + 10, h + 10), (tag + "_t", x + 26, y + h - 124, 400, 104), (tag + "_i", x + w - isz - 26, y + 22, isz, isz)])
card("c1", 64, 1092, 468, 257, A[5], -1.5, "Games", "make people compete", "lightning", INK, 84)
card("c2", 552, 1131, 466, 254, A[2], 1.5, "Merch &amp; crafts", "diyas, jewellery, thrift,<br>charm bracelets", "heart", INK, 84)
card("c3", 67, 1413, 951, 254, A[0], .6, "Something else", "surprise us", "burst", INK, 96)
# CTA pill
px, py, pw, ph = 64, 1695, 950, 94
parts.append(f'<div data-tag="pill" style="position:absolute;left:{px}px;top:{py}px;width:{pw}px;height:{ph}px;background:{INK};border-radius:999px;box-shadow:7px 7px 0 {A[4]};display:flex;align-items:center;justify-content:center;gap:22px;z-index:6;white-space:nowrap">'
             f'<span data-tag="pill_a" style="font-family:var(--d);font-weight:900;font-size:46px;color:{core.PAPER};text-transform:uppercase;letter-spacing:-.01em">DM us to get a spot</span>'
             f'<span data-tag="pill_b" style="font-family:var(--m);font-weight:700;font-size:23px;color:{core.on_dark(A[4], 23)}">@ngo.aquaterra</span></div>')
els += [("pill", px, py, pw + 8, ph + 8), ("pill_a", px + 150, py + 20, 520, 54), ("pill_b", px + 700, py + 32, 210, 30)]

html = B.page(W, H, "var(--bg)", "".join(parts), grain=False)
containers = ("tag", "c1", "c2", "c3", "pill")
text_pairs = [("h1a", INK, "var(--bg)", 124, True), ("h1b", INK, "var(--bg)", 124, True), ("dmi", core.on_cream(A[3], 34), "var(--bg)", 34, True), ("h2", INK, "var(--bg)", 96, True), ("eyebrow", tomato, "var(--bg)", 19, True),
              ("pill_a", core.PAPER, INK, 46, True), ("pill_b", core.on_dark(A[4], 23), INK, 23, True)]
async def main():
    os.makedirs("out/discodiwali/stall_call", exist_ok=True)
    await B.render(html, "out/discodiwali/stall_call/story_cream.png", W, H, elements=els, containers=containers, text_pairs=text_pairs, page_bg="var(--bg)",
                   collision_ignore=[("h1b", "tag"), ("h2", "tag"), ("spark", "tag"), ("star", "tag"), ("h2", "star"), ("tagword", "tag")])
    print("done")
asyncio.run(main())
