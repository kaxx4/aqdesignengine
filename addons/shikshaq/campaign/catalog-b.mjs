// The campaign catalog, part two: characters, subjects, who made it, proof, tutors, season, close, covers, WhatsApp squares.
import { C, subjectPalette, textOn } from '../src/tokens.mjs';
import { L, mk, slides } from './catalog-a.mjs';

const FREE = 'Free for families';
const ORIGIN = 'Made by AquaTerra, an NGO whose team are students.';

// ---- Family 5: character stories ------------------------------------------------------------------------------------------
export const char = [
  mk('MB1', 'char', 'S', 'mood', 'orange', { mood: 'rough', lines: L('Exams soon. / *No tutor yet.*'), support: 'Asking around is slow.', aud: 'students' }),
  mk('MB2', 'char', 'S', 'mood', 'orange', { mood: 'meh', lines: L('Asked around. / *Got a number* / *that does not work.*'), aud: 'students', rot: 6 }),
  mk('MB3', 'char', 'S', 'mood', 'indigo', { mood: 'fine', lines: L('Search by / *subject, class,* / *board and area.*'), aud: 'students', rot: -6 }),
  mk('MB4', 'char', 'S', 'mood', 'mint', { mood: 'good', lines: L('Found a tutor / *near you.*'), support: 'Read the profile and the reviews first.', aud: 'students' }),
  mk('MB5', 'char', 'S', 'mood', 'orange', { mood: 'great', lines: L('Message sent. / *Now it is* / *their turn.*'), aud: 'students', rot: 4 }),
  mk('EY1', 'char', 'S', 'eyes', 'orange', { lines: L('Looking for a / *tutor?*'), support: 'Search by subject, class, board and area.', cta: 'Search at shikshaq.in', aud: 'students' }),
  mk('EY2', 'char', 'S', 'eyes', 'indigo', { lines: L('Maths? Science? / *English?*'), support: 'Pick your subject. Find your tutor.', cta: 'Pick your subject', aud: 'students' }),
  mk('EY3', 'char', 'S', 'button', 'indigo', { lead: 'Found one you like?', button: 'Message your tutor', badge: 'No middleman', body: 'One tap opens WhatsApp.', aud: 'students' }),
  mk('IN1', 'char', 'S', 'poll', 'orange', { lines: L('What did you think / *Shikshaq was?*'), mascot: true, aud: 'students', sticker: 'Poll: Where you find a tutor | A charity | A coaching centre | Not sure' }),
  mk('IN2', 'char', 'S', 'poll', 'indigo', { lines: L('Which subject do / *you need a tutor for?*'), mascot: true, aud: 'students', sticker: 'Poll: Maths | Science | English | Commerce' }),
  mk('IN3', 'char', 'S', 'poll', 'mint', { lines: L('Ask us anything / *about finding a tutor.*'), mascot: true, aud: 'students', sticker: 'Question box sticker' }),
  mk('IN4', 'char', 'S', 'poll', 'orange', { lines: L('Did you show / *your parents?*'), mascot: true, aud: 'students', sticker: 'Poll: Yes | Not yet' }),
  mk('BB1', 'char', 'F', 'bento', 'orange', { copy: { plain: 'Find your', bold: 'tutor.', sub: 'Search by subject, class, board and area. Message the tutor yourself.' }, cta: 'Find your tutor', aud: 'all' }),
];

// ---- Family 6: subject posters (the eight-subject palette) -----------------------------------------------------------------
const SUBJ = [['Maths', 'arch', 'great'], ['Science', 'sun'], ['English', 'lobe'], ['Commerce', 'arch', 'good'], ['Computer', 'sun'], ['Hindi', 'arch', 'fine'], ['History', 'lobe'], ['Geography', 'arch', 'good']];
export const subjects = SUBJ.map(([s, kind, mood], i) => {
  const p = subjectPalette(s);
  return mk(`SJ${i + 1}`, 'subjects', 'F', 'plate', ['orange', 'indigo', 'mint'][i % 3], {
    subject: s, kicker: 'Classes IV to XII', kickFill: p.solid, lines: [['Find your'], [{ tag: s, fill: p.solid }], ['tutor.']],
    support: 'Search by class, board and area.', mascot: { kind, mood, fill: kind === 'arch' ? p.solid : kind === 'sun' ? '#FFC700' : p.solid }, cta: 'shikshaq.in', aud: 'students',
  });
});

