# Themed pixel-art frames for KnightsRealm chest menus (1 px = 1 GUI pixel; show at x3 with nearest-neighbour).
# python3 gui_frame2.py spec.json  ->  writes spec["out"].
# spec: rows, layout (9 per row, icon name or null), tabs [[row,[r,g,b]]], theme, optional map [r0,r1] + pins [slots].
# Geometry (shared by every theme, so the page overlay never moves):
#   roof zone y 0..16, header y 17..41 (plaque x104..194 y19..39), body y 41..41+BODY,
#   chest grid origin (68, 48), slot pitch 18, tabs x2..58 at y 49+18*row.
import json, math, random, sys
from PIL import Image

SPEC = json.load(open(sys.argv[1], encoding='utf-8'))
THEME = SPEC.get('theme', 'oak')
ROWS = SPEC['rows']
BODY = ROWS * 18 + 14
E = 10                       # extra roof height above the old layout
W, H = 262, 58 + BODY
GX, GY = 68, 38 + E
HY = 7 + E                   # header top
BY = 31 + E                  # body top
img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
px = img.load()

# ---------- palettes (dark -> light) ----------
OAK = [(70,41,22),(90,55,30),(110,68,38),(127,80,45),(147,95,55)]
DARKOAK = [(38,24,15),(52,34,21),(66,44,28),(80,54,35),(96,66,43)]
LIGHT = [(140,92,52),(164,112,66),(186,132,82),(204,151,98),(222,174,122)]
BIRCH = [(146,124,92),(172,150,112),(194,174,134),(212,194,154),(228,212,174)]
SPRUCE = [(58,40,26),(76,53,34),(94,66,42),(112,80,52),(130,95,62)]
PANEL = [(30,19,12),(40,26,17),(50,33,22),(60,40,27),(72,49,33)]
STONE = [(58,58,62),(78,78,82),(98,98,102),(120,120,124),(144,144,148)]
DSTONE = [(30,30,34),(40,40,45),(50,50,56),(60,60,66),(72,72,78)]
MARBLE = [(160,156,150),(184,180,174),(204,200,194),(222,218,212),(238,236,232)]
WALNUT = [(34,22,16),(46,30,21),(58,39,27),(70,48,33),(84,58,40)]
RED = [(84,20,14),(116,30,21),(146,42,29),(170,60,41),(194,84,58)]
SLATE = [(34,38,46),(46,52,62),(60,66,78),(74,82,96),(92,100,116)]
STRAW = [(120,92,40),(150,118,54),(178,144,70),(204,170,92),(226,196,120)]
CANVAS = [(138,128,100),(164,154,124),(188,178,148),(206,198,170),(224,218,194)]
IRON = [(30,32,36),(58,62,68),(92,97,104),(138,144,150)]
GOLD = [(104,72,16),(146,104,24),(194,148,38),(226,186,70),(250,224,134)]
FELT = [(16,42,28),(22,54,36),(28,66,44),(36,80,54),(46,94,64)]
PARCH = [(178,152,102),(198,174,122),(214,192,142),(226,206,158),(236,220,176)]
OUT = (34, 20, 11, 255)
PLASTER = [(170,162,146),(196,188,172),(216,210,196),(230,226,214),(242,240,232)]
TILE = [(104,40,22),(140,58,32),(170,78,44),(196,102,62),(218,130,88)]
BRICK = [(70,30,22),(100,44,30),(128,58,40),(150,74,52),(172,94,68)]
DBRICK = [(30,16,12),(44,24,18),(58,32,24),(72,40,30),(86,50,38)]
SOOT = [(22,18,16),(32,26,22),(42,34,28),(54,44,36),(66,54,44)]
SAND = [(170,140,90),(192,162,110),(210,182,128),(224,198,146),(236,214,166)]
BLUE = [(20,40,90),(30,56,120),(40,72,150),(56,92,176),(78,116,200)]
BARN = [(70,24,18),(100,34,24),(126,46,32),(150,62,44),(172,82,60)]
IRON5 = [(30,32,36),(46,50,56),(62,66,72),(80,86,94),(104,110,118)]
TAPESTRY = [(60,16,16),(84,22,22),(104,30,28),(124,40,36),(146,54,48)]
LSTONE = [(96,92,86),(120,116,108),(142,138,130),(162,158,150),(184,180,172)]
WATER = [(30,60,90),(40,80,116),(54,100,140),(74,124,164),(110,160,196)]
VELVET = [(36,12,44),(50,18,60),(64,26,76),(80,36,94),(98,50,114)]

