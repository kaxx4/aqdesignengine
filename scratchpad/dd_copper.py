"""Red COPPER METAL stickers for Disco Diwali whose surface IS the photographed copper mask: the fill is a mirror-tiled patch cut from engine/assets/disco_diwali/mask_copper.png
(copper_texture.jpg: its beaded filigree and glitter), clipped to a new silhouette, with a pearl-bead rim like the mask's own edge and a soft glint. Three pieces so a carousel stops
repeating the mask: heart (charity), star (date), diya (location, the flame is drawn). Each function returns ONE inline <svg>, rotation BAKED IN (do not rotate the wrapper too:
layout.double_rotation_scan). Ids carry a suffix so two stickers never share a clip. v1 of this module drew the metal as flat vector gradients and the user said "make the sticker look
like the mask": a vector can imitate colour but not the mask's photographed bead-and-filigree surface, so the surface is now borrowed from the mask itself.
"""
import base64, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TEX = None


def tex():
    global _TEX
    if _TEX is None:
        _TEX = "data:image/jpeg;base64," + base64.b64encode(open(os.path.join(ROOT, "engine", "assets", "disco_diwali", "copper_texture.jpg"), "rb").read()).decode()
    return _TEX


def _sh(u, shadow):
    return f' filter="url(#ds{u})"' if shadow else ""


def _defs(u):
    return (f'<defs><linearGradient id="tr{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFE8D8"/><stop offset=".5" stop-color="#EDA070"/><stop offset="1" stop-color="#8A3216"/></linearGradient>'
            f'<linearGradient id="gl{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<filter id="ds{u}" x="-20%" y="-20%" width="150%" height="160%"><feDropShadow dx="0" dy="14" stdDeviation="14" flood-color="#000" flood-opacity=".65"/></filter></defs>')


def _metal(u, d, vb_w, vb_h, trim_scale=.93, cx=None, cy=None):
    """Mask texture clipped to path d, a dark inner edge, a bead rim (pearl dots) just inside the outline, and a diagonal glint."""
    cx = vb_w / 2 if cx is None else cx; cy = vb_h / 2 if cy is None else cy
    sc = f"translate({cx} {cy}) scale({trim_scale}) translate({-cx} {-cy})"
    return (f'<clipPath id="cp{u}"><path d="{d}"/></clipPath>'
            f'<g clip-path="url(#cp{u})"><image href="{tex()}" x="0" y="0" width="{vb_w}" height="{vb_h}" preserveAspectRatio="xMidYMid slice"/>'
            f'<path d="{d}" fill="url(#gl{u})" transform="translate({cx} {cy}) scale(.96 .6) translate({-cx} {-cy - 60})"/></g>'
            f'<path d="{d}" fill="none" stroke="#3A0F06" stroke-opacity=".55" stroke-width="14" stroke-linejoin="round" clip-path="url(#cp{u})"/>'
            f'<path d="{d}" fill="none" stroke="url(#tr{u})" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="#FFEBDD" stroke-width="11" stroke-dasharray="0 15" stroke-linecap="round" transform="{sc}"/>'
            f'<path d="{d}" fill="none" stroke="#9C3A1A" stroke-width="3" stroke-dasharray="0 15" stroke-dashoffset="-1.5" stroke-linecap="round" transform="{sc}" opacity=".7"/>')


def heart(size=380, rot=0, u="h", shadow=True):
    d = "M200 336 C62 240 18 164 18 106 C18 52 62 16 114 16 C154 16 186 38 200 74 C214 38 246 16 286 16 C338 16 382 52 382 106 C382 164 338 240 200 336 Z"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{round(size * .9)}" viewBox="0 0 400 360" style="display:block;overflow:visible">{_defs(u)}'
            f'<g transform="rotate({rot} 200 180)"{_sh(u, shadow)}>{_metal(u, d, 400, 360, .92, 200, 176)}</g></svg>')


def star(size=340, rot=0, u="s", shadow=True):
    d = "M200 6 C214 122 278 186 394 200 C278 214 214 278 200 394 C186 278 122 214 6 200 C122 186 186 122 200 6 Z"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 400 400" style="display:block;overflow:visible">{_defs(u)}'
            f'<g transform="rotate({rot} 200 200)"{_sh(u, shadow)}>{_metal(u, d, 400, 400, .88)}</g></svg>')


