"""ท้องพระคลัง: a tied leather coin purse with a stack of gold coins in front."""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from common import *

scene()
hide = leather('hide', (0.12, 0.055, 0.022))
cord = wood('cord', (0.62, 0.50, 0.30), (0.30, 0.22, 0.10), axis='Z', scale=60, rough=0.8)
gold = metal('gold', (0.95, 0.65, 0.20), rough=0.22, var=0.06, bump=0.05)
# body: a lathed sack, then lumpy folds pushed in by noise
prof = [(0, -0.95), (0.55, -0.92), (0.85, -0.70), (0.95, -0.35), (0.88, 0.05), (0.62, 0.35), (0.30, 0.55), (0.24, 0.62)]
bag = lathe('bag', prof, 96, hide)
for v in bag.data.vertices:
    a = math.atan2(v.co.y, v.co.x)
    k = 1 + 0.05 * math.sin(7 * a + v.co.z * 4) + 0.03 * math.sin(13 * a)
    v.co.x *= k; v.co.y *= k
# gathered top flaring out of the tie, its lip waving
fr = lathe('frill', [(0.22, 0.60), (0.30, 0.72), (0.42, 0.86), (0.50, 0.95), (0.47, 0.98), (0.36, 0.86), (0.20, 0.66)], 96, hide)
for v in fr.data.vertices:
    a = math.atan2(v.co.y, v.co.x)
    rr = math.hypot(v.co.x, v.co.y)
    k = 1 + 0.07 * math.sin(10 * a) * max(0, v.co.z - 0.62) / 0.36
    v.co.x *= k; v.co.y *= k; v.co.z += 0.025 * math.sin(10 * a) * max(0, v.co.z - 0.62) / 0.36
bpy.ops.mesh.primitive_torus_add(major_radius=0.27, minor_radius=0.055, major_segments=64, location=(0, 0, 0.62))
bpy.context.object.data.materials.append(cord); bpy.ops.object.shade_smooth()
tube('end', [(0.25, -0.12, 0.60), (0.33, -0.22, 0.40), (0.30, -0.26, 0.18)], 0.04, cord)
# coins: a stack of three and one lying beside, in front on the right
def coin(x, y, z, tilt=0.0):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.42, depth=0.08, vertices=64, location=(x, y, z))
    c = bpy.context.object; c.rotation_euler.x = tilt; c.data.materials.append(gold)
    bevel(c, 0.015, 3, angle=False); bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_torus_add(major_radius=0.34, minor_radius=0.014, major_segments=64, location=(x, y, z + 0.036))
    t = bpy.context.object; t.rotation_euler.x = tilt; t.data.materials.append(gold)
for i in range(3): coin(0.72, -0.70, -0.92 + i * 0.085)
coin(0.05, -1.05, -0.92)
render('treasury')
