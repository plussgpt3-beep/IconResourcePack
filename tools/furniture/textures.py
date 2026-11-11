"""The furniture's own textures, painted in code (the user, 2026-11-11 22:18: the furniture's textures look plain, dress
them up). Sixteen by sixteen like the game's blocks, one set for each kingdom, written to
assets/knightsrealm/textures/block/furniture/<gf|sh>/<name>.png so they join the block atlas. Every material tiles;
the four in FIT are pictures stretched over one face (a banner's device, a keyboard, an open book, a door panel).
No file of the game is used: every pixel comes from the functions below."""
import math, os
from PIL import Image


def hx(c): c = c.lstrip('#'); return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
def P(*cs): return [hx(c) for c in cs]
def mix(a, b, t): return tuple(int(round(a[i] * (1 - t) + b[i] * t)) for i in range(3))
def rnd(*k):
    h = 2166136261
    for v in k: h = ((h ^ (int(v) & 0xffffffff)) * 16777619) & 0xffffffff
    h ^= h >> 13; h = (h * 0x5bd1e995) & 0xffffffff; h ^= h >> 15
    return h / 4294967296.0


GOLD = P('#8a5f12', '#c08a1e', '#e2b33c', '#f6dc7a'); IRON = P('#7d8288', '#9aa0a6', '#b6bbc0', '#d8dcdf'); DARK = P('#17181b', '#25272b', '#34373c', '#565b62')
KING = {
    'gf': dict(wood=P('#2f2014', '#42301e', '#56402a', '#6b5136', '#816444'), beam=P('#21160d', '#302013', '#412c1b', '#553b25', '#6a4b31'), cloth=P('#1a3780', '#24489f', '#2f5ab8', '#4a76d2'),
               cloth2=P('#7d1818', '#9a2222', '#b52e2e', '#d24a40'), stone=P('#5e6165', '#75787c', '#8b8e92', '#a3a6aa'), motif=hx('#e2b33c'), motif2=hx('#e2b33c')),
    'sh': dict(wood=P('#3d2a18', '#4f3822', '#62472c', '#765737', '#8a6843'), beam=P('#2a1c10', '#392717', '#4a3420', '#5c422a', '#6e5034'), cloth=P('#0f5f69', '#177883', '#20919c', '#3ab0ba'),
               cloth2=P('#b9bec3', '#d2d6da', '#e6e9eb', '#f8f9fa'), stone=P('#474d55', '#59606a', '#6c747e', '#838b95'), motif=hx('#f2f4f5'), motif2=hx('#20919c')),
}


