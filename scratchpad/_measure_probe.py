import asyncio, os, sys, importlib.util
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
B = load("build")

async def main():
    items = [
        dict(text="291", font="d", weight=900, size=300, transform="none"),
        dict(text="WORKSHOPS", font="d", weight=900, size=100, letter_spacing="-0.01em", transform="uppercase"),
        dict(text="SINCE 2021", font="m", weight=700, size=34, letter_spacing="0.08em", transform="uppercase"),
        dict(text="HANDS-ON", font="d", weight=900, size=40, transform="uppercase"),
        dict(text="LEARNING", font="d", weight=900, size=40, transform="uppercase"),
        dict(text="labs, not lectures", font="e", weight=600, size=30),
    ]
    res = await B.measure_text(items, 1080, 1080)
    for it, r in zip(items, res):
        print(it["text"], "size", it["size"], "->", r)

asyncio.run(main())
