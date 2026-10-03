"""อนุมัติ: a stamp that has just pressed a green tick onto the document."""
from _stamp import stamp


def draw():
    return stamp((0.10, 0.45, 0.12), 'check', 311)
