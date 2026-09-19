"""Recreation — sample 77e7bb34 ("AcquaSofia" two-slab poster).

MEASURED FIRST this time (compare.geometry), per the lesson from 3d846c78 where two
eyeballed proportions in the written description produced a scoring regression:

    content bbox  x 0.189..0.809   y 0.204..0.796
    margins       L 0.189  R 0.191  T 0.204  B 0.204   -> dead centred
    centroid      (0.499, 0.501)   coverage 0.355
    occupancy     two blocks: rows 2-4 (upper slab), row 5 a seam, rows 6-8 (lower)

COMPOSITION INVENTORY (acceptance checklist)
  1. deep saturated dark ground, flat, edge to edge, no texture
  2. upper slab: warm mid-tone rectangle, full content width, ~0.285H tall,
     carrying ONE chunky pixel-art motif in a light warm colour, centred
  3. a thin ground-coloured seam between the slabs (~0.015H) — the slabs do not touch
  4. lower slab: near-white rectangle, same width, ~0.29H tall, containing:
     4a. left-aligned lowercase grotesk copy, 5 short lines, generous leading
     4b. an accent-coloured url directly under the copy
     4c. top-right: a QR code  <-- NOT REPRODUCIBLE, see adaptation
     4d. bottom-right: the wordmark, small
  5. exactly four colours: ground, slab-warm, motif-light, slab-white

AQ ADAPTATION (declared)
  * the reference ground is a deep maroon. AQ has no maroon and inventing one breaks
    the palette law, so the ground is INK — a legitimate AQ ground already used by the
    ledger and swarm pieces. Warm slab -> tomato, motif -> lemon, pale slab -> cream.
  * THE QR CODE IS OMITTED. CLAUDE.md section 9: never fabricate QR codes. A fake QR
    is a fabricated asset that also happens not to scan. Replaced with the real
    handle set in mono, which is what the QR would have resolved to anyway.
  * pixel motif: the reference's jellyfish -> AQ's `sprout` (new: shapes.pixel_art)
  * copy is real: 126 return visits to one partner, Counted from the welfare CSV
"""
import asyncio, os, sys, importlib.util

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); lay = load("layout"); sh = load("shapes")

W, H = core.SIZES["feed"]
SLUG = "77e7bb34144e08"
OUT = f"out/versions/{SLUG}"
os.makedirs(OUT, exist_ok=True)
INK, CREAM = core.INK, core.CREAM
TOMATO, LEMON = core.ACCENTS[3], core.ACCENTS[2]

# MEASURED
BX0, BX1 = 0.189 * W, 0.809 * W
BY0, BY1 = 0.204 * H, 0.796 * H
CWID = BX1 - BX0
SEAM = 0.015 * H
SLAB_H = (BY1 - BY0 - SEAM) / 2

COPY = ["it's time", "to stop counting", "heads and start", "counting", "returns."]
URL = "ngoaquaterra.com"


async def main():
    els, P = [], []
    P.append(f'<div style="position:absolute;inset:0;background:{INK}"></div>')

    # ── upper slab: the pixel motif ─────────────────────────────────────────
    y1 = BY0
    motif = SLAB_H * 0.62
    P.append(f'<div style="position:absolute;left:{BX0}px;top:{y1}px;width:{CWID}px;'
             f'height:{SLAB_H}px;background:{TOMATO};z-index:4;display:flex;'
             f'align-items:center;justify-content:center">'
             f'<div style="width:{motif}px;height:{motif}px">'
             f'{sh.ink_mark(sh.pixel_art("sprout", gap=0.10), fill=LEMON, size=motif)}'
             f'</div></div>')
    els.append(("slab_top", BX0, y1, CWID, SLAB_H))

    # ── lower slab: copy, url, handle, wordmark ─────────────────────────────
    y2 = BY0 + SLAB_H + SEAM
    pad = CWID * 0.072
    fs = CWID * 0.088
    m = await B.measure_text(
        [{"text": "<br>".join(COPY), "font": "e", "size": fs, "weight": 400,
          "line_height": 1.16, "max_width": CWID - 2 * pad}])
    copy_h = m[0]["h"]

    inner = (
        f'<div style="position:absolute;left:{pad}px;top:{SLAB_H-pad*0.9-copy_h-fs*1.5}px;'
        f'width:{CWID-2*pad}px;font-family:var(--e);font-size:{fs}px;line-height:1.16;'
        f'letter-spacing:-.012em;color:{INK}">{"<br>".join(COPY)}</div>'
        f'<div style="position:absolute;left:{pad}px;bottom:{pad*0.82}px;'
        f'font-family:var(--e);font-size:{fs*0.60}px;color:{core.on_cream(TOMATO, fs*0.60)}">'
        f'{URL}</div>'
        # 4c: the reference's QR, replaced by what it would have resolved to
        f'<div style="position:absolute;right:{pad}px;top:{pad*0.9}px;'
        f'font-family:var(--m);font-weight:700;font-size:{fs*0.34}px;letter-spacing:.16em;'
        f'color:{INK};opacity:.55">@NGO.AQUATERRA</div>'
        f'<div style="position:absolute;right:{pad}px;bottom:{pad*0.82}px;'
        f'font-family:var(--d);font-weight:900;font-size:{fs*0.46}px;letter-spacing:-.01em;'
        f'color:{INK}">AquaTerra<sup style="font-size:.5em;top:-.7em;position:relative">&reg;</sup></div>')
    P.append(f'<div style="position:absolute;left:{BX0}px;top:{y2}px;width:{CWID}px;'
             f'height:{SLAB_H}px;background:{CREAM};z-index:4;overflow:hidden">{inner}</div>')
    els.append(("slab_bot", BX0, y2, CWID, SLAB_H))

    html = B.page(W, H, INK, "".join(P), grain=False)
    lay.preflight(W, H, els, html=html, page_bg=INK, core=core)
    async with B.session():
        await B.render(html, f"{OUT}/v1.png", W, H, elements=els)
    print(f"  -> {OUT}/v1.png")
    print(f"  slabs {CWID:.0f}x{SLAB_H:.0f}, seam {SEAM:.0f} | "
          f"bbox x {BX0/W:.3f}..{BX1/W:.3f} y {BY0/H:.3f}..{BY1/H:.3f}")

asyncio.run(main())
