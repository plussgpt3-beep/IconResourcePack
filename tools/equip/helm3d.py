"""3D helms worn on the head (item model in the 'head' display context): each element/tier its own shape.
t2 kettle hat with brim and nasal (open face), t3 closed great helm with crest, t4 great helm with element
ornaments (fire horns, ice crown, storm wings, venom serpent crest). The head spans 1.6..14.4 in model units."""
import os, sys, math, json
import numpy as np
from PIL import Image, ImageDraw
here = os.path.dirname(__file__); sys.path.insert(0, here)
import equip as E

A = 64           # atlas size
SW = {'metal': (0, 0), 'trim': (16, 0), 'dark': (32, 0), 'glow': (48, 0), 'leather': (0, 48), 'metal2': (16, 48),
      'front': (0, 16), 'side': (32, 16)}
SIZE = {'front': (32, 32), 'side': (32, 32)}


def atlas(elem, tier):
    L = E.Layer(elem, tier, 9)
    img = np.zeros((A, A, 4))
    def fill(name, colour, shade=True):
        x0, y0 = SW[name]; w, h = SIZE.get(name, (16, 16))
        for y in range(h):
            for x in range(w):
                t = (x + .5) / w
                c = colour * ((0.85 + 0.25 * math.sin(math.pi * t)) if shade else 1) * (0.95 + 0.08 * L.rng.random())
                if shade and (x < 1 or y < 1): c = c * 1.25
                if shade and (x >= w - 1 or y >= h - 1): c = c * 0.7
                img[y0 + y, x0 + x, :3] = np.clip(c, 0, 1); img[y0 + y, x0 + x, 3] = 1
    fill('metal', L.metal); fill('trim', L.trim); fill('dark', E.C((0.05, 0.05, 0.06)), False)
    fill('glow', L.glow, False); fill('leather', L.leather); fill('metal2', L.metal * 0.8)
    fill('front', L.metal); fill('side', L.metal)
    # engrave the front/side panels using the layer painter on a scratch canvas
    for name in ('front', 'side'):
        x0, y0 = SW[name]
        scratch = E.Layer(elem, tier, 10 + len(name))
        scratch.img = np.zeros((E.H, E.W, 4))
        f = (0, 0, 8, 8)
        scratch.img[0:32, 0:32] = img[y0:y0 + 32, x0:x0 + 32]
        if tier >= 3 and name == 'side': scratch.engrave(f, None, 1)
        if name == 'front' and tier >= 3:
            for k in range(3):
                for side in (5, 24):
                    for y in range(20 + k * 3, 21 + k * 3):
                        for x in range(side, side + 3): scratch.put(x, y, E.C((0.05, 0.05, 0.06)))
        img[y0:y0 + 32, x0:x0 + 32] = scratch.img[0:32, 0:32]
    return img


def uv(name, w=None, h=None):
    x0, y0 = SW[name]; sw, sh = SIZE.get(name, (16, 16))
    return [x0 / 4, y0 / 4, (x0 + sw) / 4, (y0 + sh) / 4]


def box(fr, to, tex='metal', faces=None, rot=None, over=None):
    over = over or {}
    f = {}
    for d in ('north', 'south', 'east', 'west', 'up', 'down'):
        if faces and d not in faces: continue
        f[d] = {'uv': uv(over.get(d, tex)), 'texture': '#t'}
    e = {'from': [round(v, 3) for v in fr], 'to': [round(v, 3) for v in to], 'faces': f}
    if rot: e['rotation'] = rot
    return e


def mirror(e):
    m = json.loads(json.dumps(e))
    a, b = m['from'][0], m['to'][0]
    m['from'][0], m['to'][0] = 16 - b, 16 - a
    if 'rotation' in m:
        r = m['rotation']; r['origin'][0] = 16 - r['origin'][0]
        if r['axis'] in ('y', 'z'): r['angle'] = -r['angle']
    if 'east' in m['faces'] and 'west' in m['faces']:
        m['faces']['east'], m['faces']['west'] = m['faces']['west'], m['faces']['east']
    return m


def great_helm(slit='dark'):
    lo, hi = 1.6, 14.4; o = 0.5
    els = [
        box([lo - o, lo, lo - o], [hi + o, 8.2, lo + 0.5], over={'north': 'front'}),          # face plate lower
        box([lo - o, 9.6, lo - o], [hi + o, hi + o, lo + 0.5], over={'north': 'front'}),      # face plate upper
        box([lo, 8.2, lo - 0.2], [hi, 9.6, lo + 0.3], slit),                                  # eye slit (dark/glow)
        box([lo - o, lo, lo - o], [lo, hi + o, hi + o], over={'west': 'side', 'east': 'side'}),
        box([hi, lo, lo - o], [hi + o, hi + o, hi + o], over={'west': 'side', 'east': 'side'}),
        box([lo, lo, hi], [hi, hi + o, hi + o], over={'south': 'side'}),
        box([lo, hi, lo], [hi, hi + o, hi], 'metal'),
        box([lo - o - .3, 9.6, lo - o - .3], [hi + o + .3, 10.4, lo], 'trim'),                # brow band
        box([7.3, lo, lo - o - .4], [8.7, 8.2, lo - o], 'trim'),                              # cross bar
    ]
    return els


