"""A blob of sealing wax with a stamped face: shared by confirm / cancel."""
import math
import bpy
from common import *


def seal(color, symbol_paths, seed=0):
    scene()
    w = wax('wax', color)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=96, ring_count=48); blob = bpy.context.object
    for v in blob.data.vertices:
        a = math.atan2(v.co.y, v.co.x)
        k = 1 + 0.05 * math.sin(5 * a + 1.3 + seed) + 0.025 * math.sin(9 * a + 0.4) + 0.012 * math.sin(17 * a)
        v.co.x *= k; v.co.y *= k; v.co.z *= 0.26
    blob.data.materials.append(w); bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_cylinder_add(radius=0.68, depth=0.06, vertices=96, location=(0, 0, 0.235)); face = bpy.context.object
    face.data.materials.append(w); bevel(face, 0.02, 3, angle=False); bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_torus_add(major_radius=0.72, minor_radius=0.045, major_segments=96, location=(0, 0, 0.255))
    rim = bpy.context.object; rim.data.materials.append(w); bpy.ops.object.shade_smooth()
    parts = [blob, face, rim]
    for path in symbol_paths:
        parts.append(tube('sym', [(x, y, 0.27) for x, y in path], 0.075, w))
    stand(parts, tilt=-22, turn=10)
