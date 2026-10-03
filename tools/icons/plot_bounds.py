"""ดูเขตที่ดิน: a plot of grass marked out by four corner stakes and a cord."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, wood, noise, cloth


def draw():
    rng = np.random.default_rng(304)
    c = Canvas()
    corners = [(70, 330), (256, 230), (442, 330), (256, 440)]   # a diamond: the plot seen at an angle
    turf = blur(poly(corners), 2)
    g = np.array([0.24, 0.45, 0.16])[None, None, :] * (0.75 + 0.45 * noise(rng, 40, 3)[..., None])
    blades = (noise(rng, 90, 1) > 0.6)
    g[blades] *= 1.25
    c.over(light(0.2 * pillow(turf, 20), np.clip(g, 0, 1), depth=30, spec=0.05), turf)
    side = blur(poly([(70, 330), (256, 440), (442, 330), (442, 352), (256, 462), (70, 352)]) * (1 - poly(corners)), 1)
    c.over(np.array([0.32, 0.20, 0.11])[None, None, :] * (0.6 + 0.5 * noise(rng, 30, 2)[..., None]), side)
    # cord joining the stakes
    tops = [(x, y - 120) for x, y in corners]
    for a, b in zip(range(4), [1, 2, 3, 0]):
        sag = ((tops[a][0] + tops[b][0]) / 2, (tops[a][1] + tops[b][1]) / 2 + 18)
        cord = blur(poly([tops[a], sag, tops[b]], width=5), 0.8)
        c.over(np.zeros((N, N, 3)) + np.array([0.85, 0.20, 0.15]), cord)
    for x, y in corners:
        st = blur(poly([(x - 12, y - 130), (x + 12, y - 130), (x + 12, y - 8), (x, y + 10), (x - 12, y - 8)]), 1)
        col = wood(rng, (0.62, 0.45, 0.26), angle=np.pi / 2, rings=4)
        c.over(light(np.clip(1 - np.abs(xx - x) / 12, 0, 1) ** 0.5 * st, col, depth=30, spec=0.2), st)
        flag = blur(poly([(x + 12, y - 128), (x + 46, y - 118), (x + 12, y - 106)]), 0.8)
        c.over(light(0.2 * flag, cloth(rng, (0.80, 0.12, 0.08)), depth=20, spec=0.1), flag)
    return c.image()
