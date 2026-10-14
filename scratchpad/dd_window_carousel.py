"""DISCO DIWALI carousel, "the window stack" (user inspo, 2026-10-14: a column of tilted search windows, each holding a club photo).

Workflow B/C hybrid: a bespoke script on the discodiwali.py primitives (Poster for img/raw/box/overlays, the asset URIs, the photo
loader), because no registered kind is a carousel and none draws a window.

MECHANISM (kept): a stack of near-identical OS windows, each tilted back in perspective, overlapping so every title bar stays visible
while each window's photo is cut off by the next. The repetition of the same title bar IS the device.

Slides (1080x1350, feed 4:5):
  01 cover   badge + copper mask + ball title lockup, two windows bleeding off the bottom, swipe cue
  02 stack   three windows, three photos
  03 pile    a loose diagonal cascade of three windows, one hero photo in front
  04 info    four windows, the SAME title bar on each, one fact per window (date, time, tickets, details)
  05 cta     badge + mask + title again, a search window whose field reads LINK IN BIO

ADAPTATIONS (CLAUDE.md sec 2 ladder, all recorded):
  - The reference's "The best nightclub - Classico Search" is another brand's copy. The title bar reads DISCO DIWALI - MASQUERADE SANGEET
    EDITION, both supplied facts. No search query or venue is invented; the one search field says LINK IN BIO.
  - Format exception to sec 9 (ink ground, off-white/gold, NeutralFace) is the Disco Diwali one, DISCO_DIWALI.md sec 4 R1. No ACCENTS.
  - Rule R2 (one hero = the lockup) bends on the inner slides: the photo stack is the hero on 02-04, the lockup returns on 01 and 05.
  - Photos are real library photos graded navy with a multiply layer so they share one hue with the diya plate. CONSENT: several show
    minors and none has a consent record (engine/assets/img/events/README.md). Check before any public post.
  - 04 has four windows where the reference has four; 02 has three because a 4:5 canvas leaves a window only ~240px of photo at four.

Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_window_carousel.py     -> out/discodiwali/carousel/window/slide_NN.png (+ sheet.png)
"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B, GROUND, OFFWHITE, GOLD, GL = dd.B, dd.GROUND, dd.OFFWHITE, dd.GOLD, dd.Poster.GL
OUT = os.path.join(ROOT, "out", "discodiwali", "carousel", "window")
W, H = 1080, 1350
N = 5
TITLE = "DISCO DIWALI&nbsp;&nbsp;-&nbsp;&nbsp;MASQUERADE SANGEET EDITION"
BAR_BG, BAR_INK = "#F1F0EC", "#0A0A0A"
BAR_H, PAD = 58, 22

# alpha bounding boxes of the assets (measured): the content origin inside each png, so a poster coordinate is the VISIBLE edge
ASSET_BBOX = {"title_lockup.png": (265, 315, 1983, 1315), "mask_copper.png": (157, 211, 1563, 1135)}

BRIEF = dict(edition="Masquerade Sangeet Edition", status="Ticket sales open soon")


class Slide:
    """One slide. Borrows Poster's helpers (img/raw/box/overlays) and keeps its own element list."""
    def __init__(self, idx):
        self.idx = idx
        self.p = dd.Poster("poster_ref", BRIEF, "feed")
        self.p.parts.clear(); self.p.elements.clear()
        self.P = self.p.parts
        self.ignore = []
        self.wins = []

    # ---- base layers -------------------------------------------------------------------------------------------
    def ground(self, plate_y=0):
        self.P.append(f'<div style="position:absolute;inset:0;background:{GROUND}"></div>')
        self.p.img("bg_diya_portrait.jpg", 0, plate_y, W, H, z=1, tag="plate", extra="object-fit:cover;")

    def placed(self, name, vis_x, vis_y, vis_w, z, tag, extra=""):
        """Place an asset so its VISIBLE (alpha) box starts at vis_x, vis_y and is vis_w wide. Returns the visible box."""
        x0, y0, x1, y1 = ASSET_BBOX[name]
        k = vis_w / (x1 - x0)
        full_w = {"title_lockup.png": 2000, "mask_copper.png": 1680}[name]
        self.p.img(name, round(vis_x - x0 * k), round(vis_y - y0 * k), round(full_w * k), z=z, tag=tag, extra=extra)
        box = (vis_x, vis_y, vis_w, round((y1 - y0) * k))
        self.p.box(tag, *box)
        return box

    def badge(self, x, y, w=240):
        self.p.img("live_badge.png", x, y, w, z=8, tag="badge")
        self.p.box("badge", x, y, w, round(w * 1005 / 1061))

    def mask(self, x, y, w, z=6, extra=""):
        return self.placed("mask_copper.png", x, y, w, z, "mask", "filter:drop-shadow(0 8px 26px rgba(0,0,0,.6));" + extra)

    def title(self, x, y, w, z=9):
        return self.placed("title_lockup.png", x, y, w, z, "title")

    def text(self, label, html, cx, cy, w, h, css, z=12):
        self.p.raw(label, html, cx, cy, w, h, "font-family:var(--d);text-transform:uppercase;" + css, z=z)

    def index_tag(self, x=64, y=58):
        self.text("index", f"{self.idx:02d}&nbsp;/&nbsp;{N:02d}", x + 52, y, 104, 28,
                  f"font-weight:700;font-size:24px;letter-spacing:.2em;color:{GL};text-shadow:0 2px 12px rgba(0,0,0,.8)")

    # ---- the window --------------------------------------------------------------------------------------------
    def window(self, label, x, y, w, h, body, z, tilt=20, roll=0, persp=950, bar_text=TITLE, bar_h=BAR_H):
        """An OS window tilted back in perspective. The top edge keeps full width; the bottom recedes (CSS perspective about the top edge).
        `body` is inner HTML laid in the body well; the well is clipped (overflow hidden) so a photo can bleed inside it."""
        xicon = ('<svg width="24" height="24" viewBox="0 0 24 24" style="position:absolute;left:26px;top:50%;margin-top:-12px">'
                 '<path d="M4 4L20 20M20 4L4 20" stroke="#555" stroke-width="2.6" stroke-linecap="round"/></svg>')
        tf = f"perspective({persp}px) rotateX({tilt}deg)" + (f" rotate({roll}deg)" if roll else "")
        self.P.append(
            f'<div data-tag="{label}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z};transform:{tf};'
            f'transform-origin:50% 0;border-radius:30px 30px 26px 26px;background:{BAR_BG};box-shadow:0 22px 50px rgba(0,0,0,.7),0 0 0 1px rgba(255,255,255,.18);">'
            f'<div style="position:absolute;left:0;top:0;width:100%;height:{bar_h}px;display:flex;align-items:center;justify-content:center;'
            f'font-family:var(--d);font-weight:700;font-size:27px;letter-spacing:.02em;color:{BAR_INK};white-space:nowrap;padding-left:52px;box-sizing:border-box">{xicon}<span data-tag="wintitle">{bar_text}</span></div>'
            f'<div data-tag="winbody" style="position:absolute;left:{PAD}px;right:{PAD}px;top:{bar_h}px;bottom:{PAD}px;overflow:hidden;'
            f'background:#000;border-radius:2px 2px 16px 16px">{body}</div></div>')
        self.p.box(label, x, y, w, h)
        self.wins.append(label)

    def photo(self, ref, focus="50% 50%", grade=.34, extra="", bright=1.0):
        """A library photo for a window well, graded navy (multiply) so it shares a hue with the diya plate."""
        return (f'<img src="{dd.photo_uri(ref)}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{focus};'
                f'filter:contrast(1.12) saturate(1.05) brightness({.95 * bright})">'
                f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,#0A1E7A,#050A33);mix-blend-mode:multiply;opacity:{grade}"></div>'
                + extra)

    # ---- output ------------------------------------------------------------------------------------------------
    def finish(self):
        self.p.overlays()
        page = B.page(W, H, GROUND, "".join(self.P), grain=False)
        # every window overlaps its neighbours by design: declare every pair, and the windows as containers
        for i, a in enumerate(self.wins):
            for b in self.wins[i + 1:]:
                self.ignore.append((a, b))
        return page


