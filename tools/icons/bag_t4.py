"""กระเป๋าเสริม Tier 4 หีบหลังนักผจญภัย (+36 ช่อง): a wooden back chest bound in iron, shoulder straps and a rolled blanket."""
import numpy as np
from lib import Canvas, blur, rect, wood, cloth, steel_tint
from _bag import part, iron_part, rivets, strap


def draw():
    rng = np.random.default_rng(1104)
    c = Canvas()
    strap(c, rng, (98, 140), (70, 440), 26, (0.34, 0.20, 0.10))
    strap(c, rng, (414, 140), (442, 440), 26, (0.34, 0.20, 0.10))
    roll = blur(rect([110, 54, 402, 124], 34), 1.5)
    part(c, roll, cloth(rng, (0.30, 0.38, 0.26), weave=3.0), 0.35, 26, 50, 0.1)
    box = blur(rect([90, 130, 422, 466], 10), 1.5)
    part(c, box, wood(rng, (0.50, 0.32, 0.18), angle=0.0), 0.25, 12, 60, 0.15)
    lid = blur(rect([82, 120, 430, 212], 14), 1.5)
    part(c, lid, wood(rng, (0.46, 0.29, 0.16), angle=0.0), 0.3, 14, 60, 0.15)
    for y in (166, 300, 430):
        b = blur(rect([86, y - 12, 426, y + 12], 4), 1)
        iron_part(c, b, 0.5, 4)
        rivets(c, [(x, y) for x in range(110, 420, 60)], 6)
    lock = blur(rect([226, 196, 286, 262], 8), 1)
    iron_part(c, lock, 0.6, 5)
    return c.image()
