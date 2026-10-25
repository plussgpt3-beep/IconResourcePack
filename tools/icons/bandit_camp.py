"""ซ่องโจร: a ragged bandit tent of patched cloth, a campfire before it, a crude axe stuck in a stump."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, cloth, wood, edge_darken, chrome, steel_tint


def draw():
    rng = np.random.default_rng(709)
    c = Canvas()
    # tent: an A-frame of patched brown cloth with a dark opening
    tent = blur(poly([(60, 400), (250, 70), (440, 400)]), 1.5)
    c.over(light(0.3 * pillow(tent, 20), cloth(rng, (0.48, 0.36, 0.22), weave=2.5), depth=50, spec=0.05) * edge_darken(tent, 12, 0.5), tent)
    patch = blur(rect([300, 250, 360, 310], 4), 1) * tent
    c.over(light(0.2 * pillow(patch, 5), cloth(rng, (0.36, 0.30, 0.20), weave=2.0), depth=30, spec=0.05), patch)
    door = blur(poly([(200, 400), (250, 220), (300, 400)]), 1)
    c.over(light(0.05 * pillow(door, 6), np.stack([0.10 + 0 * xx, 0.07 + 0 * xx, 0.05 + 0 * xx], -1), depth=20, spec=0.0), door)
    pole = blur(poly([(250, 70), (250, 40)], width=8), 1)
    c.over(light(pillow(pole, 3) * 0.5, wood(rng, (0.35, 0.22, 0.10), rings=4), depth=30, spec=0.1), pole)
    # campfire: logs and flames in front
    for (p0, p1) in (((120, 470), (230, 430)), ((120, 430), (230, 470))):
        log = blur(poly([p0, p1], width=20), 1)
        c.over(light(pillow(log, 6) * 0.6, wood(rng, (0.38, 0.22, 0.10), rings=6), depth=40, spec=0.1), log)
    flame = blur(poly([(140, 445), (160, 360), (175, 400), (190, 330), (205, 395), (215, 445)]), 2)
    fire = np.stack([1.0 + 0 * xx, 0.55 + 0.35 * np.clip((yy - 330) / 120.0, 0, 1), 0.10 + 0 * xx], -1)
    c.over(light(0.1 * pillow(flame, 10), np.clip(fire, 0, 1), depth=10, ambient=0.9, spec=0.0), flame)
    # stump with an axe
    stump = blur(rect([360, 400, 450, 480], 10), 1)
    c.over(light(0.2 * pillow(stump, 8), wood(rng, (0.45, 0.30, 0.15), rings=10), depth=40, spec=0.1) * edge_darken(stump, 6, 0.4), stump)
    handle = blur(poly([(395, 410), (450, 300)], width=12), 1)
    c.over(light(pillow(handle, 4) * 0.6, wood(rng, (0.50, 0.33, 0.16), rings=6), depth=30, spec=0.15), handle)
    head = blur(poly([(430, 300), (480, 280), (490, 335), (452, 330)]), 1)
    c.over(chrome(pillow(head, 6) * 0.6, steel_tint(), depth=40, ground=0.15), head)
    return c.image()
