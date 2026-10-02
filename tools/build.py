"""Builds the icon pack. Style A, painted in code (the user's choice 2026-10-03: no 3D renders,
they take too long), with the finish asked for the same day: darker, sharper, a dark outline.

    tools/icons/<id>.py    -> draw() returns a 512x512 RGBA painting (helpers in tools/lib.py)
    python3 tools/build.py -> every icon: cropped to the object, darkened and sharpened, given a
                              dark outline, downsampled to 64x64; writes the pack, the models and
                              KnightsRealmIcons.zip (reproducible), and prints the zip's SHA-1.
    python3 tools/build.py sheet <id>... -> also preview/sheet.png for review.
"""
import hashlib, importlib, json, os, sys, zipfile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ICONS = os.path.join(HERE, 'icons')
sys.path.insert(0, HERE); sys.path.insert(0, ICONS)
PACK = os.path.join(ROOT, 'pack')
NS = os.path.join(PACK, 'assets', 'knightsrealm')
FORMAT = 84   # Minecraft 26.1.2 (resource_major in the client's version.json)
SIZE = 64     # texture size: 4x vanilla, sharp at GUI scale 3-4
INNER = 58    # the object's longest side inside the texture; the rest is room for outline and drop shadow

CONTRAST = 1.15     # "darker, sharper edges" (the user, 2026-10-03)
SATURATION = 1.10
GAMMA = 1.12        # >1 darkens the mid-tones
OUTLINE = (24, 18, 14)


def icon_ids():
    return sorted(f[:-3] for f in os.listdir(ICONS) if f.endswith('.py') and not f.startswith('_'))


def bevel(img, width=11.0, amount=0.65):
    """Rounds the whole silhouette: edges facing the upper-left light brighten, the far edges darken."""
    px = np.asarray(img).astype(np.float32) / 255.0
    a = px[..., 3]
    ab = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(width)), np.float32) / 255.0
    gy, gx = np.gradient(ab)
    mag = np.hypot(gx, gy) + 1e-6
    facing = (gx * 0.7 + gy * 0.7) / mag          # alpha grows inward, so +grad points away from the outside
    edge = np.clip(mag * width * 2.2, 0, 1) * a
    k = 1 + amount * facing * edge
    # light falls off across the object, top-left to bottom-right: reads as one solid volume
    ys, xs = np.nonzero(a > 0.03)
    if len(xs):
        u = ((np.arange(a.shape[1])[None, :] - xs.min()) / max(1, xs.max() - xs.min()) + (np.arange(a.shape[0])[:, None] - ys.min()) / max(1, ys.max() - ys.min())) / 2
        k = k * (1.14 - 0.30 * np.clip(u, 0, 1))
    rgb = np.clip(px[..., :3] * k[..., None] + 0.12 * np.clip(facing, 0, 1)[..., None] * edge[..., None], 0, 1)
    return Image.fromarray((np.dstack([rgb, a]) * 255).astype(np.uint8), 'RGBA')


def finish(render):
    """512 painting -> 64x64 icon: crop to the object, punch up, outline."""
    img = bevel(render.convert('RGBA'))
    a = np.asarray(img)[..., 3]
    ys, xs = np.nonzero(a > 8)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    side = max(x1 - x0, y1 - y0)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    box = (int(cx - side / 2), int(cy - side / 2), int(cx - side / 2) + side, int(cy - side / 2) + side)
    sq = Image.new('RGBA', (side, side)); sq.paste(img.crop(box) if min(box) >= 0 else img, (0, 0))
    if min(box) < 0:   # object touches the frame: paste with offset instead
        sq = Image.new('RGBA', (side, side)); sq.alpha_composite(img, (-box[0], -box[1]))
    small = sq.resize((INNER, INNER), Image.LANCZOS)
    px = np.asarray(small).astype(np.float32) / 255.0
    rgb, al = px[..., :3], px[..., 3:]
    rgb = np.clip(rgb, 0, 1) ** GAMMA
    lum = (rgb * [0.299, 0.587, 0.114]).sum(axis=2, keepdims=True)
    rgb = np.clip(lum + (rgb - lum) * SATURATION, 0, 1)
    rgb = np.clip((rgb - 0.5) * CONTRAST + 0.5, 0, 1)
    small = Image.fromarray((np.dstack([rgb, al]) * 255).astype(np.uint8), 'RGBA')
    small = small.filter(ImageFilter.UnsharpMask(radius=1.0, percent=70, threshold=1))
    out = Image.new('RGBA', (SIZE, SIZE))
    off = (SIZE - INNER) // 2 - 1          # one pixel up-left: room for the drop shadow
    # drop shadow: the silhouette, soft, two pixels down-right (light from the upper left)
    sh = Image.new('L', (SIZE, SIZE)); sh.paste(small.getchannel('A'), (off + 2, off + 2))
    sh = sh.filter(ImageFilter.GaussianBlur(1.1)).point(lambda v: int(v * 0.75))
    shadow = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0)); shadow.putalpha(sh)
    out.alpha_composite(shadow)
    # outline: the silhouette grown by one pixel, in dark brown, under the icon
    sil = Image.new('L', (SIZE, SIZE)); sil.paste(small.getchannel('A').point(lambda v: 255 if v > 40 else 0), (off, off))
    grown = sil.filter(ImageFilter.MaxFilter(3))
    ring = Image.new('RGBA', (SIZE, SIZE), OUTLINE + (0,)); ring.putalpha(grown.point(lambda v: int(v * 0.85)))
    out.alpha_composite(ring)
    out.alpha_composite(small, (off, off))
    return out


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')


