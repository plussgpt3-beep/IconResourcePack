"""หม้อปรุงอาหาร (2026-11-27): the dishes of the cooking pot and its buttons. Painters for a wooden bowl of stew or
soup, a plate, a pie, a loaf, a cake, a fish, chunks and garnish; each dish icon combines them."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, chrome, noise, edge_darken, flat, gold_tint, stone
from _clinic import leaves


def _col(rgb, rng=None, k=0.25, scale=30):
    base = np.zeros((N, N, 3)) + np.array(rgb)
    if rng is None:
        return base
    return np.clip(base * (0.85 + k * noise(rng, scale, 2))[..., None], 0, 1)


def specks(c, rng, area, n, rgb, rmin=3, rmax=7, k=1.0, shade=True, jitter=0.15):
    """n small blobs (flecks of herb, pepper, oil, sugar) scattered inside the mask area."""
    ys, xs = np.nonzero(area > 0.6)
    if len(xs) == 0:
        return
    m = np.zeros((N, N), np.float32)
    cols = np.zeros((N, N, 3), np.float32)
    for _ in range(n):
        i = rng.integers(len(xs)); x, y = xs[i], ys[i]
        r = rng.uniform(rmin, rmax)
        e = ellipse([x - r, y - r * 0.75, x + r, y + r * 0.75])
        m = np.maximum(m, e)
        cols = np.where(e[..., None] > 0, np.clip(np.array(rgb) * rng.uniform(1 - jitter, 1 + jitter), 0, 1), cols)
    m = blur(m, 0.8) * area
    if shade:
        c.over(light(pillow(m, 2, 0.8) * 0.6, cols, depth=20, spec=0.5, gloss=40), m * k, cast=False)
    else:
        c.over(cols, m * k, cast=False)


def oil(c, rng, area, n=14, rgb=(1.0, 0.85, 0.45)):
    """Glossy droplets of fat floating on a broth: a ring of light around each."""
    ys, xs = np.nonzero(area > 0.8)
    if len(xs) == 0:
        return
    for _ in range(n):
        i = rng.integers(len(xs)); x, y = xs[i], ys[i]; r = rng.uniform(5, 13)
        ring = blur(np.clip(ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6]) - ellipse([x - r * 0.6, y - r * 0.35, x + r * 0.6, y + r * 0.35]), 0, 1), 1)
        c.over(np.zeros((N, N, 3)) + np.array(rgb), ring * 0.55 * area, cast=False)
        hl = blur(ellipse([x - r * 0.5, y - r * 0.45, x - r * 0.1, y - r * 0.2]), 0.8)
        c.over(np.ones((N, N, 3)), hl * 0.8 * area, cast=False)


def grain(rng, rgb, scale=6, k=0.35):
    """Fine surface texture (crumb, meat fibre, crust) as an albedo."""
    n1 = noise(rng, scale, 3); n2 = noise(rng, scale * 4, 2)
    return np.clip(np.array(rgb) * (0.75 + k * n1[..., None] + 0.2 * n2[..., None]), 0, 1)


def _dome(cx, cy, rx, ry):
    nx = (xx - cx) / rx; ny = (yy - cy) / ry
    return np.sqrt(np.clip(1 - nx ** 2 - ny ** 2, 0, 1))


def steam(c, xs=(190, 262, 330), y=225, k=0.35):
    """Wisps of steam curling up off the food. Only over what is painted (steam in the empty air would be
    cropped in and outlined dark by build.py)."""
    for i, x in enumerate(xs):
        w = poly([(x, y + 20), (x - 16, y - 8), (x + 8, y - 36), (x - 4, y - 66)], width=18)
        c.over(np.zeros((N, N, 3)) + 0.97, blur(w, 9) * k * 0.8 * c.px[..., 3], cast=False)


def bowl(c, rng, cx=256, top=250, w=1.0, clay=None):
    """A round wooden (or clay) bowl seen a little from above; returns the mask of its opening."""
    rx = 200 * w
    body = blur(ellipse([cx - rx, top - 190 * w, cx + rx, top + 190 * w]) * (yy > top), 1.2)
    foot = blur(rect([cx - 90 * w, top + 165 * w, cx + 90 * w, top + 200 * w], 10), 1.2)
    albedo = (_col(clay, rng, 0.2) if clay is not None else wood(rng, (0.56, 0.35, 0.17), angle=0.15, rings=7))
    c.over(light(0.5 * pillow(foot, 8), albedo * 0.8, depth=30, spec=0.15), foot)
    c.over(light(_dome(cx, top, rx, 190 * w) * body * 0.8, albedo, depth=60, spec=0.25) * edge_darken(body, 8, 0.3), body)
    rim = blur(ellipse([cx - rx, top - 66 * w, cx + rx, top + 66 * w]), 1)
    c.over(light(0.25 * pillow(rim, 6), albedo * 1.08, depth=30, spec=0.25), rim)
    inner = blur(ellipse([cx - rx + 18 * w, top - 50 * w, cx + rx - 18 * w, top + 50 * w]), 1)
    return inner


def broth(c, rng, inner, rgb, gloss=0.5, fat=True):
    alb = grain(rng, rgb, 10, 0.25)
    c.over(light(0.15 * pillow(inner, 10), alb, depth=20, spec=gloss, gloss=40), inner)
    # the bowl's lip throws a shadow on the far side of the broth
    far = blur(inner * (yy < (np.nonzero(inner.max(axis=1) > 0.5)[0].mean())) , 12) * inner
    c.over(np.zeros((N, N, 3)) + np.array(rgb) * 0.35, np.clip(far - 0.35, 0, 1) * 0.9, cast=False)
    if fat:
        oil(c, rng, inner)


def chunk(c, rng, cx, cy, r, rgb, shape='round', k=1.0):
    if shape == 'cube':
        m = blur(poly([(cx - r, cy - r * 0.6), (cx + r * 0.8, cy - r), (cx + r, cy + r * 0.5), (cx - r * 0.6, cy + r)]), 1.2)
    elif shape == 'slice':
        m = blur(ellipse([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45]), 1.2)
    else:
        m = blur(ellipse([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8]), 1.2)
    c.over(light(pillow(m, r * 0.5, 0.7) * k + 0.08 * noise(rng, 5, 2) * m, grain(rng, rgb, 5, 0.4), depth=45, spec=0.35), m)
    sear = blur(np.clip(noise(rng, 9, 2) - 0.55, 0, 1) * 3, 1) * m
    c.over(np.zeros((N, N, 3)) + np.array(rgb) * 0.45, np.clip(sear, 0, 1) * 0.7, cast=False)
    hl = blur(ellipse([cx - r * 0.6, cy - r * 0.6, cx - r * 0.1, cy - r * 0.3]), 2) * m
    c.over(np.ones((N, N, 3)), hl * 0.35, cast=False)


def carrot_coin(c, rng, cx, cy, r=20):
    chunk(c, rng, cx, cy, r, (0.92, 0.45, 0.08), 'slice')
    ring = blur(ellipse([cx - r * 0.45, cy - r * 0.2, cx + r * 0.45, cy + r * 0.2]), 1)
    c.over(np.zeros((N, N, 3)) + np.array([1.0, 0.62, 0.20]), ring * 0.8, cast=False)


def mushroom(c, rng, cx, cy, r=26):
    stem = blur(rect([cx - r * 0.3, cy, cx + r * 0.3, cy + r * 0.9], 6), 1)
    c.over(light(0.4 * pillow(stem, 5), _col((0.90, 0.85, 0.74), rng), depth=20, spec=0.2), stem)
    cap = blur(ellipse([cx - r, cy - r * 0.7, cx + r, cy + r * 0.4]) * (yy < cy + r * 0.2), 1)
    c.over(light(pillow(cap, r * 0.4, 0.7), _col((0.52, 0.34, 0.20), rng), depth=40, spec=0.3), cap)


def plate(c, rng, cx=256, cy=320, r=230, rgb=(0.90, 0.88, 0.82), band=(0.20, 0.36, 0.62)):
    """A glazed earthenware plate seen at a slant, with a painted blue band on its rim."""
    m = blur(ellipse([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55]), 1.2)
    c.over(light(0.2 * pillow(m, 20), grain(rng, rgb, 30, 0.08), depth=30, spec=0.6, gloss=50) * edge_darken(m, 10, 0.25), m)
    ring = blur(np.clip(ellipse([cx - r * 0.9, cy - r * 0.49, cx + r * 0.9, cy + r * 0.49]) - ellipse([cx - r * 0.82, cy - r * 0.44, cx + r * 0.82, cy + r * 0.44]), 0, 1), 1)
    c.over(np.zeros((N, N, 3)) + np.array(band), ring * 0.85, cast=False)
    well = blur(ellipse([cx - r * 0.70, cy - r * 0.37, cx + r * 0.70, cy + r * 0.37]), 8)
    c.over(np.zeros((N, N, 3)) + np.array(rgb) * 0.82, np.clip(well - 0.3, 0, 1) * 0.5, cast=False)
    arc = blur(np.clip(ellipse([cx - r * 0.86, cy - r * 0.52, cx + r * 0.6, cy + r * 0.3]) - ellipse([cx - r * 0.8, cy - r * 0.46, cx + r * 0.66, cy + r * 0.36]), 0, 1), 3) * (xx < cx)
    c.over(np.ones((N, N, 3)), arc * 0.6, cast=False)


def board(c, rng, cx=256, cy=330, w=440, h=230):
    """A wooden serving board with a handle on the right."""
    m = blur(np.maximum(rect([cx - w / 2, cy - h / 2, cx + w / 2 - 40, cy + h / 2], 40),
                        rect([cx + w / 2 - 70, cy - 30, cx + w / 2 + 10, cy + 30], 26)), 1.2)
    c.over(light(0.3 * pillow(m, 14), wood(rng, (0.62, 0.42, 0.22), angle=0.05, rings=9), depth=40, spec=0.2) * edge_darken(m, 10, 0.3), m)


def fish(c, rng, cx, cy, L=300, H=110, rgb=(0.80, 0.55, 0.25), angle=-0.15, grill=True):
    """A whole grilled fish: scaled skin, charred grill bars, fins, gill line and an eye."""
    ca, sa = np.cos(angle), np.sin(angle)
    u = (xx - cx) * ca + (yy - cy) * sa; v = -(xx - cx) * sa + (yy - cy) * ca
    t = u / (L / 2)
    half = H / 2 * np.sqrt(np.clip(1 - t ** 2, 0, 1)) * (1 - 0.35 * np.clip(t, 0, 1))
    body = ((np.abs(t) < 1) & (np.abs(v) < half)).astype(np.float32)
    tail = ((t > 0.82) & (t < 1.28) & (np.abs(v) < (t - 0.82) * H * 1.3)).astype(np.float32) * (1 - 0.6 * (np.abs(v) < (t - 1.0) * H * 0.9) * (t > 1.1))
    dorsal = ((t > -0.35) & (t < 0.45) & (v < -half + 4) & (v > -half - 26 * np.sin(np.clip((t + 0.35) / 0.8, 0, 1) * np.pi))).astype(np.float32)
    fins = blur(np.maximum(tail, dorsal), 1.5)
    rays = 0.75 + 0.25 * np.sin(u / 5.0)
    c.over(light(0.3 * pillow(fins, 6), grain(rng, np.array(rgb) * 0.8, 8, 0.3) * rays[..., None], depth=30, spec=0.3), fins)
    m = blur(body, 1.5)
    belly = np.clip((v + half * 0.2) / (half + 1e-3), 0, 1)[..., None]
    alb = grain(rng, rgb, 6, 0.3) * (1 - 0.25 * belly) + np.array([0.98, 0.88, 0.62]) * 0.25 * belly
    scales = 0.9 + 0.1 * np.sign(np.sin(u / 7.0 + np.sin(v / 7.0) * 1.5))
    c.over(light(pillow(m, 18, 0.7), np.clip(alb * scales[..., None], 0, 1), depth=50, spec=0.55, gloss=35), m)
    if grill:
        marks = ((np.sin((u + v * 0.7) / 13.0) > 0.88) * body).astype(np.float32)
        c.over(np.zeros((N, N, 3)) + np.array([0.18, 0.08, 0.03]), blur(marks, 1.2) * 0.85, cast=False)
        char = blur(np.clip(noise(rng, 10, 2) - 0.6, 0, 1) * 3, 1) * m
        c.over(np.zeros((N, N, 3)) + np.array([0.25, 0.12, 0.04]), np.clip(char, 0, 1) * 0.6, cast=False)
    gill = blur(((np.abs(t + 0.55 - 0.08 * (v / H) ** 2 * 4) < 0.018) * body).astype(np.float32), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.30, 0.15, 0.05]), gill * 0.9, cast=False)
    ex, ey = cx - L * 0.4 * ca + 10 * sa, cy - L * 0.4 * sa - 10 * ca
    eye = blur(ellipse([ex - 11, ey - 11, ex + 11, ey + 11]), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.92, 0.88, 0.75]), eye, cast=False)
    pup = blur(ellipse([ex - 6, ey - 6, ex + 6, ey + 6]), 1)
    c.over(np.zeros((N, N, 3)) + 0.05, pup, cast=False)
    c.over(np.ones((N, N, 3)), blur(ellipse([ex - 4, ey - 5, ex, ey - 1]), 0.6), cast=False)


def roast(c, rng, cx, cy, rx=150, ry=110, rgb=(0.55, 0.26, 0.12), bone=True):
    """A roast joint with crackling, a glossy glaze and dark caramelised edges."""
    m = blur(ellipse([cx - rx, cy - ry, cx + rx, cy + ry]), 1.5)
    h = _dome(cx, cy, rx, ry) * m + 0.06 * noise(rng, 7, 3) * m
    crack = 0.85 + 0.3 * np.clip(noise(rng, 6, 3), 0, 1)
    c.over(light(h, np.clip(grain(rng, rgb, 5, 0.45) * crack[..., None], 0, 1), depth=80, spec=0.7, gloss=45), m)
    c.over(np.zeros((N, N, 3)) + np.array(rgb) * 0.4, np.clip(1 - _dome(cx, cy, rx, ry) * 2.2, 0, 1) * m * 0.6, cast=False)
    if bone:
        b = blur(np.maximum(rect([cx + rx - 40, cy + 10, cx + rx + 60, cy + 44], 16),
                            np.maximum(ellipse([cx + rx + 40, cy - 14, cx + rx + 92, cy + 34]), ellipse([cx + rx + 40, cy + 22, cx + rx + 92, cy + 70]))), 1)
        c.over(light(0.5 * pillow(b, 10), grain(rng, (0.93, 0.89, 0.79), 20, 0.1), depth=40, spec=0.3), b)


def apple(c, rng, cx, cy, r=60, half=False):
    m = blur(ellipse([cx - r, cy - r * 0.9, cx + r, cy + r * 0.9]), 1.2)
    c.over(light(_dome(cx, cy, r, r * 0.9) * m, _col((0.78, 0.10, 0.08), rng, 0.2), depth=60, spec=0.6, gloss=40), m)
    if half:
        f = blur(ellipse([cx - r * 0.8, cy - r * 0.7, cx + r * 0.8, cy + r * 0.7]), 1)
        c.over(light(0.2 * pillow(f, 10), _col((0.98, 0.92, 0.70), rng, 0.1), depth=20, spec=0.2), f)
        for dx in (-10, 10):
            s = blur(ellipse([cx + dx - 5, cy - 9, cx + dx + 5, cy + 9]), 1)
            c.over(np.zeros((N, N, 3)) + np.array([0.30, 0.16, 0.06]), s, cast=False)
    stem = blur(poly([(cx, cy - r * 0.8), (cx + 8, cy - r * 1.2)], width=8), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.35, 0.22, 0.10]), stem)


def loaf(c, rng, cx=256, cy=290, rx=200, ry=120, rgb=(0.80, 0.52, 0.22)):
    """A crusty loaf: browned top, paler sides, scored cuts showing crumb, a dusting of flour."""
    m = blur(ellipse([cx - rx, cy - ry, cx + rx, cy + ry]) * (yy < cy + ry * 0.55), 1.5)
    top = np.clip((cy - yy) / ry + 0.6, 0, 1)[..., None]
    alb = grain(rng, rgb, 5, 0.35) * (0.8 + 0.25 * top) * np.array([1.0, 0.95, 0.9])
    c.over(light(_dome(cx, cy, rx, ry) * m + 0.04 * noise(rng, 5, 3) * m, np.clip(alb, 0, 1), depth=70, spec=0.4), m)
    for dx in (-0.45, 0.0, 0.45):
        x = cx + dx * rx
        cut = blur(poly([(x - rx * 0.17, cy - ry * 0.52), (x + rx * 0.17, cy - ry * 0.78)], width=int(ry * 0.13)), 1.5) * m
        c.over(light(0.3 * pillow(cut, 3), grain(rng, (0.98, 0.88, 0.62), 4, 0.3), depth=20, spec=0.1), cut * 0.95)
        lip = blur(poly([(x - rx * 0.17, cy - ry * 0.45), (x + rx * 0.17, cy - ry * 0.71)], width=5), 1.5) * m
        c.over(np.zeros((N, N, 3)) + np.array(rgb) * 0.45, lip * 0.7, cast=False)
    specks(c, rng, m * (yy < cy - ry * 0.2), 40, (0.98, 0.96, 0.90), 1.5, 3.5, k=0.7, shade=False)


def drizzle(c, rng, cx, cy, w, color=(0.95, 0.66, 0.10), drips=((-60, 70), (10, 95), (70, 60))):
    run = blur(poly([(cx - w / 2, cy), (cx - w / 4, cy - 18), (cx + w / 4, cy + 6), (cx + w / 2, cy - 12)], width=26), 2)
    for (dx, L) in drips:
        run = np.maximum(run, np.maximum(rect([cx + dx - 10, cy - 4, cx + dx + 10, cy + L], 10), ellipse([cx + dx - 15, cy + L - 16, cx + dx + 15, cy + L + 12])))
    run = blur(run, 1.5)
    c.over(light(0.5 * pillow(run, 6), _col(color), depth=30, spec=0.8, gloss=60), run)


def pie(c, rng, cx=256, cy=300, r=210, filling=(0.58, 0.06, 0.14)):
    """A berry pie in a clay dish: crimped crust, a woven lattice, glossy berries bubbling through, sugar."""
    dish = blur(ellipse([cx - r, cy - r * 0.5, cx + r, cy + r * 0.62]), 1.2)
    c.over(light(0.3 * pillow(dish, 12), grain(rng, (0.62, 0.30, 0.16), 20, 0.15), depth=40, spec=0.4) * edge_darken(dish, 8, 0.3), dish)
    crust = blur(ellipse([cx - r * 0.95, cy - r * 0.5, cx + r * 0.95, cy + r * 0.45]), 1.2)
    ang = np.arctan2((yy - cy) / 0.5, xx - cx)
    crimp = 0.5 + 0.5 * np.cos(ang * 22)
    c.over(light(0.3 * pillow(crust, 14) + 0.06 * crimp * crust + 0.03 * noise(rng, 4, 2) * crust, grain(rng, (0.84, 0.56, 0.26), 4, 0.4), depth=50, spec=0.08), crust)
    fill = blur(ellipse([cx - r * 0.78, cy - r * 0.38, cx + r * 0.78, cy + r * 0.33]), 1)
    c.over(light(0.2 * pillow(fill, 10), grain(rng, filling, 8, 0.35), depth=30, spec=0.8, gloss=50), fill)
    specks(c, rng, fill, 40, np.array(filling) * 1.4, 6, 11)
    lattice_a = np.zeros((N, N), np.float32); lattice_b = np.zeros((N, N), np.float32)
    for k in range(-3, 4):
        lattice_a = np.maximum(lattice_a, poly([(cx + k * 52 - 60, cy - r * 0.45), (cx + k * 52 + 60, cy + r * 0.42)], width=24))
        lattice_b = np.maximum(lattice_b, poly([(cx + k * 52 + 60, cy - r * 0.45), (cx + k * 52 - 60, cy + r * 0.42)], width=24))
    for lat, col in ((lattice_a, (0.80, 0.54, 0.24)), (lattice_b, (0.94, 0.70, 0.36))):
        lat = blur(lat * fill, 1.2)
        c.over(light(0.45 * pillow(lat, 6) + 0.03 * noise(rng, 4, 2) * lat, grain(rng, col, 4, 0.4), depth=35, spec=0.08), lat, cast=True)
    specks(c, rng, crust, 50, (1.0, 0.98, 0.92), 1, 2, k=0.6, shade=False)


def cake(c, rng, cx=256, base=430, w=300, layers=((0.84, 0.58, 0.28), (0.88, 0.64, 0.32), (0.84, 0.58, 0.28)), glaze=(0.95, 0.66, 0.10)):
    """A layered sponge cake: crumbly layers with cream between, honey glaze running down, berries on top."""
    h = 74
    y = base
    nx = (xx - cx) / (w / 2)
    curve = np.sqrt(np.clip(1 - nx ** 2, 0, 1))
    seams = []
    for i, col in enumerate(layers):
        m = blur(np.maximum(rect([cx - w / 2, y - h, cx + w / 2, y], 6), ellipse([cx - w / 2, y - 26, cx + w / 2, y + 26])), 1.2)
        crumb = grain(rng, col, 2.5, 0.25)
        c.over(light(curve * m * 0.6 + 0.025 * noise(rng, 2.5, 2) * m, crumb, depth=40, spec=0.15) * edge_darken(m, 8, 0.35), m)
        if i:
            seams.append(y)
        y -= h
    for sy in seams:
        band_m = blur(((np.abs(yy - (sy + 18 * curve)) < 9) & (np.abs(nx) < 1)).astype(np.float32), 1.2)
        c.over(light(0.4 * pillow(band_m, 4) + curve * band_m * 0.3, grain(rng, (0.99, 0.95, 0.84), 12, 0.08), depth=25, spec=0.4), band_m)
    top = blur(ellipse([cx - w / 2, y - 30, cx + w / 2, y + 30]), 1)
    c.over(light(0.2 * pillow(top, 10), _col(glaze, rng, 0.1), depth=20, spec=0.9, gloss=60), top)
    drizzle(c, rng, cx, y + 16, w, glaze, drips=((-120, 80), (-60, 130), (0, 70), (55, 115), (115, 90)))
    for (bx, by) in ((cx - 90, y), (cx + 90, y + 4), (cx - 40, y + 14), (cx + 40, y + 12)):
        b = blur(ellipse([bx - 18, by - 16, bx + 18, by + 16]), 1)
        c.over(light(_dome(bx, by, 18, 16) * b, _col((0.70, 0.04, 0.10)), depth=40, spec=0.9, gloss=60), b)
    return y


def crown(c, cx, cy, s=1.0):
    m = blur(poly([(cx - 60 * s, cy + 30 * s), (cx - 60 * s, cy - 20 * s), (cx - 30 * s, cy), (cx, cy - 40 * s), (cx + 30 * s, cy),
                   (cx + 60 * s, cy - 20 * s), (cx + 60 * s, cy + 30 * s)]), 1)
    c.over(chrome(0.5 * pillow(m, 6), gold_tint(), depth=40), m)


def herb_root(c, rng, cx, cy, s=1.0, rgb=(0.86, 0.76, 0.52)):
    """Ginseng: a forked pale root."""
    m = np.zeros((N, N), np.float32)
    for pts in ([(cx, cy - 70 * s), (cx + 6 * s, cy + 20 * s), (cx - 30 * s, cy + 90 * s)], [(cx + 6 * s, cy + 10 * s), (cx + 40 * s, cy + 80 * s)]):
        m = np.maximum(m, poly(pts, width=int(30 * s)))
    m = blur(m, 2)
    c.over(light(0.5 * pillow(m, 8), _col(rgb, rng, 0.25), depth=40, spec=0.3), m)


def glaze_lines(c, cx, cy, rx, ry):
    """Scored, glazed criss-cross lines across a roast."""
    m = np.zeros((N, N), np.float32)
    for k in range(-2, 3):
        m = np.maximum(m, poly([(cx + k * 50 - 40, cy - ry), (cx + k * 50 + 40, cy + ry)], width=8))
    m = blur(m * ellipse([cx - rx * 0.85, cy - ry * 0.8, cx + rx * 0.85, cy + ry * 0.8]), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.30, 0.12, 0.04]), m * 0.7, cast=False)


# ---------- phase 2 dishes (พืชใหม่, 2026-11-27) ----------

def rice_mound(c, rng, cx, cy, rx=130, ry=80, rgb=(0.96, 0.95, 0.90), fried=False):
    """A mound of cooked rice: a dome covered in plump grains (golden and flecked when fried)."""
    m = blur(ellipse([cx - rx, cy - ry, cx + rx, cy + ry * 0.7]), 1.2)
    base = (0.92, 0.78, 0.46) if fried else rgb
    c.over(light(_dome(cx, cy, rx, ry) * m * 0.9, grain(rng, base, 14, 0.15), depth=50, spec=0.25) * edge_darken(m, 8, 0.25), m)
    ys, xs = np.nonzero(m > 0.7)
    g = np.zeros((N, N), np.float32)
    for _ in range(170):
        i = rng.integers(len(xs)); x, y = xs[i], ys[i]
        a = rng.uniform(0, np.pi)
        g = np.maximum(g, blur(poly([(x - 7 * np.cos(a), y - 7 * np.sin(a)), (x + 7 * np.cos(a), y + 7 * np.sin(a))], width=6), 0.8))
    g *= m
    c.over(light(pillow(g, 2, 0.8) * 0.6 + _dome(cx, cy, rx, ry) * 0.5, flat(base) * 1.05, depth=25, spec=0.5, gloss=40), g * 0.9, cast=False)
    return m


def omelette(c, rng, cx, cy, rx=110, ry=60):
    """A puffy Thai-style omelette: smooth golden top risen in soft bubbles, a lacy crisp brown frill round the edge."""
    edge = noise(rng, 14, 2)
    rr = np.hypot((xx - cx) / rx, (yy - cy) / ry)
    m = blur(((rr < 0.86 + 0.16 * edge)).astype(np.float32), 1.5)
    frill = np.clip((rr - 0.62) / 0.3, 0, 1)
    bubbles = np.clip(noise(rng, 5, 2) - 0.45, 0, 1) * 2.2
    alb = np.zeros((N, N, 3)) + np.array([0.99, 0.80, 0.28])
    alb = alb * (0.92 + 0.1 * noise(rng, 30, 1))[..., None]
    browned = np.clip(frill * (0.6 + 0.8 * noise(rng, 22, 2)) + 0.35 * np.clip(bubbles - 0.5, 0, 1), 0, 1)[..., None]
    alb = alb * (1 - browned) + np.array([0.66, 0.38, 0.10]) * browned
    h = pillow(m, 26, 0.6) * 0.7 + 0.22 * blur(bubbles, 6) * (1 - frill) + 0.08 * noise(rng, 40, 1) * frill
    c.over(light(h * m, np.clip(alb, 0, 1), depth=60, spec=0.6, gloss=45) * edge_darken(m, 6, 0.3), m)


def tomato_slice(c, rng, cx, cy, r=42):
    m = blur(ellipse([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55]), 1)
    c.over(light(0.3 * pillow(m, 6), _col((0.85, 0.14, 0.08), rng, 0.15), depth=25, spec=0.6, gloss=40), m)
    f = blur(ellipse([cx - r * 0.82, cy - r * 0.44, cx + r * 0.82, cy + r * 0.44]), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.95, 0.32, 0.20]), f * 0.8, cast=False)
    for a in np.linspace(0, 2 * np.pi, 4, endpoint=False):   # the seed chambers
        x, y = cx + np.cos(a + 0.4) * r * 0.42, cy + np.sin(a + 0.4) * r * 0.22
        s = blur(ellipse([x - r * 0.22, y - r * 0.12, x + r * 0.22, y + r * 0.12]), 1)
        c.over(np.zeros((N, N, 3)) + np.array([0.98, 0.70, 0.30]), s * 0.8, cast=False)


def chili_ring(c, rng, cx, cy, r=12, rgb=(0.85, 0.08, 0.05)):
    m = blur(ellipse([cx - r, cy - r * 0.7, cx + r, cy + r * 0.7]), 0.8)
    c.over(light(0.4 * pillow(m, 3), _col(rgb, rng, 0.1), depth=20, spec=0.7, gloss=40), m)
    h = blur(ellipse([cx - r * 0.5, cy - r * 0.35, cx + r * 0.5, cy + r * 0.35]), 0.8)
    c.over(np.zeros((N, N, 3)) + np.array([0.98, 0.85, 0.55]), h * 0.8, cast=False)


def greens(c, rng, cx, cy, r, rgb=(0.45, 0.70, 0.30), n=6):
    """Torn leafy pieces (cabbage, lettuce, basil) heaped loosely."""
    for _ in range(n):
        x, y = cx + rng.uniform(-r, r), cy + rng.uniform(-r * 0.5, r * 0.5)
        s = rng.uniform(0.5, 0.9) * r * 0.6
        ang = np.sort(rng.uniform(0, 2 * np.pi, 8))
        rad = s * rng.uniform(0.55, 1.1, 8)
        m = blur(poly([(x + np.cos(t) * q, y + np.sin(t) * q * 0.6) for t, q in zip(ang, rad)]), 1.2)
        col = _col(tuple(np.clip(np.array(rgb) * rng.uniform(0.8, 1.2), 0, 1)), rng, 0.25)
        c.over(light(pillow(m, s * 0.4, 0.6) * 0.7, col, depth=35, spec=0.4) * edge_darken(m, 5, 0.3), m)
        v = blur(poly([(x - s * 0.7, y + s * 0.2), (x + s * 0.7, y - s * 0.2)], width=4), 1) * m
        c.over(np.zeros((N, N, 3)) + np.array([0.85, 0.95, 0.70]), v * 0.6, cast=False)


def lemongrass_bits(c, rng, area, n=6):
    ys, xs = np.nonzero(area > 0.8)
    for _ in range(n):
        i = rng.integers(len(xs)); x, y = xs[i], ys[i]
        a = rng.uniform(-0.6, 0.6)
        m = blur(poly([(x - 18 * np.cos(a), y - 18 * np.sin(a)), (x + 18 * np.cos(a), y + 18 * np.sin(a))], width=10), 1) * area
        c.over(light(0.4 * pillow(m, 3), _col((0.80, 0.84, 0.52), rng, 0.2), depth=20, spec=0.4), m)


def shallot_rings(c, rng, area, n=8):
    ys, xs = np.nonzero(area > 0.8)
    for _ in range(n):
        i = rng.integers(len(xs)); x, y = xs[i], ys[i]
        r = rng.uniform(12, 18)
        o = ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6]) - ellipse([x - r * 0.65, y - r * 0.38, x + r * 0.65, y + r * 0.38])
        m = blur(np.clip(o, 0, 1), 0.8) * area
        c.over(light(0.3 * pillow(m, 2), _col((0.86, 0.62, 0.66), rng, 0.15), depth=15, spec=0.6, gloss=40), m)
