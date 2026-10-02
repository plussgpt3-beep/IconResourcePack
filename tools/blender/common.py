"""Shared Blender scene for the KnightsRealm icons (style B: modelled in 3D, rendered with Cycles).

Every icon script calls scene(), builds its objects with the helpers here, then render(id).
One camera and one light rig for the whole set: key light from the upper left (as all icons),
a cool fill from the right and a strong rim light from behind so silhouettes separate from the
menu's grey. Renders are 640x640 RGBA with a transparent background, no ground shadow; build.py
crops, darkens, sharpens and outlines them down to 64x64.
"""
import math, os
import bpy, bmesh
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'renders')
TEX = os.path.join(HERE, 'tex')


def scene(samples=72):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.cycles.seed = 1
    sc.render.resolution_x = sc.render.resolution_y = 640
    sc.render.film_transparent = True
    sc.view_settings.view_transform = 'Filmic'
    sc.view_settings.look = 'High Contrast'
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = (0.30, 0.31, 0.34, 1)
    bg.inputs['Strength'].default_value = 0.22
    area((-3.0, -3.5, 5.0), 750, 2.5)                       # key, upper left
    area((4.5, -3.0, 0.8), 110, 4.0, (0.80, 0.88, 1.0))     # fill, right
    area((2.5, 4.5, 4.5), 650, 2.0, (1.0, 0.95, 0.85))      # rim, behind
    cam = bpy.data.cameras.new('cam'); cam.type = 'ORTHO'; cam.ortho_scale = 3.6
    co = bpy.data.objects.new('cam', cam); bpy.context.collection.objects.link(co); sc.camera = co
    co.location = Vector((1.2, -5.5, 2.0))
    co.rotation_euler = (Vector((0, 0, 0)) - co.location).to_track_quat('-Z', 'Y').to_euler()
    return sc


