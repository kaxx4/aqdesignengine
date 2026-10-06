// The look registry. renderHtml(spec) is the only door: spec in, a full HTML page out.
import { page, frame } from '../src/kit.mjs';
import { C } from '../src/tokens.mjs';
import { lay, groundOf, plate, answer, eyesLook, mood, poll, cover, button, ui } from './looks-core.mjs';
import { bands, brief, cardLook, swarm, chat, calendar, review, tutor, bento } from './looks-more.mjs';

export const LOOKS = { plate, answer, eyes: eyesLook, mood, poll, cover, button, ui, bands, brief, card: cardLook, swarm, chat, calendar, review, tutor, bento };

export function renderHtml(spec) {
  const L = lay(spec.canvas), F = frame(spec.accent || 'orange');
  const fn = LOOKS[spec.look];
  if (!fn) throw new Error(`unknown look "${spec.look}" on ${spec.id}`);
  const inner = fn(spec, L, F);
  // Display type at tight leading overflows its line box by design: the campaign opts in to a proportional fit tolerance.
  const html = page(L.W, L.H, inner, spec.look === 'cover' ? (spec.disc || F.tint) : groundOf(spec, F)).replace('<script>', '<script>window.__fitTol=.16;</script><script>');
  return { html, L };
}
