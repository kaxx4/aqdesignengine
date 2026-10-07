// Catalog v3, part two: subjects, who made it, proof, tutors, season, close, covers, WhatsApp squares, and the new series.
import { subjectPalette, textOn } from '../src/tokens.mjs';
import { L, mk, slides, ORIGIN, FREE } from './catalog-util.mjs';

const EYES = { kind: 'eyes' }, SMILE = { kind: 'smile' }, SUN = { kind: 'sun' }, LOBE = { kind: 'lobe' };
const H = o => ({ type: 'head', fill: 'card', grow: .9, ...o });

// ---- Subject posters (the eight-subject palette) ----------------------------------------------------------------------------------------
const SUBJ = [
  ['Maths', 'Stuck on the same sum / since Tuesday?', { kind: 'arch', mood: 'great' }],
  ['Science', 'Why does it work? / Ask someone who / will explain.', SUN],
  ['English', 'Write it properly. / Then write it / better.', LOBE],
  ['Commerce', 'Debit, credit, and one / doubt you keep / saving for later.', { kind: 'arch', mood: 'good' }],
  ['Computer', 'The code runs. / The exam answer / does not. Fix that.', SUN],
  ['Hindi', 'Vyakaran, but / make it make / sense.', { kind: 'arch', mood: 'fine' }],
  ['History', 'Dates stick when / someone tells you / the story.', LOBE],
  ['Geography', 'Maps, rivers, and a / tutor who draws / them for you.', { kind: 'arch', mood: 'good' }],
];
const subj = (cv, i) => { const [s, hook, m] = SUBJ[i], p = subjectPalette(s); return mk(`SJ${cv === 'S' ? 's' : ''}${i + 1}`, 'subjects', cv, ['orange', 'indigo', 'mint'][i % 3], [
  { type: 'head', fill: p.tint, eyebrow: `${s} tutors in Kolkata`, eyebrowC: p.text, lines: hook.split(' / ').map((t, li, a) => li === a.length - 1 ? [{ b: t, c: p.text }] : [t]), size: cv === 'S' ? 112 : 104, grow: 1.3, mascot: { ...m, fill: m.kind === 'arch' ? p.solid : m.kind === 'lobe' ? p.solid : undefined, size: 300 } },
  { type: 'chips', fill: 'card', eyebrow: 'Search by', chips: ['Class', 'Board', 'Area'], csize: 52, grow: .8 },
  { type: 'cta', fill: p.solid, lines: [['Find your'], [{ b: s, c: textOn(p.solid) }], ['tutor.']], button: 'shikshaq.in', size: 100, mascot: { kind: 'smile', fill: '#FFFFFF', size: 300 }, grow: 1.4 },
], { aud: 'students', subject: s, post: `SJ${cv === 'S' ? 's' : ''}${i + 1}` }); };
export const subjects = [...SUBJ.map((_, i) => subj('F', i)), ...SUBJ.map((_, i) => subj('S', i))];

// ---- Who made it (About page voice) -----------------------------------------------------------------------------------------------------------
export const who = [
  ...slides('WM1', 'who', 'F', 'orange', [
    { panels: [{ type: 'loud', fill: 'panel', lines: L('A student team, / building the list / Kolkata never had.'), mascot: { kind: 'eyes' }, msize: 300, size: 118 }] },
    { accent: 'orange', panels: [H({ eyebrow: 'How this started', lines: L('Finding a teacher / still runs on / *hearsay*'), size: 112, grow: 1 }), { type: 'tile', fill: 'orangeTint', icon: 'phone', label: 'And a phone number', lines: L('that may not / even *work*.'), size: 96, grow: 1 }] },
    { accent: 'indigo', panels: [{ type: 'answer', fill: 'indigo', eyebrow: 'So we built the boring version', lines: L('Fee, boards / and area, written / down first.'), sub: 'Then straight to WhatsApp.', mascot: { ...SUN, size: 320 }, size: 118 }] },
    { accent: 'orange', panels: [{ type: 'answer', fill: 'orange', eyebrow: 'No commission', lines: L('Because the moment / we take one, we / start having / opinions.'), sub: 'About who you should pick.', mascot: { ...EYES, size: 320 }, size: 104 }] },
    { accent: 'orange', panels: [{ type: 'loud', fill: 'orange', lines: L('Find yours.'), sub: ORIGIN, button: 'shikshaq.in', mascot: SMILE, msize: 340 }] },
  ], 'parents'),
  mk('WM2', 'who', 'S', 'orange', [{ type: 'loud', fill: 'panel', lines: L('A student team, / building the list / Kolkata never had.'), sub: ORIGIN, button: 'shikshaq.in', mascot: { kind: 'eyes' }, msize: 440 }], { aud: 'parents' }),
  mk('WM3', 'who', 'S', 'orange', [
    H({ eyebrow: 'How this started', lines: L('Finding a teacher / still runs on / *hearsay*'), size: 118, grow: 1 }),
    { type: 'tile', fill: 'orangeTint', icon: 'phone', label: 'And a phone number', lines: L('that may not / even *work*.'), size: 100, mascot: { ...EYES, size: 340 }, grow: 1 },
    { type: 'pills', runs: ['So we built the', { t: 'boring version', fill: 'orange' }, ': fee, boards and area written down before you contact anyone, then', { t: 'straight to WhatsApp', fill: 'indigo' }, '.'], psize: 54, grow: 1.4 },
  ], { aud: 'parents' }),
  mk('WM4', 'who', 'S', 'indigo', [
    H({ eyebrow: 'No commission', lines: L('Why we take / *nothing*'), size: 124, grow: .8 }),
    { type: 'answer', fill: 'indigo', lines: L('The moment we take / one, we start / having opinions.'), sub: 'About who you should pick.', mascot: { ...SUN, size: 360 }, size: 120, grow: 1.8 },
    { type: 'bento', fill: 'bone', tiles: [{ label: 'Commission', big: '₹0', fill: 'card', icon: 'heart' }, { label: 'Invoices', big: 'None', fill: 'orange', icon: 'file' }], grow: 1 },
  ], { aud: 'parents' }),
];

