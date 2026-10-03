"""Job tools and the tier medallion they sit in (Stage 7).

Each tool function paints one object on a fresh Canvas and returns the image; job(id) puts the
job's tool inside a medallion whose rim shows the Tier: bronze (1), silver (2), gold (3),
gold with gems (4), gold with a crown and a glow (5).
"""
import numpy as np
from PIL import Image
from lib import (N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, chrome, gold_tint, steel_tint,
                 cloth, leather_col, band, sword, gold_coin, coin_flat, parchment, noise, edge_darken, mask_from, load_icon)


def _stick(c, rng, p0, p1, w=13, col=(0.55, 0.36, 0.18)):
    s, t = band(p0, p1, 0)
    m = blur(((s > 0) & (s < 1) & (np.abs(t) < w)).astype(np.float32), 1)
    ang = np.arctan2(p1[1] - p0[1], p1[0] - p0[0])
    c.over(light(np.clip(1 - np.abs(t) / w, 0, 1) ** 0.5 * m, wood(rng, col, angle=ang + np.pi / 2, rings=4), depth=30, spec=0.3), m)


def _metal(c, m, tint=(0.60, 0.62, 0.66), depth=50, pill=10, k=0.5):
    c.over(chrome(k * pillow(m, pill), tint, depth=depth, sky=0.85, ground=0.1), m)


def glow(c, cx, cy, r, color, k=0.6):
    """Light thrown by something bright: tints what is already painted, never the empty air
    (a halo in the air would be cropped in and outlined as a dark square by build.py)."""
    g = blur(ellipse([cx - r, cy - r, cx + r, cy + r]), r * 0.5) * c.px[..., 3]
    c.over(np.zeros((N, N, 3)) + np.array(color), np.clip(g * k, 0, 1), cast=False)


