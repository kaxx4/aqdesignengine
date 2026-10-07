// WhatsApp stickers: 512 x 512, transparent, one die-cut object (white keyline, ink outline, soft shadow) so a student can send
// the idea to a parent in one tap. Same blob family as the site, one phrase on a tilted tag.
import { esc } from '../src/kit.mjs';
import { INK, BONE, ORANGE, INDIGO, MINT_SOLID, LEMON, ACC, mascot } from './kit3.mjs';

export function wsticker(spec, L) {
  const A = ACC[spec.accent || 'orange'], c = spec.fill || A.a;
  const m = spec.mascot || { kind: 'eyes' };
  const key = 'drop-shadow(7px 0 0 #fff) drop-shadow(-7px 0 0 #fff) drop-shadow(0 7px 0 #fff) drop-shadow(0 -7px 0 #fff) drop-shadow(5px 5px 0 #fff) drop-shadow(-5px -5px 0 #fff) drop-shadow(5px -5px 0 #fff) drop-shadow(-5px 5px 0 #fff)';
  const ink = 'drop-shadow(3px 0 0 #1F1F1F) drop-shadow(-3px 0 0 #1F1F1F) drop-shadow(0 3px 0 #1F1F1F) drop-shadow(0 -3px 0 #1F1F1F)';
  const body = mascot(m, 'position:absolute;left:72px;top:36px;width:310px;height:310px', 'mas');
  const tag = `<div data-bg="${BONE}" style="position:absolute;left:36px;top:300px;width:440px;transform:rotate(-5deg);text-align:center;background:${BONE};color:${INK};font:900 52px/1.05 Archivo,Geist,sans-serif;letter-spacing:-.05em;padding:20px 22px 26px;border-radius:30px;border:6px solid ${INK}" data-fitw="1">${esc(spec.phrase)}</div>`;
  return `<div class="a" style="left:0;top:0;width:512px;height:512px;filter:drop-shadow(0 8px 10px rgba(0,0,0,.25))"><div style="position:absolute;inset:0;filter:${key}"><div style="position:absolute;inset:0;filter:${ink}">${body}${tag}</div></div></div>`;
}
