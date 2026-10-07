// Reel scripts. One beat = one spoken line over one card. `say` is what ElevenLabs reads AND what the captions show, word by word.
// Facts here obey the campaign gate: no digits, no dashes, no "verified", never "connects families". Say the full sentence once, early.
import { L } from '../catalog-util.mjs';

const GO = 'Shikshaq is where you find your tutor.';
// the shared closing card. `ask` is the question this reel answered; the card answers it with the core line.
const end = (accent, ask, extra = {}) => ({ say: `${GO} shikshaq.in`, accent, panels: [{ type: 'loud', fill: accent, lines: L('Where you / find your / tutor.'), sub: ask, button: 'shikshaq.in', mascot: { kind: 'smile', fill: '#FFFFFF' }, msize: 300, size: 124 }], ...extra });

export const REELS = {
  R1: { id: 'R1', title: 'Find your tutor in three steps', accent: 'orange', voice: 'student', notes: 'A student, first person, speaking to a parent. Warm, quick, not a sales read.', beats: [
    { say: 'That one chapter nobody understands? Find a tutor in three steps.', panels: [{ type: 'loud', fill: 'orange', lines: L('That one chapter / nobody / *understands?*'), mascot: { kind: 'eyes', fill: '#FFFFFF' }, msize: 300, size: 124 }] },
    { say: 'One. Subject, class, area.', panels: [
      { type: 'head', fill: 'card', ordinal: '01', lines: L('Tell us / the *subject*'), size: 124, grow: 1.1 },
      { type: 'tile', fill: 'orangeTint', icon: 'search', label: 'Step one', lines: [[{ b: 'Subject, class and your area.' }]], size: 72, plainW: 600, grow: 1 }] },
    { say: 'Two. Compare real profiles. Reviews, boards, rates.', panels: [
      { type: 'head', fill: 'card', ordinal: '02', lines: L('Compare / *real profiles*'), size: 124, grow: 1.1 },
      { type: 'tile', fill: 'indigoTint', icon: 'users', label: 'Step two', lines: [[{ b: 'Rates, boards, reviews and travel radius.' }]], size: 64, plainW: 600, grow: 1 }], accent: 'indigo' },
    { say: 'Three. Message the tutor on WhatsApp.', panels: [
      { type: 'head', fill: 'card', ordinal: '03', lines: L('Message / *the tutor*'), size: 124, grow: 1.1 },
      { type: 'tile', fill: 'mintTint', icon: 'chat', label: 'Step three', lines: [[{ b: 'On WhatsApp. No middleman.' }]], size: 72, plainW: 600, grow: 1 }], accent: 'mint' },
    { say: 'Free for families. Shikshaq is where you find your tutor.', panels: [{ type: 'loud', fill: 'orange', lines: L('Where you / find your / tutor.'), sub: 'Free for families.', button: 'shikshaq.in', mascot: { kind: 'smile', fill: '#FFFFFF' }, msize: 300, size: 124 }] },
  ] },
};
export { end, GO };
