# Campaign plan: "What Shikshaq actually is" (WhatsApp Status, multi-post)

Status: PLAN, not yet generated. Nothing here is built until the open questions at the bottom are answered.

## 1. The problem, stated precisely

Interviewees (2026-10-06) said Shikshaq is a platform that teaches underprivileged students. It is a platform that connects families with tutors across Kolkata.

Likely cause (inference, not fact): Shikshaq is made by AquaTerra, an NGO. People carry the NGO frame into the product. The word "Shikshaq" also sounds like a class or a school. Both push the same reading: charity education.

The misconception costs us on both sides of the marketplace:
- **Parents** who assume it is not for them never search for a tutor.
- **Tutors** who assume it is a volunteer or charity-teaching gig never list.

## 2. One-line definition (the thing every asset must make true)

> **Shikshaq is where Kolkata families find tutors.**

Working variants, same meaning, pick one per slide: "Find a tutor near you." "Tutors in Kolkata, in one place." "Parents search. Tutors list. They talk directly."

## 3. Strategy: define first, bust second

A myth-buster that opens with "Shikshaq is NOT for underprivileged students" repeats the wrong frame as its first words. People remember the frame, not the "not". So:

1. Open with the positive definition and a concrete scene (a parent, a tutor, a search).
2. Show how it works in three steps.
3. Only then, one dedicated slide names the misunderstanding and corrects it in plain words.
4. Close with an action for each audience.

This is the one reframe I would push on. The default instinct is a "myth vs fact" poster. I recommend the myth slide sits at position 4 of 6, never first.

## 4. Audiences and split

| Audience | What they believe | What they must believe after | Action |
|---|---|---|---|
| Parents / students (primary) | "This is charity classes" | "I can find a tutor here, it is for anyone" | Search a tutor at shikshaq.in |
| Tutors (secondary) | "This is volunteering" | "I get a profile and students come to me" | Make a profile |

The WhatsApp Status run carries both, but each slide is addressed to one audience. Do not mix a parent line and a tutor line on one slide.

## 5. Slide sequence (6 Status slides, 1080x1920 story canvas)

| # | Role | Message | Audience |
|---|---|---|---|
| 1 | Hook | "Looking for a tutor in Kolkata?" Large question, logo, no explanation yet. | Parents |
| 2 | Definition | "Shikshaq connects families with tutors across Kolkata." The one-line definition as the hero. | Both |
| 3 | How it works | Three steps: search by subject, class and area; view the tutor's profile; talk to them directly. Steps must match the real product flow. | Parents |
| 4 | The correction | "Not a charity. Not a classroom. A directory of tutors that anyone in Kolkata can use." Names the misreading once, answers it. | Both |
| 5 | Tutor side | "Teach? Put your profile where families are searching." | Tutors |
| 6 | CTA | shikshaq.in, one action, plus "forward this to a parent who is hunting for a tutor". | Both |

Cadence: post slides 1 to 3 on day 1, slide 4 on day 2, slides 5 to 6 on day 3, then repeat the sequence once the following week. A Status expires after 24 hours, so slide groups need to stand alone if someone sees only one. Slide 2 and slide 4 each carry the full definition for that reason.

## 6. Companion message (WhatsApp broadcast, forwardable)

One short text sent to contacts and groups, drafted in AQ voice using the `aq-event-messaging` skill. Structure: one sentence defining Shikshaq, one sentence on how to use it, link. Written to be forwarded by a parent to another parent without edits.

## 7. Facts policy (hard rules)

- No digit ships unless it traces to a source. The copy gate in `src/validate.mjs` enforces this for the weekly engine; the same standard applies here by hand.
- Safe, recorded constants: Kolkata; classes IV to XII; ICSE, ISC, CBSE; two free question previews; zero commission; shikshaq.in.
- Do NOT use "147 teachers" as a live claim. The sample file marks it as an application count and unverified. A live figure needs `fetch-facts.mjs` against production, which has not been run yet.
- Research figures from `AQ_FACTS.md` (n=80 survey, 85% hired without verification, 11 days to under 48 hours) are sourced to internal documents. Allowed only if you confirm they are publishable.
- No "thousands", "trusted by", "best tutors", "verified" unless verification is actually true for the tutors shown.
- No fabricated tutor photos or testimonials. If we show a profile card, it is a clearly generic UI mock-up built from the real product fields, or a real consenting tutor.

## 8. Design approach

- Brand: Shikshaq, not AQ. Use the Shikshaq tokens, bone ground, accent colours, Archivo and Geist fonts in `addons/shikshaq/`. No AQ cream and no AQ doodles.
- Canvas: 1080x1920. The Shikshaq renderer is currently built for 1080x1350 feed posts, so this needs either a story canvas option in `src/render.mjs` or a bespoke render using the same tokens and gate. I would extend the renderer once, then reuse it.
- Look: one big sentence per slide, one slab of saturated colour at most two fills per poster (existing rule), mascot blobs used sparingly. Slide 4 gets the strongest visual treatment because it is the whole point.
- Gates: copy gate, layout gate (WCAG per element, collisions), then the looking gate on every PNG.
- Companion art piece: the repo rule requires a `/canvas-design` run alongside engine output. It will run after the slides are generated.

## 9. Success check

We cannot measure comprehension from Status views alone. Cheapest honest test: after the run, ask the same five or six people from today's interviews, "What is Shikshaq?" and compare answers. Optional second signal: new tutor profiles and new searches the week of the run versus the week before, read from production.

## 10. Open questions (needed before generating)

1. **Is the product claim accurate as I wrote it?** Parents search by subject, class and area, view a profile and contact the tutor directly, no payment through the platform. Please confirm the real flow, because slide 3 must match it.
2. **Is the product also for question papers?** The addon plans papers posts (Mon, Sat). Should this campaign mention papers, or stay on tutors only? I recommend tutors only: a second message dilutes the correction.
3. **Primary audience:** parents only, or parents and tutors both as planned?
4. **Which facts may I show?** Any live counts you can confirm, and whether verification or "zero commission" can be stated.
5. **Can the AquaTerra link appear?** Do you want slide 4 to say "built by a student-run NGO" to own the origin, or leave AquaTerra off? Owning it may reduce the confusion; hiding it may leave the question open.
6. **Language:** English only, or English with Bengali or Hinglish lines for Kolkata parents? Bengali needs a font check before I commit.
7. **Where does it run:** WhatsApp Status only, or also group posts and Instagram stories? Same canvas works for Status and stories.
8. **Slide count and timing:** is six slides over three days right, or do you want a tighter run?
