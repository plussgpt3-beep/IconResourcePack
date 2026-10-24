"""ยาถอนพิษ: a corked glass flask of dark green charcoal-and-kelp antidote."""
import numpy as np
from _clinic import flask


def draw():
    return flask(np.random.default_rng(2504), (0.20, 0.40, 0.14))
