"""REGISTER — companion art piece for session 10f.

PLATE I: a systematic field sweeping occluder opacity across six materials, with the
rule's actual 0.9 cutoff drawn as a hairline. The eye's threshold and the rule's
threshold do not coincide, and the plate is about that disagreement.
"""
import asyncio, base64, os, sys

_r = os.path.abspath(__file__)
while _r != os.path.dirname(_r) and not os.path.exists(os.path.join(_r, "CLAUDE.md")):
    _r = os.path.dirname(_r)
os.chdir(_r)

FONTDIR = os.path.expanduser(r"~\.claude\skills\canvas-design\canvas-fonts")

W, H = 1400, 1980
CREAM = "#F4EFE0"
INK = "#0A0A0A"
MINT = "#1B8A5A"
TEAL = "#0E7C86"

M = 104                      # outer margin — generous and exact
COLS = 11                    # opacity 0.00 .. 1.00
ROWS = 6


def font_face(name, filename, weight=400, style="normal"):
    p = os.path.join(FONTDIR, filename)
    b64 = base64.b64encode(open(p, "rb").read()).decode()
    return (f"@font-face{{font-family:'{name}';font-weight:{weight};font-style:{style};"
            f"src:url(data:font/ttf;base64,{b64}) format('truetype');}}")


FONTS = "".join([
    font_face("Disp", "BigShoulders-Bold.ttf", 700),
    font_face("Disp", "BigShoulders-Regular.ttf", 400),
    font_face("Mono", "GeistMono-Regular.ttf", 400),
    font_face("Mono", "GeistMono-Bold.ttf", 700),
    font_face("Thin", "Jura-Light.ttf", 300),
])

# Six occluding MATERIALS. The rule knows only alpha; the eye also knows luminance,
# which is exactly the disagreement this plate documents.
MATERIALS = [
    ("PAPER",  "244,239,224"),
    ("MINT",   "27,138,90"),
    ("TEAL",   "14,124,134"),
    ("INK",    "10,10,10"),
    ("WARM",   "214,203,178"),
    ("COOL",   "168,186,190"),
]

# The mark must never share a family with the plane above it, or the row is dead at
# alpha 0.00 and the sweep documents nothing. Chromatic planes take an ink mark;
# neutral planes take the mint. Decided by the material, not by rotation.
MARK_FOR = {"PAPER": MINT, "WARM": MINT, "INK": MINT,
            "MINT": INK, "TEAL": INK, "COOL": INK}

ALPHAS = [i / (COLS - 1) for i in range(COLS)]
RULE_CUTOFF = 0.9            # the value in reconcile.py. Not a perceptual constant.


def cell(mark_col, occl_rgb, alpha, cw, ch):
    """One specimen: a mark, and a plane of known strength above it."""
    # the mark — a perfect disc and a bar, identical in every cell
    d = round(ch * 0.40)
    bar_w, bar_h = round(cw * 0.52), round(ch * 0.115)
    mark = (
        f'<div style="position:absolute;left:50%;top:{round(ch*0.16)}px;'
        f'width:{d}px;height:{d}px;margin-left:{-d//2}px;border-radius:50%;'
        f'background:{mark_col}"></div>'
        f'<div style="position:absolute;left:50%;top:{round(ch*0.655)}px;'
        f'width:{bar_w}px;height:{bar_h}px;margin-left:{-bar_w//2}px;'
        f'background:{mark_col}"></div>')
    plane = (f'<div style="position:absolute;inset:0;'
             f'background:rgba({occl_rgb},{alpha:.2f})"></div>')
    return mark + plane


def sample_dots(ok, cw):
    """The check's own notation: five hit-test points, filled where the mark reaches
    the surface. The pattern is the real one — centre plus four at .2/.8."""
    pts = [(.5, .5), (.2, .3), (.8, .3), (.2, .7), (.8, .7)]
    r = 3
    box = round(cw * 0.34)
    out = []
    for i, (fx, fy) in enumerate(pts):
        filled = i < ok
        out.append(
            f'<div style="position:absolute;left:{fx*box - r:.1f}px;top:{fy*box - r:.1f}px;'
            f'width:{2*r}px;height:{2*r}px;border-radius:50%;'
            + (f'background:{INK}"></div>' if filled
               else f'border:1px solid rgba(10,10,10,.55)"></div>'))
    return (f'<div style="position:relative;width:{box}px;height:{box}px;'
            f'margin:9px auto 0">' + "".join(out) + "</div>")


