"""แผงค้า: a market stall - a plank counter under a striped awning, wares on top."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, cloth, edge_darken


def draw():
    rng = np.random.default_rng(506)
    c = Canvas()
    for x in (80, 410):
        post = blur(rect([x, 120, x + 22, 470], 6), 1)
        c.over(light(0.4 * pillow(post, 6), wood(rng, (0.45, 0.27, 0.12), angle=np.pi / 2, rings=4), depth=30, spec=0.2), post)
    counter = blur(rect([60, 320, 452, 470], 8), 1)
    planks = sum(np.exp(-((yy - y) / 2.0) ** 2) for y in (370, 420))
    c.over(light(0.2 * pillow(counter, 10) - 0.15 * planks * counter, wood(rng, (0.55, 0.35, 0.18), rings=12), depth=40, spec=0.15) * edge_darken(counter, 10, 0.4), counter)
    for k, (x, col) in enumerate(((140, (0.80, 0.15, 0.10)), (220, (0.85, 0.65, 0.10)), (300, (0.35, 0.60, 0.15)), (370, (0.80, 0.15, 0.10)))):
        for j in range(3):
            fx, fy = x + (j - 1) * 22, 300 - (j % 2) * 18
            fr = blur(ellipse([fx - 20, fy - 20, fx + 20, fy + 20]), 1)
            c.over(light(pillow(fr, 10, 0.6), np.zeros((N, N, 3)) + np.array(col), depth=40, spec=0.5), fr)
    aw = blur(poly([(40, 150), (256, 60), (472, 150), (472, 190), (40, 190)]), 1.2)
    stripes = ((xx // 44) % 2 == 0)
    col = np.where(stripes[..., None], np.array([0.78, 0.12, 0.10]), np.array([0.92, 0.88, 0.80]))
    col = col * (0.85 + 0.2 * np.random.default_rng(1).random((N, N)))[..., None] ** 0
    c.over(light(0.25 * pillow(aw, 10), cloth(rng, (1.0, 1.0, 1.0)) * col, depth=40, spec=0.1) * edge_darken(aw, 6, 0.3), aw)
    scal = np.zeros((N, N), np.float32)
    for k in range(10):
        x = 40 + k * 44 + 22
        scal = np.maximum(scal, ellipse([x - 22, 175, x + 22, 215]) * (yy > 190))
    scal = blur(scal, 1)
    c.over(light(0.3 * pillow(scal, 5), cloth(rng, (1.0, 1.0, 1.0)) * col, depth=30, spec=0.1), scal)
    return c.image()
