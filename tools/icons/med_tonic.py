"""ยาบำรุง: a corked glass flask of deep red tonic."""
import numpy as np
from _clinic import flask


def draw():
    return flask(np.random.default_rng(2505), (0.72, 0.10, 0.12))