def bolt(c, pts, width=26, color=(0.80, 0.90, 1.0)):
    """A lightning bolt along pts, with a blue halo."""
    halo = blur(poly(pts, width=width * 3), 14)
    halo = np.where(c.px[..., 3] > 0.05, halo, np.clip(halo - 0.55, 0, 1) * 2)   # a tight halo where nothing is behind it
    c.over(np.zeros((N, N, 3)) + np.array([0.35, 0.55, 1.0]), np.clip(halo * 0.7, 0, 1), cast=False)
    core = blur(poly(pts, width=width), 1.5)
    c.over(np.zeros((N, N, 3)) + np.array(color), core, cast=False)
    c.over(np.ones((N, N, 3)), blur(poly(pts, width=max(4, width // 3)), 1), cast=False)


# ===== tools =====

def pickaxe(rng, tint=(0.50, 0.52, 0.55)):
    c = Canvas()
    _stick(c, rng, (110, 470), (330, 140))
    cx, cy, r = 300, 330, 230
    rr = np.hypot(xx - cx, yy - cy); ang = np.arctan2(yy - cy, xx - cx)
    head = blur(((np.abs(rr - r) < 26 * np.clip(1 - np.abs(ang + np.pi / 2 + 0.25) / 1.0, 0.25, 1)) & (ang > -np.pi / 2 - 1.1) & (ang < -np.pi / 2 + 0.6)).astype(np.float32), 1.2)
    c.over(chrome(np.clip(1 - np.abs(rr - r) / 26, 0, 1) ** 0.5 * head, tint, depth=50, sky=0.85, ground=0.1), head)
    return c.image()


def axe(rng, double=False, tint=(0.55, 0.57, 0.60)):
    c = Canvas()
    _stick(c, rng, (150, 480), (330, 60), w=15)
    blade = poly([(300, 100), (420, 50), (450, 150), (420, 250), (300, 200)])
    if double:
        blade = np.maximum(blade, poly([(330, 110), (210, 60), (180, 150), (210, 250), (330, 200)]))
    blade = blur(blade, 1.2)
    edge = np.clip(1 - np.abs(xx - 440) / 30, 0, 1) * blade
    c.over(chrome(0.45 * pillow(blade, 16) + 0.2 * edge, tint, depth=50, sky=0.9, ground=0.1), blade)
    return c.image()


def herbs(rng):
    c = Canvas()
    for k, a in enumerate(np.linspace(-0.7, 0.7, 5)):
        tip = (256 + 200 * np.sin(a), 470 - 380 * np.cos(a))
        st = blur(poly([(256, 470), ((256 + tip[0]) / 2 + 20 * a, (470 + tip[1]) / 2), tip], width=8), 1)
        c.over(np.zeros((N, N, 3)) + np.array([0.25, 0.45, 0.15]), st)
        for j in range(3):
            fx = 256 + (tip[0] - 256) * (0.45 + j * 0.22); fy = 470 + (tip[1] - 470) * (0.45 + j * 0.22)
            for side in (-1, 1):
                lx, ly = fx + side * 34, fy + 8
                leaf = blur(poly([(fx, fy), (lx - side * 4, ly - 26), (lx + side * 10, ly), (lx - side * 4, ly + 14)]), 1)
                c.over(light(0.4 * pillow(leaf, 6), np.zeros((N, N, 3)) + np.array([0.22, 0.55, 0.18]) * (0.85 + 0.25 * rng.random()), depth=30, spec=0.3), leaf)
        fl = blur(ellipse([tip[0] - 22, tip[1] - 22, tip[0] + 22, tip[1] + 22]), 1)
        c.over(light(pillow(fl, 10), np.zeros((N, N, 3)) + np.array([0.72, 0.40, 0.85]), depth=30, spec=0.4), fl)
    return c.image()


def fishing(rng, hook_only=False):
    c = Canvas()
    if not hook_only:
        _stick(c, rng, (90, 480), (430, 50), w=10, col=(0.62, 0.48, 0.26))
        line = blur(poly([(430, 50), (440, 200), (420, 300)], width=3), 0.8)
        c.over(np.zeros((N, N, 3)) + 0.85, line, cast=False)
    fx, fy = (330, 380) if not hook_only else (256, 330)
    body = blur(ellipse([fx - 110, fy - 50, fx + 90, fy + 50]), 1.2)
    tail = blur(poly([(fx + 80, fy), (fx + 150, fy - 55), (fx + 140, fy), (fx + 150, fy + 55)]), 1.2)
    fish = np.clip(body + tail, 0, 1)
    nx = (xx - fx + 10) / 100; ny = (yy - fy) / 50
    h = np.sqrt(np.clip(1 - nx ** 2 - ny ** 2, 0, 1)) * body + 0.2 * pillow(tail, 6)
    col = np.zeros((N, N, 3)) + np.array([0.45, 0.62, 0.70])
    col = col * (1 - 0.4 * np.clip((fy - yy) / 50, 0, 1))[..., None] + np.array([0.3, 0.25, 0.1]) * np.clip((yy - fy) / 50, 0, 1)[..., None]
    scales = 0.9 + 0.1 * np.sin(xx / 6.0) * np.sin(yy / 6.0)
    c.over(chrome(h * 0.7, (0.75, 0.85, 0.90), depth=40, sky=0.9, ground=0.3) * 0.5 + col * scales[..., None] * 0.6, fish)
    eye = blur(ellipse([fx - 85, fy - 18, fx - 65, fy + 2]), 1)
    c.over(np.zeros((N, N, 3)) + 0.05, eye)
    if hook_only:
        hook = blur(mask_from(lambda d: d.arc([fx - 160, fy - 230, fx - 60, fy - 110], 0, 200, fill=255, width=12)), 1)
        c.over(chrome(0.6 * pillow(hook, 4), (0.65, 0.67, 0.72), depth=30), hook)
        ln = blur(poly([(fx - 60, fy - 175), (fx - 60, fy - 300)], width=3), 0.8)
        c.over(np.zeros((N, N, 3)) + 0.85, ln, cast=False)
    return c.image()


def spyglass(rng):
    c = Canvas()
    s, t = band((90, 400), (440, 150), 0)
    for (a, b, w, tint) in ((0.0, 0.45, 44, gold_tint()), (0.42, 0.75, 36, (0.45, 0.25, 0.12)), (0.72, 1.0, 28, gold_tint())):
        m = blur(((s > a) & (s < b) & (np.abs(t) < w)).astype(np.float32), 1)
        hh = np.clip(1 - np.abs(t) / w, 0, 1) ** 0.5 * m
        if tint[0] < 0.5:
            c.over(light(hh, leather_col(rng, tint), depth=40, spec=0.3), m)
        else:
            c.over(chrome(hh, tint, depth=40), m)
    lens = blur(ellipse([66, 350, 114, 450]), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.6, 0.8, 0.95]), lens)
    return c.image()


def bow(rng, with_arrow=True, leaf=False):
    c = Canvas()
    b = blur(mask_from(lambda d: d.arc([60, 40, 420, 480], 300, 60, fill=255, width=22)), 1)
    c.over(light(0.5 * pillow(b, 6), wood(rng, (0.48, 0.28, 0.12), rings=4), depth=40, spec=0.3), b)
    string = blur(poly([(330, 72), (330, 448)], width=3), 0.8)
    c.over(np.zeros((N, N, 3)) + 0.9, string, cast=False)
    if with_arrow:
        _stick(c, rng, (100, 260), (460, 260), w=6, col=(0.70, 0.55, 0.32))
        head = blur(poly([(460, 240), (500, 260), (460, 280)]), 1)
        _metal(c, head, pill=4)
        for dy in (-1, 1):
            fl = blur(poly([(100, 260), (140, 260), (120, 260 + dy * 30), (80, 260 + dy * 30)]), 1)
            c.over(light(0.3 * pillow(fl, 4), cloth(rng, (0.75, 0.15, 0.10)), depth=20, spec=0.1), fl)
    if leaf:
        lf = blur(poly([(330, 290), (420, 350), (470, 440), (380, 410)]), 1.2)
        c.over(light(0.4 * pillow(lf, 8), np.zeros((N, N, 3)) + np.array([0.25, 0.55, 0.18]), depth=30, spec=0.3), lf)
    return c.image()


def practice_sword(rng):
    c = Canvas()
    s, t = band((120, 440), (420, 80), 0)
    bl = blur(((s > 0.25) & (s < 1) & (np.abs(t) < 24 * np.clip((1 - s) / 0.1, 0.3, 1))).astype(np.float32), 1)
    c.over(light(0.5 * pillow(bl, 10), wood(rng, (0.70, 0.52, 0.28), angle=-0.9, rings=3), depth=40, spec=0.2), bl)
    gd = blur(((np.abs(s - 0.25) < 0.025) & (np.abs(t) < 60)).astype(np.float32), 1)
    c.over(light(0.5 * pillow(gd, 6), wood(rng, (0.45, 0.28, 0.12), rings=3), depth=40, spec=0.2), gd)
    gr = blur(((s > 0.03) & (s < 0.23) & (np.abs(t) < 12)).astype(np.float32), 1)
    wrap = 0.75 + 0.25 * np.sin(s * 160)
    c.over(light(0.5 * pillow(gr, 5), cloth(rng, (0.80, 0.75, 0.62)) * wrap[..., None], depth=30, spec=0.1), gr)
    return c.image()


def cook_pot(rng):
    c = Canvas()
    pot = blur(np.maximum(ellipse([90, 200, 422, 470]) * (yy > 240), rect([90, 240, 422, 330])), 1.2)
    nx = (xx - 256) / 166
    _ = c.over(chrome(np.sqrt(np.clip(1 - nx ** 2, 0, 1)) * pot * 0.8, (0.30, 0.30, 0.32), depth=60, sky=0.6, ground=0.06), pot)
    rim = blur(ellipse([80, 210, 432, 270]), 1)
    c.over(chrome(0.3 * pillow(rim, 6), (0.40, 0.40, 0.43), depth=40, sky=0.7, ground=0.08), rim)
    stew = blur(ellipse([100, 220, 412, 262]), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.55, 0.30, 0.12]) * (0.8 + 0.4 * noise(rng, 30, 2))[..., None], stew)
    for (x, r) in ((200, 30), (300, 34), (250, 40)):
        st = blur(ellipse([x - r, 120 - r, x + r, 120 + r]), 14) * 0.35
        c.over(np.zeros((N, N, 3)) + 0.9, st, cast=False)
    _stick(c, rng, (300, 240), (420, 60), w=11)
    bowl = blur(ellipse([270, 220, 330, 260]), 1)
    c.over(light(0.5 * pillow(bowl, 6), wood(rng, (0.55, 0.36, 0.18), rings=3), depth=30, spec=0.2), bowl)
    return c.image()


