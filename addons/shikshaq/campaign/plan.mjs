// The four-week plan. Entries are asset ids or POST ids (a post id expands to every slide).
// Each day: one MAIN feed post (19:30), on most days a SECOND feed post (12:30), stories through the day, WhatsApp pushes by id (see wa.mjs).
// A post marked gated waits on real data; a reserve post swaps in when it is not ready.
export const WEEKS = [
  { n: 1, theme: 'DEFINE: what it is, in the audience\'s own words', days: [
    { d: 'Mon', feed: 'H1', stories: ['FQ0', 'FQ1', 'FQ2', 'FQ3', 'FQ4', 'H2'], wa: ['WP1'], note: 'Launch day. Pin the FAQ highlight before the first post goes up.' },
    { d: 'Tue', feed: 'B2', feed2: 'B3', stories: ['FQ5', 'FQ6', 'FQ7', 'FQ8', 'HC1', 'WY1s'], wa: ['WP2', 'WP17'] },
    { d: 'Wed', feed: 'CH1', stories: ['B1', 'PF1', 'H4', 'SJs1'], wa: ['WP18'] },
    { d: 'Thu', feed: 'H3', feed2: 'PF5', stories: ['PF2', 'PF3', 'MB1', 'MB2', 'FT1s'], wa: ['WP3', 'WP19'] },
    { d: 'Fri', feed: 'SJ1', stories: ['MB3', 'IN1', 'SJs2', 'WY2s'], wa: ['WP4'] },
    { d: 'Sat', feed: 'FQ9', feed2: 'SY1', stories: ['CH1s', 'H5', 'SY1s', 'HC4'], wa: ['WP20'] },
    { d: 'Sun', feed: 'CL1', stories: ['CL1s', 'IN2'], wa: [], note: 'Read the numbers. Re-ask three interviewees what they thought Shikshaq was. Adjust week 2.' },
  ] },
  { n: 2, theme: 'SHOW AND ANSWER: the student tells the parent', days: [
    { d: 'Mon', feed: 'SY2', stories: ['CH2s', 'MB4', 'SY2s', 'FT2s'], wa: ['WP5', 'WP21'] },
    { d: 'Tue', feed: 'CH2', feed2: 'MG2', stories: ['CH3s', 'EY1', 'MG1s', 'SJs3'], wa: ['WP6', 'WP22'] },
    { d: 'Wed', feed: 'MG1', feed2: 'WY1', stories: ['CH4s', 'MB5', 'WY3s', 'HC6'], wa: ['WP23'] },
    { d: 'Thu', feed: 'SJ2', feed2: 'SY4', stories: ['CH5s', 'EY2', 'SY3s', 'MG2s'], wa: ['WP7', 'WP24'] },
    { d: 'Fri', feed: 'CH3', stories: ['IN3', 'EY3', 'SJs4', 'WY4s'], wa: ['WP25'] },
    { d: 'Sat', feed: 'SY3', feed2: 'SJ3', stories: ['CL2s', 'SY4s', 'HC7'], wa: ['WP8'] },
    { d: 'Sun', feed: 'CL2', stories: ['AKs1', 'AKs2'], wa: [], note: 'Read the numbers. Re-ask the interviewees. Swap CL2 for CL3 if Pujo has passed.' },
  ] },
  { n: 3, theme: 'PROOF AND BOTH SIDES: who made it, what students say, tutors', days: [
    { d: 'Mon', feed: 'WM1', stories: ['WM2', 'WM3', 'WM4', 'HC2', 'SY5s'], wa: ['WP9', 'WP26'] },
    { d: 'Tue', feed: 'RV1', feed2: 'SY5', stories: ['RV8', 'RV9', 'RV10', 'HC3', 'MG3s'], wa: ['WP10'], note: 'RV1 is gated on real reviews. If not ready, swap in RV2 only when it is filled, else SJ6.' },
    { d: 'Wed', feed: 'TT1', feed2: 'FT1', stories: ['TQ0', 'TQ1', 'TQ2', 'TQ3', 'TQ4', 'TQ5', 'TQ6'], wa: ['WP27'] },
    { d: 'Thu', feed: 'CH4', feed2: 'SJ4', stories: ['TT2', 'TT3', 'TT4', 'TT5', 'AKs3'], wa: ['WP11'] },
    { d: 'Fri', feed: 'MT4', stories: ['MT1', 'MT2', 'MT3', 'FT3s'], wa: [], note: 'Gated on tutor approval. If not ready, swap in SJ7.' },
    { d: 'Sat', feed: 'AK1', feed2: 'BB1', stories: ['RC2', 'RC3', 'IN4', 'AKs4', 'HC5'], wa: ['WP12', 'WP28'] },
    { d: 'Sun', feed: 'TT7', stories: ['AKs5', 'MG4s'], wa: [], note: 'Read the numbers. Re-ask the interviewees.' },
  ] },
  { n: 4, theme: 'YOUR MOVE: exams, classes, and the ask', days: [
    { d: 'Mon', feed: 'TT6', stories: ['RP2', 'CS1s', 'EX1s'], wa: ['WP13', 'WP29'] },
    { d: 'Tue', feed: 'CH5', feed2: 'WY2', stories: ['RP3', 'CS2s', 'SJs5'], wa: ['WP14'], rerun: ['FQ1', 'FQ2', 'FQ3'] },
    { d: 'Wed', feed: 'EX1', feed2: 'RC1', stories: ['RP4', 'CS3s', 'EX2s'], wa: ['WP30'], rerun: ['CH2s'] },
    { d: 'Thu', feed: 'CS3', feed2: 'SJ5', stories: ['CS4s', 'SJs6', 'EX3s'], wa: ['WP15'], rerun: ['best performing story from weeks 1 to 3'] },
    { d: 'Fri', feed: 'RV7', stories: ['CL3s', 'SJs7'], wa: [], rerun: ['B1'], note: 'Gated on real reviews. If not ready, swap in SJ8.' },
    { d: 'Sat', feed: 'RP1', feed2: 'FT3', stories: ['SJs8', 'SY6s'], wa: ['WP16'], rerun: ['best performing story'] },
    { d: 'Sun', feed: 'TT8', stories: [], wa: [], note: 'Final read of the numbers against the baseline. Debrief.' },
  ] },
];
// The bank: finished posts that did not get a daily slot. Run one in any quiet hour, or when a gated post is not ready.
export const RESERVE = ['SY6', 'MG3', 'MG4', 'EX2', 'EX3', 'CS1', 'CS2', 'CS4', 'WY3', 'WY4', 'FT2', 'SJ6', 'SJ7', 'SJ8', 'RV2', 'RV3', 'RV4', 'RV5', 'RV6', 'MT5', 'MT6', 'TT9', 'CL3'];
