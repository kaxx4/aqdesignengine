"""AQ ENGINE — compare: structural reference-vs-recreation measurement.

WHY THIS EXISTS
`ref_metrics.analyze()` returns five GLOBAL scalars (dom_cov, sat, contrast, ink, vdr). Global
statistics are blind to structure: a recreation with the hero bottom-left and a reference with the
hero top-right can score identically. That is precisely why the convergence loop has reported
"error 0.3" on recreations that visually stray badly — the loop had no gradient for WHERE things
are, HOW SPREAD OUT they are, or HOW DETAILED they are.

Measured on the real failure case (c42f94a09f sticker pile vs out/versions/c42f94a09f07cd/v2.png):
the reference is a tight overlapping pile of 11 die-cut stickers with internal detail; the
recreation is a loose spread of flat primitives. Every ref_metrics number was in range.

This module measures the things that actually differ:
  1. OCCUPANCY  — where content sits, how big, centroid, bbox IoU
  2. DISPERSION — radius of gyration: "your pile is spread; the reference is tight"
  3. DETAIL     — edge energy per unit content: "you drew a simpler object than the reference"
  4. PALETTE    — dominant content colors, matched pairwise, with unmatched hues named
  5. SPATIAL    — per-cell occupancy diff: which regions are over/under-filled

and turns each into a DIRECTED CRITIQUE — an actionable instruction, not just a number, so the
next iteration knows what to change. Convergence needs a gradient, not a score.

Usage:
    r = compare.compare("training_samples/reference_posters/x.jpg", "out/versions/x/v2.png")
    print(r["score"]);  [print(c) for c in r["critique"]]
"""
import numpy as np
from PIL import Image, ImageFilter
from collections import Counter

SIZE = (540, 675)          # common analysis resolution (feed aspect 4:5)


def _load(path, size=SIZE):
    im = Image.open(path).convert("RGB")
    # letterbox-free: just resize to the common analysis canvas; both inputs are the same
    # aspect in practice (1080x1350 feed), and relative geometry is what we compare.
    return im.resize(size, Image.LANCZOS)


def _arrays(im):
    a = np.asarray(im).astype(np.float32)
    lum = a @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
    return a, lum


