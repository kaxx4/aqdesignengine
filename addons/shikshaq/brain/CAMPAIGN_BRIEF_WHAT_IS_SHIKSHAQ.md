# CAMPAIGN BRIEF: "Shikshaq, in one line"

Brand: Shikshaq (not AquaTerra). Owner: AQ marketing. Drafted 2026-10-06.
Supersedes the short plan in `CAMPAIGN_WHATSAPP_WHAT_IS_SHIKSHAQ.md`. That file stays as the origin note.
Status: BRIEF. No collateral is generated yet. Items marked **[CONFIRM]** are assumptions I made so the brief is usable now. Overrule any of them and the affected assets update.

---

## 1. Why this campaign exists

### 1.1 The finding
In today's interviews, almost every respondent described Shikshaq as a platform that teaches underprivileged students. It is a platform that connects families with tutors across Kolkata.

### 1.2 Why people misread it (inference, not fact)
1. **Parentage.** AquaTerra, an NGO, builds Shikshaq. People carry the NGO frame (charity, teaching the underserved) into the product.
2. **The name.** "Shikshaq" sounds like a class, a school or a programme, not a directory.
3. **The missing verb.** Nothing people see today says "find", "search" or "tutor" in the first two seconds.

Treat 1 to 3 as hypotheses. Test them in the follow-up check in section 12 before the second week of the run.

### 1.3 What the misreading costs
- **Parents** who think "this is not for me" never search. We lose demand.
- **Tutors** who think "this is volunteer or charity teaching" never list. We lose supply.
- **Both sides** repeat the wrong description to the next person. The misreading spreads by word of mouth, which is also our best channel, so it works against us.

### 1.4 The job
Make one sentence true in the head of every Kolkata parent and tutor who sees our content:

> **Shikshaq is where Kolkata families find tutors.**

If a piece does not move someone toward that sentence, it does not ship.

---

## 2. Objectives and how we judge them

| # | Objective | Measure | Target |
|---|---|---|---|
| O1 | People describe Shikshaq correctly | Re-ask today's interviewees "what is Shikshaq?" one week after the run, plus a story poll | Set the target after the baseline. I suggest "most can say find or connect a tutor" **[CONFIRM]** |
| O2 | Parents try it | Tutor searches on shikshaq.in, week of run vs the week before | Direction up. Number set after we read the baseline |
| O3 | Tutors list | New tutor profiles started and completed, same comparison | Direction up |
| O4 | The message travels | Forwards and replies on the WhatsApp broadcast, Status views, Instagram shares and saves | Report counts. No target without a baseline |

I will not invent numeric targets. We have no recorded baseline for searches, profiles or Status views. The first job of week 1 is to read production for those numbers.

---

## 3. Audiences

### 3.1 Primary: parents of school students in Kolkata
- Classes IV to XII, ICSE, ISC and CBSE (recorded constants).
- They need a tutor now or soon. Their current method is asking friends, school notice boards and word of mouth.
- Their belief to remove: "Shikshaq is charity classes for other people's children."
- Their belief to install: "Shikshaq is where I search for a tutor near me."
- Channel: WhatsApp (groups, Status, forwards), Instagram.

### 3.2 Secondary: tutors and teachers in Kolkata
- Independent tutors, college students who tutor, retired teachers.
- Belief to remove: "this is volunteer teaching for an NGO."
- Belief to install: "I get a profile, families search for me, they contact me directly."
- Channel: WhatsApp, Instagram, tutor-to-tutor forwarding, college campuses.

### 3.3 Tertiary: the people who shape talk about us
Volunteers, AQ members, school contacts, partner NGOs. They describe Shikshaq in conversation. Give them a one-line script and a forwardable asset (series F).

### 3.4 Not an audience
Donors, sponsors and CSR contacts. Do not blend an NGO-impact message into this run. That is the exact blur we are removing.

---

## 4. Strategy

### 4.1 The core move: define first, correct second
A poster that opens "Shikshaq is NOT for underprivileged students" repeats the wrong frame as its first words, and people remember the frame rather than the "not". The correction therefore never leads. Every series opens with the positive definition and a concrete scene. The correction appears as one beat inside a sequence, never as the headline of a first impression. Series A (the misreads) is the exception and I explain the guard rails in 6.1.

### 4.2 Message hierarchy
1. **Say it:** Shikshaq connects families with tutors in Kolkata.
2. **Show it:** the search, the profile, the direct contact. Real product fields, no invented screens.
3. **Correct it:** it is not a charity and not a class. One plain sentence.
4. **Prove it:** real tutors and real parent questions answered, with consent and sources.
5. **Ask for one action:** parents search, tutors list, everyone forwards.

