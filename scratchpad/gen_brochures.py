"""TWO A4 TRIFOLD BROCHURES for the Disco Diwali 2026 programme (user brief 2026-10-09): SPONSORS and STALLS, printable.

Format: A4 LANDSCAPE, letter-fold (3 panels of 99mm). Two sheets per brochure:
  sheet 1 = OUTSIDE  [ inside flap | back cover | front cover ]   (the flap folds in behind the front cover)
  sheet 2 = INSIDE   [ left | centre | right ]
Printed double-sided, flip on the SHORT edge. Rendered at 1123x794 CSS px (A4 at 96dpi) x3 = 3369x2382 px, and the PDF is stamped at the
resolution that makes each page exactly 297x210mm.

Same design system as the decks (engine/deckkit.py): cream ground, paper cards, 28px photo frames, one accent family, one heading style.
Print adaptations (CLAUDE.md sec 2 rule 4), recorded:
  * type sizes are print-scaled: body 12.5-13.5px (~9.5-10pt), mono labels >=10px (~7.5pt), titles 34-44px.
  * 8mm (30px) safe margin inside every panel; NO bleed and NO CMYK conversion (screen sRGB art). Ask the printer before relying on edge-to-edge
    colour: the cream ground is a full-bleed fill, so a printer that needs 3mm bleed will need the art extended.
  * the inside flap panel is drawn the same width as the others (a real letter-fold flap is ~1-2mm narrower; the printer's template governs).
  * copy and numbers are the master deck's. Nothing new is claimed. Prices, fees, venue and the firm date are not in the source, so none appear.

Run:  python scratchpad/gen_brochures.py        ->  out/decks/brochures/{sponsors,stalls}_trifold_outside.png / _inside.png / .pdf
"""
import asyncio, importlib.util, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


K = _load("deckkit", "engine/deckkit.py")
B = _load("build", "engine/build.py")
core = K.core
from PIL import Image

PRIV = os.path.join(ROOT, "scratchpad", "sponsorship_private")
FACTS = json.load(open(os.path.join(PRIV, "facts.json"))) if os.path.exists(os.path.join(PRIV, "facts.json")) else {}
OUT = os.path.join(ROOT, "out", "decks", "brochures")
W, H, PW = 1123, 794, 374          # A4 landscape in CSS px, one panel
G, BL, LM, INK, MUTE = K.GREEN, K.BLUE, K.LEMON, K.INK, K.MUTE
TONES = [G, BL, LM]
NL = "\n"

CSS = f"""
.sheet{{display:flex;width:{W}px;height:{H}px;background:{K.BG};font-family:var(--e);color:{INK};position:relative}}
.pn{{width:{PW}px;height:{H}px;padding:30px;display:flex;flex-direction:column;gap:14px;position:relative;overflow:hidden;min-height:0}}
.pn.t-g{{background:{G}}}.pn.t-l{{background:{LM}}}.pn.t-b{{background:{BL};color:#fff}}.pn.t-k{{background:{K.DARK};color:{K.CREAM_ON_DARK}}}
.bt{{font-family:var(--d);font-weight:900;text-transform:uppercase;line-height:.95;letter-spacing:-.01em;margin:0}}
.bt em{{font-family:var(--s);font-style:italic;font-weight:400;text-transform:none;letter-spacing:0;background:linear-gradient(transparent 58%,{LM} 58%,{LM} 92%,transparent 92%);padding:0 .06em}}
.t-l .bt em{{background:linear-gradient(transparent 58%,{G} 58%,{G} 92%,transparent 92%)}}
.t-g .bt em,.t-b .bt em{{background:linear-gradient(transparent 58%,{LM} 58%,{LM} 92%,transparent 92%);color:{INK}}}
.t-k .bt em{{color:{K.CREAM_ON_DARK};background:linear-gradient(transparent 58%,#B8860B 58%,#B8860B 92%,transparent 92%)}}
.bp{{font:400 13px/1.38 var(--e);color:{K.INK2};margin:0}}
.t-b .bp,.t-k .bp{{color:inherit}}
.bl{{font:700 10.7px var(--m);letter-spacing:.1em;text-transform:uppercase;color:#4A4A44}}
.t-b .bl,.t-k .bl{{color:rgba(255,255,255,.78)}}
.bc{{background:{K.PAPER};border:1.2px solid {K.LINE};border-radius:16px;padding:14px 16px;box-shadow:0 10px 22px -18px rgba(10,10,10,.4)}}
.bk{{font-family:var(--d);font-weight:900;line-height:.92;letter-spacing:-.01em}}
.bchip{{display:inline-flex;align-items:center;padding:6px 14px;border-radius:999px;font:600 12px var(--e);white-space:nowrap}}
.pn .ph{{box-shadow:0 0 0 1.2px {K.LINE}}}
.bu{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:7px}}
.bu li{{display:flex;gap:9px;align-items:flex-start;font:400 12.5px/1.3 var(--e);color:{K.INK2}}}
.bu li svg{{flex:none;margin-top:1px}}
"""


