"""Builds every icon in tools/icons/ into the pack and KnightsRealmIcons.zip.

Each tools/icons/<id>.py has draw() -> a 512x512 RGBA image (realistic style, see lib.py); the file
name is the icon id (knightsrealm:<id>). Painted big, downsampled to SIZE x SIZE for the texture.
The zip is byte-for-byte reproducible, so its SHA-1 changes only when something really changes.

    python3 tools/build.py            build the pack and zip, print the SHA-1
    python3 tools/build.py sheet ids  also write preview/sheet.png of those ids (for review)
"""
import hashlib, importlib, json, os, sys, zipfile
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'icons'))

ROOT = os.path.dirname(HERE)
PACK = os.path.join(ROOT, 'pack')
NS = os.path.join(PACK, 'assets', 'knightsrealm')
FORMAT = 84   # Minecraft 26.1.2 (resource_major in the client's version.json)
SIZE = 64     # texture size: 4x vanilla, sharp at GUI scale 3-4


def icon_ids():
    return sorted(f[:-3] for f in os.listdir(os.path.join(HERE, 'icons')) if f.endswith('.py') and not f.startswith('_'))


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')


def slot_sheet(images, path):
    """Big view on top, a vanilla-looking slot row below (GUI scale 4) - how it looks in a menu."""
    S = 4; slot = 18 * S; cols = len(images)
    W = max(8 * S + slot * cols + 8 * S, 160 * cols + 20); H = 180 + slot + 24 * S
    sheet = Image.new('RGBA', (W, H), (32, 34, 40, 255)); d = ImageDraw.Draw(sheet)
    for i, (name, img) in enumerate(images):
        sheet.alpha_composite(img.resize((140, 140), Image.LANCZOS), (20 + 160 * i, 20))
        d.text((20 + 160 * i, 164), name, fill=(220, 220, 220))
    y0 = 180 + 8 * S
    d.rectangle([0, 180, W, H], fill=(198, 198, 198))
    for i, (name, img) in enumerate(images):
        x = 8 * S + i * slot
        d.rectangle([x, y0, x + slot - 1, y0 + slot - 1], fill=(139, 139, 139))
        d.rectangle([x, y0, x + slot - 1, y0 + S - 1], fill=(55, 55, 55)); d.rectangle([x, y0, x + S - 1, y0 + slot - 1], fill=(55, 55, 55))
        d.rectangle([x, y0 + slot - S, x + slot - 1, y0 + slot - 1], fill=(255, 255, 255)); d.rectangle([x + slot - S, y0, x + slot - 1, y0 + slot - 1], fill=(255, 255, 255))
        sheet.alpha_composite(img.resize((16 * S, 16 * S), Image.LANCZOS), (x + S, y0 + S))
    sheet.save(path)


def main():
    write_json(os.path.join(PACK, 'pack.mcmeta'), {'pack': {
        'pack_format': FORMAT, 'min_format': FORMAT, 'max_format': FORMAT,
        'description': 'KnightsRealm menu icons'}})
    os.makedirs(os.path.join(ROOT, 'preview'), exist_ok=True)
    textures = {}
    for name in icon_ids():
        big = importlib.import_module(name).draw()
        img = big.resize((SIZE, SIZE), Image.LANCZOS)
        textures[name] = img
        tex = os.path.join(NS, 'textures', 'item', name + '.png')
        os.makedirs(os.path.dirname(tex), exist_ok=True)
        img.save(tex)
        write_json(os.path.join(NS, 'models', 'item', name + '.json'),
                   {'parent': 'minecraft:item/generated', 'textures': {'layer0': 'knightsrealm:item/' + name}})
        write_json(os.path.join(NS, 'items', name + '.json'),
                   {'model': {'type': 'minecraft:model', 'model': 'knightsrealm:item/' + name}})
        big.resize((256, 256), Image.LANCZOS).save(os.path.join(ROOT, 'preview', name + '.png'))
    textures['treasury'].resize((64, 64), Image.LANCZOS).save(os.path.join(PACK, 'pack.png'))

    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        slot_sheet([(n, textures[n]) for n in sys.argv[2:]], os.path.join(ROOT, 'preview', 'sheet.png'))

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