### 4.3 Origin story: own it or hide it? **[CONFIRM]**
My recommendation: own it, once, late, and plainly. "Built by AquaTerra, a student-run NGO. The platform is for any family looking for a tutor." Hiding the origin leaves the question open and people will find out anyway. Put it in slide 4 of the explainer and in the caption footer, never in a headline.

### 4.4 Voice
Warm, plain, local. Short sentences. Says what happens next. No jokes that need an emoji to land. English first **[CONFIRM]**, with an optional Bengali track in phase 4 once a font and a native reviewer are in place. Follow `brain/BRAIN.md`: no em or en dashes, no "thousands", "trusted by", "best", "guaranteed", "100%".

### 4.5 One reframe I am pushing
Do not run a "myth vs fact" campaign as the spine. Run a "what it is" campaign with one correction beat. The myth format works for the people who already know the myth. Your interviewees are the evidence that most of the audience holds the myth, so we meet them with the answer, not with the argument.

---

## 5. Facts policy (hard rules)

Every claim in every asset falls into one of three bins.

**Safe to state now** (recorded constants in `facts/facts.sample.json`):
- Shikshaq is for Kolkata.
- Classes IV to XII. Boards ICSE, ISC and CBSE.
- Site: shikshaq.in.

**Safe only after you confirm** (listed in the open questions):
- Parents contact tutors directly. Shikshaq handles no payment between them. Source: `shikshaq-terms-conditions.md` per `AQ_FACTS.md`, "free platform, connection-only, zero payments/employment handled".
- Zero commission.
- Any statement that tutors are "verified". Say nothing about verification until you confirm what verification means in the product today.
- Question papers as a second feature (see section 6, series G).

**Never state:**
- "147 teachers". The sample file marks it as an application count and unverified.
- Any live count without a production query. `fetch-facts.mjs` has not run against production, so there are no live figures yet.
- Research numbers (n=80 survey, 85%, 11 days to under 48 hours) unless you confirm they are publishable and sourced correctly.
- Testimonials, tutor photos, ratings or reviews that do not exist.

The copy gate in `src/validate.mjs` enforces the digit and social-proof rules mechanically. Layouts say "three steps" in words where a digit is not traceable to a fact.

---

## 6. Content architecture: seven series

The campaign is seven series. Each has one job, one format family and one audience. Sections 7 and 8 list the assets and the calendar.

### Series A: "The Misreads" (correction, single-slide posters)
**Job:** retire the charity frame in public.
**Format:** single-slide poster, 1080x1350 feed, with a story-canvas cut.
**Pattern:** a large quoted misreading on a tilted sticker, answered below by the plain truth. Example copy:
- Sticker: "Is this a charity class?" Answer: "No. It is a tutor directory for any family in Kolkata."
- Sticker: "Is this a coaching centre?" Answer: "No. You find a tutor and talk to them yourself."
- Sticker: "Is this only for students who cannot afford tuition?" Answer: "No. It is for any family looking for a tutor." **[CONFIRM the claim and that the people who use it include all income groups]**
**Guard rails:** misreads 2 and 3 are my guesses at other readings. Replace them with the actual wording from your interview notes. Quote real phrases where you can. The correct answer is always the biggest type. The wrong frame is smaller and tilted, a visual "no".
**Count:** three posters, spaced across the run, never consecutive.

### Series B: "Find a tutor in three steps" (how it works)
**Job:** make the product concrete.
**Format:** a 6-slide Status sequence (1080x1920), an Instagram carousel (1080x1350) built from the same copy, and a one-slide poster version.
**Steps:** search by subject, class and area; read the tutor's profile; contact them directly. **[CONFIRM the real flow and order]**
**Visual:** a clean generic profile card built from real product fields. No fabricated names, ratings or photos.

### Series C: "Parent questions" (FAQ stories)
**Job:** remove the objections that follow the definition.
**Format:** Instagram and WhatsApp story singles, one question each, plus a recap carousel.
**Questions (draft, **[CONFIRM answers]**):** Do I pay Shikshaq? Which classes and boards? Which areas of Kolkata? What do I say to a tutor first? Can my child's tutor change later?
**Rule:** an answer we cannot source becomes a "we will say when we know" gap, never a guess.

