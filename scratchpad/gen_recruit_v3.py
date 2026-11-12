"""AQ recruitment push v3: the ECOSYSTEM wave. One piece per lane family, each wearing one of the owner's five
reference formats (cast list, fill-in-the-blank, the note, the full-bleed hero, the website page), so the feed is not
"that is the events post". Plan and lane table: brain/RECRUITMENT_ECOSYSTEM_NOV2026.md.

  a_loop       THE LOOP (connector)   hero      "we throw parties, we sell t-shirts, the dogs eat"
  b_sundarbans WELFARE: trips         cast      "these people ran a health camp in the Sundarbans"
  c_tails      WELFARE: drives        blank     Tails and Treats, edition 53
  d_teach      WELFARE: teaching      note      "you are not too young"
  e_crftd      CRFTD                  blank     a blank T-shirt at a school fest
  f_shikshaq   SHIKSHAQ               chat      11 days to find a tutor
  g_diaries    MAGAZINE and BLOGS     site      stories from the ground, by whoever was there
  h_doors      THE DOORS (connector)  site      every department, one form
  a_loop_story / d_teach_story        stories

ADAPTATIONS (precedence ladder, CLAUDE.md section 2), same as v2: the owner's references win on typography in the
serif pieces; fake UI became real AQ facts; ground is AQ cream; photos are real AQ photos. The welfare photos show
children and stay LOCAL-ONLY (engine/assets/img/events/welfare-feed-2026/, gitignored): this script only runs where they
exist, see the README beside them for how to re-pull them.
"""
import os, sys, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_recruit_v2 as V
core, B, dd = V.core, V.B, V.dd
W = V.W
INK, CREAM, URL = V.INK, V.CREAM, V.URL
PINK, MINT, LEM, TOM, SKY, GRAPE, TEAL = core.ACCENTS
WL = "events/welfare-feed-2026/"
OUT = "out/recruit_nov2026/v3"

# ------------------------------------------------------------------ shared pieces
def glass(x, y, w, h, inner="", r=24, a=.34):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{r}px;background:rgba(255,255,255,{a});'
            f'backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border:2px solid rgba(255,255,255,.55);z-index:12;'
            f'box-shadow:0 8px 30px rgba(0,0,0,.18)">{inner}</div>')

def pill(x, y, label, col, rot=0, icon="sparkle"):
    wpx = int(len(label) * 16 + 98)
    ic = (f'<div style="position:absolute;left:10px;top:10px;width:44px;height:44px;border-radius:50%;background:{col};z-index:2;'
          f'display:flex;align-items:center;justify-content:center"><div style="position:relative;width:26px;height:26px">{dd.stamp(icon, "#fff")}</div></div>')
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{wpx}px;height:64px;border-radius:18px;background:rgba(255,255,255,.82);'
            f'border:2px solid rgba(255,255,255,.9);z-index:14;transform:rotate({rot}deg);box-shadow:0 6px 18px rgba(0,0,0,.25);'
            f'font-family:var(--e);font-weight:600;font-size:25px;line-height:64px;color:#0A0A0A;padding-left:66px">{ic}{label}</div>')

def lane_chip(label, col, x=64, y=116):
    return V.t(label, x, y, 15, color=core.text_on(col), font="m", weight=700, ls=.06, upper=True, tag="lane",
               extra=f"background:{col};border:3px solid #0A0A0A;box-shadow:4px 4px 0 #0A0A0A;padding:6px 12px;", z=30)

def series_tab(y=58):
    s = "(just a student)"; w = int(len(s) * 15 * .66 + 34)
    return V.t(s, W - 64 - w, y, 15, color=INK, font="m", weight=700, ls=.06, upper=True, tag="series",
               extra=f"background:{LEM};border:3px solid #0A0A0A;box-shadow:4px 4px 0 #0A0A0A;padding:6px 12px;", z=30)

