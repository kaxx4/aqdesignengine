"""DISCO DIWALI hype poster for WhatsApp: the FIRST WhatsApp group is full (user, 2026-10-19: "we have officially maxed out the first whatsapp group").

1080x1350 (4:5), the WhatsApp poster geometry: no link pill (there is no link to point at inside WhatsApp). Built from the approved poster_ref skeleton
(copper-red mask top right, LIVE / ALL FOR CHARITY badge top left, diya plate, string lights) with the ball-free lockup scaled down so the news can be the hero.

COPY (R12, nothing invented): "GROUP 1/2 IS FULL" is the supplied fact (user, 2026-10-19: written "1/2"); all type is white, no gold (user, same day). It does NOT say a second group exists, because none was reported. "THAT WAS FAST. YOU DID THIS."
is voice and the credit-transfer line (the audience made it what it was). "MORE DETAILS TO FOLLOW" is supplied. No date, time or location (user, 2026-10-14).
The poster says "GROUP 1", not "whatsapp group" (user, 2026-10-18).

Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_group_full_poster.py   -> out/discodiwali/launch/group_full_poster.png
"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B, GROUND, OFFWHITE, GL, FOIL = dd.B, dd.GROUND, dd.OFFWHITE, dd.Poster.GL, dd.Poster.FOIL
OUT = os.path.join(ROOT, "out", "discodiwali", "launch", "group_full_poster.png")
W, H = 1080, 1350
BRIEF = dict(edition="Masquerade Sangeet Edition", status="Ticket sales open soon")


async def main():
    p = dd.Poster("poster_ref", BRIEF, "feed")
    p.parts.clear(); p.elements.clear(); P = p.parts
    P.append(f'<div style="position:absolute;inset:0;background:{GROUND}"></div>')
    p.img("bg_diya_portrait.jpg", 0, 0, W, H, z=1, tag="plate", extra="object-fit:cover;")
    p.img("string_lights.png", 160, -53, 1045, z=5, tag="lights")
    k = .4925                                                   # copper mask: visible outline 343..1035 x 108..560 (the approved poster_ref placement)
    p.img("mask_copper.png", round(343 - 157 * k), round(108 - 211 * k), round(1680 * k), z=6, tag="mask", extra="filter:drop-shadow(0 8px 26px rgba(0,0,0,.6));")
    p.box("mask", 343, 108, 692, 452)
    p.img("live_badge.png", 30, 122, 267, z=8, tag="badge"); p.box("badge", 30, 122, 267, 248)
    # the ball-free lockup, smaller than poster_ref's 1036px so the news below can be the hero: visible 700 wide
    x0, y0, x1, y1 = 265, 401, 1983, 1315
    w = 700; t = w / (x1 - x0); vh = round((y1 - y0) * t); vx, vy = (W - w) // 2, 490
    p.img("title_lockup_noball.png", round(vx - x0 * t), round(vy - y0 * t), round(2000 * t), z=9, tag="title")
    p.box("title", vx, vy, w, vh)
    cy = vy + vh + 70                                           # first text line, clear of the lockup
    p.raw("g1", "GROUP 1/2", W // 2, cy, 520, 64, "font-family:var(--d);font-weight:700;font-size:64px;letter-spacing:.34em;text-indent:.34em;text-transform:uppercase")
    p.raw("full", "IS FULL", W // 2, cy + 130, 900, 190,
          f"font-family:var(--d);font-weight:900;font-size:200px;letter-spacing:.01em;text-transform:uppercase;color:{OFFWHITE};filter:drop-shadow(0 4px 22px rgba(0,0,0,.6))")
    p.raw("fast", "THAT WAS FAST. YOU DID THIS.", W // 2, cy + 275, 900, 48, "font-family:var(--d);font-weight:700;font-size:46px;text-transform:uppercase")
    p.raw("more", "MORE DETAILS TO FOLLOW", W // 2, cy + 340, 600, 38, f"font-family:var(--d);font-weight:700;font-size:32px;letter-spacing:.2em;text-indent:.2em;color:{OFFWHITE};text-transform:uppercase")
    p.overlays()
    html = B.page(W, H, GROUND, "".join(P), grain=False)
    html = p.neutralise(html)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    labels = {e[0] for e in p.elements}
    ign = [pr for pr in [("title", "mask"), ("mask", "badge"), ("lights", "mask"), ("title", "badge")] if pr[0] in labels and pr[1] in labels]
    async with B.session():
        await B.render(html, OUT, W, H, elements=p.elements, collision_ignore=ign, text_pairs=[("g1", OFFWHITE, GROUND, 64, True), ("fast", OFFWHITE, GROUND, 46, True)],
                       bleed_tags=("mask", "title", "lights", "plate", "sparkles", "grain"), crop_tags=("plate", "sparkles", "grain"), page_bg=GROUND)
    print("group-full poster done ->", OUT)

asyncio.run(main())
