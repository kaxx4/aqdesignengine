"""AQUATERRA HALL OF FAME — yearbook REWORK, 1080x1350.

Source: C:/Users/kanis/Downloads/Yearbook.pdf (12 pages, 810x1012.5pt = already 4:5).
Real member photos + copy extracted to scratchpad/yearbook_src/.

BRIEF: "rework while keeping things similar" — the SKELETON is preserved exactly:
    department eyebrow (top) -> polaroid photo card (tilted) -> circular nickname badge
    (top-right, overlapping the card) -> name (bottom) -> quote (very bottom) -> doodle scatter
    on a paper field.
What changes is the LANGUAGE, into AQ brand:
  - thin grey outline doodles      -> shapes.sticker() die-cuts, ink outline + colour halo
  - soft drop shadows              -> hard offset ink shadows (AQ craft layer)
  - all-serif display              -> NeutralFace 900 UPPERCASE + Eina + ONE Instrument Serif
                                      italic accent (the quote), per CLAUDE.md §9
  - beige/grey palette             -> AQ cream #F4EFE0 + one accent PER DEPARTMENT
  - handwritten "yearbook" mark    -> Instrument Serif italic accent word, same corner
"""
import asyncio, base64, json, os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join("engine", n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); S = load("shapes")

W, H = core.SIZES["feed"]; M = 64
A = core.ACCENTS; CREAM = "var(--bg)"; TON = core.text_on
SRC = "scratchpad/yearbook_src"

# one accent per department — the only colour decision, made once, applied consistently
DEPT = {"PROJECTS": A[3], "SOCIAL MEDIA": A[4], "MARKETING": A[0], "AQ VENTURES": A[5]}

def b64(p):
    with open(p, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()

def at(x, y, w, h, i, z=6, rot=0):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'z-index:{z};transform:rotate({rot}deg)">{i}</div>')
def mono(t, s=13, c="var(--ink)", ls=".12em"):
    return (f'<span style="font-family:var(--m);font-weight:700;font-size:{s}px;letter-spacing:{ls};'
            f'text-transform:uppercase;color:{c}">{t}</span>')

def paper():
    """Keeps the original's crumpled-paper feel, in AQ cream + faint speckle."""
    sp = "".join(f'<circle cx="{(i*197)%1080}" cy="{(i*313)%1350}" r="{1+(i%3)}" '
                 f'fill="#0A0A0A" opacity=".05"/>' for i in range(260))
    return (f'<div style="position:absolute;inset:0;background:{CREAM}"></div>'
            f'<svg style="position:absolute;inset:0;z-index:2" width="1080" height="1350" '
            f'xmlns="http://www.w3.org/2000/svg">{sp}</svg>')


def member_card(dept, nick_a, nick_b, quote, name, photo, idx):
    acc = DEPT[dept.upper()]
    els = []
    # 1. department eyebrow — same position as source, AQ display type
    els.append(at(M, 128, W - 2*M, 110,
        f'<div style="text-align:center;font-family:var(--d);font-weight:900;font-size:78px;'
        f'line-height:1;letter-spacing:.02em;text-transform:uppercase;color:var(--ink)">{dept}</div>', z=20))
    els.append(at(390, 238, 300, 8,
        f'<div style="width:100%;height:8px;background:{acc}"></div>', z=20))
    # 2. polaroid photo card, tilted — AQ craft: ink border + HARD offset shadow
    els.append(at(112, 296, 856, 800,
        f'<div style="width:100%;height:100%;background:#FFFFFF;border:7px solid var(--ink);'
        f'box-shadow:16px 16px 0 var(--ink);padding:20px 20px 70px 20px;box-sizing:border-box;'
        f'position:relative">'
        f'<img src="{b64(os.path.join(SRC, "photos", photo))}" '
        f'style="width:100%;height:100%;object-fit:cover;display:block">'
        f'<div style="position:absolute;left:0;right:0;bottom:22px;text-align:center">'
        + mono(f"AQ &middot; {dept} &middot; 2026", 13, "#6A6A6A") + "</div></div>", z=14, rot=-1.6))
    # 3. nickname badge, top-right, overlapping the card — AQ die-cut sticker
    els.append(at(748, 232, 262, 262,
        S.sticker(S.scallop(15), acc, size=262,
                  inner=S.label(nick_a.strip().upper(), 14, 45, fill=TON(acc))
                       + S.label(nick_b.strip().upper(), 14, 64, fill=TON(acc))), z=30, rot=7))
    # 4. the "yearbook" mark — same corner as source, AQ serif italic
    els.append(at(92, 306, 260, 70,
        f'<div style="font-family:var(--s);font-style:italic;font-size:42px;color:var(--ink)">'
        f'yearbook</div>', z=32, rot=-9))
    # 5. name + quote
    els.append(at(M, 1126, W - 2*M, 80,
        f'<div style="text-align:center;font-family:var(--d);font-weight:900;font-size:62px;'
        f'line-height:1;text-transform:uppercase;color:var(--ink)">{name}</div>', z=24))
    els.append(at(M, 1212, W - 2*M, 92,
        f'<div style="text-align:center;font-family:var(--s);font-style:italic;font-size:32px;'
        f'line-height:1.25;color:#2E2E2E">{quote}</div>', z=24))
    # 6. doodle scatter — AQ stickers in the cream margins only, never on the photo card
    doods = [(S.starburst(10), A[2], 40, 150, 88, 12), (S.blob(idx + 2, 8), acc, 972, 556, 82, 0),
             (S.scallop(12), A[6], 20, 636, 74, -8), (S.gear(9), A[1], 976, 946, 80, 6),
             (S.capsule(100, 40), A[2], 26, 1042, 92, -12)]
    for d, c, x, y, s, r in doods:
        els.append(at(x, y, s, s, S.sticker(d, c, size=s), z=26, rot=r))
    logo = f'<img src="{core.LOGO}" style="position:absolute;top:1272px;left:{M}px;height:28px;z-index:40">'
    idxtag = at(W - 210, 1274, 146, 34,
        f'<div style="text-align:right">' + mono(f"{idx:02d} / 11", 14, "#6A6A6A") + "</div>", z=40)
    return B.page(W, H, CREAM, paper() + "".join(els) + logo + idxtag, grain=True)


