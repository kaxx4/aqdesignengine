import asyncio, os, sys, math, random

ROOT = "/home/user/aqdesignengine"
FONT_DIR = "/root/.claude/skills/synced/canvas-design/canvas-fonts"
OUT = os.path.join(ROOT, "out/companion")
os.makedirs(OUT, exist_ok=True)

W, H = 1600, 2000
random.seed(7)

PAPER = "#EDE6D6"
INK   = "#242220"
INK2  = "#5B564C"
FAINT = "#B9B1A0"
ACCENT = "#B23A2E"   # earned-threshold vermillion
GOLD   = "#C9A227"

def font_face(name, path, weight="normal", style="normal"):
    return f"@font-face {{ font-family:'{name}'; src:url('file://{path}'); font-weight:{weight}; font-style:{style}; }}"

FONTS_CSS = "\n".join([
    font_face("Mono", os.path.join(FONT_DIR, "IBMPlexMono-Regular.ttf")),
    font_face("MonoBold", os.path.join(FONT_DIR, "IBMPlexMono-Bold.ttf")),
    font_face("SerifItalic", os.path.join(FONT_DIR, "CrimsonPro-Italic.ttf")),
])

# ---------- the strata field: hundreds of hand-tally marks, bottom-up accumulation ----------
MARGIN_L, MARGIN_R = 150, 150
MARGIN_T, MARGIN_B = 280, 220
field_x0, field_x1 = MARGIN_L, W - MARGIN_R
field_y0, field_y1 = MARGIN_T, H - MARGIN_B
field_w = field_x1 - field_x0
field_h = field_y1 - field_y0

ROW_H = 15.5
N_ROWS = int(field_h / ROW_H)
THRESHOLD_ROW = int(N_ROWS * 0.115)  # top ~11.5% of rows are the earned color, rest is labor

marks_svg = []
row_labels = []

col_w = 15.2  # base spacing per mark within a row, jittered
for r in range(N_ROWS):
    y = field_y1 - r * ROW_H
    # r=0 is the base row (bottom of canvas, the earliest labor); r rises toward the TOP of
    # the canvas as more dues accumulate, so the threshold zone is the last few rows (top).
    is_threshold_zone = r >= N_ROWS - THRESHOLD_ROW
    n_marks = int(field_w / col_w)
    fill_prob = 1.0 if r > 4 else (0.35 + 0.16 * r)
    x = field_x0
    for i in range(n_marks):
        jitter_x = random.uniform(-1.1, 1.1)
        jitter_y = random.uniform(-1.3, 1.3)
        rot = random.uniform(-4, 4)
        h = random.uniform(9.5, 12.5)
        sw = random.uniform(1.15, 1.55)
        if random.random() > fill_prob:
            x += col_w
            continue
        if is_threshold_zone:
            # ember density rises the closer a row sits to the very top (the fully-earned end)
            zone_depth = r - (N_ROWS - THRESHOLD_ROW)  # 0 at the threshold line, rising toward the top
            zone_frac = zone_depth / max(THRESHOLD_ROW - 1, 1)
            in_accent = random.random() < (0.3 + 0.6 * zone_frac)
            color = ACCENT if in_accent else INK2
            op = 0.95 if in_accent else 0.55
        else:
            color = INK if random.random() > 0.06 else INK2
            op = 0.88
        cx = x + jitter_x
        cy = y + jitter_y
        marks_svg.append(
            f'<line x1="{cx:.2f}" y1="{cy:.2f}" x2="{cx:.2f}" y2="{cy-h:.2f}" '
            f'stroke="{color}" stroke-width="{sw:.2f}" stroke-linecap="round" '
            f'opacity="{op:.2f}" transform="rotate({rot:.1f} {cx:.2f} {cy:.2f})"/>'
        )
        x += col_w

# occasional five-bar tally group markers along the left margin — the "count" of the survey
tick_svg = []
for r in range(0, N_ROWS, 5):
    y = field_y1 - r * ROW_H
    tick_svg.append(f'<line x1="{field_x0-26}" y1="{y:.1f}" x2="{field_x0-10}" y2="{y:.1f}" stroke="{FAINT}" stroke-width="1"/>')
    if r % 20 == 0 and r > 0:
        tick_svg.append(f'<rect x="{field_x0-70}" y="{y-9:.1f}" width="34" height="16" fill="{PAPER}"/>')
        tick_svg.append(f'<text x="{field_x0-34}" y="{y+4:.1f}" font-family="Mono" font-size="10" fill="{FAINT}" text-anchor="end">{r:03d}</text>')

# threshold line — the exact stratum where labor becomes color (near the top: N_ROWS - THRESHOLD_ROW)
thresh_y = field_y1 - (N_ROWS - THRESHOLD_ROW) * ROW_H
threshold_line = (
    f'<line x1="{field_x0-40}" y1="{thresh_y:.1f}" x2="{field_x1+10}" y2="{thresh_y:.1f}" '
    f'stroke="{GOLD}" stroke-width="1.1" stroke-dasharray="1.5 4" opacity="0.75"/>'
)

