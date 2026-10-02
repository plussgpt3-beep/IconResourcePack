"""คืนค่า / เวลา: an hourglass in a turned wooden frame, sand running."""
import numpy as np
from lib import N, xx, yy, Canvas, shadow, light, pillow, wood, blur, rect, poly, ellipse, edge_darken, noise, mask_from


def draw():
    rng = np.random.default_rng(81)
    c = Canvas()
    shadow(c, [90, 440, 422, 496], 0.45, 16)
    # glass: two bulbs joined at a narrow waist (profile from a formula)
    dy = (yy - 256) / 170
    half = 20 + 120 * np.clip(np.abs(dy), 0, 1) ** 0.55 * np.clip(1.05 - np.abs(dy) ** 6, 0, 1)
    glass = blur(((np.abs(xx - 256) < half) & (np.abs(dy) < 1.0)).astype(np.float32), 1.5)
    # sand: a heap in the lower bulb, a little left in the upper, a thin stream between
    heap = (yy > 395 - 55 * np.clip(1 - np.abs(xx - 256) / 110, 0, 1) ** 1.5) & (yy < 420)
    top_left = (yy > 215 + 0.004 * (xx - 256) ** 2) & (yy < 250)
    stream = (np.abs(xx - 256) < 3) & (yy > 250) & (yy < 380)
    sand_m = blur(((heap | top_left) * glass > 0.5).astype(np.float32) + stream.astype(np.float32), 1.2).clip(0, 1)
    sand = np.array([0.86, 0.70, 0.42])[None, None, :] * (0.85 + 0.3 * noise(rng, 80, 2)[..., None])
    hs = pillow(sand_m, 10) * 0.4
    c.over(light(hs, sand, depth=40, spec=0.05), sand_m)
    # the glass itself: faint tint, bright rims and glints
    rimg = (blur(glass, 2) - blur(glass, 9)).clip(0, 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.75, 0.85, 0.90]), glass * 0.12 + rimg * 0.6)
    for box in ([170, 120, 190, 220], [170, 300, 190, 390]):
        c.over(np.ones((N, N, 3)), blur(ellipse(box), 5) * 0.6)
    # wooden caps and posts
    col = wood(rng, (0.52, 0.32, 0.17), angle=0.0, rings=10)
    for y0 in (52, 418):
        cap = blur(rect([110, y0, 402, y0 + 44], 14), 1.2)
        c.over(light(pillow(cap, 12, 0.6) * 0.5, col, depth=60, spec=0.3) * edge_darken(cap, 6, 0.3), cap)
    for x0 in (124, 368):
        post = blur(rect([x0, 92, x0 + 22, 420], 10), 1.0)
        bead = 0.15 * (0.5 + 0.5 * np.sin(yy / 14.0))
        c.over(light(pillow(post, 8, 0.6) * (0.5 + bead), wood(rng, (0.48, 0.30, 0.16), angle=np.pi / 2, rings=6), depth=50, spec=0.3), post)
    return c.image()
