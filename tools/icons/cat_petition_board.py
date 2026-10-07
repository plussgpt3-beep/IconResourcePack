"""หมวด "ฎีกา ราษฎร" (ฎีกาของราษฎร): yellow ribbon with the words. Generated from categories.tsv."""
from _category import ribbon

COLOR = 'YELLOW'
TEXT = 'ฎีกา\nราษฎร'


def draw():
    return ribbon(COLOR, 67)