def page(inner):
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{core.FONTS}{core.ROOT}*{{margin:0;box-sizing:border-box}}body{{background:{K.BG}}}{K.CSS}{CSS}</style></head>'
            f'<body>{inner}</body></html>')


def sheet(panels):
    return page(f'<div class="sheet p">{"".join(panels)}</div>')


def pn(inner, tone=None, style=""):
    return f'<div class="pn{(" t-" + tone) if tone else ""}" style="{style}">{inner}</div>'


def ph(i, focus="50% 50%", r=18, style=""):
    return f'<div style="width:100%;height:100%;min-height:0;{style}">{K.photo(i, focus, r=r)}</div>'


def eb(text, dot=G):
    return f'<div class="bl" style="display:flex;align-items:center;gap:8px"><i style="width:9px;height:9px;border-radius:50%;background:{dot};display:block"></i>{K.esc(text)}</div>'


def bt(text, size=38):
    import re
    t = K.esc(text).replace("\n", "<br>")
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t, count=1)
    return f'<h2 class="bt" style="font-size:{size}px">{t}</h2>'


def chip(text, bg, fg=None):
    return f'<span class="bchip" style="background:{bg};color:{fg or core.text_on(bg)}">{K.esc(text)}</span>'


def stat(v, label, tone=G, ic=None, size=40):
    d = f'<span style="width:30px;height:30px;border-radius:50%;background:{tone};color:{core.text_on(tone)};display:flex;align-items:center;justify-content:center;flex:none">{K.icon(ic, 16)}</span>' if ic else ""
    return f'<div class="bc" style="display:flex;flex-direction:column;gap:6px;justify-content:space-between;min-height:0">{d}<div><div class="bk" style="font-size:{size}px">{K.esc(v)}</div><div class="bp" style="font-size:11.5px;line-height:1.25;margin-top:3px">{K.esc(label)}</div></div></div>'


def ul(items, ic="check"):
    return '<ul class="bu">' + "".join(f"<li>{K.icon(ic, 15, K.GREEN_D, 2.4)}<span>{K.esc(i)}</span></li>" for i in items) + "</ul>"


def logo(h=22):
    return f'<img src="{core.LOGO}" style="height:{h}px;display:block" alt="AquaTerra">'


def poster_thumb(p, r=10):
    src = K.crop_uri(p[0], p[1]) if isinstance(p, tuple) else K.uri(K.asset(p))
    return f'<div style="width:100%;aspect-ratio:4/5;background:url({src}) center/cover;border-radius:{r}px;box-shadow:0 0 0 1px {K.LINE}"></div>'


POSTERS = [(132, (0, .19, 1, .728)), (134, (0, .19, 1, .728)), 136, (138, (0, .19, 1, .728)), (142, (0, .19, 1, .728)), (146, (0, .095, 1, .865))]