// ---- Family 7: who made it ---------------------------------------------------------------------------------------------
export const who = [
  ...slides('WM1', 'who', 'F', 'orange', [
    { look: 'plate', ground: 'panel', lines: L('A [student team,] / building the list / Kolkata never had.'), mascot: { kind: 'sun', fill: '#FFC700' } },
    { look: 'bands', q: 'Who is behind Shikshaq?', a: 'AquaTerra.', foot: 'An NGO whose team are students.', mascot: true },
    { look: 'plate', accent: 'mint', kicker: 'For families', lines: L('Free for / [families.]'), support: 'You search, you read, and you message the tutor yourself.', mascot: { kind: 'arch', mood: 'good' } },
    { look: 'bands', accent: 'indigo', q: 'Is it a charity or a class?', a: 'Neither.', foot: 'It is where you find your tutor.', mascot: true },
    { look: 'button', accent: 'orange', lead: 'Find yours.', button: 'Find your tutor', badge: FREE, body: 'shikshaq.in. Classes IV to XII.' },
  ]),
  mk('WM2', 'who', 'S', 'plate', 'orange', { ground: 'panel', lines: L('A [student team,] / building the list / Kolkata never had.'), mascot: { kind: 'sun', fill: '#FFC700' }, cta: 'shikshaq.in' }),
  mk('WM3', 'who', 'S', 'bands', 'orange', { q: 'Who is behind Shikshaq?', a: 'AquaTerra.', foot: 'An NGO whose team are students.', mascot: true }),
  mk('WM4', 'who', 'S', 'card', 'indigo', { scheme: 'ink', small: 'How we work', lines: ['No', 'commission.'], foot: 'You pay the tutor directly.' }),
];

// ---- Family 8: proof. Gated on real reviews and tutor approval. Copy comes from data.json, never from here. ----------------
const rv = (id, canvas, idx, accent) => mk(id, 'proof', canvas, 'review', accent, { bind: { review: idx }, sticker: 'A real review', cta: 'Read more reviews', aud: 'parents', gated: true });
export const proof = [
  ...[0, 1, 2, 3, 4, 5].map(i => rv(`RV${i + 1}`, 'F', i, ['orange', 'indigo', 'mint'][i % 3])),
  ...slides('RV7', 'proof', 'F', 'indigo', [0, 1, 2, 3, 4].map(i => ({ look: 'review', bind: { review: i }, sticker: 'A real review', cta: i === 4 ? 'Read more reviews' : null, gated: true })), 'parents'),
  ...[0, 1, 2].map(i => rv(`RV${8 + i}`, 'S', i, ['orange', 'indigo', 'mint'][i])),
  ...[0, 1, 2].map(i => mk(`MT${i + 1}`, 'proof', 'S', 'tutor', 'orange', { bind: { tutor: i }, cta: 'See the profile', aud: 'all', gated: true })),
  ...[0, 1, 2].map(i => mk(`MT${i + 4}`, 'proof', 'F', 'tutor', 'orange', { bind: { tutor: i }, cta: 'See the profile', aud: 'all', gated: true })),
];

