"""Builds the textures, models and KnightsRealmIcons.zip from tools/icons.py.

The zip is byte-for-byte reproducible (fixed timestamps, sorted entries), so its SHA-1 changes
only when an icon or a pack file really changes. Prints the SHA-1 for the server's config.yml.
"""
import hashlib, json, os, sys, zipfile
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from icons import ICONS, PALETTE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACK = os.path.join(ROOT, 'pack')
NS = os.path.join(PACK, 'assets', 'knightsrealm')
FORMAT = 84  # Minecraft 26.1.2 (resource_major in the client's version.json)


def draw(layers):
    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for grid, (ox, oy) in layers:
        for y, row in enumerate(grid):
            for x, ch in enumerate(row):
                if ch != '.':
                    img.putpixel((x + ox, y + oy), PALETTE[ch] + (255,))
    return img


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')


def main():
    write_json(os.path.join(PACK, 'pack.mcmeta'), {'pack': {
        'pack_format': FORMAT, 'min_format': FORMAT, 'max_format': FORMAT,
        'description': 'KnightsRealm menu icons'}})
    for name, layers in ICONS.items():
        img = draw(layers)
        tex = os.path.join(NS, 'textures', 'item', name + '.png')
        os.makedirs(os.path.dirname(tex), exist_ok=True)
        img.save(tex)
        write_json(os.path.join(NS, 'models', 'item', name + '.json'),
                   {'parent': 'minecraft:item/generated', 'textures': {'layer0': 'knightsrealm:item/' + name}})
        write_json(os.path.join(NS, 'items', name + '.json'),
                   {'model': {'type': 'minecraft:model', 'model': 'knightsrealm:item/' + name}})
        os.makedirs(os.path.join(ROOT, 'preview'), exist_ok=True)
        img.resize((256, 256), Image.NEAREST).save(os.path.join(ROOT, 'preview', name + '.png'))
    # pack.png: the first icon, scaled up
    first = draw(next(iter(ICONS.values())))
    first.resize((64, 64), Image.NEAREST).save(os.path.join(PACK, 'pack.png'))

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
    sha1 = hashlib.sha1(open(out, 'rb').read()).hexdigest()
    print('KnightsRealmIcons.zip sha1', sha1)


if __name__ == '__main__':
    main()