def slot_sheet(items, path, cols=6):
    S = 4; slot = 18 * S; rows = (len(items) + cols - 1) // cols
    W = cols * 200 + 40; per = (W - 40) // slot; srows = (len(items) + per - 1) // per
    H = rows * 230 + 40 + srows * (slot + 8) + 32
    sh = Image.new('RGBA', (W, H), (32, 34, 40, 255)); d = ImageDraw.Draw(sh)
    for i, (n, big, tex) in enumerate(items):
        r, c = divmod(i, cols); x = 20 + c * 200; y = 20 + r * 230
        sh.alpha_composite(tex.resize((180, 180), Image.LANCZOS), (x, y))
        d.text((x + 4, y + 190), f'{i + 1} {n}', fill=(225, 225, 225))
    y0 = rows * 230 + 40; d.rectangle([0, y0 - 10, W, H], fill=(198, 198, 198))
    for i, (n, big, tex) in enumerate(items):
        x = 20 + (i % per) * slot; y0 = rows * 230 + 40 + (i // per) * (slot + 8)
        d.rectangle([x, y0, x + slot - 1, y0 + slot - 1], fill=(139, 139, 139))
        d.rectangle([x, y0, x + slot - 1, y0 + S - 1], fill=(55, 55, 55)); d.rectangle([x, y0, x + S - 1, y0 + slot - 1], fill=(55, 55, 55))
        d.rectangle([x, y0 + slot - S, x + slot - 1, y0 + slot - 1], fill=(255, 255, 255)); d.rectangle([x + slot - S, y0, x + slot - 1, y0 + slot - 1], fill=(255, 255, 255))
        sh.alpha_composite(tex, (x + S, y0 + S))
    sh.save(path)


def main():
    write_json(os.path.join(PACK, 'pack.mcmeta'), {'pack': {
        'pack_format': FORMAT, 'min_format': FORMAT, 'max_format': FORMAT,
        'description': 'KnightsRealm menu icons'}})
    os.makedirs(os.path.join(ROOT, 'preview'), exist_ok=True)
    # drop textures/models of icons that no longer have a render
    for sub, ext in (('textures/item', '.png'), ('models/item', '.json'), ('items', '.json')):
        d = os.path.join(NS, sub)
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.endswith(ext) and f[:-len(ext)] not in icon_ids():
                    os.remove(os.path.join(d, f))
    built = {}
    for name in icon_ids():
        big = importlib.import_module(name).draw()
        tex = finish(big); built[name] = (big, tex)
        p = os.path.join(NS, 'textures', 'item', name + '.png'); os.makedirs(os.path.dirname(p), exist_ok=True)
        tex.save(p)
        write_json(os.path.join(NS, 'models', 'item', name + '.json'),
                   {'parent': 'minecraft:item/generated', 'textures': {'layer0': 'knightsrealm:item/' + name}})
        write_json(os.path.join(NS, 'items', name + '.json'),
                   {'model': {'type': 'minecraft:model', 'model': 'knightsrealm:item/' + name}})
        tex.resize((256, 256), Image.LANCZOS).save(os.path.join(ROOT, 'preview', name + '.png'))
    first = built.get('treasury', next(iter(built.values())))[1]
    first.save(os.path.join(PACK, 'pack.png'))
    with open(os.path.join(ROOT, 'icons.txt'), 'w', newline='\n') as f:   # the ids in this pack, for the plugin's test
        f.write('\n'.join(icon_ids()) + '\n')

    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        slot_sheet([(n, *built[n]) for n in sys.argv[2:]], os.path.join(ROOT, 'preview', 'sheet.png'))

    out = os.path.join(ROOT, 'KnightsRealmIcons.zip')
    files = []
    for base, _, names in os.walk(PACK):
        for n in names:
            full = os.path.join(base, n)
            files.append((os.path.relpath(full, PACK).replace(os.sep, '/'), full))
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for arc, full in sorted(files):
            info = zipfile.ZipInfo(arc, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(full, 'rb') as f:
                z.writestr(info, f.read())
    print('KnightsRealmIcons.zip sha1', hashlib.sha1(open(out, 'rb').read()).hexdigest())


if __name__ == '__main__':
    main()