def hammer_anvil(rng, gold=False):
    c = Canvas()
    tint = gold_tint() if gold else (0.38, 0.38, 0.42)
    anvil = blur(poly([(60, 260), (380, 260), (452, 230), (452, 270), (380, 320), (330, 330), (330, 400), (390, 460), (130, 460),
                       (190, 400), (190, 330), (140, 320), (60, 300)]), 1.2)
    c.over(chrome(0.35 * pillow(anvil, 16), tint, depth=50, sky=0.8, ground=0.1), anvil)
    _stick(c, rng, (180, 210), (420, 40), w=13)
    s2, t2 = band((110, 140), (230, 250), 0)
    head = blur(((s2 > 0) & (s2 < 1) & (np.abs(t2) < 40)).astype(np.float32), 1.2)
    _metal(c, head, (0.55, 0.57, 0.60), pill=10)
    return c.image()


def gear(c, cx, cy, r, teeth=10, tint=(0.62, 0.64, 0.68), hole=0.35):
    ang = np.arctan2(yy - cy, xx - cx); d = np.hypot(xx - cx, yy - cy)
    m = blur(((d < r * (0.82 + 0.18 * (np.cos(ang * teeth) > 0.1))) & (d > r * hole)).astype(np.float32), 1.2)
    h = 0.4 * pillow(m, 8) + 0.2 * (np.abs(d - r * 0.6) < r * 0.08) * m
    c.over(chrome(h, tint, depth=50, sky=0.9, ground=0.12), m)


def gear_wrench(rng):
    c = Canvas()
    gear(c, 230, 260, 170, 10)
    s, t = band((120, 460), (420, 120), 0)
    w = blur(((s > 0.05) & (s < 0.85) & (np.abs(t) < 18)).astype(np.float32), 1)
    jaw = blur(np.clip(ellipse([360, 60, 470, 170]) - ellipse([395, 50, 470, 110]), 0, 1), 1)
    _metal(c, np.clip(w + jaw, 0, 1), (0.70, 0.72, 0.76), pill=8)
    return c.image()


