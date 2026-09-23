"""AQ GANDHI JAYANTI WISH — feed (1080x1350) + story (1080x1920). Workflow C: fresh
seasonal content, bespoke build from primitives (no single reference to match).

MOTIFS CHOSEN: Gandhi's round wire-frame spectacles (the single most recognisable visual
shorthand for him — safer and more legible at poster scale than a portrait, which the
real-assets-only rule would forbid fabricating anyway) + a charkha (spinning wheel, the
second most iconic symbol, standing for self-reliance/simplicity). Both hand-drawn flat
SVG, ink-outlined, hard-shadowed — the house craft layer — never a stock photo or a
fabricated portrait.

TONE: "cute" per the brief means warm and gently illustrated, not silly — this is a
national civic holiday, not a birthday-party graphic. Kept the palette restrained (mint
hero + pink as the one constant highlight, per house rule) and the copy short and warm
rather than jokey. Values are named (truth / peace / simplicity) rather than a quoted
Gandhi line, to sidestep the many misattributed "Gandhi quotes" in circulation — the
real-assets-only rule extends to real-facts-only for attributed speech.
"""
import asyncio, os, sys, importlib.util
_r = os.path.abspath(__file__)
while _r != os.path.dirname(_r) and not os.path.exists(os.path.join(_r, "CLAUDE.md")):
    _r = os.path.dirname(_r)
os.chdir(_r)
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

# This session's playwright pip package (1.63) expects a chrome-headless-shell revision
# the pre-installed browser cache doesn't have (only chromium-1194, the full build). Every
# engine call site (`build.py`, `audit.py`, `reconcile.py`) calls `.launch()` with no
# executable_path, so patch the one shared BrowserType.launch to default to the real
# chrome binary that IS on disk, rather than editing five engine files for a local env quirk.
import playwright.async_api._generated as _pw_gen
_CHROME_BIN = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
if os.path.exists(_CHROME_BIN):
    _orig_launch = _pw_gen.BrowserType.launch
    async def _patched_launch(self, **kwargs):
        kwargs.setdefault("executable_path", _CHROME_BIN)
        return await _orig_launch(self, **kwargs)
    _pw_gen.BrowserType.launch = _patched_launch

core = load("core"); B = load("build"); dd = load("doodles"); sh = load("shapes"); lay = load("layout")

INK, CREAM = core.INK, core.CREAM
A = core.ACCENTS
PINK, MINT, LEMON, TOMATO, SKY, GRAPE, TEAL = A
M = 64

# ═════════════════════════════════════════════════════════════════ FURNITURE
def logo(x=M, y=54, h=44):
    return f'<img src="{core.LOGO}" style="position:absolute;top:{y}px;left:{x}px;height:{h}px;z-index:30">'

def eyebrow_chip(txt, acc, x, y):
    fg = core.text_on(acc)
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;z-index:25;font-family:var(--m);'
            f'font-weight:700;font-size:16px;letter-spacing:.12em;text-transform:uppercase;'
            f'color:{fg};background:{acc};border:3px solid {INK};border-radius:999px;'
            f'padding:9px 20px;box-shadow:5px 5px 0 {INK};white-space:nowrap">{txt}</div>')

def pill(txt, acc, x, y):
    fg = core.text_on(acc)
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;z-index:24;font-family:var(--m);'
            f'font-weight:700;font-size:15px;letter-spacing:.1em;text-transform:uppercase;'
            f'color:{fg};background:{acc};border:3px solid {INK};border-radius:999px;'
            f'padding:8px 18px;box-shadow:4px 4px 0 {INK};white-space:nowrap">{txt}</div>')

def footer():
    return (f'<div style="position:absolute;bottom:52px;left:{M}px;z-index:30;font-family:var(--m);'
            f'font-weight:700;font-size:15px;letter-spacing:.06em;color:{INK}">@ngo.aquaterra</div>')

def signoff(x, y, w):
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;width:{w}px;z-index:24;'
            f'font-family:var(--m);font-weight:500;font-size:16px;letter-spacing:.03em;'
            f'line-height:1.5;color:rgba(10,10,10,.55)">with warmth,<br>'
            f'<span style="font-weight:700;color:{INK}">team aquaterra</span></div>')

