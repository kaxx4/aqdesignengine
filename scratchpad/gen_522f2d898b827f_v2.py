"""Recreation — sample 522f2d89, right screen: the rotated-capsule pile.

MULTI-SCREEN REFERENCE. Per the standing ruling (CLAUDE.md section 5) one mechanism
is picked and recreated as a single AQ canvas. Two departures from habit here:

  * scored against a CROP of that screen (new: compare.crop), not the whole mockup.
    Comparing a poster to a picture of two phones on grey measures the grey, which is
    why every mockup recreation in the run so far was parked on the looking gate alone.
  * built on STORY (1080x1920, aspect 0.5625) rather than feed (0.8). The reference is
    a phone screen at 0.484; story is the AQ format that actually matches that shape,
    and is a real deliverable. Forcing it onto feed would have been a 40% aspect lie.

MEASURED (compare.geometry on the crop):
    content bbox  x 0.000..0.998  y 0.000..0.945   — bleeds off every edge
    coverage      0.692                            — very dense
    centroid      (0.491, 0.402)                   — mass sits HIGH
    occupancy     rows 0-7 saturated; row 8 fading; row 9 a centred button; row 10 a
                  short centred label

INVENTORY / ACCEPTANCE CHECKLIST
  1. black ground
  2. a dense pile of large ROTATED CAPSULES filling the top ~78%, bleeding off all four
     edges. Each is one flat accent colour, no outline, no shadow — flat vinyl.
  3. each capsule carries its label in INK, set ALONG the capsule's own angle
  4. capsules overlap heavily and in varied z-order; angles span roughly -60..+60 deg
  5. the pile stops cleanly — below it the ground is empty black
  6. a white pill button, centred, in the lower sixth
  7. a short label centred below the button
  8. no two adjacent capsules share a colour

AQ ADAPTATION
  * labels are real AQ workshop names from welfare_projects_rows.csv
  * the reference's "Sign in with Apple" -> a real AQ call to action
  * palette: the seven AQ accents. The reference uses ~9 hues including tints; AQ has 7
    and does not invent colours, so two repeat at maximum separation.
"""
import asyncio, os, sys, csv, io, math, random, importlib.util

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); lay = load("layout")

W, H = core.SIZES["story"]
SLUG = "522f2d898b827f"
OUT = f"out/versions/{SLUG}"
os.makedirs(OUT, exist_ok=True)
INK, CREAM, PAPER = core.INK, core.CREAM, core.PAPER
A = core.ACCENTS

LABELS = ["Roots in Mud", "Beyond the Stars", "Echoes of Joy", "Heal The Earth",
          "Speak Skillfully", "Hands at Work", "One for All", "Green Hour",
          "Bottled Greens", "Act It Out", "Planet First", "Smiles Shared",
          "Fun Fiesta", "Green Christmas"]
CTA = "Come to one."
SKIP = "or just read about them"

PILE_BOTTOM = 0.78          # measured: the pile stops around row 8 of 11
# MEASURED off the crop: a capsule is ~0.115 of screen height and 0.45-0.8 of its
# width. v1 used 132px on a 1920 canvas — barely half — which is why coverage came
# out 0.43x the reference and the pile read as scattered confetti on black.
CAP_H = int(0.115 * 1920)   # 221
FS = 62
MIN_CW = int(0.46 * 1080)   # no capsule shorter than 46% of the frame


