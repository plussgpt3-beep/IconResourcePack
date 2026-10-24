"""ล้างค่าซ่อมสะสม: amethyst crystals set on the anvil's face - the stone that takes away a piece's wear of repairs."""
import numpy as np
from lib import Canvas
from _smithy import anvil, amethyst


def draw():
    c = Canvas()
    anvil(c, 256, 330, 0.85)
    amethyst(c, 250, 318, 1.15)
    return c.image()