### Series D: "Meet a tutor" (proof)
**Job:** show real people on the supply side. This is the strongest proof the platform is for tutoring, not charity.
**Format:** story singles and a carousel per tutor: one tutor, one subject, one quote.
**Dependency:** real tutors, written consent for name, photo and quote, and approval of the final copy. If we have none by phase 2, this series moves to phase 4 and is replaced by series B repeats. We do not stage substitutes.

### Series E: "Teach on Shikshaq" (tutor recruitment)
**Job:** convert tutors, correct their misreading.
**Format:** story singles and a 5-slide carousel. Reuse the tutor-voice WhatsApp-chat mockup device noted in `AQ_FACTS.md` (TEXT WALA POST 01 to 05) as a visual idea, rebuilt in Shikshaq tokens.
**Message:** "Put your profile where families are searching." Three lines on what a tutor does and gets. **[CONFIRM what a tutor does, whether it is free to list, and what the profile contains]**

### Series F: "Forward this" (the share layer)
**Job:** make the one-line definition travel.
**Format:** one 1080x1080 square sized for WhatsApp forwards, a forwardable text, and a "say it in one sentence" card for volunteers.
**Rule:** every asset in this series must make sense with zero context and no caption.

### Series G: "Papers" (conditional) **[CONFIRM]**
The addon already plans question-paper posts. I recommend keeping papers out of this campaign. A second message dilutes the correction, and the interviewees' confusion is about the tutor side. If you want papers in, add them in phase 4 as a clearly separate series.

---

## 7. Asset inventory

Canvas key: **S** = story/Status 1080x1920 · **F** = feed 1080x1350 · **Q** = square 1080x1080.

| ID | Series | Asset | Canvas | Count | Audience | Notes |
|---|---|---|---|---|---|---|
| H1 | Hero | Definition poster: "Shikshaq is where Kolkata families find tutors" | F | 1 | Both | The anchor. All other copy derives from this |
| H2 | Hero | Definition story cut | S | 1 | Both | Same copy, vertical |
| A1 to A3 | A | The Misreads posters | F + S | 3 | Parents | Replace guesses with real quotes |
| B1 | B | "Find a tutor in three steps" Status sequence | S | 6 slides | Parents | The spine of the run |
| B2 | B | Same, Instagram carousel | F | 6 slides | Parents | |
| B3 | B | Same, single poster | F | 1 | Parents | Cut for feed grids |
| C1 to C5 | C | Parent question stories | S | 5 | Parents | One question each |
| C6 | C | Parent FAQ recap carousel | F | 5 slides | Parents | |
| D1 to D3 | D | Meet a tutor stories | S | up to 3 | Both | Needs real consent |
| D4 | D | Meet a tutor carousel | F | 1 per tutor | Both | Same |
| E1 to E4 | E | Tutor recruitment stories | S | 4 | Tutors | |
| E5 | E | Tutor recruitment carousel | F | 5 slides | Tutors | |
| E6 | E | Tutor recruitment single poster | F | 1 | Tutors | |
| F1 | F | Forwardable square | Q | 1 | Both | Stand-alone |
| F2 | F | Volunteer "say it in one line" card | Q | 1 | Volunteers | |
| T1 | Text | Broadcast message, parents | WhatsApp text | 1 | Parents | Draft with `aq-event-messaging` skill |
| T2 | Text | Broadcast message, tutors | WhatsApp text | 1 | Tutors | |
| T3 | Text | Group-post version, short | WhatsApp text | 1 | Both | |
| T4 | Text | Instagram captions, alt text, hashtags | Text | One per feed asset | Both | Caption gate: 900 chars, 8 hashtags |
| R1 | Reel | 15 to 20 second explainer script | Script | 1 | Both | Script and storyboard only. The engine makes stills, not video |
| P1 | Print | A5 flyer with a QR that points to shikshaq.in | Print | 1 | Both | Phase 4. The QR must be a real generated code for the real URL |

Totals: about 40 deliverables if series D has real tutors, about 32 without.

---

## 8. Calendar: three weeks plus evergreen

Posting time default: 19:30 IST, the weekly engine's slot **[CONFIRM for WhatsApp Status, where late morning and evening both work]**. A Status disappears after 24 hours, so every Status asset stands alone.

### Pre-flight (before day 1)
- Answer the open questions in section 13.
- Run `fetch-facts.mjs` against production and record baseline searches and profiles. Nothing posts before this.
- Add a story canvas (1080x1920) to the Shikshaq renderer. See section 10.
- Interview notes: pull exact misreading quotes for series A.

