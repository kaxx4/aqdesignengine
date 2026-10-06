// WhatsApp promotions. Each push is: who it goes to, when, which image, the exact message (the FRAMING around the image),
// and the replies to expect. Messages go through the same copy gate as every poster. A push marked gated waits on real data.
export const ADMIN_ASK = 'Hello. May I share one short note about a free site where families in Kolkata find a tutor? It is one image and a link, nothing else. Please tell me if it is not suitable for this group.';
export const FORMAT = 'Send the image with the message as its caption. Send once. Do not repost. Reply to questions in the group, not in private, so others read the answer.';

const REPLIES = {
  charity: ['Is it a charity?', 'No. It is where you find your tutor, for any school student in Kolkata. It is made by AquaTerra, an NGO whose team are students.'],
  pay: ['Do we pay Shikshaq?', 'No. Fees are between you and the tutor. Shikshaq takes no commission.'],
  checked: ['Are the tutors checked?', 'Yes. Tutors apply with a form. Our team runs background checks and selects who is listed.'],
  area: ['Which areas?', 'Tutors are listed across Kolkata. Filter by locality on shikshaq.in.'],
  tutorlist: ['How do I list as a tutor?', 'Fill out a form. Our team checks your background. If you are selected, you are listed. It is free to list.'],
  class: ['Which classes?', 'Classes IV to XII. ICSE, ISC, CBSE and State board.'],
};
const R = (...k) => k.map(x => REPLIES[x]);

