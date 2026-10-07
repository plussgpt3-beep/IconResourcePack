"""หมวด "แผง สถานะ" (แผงสถานะ): light gray ribbon with the words. Generated from categories.tsv."""
from _category import ribbon

COLOR = 'LIGHT_GRAY'
TEXT = 'แผง\nสถานะ'


def draw():
    return ribbon(COLOR, 75)
