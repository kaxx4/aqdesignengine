import asyncio, os, sys, random, math, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build")
W, H = 1080, 1350
random.seed(8)

# ---- palette: dusk teal / weathered verdigris / kerosene amber / one coral note ----
verdigris = ["#12403B", "#1B5952", "#2A6F63", "#0D2E2B"]
amber = "#C98A3E"
coral = "#E4543B"
paper = "#EFE7D6"

def band(y0, y1, color, opacity=1.0, noise_seed=0):
    rects = []
    h = y1 - y0
    steps = 40
    for i in range(steps):
        yy = y0 + h * i / steps
        wob = math.sin(i * 0.7 + noise_seed) * 3
        rects.append(f'<rect x="0" y="{yy:.1f}" width="{W}" height="{h/steps+1.2:.1f}" fill="{color}" opacity="{opacity*(0.85+0.15*math.sin(i*0.3+noise_seed)):.3f}" transform="translate(0,{wob:.1f})"/>')
    return "".join(rects)

def tally_cluster(cx, cy, n, scale, color, seed):
    r = random.Random(seed)
    marks = []
    for i in range(n):
        col = i // 5
        row = i % 5
        x = cx + col * (7*scale) + r.uniform(-1,1)
        y = cy + r.uniform(-1,1)
        if row < 4:
            x2 = x
            marks.append(f'<line x1="{x:.1f}" y1="{y-9*scale:.1f}" x2="{x2:.1f}" y2="{y+9*scale:.1f}" stroke="{color}" stroke-width="{2.2*scale:.2f}" stroke-linecap="round" opacity="0.82"/>')
        else:
            marks.append(f'<line x1="{x-8*scale:.1f}" y1="{y+8*scale:.1f}" x2="{x+8*scale:.1f}" y2="{y-9*scale:.1f}" stroke="{color}" stroke-width="{2.2*scale:.2f}" stroke-linecap="round" opacity="0.82"/>')
    return "".join(marks)

def tide_line(y, amp, freq, color, w=1.6, opacity=0.5):
    pts = []
    for x in range(0, W+10, 10):
        yy = y + amp*math.sin(x*freq + y*0.01)
        pts.append(f"{x},{yy:.1f}")
    return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="{w}" opacity="{opacity}"/>'

def grain_dots(n, y0, y1, color, seed):
    r = random.Random(seed)
    out = []
    for _ in range(n):
        x = r.uniform(20, W-20); y = r.uniform(y0, y1)
        rad = r.uniform(0.4, 1.3)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad:.2f}" fill="{color}" opacity="{r.uniform(0.08,0.22):.2f}"/>')
    return "".join(out)

svg_parts = []
svg_parts.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{paper}"/>')

# silt bands, dusk gradient dark->light top to bottom of a wide central field
svg_parts.append(band(0, 300, verdigris[3], 0.94, 0.3))
svg_parts.append(band(280, 640, verdigris[0], 0.92, 1.1))
svg_parts.append(band(610, 980, verdigris[2], 0.85, 2.0))
svg_parts.append(band(950, 1180, verdigris[1], 0.78, 0.6))
svg_parts.append(band(1150, H, "#0A2723", 0.9, 1.7))

# tide lines threading across
for i, (y, amp, freq, col, op) in enumerate([
    (140, 10, 0.012, "#D8CBA6", 0.35),
    (330, 14, 0.009, amber, 0.28),
    (470, 8, 0.015, "#D8CBA6", 0.22),
    (700, 12, 0.010, amber, 0.24),
    (860, 9, 0.013, "#D8CBA6", 0.20),
    (1040, 11, 0.011, amber, 0.22),
    (1230, 7, 0.014, "#D8CBA6", 0.18),
]):
    svg_parts.append(tide_line(y, amp, freq, col, w=1.4, opacity=op))

# grain / patina speckle across whole field
svg_parts.append(grain_dots(900, 0, H, "#000000", 5))
svg_parts.append(grain_dots(500, 0, H, paper, 9))

# tally clusters — density varies, "many small deposits" motif, never a printed number
cluster_specs = [
    (140, 210, 24, 1.0, paper, 11),
    (740, 200, 15, 0.9, paper, 12),
    (150, 560, 30, 1.1, paper, 13),
    (860, 540, 12, 0.85, paper, 14),
    (110, 800, 20, 1.0, "#EAD9B8", 15),
    (760, 830, 27, 1.05, "#EAD9B8", 16),
    (200, 1040, 18, 0.95, paper, 17),
    (830, 1060, 22, 1.0, paper, 18),
    (140, 1260, 14, 0.9, "#EAD9B8", 19),
]
for cx, cy, n, sc, col, sd in cluster_specs:
    svg_parts.append(tally_cluster(cx, cy, n, sc, col, sd))

# one coral note — the single human mark against the muted field
svg_parts.append(f'<circle cx="{W-190}" cy="{760}" r="5.5" fill="{coral}" opacity="0.92"/>')
svg_parts.append(f'<circle cx="{W-190}" cy="{760}" r="14" fill="none" stroke="{coral}" stroke-width="1.1" opacity="0.4"/>')

# thin gauge-marks along left margin, like a tide gauge post
gauge = []
for i in range(0, H, 26):
    ln = 18 if i % 130 == 0 else 9
    gauge.append(f'<line x1="34" y1="{i}" x2="{34+ln}" y2="{i}" stroke="{paper}" stroke-width="1" opacity="0.28"/>')
svg_parts.append("".join(gauge))

svg = f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{"".join(svg_parts)}</svg>'

inner = f'<div style="position:absolute;inset:0">{svg}</div>'
inner += (f'<div style="position:absolute;bottom:64px;left:64px;z-index:20;font-family:var(--m);'
          f'font-weight:500;font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:{paper};'
          f'opacity:.75">sundarbans &middot; dec 2025 &middot; field notes</div>')
inner += (f'<div style="position:absolute;top:100px;left:64px;z-index:20;font-family:var(--s);'
          f'font-style:italic;font-size:52px;color:{paper};opacity:.92">care, tallied quietly</div>')

html = B.page(W, H, paper, inner, grain=True)

async def main():
    os.makedirs("scratchpad/carousel_sunderbans8", exist_ok=True)
    await B.render(html, "scratchpad/carousel_sunderbans8/tidal_ledger.png", W, H)
    print("done")
asyncio.run(main())
