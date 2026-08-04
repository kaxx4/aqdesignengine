#!/usr/bin/env python3
"""
Batch reference-convergence pass: for every reference poster in training_samples/reference_posters/,
pick the best-fit ENCODED archetype (number_hero / radial_orbit / giant_type -- no new archetypes),
build AQ-appropriate content, run it through the engine's self-correcting pipeline, and write the
result to out/converge/ with a filename that traces back to the source reference.
"""
import asyncio, os, sys, importlib.util, json
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s=importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
eng = load("engine")
rm = load("ref_metrics")

REF_DIR = "training_samples/reference_posters"
OUT_DIR = "out/converge"
os.makedirs(OUT_DIR, exist_ok=True)

# AQ canonical content bank -- rotate through so each generation is distinct (TASTE variability rule)
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

def pick_archetype(metrics):
    ink, dom, sat, hisat = metrics["ink"], metrics["dom_cov"], metrics["mean_sat"], metrics["hi_sat_frac"]
    if dom > 0.45 and sat > 0.35:
        return "number_hero", "accent"
    if dom > 0.5 and sat < 0.25 and ink < 0.15:
        return "giant_type", "cream"
    if ink > 0.22:
        return "giant_type", "ink"
    return "number_hero", "cream"

async def gen_one(idx, fname):
    path = os.path.join(REF_DIR, fname)
    metrics = rm.analyze(path)
    slug = fname.split(".")[0][:10]
    # round-robin some radial_orbit in for variety regardless of metric fit (radial has no metric proxy test yet)
    if idx % 5 == 0:
        archetype, field = "radial_orbit", None
        content = dict(ORBIT_SETS[(idx // 5) % len(ORBIT_SETS)])
        accent_idx = idx % 7
    elif idx % 3 == 0:
        archetype, field = "giant_type", "ink" if idx % 2 == 0 else "cream"
        word, tags, big, band, body, meta = GIANT_WORDS[idx % len(GIANT_WORDS)]
        content = dict(field=field, meta=meta, word=word, tags=tags, big=big, band=band, body=body, footer="@ngo.aquaterra")
        accent_idx = idx % 7
    else:
        archetype, field = pick_archetype(metrics)
        if archetype == "giant_type":
            word, tags, big, band, body, meta = GIANT_WORDS[idx % len(GIANT_WORDS)]
            content = dict(field=field, meta=meta, word=word, tags=tags, big=big, band=band, body=body, footer="@ngo.aquaterra")
        else:
            number, kicker, label, chips, band, meta = NUMBER_STATS[idx % len(NUMBER_STATS)]
            content = dict(field=field, meta=meta, kicker=kicker, number=number, label=label, chips=chips, band=band,
                           body="", footer="@ngo.aquaterra")
        accent_idx = idx % 7

    name = f"{idx:02d}_{slug}_{archetype}" + (f"_{field}" if field else "")
    rep = await eng.generate(name, archetype, content, accent_idx=accent_idx)
    rep["ref_file"] = fname
    rep["ref_metrics"] = metrics
    rep["archetype"] = archetype
    rep["field"] = field
    os.replace(f"out/{name}.png", os.path.join(OUT_DIR, f"{name}.png"))
    return rep

async def main():
    files = sorted(f for f in os.listdir(REF_DIR) if f.endswith(".jpg"))
    reports = []
    for idx, fname in enumerate(files):
        try:
            rep = await gen_one(idx, fname)
            status = "PASS" if rep.get("final_ok") else "NEEDS-LOOK"
            print(f"[{idx:02d}] {fname[:14]:14} -> {rep['archetype']:13} {status}  fill={rep['iters'][-1]['fill']}")
            reports.append(rep)
        except Exception as e:
            print(f"[{idx:02d}] {fname[:14]:14} -> ERROR {e}")
            reports.append({"ref_file": fname, "error": str(e)})
    with open(os.path.join(OUT_DIR, "manifest.json"), "w") as f:
        json.dump(reports, f, indent=2, default=str)
    print(f"\ndone: {len(files)} samples -> {OUT_DIR}/")

asyncio.run(main())
