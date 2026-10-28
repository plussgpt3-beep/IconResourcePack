"""นายงาน: a green guild shield with a pickaxe and a builder's hammer crossed."""
import numpy as np
from PIL import Image
from lib import Canvas
from _guild import shield, charge
from _tools import pickaxe
from _smithy import hammer


def draw():
    rng = np.random.default_rng(2801)
    img = shield(rng, 'common').image()
    charge(img, pickaxe(rng).transpose(Image.FLIP_LEFT_RIGHT), 262, 236, 0.80)
    h = Canvas(); hammer(h, rng, (130, 440), (370, 140), head_w=44, head_len=130)
    charge(img, h.image(), 262, 236, 0.80)
    return img
