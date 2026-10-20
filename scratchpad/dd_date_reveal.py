"""DISCO DIWALI date + time reveal poster, feed (1080x1350) and story (1080x1920). Inspo: a headline over a photo, with a calendar-event card floating
under it (hour lines, one event block).

The headline teases and the card reveals: BLOCK YOUR CALENDAR, then two lines placing the date in the festival week (TWO DAYS AFTER DIWALI / ONE DAY BEFORE BHAI DOOJ, supplied by the user
2026-10-19; Diwali 2026 is Sunday 8 November, but several sources list Bhai Dooj on the 10th, so CONFIRM it against a Kolkata panchang before posting), then a white calendar card whose event block starts at 4:30 and runs off the card's
bottom edge, because the supplied time is "4:30 PM onwards" (no end time exists, so none is drawn). Same family as the location reveal poster
(scratchpad/dd_location_reveal.py): diya ground, string lights, LIVE badge top left, copper mask lying across the card's top-right corner, the
DISCO DIWALI lockup (with its ball) as a footer mark. No pill, no link.

Facts (all supplied by the user): 10th November 2026, 4:30 PM onwards, "Masquerade Sangeet Edition". The weekday (Tuesday) is DERIVED from the date.
No venue (the location poster owns that), price or lineup. The card is a drawn UI device, not a screenshot: no Google or Apple marks.
Type is NeutralFace; the event block uses a periwinkle that exists only as the calendar's own colour.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_date_reveal.py"""
import asyncio, datetime, importlib.util, math, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B = dd.B
W = 1080
OUT = os.path.join(ROOT, "out", "discodiwali", "date")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"
EVENT_DAY = datetime.date(2026, 11, 10)                      # supplied
DAY_LABEL = f"{EVENT_DAY.strftime('%a')}, {EVENT_DAY.day} {EVENT_DAY.strftime('%b %Y')}"   # "Tue, 10 Nov 2026" (weekday derived from the date)
CARD_W, CARD_H = 880, 520
ROW = 160                                                    # px per hour on the card
HOURS = ("4 PM", "5 PM", "6 PM")
INK, PERI_BG, PERI_BAR, PERI_TX = "#1f2430", "#dde2fb", "#5b69d6", "#3a4590"   # the calendar's own colours


import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dd_photo_bg as _pb
PHOTO, PHOTO_POS = "14_07", "50% 45%"             # carousel background photo (user, 2026-10-20: "use a photo in the bg of the carousel"); BG=diya restores the plate-only ground


def ground(H):
    if os.environ.get("BG") == "diya":
        return ground_diya(H)
    return _pb.photo_ground(dd, W, H, PHOTO, PHOTO_POS)


def ground_diya(H):
    plate = lambda top, extra="": (f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:{top}px;width:{W}px;height:1350px;'
                                   f'object-fit:cover;z-index:1;{extra}">')
    p = '<div data-tag="plate" style="position:absolute;inset:0;z-index:0;background:#000"></div>' + plate(0)
    if H > 1350:
        p += plate(H - 1350, "transform:scaleY(-1);-webkit-mask-image:linear-gradient(to top,transparent 0%,#000 45%);mask-image:linear-gradient(to top,transparent 0%,#000 45%);")
    p += (f'<img data-tag="lights" src="{dd.uri("string_lights.png")}" style="position:absolute;left:160px;top:-53px;width:1045px;z-index:5">'
          f'<img data-tag="plate" src="{dd.uri("sparkles.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:30;mix-blend-mode:screen;opacity:.55;pointer-events:none">'
          f'<img data-tag="plate" src="{dd.uri("grain.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:31;mix-blend-mode:screen;opacity:.35;pointer-events:none">')
    return p


