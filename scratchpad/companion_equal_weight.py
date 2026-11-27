"""Companion art piece (CLAUDE.md standing rule) for the Shikshaq format work, 2026-11-27.
Philosophy: brain/companion/EQUAL_WEIGHT_PHILOSOPHY.md. Output: brain/companion/equal_weight.png
Run:  PYTHONIOENCODING=utf-8 python scratchpad/companion_equal_weight.py"""
import asyncio, os, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
import shikshaq as sk

W, H = 1620, 2025
HUES = sorted((h, s) for (h, s, l) in sk.SUBJECT_SEEDS.values())          # eight hues, ascending
LAD = [97.0, 95.0] + [93.0 - i * 67.0 / 22 for i in range(23)] + [22.0, 19.0]       # a ladder that passes EXACTLY through 93 (tint) and 26 (ink)
M, TOP, BOT = 150, 360, 250
cw = (W - 2 * M - 70) / 8.0                                                # leave a 70px axis gutter
rh = (H - TOP - BOT) / float(len(LAD))
cells, labels = [], []
for r, L in enumerate(LAD):
    y = TOP + r * rh
    mark = abs(L - 93) < .01 or abs(L - 26) < .01
    labels.append(f'<span class="ax" style="left:{M}px;top:{y + rh/2 - 8:.1f}px;{"color:#1F1F1F;font-weight:700" if mark else ""}">{round(L)}</span>')
    for c, (h, s) in enumerate(HUES):
        x = M + 70 + c * cw
        cells.append(f'<i style="left:{x:.1f}px;top:{y:.1f}px;width:{cw-7:.1f}px;height:{rh-7:.1f}px;background:{sk.hsl_to_hex(h, s, L)}"></i>')
heads = "".join(f'<span class="ax" style="left:{M + 70 + c*cw:.1f}px;top:{TOP - 44}px">{h:03d}</span>' for c, (h, s) in enumerate(HUES))
# the datum: two hairline brackets at the two rungs the idea depends on (tint and ink)
def bracket(L):
    r = min(range(len(LAD)), key=lambda i: abs(LAD[i] - L)); y = TOP + r * rh
    return f'<b class="rule" style="left:{M + 52}px;top:{y + rh/2 - 3.5:.1f}px;width:14px"></b>'
css = """
.ax{position:absolute;font-family:'Geist';font-size:15px;letter-spacing:.14em;color:#776F67;font-weight:500}
i{position:absolute;border-radius:12px;display:block}
.rule{position:absolute;height:2px;background:#1F1F1F;display:block}
.t{position:absolute;left:%dpx;top:150px;font-family:'Archivo';font-weight:200;font-stretch:125%%;font-size:64px;letter-spacing:.34em;color:#1F1F1F;text-transform:uppercase}
.s{position:absolute;left:%dpx;top:236px;font-family:'Geist';font-weight:400;font-size:17px;letter-spacing:.22em;color:#776F67;text-transform:uppercase}
.f{white-space:pre;position:absolute;left:%dpx;bottom:112px;font-family:'Geist';font-weight:400;font-size:15px;letter-spacing:.2em;color:#776F67;text-transform:uppercase}
.pl{position:absolute;right:%dpx;bottom:112px;font-family:'Archivo';font-weight:200;font-stretch:125%%;font-size:15px;letter-spacing:.3em;color:#1F1F1F}
""" % (M, M, M, M)
body = (f'<div data-tiny><div class="t">Equal Weight</div><div class="s">Eight hues, one lightness ladder</div>{heads}{"".join(labels)}{"".join(cells)}'
        f'{bracket(93)}{bracket(26)}<div class="f">h · hue    l · lightness    plate 01</div><div class="pl">Nº 8 × 27</div>')
html = sk.doc(body, kind="poster", W=W, H=H, title="Equal Weight", extra_css=css)
res = sk.render_sync(html, "brain/companion/equal_weight.png", W, H, kind="poster", scale=1)
