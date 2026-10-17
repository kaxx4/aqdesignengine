"""DISCO DIWALI carousel, "the callout frames" (user inspo, 2026-10-14: a dimmed full-bleed night photo with gold-framed close-ups, each tied
by a thin gold line to a small viewfinder reticle on the scene behind it).

MECHANISM (kept): one dark full-bleed photograph is the ground; a few gold-bordered photos float over it; a hairline runs from each frame
to a corner-bracket reticle that lands on something in the background photo. The line says "this detail came from there".

Slides (1080x1350, feed 4:5):
  01 cover    badge + copper mask + ball title lockup over a dimmed photo, two framed photos below, reticles under the lockup
  02 callouts four frames, four reticles on the background crowd (the inspo's own composition)
  03 callouts three frames on a second background, the frames mirrored
  04 cta      badge + mask + title, status, a gold-edged LINK IN BIO pill

ADAPTATIONS (CLAUDE.md sec 2 ladder, all recorded):
  - The reference's "Recent joys" is invented-for-that-brand copy. The label here is MASQUERADE SANGEET EDITION, a supplied fact. No date, time
    or location appears anywhere (user, 2026-10-14).
  - Reference's warm red-brown grade becomes the format's navy grade (ink ground + navy multiply), DISCO_DIWALI.md sec 4 R1. Frame borders use the
    format gold, not an AQ accent.
  - R2 (one hero = the lockup) bends on 02-03: the framed photos are the hero there, as with the window carousel.
  - CONSENT: many people in these photos look like minors and none has a consent record. Check before any public post.

Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_callout_carousel.py     -> out/discodiwali/carousel/callout/slide_NN.png (+ sheet.png)
"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B, GROUND, OFFWHITE, GOLD, GL = dd.B, dd.GROUND, dd.OFFWHITE, dd.GOLD, dd.Poster.GL
OUT = os.path.join(ROOT, "out", "discodiwali", "carousel", "callout")
PHOTOS = os.path.join(ROOT, "engine", "assets", "img", "events", "disco-diwali-hall-2026-10-14")
NEW = lambda n: os.path.join(PHOTOS, n)
W, H, N = 1080, 1350, 4
LINE = "#E8C063"                                     # the format's lifted gold: a hairline on a dark photo needs the lighter value
ASSET_BBOX = {"title_lockup.png": (265, 315, 1983, 1315), "mask_copper.png": (157, 211, 1563, 1135)}
BRIEF = dict(edition="Masquerade Sangeet Edition", status="Ticket sales open soon")


class Slide:
    def __init__(self, idx):
        self.idx = idx
        self.p = dd.Poster("poster_ref", BRIEF, "feed")
        self.p.parts.clear(); self.p.elements.clear()
        self.P = self.p.parts
        self.frames, self.lines = [], []

    def ground(self, photo, focus="50% 50%", bright=.62):
        """The full-bleed photo, dimmed and graded navy so the gold frames own the contrast."""
        self.P.append(f'<div style="position:absolute;inset:0;background:{GROUND}"></div>')
        self.P.append(f'<img data-tag="photo" src="{dd.photo_uri(photo)}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;'
                      f'object-position:{focus};z-index:1;filter:contrast(1.1) saturate(.95) brightness({bright})">')
        self.P.append('<div data-tag="plate" style="position:absolute;inset:0;z-index:2;background:linear-gradient(180deg,#0A1E7A,#050A33);'
                      'mix-blend-mode:multiply;opacity:.5"></div>')
        self.P.append('<div data-tag="plate" style="position:absolute;inset:0;z-index:3;background:linear-gradient(180deg,rgba(0,0,0,.55) 0%,'
                      'rgba(0,0,0,0) 28%,rgba(0,0,0,0) 62%,rgba(0,0,0,.6) 100%)"></div>')

    def placed(self, name, vx, vy, vw, z, tag, extra=""):
        x0, y0, x1, y1 = ASSET_BBOX[name]
        k = vw / (x1 - x0)
        fw = {"title_lockup.png": 2000, "mask_copper.png": 1680}[name]
        self.p.img(name, round(vx - x0 * k), round(vy - y0 * k), round(fw * k), z=z, tag=tag, extra=extra)
        self.p.box(tag, vx, vy, vw, round((y1 - y0) * k))

    def badge(self, x, y, w=236):
        self.p.img("live_badge.png", x, y, w, z=8, tag="badge"); self.p.box("badge", x, y, w, round(w * 1005 / 1061))

    def mask(self, x, y, w):
        self.placed("mask_copper.png", x, y, w, 6, "mask", "filter:drop-shadow(0 8px 26px rgba(0,0,0,.6));")

    def title(self, x, y, w):
        self.placed("title_lockup.png", x, y, w, 9, "title")

    def text(self, label, html, cx, cy, w, h, css):
        self.p.raw(label, html, cx, cy, w, h, "font-family:var(--d);text-transform:uppercase;" + css, z=12)

    def frame(self, label, photo, x, y, w, h, focus="50% 50%", bright=1.0, anchor=None, z=10):
        """A gold-bordered photo. `anchor` = (ax, ay): the reticle it points at, joined by a hairline from the nearest frame edge midpoint."""
        self.P.append(
            f'<div data-tag="{label}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;border:3px solid {LINE};'
            f'background:#000;z-index:{z};overflow:hidden;box-shadow:0 14px 36px rgba(0,0,0,.65)">'
            f'<img src="{dd.photo_uri(photo)}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{focus};'
            f'filter:contrast(1.1) saturate(1.05) brightness({bright})">'
            f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,#0A1E7A,#050A33);mix-blend-mode:multiply;opacity:.22"></div></div>')
        self.p.box(label, x, y, w, h)
        self.frames.append(label)
        if anchor:
            ax, ay = anchor
            mids = [(x + w / 2, y), (x + w / 2, y + h), (x, y + h / 2), (x + w, y + h / 2)]          # top, bottom, left, right midpoints
            sx, sy = min(mids, key=lambda m: (m[0] - ax) ** 2 + (m[1] - ay) ** 2)
            self.lines.append((sx, sy, ax, ay))

    def reticles(self, size=46, arm=13):
        """Hairlines first, then a corner-bracket reticle at each anchor: four L-shaped corners, a gap in the middle of each side."""
        if not self.lines:
            return
        s = []
        for sx, sy, ax, ay in self.lines:
            s.append(f'<line x1="{sx}" y1="{sy}" x2="{ax}" y2="{ay}" stroke="{LINE}" stroke-width="2"/>')
        for k, (sx, sy, ax, ay) in enumerate(self.lines, 1):
            x0, y0, x1, y1 = ax - size / 2, ay - size / 2, ax + size / 2, ay + size / 2
            s.append(f'<rect x="{x0 + 2}" y="{y0 + 2}" width="{size - 4}" height="{size - 4}" fill="rgba(0,0,0,.18)"/>')       # a lift so the bracket reads on any photo
            for cx, cy, dx, dy in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
                s.append(f'<path d="M{cx + dx * arm} {cy} L{cx} {cy} L{cx} {cy + dy * arm}" fill="none" stroke="{LINE}" stroke-width="3" stroke-linecap="square"/>')
            self.p.box(f"ret{k}", ax - size / 2, ay - size / 2, size, size)
        self.P.append(f'<svg data-tag="callout-lines" width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute;left:0;top:0;z-index:9;pointer-events:none">{"".join(s)}</svg>')

    def label(self, txt="MASQUERADE SANGEET EDITION", cy=92):
        self.text("edition", txt, W // 2, cy, 640, 34,
                  f"font-weight:700;font-size:28px;letter-spacing:.2em;text-indent:.2em;color:{OFFWHITE};text-shadow:0 2px 14px rgba(0,0,0,.9)")

    def finish(self):
        self.reticles()
        self.p.overlays()
        return B.page(W, H, GROUND, "".join(self.P), grain=False)


def slide1():
    s = Slide(1)
    s.ground(NEW("01_dancers-silver-pillar-purple.jpg"), "50% 55%", .7)
    s.mask(450, 96, 566); s.badge(64, 70)
    s.title(64, 330, 952)
    s.frame("fA", NEW("09_boy-on-shoulders-star-balloon.jpg"), 64, 1005, 440, 275, "50% 38%", anchor=(284, 930))
    s.frame("fB", NEW("04_pink-ceiling-chandelier-phone.jpg"), 576, 1005, 440, 275, "50% 60%", bright=1.15, anchor=(796, 930))
    s.text("cue", "SWIPE&nbsp;&nbsp;&rarr;", W - 64 - 110, 62, 220, 34,
           f"font-weight:700;font-size:26px;letter-spacing:.24em;color:{GL};text-shadow:0 2px 12px rgba(0,0,0,.8)")
    return s


def slide2():
    s = Slide(2)
    s.ground(NEW("06_blue-room-crowd-faces.jpg"), "50% 50%", .62)
    s.label()
    s.frame("fA", NEW("07_pink-glare-girls-backs-phone.jpg"), 64, 150, 340, 255, "50% 50%", anchor=(520, 560))
    s.frame("fB", NEW("08_boy-on-shoulders-stage-lights-portrait.jpg"), 690, 190, 326, 430, "50% 45%", anchor=(740, 800))
    s.frame("fC", NEW("03_girls-dancing-yellow-top.jpg"), 64, 580, 350, 330, "50% 40%", anchor=(280, 1010))
    s.frame("fD", NEW("05_boys-crowd-green-light.jpg"), 640, 900, 376, 350, "50% 45%", anchor=(470, 1090))
    return s


def slide3():
    s = Slide(3)
    s.ground(NEW("07_pink-glare-girls-backs-phone.jpg"), "50% 50%", .7)
    s.label()
    s.frame("fA", NEW("01_dancers-silver-pillar-purple.jpg"), 676, 150, 340, 255, "50% 55%", bright=1.2, anchor=(560, 600))
    s.frame("fB", NEW("09_boy-on-shoulders-star-balloon.jpg"), 64, 330, 350, 330, "50% 40%", anchor=(380, 880))
    s.frame("fC", NEW("06_blue-room-crowd-faces.jpg"), 640, 700, 376, 340, "50% 55%", anchor=(380, 1060))
    return s


def slide4():
    s = Slide(4)
    s.ground(NEW("03_girls-dancing-yellow-top.jpg"), "50% 40%", .62)
    s.mask(450, 96, 566); s.badge(64, 70)
    s.title(90, 330, 900)
    s.text("status", "TICKET SALES OPEN SOON", W // 2, 920, 880, 62, f"font-weight:700;font-size:52px;color:{OFFWHITE};text-shadow:0 2px 14px rgba(0,0,0,.9)")
    s.P.append(f'<div data-tag="linkpill" style="position:absolute;left:315px;top:1010px;width:450px;height:103px;border-radius:22px;border:2px solid rgba(222,180,100,.75);'
               f'background:rgba(8,6,10,.7);z-index:12;display:flex;align-items:center;justify-content:center;font-family:var(--d);font-weight:700;font-size:54px;'
               f'line-height:1;color:{OFFWHITE};text-transform:uppercase">LINK IN BIO</div>')
    s.p.box("linkpill", 315, 1010, 450, 103)
    return s


BUILDERS = [slide1, slide2, slide3, slide4]


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        for i, build in enumerate(BUILDERS, 1):
            s = build()
            html = s.finish()
            labels = {e[0] for e in s.p.elements}
            pairs = [("title", "mask"), ("mask", "badge"), ("title", "badge")]
            for a in s.frames:
                for b in s.frames:
                    if a < b:
                        pairs.append((a, b))
            ignore = [pr for pr in pairs if pr[0] in labels and pr[1] in labels]
            text_pairs = [(lab, OFFWHITE, GROUND, 40, True) for lab in ("status", "edition") if lab in labels]
            await B.render(html, os.path.join(OUT, f"slide_{i:02d}.png"), W, H, elements=s.p.elements, collision_ignore=ignore, text_pairs=text_pairs,
                           containers=tuple(l for l in ("linkpill",) if l in labels),
                           bleed_tags=("title", "plate", "sparkles", "grain", "mask", "photo"),
                           crop_tags=("plate", "sparkles", "grain", "photo", "mask") + tuple(s.frames), page_bg=GROUND)
    from PIL import Image
    ims = [Image.open(os.path.join(OUT, f"slide_{i:02d}.png")).convert("RGB").resize((432, 540)) for i in range(1, N + 1)]
    sh = Image.new("RGB", (442 * N, 540), (40, 40, 40))
    for i, im in enumerate(ims):
        sh.paste(im, (i * 442, 0))
    sh.save(os.path.join(OUT, "sheet.png"))
    print("callout carousel done ->", OUT)

asyncio.run(main())