def kite_shield(rng, color=(0.15, 0.25, 0.55), emblem=None):
    c = Canvas()
    sh = blur(poly([(110, 60), (402, 60), (420, 200), (380, 340), (256, 480), (132, 340), (92, 200)]), 1.5)
    nx = (xx - 256) / 160
    h = np.sqrt(np.clip(1 - nx ** 2, 0, 1)) * sh * 0.6
    c.over(light(h, cloth(rng, color, weave=2), depth=60, spec=0.3), sh)
    inner = blur(poly([(132, 82), (380, 82), (396, 200), (360, 330), (256, 452), (152, 330), (116, 200)]), 1)
    rim = np.clip(sh - inner, 0, 1)
    c.over(chrome(0.4 * pillow(rim, 4) + 0.5 * h, (0.70, 0.72, 0.76), depth=40, sky=0.85, ground=0.1), rim)
    boss = blur(ellipse([216, 180, 296, 260]), 1)
    if emblem == 'bolt':
        bolt(c, [(280, 110), (220, 250), (290, 240), (230, 400)], width=26, color=(0.95, 0.95, 0.70))
    else:
        c.over(chrome(pillow(boss, 20, 0.7), (0.70, 0.72, 0.76), depth=50), boss)
    return c.image()


def rapier(rng):
    c = Canvas()
    sword(c, rng, (140, 440), (460, 40), blade_w=11, guard_w=40)
    cup = blur(mask_from(lambda d: d.arc([110, 300, 250, 440], 200, 380, fill=255, width=12)), 1)
    c.over(chrome(0.5 * pillow(cup, 4), gold_tint(), depth=30), cup)
    return c.image()


def barrel(rng):
    c = Canvas()
    k = blur(np.maximum(ellipse([110, 70, 402, 470]) * ((yy > 100) & (yy < 440)), rect([130, 100, 382, 440])), 1.2)
    nx = (xx - 256) / 146
    st = 0.85 + 0.15 * (np.abs(np.sin((xx - 256) / 24.0)) > 0.1)
    c.over(light(np.sqrt(np.clip(1 - nx ** 2, 0, 1)) * k * 0.8, wood(rng, (0.52, 0.32, 0.15), angle=np.pi / 2, rings=6) * st[..., None], depth=60, spec=0.2), k)
    for y in (130, 270, 410):
        hoop = blur((np.abs(yy - y) < 12).astype(np.float32) * k, 1)
        c.over(chrome(np.sqrt(np.clip(1 - nx ** 2, 0, 1)) * hoop, (0.38, 0.38, 0.40), depth=40, sky=0.7, ground=0.08), hoop)
    top = blur(ellipse([138, 80, 374, 124]), 1)
    c.over(light(0.1 * top, wood(rng, (0.45, 0.27, 0.12), rings=8), depth=20, spec=0.1), top)
    return c.image()


def magnifier(rng):
    c = Canvas()
    lf = blur(poly([(120, 420), (200, 260), (330, 180), (300, 300), (200, 400)]), 1.2)
    c.over(light(0.4 * pillow(lf, 10), np.zeros((N, N, 3)) + np.array([0.25, 0.55, 0.18]), depth=40, spec=0.3), lf)
    vein = blur(poly([(130, 410), (310, 200)], width=4), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.45, 0.70, 0.30]), vein, cast=False)
    _stick(c, rng, (360, 380), (470, 490), w=18, col=(0.40, 0.22, 0.10))
    ring = blur(np.clip(ellipse([170, 90, 400, 320]) - ellipse([192, 112, 378, 298]), 0, 1), 1)
    c.over(chrome(0.5 * pillow(ring, 5), gold_tint(), depth=40), ring)
    glass = blur(ellipse([192, 112, 378, 298]), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.75, 0.88, 0.95]), glass * 0.25, cast=False)
    c.over(np.ones((N, N, 3)), blur(ellipse([220, 140, 270, 190]), 8) * 0.6, cast=False)
    return c.image()


def potion(rng, color=(0.55, 0.15, 0.70)):
    c = Canvas()
    flask = blur(np.maximum(ellipse([110, 200, 402, 480]), rect([210, 90, 302, 260], 10)), 1.2)
    nx = (xx - 256) / 146; ny = (yy - 340) / 140
    liquid = flask * (yy > 270)
    c.over(np.zeros((N, N, 3)) + np.array(color) * (0.6 + 0.6 * np.clip(1 - np.hypot(nx + 0.3, ny + 0.2), 0, 1))[..., None], liquid)
    glassm = np.sqrt(np.clip(1 - nx ** 2 - ny ** 2, 0, 1))
    rimg = (blur(flask, 2) - blur(flask, 10)).clip(0, 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.85, 0.92, 0.95]), np.clip(flask * 0.12 + rimg * 0.7, 0, 1), cast=False)
    c.over(np.ones((N, N, 3)), blur(ellipse([160, 290, 200, 380]), 8) * 0.7, cast=False)
    cork = blur(rect([216, 60, 296, 110], 10), 1)
    c.over(light(0.5 * pillow(cork, 6), np.zeros((N, N, 3)) + np.array([0.60, 0.42, 0.25]), depth=30, spec=0.1), cork)
    glow(c, 256, 380, 130, color, 0.25)
    return c.image()


