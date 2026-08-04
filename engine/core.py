"""AQ ENGINE — core: brand tokens, embedded fonts, shared render helpers.
This is the single source for CSS tokens + fonts. build.py imports from here.
Nothing here is 'enforced per piece' — these are the raw materials only.
"""
import base64, os
HERE = os.path.dirname(os.path.abspath(__file__))
def _b64(path, mime):
    with open(os.path.join(HERE, path), "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()

# ---- real assets (never fake these) ----
LOGO   = _b64("assets/logo.png", "image/png")                       # real colored wordmark
PHOTOS = {
    "food":     _b64("assets/img/food-distribution.jpeg", "image/jpeg"),
    "edu":      _b64("assets/img/education-sundarban.jpeg", "image/jpeg"),
    "diwali":   _b64("assets/img/fundraising-diwali.jpeg", "image/jpeg"),
    "xmas":     _b64("assets/img/christmas-khidirpur.jpeg", "image/jpeg"),
}

# ---- embedded font-face block ----
FONTS = f"""
@font-face{{font-family:'NeutralFace';src:url('{_b64("assets/fonts/NeutralFace-Bold.otf","font/otf")}') format('opentype');font-weight:700 900}}
@font-face{{font-family:'NeutralFace';src:url('{_b64("assets/fonts/NeutralFace.otf","font/otf")}') format('opentype');font-weight:400}}
@font-face{{font-family:'Eina01';src:url('{_b64("assets/fonts/Eina01-Regular.ttf","font/ttf")}') format('truetype');font-weight:400}}
@font-face{{font-family:'Eina01';src:url('{_b64("assets/fonts/Eina02-SemiBold.ttf","font/ttf")}') format('truetype');font-weight:600}}
@font-face{{font-family:'Instrument Serif';src:url('{_b64("assets/fonts/InstrumentSerif-Italic.ttf","font/ttf")}') format('truetype');font-style:italic}}
@font-face{{font-family:'Instrument Serif';src:url('{_b64("assets/fonts/InstrumentSerif-Regular.ttf","font/ttf")}') format('truetype')}}
@font-face{{font-family:'JetBrains Mono';src:url('{_b64("assets/fonts/JetBrainsMono-Bold.ttf","font/ttf")}') format('truetype');font-weight:700}}
@font-face{{font-family:'JetBrains Mono';src:url('{_b64("assets/fonts/JetBrainsMono-Medium.ttf","font/ttf")}') format('truetype');font-weight:500}}
"""

# ---- brand tokens (the LAW — do not invent colors) ----
ROOT = """:root{
--bg:#F4EFE0;--bg2:#EDE6D0;--ink:#0A0A0A;--ink2:#1A1A18;--ink3:#5A5A55;
--pink:#FF4D8C;--mint:#1B8A5A;--lemon:#FFC700;--tomato:#FF4D2E;--sky:#3DA9FC;--grape:#7E5BFF;--teal:#0E7C86;--mintbright:#00E5A0;
--d:'NeutralFace',sans-serif;--e:'Eina01',sans-serif;--s:'Instrument Serif',serif;--m:'JetBrains Mono',monospace}"""

# 7 accents for free rotation (pink is default shout; teal is the 7th, canon)
ACCENTS = ["#FF4D8C","#1B8A5A","#FFC700","#FF4D2E","#3DA9FC","#7E5BFF","#0E7C86"]
# ink text required on these light accents; white text on the rest
INK_ON = {"#FFC700","#3DA9FC","#00E5A0"}

GRAIN = ("background-image:url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
         "width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='0.8' numOctaves='2'/%3E%3C/filter%3E"
         "%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.06'/%3E%3C/svg%3E\")")

# ---- canvas sizes ----
SIZES = {"feed": (1080,1350), "story": (1080,1920), "square": (1080,1080)}

def text_on(accent_hex):
    """Return correct text color for text placed ON a given accent."""
    return "#0A0A0A" if accent_hex in INK_ON else "#FFFFFF"