def cover():
    els = []
    for word, fs, y, rot in [("HALL", 186, 296, -2), ("OF", 186, 466, 3), ("FAME", 186, 636, -1)]:
        els.append(at(M, y, W - 2*M, 200,
            f'<div style="text-align:center;font-family:var(--d);font-weight:900;font-size:{fs}px;'
            f'line-height:1;text-transform:uppercase;color:var(--ink)">{word}</div>', z=20, rot=rot))
    els.append(at(M, 178, W - 2*M, 70,
        f'<div style="text-align:center">' + mono("AQUATERRA &middot; THE 2026 ROSTER", 20) + "</div>", z=20))
    els.append(at(M, 852, W - 2*M, 90,
        f'<div style="text-align:center;font-family:var(--s);font-style:italic;font-size:50px;'
        f'color:var(--ink)">eleven people who kept showing up.</div>', z=20))
    depts = [("PROJECTS", A[3], 3), ("SOCIAL MEDIA", A[4], 5), ("MARKETING", A[0], 2), ("AQ VENTURES", A[5], 1)]
    row = "".join(f'<span style="display:inline-block;background:{a};color:{TON(a)};'
                  f'border:4px solid var(--ink);border-radius:999px;padding:10px 22px;margin:5px;'
                  f'box-shadow:5px 5px 0 var(--ink);font-family:var(--m);font-weight:700;font-size:16px;'
                  f'letter-spacing:.08em">{d} &middot; {n}</span>' for d, a, n in depts)
    els.append(at(M, 968, W - 2*M, 170, f'<div style="text-align:center">{row}</div>', z=22))
    doods = [(S.starburst(11), A[2], 66, 296, 126, 12), (S.blob(3, 8), A[0], 892, 346, 116, 0),
             (S.scallop(13), A[6], 56, 618, 106, -8), (S.gear(10), A[1], 902, 656, 110, 6),
             (S.capsule(100, 40), A[5], 76, 896, 116, -10), (S.shield(), A[4], 912, 900, 96, 8)]
    for d, c, x, y, s, r in doods:
        els.append(at(x, y, s, s, S.sticker(d, c, size=s), z=26, rot=r))
    logo = f'<img src="{core.LOGO}" style="position:absolute;top:1232px;left:{M}px;height:36px;z-index:40">'
    foot = at(W - 330, 1240, 266, 34,
              f'<div style="text-align:right">' + mono("@NGO.AQUATERRA", 14, "#6A6A6A") + "</div>", z=40)
    return B.page(W, H, CREAM, paper() + "".join(els) + logo + foot, grain=True)


async def main():
    data = json.load(open(os.path.join(SRC, "members.json")))
    out = "out/yearbook_rework"; os.makedirs(out, exist_ok=True)
    await B.render(cover(), f"{out}/00_cover.png", W, H)
    for i, m in enumerate(data, start=1):
        L = m["lines"]
        dept, nick_a, nick_b = L[0], L[1], L[2]
        quote = " ".join(x for x in L[3:-1]).strip()
        name = L[-1]
        html = member_card(dept, nick_a, nick_b, quote, name, m["photo"], i)
        await B.render(html, f"{out}/{i:02d}_{name.split()[0].lower()}.png", W, H)
    print("done ->", out)

asyncio.run(main())