// ---- Proof (gated: copy comes from data.json; the panel only says where it goes) -------------------------------------------------
const rv = (id, cv, i, ac) => mk(id, 'proof', cv, ac, [
  H({ eyebrow: 'A real review', lines: L('From a student / who *messaged* them'), size: 104, grow: .8 }),
  { type: 'quote', bind: 'review', grow: 2.2 },
  { type: 'pills', runs: ['Every review comes from a student who actually', { t: 'messaged the teacher', fill: 'orange' }, '.'], psize: 48, grow: .8 },
], { bind: { review: i }, gated: true, aud: 'parents' });
export const proof = [
  ...[0, 1, 2, 3, 4, 5].map(i => rv(`RV${i + 1}`, 'F', i, ['orange', 'indigo', 'mint'][i % 3])),
  ...slides('RV7', 'proof', 'F', 'indigo', [0, 1, 2, 3, 4].map(i => ({ panels: [H({ eyebrow: 'A real review', lines: L('From a student / who *messaged* them'), size: 104, grow: .8 }), { type: 'quote', bind: 'review', grow: 2.4 }], o: { bind: { review: i }, gated: true } })), 'parents'),
  ...[0, 1, 2].map(i => rv(`RV${8 + i}`, 'S', i, ['orange', 'indigo', 'mint'][i])),
  ...[0, 1, 2].map(i => mk(`MT${i + 1}`, 'proof', 'S', 'orange', [H({ eyebrow: 'Meet a tutor', lines: L('On *Shikshaq*'), size: 120, grow: .5 }), { type: 'tutor', bind: 'tutor', grow: 3 }], { bind: { tutor: i }, gated: true, aud: 'all' })),
  ...[0, 1, 2].map(i => mk(`MT${i + 4}`, 'proof', 'F', 'orange', [H({ eyebrow: 'Meet a tutor', lines: L('On *Shikshaq*'), size: 110, grow: .5 }), { type: 'tutor', bind: 'tutor', grow: 3 }], { bind: { tutor: i }, gated: true, aud: 'all' })),
];

