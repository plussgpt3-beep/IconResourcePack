"""หมูผัดพริกกระเทียม (หม้อปรุงอาหาร เฟส 2, 2026-11-27)."""
import numpy as np
from lib import Canvas
from lib import N, blur, ellipse
from _dishes import plate, chunk, chili_ring, specks, greens


def draw():
    rng = np.random.default_rng(2907)
    c = Canvas()
    plate(c, rng)
    greens(c, rng, 256, 310, 120, (0.30, 0.55, 0.22), 5)
    for (x, y) in ((190, 290), (250, 270), (310, 285), (220, 320), (290, 320), (345, 305), (260, 300)):
        chunk(c, rng, x, y, 30, (0.64, 0.38, 0.22), 'slice')
    sauce = blur(ellipse([150, 250, 370, 350]), 6)
    c.over(np.zeros((N, N, 3)) + np.array([0.40, 0.22, 0.10]), sauce * 0.25, cast=False)
    for (x, y) in ((230, 255), (330, 270), (180, 315), (300, 335), (270, 290)):
        chili_ring(c, rng, x, y, 11)
    specks(c, rng, ellipse([160, 250, 370, 350]), 20, (0.96, 0.88, 0.60), 4, 8)
    return c.image()