def kettle():
    lo, hi = 1.6, 14.4; o = 0.5
    return [
        box([lo - o, 10.0, lo - o], [hi + o, hi + o, hi + o], over={'north': 'front', 'west': 'side', 'east': 'side'}),
        box([4, hi + o, 4], [12, hi + 1.3, 12], 'metal'),                                    # dome
        box([-1.0, 9.4, -1.0], [17.0, 10.2, 17.0], 'metal2'),                                # wide brim
        box([-1.2, 9.2, -1.2], [17.2, 9.6, 17.2], 'trim'),
        box([lo - o, 4.0, 7.0], [hi + o, 10.0, hi + o], 'metal', over={'west': 'side', 'east': 'side'}),   # back/neck guard
        box([lo - o, 5.0, lo + 1], [lo, 10.0, 7.0], 'leather'),                             # cheek straps
        box([hi, 5.0, lo + 1], [hi + o, 10.0, 7.0], 'leather'),
        box([7.4, 6.4, lo - o - .5], [8.6, 10.0, lo - o], 'trim'),                           # nasal
    ]


def ornament(elem):
    els = []
    if elem == 'fire':                       # curling horns
        segs = [([-0.6, 10.5, 6.0], [1.4, 12.8, 9.0], None),
                ([-2.6, 12.0, 6.4], [-0.4, 14.6, 8.6], {'angle': 22.5, 'axis': 'z', 'origin': [-0.4, 12, 7.5]}),
                ([-3.6, 14.2, 6.8], [-1.8, 17.4, 8.2], {'angle': 45, 'axis': 'z', 'origin': [-1.8, 14.2, 7.5]}),
                ([-3.2, 17.0, 7.1], [-2.0, 19.4, 7.9], {'angle': 22.5, 'axis': 'z', 'origin': [-2, 17, 7.5]})]
        for i, (a, b, r) in enumerate(segs):
            e = box(a, b, 'trim' if i < 2 else 'glow', rot=r); els += [e, mirror(e)]
    elif elem == 'ice':                      # crown of icicles
        for i, x in enumerate([2.6, 5.0, 7.4, 9.8, 12.2]):
            h = [2.5, 4.0, 5.5, 4.0, 2.5][i]
            els.append(box([x, 14.9, 2.2], [x + 1.4, 14.9 + h, 3.6], 'glow'))
            els.append(box([x + .3, 14.9 + h, 2.5], [x + 1.1, 15.6 + h, 3.3], 'trim'))
        els.append(box([1.4, 14.6, 1.6], [14.6, 15.3, 4.0], 'trim'))
    elif elem == 'storm':                    # swept wings
        for i, (y, ln, ang) in enumerate(((9.5, 8, 22.5), (11.5, 9, 0), (13.5, 7, -22.5))):
            e = box([-0.9, y, 6 - i], [-0.1, y + 1.4, 6 - i + ln], 'glow' if i == 1 else 'trim',
                    rot={'angle': ang, 'axis': 'x', 'origin': [-0.5, y, 8]} if ang else None)
            els += [e, mirror(e)]
    else:                                    # serpent crest + fangs
        for i, z in enumerate([2.0, 4.6, 7.2, 9.8, 12.4]):
            h = [3.0, 4.0, 4.4, 3.6, 2.6][i]
            els.append(box([7.0, 14.9, z], [9.0, 14.9 + h, z + 2.4], 'trim' if i % 2 else 'metal'))
        els.append(box([7.4, 17.2, 0.6], [8.6, 19.0, 2.4], 'glow'))
        for x in (4.4, 10.8):
            els.append(box([x, 6.0, 0.4], [x + 0.8, 8.2, 0.9], 'glow'))
    return els


def model(elem, tier):
    if tier == 2: els = kettle()
    elif tier == 3: els = great_helm() + [box([7.4, 14.9, 2.0], [8.6, 17.6, 14.0], 'trim')]
    else: els = great_helm('glow') + ornament(elem)
    return {'textures': {'t': 'knightsrealm:item/helm3d/gear_%s_t%d' % (elem, tier), 'particle': 'knightsrealm:item/helm3d/gear_%s_t%d' % (elem, tier)},
            'elements': els}