// ---- Tutor side ------------------------------------------------------------------------------------------------------------------------------------
const TC = [
  { n: 7, lines: L('The first / *message*'), msgs: [{ who: 'P', t: 'Hello, is the Maths slot on Saturday free for Class 9?' }, { who: 'S', t: 'Yes. Tell me the board and what he finds hard.' }, { who: 'P', t: 'ICSE. Algebra.' }, { who: 'S', t: 'Good. Let us fix a time that works for you.' }] },
  { n: 8, lines: L('What is / your *fee*?'), msgs: [{ who: 'P', t: 'What is your fee?' }, { who: 'S', t: 'I set my own rate. It depends on the class and how many days.' }, { who: 'P', t: 'Can we agree it here?' }, { who: 'S', t: 'Yes. You and I decide it together.' }] },
  { n: 9, lines: L('Do you / *come* home?'), msgs: [{ who: 'P', t: 'Do you teach near Salt Lake?' }, { who: 'S', t: 'I teach students near me. Send me your locality.' }, { who: 'P', t: 'Sending it now.' }] },
];
export const tutors = [
  ...slides('TT1', 'tutors', 'F', 'orange', [
    { panels: [{ type: 'loud', fill: 'orange', lines: L('Teach on / Shikshaq.'), sub: 'Put your profile where students are searching.', button: 'For tutors', mascot: SMILE, msize: 340 }] },
    { panels: [H({ eyebrow: 'How to join', lines: L('One form, / *three steps*'), size: 112, grow: .8 }), { type: 'steps', fill: 'orange', lines: L('Apply, get checked, / get listed'), rows: [{ icon: 'edit', t: 'Apply', b: 'A five-step form.' }, { icon: 'shield', t: 'Get checked', b: 'ID and degree, by a human.' }, { icon: 'users', t: 'Get listed', b: 'Reviewed in about three working days.' }], grow: 2 }] },
    { accent: 'indigo', panels: [{ type: 'answer', fill: 'indigo', eyebrow: 'Keep every rupee', lines: L('You set / the rate. / We take / nothing.'), sub: 'There is no listing fee either.', mascot: { ...SUN, size: 320 }, size: 124 }] },
    { panels: [H({ eyebrow: 'What you get', lines: L('Real students, / *no bidding*'), size: 112, grow: .9 }), { type: 'bento', fill: 'bone', tiles: [{ label: 'Listing fee', big: 'None', fill: 'card', icon: 'heart', h: 230 }, { label: 'Lead credits', big: 'None', fill: 'orange', icon: 'file', h: 230 }, { label: 'Enquiries', big: 'WhatsApp', fill: 'indigo', icon: 'chat', h: 230, size: 78 }, { label: 'Paid placement', big: 'Never', fill: 'mint', icon: 'shield', h: 230 }], grow: 1.8 }] },
    { panels: [{ type: 'loud', fill: 'orange', lines: L('Free to list.'), sub: 'We were students in this city. The platform is built for how tuition actually works in Kolkata.', button: 'Apply to teach', mascot: SMILE, msize: 300 }] },
  ], 'tutors'),
  mk('TT2', 'tutors', 'S', 'orange', [{ type: 'loud', fill: 'orange', lines: L('Teach on / Shikshaq.'), sub: 'Put your profile where students are searching.', button: 'For tutors', mascot: SMILE, msize: 460 }], { aud: 'tutors' }),
  mk('TT3', 'tutors', 'S', 'indigo', [
    H({ eyebrow: 'For tutors', lines: L('Keep every / *rupee*'), size: 130, grow: .9 }),
    { type: 'answer', fill: 'indigo', lines: L('You set the rate. / We take nothing.'), sub: 'There is no listing fee either.', mascot: { ...SUN, size: 380 }, grow: 1.6 },
    { type: 'tile', fill: 'indigoTint', icon: 'heart', label: 'Built by students', lines: L('We were students / in this *city*.'), size: 80, grow: 1 },
  ], { aud: 'tutors' }),
  mk('TT4', 'tutors', 'S', 'orange', [
    H({ eyebrow: 'How to join', lines: L('Apply. Get checked. / *Get listed*.'), size: 108, grow: .8 }),
    { type: 'steps', fill: 'orange', lines: L('Three steps'), rows: [{ icon: 'edit', t: 'Apply', b: 'A five-step form.' }, { icon: 'shield', t: 'Get checked', b: 'ID and degree, by a human.' }, { icon: 'users', t: 'Get listed', b: 'Reviewed in about three working days.' }], grow: 3 },
  ], { aud: 'tutors' }),
  mk('TT5', 'tutors', 'S', 'orange', [
    H({ eyebrow: 'Real students', lines: L('No leads. / No *bidding*.'), size: 124, grow: .9 }),
    { type: 'pills', runs: ['Enquiries reach you on', { t: 'WhatsApp', fill: 'orange' }, '. Real reviews from real students, and', { t: 'no paid placement', fill: 'indigo' }, 'in results. Ever.'], psize: 58, grow: 1.6 },
    { type: 'cta', fill: 'orange', lines: L('Free to list.'), button: 'Apply to teach', size: 110, mascot: { ...EYES, size: 340 }, grow: 1 },
  ], { aud: 'tutors' }),
  mk('TT6', 'tutors', 'F', 'orange', [
    H({ eyebrow: 'For tutors', lines: L('Your students / are *searching*'), size: 120, mascot: { ...EYES, size: 280 }, grow: 1.1 }),
    { type: 'tile', fill: 'orangeTint', icon: 'users', label: 'Put your profile where they look', lines: L('*Free* to list.'), size: 110, grow: 1 },
    { type: 'cta', fill: 'orange', lines: L('Apply to teach.'), button: 'shikshaq.in', size: 96, grow: .9 },
  ], { aud: 'tutors' }),
  ...TC.map(c => mk(`TT${c.n}`, 'tutors', 'F', 'orange', [
    H({ eyebrow: 'A parent asks', lines: c.lines, size: 116, grow: .7 }),
    { type: 'chat', fill: 'tint', msgs: c.msgs, fs: 46, grow: 2 },
  ], { count: `0${c.n - 6}/03`, aud: 'tutors' })),
  mk('RC1', 'tutors', 'F', 'orange', [
    H({ eyebrow: 'Students, this one is for you', lines: L('Know a good / *teacher*?'), size: 124, mascot: { ...LOBE, size: 280 }, grow: 1.1 }),
    { type: 'tile', fill: 'orangeTint', icon: 'heart', label: 'Recommend them', lines: L('We will reach out / and get them *listed*, / free.'), size: 78, grow: 1.3 },
    { type: 'cta', fill: 'orange', lines: L('Three fields. / We verify first.'), button: 'Recommend a tutor', size: 80, grow: 1 },
  ], { aud: 'students' }),
  mk('RC2', 'tutors', 'S', 'orange', [
    H({ eyebrow: 'Students', lines: L('Know a good / *teacher*?'), size: 130, mascot: { ...LOBE, size: 340 }, grow: 1 }),
    { type: 'steps', fill: 'orange', lines: L('Recommend them'), rows: [{ icon: 'edit', t: 'Three fields', b: 'Name, subject and area.' }, { icon: 'shield', t: 'We verify first', b: 'Before anything goes live.' }, { icon: 'users', t: 'They get listed', b: 'Free. We reach out this week.' }], grow: 2.4 },
  ], { aud: 'students' }),
  mk('RC3', 'tutors', 'S', 'indigo', [{ type: 'loud', fill: 'indigo', lines: L('Is your tutor / on Shikshaq?'), sub: 'If not, recommend them. It is free.', button: 'Recommend a tutor', mascot: { kind: 'eyes', fill: '#FFFFFF' }, msize: 420 }], { aud: 'students' }),
];

