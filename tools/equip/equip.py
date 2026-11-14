"""Worn looks (equipment layers) of evolved armour: 4 elements x tiers 2-4, drawn from scratch on the vanilla
humanoid layout at 4x (256x128): bevelled plates with rounded shading, brushed metal, rivets, gilded trim,
leather straps, mail in the gaps, and element engravings that glow from tier 3. Deterministic per element/tier."""
import sys, os, zlib, math, json
import numpy as np
from PIL import Image
here = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(here, '..', 'icons')); sys.path.insert(0, os.path.join(here, '..'))
from _gear import ELEMENTS
from _gear2 import DARK

ELEMS = ['fire', 'ice', 'storm', 'venom']
TIERS = [2, 3, 4]
S = 4                       # texels per vanilla pixel
W, H = 64 * S, 32 * S


def faces(u, v, w, h, d):
    return {'top': (u + d, v, w, d), 'bottom': (u + d + w, v, w, d),
            'right': (u, v + d, d, h), 'front': (u + d, v + d, w, h),
            'left': (u + d + w, v + d, d, h), 'back': (u + 2 * d + w, v + d, w, h)}

HEAD, BODY = faces(0, 0, 8, 8, 8), faces(16, 16, 8, 12, 4)
ARM, LEG = faces(40, 16, 4, 12, 4), faces(0, 16, 4, 12, 4)
FACE_LIGHT = {'top': 1.12, 'front': 1.0, 'right': 0.86, 'left': 0.86, 'back': 0.8, 'bottom': 0.6}
SIDES = ('front', 'right', 'left', 'back')


def C(c): return np.array(c, float)
def mix(a, b, t): return a * (1 - t) + b * t