# ---------------- tiny renderer for the preview sheet ----------------
def render(elem, tier, size=220, yaw=-30, pitch=-20):
    tex = atlas(elem, tier); m = model(elem, tier)
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))
    def proj(p):
        x, y, z = p[0] - 8, p[1] - 8, p[2] - 8
        x, z = x * cy - z * sy, x * sy + z * cy
        y, z = y * cp - z * sp, y * sp + z * cp
        return x, y, z
    def rotp(p, r):
        if not r: return p
        a = math.radians(r['angle']); o = r['origin']; x, y, z = (p[i] - o[i] for i in range(3))
        c, s = math.cos(a), math.sin(a)
        if r['axis'] == 'x': y, z = y * c - z * s, y * s + z * c
        if r['axis'] == 'y': x, z = x * c + z * s, -x * s + z * c
        if r['axis'] == 'z': x, y = x * c - y * s, x * s + y * c
        return (x + o[0], y + o[1], z + o[2])
    quads = []
    m = {'elements': [{'from': [1.6, 1.6, 1.6], 'to': [14.4, 14.4, 14.4], 'faces': {d: {'uv': [0, 12, 4, 16], 'skin': 1} for d in ('north','south','east','west','up','down')}}] + m['elements']}
    light = {'north': .95, 'south': .7, 'east': .8, 'west': .85, 'up': 1.1, 'down': .55}
    for e in m['elements']:
        (x0, y0, z0), (x1, y1, z1) = e['from'], e['to']
        F = {'north': [(x1, y1, z0), (x0, y1, z0), (x0, y0, z0), (x1, y0, z0)],
             'south': [(x0, y1, z1), (x1, y1, z1), (x1, y0, z1), (x0, y0, z1)],
             'west': [(x0, y1, z0), (x0, y1, z1), (x0, y0, z1), (x0, y0, z0)],
             'east': [(x1, y1, z1), (x1, y1, z0), (x1, y0, z0), (x1, y0, z1)],
             'up': [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)],
             'down': [(x0, y0, z1), (x1, y0, z1), (x1, y0, z0), (x0, y0, z0)]}
        for d, fd in e['faces'].items():
            pts = [rotp(p, e.get('rotation')) for p in F[d]]
            u0, v0, u1, v1 = (k * 4 for k in fd['uv'])
            n = 12
            for i in range(n):
                for j in range(n):
                    def at(a, b):
                        top = [pts[0][k] + (pts[1][k] - pts[0][k]) * a for k in range(3)]
                        bot = [pts[3][k] + (pts[2][k] - pts[3][k]) * a for k in range(3)]
                        return [top[k] + (bot[k] - top[k]) * b for k in range(3)]
                    cell = [at(i / n, j / n), at((i + 1) / n, j / n), at((i + 1) / n, (j + 1) / n), at(i / n, (j + 1) / n)]
                    tx = int(u0 + (u1 - u0) * (i + .5) / n); ty = int(v0 + (v1 - v0) * (j + .5) / n)
                    c = np.array([0.62, 0.47, 0.37, 1]) if fd.get('skin') else tex[min(ty, A - 1), min(tx, A - 1)]
                    pr = [proj(p) for p in cell]
                    depth = sum(p[2] for p in pr) / 4
                    quads.append((depth, pr, np.clip(c[:3] * light[d], 0, 1)))
    img = Image.new('RGBA', (size, size), (36, 36, 38, 255)); d = ImageDraw.Draw(img)
    sc = size / 30
    # head for scale
    for depth, pr, c in sorted(quads, key=lambda q: -q[0]):
        d.polygon([(size / 2 + p[0] * sc, size * 0.58 - p[1] * sc) for p in pr], fill=tuple(int(v * 255) for v in c))
    return img


def write(root):
    a = os.path.join(root, 'assets', 'knightsrealm')
    for e in E.ELEMS:
        for t in E.TIERS:
            i = 'gear_%s_t%d' % (e, t)
            E.save(atlas(e, t), os.path.join(a, 'textures', 'item', 'helm3d', i + '.png'))
            os.makedirs(os.path.join(a, 'models', 'item', 'helm3d'), exist_ok=True)
            m = model(e, t)
            m['display'] = {'head': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]}}
            with open(os.path.join(a, 'models', 'item', 'helm3d', i + '.json'), 'w') as f: json.dump(m, f)


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '/mnt/user-data/outputs/helm-sheet.png'
    sheet = Image.new('RGBA', (4 * 240 + 20, 3 * 250 + 20), (36, 36, 38, 255)); d = ImageDraw.Draw(sheet)
    for i, e in enumerate(E.ELEMS):
        for j, t in enumerate(E.TIERS):
            sheet.paste(render(e, t), (20 + i * 240, 20 + j * 250))
            d.text((25 + i * 240, 20 + j * 250 + 222), '%s t%d' % (e, t), fill=(240, 240, 240, 255))
    sheet.save(out)
