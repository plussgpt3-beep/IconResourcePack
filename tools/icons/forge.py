"""โรงตีบวก (นายช่างหลวง, 2026-11-14): a glowing sword hovering over the anvil, golden runes of power
rising off it and a gold plus mark - the smithy's way to raise a weapon past what it was made as."""
import numpy as np
from lib import N, Canvas, sword, blur, poly, chrome, gold_tint
from _smithy import anvil, sparks


def draw():
    rng = np.random.default_rng(1114)
    c = Canvas()
    anvil(c, 256, 330, 0.95)
    sword(c, rng, (150, 330), (360, 40), blade_w=24, guard_w=74)
    sparks(c, rng, 250, 300, n=22, spread=190, color=(1.0, 0.82, 0.30))
    # a gold plus at the upper left
    plus = blur(np.maximum(poly([(88, 64), (88, 164)], width=30), poly([(38, 114), (138, 114)], width=30)), 1.5)
    c.over(chrome(np.clip(plus * 0.8, 0, 1), gold_tint(), depth=40), plus)
    return c.image()
