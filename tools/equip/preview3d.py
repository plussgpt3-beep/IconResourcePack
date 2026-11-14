"""Whole-figure 3D preview: the worn layers on the player boxes with the 3D helm on the head."""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw
here = os.path.dirname(__file__); sys.path.insert(0, here)
import equip as E, helm3d as Hm

SKIN = np.array([0.62, 0.47, 0.37]); SHIRT = np.array([0.25, 0.35, 0.55]); PANTS = np.array([0.22, 0.22, 0.35])


def figure_quads(elem, tier, cell=2):
    l1, l2 = E.layer1(elem, tier), E.layer2(elem, tier)
    S = E.S
    quads = []
    def box(x0, y0, z0, x1, y1, z1, tex, fset, mirror=False, base=None, step=cell):
        for name, (u, v, w, h) in fset.items():
            if name == 'bottom': continue
            U, V, Wd, Hd = u * S, v * S, w * S, h * S
            for j in range(0, Hd, step):
                for i in range(0, Wd, step):
                    if tex is not None:
                        ii = (Wd - 1 - i) if mirror else i
                        c = tex[V + j, U + ii]
                        if c[3] == 0: continue
                        col = c[:3]
                    else:
                        col = base
                    a0, a1 = i / Wd, min(1, (i + step) / Wd); b0, b1 = j / Hd, min(1, (j + step) / Hd)
                    if name == 'front':
                        P = lambda a, b: (x0 + (x1 - x0) * a, y1 - (y1 - y0) * b, z0)
                    elif name == 'back':
                        P = lambda a, b: (x1 - (x1 - x0) * a, y1 - (y1 - y0) * b, z1)
                    elif name == 'right':
                        P = lambda a, b: (x0, y1 - (y1 - y0) * b, z1 - (z1 - z0) * a)
                    elif name == 'left':
                        P = lambda a, b: (x1, y1 - (y1 - y0) * b, z0 + (z1 - z0) * a)
                    else:  # top
                        P = lambda a, b: (x0 + (x1 - x0) * a, y1, z0 + (z1 - z0) * b)
                    if mirror and name in ('right', 'left'):
                        pass
                    quads.append(([P(a0, b0), P(a1, b0), P(a1, b1), P(a0, b1)], col, name))
    # bare body
    for (x0, y0, z0, x1, y1, z1, c, f) in ((-4, 24, -4, 4, 32, 4, SKIN, E.HEAD), (-4, 12, -2, 4, 24, 2, SHIRT, E.BODY),
                                           (-8, 12, -2, -4, 24, 2, SKIN, E.ARM), (4, 12, -2, 8, 24, 2, SKIN, E.ARM),
                                           (-4, 0, -2, 0, 12, 2, PANTS, E.LEG), (0, 0, -2, 4, 12, 2, PANTS, E.LEG)):
        box(x0, y0, z0, x1, y1, z1, None, f, base=c, step=E.S)
    g1, g2 = 1.0, 0.5
    box(-4 - g1, 12 - g1, -2 - g1, 4 + g1, 24 + g1, 2 + g1, l1, E.BODY)
    box(-4 - g2, 12 - g2, -2 - g2, 4 + g2, 24 + g2, 2 + g2, l2, E.BODY)
    box(-8 - g1, 12 - g1, -2 - g1, -4 + g1, 24 + g1, 2 + g1, l1, E.ARM)
    box(4 - g1, 12 - g1, -2 - g1, 8 + g1, 24 + g1, 2 + g1, l1, E.ARM, mirror=True)
    for x0, mir in ((-4, False), (0, True)):
        box(x0 - g2, 0 - g2, -2 - g2, x0 + 4 + g2, 12 + g2, 2 + g2, l2, E.LEG, mirror=mir)
        box(x0 - g1, 0 - g1, -2 - g1, x0 + 4 + g1, 12 + g1, 2 + g1, l1, E.LEG, mirror=mir)
    # helm: model units -> pixels (16 units = 10 px), centred on the head centre
    tex = Hm.atlas(elem, tier); m = Hm.model(elem, tier); k = 0.625
    for e in m['elements']:
        (a0, b0, c0), (a1, b1, c1) = e['from'], e['to']
        r = e.get('rotation')
        def W(p):
            if r:
                ang = math.radians(r['angle']); o = r['origin']; x, y, z = (p[i] - o[i] for i in range(3))
                cc, ss = math.cos(ang), math.sin(ang)
                if r['axis'] == 'x': y, z = y * cc - z * ss, y * ss + z * cc
                if r['axis'] == 'y': x, z = x * cc + z * ss, -x * ss + z * cc
                if r['axis'] == 'z': x, y = x * cc - y * ss, x * ss + y * cc
                p = (x + o[0], y + o[1], z + o[2])
            return ((p[0] - 8) * k, 28 + (p[1] - 8) * k, (p[2] - 8) * k)
        F = {'north': [(a1, b1, c0), (a0, b1, c0), (a0, b0, c0), (a1, b0, c0)], 'south': [(a0, b1, c1), (a1, b1, c1), (a1, b0, c1), (a0, b0, c1)],
             'west': [(a0, b1, c0), (a0, b1, c1), (a0, b0, c1), (a0, b0, c0)], 'east': [(a1, b1, c1), (a1, b1, c0), (a1, b0, c0), (a1, b0, c1)],
             'up': [(a0, b1, c0), (a1, b1, c0), (a1, b1, c1), (a0, b1, c1)], 'down': [(a0, b0, c1), (a1, b0, c1), (a1, b0, c0), (a0, b0, c0)]}
        lm = {'north': 'front', 'south': 'back', 'west': 'right', 'east': 'left', 'up': 'top', 'down': 'bottom'}
        for d, fd in e['faces'].items():
            pts = F[d]; u0, v0, u1, v1 = (q * 4 for q in fd['uv']); n = 10
            for i in range(n):
                for j in range(n):
                    def at(a, b):
                        top = [pts[0][q] + (pts[1][q] - pts[0][q]) * a for q in range(3)]
                        bot = [pts[3][q] + (pts[2][q] - pts[3][q]) * a for q in range(3)]
                        return W([top[q] + (bot[q] - top[q]) * b for q in range(3)])
                    cell4 = [at(i / n, j / n), at((i + 1) / n, j / n), at((i + 1) / n, (j + 1) / n), at(i / n, (j + 1) / n)]
                    tx, ty = int(u0 + (u1 - u0) * (i + .5) / n), int(v0 + (v1 - v0) * (j + .5) / n)
                    quads.append((cell4, tex[min(ty, 63), min(tx, 63)][:3], lm[d]))
    return quads


