"""หมวด "คำร้อง ของฉัน" (คำร้องของฉัน, คำร้องที่รอตรวจ): white ribbon with the words. Generated from categories.tsv."""
from _category import ribbon

COLOR = 'WHITE'
TEXT = 'คำร้อง\nของฉัน'


def draw():
    return ribbon(COLOR, 11)
