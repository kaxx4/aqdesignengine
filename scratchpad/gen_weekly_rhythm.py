import asyncio, os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
eng = load("engine")

content = dict(
    meta="aquaterra · weekly rhythm",
    title="this week,<br>on the ground.",
    kicker_left="pick a day.",
    kicker_right="ongoing",
    rows=[
        ("MON", "food distribution", 0),
        ("WED", "education circle", 4),
        ("FRI", "tree planting", 1),
        ("SAT", "health camp", 3),
    ],
    band="same city. same kids.<br>every week.",
    footer="@ngo.aquaterra",
)

async def main():
    os.makedirs("out", exist_ok=True)
    rep = await eng.generate("weekly_rhythm", "stacked_zones", content, accent_idx=5)
    status = "PASS" if rep.get("final_ok") else "NEEDS-LOOK"
    print(f"[weekly_rhythm] stacked_zones {status} fill={rep['iters'][-1]['fill']} -> out/weekly_rhythm.png")

asyncio.run(main())
