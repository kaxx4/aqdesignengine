import os
# AQ ENGINE — single entry point. Everything is a DIRECT OUTCOME of encoded rules here.
# No hand-tuning per piece. You give it (intent, archetype, content); it produces + self-corrects
# using ONLY encoded rules. If a piece is wrong, we fix the RULE here, never the individual output.
import importlib.util, asyncio, math, random
def _load(n):
    s=importlib.util.spec_from_file_location(n,os.path.join(os.path.dirname(os.path.abspath(__file__)),f"{n}.py")); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core=_load("core"); B=_load("build"); dd=_load("doodles"); audit=_load("audit"); T=_load("tex"); rm=_load("ref_metrics"); pv=_load("preview")
W,H=core.SIZES["feed"]; M=64; UNIT=8
INK_ON=getattr(core,"INK_ON",set())
def snap(v): return round(v/UNIT)*UNIT
def cs(n): return B.colspan(W,n)

# ═══════════════ ENCODED RULES (the engine's knowledge, not the LLM's) ═══════════════

ARCHETYPE_PROFILES = {
  # per-archetype gate calibration — different geometries have different natural density
  "number_hero": dict(fill_min=0.34, max_density=3),
  "radial_orbit": dict(fill_min=0.26, max_density=4),
  "giant_type": dict(fill_min=0.24, max_density=2, exempt_flat=True),   # radial is legitimately airier (center+ring)
  "stacked_zones": dict(fill_min=0.30, max_density=2),
}
RULES = {
  # measured reference targets
  "targets": dict(contrast=0.26, ink=0.11, sat=0.31, hisat=0.31, dom_cov=0.46),
  # composition gates
  "fill_min":0.34, "fill_max":0.82, "contrast_min":0.22, "quad_min":0.12,
  # craft constants
  "shadow":"6px 6px 0 var(--ink)", "outline":"4px solid var(--ink)", "radius":"14px",
  # accent rotation (functional: punctuation only)
  "accents":core.ACCENTS,
  # halftone: photos only (flat on solids) — enforced in tex.py
  # type scale floors by role
  "fs":{"title":140,"number":300,"sub":34,"body":24,"meta":14,"chip":17},
  # snarky chip bank (voice)
  "snark":["no fees, obviously","cv? never met her","run by literal teenagers",
           "show up. that's the ask","impact as a side effect","1,200 of us, still unhinged",
           "peer pressure but wholesome","not a boring ngo, promise"],
}

# ── ENCODED HELPERS (every visual element built from rules, identical everywhere) ──
def R_chip(txt,accent,x,y,rot=0):
    fg="#0A0A0A" if accent in INK_ON else "#fff"
    return (f'<div class="measure" data-tag="chip" style="position:absolute;top:{snap(y)}px;left:{snap(x)}px;'
            f'background:{accent};color:{fg};font-family:var(--e);font-weight:600;font-size:{RULES["fs"]["chip"]}px;'
            f'padding:10px 16px;border-radius:999px;border:3px solid var(--ink);box-shadow:4px 4px 0 var(--ink);'
            f'transform:rotate({rot}deg);z-index:11;line-height:1.15">{txt}</div>')
def R_doodle(kind,x,y,size,accent,rot=0,style="rough"):
    fn=getattr(dd,kind,dd.star)
    try: inner=fn(fill=accent,rot=rot,style=style)
    except TypeError:
        try: inner=fn(fill=accent,rot=rot)
        except TypeError: inner=fn(fill=accent)
    return f'<div class="measure" data-tag="doodle" style="position:absolute;top:{snap(y)}px;left:{snap(x)}px;width:{size}px;height:{size}px;z-index:6">{inner}</div>'
def R_logo(): return f'<img src="{core.LOGO}" style="position:absolute;top:{snap(52)}px;left:{M}px;height:28px;z-index:20">'
def R_meta(txt): return f'<span style="position:absolute;top:{snap(58)}px;right:{M}px;font-family:var(--m);font-weight:700;font-size:{RULES["fs"]["meta"]}px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink);z-index:20">{txt}</span>'
def R_footer(txt): return f'<span style="position:absolute;bottom:{snap(52)}px;left:{M}px;font-family:var(--m);font-weight:700;font-size:{RULES["fs"]["meta"]}px;color:var(--ink3);z-index:20">{txt}</span>'

