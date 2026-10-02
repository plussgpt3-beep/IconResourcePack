"""ปฏิเสธ: a written document torn in two, the halves pulled apart, a red ink stroke across it."""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from common import *

import random
scene()
paper = textured('paper', os.path.join(TEX, 'document.png'), rough=0.85, bump=0.08)
W, H = 1.5, 1.9
rnd = random.Random(4)
tear = []
for k in range(41):   # jagged line from bottom to top
    y = -H / 2 + H * k / 40
    tear.append((0.05 * math.sin(y * 3.2) + rnd.uniform(-0.05, 0.05), y))
box = (-W / 2, -H / 2, W / 2, H / 2)
left = sheet('left', [(-W / 2, -H / 2)] + tear + [(-W / 2, H / 2)], box, paper)
right = sheet('right', [(W / 2, H / 2)] + tear[::-1] + [(W / 2, -H / 2)], box, paper)
left.location = (-0.10, -0.03, 0); left.rotation_euler = (0, 0, math.radians(4))
right.location = (0.10, 0.04, 0.01); right.rotation_euler = (0, 0, math.radians(-5))
stand([left, right], tilt=-14, turn=8)
render('deny')