def anchor(rng):
    c = Canvas()
    tint = (0.40, 0.40, 0.44)
    shank = blur(rect([240, 110, 272, 420], 10), 1)
    stock = blur(rect([150, 140, 362, 168], 10), 1)
    ring = blur(np.clip(ellipse([212, 40, 300, 128]) - ellipse([232, 60, 280, 108]), 0, 1), 1)
    arms = blur(mask_from(lambda d: d.arc([100, 230, 412, 450], 20, 160, fill=255, width=30)), 1)
    flukes = blur(np.maximum(poly([(380, 330), (450, 300), (420, 380)]), poly([(132, 330), (62, 300), (92, 380)])), 1)
    m = np.clip(shank + stock + ring + arms + flukes, 0, 1)
    c.over(chrome(0.45 * pillow(m, 8), tint, depth=50, sky=0.75, ground=0.08), m)
    rope = blur(mask_from(lambda d: d.arc([170, 60, 360, 300], 240, 80, fill=255, width=12)), 1)
    tw = 0.5 + 0.5 * np.sin((xx + yy) / 4.0)
    c.over(light(0.4 * pillow(rope, 4), np.zeros((N, N, 3)) + np.array([0.78, 0.65, 0.42]) * (0.7 + 0.3 * tw[..., None]), depth=20, spec=0.1), rope)
    return c.image()


def storm_sword(rng):
    c = Canvas()
    sword(c, rng, (110, 450), (420, 70), blade_w=28, guard_w=70)
    bolt(c, [(470, 40), (360, 190), (430, 200), (320, 330)], width=18)
    return c.image()


def cogs(rng):
    c = Canvas()
    gear(c, 190, 300, 150, 9, gold_tint())
    gear(c, 360, 170, 110, 8, (0.62, 0.64, 0.68))
    gear(c, 380, 390, 80, 7, (0.80, 0.55, 0.30))
    return c.image()


def druid_staff(rng, orb=None):
    c = Canvas()
    _stick(c, rng, (180, 490), (300, 90), w=22, col=(0.50, 0.32, 0.16))
    top = blur(mask_from(lambda d: d.arc([240, 20, 400, 180], 120, 400, fill=255, width=20)), 1)
    c.over(light(0.5 * pillow(top, 6), wood(rng, (0.40, 0.25, 0.12), rings=4), depth=40, spec=0.2), top)
    if orb:
        glow(c, 320, 100, 90, orb, 0.6)
        o = blur(ellipse([285, 65, 355, 135]), 1)
        c.over(light(pillow(o, 20, 0.7), np.zeros((N, N, 3)) + np.array(orb), depth=50, spec=0.9), o)
    for (x, y, a) in ((250, 220, -0.6), (330, 250, 0.5), (230, 320, -0.4), (300, 170, 0.8)):
        lf = blur(poly([(x, y), (x + 70 * np.cos(a), y - 30 + 50 * np.sin(a)), (x + 40 * np.cos(a), y + 20)]), 1)
        c.over(light(0.4 * pillow(lf, 6), np.zeros((N, N, 3)) + np.array([0.25, 0.55, 0.18]), depth=30, spec=0.3), lf)
    return c.image()


def cauldron(rng):
    c = Canvas()
    pot = blur(ellipse([80, 170, 432, 480]) * (yy > 200), 1.2)
    nx = (xx - 256) / 176; ny = (yy - 325) / 155
    c.over(chrome(np.sqrt(np.clip(1 - nx ** 2 - ny ** 2, 0, 1)) * pot * 0.8, (0.22, 0.22, 0.25), depth=70, sky=0.55, ground=0.05), pot)
    brew = blur(ellipse([100, 190, 412, 240]), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.30, 0.85, 0.35]) * (0.7 + 0.4 * noise(rng, 30, 2))[..., None], brew)
    glow(c, 256, 200, 160, (0.35, 1.0, 0.45), 0.35)
    for (x, y, r) in ((200, 150, 20), (300, 120, 26), (250, 80, 16)):
        b = blur(ellipse([x - r, y - r, x + r, y + r]), 1)
        c.over(light(pillow(b, r * 0.5), np.zeros((N, N, 3)) + np.array([0.45, 0.95, 0.5]), depth=30, spec=0.8), b * 0.85)
    for x in (130, 382):
        leg = blur(poly([(x - 20, 440), (x + 20, 440), (x, 500)]), 1)
        _metal(c, leg, (0.22, 0.22, 0.25), pill=4)
    return c.image()


def paw(rng):
    c = Canvas()
    fur = np.array([0.35, 0.25, 0.18])
    pad = blur(ellipse([150, 250, 362, 450]), 1.5)
    c.over(light(pillow(pad, 40, 0.7), np.zeros((N, N, 3)) + fur * (0.85 + 0.3 * noise(rng, 40, 2))[..., None], depth=50, spec=0.2), pad)
    for (x, y) in ((120, 200), (200, 120), (312, 120), (392, 200)):
        t = blur(ellipse([x - 48, y - 58, x + 48, y + 58]), 1.5)
        c.over(light(pillow(t, 20, 0.7), np.zeros((N, N, 3)) + fur * (0.85 + 0.3 * noise(rng, 40, 2))[..., None], depth=50, spec=0.2), t)
        cl = blur(poly([(x - 14, y - 50), (x + 14, y - 50), (x + 4, y - 105)]), 1)
        c.over(chrome(0.5 * pillow(cl, 5), (0.90, 0.88, 0.82), depth=30, sky=1.0, ground=0.3), cl)
    return c.image()