def contact_panel(photo=130, focus="50% 40%"):
    ct = FACTS.get("contact", {}); rg = FACTS.get("reg", {})
    qr = K.uri("../terrathon/qr_instagram_ngo_aquaterra.svg")
    row = lambda ic, t: f'<div style="display:flex;align-items:center;gap:10px;font:600 13px var(--e)">{K.icon(ic, 17, K.GREEN_D)}<span>{K.esc(t)}</span></div>'
    inner = (f'{logo(26)}<div style="flex:1;min-height:0">{ph(photo, focus, 18)}</div>{eb("Get in touch")}{bt(ct.get("name", ""), 34)}'
             f'<div style="display:flex;flex-direction:column;gap:9px;margin-top:6px">{row("phone", ct.get("phone", ""))}{row("insta", ct.get("insta", ""))}{row("globe", ct.get("web", ""))}{row("mail", ct.get("mail", ""))}</div>'
             f'<div class="bc" style="display:flex;gap:12px;align-items:center;margin-top:10px"><img src="{qr}" style="width:78px;border-radius:6px" alt="QR code for @ngo.aquaterra"><div><div class="bk" style="font-size:18px;text-transform:uppercase">Follow the work</div><div class="bl" style="margin-top:5px">instagram.com/ngo.aquaterra</div></div></div>'
             f'<div style="display:flex;flex-direction:column;gap:6px;margin-top:10px;align-items:flex-start">{chip(rg.get("tax", "80G certified"), G)}{chip("Registration no. " + rg.get("darpan", ""), BL)}'
             f'<div class="bp" style="font-size:11px">{K.esc(rg.get("trust", ""))}. {K.esc(rg.get("csr", ""))}.</div></div>')
    return pn(inner)


