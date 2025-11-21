# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2023 Steven Garcia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ##### END MIT LICENSE BLOCK #####

import io
import os
import bpy
import json
import bmesh
import base64
import struct

from sys import float_info
from math import radians, log
from enum import Flag, Enum, auto
from mathutils import Matrix, Vector
from ...global_functions import shader_processing, mesh_processing, global_functions
from ...file_tag.tag_interface import tag_interface, tag_common

class H1ClusterPortalFlags(Flag):
    ai_cant_hear_through_this = auto()

class H1SurfaceFlags(Flag):
    two_sided = auto()
    invisible = auto()
    climbable = auto()
    breakable = auto()

class H2ClusterPortalFlags(Flag):
    ai_cant_hear_through_this = auto()
    one_way = auto()
    door = auto()
    no_way = auto()
    one_way_reversed = auto()
    no_one_can_hear_through_this = auto()

class H2SurfaceFlags(Flag):
    two_sided = auto()
    invisible = auto()
    climbable = auto()
    breakable = auto()
    invalid = auto()
    conveyor = auto()

class PartFlags(Flag):
    decalable = auto()
    new_part_type = auto()
    dislikes_photons = auto()
    override_triangle_list = auto()
    ignored_by_lightmapper = auto()

class PropertyTypeEnum(Enum):
    lightmap_resolution = 0
    lightmap_power = auto()
    lightmap_half_life = auto()
    lightmap_diffuse_scale = auto()

PLANE_PARALLEL_ANGLE_EPSILON = 0.0001
WEATHER_POLYHEDRA_TOLERANCE  = 0.00001

def point_distance_to_plane(point, normal, dist, round_adjust=0):
    '''
    Returns distance from the point to the plane.
    '''
    # NOTE: we're taking into account rounding errors for 32bit floats
    #       by calculating for rounding errors using float epsilon.
    #       23 is the mantissa length of 32bit floating point numbers, which
    #       can be used as a measurement for the accuracy of the float.
    delta_max = 2**(int(log(abs(dist) + float_info.epsilon, 2)) - 23) + abs(round_adjust)
    delta = point.dot(normal) - dist

    return 0.0 if abs(delta) < delta_max else delta

def is_point_this_side_of_plane(point, normal, dist, on_plane_ok=False,
                                side_to_check=True, round_adjust=0):
    '''
    Returns True if point is on the side of the plane being checked.
    If side_to_check == True, point is expected to be on front side of plane.
    If side_to_check == False, point is expected to be on back side of plane.
    '''
    rounded_dist = point_distance_to_plane(point, normal, dist, round_adjust)
    return (
        (on_plane_ok and rounded_dist == 0) or
        (rounded_dist if side_to_check else -rounded_dist) > 0
        )

def is_point_on_this_side_of_planes(point, planes, on_plane_ok=False,
                                    side_to_check=True, round_adjust=0):
    '''
    Returns True if point is on the side of every the plane being checked.
    If side_to_check == True, point is expected to be on front side of planes.
    If side_to_check == False, point is expected to be on back side of planes.
    '''
    for normal, dist in planes:
        if not is_point_this_side_of_plane(
                point, normal, dist, on_plane_ok,
                side_to_check, round_adjust
                ):
            return False
    return True