def catapult(rng):
    c = Canvas()
    for pts in ([(60, 440), (452, 440)], [(80, 470), (430, 470)]):
        _stick(c, rng, pts[0], pts[1], w=14)
    _stick(c, rng, (200, 450), (256, 300), w=14)
    _stick(c, rng, (320, 450), (256, 300), w=14)
    _stick(c, rng, (100, 420), (400, 120), w=14)
    cup = blur(ellipse([360, 70, 470, 150]), 1)
    c.over(light(0.5 * pillow(cup, 10), wood(rng, (0.45, 0.27, 0.12), rings=4), depth=40, spec=0.2), cup)
    rock = blur(ellipse([380, 40, 450, 110]), 1)
    c.over(light(pillow(rock, 18, 0.7), np.zeros((N, N, 3)) + np.array([0.50, 0.48, 0.45]) * (0.8 + 0.3 * noise(rng, 30, 2))[..., None], depth=40, spec=0.1), rock)
    for x in (130, 380):
        rr = np.hypot(xx - x, yy - 455); ang = np.arctan2(yy - 455, xx - x)
        wl = blur(((rr < 48) & ((rr > 36) | (np.abs(np.sin(ang * 3)) < 0.15))).astype(np.float32), 1)
        c.over(light(0.5 * pillow(wl, 5), wood(rng, (0.38, 0.22, 0.10), rings=4), depth=30, spec=0.2), wl)
    return c.image()


def crowned_helm(rng):
    c = Canvas()
    img = load_icon('positions').draw()
    c.px = np.asarray(img.resize((N, N)), np.float32) / 255.0
    cr = blur(poly([(150, 120), (150, 40), (200, 90), (256, 10), (312, 90), (362, 40), (362, 120)]), 1.2)
    c.over(chrome(0.5 * pillow(cr, 8), gold_tint(), depth=40), cr)
    return c.image()


def storm_tower(rng):
    c = Canvas()
    img = load_icon('capital').draw()
    c.px = np.asarray(img, np.float32) / 255.0
    c.px[..., :3] *= np.array([0.75, 0.80, 0.95])
    bolt(c, [(420, 10), (330, 120), (390, 130), (300, 250)], width=20)
    return c.image()


def tree(rng):
    c = Canvas()
    trunk = blur(poly([(220, 480), (292, 480), (280, 300), (330, 230), (290, 240), (256, 200), (222, 240), (182, 230), (232, 300)]), 1.2)
    c.over(light(0.4 * pillow(trunk, 12), wood(rng, (0.40, 0.25, 0.12), angle=np.pi / 2, rings=5), depth=40, spec=0.1), trunk)
    for (x, y, r) in ((256, 150, 120), (150, 210, 90), (362, 210, 90), (200, 110, 80), (312, 110, 80)):
        cl = blur(ellipse([x - r, y - r, x + r, y + r]), 2)
        col = np.zeros((N, N, 3)) + np.array([0.20, 0.48, 0.16]) * (0.75 + 0.45 * noise(rng, 40, 3))[..., None]
        c.over(light(pillow(cl, r * 0.4, 0.7) * 0.8, col, depth=50, spec=0.1), cl)
    glow(c, 256, 160, 160, (0.6, 1.0, 0.5), 0.15)
    return c.image()


def gauntlet(rng):
    c = Canvas()
    cuff = blur(poly([(140, 480), (360, 480), (340, 330), (160, 330)]), 1.2)
    _metal(c, cuff, (0.55, 0.57, 0.62), pill=14)
    hand = blur(rect([150, 170, 360, 340], 40), 1.2)
    _metal(c, hand, (0.62, 0.64, 0.68), pill=20)
    for k in range(4):
        f = blur(rect([160 + k * 50, 60, 200 + k * 50, 200], 18), 1)
        _metal(c, f, (0.66, 0.68, 0.72), pill=10)
    gear(c, 255, 255, 70, 8, gold_tint())
    return c.image()


def storm_staff(rng):
    c = Canvas()
    _stick(c, rng, (160, 490), (300, 160), w=14, col=(0.30, 0.20, 0.30))
    glow(c, 320, 110, 120, (0.4, 0.6, 1.0), 0.6)
    o = blur(ellipse([270, 60, 370, 160]), 1)
    c.over(light(pillow(o, 25, 0.7), np.zeros((N, N, 3)) + np.array([0.45, 0.65, 1.0]), depth=50, spec=0.9), o)
    for pts in ([(370, 90), (440, 60), (470, 120)], [(280, 80), (220, 30), (190, 80)], [(350, 160), (420, 220), (400, 270)]):
        bolt(c, pts, width=10)
    claw = blur(mask_from(lambda d: d.arc([250, 50, 390, 190], 60, 120, fill=255, width=16)), 1)
    c.over(chrome(0.5 * pillow(claw, 4), gold_tint(), depth=30), claw)
    return c.image()


