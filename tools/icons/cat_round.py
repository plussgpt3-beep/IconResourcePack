"""หมวด "เลี้ยงรอบ" (เลี้ยงรอบ): yellow ribbon with the words. Generated from categories.tsv."""
from _category import ribbon

COLOR = 'YELLOW'
TEXT = 'เลี้ยง\nรอบ'


def draw():
    return ribbon(COLOR, 88)
