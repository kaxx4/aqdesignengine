import { C, subjectPalette, textOn } from '../tokens.mjs';
import { page, card, box, mascot, peeker, logoBar, handle, esc, chip, sticker, glow, DEFAULT_STYLE, ground } from '../kit.mjs';

// The moodboard mechanism from the reference: one tall headline column, a mixed bento of
// character, paper, number, search and tips tiles. No stock photo (real-assets-only):
// the photo tile becomes the site's own stripe placeholder with a giant initial.
export function render(post, W, H) {
  const S = post.style || DEFAULT_STYLE;
  const c = post.copy, pal = subjectPalette('Maths'), ex = post.search;
  const stripes = `repeating-linear-gradient(45deg,${pal.solid}33 0 14px,${pal.tint} 14px 28px)`;
  const T = 140, G = 20, wa = 300, wb = 300, wc = W - 48 - (48 + wa + G + wb + G);
  const L = S.flip ? 48 + wc + G : 48, xb = L + wa + G, xc = S.flip ? 48 : xb + wb + G;
  const parts = [
    logoBar(48, 44),
    // A1: three characters
    card('chars', L, T, wa + G + wb, 250, C.card, { r: 32, ring: true }),
    mascot('c1', S.kit.shapes[0], L + 36, T + 70, 110, C.orange, S.kit.moods[0]),
    mascot('c2', S.kit.shapes[1], L + 206, T + 62, 124, C.indigo, S.kit.moods[1]),
    mascot('c3', S.kit.shapes[2], L + 392, T + 66, 124, '#FFC700', S.kit.moods[2]),
    // A2: paper tile
    card('paper', L, T + 270, wa, 330, pal.tint, { r: 28, ring: S.ground !== 'bone', inner:
      `<div style="position:absolute;left:0;top:0;width:100%;height:150px;background:${stripes}"></div>
       <div class="d" data-deco="1" style="position:absolute;left:0;top:0;width:100%;height:150px;display:flex;align-items:center;justify-content:center;font-size:130px;line-height:150px;color:${pal.solid};opacity:.5">M</div>
       <div data-fit="22" style="position:absolute;left:24px;top:172px;width:252px;height:76px;font-size:34px;font-weight:700;letter-spacing:-.045em;line-height:1;color:${pal.text}">Maths paper, Class X</div>
       <div style="position:absolute;left:24px;top:262px">${chip('Read two free', C.panel, { size: 22, color: '#fff' })}</div>` }),
    // B2: orange slab with a white blob holding the one constant fact
    card('slab', xb, T + 270, wb, 330, C.orange, { r: S.radius, shadow: glow(C.orange) }),
    `<svg class="a" data-tag="n0blob" viewBox="0 0 100 100" style="left:${xb + 36}px;top:${T + 306}px;width:228px;height:228px"><path d="M50 6 C70 2 92 18 94 42 C98 66 80 94 54 94 C30 98 6 80 6 54 C2 30 26 10 50 6Z" fill="#fff"/></svg>`,
    `<div class="a d" data-tag="zero" data-bg="#FFFFFF" style="left:${xb + 36}px;top:${T + 362}px;width:228px;height:116px;display:flex;align-items:center;justify-content:center;font-size:96px;line-height:1;color:${C.ink}">₹0</div>`,
    `<div class="a lab" data-tag="zerolab" data-bg="#FFFFFF" style="left:${xb + 36}px;top:${T + 470}px;width:228px;text-align:center;font-size:20px;color:${C.ink}">commission</div>`,
    // A3: search tile
    card('search', L, T + 620, wa, 490, C.indigoTint, { r: 28, inner:
      `<div data-fit="22" style="position:absolute;left:24px;top:36px;width:252px;height:96px;font-size:40px;font-weight:700;letter-spacing:-.045em;line-height:1;color:${C.indigoDeep}">Where are you looking?</div>
       <div style="position:absolute;left:20px;top:170px;width:260px;height:76px;border-radius:999px;background:#fff;display:flex;align-items:center;padding:0 20px;gap:10px"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="${C.secondary}" stroke-width="2.4" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg><span data-fit="14" style="font-size:22px;font-weight:500;color:${C.secondary};width:196px;white-space:nowrap">${esc(ex.area)}</span></div>
       <div style="position:absolute;left:24px;top:290px;display:flex;flex-direction:column;gap:12px;align-items:flex-start">${chip(ex.subject, '#fff', { size: 22, color: C.ink })}${chip(ex.cls, '#fff', { size: 22, color: C.ink })}</div>` }),
    // B3: tips slab
    card('tips', xb, T + 620, wb, 490, C.indigo, { r: S.radius, shadow: glow(C.indigo), inner:
      `<div data-fit="30" style="position:absolute;left:28px;top:36px;width:244px;height:70px;font-size:60px;font-weight:700;letter-spacing:-.05em;line-height:1;color:#fff">Tips</div>
       <div data-fit="18" style="position:absolute;left:28px;top:118px;width:244px;height:120px;font-size:26px;font-weight:500;line-height:1.25;color:#fff;letter-spacing:-.02em">Revision plans that fit a real week.</div>
       <svg class="a" data-tag="bubble" viewBox="0 0 100 100" style="left:96px;top:300px;width:170px;height:170px;opacity:.9"><path d="M14 18 H86 V66 H50 L30 86 V66 H14Z" fill="none" stroke="#fff" stroke-width="5" stroke-linejoin="round"/><circle cx="34" cy="42" r="4" fill="#fff"/><circle cx="50" cy="42" r="4" fill="#fff"/><circle cx="66" cy="42" r="4" fill="#fff"/></svg>` }),
    // C: tall headline column
    card('tall', xc, T, wc, 1110, C.card, { r: 32, ring: true, inner: peeker('eyes', 8, 1110 - Math.round((wc - 16) * 0.62) + 2, wc - 16, C.orange) }),
    mascot('cm', S.kit.shapes[3], xc + (wc - 120) / 2, T + 40, 120, C.mintSolid, S.kit.moods[1]),
    `<h1 class="a" data-tag="headline" data-fit="40" style="left:${xc + 24}px;top:${T + 190}px;width:${wc - 48}px;height:360px;font-size:96px;font-weight:400;color:${C.ink};text-align:center">${esc(c.plain)} <span style="font-weight:800;letter-spacing:-.06em">${esc(c.bold)}</span></h1>`,
    `<div class="a" data-tag="sub" data-fit="16" style="left:${xc + 24}px;top:${T + 580}px;width:${wc - 48}px;height:90px;font-size:26px;font-weight:500;line-height:1.25;color:${C.prose};text-align:center;letter-spacing:-.02em">${esc(c.sub)}</div>`,
    `<div class="a" data-tag="ctachip" style="left:${xc + 30}px;top:${T + 690}px;width:${wc - 60}px;height:84px;border-radius:999px;background:${C.panel};display:flex;align-items:center;justify-content:center"><div data-fit="16" style="width:${wc - 100}px;height:40px;line-height:40px;text-align:center;white-space:nowrap;color:#fff;font-size:28px;font-weight:700;letter-spacing:-.03em">${esc(post.cta)}</div></div>`,
    handle(52, 1284),
  ];
  return page(W, H, parts.join(''), ground(S, post.accent));
}