def flame_orb(rng):
    c = Canvas()
    glow(c, 256, 280, 210, (1.0, 0.45, 0.10), 0.7)
    for (r, col) in ((150, (0.95, 0.30, 0.05)), (110, (1.0, 0.55, 0.10)), (70, (1.0, 0.85, 0.35))):
        ang = np.arctan2(yy - 300, xx - 256); d = np.hypot(xx - 256, (yy - 300) * 0.9)
        flick = r * (1 + 0.25 * np.sin(ang * 5 + r) * (yy < 300))
        f = blur(((d < flick) | ((yy < 300) & (np.abs(xx - 256) < r * 0.5) & (yy > 300 - r * 1.8 + np.abs(xx - 256) * 1.5))).astype(np.float32), 4)
        c.over(np.zeros((N, N, 3)) + np.array(col), f, cast=False)
    return c.image()


def rune_tome(rng):
    c = Canvas()
    img = load_icon('roster').draw()
    c.px = np.asarray(img, np.float32) / 255.0
    c.px[..., :3] = c.px[..., :3] * np.array([0.6, 0.9, 1.1])
    glow(c, 245, 250, 120, (0.4, 0.7, 1.0), 0.35)
    return c.image()


def heart(rng, color=(0.75, 0.08, 0.12)):
    c = Canvas()
    u = (xx - 256) / 180; v = -(yy - 290) / 180
    m = blur(((u ** 2 + v ** 2 - 1) ** 3 - u ** 2 * v ** 3 < 0).astype(np.float32), 1.5)
    nx = u; ny = v
    h = np.clip(1 - (u ** 2 + v ** 2), 0, 1) ** 0.4 * m
    c.over(light(h, np.zeros((N, N, 3)) + np.array(color), depth=90, spec=0.6, gloss=40), m)
    glow(c, 256, 290, 200, (1.0, 0.5, 0.5), 0.2)
    return c.image()


def wing(rng):
    c = Canvas()
    for k in range(6):
        a = -0.9 + k * 0.22
        L = 300 - k * 25
        p0 = (140, 380)
        p1 = (140 + L * np.cos(a), 380 + L * np.sin(a))
        s, t = band(p0, p1, 0)
        w = 38 * np.clip(np.sin(np.clip(s, 0, 1) * np.pi), 0, 1) ** 0.6
        f = blur(((s > 0) & (s < 1) & (np.abs(t) < w)).astype(np.float32), 1)
        barbs = 0.85 + 0.15 * np.sin((s * 200 - np.abs(t)) / 2.0)
        c.over(light(0.3 * pillow(f, 6), np.zeros((N, N, 3)) + np.array([0.95, 0.93, 0.88]) * barbs[..., None], depth=30, spec=0.2), f)
    return c.image()


def xp_bottle(rng):
    img = potion(rng, (0.35, 0.90, 0.30))
    c = Canvas(); c.px = np.asarray(img, np.float32) / 255.0
    for (x, y) in ((180, 330), (300, 300), (250, 390), (330, 400)):
        glow(c, x, y, 22, (0.9, 1.0, 0.5), 0.9)
    return c.image()


def enchanted_book(rng):
    c = Canvas()
    img = load_icon('info').draw()
    c.px = np.asarray(img, np.float32) / 255.0
    c.px[..., :3] *= np.array([0.85, 0.75, 1.05])
    glow(c, 256, 260, 220, (0.75, 0.35, 1.0), 0.35)
    for (x, y) in ((140, 120), (380, 140), (300, 80), (200, 60)):
        glow(c, x, y, 16, (0.95, 0.75, 1.0), 1.0)
    return c.image()


def meat(rng):
    c = Canvas()
    m = blur(ellipse([100, 120, 380, 400]), 1.5)
    nx = (xx - 240) / 140; ny = (yy - 260) / 140
    c.over(light(np.sqrt(np.clip(1 - nx ** 2 - ny ** 2, 0, 1)) * m, np.zeros((N, N, 3)) + np.array([0.55, 0.26, 0.12]) * (0.8 + 0.3 * noise(rng, 30, 3))[..., None], depth=70, spec=0.5), m)
    bone = blur(np.maximum(rect([330, 330, 440, 370], 18), np.maximum(ellipse([410, 300, 470, 360]), ellipse([410, 345, 470, 405]))), 1)
    c.over(light(0.5 * pillow(bone, 10), np.zeros((N, N, 3)) + np.array([0.92, 0.88, 0.78]), depth=40, spec=0.3), bone)
    return c.image()


# ===== jobs =====