def put(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        px[x, y] = c + (255,) if len(c) == 3 else c

def get(x, y):
    return px[x, y] if 0 <= x < W and 0 <= y < H else (0, 0, 0, 0)

def wood(x0, y0, w, h, pal, orient='h', plank=6, bevel=True, knots=True, seed=0):
    r = random.Random(seed)
    along, across = (w, h) if orient == 'h' else (h, w)
    base = [r.choice([1, 2, 2, 3]) for _ in range(across // plank + 2)]
    lines = []
    for v in range(across):
        seq, cur = [], r.choice([-1, 0, 0, 0, 1])
        while len(seq) < along:
            seq += [cur] * r.randint(5, 22)
            cur = r.choice([-1, 0, 0, 0, 1]) if cur == 0 else 0
        lines.append(seq[:along])
    kn = [(r.randrange(along), r.randrange(across), r.choice([2, 3])) for _ in range(max(1, along * across // 900))] if knots else []
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
            x, y = (x0 + u, y0 + v) if orient == 'h' else (x0 + v, y0 + u)
            put(x, y, pal[max(0, min(4, lv))])

def stones(x0, y0, w, h, pal, bw=12, bh=6, seed=0):
    r = random.Random(seed)
    for y in range(h):
        row = y // bh
        off = (bw // 2) * (row % 2)
        shade_row = [r.choice([1, 2, 2, 3]) for _ in range(w // bw + 3)]
        for x in range(w):
            col = (x + off) // bw
            in_mortar = (y % bh == bh - 1) or ((x + off) % bw == bw - 1)
            if in_mortar:
                c = pal[0]
            else:
                lv = shade_row[col % len(shade_row)]
                if y % bh == 0 or (x + off) % bw == 0: lv += 1
                if r.random() < 0.12: lv += r.choice([-1, 1])
                c = pal[max(0, min(4, lv))]
            put(x0 + x, y0 + y, c)

def noise_fill(x0, y0, w, h, pal, base=2, seed=0, p=0.22):
    r = random.Random(seed)
    for y in range(h):
        for x in range(w):
            lv = base + (r.choice([-1, 1]) if r.random() < p else 0)
            put(x0 + x, y0 + y, pal[max(0, min(4, lv))])

def marble(x0, y0, w, h, seed=0):
    noise_fill(x0, y0, w, h, MARBLE, 3, seed, 0.15)
    r = random.Random(seed + 1)
    for _ in range(max(2, w * h // 500)):
        x, y = r.randrange(x0, x0 + w), r.randrange(y0, y0 + h)
        for _ in range(r.randint(8, 20)):
            put(x, y, MARBLE[1])
            x += r.choice([1, 1, 0]); y += r.choice([-1, 0, 1])
            if not (x0 <= x < x0 + w and y0 <= y < y0 + h): break

def frame(x0, y0, w, h, c=OUT):
    for x in range(x0, x0 + w): put(x, y0, c); put(x, y0 + h - 1, c)
    for y in range(y0, y0 + h): put(x0, y, c); put(x0 + w - 1, y, c)

def nail(x, y, pal=IRON):
    put(x, y, pal[3]); put(x + 1, y, pal[1]); put(x, y + 1, pal[1]); put(x + 1, y + 1, pal[0])

def bracket(x, y, flipx=False, flipy=False, pal=IRON):
    for i in range(8):
        for t in range(2):
            for (dx, dy) in ((i, t), (t, i)):
                put(x + (7 - dx if flipx else dx), y + (7 - dy if flipy else dy), pal[2] if t == 0 else pal[1])
    for (dx, dy) in ((5, 0), (0, 5), (0, 0)):
        put(x + (7 - dx if flipx else dx), y + (7 - dy if flipy else dy), pal[3])

def band(x0, x1, y, pal=IRON, h=3):
    for x in range(x0, x1):
        for k in range(h):
            put(x, y + k, pal[3] if k == 0 else pal[2] if k < h - 1 else pal[0])
    for x in range(x0 + 4, x1 - 2, 14): put(x, y + 1, pal[3]); put(x, y + 2, pal[1])

def shade(x0, y0, w, h, f):
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            c = get(x, y)
            if c[3]: px[x, y] = (int(c[0] * f), int(c[1] * f), int(c[2] * f), c[3])

def cloth(x0, y0, w, h, pal, seed=0):
    r = random.Random(seed)
    for y in range(h):
        for x in range(w):
            lv = 2 + (1 if (x + y // 2) % 4 == 0 else 0) - (1 if x == w - 1 else 0) + (1 if x == 0 else 0)
            if r.random() < 0.12: lv += r.choice([-1, 1])
            if y > h - 5:
                if (x % 2 == 0 and y > h - 3) or (y == h - 1 and x % 2): continue
                lv -= 1
            put(x0 + x, y0 + y, pal[max(0, min(4, lv))])

# ---------- decorations ----------

def rope_line(x0, x1, y):
    for x in range(x0, x1):
        put(x, y, (176, 146, 96) if (x // 2) % 2 else (130, 104, 64)); put(x, y + 1, (130, 104, 64) if (x // 2) % 2 else (176, 146, 96))

def anchor(x, y):
    for dy in range(14): put(x + 6, y + dy, IRON[2]); put(x + 7, y + dy, IRON[1])
    for dx in range(3, 11): put(x + dx, y + 3, IRON[2])
    for a in range(0, 181, 15):
        t_ = math.radians(a)
        put(int(round(x + 6.5 + 6 * math.cos(t_))), int(round(y + 9 + 5 * math.sin(t_))), IRON[2])
    for (dx, dy) in ((0, 9), (13, 9), (1, 8), (12, 8)): put(x + dx, y + dy, IRON[3])
    for a in range(0, 360, 30):
        t_ = math.radians(a); put(int(round(x + 6.5 + 2 * math.cos(t_))), int(round(y + 1 + 1.5 * math.sin(t_))), IRON[2])

def ship_wheel(cx, cy, r=7):
    for a in range(0, 360, 4):
        t_ = math.radians(a)
        put(int(round(cx + r * math.cos(t_))), int(round(cy + r * math.sin(t_))), OAK[2])
        put(int(round(cx + (r - 1) * math.cos(t_))), int(round(cy + (r - 1) * math.sin(t_))), OAK[3])
    for k in range(8):
        t_ = math.radians(k * 45)
        for s in range(0, r + 3):
            put(int(round(cx + s * math.cos(t_))), int(round(cy + s * math.sin(t_))), OAK[1] if s <= r else OAK[3])
    for dy in range(-1, 2):
        for dx in range(-1, 2): put(cx + dx, cy + dy, GOLD[2])

def tapestry(x0, y0, w, h):
    noise_fill(x0, y0, w, h, TAPESTRY, 2, 4, 0.12)
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            u, v = (x - x0) % 12, (y - y0) % 12
            if abs(u - 6) + abs(v - 6) == 5: put(x, y, GOLD[1])
            elif u == 6 and v == 6: put(x, y, GOLD[2])

def iron_plates(x0, y0, w, h, seed=0, pw=30):
    noise_fill(x0, y0, w, h, IRON5, 2, seed, 0.15)
    for x in range(x0, x0 + w, pw):
        for y in range(y0, y0 + h): put(x, y, IRON5[0]); put(x + 1, y, IRON5[3])
        for y in range(y0 + 2, y0 + h - 1, 6): put(x + 3, y, IRON5[4]); put(x + 4, y + 1, IRON5[0])

def spikes(x0, x1, ybase, h=6):
    for x in range(x0, x1):
        k = (x - x0) % 6
        top = ybase - (h - abs(k - 3) * 2)
        for y in range(top, ybase + 1): put(x, y, IRON5[3] if k < 3 else IRON5[1])

def hay(x, y, w=16, h=8):
    r = random.Random(x)
    for dy in range(h):
        for dx in range(w):
            put(x + dx, y + dy, STRAW[r.choice([1, 2, 2, 3])] if dy not in (2, h - 3) else (110, 80, 40))

def poster(x, y, seed):
    note(x, y, 12, 14, seed)
    for dx in range(1, 11): put(x + dx, y + 2, (150, 30, 30)); put(x + dx, y + 3, (150, 30, 30))
    for dy in range(5, 10):
        for dx in range(4, 8): put(x + dx, y + dy, (90, 70, 50) if dy > 6 or dx in (5, 6) else PARCH[3])

def shackle(x, y):
    for a in range(0, 360, 20):
        t_ = math.radians(a)
        put(int(round(x + 3 * math.cos(t_))), int(round(y + 3 * math.sin(t_))), IRON[2])
    for k in range(1, 8): put(x, y - 3 - k, IRON[1] if k % 2 else IRON[3])

def torch(x, y):
    for dy in range(4, 12): put(x + 1, y + dy, OAK[1]); put(x + 2, y + dy, OAK[2])
    for (dx, dy, c) in ((1, 3, (250, 220, 120)), (2, 3, (250, 200, 80)), (1, 2, (240, 150, 40)), (2, 1, (230, 110, 30)), (1, 0, (210, 80, 20)), (0, 3, (240, 150, 40)), (3, 3, (240, 150, 40))):
        put(x + dx, y + dy, c)

def anvil(x, y):
    rows = [(0, 14), (1, 14), (2, 13), (4, 9), (5, 9), (6, 9), (7, 11), (8, 13)]
    for dy, w in rows:
        for dx in range(w): put(x + dx + (14 - w) // 2 + (2 if dy < 3 and dx < 3 else 0), y + dy, IRON[2] if dy < 2 else IRON[1])
    for dx in range(3): put(x - 2 + dx, y + 1, IRON[2])   # horn
    put(x + 4, y, IRON[3]); put(x + 8, y, IRON[3])

def hammer_tongs(x, y):
    for i in range(12): put(x + i, y + i, OAK[2]); put(x + 11 - i, y + i, IRON[1])
    for dx in range(-2, 3):
        for dy in range(2): put(x + dx + 1, y + dy, IRON[2])
    put(x + 11, y, IRON[2]); put(x + 12, y + 1, IRON[2])

def smoke(x, y):
    r = random.Random(x)
    for k in range(5):
        cx, cy = x + r.randint(-2, 3) + k, y - k * 2
        for dx in range(-1, 2):
            for dy in range(-1, 1): put(cx + dx, cy + dy, (120 + k * 10, 120 + k * 10, 124 + k * 10, 180 - k * 25))

def lance(x, y, flip=False):
    for i in range(20):
        put(x + (i if not flip else -i), y + i // 2, OAK[3]); put(x + (i if not flip else -i), y + i // 2 + 1, OAK[1])
    for k in range(3): put(x + (k if not flip else -k), y - 1, IRON[3])

def pennant(x, y, c):
    for dy in range(6): put(x, y + dy, OAK[1])
    for dx in range(1, 7):
        for dy in range(0, 4 - dx // 2): put(x + dx, y + dy, c)

def bell(x, y):
    for dy in range(3): put(x + 4, y + dy, IRON[1])
    rows = [3, 5, 7, 7, 9, 9]
    for dy, w in enumerate(rows):
        for dx in range(w): put(x + 4 - w // 2 + dx, y + 3 + dy, GOLD[3] if dx < w // 2 else GOLD[1])
    put(x + 4, y + 9, IRON[2])

def note(x, y, w, h, seed):
    r = random.Random(seed)
    for dy in range(h):
        for dx in range(w):
            put(x + dx, y + dy, PARCH[3] if r.random() > 0.2 else PARCH[2])
    for dy in range(2, h - 1, 2):
        for dx in range(2, w - 2):
            if r.random() < 0.7: put(x + dx, y + dy, (120, 96, 60))
    put(x + w // 2, y, (180, 40, 40)); put(x + w // 2, y + 1, (120, 26, 26))

def plaster_timber(x0, y0, w, h, seed=0):
    noise_fill(x0, y0, w, h, PLASTER, 3, seed, 0.18)
    for x in range(x0, x0 + w, 30):                 # half-timber posts and braces
        for y in range(y0, y0 + h):
            for k in range(3): put(x + k, y, DARKOAK[2 + (k == 0)])
        for i in range(min(h, 26)):
            for k in range(2):
                put(x + 3 + i + k, y0 + i, DARKOAK[2]) if x + 3 + i + k < x0 + w and x + 3 + i < x + 30 else None

def jar(x, y, liquid):
    for dy in range(9):
        for dx in range(6):
            edge = dx in (0, 5) or dy == 8
            if dy < 2 and dx in (0, 5): continue
            c = (180, 200, 210) if edge else (liquid if dy > 3 else (200, 220, 228))
            put(x + dx, y + dy, c)
    for dx in range(1, 5): put(x + dx, y - 1, OAK[2])   # cork
    put(x + 1, y + 4, (240, 248, 250))

def herbs(x, y, leaf):
    for dy in range(3): put(x + 2, y + dy, (150, 120, 70))
    for dy in range(3, 11):
        for dx in range(5):
            if (dx + dy) % 2 == 0 or dx == 2: put(x + dx - (dy > 7) + (dy > 9), y + dy, leaf[(dx + dy) % len(leaf)])

def crown(cx, y):
    for dx in range(-8, 9):
        for dy in range(4): put(cx + dx, y + 6 + dy, GOLD[3] if dy < 2 else GOLD[1])
    for px_ in (-8, -4, 0, 4, 8):
        h = 6 if px_ in (-8, 8) else 4 if px_ in (-4, 4) else 8
        for dy in range(h): put(cx + px_, y + 6 - dy, GOLD[2]); put(cx + px_ + (1 if px_ < 8 else -1), y + 6 - dy, GOLD[3])
        put(cx + px_, y + 6 - h, GOLD[4])
    for (dx, c) in ((-4, (180, 30, 40)), (0, (40, 70, 180)), (4, (180, 30, 40))): put(cx + dx, y + 8, c)

def scale(x, y):
    for dy in range(10): put(x + 8, y + dy, IRON[2])
    for dx in range(17): put(x + dx, y + 1, IRON[3] if dx == 8 else IRON[2])
    for side in (0, 16):
        for dy in range(2, 6): put(x + side, y + dy, IRON[1])
        for dx in range(-3, 4): put(x + side + dx, y + 6, GOLD[2]); put(x + side + dx, y + 7, GOLD[1]) if abs(dx) < 3 else None
    for dx in range(5, 12): put(x + dx, y + 10, IRON[1])

def basket(x, y, fruit):
    for dy in range(6):
        for dx in range(14):
            put(x + dx, y + 4 + dy, OAK[3] if (dx + dy) % 2 else OAK[1])
    r = random.Random(x)
    for k in range(9):
        fx, fy = x + 1 + r.randrange(12), y + r.randrange(5)
        for (dx, dy) in ((0, 0), (1, 0), (0, 1), (1, 1)): put(fx + dx, fy + dy, fruit[(dx + dy) % len(fruit)])
def coin_stack(x, y, n):
    for i in range(n):
        yy = y - i * 2
        for dx in range(7):
            put(x + dx, yy, GOLD[3] if 1 <= dx <= 5 else GOLD[1]); put(x + dx, yy + 1, GOLD[1])
        put(x + 2, yy, GOLD[4])

def padlock(x, y):
    for dx in range(1, 6):
        put(x + dx, y, IRON[2])
    for dy in range(1, 4): put(x + 1, y + dy, IRON[2]); put(x + 5, y + dy, IRON[2])
    for dy in range(4, 10):
        for dx in range(7): put(x + dx, y + dy, GOLD[2] if dx not in (0, 6) else GOLD[1])
    put(x + 3, y + 6, (30, 20, 10)); put(x + 3, y + 7, (30, 20, 10)); put(x + 1, y + 4, GOLD[4])

def wax_seal(x, y, pal=RED):
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            d = dx * dx + dy * dy
            if d <= 10: put(x + dx, y + dy, pal[1] if d > 6 else pal[3] if (dx + dy) < 0 else pal[2])
    put(x, y, pal[4]); put(x - 1, y, pal[1]); put(x + 1, y, pal[1])
    put(x - 1, y + 4, pal[1]); put(x + 1, y + 5, pal[1])   # ribbon tails

def quill(x, y):
    for i in range(14):
        put(x + i, y - i // 2, (232, 228, 214) if i > 4 else (60, 50, 40))
        if i > 5: put(x + i, y - i // 2 - 1, (208, 204, 190)); put(x + i - 1, y - i // 2 + 1, (196, 190, 176))
    put(x - 1, y + 1, (20, 20, 30))

def scroll_end(x, y, h):
    for dy in range(h):
        for dx in range(6):
            put(x + dx, y + dy, PARCH[1] if dx in (0, 5) else PARCH[3] if dx == 2 else PARCH[2])
    for dx in range(6): put(x + dx, y - 1, PARCH[0]); put(x + dx, y + h, PARCH[0])

def horseshoe(x, y):
    for a in range(0, 181, 12):
        t = math.radians(a)
        put(int(round(x + 3 * math.cos(t))) + 3, int(round(y + 3 * math.sin(t))) + 3, IRON[2])
        put(int(round(x + 4 * math.cos(t))) + 3, int(round(y + 4 * math.sin(t))) + 3, IRON[1])
    put(x + 3, y + 8, IRON[3])

def wheel(cx, cy, r):
    for a in range(0, 360, 3):
        t = math.radians(a)
        for rr in (r, r - 1):
            put(int(round(cx + rr * math.cos(t))), int(round(cy + rr * math.sin(t))), OAK[1] if rr == r else OAK[3])
        put(int(round(cx + (r + 1) * math.cos(t))), int(round(cy + (r + 1) * math.sin(t))), IRON[1])
    for k in range(8):
        t = math.radians(k * 45)
        for s in range(2, r - 1):
            put(int(round(cx + s * math.cos(t))), int(round(cy + s * math.sin(t))), OAK[2])
    for dy in range(-1, 2):
        for dx in range(-1, 2): put(cx + dx, cy + dy, IRON[2])

def sword(x, y, flip=False):
    for i in range(16):
        sx = x + (i if not flip else -i); sy = y + i
        put(sx, sy, (210, 214, 220)); put(sx + (1 if not flip else -1), sy, (150, 156, 164))
    gx, gy = x + (11 if not flip else -11), y + 11
    for k in range(-3, 4): put(gx + k, gy - k if not flip else gy + k, GOLD[2])
    for k in range(1, 4): put(gx + (k if not flip else -k), gy + k, OAK[1])

def shield(x, y, pal):
    for dy in range(12):
        half = 5 if dy < 7 else 5 - (dy - 6)
        for dx in range(-half, half + 1):
            c = pal[2] if dx < 0 else pal[1]
            if abs(dx) == half or dy == 0: c = GOLD[2]
            put(x + dx, y + dy, c)
    for dy in range(2, 9): put(x, y + dy, GOLD[3])
    for dx in range(-3, 4): put(x + dx, y + 4, GOLD[3])

def column(x0, y0, w, h, pal=MARBLE):
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            k = (x - x0)
            lv = 3 if k % 3 == 1 else 2 if k % 3 == 0 else 1
            if k == 0: lv = 1
            if k == w - 1: lv = 0
            put(x, y, pal[lv])
    for x in range(x0 - 2, x0 + w + 2):
        for k in range(3):
            put(x, y0 + k, pal[4 - k]); put(x, y0 + h - 1 - k, pal[2 + (k == 0)])

def crate(x0, y0, w, h, seed):
    wood(x0, y0, w, h, SPRUCE, 'h', plank=5, knots=False, seed=seed)
    frame(x0, y0, w, h)
    for i in range(min(w, h) - 2):
        put(x0 + 1 + i * (w - 2) // (h - 2) if h > 2 else x0, y0 + 1 + i, SPRUCE[4])
    for x in range(x0, x0 + w): put(x, y0 + 1, SPRUCE[0])

def lantern(x, y):
    for dy in range(3): put(x + 2, y + dy, IRON[1])
    for dy in range(3, 10):
        for dx in range(5):
            c = IRON[1] if dx in (0, 4) or dy in (3, 9) else (250, 200, 90) if dy in (5, 6, 7) and dx == 2 else (220, 150, 50)
            put(x + dx, y + dy, c)

# ---------- theme table ----------
T = {
 'oak':      dict(header=OAK, post=OAK, tab=OAK, panel=('wood', PANEL), roof='red', plaque=LIGHT, banner=RED),
 'treasury': dict(header=DARKOAK, post=DARKOAK, tab=DARKOAK, panel=('felt', FELT), roof='slate', plaque=GOLD, banner=[(20,60,36),(28,80,48),(36,100,60),(48,120,74),(64,140,90)], bands=True),
 'registry': dict(header=BIRCH, post=BIRCH, tab=BIRCH, panel=('parch', PARCH), roof='thatch', plaque=PARCH, banner=None),
 'coach':    dict(header=OAK, post=OAK, tab=OAK, panel=('wood', PANEL), roof='canvas', plaque=LIGHT, banner=None),
 'store':    dict(header=SPRUCE, post='crates', tab=SPRUCE, panel=('shelves', PANEL), roof='lintel', plaque=LIGHT, banner=None),
 'guild':    dict(header='stone', post='stone', tab=DSTONE, panel=('dstone', DSTONE), roof='battlements', plaque=STONE, banner=[(20,40,90),(28,54,120),(38,70,150),(52,90,176),(70,112,200)]),
 'clinic':   dict(header='plaster', post=DARKOAK, tab=DARKOAK, panel=('plaster', PLASTER), roof='tiles', plaque=LIGHT, banner=[(150,150,150),(196,196,196),(226,226,226),(240,240,240),(252,252,252)]),
 'market':   dict(header=OAK, post=OAK, tab=OAK, panel=('counter', LIGHT), roof='awning', plaque=LIGHT, banner=None),
 'royal':    dict(header=WALNUT, post='curtains', tab=WALNUT, panel=('felt', VELVET), roof='crown', plaque=GOLD, banner=VELVET),
 'forge':    dict(header=SOOT, post='brick', tab=SOOT, panel=('dbrick', DBRICK), roof='chimney', plaque=LIGHT, banner=[(120,40,10),(170,70,20),(210,100,30),(236,140,50),(250,180,80)], bands=True),
 'arena':    dict(header=OAK, post='palisade', tab=OAK, panel=('sand', SAND), roof='pavilion', plaque=LIGHT, banner=BLUE),
 'board':    dict(header=SPRUCE, post=SPRUCE, tab=SPRUCE, panel=('noticeboard', OAK), roof='gable', plaque=PARCH, banner=None),
 'admin':    dict(header='iron', post='iron', tab=DSTONE, panel=('dstone', DSTONE), roof='spikes', plaque=PARCH, banner=RED),
 'stable':   dict(header=BARN, post=BARN, tab=BARN, panel=('straw', STRAW), roof='shingles', plaque=LIGHT, banner=None),
 'gaol':     dict(header='stone', post='bars', tab=DSTONE, panel=('cell', DSTONE), roof='spikes', plaque=PARCH, banner=None),
 'heraldry': dict(header=DARKOAK, post='banners', tab=DARKOAK, panel=('tapestry', TAPESTRY), roof='pennants', plaque=LIGHT, banner=None),
 'throne':   dict(header='stone', post='pillars', tab=DSTONE, panel=('carpet', LSTONE), roof='arches', plaque=GOLD, banner=RED),
 'harbor':   dict(header=SPRUCE, post='ropes', tab=SPRUCE, panel=('deck', OAK), roof='rope', plaque=LIGHT, banner=None),
 'bank':     dict(header='marble', post='columns', tab=WALNUT, panel=('wood', WALNUT), roof='pediment', plaque=GOLD, banner=[(60,20,70),(80,30,94),(100,42,118),(122,58,140),(146,80,164)]),
}[THEME]

LAYOUT = SPEC['layout']
PINS = set(SPEC.get('pins', []))
DANGER = set(SPEC.get('danger', []))

# ---------- tabs (drawn first: the left post covers their right ends) ----------
for r_, col in SPEC['tabs']:
    col = tuple(col)
    y0 = GY + 18 * r_ + 1
    tp = T['tab']
    if THEME == 'guild':
        stones(2, y0, 56, 16, DSTONE, bw=10, bh=8, seed=40 + r_)
    else:
        wood(2, y0, 56, 16, tp, 'h', plank=8, seed=40 + r_, knots=False)
    for y in range(16):
        cut = abs(7.5 - y) // 2
        for x in range(int(4 - cut)): px[2 + x, y0 + y] = (0, 0, 0, 0)
        put(2 + int(4 - cut), y0 + y, OUT)
    for x in range(2, 58): put(x, y0, OUT); put(x, y0 + 15, OUT)
    for y in range(3, 13):
        for x in range(8, 11): put(x, y0 + y, tuple(max(0, c - (35 if x == 10 else 0)) for c in col))
    nail(50, y0 + 7, GOLD if THEME in ('treasury', 'bank') else IRON)

# ---------- posts ----------
for (x0, s) in ((52, 1), (237, 2)):
    if T['post'] == 'stone':
        stones(x0, BY, 9, BODY, STONE, bw=9, bh=7, seed=10 + s)
    elif T['post'] == 'columns':
        column(x0 + 1, BY, 7, BODY)
    elif T['post'] == 'curtains':
        for y in range(BY, BY + BODY):
            for x in range(x0, x0 + 9):
                fold = (x - x0 + (y - BY) // 12) % 3
                put(x, y, VELVET[[1, 3, 2][fold]])
        tie = BY + BODY // 2
        for x in range(x0 - 1, x0 + 10): put(x, tie, GOLD[3]); put(x, tie + 1, GOLD[1])
        for dy in range(2, 7): put(x0 + 4, tie + dy, GOLD[2])
    elif T['post'] == 'brick':
        stones(x0, BY, 9, BODY, BRICK, bw=6, bh=4, seed=10 + s)
    elif T['post'] == 'palisade':
        for k in range(3):
            xx = x0 + k * 3
            for y in range(BY - 6 + (k % 2) * 2, BY + BODY):
                for dx in range(3):
                    lv = 3 if dx == 0 else 2 if dx == 1 else 1
                    if y < BY - 3 + (k % 2) * 2 and dx != 1: continue
                    put(xx + dx, y, OAK[lv])
            for y in range(BY + 8, BY + BODY, 24): put(xx + 1, y, IRON[2])
    elif T['post'] == 'iron':
        iron_plates(x0, BY, 9, BODY, seed=10 + s, pw=9)
        for y in range(BY + 4, BY + BODY, 10): put(x0 + 2, y, IRON5[4]); put(x0 + 6, y, IRON5[4])
    elif T['post'] == 'bars':
        stones(x0, BY, 9, BODY, DSTONE, bw=9, bh=7, seed=10 + s)
        for xx in (x0 + 2, x0 + 6):
            for y in range(BY, BY + BODY): put(xx, y, IRON[2]); put(xx + 1, y, IRON[1])
    elif T['post'] == 'banners':
        wood(x0, BY, 9, BODY, DARKOAK, 'v', plank=9, seed=10 + s, bevel=False)
        cols = [[(30,90,40),(40,120,54),(56,150,70)], [(140,70,20),(180,96,30),(214,124,44)], [(80,30,110),(104,44,140),(130,62,170)]]
        seg = max(12, BODY // 3)
        for k in range(3):
            for y in range(BY + k * seg + 2, min(BY + (k + 1) * seg, BY + BODY)):
                for x in range(x0 + 1, x0 + 8): put(x, y, cols[k][1 if x in (x0 + 1, x0 + 7) else 2])
            yy = min(BY + (k + 1) * seg, BY + BODY) - 1
            for x in range(x0 + 1, x0 + 8, 2): put(x, yy, (0, 0, 0, 0)) if False else put(x, yy, DARKOAK[1])
    elif T['post'] == 'pillars':
        column(x0 + 1, BY, 7, BODY, LSTONE)
    elif T['post'] == 'ropes':
        wood(x0, BY, 9, BODY, SPRUCE, 'v', plank=9, seed=10 + s, bevel=False)
        for y in range(BY + 4, BY + BODY - 4, 16):
            for k in range(6): rope_line(x0, x0 + 9, y + k) if k in (0, 2, 4) else None
    elif T['post'] == 'crates':
        y = BY
        k = 0
        while y < BY + BODY:
            hh = min(14 + (k % 2) * 4, BY + BODY - y)
            crate(x0, y, 9, hh, seed=60 + k + s * 10); y += hh; k += 1
    else:
        wood(x0, BY, 9, BODY, T['post'], 'v', plank=9, seed=10 + s, bevel=False)
        for y in range(BY, BY + BODY): put(x0, y, OUT); put(x0 + 8, y, OUT)
        for y in range(BY, BY + BODY): put(x0 + 1, y, T['post'][3]); put(x0 + 7, y, T['post'][1])
        for y in range(BY + 9, BY + BODY - 6, 50): nail(x0 + 3, y)
        if T.get('bands'):
            for y in range(BY + 6, BY + BODY - 4, 30):
                for x in range(x0, x0 + 9):
                    put(x, y, IRON[2]); put(x, y + 1, IRON[1])
                put(x0 + 4, y, IRON[3])

# ---------- panel ----------
kind, pal = T['panel']
if kind == 'wood':
    wood(61, BY, 176, BODY, pal, 'v', plank=12, seed=3)
elif kind == 'felt':
    noise_fill(61, BY, 176, BODY, pal, 2, 3, 0.25)
    for x in range(61, 237):                      # brass edging of the counting table
        put(x, BY + 2, GOLD[2]); put(x, BY + BODY - 3, GOLD[1])
    for y in range(BY, BY + BODY):
        put(63, y, GOLD[2]); put(234, y, GOLD[1])
elif kind == 'parch':
    noise_fill(61, BY, 176, BODY, pal, 2, 3, 0.2)
    for x in range(61, 237, 9):                   # faint survey grid
        for y in range(BY, BY + BODY):
            if y % 2 == 0: put(x, y, pal[1])
    for y in range(BY, BY + BODY, 9):
        for x in range(61, 237):
            if x % 2 == 0: put(x, y, pal[1])
elif kind == 'shelves':
    wood(61, BY, 176, BODY, pal, 'h', plank=18, seed=3)
elif kind == 'tapestry':
    tapestry(61, BY, 176, BODY)
    for x in range(61, 237): put(x, BY + 2, GOLD[2]); put(x, BY + BODY - 3, GOLD[2])
elif kind == 'carpet':
    stones(61, BY, 176, BODY, LSTONE, bw=18, bh=18, seed=3)
    cx0, cx1 = GX + 3 * 18 + 2, GX + 6 * 18 - 2      # a red carpet runner down the middle columns
    for y in range(BY, BY + BODY):
        for x in range(cx0, cx1):
            put(x, y, RED[1] if x in (cx0, cx1 - 1) else GOLD[2] if x in (cx0 + 1, cx1 - 2) else RED[2])
elif kind == 'deck':
    wood(61, BY, 176, BODY, OAK, 'h', plank=6, seed=3)
    for y in range(BY + BODY - 6, BY + BODY):
        for x in range(61, 237):
            put(x, y, WATER[(2 + (1 if (x + y * 2) % 7 == 0 else 0)) if y > BY + BODY - 5 else 4])
elif kind == 'straw':
    noise_fill(61, BY, 176, BODY, pal, 2, 3, 0.3)
    r = random.Random(13)
    for _ in range(220):
        x, y = r.randrange(62, 235), r.randrange(BY + 1, BY + BODY - 1)
        for k in range(r.randint(2, 4)): put(x + k, y + (k // 2), pal[r.choice([3, 4])])
elif kind == 'cell':
    stones(61, BY, 176, BODY, pal, bw=14, bh=8, seed=3)
    for col in range(10):                            # iron bars between the slot columns
        xx = GX - 1 + col * 18
        for y in range(BY + 1, BY + BODY):
            put(xx, y, IRON[2]); put(xx - 1, y, IRON[1])
    for y in (BY + 4, BY + BODY - 6):
        for x in range(64, 234): put(x, y, IRON[2]); put(x, y + 1, IRON[1])
elif kind == 'dbrick':
    stones(61, BY, 176, BODY, pal, bw=12, bh=6, seed=3)
    for x in range(61, 237):                        # embers along the hearth
        for k, c in enumerate(((250,180,60), (230,110,30), (150,50,20))):
            if random.Random(x * 7 + k).random() < 0.7 - k * 0.15: put(x, BY + BODY - 3 + k - 2, c)
elif kind == 'sand':
    noise_fill(61, BY, 176, BODY, pal, 2, 3, 0.25)
    r = random.Random(9)
    for _ in range(40):
        x, y = r.randrange(64, 234), r.randrange(BY + 3, BY + BODY - 3)
        put(x, y, pal[0]); put(x + 1, y, pal[1])
elif kind == 'noticeboard':
    wood(61, BY, 176, BODY, OAK, 'h', plank=10, seed=3)
elif kind == 'plaster':
    noise_fill(61, BY, 176, BODY, pal, 2, 3, 0.18)
    for x in range(61, 237): put(x, BY + BODY - 4, DARKOAK[2]); put(x, BY + BODY - 3, DARKOAK[1])
elif kind == 'counter':
    wood(61, BY, 176, BODY, OAK, 'h', plank=9, seed=3)
elif kind == 'dstone':
    stones(61, BY, 176, BODY, pal, bw=16, bh=9, seed=3)
for x in range(61, 237): put(x, BY, OUT)

# ---------- optional parchment map (coach) ----------
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
    for (cx, cy) in [(90, my0 + 10), (104, my0 + 7), (150, my0 + 9), (196, my0 + 12), (212, my0 + 8)]:
        for k in range(6):
            for dx in range(-k, k + 1):
                put(cx + dx, cy - 6 + k, (120,108,96) if dx < 0 else (150,138,124))
        for (dx, dy) in ((0, -6), (-1, -5), (1, -5)): put(cx + dx, cy + dy, (236,232,226))
    fr = random.Random(5)
    for _ in range(46):
        fx_, fy_ = fr.randrange(mx0 + 6, mx1 - 6), fr.randrange(my0 + 18, my1 - 26)
        for (dx, dy, c) in ((0,0,(64,96,48)),(1,0,(80,116,58)),(0,-1,(80,116,58)),(1,-1,(96,132,70)),(0,1,(70,50,30))):
            put(fx_ + dx, fy_ + dy, c)
    pins = sorted(SPEC['pins'])
    if len(pins) >= 2:
        (ax, ay), (bx, by) = [(GX + (s % 9) * 18 + 9, GY + (s // 9) * 18 + 9) for s in pins[:2]]
        steps = int(max(abs(bx - ax), abs(by - ay)))
        for i in range(steps):
            if (i // 3) % 2: continue
            t_ = i / steps
            x = round(ax + (bx - ax) * t_); y = round(ay + (by - ay) * t_ + 4 * math.sin(t_ * 6.28))
            put(x, y, (110,62,30)); put(x, y + 1, (88,48,22))
    for x in range(mx0 - 1, mx1 + 1): put(x, my0 - 1, OUT); put(x, my1, OUT)
    for y in range(my0 - 1, my1 + 1): put(mx0 - 1, y, OUT); put(mx1, y, OUT)

# ---------- sockets / pins ----------
SOCK = {
 'wood': ((16,10,6), (92,64,42), (24,16,10), (36,25,16), (42,29,19)),
 'felt': ((8,24,14), (70,120,84), (12,32,20), (18,44,28), (22,50,32)),
 'parch': ((120,96,60), (240,226,190), (150,124,82), (204,180,130), (196,172,122)),
 'shelves': ((16,10,6), (92,64,42), (24,16,10), (36,25,16), (42,29,19)),
 'dstone': ((10,10,12), (90,90,96), (16,16,20), (24,24,28), (30,30,34)),
 'tapestry': ((70,48,10), (232,190,80), (30,8,8), (44,12,12), (52,16,14)),
 'carpet': ((50,48,44), (200,196,188), (70,68,62), (96,92,86), (104,100,92)),
 'deck': ((30,18,10), (176,128,80), (44,28,16), (62,40,24), (70,46,28)),
 'straw': ((90,64,24), (230,200,130), (120,90,40), (150,116,56), (160,124,62)),
 'cell': ((10,10,12), (90,90,96), (16,16,20), (24,24,28), (30,30,34)),
 'dbrick': ((10,6,4), (110,60,40), (16,10,8), (26,16,12), (32,20,14)),
 'sand': ((110,86,50), (240,222,180), (140,112,70), (176,146,98), (186,156,106)),
 'noticeboard': ((30,18,10), (176,128,80), (44,28,16), (62,40,24), (70,46,28)),
 'plaster': ((80,60,44), (250,248,240), (110,86,64), (150,128,104), (160,138,112)),
 'counter': ((30,18,10), (176,128,80), (44,28,16), (62,40,24), (70,46,28)),
}[kind]
if THEME == 'royal': SOCK = ((70,48,10), (232,190,80), (20,8,26), (30,12,38), (36,16,44))
if THEME == 'bank': SOCK = ((70,48,10), (232,190,80), (20,13,9), (30,20,14), (36,24,17))
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
            if x == 0 or y == 0: c = SOCK[0]
            elif x == 17 or y == 17: c = SOCK[1]
            elif x == 1 or y == 1: c = SOCK[2]
            else: c = SOCK[3] if r.random() > 0.15 else SOCK[4]
            if i in DANGER and (x in (0, 17) or y in (0, 17)): c = (170, 30, 30)
            elif i in DANGER and (x in (1, 16) or y in (1, 16)): c = (110, 20, 20)
            put(sx + x, sy + y, c)
if kind == 'cell':
    rn = random.Random(21)
    for i, name in enumerate(LAYOUT):
        if name or rn.random() > 0.18: continue
        sx, sy = GX + (i % 9) * 18, GY + (i // 9) * 18
        poster(sx + 3, sy + 2, i)
if kind == 'noticeboard':
    rn = random.Random(12)
    for i, name in enumerate(LAYOUT):
        if name or rn.random() > 0.35: continue
        sx, sy = GX + (i % 9) * 18, GY + (i // 9) * 18
        note(sx + 3 + rn.randrange(3), sy + 2 + rn.randrange(3), 11, 13, i)
if kind == 'shelves':                              # a shelf board under every row
    for row in range(ROWS):
        y = GY + 18 * row + 17
        for x in range(62, 236):
            put(x, y, SPRUCE[3]); put(x, y + 1, SPRUCE[1]); put(x, y + 2, SPRUCE[0])
        for x in (66, 232): put(x, y + 3, IRON[1]); put(x, y + 4, IRON[1])

# ---------- header ----------
if T['header'] == 'stone':
    stones(44, HY, 210, 24, STONE, bw=14, bh=8, seed=21)
elif T['header'] == 'marble':
    marble(44, HY, 210, 24, seed=21)
    for x in range(44, 254): put(x, HY + 2, MARBLE[4]); put(x, HY + 21, MARBLE[1])
elif T['header'] == 'plaster':
    plaster_timber(44, HY, 210, 24, seed=21)
elif T['header'] == 'iron':
    iron_plates(44, HY, 210, 24, seed=21)
else:
    wood(44, HY, 210, 24, T['header'], 'h', plank=8, seed=21)
frame(44, HY, 210, 24)
if T.get('bands'):
    band(45, 253, HY + 3, IRON); band(45, 253, HY + 18, IRON)
if THEME == 'royal':
    for x in range(45, 253): put(x, HY + 2, GOLD[3]); put(x, HY + 21, GOLD[2])
    for x in range(48, 252, 6): put(x, HY + 4, GOLD[1]); put(x + 3, HY + 19, GOLD[1])
if T['header'] not in ('stone', 'marble', 'plaster', 'iron'):
    bp = GOLD if THEME in ('treasury', 'royal') else IRON
    bracket(45, HY + 1, pal=bp); bracket(245, HY + 1, True, pal=bp)
    bracket(45, HY + 15, flipy=True, pal=bp); bracket(245, HY + 15, True, True, pal=bp)

# plaque
pp = T['plaque']
if pp is GOLD:
    noise_fill(104, HY + 2, 90, 20, GOLD, 3, 31, 0.12)
    for x in range(104, 194): put(x, HY + 3, GOLD[4]); put(x, HY + 20, GOLD[1])
elif pp is STONE:
    stones(104, HY + 2, 90, 20, STONE, bw=30, bh=10, seed=31)
elif pp is PARCH:
    noise_fill(104, HY + 2, 90, 20, PARCH, 3, 31, 0.15)
else:
    wood(104, HY + 2, 90, 20, pp, 'h', plank=10, seed=31, knots=False)
    for x in range(105, 193): put(x, HY + 3, pp[4]); put(x, HY + 20, pp[0])
frame(104, HY + 2, 90, 20)
if THEME == 'registry':
    wax_seal(108, HY + 20); wax_seal(190, HY + 20)
else:
    for (x, y) in ((106, HY + 4), (190, HY + 4), (106, HY + 18), (190, HY + 18)):
        nail(x, y, GOLD if pp is not GOLD and THEME in ('treasury', 'bank') else IRON)

# side decorations on the header (x 60..100 and 198..238)
if THEME == 'oak' or THEME == 'store':
    for x0 in (64, 198):
        wood(x0, HY + 7, 36, 10, T['header'] if T['header'] in (OAK, SPRUCE) else OAK, 'h', plank=10, seed=x0, knots=False)
        frame(x0, HY + 7, 36, 10)
    if THEME == 'store':
        for x0 in (70, 204):
            for k, c in enumerate(((150,120,70), (170,140,86), (130,100,60))):
                put(x0 + 10 + k * 6, HY + 11, c)
elif THEME == 'treasury':
    coin_stack(68, HY + 17, 5); coin_stack(78, HY + 17, 7); coin_stack(88, HY + 17, 4)
    coin_stack(204, HY + 17, 4); coin_stack(214, HY + 17, 7); coin_stack(224, HY + 17, 5)
    padlock(146, HY + 22)
elif THEME == 'registry':
    scroll_end(66, HY + 6, 12); scroll_end(92, HY + 6, 12)
    for x in range(72, 92): put(x, HY + 8, PARCH[3]); put(x, HY + 16, PARCH[1])
    for y in range(HY + 9, HY + 16):
        for x in range(72, 92): put(x, y, PARCH[2] if (y - HY) % 3 else (120, 96, 60))
    quill(206, HY + 18)
    for dx in range(4):                            # inkpot
        for dy in range(5): put(222 + dx, HY + 14 + dy, (20, 20, 34) if dy else IRON[2])
elif THEME == 'coach':
    horseshoe(72, HY + 7); horseshoe(86, HY + 7); horseshoe(206, HY + 7); horseshoe(220, HY + 7)
elif THEME == 'guild':
    sword(66, HY + 4); sword(96, HY + 4, flip=True); shield(81, HY + 8, T['banner'])
    sword(200, HY + 4); sword(230, HY + 4, flip=True); shield(215, HY + 8, T['banner'])
elif THEME == 'heraldry':
    shield(72, HY + 6, [(20,70,30),(30,100,44),(44,130,60),(60,150,76),(80,170,96)])
    shield(86, HY + 6, [(110,50,10),(150,76,20),(190,100,30),(214,124,44),(230,150,70)])
    shield(212, HY + 6, [(60,20,90),(80,30,120),(104,44,150),(126,62,170),(150,86,190)])
    shield(226, HY + 6, RED)
elif THEME == 'throne':
    crown(84, HY + 3); crown(214, HY + 3)
    for x in range(45, 253): put(x, HY + 2, GOLD[3]); put(x, HY + 21, GOLD[2])
elif THEME == 'harbor':
    anchor(70, HY + 4); ship_wheel(222, HY + 12)
    rope_line(45, 253, HY + 1); rope_line(45, 253, HY + 21)
elif THEME == 'admin':
    wax_seal(80, HY + 12); wax_seal(218, HY + 12)
    for x0 in (64, 92, 202, 230):
        for y in range(HY + 4, HY + 20, 2): put(x0, y, IRON5[4]); put(x0 + 1, y + 1, IRON5[1])
elif THEME == 'stable':
    hay(66, HY + 9, 18, 9); horseshoe(88, HY + 6); hay(214, HY + 9, 18, 9); horseshoe(202, HY + 6)
    for (xa, xb) in ((44, 104), (194, 254)):          # white barn trim crosses
        for i in range(24):
            put(xa + i * (xb - xa) // 24, HY + i, (226, 220, 206)); put(xb - 1 - i * (xb - xa) // 24, HY + i, (226, 220, 206))
elif THEME == 'gaol':
    shackle(76, HY + 14); shackle(88, HY + 14); torch(206, HY + 6); torch(224, HY + 6)
elif THEME == 'forge':
    anvil(70, HY + 10); hammer_tongs(210, HY + 5)
elif THEME == 'arena':
    lance(64, HY + 4); lance(98, HY + 4, flip=True); shield(81, HY + 6, RED)
    lance(200, HY + 4); lance(234, HY + 4, flip=True); shield(217, HY + 6, BLUE)
elif THEME == 'board':
    lantern(72, HY + 6); bell(214, HY + 6)
    note(84, HY + 6, 10, 12, 1); note(198, HY + 6, 10, 12, 2)
elif THEME == 'clinic':
    jar(66, HY + 9, (60, 140, 70)); jar(75, HY + 9, (170, 50, 50)); jar(84, HY + 9, (200, 170, 60)); jar(93, HY + 9, (80, 90, 170))
    herbs(204, HY + 8, [(70, 110, 50), (96, 140, 66)]); herbs(214, HY + 8, [(120, 110, 60), (150, 140, 80)]); herbs(224, HY + 8, [(60, 100, 80), (90, 130, 100)])
elif THEME == 'market':
    scale(70, HY + 5)
    basket(204, HY + 8, [(190, 40, 40), (220, 70, 60)]); basket(220, HY + 8, [(230, 180, 40), (240, 200, 70)])
elif THEME == 'royal':
    for x0, flip in ((70, False), (206, True)):
        for i in range(20):
            yy = HY + 12 + int(3 * math.sin(i / 3.0))
            put(x0 + i, yy, GOLD[3]); put(x0 + i, yy + 1, GOLD[1])
elif THEME == 'bank':
    for x0 in (66, 82, 206, 222):
        column(x0, HY + 3, 6, 19)

# ---------- roof ----------
if T['roof'] == 'red':
    for x in range(41, 257):
        for y in range(E, E + 6):
            lv = 3 if y == E else (1 if y == E + 5 else 2)
            if (x + ((y - E) // 2) * 3) % 6 == 0 and E < y < E + 5: lv = 1
            put(x, y, RED[lv])
    for x in range(41, 257): put(x, E + 6, OUT)
elif T['roof'] == 'slate':
    for x in range(40, 258):
        for y in range(E - 2, E + 7):
            lv = 3 if (y - E + 2) % 3 == 0 else 2
            if (x + ((y - E + 2) // 3) * 4) % 8 == 0: lv = 0
            put(x, y, SLATE[lv])
    for x in range(40, 258): put(x, E + 7, OUT)
elif T['roof'] == 'thatch':
    r = random.Random(4)
    for x in range(38, 260):
        top = E - 4 + int(2 * math.sin(x / 7.0))
        for y in range(top, E + 7):
            put(x, y, STRAW[max(0, min(4, (2 if (x + y) % 3 else 3) + (r.choice([-1, 0, 0, 1]))))])
        put(x, E + 7, STRAW[0])
elif T['roof'] == 'canvas':
    for x in range(42, 256):
        t = (x - 42) / 213.0
        top = int(E - 9 * math.sin(math.pi * t)) + 2
        for y in range(top, E + 7):
            lv = 3 if y == top else 2
            if (x - 42) % 30 in (0, 1): lv = 1
            put(x, y, CANVAS[lv])
        put(x, top - 1, OUT); put(x, E + 7, OUT)
    for x0 in (42, 72, 102, 132, 162, 192, 222, 252):
        for y in range(E, E + 7): put(x0, y, OAK[1])
    lantern(60, HY + 25); lantern(232, HY + 25)
elif T['roof'] == 'lintel':
    wood(42, E + 1, 214, 6, SPRUCE, 'h', plank=6, seed=9, knots=False)
    frame(42, E + 1, 214, 6)
    for x in range(48, 252, 16): nail(x, E + 3)
elif T['roof'] == 'battlements':
    for x in range(42, 256):
        merlon = ((x - 42) // 10) % 2 == 0
        top = E - 6 if merlon else E
        for y in range(top, E + 7):
            lv = 3 if y == top else 2 if (x + y) % 7 else 1
            put(x, y, STONE[lv])
        put(x, top - 1, OUT)
    for x in range(42, 256): put(x, E + 7, OUT)
elif T['roof'] == 'pennants':
    wood(42, E + 1, 214, 6, DARKOAK, 'h', plank=6, seed=9, knots=False)
    frame(42, E + 1, 214, 6)
    cols = [(40,120,54), (190,100,30), (104,44,150), (170,40,40)]
    for k, x0 in enumerate(range(50, 250, 16)):
        c = cols[k % 4]
        for dy in range(7):
            for dx in range(0, 7 - dy): put(x0 + dx - (7 - dy) // 2 + 3, E - 6 + dy, c)
        put(x0 + 3, E - 7, OAK[1])
elif T['roof'] == 'arches':
    for x in range(40, 258):
        for y in range(E - 4, E + 7): put(x, y, LSTONE[2] if (x + y) % 6 else LSTONE[1])
        put(x, E - 5, OUT); put(x, E + 7, OUT)
    for cx in range(54, 250, 24):
        for a in range(0, 181, 5):
            t_ = math.radians(a)
            for rr in (8, 9):
                put(int(round(cx + rr * math.cos(t_))), int(round(E + 6 - rr * 0.6 * math.sin(t_))), LSTONE[0] if rr == 9 else GOLD[1])
elif T['roof'] == 'rope':
    wood(42, E + 1, 214, 6, SPRUCE, 'h', plank=6, seed=9, knots=False)
    frame(42, E + 1, 214, 6)
    for x0 in range(42, 256, 24):
        for i in range(25):
            put(x0 + i, E + 7 + int(3 * math.sin(math.pi * i / 24)), (176, 146, 96))
elif T['roof'] == 'spikes':
    for x in range(42, 256):
        for y in range(E + 2, E + 7): put(x, y, IRON5[2] if y > E + 2 else IRON5[4])
        put(x, E + 7, OUT)
    spikes(42, 256, E + 1, 7)
elif T['roof'] == 'shingles':
    for x in range(40, 258):
        t_ = abs((x - 149) / 109.0)
        top = int(E - 6 + 9 * t_)
        for y in range(top, E + 7):
            lv = 3 if (y - top) % 3 == 0 else 2
            if (x + (y // 3) * 3) % 6 == 0: lv = 1
            put(x, y, OAK[lv])
        put(x, top - 1, OUT); put(x, E + 7, OUT)
        if x % 9 == 0: put(x, top - 2, STRAW[3]); put(x + 1, top - 2, STRAW[2])
elif T['roof'] == 'chimney':
    for x in range(40, 258):
        for y in range(E + 1, E + 7): put(x, y, STONE[2] if (x + y) % 5 else STONE[1])
        put(x, E, STONE[3]); put(x, E + 7, OUT)
    for x in range(138, 160):
        for y in range(0, E + 1): put(x, y, BRICK[2] if (y // 3 + (x // 5)) % 2 else BRICK[1]) if y % 3 else put(x, y, BRICK[0])
    frame(138, 0, 22, E + 2)
    smoke(146, 0); smoke(152, 2)
elif T['roof'] == 'pavilion':
    for x in range(40, 258):
        t_ = abs((x - 149) / 109.0)
        top = int(E - 9 + 13 * t_)
        stripe = ((x - 40) // 9) % 2
        for y in range(top, E + 7):
            put(x, y, (BLUE if stripe else GOLD)[3 if y == top else 2])
        put(x, top - 1, OUT); put(x, E + 7, OUT)
    for dx in range(-3, 4): put(149 + dx, E + 7, GOLD[1])
    pennant(149, 0, (200, 40, 40)); pennant(60, E - 2, (40, 80, 180)); pennant(236, E - 2, (40, 80, 180))
elif T['roof'] == 'gable':
    for x in range(40, 258):
        t_ = abs((x - 149) / 109.0)
        top = int(E - 7 + 10 * t_)
        for y in range(top, E + 7):
            lv = 3 if (y - top) % 3 == 0 else 2
            if (x + (y // 3) * 4) % 7 == 0: lv = 1
            put(x, y, SPRUCE[lv])
        put(x, top - 1, OUT); put(x, E + 7, OUT)
elif T['roof'] == 'tiles':
    for x in range(40, 258):
        for y in range(E - 2, E + 7):
            k = (x - 40) % 6
            row = (y - E + 2) // 3
            lv = [1, 2, 3, 3, 2, 1][(k + row * 3) % 6]
            if (y - E + 2) % 3 == 2: lv = 0
            put(x, y, TILE[lv])
    for x in range(40, 258): put(x, E - 3, OUT); put(x, E + 7, OUT)
elif T['roof'] == 'awning':
    for x in range(38, 260):
        stripe = ((x - 38) // 10) % 2
        pal_ = RED if stripe == 0 else [(170,160,140),(200,190,170),(224,216,196),(236,230,214),(246,242,230)]
        bottom = E + 7 + (2 if (x - 38) % 10 < 5 else 4) - (1 if (x - 38) % 10 in (0, 9) else 0)
        for y in range(E - 3, bottom):
            put(x, y, pal_[3 if y == E - 3 else 2 if y < bottom - 1 else 1])
        put(x, bottom, OUT)
    for x in range(38, 260): put(x, E - 4, OUT)
    for k, x0 in enumerate(range(60, 240, 14)):     # bunting under the awning
        c = [(196,60,50), (60,110,190), (220,180,60)][k % 3]
        for dy in range(4):
            for dx in range(-3 + dy, 4 - dy): put(x0 + dx, HY + 1 + dy, c) if 0 <= dy < 4 else None
elif T['roof'] == 'crown':
    for x in range(42, 256):
        for y in range(E + 1, E + 7): put(x, y, WALNUT[3] if y == E + 1 else WALNUT[2])
        put(x, E, GOLD[3]); put(x, E + 7, OUT)
    crown(149, E - 9)
elif T['roof'] == 'pediment':
    for x in range(40, 258):
        t = abs((x - 149) / 109.0)
        top = int(E - 9 + 9 * t)
        for y in range(top, E + 7):
            put(x, y, MARBLE[3] if y > top + 1 else MARBLE[4])
        put(x, top - 1, OUT)
    for dy in range(-4, 3):                        # a coin roundel in the tympanum
        for dx in range(-4, 5):
            if dx * dx + dy * dy <= 13: put(149 + dx, E + 1 + dy, GOLD[3] if dx * dx + dy * dy < 7 else GOLD[1])
    for x in range(40, 258): put(x, E + 7, OUT)

# banner on the right post
if T['banner']:
    cloth(241, BY, 7, 46, T['banner'], seed=5)
    if THEME == 'treasury':
        for dy in (14, 15, 16):
            for dx in (2, 3, 4): put(241 + dx, BY + dy, GOLD[3])

# bottom plank + foot
if T['header'] == 'stone':
    stones(44, BY + BODY, 210, 10, STONE, bw=14, bh=5, seed=51)
elif T['header'] == 'marble':
    marble(44, BY + BODY, 210, 10, seed=51)
elif T['header'] == 'plaster':
    plaster_timber(44, BY + BODY, 210, 10, seed=51)
elif T['header'] == 'iron':
    iron_plates(44, BY + BODY, 210, 10, seed=51)
else:
    wood(44, BY + BODY, 210, 10, T['header'], 'h', plank=10, seed=51)
frame(44, BY + BODY, 210, 10)
nail(48, BY + BODY + 4); nail(248, BY + BODY + 4)
if THEME == 'coach':
    wheel(58, BY + BODY + 6, 9); wheel(240, BY + BODY + 6, 9)
else:
    foot = TAPESTRY if THEME == 'heraldry' else LSTONE if THEME == 'throne' else WATER if THEME == 'harbor' else IRON5 if THEME == 'admin' else STRAW if THEME == 'stable' else DSTONE if THEME == 'gaol' else DBRICK if THEME == 'forge' else SAND if THEME == 'arena' else DSTONE if THEME == 'guild' else MARBLE if THEME == 'bank' else PLASTER if THEME == 'clinic' else PANEL
    for y in range(BY + BODY + 10, BY + BODY + 16):
        for x in range(60, 238): put(x, y, foot[2] if y < BY + BODY + 15 else foot[0])

# cast shadows
for i, f in enumerate((0.55, 0.7, 0.82, 0.92)):
    shade(61, BY + 2 + i, 176, 1, f)
    shade(61 + i, BY + 2, 1, BODY - 2, f + 0.04)
    shade(236 - i, BY + 2, 1, BODY - 2, f + 0.04)
for i, f in enumerate((0.6, 0.78, 0.9)):
    shade(45, HY + 1 + i, 208, 1, f)
    shade(45, BY + BODY + 1 + i, 208, 1, f + 0.05)

img.save(SPEC['out'])
print('ok', THEME, W, H)