def calendar_card(left, top):
    """White calendar card: day label, hour lines, one event block that starts at 4:30 and runs off the bottom edge (overflow hidden clips it)."""
    y0 = 118                                                  # y of the first hour line
    rows = ""
    for i, h in enumerate(HOURS):
        y = y0 + i * ROW
        rows += (f'<div style="position:absolute;left:34px;top:{y - 15}px;width:100px;font-family:var(--d);font-weight:400;font-size:26px;color:#6b7280;text-transform:uppercase">{h}</div>'
                 f'<div style="position:absolute;left:150px;right:30px;top:{y}px;height:2px;background:#d4d8e0"></div>')
    ev_top = y0 + ROW // 2                                    # 4:30 = half way between the 4 PM and 5 PM lines
    event = (f'<div data-tag="event" style="position:absolute;left:162px;right:30px;top:{ev_top}px;height:{CARD_H - ev_top + 30}px;background:{PERI_BG};border-radius:16px;overflow:hidden">'
             f'<div style="position:absolute;left:0;top:0;bottom:0;width:8px;background:{PERI_BAR}"></div>'
             f'<div style="position:absolute;left:36px;top:22px;font-family:var(--d);font-weight:700;font-size:52px;line-height:1;color:{PERI_TX};text-transform:uppercase;white-space:nowrap">Disco Diwali</div>'
             f'<div style="position:absolute;left:36px;top:88px;font-family:var(--d);font-weight:400;font-size:28px;line-height:1;color:{PERI_TX};text-transform:uppercase;white-space:nowrap">Masquerade Sangeet Edition</div>'
             f'<div style="position:absolute;left:36px;top:132px;font-family:var(--d);font-weight:700;font-size:34px;line-height:1;color:{PERI_BAR};text-transform:uppercase;white-space:nowrap">4:30 PM onwards</div></div>')
    head = (f'<div style="position:absolute;left:34px;top:26px;font-family:var(--d);font-weight:700;font-size:40px;line-height:1;color:{INK};text-transform:uppercase;white-space:nowrap">{DAY_LABEL}</div>')
    return (f'<div data-tag="card" style="position:absolute;left:{left}px;top:{top}px;width:{CARD_W}px;height:{CARD_H}px;border-radius:30px;overflow:hidden;background:#fff;z-index:10;'
            f'box-shadow:0 36px 70px rgba(0,0,0,.6),0 0 0 3px rgba(255,255,255,.55)">{head}{rows}{event}</div>')


def poster(H):
    story = H > 1350
    parts, els = [ground(H)], []
    bx, by, bw = 40, (210 if story else 40), 150
    parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:{bx}px;top:{by}px;width:{bw}px;z-index:20">'); els.append(("badge", bx, by, bw, round(bw * 1005 / 1061)))
    # headline (teases) + the edition line under it
    size = 112 if story else 92
    hy = 430 if story else 205
    def line(tag, txt, top, fsize, weight, h, extra=""):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:0;width:{W}px;top:{top}px;text-align:center;font-family:var(--d);font-weight:{weight};font-size:{fsize}px;line-height:1;'
                     f'text-transform:uppercase;white-space:nowrap;{STROKE}{extra}z-index:20">{txt}</div>'); els.append((tag, 70, top, 940, h))
    line("head1", "Block your", hy, size, 700, size)
    line("head2", "calendar", hy + round(size * .96), size, 700, size)
    sy = hy + round(size * .96) * 2 + 20
    line("sub1", "Two days after Diwali", sy, 40, 400, 42)
    line("sub2", "One day before Bhai Dooj", sy + 48, 40, 400, 42)
    # the card, with the copper mask lying across its top-right corner (the placement used on the location poster)
    ctop = (800 if story else 520)
    cleft = (W - CARD_W) // 2
    parts.append(calendar_card(cleft, ctop)); els.append(("card", cleft, ctop, CARD_W, CARD_H))
    import dd_copper as _cp
    ss = 225; sx, sy_ = 842, ctop - 55                        # red-copper CALENDAR sticker (mask texture) on the card's top-right corner (user, 2026-10-20: "make a sticker for calendar")
    parts.append(f'<div data-tag="sticker" style="position:absolute;left:{sx}px;top:{sy_}px;z-index:12">{_cp.calendar(ss, 10)}</div>'); els.append(("sticker", sx, sy_, ss, ss))
    # footer mark: the lockup with its ball, visible box 265..1982 x 320..1311 of the 2000x1382 asset
    vw = 400 if story else 330
    t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2
    vy = 1420 if story else H - 64 - vh
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(vy - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">')
    els.append(("title", vx, vy, vw, vh))
    return "".join(parts), els, vy + vh


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        for name, H in (("feed", 1350), ("story", 1920)):
            inner, els, bottom = poster(H)
            print(f"[{name}] last element ends at y={bottom} of {H}")
            await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, f"{name}.png"), W, H, elements=els, containers=(), bleed_tags=("plate",), crop_tags=("plate", "card", "event"),
                           page_bg="#000", collision_ignore=[("sticker", "card"), ("card", "badge"), ("head2", "sticker"), ("sub1", "sticker"), ("sub2", "sticker")])
    print("date reveal done ->", OUT)
asyncio.run(main())
