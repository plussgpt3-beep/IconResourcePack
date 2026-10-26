"""สกินตัวละคร (ไอดีไม่แท้ตั้งสกินได้, 2026-10-26): a dyed tunic on a wooden hanger, a little dye pot beside it."""
import numpy as np
from lib import N, xx, yy, Canvas, shadow, light, pillow, blur, poly, rect, ellipse, wood, cloth, edge_darken, chrome, gold_tint


def draw():
    rng = np.random.default_rng(2610)
    c = Canvas()
    shadow(c, [110, 440, 400, 500], 0.4, 18)
    # hook and hanger bar
    hook = blur(mask_hook(), 1)
    c.over(chrome(0.5 * pillow(hook, 4), gold_tint(), depth=40), hook)
    bar = blur(poly([(118, 150), (256, 96), (394, 150)], width=18), 1)
    c.over(light(0.5 * pillow(bar, 6), wood(rng, (0.45, 0.27, 0.12), rings=5), depth=40, spec=0.25), bar)
    # tunic: shoulders, sleeves, body, a belt
    body = blur(poly([(150, 150), (362, 150), (420, 250), (372, 280), (350, 240), (350, 450), (162, 450), (162, 240), (140, 280), (92, 250)]), 1.5)
    folds = 0.5 + 0.12 * np.sin((xx - 256) / 18.0) * (yy > 260)
    col = cloth(rng, (0.18, 0.36, 0.62))
    c.over(light(pillow(body, 22, 0.5) * folds, col, depth=60, spec=0.15) * edge_darken(body, 10, 0.35), body)
    collar = blur(np.clip(ellipse([212, 128, 300, 196]) - ellipse([226, 136, 286, 182]), 0, 1) * (yy > 150), 1)
    c.over(light(0.4 * pillow(collar, 4), cloth(rng, (0.80, 0.68, 0.30)), depth=30, spec=0.3), collar)
    belt = blur(rect([162, 330, 350, 356], 4), 1)
    c.over(light(0.3 * pillow(belt, 4), np.zeros((N, N, 3)) + np.array([0.32, 0.18, 0.08]), depth=30, spec=0.3), belt)
    buckle = blur(rect([240, 326, 272, 360], 4), 1)
    c.over(chrome(0.5 * pillow(buckle, 3), gold_tint(), depth=30), buckle)
    # hem trim
    hem = blur(rect([162, 432, 350, 452], 2), 1)
    c.over(light(0.3 * pillow(hem, 3), cloth(rng, (0.80, 0.68, 0.30)), depth=30, spec=0.3), hem)
    # dye pot: clay with red dye
    pot = blur(np.maximum(ellipse([360, 380, 470, 490]) * (yy > 410), rect([360, 410, 470, 470], 20)), 1.2)
    c.over(light(pillow(pot, 16), np.zeros((N, N, 3)) + np.array([0.55, 0.32, 0.18]), depth=50, spec=0.25) * edge_darken(pot, 8, 0.3), pot)
    dye = blur(ellipse([368, 396, 462, 424]), 1)
    c.over(light(0.3 * pillow(dye, 6), np.zeros((N, N, 3)) + np.array([0.70, 0.08, 0.10]), depth=20, spec=0.6, gloss=40), dye)
    return c.image()


def mask_hook():
    from lib import mask_from
    return mask_from(lambda d: d.arc([232, 40, 280, 100], 180, 400, fill=255, width=10))