def build():
    gw = W - 2 * M
    cw = gw / COLS
    ch = 118
    gap_y = 56

    # ── the systematic field ────────────────────────────────────────────────
    field = []
    for ri, (mat, rgb) in enumerate(MATERIALS):
        y = ri * (ch + gap_y)
        # row label, left of the field
        field.append(
            f'<div style="position:absolute;left:{-M + 26}px;top:{y + ch/2 - 9}px;'
            f'width:{M - 44}px;text-align:right;font-family:Mono;font-size:11px;'
            f'font-weight:700;letter-spacing:.16em;color:{INK}">{mat}</div>')
        for ci, a in enumerate(ALPHAS):
            x = ci * cw
            ok = 5 if a < RULE_CUTOFF else 0          # what the RULE reports
            field.append(
                f'<div style="position:absolute;left:{x:.2f}px;top:{y}px;'
                f'width:{cw - 10:.2f}px;height:{ch}px;overflow:hidden;'
                f'background:{CREAM};box-shadow:3px 3px 0 rgba(10,10,10,.14)">'
                + cell(MARK_FOR[mat], rgb, a, cw - 10, ch) +
                '</div>')
            field.append(
                f'<div style="position:absolute;left:{x:.2f}px;top:{y + ch}px;'
                f'width:{cw - 10:.2f}px">' + sample_dots(ok, cw - 10) + '</div>')

    field_h = ROWS * (ch + gap_y) - gap_y + 34

    # column scale, above the field
    scale = []
    for ci, a in enumerate(ALPHAS):
        x = ci * cw
        scale.append(
            f'<div style="position:absolute;left:{x:.2f}px;top:0;width:{cw - 10:.2f}px;'
            f'text-align:center;font-family:Mono;font-size:11px;color:{INK};'
            f'opacity:.72">{a:.2f}</div>')
        scale.append(
            f'<div style="position:absolute;left:{x + (cw-10)/2:.2f}px;top:20px;'
            f'width:1px;height:9px;background:rgba(10,10,10,.5)"></div>')

    # THE THRESHOLD — one hairline, at the value the rule actually uses.
    tx = ALPHAS.index(round(RULE_CUTOFF, 2)) * cw - 5 if round(RULE_CUTOFF, 2) in [round(a, 2) for a in ALPHAS] else 9 * cw - 5
    # The label goes BELOW the field. Above, it collided with the 0.90 column number —
    # which would have been a small, stupid way to lose the whole plate.
    thresh = (
        f'<div style="position:absolute;left:{tx:.2f}px;top:-34px;width:2px;'
        f'height:{field_h + 62}px;background:{TEAL}"></div>'
        f'<div style="position:absolute;left:{tx - 3:.2f}px;top:{field_h + 40}px;'
        f'width:9px;height:9px;border-radius:50%;background:{TEAL}"></div>'
        f'<div style="position:absolute;left:{tx + 16:.2f}px;top:{field_h + 36}px;'
        f'font-family:Mono;font-size:10px;font-weight:700;letter-spacing:.2em;'
        f'color:{TEAL};white-space:nowrap">&#945;&#8202;0.90 &#183; THE RULE\'S EDGE</div>')

    # ── corner registration marks ───────────────────────────────────────────
    def reg(x, y):
        return (f'<div style="position:absolute;left:{x-13}px;top:{y-1}px;width:26px;'
                f'height:1px;background:rgba(10,10,10,.55)"></div>'
                f'<div style="position:absolute;left:{x-1}px;top:{y-13}px;width:1px;'
                f'height:26px;background:rgba(10,10,10,.55)"></div>'
                f'<div style="position:absolute;left:{x-7}px;top:{y-7}px;width:14px;'
                f'height:14px;border:1px solid rgba(10,10,10,.30);'
                f'border-radius:50%"></div>')

    regs = reg(52, 52) + reg(W - 52, 52) + reg(52, H - 52) + reg(W - 52, H - 52)

    # ── header ──────────────────────────────────────────────────────────────
    header = f"""
    <div style="position:absolute;left:{M}px;top:{M}px;width:{gw}px">
      <div style="display:flex;justify-content:space-between;align-items:baseline">
        <div style="font-family:Mono;font-size:11px;font-weight:700;
                    letter-spacing:.42em;color:{INK}">REGISTER</div>
        <div style="font-family:Mono;font-size:11px;letter-spacing:.22em;
                    color:rgba(10,10,10,.6)">PLATE&nbsp;I &nbsp;&#183;&nbsp; 66 SPECIMENS</div>
      </div>
      <div style="height:1px;background:{INK};margin-top:13px"></div>
      <div style="display:flex;justify-content:space-between;align-items:flex-start;
                  margin-top:15px">
        <div style="font-family:Thin;font-size:13px;letter-spacing:.055em;
                    color:rgba(10,10,10,.78);max-width:620px;line-height:1.55">
          One mark, laid down identically sixty-six times, beneath a plane of
          known material and known strength.
        </div>
        <div style="font-family:Mono;font-size:10px;letter-spacing:.16em;
                    text-align:right;color:rgba(10,10,10,.55);line-height:1.9">
          OCCLUDER &#945; &nbsp;0.00&nbsp;&#8594;&nbsp;1.00<br>
          MATERIALS &nbsp;n&#8202;=&#8202;6
        </div>
      </div>
    </div>"""

    field_top = M + 232

    # ── the monumental pair ─────────────────────────────────────────────────
    foot_top = field_top + field_h + 132
    DSIZE = 150
    monument = f"""
    <div style="position:absolute;left:{M}px;top:{foot_top}px;width:{gw}px">
      <div style="height:1px;background:{INK}"></div>
      <div style="position:relative;margin-top:26px">
        <div style="font-family:Disp;font-weight:700;font-size:{DSIZE}px;
                    line-height:.84;letter-spacing:.005em;color:{INK}">PRESENT</div>
        <div style="font-family:Disp;font-weight:700;font-size:{DSIZE}px;
                    line-height:.84;letter-spacing:.005em;color:{INK};
                    opacity:.085">VISIBLE</div>
        <div style="position:absolute;right:0;top:6px;text-align:right;
                    font-family:Mono;font-size:10px;letter-spacing:.17em;
                    color:rgba(10,10,10,.6);line-height:2.1">
          &#945;&#8202;1.00 &nbsp;&#183;&nbsp; 13.71&#8202;:&#8202;1<br>
          <span style="color:{TEAL}">&#945;&#8202;0.09 &nbsp;&#183;&nbsp; 1.44&#8202;:&#8202;1</span>
        </div>
      </div>
    </div>"""

    footer = f"""
    <div style="position:absolute;left:{M}px;right:{M}px;bottom:{M - 14}px;
                display:flex;justify-content:space-between;align-items:baseline">
      <div style="font-family:Mono;font-size:10px;letter-spacing:.2em;
                  color:rgba(10,10,10,.5)">
        THE RULE READS &#945; ALONE &nbsp;&#183;&nbsp; THE EYE ALSO READS LUMINANCE
      </div>
      <div style="font-family:Mono;font-size:10px;letter-spacing:.2em;
                  color:rgba(10,10,10,.5)">AQ &#183; 10f</div>
    </div>"""

    inner = f"""
    <div style="position:absolute;inset:0;background:{CREAM}"></div>
    {regs}
    {header}
    <div style="position:absolute;left:{M}px;top:{field_top}px;width:{gw}px;
                height:{field_h}px">
      <div style="position:absolute;left:0;top:-58px;width:{gw}px;height:30px">
        {"".join(scale)}
      </div>
      {thresh}
      {"".join(field)}
    </div>
    {monument}
    {footer}"""

    return (f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{FONTS}'
            f'*{{margin:0;padding:0;box-sizing:border-box}}'
            f'body{{margin:0}}'
            f'.plate{{width:{W}px;height:{H}px;position:relative;overflow:hidden;'
            f'background:{CREAM}}}</style></head>'
            f'<body><div class="plate">{inner}</div></body></html>')


async def main():
    from playwright.async_api import async_playwright
    html = build()
    out = "out/session10f/REGISTER_plate01.png"
    os.makedirs("out/session10f", exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        await pg.set_content(html, wait_until="load")
        await pg.evaluate("async () => { await document.fonts.ready; "
                          "await new Promise(r => requestAnimationFrame(() => "
                          "requestAnimationFrame(r))); }")
        await pg.locator(".plate").screenshot(path=out)
        await b.close()
    print("wrote", out)


asyncio.run(main())
