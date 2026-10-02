"""หน้าถัดไป: a parchment leaf, gently curled, with an ink arrow."""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from common import *

scene()
paper = textured('paper', os.path.join(TEX, 'page_next.png'), rough=0.85, bump=0.08)
pg = grid_sheet('page', 1.5, 1.9, paper, zfun=lambda x, y: 0.10 * (x / 0.75) ** 2 + 0.05 * (y / 0.95) ** 3)
stand([pg], tilt=-14, turn=-14)
render('page_next')