def wood(p, seed=1):
    def f(x, y):
        b, r = y // 4, y % 4; j = (x - (b * 7 + 3)) % 16
        if r == 3: return p[0]                                             # the seam between two boards
        if j == 0: return p[0]                                             # where two boards butt
        if j in (2, 14) and r == 1: return p[0] if j == 2 else p[4]        # a nail and its glint
        g = rnd(seed, (x + b * 5) // 3, b, r)
        c = p[2] if g < 0.5 else p[1] if g < 0.8 else p[3]
        if r == 0 and rnd(seed, x // 2, b, 9) < 0.6: c = p[3] if c != p[3] else p[4]        # light on the upper edge
        if rnd(seed, x, y, 7) < 0.04: c = p[0]                             # a knot here and there
        return c
    return f

def beam(p, seed=2):
    def f(x, y):
        g = rnd(seed, x, (y + x * 3) // 6)
        c = p[2] if g < 0.45 else p[1] if g < 0.8 else p[3]
        if rnd(seed, x, y // 3, 4) < 0.07: c = p[0]                        # a check in the grain
        if y % 8 == 0 and rnd(seed, x // 2, y, 5) < 0.5: c = p[4]
        return c
    return f

def carved(p):
    def f(x, y):
        u, v = x % 8, y % 8; d = abs(u - 3.5) + abs(v - 3.5)
        if d < 1.2: return p[4]
        if d < 2.6: return p[3] if u + v < 7 else p[1]                     # a raised lozenge, lit from the upper left
        if d < 3.6: return p[0]
        if u in (0, 7) or v in (0, 7): return p[3] if (u == 0 or v == 0) else p[0]            # a bead round every field
        return p[2]
    return f

def cloth(p, motif=None, kind='plain', seed=3):
    def f(x, y):
        c = p[1] if (x + y) % 2 else p[2]
        if rnd(seed, x, y // 3) < 0.12: c = p[0]
        if rnd(seed, x // 3, y, 2) < 0.08: c = p[3]
        if motif is None: return c
        u, v = (x + (4 if (y // 8) % 2 else 0)) % 8, y % 8
        if kind == 'diamond':
            d = abs(u - 3) + abs(v - 3)
            if d == 0: return mix(motif, (255, 255, 255), 0.35)
            if d == 1: return motif
            if d == 2 and (u == 3 or v == 3): return mix(c, motif, 0.55)
        elif kind == 'lattice':
            if u == v or u + v == 6: return mix(c, motif, 0.75)
            if (u, v) in ((3, 0), (0, 3), (6, 3), (3, 6)): return motif
        elif kind == 'stripe':
            if y % 8 in (1, 2): return motif if (x + y) % 2 else mix(motif, (0, 0, 0), 0.15)
            if y % 8 == 5 and x % 2: return mix(c, motif, 0.6)
        return c
    return f

def trim():
    def f(x, y):
        r = y % 4
        if r == 0: return GOLD[1] if x % 4 else GOLD[0]
        if r == 1: return GOLD[3] if x % 4 in (1, 2) else GOLD[2]
        if r == 2: return GOLD[2] if x % 4 else GOLD[0]
        return GOLD[0] if x % 2 else hx('#5a1010')                          # the fringe
    return f

def metal(p, seed, rivet=8):
    def f(x, y):
        c = p[1] if rnd(seed, x, y // 5) < 0.5 else p[2]
        if rnd(seed, x, y, 3) < 0.07: c = p[3]
        if rnd(seed, x // 2, y // 2, 6) < 0.08: c = p[0]
        if x % rivet == 1 and y % rivet == 1: return p[3]
        if x % rivet == 2 and y % rivet == 2: return p[0]
        return c
    return f

def gold():
    def f(x, y):
        d = (x + y) % 6
        c = GOLD[3] if d == 0 else GOLD[1] if d == 3 else GOLD[2]
        if x % 4 == 2 and y % 4 == 2: c = GOLD[0]                           # chased dots
        return c
    return f

def ashlar(p, seed=5):
    def f(x, y):
        row = y // 8; u = (x + (4 if row % 2 else 0)) % 8; v = y % 8
        if v == 7 or u == 7: return p[0]                                   # the joint
        c = p[2] if rnd(seed, x, y) < 0.6 else p[1]
        if v == 0 or u == 0: c = p[3]                                      # a drafted margin, lit
        if v == 6 or u == 6: c = p[1]
        if rnd(seed, x // 2, y // 2, 8) < 0.06: c = p[0]
        return c
    return f

def cobble(p, seed=6):
    def f(x, y):
        cx, cy = (x + (2 if (y // 4) % 2 else 0)) // 4, y // 4; u, v = (x + (2 if (y // 4) % 2 else 0)) % 4, y % 4
        k = 1 + int(rnd(seed, cx, cy) * 2.99)
        if (u == 3 and rnd(seed, x, y, 1) < 0.85) or (v == 3 and rnd(seed, x, y, 2) < 0.85): return p[0]
        if u == 0 and v == 0: return p[min(3, k + 1)]
        return p[k]
    return f

def flat(p, seed, streak=3):
    def f(x, y):
        c = p[2]
        if x % streak == 0 and rnd(seed, x, y // 4) < 0.6: c = p[1]
        if rnd(seed, x, y, 2) < 0.06: c = p[3]
        if rnd(seed, x, y, 4) < 0.04: c = p[0]
        return c
    return f

def flame():
    def f(x, y):
        t = y / 15.0; c = mix(hx('#fff8c8'), hx('#ffb030'), t)
        if rnd(11, x, y) < 0.18: c = mix(c, hx('#ff7a1a'), 0.6)
        if rnd(12, x, y) < 0.1: c = hx('#fffbe6')
        return c
    return f

def staves(p):
    def f(x, y):
        if y % 16 in (2, 3, 12, 13): return DARK[3] if x % 8 == 1 else DARK[2] if y % 16 in (2, 12) else DARK[1]       # the hoops, a rivet on each
        if x % 4 == 3: return p[0]
        g = rnd(21, x, y // 5)
        return p[2] if g < 0.5 else p[1] if g < 0.8 else p[3]
    return f

def head(p):
    def f(x, y):
        d = max(abs(x - 7.5), abs(y - 7.5))
        if d > 6.9: return DARK[2] if (x + y) % 5 else DARK[3]
        if d > 5.9: return p[0]
        if y % 4 == 1: return p[0]
        if (x, y) in ((7, 7), (8, 7), (7, 8), (8, 8)): return DARK[1]                         # the bung
        return p[2] if rnd(22, x // 3, y) < 0.6 else p[3]
    return f

def books(p):
    SP = (hx('#8c2a22'), hx('#27583a'), hx('#2a4a86'), hx('#b08a3c'), hx('#5a2d6e'), hx('#7a4a25'), hx('#1e6a70')); W = (2, 3, 2, 2, 3, 2, 2)
    def f(x, y):
        sh, v = y // 8, y % 8
        if v == 7: return p[1]                                             # the shelf
        if v == 0: return p[0]
        i = 0; a = 0
        while a + W[i % 7] <= x: a += W[i % 7]; i += 1
        c = SP[(i * 3 + sh * 2) % 7]
        if x == a: c = mix(c, (0, 0, 0), 0.35)
        if v in (2, 5): c = GOLD[2] if x != a else GOLD[0]
        if v == 1 and (i + sh) % 4 == 0: return p[0]                       # a shorter book
        return c
    return f

def pot():
    p = P('#7f3f22', '#a0522c', '#bb6638', '#d5814f'); cream, blue = hx('#ead9b0'), hx('#2f5ab8')
    def f(x, y):
        v = y % 16
        if v in (5, 9): return cream
        if 6 <= v <= 8: return blue if (x + (v - 6)) % 4 in (0, 1) else cream
        c = p[2] if rnd(31, x, y // 2) < 0.6 else p[1]
        if rnd(32, x, y) < 0.06: c = p[3]
        return c
    return f

def hay():
    p = P('#7d5f17', '#a88222', '#c9a030', '#e3c04e')
    def f(x, y):
        if y % 8 == 4: return hx('#6a4a26') if x % 3 else hx('#8a6234')    # the twine
        k = int(rnd(41, x, (y + x) // 3) * 3.99)
        return p[k]
    return f

def parchment():
    p = P('#c4ac76', '#d9c38e', '#e9d8a8', '#f4e9c4'); ink = hx('#4a3826')
    def f(x, y):
        c = p[2] if rnd(51, x // 2, y // 2) < 0.7 else p[1]
        if rnd(52, x, y) < 0.05: c = p[3]
        if y % 3 == 1 and 2 <= x % 16 <= 9 + int(rnd(53, y) * 5) and rnd(54, x, y) < 0.82: c = mix(c, ink, 0.75)
        return c
    return f

def noise(cols, seed):
    def f(x, y): return cols[int(rnd(seed, x, y) * (len(cols) - 0.01))]
    return f

def water():
    p = P('#1c489c', '#2a60bd', '#4682d8', '#9cc2f2')
    def f(x, y):
        c = p[1]
        if (x + 2 * y) % 7 == 0: c = p[2]
        if (x * 3 + y) % 11 == 0: c = p[0]
        if rnd(61, x, y) < 0.04: c = p[3]
        return c
    return f

def marble():
    p = P('#a9acaf', '#c9cccf', '#e0e3e5', '#f4f5f6')
    def f(x, y):
        c = p[2] if rnd(71, x // 2, y // 2) < 0.7 else p[3]
        if (x * 3 + y * 5 + int(2 * math.sin(y / 2.0))) % 17 == 0: c = p[0]
        elif (x * 3 + y * 5 + int(2 * math.sin(y / 2.0))) % 17 == 1: c = p[1]
        return c
    return f

def fruit(wd):
    red = P('#6e0e0e', '#a81a1a', '#d02c2c', '#f07060'); grn = P('#3a5a12', '#56801c', '#78a82a', '#a8d060')
    def f(x, y):
        cx, cy = x // 8, y // 8; u, v = x % 8, y % 8; d = math.hypot(u - 3.5, v - 4.0); p = grn if (cx + cy * 3) % 4 == 3 else red
        if (u, v) == (3, 0): return hx('#4a3018')
        if (u, v) == (4, 0): return grn[2]
        if d < 1.2 and u < 4 and v < 4: return p[3]
        if d < 2.3: return p[2] if u + v < 8 else p[1]
        if d < 3.2: return p[1] if u + v < 8 else p[0]
        return wd[0]
    return f

# ---- pictures stretched over one face
def emblem(k, kingdom):
    p = k['cloth']; g = GOLD
    def f(x, y):
        if x in (0, 15) or y in (0, 15): return g[2] if (x + y) % 2 else g[1]
        if x in (1, 14) or y in (1, 14): return p[0]
        c = p[1] if (x + y) % 2 else p[2]
        dx, dy = x - 7.5, y - 7.5; d = math.hypot(dx, dy)
        if kingdom == 'gf':                                               # the gear of GearFord
            a = math.degrees(math.atan2(dy, dx)) % 45
            if d < 1.3: return c
            if d < 2.2: return g[3]
            if 2.9 <= d <= 4.3: return g[2] if dx + dy < 0 else g[1]
            if 4.3 < d <= 5.9 and (a < 9 or a > 36): return g[2] if dx + dy < 0 else g[1]
        else:                                                              # the bolt of Stormhold over the sea
            bolt = {(9, 2), (10, 2), (8, 3), (9, 3), (7, 4), (8, 4), (6, 5), (7, 5), (6, 6), (7, 6), (8, 6), (9, 6), (8, 7), (9, 7), (7, 8), (8, 8), (6, 9), (7, 9), (5, 10), (6, 10), (5, 11)}
            if (x, y) in bolt: return hx('#fff6c0') if (x + y) % 3 else g[3]
            if any((x + a, y + b) in bolt for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))): return g[1]
            if y in (12, 13) and (x + (y - 12) * 2) % 4 < 2 and 2 < x < 13: return hx('#f2f4f5')
        return c
    return f

def keys():
    def f(x, y):
        if y >= 14: return hx('#2a1c11')
        if y < 9 and x % 2 == 1 and (x // 2) % 7 in (0, 1, 3, 4, 5): return hx('#141416')
        if x % 2 == 1 and y >= 9: return hx('#bdb49f')
        return hx('#f4efe0') if y < 12 else hx('#dcd4bf')
    return f

def page():
    p = P('#cdb682', '#e4d29e', '#f1e4ba', '#faf2d4'); ink = hx('#3f3020')
    def f(x, y):
        if x in (7, 8): return p[0]
        if x in (0, 15) or y in (0, 15): return p[1]
        c = p[2] if x < 7 else p[3] if (x + y) % 5 else p[2]
        if (x, y) in ((2, 2), (3, 2), (2, 3), (3, 3), (2, 4)): return hx('#a81a1a')              # the initial
        if y in (3, 5, 7, 9, 11, 13) and (2 <= x <= 5 or 10 <= x <= 13) and not (y == 3 and x < 5) and rnd(81, x, y) < 0.85: return ink
        return c
    return f

def panel(k):
    w, b = k['wood'], k['beam']
    def f(x, y):
        e = min(x, 15 - x, y, 15 - y)
        if e < 2: return b[1] if (x + y) % 3 else b[2]                    # the frame
        if e == 2: return b[0] if (x < 8) == (y < 8) or True else w[4]
        if y in (4, 11) and x < 7: return DARK[2] if x != 5 else DARK[3]  # two hinge straps
        if (x, y) in ((12, 7), (12, 8), (13, 7), (13, 8)): return GOLD[2]  # the ring
        d = abs(x - 8) + abs(y - 7.5)
        if d < 1.6: return w[4]
        if d < 3.2: return w[3] if x + y < 16 else w[1]
        if d < 4.2: return w[0]
        return w[2] if rnd(91, x // 2, y) < 0.6 else w[1]
    return f


NAMES = dict(w='wood', l='beam', C='carved', c='cloth', r='cloth2', T='trim', m='iron', d='dark_iron', g='gold', s='stone', x='wax', f='flame', k='barrel_side', t='barrel_top', b='books', p='pot', h='hay',
             q='parchment', e='ember', n='coal', y='cloth_yellow', o='burlap', v='cloth_green', u='cloth_purple', W='linen', z='water', i='marble', a='fruit', E='emblem', K='keys', G='page', D='panel')
FIT = set('EKGD')


def paint(kingdom):
    k = KING[kingdom]; out = {}
    F = dict(w=wood(k['wood']), l=beam(k['beam']), C=carved(k['beam']), c=cloth(k['cloth'], k['motif'], 'diamond'), r=cloth(k['cloth2'], k['motif2'], 'lattice' if kingdom == 'gf' else 'stripe'), T=trim(),
             m=metal(IRON, 13), d=metal(DARK, 14), g=gold(), s=ashlar(k['stone']) if kingdom == 'gf' else cobble(k['stone']), x=flat(P('#cfc4a3', '#e2d8b8', '#f1ead2', '#fffaf0'), 15), f=flame(),
             k=staves(k['wood']), t=head(k['wood']), b=books(k['beam']), p=pot(), h=hay(), q=parchment(), e=noise(P('#4a1006', '#a02a0a', '#f06a14', '#ffc850'), 16), n=noise(P('#0f0f11', '#19191c', '#19191c', '#2c2c33'), 17),
             y=cloth(P('#a8811a', '#c9a024', '#e0b730', '#f2d460')), o=cloth(P('#5a3d22', '#74502e', '#8c633a', '#a67a4c'), seed=4), v=cloth(P('#2a5a1c', '#3a7426', '#4c8f32', '#6aae48')), u=cloth(P('#47205f', '#5d2c7c', '#74399a', '#9558bd')),
             W=flat(P('#c4c8cc', '#dadde0', '#eceef0', '#ffffff'), 18, 5), z=water(), i=marble(), a=fruit(k['wood']), E=emblem(k, kingdom), K=keys(), G=page(), D=panel(k))
    for letter, fn in F.items():
        im = Image.new('RGBA', (16, 16))
        for x in range(16):
            for y in range(16): im.putpixel((x, y), tuple(fn(x, y)) + (255,))
        out[letter] = im
    return out


def write(pack):
    n = 0
    for kingdom in ('gf', 'sh'):
        d = os.path.join(pack, 'assets', 'knightsrealm', 'textures', 'block', 'furniture', kingdom); os.makedirs(d, exist_ok=True)
        for letter, im in paint(kingdom).items(): im.save(os.path.join(d, NAMES[letter] + '.png'), optimize=True); n += 1
    return n


if __name__ == '__main__':
    import sys
    sheet = Image.new('RGBA', (len(NAMES) * 34 + 2, 2 * 34 + 2), (40, 40, 44, 255))
    for r, kingdom in enumerate(('gf', 'sh')):
        for c, (letter, im) in enumerate(paint(kingdom).items()): sheet.paste(im.resize((32, 32), Image.NEAREST), (2 + c * 34, 2 + r * 34))
    sheet = sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST); sheet.save(sys.argv[1] if len(sys.argv) > 1 else 'textures.png'); print(sheet.size)
