import os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
spec = importlib.util.spec_from_file_location("layout", os.path.join(ENGINE_DIR, "layout.py"))
layout = importlib.util.module_from_spec(spec); spec.loader.exec_module(layout)

W, H = 1080, 1350
passed = 0
total = 0

def check(name, cond):
    global passed, total
    total += 1
    print(f"{'OK  ' if cond else 'FAIL'} {name}")
    if cond:
        passed += 1

# --- sample 26 shape: a thumbsup doodle dropped directly over a text pill ---
elements = [
    ("volunteer_pill", 200, 900, 400, 90),
    ("thumbsup", 420, 920, 140, 140),   # overlaps the pill by ~120x70
]
hits_before = layout.collision_check(elements)
check("reproduces the sample-26 collision before nudging", len(hits_before) == 1)

nudged, unresolved = layout.collision_nudge(elements, W, H)
check("collision resolved after auto-nudge", len(unresolved) == 0)
check("hero/earlier element (pill) left in place", nudged[0][1:] == elements[0][1:])
check("later element (thumbsup) moved", nudged[1][1:] != elements[1][1:])
nx, ny, nw, nh = nudged[1][1:]
check("nudged element stays on-canvas", 0 <= nx <= W - nw and 0 <= ny <= H - nh)

# --- degenerate case: identical centers must not hang / divide-by-zero ---
same_center = [("a", 500, 500, 100, 100), ("b", 500, 500, 100, 100)]
_, unresolved2 = layout.collision_nudge(same_center, W, H, max_iters=60)
check("identical-center collision still resolves (no infinite loop / crash)", len(unresolved2) == 0)

# --- preflight auto_nudge wiring returns nudged_elements and clears 'collisions' ---
r = layout.preflight(W, H, elements, auto_nudge=True)
check("preflight(auto_nudge=True) clears collisions", r['collisions'] == [])
check("preflight(auto_nudge=True) reports clean", r['clean'] is True)
check("preflight(auto_nudge=True) surfaces nudged_elements", r['nudged_elements'] is not None)

print(f"\n{passed}/{total} passed")
sys.exit(0 if passed == total else 1)