// ---- Season -------------------------------------------------------------------------------------------------------------------------------------------
const CAL = (id, accent, eyebrow, lines, notes, rows = 2) => ['F', 'S'].map(cv => mk(`${id}${cv === 'S' ? 's' : ''}`, 'season', cv, accent, [
  H({ eyebrow, lines, size: 116, grow: .8 }),
  { type: 'calendar', fill: 'tint', rows: cv === 'S' ? rows + 1 : rows, notes, foot: 'An example week. Agree your own slots with your tutor.', grow: 2.2 },
], { aud: 'students' }));
export const season = [
  ...CAL('CL1', 'indigo', 'Your week', L('A week / *with a tutor*'), [{ col: 0, row: 0, t: 'Maths' }, { col: 3, row: 0, t: 'English' }, { col: 5, row: 1, t: 'Doubts' }, { col: 1, row: 1, t: 'Science' }]),
  ...CAL('CL2', 'orange', 'Pujo season', L('Puja break, / *sorted*'), [{ col: 0, row: 0, t: 'One weak chapter', span: 2.8 }, { col: 3.4, row: 0, t: 'Doubt class', span: 2.4 }, { col: 4, row: 1, t: 'Pandal day', span: 2.4 }, { col: 1, row: 1, t: 'Revise it', span: 2.2 }]),
  ...CAL('CL3', 'mint', 'Before the exams', L('Pre-boards, / *planned*'), [{ col: 0, row: 0, t: 'Revision slot', span: 2.6 }, { col: 3, row: 0, t: 'Doubts', span: 2 }, { col: 5, row: 1, t: 'Last check', span: 2 }, { col: 1, row: 1, t: 'Weak topic', span: 2.4 }]),
];

// ---- Week four close ---------------------------------------------------------------------------------------------------------------------------------
export const close = [
  ...slides('RP1', 'close', 'F', 'indigo', [
    { panels: [{ type: 'loud', fill: 'indigo', lines: L('Four weeks / of Shikshaq.'), sub: 'The short version.', mascot: { kind: 'eyes', fill: '#FFFFFF' }, msize: 320 }] },
    { accent: 'orange', panels: [{ type: 'loud', fill: 'orange', lines: L('Shikshaq is / where you find / your tutor.'), sub: 'Connecting every student in Kolkata to teachers.', mascot: SMILE, msize: 280 }] },
    { accent: 'orange', panels: [H({ eyebrow: 'The three steps', lines: L('Search. Compare. / *Message*.'), size: 112, grow: .8 }), { type: 'index', fill: 'card', rows: [{ t: 'Tell us the subject' }, { t: 'Compare real profiles' }, { t: 'Message on WhatsApp' }], grow: 2 }] },
    { accent: 'indigo', panels: [{ type: 'answer', fill: 'indigo', eyebrow: 'Is it a charity?', lines: L('Not a charity. / Not a class.'), sub: ORIGIN, mascot: { ...SUN, size: 320 }, size: 128 }] },
    { accent: 'mint', panels: [{ type: 'answer', fill: 'mint', eyebrow: 'The tutors', lines: L('Checked by / a human.'), sub: 'ID and degree, before a profile goes live.', mascot: { kind: 'arch', mood: 'good', size: 300 }, size: 128 }] },
    { accent: 'orange', panels: [{ type: 'loud', fill: 'orange', lines: L('Tutors: / free to list.'), sub: 'Set your own rate. Keep every rupee.', button: 'Apply to teach', mascot: SMILE, msize: 280 }] },
    { accent: 'orange', panels: [{ type: 'loud', fill: 'orange', lines: L('Your move.'), sub: 'Show it to a parent.', button: 'shikshaq.in', mascot: EYES, msize: 320 }] },
  ]),
  mk('RP2', 'close', 'S', 'indigo', [{ type: 'loud', fill: 'indigo', lines: L('Students,'), sub: 'Search, compare, message. Then show a parent.', button: 'shikshaq.in', mascot: { kind: 'eyes', fill: '#FFFFFF' }, msize: 480 }], { aud: 'students' }),
  mk('RP3', 'close', 'S', 'orange', [{ type: 'loud', fill: 'orange', lines: L('Parents,'), sub: 'Fees go straight to the tutor. No commission.', button: 'shikshaq.in', mascot: SMILE, msize: 480 }], { aud: 'parents' }),
  mk('RP4', 'close', 'S', 'mint', [{ type: 'loud', fill: 'mint', lines: L('Tutors,'), sub: 'Free to list. Set your own rate. Keep every rupee.', button: 'Apply to teach', mascot: { kind: 'arch', mood: 'great', fill: '#FFFFFF' }, msize: 480 }], { aud: 'tutors' }),
  mk('RP5', 'close', 'Q', 'indigo', [{ type: 'loud', fill: 'indigo', lines: L('Where you find / your tutor.'), sub: 'Send this to someone looking for one.', button: 'shikshaq.in', mascot: { kind: 'eyes', fill: '#FFFFFF' }, msize: 240, size: 130 }], { aud: 'all' }),
];