# ───────────────────────── SPONSORS TRIFOLD ─────────────────────────
def sponsors():
    flap = pn(f'{eb("The proof", LM)}<div class="bk" style="font-size:78px;color:{G};margin-top:6px">₹22.5L+</div><div class="bp" style="color:inherit;margin-top:-4px">raised for welfare across five of our six flagship events</div>'
              f'<div class="bk" style="font-size:44px;color:{LM};margin-top:10px">2,850+</div><div class="bp" style="color:inherit;margin-top:-4px">guests across the same five</div>'
              f'<div style="flex:1;min-height:0;margin-top:6px">{ph(126, "50% 40%", 16)}</div>'
              f'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px">{"".join(poster_thumb(p, 8) for p in POSTERS)}</div>'
              f'<div class="bl" style="margin-top:6px">Six flagship events and counting.</div>', "k")
    back = contact_panel(184, "50% 50%")
    front = pn(f'<div style="display:flex;justify-content:space-between;align-items:center">{logo(24)}{chip("Nov 2026 (tentative)", LM)}</div>'
               f'<div style="flex:1;min-height:0;margin-top:6px">{ph(148, "50% 38%", 22)}</div>'
               f'{eb("Sponsorship & partnership proposal")}<h1 class="bt" style="font-size:78px;margin-top:-2px">Disco<br><em>Diwali</em></h1>'
               f'<p class="bp" style="font-size:13.5px">The flagship Diwali fundraiser from AquaTerra, Kolkata’s student-run NGO. Every net rupee goes to welfare work.</p>'
               f'<div style="display:flex;gap:6px;flex-wrap:wrap">{chip("All for charity", G)}{chip("400+ expected", INK, K.CREAM_ON_DARK)}</div>')
    left = pn(f'{eb("About AquaTerra")}{bt("A student-run NGO that *delivers*", 31)}'
              f'<p class="bp">A registered NGO in Kolkata. We power some of the city’s biggest youth-led fundraising events, and every net rupee goes back into welfare work across the city.</p>'
              f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:9px">{stat("5+", "years of student welfare work", G, "calendar", 34)}{stat("1.5K+", "student volunteers", BL, "users", 34)}{stat("500+", "welfare projects", LM, "heart", 34)}{stat("5K+", "Instagram followers", G, "insta", 34)}</div>'
              f'<div style="flex:1;min-height:0">{ph(34, "40% 50%", 18)}</div>')
    pie = K.donut([("9-10", 29, G), ("11-12", 45, BL), ("College", 26, LM)], 300, 150)
    leg = "".join(f'<div style="display:flex;align-items:center;gap:7px;font:600 11.5px var(--e)"><i style="width:10px;height:10px;border-radius:50%;background:{c};display:block"></i>{n}</div>' for n, c in [("Class 9-10  29%", G), ("Class 11-12  45%", BL), ("College  26%", LM)])
    centre = pn(f'{eb("The night")}{bt("One night, *four* reasons", 31)}'
                f'<div style="display:flex;align-items:flex-end;gap:12px"><div class="bk" style="font-size:66px;color:{K.GREEN_D}">400+</div><div class="bp" style="padding-bottom:8px">expected at the party</div></div>'
                f'<div class="bp"><b>Tentative date:</b> 2nd week of November 2026.<br><b>Who:</b> school (classes 6-12) and college students.</div>'
                f'<ul class="bu">' + "".join(f"<li>{K.icon(ic, 15, K.GREEN_D, 2)}<span>{t}</span></li>" for ic, t in [("store", "Food and sales stalls"), ("sparkle", "A traditional Diwali event"), ("music", "A DJ-led party night"), ("gift", "Cash prizes and surprise gifts")]) + '</ul>'
                f'<div style="display:flex;align-items:center;gap:10px" class="bc">{pie.replace("width=\"300\" height=\"300\"", "width=\"104\" height=\"104\"")}<div style="display:flex;flex-direction:column;gap:5px">{leg}<div class="bl" style="font-size:10.7px">Survey of 1,810 respondents</div></div></div>'
                f'<div style="flex:1;min-height:0">{ph(194, "50% 40%", 18)}</div>')
    tiers = [("Title sponsor", "Powered by", LM, ["Exclusive standee spots on the night", "30+ stories and interactions", "Grid of 3 Instagram posts", "Emcee mentions, chief guest slot"]),
             ("Co-sponsor", "Second billing", BL, ["Exclusive standee spots on the night", "20+ stories and interactions", "1 exclusive Instagram post"]),
             ("Associate sponsor", "Visible partner", G, ["Standees at the event", "5+ stories and interactions", "Stall space at the event"])]
    cards = "".join(f'<div class="bc" style="padding:12px 14px"><div style="display:flex;justify-content:space-between;align-items:center">{chip(n, t, INK)}<span class="bl" style="font-size:10.7px">{sub}</span></div>'
                    f'<div style="margin-top:9px">{ul(it)}</div></div>' for n, sub, t, it in tiers)
    right = pn(f'{eb("Ways to partner")}{bt("Pick your *place* in the night", 31)}{cards}'
               f'<div class="bc" style="padding:12px 14px"><div class="bl">Also open</div><div class="bp" style="margin-top:6px;font-size:12px"><b>Education and media partners</b>, <b>in-kind partners</b> (media, stationery, gift) and <b>category sponsors</b> (hydration, fashion). Ask us for the full deck.</div></div>'
               f'<div style="flex:1;min-height:0">{ph(192, "50% 35%", 18)}</div>')
    return [flap, back, front], [left, centre, right]