# ── ENCODED ARCHETYPE GENERATORS (structure = rule, not improvisation) ──
def archetype_number_hero(content, accent, density=0):
    """density 0..3 — engine escalates this automatically when preview flags 'sparse'.
    Higher density = bigger number, wider accent block, added corner mass. Encoded, not hand-tuned.
    field: "cream" (default, dominant field = brand bg) or "accent" (dominant field = the accent
    itself, textured with halftone_gradient — for pieces whose reference signature is a single
    saturated field, e.g. dom_cov>.45 + mean_sat>.4. Same craft layer either way, just the base swaps."""
    field = content.get("field","cream")
    fg="#0A0A0A" if accent in INK_ON else "#fff"
    # rule: every supporting color (chips/masses/corner/band) is relative to the CHOSEN hero accent,
    # not a fixed absolute index. Session 6 finding: the hero rotated per generation but the whole
    # supporting palette was frozen at fixed literals, so only one color ever changed — the piece
    # still read as "the same design" underneath. Rotating everything together is a real palette shift.
    ai = RULES["accents"].index(accent)
    A = lambda off: RULES["accents"][(ai+off)%7]
    num_fs = RULES["fs"]["number"] + density*40           # rule: scale number up per density step
    block_w = 5 + min(density,1)                           # rule: widen accent block
    label_fs = 88 + density*10
    if field=="accent":
        base_css = T.halftone_gradient(accent)             # textured saturated field, not flat/banned-gloss
        onfield = fg                                        # text sitting directly on the field
        block_bg = "var(--ink)"                             # hero block inverts to ink so number still pops
        num_fg = "#fff"
        logo = R_logo()  # bare, matching the giant_type dark-base precedent (DECISIONS.md: never pill-wrap)
        # rule: meta sits inside the top-right corner block's footprint once density>=2 adds it —
        # contrast against what's actually BEHIND it (the corner accent), not the field default.
        meta_bg = A(2) if density>=2 else accent
        meta_fg = "#0A0A0A" if meta_bg in INK_ON else "#fff"
        meta = f'<span style="position:absolute;top:{snap(58)}px;right:{M}px;font-family:var(--m);font-weight:700;font-size:{RULES["fs"]["meta"]}px;letter-spacing:.1em;text-transform:uppercase;color:{meta_fg};z-index:20">{content["meta"]}</span>'
    else:
        base_css = "background:var(--bg);"
        onfield = "var(--ink)"
        block_bg = accent
        num_fg = fg
        logo = R_logo(); meta = R_meta(content["meta"])
    # rule: at density>=1 add a full-width footer band (mass in bottom quadrants)
    band = f'<div style="position:absolute;bottom:0;left:0;right:0;height:{140+density*40}px;background:{A(1)};border-top:5px solid var(--ink);z-index:1"></div>' if density>=1 else ''
    band_txt = f'<div style="position:absolute;bottom:{snap(56)}px;left:{M}px;width:{cs(6)}px;font-family:var(--d);font-weight:900;font-size:40px;text-transform:uppercase;color:#fff;z-index:11;line-height:.9">{content.get("band","every number is a person.")}</div>' if density>=1 else ''
    # rule: at density>=2 add a second accent block top-right (kills dead TR)
    corner = f'<div style="position:absolute;top:0;right:0;width:320px;height:240px;background:{A(2)};border-radius:0 0 0 50%;border-bottom:5px solid var(--ink);border-left:5px solid var(--ink);z-index:1"></div>' if density>=2 else ''
    return "".join([
      f'<div style="position:absolute;inset:0;{base_css}"></div>', corner,
      logo, meta,
      f'<div style="position:absolute;top:{snap(200)}px;left:{M}px;font-family:var(--d);font-weight:900;font-size:48px;text-transform:uppercase;color:{onfield};z-index:6">{content["kicker"]}</div>',
      f'<div style="position:absolute;top:{snap(300)}px;left:{M-8}px;width:{cs(block_w)}px;height:{340+density*20}px;background:{block_bg};box-shadow:12px 12px 0 var(--ink);z-index:3"></div>',
      f'<div class="measure" data-tag="number" style="position:absolute;top:{snap(300)}px;left:{M+20}px;font-family:var(--d);font-weight:900;font-size:{num_fs}px;line-height:.75;letter-spacing:-.06em;color:{num_fg};text-shadow:8px 8px 0 var(--ink);z-index:5">{content["number"]}</div>',
      f'<div class="measure" data-tag="label" style="position:absolute;top:{snap(300+(340+density*20)+30)}px;left:{M}px;width:{cs(6)}px;font-family:var(--d);font-weight:900;font-size:{label_fs}px;line-height:.85;text-transform:uppercase;color:{onfield};z-index:6">{content["label"]}</div>',
      # chips anchored as a connected row just under the label (no floating island).
      # rule: the whole chips row LIFTS when density>=1 so the always-on body copy clears it —
      # fixed y-positions collided with the body once the band pushed content up (caught 2026-07-21).
      R_chip(content["chips"][0], A(4), M, 900 if density>=1 else 940, -2),
      R_chip(content["chips"][1], A(5), M+330, 904 if density>=1 else 944, 3),
      # accent tick connecting label to chips (kills the disconnected feel)
      f'<div style="position:absolute;top:{snap(880 if density>=1 else 920)}px;left:{M}px;width:70px;height:8px;background:{A(3)};z-index:5"></div>',
      # rule: doodles come in a SIZE PAIR (small + large, §9 "mix 60px and 160px") — a lone
      # mid-size doodle reads as an afterthought; contrast in scale is the eye-candy signal.
      R_doodle("star", 860, 290, 128+density*10, A(5), -12),
      R_doodle("sparkle", 952, 176, 58, A(3), 15),
      # rule: body copy ALWAYS renders — dropping it at density>=1 left a dead cream strip
      # between the chips row and the footer band (caught by eye, 2026-07-21). It sits on the
      # cream above the band, shifting up as the band grows taller.
      f'<div class="measure" data-tag="body" style="position:absolute;top:{snap(min(1090, H-(140+density*40)-160) if density>=1 else 1090)}px;left:{M}px;width:{cs(5)}px;font-family:var(--e);font-weight:600;font-size:{RULES["fs"]["body"]}px;line-height:1.4;color:{"var(--ink2)" if field=="cream" else onfield};z-index:11">{content["body"]}</div>',
      band, band_txt,
      R_footer(content["footer"]) if (density<1 and field=="cream") else f'<span style="position:absolute;bottom:16px;left:{M}px;font-family:var(--m);font-weight:700;font-size:12px;color:{"rgba(255,255,255,.7)" if density>=1 else onfield};z-index:12">{content["footer"]}</span>',
    ])

