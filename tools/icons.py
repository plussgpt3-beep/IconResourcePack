"""KnightsRealm menu icons, drawn as 16x16 pixel art from character grids.

Each icon is a list of layers (grid, offset). One character = one pixel; '.' is transparent.
Run tools/build.py to turn these into textures and the pack zip.
"""

PALETTE = {
    # leather and outlines
    'k': (43, 26, 14), 'B': (196, 140, 74), 'b': (150, 98, 48), 'd': (102, 63, 28),
    # rope
    'r': (232, 206, 140), 'R': (176, 146, 86),
    # gold
    'O': (92, 62, 4), 'y': (244, 196, 48), 'Y': (255, 244, 160), 'o': (196, 140, 16),
}

_BAG = [
    "................",
    "......kkkk......",
    ".....kBbbdk.....",
    "....kBBbbbdk....",
    ".....kRrrRk.....",
    "....kBbbbbdk....",
    "...kBBbbbbbdk...",
    "..kBBbbbbbbbdk..",
    ".kBBbbbbbbbbbdk.",
    ".kBbbbbbbbbbbdk.",
    ".kBbbbbbbbbbbdk.",
    ".kBbbbbbbbbbbdk.",
    ".kbbbbbbbbbbddk.",
    "..kbbbbbbbbddk..",
    "...kddddddddk...",
    "....kkkkkkkk....",
]

_COIN = [
    "..OOO..",
    ".OYYyO.",
    "OYYyyoO",
    "OYyyyoO",
    "OyyyooO",
    ".OoooO.",
    "..OOO..",
]

# name -> layers; the name is the texture, model and item-model id (knightsrealm:<name>)
ICONS = {
    # ท้องพระคลัง: a coin purse with a gold coin
    'treasury': [(_BAG, (0, 0)), (_COIN, (9, 8))],
}
