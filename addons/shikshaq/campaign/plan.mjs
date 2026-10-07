// The four-week plan (revised after the owner's answers of 2026-10-07).
//   Launch: Monday 12 October, no Puja pause (the plan rides it). Day 0 is Sunday 11 October: pin the FAQ highlight before anything else goes up.
//   Goal: parents know what Shikshaq is. Feed is lighter (five a week) and anchored on the chat, Things parents say, the facts, three steps and the parent's guide.
//   Everything else runs as stories, reels and WhatsApp. Entries are asset ids or POST ids (a post id expands to every slide).
//   Feed 19:30. Stories through the day. Reels in the evening on their day. WhatsApp pushes by id (wa.mjs, four a week).
export const WEEKS = [
  { n: 1, theme: 'DEFINE: what it is, in the audience\'s own words', days: [
    { d: 'Mon', feed: 'H1', stories: ['FQ0', 'FQ1', 'FQ2', 'FQ3', 'FQ4', 'H2'], wa: ['WP1'], note: 'Launch day. Day 0 (Sunday) is setup: pin the FAQ highlight (FQ0 to FQ8) and the other highlight covers before the first post goes up.' },
    { d: 'Tue', feed: 'B2', reel: 'RS1', stories: ['FQ5', 'FQ6', 'FQ7', 'FQ8', 'HC1', 'WY1s'], wa: ['WP2'] },
    { d: 'Wed', reel: 'R1', stories: ['B1', 'PF1', 'H4', 'SJs1'] },
    { d: 'Thu', feed: 'CH1', stories: ['PF2', 'PF3', 'MB1', 'MB2', 'FT1s'], wa: ['WP19'] },
    { d: 'Fri', feed: 'SY1', reel: 'RS2', stories: ['MB3', 'IN1', 'SJs2', 'WY2s'] },
    { d: 'Sat', feed: 'FT1', stories: ['CH1s', 'H5', 'SY1s', 'HC4'], wa: ['WP17'] },
    { d: 'Sun', reel: 'R2', stories: ['CL1s', 'IN2'], note: 'Read the numbers. Re-ask three interviewees what they thought Shikshaq was. Adjust week 2.' },
  ] },
  { n: 2, theme: 'SHOW AND ANSWER: the student tells the parent', days: [
    { d: 'Mon', feed: 'PG1', stories: ['CH2s', 'MB4', 'SY2s', 'FT2s'], wa: ['WP5'], note: 'Puja week: keep the posts, they are short. Seasonal story CL2s can run in place of CL1s.' },
    { d: 'Tue', feed: 'CH2', reel: 'RS3', stories: ['CH3s', 'EY1', 'PG1s', 'SJs3'], wa: ['WP18'] },
    { d: 'Wed', reel: 'R3', stories: ['CH4s', 'MB5', 'WY3s', 'HC6'] },
    { d: 'Thu', feed: 'SY2', stories: ['CH5s', 'EY2', 'SY3s', 'PG2s'], wa: ['WP7'] },
    { d: 'Fri', feed: 'FT2', reel: 'RS4', stories: ['IN3', 'EY3', 'SJs4', 'WY4s'] },
    { d: 'Sat', feed: 'PG2', stories: ['CL2s', 'SY4s', 'HC7'], wa: ['WP21'] },
    { d: 'Sun', reel: 'R4', stories: ['AKs1', 'AKs2'], note: 'Read the numbers. Re-ask the interviewees.' },
  ] },
  { n: 3, theme: 'PROOF AND BOTH SIDES: who made it, what students say, tutors', days: [
    { d: 'Mon', feed: 'WM1', stories: ['WM2', 'WM3', 'WM4', 'HC2', 'SY5s'], wa: ['WP9'], note: 'WM1 also goes on the AquaTerra account.' },
    { d: 'Tue', feed: 'CH3', reel: 'RS5', stories: ['RV8', 'RV9', 'RV10', 'HC3', 'PG3s'], wa: ['WP10'], note: 'RV stories are gated on real reviews. If not ready, run SJs and PG stories instead.' },
    { d: 'Wed', reel: 'R5', stories: ['TQ0', 'TQ1', 'TQ2', 'TQ3', 'TQ4', 'TQ5', 'TQ6'] },
    { d: 'Thu', feed: 'RV1', stories: ['TT2', 'TT3', 'TT4', 'TT5', 'AKs3'], wa: ['WP27'], note: 'RV1 is gated on real reviews. If not ready, swap in SY3.' },
    { d: 'Fri', feed: 'FT3', reel: 'RS6', stories: ['MT1', 'MT2', 'MT3', 'FT3s'], note: 'MT stories are gated on tutor approval. If not ready, swap in SJs7.' },
    { d: 'Sat', feed: 'TT1', stories: ['RC2', 'RC3', 'IN4', 'AKs4', 'HC5'], wa: ['WP28'] },
    { d: 'Sun', reel: 'R6', stories: ['AKs5', 'PG4s'], note: 'Read the numbers. Re-ask the interviewees.' },
  ] },
  { n: 4, theme: 'YOUR MOVE: exams, classes, and the ask', days: [
    { d: 'Mon', feed: 'PG3', stories: ['RP2', 'CS1s', 'EX1s'], wa: ['WP13'] },
    { d: 'Tue', feed: 'CH4', reel: 'RS7', stories: ['RP3', 'CS2s', 'SJs5'], wa: ['WP14'], rerun: ['FQ1', 'FQ2', 'FQ3'] },
    { d: 'Wed', reel: 'R7', stories: ['RP4', 'CS3s', 'EX2s'], rerun: ['CH2s'] },
    { d: 'Thu', feed: 'CH5', stories: ['CS4s', 'SJs6', 'EX3s'], wa: ['WP15'], rerun: ['best performing story from weeks 1 to 3'] },
    { d: 'Fri', feed: 'PG4', reel: 'RS8', stories: ['CL3s', 'SJs7', 'SJs8'], rerun: ['B1'] },
    { d: 'Sat', feed: 'RP1', stories: ['SY6s'], wa: ['WP16'], rerun: ['best performing story'] },
    { d: 'Sun', reel: 'R1', note: 'Rerun the best-performing reel. Final read of the numbers against the baseline. Debrief.' },
  ] },
];
// The bank: finished posts that did not get a daily slot. Run one in any quiet hour, on a gated day that is not ready, or as a story where a story version exists.
export const RESERVE = ['H3', 'B3', 'PF5', 'BB1', 'FQ9', 'SY3', 'SY4', 'SY5', 'SY6', 'AK1', 'EX1', 'EX2', 'EX3', 'CS1', 'CS2', 'CS3', 'CS4', 'WY1', 'WY2', 'WY3', 'WY4', 'SJ1', 'SJ2', 'SJ3', 'SJ4', 'SJ5', 'SJ6', 'SJ7', 'SJ8', 'RV2', 'RV3', 'RV4', 'RV5', 'RV6', 'RV7', 'MT4', 'MT5', 'MT6', 'TT6', 'TT7', 'TT8', 'TT9', 'RC1', 'CL1', 'CL2', 'CL3'];
// Reels. Series reels carry a story; subject loops are eight to ten seconds. Audio comes later (ElevenLabs): see reels/README.md.
export const REELS = {
  R1: 'Find your tutor in three steps', R2: 'The chat at home', R3: 'Things parents say', R4: 'The facts, plainly', R5: 'Who made it', R6: 'For tutors: keep every rupee', R7: 'Questions to ask a tutor',
  RS1: 'Maths loop', RS2: 'Science loop', RS3: 'English loop', RS4: 'Commerce loop', RS5: 'Computer loop', RS6: 'Hindi loop', RS7: 'History loop', RS8: 'Geography loop',
};
// The AquaTerra account takes these (owner ruling 2026-10-07: who made it, and the facts) and nothing else.
export const AQUATERRA = ['WM1', 'WM2', 'WM3', 'WM4', 'FT1', 'FT2', 'FT3'];