def archetype_radial_orbit(content, accent, density=0):
    """Radial: focal center + orbit stickers. density escalates orbit count/size + focal size."""
    cx,cy=W//2,int(H*0.44)
    focal_d=360+density*30
    ai = RULES["accents"].index(accent)
    A = lambda off: RULES["accents"][(ai+off)%7]
    fg="#0A0A0A" if A(2) in INK_ON else "#fff"
    # rule: font-size auto-fits the focal number to the circle by character count (the roadsign bug,
    # applied here) -- a fixed size only worked for 3-char numbers like "534"; "1.2K" (4 chars) spilled
    # past the circle edge. Scale down for longer numbers, never exceed the density-scaled max.
    num_len = max(len(str(content["number"])), 1)
    num_fs = min(170+density*16, int(focal_d*0.82/num_len*1.6))
    focal=(f'<div style="position:absolute;top:{cy-focal_d//2}px;left:{cx-focal_d//2}px;width:{focal_d}px;height:{focal_d}px;'
           f'border-radius:50%;background:var(--ink);border:5px solid var(--ink);box-shadow:0 0 0 14px var(--bg),0 0 0 18px var(--ink);'
           f'z-index:8;display:flex;flex-direction:column;align-items:center;justify-content:center">'
           f'<span style="font-family:var(--m);font-weight:700;font-size:15px;letter-spacing:.12em;text-transform:uppercase;color:{A(2)};margin-bottom:4px">{content["kicker"]}</span>'
           f'<span style="font-family:var(--d);font-weight:900;font-size:{num_fs}px;line-height:.78;color:{A(2)}">{content["number"]}</span>'
           f'<span style="font-family:var(--d);font-weight:900;font-size:30px;text-transform:uppercase;color:#fff">{content["label"]}</span></div>')
    items=content["orbit"]; n=len(items); orb=""; r=340+density*10
    for i,(lab,ai) in enumerate(items):
        ang=(i/n)*2*math.pi - math.pi/2
        x=int(cx+r*math.cos(ang)); y=int(cy+r*math.sin(ang))
        col=RULES["accents"][ai]; fgc="#0A0A0A" if col in INK_ON else "#fff"
        # rule: orbit stickers alternate scale (0.86x / 1.14x) — identical diameters are the
        # literal "bingo-card uniformity" failure preview.critique flags; scale rhythm is encoded,
        # not left to chance.
        d=int((120+density*16) * (1.14 if i%2==0 else 0.86))
        orb+=(f'<svg style="position:absolute;inset:0;width:100%;height:100%;z-index:2;pointer-events:none" xmlns="http://www.w3.org/2000/svg"><line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="#0A0A0A" stroke-width="2.5" stroke-dasharray="3 10"/></svg>'
               f'<div style="position:absolute;top:{y-d//2}px;left:{x-d//2}px;width:{d}px;height:{d}px;border-radius:50%;background:{col};border:4px solid var(--ink);box-shadow:4px 4px 0 var(--ink);z-index:6;display:flex;align-items:center;justify-content:center"><span style="font-family:var(--d);font-weight:900;font-size:22px;text-transform:uppercase;color:{fgc}">{lab}</span></div>')
    # rule: corner mass must stay fully on-canvas (clamped left>=0) — a half-bled, unlabeled, orbit-
    # disconnected circle at the frame edge reads as stray debris, not an intentional design bleed
    # (found generating community.png: it clipped off the left edge with no orbit line/label).
    corner = f'<div style="position:absolute;bottom:{snap(200)}px;left:0px;width:220px;height:220px;border-radius:50%;background:{A(1)};border:5px solid var(--ink);z-index:1"></div>' if density>=2 else ''
    return "".join([
      f'<div style="position:absolute;inset:0;background:var(--bg)"></div>', corner,
      R_logo(), R_meta(content["meta"]),
      f'<div style="position:absolute;top:{snap(56)}px;left:0;right:0;text-align:center;z-index:9"><span style="font-family:var(--s);font-style:italic;font-size:56px;color:var(--ink)">{content["top"]}</span></div>',
      orb, focal,
      R_chip(content["chips"][0], A(3), 90, 200, -4),
      R_chip(content["chips"][1], A(4), 720, 210, 5),
      f'<div class="measure" data-tag="body" style="position:absolute;bottom:{snap(120)}px;left:{M}px;right:{M}px;text-align:center;font-family:var(--d);font-weight:900;font-size:52px;text-transform:uppercase;letter-spacing:-.03em;color:var(--ink);z-index:9;line-height:.95">{content["big"]}</div>',
      f'<span style="position:absolute;bottom:{snap(56)}px;left:0;right:0;text-align:center;font-family:var(--m);font-weight:700;font-size:14px;color:var(--ink3);z-index:20">{content["footer"]}</span>',
    ])

