"""List and download images from a PUBLIC Google Drive folder — no API key, no auth.

Drive's folder page embeds each item as data-id="<fileId>" ... data-tooltip="<name> <Kind>".
Scraping that pair is enough to enumerate a shared folder. Downloads go through the thumbnail
endpoint, which returns a real JPEG for any image type (including HEIC, which the raw download
endpoint serves as an unusable .heic) and needs no confirm-token dance for large files.

    python drive_fetch.py <folderId>          # list images
    from drive_fetch import images, download  # use as a module

If the folder is not shared publicly the page returns a sign-in screen and listing() yields
nothing — that is the expected signal, not a bug. Ask the owner to share it.
"""
import re, os, sys, subprocess, json

IMG_EXT = ('.jpg', '.jpeg', '.png', '.heic')


def listing(folder_id, cache_dir):
    """All items in the folder as [{id, name, kind}]. The fetched HTML is cached."""
    os.makedirs(cache_dir, exist_ok=True)
    html_path = os.path.join(cache_dir, folder_id + '.html')
    if not os.path.exists(html_path):
        subprocess.run(['curl', '-sL', f'https://drive.google.com/drive/folders/{folder_id}',
                        '-o', html_path], check=True)
    h = open(html_path, encoding='utf-8', errors='replace').read()
    pairs = re.findall(
        r'data-id="([0-9A-Za-z_-]{20,60})"[^>]*data-tooltip="([^"]+?) (Image|Video|PDF|File)"', h)
    seen, out = set(), []
    for fid, name, kind in pairs:
        if fid in seen:
            continue
        seen.add(fid)
        out.append({'id': fid, 'name': name, 'kind': kind})
    return out


def images(folder_id, cache_dir):
    return [f for f in listing(folder_id, cache_dir) if f['name'].lower().endswith(IMG_EXT)]


def download(fid, dest, size='w1600'):
    """Fetch one image. Returns False (and removes the file) if Drive served an error page."""
    if os.path.exists(dest) and os.path.getsize(dest) > 20000:
        return True
    subprocess.run(['curl', '-sL', f'https://drive.google.com/thumbnail?id={fid}&sz={size}',
                    '-o', dest], check=True)
    ok = os.path.exists(dest) and os.path.getsize(dest) > 20000
    if not ok and os.path.exists(dest):
        os.remove(dest)
    return ok


def fetch_folder(folder_id, dest_dir, cache_dir):
    """Download every image in the folder to dest_dir as 00.jpg, 01.jpg, … Returns count."""
    os.makedirs(dest_dir, exist_ok=True)
    got = 0
    for i, f in enumerate(images(folder_id, cache_dir)):
        if download(f['id'], os.path.join(dest_dir, f'{i:02d}.jpg')):
            got += 1
    return got


if __name__ == '__main__':
    cache = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.drive_cache')
    ims = images(sys.argv[1], cache)
    print(json.dumps({'count': len(ims), 'files': [i['name'] for i in ims]}, indent=1))
