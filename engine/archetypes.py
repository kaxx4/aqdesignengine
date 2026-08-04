# COMPOSITION ARCHETYPES — the decision layer that was MISSING.
# Every generation must PICK an archetype first. Each has fundamentally different geometry:
# reading axis, focal placement, element flow. This is what makes outcomes variable BY DESIGN (taste),
# not a fixed template with swapped words. Derived from INSPIRATION.md teardowns.
import math, importlib.util
def load(n):
    s=importlib.util.spec_from_file_location(n,f"" + os.path.dirname(os.path.abspath(__file__)) + "/{n}.py"); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core=load("core")
W,H=core.SIZES["feed"]; M=64

# Each archetype = a GEOMETRY GENERATOR that returns slot positions. NOT styling — pure structure.
# The point: the same content placed through different archetypes yields genuinely different posters.

ARCHETYPES = {
 "radial_orbit": {
    "desc": "focal in CENTER, elements ORBIT around it at varied radii/sizes. reading = center-out.",
    "focal": (W//2, int(H*0.42)),
    "reading": "center-out",
    "slots": "orbit",   # positions computed on a circle around focal
 },
 "diagonal_cascade": {
    "desc": "elements step DIAGONALLY top-left to bottom-right. reading = diagonal axis. dynamic.",
    "focal": (int(W*0.3), int(H*0.3)),
    "reading": "diagonal",
    "slots": "diagonal",
 },
 "off_frame_bleed": {
    "desc": "giant word/object BLEEDS off an edge (half-cut), implying scale beyond canvas. tension.",
    "focal": (int(W*0.6), int(H*0.4)),
    "reading": "edge-anchored",
    "slots": "bleed",
 },
 "stacked_zones": {
    "desc": "horizontal BANDS/zones stacked, each a different color/pattern block. reading = top-down strata.",
    "focal": (M, int(H*0.35)),
    "reading": "top-down",
    "slots": "bands",
 },
 "scatter_collage": {
    "desc": "angled CARDS/objects scattered like flyers, Z-pattern flow, no single hero. density.",
    "focal": None,
    "reading": "z-pattern",
    "slots": "scatter",
 },
 "giant_type_hero": {
    "desc": "ONE huge word fills the whole frame; everything else nests INTO the letters. type IS the image.",
    "focal": (W//2, int(H*0.45)),
    "reading": "typographic",
    "slots": "in-type",
 },
 "isometric_grid": {
    "desc": "3D extruded tiles/keycaps on a graph grid, separated, shared light. clean dimensional depth.",
    "focal": (W//2, int(H*0.35)),
    "reading": "scan",
    "slots": "iso",
 },
 "corner_anchor": {
    "desc": "focal pinned to ONE corner, negative space diagonal opposite. asymmetric-balanced minimal.",
    "focal": (int(W*0.68), int(H*0.7)),
    "reading": "corner-diagonal",
    "slots": "corner",
 },
}

def orbit_positions(focal, n, r_base=300, r_var=90):
    """positions on a ring around focal, varied radius, for radial_orbit."""
    cx,cy=focal; out=[]
    for i in range(n):
        ang=(i/n)*2*math.pi - math.pi/2
        r=r_base + (r_var if i%2 else -r_var)
        x=int(cx + r*math.cos(ang)); y=int(cy + r*math.sin(ang))
        out.append((x,y,ang))
    return out

def diagonal_positions(n, x0=M, y0=200, dx=140, dy=170):
    return [(x0+i*dx, y0+i*dy) for i in range(n)]

def pick_variation(seed):
    """A deterministic 'taste' cascade: from a seed, choose a coherent SET of decisions
    (archetype + base-mode + accent-scheme + type-treatment) that hang together — intentional, not random."""
    import random; rng=random.Random(seed)
    arch=rng.choice(list(ARCHETYPES.keys()))
    base=rng.choice(["cream","ink","accent-field","photo","muted"])
    # coherence rules: some combos are better — encode taste, not pure random
    accent_scheme=rng.choice(["mono-pop","duo","triad","rainbow-letter"])
    type_treat=rng.choice(["clean-bold","serif-accent","sticker-label","per-letter","outline"])
    reading=ARCHETYPES[arch]["reading"]
    return dict(archetype=arch, base=base, accent_scheme=accent_scheme, type_treat=type_treat, reading=reading)

if __name__=="__main__":
    print("ARCHETYPE MENU (each = different geometry):\n")
    for k,v in ARCHETYPES.items():
        print(f"  {k:18} [{v['reading']:14}] {v['desc']}")
    print("\nSAMPLE TASTE CASCADES (seeded, coherent decision sets):")
    for s in range(6):
        d=pick_variation(s)
        print(f"  seed {s}: {d['archetype']:16} base={d['base']:11} accents={d['accent_scheme']:12} type={d['type_treat']}")