def render(elem, tier, yaw, pitch=-15, size=(260, 420)):
    light = {'front': .95, 'back': .8, 'right': .78, 'left': .86, 'top': 1.1, 'bottom': .55}
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw)); cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))
    def proj(p):
        x, y, z = p[0], p[1] - 16, p[2]
        x, z = x * cy - z * sy, x * sy + z * cy
        y, z = y * cp - z * sp, y * sp + z * cp
        return x, y, z
    img = Image.new('RGBA', size, (36, 36, 38, 255)); d = ImageDraw.Draw(img); sc = 9.5
    items = []
    for pts, col, name in figure_quads(elem, tier):
        pr = [proj(p) for p in pts]
        items.append((sum(p[2] for p in pr) / 4, pr, np.clip(np.array(col) * light[name], 0, 1)))
    for depth, pr, c in sorted(items, key=lambda q: -q[0]):
        d.polygon([(size[0] / 2 + p[0] * sc, size[1] * 0.52 - p[1] * sc) for p in pr], fill=tuple(int(v * 255) for v in c))
    return img


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '/mnt/user-data/outputs/armour-3d.png'
    cw, ch = 260, 420
    sheet = Image.new('RGBA', (4 * (2 * cw + 20) + 20, 3 * (ch + 30) + 20), (36, 36, 38, 255)); dr = ImageDraw.Draw(sheet)
    for i, e in enumerate(E.ELEMS):
        for j, t in enumerate(E.TIERS):
            x, y = 20 + i * (2 * cw + 20), 20 + j * (ch + 30)
            sheet.paste(render(e, t, -25), (x, y)); sheet.paste(render(e, t, 155), (x + cw, y))
            dr.text((x + 5, y + ch + 4), '%s t%d (front | back)' % (e, t), fill=(240, 240, 240, 255))
    sheet.save(out)
