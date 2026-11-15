import sys, glob
from PIL import Image
def sheet(pat, out, cols, tw):
    fs = sorted(glob.glob(pat)); ims = [Image.open(f).convert('RGB') for f in fs]
    if not ims: return
    th = max(int(tw * im.height / im.width) for im in ims); rows = (len(ims) + cols - 1) // cols
    S = Image.new('RGB', (cols * tw, rows * th), 'white')
    for i, im in enumerate(ims): S.paste(im.resize((tw, int(tw * im.height / im.width))), ((i % cols) * tw, (i // cols) * th))
    S.save(out, quality=86)
d = sys.argv[1]
for k in ['E_round', 'F_sund', 'G_learn', 'H_collab', 'I_terra', 'J_comein']:
    sheet(f'{d}/{k}_[0-9]*.jpg', f'{d}/_sheet_{k}.jpg', 7, 340)
sheet(f'{d}/*_story*.jpg', f'{d}/_sheet_stories.jpg', 9, 240)
sheet(f'{d}/K_*.jpg', f'{d}/_sheet_highlights.jpg', 8, 240)
sheet(f'{d}/L_*.jpg', f'{d}/_sheet_whatsapp.jpg', 3, 500)
