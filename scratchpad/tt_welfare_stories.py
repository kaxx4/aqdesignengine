"""TerraThon-look WELFARE IMPACT stories, v2 (2026-10-19): cover + 2 overview slides + one data slide per welfare pillar + close, feed 1080x1350 AND story 1080x1920.
Workflow C on the TerraThon format, reusing tt_carousel.py (black ground, tilted slab with orchid border, shuriken, kit stickers, StretchPro cover title).
v2 is data-first: every pillar slab holds a headline, THREE big-number blocks and one short line, over a real photo (user-supplied) in the circle.

Where each number comes from (never mix them silently):
  TABLE  = the user's pasted 558-row project table (scratchpad/welfare_projects_2026-10-19.psv, counted by tt_welfare_stats.py). The pillar a row falls under is a
           keyword mapping by title/category, so a pillar count is "projects logged under this pillar", not an audited total. Volunteers are TURNOUTS, not people.
  SITE   = the user's AquaTerra directory page text (2026-10-19): 4,000+ saplings planted, 3,500+ kids reached, 8 Sundarbans trips, 15,000+ bananas distributed.
           Printed with the page's own "+" and never re-derived.
NOT used: the directory's "582+ drives, blogs & openings" (it counts blogs and openings too, so it is not a drive count). NOT claimed: people helped, rupees, or
any activity the table has no row for (cleanups, blankets, water bowls, tuition appear in the user's scope list but have no row, so they are not named).
Photos (user-supplied, git-ignored in engine/assets/terrathon/carousel_photos/, people incl. minors: confirm consent): children = repo Sundarbans classroom shot,
health (a third-party banner's address and phone are blurred), community, women, elderly, environment, animals. A slide falls back to a kit sticker if its file is absent.
Run: PYTHONIOENCODING=utf-8 python scratchpad/tt_welfare_stories.py [feed story]
"""
import asyncio, base64, importlib.util, io, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
tc = _load("tt_carousel", "scratchpad/tt_carousel.py")
st = _load("tt_welfare_stats", "scratchpad/tt_welfare_stats.py")
from PIL import Image

edu = Image.open("engine/assets/img/education-sundarban.jpeg"); ew, eh = edu.size
def uri(path, w=900, crop=None):
    im = Image.open(path).convert("RGB")
    if crop: im = im.crop(crop)
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)))
    b = io.BytesIO(); im.save(b, "JPEG", quality=86); return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
PD = "engine/assets/terrathon/carousel_photos/"
PHOTOS = {"children": [(uri("engine/assets/img/education-sundarban.jpeg", crop=(0, 0, ew, int(eh * 0.72))), "50% 30%")]}
for key in ("health", "women", "elderly", "community", "environment", "animals"):
    if os.path.exists(f"{PD}{key}_welfare.jpg"): PHOTOS[key] = [(uri(f"{PD}{key}_welfare.jpg", w=1200), "50% 50%")]
tc.photo_list = lambda key: PHOTOS.get(key, [])

P = {p: st.pstat(p) for p in st.PILLARS}
rows = lambda p, pat: sum(1 for r in P[p]["rows"] if re.search(pat, r["title"]))
plant = sum(1 for r in st.ROWS if r["cat"] == "PD")
tails_max = max(int(m.group(1)) for r in st.ROWS for m in [re.match(r"Tails and Treats (\d+)\.0", r["title"])] if m)
first_visit = min(r["year"] for r in P["elderly"]["rows"])
fmt = lambda n: f"{n:,}"
tc.DATE, tc.VENUE = "2021 TO 2026", f"{st.N} PROJECTS LOGGED"