// ---- Covers ---------------------------------------------------------------------------------------------------------------------------------------------
export const covers = [
  mk('HC1', 'covers', 'C', 'indigo', [], { look: 'cover', label: 'How it works', mood: 'fine', disc: '#EDEEFF' }),
  mk('HC2', 'covers', 'C', 'orange', [], { look: 'cover', label: 'Who made it', char: 'sun', disc: '#FFF4E8' }),
  mk('HC3', 'covers', 'C', 'mint', [], { look: 'cover', label: 'Reviews', mood: 'great', disc: '#E3F7EC', gated: true }),
  mk('HC4', 'covers', 'C', 'orange', [], { look: 'cover', label: 'Parents say', mood: 'meh', disc: '#FCECDE' }),
  mk('HC5', 'covers', 'C', 'indigo', [], { look: 'cover', label: 'Ask a tutor', char: 'lobe', disc: '#EDEEFF' }),
  mk('HC6', 'covers', 'C', 'mint', [], { look: 'cover', label: 'Messages', mood: 'good', disc: '#E3F7EC' }),
  mk('HC7', 'covers', 'C', 'orange', [], { look: 'cover', label: 'Stickers', char: 'sun', disc: '#FFF4E8' }),
];

// ---- WhatsApp squares ------------------------------------------------------------------------------------------------------------------------------
const WQ = (id, ac, lines, sub, button, aud, m = 'smile') => mk(id, 'wa', 'Q', ac, [{ type: 'loud', fill: ac === 'indigo' ? 'indigo' : ac === 'mint' ? 'mint' : 'orange', lines, sub, button, mascot: { kind: m, fill: ac === 'indigo' && (m === 'eyes') ? '#FFFFFF' : undefined }, msize: 250, size: 128 }], { aud });
export const wq = [
  WQ('WQ1', 'indigo', L('Find a tutor / for your child.'), 'Subject, class, board and area.', 'shikshaq.in', 'parents', 'eyes'),
  WQ('WQ2', 'orange', L('Show this / to your parents.'), 'Shikshaq is where you find your tutor.', 'shikshaq.in', 'students'),
  WQ('WQ3', 'orange', L('Teach on / Shikshaq.'), 'Free to list. Keep every rupee.', 'Apply to teach', 'tutors', 'eyes'),
  WQ('WQ4', 'mint', L('Free for / families.'), 'No commission. Fees go to the tutor.', 'shikshaq.in', 'parents'),
  WQ('WQ5', 'indigo', L('Checked / by a human.'), 'ID and degree, before a profile goes live.', 'shikshaq.in', 'parents', 'eyes'),
  WQ('WQ6', 'orange', L('Know a good / teacher?'), 'Recommend them. It is free.', 'Recommend a tutor', 'students'),
  WQ('WQ7', 'indigo', L('Pre-boards / coming?'), 'Find a tutor before the rush.', 'shikshaq.in', 'students', 'eyes'),
  WQ('WQ8', 'mint', L('Puja break, / sorted.'), 'Book your doubt class before the pandals.', 'shikshaq.in', 'students'),
  WQ('WQ9', 'orange', L('Thank you, / Sir. Thank you, / Ma\'am.'), 'Leave a review on Shikshaq.', 'shikshaq.in', 'students'),
  WQ('WQ10', 'indigo', L('Message first. / Then decide.'), 'You talk to the tutor yourself.', 'shikshaq.in', 'parents', 'eyes'),
];