class Layer:
    def __init__(self, elem, tier, salt):
        self.img = np.zeros((H, W, 4))
        self.rng = np.random.default_rng(zlib.crc32(repr(('equip2', elem, tier, salt)).encode()))
        blade, glow, guard, grip = (C(c) for c in ELEMENTS[elem])
        steel = C((0.78, 0.80, 0.83))
        self.metal = mix(C(DARK[elem]), steel * 0.35, 0.25) if tier == 4 else mix(blade, steel, 0.45 if tier == 2 else 0.25)
        self.trim = mix(guard, C((0.95, 0.78, 0.35)), 0.55 if tier < 4 else 0.25)
        self.leather = mix(grip, C((0.32, 0.20, 0.12)), 0.6)
        self.glow, self.elem, self.tier = glow, elem, tier

    # --- primitives on a face rect given in vanilla px; rows are vanilla rows inside the face ---
    def rect(self, f, rows=None):
        u, v, w, h = f
        r0, r1 = rows if rows else (0, h)
        return u * S, (v + r0) * S, w * S, (r1 - r0) * S

    def put(self, x, y, c, a=1.0):
        if 0 <= x < W and 0 <= y < H:
            base = self.img[y, x]
            if a >= 1 or base[3] == 0:
                base[:3] = np.clip(c, 0, 1); base[3] = max(base[3], a) if a < 1 else 1
            else:
                base[:3] = np.clip(mix(base[:3], c, a), 0, 1)

    def plate(self, f, name, rows=None, colour=None, round_=True, bevel=2):
        x0, y0, w, h = self.rect(f, rows)
        col = self.metal if colour is None else colour
        lit = FACE_LIGHT[name]
        streak = self.rng.random(h) * 0.06
        hi_x = 0.28 + 0.1 * self.rng.random()
        for y in range(h):
            for x in range(w):
                t = (x + 0.5) / w
                curve = (0.80 + 0.28 * math.sin(math.pi * t)) if round_ and name not in ('top', 'bottom') else 1.0
                spec = 0.35 * math.exp(-((t - hi_x) / 0.07) ** 2) if name in ('front', 'back', 'top') else 0.0
                s = lit * curve * (1.04 - 0.14 * y / h) * (0.97 + streak[y] + 0.04 * self.rng.random())
                c = col * s + spec * 0.6
                if x < bevel or y < bevel: c = c * 1.28 + 0.06
                elif x >= w - bevel or y >= h - bevel: c = c * 0.62
                self.put(x0 + x, y0 + y, c)
        return x0, y0, w, h

    def wear(self, f, rows=None, n=6):
        x0, y0, w, h = self.rect(f, rows)
        for _ in range(n):            # scratches
            x, y = self.rng.integers(2, w - 2), self.rng.integers(2, h - 2)
            ln = int(self.rng.integers(2, 6))
            for k in range(ln):
                xx, yy = x0 + x + k, y0 + y + (k // 2)
                if xx < x0 + w - 2 and yy < y0 + h - 2:
                    self.put(xx, yy, C((1, 1, 1)), 0.25)

    def trimband(self, f, rows, row_at, thick=2):
        x0, y0, w, h = self.rect(f, rows)
        yy = y0 + row_at
        for y in range(yy, min(yy + thick, y0 + h)):
            for x in range(w):
                c = self.trim * (1.25 if y == yy else 0.8) * (0.95 + 0.1 * math.sin(x * 0.9))
                self.put(x0 + x, y, c)

    def edge_trim(self, f, rows=None, thick=2):
        x0, y0, w, h = self.rect(f, rows)
        for y in range(h):
            for x in range(w):
                if x < thick or x >= w - thick or y < thick or y >= h - thick:
                    lit = 1.3 if (x < thick or y < thick) else 0.7
                    self.put(x0 + x, y0 + y, self.trim * lit)

    def rivet(self, x, y):
        self.put(x, y, mix(self.metal, C((1, 1, 1)), 0.7)); self.put(x + 1, y, mix(self.metal, C((1, 1, 1)), 0.45))
        self.put(x, y + 1, mix(self.metal, C((1, 1, 1)), 0.45)); self.put(x + 1, y + 1, self.metal * 0.45)

    def mail(self, f, name, rows=None):
        x0, y0, w, h = self.rect(f, rows)
        base = C((0.42, 0.43, 0.46)) * FACE_LIGHT[name]
        for y in range(h):
            for x in range(w):
                ring = ((x + (y // 2) % 2 * 2) % 4, y % 2)
                c = base * (1.35 if ring == (1, 0) else 0.75 if ring[1] == 1 else 1.0)
                self.put(x0 + x, y0 + y, c)

    def strap(self, f, rows, x_at, wid=3):
        x0, y0, w, h = self.rect(f, rows)
        for y in range(h):
            for x in range(x_at, min(w, x_at + wid)):
                c = self.leather * (1.15 if x == x_at else 0.8 if x == x_at + wid - 1 else 1.0) * (0.92 + 0.12 * self.rng.random())
                self.put(x0 + x, y0 + y, c)

    def line(self, pts, col, under=True):
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            n = int(max(abs(bx - ax), abs(by - ay))) + 1
            for k in range(n):
                t = k / max(n - 1, 1)
                x, y = int(round(ax + (bx - ax) * t)), int(round(ay + (by - ay) * t))
                if under: self.put(x + 1, y + 1, self.metal * 0.35)
                self.put(x, y, col)

    def engrave(self, f, rows=None, count=1):
        """Element motif inside a face: flames, frost, bolts or creeping venom; glows from tier 3, etched at tier 2."""
        x0, y0, w, h = self.rect(f, rows)
        glow = self.glow if self.tier >= 3 else mix(self.metal, C((0, 0, 0)), 0.45)
        bright = mix(self.glow, C((1, 1, 1)), 0.45)
        r = self.rng
        for _ in range(count):
            cx = x0 + int(r.integers(3, max(4, w - 3)))
            if self.elem == 'fire':
                for k in (-2, 0, 2):
                    base_y = y0 + h - 3
                    top = y0 + int(h * (0.35 + 0.15 * r.random()))
                    pts = [(cx + k * 2, base_y), (cx + k * 2 + 2, (base_y + top) // 2 + 2), (cx + k * 2 - 1, (base_y + top) // 2), (cx + k, top)]
                    self.line(pts, glow)
            elif self.elem == 'ice':
                cy = y0 + int(r.integers(4, max(5, h - 4)))
                ln = min(w, h) // 3
                for a in range(0, 180, 60):
                    dx, dy = math.cos(math.radians(a)) * ln, math.sin(math.radians(a)) * ln
                    self.line([(cx - dx, cy - dy), (cx + dx, cy + dy)], glow)
                self.put(cx, cy, bright)
            elif self.elem == 'storm':
                y = y0 + 2; x = cx; pts = [(x, y)]
                while y < y0 + h - 3:
                    y += int(r.integers(3, 6)); x += int(r.choice([-3, 3]))
                    x = max(x0 + 2, min(x0 + w - 3, x)); pts.append((x, min(y, y0 + h - 3)))
                self.line(pts, glow)
            else:
                y = y0 + 2; x = cx; pts = [(x, y)]
                for _ in range(5):
                    y += int(r.integers(2, 5)); x += int(r.integers(-2, 3)); pts.append((x, min(y, y0 + h - 4)))
                self.line(pts, glow)
                lx, ly = pts[-1]
                self.put(lx, ly + 1, bright); self.put(lx, ly + 2, glow)
        if self.tier == 4:            # embers / sparks around the motif
            for _ in range(4):
                self.put(x0 + int(r.integers(2, w - 2)), y0 + int(r.integers(2, h - 2)), bright)

    def core(self, x, y, rad=4):
        for dy in range(-rad, rad + 1):
            for dx in range(-rad, rad + 1):
                d = math.hypot(dx, dy)
                if d <= rad:
                    self.put(x + dx, y + dy, mix(C((1, 1, 1)), self.glow, min(1, d / rad + 0.2)), 1 if d < rad - 1 else 0.6)


def layer1(elem, tier):
    L = Layer(elem, tier, 1)
    # ---- helmet layer (used only when the 3D helm model is missing) ----
    for n in ('top', 'right', 'left', 'back', 'bottom', 'front'):
        L.plate(HEAD[n], n)
    x0, y0, w, h = L.rect(HEAD['front'])
    for x in range(4, w - 4):
        for y in range(4 * S, 4 * S + 3): L.put(x0 + x, y0 + y, C((0.04, 0.04, 0.05)))
    if tier == 2: brigandine(L)
    elif tier == 3: half_plate(L)
    else: full_plate(L)
    return L.img


def brigandine(L):
    """Tier 2: a cloth-covered brigandine studded with small plates, mail sleeves, leather bracers and boots."""
    cloth = mix(L.trim, L.leather, 0.55) * 0.85
    for n in ('top', 'bottom'): L.plate(BODY[n], n, colour=cloth, round_=False)
    for n in SIDES:
        x0, y0, w, h = L.plate(BODY[n], n, colour=cloth, round_=True, bevel=1)
        for y in range(5, h - 4, 7):                 # rows of rivets over hidden plates
            off = 3 if (y // 7) % 2 else 6
            for x in range(off, w - 3, 7): L.rivet(x0 + x, y0 + y)
        L.trimband(BODY[n], None, 12 * S - 4, 2)
    bx, by, bw, bh = L.rect(BODY['front'])
    for y in range(2, 9 * S):                         # front lacing
        L.put(bx + bw // 2, by + y, L.leather * (1.2 if y % 4 < 2 else 0.6))
    L.plate(BODY['front'], 'front', (1, 5), colour=L.metal)    # small breast plate
    L.engrave(BODY['front'], (1, 5), 1)
    for n in SIDES:
        L.mail(ARM[n], n, (0, 9))
        L.plate(ARM[n], n, (9, 12), colour=L.leather * 1.1, round_=True, bevel=1)
        L.strap(ARM[n], (0, 2), 0, ARM[n][2] * S)
    L.mail(ARM['top'], 'top'); L.plate(ARM['bottom'], 'bottom', colour=L.leather)
    for n in SIDES:                                  # leather boots with a steel toe cap
        L.plate(LEG[n], n, (8, 12), colour=L.leather * 1.05, bevel=1)
        L.strap(LEG[n], (8, 9), 0, LEG[n][2] * S)
    L.plate(LEG['front'], 'front', (10, 12)); L.plate(LEG['bottom'], 'bottom', colour=L.leather * 0.7)


def half_plate(L):
    """Tier 3: breastplate with lames, layered pauldrons over a mail sleeve, vambraces, sabatons."""
    for n in ('top', 'bottom'): L.plate(BODY[n], n)
    for n in SIDES:
        L.plate(BODY[n], n, (0, 8))
        for k, r in enumerate(((8, 10), (10, 12))):
            L.plate(BODY[n], n, r, colour=L.metal * (0.95 - 0.05 * k))
        L.wear(BODY[n], (0, 8), 5)
    bx, by, bw, bh = L.rect(BODY['front'])
    for y in range(3, 8 * S - 2):
        L.put(bx + bw // 2 - 1, by + y, L.metal * 1.5); L.put(bx + bw // 2, by + y, L.metal * 0.55)
    L.edge_trim(BODY['front'], (0, 1), 2)
    for n in ('front', 'back'): L.trimband(BODY[n], None, 8 * S - 2, 2)
    for rx, ry in ((3, 3), (bw - 5, 3), (3, 8 * S - 6), (bw - 5, 8 * S - 6)): L.rivet(bx + rx, by + ry)
    L.strap(BODY['right'], (0, 12), 6, 4); L.strap(BODY['left'], (0, 12), 6, 4)
    L.strap(BODY['back'], (0, 8), 4, 3); L.strap(BODY['back'], (0, 8), bw - 7, 3)
    L.engrave(BODY['front'], (1, 8), 2); L.engrave(BODY['back'], (1, 8), 1)
    L.plate(ARM['top'], 'top')
    for n in SIDES:
        L.plate(ARM[n], n, (0, 2)); L.plate(ARM[n], n, (2, 4), colour=L.metal * 0.93)
        L.mail(ARM[n], n, (4, 8))
        L.plate(ARM[n], n, (8, 12)); L.trimband(ARM[n], (8, 12), 0, 2)
    L.trimband(ARM['front'], (0, 2), 0, 2)
    L.engrave(ARM['front'], (8, 12), 1); L.engrave(ARM['right'], (0, 4), 1)
    L.plate(ARM['bottom'], 'bottom')
    L.plate(LEG['bottom'], 'bottom')
    for n in SIDES:
        L.plate(LEG[n], n, (7, 10)); L.plate(LEG[n], n, (10, 12), colour=L.metal * 0.9)
        L.trimband(LEG[n], (7, 12), 0, 2)
    L.engrave(LEG['front'], (7, 12), 1)


def flutes(L, f, rows, step=6):
    x0, y0, w, h = L.rect(f, rows)
    for x in range(3, w - 3, step):
        for y in range(3, h - 3):
            L.put(x0 + x, y0 + y, L.metal * 1.45); L.put(x0 + x + 1, y0 + y, L.metal * 0.5)


def spikes(L, f, rows, up=True, n=3, glow=False):
    """Pointed rims (a jagged silhouette): saw-tooth notches cut out of the top of a band."""
    x0, y0, w, h = L.rect(f, rows)
    tooth = w // n
    for k in range(n):
        for x in range(tooth):
            depth = int(abs(x - tooth / 2) / (tooth / 2) * 6)
            for y in range(depth):
                yy = y0 + (y if up else h - 1 - y)
                L.img[yy, x0 + k * tooth + x, 3] = 0
            if glow:
                yy = y0 + (depth if up else h - 1 - depth)
                L.put(x0 + k * tooth + x, yy, L.glow)


def full_plate(L):
    """Tier 4: full fluted gothic plate: one-piece breastplate, great spiked pauldrons, couters, greaves, pointed sabatons."""
    for n in ('top', 'bottom'): L.plate(BODY[n], n)
    for n in SIDES:
        L.plate(BODY[n], n, (0, 12))
        flutes(L, BODY[n], (1, 8))
        L.trimband(BODY[n], None, 8 * S - 2, 3)
        L.wear(BODY[n], (0, 12), 3)
    bx, by, bw, bh = L.rect(BODY['front'])
    L.edge_trim(BODY['front'], (0, 2), 3)
    L.engrave(BODY['front'], (2, 11), 2); L.engrave(BODY['back'], (2, 11), 2)
    L.core(bx + bw // 2, by + 4 * S, 5)
    L.plate(ARM['top'], 'top', colour=L.metal * 1.05)
    for n in SIDES:
        L.plate(ARM[n], n, (0, 6), colour=L.metal * 1.05)        # great pauldron down to the elbow
        L.trimband(ARM[n], (0, 6), 6 * S - 3, 3)
        L.plate(ARM[n], n, (6, 8), colour=L.metal * 0.9)          # couter
        L.plate(ARM[n], n, (8, 12)); flutes(L, ARM[n], (8, 12), 5)
        spikes(L, ARM[n], (0, 2), True, 2, True)
    L.engrave(ARM['front'], (1, 6), 1); L.engrave(ARM['right'], (1, 6), 1)
    L.plate(ARM['bottom'], 'bottom')
    L.plate(LEG['bottom'], 'bottom')
    for n in SIDES:
        L.plate(LEG[n], n, (6, 12)); flutes(L, LEG[n], (6, 10), 5)
        L.trimband(LEG[n], (6, 12), 0, 3)
    L.engrave(LEG['front'], (6, 11), 1)


def layer2(elem, tier):
    L = Layer(elem, tier, 2)
    bx, by, bw, bh = L.rect(BODY['front'], (8, 9))
    if tier == 2:                                     # leather chausses, quilted, knee cop only
        cloth = mix(L.trim, L.leather, 0.55) * 0.8
        for n in SIDES:
            x0, y0, w, h = L.plate(LEG[n], n, (0, 9), colour=cloth, bevel=1)
            for y in range(4, h - 2, 6):
                for x in range(w): L.put(x0 + x, y0 + y, cloth * 0.7)
            L.strap(BODY[n], (8, 10), 0, BODY[n][2] * S)
        L.plate(LEG['front'], 'front', (4, 6), colour=L.metal)
        L.plate(LEG['top'], 'top', colour=cloth)
        L.engrave(LEG['front'], (0, 4), 1)
    elif tier == 3:                                   # tassets, cuisses, poleyn, greaves
        for n in SIDES:
            L.plate(BODY[n], n, (9, 12)); L.strap(BODY[n], (8, 9), 0, BODY[n][2] * S)
            L.plate(LEG[n], n, (0, 4)); L.mail(LEG[n], n, (4, 5))
            L.plate(LEG[n], n, (5, 7), colour=L.metal * 1.08); L.plate(LEG[n], n, (7, 9))
            L.trimband(LEG[n], (5, 7), 0, 2); L.wear(LEG[n], (0, 4), 3)
        L.plate(LEG['top'], 'top')
        lx, ly, lw, lh = L.rect(LEG['front'], (5, 7)); L.rivet(lx + lw // 2 - 1, ly + lh // 2 - 1)
        L.strap(LEG['back'], (0, 9), 4, 3)
        L.engrave(LEG['front'], (0, 4), 1); L.engrave(LEG['right'], (0, 4), 1)
    else:                                             # long fluted tassets, full cuisses, spiked poleyn
        for n in SIDES:
            L.plate(BODY[n], n, (8, 12)); flutes(L, BODY[n], (9, 12), 5)
            L.trimband(BODY[n], (8, 12), 0, 3)
            L.plate(LEG[n], n, (0, 9)); flutes(L, LEG[n], (0, 4), 5)
            L.plate(LEG[n], n, (4, 6), colour=L.metal * 1.1); L.trimband(LEG[n], (4, 6), 0, 3)
        L.plate(LEG['top'], 'top')
        lx, ly, lw, lh = L.rect(LEG['front'], (4, 6)); L.core(lx + lw // 2, ly + lh // 2, 3)
        L.engrave(LEG['front'], (0, 4), 1); L.engrave(LEG['right'], (6, 9), 1)
    return L.img


def save(img, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    Image.fromarray((np.clip(img, 0, 1) * 255).round().astype(np.uint8), 'RGBA').save(path)


def ids(): return ['gear_%s_t%d' % (e, t) for e in ELEMS for t in TIERS]


def write(root):
    for e in ELEMS:
        for t in TIERS:
            i = 'gear_%s_t%d' % (e, t)
            a = os.path.join(root, 'assets', 'knightsrealm')
            save(layer1(e, t), os.path.join(a, 'textures', 'entity', 'equipment', 'humanoid', i + '.png'))
            save(layer2(e, t), os.path.join(a, 'textures', 'entity', 'equipment', 'humanoid_leggings', i + '.png'))
            os.makedirs(os.path.join(a, 'equipment'), exist_ok=True)
            tex = {'texture': 'knightsrealm:' + i}
            with open(os.path.join(a, 'equipment', i + '.json'), 'w') as f:
                json.dump({'layers': {'humanoid': [tex], 'humanoid_leggings': [tex]}}, f, indent=2)


def view(e, t, side='front', scale=2):
    a, b = layer1(e, t), layer2(e, t)
    out = np.zeros((32 * S, 16 * S, 4)); out[..., :3] = 0.16; out[..., 3] = 1
    skin = C((0.55, 0.42, 0.33))
    def blit(src, f, dx, dy, mirror=False, under=None):
        u, v, w, h = (k * S for k in f)
        part = src[v:v + h, u:u + w]
        if mirror: part = part[:, ::-1]
        m = part[..., 3:4] > 0
        out[dy * S:dy * S + h, dx * S:dx * S + w] = np.where(m, part, out[dy * S:dy * S + h, dx * S:dx * S + w])
    for (f, dx, dy, mir) in ((HEAD[side], 4, 0, False), (BODY[side], 4, 8, False), (ARM[side], 0, 8, False),
                              (ARM[side], 12, 8, True), (LEG[side], 4, 20, False), (LEG[side], 8, 20, True)):
        u, v, w, h = f
        out[dy * S:(dy + h) * S, dx * S:(dx + w) * S, :3] = skin * 0.8
    blit(a, HEAD[side], 4, 0)
    blit(b, BODY[side], 4, 8); blit(a, BODY[side], 4, 8)
    blit(a, ARM[side], 0, 8); blit(a, ARM[side], 12, 8, True)
    for dx, m in ((4, False), (8, True)):
        blit(b, LEG[side], dx, 20, m); blit(a, LEG[side], dx, 20, m)
    return Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), 'RGBA').resize((16 * S * scale, 32 * S * scale), Image.NEAREST)


if __name__ == '__main__':
    from PIL import ImageDraw
    cw, ch = 16 * S * 2, 32 * S * 2
    sheet = Image.new('RGBA', (len(ELEMS) * (cw * 2 + 30) + 20, len(TIERS) * (ch + 40) + 20), (36, 36, 38, 255))
    d = ImageDraw.Draw(sheet)
    for i, e in enumerate(ELEMS):
        for j, t in enumerate(TIERS):
            x, y = 20 + i * (cw * 2 + 30), 20 + j * (ch + 40)
            sheet.paste(view(e, t, 'front'), (x, y)); sheet.paste(view(e, t, 'back'), (x + cw + 6, y))
            d.text((x, y + ch + 6), '%s t%d (front | back)' % (e, t), fill=(240, 240, 240, 255))
    sheet.save(sys.argv[1] if len(sys.argv) > 1 else '/mnt/user-data/outputs/equip-sheet2.png')


def install(pack):
    """Writes the worn layers, the 3D helms and the helmets' head-context item definitions into the pack.
    Returns the ids to list in icons.txt (equip_<asset>, helm3d_<asset>) so the plugin knows they exist."""
    import helm3d
    write(pack); helm3d.write(pack)
    ns = os.path.join(pack, 'assets', 'knightsrealm')
    for e in ELEMS:
        for t in TIERS:
            name = 'gear_helmet_%s_t%d' % (e, t)
            path = os.path.join(ns, 'items', name + '.json')
            with open(path, 'w', newline='\n') as f:
                json.dump({'model': {'type': 'minecraft:select', 'property': 'minecraft:display_context',
                                     'cases': [{'when': 'head', 'model': {'type': 'minecraft:model',
                                                'model': 'knightsrealm:item/helm3d/gear_%s_t%d' % (e, t)}}],
                                     'fallback': {'type': 'minecraft:model', 'model': 'knightsrealm:item/' + name}}}, f, indent=2)
    return ['equip_' + i for i in ids()] + ['helm3d_' + i for i in ids()]