# ------------------------------------------------------------------ FORMAT: full-bleed hero (reference 4)
async def hero(sp, story=False):
    H = V.H
    ts, ms, bs = (170, (H - 1350) // 2, H - 1350 - 258) if story else (0, 0, 0)
    ph = V.cover(sp["photo"], W, H, fx=sp.get("fx", .5), fy=sp.get("fy", .5))
    P = [V.img(V.uri(ph), 0, 0, W, H, z=1),
         V.box(0, 0, W, H, "background:linear-gradient(180deg,rgba(6,12,30,.38),rgba(6,12,30,.22) 45%,rgba(6,12,30,.62));", z=2)]
    lines = sp["lines"]
    ws = await V.mw([dict(text=s_, font="d", size=150, weight=900) for s_ in lines])
    size = int(150 * min(1.0, 940 / max(ws))); step = round(size * .95); y0 = sp.get("y0", 470) + ms
    for i, s_ in enumerate(lines):
        P.append(V.t(s_, 0, y0 + i * step, size, color="#fff", font="d", weight=900, w=W, lh=step, extra="text-align:center;", tag=f"h{i}", upper=True))
    for (label, col, icon, x, k, off, rot) in sp["pills"]:
        P.append(pill(x, y0 + step * k + off, label, col, rot, icon))
    c1, c2, c3 = sp["card"]
    card = (f'<div style="position:absolute;left:22px;top:20px;width:12px;height:12px;border-radius:50%;background:#2ecc71"></div>'
            f'<div style="position:absolute;left:44px;top:12px;font-family:var(--e);font-size:17px;color:#0A0A0A">{c1}</div>'
            f'<div style="position:absolute;left:22px;top:42px;font-family:var(--e);font-weight:600;font-size:23px;color:#0A0A0A">{c2}</div>'
            f'<div style="position:absolute;left:22px;top:78px;width:330px;font-family:var(--e);font-size:17px;line-height:24px;color:#222">{c3}</div>')
    P.append(glass(64, 150 + ts, 380, 140, card, r=26, a=.5))
    P.append(V.logo_pill(425, 44 + ts, dark=True))
    P.append(f'<div style="position:absolute;left:880px;top:{210+ts}px;width:120px;height:120px;z-index:10">{dd.stamp("spiral", "#FFC700", rot=20)}</div>')
    P.append(f'<div style="position:absolute;left:910px;top:{330+ts}px;width:110px;height:60px;z-index:10">{dd.stamp("zigzag", "#3DA9FC")}</div>')
    P.append(f'<div style="position:absolute;left:150px;top:{960+ms}px;width:74px;height:74px;z-index:10">{dd.stamp("zigzag", "#FF4D8C", rot=-20)}</div>')
    P.append(V.t(sp["caption"], 64, 1160 + bs, 24, color="#fff", font="e", weight=600, w=290, lh=33, tag="capt"))
    icons = "".join(f'<div style="width:66px;height:66px;border-radius:18px;background:{c};display:flex;align-items:center;justify-content:center;border:2px solid rgba(255,255,255,.7)">'
                    f'<div style="position:relative;width:40px;height:40px">{dd.stamp(k, "#0A0A0A")}</div></div>' for c, k in sp["dock"])
    P.append(glass(372, 1176 + bs, 328, 98, f'<div style="display:flex;gap:12px;padding:14px 16px">{icons}</div>', r=28, a=.3))
    for k in (2, 1):
        P.append(glass(730 + k * 10, 1176 + bs - k * 12, 290, 112, "", r=18, a=.22))
    s1, s2, s3 = sp["stack"]
    P.append(glass(730, 1176 + bs, 290, 112, (f'<div style="position:absolute;left:18px;top:12px;font-family:var(--m);font-size:13px;font-weight:700;color:#222">{s1}</div>'
                                              f'<div style="position:absolute;left:18px;top:36px;font-family:var(--e);font-weight:600;font-size:24px;color:#0A0A0A">{s2}</div>'
                                              f'<div style="position:absolute;left:18px;top:72px;font-family:var(--m);font-weight:700;font-size:14px;color:#0A0A0A">{s3}</div>'), r=18, a=.62))
    return sp["name"] + ("_story" if story else ""), V.page("".join(P), bg="#0b1030"), []

# ------------------------------------------------------------------ FORMAT: cast list (reference 1)
def cast(sp):
    H = V.H
    m = V.mono(V.cover(sp["photo"], W, H, fx=sp.get("fx", .5), fy=sp.get("fy", .4)), contrast=sp.get("contrast", 1.08))
    P = [V.img(V.uri(m), 0, 0, W, H, z=1),
         V.box(0, 0, W, sp.get("fade", 520), "background:linear-gradient(180deg,rgba(236,236,232,.96) 0%,rgba(236,236,232,.9) 52%,rgba(236,236,232,0) 100%);", z=2)]
    for (x, y, w, h, c, label, side) in sp["wins"]:
        P.append(V.box(x, y, w, h, f"background:{c};mix-blend-mode:multiply;opacity:.92;", z=6))
        lw = int(len(label) * 8.1 + 22); th = 26
        tx = x + w - lw if side in ("tr", "br") else x
        ty = y - th if side in ("tr", "tl") else y + h
        P.append(f'<div style="position:absolute;left:{tx}px;top:{ty}px;height:{th}px;padding:0 10px;background:{c};z-index:9;font-family:var(--e);font-weight:600;'
                 f'font-size:14.5px;line-height:{th}px;color:#0A0A0A;white-space:nowrap">{label}</div>')
    px, py = sp.get("para_xy", (64, 120))
    P.append(V.t(sp["para"], px, py, 17, color="#0A0A0A", w=340, lh=27, tag="para"))
    for (txt, x, y, size, ital) in sp["title"]:
        P.append(V.t(txt, x, y, size, font="s", italic=ital, lh=size, tag="ttl", z=9))
    P.append(V.t("by @ngo.aquaterra", sp["by_xy"][0], sp["by_xy"][1], 20, font="e", weight=600, tag="by"))
    P.append(V.logo_pill(64, 48))
    return sp["name"], V.page("".join(P)), [("para", px, py, 340, 190)]

# ------------------------------------------------------------------ FORMAT: fill-in-the-blank (reference 2)
def blank(sp):
    from PIL import ImageDraw
    H = V.H; PH_Y = sp.get("ph_y", 560); PH_H = H - PH_Y; S = V.S
    base = V.cover(sp["photo"], W, PH_H, fx=sp.get("fx", .5), fy=sp.get("fy", .3), zoom=sp.get("zoom", 1.0))
    boxes = sp["boxes"]
    punched = base.copy(); d = ImageDraw.Draw(punched)
    for (x, y, w, h) in boxes:
        d.rectangle([x * S, y * S, (x + w) * S, (y + h) * S], fill=V.hexrgb(CREAM))
    P = [V.img(V.uri(punched), 0, PH_Y, W, PH_H, z=2)]
    def thumb(i, th=66):
        x, y, w, h = boxes[i]
        crop = base.crop((round(x * S), round(y * S), round((x + w) * S), round((y + h) * S)))
        tw = round(th * w / h)
        return (f'<img src="{V.uri(crop)}" style="display:inline-block;vertical-align:middle;height:{th}px;width:{tw}px;object-fit:cover;'
                f'margin:0 6px;border-radius:5px;border:2px solid #0A0A0A">')
    body = sp["sentence"].format(*[thumb(i) for i in range(len(boxes))])
    P.append(f'<div style="position:absolute;left:56px;top:{sp.get("text_y",150)}px;width:968px;text-align:center;font-family:var(--e);font-weight:400;'
             f'font-size:{sp.get("fs",31)}px;line-height:{sp.get("lh",84)}px;color:#0A0A0A;z-index:8">{body}</div>')
    P.append(V.logo_pill(64, 46)); P.append(series_tab(50))
    P.append(lane_chip(sp["lane"][0], sp["lane"][1], 64, 112))
    return sp["name"], V.page("".join(P)), []

# ------------------------------------------------------------------ FORMAT: the note (reference 3)
def note(sp, story=False):
    H = V.H
    TB, ys = (330, 230) if story else (150, 0)
    pal = ["#0d2413", "#17391c", "#245a24", "#3f7a2a", "#7a9a35", "#b9b04a", "#e6dca0"]
    pal2 = ["#0d2413", "#143018", "#1d4524", "#276028", "#3a7a2c", "#5b8f31", "#86a038", "#b0ab45", "#d3c673", "#ece3ad"]
    bg = V.posterise(V.cover(sp["bg"], W, H - TB, fy=sp.get("bg_fy", .45)), pal, blur=5)
    cp = V.posterise(V.cover(sp["card_photo"], 480, 360, fy=sp.get("cp_fy", .5)), pal2, blur=1)
    P = [V.img(V.uri(bg, "PNG"), 0, TB, W, H - TB, z=1), V.box(0, 0, W, TB, f"background:{CREAM};", z=2)]
    P.append(V.t(sp["cap_top"], 0, 66 + (196 if story else 0), 31, font="s", italic=True, w=W, lh=40, extra="text-align:center;", tag="cap"))
    P.append(V.logo_pill(64, 24 + (182 if story else 0)))
    cx, cy, cw, ch = 64, 330 + ys, 560, 700
    P.append(V.box(560, TB, 520, H - TB, "background:linear-gradient(90deg,rgba(6,22,10,0),rgba(6,22,10,.5) 35%,rgba(6,22,10,.55));", z=3))
    P.append(V.box(0, H - (340 if story else 170), W, 340 if story else 170, "background:linear-gradient(180deg,rgba(6,22,10,0),rgba(6,22,10,.72));", z=3))
    P.append(V.box(cx, cy, cw, ch, "background:rgba(244,239,224,.62);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border:3px solid rgba(255,255,255,.8);", z=4))
    P.append(V.img(V.uri(cp, "PNG"), cx + 26, cy + 58, cw - 52, 410, z=5, extra="border:3px solid #fff;object-fit:cover;"))
    P.append(V.t(sp["pre"], cx + 28, cy + 505, 34, color="#0A0A0A", font="e", weight=400, tag="n1"))
    P.append(f'<div style="position:absolute;left:{cx+28}px;top:{cy+550}px;padding:4px 18px 8px;background:{SKY};z-index:6;font-family:var(--e);font-weight:600;font-size:70px;line-height:80px;color:#0A0A0A">{sp["chip"]}</div>')
    rx, rw = 656, 360
    P.append(V.t(sp["p1"], rx, 360 + ys, 25, font="s", italic=True, color="#fff", w=rw, lh=34, extra="text-align:right;", tag="p1"))
    P.append(f'<div style="position:absolute;left:{1016-292}px;top:{640+ys}px;padding:5px 12px;background:{SKY};z-index:8;font-family:var(--m);font-weight:700;font-size:15px;color:#0A0A0A">{URL}</div>')
    P.append(V.stick("run", "#fff", 96, 690, 700 + ys)); P.append(V.stick("jump", "#fff", 96, 800, 692 + ys)); P.append(V.stick("wave", "#fff", 96, 905, 700 + ys))
    P.append(V.t(sp["p2"], rx, 960 + ys, 25, font="s", italic=True, color="#fff", w=rw, lh=34, extra="text-align:right;", tag="p2"))
    P.append(V.t(sp["cap_bot"], 0, 1500 if story else 1262, 28, font="s", italic=True, color="#fff", w=W, lh=36, extra="text-align:center;", tag="cap2"))
    return sp["name"] + ("_story" if story else ""), V.page("".join(P)), []

# ------------------------------------------------------------------ FORMAT: website page (reference 5)
def site(sp):
    H = V.H; P = []
    P.append(B.logo(dark=False, x=48, y=26))
    for i, s_ in enumerate(sp["nav"]):
        P.append(V.t(s_, 330 + i * 130, 30, 19, font="e", weight=400, tag=f"nav{i}"))
    P.append(f'<div style="position:absolute;right:0;top:0;width:190px;height:78px;background:#0A0A0A;z-index:8;color:#fff;font-family:var(--e);font-weight:600;font-size:20px;line-height:78px;text-align:center">Apply now &rarr;</div>')
    P.append(f'<div style="position:absolute;left:48px;top:112px;width:{sp.get("hw",620)}px;font-family:var(--s);font-size:{sp.get("hs",100)}px;line-height:{sp.get("hl",96)}px;letter-spacing:-.02em;color:#0A0A0A;z-index:8">{sp["headline"]}</div>')
    P.append(V.t(sp["sub"], 700, sp.get("sub_y", 262), 20, color="#555", w=316, lh=30, tag="sub"))
    by = sp.get("btn_y", 382)
    P.append(f'<div style="position:absolute;left:700px;top:{by}px;width:170px;height:56px;background:#0A0A0A;z-index:8;color:#fff;font-family:var(--e);font-weight:600;font-size:19px;line-height:56px;text-align:center">Apply now &rarr;</div>')
    P.append(V.t(sp["link"], 888, by + 14, 16, tag="lnk"))
    sy, sh = sp["strip_y"], sp.get("strip_h", 168)
    tiles = sp["strip"]; tw = 984 // len(tiles)
    for i, tl in enumerate(tiles):
        x = 48 + i * tw
        if tl[0] == "dither":
            im = V.dither(V.cover(tl[1], tw, sh, fy=tl[3], s=1.6), tl[2], cell=5)
            P.append(V.img(V.uri(im, "PNG"), x, sy, tw, sh, z=5))
        elif tl[0] == "photo":
            P.append(V.img(V.uri(V.cover(tl[1], tw, sh, fy=tl[2], s=1.4)), x, sy, tw, sh, z=5, extra="object-fit:cover;"))
        elif tl[0] == "cover":
            P.append(V.img(V.uri(V.cover(tl[1], tw - 6, sh - 34, fy=.5, s=1.4)), x, sy, tw - 6, sh - 34, z=5, extra="object-fit:cover;"))
            P.append(f'<div style="position:absolute;left:{x}px;top:{sy+sh-34}px;width:{tw-6}px;height:34px;background:#0A0A0A;z-index:5;color:#fff;font-family:var(--e);font-size:14px;line-height:34px;padding-left:10px;white-space:nowrap;overflow:hidden">{tl[2]}</div>')
        elif tl[0] == "block":
            P.append(f'<div style="position:absolute;left:{x}px;top:{sy}px;width:{tw}px;height:{sh}px;background:{tl[1]};z-index:5">'
                     f'<div style="position:absolute;left:14px;top:12px;font-family:var(--e);font-size:13px;color:#0A0A0A">{tl[2]}</div>'
                     f'<div style="position:absolute;left:14px;bottom:34px;font-family:var(--s);font-size:27px;line-height:28px;color:#0A0A0A">{tl[3]}</div>'
                     f'<div style="position:absolute;left:14px;bottom:12px;font-family:var(--e);font-size:12px;color:#0A0A0A">{tl[4]}</div></div>')
        else:
            P.append(f'<div style="position:absolute;left:{x}px;top:{sy}px;width:{tw}px;height:{sh}px;background:#0A0A0A;z-index:5">'
                     f'<div style="position:absolute;left:{tw//2-46}px;top:{sh//2-46}px;width:92px;height:92px">{dd.stamp("burst", PINK)}</div></div>')
    P.append(f'<div style="position:absolute;left:48px;top:{sp["t2_y"]}px;width:560px;font-family:var(--s);font-size:62px;line-height:62px;letter-spacing:-.02em;z-index:8">{sp["title2"]}</div>')
    P.append(V.t(sp["sub2"], 700, sp["t2_y"] + 20, 19, color="#555", w=316, lh=28, tag="s2"))
    cols = sp.get("cols", 4); gap = 8; bw = (984 - gap * (cols - 1)) // cols; bh = sp["bh"]
    for i, b in enumerate(sp["blocks"]):
        x = 48 + (i % cols) * (bw + gap); y = sp["by"] + (i // cols) * (bh + gap)
        ic = {"circle": '<circle cx="20" cy="20" r="20" fill="#0A0A0A"/>',
              "half": '<path d="M0 20a20 20 0 0 1 40 0z" fill="#0A0A0A"/><path d="M0 24a20 20 0 0 0 40 0z" fill="#0A0A0A"/>',
              "dots": '<circle cx="10" cy="10" r="9" fill="#0A0A0A"/><circle cx="30" cy="10" r="9" fill="#0A0A0A"/><circle cx="10" cy="30" r="9" fill="#0A0A0A"/><circle cx="30" cy="30" r="9" fill="#0A0A0A"/>',
              "star": '<g stroke="#0A0A0A" stroke-width="4" stroke-linecap="round"><path d="M20 2v36M2 20h36M7 7l26 26M33 7L7 33"/></g>'}[b["icon"]]
        nm = sp.get("bname", 40); fg = core.text_on(b["col"]); ic = ic.replace("#0A0A0A", fg)
        P.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{bw}px;height:{bh}px;background:{b["col"]};z-index:5">'
                 f'<div style="position:absolute;left:16px;top:14px;font-family:var(--e);font-size:13px;color:{fg}">{b["top"]}</div>'
                 f'<svg style="position:absolute;right:14px;top:12px" width="34" height="34" viewBox="0 0 40 40">{ic}</svg>'
                 f'<div style="position:absolute;left:16px;bottom:{sp.get("bdesc_h",76)+12}px;font-family:var(--s);font-size:{nm}px;line-height:{nm}px;color:{fg}">{b["name"]}</div>'
                 f'<div style="position:absolute;left:16px;bottom:14px;width:{bw-32}px;font-family:var(--e);font-size:14px;line-height:19px;color:{fg}">{b["desc"]}</div></div>')
    band_y = sp["band_y"]
    P.append(f'<div style="position:absolute;left:0;top:{band_y}px;width:{W}px;height:{H-band_y}px;background:#0A0A0A;z-index:4"></div>')
    P.append(f'<div style="position:absolute;left:48px;top:{band_y+18}px;font-family:var(--s);font-size:44px;line-height:44px;color:#fff;z-index:8">{sp["band_title"]}</div>')
    P.append(V.t(sp["band_text"], 620, band_y + 22, 15, color="#bbb", w=396, lh=22, tag="how"))
    for i, (c, n) in enumerate(sp["numerals"]):
        P.append(f'<div style="position:absolute;left:{48+i*(984//len(sp["numerals"]))}px;top:{band_y+68}px;font-family:var(--s);font-size:{sp.get("numsize",100)}px;line-height:{sp.get("numsize",100)}px;color:{c};z-index:8">{n}</div>')
    return sp["name"], V.page("".join(P)), []

# ------------------------------------------------------------------ FORMAT: chat bubbles (ShikshAQ's own signature device)
def chat(sp):
    P = [V.logo_pill(64, 48), series_tab(50), lane_chip("ShikshAQ", LEM, 64, 112)]
    hs = sp["h1_size"]; hl = int(hs * .96)
    P.append(V.t(sp["h1"], 64, 190, hs, font="d", weight=900, lh=hl, w=952, tag="h1", upper=True))
    y = 190 + hl * sp["h1_lines"] + 26
    P.append(f'<div style="position:absolute;left:64px;top:{y}px;width:952px;font-family:var(--s);font-style:italic;font-size:86px;line-height:90px;color:{core.on_cream(LEM, 86, bold=False)};z-index:8">{sp["h2"]}</div>')
    y += 120
    def bubble(text, x, yy, w, col, right=False, who=""):
        tail = f'<div style="position:absolute;{"right" if right else "left"}:-10px;bottom:14px;width:22px;height:22px;background:{col};transform:rotate(45deg);border-right:3px solid #0A0A0A;border-bottom:3px solid #0A0A0A;z-index:-1"></div>'
        return (f'<div style="position:absolute;left:{x}px;top:{yy}px;width:{w}px;background:{col};border:3px solid #0A0A0A;border-radius:26px;box-shadow:6px 6px 0 #0A0A0A;padding:22px 26px;'
                f'font-family:var(--e);font-weight:600;font-size:30px;line-height:40px;color:#0A0A0A;z-index:6">'
                f'<div style="font-family:var(--m);font-weight:700;font-size:13px;letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px;color:#333">{who}</div>{text}</div>')
    P.append(bubble(sp["b1"], 64, y, 600, "#FFFFFF", False, "a parent, asking around"))
    P.append(bubble(sp["b2"], 330, y + 200, 686, LEM, True, "shikshaq"))
    P.append(bubble(sp["b3"], 64, y + 400, 560, "#FFFFFF", False, "the same parent"))
    P.append(V.t(sp["src"], 64, y + 590, 15, color="var(--ink3)", font="m", weight=700, ls=.04, w=952, lh=22, tag="src", upper=False))
    P.append(f'<div style="position:absolute;left:64px;top:1188px;width:952px;height:84px;background:{INK};border-radius:999px;z-index:4"></div>')
    P.append(V.t(URL, 104, 1210, 34, color=LEM, font="m", weight=700, ls=.02, tag="cta", z=8, upper=False))
    return sp["name"], V.page("".join(P)), []

# ------------------------------------------------------------------ the specs
SP = {}
SP["a"] = dict(name="a_loop", photo=WL + "08_dog-drive-bhowanipur.jpg", fy=.4, y0=470,
    lines=["WE THROW PARTIES.", "WE SELL T-SHIRTS.", "THE DOGS EAT."],
    pills=[("Events", SKY, "sparkle", 720, 0, -72, -4), ("Crftd", LEM, "star", 40, 2, 78, -3), ("Welfare", MINT, "heart", 840, 2, 80, 3)],
    card=("Applications open", "AQUATERRA, KOLKATA", "1,400+ students, ages 14 to 19. 540+ drives since 2021."),
    caption="&mdash; zero donations. students earn every rupee, then spend it on drives.",
    dock=[(LEM, "star"), (SKY, "burst"), (MINT, "leaf"), (PINK, "speech")], stack=("RECRUITMENT", "Open now", URL + " &rarr;"))

SP["b"] = dict(name="b_sundarbans", photo=WL + "09_sundarbans-sunset-group.png", fy=.5, fade=480,
    title=[("These people", 500, 78, 76, False), ("ran a health camp", 470, 160, 70, False), ("in the", 500, 236, 70, False), ("Sundarbans.", 490, 296, 108, True)],
    by_xy=(520, 420),
    para="Sunderbans 8.0, December 2025. 120+ health checkups, and 25K worth of medicines and stationery handed over. Everyone on this trip is a student. Applications are open at " + URL + ".",
    wins=[(70, 560, 250, 220, "#FFC700", "120+ CHECKUPS", "tr"), (410, 520, 250, 240, "#3DA9FC", "TRACK 08 : the eighth trip", "br"),
          (740, 560, 270, 240, "#FF4D8C", "25K OF MEDS AND STATIONERY", "tl"), (60, 930, 240, 270, "#7E5BFF", "THIS SEAT : yours", "tr"),
          (700, 900, 280, 280, "#1B8A5A", "OUTRO : sunset, finally", "bl")])

SP["c"] = dict(name="c_tails", photo=WL + "08_dog-drive-bhowanipur.jpg", fy=.6, ph_y=560, lane=("welfare: drives", MINT),
    boxes=[(945, 360, 135, 190), (690, 225, 245, 150), (290, 385, 225, 195), (0, 385, 125, 185)],
    sentence=("Tails and Treats has run 53 times since January 2022. Every round is a bag of ( {0} ) biscuits, a few ( {1} ) volunteers, "
              "and some ( {2} ) dogs who have never once asked anyone's age. ( {3} ) Applications are open."), fs=30, lh=82)

SP["d"] = dict(name="d_teach", bg=WL + "10_teaching-abc-board.jpg", bg_fy=.45, card_photo=WL + "11_art-workshop-table.jpg",
    cap_top="About 70% of our welfare work is a classroom, run by students.", pre="You are not", chip="too young.",
    p1="Teaching internships, worksheets, a Sunday school. You get a class, a marker, and a room of kids who will tell you exactly how your explanation went.",
    p2="Nobody asks if you are old enough. They ask if you showed up.", cap_bot="Applications are open. Bring a marker.")

SP["e"] = dict(name="e_crftd", photo=WL + "12_roots-stall-novus-tee.jpg", fy=.35, ph_y=560, lane=("crftd", LEM),
    boxes=[(380, 20, 190, 190), (440, 200, 150, 110), (130, 340, 180, 180), (440, 600, 180, 180), (780, 90, 170, 150)],
    sentence=("Crftd turns up at a school fest, hangs a blank ( {0} ) T-shirt, and 300 ( {1} ) students walk in. They spray it ( {2} ) until it looks like this. ( {3} ) "
              "Every rupee of profit funds a welfare drive. ( {4} )"), fs=30, lh=82)

SP["f"] = dict(name="f_shikshaq", h1="ASKED THREE COUSINS.<br>STILL NO TUTOR.", h1_lines=2, h1_size=66, h2="Or just search.",
    b1="need a maths tutor near salt lake. asked three cousins and a neighbour.", b2="search for a tutor near you at shikshaq.in. classes iv to xii.",
    b3="...that was it?", src="shikshaq.in. icse, isc, cbse and state board. run by aquaterra students.")

SP["g"] = dict(name="g_diaries", nav=["Home", "Projects", "Teams", "Diaries"], headline="Stories from the ground, written by <i>whoever was there.</i>",
    sub="Essays, field notes and art from members who were actually in the room.",
    link="Join the writers", strip_y=548, strip_h=300,
    strip=[("cover", WL + "blog-people-in-the-mirror.jpg", "People in the Mirror"), ("cover", WL + "blog-dynamics.jpg", "Dynamics"),
           ("cover", WL + "blog-he-barks-i-heal.jpg", "He Barks, I Heal"), ("cover", WL + "blog-voicing-opinions.jpg", "Voicing One's Opinions"),
           ("cover", WL + "blog-letter-to-my-city.jpg", "Letter to My City")],
    t2_y=884, title2="How to get in.", sub2="Three steps. The last one is the one you will screenshot.", cols=3, bh=210, by=968, bname=46, bdesc_h=60,
    blocks=[dict(col="#C9B8FF", top="01", name="Join the group", desc="the writer community group, open to anyone in the AQ community", icon="circle"),
            dict(col="#FF8AD6", top="02", name="Send a draft", desc="through the submission form. any length, any weird angle", icon="dots"),
            dict(col="#FFD84A", top="03", name="See it live", desc="published on our own site, under your name", icon="star")],
    band_y=1204, band_title="Also open.", band_text="Eight departments, one form. Apply at " + URL, numerals=[("#C9B8FF", "01"), ("#FF8AD6", "02"), ("#FFD84A", "03")])

SP["h"] = dict(name="h_doors", nav=["Teams +", "Drives", "Magazine", "Shikshaq"], headline="Eight departments, all run by people <i>still doing homework.</i>",
    sub="Pick the door that sounds like your kind of chaos. You can walk through more than one.", sub_y=300, btn_y=392, link="See the drives",
    strip_y=548, strip_h=128,
    strip=[("dither", V.P_FACES, "#3DA9FC", .4), ("block", MINT, "Welfare", "Tails and Treats", "edition 53"), ("glyph",),
           ("dither", WL + "12_roots-stall-novus-tee.jpg", "#FF4D2E", .4), ("block", MINT, "Welfare", "Sharbat Seva", "edition 33"),
           ("dither", WL + "09_sundarbans-sunset-group.png", "#7E5BFF", .5)],
    t2_y=708, title2="Eight doors, one form.", sub2="Every team is run by students. Nobody gets a script.", cols=4, bh=206, by=786, bname=34, bdesc_h=58,
    blocks=[dict(col=SKY, top="01 · events", name="Events", desc="Fests, vendors, sponsors, a dance floor built from nothing.", icon="circle"),
            dict(col=MINT, top="02 · welfare", name="Welfare", desc="Dogs, food, plantations, classrooms and trips.", icon="half"),
            dict(col=TOM, top="03 · crftd", name="Crftd", desc="Streetwear. Profit funds a welfare drive.", icon="star"),
            dict(col=LEM, top="04 · shikshaq", name="ShikshAQ", desc="A tutor search for Kolkata, run by students.", icon="dots"),
            dict(col=GRAPE, top="05 · social media", name="Social", desc="Reels, design, the account you scroll.", icon="star"),
            dict(col=GRAPE, top="06 · blogs", name="Blogs", desc="Written and published by students.", icon="circle"),
            dict(col=PINK, top="07 · collabs", name="Collabs", desc="Schools, NGOs, a foundation or two.", icon="half"),
            dict(col=TEAL, top="08 · hr", name="HR", desc="Onboarding, interviews, certificates.", icon="dots")],
    band_y=1224, band_title="Come in.", band_text="Apply and you are in the community. Join a team when you find yours.", numsize=80,
    numerals=[(SKY, "Events"), (MINT, "Welfare"), (TOM, "Crftd"), (LEM, "ShikshAQ")])

async def main():
    os.makedirs(OUT, exist_ok=True)
    jobs = [("a", lambda: hero(SP["a"]), 1350), ("b", lambda: cast(SP["b"]), 1350), ("c", lambda: blank(SP["c"]), 1350), ("d", lambda: note(SP["d"]), 1350),
            ("e", lambda: blank(SP["e"]), 1350), ("f", lambda: chat(SP["f"]), 1350), ("g", lambda: site(SP["g"]), 1350), ("h", lambda: site(SP["h"]), 1350),
            ("as", lambda: hero(SP["a"], True), 1920), ("ds", lambda: note(SP["d"], True), 1920)]
    async with B.session():
        for key, mk, hh in jobs:
            if len(sys.argv) > 1 and key not in sys.argv[1:]: continue
            V.H = hh
            res = mk()
            if asyncio.iscoroutine(res): res = await res
            name, html, els = res
            await B.render(html, f"{OUT}/{name}.png", W, hh, elements=els or None, page_bg="var(--bg)")
            print("rendered", name)
        V.H = 1350

if __name__ == "__main__":
    asyncio.run(main())