async def main():
    rng = random.Random(7)
    m = await B.measure_text([{"text": t, "font": "e", "size": FS, "weight": 600}
                              for t in LABELS])
    widths = [x["w"] for x in m]

    els, P = [], []
    P.append(f'<div style="position:absolute;inset:0;background:{INK}"></div>')

    # ── the pile ────────────────────────────────────────────────────────────
    # Laid on a jittered 2-column grid over the pile region so the field is covered
    # evenly, then each capsule is rotated about its own centre. Generous overlap is
    # the POINT here — scatter_solve exists to avoid overlap and is the wrong tool.
    band_h = H * PILE_BOTTOM
    cols, rows = 3, 5
    prev_hue = None
    caps = []
    for i in range(len(LABELS)):
        r, c = divmod(i, cols)
        label, tw = LABELS[i], widths[i]
        cw = max(MIN_CW, tw + 110)
        cx = (c + 0.5) * (W / cols) + rng.uniform(-0.16, 0.16) * W
        cy = (r + 0.5) * (band_h / rows) + rng.uniform(-0.07, 0.07) * band_h
        rot = rng.uniform(-58, 58)
        choices = [k for k in range(len(A)) if k != prev_hue]
        hue = rng.choice(choices); prev_hue = hue
        caps.append(dict(i=i, label=label, cw=cw, cx=cx, cy=cy, rot=rot,
                         fill=A[hue], z=10 + i))

    # The LABEL box, not the capsule, is what must stay readable: heavy capsule
    # overlap is the whole effect, one capsule covering another's words never is.
    lab_boxes = []
    for cp in caps:
        lw = widths[cp["i"]] + 20
        lab_boxes.append((f'c{cp["i"]}',
                          lay.rotated_bbox(cp["cx"] - lw / 2, cp["cy"] - FS * 0.62,
                                           lw, FS * 1.24, cp["rot"]),
                          cp["z"]))
    zmap, unresolved = lay.resolve_label_z(lab_boxes, min_visible=0.80)
    if unresolved:
        print(f"    ! labels still covered after z-resolution: {unresolved} "
              f"— these need MOVING, not restacking")
    for cp in caps:
        cp["z"] = zmap.get(f'c{cp["i"]}', cp["z"])

    for cp in caps:
        cw, cx, cy, rot, fill = cp["cw"], cp["cx"], cp["cy"], cp["rot"], cp["fill"]
        P.append(
            f'<div style="position:absolute;left:{cx-cw/2:.1f}px;top:{cy-CAP_H/2:.1f}px;'
            f'width:{cw:.1f}px;height:{CAP_H}px;background:{fill};border-radius:999px;'
            f'transform:rotate({rot:.1f}deg);z-index:{cp["z"]};display:flex;'
            f'align-items:center;justify-content:center;overflow:hidden">'
            f'<span style="font-family:var(--e);font-weight:600;font-size:{FS}px;'
            f'color:{core.text_on(fill)};white-space:nowrap">{cp["label"]}</span></div>')
        els.append((f'cap{cp["i"]}', *lay.rotated_bbox(cx - cw / 2, cy - CAP_H / 2,
                                                       cw, CAP_H, rot)))

    # ── the button + label ──────────────────────────────────────────────────
    bw, bh = W * 0.62, 108
    by = H * 0.855
    P.append(f'<div style="position:absolute;left:{(W-bw)/2}px;top:{by}px;width:{bw}px;'
             f'height:{bh}px;background:{PAPER};border-radius:999px;z-index:40;'
             f'display:flex;align-items:center;justify-content:center">'
             f'<span style="font-family:var(--e);font-weight:600;font-size:40px;'
             f'color:{INK}">{CTA}</span></div>')
    els.append(("cta", (W - bw) / 2, by, bw, bh))
    P.append(f'<div style="position:absolute;left:0;top:{by+bh+40}px;width:{W}px;'
             f'text-align:center;font-family:var(--e);font-size:34px;color:{CREAM};'
             f'opacity:.85;z-index:40">{SKIP}</div>')
    els.append(("skip", W * 0.2, by + bh + 40, W * 0.6, 44))

    html = B.page(W, H, INK, "".join(P), grain=False)
    lay.preflight(W, H, els, html=html, page_bg=INK, core=core,
                  collision_ignore=frozenset())
    async with B.session():
        await B.render(html, f"{OUT}/v2.png", W, H)
    print(f"  -> {OUT}/v2.png  ({W}x{H}, aspect {W/H:.3f} vs reference 0.484)")

asyncio.run(main())
