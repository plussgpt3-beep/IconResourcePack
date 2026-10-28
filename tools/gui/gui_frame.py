# Pixel-art frame for the KnightsRealm main menu (layout D), at game resolution (1 px = 1 GUI pixel).
import random, json, sys
SPEC = json.load(open(sys.argv[1], encoding='utf-8'))
ROWS = SPEC['rows']
BODY = ROWS * 18 + 14
from PIL import Image
R = random.Random(7)
W, H = 262, 48 + BODY
img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
px = img.load()

WOOD = [(70,41,22),(90,55,30),(110,68,38),(127,80,45),(147,95,55)]
LIGHT = [(140,92,52),(164,112,66),(186,132,82),(204,151,98),(222,174,122)]
DARK = [(30,19,12),(40,26,17),(50,33,22),(60,40,27),(72,49,33)]
RED = [(84,20,14),(116,30,21),(146,42,29),(170,60,41),(194,84,58)]
IRON = [(30,32,36),(58,62,68),(92,97,104),(138,144,150)]
OUT = (34,20,11,255)

def put(x, y, c):
    if 0 <= x < W and 0 <= y < H: px[x, y] = c + (255,) if len(c) == 3 else c

def wood(x0, y0, w, h, pal, orient='h', plank=6, bevel=True, knots=True, seed=0):
    r = random.Random(seed)
    along, across = (w, h) if orient == 'h' else (h, w)
    base = [r.choice([1, 2, 2, 3]) for _ in range(across // plank + 2)]
    lines = []
    for v in range(across):
        seq, cur = [], r.choice([-1, 0, 0, 0, 1])
        while len(seq) < along:
            run = r.randint(5, 22)
            seq += [cur] * run
            cur = r.choice([-1, 0, 0, 0, 1]) if cur == 0 else 0
        lines.append(seq[:along])
    kn = []
    if knots:
        for _ in range(max(1, along * across // 900)):
            kn.append((r.randrange(along), r.randrange(across), r.choice([2, 3])))
    for v in range(across):
        p, pv = v // plank, v % plank
        for u in range(along):
            lv = base[p] + lines[v][u]
            for ku, kv, kr in kn:
                d = ((u - ku) / (kr * 1.8)) ** 2 + ((v - kv) / kr) ** 2
                if d < 1: lv = 0 if d < 0.35 else 1
            if bevel and pv == 0: lv += 1
            if bevel and pv == plank - 1: lv -= 1
            if pv == plank - 1 and p < across // plank: lv = min(lv, 0)
            lv = max(0, min(4, lv))
            x, y = (x0 + u, y0 + v) if orient == 'h' else (x0 + v, y0 + u)
            put(x, y, pal[lv])

def frame(x0, y0, w, h, c=OUT):
    for x in range(x0, x0 + w): put(x, y0, c); put(x, y0 + h - 1, c)
    for y in range(y0, y0 + h): put(x0, y, c); put(x0 + w - 1, y, c)

def nail(x, y):
    put(x, y, IRON[2]); put(x + 1, y, IRON[1]); put(x, y + 1, IRON[1]); put(x + 1, y + 1, IRON[0])
    put(x, y, IRON[3])

def bracket(x, y, flipx=False, flipy=False):
    # an iron L-bracket 8x8 with two rivets
    for i in range(8):
        for t in range(2):
            a, b = (i, t), (t, i)
            for (dx, dy) in (a, b):
                X = x + (7 - dx if flipx else dx); Y = y + (7 - dy if flipy else dy)
                put(X, Y, IRON[2] if t == 0 else IRON[1])
    for (dx, dy) in ((5, 0), (0, 5)):
        X = x + (7 - dx if flipx else dx); Y = y + (7 - dy if flipy else dy)
        put(X, Y, IRON[3])
    put(x + (7 if flipx else 0), y + (7 if flipy else 0), IRON[3])

def cloth(x0, y0, w, h, seed=0):
    r = random.Random(seed)
    for y in range(h):
        for x in range(w):
            lv = 2 + (1 if (x + y // 2) % 4 == 0 else 0) - (1 if x == w - 1 else 0) + (1 if x == 0 else 0)
            if r.random() < 0.12: lv += r.choice([-1, 1])
            if y > h - 5:  # fringe
                if (x % 2 == 0 and y > h - 3) or (y == h - 1 and x % 2): continue
                lv -= 1
            put(x0 + x, y0 + y, RED[max(0, min(4, lv))])

# ---- geometry (game px) ----
GX, GY = 68, 38              # chest grid origin
LAYOUT = SPEC['layout']

# tabs (drawn first: the left post covers their right ends)
for r_, col in SPEC['tabs']:
    col = tuple(col)
    y0 = GY + 18 * r_ + 1
    wood(2, y0, 56, 16, WOOD, 'h', plank=8, seed=40 + r_, knots=False)
    for y in range(16):          # pointed left end
        cut = abs(7.5 - y) // 2
        for x in range(int(4 - cut)):
            px[2 + x, y0 + y] = (0, 0, 0, 0)
    for y in range(16):
        d = abs(7.5 - y) // 2
        put(2 + int(4 - d), y0 + y, OUT)
    for x in range(2, 58): put(x, y0, OUT); put(x, y0 + 15, OUT)
    for y in range(3, 13):       # category cloth strip
        for x in range(8, 11): put(x, y0 + y, tuple(max(0, c - (35 if x == 10 else 0)) for c in col))
    nail(50, y0 + 7)

# posts
for (x0, s) in ((52, 1), (237, 2)):
    wood(x0, 31, 9, BODY, WOOD, 'v', plank=9, seed=10 + s, bevel=False)
    for y in range(31, 31 + BODY): put(x0, y, OUT); put(x0 + 8, y, OUT)
    for y in range(31, 31 + BODY): put(x0 + 1, y, WOOD[3]); put(x0 + 7, y, WOOD[1])
    for y in range(40, 31 + BODY - 6, 50): nail(x0 + 3, y)

# panel
wood(61, 31, 176, BODY, DARK, 'v', plank=12, seed=3)
for x in range(61, 237): put(x, 31, OUT); put(x, 32, DARK[0]); put(x, 30 + BODY, DARK[3])

# ---- optional parchment map over some rows (coach station) ----
PINS = set(SPEC.get('pins', []))
if 'map' in SPEC:
    r0, r1 = SPEC['map']
    mx0, mx1 = 63, 235
    my0, my1 = GY + 18 * r0 - 3, GY + 18 * (r1 + 1) + 2
    rr = random.Random(11)
    G = 8
    grid = [[rr.random() for _ in range((mx1 - mx0) // G + 3)] for _ in range((my1 - my0) // G + 3)]
    def noise(x, y):
        gx, gy = x / G, y / G
        ix, iy = int(gx), int(gy); fx, fy = gx - ix, gy - iy
        fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
        a = grid[iy][ix] * (1 - fx) + grid[iy][ix + 1] * fx
        b = grid[iy + 1][ix] * (1 - fx) + grid[iy + 1][ix + 1] * fx
        return a * (1 - fy) + b * fy
    PAPER = [(196,170,118),(214,190,138),(226,204,154),(236,218,172)]
    SEA = [(112,138,140),(128,156,156),(144,172,168)]
    INK = (78,56,34)
    H_ = my1 - my0
    for y in range(my0, my1):
        for x in range(mx0, mx1):
            u, v = x - mx0, y - my0
            n = noise(u, v)
            coast = (v / H_) * 0.9 + n * 0.55
            edge = min(u, v, mx1 - 1 - x, my1 - 1 - y)
            if coast > 0.98:
                c = SEA[1 if (u + v) % 5 else 0]
                if coast < 1.03: c = SEA[2]
            else:
                lv = 2 if n > 0.35 else 1
                if rr.random() < 0.08: lv += rr.choice([-1, 1])
                c = PAPER[max(0, min(3, lv))]
                if 0.95 < coast <= 0.98: c = INK
            if edge < 2: c = tuple(int(k * 0.8) for k in c)
            put(x, y, c)
    # mountains (north) and forests
    for (cx, cy) in [(90, my0 + 10), (104, my0 + 7), (150, my0 + 9), (196, my0 + 12), (212, my0 + 8)]:
        for k in range(6):
            for dx in range(-k, k + 1):
                put(cx + dx, cy - 6 + k, (120,108,96) if dx < 0 else (150,138,124))
        put(cx, cy - 6, (236,232,226)); put(cx - 1, cy - 5, (236,232,226)); put(cx + 1, cy - 5, (236,232,226))
    fr = random.Random(5)
    for _ in range(46):
        fx_, fy_ = fr.randrange(mx0 + 6, mx1 - 6), fr.randrange(my0 + 18, my1 - 26)
        for (dx, dy, c) in ((0,0,(64,96,48)),(1,0,(80,116,58)),(0,-1,(80,116,58)),(1,-1,(96,132,70)),(0,1,(70,50,30))):
            put(fx_ + dx, fy_ + dy, c)
    # the road between the pins (dashed ink)
    pins = sorted(SPEC['pins'])
    if len(pins) >= 2:
        (ax, ay), (bx, by) = [(GX + (s % 9) * 18 + 9, GY + (s // 9) * 18 + 9) for s in pins[:2]]
        steps = int(max(abs(bx - ax), abs(by - ay)))
        for i in range(steps):
            if (i // 3) % 2: continue
            t_ = i / steps
            x = round(ax + (bx - ax) * t_); y = round(ay + (by - ay) * t_ + 4 * __import__('math').sin(t_ * 6.28))
            put(x, y, (110,62,30)); put(x, y + 1, (88,48,22))
    # frame of the map
    for x in range(mx0 - 1, mx1 + 1): put(x, my0 - 1, OUT); put(x, my1, OUT)
    for y in range(my0 - 1, my1 + 1): put(mx0 - 1, y, OUT); put(mx1, y, OUT)

# sockets where a button sits
for i, name in enumerate(LAYOUT):
    if not name: continue
    sx, sy = GX + (i % 9) * 18, GY + (i // 9) * 18

    if i in PINS:
        cx, cy = sx + 9, sy + 9
        for y in range(-9, 10):
            for x in range(-9, 10):
                d = (x * x + y * y) ** 0.5
                if d <= 9.2: put(cx + x, cy + y, (70,44,22) if d > 8 else ((176,128,64) if d > 6.8 else (232,206,150)))
        continue
    r = random.Random(100 + i)
    for y in range(18):
        for x in range(18):
            if x == 0 or y == 0: c = (16, 10, 6)
            elif x == 17 or y == 17: c = (92, 64, 42)
            elif x == 1 or y == 1: c = (24, 16, 10)
            else:
                c = (36, 25, 16) if r.random() > 0.15 else (42, 29, 19)
            put(sx + x, sy + y, c)

# header
for x in range(41, 221 + 36):          # roof: red shingles
    for y in range(0, 6):
        lv = 3 if y == 0 else (1 if y == 5 else 2)
        if (x + (y // 2) * 3) % 6 == 0 and 0 < y < 5: lv = 1
        put(x, y, RED[lv])
for x in range(41, 257): put(x, 6, OUT)
wood(44, 7, 210, 24, WOOD, 'h', plank=8, seed=21)
frame(44, 7, 210, 24)
bracket(45, 8); bracket(245, 8, flipx=True); bracket(45, 22, flipy=True); bracket(245, 22, flipx=True, flipy=True)
# plaque
wood(104, 9, 90, 20, LIGHT, 'h', plank=10, seed=31, knots=False)
frame(104, 9, 90, 20)
for x in range(105, 193): put(x, 10, LIGHT[4]); put(x, 27, LIGHT[0])
for (x, y) in ((106, 11), (190, 11), (106, 25), (190, 25)): nail(x, y)
# side boards on the header
for x0 in (64, 198):
    wood(x0, 14, 36, 10, WOOD, 'h', plank=10, seed=x0, knots=False)
    frame(x0, 14, 36, 10)

# cloth banner on the right post
cloth(241, 31, 7, 46, seed=5)

# bottom plank + foot
wood(44, 31 + BODY, 210, 10, WOOD, 'h', plank=10, seed=51)
frame(44, 31 + BODY, 210, 10)
nail(48, 35 + BODY); nail(248, 35 + BODY)
wood(60, 41 + BODY, 178, 6, DARK, 'h', plank=6, seed=52, knots=False)
for x in range(60, 238): put(x, 46 + BODY, OUT)


def shade(x0, y0, w, h, f):
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            if 0 <= x < W and 0 <= y < H:
                c = px[x, y]
                if c[3]: px[x, y] = (int(c[0] * f), int(c[1] * f), int(c[2] * f), c[3])

# cast shadows: header onto the panel, posts onto the panel edges, roof onto the header
for i, f in enumerate((0.55, 0.7, 0.82, 0.92)):
    shade(61, 33 + i, 176, 1, f)
    shade(61 + i, 33, 1, BODY - 2, f + 0.04)
    shade(236 - i, 33, 1, BODY - 2, f + 0.04)
for i, f in enumerate((0.6, 0.78, 0.9)):
    shade(45, 8 + i, 208, 1, f)
    shade(45, 32 + BODY + i, 208, 1, f + 0.05)

img.save(SPEC['out'])
print('ok', W, H)
