"""Companion art piece (standing rule, CLAUDE.md) for the TerraThon x Disco Diwali ticket poster.
FACET LEDGER: an orthographic mirror ball, 22 x 44 tiles. One rule: a tile is lit by how squarely it faces a single light
(upper left), and its colour is its brightness band (cream, green, blue, orchid, unlit). The subtle reference is the price:
a ring of 55 ticks (Rs. 550 = 55 tens), every fifth one long, 11 in all. See brain/companion/FACET_LEDGER_PHILOSOPHY.md."""
import glob, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SS = 2; W, H = 2400 * SS, 3000 * SS
BLACK, CREAM, ORCHID, GREEN, BLUE, NAVY = (0, 0, 0), (243, 236, 222), (222, 104, 240), (47, 210, 132), (3, 150, 255), (14, 40, 96)
CX, CY, R = W // 2, int(H * 0.47), 800 * SS
img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img)
L = np.array([-0.55, -0.6, 0.58]); L /= np.linalg.norm(L)
N_LAT, N_LON = 22, 44
GAP = math.radians(0.9)
counts = {"cream": 0, "green": 0, "blue": 0, "orchid": 0, "unlit": 0}
def pt(la, lo):
    x, y, z = math.cos(la) * math.sin(lo), math.sin(la), math.cos(la) * math.cos(lo)
    return x, y, z
for j in range(N_LAT):
    la0 = math.radians(-90 + j * 180 / N_LAT) + GAP; la1 = math.radians(-90 + (j + 1) * 180 / N_LAT) - GAP
    for i in range(N_LON):
        lo0 = math.radians(-180 + i * 360 / N_LON) + GAP; lo1 = math.radians(-180 + (i + 1) * 360 / N_LON) - GAP
        if (lo0 + lo1) / 2 < -math.pi / 2 or (lo0 + lo1) / 2 > math.pi / 2: continue      # far side is hidden
        cla, clo = (la0 + la1) / 2, (lo0 + lo1) / 2
        n = np.array(pt(cla, clo)); b = float(n @ L)
        band = "cream" if b > .86 else "green" if b > .68 else "blue" if b > .48 else "orchid" if b > .30 else "unlit"
        counts[band] += 1
        poly = []
        for la, lo in ((la0, lo0), (la0, lo1), (la1, lo1), (la1, lo0)):
            # tiles are flat facets: interpolate corners linearly, as a real mirror tile is
            x, y, z = pt(la, lo); poly.append((CX + R * x, CY + R * y))
        if band == "unlit": d.polygon(poly, outline=NAVY, width=2 * SS)
        else: d.polygon(poly, fill={"cream": CREAM, "green": GREEN, "blue": BLUE, "orchid": ORCHID}[band])
# the ring: 55 ticks, every 5th long (11 long)
RR = R + 120 * SS
for k in range(55):
    a = math.radians(-90 + k * 360 / 55); long_ = k % 5 == 0
    r0, r1 = RR, RR + (70 if long_ else 34) * SS
    d.line([(CX + r0 * math.cos(a), CY + r0 * math.sin(a)), (CX + r1 * math.cos(a), CY + r1 * math.sin(a))],
           fill=CREAM if long_ else NAVY, width=(5 if long_ else 3) * SS)
img = img.resize((W // SS, H // SS), Image.LANCZOS); d = ImageDraw.Draw(img)
fp = glob.glob("/root/.claude/skills/synced/*/canvas-design/canvas-fonts/GeistMono-Regular.ttf")[0]
f = ImageFont.truetype(fp, 30); fs = ImageFont.truetype(fp, 24)
lit = sum(v for k, v in counts.items() if k != "unlit"); tot = lit + counts["unlit"]
MX = 150
d.text((MX, 2740), "FACET LEDGER", font=f, fill=CREAM)
d.text((MX, 2790), f"{lit} OF {tot} FACES LIT. ONE LIGHT.", font=fs, fill=(150, 170, 200))
d.text((2400 - MX, 2740), "550", font=f, fill=ORCHID, anchor="ra")
d.text((2400 - MX, 2790), "55 x 10. 11 LONG MARKS.", font=fs, fill=(150, 170, 200), anchor="ra")
os.makedirs("brain/companion", exist_ok=True)
img.save("brain/companion/dd_tickets_facets.png"); print(counts, lit, tot)
