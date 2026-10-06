// The four-week plan. Entries are asset ids or POST ids (a post id expands to every slide). One feed post a day,
// stories through the day, WhatsApp pushes by id (see wa.mjs). Reserve posts swap in when a gated post is not ready.
export const WEEKS = [
  { n: 1, theme: 'DEFINE: what it is', days: [
    { d: 'Mon', feed: 'H1', stories: ['FQ0', 'FQ1', 'FQ2', 'FQ3', 'H2'], wa: ['WP1'] },
    { d: 'Tue', feed: 'B2', stories: ['FQ4', 'FQ5', 'FQ6', 'FQ7', 'FQ8', 'HC1'], wa: ['WP2'] },
    { d: 'Wed', feed: 'CH1', stories: ['B1', 'PF1'], wa: [] },
    { d: 'Thu', feed: 'H3', stories: ['PF2', 'PF3', 'MB1', 'MB2'], wa: ['WP3'] },
    { d: 'Fri', feed: 'SJ1', stories: ['MB3', 'IN1'], wa: ['WP4'] },
    { d: 'Sat', feed: 'FQ9', stories: ['CH1s'], wa: [] },
    { d: 'Sun', feed: 'CL1', stories: [], wa: [], note: 'Read the numbers. Re-ask three interviewees. Adjust week 2.' },
  ] },
  { n: 2, theme: 'SHOW AND ANSWER: the student tells the parent', days: [
    { d: 'Mon', feed: 'B3', stories: ['CH2s', 'MB4'], wa: ['WP5'] },
    { d: 'Tue', feed: 'CH2', stories: ['CH3s', 'EY1'], wa: ['WP6'] },
    { d: 'Wed', feed: 'SJ2', stories: ['CH4s', 'MB5'], wa: [] },
    { d: 'Thu', feed: 'PF5', stories: ['CH5s', 'EY2'], wa: ['WP7'] },
    { d: 'Fri', feed: 'CH3', stories: ['IN2', 'EY3'], wa: [] },
    { d: 'Sat', feed: 'SJ3', stories: ['CL1s', 'CL2s'], wa: ['WP8'] },
    { d: 'Sun', feed: 'CL2', stories: ['CL3s'], wa: [], note: 'Read the numbers. Re-ask the interviewees.' },
  ] },
  { n: 3, theme: 'PROOF AND BOTH SIDES', days: [
    { d: 'Mon', feed: 'WM1', stories: ['WM2', 'WM3', 'WM4', 'HC2'], wa: ['WP9'] },
    { d: 'Tue', feed: 'RV1', stories: ['RV8', 'RV9', 'RV10', 'HC3'], wa: ['WP10'], note: 'Gated on real reviews. If not ready, swap in SJ5.' },
    { d: 'Wed', feed: 'TT1', stories: ['TQ0', 'TQ1', 'TQ2', 'TQ3', 'TQ4', 'TQ5', 'TQ6'], wa: [] },
    { d: 'Thu', feed: 'CH4', stories: ['TT2', 'TT3', 'TT4', 'TT5'], wa: ['WP11'] },
    { d: 'Fri', feed: 'MT4', stories: ['MT1', 'MT2', 'MT3'], wa: [], note: 'Gated on tutor approval. If not ready, swap in SJ6.' },
    { d: 'Sat', feed: 'BB1', stories: ['RC2', 'RC3', 'IN3'], wa: ['WP12'] },
    { d: 'Sun', feed: 'TT7', stories: [], wa: [], note: 'Read the numbers. Re-ask the interviewees.' },
  ] },
  { n: 4, theme: 'YOUR MOVE', days: [
    { d: 'Mon', feed: 'TT6', stories: ['RP2'], wa: ['WP13'] },
    { d: 'Tue', feed: 'CH5', stories: ['RP3'], wa: ['WP14'], rerun: ['FQ1', 'FQ2', 'FQ3'] },
    { d: 'Wed', feed: 'RC1', stories: ['RP4'], wa: [], rerun: ['CH2s'] },
    { d: 'Thu', feed: 'SJ4', stories: [], wa: ['WP15'], rerun: ['best performing story from weeks 1 to 3'] },
    { d: 'Fri', feed: 'RV7', stories: ['IN4'], wa: [], rerun: ['B1'], note: 'Gated on real reviews. If not ready, swap in SJ7.' },
    { d: 'Sat', feed: 'RP1', stories: [], wa: ['WP16'], rerun: ['best performing story'] },
    { d: 'Sun', feed: 'TT8', stories: [], wa: [], note: 'Final read of the numbers against the baseline. Debrief.' },
  ] },
];
export const RESERVE = ['PF4', 'SJ5', 'SJ6', 'SJ7', 'SJ8', 'RV2', 'RV3', 'RV4', 'RV5', 'RV6', 'MT5', 'MT6', 'TT9', 'CL3'];