// ---- NEW: things parents say -----------------------------------------------------------------------------------------------------------------------
const SAY = [
  ['“Ask your friend’s / tutor’s number.”', L('Or *search* / for one.'), 'Subject, class and your area. Three taps, no account needed.', 'search', 'orange'],
  ['“Why another / website?”', L('Because asking / *aunties* is slow.'), 'Hearsay, and a phone number that may not even work.', 'phone', 'indigo'],
  ['“Is the tutor / even good?”', L('Read the *reviews*. / Message first.'), 'Every review comes from a student who actually messaged the teacher.', 'star', 'orange'],
  ['“Is it far / from home?”', L('Filter by *area*.'), 'Howrah, Salt Lake, Jadavpur, Bhowanipore, Ballygunge and more.', 'pin', 'mint'],
  ['“How much / will it cost?”', L('Fees are / *between you* / and the tutor.'), 'Shikshaq takes no commission. Teachers keep every rupee.', 'heart', 'orange'],
  ['“Another / coaching class?”', L('No class. A tutor / *you pick*.'), ORIGIN, 'cap', 'indigo'],
];
const sayOf = ([q, a, sub, icon, ac], i, cv) => mk(`SY${i + 1}${cv === 'S' ? 's' : ''}`, 'say', cv, ac, [
  { type: 'head', fill: 'card', eyebrow: 'Things parents say', lines: q.split(' / ').map((t, li, arr) => li === arr.length - 1 ? [{ b: t }] : [t]), size: cv === 'S' ? 118 : 108, grow: 1.1, mascot: { kind: 'sleep', size: 240 } },
  { type: 'answer', fill: ac === 'indigo' ? 'indigo' : ac === 'mint' ? 'mint' : 'orange', eyebrow: 'You say', lines: a, size: cv === 'S' ? 132 : 118, grow: 1.6, mascot: { kind: 'eyes', size: 300 } },
  { type: 'tile', fill: ac === 'indigo' ? 'indigoTint' : ac === 'mint' ? 'mintTint' : 'orangeTint', icon, label: 'Because', lines: [[{ b: sub }]], size: cv === 'S' ? 52 : 46, plainW: 600, grow: 1 },
], { aud: 'students', post: `SY${i + 1}${cv === 'S' ? 's' : ''}` });
export const say = [...SAY.map((x, i) => sayOf(x, i, 'F')), ...SAY.map((x, i) => sayOf(x, i, 'S'))];

// ---- NEW: five questions to ask a tutor ---------------------------------------------------------------------------------------------------------
const ASKQ = [
  ['Which board / and class / do you teach?', 'Check it matches yours. Boards teach differently.', 'book'],
  ['How do you / handle doubts / between classes?', 'Ask if you can message a doubt on WhatsApp.', 'chat'],
  ['Where do you / teach, and how / far is it?', 'Travel time eats study time. Filter by area.', 'pin'],
  ['How do we / agree the fee?', 'Fees are between you and the tutor. Agree it in the chat.', 'heart'],
  ['What do other / students say?', 'Read the reviews on the profile first.', 'star'],
];
export const ask = [
  ...slides('AK1', 'ask', 'F', 'indigo', [
    { panels: [{ type: 'loud', fill: 'indigo', lines: L('Five questions / before you / say yes.'), sub: 'To ask a tutor on WhatsApp.', mascot: { kind: 'eyes', fill: '#FFFFFF' }, msize: 300 }] },
    ...ASKQ.map(([q, hint, icon], i) => ({ accent: ['orange', 'indigo', 'mint', 'orange', 'indigo'][i], panels: [{ type: 'head', fill: 'card', ordinal: `0${i + 1}`, lines: q.split(' / ').map((t, li, a) => li === a.length - 1 ? [{ b: t }] : [t]), size: 108, grow: 1.4 }, { type: 'tile', fill: ['orangeTint', 'indigoTint', 'mintTint', 'orangeTint', 'indigoTint'][i], icon, label: 'A good sign', lines: [[{ b: hint }]], size: 56, plainW: 600, grow: 1 }] })),
    { accent: 'orange', panels: [{ type: 'loud', fill: 'orange', lines: L('Now go / ask.'), sub: 'Message the tutor yourself.', button: 'shikshaq.in', mascot: SMILE, msize: 300 }] },
  ], 'students'),
  ...ASKQ.map(([q, hint, icon], i) => mk(`AKs${i + 1}`, 'ask', 'S', ['orange', 'indigo', 'mint', 'orange', 'indigo'][i], [
    { type: 'head', fill: 'card', eyebrow: `Question ${['one', 'two', 'three', 'four', 'five'][i]}`, lines: q.split(' / ').map((t, li, a) => li === a.length - 1 ? [{ b: t }] : [t]), size: 124, grow: 1.4 },
    { type: 'tile', fill: ['orangeTint', 'indigoTint', 'mintTint', 'orangeTint', 'indigoTint'][i], icon, label: 'A good sign', lines: [[{ b: hint }]], size: 60, plainW: 600, grow: 1, mascot: { kind: 'eyes', size: 300 } },
    { type: 'cta', fill: 'accent', lines: L('Ask them / on WhatsApp.'), button: 'shikshaq.in', size: 96, grow: .9 },
  ], { aud: 'students' })),
];

