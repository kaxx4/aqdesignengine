"""TerraThon-look WELFARE IMPACT stories (2026-10-19): cover + one slide per welfare pillar + close, feed 1080x1350 AND story 1080x1920.
Workflow C on the TerraThon format, reusing tt_carousel.py (black ground, tilted slab with orchid border, shuriken, kit stickers, StretchPro cover title).

Pillars and their one-line scope are the USER's (2026-10-19). Every NUMBER is counted from the user's pasted project table (558 rows, transcribed in
scratchpad/welfare_projects_2026-10-19.psv, counted by tt_welfare_stats.py); the pillar a row falls under is a keyword mapping by title/category, so a
count is "projects logged under this pillar", not an audited total. Volunteers are TURNOUTS (the qualifier travels with the number, VOICE.md sec 2).
NOT claimed: people helped, beneficiaries, rupees, or any activity the table has no row for (cleanups, blankets, bananas, water bowls, tuition appear in
the user's scope list but have no row, so no number is printed for them and they are not named on a slide).
Adaptations (CLAUDE.md sec 2 rule 4): kit stickers stand in for photos except Children (the repo's real Sundarbans classroom photo); fest pill reads
AQUATERRA, not TERRATHON, because this is all of AQ's work, not the fest; footer CTA is the carousel's fixed ALL FOR CHARITY.
Run: PYTHONIOENCODING=utf-8 python scratchpad/tt_welfare_stories.py [feed story]
"""
import asyncio, base64, importlib.util, io, os, sys
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
PHOTOS = {"children": [(uri("engine/assets/img/education-sundarban.jpeg", crop=(0, 0, ew, int(eh * 0.72))), "50% 30%")]}
ELD = "engine/assets/terrathon/carousel_photos/elderly_welfare.jpg"      # user-supplied old age home photo (git-ignored: people, public repo); the pillar keeps its sticker if the file is absent
if os.path.exists(ELD): PHOTOS["elderly"] = [(uri(ELD, w=1200), "50% 40%")]
ANI = "engine/assets/terrathon/carousel_photos/animals_welfare.jpg"      # user-supplied feeding-drive photo (a minor's face; git-ignored); sticker fallback if absent
if os.path.exists(ANI): PHOTOS["animals"] = [(uri(ANI, w=1200), "50% 50%")]
ENV = "engine/assets/terrathon/carousel_photos/environment_welfare.jpg"  # user-supplied plantation photo (face hidden by a cap; git-ignored); sticker fallback if absent
if os.path.exists(ENV): PHOTOS["environment"] = [(uri(ENV, w=1200), "50% 50%")]
HLT = "engine/assets/terrathon/carousel_photos/health_welfare.jpg"       # user-supplied health camp photo (git-ignored); the banner phone number behind them is blurred; sticker fallback if absent
if os.path.exists(HLT): PHOTOS["health"] = [(uri(HLT, w=1200), "50% 40%")]
COM = "engine/assets/terrathon/carousel_photos/community_welfare.jpg"    # user-supplied donation-drive photo (minors; git-ignored); sticker fallback if absent
if os.path.exists(COM): PHOTOS["community"] = [(uri(COM, w=1200), "50% 50%")]
WOM = "engine/assets/terrathon/carousel_photos/women_welfare.jpg"        # user-supplied menstrual hygiene workshop photo (git-ignored); sticker fallback if absent
if os.path.exists(WOM): PHOTOS["women"] = [(uri(WOM, w=1200), "50% 45%")]
tc.photo_list = lambda key: PHOTOS.get(key, [])

P = {p: st.pstat(p) for p in st.PILLARS}
plant = sum(1 for r in st.ROWS if r["cat"] == "PD")
tc.DATE, tc.VENUE = "2021 TO 2026", f"{st.N} PROJECTS LOGGED"
ITEMS = [   # key, headline, tagline (DRAFT copy), sticker, recolour
    ("children", "CHILDREN + EDUCATION", f"{P['children']['n']} PROJECTS. ART, ENGLISH AND BOOKS. NO HOMEWORK GUILT.", "smiley.png", False),
    ("health", "HEALTHCARE", f"{P['health']['n']} PROJECTS. CAMPS, CHECKUPS AND MIND MATTERS.", "smiley.png", True),
    ("women", "WOMEN EMPOWERMENT", f"{P['women']['n']} PROJECTS. PERIOD TALK, PADS AND MONEY SKILLS.", "flower.png", True),
    ("elderly", "ELDERLY", f"{P['elderly']['n']} OLD AGE HOME VISITS. SOMEONE SHOWED UP.", "flower.png", False),
    ("community", "COMMUNITY WELFARE", f"{P['community']['n']} DRIVES. FOOD, CLOTHES, BOOKS, SHARBAT. ALL FREE.", "carnival.png", False),
    ("environment", "ENVIRONMENT", f"{P['environment']['n']} PROJECTS. {plant} PLANTATION DRIVES. ZERO EXCUSES.", "flower.png", True),
    ("animals", "ANIMAL WELFARE", f"{P['animals']['n']} DRIVES. DINNER FOR STRAYS. BELLY RUBS INCLUDED.", "smiley.png", False),
]
tc.DECKS["welfare"] = dict(items=ITEMS, head=("WHAT WE DO", "SEVEN WAYS WE SHOW UP"), swipe="SWIPE FOR THE SEVEN", head_w=770, num=True, free_sub=True, compact=True,
                           pill="AQUATERRA", cover_titles=("AQUATERRA", "IMPAACT"), cover_sub=f"{st.N} PROJECTS. {st.VOLS:,} TURNOUTS.",
                           close=("COME TO", "THE NEXT ONE", "@NGO.AQUATERRA"))
if __name__ == "__main__":
    cvs = [a for a in sys.argv[1:] if a in ("feed", "story")] or ["feed", "story"]
    asyncio.run(tc.main(cvs, ("welfare",)))
