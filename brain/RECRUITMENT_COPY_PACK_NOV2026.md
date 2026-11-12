# RECRUITMENT PUSH, COPY PACK v2 (2026-11-12)

Supersedes the sample copy and the v1 design mapping in `RECRUITMENT_CAMPAIGN_NOV2026.md` sections 5, 8 and 9b. The v1 copy read like a brochure and the v1 designs softened the references into safe boxes. Both were rejected by the owner. This pack is the replacement.

Approver: the owner. Nothing posts without them. Rendered pieces live in `out/recruit_nov2026/v2/` (gitignored, the repo is public). Build script: `scratchpad/gen_recruit_v2.py`.

## 1. The intent, in one paragraph

Get a lot of Kolkata school students and college first years to join a community that earns its own money, runs its own things and argues with real vendors, even though everyone in it is a student. The campaign is not "join our NGO". It is a run of small scenes that make a student think "wait, I could do that", with the ask arriving late and small. The perk is not being the one who watched it happen from the sidelines. Application: **ngoaquaterra.com/recruitment** (the owner said "ngoaquata"; the repo and every live link use `ngoaquaterra.com`, so that is what is printed. Confirm).

## 2. The tiers (not every piece recruits)

| Tier | Job | Ask | Pieces |
|---|---|---|---|
| **T1 what you can do** | show the work, no pitch | none | `r2_blank` |
| **T2 recruit** | nudge to apply | direct, small | `r5_site`, WhatsApp A, story links |
| **T3 FOMO** | make the sidelines feel loud | soft | `r1_cast`, WhatsApp B |
| **T4 learning** | the skills school skips | soft | `r4_haggling` (feed and story) |
| **T5 general** | a joke a student forwards, AQ nearly invisible | footer only | `r3_late` (feed and story) |

Rule of thumb for the calendar: three of every five pieces carry no ask. T2 is the minority on purpose (the master brief keeps recruitment the rarest pillar; this push loosens that for a few weeks, not forever).

## 3. The five pieces, each a close recreation of one reference

| File | Reference mechanism, kept | AQ photo | Copy |
|---|---|---|---|
| `r1_cast` | B&W photo, colour windows with track-name tabs, serif title lockup, small paragraph | registration desk, Summer AQ turns five | Title: **Everyone in this photo is a student.** Tabs: INTRO : we're students, apparently / TRACK 02 : the last price (it was not) / SKIT : whose laptop is this / THIS SEAT : yours / OUTRO : someone find the wristbands / TRACK 05 : who has the walkie-talkie. Paragraph: "Registration desk. four laptops, two walkie-talkies and a wristband situation. nobody in this photo has a boss, and the line still moved. applications are open at ngoaquaterra.com/recruitment." |
| `r2_blank` | fill-in-the-blank sentence, photo crops as words, cut-outs left in the photo | Disco Diwali hall, green light | "Some students built a (crop) hall, hung (crop) lights, lost an argument with a vendor over (crop) balloons, and then danced on the result. (crop) Applications are open. Bring opinions about balloons. (crop)" |
| `r3_late` | posterised landscape, frosted card, highlight chip, stick figures, italic captions | street dog (faceless), dog close up | Top: "Doing nothing over winter break is more common than you think." Card: **You are not late.** Right: "Nobody started anything on 1st January at 9am sharp. Most good ideas begin on a random Tuesday, right after someone says what if we just did it." / chip: the URL / "We are students who feed dogs, throw fests and lose arguments to vendors. Come be late with us." Bottom: "Applications are open. Nobody is checking your timing." |
| `r4_haggling` | full-bleed photo, white headline, glass pills, glass fact card, dock, stacked card, squiggles | blurred dance floor | **SCHOOL TEACHES ALGEBRA. WE TEACH HAGGLING.** Pills: Vendors, Sponsors, Budgets. Card: "Applications open / AQUATERRA, KOLKATA / student-run since 2021. events, welfare, startups, a magazine." Caption: "no donations. we throw parties and sell clothes, and that pays for everything." |
| `r5_site` | a website page: nav, serif headline with italic tail, dithered photo strip, four colour blocks, black "How it works" band with numerals running off the bottom | event and drive photos, dithered | **Fests, drives and startups, run by people still doing homework.** Blocks: Events / Welfare / Startups / Magazine, one line each. "How it works: Fill the form. Come to one drive. Find your team. Certificate and LOR if you do the work." |

## 4. Instagram captions (one per feed piece, lowercase, link in bio)

