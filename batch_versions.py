#!/usr/bin/env python3
"""
Generate a v1 (or next version) for EVERY reference poster in training_samples/reference_posters/,
stored per-sample at out/versions/<slug>/vN.png. Reuses the archetype-fit heuristic from
batch_converge.py, extended to include stacked_zones. Skips samples that already have a v1 unless
--force is passed (so repeated runs add v2/v3 instead of clobbering).
"""
import asyncio, os, sys, importlib.util, json, re
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s=importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
eng = load("engine")
rm = load("ref_metrics")

REF_DIR = "training_samples/reference_posters"
VER_DIR = "out/versions"
os.makedirs(VER_DIR, exist_ok=True)

NUMBER_STATS = [
    ("15k", "we served", '<span style="font-family:var(--s);font-style:italic;text-transform:none;color:var(--tomato)">meals.</span> not<br>numbers.',
     ["one crate at a time","students, not staff"], "every plate had a face.", "welfare · food"),
    ("4k", "we planted", 'trees.<br>real ones.',
     ["dirt under our nails","not a photo op"], "roots don't lie.", "climate · trees"),
    ("3.5k", "we taught", 'kids.<br>for free.',
     ["no classroom needed","peer to peer"], "anyone can teach if they show up.", "education"),
    ("1.5k", "we fed", 'dogs.<br>every week.',
     ["strays get names here","no shelter required"], "the streets are ours too.", "welfare · animals"),
    ("2.5t", "we collected", 'clothes.<br>reworn.',
     ["your closet's loss","zero landfill"], "hand-me-downs, upgraded.", "welfare · clothes"),
    ("1.6k", "we ran", 'free health<br>checkups.',
     ["no insurance needed","students with stethoscopes"], "everyone deserves a checkup.", "welfare · health"),
    ("15k", "we handed out", 'bananas.<br>literally.',
     ["potassium, but make it activism","weirdly specific, very real"], "small fruit, real intent.", "welfare · food"),
    ("534", "we hit", 'drives.<br>documented.',
     ["students, not staff","zero paid staff"], "we don't do quiet wins.", "welfare · food"),
    ("500+", "we ran", 'campaigns.<br>and counting.',
     ["1,200 of us, unhinged","peer pressure but wholesome"], "impact as a side effect.", "everything we do"),
    ("6", "we run", 'departments.<br>no bosses.',
     ["cv? never met her","show up, that's the ask"], "run by literal teenagers.", "welfare · structure"),
]
GIANT_WORDS = [
    ("roots", ["welfare","climate","education"], "deep roots.<br>loud growth.", "grown by teenagers.",
     "a youth movement from one idea: teenagers can run real change.", "est. 2021 · kolkata"),
    ("show up", ["welfare","climate","education"], "no cv.<br>no committee.", "just show up.",
     "impact as a side effect of 1,200 teenagers doing the work.", "est. 2021 · kolkata"),
    ("paradox", ["fundraiser","music","chaos"], "loud room.<br>real cause.", "every ticket funds a drive.",
     "our flagship night -- proceeds straight into the next drive.", "aquaterra presents"),
    ("shikshaq", ["education","tuition","students"], "taught by<br>students.", "learning, peer to peer.",
     "a free tuition platform run by the students who needed it first.", "aquaterra ventures"),
]
ORBIT_SETS = [
    dict(top="one community,", kicker="since 2021", number="534", label="drives",
         big="six ways to<br>show up.", orbit=[("food",3),("trees",1),("books",4),("dogs",0),("clothes",5),("health",6)],
         chips=["pick any. or all six.","no fees, ever"], footer="@ngo.aquaterra -> pick your lane", meta="everything we do"),
    dict(top="what we run,", kicker="6 departments", number="1.2k", label="students",
         big="no bosses.<br>just lanes.", orbit=[("welfare",0),("climate",1),("edu",2),("roots",5),("shiksh",4),("events",6)],
         chips=["pick a lane","no cv needed"], footer="@ngo.aquaterra -> join a lane", meta="est. 2021 · kolkata"),
]
STACKED_SETS = [
    dict(meta="events · timeline", title="our timeline.", kicker_left="since 2021", kicker_right="ongoing",
         rows=[("01","documented drives",1),("04","free health checkups",4),("07","tree plantation runs",2),
               ("11","clothing drives",5),("15","dog feeding rounds",0),("20","meal service days",3)],
         band="more ways to show up.", footer="@ngo.aquaterra"),
    dict(meta="highlights · this month", title="what a month.", kicker_left="highlights", kicker_right="october",
         rows=[("01","promotion drives",1),("07","teva workshop",4),("14","growth tactics talk",2),("23","black friday prep",5)],
         band="", footer="@ngo.aquaterra"),
]