def archetype_giant_type(content, accent, density=0):
    """Giant word fills the frame. FIX: word spans wider + right-side accent mass kills dead ink.
    field: "ink" (default, dark dominant base — the shipped signature) or "cream" (light dominant
    base — for references like DRÖM: giant word as the ONLY major ink mass, scattered flat cut-paper
    objects at low overall saturation, dom_cov driven by the LIGHT field not a dark one). Same
    scattered-mass craft layer either way; only the base + text-on-base colors swap."""
    field = content.get("field","ink")
    ai = RULES["accents"].index(accent)
    A = lambda off: RULES["accents"][(ai+off)%7]
    onfield = "var(--ink)" if field=="cream" else "#fff"
    body_col = "var(--ink2)" if field=="cream" else "rgba(255,255,255,.9)"
    base_bg = "var(--bg)" if field=="cream" else "var(--ink)"
    logo_el = (f'<img src="{core.LOGO}" style="position:absolute;top:{snap(52)}px;left:{M}px;height:26px;z-index:20">' if field=="cream"
               else f'<img src="{core.LOGO}" style="position:absolute;top:{snap(52)}px;left:{M}px;height:26px;z-index:20;filter:drop-shadow(0 2px 4px rgba(0,0,0,.6))">')
    tags=""
    tcols=[A(2),A(3),A(5)]
    for i,t in enumerate(content.get("tags",[])[:3]):
        fg="#0A0A0A" if tcols[i] in INK_ON else "#fff"
        tags+=f'<span style="font-family:var(--m);font-weight:700;font-size:16px;letter-spacing:.1em;text-transform:uppercase;color:{fg};background:{tcols[i]};padding:9px 15px;border-radius:6px;margin-right:12px">{t}</span>'
    # RIGHT-SIDE ACCENT MASS: big shape filling the dead ink beside/below the narrow serif word
    wl=len(content["word"])
    # rule: on a cream field the scattered masses are OBJECTS on a light ground (like DRÖM's toy shapes)
    # not a saturated flood — shrink + soften them so mean_sat/hi_sat_frac don't run hot vs a light-
    # dominant reference. Ink base keeps them full-size/full-opacity (its own signature is bold+flat).
    mass_scale = 0.75 if field=="cream" else 1.0
    mass_alpha = "CC" if field=="cream" else ""  # ~80% opacity, blends toward the cream field
    # rule: leftmass previously ignored `density` entirely while rightmass/lowmass both scale with
    # it — giant_type's only TL-quadrant mass had no headroom to help clear a stuck flat_dominant/
    # sparse TL reading once density escalated (session: teachers_day, fill=0.28 stuck at the old
    # max_density=1 cap with TL/TR both <0.17). Scale it the same way its siblings do.
    leftmass=(f'<div style="position:absolute;top:{snap(120)}px;left:{snap(60)}px;width:{int((200+density*40)*mass_scale)}px;height:{int((170+density*30)*mass_scale)}px;border-radius:16px;transform:rotate(-6deg);background:{A(3)}{mass_alpha};border:5px solid var(--ink);z-index:1"></div>')
    rightmass=(f'<div style="position:absolute;top:{snap(360)}px;right:-70px;width:{int((300+density*40)*mass_scale)}px;height:{int((300+density*40)*mass_scale)}px;'
               f'border-radius:50%;background:{A(2)}{mass_alpha};border:5px solid var(--ink);z-index:1"></div>')
    lowmass=(f'<div style="position:absolute;bottom:{snap(300)}px;right:{M}px;width:{int((220+density*30)*mass_scale)}px;height:{int((220+density*30)*mass_scale)}px;'
             f'border-radius:40% 60% 55% 45%;background:{A(4)}{mass_alpha};border:5px solid var(--ink);z-index:1"></div>') if density>=1 else ''
    # rule: the word div's own bounding box spans the full grid width (cs(6), ~952px) for
    # wrapping purposes even though short words like "teachers" only render glyphs to ~65% of
    # it — so a filler shape placed beside the word at word-height would sit INSIDE that
    # (invisible) box and risk a collision flag, while the real visual gap it needs to fill is
    # TR-quadrant space the existing masses don't reach. midmass sits in the one window clear of
    # both the word box (ends ~y430) and the tags row (starts y640+): a real, needed 3rd escalation
    # tier for pieces where density=1 still leaves TR sparse/flat_dominant (session: teachers_day).
    midmass=(f'<div style="position:absolute;top:{snap(470)}px;right:{snap(90)}px;width:{int(260*mass_scale)}px;height:{int(150*mass_scale)}px;'
             f'border-radius:20px;transform:rotate(4deg);background:{A(6)}{mass_alpha};border:5px solid var(--ink);z-index:1"></div>') if density>=2 else ''
    band = f'<div style="position:absolute;bottom:0;left:0;right:0;height:{160+density*30}px;background:{accent};border-top:5px solid var(--ink);z-index:2"></div>' if density>=1 else ''
    bandfg="#0A0A0A" if accent in INK_ON else "#fff"
    bandtxt = f'<div style="position:absolute;bottom:{snap(60)}px;left:{M}px;font-family:var(--d);font-weight:900;font-size:48px;text-transform:uppercase;color:{bandfg};z-index:11;line-height:.9">{content.get("band","")}</div>' if density>=1 else ''
    return "".join([
      f'<div style="position:absolute;inset:0;background:{base_bg}"></div>',
      # field fragmentation: a large tilted accent panel breaks the flat field (kills flat_dominant)
      f'<div style="position:absolute;top:40px;left:-80px;width:420px;height:420px;border-radius:50%;border:3px solid {A(5)}44;z-index:0"></div>',
      f'<div style="position:absolute;bottom:120px;right:-60px;width:360px;height:360px;border-radius:50%;border:3px solid {A(2)}44;z-index:0"></div>',
      leftmass, rightmass, lowmass, midmass,
      # rule: giant_type carries the same size-pair doodle vocabulary as the other archetypes
      # (§9) — it previously had ZERO doodles, reading flatter than every reference. Small
      # sparkle top-right (below meta, above rightmass) + large star near the lower-left edge
      # of the word column; both in measured free zones for all density levels.
      R_doodle("sparkle", 872, 150, 60, A(4), 12),
      R_doodle("star", 688, 112, 120, A(5), -14),
      logo_el,
      f'<span style="position:absolute;top:{snap(58)}px;right:{M}px;font-family:var(--m);font-weight:700;font-size:14px;letter-spacing:.12em;text-transform:uppercase;color:{onfield};z-index:20">{content["meta"]}</span>',
      (lambda wl: f'<div class="measure" data-tag="title" style="position:absolute;top:{snap(240)}px;left:{M}px;width:{cs(6)}px;font-family:var(--s);font-style:italic;font-size:{min(300+density*24, int(cs(6)/max(wl,1)*1.75))}px;line-height:.82;color:{onfield};z-index:6">{content["word"]}<span style="color:{A(2)}">.</span></div>')(len(content["word"])),
      f'<div style="position:absolute;top:{snap(640+density*24)}px;left:{M}px;z-index:7">{tags}</div>',
      f'<div class="measure" data-tag="body" style="position:absolute;top:{snap(760+density*24)}px;left:{M}px;width:{cs(4)}px;font-family:var(--e);font-weight:600;font-size:{RULES["fs"]["body"]+2}px;line-height:1.45;color:{body_col};z-index:6">{content["body"]}</div>',
      f'<div class="measure" data-tag="big" style="position:absolute;bottom:{snap(220 if density>=1 else 90)}px;left:{M}px;font-family:var(--d);font-weight:900;font-size:52px;text-transform:uppercase;letter-spacing:-.03em;color:{A(2) if field=="ink" else "var(--ink)"};z-index:11">{content["big"]}</div>',
      band, bandtxt,
      f'<span style="position:absolute;bottom:{snap(16) if density>=1 else snap(52)}px;right:{M}px;font-family:var(--m);font-weight:700;font-size:14px;color:{bandfg if density>=1 else onfield};z-index:20">{content["footer"]}</span>',
    ])