- `r1`: four laptops, two walkie-talkies, zero bosses. applications are open. link in bio.
- `r2`: we lost the argument. the balloons still showed up. applications are open, link in bio.
- `r3`: you are not late. link in bio.
- `r4`: school teaches algebra. we teach haggling. link in bio.
- `r5`: fests, drives, startups, a magazine. all run by students who also have homework. link in bio.

## 5. Story set

Stories 1080x1920, top 200 and bottom 250 stay clear for the Instagram UI. `r4_haggling_story` and `r3_late_story` are built. Copy-only extras, ready to build from the same two mechanisms:

1. **Poll.** "the vendor says the price is final. you: / pay it / haggle." Photo: the vendor with the googly eyes (`events/nandu-jee`).
2. **Question box.** "ask us anything about aq. yes, even the vendor stuff."
3. **This or that.** "winter break: a) reorganise your desktop again b) argue with a vendor"
4. **Link story.** "applications are open." Link sticker over the URL, nothing else.
5. **Countdown-free reminder.** "still open. no one is checking your timing." (no date, no deadline exists)

## 6. WhatsApp (plain text, no emojis, forward-friendly)

**A. Recruit (T2), to school groups and broadcast lists**
> ok so. aq applications are open.
>
> if you have ever wanted to haggle with a vendor, run a check-in desk, or write something people actually read, this is the version of that where you are allowed to.
>
> fests, drives, a magazine, startups. all run by students. none of it needs a resume.
>
> form: ngoaquaterra.com/recruitment
> come to one drive first, decide after. certificates and LORs are real, for people who do the work.

**B. The forward (T3 FOMO), meant to be sent to one friend**
> bhai you watched the disco diwali stories and said we should do something like that. this is the something. ngoaquaterra.com/recruitment

**C. Member to friend (T3)**
> i'm in aq. nobody has a boss, the vendors are scary, the dogs are very grateful. come to one drive, you can hate it after. ngoaquaterra.com/recruitment

**D. One-liner for class groups (T5)**
> winter break plan: sleep, then something. ngoaquaterra.com/recruitment

**E. Parent version (register 2, no snark)**
> Hello, this is Team AquaTerra, a student-run, DARPAN-certified NGO in Kolkata (registration AAFTT2300ME20251). We are inviting school students and college first years to join as volunteers. Students take part in teaching workshops, welfare drives, events and our magazine. The application form is at ngoaquaterra.com/recruitment. Please write to us with any questions. **[CONFIRM supervision and safety wording before sending]**

## 7. What is real and what still needs the owner

| Line | Status |
|---|---|
| founded 2021, student-run | counted (`AQ_FACTS.md` section 1) |
| no donations, parties and clothes pay for it | counted (`AquaTerra_Revenue_Streams.md`: ~90% events, ~10% ROOTS, 0% donations) |
| 65+ kids, Sunday class | counted (Pather Sathi, running 2.5 years) |
| 4.5 L of sharbat | counted (platform post 877, one drive) |
| Disco Diwali Masquerade Sangeet, Nov 2026 | counted (`DISCO_DIWALI.md`) |
| certificates and LORs for people who do the work | stated by the owner, 2026-11-12 |
| **minimum commitment is one drive** | **[CONFIRM] the owner said "just that drive"; read as "one welfare drive"** |
| "come to one drive first" on any poster | depends on the line above |
| magazine, "Read the magazine" link target | **[CONFIRM] where does it point** |
| the parent message's safety language | **[CONFIRM]** |
| photos of real guests and volunteers | consent caveat stands; `welfare-feed-2026` frames with children are local-only |

## 8. Adaptations recorded (precedence ladder)

- The owner's references win on typography here: `r1` and `r5` use Instrument Serif for the headline because the reference IS the serif headline. This overrides the usual one-accent-word rule on those two pieces only.
- Fake UI in the references (a "SARAH, product designer" profile card, a case-study card) became real AQ facts and a real recruitment card.
- Ground is AQ cream, not the references' white or grey.
- Posterise and dither are done in PIL on real AQ photos. Nothing is stock.
- Glass chips use a backdrop blur, a deliberate exception to the "no faint washes" rule because the reference is that effect.
- The gate was run per render. `OFF-CANVAS` on the `r5` numerals and the full-width text-box `MARGIN` notes are by design (the numerals run off the bottom like the reference).

## 9. Still to build, in this order

1. The vendor poll story and the "ask us anything" story.
2. A second pass of `r1` and `r2` on different photos so the feed is not five pieces from one event.
3. A parent-facing poster (register 2) and a school notice-board PDF.
4. A WhatsApp group DP.
