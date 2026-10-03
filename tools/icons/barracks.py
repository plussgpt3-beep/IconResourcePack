"""ค่ายทหาร: a soldiers' camp - a canvas tent with a dark open flap inside a pointed wooden palisade, a red pennant on its pole."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, wood, cloth, chrome, gold_tint, steel_tint, edge_darken


def draw():
    rng = np.random.default_rng(1201)
    c = Canvas()
    # the palisade behind: sharpened logs in a row
    for k, x in enumerate(range(40, 480, 44)):
        top = 150 + (k % 2) * 18
        log = blur(np.maximum(rect([x, top + 30, x + 38, 470], 6), poly([(x, top + 32), (x + 19, top), (x + 38, top + 32)])), 1.2)
        c.over(light(pillow(log, 12, 0.6) * 0.8, wood(rng, (0.40, 0.25, 0.12), angle=np.pi / 2, rings=5), depth=55, spec=0.15)
               * edge_darken(log, 6, 0.3), log)
    band = blur(rect([30, 250, 482, 268], 4), 1)
    c.over(light(0.3 * pillow(band, 5), wood(rng, (0.28, 0.16, 0.07), rings=4), depth=30, spec=0.1), band)
    # the tent: two canvas faces meeting at a ridge, the near one lit
    left = blur(poly([(256, 120), (90, 470), (256, 470)]), 1.2)
    right = blur(poly([(256, 120), (256, 470), (430, 470)]), 1.2)
    canvas = cloth(rng, (0.86, 0.80, 0.64), weave=2.6)
    sag = 0.12 * np.sin((yy - 120) / 60.0)
    c.over(light(0.25 * pillow(left, 14) + sag * left, canvas, depth=40, spec=0.05) * edge_darken(left, 8, 0.25), left)
    c.over(light(0.25 * pillow(right, 14) + sag * right, canvas * 0.78, depth=40, spec=0.05) * edge_darken(right, 8, 0.25), right)
    # the open flap: a dark doorway with the folded-back canvas
    door = blur(poly([(256, 250), (206, 470), (306, 470)]), 1.2)
    c.over(np.zeros((N, N, 3)) + np.array([0.08, 0.06, 0.05]), door)
    flap = blur(poly([(256, 250), (306, 470), (346, 470), (268, 270)]), 1.2)
    c.over(light(0.3 * pillow(flap, 6), canvas * 0.95, depth=30, spec=0.05), flap)
    seam = blur(poly([(256, 118), (256, 250)], width=6), 1)
    c.over(np.zeros((N, N, 3)) + np.array([0.45, 0.36, 0.24]), seam * 0.8)
    # guy ropes
    for p0, p1 in (((256, 125), (40, 430)), ((256, 125), (472, 430))):
        rope = blur(poly([p0, p1], width=4), 0.8)
        c.over(np.zeros((N, N, 3)) + np.array([0.55, 0.45, 0.30]), rope * 0.9)
    # the pole and its pennant
    pole = blur(rect([250, 24, 262, 130], 4), 1)
    c.over(light(0.5 * pillow(pole, 4), wood(rng, (0.35, 0.20, 0.09), angle=np.pi / 2, rings=3), depth=40, spec=0.2), pole)
    tip = blur(ellipse([246, 12, 266, 32]), 1)
    c.over(chrome(0.6 * pillow(tip, 6), gold_tint(), depth=40), tip)
    wave = 8 * np.sin((xx - 262) / 22.0)
    pen = blur(poly([(262, 30), (400, 52), (262, 88)]) * ((yy - wave) > 0), 1.2)
    pen = blur(np.clip(poly([(262, 30 + 0), (400, 54), (262, 90)]), 0, 1), 1.2)
    c.over(light(0.15 * pillow(pen, 6) + 0.08 * np.sin((xx - 262) / 20.0) * pen, cloth(rng, (0.70, 0.10, 0.08), weave=2.0), depth=30, spec=0.1), pen)
    # crossed spears leaning at the door
    for p0, p1 in (((150, 470), (232, 210)), ((362, 470), (280, 210))):
        shaft = blur(poly([p0, p1], width=9), 1)
        c.over(light(0.4 * pillow(shaft, 4), wood(rng, (0.38, 0.22, 0.10), rings=3), depth=30, spec=0.2), shaft)
        d = np.array(p1, float) - np.array(p0, float); d /= np.linalg.norm(d); n = np.array([-d[1], d[0]])
        tip = np.array(p1, float)
        head = blur(poly([tuple(tip + d * 46), tuple(tip + n * 13), tuple(tip - d * 6), tuple(tip - n * 13)]), 1)
        c.over(chrome(0.7 * pillow(head, 6), steel_tint(), depth=50), head)
    return c.image()
