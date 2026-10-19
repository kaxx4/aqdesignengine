"""DISCO DIWALI carousel, "the selection" (user inspo, 2026-10-18: a soft full-bleed photo with one line of copy SELECTED in a text editor: a pale
highlight, gold drag handles and a Cut / Copy / Paste / Delete menu floating above, the brand name small at the foot).

MECHANISM (kept): the line is the message, the editing UI is the voice. Each slide selects one supplied line, as if the sentence were being drafted
live. The menu is identical on every slide; only the selected words change.

Slides (1080x1350, feed 4:5):
  01 "Disco Diwali. Masquerade Sangeet Edition."
  02 "Ticket sales open soon."
  03 "All for charity."
  04 "More details to follow. Link in the bio."

COPY (R12, nothing invented): every selected line is supplied copy. No date, time or location (user, 2026-10-14). The link is for joining the group and is
never called a booking link; the copy says only "link in the bio" (user, 2026-10-18).

CAROUSEL RULES CARRIED FROM THE CHAT CAROUSEL (user, 2026-10-18): the LIVE / ALL FOR CHARITY badge top left, the copper-red mask top right, and the SAME
lockup footer, same size and place on every slide.

ADAPTATIONS (sec 2 ladder, all recorded):
  - The inspo's "FoundHER HAUS" is another brand's name and its quote is another brand's copy; replaced by the Disco Diwali lockup and supplied lines.
  - The selection UI is drawn, laid over a real photo, not a fabricated screenshot. Its cream highlight, gold handles and red Delete are the borrowed
    device's colours and sit outside the format palette on purpose, like the chat carousel's bubbles. Body type is Eina (sec 9).
  - R2 (one hero = the lockup) bends: the selected line is the hero on every slide, the lockup signs off.
  - CONSENT: many people in these photos look like minors; none has a consent record. Check before any public post.

Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_select_carousel.py     -> out/discodiwali/carousel/select/slide_NN.png (+ sheet.png)
"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B, GROUND = dd.B, dd.GROUND
OUT = os.path.join(ROOT, "out", "discodiwali", "carousel", "select")
HALL = os.path.join(ROOT, "engine", "assets", "img", "events", "disco-diwali-hall-2026-10-14")
HP = lambda n: os.path.join(HALL, n)
W, H, N, M = 1080, 1350, 4, 64
FS, LH, BARH, PADX = 56, 84, 74, 16                           # selected type size, line pitch, highlight bar height, bar padding
HL, INK, HANDLE = "#FBF1CB", "#26231C", "#E5A800"
TX = 96                                                       # left edge of the selected text block
BBOX_T = (265, 315, 1983, 1315)
BRIEF = dict(edition="Masquerade Sangeet Edition", status="Ticket sales open soon")

SLIDES = [
    dict(photo=HP("06_blue-room-crowd-faces.jpg"), focus="30% 50%", bright=.85, lines=["Disco Diwali.", "Masquerade Sangeet Edition."]),
    dict(photo=HP("01_dancers-silver-pillar-purple.jpg"), focus="70% 50%", bright=.9, lines=["Ticket sales open soon."]),
    dict(photo=HP("09_boy-on-shoulders-star-balloon.jpg"), focus="22% 50%", bright=.95, lines=["All for charity."]),
    dict(photo=HP("03_girls-dancing-yellow-top.jpg"), focus="30% 50%", bright=1.0, lines=["More details to follow.", "Link in the bio."]),
]

CSS = (f".sel{{position:absolute;box-sizing:border-box;background:{HL};color:{INK};font-family:var(--e);font-weight:400;font-size:{FS}px;line-height:1;"
       f"white-space:nowrap;z-index:12;height:{BARH}px;display:flex;align-items:center;padding:0 {PADX}px}}"
       f".menu{{position:absolute;box-sizing:border-box;z-index:13;height:88px;border-radius:44px;background:#fff;display:flex;align-items:center;"
       f"font-family:var(--e);font-weight:400;font-size:40px;color:#111;box-shadow:0 10px 30px rgba(0,0,0,.3);padding:0 8px 0 40px;gap:0}}"
       f".menu span.i{{padding:0 30px 0 0;margin-right:30px;border-right:2px solid #E4E4E4;line-height:44px;height:44px;display:block}}"
       f".menu span.i.last{{border-right:0;margin-right:14px;padding-right:0}}.menu span.del{{color:#E5383B}}"
       f".menu .chev{{flex:none;width:72px;height:72px;border-radius:50%;background:#EDEDED;display:flex;align-items:center;justify-content:center}}"
       f".handle{{position:absolute;z-index:14;width:38px;height:38px;border-radius:50%;background:{HANDLE};box-shadow:0 2px 8px rgba(0,0,0,.3)}}"
       f".stem{{position:absolute;z-index:14;width:5px;background:{HANDLE}}}")
SPARK = ('<svg width="40" height="40" viewBox="0 0 40 40" style="margin-right:22px"><circle cx="20" cy="20" r="14" fill="none" stroke="#111" stroke-width="3"/>'
         '<path d="M20 9v22M9 20h22M12 12l16 16M28 12L12 28" stroke="#111" stroke-width="2.6" stroke-linecap="round"/></svg>')
CHEV = '<span class="chev"><svg width="22" height="30" viewBox="0 0 22 30"><path d="M5 4l12 11L5 26" fill="none" stroke="#111" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg></span>'


class Slide:
    def __init__(self, spec, widths):
        self.spec, self.widths = spec, widths
        self.p = dd.Poster("poster_ref", BRIEF, "feed")
        self.p.parts.clear(); self.p.elements.clear()
        self.P = self.p.parts

    def ground(self):
        s = self.spec
        self.P.append(f'<div style="position:absolute;inset:0;background:{GROUND}"></div>')
        self.P.append(f'<img data-tag="photo" src="{dd.photo_uri(s["photo"])}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;'
                      f'object-position:{s["focus"]};z-index:1;filter:contrast(1.05) saturate(1.0) brightness({s["bright"]})">')
        self.P.append('<div data-tag="plate" style="position:absolute;inset:0;z-index:2;background:linear-gradient(180deg,#0A1E7A,#050A33);mix-blend-mode:multiply;opacity:.25"></div>')
        self.P.append('<div data-tag="plate" style="position:absolute;inset:0;z-index:3;background:linear-gradient(180deg,rgba(0,0,0,.35) 0%,rgba(0,0,0,0) 30%,'
                      'rgba(0,0,0,0) 55%,rgba(0,0,0,.82) 100%)"></div>')

    def top(self):
        bw = 236
        self.p.img("live_badge.png", M, 70, bw, z=8, tag="badge"); self.p.box("badge", M, 70, bw, round(bw * 1005 / 1061))
        x0, y0, x1, y1 = 157, 211, 1563, 1135; w = 520; k = w / (x1 - x0); vx, vy = W - M - w, 62
        self.p.img("mask_copper.png", round(vx - x0 * k), round(vy - y0 * k), round(1680 * k), z=6, tag="mask", extra="filter:drop-shadow(0 8px 26px rgba(0,0,0,.6));")
        self.p.box("mask", vx, vy, w, round((y1 - y0) * k))

    def selection(self, ty=600):
        lines = self.spec["lines"]; n = len(lines)
        for i, ln in enumerate(lines):
            w = round(self.widths[ln] + 2 * PADX); y = ty + i * LH
            self.P.append(f'<div data-tag="sel{i + 1}" class="sel" style="left:{TX}px;top:{y}px;width:{w}px">{ln}</div>')
            self.p.box(f"sel{i + 1}", TX, y, w, BARH)
        lw = round(self.widths[lines[-1]] + 2 * PADX); ly = ty + (n - 1) * LH
        # drag handles: a gold dot on a stem at the start (above the first bar) and at the end (below the last bar)
        self.P.append(f'<div class="stem" style="left:{TX - 3}px;top:{ty - 18}px;height:{BARH + 18}px"></div><div class="handle" data-tag="h1" style="left:{TX - 19}px;top:{ty - 52}px"></div>')
        self.p.box("h1", TX - 19, ty - 52, 38, 38)
        ex = TX + lw
        self.P.append(f'<div class="stem" style="left:{ex - 2}px;top:{ly}px;height:{BARH + 14}px"></div><div class="handle" data-tag="h2" style="left:{ex - 19}px;top:{ly + BARH + 10}px"></div>')
        self.p.box("h2", ex - 19, ly + BARH + 10, 38, 38)
        mw, my = 820, ty - 52 - 28 - 88
        self.P.append(f'<div data-tag="menu" class="menu" style="left:{(W - mw) // 2}px;top:{my}px;width:{mw}px"><span class="i">Cut</span><span class="i">Copy</span>'
                      f'<span class="i">Paste</span><span class="i del">Delete</span><span class="i last" style="display:flex;align-items:center;margin-left:-6px">{SPARK}</span>{CHEV}</div>')
        self.p.box("menu", (W - mw) // 2, my, mw, 88)

    def lockup(self, w=480):
        x0, y0, x1, y1 = BBOX_T; k = w / (x1 - x0); vh = round((y1 - y0) * k)
        vx, vy = (W - w) // 2, H - 70 - vh
        self.p.img("title_lockup.png", round(vx - x0 * k), round(vy - y0 * k), round(2000 * k), z=9, tag="title")
        self.p.box("title", vx, vy, w, vh)

    def finish(self):
        self.p.overlays()
        return B.page(W, H, GROUND, "".join(self.P), grain=False).replace("</style>", CSS + "</style>", 1)


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        texts = sorted({ln for s in SLIDES for ln in s["lines"]})
        res = await B.measure_text([dict(text=t, font="e", size=FS, weight=400) for t in texts])
        widths = {t: r["text_w"] for t, r in zip(texts, res)}
        for i, spec in enumerate(SLIDES, 1):
            s = Slide(spec, widths)
            s.ground(); s.top(); s.selection(); s.lockup()
            html = s.finish()
            labels = {e[0] for e in s.p.elements}
            ign = [("h1", "sel1"), ("h2", "sel1"), ("h2", "sel2"), ("menu", "h1"), ("sel1", "sel2"), ("mask", "menu")]
            ign = [p for p in ign if p[0] in labels and p[1] in labels]
            await B.render(html, os.path.join(OUT, f"slide_{i:02d}.png"), W, H, elements=s.p.elements, collision_ignore=ign,
                           text_pairs=[("sel1", INK, HL, FS, False)], bleed_tags=("title", "plate", "sparkles", "grain", "photo", "mask"),
                           crop_tags=("plate", "sparkles", "grain", "photo"), page_bg=GROUND)
    from PIL import Image
    ims = [Image.open(os.path.join(OUT, f"slide_{i:02d}.png")).convert("RGB").resize((432, 540)) for i in range(1, N + 1)]
    sh = Image.new("RGB", (442 * N, 540), (40, 40, 40))
    for i, im in enumerate(ims):
        sh.paste(im, (i * 442, 0))
    sh.save(os.path.join(OUT, "sheet.png")); print("select carousel done ->", OUT)

asyncio.run(main())