ITEMS = [   # key, headline, short line under the stats (DRAFT copy), sticker (used only where no photo), recolour
    ("all_a", "THE NUMBERS", "ALL DOCUMENTED SINCE 2021.", "carnival.png", False),
    ("all_b", "AND KEEP COUNTING", "EVERY ONE OF THEM SHOWED UP.", "smiley.png", False),
    ("children", "CHILDREN + EDUCATION", "ART, ENGLISH AND BOOKS.", "smiley.png", False),
    ("health", "HEALTHCARE", "PLUS A MEDICAL CAMP IN THE SUNDARBANS.", "smiley.png", True),
    ("women", "WOMEN EMPOWERMENT", "PERIOD TALK. PADS. MONEY SKILLS.", "flower.png", True),
    ("elderly", "ELDERLY", "SOMEONE SHOWED UP.", "flower.png", False),
    ("community", "COMMUNITY WELFARE", "FOOD. CLOTHES. BOOKS. SHARBAT. TOYS.", "carnival.png", False),
    ("environment", "ENVIRONMENT", "ZERO EXCUSES.", "flower.png", True),
    ("animals", "ANIMAL WELFARE", "DINNER FOR STRAYS.", "smiley.png", False),
]
STATS = {
    "all_a": [(fmt(st.N), "PROJECTS LOGGED"), ("3,500+", "KIDS REACHED"), ("4,000+", "SAPLINGS PLANTED")],
    "all_b": [("15,000+", "BANANAS DISTRIBUTED"), ("8", "SUNDARBANS TRIPS"), (fmt(st.VOLS), "VOLUNTEER TURNOUTS")],
    "children": [(fmt(P["children"]["n"]), "PROJECTS"), ("3,500+", "KIDS REACHED"), (fmt(P["children"]["vol"]), "VOLUNTEER TURNOUTS")],
    "health": [(fmt(P["health"]["n"]), "PROJECTS"), (str(rows("health", r"Dental|Tooth|Say Cheese")), "DENTAL CAMPS"), (str(rows("health", r"One Drop")), "BLOOD DONATION DRIVE")],
    "women": [(fmt(P["women"]["n"]), "PROJECTS"), (str(rows("women", r"Menstrual|Breaking the Cycle|Body Basics|Comfort Kits|Cycle of Care")), "PERIOD AND PAD PROJECTS"),
              (str(rows("women", r"Budget Basics|Money Talks|Finance for All")), "MONEY SKILLS WORKSHOPS")],
    "elderly": [(fmt(P["elderly"]["n"]), "OLD AGE HOME VISITS"), (fmt(P["elderly"]["vol"]), "VOLUNTEER TURNOUTS"), (str(first_visit), "VISITING SINCE")],
    "community": [(fmt(P["community"]["n"]), "DRIVES"), ("15,000+", "BANANAS DISTRIBUTED"), (fmt(P["community"]["vol"]), "VOLUNTEER TURNOUTS")],
    "environment": [(fmt(P["environment"]["n"]), "PROJECTS"), ("4,000+", "SAPLINGS PLANTED"), (str(plant), "PLANTATION DRIVES")],
    "animals": [(fmt(P["animals"]["n"]), "DRIVES"), (str(tails_max), "TAILS AND TREATS EDITIONS"), (fmt(P["animals"]["vol"]), "VOLUNTEER TURNOUTS")],
}
LAYOUT = {   # taller slab for the stat row, circle sized to the room above it; the strip and footer keep their own bands
    "feed": dict(hero_max=(720, 560), slab_top=668, slab_h=470, D=560, SX=90, SW=900, strip_y=1156),
    "story": dict(hero_max=(800, 700), slab_top=944, slab_h=500, D=700, SX=90, SW=900, strip_y=1482),
}
tc.DECKS["welfare"] = dict(items=ITEMS, stats=STATS, layout=LAYOUT, num_skip=2, head=("WHAT WE DO", "SEVEN WAYS WE SHOW UP"), swipe="SWIPE FOR THE PROOF", head_w=770,
                           num=True, free_sub=True, compact=True, pill="AQUATERRA", cover_titles=("AQUATERRA", "IMPAACT"),
                           cover_sub=f"{st.N} PROJECTS. {st.VOLS:,} TURNOUTS.", close=("COME TO", "THE NEXT ONE", "@NGO.AQUATERRA"))
if __name__ == "__main__":
    cvs = [a for a in sys.argv[1:] if a in ("feed", "story")] or ["feed", "story"]
    asyncio.run(tc.main(cvs, ("welfare",)))