export const PUSHES = [
  { id: 'WP1', week: 1, day: 'Mon', time: '11:00', to: 'Parent groups', image: ['WQ1'], replies: R('charity', 'pay', 'checked', 'area'),
    message: 'Looking for a tutor for your child in Kolkata?\n\nShikshaq is where you find your tutor. Search by subject, class, board and area, read the profile and the reviews, then message the tutor yourself on WhatsApp.\n\nClasses IV to XII. ICSE, ISC, CBSE and State board. Free for families.\n\nshikshaq.in\n\nIf you know another parent who is looking, please forward this.' },
  { id: 'WP2', week: 1, day: 'Tue', time: '17:30', to: 'Student and class groups', image: ['WQ2'], replies: R('charity', 'class'),
    message: 'Looking for a tutor? Here is a way that does not need you to ask around.\n\nShikshaq is where you find your tutor. Search by subject, class, board and area, read the profile, then message the tutor.\n\nShow it to your parents. They can search too.\n\nshikshaq.in' },
  { id: 'WP3', week: 1, day: 'Thu', time: '19:00', to: 'Volunteers and the AquaTerra team', image: ['PF4-1', 'PF4-2', 'PF4-3', 'PF4-4'], replies: R('charity', 'pay', 'checked'),
    message: 'A note for the team, so we all say it the same way.\n\nShikshaq is where you find your tutor. Connecting every student in Kolkata to teachers.\n\nIt is not a charity and not a class. It is made by AquaTerra, an NGO whose team are students, and it is free for families.\n\nIf someone asks something you cannot answer, send them to shikshaq.in. The four cards are made to be forwarded.' },
  { id: 'WP4', week: 1, day: 'Fri', time: '18:00', to: 'School and community contacts', image: ['WQ4'], replies: R('charity', 'pay', 'class'),
    message: 'Hello. Sharing something that may help families you know.\n\nShikshaq is a free place for families to find a tutor in Kolkata. Search by subject, class, board and area, then message the tutor directly. No commission and no middleman.\n\nIf you can forward this to a parents group, it would help.\n\nshikshaq.in' },
  { id: 'WP5', week: 2, day: 'Mon', time: '11:00', to: 'Parent groups', image: ['WQ5'], replies: R('area', 'class'),
    message: 'Three questions we hear most about Shikshaq.\n\nIs it a charity? No. It is where you find your tutor.\nDo we pay? No. Fees are between you and the tutor.\nAre the tutors checked? Yes. Our team runs background checks and selects who is listed.\n\nMore answers: shikshaq.in' },
  { id: 'WP6', week: 2, day: 'Tue', time: '17:30', to: 'Student and class groups', image: ['CH2'], replies: R('charity', 'pay'),
    message: 'Parents asking what Shikshaq is? This is how one student explained it. Send it to yours.\n\nshikshaq.in' },
  { id: 'WP7', week: 2, day: 'Thu', time: '19:00', to: 'Tutor and teacher groups', image: ['WQ3'], replies: R('tutorlist', 'pay'),
    message: 'Are you a tutor in Kolkata?\n\nShikshaq puts your profile where students and parents are searching. Free to list. You set your own rate and keep all of it. Students and parents message you directly on WhatsApp.\n\nFill out a form. Our team checks your background. If you are selected, you are listed.\n\nshikshaq.in' },
  { id: 'WP8', week: 2, day: 'Sat', time: '11:00', to: 'Parent groups', image: ['FQ7'], replies: R('checked', 'pay'),
    message: 'One thing parents ask first: are the tutors checked?\n\nYes. Tutors apply with a form. Our team runs background checks and selects who is listed. Then you read the profile and message the tutor yourself.\n\nshikshaq.in' },
  { id: 'WP9', week: 3, day: 'Mon', time: '11:00', to: 'Community and parent groups', image: ['WM2'], replies: R('charity', 'pay'),
    message: 'Who is behind Shikshaq?\n\nA student team. Shikshaq is made by AquaTerra, an NGO whose team are students, building the list Kolkata never had. It is free for families.\n\nshikshaq.in' },
  { id: 'WP10', week: 3, day: 'Tue', time: '18:00', to: 'Parent groups', image: ['RV1'], gated: 'reviews', replies: R('pay', 'checked'),
    message: 'A review from Shikshaq:\n\n"{{review.0.text}}"\n{{review.0.first}}, {{review.0.subject}}\n\nSearch by subject, class, board and area, then message the tutor yourself.\n\nshikshaq.in' },
  { id: 'WP11', week: 3, day: 'Thu', time: '19:00', to: 'Tutor groups', image: ['MT4'], gated: 'tutors', replies: R('tutorlist'),
    message: 'Meet {{tutor.0.name}}, who teaches {{tutor.0.subject}} on Shikshaq.\n\n"{{tutor.0.quote}}"\n\nTeach on Shikshaq. Free to list. You set your own rate.\n\nshikshaq.in' },
  { id: 'WP12', week: 3, day: 'Sat', time: '17:30', to: 'Student and class groups', image: ['WQ6'], replies: R('tutorlist'),
    message: 'Is your own tutor on Shikshaq? If not, recommend them on shikshaq.in so the next student can find them too.' },
  { id: 'WP13', week: 4, day: 'Mon', time: '11:00', to: 'Parent groups', image: ['WQ1'], replies: R('pay', 'checked'),
    message: 'Still looking for a tutor?\n\nSearch on Shikshaq by subject, class, board and area, then message the tutor yourself. Free for families.\n\nshikshaq.in' },
  { id: 'WP14', week: 4, day: 'Tue', time: '17:30', to: 'Student and class groups', image: ['WQ2'], replies: R('charity'),
    message: 'Did you show your parents?\n\nSend them this. Shikshaq is where you find your tutor.\n\nshikshaq.in' },
  { id: 'WP15', week: 4, day: 'Thu', time: '19:00', to: 'Tutor and teacher groups', image: ['WQ3'], replies: R('tutorlist', 'pay'),
    message: 'Last call for tutors in Kolkata.\n\nApply to teach on Shikshaq. Free to list. You set your own rate and keep all of it. Our team checks your background and selects who is listed.\n\nshikshaq.in' },
  { id: 'WP16', week: 4, day: 'Sat', time: '11:00', to: 'All the groups above, one more time', image: ['RP5'], replies: R('charity', 'pay', 'checked'),
    message: 'Thank you for passing Shikshaq on.\n\nIf you know a student, a parent or a tutor who needs it, please forward this.\n\nshikshaq.in' },
];