# corner registration marks (survey-plate convention)
def reg_mark(x, y, s=14):
    return (f'<line x1="{x-s}" y1="{y}" x2="{x+s}" y2="{y}" stroke="{INK2}" stroke-width="1"/>'
            f'<line x1="{x}" y1="{y-s}" x2="{x}" y2="{y+s}" stroke="{INK2}" stroke-width="1"/>')
corners = "".join([
    reg_mark(70, 70), reg_mark(W-70, 70), reg_mark(70, H-70), reg_mark(W-70, H-70)
])

svg_body = "".join(marks_svg)
tick_body = "".join(tick_svg)

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{FONTS_CSS}
*{{margin:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;background:{PAPER};position:relative;overflow:hidden;
     font-family:Mono;
     background-image:
       radial-gradient(ellipse at 30% 20%, rgba(0,0,0,.025), transparent 60%),
       radial-gradient(ellipse at 80% 85%, rgba(0,0,0,.03), transparent 55%);}}
.frame{{position:absolute;inset:56px;border:1px solid {INK2};opacity:.55}}
.frame2{{position:absolute;inset:60px;border:1px solid {INK2};opacity:.25}}
.hdr{{position:absolute;top:88px;left:{MARGIN_L}px;right:{MARGIN_R}px;
     display:flex;justify-content:space-between;align-items:flex-end;}}
.hdr-l{{font-family:MonoBold;font-size:13px;letter-spacing:.16em;color:{INK};text-transform:uppercase}}
.hdr-sub{{font-family:Mono;font-size:10.5px;letter-spacing:.1em;color:{INK2};margin-top:8px}}
.hdr-r{{font-family:Mono;font-size:10.5px;letter-spacing:.08em;color:{INK2};text-align:right;line-height:1.7}}
.fig{{position:absolute;top:168px;left:{MARGIN_L}px;font-family:Mono;font-size:11px;
     letter-spacing:.14em;color:{INK2};text-transform:uppercase}}
.note{{position:absolute;font-family:SerifItalic;font-style:italic;font-size:22px;color:{INK};
      opacity:.92}}
.axis-lbl{{position:absolute;font-family:Mono;font-size:9.5px;letter-spacing:.12em;color:{FAINT};
          text-transform:uppercase}}
.tag{{position:absolute;background:{PAPER};padding:5px 10px}}
.tag .axis-lbl,.tag .note{{position:static}}
.footer{{position:absolute;bottom:96px;left:{MARGIN_L}px;right:{MARGIN_R}px;
        display:flex;justify-content:space-between;align-items:flex-end}}
.footer-l{{font-family:Mono;font-size:10px;letter-spacing:.08em;color:{INK2};line-height:1.7}}
.footer-r{{font-family:MonoBold;font-size:11px;letter-spacing:.1em;color:{INK};text-align:right}}
</style></head>
<body>
  <div class="frame"></div>
  <div class="frame2"></div>
  {corners}

  <div class="hdr">
    <div>
      <div class="hdr-l">Survey of Accumulated Effort</div>
      <div class="hdr-sub">core sample &middot; strata of unglamorous labor, dated &amp; counted</div>
    </div>
    <div class="hdr-r">
      FIELD LOG NO. 02&mdash;07<br>
      DEPTH 000&ndash;{N_ROWS:03d}<br>
      INSTRUMENT: HAND
    </div>
  </div>
  <div class="fig">Fig. 3 &mdash; one mark per unit of dues paid, read bottom to top</div>

  <svg width="{W}" height="{H}" style="position:absolute;top:0;left:0">
    {tick_body}
    {svg_body}
    {threshold_line}
  </svg>

  <div class="tag" style="top:{thresh_y-30:.0f}px;left:{field_x1-260}px">
    <div class="axis-lbl">threshold &mdash; the right to choose, earned</div>
  </div>
  <div class="tag" style="top:{thresh_y+22:.0f}px;left:{field_x0+30}px">
    <div class="note">the reward, once.</div>
  </div>

  <div class="axis-lbl" style="bottom:{H-field_y1-4}px;left:{field_x0}px">base layer &mdash; entry fee</div>

  <div class="footer">
    <div class="footer-l">
      SAMPLE: 000&ndash;{N_ROWS:03d} MARKS COUNTED<br>
      METHOD: ONE GESTURE, ONE UNIT, NO SHORTCUT
    </div>
    <div class="footer-r">SEDIMENT DISCIPLINE</div>
  </div>
</body></html>
"""

with open(os.path.join(OUT, "_sediment_render.html"), "w") as f:
    f.write(html)

async def main():
    from playwright.async_api import async_playwright
    chrome = "/opt/pw-browsers/chromium"
    kw = {"executable_path": chrome} if os.path.exists(chrome) else {}
    async with async_playwright() as p:
        b = await p.chromium.launch(**kw)
        pg = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        await pg.goto("file://" + os.path.join(OUT, "_sediment_render.html"), wait_until="load")
        await pg.wait_for_timeout(400)
        await pg.screenshot(path=os.path.join(OUT, "passion_sequence_art.png"))
        await b.close()
    print("done")

asyncio.run(main())
