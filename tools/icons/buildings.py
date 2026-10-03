"""อาคารของเมือง: a row of town buildings - a hall with a bell tower between two houses."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, stone, wood, noise, edge_darken


def house(c, rng, x0, x1, ybase, yroof, wall_col, roof_col):
    walls = blur(rect([x0, yroof + 50, x1, ybase]), 1)
    c.over(light(0.15 * pillow(walls, 8), np.array(wall_col)[None, None, :] * (0.85 + 0.2 * noise(rng, 20, 2)[..., None]), depth=30, spec=0.05) * edge_darken(walls, 8, 0.3), walls)
    mx = (x0 + x1) / 2
    roof = blur(poly([(x0 - 14, yroof + 56), (mx, yroof - 20), (x1 + 14, yroof + 56)]), 1)
    tiles = 0.85 + 0.15 * ((yy // 12) % 2)
    c.over(light(0.2 * pillow(roof, 8), np.array(roof_col)[None, None, :] * tiles[..., None], depth=30, spec=0.1) * edge_darken(roof, 6, 0.35), roof)
    for wx in (x0 + 20, x1 - 44):
        win = blur(rect([wx, yroof + 80, wx + 24, yroof + 112], 3), 1)
        c.over(np.zeros((N, N, 3)) + np.array([0.95, 0.75, 0.35]), win)


def draw():
    rng = np.random.default_rng(411)
    c = Canvas()
    house(c, rng, 30, 160, 470, 250, (0.86, 0.80, 0.66), (0.55, 0.20, 0.12))
    house(c, rng, 352, 482, 470, 270, (0.80, 0.72, 0.58), (0.30, 0.32, 0.40))
    tower = blur(rect([196, 90, 316, 470]), 1)
    c.over(light(0.2 * pillow(tower, 10), stone(rng, (0.62, 0.58, 0.52)), depth=30, spec=0.05) * edge_darken(tower, 8, 0.3), tower)
    spire = blur(poly([(184, 100), (256, 10), (328, 100)]), 1)
    c.over(light(0.25 * pillow(spire, 8), np.zeros((N, N, 3)) + np.array([0.28, 0.30, 0.38]), depth=30, spec=0.2), spire)
    arch = blur(np.maximum(rect([226, 130, 286, 200]), ellipse([226, 110, 286, 160])), 1)
    c.over(np.zeros((N, N, 3)) + 0.06, arch)
    bell = blur(np.maximum(ellipse([236, 140, 276, 180]), rect([232, 160, 280, 190], 6)), 1)
    c.over(light(0.5 * pillow(bell, 8), np.zeros((N, N, 3)) + np.array([0.80, 0.60, 0.25]), depth=30, spec=0.6), bell)
    door = blur(np.maximum(rect([226, 380, 286, 470]), ellipse([226, 350, 286, 410])), 1)
    c.over(wood(rng, (0.34, 0.19, 0.09), angle=np.pi / 2, rings=8) * 0.85, door)
    return c.image()