// ---- NEW: copy this message -----------------------------------------------------------------------------------------------------------------------
const MSG = [
  ['The first message', 'Hello Sir, I found your profile on Shikshaq. I am in Class 10, ICSE. Are you taking new students for Maths?', 'Swap the board and subject. Say Ma’am if it is Ma’am.'],
  ['Asking about timing', 'Are evenings after school possible? We are near Salt Lake. We can work around your slot.', 'Tell them where you are. It saves a round of messages.'],
  ['Talking about the fee', 'What is your fee for one subject, three days a week? We would like to agree it here before we start.', 'Fees are between you and the tutor. Shikshaq takes nothing.'],
  ['Moving a class', 'So sorry, can we move today’s class to tomorrow? I will send the chapter I am stuck on.', 'A polite message and the chapter name. Tutors like both.'],
];
const msgOf = ([t, text, foot], i, cv) => mk(`MG${i + 1}${cv === 'S' ? 's' : ''}`, 'msg', cv, ['orange', 'indigo', 'mint', 'orange'][i], [
  H({ eyebrow: 'Copy this', lines: t.includes('first') ? L('The first / *message*') : t.includes('timing') ? L('Asking about / *timing*') : t.includes('fee') ? L('Talking about / *the fee*') : L('Moving / *a class*'), size: cv === 'S' ? 124 : 110, grow: .8 }),
  { type: 'copy', fill: 'tint', text, foot, size: cv === 'S' ? 58 : 50, grow: 2 },
], { aud: 'students', post: `MG${i + 1}${cv === 'S' ? 's' : ''}` });
export const msg = [...MSG.map((x, i) => msgOf(x, i, 'F')), ...MSG.map((x, i) => msgOf(x, i, 'S'))];

// ---- NEW: exam season ---------------------------------------------------------------------------------------------------------------------------------
const EXAM = [
  ['indigo', 'Before the pre-boards', L('Three things / *this week*'), [{ t: 'Pick one weak chapter', b: 'Only one. Not the whole book.' }, { t: 'Book a doubt class', b: 'Ask your tutor for one slot.' }, { t: 'Sleep', b: 'It counts as revision.' }]],
  ['orange', 'Puja break', L('Three things / *before the pandals*'), [{ t: 'Revise one chapter a day', b: 'Small enough to actually do.' }, { t: 'Keep one day for pandals', b: 'Planned rest is still rest.' }, { t: 'Message your tutor first', b: 'Agree the slots before the break.' }]],
  ['mint', 'Result day', L('Three things / *after the marks*'), [{ t: 'Read the marks calmly', b: 'Then close the page.' }, { t: 'List where marks were lost', b: 'By chapter, not by feeling.' }, { t: 'Find a tutor for the biggest one', b: 'Subject, class, area. Three taps.' }]],
];
const exOf = ([ac, eyebrow, lines, rows], i, cv) => mk(`EX${i + 1}${cv === 'S' ? 's' : ''}`, 'exam', cv, ac, [
  H({ eyebrow, lines, size: cv === 'S' ? 116 : 104, grow: .9, mascot: { kind: i === 1 ? 'sun' : 'eyes', size: 280 } }),
  { type: 'index', fill: 'card', rows, grow: 2.4 },
  { type: 'cta', fill: 'accent', lines: L('Find a tutor.'), button: 'shikshaq.in', size: 92, grow: .7 },
], { aud: 'students', post: `EX${i + 1}${cv === 'S' ? 's' : ''}` });
export const exam = [...EXAM.map((x, i) => exOf(x, i, 'F')), ...EXAM.map((x, i) => exOf(x, i, 'S'))];

// ---- NEW: by the class they are sitting ---------------------------------------------------------------------------------------------------------
const CLS = [
  ['orange', ['4', '5', '6'], 'Classes IV to VI', L('Starting out?'), 'A patient tutor beats a fast one.'],
  ['indigo', ['7', '8'], 'Classes VII and VIII', L('Chapters / get *longer*'), 'Middle school is where the syllabus stops being small.'],
  ['mint', ['9', '10'], 'Classes IX and X', L('Board year is / *closer* than it feels'), 'ICSE, CBSE or State board: pick a tutor who knows yours.'],
  ['orange', ['11', '12'], 'Classes XI and XII', L('ISC, CBSE / or *State board*'), 'Filter by your board, then read the reviews.'],
];
const clsOf = ([ac, on, eyebrow, lines, sub], i, cv) => mk(`CS${i + 1}${cv === 'S' ? 's' : ''}`, 'class', cv, ac, [
  H({ eyebrow, lines, size: cv === 'S' ? 124 : 112, grow: 1 }),
  { type: 'grid', fill: 'card', lines: L('Pick your class'), size: 70, tiles: ['4', '5', '6', '7', '8', '9', '10', '11', '12'], on, foot: sub, grow: 1.8 },
  { type: 'cta', fill: 'accent', lines: L('Find a tutor.'), button: 'shikshaq.in', size: 90, grow: .7 },
], { aud: 'students', post: `CS${i + 1}${cv === 'S' ? 's' : ''}` });
export const cls = [...CLS.map((x, i) => clsOf(x, i, 'F')), ...CLS.map((x, i) => clsOf(x, i, 'S'))];

