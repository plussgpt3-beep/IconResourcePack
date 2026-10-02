"""พิมพ์เอง: a goose quill standing in a dark glass inkwell."""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from common import *

scene()
dglass = plain('inkglass', (0.012, 0.016, 0.04), rough=0.06, spec=1.0)
ink = plain('ink', (0.0, 0.0, 0.0), rough=0.02, spec=1.0)
feather = textured('feather', os.path.join(TEX, 'feather.png'), rough=0.7, bump=0.0, alpha=True)
shaft_m = plain('shaft', (0.75, 0.68, 0.52), rough=0.4)
prof = [(0, 0), (0.62, 0), (0.70, 0.08), (0.70, 0.40), (0.55, 0.62), (0.26, 0.70), (0.24, 0.84), (0.29, 0.86),
        (0.29, 0.92), (0.19, 0.92), (0.18, 0.70), (0, 0.68)]
well = lathe('well', prof, 96, dglass); well.location.z = -0.9
bpy.ops.mesh.primitive_cylinder_add(radius=0.185, depth=0.01, vertices=64, location=(0, 0, -0.9 + 0.86))
bpy.context.object.data.materials.append(ink)
# the quill: a textured card (feather) on a shaft, leaning out to the right
q = grid_sheet('vane', 0.8, 1.9, feather, nx=8, ny=30, zfun=lambda x, y: 0.10 * (x / 0.4) ** 2, thickness=0)
q.location = (0.42, 0.0, 0.85); q.rotation_euler = (math.radians(90), math.radians(28), math.radians(8))
# the shaft runs from inside the well up into the vane, along its axis
ax = (math.sin(math.radians(28)), 0, math.cos(math.radians(28)))
tube('shaft', [(-0.03 - ax[0] * 0.2, 0, 0.01 - ax[2] * 0.2), (-0.03 + ax[0] * 0.45, 0, 0.01 + ax[2] * 0.45)], 0.024, shaft_m)
render('type_in')
