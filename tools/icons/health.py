"""สุขภาพ: a plump red heart - how the body is doing."""
from lib import Canvas
from _clinic import heart


def draw():
    c = Canvas()
    heart(c, 256, 280, 1.15)
    return c.image()
