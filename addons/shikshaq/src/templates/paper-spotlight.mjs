import { C, subjectPalette } from '../tokens.mjs';
import { page, card, box, mascot, logoBar, handle, headline, ctaBar, frame, esc, chip, sticker, DEFAULT_STYLE, ground } from '../kit.mjs';

// A paper card dressed exactly like the site's (subject tint, badge row, stripe band).
export function render(post, W, H) {
  const S = post.style || DEFAULT_STYLE;
  const { a } = frame(post.accent), c = post.copy, p = post.paper, pal = subjectPalette(p.subject);
  const stripes = `repeating-linear-gradient(45deg,${pal.solid}33 0 14px,${pal.tint} 14px 28px)`;
  const meta = [p.board, p.exam, p.year].filter(Boolean).join(' · ');
  const parts = [
    logoBar(48, 44),
    `<div class="a lab" data-tag="eyebrow" style="left:48px;top:128px;color:#A34D00">${esc(c.eyebrow)}</div>`,
    headline(48, 168, 800, c.plain, c.bold, 104),
    card('paper', 48, 420, 984, 660, pal.tint, { r: 28, ring: S.ground !== 'bone', inner:
      `<div style="position:absolute;left:0;top:0;width:100%;height:260px;background:${stripes}"></div>
       <div class="d" data-deco="1" style="position:absolute;left:0;top:0;width:100%;height:260px;display:flex;align-items:center;justify-content:center;font-size:210px;line-height:260px;color:${pal.solid};opacity:.5">${esc(p.subject[0])}</div>
       <div style="position:absolute;left:44px;top:296px;display:flex;gap:12px">${chip(p.subject, pal.solid, { size: 26, color: pal.badgeText })}${chip('Class ' + p.cls, 'rgba(31,31,31,.08)', { size: 26, color: C.ink })}</div>
       <div data-fit="44" style="position:absolute;left:44px;top:362px;width:896px;height:150px;font-size:92px;font-weight:700;letter-spacing:-.05em;line-height:.98;color:${pal.text}">${esc(p.subject)} paper, Class ${esc(p.cls)}</div>
       <div data-fit="22" style="position:absolute;left:44px;top:514px;width:896px;height:52px;font-size:36px;font-weight:500;color:${pal.meta}">${esc(meta)}</div>
       <div style="position:absolute;left:44px;right:44px;top:576px;height:1px;background:rgba(31,31,31,.09)"></div>
       <div data-fit="18" style="position:absolute;left:44px;top:594px;width:896px;height:36px;font-size:28px;font-weight:500;color:${pal.meta}">${esc(c.line)}</div>` }),
    sticker('stk', 800, 392, 'NEW', C.orange, 6 * S.stickerSign, 30),
    mascot('m1', S.kit.shapes[2], 868, 140, 150, '#FFC700', S.kit.moods[2], -8),
    ctaBar(1110, post.cta, a, { variant: S.cta }),
    handle(52, 1284),
  ];
  return page(W, H, parts.join(''), ground(S, post.accent));
}
