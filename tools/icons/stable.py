"""คอกสัตว์ขนของ: a stable's half-door under a little roof, a horseshoe over it, a hay bale in front."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, wood, chrome, edge_darken, noise


def draw():
    rng = np.random.default_rng(2425)
    c = Canvas()
    wall = blur(rect([80, 150, 432, 470], 6), 1.2)
    c.over(light(0.2 * pillow(wall, 10), wood(rng, (0.50, 0.30, 0.14), angle=np.pi / 2, rings=8), depth=30, spec=0.1) * edge_darken(wall, 8, 0.35), wall)
    dark = blur(rect([150, 220, 362, 330], 4), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.08, 0.06, 0.05]), dark, cast=False)
    door = blur(rect([150, 330, 362, 470], 4), 1)
    planks = 0.88 + 0.12 * (np.abs(np.sin((xx - 150) / 17.0)) > 0.1)
    c.over(light(0.3 * pillow(door, 8), wood(rng, (0.60, 0.40, 0.20), angle=np.pi / 2, rings=6) * planks[..., None], depth=40, spec=0.15) * edge_darken(door, 6, 0.4), door)
    brace = blur(np.maximum(poly([(160, 460), (352, 340)], width=16), rect([150, 390, 362, 404])), 1) * door
    c.over(light(0.4 * pillow(brace, 4), wood(rng, (0.45, 0.27, 0.12), rings=4), depth=30, spec=0.15), brace)
    roof = blur(poly([(50, 170), (256, 60), (462, 170), (462, 196), (50, 196)]), 1.2)
    c.over(light(0.3 * pillow(roof, 10), wood(rng, (0.34, 0.18, 0.08), angle=0.5, rings=10), depth=40, spec=0.1) * edge_darken(roof, 8, 0.4), roof)
    rr = np.hypot(xx - 256, yy - 150)
    shoe = blur(((rr > 22) & (rr < 36) & (yy > 132)).astype(np.float32), 1)
    c.over(chrome(0.5 * pillow(shoe, 4), (0.55, 0.55, 0.58), depth=30), shoe)
    hay = blur(rect([300, 380, 470, 470], 10), 1)
    straw = 0.8 + 0.2 * noise(rng, 40, 2)
    c.over(light(0.35 * pillow(hay, 10), np.array([0.85, 0.72, 0.30])[None, None, :] * straw[..., None], depth=40, spec=0.1) * edge_darken(hay, 6, 0.3), hay)
    for y in (402, 448):
        band = blur(rect([300, y, 470, y + 8]), 0.8) * hay
        c.over(np.zeros((N, N, 3)) + np.array([0.45, 0.30, 0.10]), band, cast=False)
    return c.image()
