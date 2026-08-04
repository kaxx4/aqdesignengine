# PREVIEW-CRITIQUE — mandatory self-review step after every render, BEFORE showing the user.
# Catches the "basics" the collision auditor misses: dead quadrants, sparseness, cramming,
# bingo-card uniformity, flatness. Returns pass/fail + specific fixes.
from PIL import Image
import numpy as np
def critique(path):
    im=Image.open(path).convert("RGB")
    arr=np.asarray(im.resize((216,270))).astype(int)
    bg=arr[2,2]; dist=np.abs(arr-bg).sum(2); content=(dist>45)
    H2,W2=content.shape
    quads={"TL":content[:H2//2,:W2//2].mean(),"TR":content[:H2//2,W2//2:].mean(),
           "BL":content[H2//2:,:W2//2].mean(),"BR":content[H2//2:,W2//2:].mean()}
    fill=content.mean()
    lum=(0.299*arr[:,:,0]+0.587*arr[:,:,1]+0.114*arr[:,:,2]); contrast=lum.std()/255
    from collections import Counter
    q24=(arr//24*24).reshape(-1,3)
    dom_color=Counter(map(tuple,q24)).most_common(1)[0][1]/len(q24)
    row_var=np.var([content[i*H2//6:(i+1)*H2//6,:].mean() for i in range(6)])
    col_var=np.var([content[:,i*W2//6:(i+1)*W2//6].mean() for i in range(6)])
    issues=[]
    dead=[k for k,v in quads.items() if v<0.10]
    if dead: issues.append(("dead_quadrant",f"quadrants {dead} nearly empty — spread elements there"))
    if fill<0.32: issues.append(("sparse",f"fill {fill:.2f} too low — scale elements up / add mass"))
    if fill>0.85: issues.append(("crammed",f"fill {fill:.2f} too high — remove or shrink elements"))
    if contrast<0.20: issues.append(("flat",f"contrast {contrast:.2f} — add dark type / bolder color"))
    if dom_color>0.52:
        # rule: tightened from .60 (session 5 finding — a 44-sample batch showed dom_cov running
        # +0.13 to +0.24 over target across ALL FOUR archetypes; too loose a trigger meant density
        # never escalated to break up the field even when it was clearly more uniform than target).
        issues.append(("flat_dominant","one flat color >52% — break up the field with mass/texture"))
    if row_var<0.006 and col_var<0.006 and 0.3<fill<0.85:
        issues.append(("uniform",f"even grid (bingo-card) — vary scale + overlap"))
    ok=len(issues)==0
    return dict(ok=ok, fill=round(fill,2), contrast=round(contrast,2),
                quads={k:round(v,2) for k,v in quads.items()}, issues=issues)

def accent_coverage(path, core, tol=30):
    """
    Fraction of the rendered image covered by ANY of the 7 brand accents (core.ACCENTS),
    regardless of which one — distinct from `flat_dominant`, which only fires when a SINGLE
    quantized color exceeds 52% of the canvas.

    DIAGNOSTIC ONLY — manual, like antipattern_scan. NOT wired into `critique`/the auto-gate.
    It was built to catch a real session-9 miss (a filler band colored the same accent as the
    hero card, reading as a flood by eye at 37% coverage — under flat_dominant's 52% trigger).
    But tested against the fix for that exact piece, plus 3 already-shipped, already-approved
    archetype outputs, it reads 0.54 for a LEGITIMATE multi-accent design (a row list where
    each row is a different accent — punctuation via VARIETY, not a flooded field) and only
    0.15-0.29 for the plain hero pieces. Total accent coverage doesn't distinguish "one big
    flooding field" from "many small, differently-colored chips" — the failure mode this was
    meant to catch is about FIELD SIZE/CONTIGUITY (two large blocks sharing a hue), not total
    coverage summed across arbitrarily many small elements. Auto-wiring it as a hard-fail would
    have blocked the very design it was built to validate. Call it by hand, read the number, use
    judgment — don't gate on it until it's rebuilt around connected-component size per accent
    rather than a flat sum (see the note in accent_flood_check).
    tol: per-channel-ish euclidean tolerance for "counts as this accent" (handles anti-aliased
    edges/shadows near a solid accent fill without needing an exact hex match).
    Returns the covered fraction (0..1); caller decides the ceiling (see accent_flood_check).
    """
    im = Image.open(path).convert("RGB")
    arr = np.asarray(im.resize((216, 270))).astype(int)
    accents = [tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) for h in core.ACCENTS]
    flat = arr.reshape(-1, 3)
    covered = np.zeros(len(flat), dtype=bool)
    for ac in accents:
        d = np.abs(flat - np.array(ac)).sum(1)
        covered |= (d < tol * 3)
    return covered.mean()

def accent_flood_check(path, core, max_frac=0.34):
    """
    NOT auto-gate-safe (see accent_coverage's docstring — it false-positives on legitimate
    multi-accent list layouts). Left here as a manual diagnostic for the specific shape it DOES
    catch reliably: two-or-fewer large accent fields sharing a hue. Before trusting a flag from
    this, look at the render — a fail here on a piece with many small differently-colored chips
    (row lists, badge piles) is very likely a false positive, not a real flood.
    TODO (not done): rebuild around per-accent connected-component size (largest contiguous
    same-hue blob as a fraction of canvas) instead of a flat total, which would tell "one huge
    field" apart from "many small pieces" and could then graduate into the real auto-gate.
    Hard-fail wrapper around accent_coverage: total accent presence (summed across however many
    distinct accents are on the piece) must stay near the §9 punctuation ceiling. 0.34 gives a
    little headroom over the documented ~30% target (posters legitimately vary +/- a few points)
    without accepting a genuine flood. Returns [] (pass) or one issue tuple.
    """
    frac = accent_coverage(path, core)
    if frac > max_frac:
        return [("accent_flood", f"accents cover {frac:.2f} of the piece (ceiling {max_frac}) — "
                                  f"accents are punctuation, not a field; swap a filler/band to "
                                  f"ink, cream, or a neutral instead of another accent hue")]
    return []

def report(path,name=""):
    c=critique(path)
    tag="✓ PASS" if c['ok'] else "✗ NEEDS FIX"
    print(f"[preview] {name} {tag} fill={c['fill']} contrast={c['contrast']} quads={c['quads']}")
    for code,msg in c['issues']: print(f"          → {msg}")
    return c
