"""DISCO DIWALI "text selection" carousel + static (user inspo, 2026-10-11): a full-bleed photo with an iOS text-selection overlay:
a context-menu pill (Copy | Select All | Look Up >), one sentence set in white, part of it highlighted blue with drag handles.
Dressed in TerraThon: cream/orchid menu pill, shuriken-free (the photo carries it), real DD photos, logo in a cream pill (photo rule).
Teaser: no tickets, date, venue or price. Photos are 1500x1000 landscape, so the story's 9:16 crop is soft (flagged).
Carousel (4 slides): 1 dance / 2 group / 3 decor blocks / 4 closer. Static: decor arch.  Feed 1080x1350, story 1080x1920.
Run: PYTHONIOENCODING=utf-8 python scratchpad/tt_dd_select.py [story]  -> out/collaterals/dd_select[_story]/
"""
import asyncio, base64, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sp = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(sp); sp.loader.exec_module(tt)
core, B, W = tt.core, tt.B, tt.W
ORCHID, CTA_FILL, INK, WHITE = tt.ORCHID, tt.CTA_FILL, tt.INK, tt.WHITE
STORY = len(sys.argv) > 1 and sys.argv[1] == "story"
H = 1920 if STORY else 1350
OY = 200 if STORY else 0
FOOT = 270 if STORY else 0
SKY = "#3DA9FC"
SEL = "rgba(61,169,252,.5)"
PH = {n: "data:image/jpeg;base64," + base64.b64encode(open(f"engine/assets/terrathon/dd_photos/{n}.jpg", "rb").read()).decode() for n in ("dance", "decor", "group")}
FS, LH, PITCH = 60, 78, 98          # type size, highlight box height, line pitch

SLIDES = {  # key: photo, bg-position, lines (list of segments (text, selected)), menu items, footer
    "1": ("dance", "55% 40%", [[("The dance floor is our love", True)], [("language,", True), (" from first song to last.", False)]], ["Copy", "Select All", "Look Up"], None),
    "2": ("group", "45% 40%", [[("Dress up. Show up.", True)], [("Then dance till late.", False)]], ["Copy", "Select All", "Look Up"], None),
    "3": ("decor", "88% 55%", [[("Balls, blocks and a cassette,", True)], [("built for one night.", False)]], ["Copy", "Select All", "Look Up"], None),
    "4": ("dance", "10% 60%", [[("Disco Diwali", True), (" is coming.", False)], [("Save this post.", False)]], ["Copy", "Select All", "Look Up"], "STAY TUNED"),
    "static": ("decor", "40% 50%", [[("Disco Diwali is our love", True)], [("language,", True), (" from first song to last.", False)]], ["Copy", "Select All", "Look Up"], "STAY TUNED")}


