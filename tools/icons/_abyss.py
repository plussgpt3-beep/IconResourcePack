"""แดนอเวจี (แดนนอก เขต 5, 2026-11-20): the raw drops and goods of the outermost zone - black-violet shell and plate,
a demon's horn and the blade cut from it - plus the fifth grade of the element stones, ดวงใจ: a heart-cut stone glowing in a
cage of obsidian claws."""
import numpy as np
from lib import N, xx, yy, light, pillow, blur, poly, ellipse, rect, chrome, noise, stone, steel_tint, leather_col
from _wild import fang

ABYSS = (0.20, 0.10, 0.26)        # black-violet chitin
EMBER = (0.95, 0.35, 0.95)        # the violet glow in the cracks
HORN = (0.24, 0.10, 0.10)


def glow(c, mask, colour, a=0.8, r=6):
    c.over(np.zeros((N, N, 3)) + np.array(colour), blur(mask, r) * a, cast=False)


def shell(c, rng):
    """A curved slab of dark chitin with ridges, violet light seeping from the cracks."""
    out = blur(poly([(110, 330), (150, 170), (256, 105), (362, 170), (402, 330), (330, 410), (182, 410)]), 2)
    tex = (np.zeros((N, N, 3)) + np.array(ABYSS)) * (0.8 + 0.4 * noise(rng, 30, 3)[..., None])
    c.over(light(0.75 * pillow(out, 60), np.clip(tex, 0, 1), depth=80, spec=0.7, gloss=55), out)
    for k in range(4):
        y = 170 + k * 55
        ridge = blur(poly([(160 + k * 6, y + 40), (256, y), (352 - k * 6, y + 40)], width=7), 1.2) * out
        c.over(light(0.4 * pillow(ridge, 5), np.zeros((N, N, 3)) + np.array(ABYSS) * 1.8, depth=40, spec=0.9), ridge)
    cracks = np.zeros((N, N), np.float32)
    for pts in ([(200, 150), (230, 230), (210, 300), (240, 370)], [(320, 180), (300, 260), (330, 340)], [(256, 120), (262, 200)]):
        cracks = np.maximum(cracks, poly(pts, width=4))
    cracks = blur(cracks, 1) * out
    glow(c, cracks, EMBER, 0.9, 5)
    c.over(np.zeros((N, N, 3)) + 1.0, cracks * 0.55, cast=False)


def plate(c, rng):
    """The worked shell: a riveted black-violet armour plate with a glowing rune."""
    m = blur(rect([118, 118, 394, 394], 34), 2)
    c.over(chrome(0.6 * pillow(m, 34), np.array([0.30, 0.20, 0.36]), depth=70, ground=0.12), m)
    inner = blur(rect([150, 150, 362, 362], 24), 2)
    tex = (np.zeros((N, N, 3)) + np.array(ABYSS)) * (0.85 + 0.3 * noise(rng, 26, 3)[..., None])
    c.over(light(0.5 * pillow(inner, 20), np.clip(tex, 0, 1), depth=60, spec=0.8, gloss=60), inner)
    rune = np.zeros((N, N), np.float32)
    for pts in ([(256, 190), (256, 322)], [(206, 230), (306, 282)], [(306, 230), (206, 282)]):
        rune = np.maximum(rune, poly(pts, width=8))
    rune = np.maximum(rune, np.clip(1 - np.abs(np.hypot(xx - 256, yy - 256) / 70.0 - 1) * 18, 0, 1))
    rune = blur(rune, 1.2) * inner
    glow(c, rune, EMBER, 0.85, 7)
    c.over(np.zeros((N, N, 3)) + np.array([1.0, 0.85, 1.0]), rune * 0.7, cast=False)
    for (x, y) in ((140, 140), (372, 140), (140, 372), (372, 372)):
        r = blur(ellipse([x - 13, y - 13, x + 13, y + 13]), 1)
        c.over(chrome(0.6 * pillow(r, 4), steel_tint(), depth=40), r)


