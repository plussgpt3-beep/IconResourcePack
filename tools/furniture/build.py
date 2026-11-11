"""Builds the furniture pack (the user, 2026-11-11: medieval furniture of our own for the capitals, shown by the plugin
as item displays - no client mod, no bought pack).

    tools/furniture/models.py   every piece as boxes; the front is north
    python3 tools/furniture/build.py [vanilla-assets-dir] -> furniture/pack/... , KnightsRealmFurniture.zip (reproducible),
                                    furniture/furniture.txt (the ids) and furniture/preview.png

A piece is assets/knightsrealm/models/furniture/<gf|sh>/<id>.json with the item definition
assets/knightsrealm/items/furniture/<gf|sh>/<id>.json; the plugin gives an item display the item_model
knightsrealm:furniture/<gf|sh>/<id>. Textures are the game's own (minecraft:block/...).
"""
import hashlib, json, os, sys, zipfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import models

PACK = os.path.join(ROOT, 'furniture', 'pack')
FORMAT = 84                                   # as the icon pack: Minecraft 26.1.2 and up
FACES = ('north', 'south', 'east', 'west', 'up', 'down')


def span(a0, a1):
    L = a1 - a0
    if L >= 16: return 0, 16
    s = a0 % 16
    if s + L > 16: s = 16 - L
    return round(s, 3), round(s + L, 3)


def element(e):
    (x0, y0, z0), (x1, y1, z1) = e['a'], e['b']
    assert x0 < x1 and y0 < y1 and z0 < z1, e
    assert all(-16 <= v <= 32 for v in e['a'] + e['b']), e
    faces = {}
    for f in FACES:
        if f in ('north', 'south'): (u0, u1), (v1_, v0_) = span(x0, x1), span(y0, y1); uv = [u0, 16 - v0_, u1, 16 - v1_]
        elif f in ('east', 'west'): (u0, u1), (v1_, v0_) = span(z0, z1), span(y0, y1); uv = [u0, 16 - v0_, u1, 16 - v1_]
        else: (u0, u1), (v0, v1) = span(x0, x1), span(z0, z1); uv = [u0, v0, u1, v1]
        faces[f] = {'uv': uv, 'texture': '#' + e['over'].get(f, e['tex'])}
    out = {'from': [x0, y0, z0], 'to': [x1, y1, z1], 'faces': faces}
    if e['rot']:
        ang, axis, origin = e['rot']; assert ang in (-45, -22.5, 22.5, 45) and axis in 'xyz'
        out['rotation'] = {'angle': ang, 'axis': axis, 'origin': list(origin)}
    if e['glow']: out['light_emission'] = 15; out['shade'] = False
    return out


def model(name, kingdom):
    els = models.M[name]; used = sorted({t for e in els for t in [e['tex']] + list(e['over'].values())})
    tex = dict(models.COMMON); tex.update(models.TEX[kingdom])
    textures = {t: 'minecraft:block/' + tex[t] for t in used}
    textures['particle'] = 'minecraft:block/' + tex['w']
    return {'textures': textures, 'elements': [element(e) for e in els]}


def dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='\n') as f: json.dump(obj, f, separators=(',', ':'), sort_keys=True); f.write('\n')


def build(vanilla=None):
    ids = sorted(models.M)
    for kingdom in ('gf', 'sh'):
        for name in ids:
            m = model(name, kingdom)
            if vanilla:
                for t in m['textures'].values():
                    assert os.path.exists(os.path.join(vanilla, 'textures', 'block', t.split('/')[-1] + '.png')), (name, t)
            dump(os.path.join(PACK, 'assets', 'knightsrealm', 'models', 'furniture', kingdom, name + '.json'), m)
            dump(os.path.join(PACK, 'assets', 'knightsrealm', 'items', 'furniture', kingdom, name + '.json'),
                 {'model': {'type': 'minecraft:model', 'model': 'knightsrealm:furniture/%s/%s' % (kingdom, name)}})
    with open(os.path.join(PACK, 'pack.mcmeta'), 'w', newline='\n') as f:
        json.dump({'pack': {'pack_format': FORMAT, 'min_format': FORMAT, 'max_format': FORMAT,
                            'description': 'KnightsRealm furniture © 2026 KnightsRealm - All rights reserved'}}, f, indent=2); f.write('\n')
    with open(os.path.join(ROOT, 'furniture', 'furniture.txt'), 'w', newline='\n') as f:
        for name in ids:
            f.write('%s %d %d %d %d\n' % (name, models.SOLID.get(name, 0), models.WIDE.get(name, (0, 0))[0], models.WIDE.get(name, (0, 0))[1], models.LIGHT.get(name, 0)))
    return ids


