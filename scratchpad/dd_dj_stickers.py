"""Disco Diwali DJ STICKER SET, drawn here (user, 2026-10-23: "make your own stickers and use them"): headphones, vinyl record, music notes, lightning bolt, equalizer.

Style: flat gold and copper art with a 7px ink outline, and a die-cut OFF-WHITE border grown from the art's own alpha (feMorphology dilate), like a real peel-off sticker. NO drop shadow
(user, 2026-10-23: "remove the shadow and shade"). The palette is the format's: gold (#F0C65A / #C9971C / #A8721A), copper (#E07A4B / #8A3216), ink, off-white. Each function returns ONE
inline <svg>, rotation BAKED IN (do not rotate the wrapper too: layout.double_rotation_scan). `u` makes ids unique so two stickers never share a gradient or filter.
Every sticker's declared box is its svg box: width == height == `size` (declare (label, x, y, size, size), CLAUDE.md sec 9), the die-cut border stays inside it.
CLI: PYTHONIOENCODING=utf-8 python scratchpad/dd_dj_stickers.py  -> transparent 3x PNGs in sample_outputs/disco_diwali_dj_stickers/"""
import asyncio, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INK, OFF = "#0A0A0A", "#F2F2F2"
OUTLINE = f'stroke="{INK}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"'


def _defs(u):
    return (f'<defs>'
            f'<linearGradient id="g{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF1B8"/><stop offset=".35" stop-color="#F0C65A"/><stop offset=".7" stop-color="#C9971C"/><stop offset="1" stop-color="#A8721A"/></linearGradient>'
            f'<linearGradient id="c{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F29A6A"/><stop offset=".55" stop-color="#C85A2E"/><stop offset="1" stop-color="#7A2A12"/></linearGradient>'
            # the die-cut: dilate the art's alpha, paint it off-white, put the art back on top
            f'<filter id="d{u}" x="-12%" y="-12%" width="124%" height="124%" color-interpolation-filters="sRGB"><feMorphology in="SourceAlpha" operator="dilate" radius="13" result="fat"/>'
            f'<feGaussianBlur in="fat" stdDeviation="1.2" result="soft"/><feFlood flood-color="{OFF}"/><feComposite in2="soft" operator="in" result="cut"/>'
            f'<feMerge><feMergeNode in="cut"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>')


def _wrap(u, size, rot, art, vb=400):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {vb} {vb}" style="display:block;overflow:visible">{_defs(u)}'
            f'<g filter="url(#d{u})"><g transform="rotate({rot} {vb / 2} {vb / 2})">{art}</g></g></svg>')


def headphones(size=200, rot=0, u="hp"):
    band = "M78 232 V196 C78 112 130 62 200 62 C270 62 322 112 322 196 V232"
    art = (f'<path d="{band}" fill="none" stroke="{INK}" stroke-width="48" stroke-linecap="round"/>'
           f'<path d="{band}" fill="none" stroke="url(#g{u})" stroke-width="34" stroke-linecap="round"/>'
           f'<path d="M68 196 C70 118 124 56 200 54" fill="none" stroke="#FFF8DC" stroke-width="7" stroke-linecap="round" opacity=".7"/>'   # on the band (x 61..95), not floating in the hollow
           # ear cups: copper shells, gold rims, dark cushions
           + "".join(f'<g><rect x="{x}" y="204" width="86" height="148" rx="38" fill="url(#c{u})" {OUTLINE}/>'
                     f'<rect x="{x + 12}" y="222" width="62" height="112" rx="28" fill="url(#g{u})" {OUTLINE}/>'
                     f'<ellipse cx="{x + 43}" cy="278" rx="19" ry="33" fill="#2A0E06" {OUTLINE}/></g>' for x in (46, 268)))
    return _wrap(u, size, rot, art)