async def build(name):
    key, pos, lines, menu, cta = SLIDES[name]
    els, parts = [], []
    # photo + scrim
    parts.append(f'<div style="position:absolute;inset:0;background:url({PH[key]}) {pos}/cover no-repeat;z-index:0"></div>')
    parts.append('<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.66) 0%,rgba(0,0,0,.38) 38%,rgba(0,0,0,.14) 62%,rgba(0,0,0,.58) 100%);z-index:1"></div>')
    # menu pill
    mx_w, mh, my = 600, 84, 170 + OY
    mx = (W - mx_w) / 2
    cells = "".join(f'<div style="flex:1;height:100%;display:flex;align-items:center;justify-content:center;font-family:var(--e);font-weight:600;font-size:34px;color:{INK};{"border-left:3px solid rgba(10,10,10,.14);" if i else ""}white-space:nowrap">{t}</div>' for i, t in enumerate(menu))
    chev = f'<div style="width:78px;height:100%;display:flex;align-items:center;justify-content:center;border-left:3px solid rgba(10,10,10,.14)"><svg width="22" height="34" viewBox="0 0 22 34" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5,5 L17,17 L5,29"/></svg></div>'
    parts.append(f'<div class="measure" data-tag="menu" style="position:absolute;left:{mx}px;top:{my}px;width:{mx_w}px;height:{mh}px;box-sizing:border-box;border:5px solid {ORCHID};border-radius:999px;background:{CTA_FILL};display:flex;overflow:hidden;z-index:6">{cells}{chev}</div>')
    parts.append(f'<div style="position:absolute;left:{W / 2 - 22}px;top:{my + mh - 3}px;width:0;height:0;border-left:22px solid transparent;border-right:22px solid transparent;border-top:26px solid {ORCHID};z-index:5"></div>'
                 f'<div style="position:absolute;left:{W / 2 - 15}px;top:{my + mh - 9}px;width:0;height:0;border-left:15px solid transparent;border-right:15px solid transparent;border-top:18px solid {CTA_FILL};z-index:7"></div>')
    els.append(("menu", mx, my, mx_w, mh + 26))
    # selected text block
    segs = [t for ln in lines for t, _ in ln]
    meas = await B.measure_text([dict(text=t, font="e", size=FS, weight=400) for t in segs], extra_css=tt.FONT_CSS)
    X0, Y0 = 90, my + mh + 130
    k = 0
    first = last = None
    for li, ln in enumerate(lines):
        x = X0; y = Y0 + li * PITCH
        html = ""
        for t, sel in ln:
            w = meas[k]["text_w"]; k += 1
            if sel:
                if first is None: first = (x, y)
                last = (x + w, y)
                html += f'<span style="display:inline-block;height:{LH}px;line-height:{LH}px;background:{SEL};white-space:pre">{t}</span>'
            else:
                html += f'<span style="display:inline-block;height:{LH}px;line-height:{LH}px;white-space:pre">{t}</span>'
            x += w
        parts.append(f'<div class="measure" data-tag="ln{li}" style="position:absolute;left:{X0}px;top:{y}px;height:{LH}px;font-family:var(--e);font-weight:400;font-size:{FS}px;color:{WHITE};white-space:pre;z-index:6;text-shadow:0 2px 12px rgba(0,0,0,.35)">{html}</div>')
        els.append((f"ln{li}", X0, y, x - X0, LH))
    # handles: bar + dot, start (top-left of first selection) and end (bottom-right of last)
    fx, fy = first; lx, ly = last
    parts.append(f'<div style="position:absolute;left:{fx - 2}px;top:{fy}px;width:5px;height:{LH}px;background:{SKY};border-radius:3px;z-index:7"></div>'
                 f'<div style="position:absolute;left:{fx - 14}px;top:{fy - 24}px;width:26px;height:26px;border-radius:50%;background:{SKY};z-index:7"></div>')
    parts.append(f'<div style="position:absolute;left:{lx - 2}px;top:{ly}px;width:5px;height:{LH}px;background:{SKY};border-radius:3px;z-index:7"></div>'
                 f'<div style="position:absolute;left:{lx - 11}px;top:{ly + LH - 2}px;width:26px;height:26px;border-radius:50%;background:{SKY};z-index:7"></div>')
    # footer: logo in a cream pill (photo rule) + index or CTA
    fy2 = H - FOOT - 27 - 76
    parts.append(f'<div class="measure" data-tag="logo" style="position:absolute;left:27px;top:{fy2}px;height:76px;padding:0 24px;box-sizing:border-box;border:5px solid {ORCHID};border-radius:999px;background:{CTA_FILL};display:flex;align-items:center;z-index:9"><img src="{core.LOGO}" style="height:40px"></div>')
    els.append(("logo", 27, fy2, 330, 76))
    cw, ch = (330, 70) if cta else (150, 54)
    cx, cy = W - 27 - cw, H - FOOT - 27 - ch
    lab = cta or (f"{int(name):02d} / 04" if name.isdigit() else "")
    if lab:
        parts.append(f'<div class="measure" data-tag="cta" style="position:absolute;left:{cx}px;top:{cy}px;width:{cw}px;height:{ch}px;box-sizing:border-box;border:5px solid {ORCHID};border-radius:999px;background:{CTA_FILL};display:flex;align-items:center;justify-content:center;font-family:var(--d);font-weight:900;font-size:{28 if cta else 24}px;color:{INK};z-index:9">{lab}</div>')
        els.append(("cta", cx, cy, cw, ch))
    return B.page(W, H, "#000", f'<style>{tt.FONT_CSS}</style>' + "".join(parts), grain=False), els


async def main():
    outdir = "out/collaterals/dd_select" + ("_story" if STORY else ""); os.makedirs(outdir, exist_ok=True)
    async with B.session():
        for name in SLIDES:
            html, els = await build(name)
            out = f"{outdir}/dd_select_{name}.png"
            await B.render(html, out, W, H, elements=els, page_bg="#000", expect_hero=False, margin=12, collision_ignore={("menu", "ln0")})
            print("done", out)

asyncio.run(main())