def diya(size=420, rot=0, u="d", shadow=True):
    bowl = "M16 152 C16 252 98 312 232 312 C366 312 448 252 448 152 C406 172 334 180 232 180 C130 180 58 172 16 152 Z"
    lip = "M440 150 C470 126 490 100 498 72 C490 108 478 142 450 176 Z"
    flame = "M234 118 C194 76 214 38 234 4 C258 42 276 78 234 118 Z"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{round(size * .72)}" viewBox="0 0 500 330" style="display:block;overflow:visible">{_defs(u)}'
            f'<defs><linearGradient id="fl{u}" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#E8431A"/><stop offset=".55" stop-color="#FF9A2E"/><stop offset="1" stop-color="#FFE9A0"/></linearGradient>'
            f'<filter id="fg{u}" x="-80%" y="-60%" width="260%" height="220%"><feGaussianBlur stdDeviation="9"/></filter></defs>'
            f'<g transform="rotate({rot} 250 165)"><g{_sh(u, shadow)}>'
            f'<path d="{lip}" fill="#A33C1C" stroke="url(#tr{u})" stroke-width="8" stroke-linejoin="round"/>{_metal(u, bowl, 500, 330, .93, 232, 246)}</g>'
            f'<ellipse cx="232" cy="156" rx="214" ry="30" fill="#7A2A12" stroke="url(#tr{u})" stroke-width="7"/><ellipse cx="232" cy="160" rx="176" ry="17" fill="#2E0C05"/><ellipse cx="232" cy="156" rx="150" ry="10" fill="#C2641E" opacity=".85"/>'
            f'<g transform="translate(0 22)"><path d="{flame}" fill="#FF9A2E" opacity=".55" filter="url(#fg{u})"/><path d="{flame}" fill="url(#fl{u})"/></g></g></svg>')


def calendar(size=360, rot=0, u="c", shadow=True):
    """Copper desk calendar: mask-texture page, a darker header band, two binder rings, a grid of pearl 'days' and one gem for the day."""
    d = "M40 70 H360 Q380 70 380 90 V340 Q380 360 360 360 H40 Q20 360 20 340 V90 Q20 70 40 70 Z"
    beads = "".join(f'<circle cx="{110 + c * 62}" cy="{196 + r * 56}" r="10" fill="#FFEBDD" stroke="#7A2A12" stroke-width="3"/>' for r in range(3) for c in range(4) if (r, c) != (1, 2))
    ring = lambda x: (f'<rect x="{x}" y="22" width="26" height="76" rx="13" fill="url(#tr{u})" stroke="#5A180B" stroke-width="4"/>'
                      f'<rect x="{x + 7}" y="34" width="12" height="40" rx="6" fill="#2E0C05" opacity=".75"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 400 400" style="display:block;overflow:visible">{_defs(u)}'
            f'<defs><radialGradient id="gem{u}" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#FFEADF"/><stop offset=".35" stop-color="#FF7A5A"/><stop offset="1" stop-color="#6A1208"/></radialGradient></defs>'
            f'<g transform="rotate({rot} 200 200)"{_sh(u, shadow)}>{_metal(u, d, 400, 400, .93, 200, 215)}'
            f'<path d="M40 70 H360 Q380 70 380 90 V132 H20 V90 Q20 70 40 70 Z" fill="#3A0F06" opacity=".62"/>'
            f'<path d="M20 132 H380" stroke="url(#tr{u})" stroke-width="6"/>{beads}'
            f'<circle cx="234" cy="252" r="27" fill="url(#gem{u})" stroke="url(#tr{u})" stroke-width="6"/>{ring(112)}{ring(262)}</g></svg>')


def pin(size=340, rot=0, u="p", shadow=True):
    """Copper map pin: mask-texture teardrop, a pearl ring round a gem 'hole'."""
    d = "M200 388 C200 388 56 246 56 150 C56 70 118 12 200 12 C282 12 344 70 344 150 C344 246 200 388 200 388 Z"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 400 400" style="display:block;overflow:visible">{_defs(u)}'
            f'<defs><radialGradient id="gem{u}" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#FFEADF"/><stop offset=".35" stop-color="#FF7A5A"/><stop offset="1" stop-color="#6A1208"/></radialGradient></defs>'
            f'<g transform="rotate({rot} 200 200)"{_sh(u, shadow)}>{_metal(u, d, 400, 400, .9, 200, 170)}'
            f'<circle cx="200" cy="150" r="66" fill="#2E0C05" stroke="url(#tr{u})" stroke-width="8"/>'
            f'<circle cx="200" cy="150" r="66" fill="none" stroke="#FFEBDD" stroke-width="9" stroke-dasharray="0 14" stroke-linecap="round" transform="translate(200 150) scale(.84) translate(-200 -150)"/>'
            f'<circle cx="200" cy="150" r="34" fill="url(#gem{u})" stroke="url(#tr{u})" stroke-width="6"/></g></svg>')


