// The look registry. v3: everything is a panel stack (see stack.mjs), plus the circle-safe highlight cover.
import { page } from '../src/kit.mjs';
import { BONE, ACC } from './kit3.mjs';
import { lay, cover } from './looks-core.mjs';
import { stackLook } from './stack.mjs';
import { wsticker } from './wsticker.mjs';
import { frame } from '../src/kit.mjs';

export const LOOKS = { stack: stackLook, cover, wsticker };

export function renderHtml(spec) {
  const L = lay(spec.canvas), F = frame(spec.accent || 'orange');
  const fn = LOOKS[spec.look || 'stack'];
  if (!fn) throw new Error(`unknown look "${spec.look}" on ${spec.id}`);
  const inner = fn(spec, L, F);
  const bg = spec.look === 'cover' ? (spec.disc || F.tint) : spec.look === 'wsticker' ? 'transparent' : BONE;
  const html = page(L.W, L.H, inner, bg).replace('<script>', '<script>window.__fitTol=.16;</script><script>');
  return { html, L };
}