def get_intersection_point_and_ray_of_planes(plane_a, plane_b):
    '''
    Solves for the ray vector parallel with the intersection
    of the planes, and an arbitrary point on the ray. Throws
    ValueError if planes do not intersect.
    '''
    ray = plane_a[0].cross(plane_b[0])
    if ray.magnitude < PLANE_PARALLEL_ANGLE_EPSILON:
        raise ValueError("Magnitude is less than epsilon")

    ray.normalize()
    # calculate an arbitrary point on the ray.
    # we do this by setting the same coordinate in each plane to
    # zero, isolating a second variable to one side of an equation,
    # and substituting it into the other to find the third variable.
    # then take your 2 known variables and solve for the unknown.
    #   d0 = x*a0 + y*b0 + z*c0   and   d1 = x*a1 + y*b1 + z*c1
    # holding x at 0, we simplify like so:
    #   d0 = y*b0 + z*c0          and   d1 = y*b1 + z*c1
    #   (d0 -y*b0)/c0 = z         and   (d1 - z*c1)/b1 = y
    #   y             = (d1 - ((d0 - y*b0)/c0)*c1)/b1
    #   y*b1          = d1 - ((d0 - y*b0)/c0)*c1
    #   y*(b1/c1)     = d1/c1 - (d0 - y*b0)/c0
    #   d1            = y*b1 + (d0 - y*b0)*(c1/c0)
    #   d1            = y*b1 + (d0*c1)/c0 - y*(b0*c1)/c0
    #   d1*c0 - d0*c1 = y*b1*c0 - y*b0*c1
    # holding x at 0 the equations are:
    #   y             = (d1*c0 - d0*c1) / (b1*c0 - b0*c1)
    #   z             = (d0*b1 - d1*b0) / (c0*b1 - c1*b0)
    # holding y at 0 the equations are:
    #   x             = (d1*c0 - d0*c1) / (a1*c0 - a0*c1)
    #   z             = (d0*a1 - d1*a0) / (c0*a1 - c1*a0)
    # holding z at 0 the equations are:
    #   y             = (d1*a0 - d0*a1) / (b1*a0 - b0*a1)
    #   x             = (d0*b1 - d1*b0) / (a0*b1 - a1*b0)
    a0, b0, c0 = plane_a[0]
    a1, b1, c1 = plane_b[0]
    d0, d1     = plane_a[1], plane_b[1]
    pos  = Vector([0, 0, 0])
    # we pick the axis to hold at 0 by which has the largest magnitude.
    if (abs(ray.x) > abs(ray.y) and
        abs(ray.x) > abs(ray.z)):
        pos.y = (d1*c0 - d0*c1) / (b1*c0 - b0*c1)
        pos.z = (d0*b1 - d1*b0) / (c0*b1 - c1*b0)
    elif abs(ray.y) > abs(ray.z):
        pos.x = (d1*c0 - d0*c1) / (a1*c0 - a0*c1)
        pos.z = (d0*a1 - d1*a0) / (c0*a1 - c1*a0)
    elif abs(ray.z) > 0:
        pos.y = (d1*a0 - d0*a1) / (b1*a0 - b0*a1)
        pos.x = (d0*b1 - d1*b0) / (a0*b1 - a1*b0)

    return ray, pos

def get_point_on_plane(norm, dist):
    '''
    Solves for an arbitrary point on the plane by rearranging
    the plane equation(d = x*a + y*b + z*c) and holding two of
    the values constant and solve for the third.
    '''
    # Solve for the axis with the largest magnitude, as it
    # indicates the other axis values can be held at 0.
    # we can simplify from this:
    #   d   = x*a + y*b + z*c
    # to this:
    #   d/x = a
    pos  = Vector([0, 0, 0])
    if (abs(norm.x) > abs(norm.y) and
        abs(norm.x) > abs(norm.z)):
        pos.x = dist/norm.x
    elif abs(norm.y) > abs(norm.z):
        pos.y = dist/norm.y
    elif abs(norm.z) > 0:
        pos.z = dist/norm.z

    return pos

def find_intersect_point_of_planes(plane_0, plane_1, plane_2):
    '''
    Returns intersection point of 3 planes as a Vector, or
    None if there is no intersection. If any of the planes
    are parallel to each other, there is no intersection.
    '''
    norm_0, norm_1, norm_2 = plane_0[0], plane_1[0], plane_2[0]

    # find the intersection vectors between each plane
    cross_01 = norm_0.cross(norm_1)
    cross_02 = norm_2.cross(norm_0)
    cross_12 = norm_1.cross(norm_2)
    # the magnitude of the crosses is the sine of the angle between them.
    # any being ~zero indicates the planes are parallel to each other.
    if min(cross_01.magnitude, cross_02.magnitude, cross_12.magnitude) < PLANE_PARALLEL_ANGLE_EPSILON:
        return None

    # figure out which planes to cross and which to try and intersect
    # with. we're comparing the angle between the planes being crossed
    # to ensure we maximize the precision of the crossed vectors.
    if (cross_01.magnitude > cross_02.magnitude and
        cross_01.magnitude > cross_12.magnitude):
        plane_a, plane_b, plane_c = plane_0, plane_1, plane_2
    elif cross_02.magnitude > cross_12.magnitude:
        plane_a, plane_b, plane_c = plane_0, plane_2, plane_1
    else:
        plane_a, plane_b, plane_c = plane_2, plane_1, plane_0

    # find the point where the edge ray intersects the plane
    edge_ray, edge_pos = get_intersection_point_and_ray_of_planes(
        plane_a, plane_b
        )

    # find the distance from origin to the intersection of plane and edge
    plane_norm, plane_dist = plane_c
    plane_pos = get_point_on_plane(plane_norm, plane_dist)

    # find and return the point that the edge intersects the other plane
    cos_angle = plane_norm.dot(edge_ray)
    if cos_angle < PLANE_PARALLEL_ANGLE_EPSILON:
        return None

    intersect_dist_to_origin = plane_norm.dot(plane_pos-edge_pos) / cos_angle
    return edge_pos + edge_ray * intersect_dist_to_origin