// ---- Family 9: tutor side ------------------------------------------------------------------------------------------------
const tutorChats = [
  { n: 7, lines: L('The first / [message.]'), msgs: [{ who: 'P', t: 'Hello, is the Maths slot on Saturday free for Class IX?' }, { who: 'S', t: 'Yes. Tell me the board and what he finds hard.' }, { who: 'P', t: 'ICSE. Algebra.' }, { who: 'S', t: 'Good. Let us fix a time that works for you.' }] },
  { n: 8, lines: L('What is / your [fee?]'), msgs: [{ who: 'P', t: 'What is your fee?' }, { who: 'S', t: 'I set my own rate. It depends on the class and how many days.' }, { who: 'P', t: 'Can we agree it here?' }, { who: 'S', t: 'Yes. You and I decide it together.' }] },
  { n: 9, lines: L('Do you / [come] home?'), msgs: [{ who: 'P', t: 'Do you teach near Behala?' }, { who: 'S', t: 'I teach students near me. Send me your locality.' }, { who: 'P', t: 'Sending it now.' }] },
];
export const tutors = [
  ...slides('TT1', 'tutors', 'F', 'orange', [
    { look: 'plate', kicker: 'For tutors', lines: L('Teach on / {Shikshaq.}'), support: 'Put your profile where students are searching.', mascot: { kind: 'sun', fill: '#FFC700' } },
    { look: 'card', scheme: 'orange', small: 'Step one', lines: ['Fill', 'out a', 'form.'], foot: 'It takes a few minutes.' },
    { look: 'card', accent: 'indigo', scheme: 'indigo', small: 'Step two', lines: ['We', 'check.'], foot: 'Our team checks your background.' },
    { look: 'card', accent: 'mint', scheme: 'ink', small: 'Step three', lines: ['You are', 'listed.'], foot: 'Students and parents message you on WhatsApp.' },
    { look: 'button', lead: 'Free to list.', button: 'Apply to teach', badge: 'Your rate', body: 'You set your own rate and keep all of it.' },
  ], 'tutors'),
  mk('TT2', 'tutors', 'S', 'plate', 'orange', { kicker: 'For tutors', lines: L('Teach on / {Shikshaq.}'), support: 'Put your profile where students are searching.', mascot: { kind: 'sun', fill: '#FFC700' }, cta: 'Apply to teach', aud: 'tutors' }),
  mk('TT3', 'tutors', 'S', 'card', 'orange', { scheme: 'orange', small: 'For tutors', lines: ['Free', 'to list.'], foot: 'You set your own rate and keep all of it.', aud: 'tutors' }),
  mk('TT4', 'tutors', 'S', 'brief', 'orange', { ground: 'panel', title: 'List in three steps', rows: [{ pre: 'Fill out a', hl: 'form.' }, { pre: 'Our team', hl: 'checks', post: 'your background.' }, { pre: 'If you are selected, you are', hl: 'listed.' }], note: 'Free', cta: 'Apply to teach', aud: 'tutors' }),
  mk('TT5', 'tutors', 'S', 'button', 'orange', { lead: 'Students are searching.', button: 'Apply to teach', badge: 'Free to list', body: 'Real people message you on WhatsApp. Not sold leads.', aud: 'tutors' }),
  mk('TT6', 'tutors', 'F', 'plate', 'orange', { lines: L('Your students / are {searching.}'), support: 'Put your profile where they look.', mascot: { kind: 'arch', mood: 'great' }, cta: 'Apply to teach', aud: 'tutors' }),
  ...tutorChats.map(c => mk(`TT${c.n}`, 'tutors', 'F', 'chat', 'orange', { lines: c.lines, msgs: c.msgs, count: `0${c.n - 6}/03`, names: { S: 'Tutor', P: 'Parent' }, aud: 'tutors' })),
  mk('RC1', 'tutors', 'F', 'plate', 'orange', { kicker: 'Students, this one is for you', lines: L('Know a good / [tutor?] / {Recommend them.}'), support: 'Your own teacher can be on Shikshaq too.', mascot: { kind: 'lobe', fill: '#5B7BD9' }, cta: 'Recommend a tutor', aud: 'students' }),
  mk('RC2', 'tutors', 'S', 'plate', 'orange', { kicker: 'Students', lines: L('Know a good / [tutor?] / {Recommend them.}'), support: 'Your own teacher can be on Shikshaq too.', mascot: { kind: 'lobe', fill: '#5B7BD9' }, cta: 'Recommend a tutor', aud: 'students' }),
  mk('RC3', 'tutors', 'S', 'eyes', 'indigo', { lines: L('Is your tutor / *on Shikshaq?*'), support: 'If not, recommend them.', cta: 'Recommend a tutor', aud: 'students' }),
];

// ---- Family 10: season and calendar ---------------------------------------------------------------------------------------
const cal = (id, lines, notes, accent) => ['F', 'S'].map(cv => mk(`${id}${cv === 'S' ? 's' : ''}`, 'season', cv, 'calendar', accent, { lines: L(lines), notes, label: 'An example week', cta: 'Find a slot', aud: 'students' }));
export const season = [
  ...cal('CL1', 'Your week / *with a tutor.*', [{ col: 0, row: 0, t: 'Maths' }, { col: 3, row: 0, t: 'English' }, { col: 5, row: 1, t: 'Doubts' }, { col: 1, row: 1, t: 'Science' }], 'indigo'),
  ...cal('CL2', 'Puja break, / *sorted.*', [{ col: 0, row: 0, t: 'One weak chapter' }, { col: 3, row: 0, t: 'Doubt class' }, { col: 4, row: 1, t: 'Rest day' }, { col: 1, row: 1, t: 'Revise it' }], 'orange'),
  ...cal('CL3', 'Before the / *exams.*', [{ col: 0, row: 0, t: 'Revision slot' }, { col: 3, row: 0, t: 'Doubts' }, { col: 5, row: 1, t: 'Last check' }, { col: 1, row: 1, t: 'Weak topic' }], 'mint'),
];

