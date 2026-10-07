"""การมีส่วนร่วมกับเมือง: a civic merit medal - a gold disc struck with the city's tower and gate,
hung from a blue-and-red ribbon, as a town gives to the citizens who did their part."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, chrome, cloth


def draw():
    rng = np.random.default_rng(1007)
    c = Canvas()
    # the ribbon: two folded tails meeting behind the medal
    for pts, col in (([(120, 30), (230, 30), (290, 270), (215, 290)], (0.16, 0.30, 0.62)),
                     ([(282, 30), (392, 30), (297, 290), (222, 270)], (0.62, 0.10, 0.10))):
        tail = blur(poly(pts), 1.2)
        stripe = cloth(rng, col, weave=2.6)
        # a pale stripe down each tail
        mid = np.array(pts).mean(axis=0)
        pale = blur(poly([((pts[0][0] + pts[1][0]) / 2 - 10, 30), ((pts[0][0] + pts[1][0]) / 2 + 10, 30),
                          (mid[0] + 18, 280), (mid[0] - 2, 280)]), 1) * tail
        stripe = stripe * (1 - pale[..., None]) + pale[..., None] * np.array([0.92, 0.88, 0.78])
        c.over(light(0.25 * pillow(tail, 8), stripe, depth=35, spec=0.08), tail)
    # the ring that holds it
    ring = blur(np.clip(ellipse([232, 232, 280, 280]) - ellipse([244, 244, 268, 268]), 0, 1), 1)
    c.over(chrome(pillow(ring, 6) * 0.6, (1.0, 0.78, 0.34), depth=40), ring)
    # the disc, with a raised rim
    disc = blur(ellipse([106, 254, 406, 500]), 1.2)
    rim = np.clip(disc - blur(ellipse([128, 274, 384, 480]), 1), 0, 1)
    face = disc - rim
    # the city struck in relief: a tower with battlements, an arched gate, two low walls
    tower = rect([216, 300, 296, 440])
    for x in (216, 244, 272):
        tower = np.maximum(tower, rect([x, 288, x + 24, 306]))
    walls = np.maximum(rect([160, 372, 352, 440]), 0)
    for x in (160, 184, 312, 336):
        walls = np.maximum(walls, rect([x, 360, x + 16, 376]))
    gate = np.maximum(rect([240, 400, 272, 440]), ellipse([240, 384, 272, 416]))
    city = blur(np.clip(np.maximum(tower, walls) - gate, 0, 1), 1.5) * face
    h = 0.55 * pillow(disc, 16) + 0.5 * pillow(rim, 6) + 0.6 * pillow(city, 5)
    c.over(chrome(h, (1.0, 0.76, 0.30), depth=70), disc)
    return c.image()