def archetype_stacked_zones(content, accent, density=0):
    """Horizontal pill-row list, top-down reading (matches EVENTS-CALENDAR-style references: a
    rounded title card, a meta row, then a stacked list of colored index+label pill rows in an
    ink container). density 0..2 — escalates row height + row count via a bottom filler row + a
    footer-band, never by shrinking rows below their legible floor."""
    rows = content["rows"]  # list of (tag, label, accent_idx)
    n = len(rows)
    row_h = 92 + density*10
    gap = 16
    title_h = 260 + density*20
    header_top = snap(180)
    list_top = header_top + title_h + snap(90)
    list_h = n*row_h + (n-1)*gap + 48
    rows_html = ""
    for i,(tag,label,ai) in enumerate(rows):
        y = list_top + 24 + i*(row_h+gap)
        tagcol = RULES["accents"][(ai+3)%7]
        col = RULES["accents"][ai]
        fgc = "#0A0A0A" if col in INK_ON else "#fff"
        tagfg = "#0A0A0A" if tagcol in INK_ON else "#fff"
        rows_html += (
          f'<div style="position:absolute;top:{y}px;left:{M+20}px;width:{row_h-16}px;height:{row_h-16}px;background:{tagcol};'
          f'border-radius:14px;border:4px solid var(--ink);display:flex;align-items:center;justify-content:center;'
          f'font-family:var(--d);font-weight:900;font-size:26px;color:{tagfg};z-index:6">{tag}</div>'
          f'<div class="measure" data-tag="row" style="position:absolute;top:{y}px;left:{M+20+row_h+8}px;width:{cs(6)-row_h-8}px;height:{row_h-16}px;background:{col};'
          f'border-radius:999px;border:4px solid var(--ink);display:flex;align-items:center;padding:0 28px;'
          f'font-family:var(--d);font-weight:900;font-size:24px;text-transform:uppercase;color:{fgc};z-index:6;line-height:1.1">{label}</div>'
        )
    # Fill the leftover canvas below the list with the band, sized to whatever space actually
    # remains (not gated behind `density>=1`) — a fixed-height band left the ink list floating
    # over a dead cream gap whenever row count x row_h didn't reach the canvas floor on its own
    # (preview.critique's 2x2 quadrant check is too coarse to catch a gap confined to the lower
    # slice of the bottom half). See brain/DECISIONS.md, bug catalog "dead half the reference
    # fills".
    # Cap the band's height and give it a color DERIVED from (not equal to) the hero card's
    # accent: an uncapped same-hued band just swaps one flaw (dead cream gap) for another
    # (two huge fields of the identical hue flooding the piece, breaking the "accents are
    # punctuation, ~30% max, never a flood" rule) — neither is caught by preview.critique's
    # fill%/quadrant numbers, only by looking. See brain/DECISIONS.md, bug catalog.
    MAX_BAND = 420
    band_top = list_top + list_h
    band_avail = H - band_top
    band_h = min(band_avail, MAX_BAND)
    show_band = band_h >= 110
    band_accent = RULES["accents"][(RULES["accents"].index(accent) + 2) % 7]
    band = f'<div style="position:absolute;bottom:0;left:0;right:0;height:{band_h}px;background:{band_accent};border-top:5px solid var(--ink);z-index:1"></div>' if show_band else ''
    bandfg = "#0A0A0A" if band_accent in INK_ON else "#fff"
    bandtxt = f'<div style="position:absolute;bottom:{snap(58)}px;left:{M}px;font-family:var(--d);font-weight:900;font-size:42px;text-transform:uppercase;color:{bandfg};z-index:11;line-height:.9">{content.get("band","")}</div>' if show_band and content.get("band") else ''
    return "".join([
      f'<div style="position:absolute;inset:0;background:var(--bg)"></div>',
      f'<div style="position:absolute;top:{list_top}px;left:{M}px;width:{cs(6)+row_h+28}px;height:{list_h}px;background:var(--ink);border-radius:20px;z-index:2"></div>',
      R_logo(), R_meta(content["meta"]),
      f'<div style="position:absolute;top:{header_top}px;left:{M}px;width:{cs(6)}px;min-height:{title_h}px;background:{accent};border-radius:24px;border:5px solid var(--ink);box-shadow:8px 8px 0 var(--ink);z-index:3;display:flex;align-items:center;padding:0 32px">'
      f'<span class="measure" data-tag="title" style="font-family:var(--d);font-weight:900;font-size:64px;line-height:.95;text-transform:uppercase;color:{"#0A0A0A" if accent in INK_ON else "#fff"}">{content["title"]}</span></div>',
      R_doodle("star", cs(6)-40, header_top-30, 70, RULES["accents"][(RULES["accents"].index(accent)+5)%7], -10),
      R_chip(content.get("kicker_left","pick any."), RULES["accents"][(RULES["accents"].index(accent)+3)%7], M, list_top-60, -3),
      R_chip(content.get("kicker_right","ongoing"), RULES["accents"][(RULES["accents"].index(accent)+4)%7], M+cs(6)-100, list_top-56, 3),
      rows_html,
      band, bandtxt,
      R_footer(content["footer"]) if not show_band else f'<span style="position:absolute;bottom:16px;left:{M}px;font-family:var(--m);font-weight:700;font-size:12px;color:rgba(255,255,255,.7);z-index:12">{content["footer"]}</span>',
    ])