def svgbox(inner, x, y, size, vb_w, vb_h, rot=0, z=14):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{size}px;'
            f'height:{size * vb_h / vb_w:.1f}px;z-index:{z};transform:rotate({rot}deg)">'
            f'<svg viewBox="0 0 {vb_w} {vb_h}" width="100%" height="100%" style="overflow:visible" '
            f'xmlns="http://www.w3.org/2000/svg">{inner}</svg></div>')

def doodle(kind, x, y, size, fill, rot=0, z=16):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;'
            f'z-index:{z}">{dd.stamp(kind, fill, rot=rot)}</div>')


# ═════════════════════════════════════════════════════════════════ HAND-DRAWN ICONS
def icon_glasses():
    """Round wire-frame spectacles — Gandhi's single most recognisable visual shorthand.
    viewBox 480x260. Cream lenses (not a fabricated face inside them) + a tiny mint leaf
    tucked at one temple, the one cute/warm liberty taken."""
    LX, RX, CY, R = 150, 330, 140, 80
    g = (
        f'<g transform="translate(8,10)"><circle cx="{LX}" cy="{CY}" r="{R}" fill="{INK}"/>'
        f'<circle cx="{RX}" cy="{CY}" r="{R}" fill="{INK}"/></g>'
        f'<path d="M{LX - R + 24} {CY - 34} L{LX - R - 46} {CY - 52}" stroke="{INK}" stroke-width="20" stroke-linecap="round"/>'
        f'<path d="M{RX + R - 24} {CY - 34} L{RX + R + 46} {CY - 52}" stroke="{INK}" stroke-width="20" stroke-linecap="round"/>'
        f'<path d="M{LX + R - 4} {CY - 4} Q{(LX + RX) / 2} {CY - 24} {RX - R + 4} {CY - 4}" '
        f'fill="none" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>'
        f'<circle cx="{LX}" cy="{CY}" r="{R}" fill="{CREAM}" stroke="{INK}" stroke-width="12"/>'
        f'<circle cx="{RX}" cy="{CY}" r="{R}" fill="{CREAM}" stroke="{INK}" stroke-width="12"/>'
        f'<circle cx="{LX - 28}" cy="{CY - 32}" r="10" fill="#FFFFFF" opacity=".55"/>'
        f'<circle cx="{RX - 28}" cy="{CY - 32}" r="10" fill="#FFFFFF" opacity=".55"/>'
        # tiny leaf tucked at the right temple — the one cute liberty
        f'<g transform="translate({RX + R + 20},{CY - 66}) rotate(18)">'
        f'<path d="M0 20 Q6 0 24 0 Q18 20 0 20 Z" fill="{MINT}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
        f'<path d="M2 18 Q12 10 22 3" fill="none" stroke="{INK}" stroke-width="3"/></g>'
    )
    return g, 480, 260


def icon_charkha(acc):
    """A charkha (spinning wheel) — self-reliance, simplicity. Flat line icon: rim, hub,
    eight spokes, a small stand, a spindle with a bobbin. viewBox 300x300."""
    CX, CY, RR = 150, 118, 92
    spokes = "".join(
        f'<line x1="{CX}" y1="{CY}" x2="{CX + RR * 0.92 * __import__("math").cos(a)}" '
        f'y2="{CY + RR * 0.92 * __import__("math").sin(a)}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
        for a in [i * 3.14159265 / 4 for i in range(8)]
    )
    g = (
        f'<circle cx="{CX}" cy="{CY}" r="{RR}" fill="none" stroke="{INK}" stroke-width="14"/>'
        f'<circle cx="{CX}" cy="{CY}" r="{RR}" fill="none" stroke="{acc}" stroke-width="6"/>'
        + spokes +
        f'<circle cx="{CX}" cy="{CY}" r="16" fill="{acc}" stroke="{INK}" stroke-width="7"/>'
        # stand
        f'<path d="M{CX - 46} 258 L{CX - 18} {CY + RR - 6} L{CX + 18} {CY + RR - 6} L{CX + 46} 258 Z" '
        f'fill="{CREAM}" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
        f'<rect x="{CX - 60}" y="252" width="120" height="16" rx="8" fill="{INK}"/>'
        # spindle + bobbin, extending right
        f'<line x1="{CX + RR}" y1="{CY}" x2="264" y2="{CY}" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
        f'<rect x="252" y="{CY - 22}" width="34" height="44" rx="10" fill="{acc}" stroke="{INK}" stroke-width="8"/>'
    )
    return g, 300, 300