def stall(size=420, rot=0, u="t", shadow=True):
    """Copper market stall (for the stalls group): a scalloped awning with dark stripes, two posts, a beaded counter and three gem jars on it. Surface is the mask's own copper texture."""
    n, w0 = 5, 92.8
    awn = "M70 30 H430 L482 150 " + "".join(f"A{w0 / 2} 40 0 0 1 {482 - w0 * (i + 1):.1f} 150 " for i in range(n)) + "L70 30 Z"
    bands = "".join(f'<rect x="{18 + w0 * i:.1f}" y="20" width="{w0 / 2:.1f}" height="190" fill="#3A0F06" opacity=".62"/>' for i in range(n))
    post = lambda x, k: (f'<rect x="{x}" y="170" width="24" height="190" rx="6" fill="url(#tr{u})" stroke="#3A0F06" stroke-width="5"/>'
                         f'<rect x="{x + 8}" y="180" width="8" height="165" rx="4" fill="#2E0C05" opacity=".6"/>')
    counter = "M16 300 H484 Q500 300 500 316 V372 Q500 388 484 388 H16 Q0 388 0 372 V316 Q0 300 16 300 Z"
    beads = "".join(f'<circle cx="{40 + i * 52}" cy="346" r="9" fill="#FFEBDD" stroke="#7A2A12" stroke-width="3"/>' for i in range(9))
    jars = "".join(f'<g transform="translate({x} 0)"><rect x="-22" y="250" width="44" height="50" rx="12" fill="#2E0C05" stroke="url(#tr{u})" stroke-width="5"/><circle cx="0" cy="274" r="13" fill="url(#gem{u})" stroke="url(#tr{u})" stroke-width="3"/></g>' for x in (170, 250, 330))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{round(size * .82)}" viewBox="0 0 500 410" style="display:block;overflow:visible">{_defs(u)}'
            f'<defs><radialGradient id="gem{u}" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#FFEADF"/><stop offset=".35" stop-color="#FF7A5A"/><stop offset="1" stop-color="#6A1208"/></radialGradient></defs>'
            f'<g transform="rotate({rot} 250 205)"{_sh(u, shadow)}>{post(52, 1)}{post(424, 2)}'
            f'{_metal(u + "c", counter, 500, 410, .93, 250, 344)}{beads}{jars}'
            f'{_metal(u, awn, 500, 410, .93, 250, 90)}<clipPath id="ab{u}"><path d="{awn}"/></clipPath><g clip-path="url(#ab{u})">{bands}</g></g></svg>')


def cupcake(size=380, rot=0, u="k", shadow=True):
    """Copper cupcake (a dessert stall): pleated wrapper, a swirled frosting blob and a gem cherry, all in the mask's copper texture."""
    wrap = "M104 226 H296 L266 372 Q263 388 247 388 H153 Q137 388 134 372 Z"
    frost = "M62 232 C42 194 84 172 120 180 C106 136 154 108 192 128 C208 84 270 88 278 134 C322 126 346 172 314 198 C346 210 340 232 312 232 Z"
    pleats = "".join(f'<path d="M{x1} 236 L{x2} 380" stroke="#3A0F06" stroke-opacity=".55" stroke-width="6" stroke-linecap="round"/>' for x1, x2 in ((140, 156), (176, 183), (212, 217), (248, 241)))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 400 400" style="display:block;overflow:visible">{_defs(u)}'
            f'<defs><radialGradient id="gem{u}" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#FFEADF"/><stop offset=".35" stop-color="#FF7A5A"/><stop offset="1" stop-color="#6A1208"/></radialGradient></defs>'
            f'<g transform="rotate({rot} 200 200)"{_sh(u, shadow)}>{_metal(u + "w", wrap, 400, 400, .92, 200, 310)}<path d="{wrap}" fill="#3A0F06" opacity=".38"/>{pleats}'
            f'{_metal(u, frost, 400, 400, .9, 190, 170)}'
            f'<path d="M200 70 C206 48 220 36 236 34" fill="none" stroke="url(#tr{u})" stroke-width="7" stroke-linecap="round"/>'
            f'<circle cx="200" cy="82" r="30" fill="url(#gem{u})" stroke="url(#tr{u})" stroke-width="6"/></g></svg>')
