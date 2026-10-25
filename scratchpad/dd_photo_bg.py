"""Shared PHOTO background for the Disco Diwali carousel posters (cover, charity, date, location), feed and story.

Layer order, back to front: black, the event photo graded dark (object-fit cover, per-slide focus), a navy-to-black scrim (top and bottom heavier so type reads), the
(optional, OFF by default) navy diya plate SCREEN-blended, the string lights, gold dust and film grain. Every layer is tagged plate
(deliberate full bleed). A tall canvas just crops the photo wider; no second plate is needed because the photo already fills it.

Consent caveat (brain/DISCO_DIWALI.md): the event photos show people, several apparent minors, with no consent record. Frames are chosen for atmosphere with small or
turned faces; check before any public post. Use: photo_ground(dd, W, H, "14_04", "50% 30%", dim=.62)
"""
import glob, os

EVENTS = ("unsorted-2026-10-07", "disco-diwali-hall-2026-10-14", "disco-diwali-2026-10-21")


def find(dd, ref):
    """ref like '07_03': '07' = unsorted-2026-10-07, '14' = disco-diwali-hall-2026-10-14, then the NN_ file prefix."""
    day, nn = ref.split("_")
    folder = [e for e in EVENTS if e.endswith("-" + day)][0]
    hits = sorted(glob.glob(os.path.join(dd.ROOT, "engine", "assets", "img", "events", folder, f"{nn}_*.jpg")))
    if len(hits) != 1:
        raise ValueError(f"photo {ref!r} matched {len(hits)} files")
    return hits[0]


def photo_ground(dd, W, H, ref, pos="50% 40%", dim=.60, plate_opacity=0, bright=1.0):
    path = find(dd, ref)
    uri = dd.photo_uri(path, 1800)
    p = ['<div data-tag="plate" style="position:absolute;inset:0;z-index:0;background:#000"></div>',
         f'<img data-tag="plate" src="{uri}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;object-fit:cover;object-position:{pos};z-index:1;'
         f'filter:contrast(1.08) saturate(1.05) brightness({bright})">',
         # navy scrim: heavier at the top and bottom so headline and footer read, lighter through the middle so the photo shows
         f'<div data-tag="plate" style="position:absolute;inset:0;z-index:2;pointer-events:none;background:linear-gradient(180deg,rgba(6,5,24,{dim + .22}) 0%,rgba(6,5,24,{dim}) 38%,rgba(6,5,24,{dim - .08}) 60%,rgba(0,0,0,{dim + .25}) 100%)"></div>']
    if plate_opacity > 0:   # the navy diya texture is OFF by default (user, 2026-10-20: 'remove the blue diya lamp texture')
        p.append(f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:0;width:{W}px;height:1350px;object-fit:cover;z-index:3;mix-blend-mode:screen;opacity:{plate_opacity};pointer-events:none">')
    if H > 1350 and plate_opacity > 0:
        p.append(f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:{H - 1350}px;width:{W}px;height:1350px;object-fit:cover;z-index:3;mix-blend-mode:screen;'
                 f'opacity:{plate_opacity};transform:scaleY(-1);pointer-events:none;-webkit-mask-image:linear-gradient(to top,transparent 0%,#000 45%);mask-image:linear-gradient(to top,transparent 0%,#000 45%)">')
    p.append(f'<img data-tag="lights" src="{dd.uri("string_lights.png")}" style="position:absolute;left:160px;top:-53px;width:1045px;z-index:5">')
    p.append(f'<img data-tag="plate" src="{dd.uri("sparkles.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:30;mix-blend-mode:screen;opacity:.55;pointer-events:none">'
             f'<img data-tag="plate" src="{dd.uri("grain.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:31;mix-blend-mode:screen;opacity:.35;pointer-events:none">')
    return "".join(p)
