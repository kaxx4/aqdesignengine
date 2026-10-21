"""Disco Diwali UPI payment QR that pre-fills the payment NOTE with "Disco Diwali".

The existing TERRAROOTS code (engine/assets/terrathon/qr_dd_payment_terraroots_source.png) is a static EMV merchant QR
with no note field, and its payload is never edited (tt_dd_pay_sign.py rule). A note needs the UPI deep-link form instead:
    upi://pay?pa=<VPA>&pn=<payee>&tn=Disco%20Diwali&cu=INR
Payee VPA, name and merchant code are READ out of that same payload (EMV TLV), not retyped. No amount (buyer types it).

Outputs: out/collaterals/dd_upi_note_qr.png (dark on white, 4-module quiet zone) + .svg, and a printed decode check.
TEST-SCAN WITH A REAL PAYMENT APP before printing: apps differ in whether they honour tn on a merchant VPA.
Run:  PYTHONIOENCODING=utf-8 python scratchpad/dd_upi_note_qr.py
"""
import os, sys, urllib.parse
import cv2, segno

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EMV = "000201010211021644038482021656080415522024082021656061661000308202165650825HDFC00000015020011163278526460010A0000005240128Vyapar.174068471103@hdfcbank27420010A0000005240124STQD295260117541249217725204829953033565802IN5910TERRAROOTS6007KOLKATA610670001562400524STQD2952601175412492177207088202165663045267"
NOTE = "Disco Diwali"


def tlv(s):
    out, i = {}, 0
    while i < len(s):
        n = int(s[i + 2:i + 4])
        out[s[i:i + 2]] = s[i + 4:i + 4 + n]
        i += 4 + n
    return out


q = lambda v: urllib.parse.quote(v, safe="@.-")
if "personal" in sys.argv:
    # user's own GPay QR (2026-10-21), decoded: upi://pay?pa=kanishk.ag2468-2@okhdfcbank&pn=Kanishk%20Agarwal&aid=...
    # A personal VPA has no merchant code, so apps keep the note. aid (a GPay-only id) is dropped to stay app-neutral.
    SLUG, link = "dd_upi_note_qr_personal", f"upi://pay?pa={q('kanishk.ag2468-2@okhdfcbank')}&pn={q('Kanishk Agarwal')}&tn={q(NOTE)}&cu=INR"
else:
    top = tlv(EMV)
    vpa = next(v for v in tlv(top["26"]).values() if "@" in v)       # tag 26 sub-field holding the payee VPA
    SLUG, link = "dd_upi_note_qr", f"upi://pay?pa={q(vpa)}&pn={q(top['59'])}&tn={q(NOTE)}&mc={top['52']}&cu=INR"
print("LINK", link)

code = segno.make(link, error="m")
os.makedirs("out/collaterals", exist_ok=True)
code.save(f"out/collaterals/{SLUG}.svg", scale=10, border=4, dark="#0A0A0A", light="#FFFFFF")
code.save(f"out/collaterals/{SLUG}.png", scale=16, border=4, dark="#0A0A0A", light="#FFFFFF")

img = cv2.imread(f"out/collaterals/{SLUG}.png")
hits = []
for f in (1.0, .5, .35, .25):
    got = cv2.QRCodeDetector().detectAndDecode(img if f == 1 else cv2.resize(img, None, fx=f, fy=f, interpolation=cv2.INTER_AREA))[0]
    hits.append((f, got == link))
print("DECODES TO LINK at scales:", hits)
assert all(ok for _, ok in hits[:3]), "QR does not decode reliably"
parsed = urllib.parse.parse_qs(urllib.parse.urlparse(link).query)
print("PARSED:", {k: v[0] for k, v in parsed.items()})