def horn(c, rng):
    """A great curved demon horn, ridged, the tip burning violet."""
    t = np.linspace(0, 1, 40)
    # centre line: a quadratic curve from the root (bottom left) sweeping up and over to the tip (top right)
    p0, p1, p2 = np.array([150.0, 420.0]), np.array([120.0, 140.0]), np.array([390.0, 110.0])
    cl = ((1 - t) ** 2)[:, None] * p0 + (2 * (1 - t) * t)[:, None] * p1 + (t ** 2)[:, None] * p2
    tan = np.gradient(cl, axis=0); tan /= np.linalg.norm(tan, axis=1)[:, None]
    nrm = np.stack([-tan[:, 1], tan[:, 0]], axis=1)
    w = 58 * (1 - t) ** 0.9 + 4
    left = cl + nrm * w[:, None]; right = cl - nrm * w[:, None]
    m = blur(poly([tuple(p) for p in left] + [tuple(p) for p in right[::-1]]), 1.5)
    tex = (np.zeros((N, N, 3)) + np.array(HORN)) * (0.75 + 0.45 * noise(rng, 22, 3)[..., None])
    c.over(light(0.6 * pillow(m, 24), np.clip(tex, 0, 1), depth=75, spec=0.55, gloss=40), m)
    for i in range(3, 34, 4):
        ring = blur(poly([tuple(left[i]), tuple(right[i])], width=5), 1) * m
        c.over(np.zeros((N, N, 3)) + np.array(HORN) * 0.4, ring * 0.85)
    hi = blur(poly([tuple(p) for p in (cl + nrm * (w * 0.45)[:, None])[2:30]], width=6), 3) * m
    c.over(np.zeros((N, N, 3)) + np.array([0.6, 0.35, 0.35]), hi * 0.45, cast=False)
    tx, ty = cl[-1]
    glow(c, blur(ellipse([tx - 30, ty - 30, tx + 30, ty + 30]), 4), EMBER, 0.85, 14)
    rx, ry = cl[0]
    base = blur(ellipse([rx - 66, ry - 26, rx + 66, ry + 30]), 2)
    c.over(light(0.4 * pillow(base, 10), stone(rng, (0.22, 0.18, 0.20)), depth=40, spec=0.2), base)


def edge(c, rng):
    """A long blade ground from demon horn: black-violet with a burning violet edge, horn grip."""
    m = blur(poly([(110, 404), (150, 352), (384, 92), (430, 76), (414, 122), (190, 398)]), 1.2)
    c.over(chrome(0.75 * pillow(m, 9), np.array([0.32, 0.22, 0.40]), depth=65, ground=0.10), m)
    e = blur(poly([(148, 372), (392, 104)], width=6), 2)
    glow(c, e, EMBER, 0.95, 6)
    c.over(np.zeros((N, N, 3)) + np.array([1.0, 0.9, 1.0]), blur(poly([(160, 360), (392, 104)], width=2), 1) * 0.8, cast=False)
    guard = blur(poly([(120, 340), (200, 420)], width=20), 1)
    c.over(chrome(0.6 * pillow(guard, 6), np.array([0.28, 0.16, 0.30]), depth=50), guard)
    grip = blur(poly([(86, 446), (140, 392)], width=26), 1)
    c.over(light(0.5 * pillow(grip, 8), leather_col(rng, HORN), depth=40, spec=0.2), grip)


def heart(c, el, rng, col, glow_col):
    """ดวงใจ (grade 5): a heart-cut stone held by four obsidian claws, its light spilling out."""
    t = np.linspace(0, 2 * np.pi, 80)
    hx = 16 * np.sin(t) ** 3
    hy = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
    pts = [(256 + 9.5 * x, 236 - 9.5 * y) for x, y in zip(hx, hy)]
    m = blur(poly(pts), 1.6)
    d = np.hypot(xx - 225, yy - 200) / 170.0
    cc = (np.zeros((N, N, 3)) + np.array(col)) * (1.25 - 0.7 * np.clip(d, 0, 1))[..., None]
    c.over(light(0.8 * pillow(m, 55), np.clip(cc, 0, 1), depth=85, spec=1.0, gloss=70), m)
    for pts2 in ([(256, 150), (200, 205), (256, 330)], [(256, 150), (312, 205), (256, 330)]):
        f = blur(poly(pts2), 1.2) * m
        c.over(np.zeros((N, N, 3)) + np.array(col) * 1.35, f * 0.35, cast=False)
    glow(c, blur(ellipse([196, 170, 316, 300]), 2), glow_col, 0.7, 22)
    claw = stone(rng, (0.10, 0.07, 0.14))
    for cp in ([(112, 250), (150, 214), (170, 236), (128, 300)], [(400, 250), (362, 214), (342, 236), (384, 300)],
               [(176, 404), (204, 340), (228, 366), (210, 424)], [(336, 404), (308, 340), (284, 366), (302, 424)]):
        k = blur(poly(cp), 1.2)
        c.over(light(0.55 * pillow(k, 10), claw, depth=60, spec=0.7, gloss=60), k)
    base = blur(ellipse([176, 400, 336, 452]), 2)
    c.over(light(0.5 * pillow(base, 14), claw, depth=55, spec=0.6, gloss=50), base)
    for (x, y) in ((214, 196), (300, 210)):
        glow(c, blur(ellipse([x - 9, y - 9, x + 9, y + 9]), 1), (1, 1, 1), 0.9, 3)
