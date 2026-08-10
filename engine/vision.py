"""AQ ENGINE — vision: automatic placement intelligence for real-photo pieces.

WHY THIS EXISTS
CAROUSEL_PLAYBOOK.md says the one irreducibly manual step in a photo carousel is "look at the photo
and find the empty zone" — and every face-collision / edge-clip bug in the Sunderbans batch came from
a human eyeballing that step wrong. It is NOT irreducible. A photo's empty regions are measurable:
they are the low-edge-energy, low-variance areas (sky, walls, ceilings). Faces and bodies are, by
construction, the HIGH-detail regions. So a flatness map solves subject-avoidance and free-zone
finding with the same measurement.

This module turns these into RULES (CLAUDE.md §8), replacing eye-judgment:
  - where can decoration go?            -> free_zones() / plan_spots()
  - will it land on a face/subject?      -> busy + skin gating, never place on high-detail cells
  - will it be visible once placed?      -> pick_visible() measures LOCAL luminance behind the spot
  - how big should it be?                -> size derived from actual clearance, not a guessed constant

Dependencies: PIL + numpy only (no cv2/scipy in this environment — deliberately avoided).

Coordinates are CANVAS space (e.g. 1080x1350), matching what the bespoke scripts and build.render
use, so returned (x,y,size) can be passed straight to a doodle helper.
"""
import os
import numpy as np
from PIL import Image
from collections import deque

CELL = 30          # grid resolution in canvas px; 1080x1350 -> 36x45 cells.
                   # 45px was too coarse: the clearance test could only express distance in
                   # 45px steps, so requiring 3 cells demanded 135px of air and starved real
                   # photos down to 1-2 usable spots. At 30px the same rule asks for 90px and
                   # size falls out of actual clearance, giving natural small/large variety.
BUSY_PCTL = 45     # cells below this percentile of busy-score are candidate "flat"
SKIN_MAX = 0.02    # any cell with >2% skin-tone pixels is never a placement candidate


# ── image loading that MATCHES the render ──────────────────────────────────────
def _cover(im, W, H):
    """Replicate CSS `object-fit:cover` exactly: scale to cover, then center-crop.
    Without this the analysis grid would be measuring a differently-framed image than
    the one that actually renders, and every returned coordinate would be subtly wrong."""
    iw, ih = im.size
    s = max(W / iw, H / ih)
    nw, nh = max(1, round(iw * s)), max(1, round(ih * s))
    im = im.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - W) // 2, (nh - H) // 2
    return im.crop((left, top, left + W, top + H))


def _load(path, W, H):
    im = _cover(Image.open(path).convert("RGB"), W, H)
    rgb = np.asarray(im).astype(np.float32)
    gray = rgb @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
    return rgb, gray


def _skin(rgb):
    """Classic RGB skin-tone rule. A cheap second safety net on top of the busy map:
    skin can occasionally be smooth (a cheek in soft light reads LOW-edge), which is exactly
    the case a pure flatness map would wrongly call 'free'."""
    R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx, mn = rgb.max(-1), rgb.min(-1)
    return ((R > 95) & (G > 40) & (B > 20) & ((mx - mn) > 15) &
            (np.abs(R - G) > 15) & (R > G) & (R > B))


# ── the measurement ────────────────────────────────────────────────────────────
def analyze(path, W, H, cell=CELL):
    """Return per-cell maps: busy score, mean luminance, skin fraction."""
    rgb, gray = _load(path, W, H)
    gy = np.abs(np.diff(gray, axis=0, prepend=gray[:1, :]))
    gx = np.abs(np.diff(gray, axis=1, prepend=gray[:, :1]))
    edge = gx + gy
    skin = _skin(rgb).astype(np.float32)

    rows, cols = H // cell, W // cell
    def agg(a, fn):
        return np.array([[fn(a[r*cell:(r+1)*cell, c*cell:(c+1)*cell])
                          for c in range(cols)] for r in range(rows)], dtype=np.float32)

    e = agg(edge, np.mean)
    v = agg(gray, np.std)
    lum = agg(gray, np.mean)
    skf = agg(skin, np.mean)

    def norm(a):
        lo, hi = float(a.min()), float(a.max())
        return (a - lo) / (hi - lo) if hi > lo else np.zeros_like(a)

    busy = 0.65 * norm(e) + 0.35 * norm(v)   # edges dominate; variance catches flat-but-noisy
    return dict(busy=busy, lum=lum, skin=skf, cell=cell, rows=rows, cols=cols, W=W, H=H)


