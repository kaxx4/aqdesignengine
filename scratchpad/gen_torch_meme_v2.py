import asyncio, os, sys, base64, importlib.util

os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)

def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout"); T = load("tex")

W, H = 1080, 1440
M = 64
A = core.ACCENTS

def snap(v): return round(v / 8) * 8

def b64_img(path, mime="image/png"):
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()

def chip(txt, accent, x, y, rot=0, dark_border=False, fs=17):
    fg = "#0A0A0A" if accent in core.INK_ON else "#fff"
    edge = "var(--bg)" if dark_border else "var(--ink)"
    return (f'<div style="position:absolute;top:{snap(y)}px;left:{snap(x)}px;background:{accent};color:{fg};'
            f'font-family:var(--m);font-weight:700;font-size:{fs}px;letter-spacing:.05em;text-transform:uppercase;'
            f'padding:10px 18px;border-radius:999px;border:3px solid {edge};box-shadow:4px 4px 0 {edge};'
            f'transform:rotate({rot}deg);z-index:14;white-space:nowrap">{txt}</div>')

def doodle(kind, x, y, size, accent, rot=0, z=15):
    fn = getattr(dd, kind, dd.star)
    try: inner = fn(fill=accent, rot=rot)
    except TypeError:
        try: inner = fn(stroke=accent, rot=rot)
        except TypeError: inner = fn(rot=rot)
    return f'<div style="position:absolute;top:{snap(y)}px;left:{snap(x)}px;width:{size}px;height:{size}px;z-index:{z}">{inner}</div>'

def photo_wrap(src, tint, object_pos="50% 50%", grayscale=True):
    filt = "filter:grayscale(1) contrast(1.2) brightness(1.05)" if grayscale else "filter:contrast(1.08) brightness(1.02)"
    return (f'<div style="position:relative;width:100%;height:100%;overflow:hidden">'
            f'<img src="{src}" style="width:100%;height:100%;object-fit:cover;object-position:{object_pos};{filt}">'
            f'<div style="position:absolute;inset:0;background:{tint};mix-blend-mode:multiply;opacity:.55"></div>'
            f'<div style="position:absolute;inset:0;background-image:radial-gradient(#00000055 1.2px,transparent 1.6px);'
            f'background-size:5px 5px;mix-blend-mode:multiply;opacity:.4"></div></div>')

def header(kicker_txt, top_right_txt):
    return "".join([
        f'<img src="{core.LOGO}" style="position:absolute;top:48px;left:{M}px;height:34px;z-index:20">',
        f'<span style="position:absolute;top:96px;left:{M}px;font-family:var(--m);font-weight:700;font-size:13px;'
        f'letter-spacing:.12em;text-transform:uppercase;color:var(--ink);opacity:.7;z-index:20">{kicker_txt}</span>',
        f'<div style="position:absolute;top:44px;right:{M}px;background:var(--ink);color:var(--bg);'
        f'font-family:var(--m);font-weight:700;font-size:15px;letter-spacing:.06em;padding:8px 16px;'
        f'border-radius:999px;z-index:20;white-space:nowrap">{top_right_txt}</div>',
    ])

yamal_uri = b64_img("scratchpad/Screenshot 2026-07-18 115448.png")
messi_uri = b64_img("scratchpad/Screenshot 2026-07-18 115500.png")
esp_accent = A[3]   # tomato
arg_accent = A[4]   # sky
badge_accent = A[2] # lemon

RESULTS = []

def emit(slug, html, elements, color_pairs, collision_ignore=frozenset()):
    RESULTS.append((slug, html, elements, color_pairs, collision_ignore))

# ═══════════════════════════════════════════════════════════════════
# LAYOUT A — "AGE GAP FLEX": stacked split + VS badge (the classic versus format, kept as-is
# because it's the one joke that's actually ABOUT a head-to-head confrontation).
# ═══════════════════════════════════════════════════════════════════
frame_w = W - 2 * M
yamal_y, yamal_h = 128, 508
messi_y, messi_h = yamal_y + yamal_h + 26, 508
panel_y = messi_y + messi_h + 26
panel_h = H - panel_y - M
yamal_photo = photo_wrap(yamal_uri, esp_accent + "40", object_pos="50% 12%")
messi_photo = photo_wrap(messi_uri, arg_accent + "40", object_pos="50% 30%")