// ---- NEW: wayfinding signposts --------------------------------------------------------------------------------------------------------------------
const WAY = [
  ['orange', 'Find your subject', L('Which way / *to Maths*?'), [{ t: 'Maths', dir: 'right' }, { t: 'Science', dir: 'left' }, { t: 'English', dir: 'right' }, { t: 'Commerce', dir: 'left' }], 'And Computer, Hindi, History and Geography.'],
  ['indigo', 'Find your board', L('Which way / *to your board*?'), [{ t: 'ICSE', dir: 'right' }, { t: 'ISC', dir: 'left' }, { t: 'CBSE', dir: 'right' }, { t: 'State board', dir: 'left' }], 'Filter by board, then read the reviews.'],
  ['mint', 'Find your area', L('Which way / *to you*?'), [{ t: 'Salt Lake', dir: 'right' }, { t: 'Jadavpur', dir: 'left' }, { t: 'Howrah', dir: 'right' }, { t: 'Ballygunge', dir: 'left' }], 'Bhowanipore and many other localities.'],
  ['orange', 'Find your class', L('Which way / *to your class*?'), [{ t: 'Classes IV to VI', dir: 'right' }, { t: 'VII and VIII', dir: 'left' }, { t: 'IX and X', dir: 'right' }, { t: 'XI and XII', dir: 'left' }], 'Every board, every class.'],
];
const wayOf = ([ac, eyebrow, lines, plates, sub], i, cv) => mk(`WY${i + 1}${cv === 'S' ? 's' : ''}`, 'way', cv, ac, [
  H({ eyebrow, lines, size: cv === 'S' ? 120 : 108, grow: .8 }),
  { type: 'signpost', fill: 'bone', plates: plates.map(p => ({ ...p, size: cv === 'S' ? 76 : 68 })), sub, grow: 2.4 },
], { aud: 'students', post: `WY${i + 1}${cv === 'S' ? 's' : ''}` });
export const way = [...WAY.map((x, i) => wayOf(x, i, 'F')), ...WAY.map((x, i) => wayOf(x, i, 'S'))];

// ---- NEW: the facts, plainly -----------------------------------------------------------------------------------------------------------------------
const FACTS = [
  ['orange', 'About money', L('What it / *costs*'), [{ label: 'Commission', big: '₹0', fill: 'card', icon: 'heart' }, { label: 'To contact', big: 'Free', fill: 'mint', icon: 'chat' }, { label: 'Listing fee', big: 'None', fill: 'orange', icon: 'file' }, { label: 'Invoices', big: 'Never', fill: 'indigo', icon: 'shield' }]],
  ['indigo', 'About coverage', L('What it / *covers*'), [{ label: 'City', big: 'Kolkata', fill: 'card', icon: 'pin', size: 84 }, { label: 'Classes', big: 'IV to XII', fill: 'orange', icon: 'book' }, { label: 'Boards', big: 'Four', fill: 'indigo', icon: 'file' }, { label: 'Subjects', big: 'Eight', fill: 'mint', icon: 'star' }]],
  ['mint', 'About trust', L('Why it / *can be trusted*'), [{ label: 'Before listing', big: 'Checked', fill: 'card', icon: 'shield', size: 84 }, { label: 'Reviews from', big: 'Students', fill: 'orange', icon: 'star', size: 84 }, { label: 'Paid placement', big: 'Never', fill: 'indigo', icon: 'heart' }, { label: 'Your number', big: 'Safe', fill: 'mint', icon: 'chat' }]],
];
const factOf = ([ac, eyebrow, lines, tiles], i, cv) => mk(`FT${i + 1}${cv === 'S' ? 's' : ''}`, 'facts', cv, ac, [
  H({ eyebrow, lines, size: cv === 'S' ? 124 : 110, grow: .9, mascot: { kind: 'eyes', size: 280 } }),
  { type: 'bento', fill: 'bone', tiles: tiles.map(t => ({ ...t, h: cv === 'S' ? 330 : 240 })), grow: 2.4 },
], { aud: 'all', post: `FT${i + 1}${cv === 'S' ? 's' : ''}` });
export const facts = [...FACTS.map((x, i) => factOf(x, i, 'F')), ...FACTS.map((x, i) => factOf(x, i, 'S'))];

// ---- NEW: WhatsApp stickers (512 square, transparent) -----------------------------------------------------------------------------------------
const STK = [['Sending the link', 'orange', { kind: 'eyes' }], ['Ma, look', 'indigo', { kind: 'smile' }], ['Tutor found', 'mint', { kind: 'arch', mood: 'great', fill: '#FF8000' }], ['Doubt cleared', 'orange', { kind: 'sun' }], ['Pre-board panic', 'orange', { kind: 'arch', mood: 'rough' }], ['Thank you, Sir', 'indigo', { kind: 'lobe' }], ['Thank you, Ma’am', 'orange', { kind: 'smile' }], ['Message first', 'mint', { kind: 'eyes' }], ['Free for us', 'orange', { kind: 'sun' }], ['Show your parents', 'indigo', { kind: 'eyes' }], ['Result day', 'orange', { kind: 'arch', mood: 'meh' }], ['Pujo mode', 'orange', { kind: 'arch', mood: 'great' }]];
export const stickers = STK.map(([phrase, ac, m], i) => mk(`ST${i + 1}`, 'stickers', 'K', ac, [], { look: 'wsticker', phrase, mascot: m, aud: 'students', post: 'ST' }));