def pick_archetype(metrics):
    ink, dom, sat, hisat = metrics["ink"], metrics["dom_cov"], metrics["mean_sat"], metrics["hi_sat_frac"]
    if dom > 0.55 and sat < 0.20 and ink < 0.20:
        return "stacked_zones", None
    if dom > 0.45 and sat > 0.35:
        return "number_hero", "accent"
    if dom > 0.5 and sat < 0.25 and ink < 0.15:
        return "giant_type", "cream"
    if ink > 0.22:
        return "giant_type", "ink"
    return "number_hero", "cream"

async def gen_one(idx, fname, version):
    path = os.path.join(REF_DIR, fname)
    metrics = rm.analyze(path)
    slug = fname.split(".")[0][:14]
    outdir = os.path.join(VER_DIR, slug)
    os.makedirs(outdir, exist_ok=True)

    if idx % 6 == 0:
        archetype, field = "radial_orbit", None
        content = dict(ORBIT_SETS[(idx // 6) % len(ORBIT_SETS)])
        accent_idx = idx % 7
    elif idx % 5 == 0:
        archetype, field = "stacked_zones", None
        content = dict(STACKED_SETS[(idx // 5) % len(STACKED_SETS)])
        accent_idx = idx % 7
    elif idx % 3 == 0:
        archetype, field = "giant_type", "ink" if idx % 2 == 0 else "cream"
        word, tags, big, band, body, meta = GIANT_WORDS[idx % len(GIANT_WORDS)]
        content = dict(field=field, meta=meta, word=word, tags=tags, big=big, band=band, body=body, footer="@ngo.aquaterra")
        accent_idx = idx % 7
    else:
        archetype, field = pick_archetype(metrics)
        if archetype == "stacked_zones":
            content = dict(STACKED_SETS[idx % len(STACKED_SETS)])
        elif archetype == "giant_type":
            word, tags, big, band, body, meta = GIANT_WORDS[idx % len(GIANT_WORDS)]
            content = dict(field=field, meta=meta, word=word, tags=tags, big=big, band=band, body=body, footer="@ngo.aquaterra")
        else:
            number, kicker, label, chips, band, meta = NUMBER_STATS[idx % len(NUMBER_STATS)]
            content = dict(field=field, meta=meta, kicker=kicker, number=number, label=label, chips=chips, band=band,
                           body="", footer="@ngo.aquaterra")
        accent_idx = idx % 7

    name = f"{slug}_tmp"
    rep = await eng.generate(name, archetype, content, accent_idx=accent_idx)
    dest = os.path.join(outdir, f"v{version}.png")
    os.replace(f"out/{name}.png", dest)
    rep["ref_file"] = fname; rep["archetype"] = archetype; rep["field"] = field; rep["dest"] = dest
    rep["ref_metrics"] = metrics
    return rep

async def main():
    files = sorted(f for f in os.listdir(REF_DIR) if f.endswith(".jpg"))
    reports = []
    for idx, fname in enumerate(files):
        slug = fname.split(".")[0][:14]
        outdir = os.path.join(VER_DIR, slug)
        existing = sorted(f for f in os.listdir(outdir)) if os.path.isdir(outdir) else []
        nums = [int(f[1:-4]) for f in existing if f.startswith("v") and f[1:-4].isdigit()]
        version = (max(nums)+1) if nums else 1
        try:
            rep = await gen_one(idx, fname, version)
            status = "PASS" if rep.get("final_ok") else "NEEDS-LOOK"
            print(f"[{idx:02d}] {fname[:14]:14} -> {rep['archetype']:13} {status} -> {rep['dest']}")
            reports.append(rep)
        except Exception as e:
            print(f"[{idx:02d}] {fname[:14]:14} -> ERROR {e}")
    with open(os.path.join(VER_DIR, "manifest_v1_pass.json"), "w") as f:
        json.dump(reports, f, indent=2, default=str)
    print(f"\ndone: {len(reports)} new v1s written")

asyncio.run(main())
