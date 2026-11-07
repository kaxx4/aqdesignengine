"""Shared BLUE DIYA GROUND for the A3 signs (user, 2026-11-07: 'change the shades in all the A3 signs to the blue shadows like in the special invitation poster').
Portrait (1080 x <=1527): the approved plate bg_diya_portrait.jpg, stacked with a flipped, faded-in second copy when the canvas is taller than the plate (engine format rule 8).
Landscape: there is no landscape diya plate in the engine, so one is DERIVED from the real plate's own clusters (engine/assets/disco_diwali/bg_diya_landscape.jpg, built once):
the top-right cluster mirrored to the top-left, the lower-left cluster mirrored to the lower-right, black centre kept. Same pixels as the portrait plate, never redrawn."""
import os
from PIL import Image, ImageChops, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "engine", "assets", "disco_diwali")
LAND = os.path.join(A, "bg_diya_landscape.jpg")


def build_landscape(force=False):
    if os.path.exists(LAND) and not force:
        return LAND
    P = Image.open(os.path.join(A, "bg_diya_portrait.jpg")).convert("RGB")      # 1600 x 2000
    W, H = 2400, 1700
    C = Image.new("RGB", (W, H), (0, 0, 0))
    import numpy as np
    def feathered(img, left=0, right=0, topf=0, bottom=0):
        """Fade the named edges of a crop to black over the given pixels, so it dissolves into the black ground instead of ending in a hard line."""
        a = np.asarray(img).astype(float); h, w = a.shape[:2]
        m = np.ones((h, w))
        ramp = lambda n: np.linspace(0, 1, n) ** 1.5
        if left: m[:, :left] *= ramp(left)[None, :]
        if right: m[:, w - right:] *= ramp(right)[::-1][None, :]
        if topf: m[:topf, :] *= ramp(topf)[:, None]
        if bottom: m[h - bottom:, :] *= ramp(bottom)[::-1][:, None]
        return Image.fromarray((a * m[..., None]).astype("uint8"))
    top = feathered(P.crop((560, 0, 1600, 620)), left=300, bottom=140)          # the top-right cluster
    bot = feathered(P.crop((0, 1330, 1040, 2000)), right=300, topf=200)         # the bottom-left cluster + the bottom edge row
    def put(img, x, y):
        nonlocal C
        layer = Image.new("RGB", (W, H), (0, 0, 0)); layer.paste(img, (x, y)); C = ImageChops.lighter(C, layer)
    put(top, W - 1040, 0); put(ImageOps.mirror(top), 0, 0)
    put(bot, 0, H - 670); put(ImageOps.mirror(bot), W - 1040, H - 670)
    C.save(LAND, quality=90)
    return LAND


def ground(dd, W, H, lights_x=None):
    """HTML for the ground: black, the diya plate, string lights, gold dust, grain. `dd` is the loaded discodiwali module (for dd.uri)."""
    P = ['<div data-tag="plate" style="position:absolute;inset:0;z-index:0;background:#000"></div>']
    if W > H:
        P.append(f'<img data-tag="plate" src="{dd.photo_uri(build_landscape(), 2400)}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1">')
    else:
        base = min(H, 1350)
        P.append(f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:0;width:{W}px;height:{base}px;object-fit:cover;z-index:1">')
        if H > 1350:
            P.append(f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:{H - 1350}px;width:{W}px;height:1350px;object-fit:cover;z-index:1;'
                     'transform:scaleY(-1);-webkit-mask-image:linear-gradient(to top,transparent 0%,#000 45%);mask-image:linear-gradient(to top,transparent 0%,#000 45%)">')
    lx = (W - 1300) if lights_x is None else lights_x
    P += [f'<img data-tag="lights" src="{dd.uri("string_lights.png")}" style="position:absolute;left:{lx}px;top:-60px;width:1150px;z-index:5">',
          f'<img data-tag="plate" src="{dd.uri("sparkles.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:30;mix-blend-mode:screen;opacity:.5;pointer-events:none">',
          f'<img data-tag="plate" src="{dd.uri("grain.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:31;mix-blend-mode:screen;opacity:.3;pointer-events:none">']
    return "".join(P)


if __name__ == "__main__":
    print(build_landscape(force=True))
