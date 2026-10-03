"""ปฏิเสธคำร้อง: a stamp that has just pressed a red cross onto the document."""
from _stamp import stamp


def draw():
    return stamp((0.65, 0.06, 0.05), 'x', 312)