### Week 1: DEFINE
| Day | Content |
|---|---|
| Mon | H1 hero poster (feed). H2 story. T1 broadcast to parent groups |
| Tue | B1 slides 1 to 3 on Status |
| Wed | B1 slides 4 to 6 on Status. B2 carousel on Instagram |
| Thu | F1 forwardable square. Volunteers get F2 |
| Fri | A1 first misread poster |
| Sat | C1 and C2 parent question stories |
| Sun | Read the numbers. Re-ask three interviewees. Adjust week 2 |

### Week 2: SHOW AND ANSWER
| Day | Content |
|---|---|
| Mon | B3 single poster. C3 story |
| Tue | D1 tutor story (if consent). A2 poster |
| Wed | C4 and C5 stories. C6 FAQ carousel |
| Thu | D2 story or a B1 repeat. T3 group post |
| Fri | A3 poster. Story poll: "What did you think Shikshaq was?" (native sticker, added in the app) |
| Sat | Repeat the best performing asset from week 1 |
| Sun | Read the numbers. Re-ask the interviewees |

### Week 3: ACTIVATE BOTH SIDES
| Day | Content |
|---|---|
| Mon | E6 tutor poster. T2 broadcast to tutor groups |
| Tue | E1 and E2 tutor stories |
| Wed | E5 tutor carousel. D3 or D4 |
| Thu | E3 and E4 stories |
| Fri | H1 reprise with a new line: "Search or list. Both start at shikshaq.in" |
| Sat | Parent CTA story and tutor CTA story on the same day |
| Sun | Full read of the numbers against the baseline. Debrief |

### Phase 4: SUSTAIN
- Keep H1, B1 and F1 in the story highlights and the pinned post.
- One misread poster or one parent question a week folded into the existing weekly Instagram engine (`run-week.mjs`) as a rotating slot, so the correction does not vanish after week 3.
- Optional: Bengali track, A5 flyer (P1), papers series (G), reel (R1).

---

## 9. Creative direction

### 9.1 Brand
Shikshaq tokens only: warm bone ground (never white), saturated slabs at radius 32, the weight-400 plus weight-800 headline pair, tilted overhanging stickers (one per card at most), blob mascots in the site palette, at most two saturated fills per poster. Fonts are Archivo and Geist in `assets/fonts/`. No AQ cream, no AQ doodles. The accent is semantic per pillar: indigo for the how-it-works and parent series, orange for tutors, mint for answers and tips **[CONFIRM against the site]**.

### 9.2 The look of the idea
- **One sentence per slide.** The type is the hero. The eye lands on the answer, never on the myth.
- **The misread is a sticker, the truth is a slab.** A tilted, smaller, outlined sticker carries the wrong frame. A full-width saturated slab carries the right one. Scale does the arguing.
- **Directory visual, not classroom visual.** Search bar, profile card, location pin, subject chips. No chalkboards, no uniforms, no charity-shaped imagery (hands, donation motifs, "helping" poses). The imagery is the loudest part of the correction.
- **Mascots:** the blob characters appear as the asker and the tutor, never as a teacher at a blackboard.

### 9.3 Series colour and layout rules
| Series | Accent | Template family |
|---|---|---|
| H, B, C, F | Indigo | `steps`, `find-teacher` |
| A | Mint answer on bone, orange sticker | `number-bento` adapted, or a bespoke build |
| D, E | Orange | `find-teacher`, `bento-board` for the tutor mosaic |

The existing templates are `bento-board`, `find-teacher`, `number-bento`, `paper-spotlight`, `steps` and `subject-mosaic`. The story canvas and the misread layout are new. See section 10.

### 9.4 Photography
No stock children, no staged classroom shots. Real tutors only, with consent. If a series needs a face and has none, it uses a mascot.

---

## 10. Production plan

Build in this order so each step reduces risk for the next.

1. **Fact baseline.** `node src/fetch-facts.mjs` against production. Record searches, profiles, tutor count and which statements in section 5 hold.
2. **Story canvas.** Extend `src/render.mjs` so templates render at 1080x1920. Add a story-safe zone (top and bottom bands reserved for the WhatsApp and Instagram chrome) as a layout-gate rule. Prove it in `selftest-render.mjs`. This is the engine rule, and it applies to every future story, not just this campaign.
3. **Misread template.** A new template for series A: sticker over slab. Add it to the style bank with a recipe, then run `npm run test:render`.
4. **Copy bank.** Put the campaign copy in `pillars.json` or a campaign-specific file so `validate.mjs` polices it. A weak line is a missing rule, not a one-off edit.
5. **Generate in waves.** Wave 1 H1, H2, B1, B2, B3, F1. Wave 2 A, C. Wave 3 E and D.
6. **Gates on every asset.** Copy gate before drawing. Layout gate on the rendered DOM (clipped text, margins, per-element WCAG contrast, collisions). Then the looking gate: open each PNG and `_week.png`-style contact sheet and review it by eye. Numeric gates passed visibly wrong posters during the addon's own build, so the eye stays mandatory.
7. **Companion art.** The repo's standing rule requires one `/canvas-design` companion piece alongside engine output. I run it once per generation wave.
8. **Text assets.** Broadcast, group-post and caption drafts via the `aq-event-messaging` skill, then the caption gate.
9. **Hand-off folder.** `out/campaign-what-is-shikshaq/` with PNGs grouped by series, a `schedule.md` with day, time, asset and caption, and alt text for every image.

