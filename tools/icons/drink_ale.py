"""เบียร์: a staved wooden tankard of ale with a head of foam running over the rim."""
import numpy as np
from _tavern import tankard


def draw():
    return tankard(np.random.default_rng(2301))