def vinyl(size=200, rot=0, u="vn"):
    rings = "".join(f'<circle cx="200" cy="200" r="{r}" fill="none" stroke="#3A3A3A" stroke-width="3"/>' for r in (176, 154, 132, 110, 92))
    art = (f'<circle cx="200" cy="200" r="190" fill="#141414" {OUTLINE}/>{rings}'
           f'<path d="M200 200 L300 40 A190 190 0 0 1 372 150 Z" fill="#fff" opacity=".1"/><path d="M200 200 L100 360 A190 190 0 0 1 28 250 Z" fill="#fff" opacity=".1"/>'
           f'<circle cx="200" cy="200" r="72" fill="url(#g{u})" {OUTLINE}/>'
           f'<path d="M200 150 C206 184 216 194 250 200 C216 206 206 216 200 250 C194 216 184 206 150 200 C184 194 194 184 200 150 Z" fill="url(#c{u})" {OUTLINE}/>'
           f'<circle cx="200" cy="200" r="11" fill="{INK}"/>')
    art = f'<g transform="translate(200 200) scale(.9) translate(-200 -200)">{art}</g>'     # leave room inside the box for the die-cut border (v1 clipped it at the svg edge)
    return _wrap(u, size, rot, art)


def notes(size=200, rot=0, u="nt"):
    head = lambda cx, cy: f'<ellipse cx="{cx}" cy="{cy}" rx="52" ry="38" transform="rotate(-24 {cx} {cy})" fill="url(#c{u})" {OUTLINE}/>'
    art = (f'<path d="M150 296 V104 L318 66 V258" fill="none" stroke="{INK}" stroke-width="40" stroke-linecap="butt" stroke-linejoin="miter"/>'
           f'<path d="M150 296 V104 L318 66 V258" fill="none" stroke="url(#g{u})" stroke-width="26" stroke-linejoin="miter"/>'
           f'<path d="M150 104 L318 66 V128 L150 166 Z" fill="url(#g{u})" {OUTLINE}/>'
           + head(110, 304) + head(278, 266))
    return _wrap(u, size, rot, art)


def bolt(size=200, rot=0, u="bl"):
    art = (f'<path d="M232 14 L88 218 H178 L142 386 L322 150 H226 Z" fill="url(#g{u})" {OUTLINE}/>'
           f'<path d="M226 52 L128 196" fill="none" stroke="#FFF8DC" stroke-width="9" stroke-linecap="round" opacity=".8"/>')
    return _wrap(u, size, rot, art)


def equalizer(size=200, rot=0, u="eq"):
    bars = ((40, 110), (110, 230), (180, 320), (250, 190), (320, 270))     # (x, height); bars grow from y=360
    art = "".join(f'<rect x="{x}" y="{360 - h}" width="52" height="{h}" rx="20" fill="url(#{"g" if i % 2 == 0 else "c"}{u})" {OUTLINE}/>'
                  f'<rect x="{x + 11}" y="{360 - h + 18}" width="9" height="{max(24, h - 54)}" rx="4" fill="#fff" opacity=".35"/>' for i, (x, h) in enumerate(bars))
    return _wrap(u, size, rot, art)


SET = {"headphones": headphones, "vinyl": vinyl, "notes": notes, "bolt": bolt, "equalizer": equalizer}


async def export():
    from playwright.async_api import async_playwright
    out = os.path.join(ROOT, "sample_outputs", "disco_diwali_dj_stickers")
    os.makedirs(out, exist_ok=True)
    async with async_playwright() as pw:
        br = await pw.chromium.launch()
        pg = await br.new_page(viewport={"width": 520, "height": 520}, device_scale_factor=3)
        for name, fn in SET.items():
            await pg.set_content(f'<html><body style="margin:0;background:transparent"><div id="s" style="position:absolute;left:60px;top:60px">{fn(400, 0, u=name)}</div></body></html>')
            await pg.locator("#s svg").screenshot(path=os.path.join(out, f"{name}.png"), omit_background=True)
            print("sticker", name)
        await br.close()
    print("stickers ->", out)


if __name__ == "__main__":
    asyncio.run(export())