def _bg_color(a):
    """Modal quantized color = the background field."""
    q = (a // 24 * 24).reshape(-1, 3)
    common = Counter(map(tuple, q)).most_common(1)[0][0]
    return np.array(common, dtype=np.float32)


def content_mask(a, tol=46, im=None, denoise=True):
    """Pixels that are NOT the background field. This is 'the design' as opposed to 'the paper'.

    DENOISE matters: several references are riso/paper-textured, and raw grain deviates from the
    modal colour enough to register as CONTENT. Measured on the textured set (64b2248475,
    d375fd7dbc, eaad68d630, 502e07d0eb) that inflated reference coverage so much that clean flat
    AQ renders were reported at 0.26-0.39x area — a false 'CONTENT TOO SMALL' on all four, which
    would have driven the loop to cram the canvas to chase a measurement artifact.
    A small blur before masking averages grain away while leaving real shape edges intact.
    """
    if denoise and im is not None:
        a = np.asarray(im.filter(ImageFilter.GaussianBlur(2.2))).astype(np.float32)
    bg = _bg_color(a)
    d = np.sqrt(((a - bg) ** 2).sum(-1))
    return d > tol


def _occupancy(mask):
    ys, xs = np.nonzero(mask)
    H, W = mask.shape
    if len(xs) == 0:
        return dict(area=0.0, bbox=(0, 0, 0, 0), centroid=(0.5, 0.5), gyration=0.0)
    x0, x1, y0, y1 = xs.min() / W, xs.max() / W, ys.min() / H, ys.max() / H
    cx, cy = xs.mean() / W, ys.mean() / H
    # radius of gyration (normalised): how spread the content is about its own centroid.
    # A tight overlapping pile has small gyration; a loose scatter has large.
    gy = float(np.sqrt((((xs / W - cx) ** 2) + ((ys / H - cy) ** 2)).mean()))
    return dict(area=float(mask.mean()), bbox=(x0, y0, x1, y1), centroid=(float(cx), float(cy)),
                gyration=gy)


def _detail(im, mask):
    """Edge energy per unit of content. THE metric that catches 'detailed sticker -> flat blob'.
    A reference laptop with keyboard keys and a hand with knuckle lines carries far more internal
    edge per pixel of ink than a plain rounded rectangle of the same size and colour."""
    g = np.asarray(im.convert("L").filter(ImageFilter.FIND_EDGES)).astype(np.float32)
    n = max(1, int(mask.sum()))
    return float(g[mask].sum() / n) if mask.any() else 0.0


def _palette(a, mask, k=6):
    """Dominant colours of the CONTENT only (background excluded), by coverage."""
    if not mask.any():
        return []
    q = (a[mask] // 32 * 32)
    cnt = Counter(map(tuple, q.astype(int)))
    tot = sum(cnt.values())
    return [(np.array(c, dtype=np.float32), n / tot) for c, n in cnt.most_common(k)]


def _match_palette(pa, pb):
    """Greedy nearest-colour matching; returns (mean_dist_of_matched, unmatched_from_a)."""
    used, dists, unmatched = set(), [], []
    for ca, wa in pa:
        best, bi = None, None
        for i, (cb, wb) in enumerate(pb):
            if i in used:
                continue
            d = float(np.sqrt(((ca - cb) ** 2).sum()))
            if best is None or d < best:
                best, bi = d, i
        if best is not None and best < 110:
            used.add(bi)
            dists.append(best * wa)
        else:
            unmatched.append((ca, wa))
    return (float(np.sum(dists)) if dists else 0.0), unmatched


def _grid_occupancy(mask, gw=9, gh=11):
    H, W = mask.shape
    out = np.zeros((gh, gw), dtype=np.float32)
    for r in range(gh):
        for c in range(gw):
            out[r, c] = mask[r * H // gh:(r + 1) * H // gh, c * W // gw:(c + 1) * W // gw].mean()
    return out


def _name_color(c):
    r, g, b = [int(v) for v in c]
    mx, mn = max(r, g, b), min(r, g, b)
    if mx - mn < 28:
        return "near-neutral" if mx > 120 else "dark/ink"
    if r >= g and r >= b:
        return "warm red/pink" if b >= g else "orange/warm"
    if g >= r and g >= b:
        return "green/teal"
    return "blue/purple"


def compare(ref_path, gen_path, gw=9, gh=11):
    ref, gen = _load(ref_path), _load(gen_path)
    ra, rl = _arrays(ref)
    ga, gl = _arrays(gen)
    rm, gm = content_mask(ra, im=ref), content_mask(ga, im=gen)

    ro, go = _occupancy(rm), _occupancy(gm)
    rd, gd = _detail(ref, rm), _detail(gen, gm)
    rp, gp = _palette(ra, rm), _palette(ga, gm)
    pal_dist, unmatched = _match_palette(rp, gp)

    rg, gg = _grid_occupancy(rm, gw, gh), _grid_occupancy(gm, gw, gh)
    cell_delta = np.abs(rg - gg)

    # bbox IoU
    def iou(b1, b2):
        ax0, ay0, ax1, ay1 = b1
        bx0, by0, bx1, by1 = b2
        ix0, iy0 = max(ax0, bx0), max(ay0, by0)
        ix1, iy1 = min(ax1, bx1), min(ay1, by1)
        iw, ih = max(0.0, ix1 - ix0), max(0.0, iy1 - iy0)
        inter = iw * ih
        ua = (ax1 - ax0) * (ay1 - ay0) + (bx1 - bx0) * (by1 - by0) - inter
        return float(inter / ua) if ua > 0 else 0.0

    box_iou = iou(ro["bbox"], go["bbox"])
    area_ratio = (go["area"] / ro["area"]) if ro["area"] > 0 else 0.0
    detail_ratio = (gd / rd) if rd > 0 else 0.0
    gyr_ratio = (go["gyration"] / ro["gyration"]) if ro["gyration"] > 0 else 0.0

    # ── weighted score: 0 is a perfect match, ~1.0 is badly off ──
    score = (0.30 * float(cell_delta.mean()) * 4
             + 0.20 * abs(1 - min(area_ratio, 3))
             + 0.20 * abs(1 - min(detail_ratio, 3))
             + 0.15 * (1 - box_iou)
             + 0.15 * min(pal_dist / 90.0, 1.5))

    # ── DIRECTED CRITIQUE: each number becomes an instruction ──
    crit = []
    if detail_ratio < 0.72:
        crit.append(f"DETAIL TOO LOW ({detail_ratio:.2f}x reference): your shapes are simpler than "
                    f"the reference's. Its objects carry internal linework (keys, creases, teeth, "
                    f"scallops); yours are flat silhouettes. Add interior detail or use a richer "
                    f"silhouette — do NOT just recolour a primitive.")
    elif detail_ratio > 1.45:
        crit.append(f"DETAIL TOO HIGH ({detail_ratio:.2f}x): more linework/texture than the "
                    f"reference. Simplify or remove outline weight.")
    if area_ratio < 0.75:
        crit.append(f"CONTENT TOO SMALL ({area_ratio:.2f}x reference coverage): scale the "
                    f"composition up before adding anything new.")
    elif area_ratio > 1.3:
        crit.append(f"CONTENT TOO LARGE ({area_ratio:.2f}x): reduce scale or trim elements.")
    if gyr_ratio > 1.18:
        crit.append(f"TOO DISPERSED ({gyr_ratio:.2f}x the reference's spread): the reference is a "
                    f"TIGHTER cluster. Pull elements toward the centroid and allow overlap.")
    elif gyr_ratio < 0.84 and gyr_ratio > 0:
        crit.append(f"TOO CLUSTERED ({gyr_ratio:.2f}x): the reference spreads wider across the canvas.")
    dc = (go["centroid"][0] - ro["centroid"][0], go["centroid"][1] - ro["centroid"][1])
    if abs(dc[0]) > 0.06 or abs(dc[1]) > 0.06:
        crit.append(f"CENTROID OFF by ({dc[0]:+.2f}, {dc[1]:+.2f}) of canvas: shift the mass "
                    f"{'right' if dc[0] < 0 else 'left'}/"
                    f"{'down' if dc[1] < 0 else 'up'} to match.")
    for c, w in unmatched[:3]:
        crit.append(f"MISSING COLOUR {_name_color(c)} rgb{tuple(int(v) for v in c)} "
                    f"({w*100:.0f}% of reference content) has no counterpart in your render.")
    # worst regions
    flat = [(float(cell_delta[r, c]), r, c) for r in range(gh) for c in range(gw)]
    flat.sort(reverse=True)
    for d, r, c in flat[:3]:
        if d < 0.10:
            break
        where = f"row {r+1}/{gh}, col {c+1}/{gw}"
        side = "UNDER-filled" if gg[r, c] < rg[r, c] else "OVER-filled"
        crit.append(f"REGION {side} at {where} (delta {d:.2f}) — reference has "
                    f"{rg[r,c]:.2f} coverage there, you have {gg[r,c]:.2f}.")

    return dict(score=round(float(score), 3),
                area_ratio=round(area_ratio, 3), detail_ratio=round(detail_ratio, 3),
                gyration_ratio=round(gyr_ratio, 3), bbox_iou=round(box_iou, 3),
                palette_dist=round(pal_dist, 1),
                ref=dict(area=round(ro["area"], 3), centroid=[round(v, 3) for v in ro["centroid"]],
                         gyration=round(ro["gyration"], 3), detail=round(rd, 2)),
                gen=dict(area=round(go["area"], 3), centroid=[round(v, 3) for v in go["centroid"]],
                         gyration=round(go["gyration"], 3), detail=round(gd, 2)),
                critique=crit)


def report(ref_path, gen_path):
    r = compare(ref_path, gen_path)
    lines = [f"SCORE {r['score']}  (0 = match)",
             f"  area {r['area_ratio']}x | detail {r['detail_ratio']}x | "
             f"spread {r['gyration_ratio']}x | bbox IoU {r['bbox_iou']} | palette {r['palette_dist']}"]
    lines += ["  - " + c for c in r["critique"]]
    return "\n".join(lines)