def stacked_ignores(s, extra=()):
    labels = {e[0] for e in s.p.elements}
    pairs = list(s.ignore) + [("title", "mask"), ("mask", "badge"), ("title", "badge"), ("lights", "mask")] + list(extra)
    return [pr for pr in pairs if pr[0] in labels and pr[1] in labels]


# ---------------------------------------------------------------------------------------------------------------------
def slide1():
    s = Slide(1)
    s.ground()
    s.mask(430, 96, 590)                                  # copper mask, top right, visible outline 590 wide
    s.badge(64, 70, 236)
    s.title(64, 340, 952)
    s.window("w1", 115, 905, 850, 360, s.photo("07", "50% 62%"), z=10, tilt=18)
    s.window("w2", 115, 1130, 850, 360, s.photo("05", "50% 40%"), z=11, tilt=18)
    s.text("cue", "SWIPE&nbsp;&nbsp;&rarr;", W - 64 - 110, 62, 220, 34,
           f"font-weight:700;font-size:26px;letter-spacing:.24em;color:{GL};text-shadow:0 2px 12px rgba(0,0,0,.8)")
    return s


def slide2():
    s = Slide(2)
    s.ground()
    s.index_tag()
    ys = (150, 530, 910)
    focus = ("50% 45%", "50% 58%", "50% 62%")
    for i, (y, ph) in enumerate(zip(ys, ("05", "07", "10"))):
        s.window(f"w{i + 1}", 115, y, 850, 410 if i < 2 else 392, s.photo(ph, focus[i], bright=1.0), z=10 + i, tilt=18)
    return s


