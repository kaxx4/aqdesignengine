"""NEW red COPPER stickers for the DJ poster (user, 2026-10-23: "make mew stickers", after "i want the red textured branded stickers like the mask, sparkle and heart").

Same surface as dd_copper's heart, star and diya: the fill IS the photographed copper mask (copper_texture.jpg, mirror-tiled), clipped to a new silhouette, with a pearl-bead rim, a dark inner
edge and a diagonal glint. New silhouettes, all DJ: headphones, vinyl record, music notes, lightning bolt, disco ball. Built on dd_copper._defs/_metal so the metal stays ONE recipe.
NO drop shadow (user, 2026-10-23: "remove the shadow and shade"). Each function returns ONE inline <svg>, size x size, rotation BAKED IN (do not rotate the wrapper too:
layout.double_rotation_scan). `u` keeps ids unique per sticker. Declare (label, x, y, size, size).
CLI: PYTHONIOENCODING=utf-8 python scratchpad/dd_dj_copper.py  -> transparent 3x PNGs in sample_outputs/disco_diwali_copper_dj_stickers/"""
import asyncio, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dd_copper as cp

ROOT = cp.ROOT


def _wrap(u, size, rot, d, trim=.93, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 400 400" style="display:block;overflow:visible">{cp._defs(u)}'
            f'<g transform="rotate({rot} 200 200)">{cp._metal(u, d, 400, 400, trim, 200, 200)}{extra}</g></svg>')


# headphones: an arch band and two ear cups, one compound outline (the overlaps read as the cups clamping the band)
HEADPHONES = ("M48 214 C48 100 120 38 200 38 C280 38 352 100 352 214 L292 214 C292 130 252 98 200 98 C148 98 108 130 108 214 Z "   # a thick band centred on each cup (v1 had a thin band and boxy cups: a padlock)
              "M28 250 Q28 206 78 206 Q128 206 128 250 V330 Q128 374 78 374 Q28 374 28 330 Z "
              "M272 250 Q272 206 322 206 Q372 206 372 250 V330 Q372 374 322 374 Q272 374 272 330 Z")
# vinyl: a disc with a centre hole (the hole winds the other way, so the clip leaves it empty)
VINYL = ("M200 20 A180 180 0 1 1 200 380 A180 180 0 1 1 200 20 Z "
         "M200 166 A34 34 0 1 0 200 234 A34 34 0 1 0 200 166 Z")
# music notes: two heads, two stems and a beam
NOTES = ("M60 310 A52 38 0 1 1 164 310 A52 38 0 1 1 60 310 Z M148 310 V96 H176 V310 Z "
         "M226 270 A52 38 0 1 1 330 270 A52 38 0 1 1 226 270 Z M302 270 V62 H330 V270 Z "
         "M148 96 L330 56 V122 L148 162 Z")
BOLT = "M232 14 L88 218 H178 L142 386 L322 150 H226 Z"
# disco ball: a sphere with a hanging cap
BALL = ("M200 62 A158 158 0 1 1 200 378 A158 158 0 1 1 200 62 Z M178 20 H222 V66 H178 Z")

FACETS = "".join(f'<path d="{d}" fill="none" stroke="#3A0F06" stroke-opacity=".6" stroke-width="5"/>' for d in (
    "M60 150 H340", "M44 220 H356", "M60 290 H340", "M200 66 V378"))     # a cross-hatch of 3 latitudes and 1 meridian; curved meridians over the filigree read as noise


def headphones(size=200, rot=0, u="chp"):
    return _wrap(u, size, rot, HEADPHONES, .94)


def vinyl(size=200, rot=0, u="cvn"):
    grooves = "".join(f'<circle cx="200" cy="200" r="{r}" fill="none" stroke="#3A0F06" stroke-opacity=".5" stroke-width="3"/>' for r in (62, 92, 122, 152))
    return _wrap(u, size, rot, VINYL, .93, grooves)


def notes(size=200, rot=0, u="cnt"):
    return _wrap(u, size, rot, NOTES, .95)


def bolt(size=200, rot=0, u="cbl"):
    return _wrap(u, size, rot, BOLT, .93)


def discoball(size=200, rot=0, u="cdb"):
    return _wrap(u, size, rot, BALL, .93, FACETS)


SET = {"headphones": headphones, "vinyl": vinyl, "notes": notes, "bolt": bolt, "discoball": discoball}


async def export():
    from playwright.async_api import async_playwright
    out = os.path.join(ROOT, "sample_outputs", "disco_diwali_copper_dj_stickers")
    os.makedirs(out, exist_ok=True)
    async with async_playwright() as pw:
        br = await pw.chromium.launch()
        pg = await br.new_page(viewport={"width": 520, "height": 520}, device_scale_factor=3)
        for name, fn in SET.items():
            await pg.set_content(f'<html><body style="margin:0;background:transparent"><div id="s" style="position:absolute;left:60px;top:60px">{fn(400, 0, u=name)}</div></body></html>')
            await pg.locator("#s svg").screenshot(path=os.path.join(out, f"{name}.png"), omit_background=True)
            print("sticker", name)
        await br.close()
    print("copper dj stickers ->", out)


if __name__ == "__main__":
    asyncio.run(export())