elements = [
    ("logo", M, 48, 210, 34), ("kicker", M, 96, 380, 24), ("index_chip", W - M - 230, 44, 230, 40),
    ("yamal_frame", M, yamal_y, frame_w, yamal_h), ("messi_frame", M, messi_y, frame_w, messi_h),
    ("vs_badge", W // 2 - 62, yamal_y + yamal_h - 62, 124, 124), ("panel", M, panel_y, frame_w, panel_h),
]
color_pairs = [("panel", "var(--ink)", "var(--bg)"), ("yamal_chip", esp_accent, "var(--ink)"),
               ("messi_chip", arg_accent, "var(--ink)")]
panel_content = "".join([
    f'<div style="font-family:var(--d);font-weight:900;font-size:50px;line-height:1.02;text-transform:uppercase;'
    f'color:{badge_accent}">messi&rsquo;s socks are older<br>than this kid</div>',
    f'<div style="font-family:var(--m);font-weight:700;font-size:16px;letter-spacing:.03em;color:var(--bg);'
    f'opacity:.8">professional since 2004 vs. barely legal to drive. still not a fair fight.</div>',
])
inner = "".join([
    '<div style="position:absolute;inset:0;background:var(--bg)"></div>',
    header("field notes &middot; not sponsored", "20 YEAR AGE GAP"),
    f'<div style="position:absolute;left:{M}px;top:{yamal_y}px;width:{frame_w}px;height:{yamal_h}px;'
    f'border-radius:24px;border:6px solid var(--ink);box-shadow:10px 10px 0 var(--ink);overflow:hidden;z-index:4">{yamal_photo}</div>',
    chip("lamine yamal, 17 &middot; &quot;the new kid&quot;", esp_accent, M + 24, yamal_y + yamal_h - 64, rot=-1.5),
    doodle("star", M + frame_w - 66, yamal_y - 30, 76, badge_accent, rot=-10, z=16),
    f'<div style="position:absolute;left:{M}px;top:{messi_y}px;width:{frame_w}px;height:{messi_h}px;'
    f'border-radius:24px;border:6px solid var(--ink);box-shadow:10px 10px 0 var(--ink);overflow:hidden;z-index:4">{messi_photo}</div>',
    chip("lionel messi &middot; age 37 &middot; &quot;still here&quot;", arg_accent, M + 24, messi_y + messi_h - 64, rot=1.5),
    f'<div style="position:absolute;left:{W//2-62}px;top:{yamal_y+yamal_h-62}px;width:124px;height:124px;'
    f'border-radius:50%;background:{badge_accent};border:6px solid var(--ink);box-shadow:6px 6px 0 var(--ink);'
    f'display:flex;align-items:center;justify-content:center;z-index:10">'
    f'<span style="font-family:var(--d);font-weight:900;font-size:30px;color:#0A0A0A">VS</span></div>',
    f'<div style="position:absolute;left:{M}px;top:{panel_y}px;width:{frame_w}px;height:{panel_h}px;'
    f'background:var(--ink);border-radius:24px;box-shadow:10px 10px 0 rgba(10,10,10,0.28);z-index:4;'
    f'display:flex;flex-direction:column;justify-content:center;gap:16px;padding:36px;box-sizing:border-box">{panel_content}</div>',
    doodle("burst", M + frame_w - 90, panel_y + panel_h - 90, 66, esp_accent, rot=8, z=12),
])
emit("age_gap_flex", B.page(W, H, "var(--bg)", inner, grain=True), elements, color_pairs,
     collision_ignore=frozenset({frozenset({"panel", "vs_badge"}), frozenset({"yamal_frame", "vs_badge"}),
                                  frozenset({"messi_frame", "vs_badge"})}))

# ═══════════════════════════════════════════════════════════════════
# LAYOUT B — "QUOTE FLIP": single big Messi hero (he's the subject of the quote), Yamal as a
# small circular inset avatar pinned to the frame's corner, giant serif pull-quote below on
# cream (not another ink panel — visual variety from layout A).
# ═══════════════════════════════════════════════════════════════════
hero_y, hero_h = 128, 700
avatar_d = 176
avatar_x, avatar_y = M + 32, hero_y + hero_h - avatar_d // 2
quote_y = hero_y + hero_h + 112  # clear the avatar's dip below the hero frame (avatar_d//2 + margin)
attrib_y = quote_y + 148

messi_hero = photo_wrap(messi_uri, arg_accent + "35", object_pos="50% 28%")
yamal_avatar = photo_wrap(yamal_uri, esp_accent + "45", object_pos="50% 15%")

elements = [
    ("logo", M, 48, 210, 34), ("kicker", M, 96, 380, 24), ("index_chip", W - M - 200, 44, 200, 40),
    ("hero_frame", M, hero_y, frame_w, hero_h),
    ("avatar", avatar_x, avatar_y, avatar_d, avatar_d),
    ("quote", M, quote_y, frame_w, 148),
    ("attrib", M, attrib_y, frame_w, 56),
    ("attrib_footer", M, attrib_y + 102, 260, 24),
    ("attrib_doodle", M + frame_w - 58, attrib_y + 84, 58, 58),
]
color_pairs = [("avatar_ring", "var(--ink)", "var(--bg)")]
inner = "".join([
    '<div style="position:absolute;inset:0;background:var(--bg)"></div>',
    header("field notes &middot; not sponsored", "REAL QUOTE, REAL CHEEK"),
    f'<div style="position:absolute;left:{M}px;top:{hero_y}px;width:{frame_w}px;height:{hero_h}px;'
    f'border-radius:28px;border:6px solid var(--ink);box-shadow:12px 12px 0 var(--ink);overflow:hidden;z-index:4">{messi_hero}</div>',
    chip("lionel messi &middot; the subject", arg_accent, M + 28, hero_y + 28, rot=-1),
    f'<div style="position:absolute;left:{avatar_x}px;top:{avatar_y}px;width:{avatar_d}px;height:{avatar_d}px;'
    f'border-radius:50%;border:7px solid var(--ink);box-shadow:6px 6px 0 var(--ink);overflow:hidden;z-index:10">{yamal_avatar}</div>',
    chip("yamal says &darr;", esp_accent, avatar_x + avatar_d + 16, avatar_y + avatar_d - 44, rot=2),
    doodle("star", M + frame_w - 66, hero_y - 30, 76, badge_accent, rot=-10, z=16),
    f'<div style="position:absolute;left:{M}px;top:{quote_y}px;width:{frame_w}px;font-family:var(--s);'
    f'font-style:italic;font-size:52px;line-height:1.12;color:var(--ink);z-index:12">'
    f'&ldquo;this kid doesn&rsquo;t play football&hellip;<br>he plays <span style="color:{esp_accent}">something else</span>&rdquo;</div>',
    f'<div style="position:absolute;left:{M}px;top:{attrib_y}px;width:{frame_w}px;font-family:var(--m);'
    f'font-weight:700;font-size:16px;letter-spacing:.03em;color:var(--ink);opacity:.65;z-index:12">'
    f'&mdash; lamine yamal, on lionel messi. bold words from a guy who was in diapers for messi&rsquo;s first ballon d&rsquo;or.</div>',
    f'<div style="position:absolute;left:{M}px;top:{attrib_y+82}px;width:{frame_w}px;height:1px;'
    f'background:rgba(10,10,10,0.15);z-index:8"></div>',
    f'<span style="position:absolute;left:{M}px;top:{attrib_y+102}px;font-family:var(--m);font-weight:700;'
    f'font-size:13px;letter-spacing:.1em;color:var(--ink);opacity:.55;z-index:12">field notes carousel &middot; 02/05</span>',
    doodle("burst", M + frame_w - 58, attrib_y + 84, 58, esp_accent, rot=8, z=12),
])
emit("quote_flip_v2", B.page(W, H, "var(--bg)", inner, grain=True), elements, color_pairs,
     collision_ignore=frozenset({frozenset({"hero_frame", "avatar"})}))

# ═══════════════════════════════════════════════════════════════════
# LAYOUT C — "TROPHY VS SKINCARE": side-by-side split (not stacked), a stat strip under each
# half, one headline banner spanning the full width underneath.
# ═══════════════════════════════════════════════════════════════════
half_w = (frame_w - 24) / 2
sbs_y, sbs_h = 128, 760
left_x = M
right_x = M + half_w + 24
stat_y = sbs_y + sbs_h + 24
panel2_y = stat_y + 90
panel2_h = H - panel2_y - M

yamal_side = photo_wrap(yamal_uri, esp_accent + "40", object_pos="50% 14%")
messi_side = photo_wrap(messi_uri, arg_accent + "40", object_pos="50% 32%")

elements = [
    ("logo", M, 48, 210, 34), ("kicker", M, 96, 380, 24), ("index_chip", W - M - 220, 44, 220, 40),
    ("yamal_half", left_x, sbs_y, half_w, sbs_h), ("messi_half", right_x, sbs_y, half_w, sbs_h),
    ("yamal_stat", left_x, stat_y, half_w, 64), ("messi_stat", right_x, stat_y, half_w, 64),
    ("panel", M, panel2_y, frame_w, panel2_h),
]
color_pairs = [("panel", "var(--ink)", "var(--bg)"), ("yamal_stat_bg", esp_accent, "var(--bg)"),
               ("messi_stat_bg", arg_accent, "var(--bg)")]
panel2_content = "".join([
    f'<div style="font-family:var(--d);font-weight:900;font-size:52px;line-height:1.02;text-transform:uppercase;'
    f'color:{badge_accent}">8 ballon d&rsquo;ors vs. an<br>8-step skincare routine</div>',
    f'<div style="font-family:var(--m);font-weight:700;font-size:16px;letter-spacing:.03em;color:var(--bg);'
    f'opacity:.8">only one of these routines actually ages well.</div>',
])
inner = "".join([
    '<div style="position:absolute;inset:0;background:var(--bg)"></div>',
    header("field notes &middot; not sponsored", "GENERATIONAL GAP"),
    f'<div style="position:absolute;left:{left_x}px;top:{sbs_y}px;width:{half_w}px;height:{sbs_h}px;'
    f'border-radius:22px;border:6px solid var(--ink);box-shadow:8px 8px 0 var(--ink);overflow:hidden;z-index:4">{yamal_side}</div>',
    f'<div style="position:absolute;left:{right_x}px;top:{sbs_y}px;width:{half_w}px;height:{sbs_h}px;'
    f'border-radius:22px;border:6px solid var(--ink);box-shadow:8px 8px 0 var(--ink);overflow:hidden;z-index:4">{messi_side}</div>',
    doodle("star", left_x + half_w - 60, sbs_y - 28, 68, badge_accent, rot=-10, z=16),
    f'<div style="position:absolute;left:{left_x}px;top:{stat_y}px;width:{half_w}px;height:64px;background:{esp_accent};'
    f'border-radius:16px;border:4px solid var(--ink);box-shadow:5px 5px 0 var(--ink);display:flex;flex-direction:column;'
    f'align-items:center;justify-content:center;z-index:8">'
    f'<span style="font-family:var(--d);font-weight:900;font-size:20px;color:#0A0A0A">YAMAL, 17</span>'
    f'<span style="font-family:var(--m);font-weight:700;font-size:12px;color:#0A0A0A;opacity:.75">10-STEP ROUTINE</span></div>',
    f'<div style="position:absolute;left:{right_x}px;top:{stat_y}px;width:{half_w}px;height:64px;background:{arg_accent};'
    f'border-radius:16px;border:4px solid var(--ink);box-shadow:5px 5px 0 var(--ink);display:flex;flex-direction:column;'
    f'align-items:center;justify-content:center;z-index:8">'
    f'<span style="font-family:var(--d);font-weight:900;font-size:20px;color:#0A0A0A">MESSI, 37</span>'
    f'<span style="font-family:var(--m);font-weight:700;font-size:12px;color:#0A0A0A;opacity:.75">8 BALLON D&rsquo;ORS</span></div>',
    f'<div style="position:absolute;left:{M}px;top:{panel2_y}px;width:{frame_w}px;height:{panel2_h}px;'
    f'background:var(--ink);border-radius:24px;box-shadow:10px 10px 0 rgba(10,10,10,0.28);z-index:4;'
    f'display:flex;flex-direction:column;justify-content:center;gap:16px;padding:36px;box-sizing:border-box">{panel2_content}</div>',
    doodle("burst", M + frame_w - 90, panel2_y + panel2_h - 90, 66, esp_accent, rot=8, z=12),
])
emit("trophy_vs_skincare_v2", B.page(W, H, "var(--bg)", inner, grain=True), elements, color_pairs)

# ═══════════════════════════════════════════════════════════════════
# LAYOUT D — "RETIREMENT POSTPONED": full-bleed breaking-news hero (Messi), headline set
# directly over a dark gradient at the photo's base (chyron-style), small circular Yamal
# badge pinned top-right of the photo as "the reason why."
# ═══════════════════════════════════════════════════════════════════
bleed_y, bleed_h = 128, 980
cap_y = bleed_y + bleed_h + 32
messi_bleed = photo_wrap(messi_uri, "#00000000", object_pos="50% 22%")
badge2_d = 170
badge2_x, badge2_y = M + frame_w - badge2_d - 28, bleed_y + 28

elements = [
    ("logo", M, 48, 210, 34), ("kicker", M, 96, 380, 24), ("index_chip", W - M - 200, 44, 200, 40),
    ("bleed_frame", M, bleed_y, frame_w, bleed_h),
    ("yamal_badge", badge2_x, badge2_y, badge2_d, badge2_d),
    ("headline", M + 28, bleed_y + bleed_h - 210, frame_w - 56, 180),
    ("caption", M, cap_y, frame_w, 60),
    ("cap_footer", M, cap_y + 70, 260, 24),
    ("cap_doodle", M + frame_w - 58, cap_y + 52, 58, 58),
]
color_pairs = []
inner = "".join([
    '<div style="position:absolute;inset:0;background:var(--bg)"></div>',
    header("field notes &middot; not sponsored", "RETIREMENT: TBD"),
    f'<div style="position:absolute;left:{M}px;top:{bleed_y}px;width:{frame_w}px;height:{bleed_h}px;'
    f'border-radius:28px;border:6px solid var(--ink);box-shadow:12px 12px 0 var(--ink);overflow:hidden;z-index:4">'
    f'{messi_bleed}<div style="position:absolute;inset:0;background:linear-gradient(180deg,transparent 45%,rgba(10,10,10,.88) 92%);z-index:2"></div></div>',
    f'<div style="position:absolute;left:{badge2_x}px;top:{badge2_y}px;width:{badge2_d}px;height:{badge2_d}px;'
    f'border-radius:50%;border:6px solid var(--ink);box-shadow:6px 6px 0 var(--ink);overflow:hidden;z-index:10">'
    f'{photo_wrap(yamal_uri, esp_accent + "40", object_pos="50% 12%")}</div>',
    chip("the reason why", esp_accent, badge2_x - 40, badge2_y + badge2_d - 6, rot=-2),
    f'<div style="position:absolute;left:{M+28}px;top:{bleed_y+bleed_h-210}px;width:{frame_w-56}px;z-index:8;'
    f'font-family:var(--d);font-weight:900;font-size:56px;line-height:1.0;text-transform:uppercase;'
    f'color:{badge_accent};text-shadow:3px 3px 0 rgba(0,0,0,.6)">retirement tour:<br>now entering year 6</div>',
    f'<div style="position:absolute;left:{M}px;top:{cap_y}px;width:{frame_w}px;font-family:var(--m);'
    f'font-weight:700;font-size:16px;letter-spacing:.03em;color:var(--ink);opacity:.7;z-index:12">'
    f'cancelled again due to teenager interference. sunset rescheduled indefinitely.</div>',
    f'<div style="position:absolute;left:{M}px;top:{cap_y+50}px;width:{frame_w}px;height:1px;'
    f'background:rgba(10,10,10,0.15);z-index:8"></div>',
    f'<span style="position:absolute;left:{M}px;top:{cap_y+70}px;font-family:var(--m);font-weight:700;'
    f'font-size:13px;letter-spacing:.1em;color:var(--ink);opacity:.55;z-index:12">field notes carousel &middot; 04/05</span>',
    doodle("burst", M + frame_w - 58, cap_y + 52, 58, esp_accent, rot=8, z=12),
])
emit("retirement_postponed_v2", B.page(W, H, "var(--bg)", inner, grain=True), elements, color_pairs,
     collision_ignore=frozenset({frozenset({"bleed_frame", "yamal_badge"}), frozenset({"bleed_frame", "headline"})}))

# ═══════════════════════════════════════════════════════════════════
# LAYOUT E — "EMPLOYMENT STATUS": side-by-side square-cornered ID cards (distinct from layout
# C's rounded side-by-side — passport-photo styling) with rotated rubber-stamp badges instead
# of pill chips, playing the "job application" bit.
# ═══════════════════════════════════════════════════════════════════
id_y, id_h = 168, 760
id_stat_y = id_y + id_h + 28
panel3_y = id_stat_y + 96
panel3_h = H - panel3_y - M

yamal_id = photo_wrap(yamal_uri, esp_accent + "35", object_pos="50% 14%", grayscale=True)
messi_id = photo_wrap(messi_uri, arg_accent + "35", object_pos="50% 32%", grayscale=True)

def stamp(txt, color, x, y, w, rot):
    return (f'<div style="position:absolute;top:{snap(y)}px;left:{snap(x)}px;width:{w}px;text-align:center;'
            f'border:5px solid {color};border-radius:14px;color:{color};font-family:var(--d);font-weight:900;'
            f'font-size:22px;letter-spacing:.04em;text-transform:uppercase;padding:12px 10px;'
            f'transform:rotate({rot}deg);opacity:.92;z-index:14;background:rgba(244,239,224,.55)">{txt}</div>')

elements = [
    ("logo", M, 48, 210, 34), ("kicker", M, 96, 380, 24), ("index_chip", W - M - 230, 44, 230, 40),
    ("yamal_id", left_x, id_y, half_w, id_h), ("messi_id", right_x, id_y, half_w, id_h),
    ("yamal_id_label", left_x, id_stat_y, half_w, 64), ("messi_id_label", right_x, id_stat_y, half_w, 64),
    ("panel", M, panel3_y, frame_w, panel3_h),
]
color_pairs3 = [("panel", "var(--ink)", "var(--bg)")]
panel3_content = "".join([
    f'<div style="font-family:var(--d);font-weight:900;font-size:50px;line-height:1.04;text-transform:uppercase;'
    f'color:{badge_accent}">application received.<br>position not open.</div>',
    f'<div style="font-family:var(--m);font-weight:700;font-size:16px;letter-spacing:.03em;color:var(--bg);'
    f'opacity:.8">messi has held the role since 2005. hr says he&rsquo;s &ldquo;not going anywhere.&rdquo;</div>',
])
inner = "".join([
    '<div style="position:absolute;inset:0;background:var(--bg)"></div>',
    header("field notes &middot; not sponsored", "HIRING FREEZE"),
    f'<div style="position:absolute;left:{left_x}px;top:{id_y}px;width:{half_w}px;height:{id_h}px;'
    f'border-radius:6px;border:6px solid var(--ink);box-shadow:8px 8px 0 var(--ink);overflow:hidden;z-index:4">{yamal_id}</div>',
    stamp("pending review", esp_accent, left_x + 20, id_y + id_h - 150, half_w - 40, -8),
    f'<div style="position:absolute;left:{right_x}px;top:{id_y}px;width:{half_w}px;height:{id_h}px;'
    f'border-radius:6px;border:6px solid var(--ink);box-shadow:8px 8px 0 var(--ink);overflow:hidden;z-index:4">{messi_id}</div>',
    stamp("not accepting resignations", arg_accent, right_x + 12, id_y + id_h - 150, half_w - 24, 6),
    doodle("star", left_x + half_w - 56, id_y - 28, 64, badge_accent, rot=-10, z=16),
    f'<div style="position:absolute;left:{left_x}px;top:{id_stat_y}px;width:{half_w}px;font-family:var(--m);'
    f'font-weight:700;font-size:15px;text-align:center;color:var(--ink);z-index:8">LAMINE YAMAL<br>'
    f'<span style="opacity:.6;font-weight:500;font-size:13px">APPLICANT, STATUS: PENDING</span></div>',
    f'<div style="position:absolute;left:{right_x}px;top:{id_stat_y}px;width:{half_w}px;font-family:var(--m);'
    f'font-weight:700;font-size:15px;text-align:center;color:var(--ink);z-index:8">LIONEL MESSI<br>'
    f'<span style="opacity:.6;font-weight:500;font-size:13px">INCUMBENT, STATUS: EMPLOYED</span></div>',
    f'<div style="position:absolute;left:{M}px;top:{panel3_y}px;width:{frame_w}px;height:{panel3_h}px;'
    f'background:var(--ink);border-radius:24px;box-shadow:10px 10px 0 rgba(10,10,10,0.28);z-index:4;'
    f'display:flex;flex-direction:column;justify-content:center;gap:16px;padding:36px;box-sizing:border-box">{panel3_content}</div>',
    doodle("burst", M + frame_w - 90, panel3_y + panel3_h - 90, 66, esp_accent, rot=8, z=12),
])
emit("employment_status", B.page(W, H, "var(--bg)", inner, grain=True), elements, color_pairs3)

async def main():
    os.makedirs("out", exist_ok=True)
    for slug, html, elements, color_pairs, ignore in RESULTS:
        pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs,
                            page_bg="var(--bg)", core=core, expect_hero=True, collision_ignore=ignore)
        out = f"out/torch_meme_{slug}.png"
        await B.render(html, out, W, H)
        print(f"[{slug:26s}] clean={pf['clean']} -> {out}")

asyncio.run(main())
