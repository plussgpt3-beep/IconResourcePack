"""ย้อนกลับ: an arrow carved from oak, curving back over the top, head pointing down-left."""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from common import *

scene()
oak = wood('oak', (0.26, 0.12, 0.045), (0.08, 0.035, 0.012), axis='X', scale=5, rough=0.32)
cx = 0.15
outer = arc(cx, 0, 1.0, 0, math.pi, 48)
inner = arc(cx, 0, 0.62, math.pi, 0, 36)
pts = outer + [(-1.13, 0), (-0.66, -0.66), (-0.19, 0)] + inner
a = extrude('arrow', pts, 0.26, oak, bevel_w=0.05, segs=4)
stand([a], tilt=-12, turn=14)
render('back')
