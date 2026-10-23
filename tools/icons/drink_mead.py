"""น้ำผึ้งหมัก: a round clay jug of mead, honey glaze running down from the corked lip."""
import numpy as np
from _tavern import jug


def draw():
    return jug(np.random.default_rng(2302))