def planes_to_convex_hull_vert_coords(planes, round_adjust=0.000001):
    '''
    Returns a list of all points that make up a convex hull formed by
    the intersection of all provided planes. Note that there is little
    cleanup done here, so the list may have nearly-coplanar verts.
    '''
    verts = []

    # find the intersect points of all planes within the polyhedron
    plane_ct = len(planes)
    for i in range(plane_ct):
        for j in range(plane_ct):
            if i == j: continue
            for k in range(plane_ct):
                if k == i or k == j:
                    continue

                intersect = find_intersect_point_of_planes(
                    planes[i], planes[j], planes[k],
                    )

                if (intersect is not None and is_point_on_this_side_of_planes(
                        intersect, planes, True, round_adjust=round_adjust
                        )):
                    verts.append(intersect)

    return verts

def build_scene(context, tag_ref, asset_cache, game_title, fix_rotations, empty_markers, report, collection_override=None, cluster_collection_override=None):
    if game_title == "halo1":
        tag_groups = tag_common.h1_tag_groups
    elif game_title == "halo2":
        tag_groups = tag_common.h2_tag_groups
    else:
        print("%s is not supported." % game_title)

    level_asset = tag_interface.get_disk_asset(tag_ref["path"], tag_groups.get(tag_ref["group name"]))
    level_data = level_asset["Data"]

    collection = context.collection
    if not collection_override == None:
        collection = collection_override

    if cluster_collection_override == None:
        cluster_collection_override = collection

    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors

    level_root = bpy.data.objects.get("frame_root")
    if level_root == None:
        level_mesh = bpy.data.meshes.new("frame_root")
        level_root = bpy.data.objects.new("frame_root", level_mesh)
        level_root.color = (1, 1, 1, 0)
        collection.objects.link(level_root)

        mesh_processing.select_object(context, level_root)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.ops.object.mode_set(mode='OBJECT')
        level_root.hide_set(True)
        level_root.hide_render = True

    if game_title == "halo1":
        if len(level_data["lightmaps"]) > 0:
            surfaces = level_data["surfaces"]
            for lightmap_idx, lightmap in enumerate(level_data["lightmaps"]):
                if len(lightmap["materials"]) > 0:
                    cluster_name = "cluster_%s" % lightmap_idx
                    full_mesh = bpy.data.meshes.new(cluster_name)
                    object_mesh = bpy.data.objects.new(cluster_name, full_mesh)
                    object_mesh.color = (1, 1, 1, 0)
                    object_mesh.tag_mesh.lightmap_index = lightmap["bitmap"]

                    object_mesh.parent = level_root
                    cluster_collection_override.objects.link(object_mesh)
                    
                    if (4, 1, 0) > bpy.app.version:
                        object_mesh.data.use_auto_smooth = True
                    
                    bm = bmesh.new()

                    for material_idx, material in enumerate(lightmap["materials"]):
                        has_lightmap = False
                        if material["vertex count"] == material["vertex count_1"]:
                            has_lightmap = True

                        material_name = "material_%s" % material_idx
                        mesh = bpy.data.meshes.new(material_name)
                        start_index = material["surfaces"]

                        uncompressed_data = base64.b64decode(material["uncompressed vertices"]["encoded"])
                        compressed_data = base64.b64decode(material["compressed vertices"]["encoded"])

                        uncompressed_stream = io.BytesIO(uncompressed_data)
                        compressed_stream = io.BytesIO(compressed_data)

                        uc_vertices = []
                        c_vertices = []
                        for ucr_vertex_idx in range(material["vertex count"]):
                            position = struct.unpack("<fff", uncompressed_stream.read(12))
                            normal = struct.unpack("<fff", uncompressed_stream.read(12))
                            binormal = struct.unpack("<fff", uncompressed_stream.read(12))
                            tangent = struct.unpack("<fff", uncompressed_stream.read(12))
                            texture_coords = struct.unpack("<ff", uncompressed_stream.read(8))

                            vertex_dict = {
                                "position": position,
                                "normal": normal,
                                "binormal": binormal,
                                "tangent": tangent,
                                "texture_coords": texture_coords}

                            uc_vertices.append(vertex_dict)

                        if has_lightmap:
                            for uc_vertex in uc_vertices:
                                l_normal = struct.unpack("<fff", uncompressed_stream.read(12))
                                l_texture_coords = struct.unpack("<ff", uncompressed_stream.read(8))

                                uc_vertex["l_normal"] = l_normal
                                uc_vertex["l_texture_coords"] = l_texture_coords

                        # Compressed vertices stuff but we never use it so why bother - Gen
                        if False:
                            for cr_vertex_idx in range(material["vertex count"]):
                                c_position = struct.unpack(">fff", compressed_stream.read(12))
                                c_normal = struct.unpack(">I", compressed_stream.read(4))
                                c_binormal = struct.unpack(">I", compressed_stream.read(4))
                                c_tangent = struct.unpack(">I", compressed_stream.read(4))
                                c_texture_coords = struct.unpack(">ff", compressed_stream.read(8))

                                c_vertex_dict = {
                                    "position": c_position,
                                    "normal": c_normal,
                                    "binormal": c_binormal,
                                    "tangent": c_tangent,
                                    "texture_coords": c_texture_coords}

                                cr_vertices.append(c_vertex_dict)

                            if has_lightmap:
                                for cl_vertex_idx in range(material["vertex count_1"]):
                                    cl_normal = struct.unpack(">I", compressed_stream.read(4))
                                    cl_texture_coords = struct.unpack(">hh", compressed_stream.read(4))

                                    cl_vertex_dict = {
                                        "normal": cl_normal,
                                        "texture_coords": cl_texture_coords}

                                cl_vertices.append(cl_vertex_dict)

                        triangles = []
                        vertices = [Vector(vertex["position"]) * 100 for vertex in uc_vertices]
                        normals = [Vector(vertex["normal"]) for vertex in uc_vertices]
                        for idx in range(material["surface count"]):
                            surface_idx = start_index + idx
                            triangles.append([surfaces[surface_idx]["vertex2 index"], surfaces[surface_idx]["vertex1 index"], surfaces[surface_idx]["vertex0 index"]]) # Reversed order to fix facing normals

                        mesh.from_pydata(vertices, [], triangles)
                        for tri_idx, poly in enumerate(mesh.polygons):
                            poly.use_smooth = True

                        mesh.normals_split_custom_set_from_vertices(normals)
                        for triangle_idx, triangle in enumerate(triangles):
                            shader_tag = material["shader"]
                            shader_group = shader_tag["group name"]
                            shader_name = shader_tag["path"]
                            permutation = material["shader permutation"]

                            has_permutation = permutation != 0

                            SHAD_ASSET = asset_cache.get(shader_group, {}).get(shader_name)
                            if SHAD_ASSET:
                                material_name = os.path.basename(shader_name)
                                if has_permutation:
                                    material_name = "%s%s" % (material_name, permutation)
                                    
                                mat = SHAD_ASSET["blender_assets"].get(material_name)
                                if not mat:
                                    mat = bpy.data.materials.new(name=material_name)
                                    shader_processing.generate_h1_shader(mat, shader_tag, permutation, asset_cache, report)
                                    SHAD_ASSET["blender_assets"][material_name] = mat

                            else:
                                material_name = "invalid"
                                if global_functions.string_empty_check(shader_name):
                                    material_name = os.path.basename(shader_name)

                                if has_permutation:
                                    material_name = "%s%s" % (material_name, permutation)

                                mat = bpy.data.materials.get(material_name)
                                if not mat:
                                    mat = bpy.data.materials.new(name=material_name)

                            if mat.name not in object_mesh.data.materials:
                                object_mesh.data.materials.append(mat)

                            mat.diffuse_color = random_color_gen.next()
                            material_index = object_mesh.data.materials.find(mat.name)
                            mesh.polygons[triangle_idx].material_index = material_index

                            uv_name = 'UVMap_Render'
                            uv_lightmap_name = 'UVMap_Lightmap'

                            layer_uv = mesh.uv_layers.get(uv_name)
                            if layer_uv is None:
                                layer_uv = mesh.uv_layers.new(name=uv_name)

                            layer_uv_lightmap = mesh.uv_layers.get(uv_lightmap_name)
                            if layer_uv_lightmap is None:
                                layer_uv_lightmap = mesh.uv_layers.new(name=uv_lightmap_name)

                            render_vertex_list = [uc_vertices[triangle[0]], uc_vertices[triangle[1]], uc_vertices[triangle[2]]]
                            for vertex_idx, vertex in enumerate(render_vertex_list):
                                loop_index = (3 * triangle_idx) + vertex_idx

                                u = vertex["texture_coords"][0]
                                v = vertex["texture_coords"][1]

                                layer_uv.data[loop_index].uv = (u, 1 - v)

                            if has_lightmap:
                                lightmap_vertex_list = [uc_vertices[triangle[0]], uc_vertices[triangle[1]], uc_vertices[triangle[2]]]
                                for vertex_idx, vertex in enumerate(lightmap_vertex_list):
                                    loop_index = (3 * triangle_idx) + vertex_idx

                                    u_l = vertex["l_texture_coords"][0]
                                    v_l = vertex["l_texture_coords"][1]

                                    layer_uv_lightmap.data[loop_index].uv = (u_l, v_l)

                        bm.from_mesh(mesh)
                        bpy.data.meshes.remove(mesh)

                    bm.to_mesh(full_mesh)
                    bm.free()

        if len(level_data["cluster portals"]) > 0:
            portal_bm = bmesh.new()
            portal_mesh = bpy.data.meshes.new("level_portals")
            portal_object = bpy.data.objects.new("level_portals", portal_mesh)
            portal_object.color = (1, 1, 1, 0)
            portal_object.parent = level_root
            collection.objects.link(portal_object)
            portal_object.hide_set(True)
            portal_object.hide_render = True
            for cluster in level_data["clusters"]:
                for portal in cluster["portals"]:
                    vert_indices = []
                    cluster_portal = level_data["cluster portals"][portal["portal"]]
                    for vertex in cluster_portal["vertices"]:
                        vert_indices.append(portal_bm.verts.new(Vector(vertex["point"]) * 100))

                    portal_bm.faces.new(vert_indices)

                portal_bm.verts.ensure_lookup_table()
                portal_bm.faces.ensure_lookup_table()

                for portal_idx, portal in enumerate(cluster["portals"]):
                    cluster_portal = level_data["cluster portals"][portal["portal"]]
                    material_list = []

                    material_name = "+portal"
                    if H1ClusterPortalFlags.ai_cant_hear_through_this in H1ClusterPortalFlags(cluster_portal["flags"]):
                        material_name = "+portal&"

                    mat = bpy.data.materials.get(material_name)
                    if mat is None:
                        mat = bpy.data.materials.new(name=material_name)

                    for slot in portal_object.material_slots:
                        material_list.append(slot.material)

                    if not mat in material_list:
                        material_list.append(mat)
                        portal_object.data.materials.append(mat)

                    mat.diffuse_color = random_color_gen.next()
                    material_index = material_list.index(mat)
                    portal_bm.faces[portal_idx].material_index = material_index

                    cluster_portal = level_data["cluster portals"][portal["portal"]]
                    poly = portal_bm.faces[portal_idx]
                    plane = level_data["collision bsp"][0]["planes"][cluster_portal["plane index"]]
                    x, y, z, d = plane["plane"]
                    if poly.normal.dot(Vector((x, y, z))) < 0:
                        poly.flip()

            portal_bm.to_mesh(portal_mesh)
            portal_bm.free()

        for marker in level_data["markers"]:
            object_name_prefix = '#%s' % marker["name"]
            marker_name_override = ""
            if context.scene.objects.get('#%s' % marker["name"]):
                marker_name_override = marker["name"]

            mesh = bpy.data.meshes.new(object_name_prefix)
            object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
            object_mesh.color = (1, 1, 1, 0)
            collection.objects.link(object_mesh)
            object_mesh.hide_set(True)
            object_mesh.hide_render = True

            object_mesh.ass_jms.name_override = marker_name_override

            bm = bmesh.new()
            bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
            bm.to_mesh(mesh)
            bm.free()

            object_mesh.parent = level_root

            matrix_translate = Matrix.Translation(Vector(marker["position"]) * 100)
            marker_rot = global_functions.convert_quaternion(marker["rotation"]).inverted()
            matrix_rotation = marker_rot.to_matrix().to_4x4()

            transform_matrix = matrix_translate @ matrix_rotation
            if fix_rotations:
                transform_matrix = Matrix.Rotation(radians(90.0), 4, 'Z') @ transform_matrix

            object_mesh.matrix_world = transform_matrix
            object_mesh.data.ass_jms.Object_Type = 'SPHERE'
            object_mesh.dimensions = (2, 2, 2)

        if len(level_data["fog planes"]) > 0:
            fog_planes_bm = bmesh.new()
            fog_planes_mesh = bpy.data.meshes.new("level_fog_planes")
            fog_planes_object = bpy.data.objects.new("level_fog_planes", fog_planes_mesh)
            fog_planes_object.color = (1, 1, 1, 0)
            fog_planes_object.parent = level_root
            collection.objects.link(fog_planes_object)
            fog_planes_object.hide_set(True)
            fog_planes_object.hide_render = True
            for fog_plane in level_data["fog planes"]:
                vert_indices = []
                for vertex in fog_plane["vertices"]:
                    vert_indices.append(fog_planes_bm.verts.new(Vector(vertex["point"]) * 100))

                fog_planes_bm.faces.new(vert_indices)

            fog_planes_bm.verts.ensure_lookup_table()
            fog_planes_bm.faces.ensure_lookup_table()

            material_list = []

            material_name = "+unused$"
            mat = bpy.data.materials.get(material_name)
            if mat is None:
                mat = bpy.data.materials.new(name=material_name)

            for slot in fog_planes_object.material_slots:
                material_list.append(slot.material)

            if not mat in material_list:
                material_list.append(mat)
                fog_planes_object.data.materials.append(mat)

            mat.diffuse_color = random_color_gen.next()

            fog_planes_bm.to_mesh(fog_planes_mesh)
            fog_planes_bm.free()

        if len(level_data["weather polyhedra"]) > 0:
            material_name = "+weatherpoly"
            mat = bpy.data.materials.get(material_name)
            if mat is None:
                mat = bpy.data.materials.new(name=material_name)

            mat.diffuse_color = random_color_gen.next()
            for poly_idx, weather_polyhedra in enumerate(level_data["weather polyhedra"]):
                bsc_vector = Vector(weather_polyhedra["bounding sphere center"])
                tolerance = bsc_vector.magnitude * WEATHER_POLYHEDRA_TOLERANCE
                weather_planes = []
                for plane in weather_polyhedra["planes"]:
                    x, y, z, d = plane["plane"]
                    weather_planes.append((Vector((x, y, z)), d))

                coords = planes_to_convex_hull_vert_coords(weather_planes, tolerance)
                if len(coords) <= 3:
                    continue

                bm = bmesh.new()
                for coord in coords:
                    bm.verts.new(coord * 100)

                bmesh.ops.convex_hull(bm, input=bm.verts)
                mesh = bpy.data.meshes.new("weather_polyhedra_%d" % poly_idx)
                obj = bpy.data.objects.new("weather_polyhedra_%d" % poly_idx, mesh)
                obj.color = (1, 1, 1, 0)
                obj.parent = level_root
                collection.objects.link(obj)
                bm.to_mesh(mesh)
                bm.free()

                if not mat in mesh.materials.values():
                    mesh.materials.append(mat)

    else:
        shader_collection_dic = {}
        shader_collection_path = os.path.join(bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_tag_path, r"scenarios\shaders\shader_collections.shader_collections")
        if os.path.isfile(shader_collection_path):
            shader_collection_file = open(shader_collection_path, "r")
            for line in shader_collection_file.readlines():
                if not global_functions.string_empty_check(line) and not line.startswith(";"):
                    split_result = line.split()
                    if len(split_result) == 2:
                        prefix = split_result[0]
                        path = split_result[1]
                        shader_collection_dic[path] = prefix

        for material in level_data["materials"]:
            shader_tag = material["shader"]
            old_shader_tag = material["old shader"]
            shader_group = shader_tag["group name"]
            shader_name = shader_tag["path"]
            if global_functions.string_empty_check(shader_name):
                shader_tag = old_shader_tag
                shader_group = old_shader_tag["group name"]
                shader_name = old_shader_tag["path"]

            shader_directory = os.path.dirname(shader_name)
            base_name = os.path.basename(shader_name)
            has_collection = False
            has_parameter = False

            collection_prefix = shader_collection_dic.get(shader_directory)
            if not collection_prefix == None:
                has_collection = True

            lightmap_parameters = ""
            for material_property in material["properties"]:
                property_enum = PropertyTypeEnum(material_property["type"]["value"])
                property_value = material_property["real-value"]
                if PropertyTypeEnum.lightmap_resolution == property_enum:
                    lightmap_parameters += " lm:%s" % property_value
                    has_parameter = True

                elif PropertyTypeEnum.lightmap_power == property_enum:
                    lightmap_parameters += " lp:%s" % property_value
                    has_parameter = True

                elif PropertyTypeEnum.lightmap_half_life == property_enum:
                    lightmap_parameters += " hl:%s" % property_value
                    has_parameter = True

                elif PropertyTypeEnum.lightmap_diffuse_scale == property_enum:
                    lightmap_parameters += " ds:%s" % property_value
                    has_parameter = True

            SHAD_ASSET = asset_cache.get(shader_group, {}).get(shader_name)
            if SHAD_ASSET:
                material_name = base_name
                if has_collection:
                    material_name = "%s %s" % (collection_prefix, material_name)

                if has_parameter:
                    material_name = "%s%s" % (material_name, lightmap_parameters)

                mat = SHAD_ASSET["blender_assets"].get(material_name)
                if not mat:
                    mat = bpy.data.materials.new(name=material_name)
                    shader_processing.generate_h2_shader(mat, shader_tag, asset_cache, report)
                    SHAD_ASSET["blender_assets"][material_name] = mat
  
            else:
                material_name = "invalid"
                if global_functions.string_empty_check(shader_name):
                    material_name = os.path.basename(shader_name)

                if has_collection:
                    material_name = "%s %s" % (collection_prefix, material_name)

                if has_parameter:
                    material_name = "%s%s" % (material_name, lightmap_parameters)

                mat = bpy.data.materials.get(material_name)
                if not mat:
                    mat = bpy.data.materials.new(name=material_name)

        if len(level_data["clusters"]) > 0:
            for cluster_idx, cluster in enumerate(level_data["clusters"]):
                cluster_name = "cluster_%s" % cluster_idx
                mesh = bpy.data.meshes.new(cluster_name)
                object_mesh = bpy.data.objects.new(cluster_name, mesh)
                object_mesh.color = (1, 1, 1, 0)

                object_mesh.parent = level_root
                mesh_processing.get_mesh_data(level_data, asset_cache, cluster["cluster data"], mesh, random_color_gen, shader_collection_dic)

                cluster_collection_override.objects.link(object_mesh)

                if (4, 1, 0) > bpy.app.version:
                    object_mesh.data.use_auto_smooth = True

        if len(level_data["instanced geometry instances"]) > 0:
            instance_collection = cluster_collection_override
            if not cluster_collection_override == None:
                bsp_name = instance_collection.name.split("_", 1)[0]
                intances_name = "%s_instances" % bsp_name
                instance_collection = bpy.data.collections.get(intances_name)
                if instance_collection == None:
                    instance_collection = bpy.data.collections.new(intances_name)
                    cluster_collection_override.children.link(instance_collection)

            meshes = []
            for instanced_geometry_definition_idx, instanced_geometry_definition in enumerate(level_data["instanced geometries definitions"]):
                cluster_name = "instanced_geometry_definition_%s" % instanced_geometry_definition_idx
                mesh = bpy.data.meshes.new(cluster_name)
                mesh_processing.get_mesh_data(level_data, asset_cache, instanced_geometry_definition["render data"], mesh, random_color_gen, shader_collection_dic)

                meshes.append(mesh)

            for instanced_geometry_instance in level_data["instanced geometry instances"]:
                mesh = meshes[instanced_geometry_instance["instance definition"]]
                ob_name = instanced_geometry_instance["name"]

                object_mesh = bpy.data.objects.new(ob_name, mesh)
                object_mesh.color = (1, 1, 1, 0)
                object_mesh.tag_mesh.instance_lightmap_policy_enum = str(instanced_geometry_instance["lightmapping policy"]["value"])

                object_mesh.parent = level_root
                instance_collection.objects.link(object_mesh)

                matrix_scale = Matrix.Scale(instanced_geometry_instance["scale"], 4)
                matrix_rotation = Matrix()
                matrix_rotation[0] = *Vector(instanced_geometry_instance["forward"]), 0
                matrix_rotation[1] = *Vector(instanced_geometry_instance["left"]), 0
                matrix_rotation[2] = *Vector(instanced_geometry_instance["up"]), 0
                matrix_rotation = matrix_rotation.inverted()
                matrix_translation = Matrix.Translation(Vector(instanced_geometry_instance["position"]) * 100)
                transform_matrix = (matrix_translation @ matrix_rotation @ matrix_scale)
                object_mesh.matrix_world = transform_matrix

                if (4, 1, 0) > bpy.app.version:
                    object_mesh.data.use_auto_smooth = True

        if len(level_data["cluster portals"]) > 0:
            portal_bm = bmesh.new()
            portal_mesh = bpy.data.meshes.new("level_portals")
            portal_object = bpy.data.objects.new("level_portals", portal_mesh)
            portal_object.color = (1, 1, 1, 0)
            portal_object.parent = level_root
            collection.objects.link(portal_object)
            portal_object.hide_set(True)
            portal_object.hide_render = True
            for cluster in level_data["clusters"]:
                for portal in cluster["portals"]:
                    vert_indices = []
                    cluster_portal = level_data["cluster portals"][portal["portal index"]]
                    for vertex in cluster_portal["vertices"]:
                        position = Vector(vertex["point"]) * 100
                        vert_indices.append(portal_bm.verts.new(position))

                    portal_bm.faces.new(vert_indices)

                portal_bm.verts.ensure_lookup_table()
                portal_bm.faces.ensure_lookup_table()

                for portal_idx, portal in enumerate(cluster["portals"]):
                    cluster_portal = level_data["cluster portals"][portal["portal index"]]
                    material_list = []

                    material_name = "+portal"
                    if H2ClusterPortalFlags.ai_cant_hear_through_this in H2ClusterPortalFlags(cluster_portal["flags"]):
                        material_name = "+portal&"

                    mat = bpy.data.materials.get(material_name)
                    if mat is None:
                        mat = bpy.data.materials.new(name=material_name)

                    for slot in portal_object.material_slots:
                        material_list.append(slot.material)

                    if not mat in material_list:
                        material_list.append(mat)
                        portal_object.data.materials.append(mat)

                    mat.diffuse_color = random_color_gen.next()
                    material_index = material_list.index(mat)
                    portal_bm.faces[portal_idx].material_index = material_index

            portal_bm.to_mesh(portal_mesh)
            portal_bm.free()

        for marker in level_data["markers"]:
            marker_name = marker["name"]
            object_name_prefix = '#%s' % marker_name
            marker_name_override = ""
            if context.scene.objects.get('#%s' % marker_name):
                marker_name_override = marker_name

            mesh = bpy.data.meshes.new(object_name_prefix)
            object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
            object_mesh.color = (1, 1, 1, 0)
            collection.objects.link(object_mesh)
            object_mesh.hide_set(True)
            object_mesh.hide_render = True

            object_mesh.ass_jms.name_override = marker_name_override

            bm = bmesh.new()
            bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
            bm.to_mesh(mesh)
            bm.free()

            object_mesh.parent = level_root

            position = Vector(marker["position"]) * 100
            matrix_translate = Matrix.Translation(position)
            matrix_rotation = global_functions.convert_quaternion(marker["rotation"]).to_matrix().to_4x4()

            transform_matrix = matrix_translate @ matrix_rotation
            if fix_rotations:
                transform_matrix = Matrix.Rotation(radians(90.0), 4, 'Z') @ transform_matrix

            object_mesh.matrix_world = transform_matrix
            object_mesh.data.ass_jms.Object_Type = 'SPHERE'
            object_mesh.dimensions = (2, 2, 2)

    for bsp_idx, bsp in enumerate(level_data["collision bsp"]):
        collision_name = "level_collision"
        collision_bm = bmesh.new()

        collision_mesh = bpy.data.meshes.new(collision_name)
        collision_object = bpy.data.objects.new(collision_name, collision_mesh)
        collision_object.color = (1, 1, 1, 0)
        collection.objects.link(collision_object)
        collision_object.hide_set(True)
        collision_object.hide_render = True
        for surface_idx, surface in enumerate(bsp["surfaces"]):
            edge_index = surface["first edge"]
            surface_edges = []
            vert_indices = []
            while edge_index not in surface_edges:
                surface_edges.append(edge_index)
                edge = bsp["edges"][edge_index]
                if edge["left surface"] == surface_idx:
                    vert_indices.append(collision_bm.verts.new(Vector(bsp["vertices"][edge["start vertex"]]["point"]) * 100))
                    edge_index = edge["forward edge"]

                else:
                    vert_indices.append(collision_bm.verts.new(Vector(bsp["vertices"][edge["end vertex"]]["point"]) * 100))
                    edge_index = edge["reverse edge"]

            is_invalid = False
            if game_title == "halo2" and H2SurfaceFlags.invalid in H2SurfaceFlags(surface["flags"]):
                is_invalid = True

            if not is_invalid and len(vert_indices) >= 3:
                collision_bm.faces.new(vert_indices)

        collision_bm.verts.ensure_lookup_table()
        collision_bm.faces.ensure_lookup_table()
        surface_idx = 0
        for surface in bsp["surfaces"]:
            is_invalid = False
            if game_title == "halo2" and H2SurfaceFlags.invalid in H2SurfaceFlags(surface["flags"]):
                is_invalid = True

            if not is_invalid:
                ngon_material_index = surface["material"]
                if not ngon_material_index == -1:
                    mat = level_data["collision materials"][ngon_material_index]

                if not ngon_material_index == -1:
                    if game_title == "halo1":
                        shader_path = mat["shader"]["path"]
                        material_name = os.path.basename(shader_path)
                    else:
                        shader_path = mat["new shader"]["path"]

                        material_directory = os.path.dirname(shader_path)
                        material_name = os.path.basename(shader_path)

                        collection_prefix = shader_collection_dic.get(material_directory)
                        if not collection_prefix == None:
                            material_name = "%s %s" % (collection_prefix, material_name)

                    if game_title == "halo1":
                        surface_flags = H1SurfaceFlags(surface["flags"])
                        if H1SurfaceFlags.two_sided in surface_flags:
                            material_name += "%"

                        if H1SurfaceFlags.invisible in surface_flags:
                            material_name += "*"

                        if H1SurfaceFlags.climbable in surface_flags:
                            material_name += "^"

                        if H1SurfaceFlags.breakable in surface_flags:
                            material_name += "-"

                    else:
                        surface_flags = H2SurfaceFlags(surface["flags"])
                        if H2SurfaceFlags.two_sided in surface_flags:
                            material_name += "%"

                        if H2SurfaceFlags.invisible in surface_flags:
                            material_name += "*"

                        if H2SurfaceFlags.climbable in surface_flags:
                            material_name += "^"

                        if H2SurfaceFlags.breakable in surface_flags:
                            material_name += "-"

                        if H2SurfaceFlags.conveyor in surface_flags:
                            material_name += ">"

                else:
                    material_name = "+sky"

                material_list = []
                mat = bpy.data.materials.get(material_name)
                if mat is None:
                    mat = bpy.data.materials.new(name=material_name)

                for slot in collision_object.material_slots:
                    material_list.append(slot.material)

                if not mat in material_list:
                    material_list.append(mat)
                    collision_object.data.materials.append(mat)

                mat.diffuse_color = random_color_gen.next()
                material_index = material_list.index(mat)
                collision_bm.faces[surface_idx].material_index = material_index
                surface_idx += 1

        collision_bm.to_mesh(collision_mesh)
        collision_bm.free()

        collision_object.parent = level_root
