"""DISCO DIWALI "LAST CHANCE TO PUT UP A stall" story (1080x1920) in the Disco Diwali BRANDING (user, 2026-10-21: "use the disco diwali branding").

Format skeleton (brain/DISCO_DIWALI.md): ink ground, navy+gold lotus-diya corner plate with string lights, gold dust and film grain, LIVE badge top left (the AQ presence on this format),
title lockup with ball top right as the mark, off-white stroked NeutralFace type, gold accents, copper texture. No cream, no AQ accent colours (recorded format exception, DD rule 1).
Layout and copy are the approved cream story's: LAST CHANCE / TO PUT UP A / stall / AT DISCO DIWALI, don't miss it, GAMES / MERCH & CRAFTS (diyas, jewellery, thrift, charm bracelets) / SOMETHING ELSE, DM pill @ngo.aquaterra. NO deadline.
Diya plate rather than a photo: no consent question. Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_stall_call_brand.py"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT); sys.path.insert(0, os.path.join(ROOT, "engine"))
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ROOT, "engine", n + ".py")); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
dd = load("discodiwali"); B = dd.B; core = dd.core; dood = load("doodles")
W, H = 1080, 1920; M = 64
OFFW, GOLD, SILVER, COPPER, INK = "#F2EEE4", "#E8C26A", "#C9CCD3", "#D9774B", "#0A0A0A"
STROKE = f"color:{OFFW};-webkit-text-stroke:4px #000;paint-order:stroke fill;"
GLASS = "background:rgba(8,8,14,.68);"
els, parts = [], []
def uri(n): return dd.uri(n)

def ground():
    plate = lambda top, extra="": (f'<img data-tag="plate" src="{uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:{top}px;width:{W}px;height:1350px;object-fit:cover;z-index:1;{extra}">')
    p = '<div data-tag="plate" style="position:absolute;inset:0;z-index:0;background:#000"></div>' + plate(0)
    p += plate(H - 1350, "transform:scaleY(-1);-webkit-mask-image:linear-gradient(to top,transparent 0%,#000 45%);mask-image:linear-gradient(to top,transparent 0%,#000 45%);")
    p += (f'<img data-tag="lights" src="{uri("string_lights.png")}" style="position:absolute;left:160px;top:-53px;width:1045px;z-index:5">'
          f'<img data-tag="plate" src="{uri("sparkles.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:30;mix-blend-mode:screen;opacity:.55;pointer-events:none">'
          f'<img data-tag="plate" src="{uri("grain.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:31;mix-blend-mode:screen;opacity:.35;pointer-events:none">')
    return p
def doodle(kind, x, y, size, fill, tag="doodle"):
    return f'<div data-tag="{tag}" style="position:absolute;top:{y}px;left:{x}px;width:{size}px;height:{size}px;z-index:8">{dood.stamp(kind, fill)}</div>'

parts.append(ground())
parts.append(f'<img data-tag="badge" src="{uri("live_badge.png")}" style="position:absolute;left:40px;top:84px;width:150px;z-index:20">'); els.append(("badge", 40, 84, 150, 142))
lw = 300; t = lw / 1717; lh = round(991 * t); lx = W - 40 - lw; ly = 84
parts.append(f'<img data-tag="title" src="{uri("title_lockup.png")}" style="position:absolute;left:{round(lx - 265 * t)}px;top:{round(ly - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">'); els.append(("title", lx, ly, lw, lh))

def head(tag, txt, top, size, h):
    parts.append(f'<div data-tag="{tag}" style="position:absolute;left:{M - 6}px;top:{top}px;font-family:var(--d);font-weight:900;font-size:{size}px;line-height:1;text-transform:uppercase;white-space:nowrap;letter-spacing:-.02em;{STROKE}z-index:20">{txt}</div>')
    els.append((tag, M, top, 930, h))
head("h1a", "Last chance", 280, 124, 124)
head("h1b", "to put up a", 280 + 114, 124, 124)
tx, ty, tw, th = 59, 546, 719, 357
parts.append(f'<div data-tag="tag" style="position:absolute;left:{tx}px;top:{ty}px;width:{tw}px;height:{th}px;background:linear-gradient(rgba(10,6,4,.42),rgba(10,6,4,.42)),url({uri("copper_texture.jpg")}) center/cover;border:3px solid {GOLD};border-radius:32px;box-shadow:0 16px 36px rgba(0,0,0,.55);transform:rotate(-1.5deg);z-index:5">'
             f'<span data-tag="tagword" style="position:absolute;left:40px;top:0;height:100%;display:flex;align-items:center;font-family:var(--s);font-style:italic;font-size:340px;line-height:1;white-space:nowrap;{STROKE}">stall</span></div>')
els += [("tag", tx, ty - 20, tw + 10, 395), ("tagword", tx + 30, ty - 20, 540, 395)]
parts.append(doodle("sparkle", 840, 600, 170, GOLD, "spark")); els.append(("spark", 840, 608, 170, 170))
parts.append(doodle("star", 880, 798, 100, SILVER, "star")); els.append(("star", 880, 798, 100, 100))
head("h2", "At Disco Diwali", 940, 96, 96)
parts.append(f'<div data-tag="dmi" style="position:absolute;left:{M}px;top:1046px;font-family:var(--e);font-weight:700;font-size:34px;line-height:1;color:{GOLD};-webkit-text-stroke:2px #000;paint-order:stroke fill;z-index:20">don\'t miss it</div>'); els.append(("dmi", M, 1046, 230, 36))

def card(tag, x, y, w, h, rot, title, sub, icon, icon_fill, isz):
    parts.append(f'<div data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;{GLASS}border:2px solid {GOLD};border-radius:32px;box-shadow:0 14px 30px rgba(0,0,0,.5);transform:rotate({rot}deg);z-index:5">'
                 f'<div data-tag="{tag}_t" style="position:absolute;left:26px;bottom:24px"><div style="font-family:var(--d);font-weight:900;font-size:40px;line-height:1;text-transform:uppercase;letter-spacing:-.01em;color:{OFFW}">{title}</div>'
                 f'<div style="font-family:var(--e);font-weight:500;font-size:25px;line-height:1.2;margin-top:6px;text-transform:lowercase;color:{GOLD}">{sub}</div></div>'
                 f'<div data-tag="{tag}_i" style="position:absolute;right:26px;top:22px;width:{isz}px;height:{isz}px">{dood.stamp(icon, icon_fill)}</div></div>')
    els.extend([(tag, x, y, w + 10, h + 10), (tag + "_t", x + 26, y + h - 124, 400, 104), (tag + "_i", x + w - isz - 26, y + 22, isz, isz)])
card("c1", 64, 1112, 468, 257, -1.5, "Games", "make people compete", "lightning", SILVER, 84)
card("c2", 552, 1151, 466, 254, 1.5, "Merch &amp; crafts", "diyas, jewellery, thrift,<br>charm bracelets", "heart", GOLD, 84)
card("c3", 67, 1433, 951, 254, .6, "Something else", "surprise us", "burst", COPPER, 96)
px, py, pw, ph = 64, 1715, 950, 94
parts.append(f'<div data-tag="pill" style="position:absolute;left:{px}px;top:{py}px;width:{pw}px;height:{ph}px;background:{GOLD};border-radius:999px;box-shadow:0 12px 28px rgba(0,0,0,.55);display:flex;align-items:center;justify-content:center;gap:22px;z-index:6;white-space:nowrap">'
             f'<span data-tag="pill_a" style="font-family:var(--d);font-weight:900;font-size:46px;color:{INK};text-transform:uppercase;letter-spacing:-.01em">DM us to get a spot</span>'
             f'<span data-tag="pill_b" style="font-family:var(--m);font-weight:700;font-size:23px;color:#3A2A00">@ngo.aquaterra</span></div>')
els += [("pill", px, py, pw + 8, ph + 8), ("pill_a", px + 150, py + 20, 520, 54), ("pill_b", px + 700, py + 32, 210, 30)]

html = B.page(W, H, "#000", "".join(parts), grain=False)
text_pairs = [("pill_a", INK, GOLD, 46, True), ("pill_b", "#3A2A00", GOLD, 23, True), ("c1_t", OFFW, "#0B0B12", 40, True), ("c2_t", GOLD, "#0B0B12", 25, False), ("c3_t", OFFW, "#0B0B12", 40, True)]
async def main():
    os.makedirs("out/discodiwali/stall_call", exist_ok=True)
    await B.render(html, "out/discodiwali/stall_call/story_brand.png", W, H, elements=els, containers=("tag", "c1", "c2", "c3", "pill"), text_pairs=text_pairs, page_bg="#000",
                   bleed_tags=("plate", "lights"), crop_tags=("plate",),
                   collision_ignore=[("h1b", "tag"), ("h2", "tag"), ("spark", "tag"), ("star", "tag"), ("h2", "star"), ("tagword", "tag"), ("h1a", "title"), ("h1a", "badge")])
    print("done")
asyncio.run(main())
