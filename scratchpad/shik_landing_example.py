"""WORKED EXAMPLE: the board-exam-season landing page, built ONLY from engine/shikshaq.py.

This is the page designed in the learning session, now assembled from the module's builders so
the next Shikshaq page starts here instead of from a blank file. Every figure is a sk.FACTS value.
Run:  PYTHONIOENCODING=utf-8 python scratchpad/shik_landing_example.py
"""
import os, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
import shikshaq as sk

F = sk.FACTS
P = sk.need("papers")   # asked each time (owner ruling 2026-11-27): export SHIKSHAQ_PAPERS=N after asking
st, bt = F["subject_teachers"], F["board_teachers"]
sp = F["sample_papers"]

copy = ["That paper you keep avoiding?", "Read it today.", "Every board, every class.",
        "Free past papers: ICSE, CBSE and ISC, read as questions with marks, chapters and figures. The first two questions need no account.",
        "Tell us the subject", "Subject, class and your area. Three taps, no account needed.",
        "No fees, no middleman, no commission.", "We list teachers, verify who they say they are, then get out of the way.",
        f"{F['teachers']} verified teachers listed", f"{P} past papers, free to read", "Class 10 Maths"]
errs, warns = sk.copy_gate(copy)
assert not errs, errs

body = (
    sk.nav()
    + sk.hero("Board exams · ICSE, CBSE, ISC", "That paper you keep avoiding?", "Read it today.",
              counts=[(f"Chemistry · {st['Chemistry']}", "Chemistry"), (f"Hindi · {st['Hindi']}", "Hindi"),
                      (f"English · {st['English']}", "English"), (f"Maths · {st['Maths']}", "Maths")],
              quick=["Class 10", "Maths", "Under ₹800", "Home tuition"])
    + sk.category_section("02", "Or go straight", "to the subject", "Every board, every class.",
                          [("Maths", f"{st['Maths']} teachers"), ("English", f"{st['English']} teachers"),
                           ("Hindi", f"{st['Hindi']} teachers"), ("Chemistry", f"{st['Chemistry']} teachers")],
                          [("ICSE", f"{bt['ICSE']} teachers", "orange"), ("CBSE", f"{bt['CBSE']} teachers", "indigo"),
                           ("IGCSE", f"{bt['IGCSE']} teachers", "dark"), ("IB", f"{bt['IB']} teachers", "muted"),
                           ("State", f"{bt['State']} teachers", "muted")])
    + sk.papers_slab("03", "the boards set", copy[3], "Browse past papers",
                     [sk.cover("Maths", f"ICSE · {sp[0]['year']}", f"Class {sp[0]['cls']}", f"Board · {sp[0]['questions']} questions"),
                      sk.cover("Maths", f"ISC · {sp[1]['year']}", f"Class {sp[1]['cls']}", f"Board · {sp[1]['questions']} questions"),
                      sk.cover("Maths", f"ISC · {sp[2]['year']}", f"Class {sp[2]['cls']}", f"Board · {sp[2]['questions']} questions")])
    + sk.steps_slab("04 · Two minutes, start to finish", "Then talk to them yourself",
                    [("search", "Tell us the subject", copy[5]),
                     ("people", "Compare real profiles", "Rates, boards, reviews and travel radius, all on one card."),
                     ("chat", "Message on WhatsApp", "Talk to the teacher directly. Shikshaq never sits in the middle.")],
                    copy[6])
    + sk.stats_section("05", "No commission.", sk.mark("Ever."), copy[7],
                       [(F["teachers"], "verified teachers listed", "teachers"), (P, "past papers, free to read", "papers"),
                        ("₹0", "commission taken from a fee", "mint")])
    + sk.eyes_section("Still deciding?", "We’re watching out for you.", "Fill in the blanks and we’ll take you straight there.",
                      f"Show {F['teachers']} teachers")
    + sk.footer("Shikshaq is " + sk.emph("verified teachers") + " in Kolkata, and " + sk.emph("past papers") + ".",
                small="Free to search, free to contact. We never sell your number.")
    + sk.EYES_JS
)

async def main():
    async with sk.session() as s:
        html = sk.doc(body, kind="page", title="Board exam season | Shikshaq")
        r1 = await s.render(html, "out/shikshaq/landing-m.png", 390, 844, kind="page", scale=2, name="landing-m")
        r2 = await s.render(html, "out/shikshaq/landing-d.png", 1280, 800, kind="page", name="landing-d")
        return r1, r2

if __name__ == "__main__":
    import asyncio
    a, b = asyncio.run(main())
    print("CLEAN" if a.clean and b.clean else "NOT CLEAN")
