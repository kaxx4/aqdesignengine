"""Snapshot every launch-pack mask's placement (the <img data-tag="mask"> style, base64 stripped) so a later change can prove the mask did not move.
Run:  python scratchpad/mask_snapshot.py <out.json>   (writes the snapshot)   |   python scratchpad/mask_snapshot.py <ref.json> --check
"""
import importlib.util, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
FACTS = dict(edition="Masquerade Sangeet Edition", date="10th November, 2026", time="4:30 PM Onwards", status="Ticket sales open soon", note="More details to follow")
STORIES = [("03","foil","classic","copper"),("05","outline","mask_hero","copper"),("12","editorial","mask_behind","copper"),("06","stack","classic","copper"),
           ("09","foil","mask_hero","copper"),("11","outline","classic","asset"),("07","editorial","mask_behind","copper"),("13","stack","mask_hero","copper"),
           ("08","foil","mask_behind","copper"),("10","outline","classic","asset" if False else "copper")]
def snap():
    out = {}
    for i, (ph, ty, lay, mk) in enumerate(STORIES, 1):
        h = dd.Poster("story_launch", dict(FACTS, photo=ph), "story", style="photo", mask=mk, typo=ty, layout=lay).build()
        m = re.search(r'<img src="[^"]*" data-tag="mask" style="([^"]*)"', h)
        out[f"story_{i:02d}"] = m.group(1) if m else None
    h = dd.Poster("wa_poster", dict(FACTS, photo="05"), "feed", style="photo", mask="copper", typo="foil").build()
    out["wa_poster"] = re.search(r'<img src="[^"]*" data-tag="mask" style="([^"]*)"', h).group(1)
    h = dd.Poster("wa_dp", dict(edition=FACTS["edition"], date=FACTS["date"]), "square", style="plate", mask="copper").build()
    out["wa_dp"] = re.search(r'<img src="[^"]*" data-tag="mask" style="([^"]*)"', h).group(1)
    return out
if __name__ == "__main__":
    if "--check" in sys.argv:
        ref = json.load(open(sys.argv[1])); now = snap()
        moved = [k for k in ref if ref[k] != now.get(k)]
        print("MASK MOVED in:", moved) if moved else print(f"mask placement identical in all {len(ref)} pieces")
        sys.exit(1 if moved else 0)
    json.dump(snap(), open(sys.argv[1], "w"), indent=1); print("snapshot written", sys.argv[1])
