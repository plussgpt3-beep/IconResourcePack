"""หัวหน้างาน: the master builder's tools - an iron set square and a pair of dividers."""
import numpy as np
from lib import N, xx, yy, Canvas, light, pillow, blur, poly, rect, ellipse, chrome, band, gold_tint


def draw():
    c = Canvas()
    sq = blur(np.clip(poly([(70, 120), (130, 120), (130, 400), (430, 400), (430, 460), (70, 460)]), 0, 1), 1)
    marks = np.zeros((N, N), np.float32)
    for k in range(12):
        marks = np.maximum(marks, rect([140 + k * 24, 402, 143 + k * 24, 418]))
        marks = np.maximum(marks, rect([112, 380 - k * 22, 128, 383 - k * 22]))
    c.over(chrome(0.4 * pillow(sq, 6) - 0.15 * marks, (0.62, 0.64, 0.68), depth=40, sky=0.85, ground=0.12), sq)
    # dividers: two legs hinged at a brass head
    hx, hy = 300, 70
    for tip in ((210, 340), (390, 340)):
        s, t = band((hx, hy), tip, 0)
        leg = blur(((s > 0) & (s < 1) & (np.abs(t) < 12 * (1 - s * 0.8))).astype(np.float32), 1)
        c.over(chrome(np.clip(1 - np.abs(t) / 12, 0, 1) ** 0.5 * leg, (0.70, 0.72, 0.76), depth=40, sky=0.9, ground=0.12), leg)
    head = blur(ellipse([hx - 28, hy - 28, hx + 28, hy + 28]), 1)
    c.over(chrome(pillow(head, 12, 0.7), gold_tint(), depth=50), head)
    return c.image()
