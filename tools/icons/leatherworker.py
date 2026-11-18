"""นายช่างเครื่องหนัง (NPC ขายกระเป๋าเสริม, 2026-11-18): a stretched hide with an awl and a stitched seam."""
import numpy as np
from lib import Canvas, blur, poly, leather_col, cloth, wood, steel_tint, noise
from _bag import part, metal_part


def draw():
    rng = np.random.default_rng(1106)
    c = Canvas()
    hide = blur(poly([(110, 120), (200, 80), (330, 96), (420, 150), (400, 300), (430, 410), (300, 450),
                      (180, 430), (90, 380), (120, 260)]), 3)
    spots = (noise(rng, 50) > 0.6).astype(np.float32)
    part(c, hide, leather_col(rng, (0.62, 0.42, 0.24)) * (1 - 0.15 * spots[..., None]), 0.25, 30, 50, 0.15, 0.4)
    for i in range(9):
        x = 150 + i * 26
        st = blur(poly([(x, 330 - i * 8), (x + 14, 322 - i * 8)], width=5), 1)
        part(c, st, cloth(rng, (0.90, 0.84, 0.66), weave=1.0), 0.2, 2, 20, 0.1, 0.2)
    grip = blur(poly([(330, 150), (420, 60)], width=40), 1.5)
    part(c, grip, wood(rng, (0.58, 0.38, 0.20), angle=0.8), 0.4, 14, 50, 0.3)
    point = blur(poly([(338, 142), (230, 250)], width=10), 1)
    metal_part(c, point, steel_tint(), 0.7, 3)
    return c.image()
