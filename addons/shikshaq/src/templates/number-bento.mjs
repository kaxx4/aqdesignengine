import { C, textOn } from '../tokens.mjs';
import { page, card, box, mascot, logoBar, handle, headline, ctaBar, frame, esc, glow, chip, DEFAULT_STYLE, ground } from '../kit.mjs';

// One giant fact in a saturated slab, a mint mascot card, one line of proof, one CTA.
export function render(post, W, H) {
  const S = post.style || DEFAULT_STYLE;
  const { a } = frame(post.accent), c = post.copy;
  const num = esc(c.bigDisplay);
  const size = Math.min(380, Math.floor(880 / (c.bigDisplay.length * 0.66)));
  const parts = [
    logoBar(48, 44),
    headline(48, 132, 984, c.plain, c.bold, 108),
    card('slab', 48, 380, 984, 470, a, { r: S.radius, shadow: glow(a), inner:
      `<div class="d" data-fit="120" style="position:absolute;left:52px;top:14px;width:${Math.min(880, Math.round(c.bigDisplay.length * 0.68 * size))}px;height:${Math.round(size * 0.92)}px;font-size:${size}px;line-height:.92;color:${textOn(a)}">${num}</div>
       <div style="position:absolute;left:56px;bottom:30px">${chip(c.bigLabel, C.panel, { size: 30, color: '#fff' })}</div>` }),
    ...(c.bigDisplay.length * 0.68 * size <= 700 ? [mascot('m0', S.kit.shapes[2], 800, 430, 170, '#FFC700', S.kit.moods[2], 10)] : []),
    card('mint', 48, 870, 482, 220, C.mint, { r: 28, inner: '' }),
    mascot('m1', S.kit.shapes[1], 172, 880, 200, C.mintSolid, S.kit.moods[3], 8),
    card('proof', 550, 870, 482, 220, C.card, { r: 28, ring: true, inner:
      `<div data-fit="20" style="position:absolute;left:32px;top:30px;width:418px;height:170px;font-size:34px;line-height:1.2;font-weight:500;color:${C.prose};letter-spacing:-.02em;text-wrap:pretty">${esc(c.sub)}</div>` }),
    ctaBar(1110, post.cta, a, { variant: S.cta }),
    handle(52, 1284),
  ];
  return page(W, H, parts.join(''), ground(S, post.accent));
}
