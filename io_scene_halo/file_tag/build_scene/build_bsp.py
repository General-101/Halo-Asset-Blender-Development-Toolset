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

import os
import bpy
import bmesh

from ... import config
from sys import float_info
from math import radians, log
from mathutils import Matrix, Vector
from ..h2.file_scenario_structure_bsp.format import ClusterPortalFlags as H2ClusterPortalFlags, SurfaceFlags as H2SurfaceFlags, PartFlags, PropertyTypeEnum
from ...global_functions import shader_processing, mesh_processing, global_functions
from ..h1.file_scenario_structure_bsp.format import ClusterPortalFlags as H1ClusterPortalFlags, SurfaceFlags as H1SurfaceFlags

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
    #print(delta_max, delta, round_adjust)
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

def build_scene(context, LEVEL, game_version, game_title, file_version, fix_rotations, empty_markers, report, collection_override=None, cluster_collection_override=None):
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
        collection.objects.link(level_root)

        mesh_processing.select_object(context, level_root)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.ops.object.mode_set(mode='OBJECT')
        level_root.hide_set(True)
        level_root.hide_render = True

    if game_title == "halo1":
        if len(LEVEL.lightmaps) > 0:
            surfaces = LEVEL.surfaces
            for lightmap_idx, lightmap in enumerate(LEVEL.lightmaps):
                if len(lightmap.materials) > 0:
                    cluster_name = "cluster_%s" % lightmap_idx
                    full_mesh = bpy.data.meshes.new(cluster_name)
                    object_mesh = bpy.data.objects.new(cluster_name, full_mesh)
                    object_mesh.tag_view.data_type_enum = '1'
                    object_mesh.tag_view.lightmap_index = lightmap.bitmap_index

                    object_mesh.parent = level_root
                    cluster_collection_override.objects.link(object_mesh)
                    bm = bmesh.new()

                    for material_idx, material in enumerate(lightmap.materials):
                        has_lightmap = False
                        if material.vertices_count == material.lightmap_vertices_count:
                            has_lightmap = True

                        material_name = "material_%s" % material_idx
                        mesh = bpy.data.meshes.new(material_name)

                        triangles = []
                        start_index = material.surfaces

                        triangle_indices = []
                        triangles = []
                        vertices = [vertex.translation for vertex in material.uncompressed_render_vertices]
                        normals = [vertex.normal for vertex in material.uncompressed_render_vertices]

                        for idx in range(material.surface_count):
                            surface_idx = start_index + idx
                            triangles.append([surfaces[surface_idx].v2, surfaces[surface_idx].v1, surfaces[surface_idx].v0]) # Reversed order to fix facing normals

                        mesh.from_pydata(vertices, [], triangles)
                        for tri_idx, poly in enumerate(mesh.polygons):
                            poly.use_smooth = True

                        mesh.normals_split_custom_set_from_vertices(normals)
                        for triangle_idx, triangle in enumerate(triangles):
                            if material.shader_tag_ref.name_length > 0:
                                permutation_index = ""
                                if not material.shader_permutation == 0:
                                    permutation_index = "%s" % material.shader_permutation

                                material_name = "%s%s" % (os.path.basename(material.shader_tag_ref.name), permutation_index)

                            else:
                                material_name = "invalid_material_%s" % material_idx

                            mat = bpy.data.materials.get(material_name)
                            if mat is None:
                                mat = bpy.data.materials.new(name=material_name)
                                if material.shader_tag_ref.name_length > 0:
                                    shader_processing.generate_h1_shader(mat, material.shader_tag_ref, material.shader_permutation, report)

                            if not material_name in object_mesh.data.materials.keys():
                                object_mesh.data.materials.append(mat)

                            mat.diffuse_color = random_color_gen.next()
                            material_index = object_mesh.data.materials.keys().index(material_name)
                            mesh.polygons[triangle_idx].material_index = material_index

                            render_vertex_list = [material.uncompressed_render_vertices[triangle[0]], material.uncompressed_render_vertices[triangle[1]], material.uncompressed_render_vertices[triangle[2]]]
                            for vertex_idx, vertex in enumerate(render_vertex_list):
                                loop_index = (3 * triangle_idx) + vertex_idx
                                uv_name = 'UVMap_%s' % 0
                                layer_uv = mesh.uv_layers.get(uv_name)
                                if layer_uv is None:
                                    layer_uv = mesh.uv_layers.new(name=uv_name)

                                U = vertex.UV[0]
                                V = vertex.UV[1]

                                layer_uv.data[loop_index].uv = (U, 1 - V)

                            if has_lightmap:
                                lightmap_vertex_list = [material.uncompressed_lightmap_vertices[triangle[0]], material.uncompressed_lightmap_vertices[triangle[1]], material.uncompressed_lightmap_vertices[triangle[2]]]
                                for vertex_idx, vertex in enumerate(lightmap_vertex_list):
                                    loop_index = (3 * triangle_idx) + vertex_idx
                                    uv_lightmap_name = 'UVMap_Lightmap_%s' % 0

                                    layer_uv_lightmap = mesh.uv_layers.get(uv_lightmap_name)
                                    if layer_uv_lightmap is None:
                                        layer_uv_lightmap = mesh.uv_layers.new(name=uv_lightmap_name)

                                    U_L = vertex.UV[0]
                                    V_L = vertex.UV[1]

                                    layer_uv_lightmap.data[loop_index].uv = (U_L, V_L)

                        bm.from_mesh(mesh)
                        bpy.data.meshes.remove(mesh)

                    bm.to_mesh(full_mesh)
                    bm.free()

        if len(LEVEL.cluster_portals) > 0:
            portal_bm = bmesh.new()
            portal_mesh = bpy.data.meshes.new("level_portals")
            portal_object = bpy.data.objects.new("level_portals", portal_mesh)
            portal_object.parent = level_root
            collection.objects.link(portal_object)
            portal_object.hide_set(True)
            portal_object.hide_render = True
            for cluster in LEVEL.clusters:
                for portal in cluster.portals:
                    vert_indices = []
                    cluster_portal = LEVEL.cluster_portals[portal]
                    for vertex in cluster_portal.vertices:
                        vert_indices.append(portal_bm.verts.new(vertex.translation))

                    portal_bm.faces.new(vert_indices)

                portal_bm.verts.ensure_lookup_table()
                portal_bm.faces.ensure_lookup_table()

                for portal_idx, portal in enumerate(cluster.portals):
                    cluster_portal = LEVEL.cluster_portals[portal]
                    material_list = []

                    material_name = "+portal"
                    if H1ClusterPortalFlags.ai_cant_hear_through_this in H1ClusterPortalFlags(cluster_portal.flags):
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

                    cluster_portal = LEVEL.cluster_portals[portal]
                    poly = portal_bm.faces[portal_idx]
                    plane = LEVEL.collision_bsps[0].planes[cluster_portal.plane_index]
                    if poly.normal.dot(plane.point_3d) < 0:
                        poly.flip()

            portal_bm.to_mesh(portal_mesh)
            portal_bm.free()

        for marker in LEVEL.markers:
            object_name_prefix = '#%s' % marker.name
            marker_name_override = ""
            if context.scene.objects.get('#%s' % marker.name):
                marker_name_override = marker.name

            mesh = bpy.data.meshes.new(object_name_prefix)
            object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
            collection.objects.link(object_mesh)
            object_mesh.hide_set(True)
            object_mesh.hide_render = True

            object_mesh.ass_jms.name_override = marker_name_override

            bm = bmesh.new()
            bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
            bm.to_mesh(mesh)
            bm.free()

            object_mesh.parent = level_root

            matrix_translate = Matrix.Translation(marker.translation)
            matrix_rotation = marker.rotation.to_matrix().to_4x4()

            transform_matrix = matrix_translate @ matrix_rotation
            if fix_rotations:
                transform_matrix = Matrix.Rotation(radians(90.0), 4, 'Z') @ transform_matrix

            object_mesh.matrix_world = transform_matrix
            object_mesh.data.ass_jms.Object_Type = 'SPHERE'
            object_mesh.dimensions = (2, 2, 2)

        if len(LEVEL.fog_planes) > 0:
            fog_planes_bm = bmesh.new()
            fog_planes_mesh = bpy.data.meshes.new("level_fog_planes")
            fog_planes_object = bpy.data.objects.new("level_fog_planes", fog_planes_mesh)
            fog_planes_object.parent = level_root
            collection.objects.link(fog_planes_object)
            fog_planes_object.hide_set(True)
            fog_planes_object.hide_render = True
            for fog_plane in LEVEL.fog_planes:
                vert_indices = []
                for vertex in fog_plane.vertices:
                    vert_indices.append(fog_planes_bm.verts.new(vertex.translation))

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

        if len(LEVEL.weather_polyhedras) > 0:
            material_name = "+weatherpoly"
            mat = bpy.data.materials.get(material_name)
            if mat is None:
                mat = bpy.data.materials.new(name=material_name)

            mat.diffuse_color = random_color_gen.next()
            for poly_idx, weather_polyhedra in enumerate(LEVEL.weather_polyhedras):
                tolerance = weather_polyhedra.bounding_sphere_center.magnitude * WEATHER_POLYHEDRA_TOLERANCE
                coords = planes_to_convex_hull_vert_coords([
                    (plane.point_3d, plane.distance)
                    for plane in weather_polyhedra.planes
                    ], tolerance
                    )
                if len(coords) <= 3:
                    continue

                bm = bmesh.new()
                for coord in coords:
                    bm.verts.new(coord*100)

                bmesh.ops.convex_hull(bm, input=bm.verts)
                mesh = bpy.data.meshes.new("weather_polyhedra_%d" % poly_idx)
                obj = bpy.data.objects.new("weather_polyhedra_%d" % poly_idx, mesh)
                obj.parent = level_root
                collection.objects.link(obj)
                bm.to_mesh(mesh)
                bm.free()

                if not mat in mesh.materials.values():
                    mesh.materials.append(mat)

    else:
        shader_collection_dic = {}
        shader_collection_path = os.path.join(config.HALO_2_TAG_PATH, r"scenarios\shaders\shader_collections.shader_collections")
        if os.path.isfile(shader_collection_path):
            shader_collection_file = open(shader_collection_path, "r")
            for line in shader_collection_file.readlines():
                if not global_functions.string_empty_check(line) and not line.startswith(";"):
                    split_result = line.split()
                    if len(split_result) == 2:
                        prefix = split_result[0]
                        path = split_result[1]
                        shader_collection_dic[path] = prefix

        materials = []
        for material in LEVEL.materials:
            material_path = material.shader.name
            if global_functions.string_empty_check(material_path):
                material_path = material.old_shader.name

            material_directory = os.path.dirname(material_path)
            material_name = os.path.basename(material_path)

            collection_prefix = shader_collection_dic.get(material_directory)
            if not collection_prefix == None:
                material_name = "%s %s" % (collection_prefix, material_name)
            else:
                print("Could not find a collection for: %s" % material_path)

            for material_property in material.properties:
                property_enum = PropertyTypeEnum(material_property.property_type)
                property_value = material_property.real_value
                if PropertyTypeEnum.lightmap_resolution == property_enum:
                    material_name += " lm:%s" % property_value

                elif PropertyTypeEnum.lightmap_power == property_enum:
                    material_name += " lp:%s" % property_value

                elif PropertyTypeEnum.lightmap_half_life == property_enum:
                    material_name += " hl:%s" % property_value

                elif PropertyTypeEnum.lightmap_diffuse_scale == property_enum:
                    material_name += " ds:%s" % property_value

            mat = bpy.data.materials.new(name=material_name)
            shader_processing.generate_h2_shader(mat, material.shader, report)

            materials.append(mat)

        if len(LEVEL.clusters) > 0:
            material_count = len(LEVEL.materials)
            for cluster_idx, cluster in enumerate(LEVEL.clusters):
                cluster_name = "cluster_%s" % cluster_idx
                mesh = bpy.data.meshes.new(cluster_name)
                object_mesh = bpy.data.objects.new(cluster_name, mesh)
                object_mesh.tag_view.data_type_enum = '1'

                object_mesh.parent = level_root
                mesh_processing.get_mesh_data(LEVEL, cluster.cluster_data, mesh, material_count, materials, random_color_gen, PartFlags)

                cluster_collection_override.objects.link(object_mesh)

        if len(LEVEL.instanced_geometry_instances) > 0:
            meshes = []
            for instanced_geometry_definition_idx, instanced_geometry_definition in enumerate(LEVEL.instanced_geometry_definition):
                cluster_name = "instanced_geometry_definition_%s" % instanced_geometry_definition_idx
                mesh = bpy.data.meshes.new(cluster_name)
                mesh_processing.get_mesh_data(LEVEL, instanced_geometry_definition.render_data, mesh, material_count, materials, random_color_gen, PartFlags)

                meshes.append(mesh)

            for instanced_geometry_instance_idx, instanced_geometry_instance in enumerate(LEVEL.instanced_geometry_instances):
                mesh = meshes[instanced_geometry_instance.instance_definition]
                ob_name = instanced_geometry_instance.name

                object_mesh = bpy.data.objects.new(ob_name, mesh)
                object_mesh.tag_view.data_type_enum = '16'
                object_mesh.tag_view.instance_lightmap_policy_enum = str(instanced_geometry_instance.lightmapping_policy)

                object_mesh.parent = level_root
                cluster_collection_override.objects.link(object_mesh)

                matrix_scale = Matrix.Scale(instanced_geometry_instance.scale, 4)
                matrix_rotation = Matrix()
                matrix_rotation[0] = *instanced_geometry_instance.forward, 0
                matrix_rotation[1] = *instanced_geometry_instance.left, 0
                matrix_rotation[2] = *instanced_geometry_instance.up, 0
                matrix_rotation = matrix_rotation.inverted()
                matrix_translation = Matrix.Translation(instanced_geometry_instance.position)
                transform_matrix = (matrix_translation @ matrix_rotation @ matrix_scale)
                object_mesh.matrix_world = transform_matrix

        if len(LEVEL.cluster_portals) > 0:
            portal_bm = bmesh.new()
            portal_mesh = bpy.data.meshes.new("level_portals")
            portal_object = bpy.data.objects.new("level_portals", portal_mesh)
            portal_object.parent = level_root
            collection.objects.link(portal_object)
            portal_object.hide_set(True)
            portal_object.hide_render = True
            for cluster in LEVEL.clusters:
                for portal in cluster.portals:
                    vert_indices = []
                    cluster_portal = LEVEL.cluster_portals[portal]
                    for vertex in cluster_portal.vertices:
                        vert_indices.append(portal_bm.verts.new(vertex))

                    portal_bm.faces.new(vert_indices)

                portal_bm.verts.ensure_lookup_table()
                portal_bm.faces.ensure_lookup_table()

                for portal_idx, portal in enumerate(cluster.portals):
                    cluster_portal = LEVEL.cluster_portals[portal]
                    material_list = []

                    material_name = "+portal"
                    if H2ClusterPortalFlags.ai_cant_hear_through_this in H2ClusterPortalFlags(cluster_portal.flags):
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

                    cluster_portal = LEVEL.cluster_portals[portal]
                    poly = portal_bm.faces[portal_idx]
                    plane = LEVEL.collision_bsps[0].planes[cluster_portal.plane_index]

            portal_bm.to_mesh(portal_mesh)
            portal_bm.free()

        for marker in LEVEL.markers:
            object_name_prefix = '#%s' % marker.name
            marker_name_override = ""
            if context.scene.objects.get('#%s' % marker.name):
                marker_name_override = marker.name

            mesh = bpy.data.meshes.new(object_name_prefix)
            object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
            collection.objects.link(object_mesh)
            object_mesh.hide_set(True)
            object_mesh.hide_render = True

            object_mesh.ass_jms.name_override = marker_name_override

            bm = bmesh.new()
            bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
            bm.to_mesh(mesh)
            bm.free()

            object_mesh.parent = level_root

            matrix_translate = Matrix.Translation(marker.position)
            matrix_rotation = marker.rotation.to_matrix().to_4x4()

            transform_matrix = matrix_translate @ matrix_rotation
            if fix_rotations:
                transform_matrix = Matrix.Rotation(radians(90.0), 4, 'Z') @ transform_matrix

            object_mesh.matrix_world = transform_matrix
            object_mesh.data.ass_jms.Object_Type = 'SPHERE'
            object_mesh.dimensions = (2, 2, 2)

    for bsp_idx, bsp in enumerate(LEVEL.collision_bsps):
        collision_name = "level_collision"
        collision_bm = bmesh.new()

        collision_mesh = bpy.data.meshes.new(collision_name)
        collision_object = bpy.data.objects.new(collision_name, collision_mesh)
        collection.objects.link(collision_object)
        collision_object.hide_set(True)
        collision_object.hide_render = True
        for surface_idx, surface in enumerate(bsp.surfaces):
            edge_index = surface.first_edge
            surface_edges = []
            vert_indices = []
            while edge_index not in surface_edges:
                surface_edges.append(edge_index)
                edge = bsp.edges[edge_index]
                if edge.left_surface == surface_idx:
                    vert_indices.append(collision_bm.verts.new(bsp.vertices[edge.start_vertex].translation))
                    edge_index = edge.forward_edge

                else:
                    vert_indices.append(collision_bm.verts.new(bsp.vertices[edge.end_vertex].translation))
                    edge_index = edge.reverse_edge

            is_invalid = False
            if game_title == "halo2" and H2SurfaceFlags.invalid in H2SurfaceFlags(surface.flags):
                is_invalid = True

            if not is_invalid and len(vert_indices) >= 3:
                collision_bm.faces.new(vert_indices)

        collision_bm.verts.ensure_lookup_table()
        collision_bm.faces.ensure_lookup_table()
        surface_idx = 0
        for surface in bsp.surfaces:
            is_invalid = False
            if game_title == "halo2" and H2SurfaceFlags.invalid in H2SurfaceFlags(surface.flags):
                is_invalid = True

            if not is_invalid:
                ngon_material_index = surface.material
                if not ngon_material_index == -1:
                    mat = LEVEL.collision_materials[ngon_material_index]

                if not ngon_material_index == -1:
                    if game_title == "halo1":
                        shader_path = mat.shader_tag_ref.name
                        material_name = os.path.basename(shader_path)
                    else:
                        shader_path = mat.new_shader.name

                        material_directory = os.path.dirname(shader_path)
                        material_name = os.path.basename(shader_path)

                        collection_prefix = shader_collection_dic.get(material_directory)
                        if not collection_prefix == None:
                            material_name = "%s %s" % (collection_prefix, material_name)
                        else:
                            print("Could not find a collection for: %s" % material_path)


                    if game_title == "halo1":
                        if H1SurfaceFlags.two_sided in H1SurfaceFlags(surface.flags):
                            material_name += "%"

                        if H1SurfaceFlags.invisible in H1SurfaceFlags(surface.flags):
                            material_name += "*"

                        if H1SurfaceFlags.climbable in H1SurfaceFlags(surface.flags):
                            material_name += "^"

                        if H1SurfaceFlags.breakable in H1SurfaceFlags(surface.flags):
                            material_name += "-"

                    else:
                        if H2SurfaceFlags.two_sided in H2SurfaceFlags(surface.flags):
                            material_name += "%"

                        if H2SurfaceFlags.invisible in H2SurfaceFlags(surface.flags):
                            material_name += "*"

                        if H2SurfaceFlags.climbable in H2SurfaceFlags(surface.flags):
                            material_name += "^"

                        if H2SurfaceFlags.breakable in H2SurfaceFlags(surface.flags):
                            material_name += "-"

                        if H2SurfaceFlags.conveyor in H2SurfaceFlags(surface.flags):
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
