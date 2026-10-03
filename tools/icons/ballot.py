"""เสียงประชาชน: a sealed ballot box, a folded vote going in at the slot."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, parchment, blur, poly, rect, wood, edge_darken, chrome, gold_tint


def draw():
    rng = np.random.default_rng(608)
    c = Canvas()
    front = blur(poly([(80, 230), (320, 270), (320, 470), (80, 430)]), 1)
    side = blur(poly([(320, 270), (440, 220), (440, 420), (320, 470)]), 1)
    top = blur(poly([(80, 230), (200, 180), (440, 220), (320, 270)]), 1)
    for m, k, ang in ((front, 1.0, 0.16), (side, 0.72, -0.4), (top, 1.15, 0.2)):
        c.over(light(0.1 * pillow(m, 6), wood(rng, (0.46, 0.26, 0.12), angle=ang, rings=10) * k, depth=30, spec=0.15) * edge_darken(m, 6, 0.35), m)
    slot = blur(poly([(200, 218), (300, 228), (300, 238), (200, 228)]), 0.8)
    c.over(np.zeros((N, N, 3)) + 0.04, slot)
    vote = blur(poly([(215, 80), (300, 95), (295, 230), (210, 220)]), 1)
    col = parchment(rng, (0.95, 0.92, 0.82))
    tick = poly([(232, 140), (250, 165), (282, 115)], width=9)
    col = col * (1 - tick[..., None] * np.array([0.8, 0.4, 0.85]))
    c.over(light(0.1 * vote, col, depth=20, spec=0.05), vote)
    plate = blur(poly([(150, 320), (260, 338), (260, 390), (150, 372)]), 1)
    c.over(chrome(0.4 * pillow(plate, 6), gold_tint(), depth=30), plate)
    return c.image()