def _clearance(free):
    """Chebyshev-ish distance (in cells) from every free cell to the nearest busy cell,
    via multi-source BFS. Padding with a busy border means canvas edges also push the
    distance down — that is what stops a chip from being placed hard against the margin
    and clipping (the 'FREE CHECK' bug)."""
    R, C = free.shape
    pad = np.zeros((R + 2, C + 2), dtype=bool)
    pad[1:-1, 1:-1] = free
    dist = np.full(pad.shape, -1, dtype=int)
    dq = deque()
    busy_idx = np.argwhere(~pad)
    for r, c in busy_idx:
        dist[r, c] = 0
        dq.append((int(r), int(c)))
    while dq:
        r, c = dq.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < dist.shape[0] and 0 <= nc < dist.shape[1] and dist[nr, nc] < 0:
                dist[nr, nc] = dist[r, c] + 1
                dq.append((nr, nc))
    dist[dist < 0] = 0
    return dist[1:-1, 1:-1]


def free_grid(a, exclude=None, busy_pctl=BUSY_PCTL):
    """Boolean grid of cells that are genuinely placeable.
    exclude: list of (x,y,w,h) canvas rects already occupied (logo, dots, caption, footer)."""
    busy, skin, cell = a["busy"], a["skin"], a["cell"]
    thresh = np.percentile(busy, busy_pctl)
    free = (busy <= thresh) & (skin < SKIN_MAX)
    for (ex, ey, ew, eh) in (exclude or []):
        c0, c1 = max(0, ex // cell), min(a["cols"] - 1, (ex + ew) // cell)
        r0, r1 = max(0, ey // cell), min(a["rows"] - 1, (ey + eh) // cell)
        free[r0:r1 + 1, c0:c1 + 1] = False
    return free


def _components(free):
    """Label 4-connected components of free cells. Returns (labels, {id: [cells]})."""
    R, C = free.shape
    lab = np.zeros((R, C), dtype=int)
    groups, nxt = {}, 0
    for r0 in range(R):
        for c0 in range(C):
            if not free[r0, c0] or lab[r0, c0]:
                continue
            nxt += 1
            cells, dq = [], deque([(r0, c0)])
            lab[r0, c0] = nxt
            while dq:
                r, c = dq.popleft()
                cells.append((r, c))
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < R and 0 <= nc < C and free[nr, nc] and not lab[nr, nc]:
                        lab[nr, nc] = nxt
                        dq.append((nr, nc))
            groups[nxt] = cells
    return lab, groups


def background_grid(a, exclude=None, busy_pctl=BUSY_PCTL, min_cells=6):
    """THE key refinement over raw flatness.

    A pure flatness map cannot tell 'empty sky' from 'a smooth black hoodie' — both are
    low-edge and low-variance. Measured on the Sunderbans set, naive flatness happily chose
    spots at luminance 4-33: the volunteers' dark clothing. Placing a doodle there is the exact
    face/subject-collision bug this module exists to kill.

    The discriminator is TOPOLOGY, not brightness: real background is a region that runs off the
    edge of the frame, while a subject is a flat island ENCLOSED by busy pixels. So we keep only
    free components that touch the top edge, or touch a side edge while sitting in the upper part
    of the frame (sky/wall/ceiling). A hoodie in the lower-middle touches nothing and is dropped,
    even though it is perfectly flat. The bottom edge is never a qualifying border — in these
    photos the bottom is always foreground subject.
    """
    free = free_grid(a, exclude=exclude, busy_pctl=busy_pctl)
    R, C = free.shape
    lab, groups = _components(free)
    keep = np.zeros_like(free)
    for gid, cells in groups.items():
        if len(cells) < min_cells:
            continue
        rs = [r for r, _ in cells]
        cs = [c for _, c in cells]
        touches_top = min(rs) == 0
        touches_side = (min(cs) == 0 or max(cs) == C - 1)
        upper = (sum(rs) / len(rs)) < R * 0.55
        if touches_top or (touches_side and upper):
            for r, c in cells:
                keep[r, c] = True
    return keep


# ── the deliverable: placements ────────────────────────────────────────────────
def plan_spots(path, W, H, n=4, exclude=None, min_size=26, max_size=90,
               seed=0, busy_pctl=BUSY_PCTL, cell=CELL):
    """Return up to n placement dicts, ranked by how much genuinely open room they have.

    Each dict: {x, y, size, clearance_px, lum, dark_bg}
      x,y   -> top-left in canvas space, ready for an absolutely-positioned doodle div
      size  -> DERIVED from real clearance (never a guessed constant), clamped to [min,max]
      lum   -> mean luminance behind the spot (0-255)
      dark_bg -> True if the local background is dark, so the caller can pick a light fill

    Spots are spread: once one is taken, its neighbourhood is burned so the next pick can't
    pile up beside it. This is what stops the 'six doodles crammed in one sky pocket' failure.
    """
    a = analyze(path, W, H, cell=cell)
    free = background_grid(a, exclude=exclude, busy_pctl=busy_pctl)
    if not free.any():
        return []
    dist = _clearance(free)
    dist = np.where(free, dist, 0)

    # vertical prior: among equally-clear background cells, prefer higher ones. Sky/ceiling is
    # safer than a low flat patch that may be foreground the topology test let through.
    R = free.shape[0]
    prior = np.linspace(1.0, 0.0, R)[:, None] * 0.8

    # Clearance floor is VERTICALLY AWARE. A cell with clearance 2 sits two steps from busy
    # pixels, so a square centred there spans right up to the subject — measured on img1 that
    # jammed doodles into the narrow sliver beside a woman's face. But a flat floor is wrong too:
    # the upper frame is sky/ceiling (safe at 3 cells) while the lower frame is subject territory
    # where a "background" channel is usually just a gap between two people, and needs 4.
    R_ = free.shape[0]
    def min_clear_at(row):
        return 3 if row < R_ * 0.40 else 4
    rgb, gray = _load(path, W, H)
    skinpx = _skin(rgb)

    out, taken = [], np.zeros_like(free, dtype=bool)
    rng = np.random.default_rng(seed)
    floor = np.array([[min_clear_at(r)] for r in range(R_)], dtype=int)  # per-row requirement
    while len(out) < n:
        cand = np.where(taken, -1, dist)
        # tiny deterministic jitter breaks ties without making output random per run
        score = cand + prior + rng.random(cand.shape) * 0.4
        score[cand < floor] = -1
        if score.max() < 0:             # nothing left with real breathing room
            break
        r, c = np.unravel_index(int(np.argmax(score)), score.shape)
        clear_cells = int(dist[r, c])
        clear_px = clear_cells * cell
        # half-width must stay within (clear_cells-1) cells so the shape never abuts the subject
        size = int(max(min_size, min(max_size, (clear_cells - 1) * cell)))
        cx, cy = c * cell + cell // 2, r * cell + cell // 2
        x, y = int(cx - size // 2), int(cy - size // 2)
        rad = max(2, clear_cells)
        taken[max(0, r - rad):r + rad + 1, max(0, c - rad):c + rad + 1] = True

        # FINAL PIXEL-LEVEL VETO: check the real pixels (padded 25%) rather than the coarse grid.
        # A face can occupy a fraction of a 45px cell and still be hit; this catches that.
        pad = int(size * 0.25)
        y0, y1 = max(0, y - pad), min(H, y + size + pad)
        x0, x1 = max(0, x - pad), min(W, x + size + pad)
        if skinpx[y0:y1, x0:x1].mean() > 0.01:
            continue                     # skin in the footprint — reject, try the next best cell
        out.append(dict(x=x, y=y, size=size, clearance_px=clear_px,
                        lum=float(a["lum"][r, c]), dark_bg=bool(a["lum"][r, c] < 118)))
    return out


def plan_spots_relaxed(path, W, H, n=4, exclude=None, seed=0, want=2,
                       ladder=(BUSY_PCTL, 55, 65, 75), **kw):
    """plan_spots with an escalating busy-percentile ladder, and a hard warning when it still
    comes up empty.

    WHY (bug found 2026-08-07, 2026 workshop carousel batch). plan_spots returns [] on a dense
    photo — every cell fails the clearance floor — and a caller that just does `for s in spots`
    then renders a slide with NO doodles at all. The whole craft layer vanishes SILENTLY: the
    preflight gate passes (nothing is off-canvas or colliding, because nothing exists), and only
    the looking gate catches it. That is precisely the class of flaw CLAUDE.md §8 says to convert
    into a rule.

    Two things are encoded here:
      1. Escalate busy_pctl before giving up. The default 45 is tuned for outdoor photos with real
         sky; indoor workshop shots (walls, crowded rooms) legitimately need a looser flatness bar
         to expose the same amount of genuinely-free wall. Subject safety is NOT relaxed — the
         topology test in background_grid and the skin veto in plan_spots still run at every rung.
      2. Return the ladder rung actually used, and warn on total failure, so "this slide has no
         decoration" is reported rather than silently shipped.

    Returns (spots, info) where info = {'busy_pctl': int|None, 'starved': bool}.
    """
    for pct in ladder:
        spots = plan_spots(path, W, H, n=n, exclude=exclude, seed=seed, busy_pctl=pct, **kw)
        if len(spots) >= want:
            return spots, dict(busy_pctl=pct, starved=False)
    # last rung's result (possibly 1 spot, possibly none) — surfaced, never silently swallowed
    print(f"  [vision] WARNING starved: {os.path.basename(path)} yielded {len(spots)} spot(s) "
          f"even at busy_pctl={ladder[-1]} — slide will be under-decorated")
    return spots, dict(busy_pctl=ladder[-1], starved=True)


def best_band(path, W, H, band_h=140, exclude=None, cell=CELL):
    """Find the flattest full-width horizontal band — where a text chip or caption can sit
    without fighting the photo. Returns (y, mean_busy, dark_bg) or None.
    This is the encoded version of 'if the sky is too cluttered, drop the sticker into the
    scrim band instead' — now a measurement, not a judgement call."""
    a = analyze(path, W, H, cell=cell)
    free = free_grid(a, exclude=exclude, busy_pctl=100)   # measure all cells, don't pre-filter
    rows_per = max(1, band_h // cell)
    best = None
    for r in range(0, a["rows"] - rows_per + 1):
        sl = a["busy"][r:r + rows_per, :]
        ok = free[r:r + rows_per, :]
        if not ok.any():
            continue
        m = float(sl.mean())
        if best is None or m < best[1]:
            best = (r * cell, m, bool(a["lum"][r:r + rows_per, :].mean() < 118))
    return best


def pick_visible(accents, lum, core=None, min_delta=42):
    """Choose the first accent whose luminance differs enough from the LOCAL background to be seen.
    Generalises layout.invisible_color_check from 'vs the page bg' to 'vs whatever pixels are
    actually behind this element' — the photo case that check could never handle.
    Returns (hex, ok). ok=False means nothing in the palette clears the bar; caller should use
    white/ink instead."""
    def hexlum(h):
        h = h.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return 0.299 * r + 0.587 * g + 0.114 * b
    ranked = sorted(accents, key=lambda c: -abs(hexlum(c) - lum))
    top = ranked[0]
    return (top, abs(hexlum(top) - lum) >= min_delta)


def report(path, W, H, exclude=None):
    """Human-readable summary — the headless proxy for 'I looked at the photo'."""
    a = analyze(path, W, H)
    free = background_grid(a, exclude=exclude)
    frac = float(free.mean())
    spots = plan_spots(path, W, H, n=6, exclude=exclude)
    return dict(free_fraction=round(frac, 3),
                open_spots=len(spots),
                largest_clearance_px=max([s["clearance_px"] for s in spots], default=0),
                spots=spots)