def write_zip():
    out = os.path.join(ROOT, 'KnightsRealmFurniture.zip'); files = []
    for base, _, fs in os.walk(PACK):
        for fn in fs: files.append(os.path.join(base, fn))
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(files):
            info = zipfile.ZipInfo(os.path.relpath(path, PACK).replace(os.sep, '/'), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED; info.external_attr = 0o644 << 16
            z.writestr(info, open(path, 'rb').read(), compresslevel=9)
    print('KnightsRealmFurniture.zip', os.path.getsize(out), 'bytes, sha1', hashlib.sha1(open(out, 'rb').read()).hexdigest())


def preview(vanilla, kingdom='gf', S=9):
    """Every piece from the front left, boxes in the mean colour of their texture (rotated boxes drawn unrotated)."""
    from PIL import Image, ImageDraw, ImageFont
    tex = dict(models.COMMON); tex.update(models.TEX[kingdom]); col = {}
    for k, t in tex.items():
        im = Image.open(os.path.join(vanilla, 'textures', 'block', t + '.png')).convert('RGBA').crop((0, 0, 16, 16)); px = [p for p in im.getdata() if p[3] > 0]
        col[k] = tuple(sum(p[i] for p in px) // len(px) for i in range(3))
    ids = sorted(models.M); cols = 7; rows = (len(ids) + cols - 1) // cols; CW, CH = 62 * S // 2, 60 * S // 2
    sheet = Image.new('RGB', (cols * CW, rows * CH), (232, 228, 218)); d = ImageDraw.Draw(sheet)
    try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)
    except Exception: font = None
    for i, name in enumerate(ids):
        ox, oy = (i % cols) * CW + CW // 2, (i // cols) * CH + CH - 5 * S
        def P(x, y, z):                                               # seen from the north-west and above: the front (north) and the west side show
            X, Z = 16 - x, 16 - z
            return ox + (X - Z) * 0.866 * S / 2, oy + (X + Z) * 0.5 * S / 2 - y * S / 2 - 8 * S / 2
        els = sorted(models.M[name], key=lambda e: -(e['a'][0] + e['b'][0]) / 2 - (e['a'][2] + e['b'][2]) / 2 + (e['a'][1] + e['b'][1]) / 2)
        for e in els:
            (x0, y0, z0), (x1, y1, z1) = e['a'], e['b']
            def shade(face, k): c = col[e['over'].get(face, e['tex'])]; return tuple(min(255, int(v * k)) for v in c)
            g = 1.25 if e['glow'] else 1.0
            d.polygon([P(x0, y1, z0), P(x1, y1, z0), P(x1, y1, z1), P(x0, y1, z1)], fill=shade('up', 1.0 * g))
            d.polygon([P(x0, y0, z0), P(x1, y0, z0), P(x1, y1, z0), P(x0, y1, z0)], fill=shade('north', 0.8 * g))
            d.polygon([P(x0, y0, z0), P(x0, y0, z1), P(x0, y1, z1), P(x0, y1, z0)], fill=shade('west', 0.62 * g))
        d.text(((i % cols) * CW + 8, (i // cols) * CH + 6), name, fill=(40, 34, 28), font=font)
    out = os.path.join(ROOT, 'furniture', 'preview-%s.png' % kingdom); sheet.save(out); print(out, sheet.size)


if __name__ == '__main__':
    vanilla = sys.argv[1] if len(sys.argv) > 1 else None
    n = build(vanilla); print(len(n), 'pieces x 2 kingdoms:', ' '.join(n)); write_zip()
    if vanilla: preview(vanilla, 'gf'); preview(vanilla, 'sh')