Delivery stays as `BRAIN.md` states: the engine produces a reviewable folder. Nothing posts automatically.

---

## 11. Risks and how the brief handles them

| Risk | Why it matters | Handling |
|---|---|---|
| The correction reinforces the myth | Repeating the wrong frame embeds it | Define first. Misread is a small sticker. Never lead with a negation |
| A claim we cannot back | One false line damages a trust product | Section 5 fact bins. Copy gate. [CONFIRM] flags |
| "Verified" overclaim | Parents will rely on it | No verification language until the product's real process is confirmed |
| Tutor consent missing | Using a real person's face or words without consent | Series D is gated on written consent. Otherwise it moves to phase 4 |
| Two audiences in one poster | Blurs both messages | Every asset addresses one audience |
| Story chrome covers type | WhatsApp and Instagram overlay the top and bottom | Story-safe zone as a layout-gate rule |
| Status expires in 24 hours | A viewer sees one slide only | Each Status slide carries a full sentence of meaning |
| Interview sample is small and self-selected | We may be generalising from a few people | The re-ask and the poll are the real test. Re-weight week 2 and week 3 on what they show |
| The campaign works for parents and tutors diverge | A tutor reading a parent poster gets confused | Separate calendar days and separate groups for parent and tutor broadcasts |
| Bengali copy without a native review | Wrong words in a trust message | Bengali is optional and ships only with a native reviewer and a font check |

---

## 12. Measurement and learning loop

1. **Baseline (pre-flight):** searches and tutor profiles in the week before day 1, from production.
2. **Weekly read (Sunday):** same two numbers, plus Status views, replies, forwards, Instagram saves and shares per asset.
3. **Comprehension check:** re-ask the interviewees "What is Shikshaq?" at the end of week 1 and again at the end of week 3. Record their words verbatim. Add the story poll in week 2.
4. **Decision rule:** if the answer is still "charity classes" after week 1, change the creative (more of the directory visual, fewer words) before changing the volume. If the answer is correct but searches do not move, the problem is the call to action or the product, not the message.
5. **Write back to the engine.** Any visual flaw caught by eye becomes a rule in `validate.mjs` or the `gate()` in `render.mjs`, proven in the self-test, then regenerated. That is how the Shikshaq engine improves.

---

## 13. Open decisions (each one changes specific assets)

1. **Product flow** (changes B, C, E): confirm the search, profile, direct-contact order and that Shikshaq handles no payment between family and tutor.
2. **Zero commission and free listing** (changes C, E): confirm both and the exact wording you are comfortable with.
3. **Verification** (changes A, C, D): what, if anything, may we say about tutor verification today?
4. **Papers** (changes G): in or out. Recommended out.
5. **Origin story** (changes H, B slide 4, captions): own "built by a student-run NGO" or leave it off.
6. **Audiences** (changes E and the calendar): parents only, or parents and tutors as drafted.
7. **Language** (changes everything text): English only or English plus Bengali.
8. **Real tutors** (changes D): do we have any who consent to appear, and how many?
9. **Real quotes** (changes A): paste the actual misreading phrases from the interviews.
10. **Channels and times** (changes the calendar): WhatsApp Status, groups and broadcast lists, Instagram feed and stories. Confirm which exist and who posts.
11. **Accent mapping** (changes the look): confirm indigo, orange and mint against the site.
12. **Approver and cadence** (changes delivery): who signs off, and by when each wave is needed.

---

## 14. Next steps

1. You answer section 13. Partial answers are enough. I proceed on the assumptions marked [CONFIRM] and flag every asset they touch.
2. I run the production fact baseline if I can reach Supabase from this environment. If I cannot, the baseline is yours to read and I will say so.
3. I build the story canvas and the misread template, with self-tests.
4. I generate wave 1, look at every PNG, and send you the contact sheet before wave 2.