# ───────────────────────── STALLS TRIFOLD ─────────────────────────
def stalls():
    flap = pn(f'{eb("Past stalls", LM)}{bt("The stalls, *last time*", 31)}'
              f'<div style="flex:1;min-height:0;display:grid;grid-template-rows:1.2fr 1fr 1fr;gap:9px">{ph(186, "50% 40%", 14)}{ph(130, "50% 40%", 14)}{ph(192, "50% 40%", 14)}</div>'
              f'<div class="bl">Not a one-off. Six flagship events and counting.</div>', "k")
    back = contact_panel(178, "50% 50%")
    front = pn(f'<div style="display:flex;justify-content:space-between;align-items:center">{logo(24)}{chip("Stalls open 4:00 PM", G)}</div>'
               f'<div style="flex:1;min-height:0;margin-top:6px">{ph(182, "50% 45%", 22)}</div>'
               f'{eb("Take a stall")}<h1 class="bt" style="font-size:78px;margin-top:-2px">Disco<br><em>Diwali</em></h1>'
               f'<p class="bp" style="font-size:13.5px">Put your stall in front of Kolkata’s school and college students at AquaTerra’s flagship Diwali fundraiser.</p>'
               f'<div style="display:flex;gap:6px;flex-wrap:wrap">{chip("2nd week of Nov 2026 (tentative)", LM)}{chip("400+ expected", INK, K.CREAM_ON_DARK)}</div>')
    pie = K.donut([("9-10", 29, G), ("11-12", 45, BL), ("College", 26, LM)], 300, 150)
    leg = "".join(f'<div style="display:flex;align-items:center;gap:7px;font:600 11.5px var(--e)"><i style="width:10px;height:10px;border-radius:50%;background:{c};display:block"></i>{n}</div>' for n, c in [("Class 9-10  29%", G), ("Class 11-12  45%", BL), ("College  26%", LM)])
    ben = [("pin", "Spots we know you’ll love"), ("wand", "Basic amenities and support"), ("megaphone", "Dedicated shoutouts"), ("store", "Ample stall space"),
           ("users", "Connect directly with your audience"), ("target", "Benefit from high footfall at the event")]
    left = pn(f'{eb("Why a stall")}{bt("A room full of *students*", 31)}'
              f'<div style="display:flex;align-items:flex-end;gap:12px"><div class="bk" style="font-size:66px;color:{K.GREEN_D}">400+</div><div class="bp" style="padding-bottom:8px">expected at the party</div></div>'
              f'<div class="bc" style="display:flex;align-items:center;gap:10px">{pie.replace("width=\"300\" height=\"300\"", "width=\"104\" height=\"104\"")}<div style="display:flex;flex-direction:column;gap:5px">{leg}<div class="bl" style="font-size:10.7px">Survey of 1,810 respondents</div></div></div>'
              f'<div style="flex:1;min-height:0">{ph(190, "50% 45%", 18)}</div>')
    ros = [("1:00 PM", "Decor and venue setup"), ("3:00 PM", "Stall setup"), ("4:00 PM", "Stalls go live, DJ and sound setup"), ("5:30 PM", "Team and vendor briefing"),
           ("6:30 PM", "Registrations open"), ("7:45 PM", "Dhol entry and opening"), ("8:00 - 9:00 PM", "DJ set: peak hours"), ("9:00 PM", "Closing moment")]
    tl = "".join(f'<div style="display:flex;gap:10px;align-items:flex-start;padding:7px 0;{"border-top:1.2px solid " + K.LINE + ";" if i else ""}"><div style="width:118px;flex:none">{chip(t, INK, K.CREAM_ON_DARK)}</div>'
                 f'<div style="font:600 12.5px/1.25 var(--e);padding-top:4px">{n}</div></div>' for i, (t, n) in enumerate(ros))
    centre = pn(f'{eb("Run of show")}{bt("The day, *hour* by hour", 31)}<div class="bc" style="padding:6px 14px">{tl}</div>'
                f'<div class="bp" style="font-size:12px"><b>Setup from 3:00 PM. Stalls go live at 4:00 PM.</b> The night ends at 9:00 PM.</div><div style="flex:1;min-height:0">{ph(184, "50% 50%", 18)}</div>')
    steps = [("1", "Call or message us", "Tell us what you sell and what you want from the night."), ("2", "We share the details", "Fees, layout and terms, matched to your stall."), ("3", "Lock your spot", "We confirm placement and send the run of show.")]
    cards = "".join(f'<div class="bc" style="display:flex;gap:12px;align-items:center;padding:12px 14px"><div class="bk" style="font-size:44px;color:{TONES[i % 3] if i != 2 else K.GREEN_D}">{n}</div><div><div style="font:900 15px/1.05 var(--d);text-transform:uppercase">{h}</div><div class="bp" style="font-size:12px;margin-top:4px">{d}</div></div></div>' for i, (n, h, d) in enumerate(steps))
    right = pn(f'{eb("Next step")}{bt("Fees and terms, *on request*", 31)}<p class="bp">We share fees, layout and terms once you are interested, so we can match them to your stall.</p>{cards}'
               f'<div class="bc" style="padding:12px 14px"><div class="bl">What a stall gets</div><div style="margin-top:7px">{ul([t for _, t in ben[:3]] + ["Marketing and coverage"])}</div></div>'
               f'<div style="flex:1;min-height:0">{ph(126, "50% 40%", 18)}</div>')
    return [flap, back, front], [left, centre, right]


