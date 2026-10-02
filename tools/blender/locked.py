"""ทำไม่ได้ / ล็อก: a cast-iron padlock with a steel shackle and a brass keyhole plate."""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from common import *

scene()
iron = metal('iron', (0.09, 0.09, 0.10), rough=0.45, var=0.15, bump=0.3)
steel = metal('steel', (0.78, 0.79, 0.81), rough=0.18, var=0.06, bump=0.0)
brass = metal('brass', (0.80, 0.50, 0.14), rough=0.30, var=0.08, bump=0.05)
dark = plain('dark', (0.01, 0.01, 0.01), rough=0.9)

bpy.ops.mesh.primitive_cube_add(size=1); body = bpy.context.object
body.scale = (1.5, 0.55, 1.2); bpy.ops.object.transform_apply(scale=True)
bevel(body, 0.18, 6, angle=False); body.data.materials.append(iron); bpy.ops.object.shade_smooth()

pts = [(0.5, 0, 0.35)] + [(0.5 * math.cos(math.pi * i / 40), 0, 0.95 + 0.5 * math.sin(math.pi * i / 40)) for i in range(41)] + [(-0.5, 0, 0.35)]
tube('shackle', pts, 0.13, steel)

bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=0.06, location=(0, -0.3, -0.05), rotation=(math.pi / 2, 0, 0))
esc = bpy.context.object; esc.data.materials.append(brass); bevel(esc, 0.02, 3); bpy.ops.object.shade_smooth()
bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.05, location=(0, -0.335, 0.03), rotation=(math.pi / 2, 0, 0))
bpy.context.object.data.materials.append(dark)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.335, -0.12)); k = bpy.context.object
k.scale = (0.07, 0.05, 0.2); k.data.materials.append(dark)
for x, z in [(-0.6, 0.42), (0.6, 0.42), (-0.6, -0.42), (0.6, -0.42)]:
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06, location=(x, -0.27, z)); r = bpy.context.object
    r.scale = (1, 0.5, 1); r.data.materials.append(steel); bpy.ops.object.shade_smooth()

render('locked')
