"""ธนาคารหลวง / นายธนาคาร / สถานะธนาคาร: a round strongroom door of steel with a gold wheel, a stack of coins before it."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, chrome, gold_tint, steel_tint, stone, edge_darken, gold_coin


def draw():
    rng = np.random.default_rng(613)
    c = Canvas()
    # the stone wall around the door
    wall = blur(rect([40, 50, 472, 470], 30), 1.5)
    c.over(light(0.15 * pillow(wall, 14), stone(rng, (0.52, 0.50, 0.46)), depth=40, spec=0.1) * edge_darken(wall, 14, 0.5), wall)
    rr = np.hypot(xx - 256, yy - 250)
    door = blur((rr < 180).astype(np.float32), 1.5)
    c.over(chrome(pillow(door, 30) * 0.7, steel_tint(), depth=60, ground=0.2), door)
    rim = blur(((rr < 186) & (rr > 166)).astype(np.float32), 1)
    c.over(chrome(pillow(rim, 6) * 0.8, (0.40, 0.40, 0.44), depth=50, ground=0.15), rim)
    # rivets
    for k in range(12):
        a = k * np.pi / 6
        cx, cy = 256 + 150 * np.cos(a), 250 + 150 * np.sin(a)
        rv = blur((np.hypot(xx - cx, yy - cy) < 9).astype(np.float32), 1)
        c.over(chrome(pillow(rv, 4), (0.55, 0.55, 0.58), depth=40, ground=0.2), rv)
    # the gold wheel: hub and six spokes with knobs
    ang = np.arctan2(yy - 250, xx - 256)
    spokes = ((np.abs(np.sin(ang * 3)) < 9.0 / (rr + 1)) & (rr < 92)).astype(np.float32)
    ring = ((rr < 70) & (rr > 54)).astype(np.float32)
    wheel = blur(np.clip(spokes + ring, 0, 1), 1)
    c.over(chrome(pillow(wheel, 5) * 0.7, gold_tint(), depth=40, ground=0.15), wheel)
    hub = blur((rr < 24).astype(np.float32), 1)
    c.over(chrome(pillow(hub, 10), gold_tint(), depth=40, ground=0.15), hub)
    for k in range(6):
        a = k * np.pi / 3
        cx, cy = 256 + 96 * np.cos(a), 250 + 96 * np.sin(a)
        kn = blur((np.hypot(xx - cx, yy - cy) < 14).astype(np.float32), 1)
        c.over(chrome(pillow(kn, 6), gold_tint(), depth=40, ground=0.15), kn)
    # coins stacked at the lower left
    for i in range(4):
        gold_coin(c, 120, 430 - i * 22, 62, 22, 14)
    return c.image()
