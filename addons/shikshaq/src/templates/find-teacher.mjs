import { C, textOn } from '../tokens.mjs';
import { page, card, mascot, peeker, logoBar, handle, headline, ctaBar, frame, esc, chip, glow, DEFAULT_STYLE, ground } from '../kit.mjs';

// The parent flow as a picture: a search, three tilted chips, a WhatsApp card,
// and the peeking-eyes blob from the bento reference.
export function render(post, W, H) {
  const S = post.style || DEFAULT_STYLE;
  const { a } = frame(post.accent), c = post.copy, ex = post.search;
  const search = `<div style="position:absolute;left:56px;top:250px;width:872px;height:96px;border-radius:999px;background:#fff;display:flex;align-items:center;padding:0 36px;gap:18px">
      <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="${C.secondary}" stroke-width="2.4" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>
      <span style="font-size:34px;font-weight:500;color:${C.secondary};letter-spacing:-.02em">${esc(ex.subject)}, ${esc(ex.cls)}, ${esc(ex.area)}</span></div>`;
  const parts = [
    logoBar(48, 44),
    headline(48, 132, 984, c.plain, c.bold, 112),
    card('slab', 48, 380, 984, 460, a, { r: S.radius, shadow: glow(a), inner:
      `<div data-fit="26" style="position:absolute;left:56px;top:70px;width:872px;height:56px;font-size:46px;font-weight:700;letter-spacing:-.04em;color:${textOn(a)}">${esc(c.ask)}</div>
       <div style="position:absolute;left:56px;top:140px;width:872px;font-size:30px;font-weight:500;color:${textOn(a)};opacity:.9;letter-spacing:-.02em" data-fit="20">${esc(c.sub)}</div>
       ${search}
       <div style="position:absolute;left:56px;top:372px;display:flex;gap:14px">${chip('Subject', 'rgba(31,31,31,.14)', { size: 24, color: textOn(a) })}${chip('Class', 'rgba(31,31,31,.14)', { size: 24, color: textOn(a) })}${chip('Area', 'rgba(31,31,31,.14)', { size: 24, color: textOn(a) })}</div>` }),
    card('wa', 48, 860, 520, 230, C.card, { r: 28, ring: true, inner:
      `<div style="position:absolute;left:36px;top:34px">${chip('WhatsApp', '#25D366', { size: 28, color: C.ink })}</div>
       <div data-fit="22" style="position:absolute;left:36px;top:104px;width:450px;height:100px;font-size:40px;font-weight:700;letter-spacing:-.045em;line-height:1.05;color:${C.ink}">One tap opens the chat.</div>` }),
    card('eyes', 588, 860, 444, 230, C.indigoTint, { r: 28, inner: peeker('eyesvg', 72, 40, 300, C.indigo) }),
    ctaBar(1110, post.cta, a, { variant: S.cta }),
    handle(52, 1284),
  ];
  return page(W, H, parts.join(''), ground(S, post.accent));
}
