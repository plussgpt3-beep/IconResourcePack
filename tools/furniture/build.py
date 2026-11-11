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
import models, textures

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
        t = e['over'].get(f, e['tex'])
        if t in textures.FIT: uv = [0, 0, 16, 16]                             # a picture, stretched over the face
        faces[f] = {'uv': uv, 'texture': '#' + t}
    out = {'from': [x0, y0, z0], 'to': [x1, y1, z1], 'faces': faces}
    if e['rot']:
        ang, axis, origin = e['rot']; assert ang in (-45, -22.5, 22.5, 45) and axis in 'xyz'
        out['rotation'] = {'angle': ang, 'axis': axis, 'origin': list(origin)}
    if e['glow']: out['light_emission'] = 15; out['shade'] = False
    return out


def model(name, kingdom):
    els = models.M[name]; used = sorted({t for e in els for t in [e['tex']] + list(e['over'].values())})
    tx = {t: 'knightsrealm:block/furniture/%s/%s' % (kingdom, textures.NAMES[t]) for t in used}
    tx['particle'] = 'knightsrealm:block/furniture/%s/wood' % kingdom
    return {'textures': tx, 'elements': [element(e) for e in els]}


def dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='\n') as f: json.dump(obj, f, separators=(',', ':'), sort_keys=True); f.write('\n')


def build(vanilla=None):
    ids = sorted(models.M); textures.write(PACK)
    for kingdom in ('gf', 'sh'):
        for name in ids:
            m = model(name, kingdom)
            for t in m['textures'].values(): assert os.path.exists(os.path.join(PACK, 'assets', 'knightsrealm', 'textures', t.split(':')[1] + '.png')), (name, t)
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


def preview(kingdom='gf', S=10, ids=None, out=None, cols=8):
    """Every piece from the front left with its real textures, texel by texel (rotated boxes drawn unrotated)."""
    from PIL import Image, ImageDraw, ImageFont
    tex = {k: im.convert('RGB').load() for k, im in textures.paint(kingdom).items()}
    ids = ids or sorted(models.M); rows = (len(ids) + cols - 1) // cols; CW, CH = 66 * S // 2, 62 * S // 2
    sheet = Image.new('RGB', (cols * CW, rows * CH), (226, 221, 210)); d = ImageDraw.Draw(sheet)
    try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)
    except Exception: font = None
    def cuts(p0, p1, t0, t1):
        """The face from p0 to p1 carries the texture from t0 to t1: the pieces of it that fall in one texel each."""
        out = []; n = max(1, int(round(abs(t1 - t0) * 2))); lo = min(t0, t1)
        ks = sorted({t0, t1} | {float(k) for k in range(int(lo) - 1, int(max(t0, t1)) + 2) if lo < k < max(t0, t1)}, reverse=t1 < t0)
        for a, b in zip(ks[:-1], ks[1:]):
            pa = p0 + (p1 - p0) * (a - t0) / (t1 - t0); pb = p0 + (p1 - p0) * (b - t0) / (t1 - t0); out.append((pa, pb, min(15, max(0, int(min(a, b) + 1e-6)))))
        return out
    for i, name in enumerate(ids):
        ox, oy = (i % cols) * CW + CW // 2, (i // cols) * CH + CH - 6 * S
        def Pt(x, y, z):
            X, Z = 16 - x, 16 - z
            return ox + (X - Z) * 0.866 * S / 2, oy + (X + Z) * 0.5 * S / 2 - y * S / 2 - 8 * S / 2
        for e in sorted(models.M[name], key=lambda e: -(e['a'][0] + e['b'][0]) / 2 - (e['a'][2] + e['b'][2]) / 2 + (e['a'][1] + e['b'][1]) / 2):
            (x0, y0, z0), (x1, y1, z1) = e['a'], e['b']; el = element(e); g = 1.2 if e['glow'] else 1.0
            for face, k in (('up', 1.0), ('north', 0.78), ('west', 0.6)):
                u0, v0, u1, v1 = el['faces'][face]['uv']; px = tex[el['faces'][face]['texture'][1:]]
                if face == 'up': A, Bq = cuts(x0, x1, u0, u1), cuts(z0, z1, v0, v1)
                elif face == 'north': A, Bq = cuts(x1, x0, u0, u1), cuts(y1, y0, v0, v1)
                else: A, Bq = cuts(z0, z1, u0, u1), cuts(y1, y0, v0, v1)
                for (a0, a1, tu) in A:
                    for (b0, b1, tv) in Bq:
                        c = tuple(min(255, int(v * k * g)) for v in px[tu, tv])
                        if face == 'up': q = [Pt(a0, y1, b0), Pt(a1, y1, b0), Pt(a1, y1, b1), Pt(a0, y1, b1)]
                        elif face == 'north': q = [Pt(a0, b0, z0), Pt(a1, b0, z0), Pt(a1, b1, z0), Pt(a0, b1, z0)]
                        else: q = [Pt(x0, b0, a0), Pt(x0, b0, a1), Pt(x0, b1, a1), Pt(x0, b1, a0)]
                        d.polygon(q, fill=c)
        d.text(((i % cols) * CW + 8, (i // cols) * CH + 6), name, fill=(40, 34, 28), font=font)
    out = out or os.path.join(ROOT, 'furniture', 'preview-%s.png' % kingdom); sheet.save(out); print(out, sheet.size)


if __name__ == '__main__':
    vanilla = sys.argv[1] if len(sys.argv) > 1 else None
    n = build(vanilla); print(len(n), 'pieces x 2 kingdoms:', ' '.join(n)); write_zip()
    preview('gf'); preview('sh')