// ---- Family 11: week 4 close ----------------------------------------------------------------------------------------------
export const close = [
  ...slides('RP1', 'close', 'F', 'indigo', [
    { look: 'calendar', lines: L('Four weeks / *of Shikshaq.*'), notes: [{ col: 0, row: 0, t: 'Search', span: 1.9 }, { col: 2.4, row: 0, t: 'Read', span: 1.9 }, { col: 4.8, row: 0, t: 'Message', span: 1.9 }, { col: 1, row: 1, t: 'Ask your parents', span: 2.6 }], label: 'The short version' },
    { look: 'plate', accent: 'indigo', lines: L('Shikshaq is / where you / [find] your / {tutor.}'), support: 'Connecting every student in Kolkata to teachers.', mascot: { kind: 'sun', fill: '#FFC700' } },
    { look: 'brief', ground: 'panel', title: 'Three steps', rows: [{ pre: 'Search by', hl: 'subject, class, board and area.' }, { pre: 'Read the', hl: 'profile and the reviews.' }, { pre: 'Message the tutor on', hl: 'WhatsApp.' }], note: 'Free' },
    { look: 'bands', accent: 'orange', q: 'Is it a charity?', a: 'Not a charity. Not a class.', foot: ORIGIN, mascot: true },
    { look: 'card', accent: 'mint', scheme: 'bone', small: 'The tutors', lines: ['Checked', 'and', 'selected.'], foot: 'Our team checks every tutor.' },
    { look: 'plate', accent: 'orange', kicker: 'For tutors', lines: L('Teach on / {Shikshaq.}'), support: 'Free to list. Set your own rate.', mascot: { kind: 'arch', mood: 'great' } },
    { look: 'button', accent: 'orange', lead: 'Your move.', button: 'Find your tutor', badge: FREE, body: 'shikshaq.in. Show this to a parent.' },
  ]),
  mk('RP2', 'close', 'S', 'button', 'indigo', { lead: 'Students,', button: 'Find your tutor', badge: FREE, body: 'Search, read, message. Then show a parent.', aud: 'students' }),
  mk('RP3', 'close', 'S', 'button', 'orange', { lead: 'Parents,', button: 'Message a tutor', badge: FREE, body: 'Fees go straight to the tutor. No commission.', aud: 'parents' }),
  mk('RP4', 'close', 'S', 'button', 'mint', { lead: 'Tutors,', button: 'Apply to teach', badge: 'Free to list', body: 'Set your own rate and keep all of it.', aud: 'tutors' }),
  mk('RP5', 'close', 'Q', 'plate', 'indigo', { lines: L('Shikshaq is / where you / [find] your / {tutor.}'), support: 'Send this to someone looking for a tutor.', cta: 'shikshaq.in', aud: 'all' }),
];

// ---- Family 12: highlight covers --------------------------------------------------------------------------------------------
export const covers = [
  mk('HC1', 'covers', 'C', 'cover', 'indigo', { label: 'How it works', mood: 'fine', disc: C.indigoTint }),
  mk('HC2', 'covers', 'C', 'cover', 'orange', { label: 'Who made it', char: 'sun', disc: C.orangeTint }),
  mk('HC3', 'covers', 'C', 'cover', 'mint', { label: 'Reviews', mood: 'great', disc: C.mint, gated: true }),
];

// ---- Family 14: WhatsApp squares (one per broadcast, forward-ready) ------------------------------------------------------------
export const wq = [
  mk('WQ1', 'wa', 'Q', 'plate', 'indigo', { lines: L('Find a [tutor] / for your / {child.}'), support: 'Search by subject, class, board and area.', cta: 'shikshaq.in', aud: 'parents' }),
  mk('WQ2', 'wa', 'Q', 'plate', 'orange', { lines: L('Show this / to your / {parents.}'), support: 'Shikshaq is where you find your tutor.', cta: 'shikshaq.in', aud: 'students' }),
  mk('WQ3', 'wa', 'Q', 'plate', 'orange', { lines: L('Teach on / {Shikshaq.}'), support: 'Free to list. Set your own rate.', cta: 'Apply to teach', aud: 'tutors' }),
  mk('WQ4', 'wa', 'Q', 'plate', 'mint', { lines: L('Free for / [families.]'), support: 'No commission. Fees go straight to the tutor.', cta: 'shikshaq.in', aud: 'parents' }),
  mk('WQ5', 'wa', 'Q', 'plate', 'indigo', { lines: L('Every tutor is / [checked] and / {selected.}'), support: 'By our team, before they are listed.', cta: 'shikshaq.in', aud: 'parents' }),
  mk('WQ6', 'wa', 'Q', 'plate', 'orange', { lines: L('Know a good / [tutor?]'), support: 'Recommend them to Shikshaq.', cta: 'Recommend a tutor', aud: 'students' }),
];
