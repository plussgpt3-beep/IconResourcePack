"""แกงขมิ้นปลาแซลมอน (หม้อปรุงอาหาร, 2026-11-27): a bowl of golden turmeric curry with pink salmon pieces."""
import numpy as np
from lib import Canvas
from _dishes import specks, bowl, broth, chunk, steam


def draw():
    rng = np.random.default_rng(2707)
    c = Canvas()
    inner = bowl(c, rng)
    broth(c, rng, inner, (0.95, 0.66, 0.08), gloss=0.6)
    chunk(c, rng, 180, 245, 32, (0.96, 0.52, 0.42), 'cube')
    chunk(c, rng, 270, 228, 30, (0.96, 0.55, 0.45), 'cube')
    chunk(c, rng, 345, 252, 28, (0.94, 0.50, 0.40), 'cube')
    specks(c, rng, inner, 16, (0.30, 0.58, 0.22), 2, 5)
    steam(c)
    return c.image()
