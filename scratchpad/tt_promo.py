"""TerraThon sports PROMOTION STORIES (Wed 30 Sep): 9 event cards + 1 umbrella = 10 stories, 1080x1920.
Cards per sport: prize | closing (registrations close 1 Oct) | fee (fee and team size). Reflow of the feed poster with Instagram's safe zones.
The photo-based variant the user's sample shows is tt_promo_photo.py (needs the photo files)."""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)

async def main():
    d = "out/collaterals/promo_stories"; os.makedirs(d, exist_ok=True)
    async with tt.B.session():
        for n, ev in tt.EVENTS.items():
            for card in ("prize", "closing", "fee"):
                await tt.build(ev, "LINK IN BIO", f"{d}/{n}_{card}.png", canvas="story", card=card)
    print("done")
if __name__ == "__main__":
    asyncio.run(main())
