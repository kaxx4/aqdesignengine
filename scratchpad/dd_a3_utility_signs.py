"""DISCO DIWALI A3 UTILITY SIGNS (2026-11-06): EMERGENCY EXIT and WASHROOM, A3 landscape, 300 dpi, on the venue-signage system (dd_a3_event_signs.Sign: beaded celestial ground,
string lights, LIVE badge, copper mask, gold-rule credit line). One page per arrow (left, right, up) because where each sign hangs is not supplied. Type is measured and fitted to the
room beside the arrow. Copy is just the word(s): no venue facts, no floor, nothing invented. NOTE: a real emergency-exit sign is normally green-on-white and may be required to
be by the fire code; these are the brand version for the event, confirm with the venue.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_a3_utility_signs.py -> out/discodiwali/print_a3_utility/"""
import asyncio, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dd_a3_event_signs as E   # noqa: E402
dd, B, Sign, GOLD = E.dd, E.B, E.Sign, E.GOLD
OUT = os.path.join(E.ROOT, "out", "discodiwali", "print_a3_utility")
LW, LH = 1527, 1080
ARROW, GAP, SIDE = 300, 70, 90


def arrow(size, deg):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 200 200" style="display:block;overflow:visible">'
            f'<g transform="rotate({deg} 100 100)"><path d="M20 78 H112 V34 L184 100 L112 166 V122 H20 Z" fill="{GOLD}" stroke="#000" stroke-width="8" stroke-linejoin="round"'
            f' style="filter:drop-shadow(0 6px 10px rgba(0,0,0,.7))"/></g></svg>')


async def fit(lines, avail, cap=210):
    m = await B.measure_text([dict(text=t.upper(), font="d", size=100, weight=700) for t in lines], W=LW, H=LH)
    wide = max(r["text_w"] for r in m)
    return min(cap, int(100 * avail / wide)), [round(r["text_w"] * min(cap, int(100 * avail / wide)) / 100) for r in m]


def sign(lines, deg, fs):
    s = Sign(LW, LH); s.badge()
    s.mask(1180, 50, 270, 14)
    s.lockup(763, 90, 360)
    lh = fs; tot = len(lines) * lh + (len(lines) - 1) * 10
    ty = 400 + (480 - tot) // 2
    block_w = max(1, SIDE)                                   # text column centred in the room beside the arrow
    room_x0, room_x1 = (SIDE + ARROW + GAP, LW - SIDE) if deg == 0 else (SIDE, LW - SIDE - ARROW - GAP)
    ax = (LW - SIDE - ARROW) if deg == 0 else SIDE
    if deg == 0:       # arrow points right: it sits on the right, text on the left
        room_x0, room_x1, ax = SIDE, LW - SIDE - ARROW - GAP, LW - SIDE - ARROW
    elif deg == 180:   # arrow points left: it sits on the left
        room_x0, room_x1, ax = SIDE + ARROW + GAP, LW - SIDE, SIDE
    else:              # up: arrow on the left, pointing up
        room_x0, room_x1, ax = SIDE + ARROW + GAP, LW - SIDE, SIDE
    s.add("arrow", ax, 400 + (480 - ARROW) // 2, ARROW, ARROW, arrow(ARROW, deg), z=21)
    y = ty
    for i, t in enumerate(lines):
        s.text(f"w{i}", t, y, fs, x=room_x0, w=room_x1 - room_x0); y += lh + 10
    s.sticker("st_l", "star", 50, 800, 150, -12)
    s.sticker("st_r", "heart", 1330, 810, 150, 10)
    s.credit()
    return s


JOBS = [("emergency_exit", ["Emergency", "Exit"]), ("washroom", ["Washroom"])]
ARROWS = [("left", 180), ("right", 0), ("up", -90)]


async def main():
    os.makedirs(OUT, exist_ok=True)
    from PIL import Image
    n = 0
    async with B.session(scale=E.SCALE):
        for name, lines in JOBS:
            fs, widths = await fit(lines, LW - 2 * SIDE - ARROW - GAP)
            for tag, deg in ARROWS:
                n += 1
                s = sign(lines, deg, fs)
                png = os.path.join(OUT, f"{n:02d}_{name}_{tag}_a3.png")
                print(f"--- {name} {tag} (type {fs}px)")
                await B.render(B.page(s.W, s.H, "#000", "".join(s.parts), grain=False), png, s.W, s.H, elements=s.els, bleed_tags=("plate",), crop_tags=("plate",),
                               page_bg="#000", text_pairs=[("text", "#fff", "#000", 120, True), ("credit", "#fff", "#000", 28, True)])
                Image.open(png).convert("RGB").save(png[:-4] + ".pdf", "PDF", resolution=300)
    print("utility signs done ->", OUT)
if __name__ == "__main__":
    asyncio.run(main())
