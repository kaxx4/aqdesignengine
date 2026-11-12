# RECRUITMENT BUILD BRIEF (v4, 2026-11-12)

For anyone building a piece of the "(just a student)" recruitment campaign. Read this, then `RECRUITMENT_ECOSYSTEM_NOV2026.md` (the plan), then CLAUDE.md sections 3, 6, 9 and 10.

## 0. What the owner asked for, in their words

"Learn from other designs and incorporate all these elements in AQ's design. Every design looks different, yet it is part of the same campaign. A very cohesive campaign, with a lot of variation." Earlier waves each used one of the owner's five references (cast list, fill-in-the-blank, the note, the full-bleed hero, the website page). This wave draws 17 more mechanisms from the 74-style bank, one per piece, so no two pieces share a skeleton.

## 1. THE CAMPAIGN CONSTANTS (what makes 20 different pieces one campaign)

Every piece, whatever its style, carries ALL of these, using the kit (`scratchpad/recruit_kit.py`):

1. **`K.series_tab()`**, the yellow `(just a student)` tab, top right. (If a style's composition makes that impossible, keep the words on a sticker, tab or pill elsewhere. Never drop it.)
2. **`K.lane_chip("<dept>")`**, a small chip in the department colour, top left under the logo, naming the department. Colours: events sky, welfare mint, Crftd tomato, ShikshAQ lemon, social media and blogs grape, collabs pink, HR teal. Connectors use `"all"`.
3. **The logo**, top left (`K.logo()`, or `K.logo_pill()` over a photo).
4. **The exit**: `ngoaquaterra.com/recruitment`, as `K.url_pill()` or `K.footer()`. Soft ask only.
5. **One real number**, with its qualifier, taken from `K.FACTS`. Never type a number that is not in that table.
6. **The reveal order**: a situation or a claim a student would not expect, then "and yet", then the proof. The ask is optional and small.
7. **The department's own photo.** A welfare piece uses a welfare photo, a Crftd piece the Crftd stall photos, a blogs piece the real blog covers, the Social Media lane the team's own slides. `K.PH` names every photo; `K.contact(folder, out)` makes a contact sheet so you can look.
8. **AQ ground and craft**: cream ground (never white), ink outlines and hard offset shadows on solid objects, one hero, accents as punctuation. The reference style decides the SKELETON; the AQ tokens decide the colour, type and craft.

Variation comes from the style assignment. Cohesion comes from the eight items above. A piece that looks like an earlier wave (look at `out/recruit_nov2026/v2/*.jpg` and `v3/*.jpg` first) has failed the brief.

## 2. VOICE (copy is the part the owner has rejected twice, so this section is not optional)

The voice is a dry, specific friend, not an organisation. House register 3 on the `VOICE.md` ladder: understated, one aside per piece, the joke is on AQ or on the situation, never on a person.

- **Specific beats general.** "lost an argument with a vendor over balloons" beats "learn negotiation".
- **Lowercase body, UPPERCASE display** (the style may override display case where its recipe is serif-led; record that).
- **No em dashes. No emojis on graphics. No Bengali, no "adda", no regional slang.** Plain English with the occasional "bhai" or "ngl" at most, and only where it earns its place.
- **Never**: "join AQ now", "make a difference", "change the world", "passionate", "empower", "journey", "impact", "so, what's stopping you", or a paragraph describing what AQ is.
- **Never preach, never guilt, never judge a non-member.** Every ask has an easy exit.
- **Soft CTA ceiling:** "applications are open." / "link in bio." / the URL. No countdowns, no deadlines (none exist).
- **First names only** for any person, and only if the owner supplied them (none have been). Do not name members.
- **Do not invent**: numbers, quotes, member testimonials, partner names, dates. If the fact is not in `K.FACTS` or a file you actually read, leave it out.
- Good lines already shipped (match this level, do not copy them): "SCHOOL TEACHES ALGEBRA. WE TEACH HAGGLING." / "WE THROW PARTIES. WE SELL T-SHIRTS. THE DOGS EAT." / "...that was it?" / "You are not too young." / "nobody in this photo has a boss, and the line still moved." / "bring opinions about balloons."

## 3. HOW AQ TALKS ABOUT JOINING (the owner's rulings, 2026-11-12)

- The campaign recruits into **Community AQ**: you apply, you are in, quickly and easily. There is an interview behind it. **Do not talk about the process.** No step lists, no "how it works", no "we message you on WhatsApp". The ask is just the URL.
- Once someone is in a department they are in **Team AQ**. You may say "Team AQ" when you mean the people inside a department. Do not explain the two layers.
- The eight departments: **events, welfare, Crftd (formerly ROOTS), ShikshAQ, social media (marketing and social media are one department), blogs, collabs, HR.**
- Certificates and letters of recommendation are real, for people who do the work, but they are **not a selling point**. At most one tiny line, never a headline. The perk is not being the person who watched it happen from the sidelines.
- Photos of children are cleared by the owner, for every frame in the library.

## 4. THE FIVE TIERS (state which tier each piece is in your report)

T1 what you can do (no ask) · T2 recruit (direct, small) · T3 FOMO · T4 learning · T5 general (a joke worth forwarding, AQ nearly invisible). Three of every five pieces carry no ask.

## 5. HOW TO BUILD (process)

1. `K.style_brief("<style id>")` prints the recipe and the path to the reference image. **`Read` the reference image.** Then write the composition description (the CLAUDE.md step-1 checklist) in your head or a comment.
2. Browse the photos you will use: `K.contact("events/welfare-feed-2026", "<scratchpad>/c.jpg")` then `Read` it.
3. Write one script per department group, `scratchpad/gen_recruit_v4_<group>.py`, using `import recruit_kit as K` (copy the first lines of `gen_recruit_v3.py` for the pattern). Build the HTML from kit helpers and absolute-positioned divs. Heavy raster work (posterise, dither, duotone, halftone) is done in PIL, as in v2/v3.
4. `K.render("<dept>_<n>", html, H=1350)` writes `out/recruit_nov2026/v4/<name>.png` and `.jpg`. It runs the render gate; **read what it prints**, but a clean gate proves nothing visual.
5. **`Read` the `.jpg` and run the looking gate (CLAUDE.md section 3):** legibility, hierarchy, balance, no dead quadrant, no collisions, nothing clipped. Compare against the reference image. At least two iterations. Fix, re-render, look again.
6. Precedence ladder (CLAUDE.md section 2): a hard brand rule beats the recipe; the recipe's count is a target not a ceiling; **the mechanism is the part you may not drop**; record every adaptation in the script docstring.
7. Do not commit or push. Do not edit another builder's files or the shared kit. If the kit is missing something, write the helper in your own script.
8. The standing companion-art-piece rule belongs to the session that dispatched you. Say in your report that it is outstanding; do not produce one.

## 6. WHAT TO REPORT

Per piece: file path, style id, lane, tier, headline and the key copy, the real number used and where it came from, adaptations made, anything unverified or that the owner must confirm, and an honest line on what you think is still weak. Do not claim a clean looking gate you did not run.
