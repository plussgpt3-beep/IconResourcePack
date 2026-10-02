"""ออกจากอาณาจักร: an arched doorway standing open onto bright daylight."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, wood, metal, blur, rect, ellipse, edge_darken, noise, poly


def draw():
    rng = np.random.default_rng(220)
    c = Canvas()
    frame = blur(np.maximum(rect([96, 150, 416, 470]), ellipse([96, 40, 416, 300])), 1.5)
    stone = np.array([0.50, 0.48, 0.45])[None, None, :] * (0.8 + 0.35 * noise(rng, 25, 3))[..., None]
    c.over(light(pillow(frame, 10, 0.5) * 0.4, stone, depth=40, spec=0.1) * edge_darken(frame, 8, 0.35), frame)
    # the opening: sky over a green field and a road leading away
    hole = blur(np.maximum(rect([126, 160, 386, 462]), ellipse([126, 70, 386, 300])), 1.2)
    sky = np.array([0.55, 0.75, 0.95]) * (1 - 0.35 * np.clip((yy - 70) / 300, 0, 1))[..., None] + np.array([0.0, 0.0, 0.0])
    field = (yy > 330 + 10 * np.sin(xx / 40.0))
    scene = np.where(field[..., None], np.array([0.30, 0.55, 0.20]) * (0.8 + 0.3 * noise(rng, 20, 2))[..., None], sky)
    road = (np.abs(xx - 256 - (yy - 462) * -0.15) < (yy - 330) * 0.35) & field
    scene = np.where(road[..., None], np.array([0.70, 0.60, 0.42]), scene)
    sun = blur(ellipse([280, 120, 340, 180]), 6)
    scene = scene + sun[..., None] * 0.5
    c.over(np.clip(scene, 0, 1), hole)
    # the door swung inwards to the left: a narrow slab in perspective
    door = blur(poly([(126, 175), (196, 120), (196, 500), (126, 462)]), 1)
    col = wood(rng, (0.34, 0.19, 0.09), angle=np.pi / 2, rings=9)
    c.over(light(pillow(door, 6) * 0.3, col, depth=40, spec=0.1) * edge_darken(door, 8, 0.5), door)
    return c.image()