ARCHETYPES={"number_hero":archetype_number_hero,"radial_orbit":archetype_radial_orbit,"giant_type":archetype_giant_type,"stacked_zones":archetype_stacked_zones}

# ── ENCODED AUTO-FIX RULES (engine corrects itself from rules, not LLM hand-editing) ──
def rule_fixes(critique, content, accent):
    """Given a preview critique, return RULE-BASED parameter adjustments. Encoded, deterministic."""
    fixes=[]
    for code,msg in critique["issues"]:
        if code=="sparse": fixes.append("scale_up")      # enlarge hero/number per rule
        if code=="crammed": fixes.append("scale_down")
        if code=="dead_quadrant": fixes.append("redistribute")
        if code=="flat": fixes.append("add_ink")
        if code=="uniform": fixes.append("vary_scale")
    return fixes

# ── THE PIPELINE (single call; every stage encoded) ──
async def generate(name, archetype, content, accent_idx=0, max_iters=3):
    accent=RULES["accents"][accent_idx]
    report={"name":name,"archetype":archetype,"iters":[]}
    prof=ARCHETYPE_PROFILES.get(archetype, dict(fill_min=RULES["fill_min"], max_density=3))
    density=0
    for it in range(prof["max_density"]+1):
        inner=ARCHETYPES[archetype](content, accent, density)
        # rule: grain is ALWAYS on for Workflow A output — the 0.06-opacity turbulence overlay is
        # the cheapest encoded depth cue; matte-flat fields were the recurring "flat" eye-catch.
        html=B.page(W,H,"var(--bg)",inner,grain=True)
        # STAGE 1: collision audit (encoded)
        # STAGE 2: render
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            b=await p.chromium.launch(); pg=await b.new_page(viewport={"width":W,"height":H},device_scale_factor=2)
            await pg.set_content(html,wait_until="load"); await pg.wait_for_timeout(1200)
            await pg.locator(".p").screenshot(path=f"out/{name}.png"); await b.close()
        # STAGE 3: numeric preview (encoded gate)
        crit=pv.critique(f"out/{name}.png")
        # rule: exempt_flat is a per-archetype flag meant for ONE specific signature (giant_type's
        # dark ink base), not the whole archetype regardless of content. Session 5 finding: giant_type
        # had the worst dom_cov overshoot of all 4 archetypes (+.238) even after wiring flat_dominant
        # into the gate, because this exemption blanket-applied to field=="cream" pieces too, which
        # have no reason to be flat-exempt (only the dark "ink" field is an intentional signature).
        is_exempt_field = content.get("field","ink") != "cream"
        if (prof.get("exempt_flat") and is_exempt_field) or content.get("field")=="accent":
            crit["issues"]=[(c,m) for c,m in crit["issues"] if c!="flat_dominant"]
        # apply archetype-specific fill floor (encoded per-archetype gate)
        # rule: flat_dominant must be part of the PASS/FAIL gate, not just available as an escalation
        # trigger — otherwise a piece that already clears fill/contrast/quads exits at iteration 0
        # and never gets a chance to escalate, no matter how dominant its field is (session 5 finding:
        # this is why the earlier flat_dominant threshold fix had zero measured effect on 44/44 samples).
        no_flat_dominant = not any(c=="flat_dominant" for c,_ in crit["issues"])
        arch_ok = (crit["fill"]>=prof["fill_min"] and crit["contrast"]>=RULES["contrast_min"]
                   and all(v>=RULES["quad_min"] for v in crit["quads"].values()) and crit["fill"]<=RULES["fill_max"]
                   and no_flat_dominant)
        arch_ok=bool(arch_ok)
        crit["ok"]=arch_ok
        report["iters"].append({"iter":it,"ok":arch_ok,"fill":float(crit["fill"]),"issues":[c for c,_ in crit["issues"]]})
        if arch_ok:
            report["final_ok"]=True; report["png"]=f"out/{name}.png"; break
        # STAGE 4: ENCODED rule-based fix — escalate density when sparse/dead-quadrant/flat_dominant.
        # No hand-editing. (session 5 finding: flat_dominant was computed but never wired to any
        # corrective action — a 44-sample batch showed dom_cov running +0.13 to +0.24 over target
        # across every archetype because the static per-archetype "field fragmentation" panels alone
        # weren't enough. Density escalation adds MORE mass — corner blocks, footer bands, wider
        # accent blocks — which is exactly what breaks up an over-dominant field, same mechanism
        # already used for sparse/dead_quadrant.)
        codes=[c for c,_ in crit["issues"]]
        if ("sparse" in codes or "dead_quadrant" in codes or "flat_dominant" in codes) and density<prof["max_density"]:
            density=min(density+1,prof["max_density"])
        elif "crammed" in codes: density=max(density-1,0)
        else: break
    else:
        report["final_ok"]=False; report["png"]=f"out/{name}.png"
    # STAGE 5: reference-metric drift ADVISORY (targets from RULES["targets"], §7c) — logged on
    # EVERY run so dom_cov/sat/contrast drift is visible per-generation, not only in batch audits.
    # Advisory only: vdr under-reads on flat-vector output (known metric limitation), so this
    # never gates — it informs the looking gate.
    try:
        rmx=rm.analyze(report["png"])
        t=RULES["targets"]
        report["ref_metrics"]={k:round(float(rmx[k]),3) for k in ("dom_cov","mean_sat","contrast","ink","vdr")}
        report["ref_drift"]={k:round(float(rmx[k])-t[tk],3) for k,tk in
                             (("dom_cov","dom_cov"),("mean_sat","sat"),("contrast","contrast"),("ink","ink"))}
    except Exception as e:
        report["ref_metrics_error"]=str(e)
    # STAGE 6: LOOKING GATE is executed by the operator (LLM VIEWS png) — hard requirement, logged
    report["looking_required"]=True
    return report

if __name__=="__main__":
    async def demo():
        content=dict(meta="health · free camps", kicker="we checked",
            number="1.6k", label='people, free.<br>no <span style="font-family:var(--s);font-style:italic;text-transform:none;color:var(--tomato)">questions.</span>',
            chips=["blood pressure, sugar, eyes","run by student volunteers"],
            body="free health checkups in communities that don't get them. organised by teenagers, backed by real doctors.",
            footer="@ngo.aquaterra")
        rep=await generate("ENG_medical","number_hero",content,accent_idx=3)
        import json; print(json.dumps(rep,indent=2))
    asyncio.run(demo())