PHOTO3 = os.path.join(ROOT, "engine", "assets", "img", "events", "disco-diwali-hall-2026-10-14")


def slide3():
    """A regular cascade: three EQUAL windows, no roll, one tilt, one title, stepping 73px right and 330px down. The earlier pile mixed three
    widths, three rolls and two titles, which read as misaligned rather than loose."""
    s = Slide(3)
    s.ground()
    s.index_tag()
    pics = (("07_pink-glare-girls-backs-phone.jpg", "50% 45%"), ("09_boy-on-shoulders-star-balloon.jpg", "50% 40%"),
            ("03_girls-dancing-yellow-top.jpg", "50% 35%"))
    for i, (name, focus) in enumerate(pics):
        s.window(f"w{i + 1}", 102 + 73 * i, 150 + 330 * i, 720, 380 if i < 2 else 470,
                 s.photo(os.path.join(PHOTO3, name), focus), z=10 + i, tilt=16, bar_text="DISCO DIWALI")
    return s


INFO = (("ALL FOR CHARITY", 72), ("TICKET SALES OPEN SOON", 48), ("MORE DETAILS SOON", 64))


def slide4():
    s = Slide(4)
    s.ground()
    s.index_tag()
    ys = (150, 530, 910)
    for i, ((txt, fs), y) in enumerate(zip(INFO, ys)):
        body = (f'<img src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:{-120 - i * 40}px;width:100%;height:700px;object-fit:cover;opacity:.9">'
                f'<div style="position:absolute;inset:0;background:radial-gradient(ellipse 90% 90% at 50% 50%,rgba(0,0,0,.82),rgba(0,0,0,.45))"></div>'
                f'<div data-tag="wintext{i + 1}" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:var(--d);'
                f'font-weight:700;font-size:{fs}px;line-height:1;color:{OFFWHITE if i != 0 else "#F6D77A"};white-space:nowrap;letter-spacing:.01em">{txt}</div>')
        s.window(f"w{i + 1}", 115, y, 850, 410 if i < 2 else 392, body, z=10 + i, tilt=18)
    return s


def slide5():
    s = Slide(5)
    s.ground()
    s.mask(450, 96, 566)
    s.badge(64, 70, 236)
    s.title(90, 330, 900)
    s.text("status", "TICKET SALES OPEN SOON", W // 2, 920, 880, 62, f"font-weight:700;font-size:52px;color:{OFFWHITE}")
    glass = ('<svg width="46" height="46" viewBox="0 0 24 24" style="position:absolute;left:44px;top:50%;margin-top:-23px"><circle cx="10" cy="10" r="6.2" fill="none" '
             'stroke="#0A0A0A" stroke-width="2.4"/><path d="M15 15L21 21" stroke="#0A0A0A" stroke-width="2.6" stroke-linecap="round"/></svg>')
    body = (f'<div style="position:absolute;inset:0;background:{BAR_BG}"></div>'
            f'<div data-tag="field" style="position:absolute;left:34px;right:34px;top:34px;bottom:34px;border-radius:999px;background:#fff;border:3px solid #0A0A0A;'
            f'display:flex;align-items:center;justify-content:center;font-family:var(--d);font-weight:700;font-size:50px;color:#0A0A0A;letter-spacing:.04em">{glass}LINK IN BIO</div>')
    s.window("w1", 115, 1030, 850, 260, body, z=10, tilt=14)
    return s


BUILDERS = [slide1, slide2, slide3, slide4, slide5]


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        for i, build in enumerate(BUILDERS, 1):
            s = build()
            html = s.finish()
            labels = {e[0] for e in s.p.elements}
            text_pairs = [("wintitle", BAR_INK, BAR_BG, 27, True)]
            if "wintext2" in labels:
                text_pairs += [("wintext", OFFWHITE, GROUND, 54, True)]
            await B.render(html, os.path.join(OUT, f"slide_{i:02d}.png"), W, H, elements=s.p.elements,
                           containers=tuple(l for l in s.wins), collision_ignore=stacked_ignores(s), text_pairs=text_pairs,
                           bleed_tags=("title", "plate", "sparkles", "grain", "mask", "w1", "w2", "w3", "w4", "photo", "winbody"),
                           crop_tags=("plate", "sparkles", "grain", "photo", "winbody", "mask"), page_bg=GROUND)
    from PIL import Image
    ims = [Image.open(os.path.join(OUT, f"slide_{i:02d}.png")).convert("RGB").resize((432, 540)) for i in range(1, N + 1)]
    sh = Image.new("RGB", (442 * N, 540), (40, 40, 40))
    for i, im in enumerate(ims):
        sh.paste(im, (i * 442, 0))
    sh.save(os.path.join(OUT, "sheet.png"))
    print("window carousel done ->", OUT)

asyncio.run(main())