def area(loc, energy, size, color=(1, 1, 1)):
    l = bpy.data.lights.new('l', 'AREA'); l.energy = energy; l.size = size; l.color = color
    o = bpy.data.objects.new('l', l); o.location = loc; bpy.context.collection.objects.link(o)
    o.rotation_euler = (Vector((0, 0, 0)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()


def render(name):
    os.makedirs(OUT, exist_ok=True)
    bpy.context.scene.render.filepath = os.path.join(OUT, name + '.png')
    bpy.ops.render.render(write_still=True)


# ===== materials =====

def _nodes(m):
    m.use_nodes = True
    return m.node_tree, m.node_tree.nodes['Principled BSDF']


def _noise(nt, scale, detail=8, coords='Object'):
    tc = nt.nodes.new('ShaderNodeTexCoord')
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = scale; nz.inputs['Detail'].default_value = detail
    nt.links.new(tc.outputs[coords], nz.inputs['Vector'])
    return nz


def _bump(nt, b, height_out, strength, distance=0.02):
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = strength; bp.inputs['Distance'].default_value = distance
    nt.links.new(height_out, bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return bp


def _rough_from(nt, b, fac_out, lo, hi):
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = lo; mr.inputs['To Max'].default_value = hi
    nt.links.new(fac_out, mr.inputs['Value']); nt.links.new(mr.outputs['Result'], b.inputs['Roughness'])


def metal(name, color, rough=0.3, var=0.1, bump=0.15, scale=40):
    m = bpy.data.materials.new(name); nt, b = _nodes(m)
    b.inputs['Base Color'].default_value = (*color, 1); b.inputs['Metallic'].default_value = 1.0
    nz = _noise(nt, scale)
    _rough_from(nt, b, nz.outputs['Fac'], rough - var, rough + var)
    if bump: _bump(nt, b, nz.outputs['Fac'], bump)
    return m


def plain(name, color, rough=0.5, spec=0.5, bump=0.0, scale=30):
    m = bpy.data.materials.new(name); nt, b = _nodes(m)
    b.inputs['Base Color'].default_value = (*color, 1); b.inputs['Roughness'].default_value = rough
    b.inputs['Specular IOR Level'].default_value = spec
    if bump:
        nz = _noise(nt, scale); _bump(nt, b, nz.outputs['Fac'], bump)
    return m


def wax(name, color):
    m = bpy.data.materials.new(name); nt, b = _nodes(m)
    b.inputs['Base Color'].default_value = (*color, 1)
    b.inputs['Roughness'].default_value = 0.33
    b.inputs['Subsurface Weight'].default_value = 0.06
    b.inputs['Subsurface Radius'].default_value = (0.3, 0.08, 0.05)
    b.inputs['Subsurface Scale'].default_value = 0.05
    nz = _noise(nt, 12, 6); _bump(nt, b, nz.outputs['Fac'], 0.12)
    return m


def wood(name, color=(0.42, 0.24, 0.11), dark=(0.20, 0.10, 0.04), axis='Z', scale=6.0, rough=0.45):
    """Procedural grain: wave bands along `axis`, distorted by noise, between two browns."""
    m = bpy.data.materials.new(name); nt, b = _nodes(m)
    tc = nt.nodes.new('ShaderNodeTexCoord')
    wv = nt.nodes.new('ShaderNodeTexWave'); wv.wave_type = 'BANDS'
    wv.bands_direction = {'X': 'X', 'Y': 'Y', 'Z': 'Z'}[axis]
    wv.inputs['Scale'].default_value = scale; wv.inputs['Distortion'].default_value = 6; wv.inputs['Detail'].default_value = 4
    nt.links.new(tc.outputs['Object'], wv.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (*dark, 1); ramp.color_ramp.elements[1].color = (*color, 1)
    nt.links.new(wv.outputs['Fac'], ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = rough
    _bump(nt, b, wv.outputs['Fac'], 0.08)
    return m


def leather(name, color=(0.30, 0.15, 0.07)):
    m = bpy.data.materials.new(name); nt, b = _nodes(m)
    tc = nt.nodes.new('ShaderNodeTexCoord')
    vo = nt.nodes.new('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = 60
    nt.links.new(tc.outputs['Object'], vo.inputs['Vector'])
    nz = _noise(nt, 4, 4)
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'
    mix.inputs['A'].default_value = (*color, 1); mix.inputs['B'].default_value = (color[0] * 1.6, color[1] * 1.6, color[2] * 1.5, 1)
    nt.links.new(nz.outputs['Fac'], mix.inputs['Factor']); nt.links.new(mix.outputs['Result'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.55
    _bump(nt, b, vo.outputs['Distance'], 0.25, 0.01)
    return m


def textured(name, image_path, rough=0.8, bump=0.05, coords='UV', alpha=False):
    """An image texture laid over the object's bounding box (flat sheets: pages, documents)."""
    m = bpy.data.materials.new(name); nt, b = _nodes(m)
    tc = nt.nodes.new('ShaderNodeTexCoord')
    im = nt.nodes.new('ShaderNodeTexImage'); im.image = bpy.data.images.load(image_path)
    nt.links.new(tc.outputs[coords], im.inputs['Vector'])
    nt.links.new(im.outputs['Color'], b.inputs['Base Color'])
    if alpha: nt.links.new(im.outputs['Alpha'], b.inputs['Alpha'])
    b.inputs['Roughness'].default_value = rough
    if bump:
        nz = _noise(nt, 25, 8); _bump(nt, b, nz.outputs['Fac'], bump)
    return m


def glass(name, color=(0.9, 0.95, 1.0), rough=0.02):
    m = bpy.data.materials.new(name); nt, b = _nodes(m)
    b.inputs['Base Color'].default_value = (*color, 1)
    b.inputs['Transmission Weight'].default_value = 1.0
    b.inputs['Roughness'].default_value = rough; b.inputs['IOR'].default_value = 1.45
    return m


# ===== geometry =====

def link(obj, mat=None, smooth=True):
    bpy.context.collection.objects.link(obj)
    if mat is not None: obj.data.materials.append(mat)
    if smooth and obj.type == 'MESH':
        for p in obj.data.polygons: p.use_smooth = True
    return obj


def bevel(obj, width, segments=4, angle=True):
    b = obj.modifiers.new('bevel', 'BEVEL'); b.width = width; b.segments = segments
    if angle: b.limit_method = 'ANGLE'
    return obj


def lathe(name, profile, segments=64, mat=None, cap=True):
    """Revolves (r, z) points around Z. First/last point with r == 0 close the ends."""
    bm = bmesh.new(); rings = []
    for r, z in profile:
        ring = [bm.verts.new((r * math.cos(2 * math.pi * i / segments), r * math.sin(2 * math.pi * i / segments), z))
                for i in range(segments)]
        rings.append(ring)
    for a, b in zip(rings, rings[1:]):
        for i in range(segments):
            j = (i + 1) % segments
            try: bm.faces.new((a[i], a[j], b[j], b[i]))
            except ValueError: pass
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    return link(bpy.data.objects.new(name, me), mat)


def extrude(name, points, depth, mat=None, bevel_w=0.0, segs=4):
    """A flat 2D outline (x, y) extruded along Z by depth, centred on z=0."""
    bm = bmesh.new()
    vs = [bm.verts.new((x, y, -depth / 2)) for x, y in points]
    f = bm.faces.new(vs)
    ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    for v in ext['geom']:
        if isinstance(v, bmesh.types.BMVert): v.co.z += depth
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = link(bpy.data.objects.new(name, me), mat, smooth=False)
    if bevel_w: bevel(o, bevel_w, segs)
    return o


def tube(name, points, radius, mat=None, res=6, cyclic=False):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'
    sp = cu.splines.new('POLY'); sp.points.add(len(points) - 1)
    for p, co in zip(sp.points, points): p.co = (*co, 1)
    sp.use_cyclic_u = cyclic
    cu.bevel_depth = radius; cu.bevel_resolution = res; cu.use_fill_caps = True
    o = bpy.data.objects.new(name, cu); bpy.context.collection.objects.link(o)
    if mat is not None: o.data.materials.append(mat)
    return o


def arc(cx, cy, r, a0, a1, n=32):
    return [(cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def stand(objs, tilt=-15, turn=12):
    """Parents objects to an empty and stands the group up facing the camera (flat things lie in XY)."""
    e = bpy.data.objects.new('stand', None); bpy.context.collection.objects.link(e)
    for o in objs: o.parent = e
    e.rotation_euler = (math.radians(90 + tilt), 0, math.radians(turn))
    return e


def sheet(name, points, uv_box, mat, thickness=0.012):
    """A flat sheet (paper) from a 2D outline, UV-mapped by uv_box = (x0, y0, x1, y1), with thickness."""
    bm = bmesh.new()
    vs = [bm.verts.new((x, y, 0)) for x, y in points]
    f = bm.faces.new(vs)
    uv = bm.loops.layers.uv.new()
    x0, y0, x1, y1 = uv_box
    for loop in f.loops:
        loop[uv].uv = ((loop.vert.co.x - x0) / (x1 - x0), (loop.vert.co.y - y0) / (y1 - y0))
    bmesh.ops.triangulate(bm, faces=[f])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = link(bpy.data.objects.new(name, me), mat, smooth=False)
    s = o.modifiers.new('solid', 'SOLIDIFY'); s.thickness = thickness
    return o


def grid_sheet(name, w, h, mat, nx=40, ny=50, zfun=None, thickness=0.012):
    """A subdivided w x h sheet with UVs over the whole image; zfun(x, y) bends it."""
    bm = bmesh.new(); uv = bm.loops.layers.uv.new()
    verts = [[bm.verts.new((-w / 2 + w * i / nx, -h / 2 + h * j / ny, 0)) for i in range(nx + 1)] for j in range(ny + 1)]
    for j in range(ny):
        for i in range(nx):
            f = bm.faces.new((verts[j][i], verts[j][i + 1], verts[j + 1][i + 1], verts[j + 1][i]))
            for loop in f.loops:
                loop[uv].uv = ((loop.vert.co.x + w / 2) / w, (loop.vert.co.y + h / 2) / h)
    if zfun:
        for v in bm.verts: v.co.z = zfun(v.co.x, v.co.y)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = link(bpy.data.objects.new(name, me), mat)
    if thickness:
        s = o.modifiers.new('solid', 'SOLIDIFY'); s.thickness = thickness
    return o