# ═════════════════════════════════════════════════════════════════ POSTER BUILDER
async def build(W, H, story=False):
    # No separate bg div: B.page()'s `.p` element already paints CREAM full-bleed —
    # a second div matching it exactly is a same-as-page-bg "invisible fill" by definition.
    els, parts = [], []

    parts.append(logo()); els.append(("logo", M, 54, 160, 44))
    chip_x = W - M - 340 if not story else W - M - 340
    parts.append(eyebrow_chip("02 OCT &middot; GANDHI JAYANTI", MINT, chip_x, 58))
    els.append(("chip", chip_x, 58, 340, 46))

    # sized to clear dominance_check's 12%-of-canvas hero floor at this aspect (480x260)
    hero_size = 580 if not story else 700
    hero_y = 150 if not story else 190
    g_inner, g_w, g_h = icon_glasses()
    hero_x = (W - hero_size) / 2
    hero_rot = -2
    parts.append(svgbox(g_inner, hero_x, hero_y, hero_size, g_w, g_h, rot=hero_rot))
    hero_h = hero_size * g_h / g_w
    els.append(("hero", *lay.rotated_bbox(hero_x, hero_y, hero_size, hero_h, hero_rot)))

    # balancing accents either side of the hero, in the free margins
    parts.append(doodle("leaf", W - M - 96, hero_y + hero_h * 0.15, 84, MINT, rot=-10))
    els.append(("leaf1", *lay.rotated_bbox(W - M - 96, hero_y + hero_h * 0.15, 84, 84, -10)))
    parts.append(doodle("dots", M + 4, hero_y + hero_h * 0.35, 70, SKY, rot=0))
    els.append(("dots1", M + 4, hero_y + hero_h * 0.35, 70, 70))

    head_y = hero_y + hero_h + (34 if not story else 46)
    fs_head = 106 if not story else 128
    head_txt = "GANDHI<br>JAYANTI"
    hm = await B.measure_text([{"text": "GANDHI", "font": "d", "size": fs_head, "weight": 900,
                                 "letter_spacing": "-.03em", "max_width": W - 2 * M}], W, H)
    line_h = hm[0]["ink_h"]
    head_h = line_h * 2 * 0.98
    parts.append(f'<div style="position:absolute;top:{head_y}px;left:{M}px;width:{W - 2 * M}px;'
                  f'z-index:22;font-family:var(--d);font-weight:900;font-size:{fs_head}px;'
                  f'line-height:.9;letter-spacing:-.03em;color:{INK};text-transform:uppercase">{head_txt}</div>')
    els.append(("head", M, head_y, W - 2 * M, head_h))

    sub_y = head_y + head_h + (26 if not story else 34)
    fs_sub = 38 if not story else 46
    sub_txt = (f'peace isn&rsquo;t one big gesture &mdash; it&rsquo;s a hundred '
               f'<span style="font-family:var(--s);font-style:italic;color:{MINT}">quiet</span> ones.')
    sub_w = W - 2 * M if not story else W - 2 * M - 60
    parts.append(f'<div style="position:absolute;top:{sub_y}px;left:{M}px;width:{sub_w}px;'
                  f'z-index:22;font-family:var(--e);font-weight:400;font-size:{fs_sub}px;'
                  f'line-height:1.3;letter-spacing:-.015em;color:{INK}">{sub_txt}</div>')
    sub_h = (fs_sub * 1.3 * 2) if not story else (fs_sub * 1.3 * 2)
    els.append(("sub", M, sub_y, sub_w, sub_h))

    pills_y = sub_y + sub_h + (22 if not story else 30)
    words = [("truth", TOMATO), ("peace", SKY), ("simplicity", LEMON)]
    px = M
    pill_positions = []
    for i, (w_txt, acc) in enumerate(words):
        pw = 130 + len(w_txt) * 9
        parts.append(pill(w_txt, acc, px, pills_y))
        els.append((f"pill{i}", px, pills_y, pw, 42))
        pill_positions.append((f"pill{i}", px, pills_y, pw, 42))
        px += pw + 16

    # charkha badge, bottom-left — reinforces the theme, balances the bottom-right sparkle.
    # Placed FORWARD from the pills row (not anchored to canvas bottom): anchoring it to H
    # left a ~400px dead run on the story canvas once the hero/headline grew to clear the
    # dominance floor above.
    ch_size = 150 if not story else 190
    if not story:
        ch_y = pills_y + 42 + 70
    else:
        # Forward flow from the pills row left a 350px dead run before the footer on the
        # taller story canvas once the hero/headline grew to clear the dominance floor.
        # Anchoring the block to the bottom instead just MOVED the hole to before it (still
        # one big empty run, only above the charkha). Splitting the slack into two equal
        # gaps — pills-to-charkha and sign-off-to-footer — spreads it as margin on both
        # sides of the block instead of leaving it as a single dead run on either.
        tail_h = ch_size + 46 + 70   # charkha + its gap to the sign-off + the sign-off block
        slack = (H - 70) - (pills_y + 42) - tail_h
        ch_y = pills_y + 42 + slack / 2
    ch_rot = -4
    ch_inner, ch_w, ch_h = icon_charkha(TEAL)
    parts.append(svgbox(ch_inner, M, ch_y, ch_size, ch_w, ch_h, rot=ch_rot))
    els.append(("charkha", *lay.rotated_bbox(M, ch_y, ch_size, ch_size, ch_rot)))

    spark_x, spark_y, spark_rot = W - M - 110, ch_y + 10, 12
    parts.append(doodle("sparkle", spark_x, spark_y, 96, PINK, rot=spark_rot))
    els.append(("sparkle1", *lay.rotated_bbox(spark_x, spark_y, 96, 96, spark_rot)))

    if story:
        so_w = 420
        parts.append(signoff(M, ch_y + ch_size + 46, so_w))
        els.append(("signoff", M, ch_y + ch_size + 46, so_w, 70))

    parts.append(footer()); els.append(("footer", M, H - 70, 300, 20))

    html_inner = "".join(parts)
    html = B.page(W, H, CREAM, html_inner, grain=True)

    text_pairs = [
        ("head", INK, CREAM, fs_head, True),
        ("sub", INK, CREAM, fs_sub, False),
    ] + [(f"pill{i}", core.text_on(acc), acc, 15, True) for i, (_, acc) in enumerate(words)]
    color_pairs = [(f"pill{i}", acc, CREAM) for i, (_, acc) in enumerate(words)]

    pf = lay.preflight(W, H, els, html=html, color_pairs=color_pairs, text_pairs=text_pairs,
                        page_bg=CREAM, core=core, expect_hero=True)
    return html, els, color_pairs, text_pairs, pf


async def main():
    os.makedirs("out", exist_ok=True)
    async with B.session():
        Wf, Hf = core.SIZES["feed"]
        html, els, cp, tp, pf = await build(Wf, Hf, story=False)
        print("FEED preflight clean=", pf.get("clean"), pf.get("issues", pf.get("summary")))
        await B.render(html, "out/gandhi_jayanti_feed.png", Wf, Hf, elements=els,
                        color_pairs=cp, text_pairs=tp, page_bg=CREAM, expect_hero=True)

        Ws, Hs = core.SIZES["story"]
        html2, els2, cp2, tp2, pf2 = await build(Ws, Hs, story=True)
        print("STORY preflight clean=", pf2.get("clean"), pf2.get("issues", pf2.get("summary")))
        await B.render(html2, "out/gandhi_jayanti_story.png", Ws, Hs, elements=els2,
                        color_pairs=cp2, text_pairs=tp2, page_bg=CREAM, expect_hero=True)
    print("DONE")

asyncio.run(main())
