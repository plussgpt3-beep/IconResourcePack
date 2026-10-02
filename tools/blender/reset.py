"""คืนค่า / เวลา: an hourglass in a turned walnut frame, sand running through."""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from common import *

scene()
gl = glass('glass')
sand = plain('sand', (0.55, 0.40, 0.18), rough=0.95, bump=0.5, scale=200)
walnut = wood('walnut', (0.28, 0.15, 0.07), (0.10, 0.05, 0.02), axis='Z', scale=10)
def r(z): return 0.06 + 0.52 * math.sin(math.pi * min(abs(z), 0.94) / 0.94) ** 0.85
zs = [-0.94 + 1.88 * k / 80 for k in range(81)]
lathe('glass', [(0.0, -0.94)] + [(r(z), z) for z in zs] + [(0.0, 0.94)], 64, gl)
# sand: a heap in the lower bulb, a little left above the neck, a thin stream
heap = [(0, -0.92)] + [(r(z) * 0.94, z) for z in zs if z < -0.55] + [(r(-0.55) * 0.9, -0.55), (0.0, -0.36)]
lathe('heap', heap, 64, sand)
top = [(0, 0.06)] + [(r(z) * 0.92, z) for z in zs if 0.06 < z < 0.30] + [(0, 0.30)]
lathe('top', top, 64, sand)
bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.44, location=(0, 0, -0.16)); bpy.context.object.data.materials.append(sand)
for z in (-1.02, 1.02):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.78, depth=0.16, vertices=96, location=(0, 0, z)); c = bpy.context.object
    c.data.materials.append(walnut); bevel(c, 0.04, 4, angle=False); bpy.ops.object.shade_smooth()
for k in range(3):
    a = math.pi / 2 + 2 * math.pi * k / 3
    prof = [(0.0, -0.95)] + [(0.055 + 0.018 * math.sin(z * 18) ** 2, z) for z in [-0.95 + 1.9 * j / 40 for j in range(41)]] + [(0.0, 0.95)]
    p = lathe('post', prof, 24, walnut); p.location = (0.64 * math.cos(a), 0.64 * math.sin(a), 0)
render('reset')
