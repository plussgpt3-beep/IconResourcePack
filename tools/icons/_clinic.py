"""The physician's things (หมอ + โรงหมอ, 2026-10-24): a round glass flask of medicine with a cork, a
rolled linen bandage, a splint of two slats bound with cloth, a stone mortar with its pestle and a
sprig of herbs, a red heart. Painters paint onto a Canvas or return an upright PIL image."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, cloth, stone, noise, edge_darken, chrome


def flask(rng, liquid=(0.85, 0.55, 0.15)):
    """A round-bellied glass flask, three-quarters full of a coloured remedy, a cork in its neck."""
    c = Canvas()
    cx, cy, r = 256, 318, 150
    belly = ellipse([cx - r, cy - r, cx + r, cy + r])
    neck = rect([cx - 46, 70, cx + 46, cy - r + 40], 10)
    glass = blur(np.maximum(belly, neck), 1.2)
    # the remedy inside: the lower part of the belly, with a meniscus
    level = cy - r * 0.25
    inside = blur(ellipse([cx - r + 14, cy - r + 14, cx + r - 14, cy + r - 14]) * (yy > level), 1.2)
    nx = (xx - cx) / r
    shade = np.sqrt(np.clip(1 - nx ** 2, 0, 1))
    liq = np.array(liquid)[None, None, :] * (0.55 + 0.55 * shade[..., None]) * (0.9 + 0.1 * noise(rng, 20, 2)[..., None])
    c.over(light(0.5 * pillow(inside, 30), np.clip(liq, 0, 1), depth=40, spec=0.5, gloss=40), inside)
    # the glass: faint tint over the empty part, bright rim and a glint
    empty = np.clip(glass - inside, 0, 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.80, 0.88, 0.90]), empty * 0.28, cast=False)
    rim = np.clip(glass - blur(np.maximum(ellipse([cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10]), rect([cx - 36, 60, cx + 36, cy - r + 50], 8)), 2), 0, 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.86, 0.94, 0.96]), np.clip(rim * 1.4, 0, 1) * 0.85, cast=False)
    glint = blur(ellipse([cx - r * 0.62, cy - r * 0.55, cx - r * 0.30, cy + r * 0.05]), 6)
    c.over(np.zeros((N, N, 3)) + 1.0, glint * 0.55, cast=False)
    lip = blur(rect([cx - 58, 64, cx + 58, 92], 12), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.84, 0.92, 0.94]), lip * 0.7, cast=False)
    cork = blur(rect([cx - 38, 22, cx + 38, 84], 12), 1.2)
    c.over(light(0.6 * pillow(cork, 10), np.array([0.70, 0.52, 0.32])[None, None, :] * (0.8 + 0.3 * noise(rng, 30, 3)[..., None]),
                 depth=40, spec=0.1), cork)
    return c.image()


def bandage(c, rng, cx=256, cy=250, r=150, tint=(0.94, 0.92, 0.86)):
    """A rolled linen bandage seen from the side: the round roll, its spiral face, a loose tail."""
    tail = blur(poly([(cx + r * 0.2, cy + r * 0.85), (cx + r * 1.55, cy + r * 1.1), (cx + r * 1.5, cy + r * 1.5), (cx - r * 0.1, cy + r * 1.1)]), 1.5)
    lin = cloth(rng, tint, 2.4)
    c.over(light(0.35 * pillow(tail, 8), lin, depth=30, spec=0.1) * edge_darken(tail, 6, 0.25), tail)
    roll = blur(ellipse([cx - r, cy - r, cx + r, cy + r]), 1.2)
    rr = np.hypot(xx - cx, yy - cy) / r
    ang = np.arctan2(yy - cy, xx - cx)
    spiral = 0.5 + 0.5 * np.sin((rr * 9 - ang / np.pi) * np.pi)
    h = 0.55 * pillow(roll, 30) * (0.88 + 0.12 * spiral)
    c.over(light(h, lin * (0.86 + 0.14 * spiral)[..., None], depth=50, spec=0.15), roll)
    core = blur(ellipse([cx - r * 0.22, cy - r * 0.22, cx + r * 0.22, cy + r * 0.22]), 1.5)
    c.over(np.zeros((N, N, 3)) + np.array([0.55, 0.50, 0.42]), core * 0.8, cast=False)


def splint(c, rng):
    """Two wooden slats side by side, bound round with three strips of linen."""
    for x0 in (150, 262):
        slat = blur(rect([x0, 40, x0 + 100, 472], 18), 1.2)
        c.over(light(0.45 * pillow(slat, 14), wood(rng, (0.66, 0.46, 0.24), angle=np.pi / 2, rings=5), depth=50, spec=0.15)
               * edge_darken(slat, 8, 0.3), slat)
    lin = cloth(rng, (0.93, 0.90, 0.84), 2.2)
    for y in (110, 250, 390):
        tie = blur(rect([132, y - 26, 380, y + 26], 14), 1.2)
        folds = 0.85 + 0.15 * np.sin((yy - y) / 6.0)
        c.over(light(0.5 * pillow(tie, 10), lin * folds[..., None], depth=40, spec=0.1) * edge_darken(tie, 6, 0.25), tie)
        knot = blur(ellipse([360, y - 30, 416, y + 30]), 1.2)
        c.over(light(0.6 * pillow(knot, 12), lin, depth=40, spec=0.1), knot)


def leaves(c, rng, cx, cy, s=1.0, color=(0.30, 0.55, 0.20)):
    """A sprig: a stem with five pointed leaves."""
    stem = blur(poly([(cx, cy + 90 * s), (cx + 10 * s, cy), (cx + 30 * s, cy - 90 * s)], width=int(10 * s)), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.28, 0.40, 0.16]), stem)
    for (dx, dy, ang) in ((-40, 50, 0.7), (45, 30, -0.5), (-30, -20, 0.9), (50, -40, -0.6), (25, -100, -0.1)):
        px, py = cx + dx * s, cy + dy * s
        L, W = 70 * s, 26 * s
        a = np.arctan2(dy, dx) if dx else -np.pi / 2
        u = (xx - px) * np.cos(a) + (yy - py) * np.sin(a)
        v = -(xx - px) * np.sin(a) + (yy - py) * np.cos(a)
        leaf = blur(((u > -L * 0.5) & (u < L * 0.5) & (np.abs(v) < W * np.cos(np.clip(u / (L * 0.5), -1, 1) * np.pi / 2))).astype(np.float32), 1.2)
        vein = np.exp(-(v / 2.5) ** 2) * leaf
        col = np.array(color)[None, None, :] * (0.85 + 0.25 * noise(rng, 20, 2)[..., None]) * (1 - 0.25 * vein[..., None])
        c.over(light(0.4 * pillow(leaf, 6), np.clip(col, 0, 1), depth=30, spec=0.2), leaf)


def mortar(c, rng, cx=256, top=250, w=1.0):
    """A stone mortar (a deep bowl on a short foot) with a wooden pestle leaning in it."""
    pestle_p0 = (cx + 150 * w, top - 190 * w)
    pestle_p1 = (cx + 20 * w, top + 40 * w)
    pes = blur(poly([pestle_p0, pestle_p1], width=int(46 * w)), 1.5)
    c.over(light(0.5 * pillow(pes, 10), wood(rng, (0.58, 0.40, 0.22), angle=0.9, rings=4), depth=40, spec=0.2), pes)
    bowl = blur(np.maximum(ellipse([cx - 190 * w, top - 40 * w, cx + 190 * w, top + 230 * w]) * (yy > top),
                           ellipse([cx - 190 * w, top - 40 * w, cx + 190 * w, top + 40 * w])), 1.2)
    foot = blur(rect([cx - 110 * w, top + 200 * w, cx + 110 * w, top + 250 * w], 10), 1.2)
    st = stone(rng, (0.62, 0.60, 0.56))
    c.over(light(0.4 * pillow(foot, 10), st * 0.85, depth=40, spec=0.1), foot)
    c.over(light(0.55 * pillow(bowl, 40), st, depth=60, spec=0.15) * edge_darken(bowl, 10, 0.3), bowl)
    mouth = blur(ellipse([cx - 160 * w, top - 26 * w, cx + 160 * w, top + 26 * w]), 1.2)
    c.over(np.zeros((N, N, 3)) + np.array([0.20, 0.30, 0.12]), mouth * 0.9, cast=False)
    c.over(light(0.5 * pillow(pes * (yy < top), 10), wood(rng, (0.58, 0.40, 0.22), angle=0.9, rings=4), depth=40, spec=0.2), pes * (yy < top))


def heart(c, cx=256, cy=270, s=1.0, color=(0.78, 0.08, 0.10)):
    """A plump red heart."""
    t = np.linspace(0, 2 * np.pi, 200)
    hx = 16 * np.sin(t) ** 3
    hy = -(13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))
    pts = [(cx + x * 12 * s, cy + y * 12 * s) for x, y in zip(hx, hy)]
    m = blur(poly(pts), 1.5)
    c.over(light(0.75 * pillow(m, 50), np.zeros((N, N, 3)) + np.array(color), depth=60, spec=0.55, gloss=30), m)
    return m