# ── PRINT BUILD: 3mm bleed + crop and fold marks, 300 dpi ───────────────────────────────────────────────
BLEED, SLUG = 12, 22                           # ~3.2mm bleed (>= 3mm) and ~5.8mm slug, whole CSS px so the canvas is an integer
M_ = BLEED + SLUG                           # trim box offset inside the print canvas
PWc, PHc = W + 2 * M_, H + 2 * M_


def print_page(panels, fills):
    """The sheet inside a bleed + slug canvas. fills = [(x, y, w, h, colour)] in TRIM coordinates, drawn first, so a full-bleed colour
    (the cream ground, a dark flap) runs 3mm past the cut. Crop marks sit in the slug; fold marks are two short ticks above the trim."""
    bg = "".join(f'<div style="position:absolute;left:{M_ + x}px;top:{M_ + y}px;width:{w}px;height:{h}px;background:{c}"></div>' for x, y, w, h, c in fills)
    ln = lambda x, y, w, h: f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:#000"></div>'
    L = 14
    marks = ""
    for cx in (M_, M_ + W):
        for cy in (M_, M_ + H):
            sx = -1 if cx == M_ else 1; sy = -1 if cy == M_ else 1
            x0 = cx + sx * (BLEED + 3) if sx > 0 else cx - (BLEED + 3) - L
            y0 = cy + sy * (BLEED + 3) if sy > 0 else cy - (BLEED + 3) - L
            marks += ln(x0, cy, L, .75) + ln(cx, y0, .75, L)
    for k in (1, 2):
        fx = M_ + k * PW
        marks += ln(fx, M_ - BLEED - 3 - 10, .75, 10) + ln(fx, M_ + H + BLEED + 3, .75, 10)
    inner = (f'<div class="p" style="position:relative;width:{PWc}px;height:{PHc}px;background:#fff;overflow:hidden">{bg}'
             f'<div class="sheet" style="position:absolute;left:{M_}px;top:{M_}px;background:transparent">{"".join(panels)}</div>{marks}</div>')
    return page(inner)


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session(scale=3):
        for name, fn in [("sponsors", sponsors), ("stalls", stalls)]:
            out_p, in_p = fn()
            for tag, panels in (("outside", out_p), ("inside", in_p)):
                await B.render(sheet(panels), f"{OUT}/{name}_trifold_{tag}.png", W, H, page_bg=K.BG, margin=20)
            pages = [Image.open(f"{OUT}/{name}_trifold_{t}.png").convert("RGB") for t in ("outside", "inside")]
            pages[0].save(f"{OUT}/{name}_trifold.pdf", save_all=True, append_images=pages[1:], resolution=288, quality=92)
            print("brochure", name, pages[0].size)
    async with B.session(scale=3.125):                          # 300 dpi exactly: 96 css px/in x 3.125 = 300 px/in
        for name, fn in [("sponsors", sponsors), ("stalls", stalls)]:
            out_p, in_p = fn()
            fills_in = [(-BLEED, -BLEED, W + 2 * BLEED, H + 2 * BLEED, K.BG)]
            fills_out = fills_in + [(-BLEED, -BLEED, PW + BLEED, H + 2 * BLEED, K.DARK)]
            files = []
            for tag, panels, fills in (("outside", out_p, fills_out), ("inside", in_p, fills_in)):
                f = f"{OUT}/{name}_trifold_PRINT_{tag}.png"
                await B.render(print_page(panels, fills), f, PWc, PHc, page_bg="#fff", margin=0)
                files.append(f)
            pg = [Image.open(f).convert("RGB") for f in files]
            pg[0].save(f"{OUT}/{name}_trifold_PRINT.pdf", save_all=True, append_images=pg[1:], resolution=300, quality=95)
            print("print", name, pg[0].size)


if __name__ == "__main__":
    asyncio.run(main())
