"""ปิดเมนู: an arched plank door, shut, with iron straps and a ring pull."""
import numpy as np
from lib import N, xx, yy, Canvas, shadow, light, pillow, wood, metal, blur, rect, ellipse, edge_darken, mask_from, poly, noise


def draw():
    rng = np.random.default_rng(101)
    c = Canvas()
    shadow(c, [80, 440, 432, 496], 0.45, 16)
    # stone surround
    frame = blur(np.maximum(rect([96, 150, 416, 470]), ellipse([96, 40, 416, 300])), 1.5)
    stone = np.array([0.55, 0.53, 0.50])[None, None, :] * (0.8 + 0.35 * noise(rng, 25, 3))[..., None]
    c.over(light(pillow(frame, 10, 0.5) * 0.4, stone, depth=40, spec=0.1) * edge_darken(frame, 8, 0.35), frame)
    # the door leaf: vertical planks under an arch
    door = blur(np.maximum(rect([126, 160, 386, 462]), ellipse([126, 70, 386, 300])), 1.2)
    col = wood(rng, (0.50, 0.31, 0.16), angle=np.pi / 2, rings=9)
    seams = sum(np.exp(-((xx - x) / 2.2) ** 2) for x in (191, 256, 321))
    h = 0.15 * pillow(door, 6) - 0.25 * seams * door
    c.over(light(h, col, depth=60, spec=0.15) * edge_darken(door, 14, 0.5), door)
    # iron straps with rivets
    iron = metal(rng, (0.25, 0.25, 0.27))
    for y0 in (190, 370):
        strap = blur(rect([126, y0, 386, y0 + 28]) * door, 1)
        c.over(light(pillow(strap, 6) * 0.4, iron, depth=40, spec=0.5), strap)
        for x in range(150, 380, 46):
            rv = ellipse([x - 7, y0 + 7, x + 7, y0 + 21])
            c.over(light(pillow(rv, 4) * 0.6, metal(rng, (0.45, 0.45, 0.48)), depth=30, spec=0.8), rv)
    # ring pull
    ring = mask_from(lambda d: d.ellipse([300, 268, 352, 320], outline=255, width=11))
    ring = blur(ring, 1)
    c.over(light(pillow(ring, 4, 0.8) * 0.8, metal(rng, (0.40, 0.40, 0.42)), depth=30, spec=0.8), ring)
    boss = ellipse([316, 258, 336, 278])
    c.over(light(pillow(boss, 5) * 0.6, iron, depth=30, spec=0.6), boss)
    return c.image()