JOBS = {
    # id: (tier, tool)
    'miner': (1, lambda r: pickaxe(r)), 'lumberjack': (1, lambda r: axe(r)), 'farmer': (1, lambda r: load_icon('mastery').draw()),
    'herbalist': (1, herbs), 'fisher': (1, lambda r: fishing(r)), 'scout': (1, spyglass), 'hunter': (1, lambda r: bow(r)),
    'apprentice_fighter': (1, practice_sword), 'cook': (1, cook_pot), 'merchant': (1, lambda r: load_icon('treasury').draw()),
    'blacksmith': (2, lambda r: hammer_anvil(r)), 'engineer': (2, gear_wrench), 'guard': (2, lambda r: kite_shield(r, (0.62, 0.10, 0.08))),
    'duelist': (2, rapier), 'quartermaster': (2, barrel), 'pathfinder': (2, lambda r: load_icon('travel').draw()),
    'naturalist': (2, magnifier), 'alchemist': (2, lambda r: potion(r)), 'angler': (2, lambda r: fishing(r, hook_only=True)),
    'sea_trader': (2, anchor), 'ranger': (2, lambda r: bow(r, leaf=True)), 'storm_blade': (2, storm_sword),
    'artificer': (3, cogs), 'master_smith': (3, lambda r: hammer_anvil(r, gold=True)), 'knight': (3, lambda r: load_icon('positions').draw()),
    'berserker': (3, lambda r: axe(r, double=True)), 'druid': (3, lambda r: druid_staff(r, orb=(0.35, 0.95, 0.40))), 'alchemy_master': (3, cauldron),
    'tempest_guard': (3, lambda r: kite_shield(r, (0.20, 0.22, 0.35), 'bolt')), 'beast_lord': (3, paw),
    'war_engineer': (4, catapult), 'grand_knight': (4, crowned_helm), 'storm_sentinel': (4, storm_tower),
    'archdruid': (4, tree), 'mech_warlord': (5, gauntlet), 'storm_archmage': (5, storm_staff),
}

TIER_RIM = {1: (0.85, 0.52, 0.28), 2: (0.80, 0.83, 0.88), 3: gold_tint(), 4: gold_tint(), 5: gold_tint()}
TIER_FIELD = {1: (0.40, 0.36, 0.27), 2: (0.28, 0.36, 0.50), 3: (0.50, 0.16, 0.13), 4: (0.36, 0.20, 0.44), 5: (0.16, 0.11, 0.28)}


def medallion(tier, tool_img, scale=0.66):
    c = Canvas()
    cx, cy, R = 256, 266, 236
    disc = blur(ellipse([cx - R, cy - R, cx + R, cy + R]), 1.5)
    rr = np.hypot(xx - cx, yy - cy) / R
    field = np.zeros((N, N, 3)) + np.array(TIER_FIELD[tier])
    field = field * (0.7 + 0.6 * np.clip(1 - np.hypot((xx - cx + 60) / R, (yy - cy + 60) / R), 0, 1))[..., None]
    c.over(light(0.25 * np.clip(1 - rr, 0, 1) ** 0.5 * disc, field, depth=40, spec=0.2), disc)
    rim = np.clip(1 - np.abs(rr - 0.93) / 0.07, 0, 1)
    c.over(chrome(rim * 0.9, TIER_RIM[tier], depth=50), blur((rim > 0.05).astype(np.float32) * disc, 1))
    if tier >= 4:
        for a in (-np.pi / 2, 0, np.pi / 2, np.pi):
            gx, gy = cx + R * 0.93 * np.cos(a), cy + R * 0.93 * np.sin(a)
            g = blur(ellipse([gx - 22, gy - 22, gx + 22, gy + 22]), 1)
            c.over(light(pillow(g, 10, 0.6), np.zeros((N, N, 3)) + np.array([0.75, 0.06, 0.10] if tier == 4 else [0.20, 0.35, 0.95]), depth=40, spec=0.9), g)
    if tier == 5:
        glow(c, cx, cy, R * 0.8, (0.9, 0.7, 1.0), 0.18)
    # fit the tool's own bounding box into the medallion's field
    a = np.asarray(tool_img)[..., 3]
    ys, xs_ = np.nonzero(a > 8)
    tool_img = tool_img.crop((xs_.min(), ys.min(), xs_.max() + 1, ys.max() + 1))
    box = int(R * 2 * 0.70)
    k = box / max(tool_img.size)
    t = tool_img.resize((max(1, int(tool_img.width * k)), max(1, int(tool_img.height * k))), Image.LANCZOS)
    layer = Image.new('RGBA', (N, N)); layer.alpha_composite(t, (int(cx - t.width / 2), int(cy - t.height / 2)))
    lp = np.asarray(layer, np.float32) / 255.0
    c.over(lp[..., :3], lp[..., 3], cast=True)
    if tier == 5:
        cr = blur(poly([(176, 70), (176, 10), (216, 45), (256, -5), (296, 45), (336, 10), (336, 70)]), 1.2)
        c.over(chrome(0.5 * pillow(cr, 8), gold_tint(), depth=40), cr)
    return c.image()


def job(job_id):
    tier, tool = JOBS[job_id]
    return medallion(tier, tool(np.random.default_rng(700 + list(JOBS).index(job_id))))
