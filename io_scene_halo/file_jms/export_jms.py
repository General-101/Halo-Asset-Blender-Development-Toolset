# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2020 Steven Garcia
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
import sys
import traceback

from decimal import *
from math import degrees
from bpy_extras import io_utils
from random import seed, randint
from mathutils import Vector, Quaternion, Matrix
from io_scene_halo.global_functions import global_functions

def get_region(default_region, region):
    set_region = None
    if not len(region) == 0:
        set_region = region

    else:
        set_region = default_region

    return set_region

def get_permutation(default_permutation, permutation):
    set_permutation = None
    if not len(permutation) == 0:
        set_permutation = permutation

    else:
        set_permutation = default_permutation

    return set_permutation

def get_default_region_permutation_name(game_version):
    default_name = None
    if game_version == 'haloce':
        default_name = 'unnamed'

    elif game_version == 'halo2':
        default_name = 'Default'

    return default_name

def get_lod(lod_setting, game_version):
    LOD_name = None
    if game_version == 'haloce':
        if lod_setting == '1':
            LOD_name = 'superlow'

        elif lod_setting == '2':
            LOD_name = 'low'

        elif lod_setting == '3':
            LOD_name = 'medium'

        elif lod_setting == '4':
            LOD_name = 'high'

        elif lod_setting == '5':
            LOD_name = 'superhigh'

    elif game_version == 'halo2':
        if lod_setting == '1':
            LOD_name = 'L1'

        elif lod_setting == '2':
            LOD_name = 'L2'

        elif lod_setting == '3':
            LOD_name = 'L3'

        elif lod_setting == '4':
            LOD_name = 'L4'

        elif lod_setting == '5':
            LOD_name = 'L5'

        elif lod_setting == '6':
            LOD_name = 'L6'

    return LOD_name

class JMSScene(global_functions.HaloAsset):
    class Node:
        def __init__(self, name, children=None, child=-1, sibling=-1, parent=-1, rotation=None, translation=None):
            self.name = name
            self.children = children
            self.child = child
            self.sibling = sibling
            self.parent = parent
            self.rotation = rotation
            self.translation = translation

    class Material:
        def __init__(self, name, texture_path=None, slot=None, lod=None, permutation=None, region=None):
            self.name = name
            self.texture_path = texture_path
            self.slot = slot
            self.lod = lod
            self.permutation = permutation
            self.region = region

    class Marker:
        def __init__(self, name, region=-1, parent=-1, rotation=None, translation=None, scale=0.0):
            self.name = name
            self.region = region
            self.parent = parent
            self.rotation = rotation
            self.translation = translation
            self.scale = scale

    class XREF:
        def __init__(self, path, name):
            self.path = path
            self.name = name

    class XREF_Marker:
        def __init__(self, name, unique_identifier=-1, index=-1, rotation=None, translation=None):
            self.name = name
            self.unique_identifier = unique_identifier
            self.index = index
            self.rotation = rotation
            self.translation = translation

    class Region:
        def __init__(self, name):
            self.name = name

    class Vertex:
        def __init__(self, node_influence_count=0, node_set=None, region=-1, translation=None, normal=None, uv_set=None):
            self.node_influence_count = node_influence_count
            self.node_set = node_set
            self.region = region
            self.translation = translation
            self.normal = normal
            self.uv_set = uv_set

    class Triangle:
        def __init__(self, region=-1, material_index=-1, v0=-1, v1=-1, v2=-1):
            self.region = region
            self.material_index = material_index
            self.v0 = v0
            self.v1 = v1
            self.v2 = v2

    class Sphere:
        def __init__(self, name, parent_index=-1, material_index=-1, rotation=None, translation=None, scale=0.0):
            self.name = name
            self.parent_index = parent_index
            self.material_index = material_index
            self.rotation = rotation
            self.translation = translation
            self.scale = scale

    class Box:
        def __init__(self, name, parent_index=-1, material_index=-1, rotation=None, translation=None, width=0.0, length=0.0, height=0.0):
            self.name = name
            self.parent_index = parent_index
            self.material_index = material_index
            self.rotation = rotation
            self.translation = translation
            self.width = width
            self.length = length
            self.height = height

    class Capsule:
        def __init__(self, name, parent_index=-1, material_index=-1, rotation=None, translation=None, height=0.0, radius=0.0):
            self.name = name
            self.parent_index = parent_index
            self.material_index = material_index
            self.rotation = rotation
            self.translation = translation
            self.height = height
            self.radius = radius

    class Convex_Shape:
        def __init__(self, name, parent_index=-1, material_index=-1, rotation=None, translation=None, verts=None):
            self.name = name
            self.parent_index = parent_index
            self.material_index = material_index
            self.rotation = rotation
            self.translation = translation
            self.verts = verts

    class Ragdoll:
        def __init__(self, name, attached_index=-1, referenced_index=-1, attached_rotation=None, attached_translation=None, referenced_rotation=None, referenced_translation=None, min_twist=0.0, max_twist=0.0, min_cone=0.0, max_cone=0.0, min_plane=0.0, max_plane=0.0):
            self.name = name
            self.attached_index = attached_index
            self.referenced_index = referenced_index
            self.attached_rotation = attached_rotation
            self.attached_translation = attached_translation
            self.referenced_rotation = referenced_rotation
            self.referenced_translation = referenced_translation
            self.min_twist = min_twist
            self.max_twist = max_twist
            self.min_cone = min_cone
            self.max_cone = max_cone
            self.min_plane = min_plane
            self.max_plane = max_plane

    class Hinge:
        def __init__(self, name, body_a_index=-1, body_b_index=-1, body_a_rotation=None, body_a_translation=None, body_b_rotation=None, body_b_translation=None, is_limited=0, friction_limit=0.0, min_angle=0.0, max_angle=0.0):
            self.name = name
            self.body_a_index = body_a_index
            self.body_b_index = body_b_index
            self.body_a_rotation = body_a_rotation
            self.body_a_translation = body_a_translation
            self.body_b_rotation = body_b_rotation
            self.body_b_translation = body_b_translation
            self.is_limited = is_limited
            self.friction_limit = friction_limit
            self.min_angle = min_angle
            self.max_angle = max_angle

    class Car_Wheel:
        def __init__(self, name, chassis_index=-1, wheel_index=-1, chassis_rotation=None, chassis_translation=None, wheel_rotation=None, wheel_translation=None, suspension_rotation=None, suspension_translation=None, suspension_min_limit=0.0, suspension_max_limit=0.0, friction_limit=0.0, velocity=0.0, gain=0.0):
            self.name = name
            self.chassis_index = chassis_index
            self.wheel_index = wheel_index
            self.chassis_rotation = chassis_rotation
            self.chassis_translation = chassis_translation
            self.wheel_rotation = wheel_rotation
            self.wheel_translation = wheel_translation
            self.suspension_rotation = suspension_rotation
            self.suspension_translation = suspension_translation
            self.suspension_min_limit = suspension_min_limit
            self.suspension_max_limit = suspension_max_limit
            self.friction_limit = friction_limit
            self.velocity = velocity
            self.gain = gain

    class Point_to_Point:
        def __init__(self, name, body_a_index=-1, body_b_index=-1, body_a_rotation=None, body_a_translation=None, body_b_rotation=None, body_b_translation=None, constraint_type=0, x_min_limit=0.0, x_max_limit=0.0, y_min_limit=0.0, y_max_limit=0.0, z_min_limit=0.0, z_max_limit=0.0, spring_length=0.0):
            self.name = name
            self.body_a_index = body_a_index
            self.body_b_index = body_b_index
            self.body_a_rotation = body_a_rotation
            self.body_a_translation = body_a_translation
            self.body_b_rotation = body_b_rotation
            self.body_b_translation = body_b_translation
            self.constraint_type = constraint_type
            self.x_min_limit = x_min_limit
            self.x_max_limit = x_max_limit
            self.y_min_limit = y_min_limit
            self.y_max_limit = y_max_limit
            self.z_min_limit = z_min_limit
            self.z_max_limit = z_max_limit
            self.spring_length = spring_length

    class Prismatic:
        def __init__(self, name, body_a_index=-1, body_b_index=-1, body_a_rotation=None, body_a_translation=None, body_b_rotation=None, body_b_translation=None, is_limited=0, suspension_max_limit=0.0, friction_limit=0.0, min_limit=0.0, max_limit=0.0):
            self.name = name
            self.body_a_index = body_a_index
            self.body_b_index = body_b_index
            self.body_a_rotation = body_a_rotation
            self.body_a_translation = body_a_translation
            self.body_b_rotation = body_b_rotation
            self.body_b_translation = body_b_translation
            self.is_limited = is_limited
            self.friction_limit = friction_limit
            self.min_limit = min_limit
            self.max_limit = max_limit

    class Bounding_Sphere:
        def __init__(self, translation=None, scale=0.0):
            self.translation = translation
            self.scale = scale

    def __init__(self, context, report, version, game_version, apply_modifiers, hidden_geo, export_render, export_collision, export_physics, custom_scale, object_list):
        self.gen_2 = ['halo2']
        scene = bpy.context.scene
        view_layer = bpy.context.view_layer
        armature = None
        armature_count = 0
        mesh_frame_count = 0
        default_region = get_default_region_permutation_name(game_version)
        default_permutation = get_default_region_permutation_name(game_version)
        region_list = ['unnamed']
        permutation_list = []
        self.nodes = []
        self.materials = []
        self.markers = []
        self.xref_instances = []
        self.xref_markers = []
        self.regions = []
        self.geometry_list = []
        self.original_geometry_list = []
        self.triangles = []
        self.vertices = []
        self.spheres = []
        self.boxes = []
        self.capsules = []
        self.convex_shapes = []
        self.ragdolls = []
        self.hinges = []
        self.car_wheels = []
        self.point_to_points = []
        self.prismatics = []
        self.bounding_spheres = []
        node_list = []
        material_list = []
        marker_list = []
        instance_xref_paths  = []
        instance_markers = []
        geometry_list = []
        original_geometry_list = []
        sphere_list = []
        box_list = []
        capsule_list = []
        convex_shape_list = []
        ragdoll_list = []
        hinge_list = []
        car_wheel_list = []
        point_to_point_list = []
        prismatic_list = []
        bounding_sphere_list = []
        depsgraph = context.evaluated_depsgraph_get()
        node_prefix_tuple = ('b ', 'b_', 'bone', 'frame', 'bip01')
        for obj in object_list:
            name = obj.name.lower()
            parent_name = None
            if obj.parent:
                parent_name = obj.parent.name.lower()

            if obj.type == 'ARMATURE':
                global_functions.unhide_object(obj)
                armature_count += 1
                armature = obj
                node_list = list(obj.data.bones)

            elif name.startswith(node_prefix_tuple):
                global_functions.unhide_object(obj)
                node_list.append(obj)
                mesh_frame_count += 1

            elif obj.name[0:1].lower() == '#':
                if global_functions.set_ignore(obj) == False or hidden_geo:
                    if not obj.parent == None:
                        if obj.parent.type == 'ARMATURE' or parent_name.startswith(node_prefix_tuple):
                            marker_list.append(obj)

            elif obj.name[0:1].lower() == '@' and len(obj.data.polygons) > 0:
                if global_functions.set_ignore(obj) == False or hidden_geo:
                    if export_collision:
                        if not obj.parent == None:
                            if obj.parent.type == 'ARMATURE' or parent_name.startswith(node_prefix_tuple):
                                if apply_modifiers:
                                    obj_for_convert = obj.evaluated_get(depsgraph)
                                    me = obj_for_convert.to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)
                                    geometry_list.append(me)
                                    original_geometry_list.append(obj)

                                else:
                                    geometry_list.append(obj.to_mesh(preserve_all_data_layers=True))
                                    original_geometry_list.append(obj)

            elif obj.name[0:1].lower() == '$' and version > 8205:
                if global_functions.set_ignore(obj) == False or hidden_geo:
                    if export_physics:
                        if not obj.rigid_body_constraint == None:
                            if obj.rigid_body_constraint.type == 'HINGE':
                                hinge_list.append(obj)

                            elif obj.rigid_body_constraint.type == 'GENERIC':
                                ragdoll_list.append(obj)

                            elif obj.rigid_body_constraint.type == 'GENERIC_SPRING':
                                point_to_point_list.append(obj)

                        if obj.type == 'MESH':
                            if obj.data.ass_jms.Object_Type == 'SPHERE':
                                sphere_list.append(obj)

                            elif obj.data.ass_jms.Object_Type == 'BOX':
                                box_list.append(obj)

                            elif obj.data.ass_jms.Object_Type == 'CAPSULES':
                                capsule_list.append(obj)

                            elif obj.data.ass_jms.Object_Type == 'CONVEX SHAPES':
                                convex_shape_list.append(obj)

            elif obj.type == 'MESH' and not len(obj.data.ass_jms.XREF_path) == 0 and version > 8205:
                if global_functions.set_ignore(obj) == False or hidden_geo:
                    if export_render:
                        instance_markers.append(obj)
                        if not obj.data.ass_jms.XREF_path in instance_xref_paths:
                            instance_xref_paths.append(obj.data.ass_jms.XREF_path)

            elif obj.type == 'MESH' and obj.data.ass_jms.bounding_radius == True and version >= 8209:
                if global_functions.set_ignore(obj) == False or hidden_geo:
                    if export_render:
                        bounding_sphere_list.append(obj)

            elif obj.type == 'MESH' and len(obj.data.polygons) > 0:
                if global_functions.set_ignore(obj) == False or hidden_geo:
                    if export_render:
                        if not obj.parent == None:
                            if obj.parent.type == 'ARMATURE' or parent_name.startswith(node_prefix_tuple):
                                if apply_modifiers:
                                    obj_for_convert = obj.evaluated_get(depsgraph)
                                    me = obj_for_convert.to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)
                                    geometry_list.append(me)
                                    original_geometry_list.append(obj)

                                else:
                                    geometry_list.append(obj.to_mesh(preserve_all_data_layers=True))
                                    original_geometry_list.append(obj)

        root_node_count = global_functions.count_root_nodes(node_list)
        node_count = len(node_list)

        if game_version == 'haloce' and node_count == 0: #JMSv2 files can have JMS files without a node for physics.
            raise global_functions.SceneParseError("No nodes in scene. Add an armature or object mesh named frame.")

        elif root_node_count >= 2:
            raise global_functions.SceneParseError("More than one root node. Please remove or rename objects until you only have one root frame object.")

        elif len(object_list) == 0:
            raise global_functions.SceneParseError("No objects in scene.")

        elif mesh_frame_count > 0 and armature_count > 0:
            raise global_functions.SceneParseError("Using both armature and object mesh node setup. Choose one or the other.")

        elif game_version == 'haloce' and len(geometry_list) == 0 and len(marker_list) == 0:
            raise global_functions.SceneParseError("No geometry in scene.")

        elif game_version == 'haloce' and version >= 8201:
            raise global_functions.SceneParseError("This version is not supported for Halo CE. Choose from 8197-8200 if you wish to export for Halo CE.")

        elif game_version == 'halo2' and version >= 8211:
            raise global_functions.SceneParseError("This version is not supported for Halo 2. Choose from 8197-8210 if you wish to export for Halo 2.")

        elif game_version == 'haloce' and node_count > 64:
            raise global_functions.SceneParseError("This model has more nodes than Halo CE supports. Please limit your node count to 64 nodes")

        elif game_version == 'halo2' and node_count > 255:
            raise global_functions.SceneParseError("This model has more nodes than Halo 2 supports. Please limit your node count to 255 nodes")

        sorted_list = global_functions.sort_list(node_list, armature, game_version, version, False)
        joined_list = sorted_list[0]
        reversed_joined_list = sorted_list[1]
        self.node_checksum = 0
        for node in joined_list:
            is_bone = False
            if armature:
                is_bone = True

            find_child_node = global_functions.get_child(node, reversed_joined_list)
            find_sibling_node = global_functions.get_sibling(armature, node, reversed_joined_list)

            first_child_node = -1
            first_sibling_node = -1
            parent_node = -1

            if not find_child_node == None:
                first_child_node = joined_list.index(find_child_node)
            if not find_sibling_node == None:
                first_sibling_node = joined_list.index(find_sibling_node)
            if not node.parent == None:
                parent_node = joined_list.index(node.parent)

            bone_matrix = global_functions.get_matrix(node, node, True, armature, joined_list, True, version, 'JMS', 0)
            mesh_dimensions = global_functions.get_dimensions(bone_matrix, node, None, None, custom_scale, version, None, False, is_bone, armature, 'JMS')

            name = node.name
            child = first_child_node
            sibling = first_sibling_node
            parent = parent_node

            current_node_children = []
            children = []
            for child_node in node.children:
                if child_node in joined_list:
                    current_node_children.append(child_node.name)

            current_node_children.sort()

            if is_bone:
                for child_node in current_node_children:
                    children.append(joined_list.index(armature.data.bones[child_node]))
            else:
                for child_node in current_node_children:
                    children.append(joined_list.index(bpy.data.objects[child_node]))

            rotation = (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a)
            translation = (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a)

            self.nodes.append(JMSScene.Node(name, children, child, sibling, parent, rotation, translation))

        self.node_checksum = global_functions.node_hierarchy_checksum(self.nodes, self.nodes[0], self.node_checksum)

        for marker in marker_list:
            untouched_name = marker.name.split('#', 1)[1] #remove marker symbol from name
            name = untouched_name.rsplit('.', 1)[0] #remove name change from duplicating objects in Blender

            region_idx = -1
            if marker.face_maps.active:
                region_face_map_name = marker.face_maps[0].name
                if not region_face_map_name in region_list:
                    region_list.append(region_face_map_name)

                region_idx = region_list.index(region_face_map_name)

            parent_idx = global_functions.get_parent(armature, marker, joined_list, 0)
            marker_matrix = global_functions.get_matrix(marker, marker, True, armature, joined_list, False, version, 'JMS', 0)
            mesh_dimensions = global_functions.get_dimensions(marker_matrix, marker, None, None, custom_scale, version, None, False, False, armature, 'JMS')

            rotation = (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a)
            translation = (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a)
            scale = (mesh_dimensions.radius_a)

            self.markers.append(JMSScene.Marker(name, region_idx, parent_idx[0], rotation, translation, scale))

        for xref_path in instance_xref_paths:
            path = bpy.path.abspath(xref_path)
            name = os.path.basename(xref_path).rsplit('.', 1)[0]

            self.xref_instances.append(JMSScene.XREF(path, name))

        seed(1)
        starting_ID = -1 * (randint(0, 3000000000))
        for idx, int_markers in enumerate(instance_markers):
            name = int_markers.name
            unique_identifier = starting_ID - idx
            index = instance_xref_paths.index(int_markers.data.ass_jms.XREF_path)
            int_markers_matrix = global_functions.get_matrix(int_markers, int_markers, False, armature, joined_list, False, version, 'JMS', 0)
            mesh_dimensions = global_functions.get_dimensions(int_markers_matrix, int_markers, None, None, custom_scale, version, None, False, False, armature, 'JMS')

            rotation = (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a)
            translation = (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a)

            self.xref_markers.append(JMSScene.XREF_Marker(name, unique_identifier, index, rotation, translation))

        for idx, geometry in enumerate(geometry_list):
            original_geo = original_geometry_list[idx]
            vertex_groups = original_geo.vertex_groups.keys()
            original_geo_matrix = global_functions.get_matrix(original_geo, original_geo, False, armature, joined_list, False, version, 'JMS', 0)
            for idx, face in enumerate(geometry.polygons):
                region_index = -1
                region = default_region
                permutation = default_permutation
                if game_version == 'haloce':
                    region_face_map_name = default_region
                    region_index = region_list.index(region_face_map_name)
                    if geometry.face_maps.active:
                        face_map_idx = geometry.face_maps.active.data[idx].value
                        if not face_map_idx == -1:
                            region_face_map_name = original_geo.face_maps[face_map_idx].name
                            if not region_face_map_name in region_list:
                                region_list.append(region_face_map_name)

                        region_index = region_list.index(region_face_map_name)

                elif game_version == 'halo2':
                    if geometry.face_maps.active:
                        region_permutation_face_map_name = [default_permutation, default_region]
                        face_map_idx = geometry.face_maps.active.data[idx].value
                        if not face_map_idx == -1:
                            region_permutation_face_map_name = original_geo.face_maps[face_map_idx].name.split()

                        if len(region_permutation_face_map_name) > 0:
                            permutation = region_permutation_face_map_name[0]
                        if not permutation in permutation_list:
                            permutation_list.append(permutation)

                        if len(region_permutation_face_map_name) > 1:
                            region = region_permutation_face_map_name[1]
                        if not region in region_list:
                            region_list.append(region)

                material = global_functions.get_material(game_version, original_geo, face, geometry, material_list, 'JMS', region, permutation,)
                material_index = -1
                if not material == -1:
                    material_list = global_functions.gather_materials(game_version, material, material_list, 'JMS', region, permutation, original_geo.data.ass_jms.level_of_detail)
                    material_index = material_list.index(material)

                v0 = len(self.vertices)
                v1 = len(self.vertices) + 1
                v2 = len(self.vertices) + 2

                self.triangles.append(JMSScene.Triangle(region_index, material_index, v0, v1, v2))
                for loop_index in face.loop_indices:
                    vert = geometry.vertices[geometry.loops[loop_index].vertex_index]
                    translation = original_geo_matrix @ vert.co
                    normal = original_geo_matrix @ (vert.co + vert.normal) - translation
                    region = region_index
                    uv_set = []
                    for uv_index in range(len(geometry.uv_layers)):
                        geometry.uv_layers.active = geometry.uv_layers[uv_index]
                        uv = geometry.uv_layers.active.data[geometry.loops[loop_index].index].uv
                        uv_set.append(uv)

                    if not uv_set and version <= 8204:
                        uv_set = [(0.0, 0.0)]

                    uv = uv_set
                    if len(vert.groups) != 0:
                        object_vert_group_list = []
                        vertex_vert_group_list = []
                        for group_index in range(len(vert.groups)):
                            vert_group = vert.groups[group_index].group
                            object_vertex_group = vertex_groups[vert_group]
                            if armature:
                                if object_vertex_group in armature.data.bones:
                                    vertex_vert_group_list.append(group_index)
                                    if armature.data.bones[object_vertex_group] in joined_list:
                                        object_vert_group_list.append(vert_group)

                            else:
                                if object_vertex_group in bpy.data.objects:
                                    vertex_vert_group_list.append(group_index)
                                    if bpy.data.objects[object_vertex_group] in joined_list:
                                        object_vert_group_list.append(vert_group)

                        value = len(object_vert_group_list)
                        if value > 4:
                            value = 4

                        node_influence_count = int(value)
                        node_set = []
                        if len(object_vert_group_list) != 0:
                            for idx, group_index in enumerate(object_vert_group_list):
                                vert_index = int(vertex_vert_group_list[idx])
                                vert_group = vert.groups[vert_index].group
                                object_vertex_group = vertex_groups[vert_group]
                                if armature:
                                    node_obj = armature.data.bones[object_vertex_group]

                                else:
                                    node_obj = bpy.data.objects[object_vertex_group]

                                node_index = int(joined_list.index(node_obj))
                                node_weight = float(vert.groups[vert_index].weight)
                                node_set.append([node_index, node_weight])

                        else:
                            node_set = []
                            parent_index = global_functions.get_parent(armature, original_geo, joined_list, 0)
                            node_influence_count = int(1)
                            node_index = int(parent_index[0])
                            node_weight = float(1.0000000000)
                            node_set.append([node_index, node_weight])

                    else:
                        node_set = []
                        parent_index = global_functions.get_parent(armature, original_geo, joined_list, 0)
                        node_influence_count = int(1)
                        node_index = int(parent_index[0])
                        node_weight = float(1.0000000000)
                        node_set.append([node_index, node_weight])

                    self.vertices.append(JMSScene.Vertex(node_influence_count, node_set, region, translation, normal, uv_set))

        for spheres in sphere_list:
            name = spheres.name.split('$', 1)[1]
            mesh_sphere = spheres.to_mesh()
            face = mesh_sphere.polygons[0]

            region = default_region
            permutation = default_permutation
            if spheres.face_maps.active:
                region_permutation_face_map_name = spheres.face_maps[0].name.split()
                if len(region_permutation_face_map_name) > 0:
                    permutation = region_permutation_face_map_name[0]
                if not permutation in permutation_list:
                    permutation_list.append(permutation)

                if len(region_permutation_face_map_name) > 1:
                    region = region_permutation_face_map_name[1]
                if not region in region_list:
                    region_list.append(region)

            material = global_functions.get_material(game_version, spheres, face, mesh_sphere, material_list, 'JMS', region, permutation,)
            material_index = -1
            if not material == -1:
                material_list = global_functions.gather_materials(game_version, material, material_list, 'JMS', region, permutation, spheres.data.ass_jms.level_of_detail)
                material_index = material_list.index(material)

            parent_index = global_functions.get_parent(armature, spheres, joined_list, -1)
            sphere_matrix = global_functions.get_matrix(spheres, spheres, True, armature, joined_list, False, version, 'JMS', 0)
            mesh_dimensions = global_functions.get_dimensions(sphere_matrix, spheres, None, None, custom_scale, version, None, False, False, armature, 'JMS')

            rotation = (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a)
            translation = (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a)
            scale = (mesh_dimensions.radius_a)

            self.spheres.append(JMSScene.Sphere(name, parent_index[0], material_index, rotation, translation, scale))

        for boxes in box_list:
            name = boxes.name.split('$', 1)[1]
            mesh_boxes = boxes.to_mesh()
            face = mesh_boxes.polygons[0]

            region = default_region
            permutation = default_permutation
            if boxes.face_maps.active:
                region_permutation_face_map_name = boxes.face_maps[0].name.split()
                if len(region_permutation_face_map_name) > 0:
                    permutation = region_permutation_face_map_name[0]
                if not permutation in permutation_list:
                    permutation_list.append(permutation)

                if len(region_permutation_face_map_name) > 1:
                    region = region_permutation_face_map_name[1]
                if not region in region_list:
                    region_list.append(region)

            material = global_functions.get_material(game_version, boxes, face, mesh_boxes, material_list, 'JMS', region, permutation,)
            material_index = -1
            if not material == -1:
                material_list = global_functions.gather_materials(game_version, material, material_list, 'JMS', region, permutation, boxes.data.ass_jms.level_of_detail)
                material_index = material_list.index(material)

            parent_index = global_functions.get_parent(armature, boxes, joined_list, -1)
            box_matrix = global_functions.get_matrix(boxes, boxes, True, armature, joined_list, False, version, 'JMS', 0)
            mesh_dimensions = global_functions.get_dimensions(box_matrix, boxes, None, None, custom_scale, version, None, False, False, armature, 'JMS')

            rotation = (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a)
            translation = (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a)
            width = (mesh_dimensions.dimension_x_a)
            length = (mesh_dimensions.dimension_y_a)
            height = (mesh_dimensions.dimension_z_a)

            self.boxes.append(JMSScene.Box(name, parent_index[0], material_index, rotation, translation, width, length, height))

        for capsule in capsule_list:
            name = capsule.name.split('$', 1)[1]
            mesh_capsule = capsule.to_mesh()
            face = mesh_capsule.polygons[0]

            region = default_region
            permutation = default_permutation
            if capsule.face_maps.active:
                region_permutation_face_map_name = capsule.face_maps[0].name.split()
                if len(region_permutation_face_map_name) > 0:
                    permutation = region_permutation_face_map_name[0]
                if not permutation in permutation_list:
                    permutation_list.append(permutation)

                if len(region_permutation_face_map_name) > 1:
                    region = region_permutation_face_map_name[1]
                if not region in region_list:
                    region_list.append(region)

            material = global_functions.get_material(game_version, capsule, face, mesh_capsule, material_list, 'JMS', region, permutation,)
            material_index = -1
            if not material == -1:
                material_list = global_functions.gather_materials(game_version, material, material_list, 'JMS', region, permutation, capsule.data.ass_jms.level_of_detail)
                material_index = material_list.index(material)

            parent_index = global_functions.get_parent(armature, capsule, joined_list, -1)
            capsule_matrix = global_functions.get_matrix(capsule, capsule, True, armature, joined_list, False, version, 'JMS', 0)
            mesh_dimensions = global_functions.get_dimensions(capsule_matrix, capsule, None, None, custom_scale, version, None, False, False, armature, 'JMS')

            rotation = (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a)
            translation = (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a)
            height = (mesh_dimensions.pill_z_a)
            scale = (mesh_dimensions.radius_a)

            self.capsules.append(JMSScene.Capsule(name, parent_index[0], material_index, rotation, translation, height, scale))

        for convex_shape in convex_shape_list:
            verts = []
            name = convex_shape.name.split('$', 1)[1]
            if apply_modifiers:
                convex_shape_for_convert = convex_shape.evaluated_get(depsgraph)
                mesh_convex_shape = convex_shape_for_convert.to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)

            else:
                mesh_convex_shape = convex_shape.to_mesh(preserve_all_data_layers=True)

            face = mesh_convex_shape.polygons[0]

            region = default_region
            permutation = default_permutation
            if convex_shape.face_maps.active:
                region_permutation_face_map_name = convex_shape.face_maps[0].name.split()
                if len(region_permutation_face_map_name) > 0:
                    permutation = region_permutation_face_map_name[0]
                if not permutation in permutation_list:
                    permutation_list.append(permutation)

                if len(region_permutation_face_map_name) > 1:
                    region = region_permutation_face_map_name[1]
                if not region in region_list:
                    region_list.append(region)

            material = global_functions.get_material(game_version, convex_shape, face, mesh_convex_shape, material_list, 'JMS', region, permutation,)
            material_index = -1
            if not material == -1:
                material_list = global_functions.gather_materials(game_version, material, material_list, 'JMS', region, permutation, convex_shape.data.ass_jms.level_of_detail)
                material_index = material_list.index(material)

            parent_index = global_functions.get_parent(armature, convex_shape, joined_list, -1)
            convex_matrix = global_functions.get_matrix(convex_shape, convex_shape, True, armature, joined_list, False, version, 'JMS', 0)

            mesh_dimensions = global_functions.get_dimensions(convex_matrix, convex_shape, None, None, custom_scale, version, None, False, False, armature, 'JMS')

            rotation = (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a)
            translation = (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a)
            for vertex in mesh_convex_shape.vertices:
                pos  = vertex.co
                mesh_dimensions = global_functions.get_dimensions(None, None, None, None, custom_scale, version, pos, True, False, armature, 'JMS')
                vert_translation = (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a)

                verts.append(JMSScene.Vertex(None, None, None, vert_translation, None, None))

            self.convex_shapes.append(JMSScene.Convex_Shape(name, parent_index[0], material_index, rotation, translation, verts))

        for region in region_list:
            name = region

            self.regions.append(JMSScene.Region(name))

        for material in material_list:
            name = None
            texture_path = None
            slot = None
            lod = None
            permutation = default_permutation
            region = default_region
            if game_version == 'haloce':
                name = '<none>'
                texture_path = '<none>'
                if not material == None:
                    name = material.name
                    if not material.node_tree == None:
                        for node in material.node_tree.nodes:
                            if node.type == 'TEX_IMAGE':
                                if not node.image == None:
                                    image_filepath = bpy.path.abspath(node.image.filepath)
                                    image_path = image_filepath.rsplit('.', 1)[0]
                                    image_name = bpy.path.basename(image_path)
                                    tex = image_name
                                    if version >= 8200:
                                        tex = image_path

                                    texture_path = tex

            elif game_version in self.gen_2:
                name = material[0].name
                slot = bpy.data.materials.find(material[0].name)
                lod = get_lod(material[1], game_version)
                #This doesn't matter for CE but for Halo 2 the region or permutation names can't have any whitespace.
                #Lets fix that here to make sure nothing goes wrong.
                if len(material[2]) != 0:
                    region = material[2].replace(' ', '_').replace('\t', '_')

                if len(material[3]) != 0:
                    permutation = material[3].replace(' ', '_').replace('\t', '_')

            self.materials.append(JMSScene.Material(name, texture_path, slot, lod, permutation, region))

        for ragdoll in ragdoll_list:
            body_a_obj = ragdoll.rigid_body_constraint.object1
            body_b_obj = ragdoll.rigid_body_constraint.object2
            body_a_name = 'Null'
            body_b_name = 'Null'
            if body_a_obj:
                body_a_name = body_a_obj.name.split('$', 1)[1]

            if body_b_obj:
                body_b_name = body_b_obj.name.split('$', 1)[1]

            name = 'ragdoll:%s:%s' % (body_a_name, body_b_name)
            attached_index = global_functions.get_parent(armature, body_a_obj, joined_list, -1)
            referenced_index = global_functions.get_parent(armature, body_b_obj, joined_list, -1)
            body_a_matrix = global_functions.get_matrix(ragdoll, body_a_obj, True, armature, joined_list, False, version, 'JMS', 1)
            body_b_matrix = global_functions.get_matrix(ragdoll, body_b_obj, True, armature, joined_list, False, version, 'JMS', 1)
            mesh_dimensions = global_functions.get_dimensions(body_a_matrix, body_a_obj, body_b_matrix, body_b_obj, custom_scale, version, None, False, False, armature, 'JMS')
            is_limited_x = int(ragdoll.rigid_body_constraint.use_limit_ang_x)
            is_limited_y = int(ragdoll.rigid_body_constraint.use_limit_ang_y)
            is_limited_z = int(ragdoll.rigid_body_constraint.use_limit_ang_z)
            min_twist = 0
            max_twist = 0
            if is_limited_x:
                min_twist = degrees(ragdoll.rigid_body_constraint.limit_ang_x_lower)
                max_twist = degrees(ragdoll.rigid_body_constraint.limit_ang_x_upper)

            min_cone = 0
            max_cone = 0
            if is_limited_y:
                min_cone = degrees(ragdoll.rigid_body_constraint.limit_ang_y_lower)
                max_cone = degrees(ragdoll.rigid_body_constraint.limit_ang_y_upper)

            min_plane = 0
            max_plane = 0
            if is_limited_z:
                min_plane = degrees(ragdoll.rigid_body_constraint.limit_ang_z_lower)
                max_plane = degrees(ragdoll.rigid_body_constraint.limit_ang_z_upper)

            attached_rotation = (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a)
            attached_translation = (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a)
            referenced_rotation = (mesh_dimensions.quat_i_b, mesh_dimensions.quat_j_b, mesh_dimensions.quat_k_b, mesh_dimensions.quat_w_b)
            referenced_translation = (mesh_dimensions.pos_x_b, mesh_dimensions.pos_y_b, mesh_dimensions.pos_z_b)

            self.ragdolls.append(JMSScene.Ragdoll(name, attached_index[0], referenced_index[0], attached_rotation, attached_translation, referenced_rotation, referenced_translation, min_twist, max_twist, min_cone, max_cone, min_plane, max_plane))

        for hinge in hinge_list:
            body_a_obj = hinge.rigid_body_constraint.object1
            body_b_obj = hinge.rigid_body_constraint.object2
            body_a_name = 'Null'
            body_b_name = 'Null'
            if body_a_obj:
                body_a_name = body_a_obj.name.split('$', 1)[1]

            if body_b_obj:
                body_b_name = body_b_obj.name.split('$', 1)[1]

            name = 'hinge:%s:%s' % (body_a_name, body_b_name)
            body_a_index = global_functions.get_parent(armature, body_a_obj, joined_list, -1)
            body_b_index = global_functions.get_parent(armature, body_b_obj, joined_list, -1)
            body_a_matrix = global_functions.get_matrix(hinge, body_a_obj, True, armature, joined_list, False, version, 'JMS', 1)
            body_b_matrix = global_functions.get_matrix(hinge, body_b_obj, True, armature, joined_list, False, version, 'JMS', 1)
            mesh_dimensions = global_functions.get_dimensions(body_a_matrix, body_a_obj, body_b_matrix, body_b_obj, custom_scale, version, None, False, False, armature, 'JMS')
            friction_limit = 0
            if body_b_obj:
                friction_limit = body_b_obj.rigid_body.angular_damping

            min_angle = 0
            max_angle = 0
            is_limited = int(hinge.rigid_body_constraint.use_limit_ang_z)
            if is_limited:
                min_angle = degrees(hinge.rigid_body_constraint.limit_ang_z_lower)
                max_angle = degrees(hinge.rigid_body_constraint.limit_ang_z_upper)

            body_a_rotation = (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a)
            body_a_translation = (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a)
            body_b_rotation = (mesh_dimensions.quat_i_b, mesh_dimensions.quat_j_b, mesh_dimensions.quat_k_b, mesh_dimensions.quat_w_b)
            body_b_translation = (mesh_dimensions.pos_x_b, mesh_dimensions.pos_y_b, mesh_dimensions.pos_z_b)

            self.hinges.append(JMSScene.Hinge(name, body_a_index[0], body_b_index[0], body_a_rotation, body_a_translation, body_b_rotation, body_b_translation, is_limited, friction_limit, min_angle, max_angle))

        for car_wheel in car_wheel_list:
            chassis_obj = car_wheel.rigid_body_constraint.object1
            wheel_obj = car_wheel.rigid_body_constraint.object2
            chassis_name = 'Null'
            wheel_name = 'Null'
            if chassis_obj:
                chassis_name = chassis_obj.name.split('$', 1)[1]

            if wheel_obj:
                wheel_name = wheel_obj.name.split('$', 1)[1]

            name = 'hinge:%s:%s' % (chassis_name, wheel_name)
            chassis_index = global_functions.get_parent(armature, chassis_obj, joined_list, -1)
            wheel_index = global_functions.get_parent(armature, wheel_obj, joined_list, -1)
            chassis_matrix = global_functions.get_matrix(hinge, chassis_obj, True, armature, joined_list, False, version, 'JMS', 1)
            wheel_matrix = global_functions.get_matrix(hinge, wheel_obj, True, armature, joined_list, False, version, 'JMS', 1)
            mesh_dimensions = global_functions.get_dimensions(chassis_matrix, chassis_obj, wheel_matrix, wheel_obj, custom_scale, version, None, False, False, armature, 'JMS')
            suspension_min_limit = 0
            suspension_max_limit = 0
            if wheel_obj:
                suspension_min_limit = 0
                suspension_max_limit = 0

            friction_limit = 0
            velocity = 0
            gain = 0

            chassis_rotation = (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a)
            chassis_translation = (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a)
            wheel_rotation = (mesh_dimensions.quat_i_b, mesh_dimensions.quat_j_b, mesh_dimensions.quat_k_b, mesh_dimensions.quat_w_b)
            wheel_translation = (mesh_dimensions.pos_x_b, mesh_dimensions.pos_y_b, mesh_dimensions.pos_z_b)
            suspension_rotation = (mesh_dimensions.quat_i_b, mesh_dimensions.quat_j_b, mesh_dimensions.quat_k_b, mesh_dimensions.quat_w_b)
            suspension_translation = (mesh_dimensions.pos_x_b, mesh_dimensions.pos_y_b, mesh_dimensions.pos_z_b)

            self.car_wheels.append(JMSScene.Car_Wheel(name, chassis_index[0], wheel_index[0], chassis_rotation, chassis_translation, wheel_rotation, wheel_translation, suspension_rotation, suspension_translation, suspension_min_limit, suspension_max_limit, friction_limit, velocity, gain))

        for point_to_point in point_to_point_list:
            body_a_obj = point_to_point.rigid_body_constraint.object1
            body_b_obj = point_to_point.rigid_body_constraint.object2
            body_a_name = 'Null'
            body_b_name = 'Null'
            body_a_matrix = Matrix.Translation((0, 0, 0))
            body_b_matrix = Matrix.Translation((0, 0, 0))
            if body_a_obj:
                body_a_name = body_a_obj.name.split('$', 1)[1]
                body_a_matrix = global_functions.get_matrix(point_to_point, body_a_obj, True, armature, joined_list, False, version, 'JMS', 1)

            if body_b_obj:
                body_b_name = body_b_obj.name.split('$', 1)[1]
                body_b_matrix = global_functions.get_matrix(point_to_point, body_b_obj, True, armature, joined_list, False, version, 'JMS', 1)

            name = 'point_to_point:%s:%s' % (body_a_name, body_b_name)
            body_a_index = global_functions.get_parent(armature, body_a_obj, joined_list, -1)
            body_b_index = global_functions.get_parent(armature, body_b_obj, joined_list, -1)
            mesh_dimensions = global_functions.get_dimensions(body_a_matrix, point_to_point, body_b_matrix, point_to_point, custom_scale, version, None, False, False, armature, 'JMS')

            constraint_type = int(point_to_point.jms.jms_spring_type)
            x_min_limit = degrees(-45.0)
            x_max_limit = degrees(45.0)
            if point_to_point.rigid_body_constraint.use_limit_ang_x is True and constraint_type == 1:
                x_min_limit = degrees(point_to_point.rigid_body_constraint.limit_ang_x_lower)
                x_max_limit = degrees(point_to_point.rigid_body_constraint.limit_ang_x_upper)

            y_min_limit = degrees(-45.0)
            y_max_limit = degrees(45.0)
            if point_to_point.rigid_body_constraint.use_limit_ang_y is True and constraint_type == 1:
                y_min_limit = degrees(point_to_point.rigid_body_constraint.limit_ang_y_lower)
                y_max_limit = degrees(point_to_point.rigid_body_constraint.limit_ang_y_upper)

            z_min_limit = degrees(-45.0)
            z_max_limit = degrees(45.0)
            if point_to_point.rigid_body_constraint.use_limit_ang_z is True and constraint_type == 1:
                z_min_limit = degrees(point_to_point.rigid_body_constraint.limit_ang_z_lower)
                z_max_limit = degrees(point_to_point.rigid_body_constraint.limit_ang_z_upper)

            spring_length = float(0.0)
            if point_to_point.rigid_body_constraint.use_limit_lin_z is True and constraint_type == 2:
                spring_length = float(point_to_point.rigid_body_constraint.limit_lin_z_upper)

            body_a_rotation = (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a)
            body_a_translation = (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a)
            body_b_rotation = (mesh_dimensions.quat_i_b, mesh_dimensions.quat_j_b, mesh_dimensions.quat_k_b, mesh_dimensions.quat_w_b)
            body_b_translation = (mesh_dimensions.pos_x_b, mesh_dimensions.pos_y_b, mesh_dimensions.pos_z_b)

            self.point_to_points.append(JMSScene.Point_to_Point(name, body_a_index[0], body_b_index[0], body_a_rotation, body_a_translation, body_b_rotation, body_b_translation, constraint_type, x_min_limit, x_max_limit, y_min_limit, y_max_limit, z_min_limit, z_max_limit, spring_length))

        for prismatic in prismatic_list:
            body_a_obj = prismatic.rigid_body_constraint.object1
            body_b_obj = prismatic.rigid_body_constraint.object2
            body_a_name = 'Null'
            body_b_name = 'Null'
            if body_a_obj:
                body_a_name = chassis_obj.name.split('$', 1)[1]

            if body_b_obj:
                body_b_name = wheel_obj.name.split('$', 1)[1]

            name = 'hinge:%s:%s' % (body_a_name, body_b_name)
            body_a_index = global_functions.get_parent(armature, body_a_obj, joined_list, -1)
            body_b_index = global_functions.get_parent(armature, body_b_obj, joined_list, -1)
            body_a_matrix = global_functions.get_matrix(prismatic, body_a_obj, True, armature, joined_list, False, version, 'JMS', 1)
            body_b_matrix = global_functions.get_matrix(prismatic, body_b_obj, True, armature, joined_list, False, version, 'JMS', 1)
            mesh_dimensions = global_functions.get_dimensions(body_a_matrix, body_a_obj, body_b_matrix, body_b_obj, custom_scale, version, None, False, False, armature, 'JMS')
            is_limited = 0
            friction_limit = 0
            min_limit = 0
            max_limit = 0
            if wheel_obj:
                min_limit = 0
                max_limit = 0

            body_a_rotation = (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a)
            body_a_translation = (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a)
            body_b_rotation = (mesh_dimensions.quat_i_b, mesh_dimensions.quat_j_b, mesh_dimensions.quat_k_b, mesh_dimensions.quat_w_b)
            body_b_translation = (mesh_dimensions.pos_x_b, mesh_dimensions.pos_y_b, mesh_dimensions.pos_z_b)

            self.prismatics.append(JMSScene.Prismatic(name, body_a_index[0], body_b_index[0], body_a_rotation, body_a_translation, body_b_rotation, body_b_translation, is_limited, friction_limit, min_limit, max_limit))

        for bound_sphere in bounding_sphere_list:
            bound_sphere_matrix = global_functions.get_matrix(bound_sphere, bound_sphere, False, armature, joined_list, False, version, 'JMS', 0)
            mesh_dimensions = global_functions.get_dimensions(bound_sphere_matrix, bound_sphere, None, None, custom_scale, version, None, False, False, armature, 'JMS')
            translation = (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a)
            scale = mesh_dimensions.radius_a

            self.bounding_spheres.append(JMSScene.Bounding_Sphere(translation, scale))

def write_file(context, filepath, report, version, game_version, encoding, folder_structure, apply_modifiers, custom_scale, permutation_ce, level_of_detail_ce, hidden_geo, export_render, export_collision, export_physics, model_type, object_list):
    try:
        jms_scene = JMSScene(context, report, version, game_version, apply_modifiers, hidden_geo, export_render, export_collision, export_physics, custom_scale, object_list)
    except global_functions.SceneParseError as parse_error:
        info = sys.exc_info()
        traceback.print_exception(info[0], info[1], info[2])
        report({'ERROR'}, "Bad scene: {0}".format(parse_error))
        return {'CANCELLED'}
    except:
        info = sys.exc_info()
        traceback.print_exception(info[0], info[1], info[2])
        report({'ERROR'}, "Internal error: {1}({0})".format(info[1], info[0]))
        return {'CANCELLED'}

    if version > 8209:
        decimal_1 = '\n%0.10f'
        decimal_2 = '\n%0.10f\t%0.10f'
        decimal_3 = '\n%0.10f\t%0.10f\t%0.10f'
        decimal_4 = '\n%0.10f\t%0.10f\t%0.10f\t%0.10f'

    else:
        decimal_1 = '\n%0.6f'
        decimal_2 = '\n%0.6f\t%0.6f'
        decimal_3 = '\n%0.6f\t%0.6f\t%0.6f'
        decimal_4 = '\n%0.6f\t%0.6f\t%0.6f\t%0.6f'

    extension = '.JMS'
    ce_settings = ''
    directory = filepath.rsplit(os.sep, 1)[0]
    filename = filepath.rsplit(os.sep, 1)[1]
    if filename.lower().endswith('.jms') or filename.lower().endswith('.jmp'):
        filename = filename.rsplit('.', 1)[0]

    foldername = filename
    blend_filename = bpy.path.basename(bpy.context.blend_data.filepath)
    if len(blend_filename) > 0:
        parent_folder = blend_filename.rsplit('.', 1)[0]
    else:
        parent_folder = 'default'

    if game_version == 'haloce':
        if not permutation_ce == '':
            ce_settings += '%s ' % (permutation_ce.replace(' ', '_').replace('\t', '_'))

            if level_of_detail_ce == None:
                ce_settings += '%s' % ('superhigh')

        if not level_of_detail_ce == None:
            if permutation_ce == '':
                ce_settings += '%s ' % ('unnamed')

            ce_settings += '%s' % (level_of_detail_ce)

        if not permutation_ce == '' or not level_of_detail_ce == None:
            filename = ''

    level_prefix_tuple = ('b ', 'b_')
    if game_version == 'haloce':
        folder_type = "models"
    else:
        if jms_scene.nodes[0].name.lower().startswith(level_prefix_tuple):
            folder_type = "structure"
        else:
            folder_type = "render"

    if model_type == "_collision":
        if game_version == 'haloce':
            folder_type = "physics"
        else:
            folder_type = "collision"

    elif model_type == "_physics":
        folder_type = "physics"

    if folder_structure:
        output_path = directory + os.sep + parent_folder
        root_directory = output_path + os.sep + folder_type
        if not os.path.exists(output_path + os.sep + folder_type):
            os.makedirs(output_path + os.sep + folder_type)
    else:
        root_directory = directory

    file = open(root_directory + os.sep + ce_settings + filename + model_type + extension, 'w', encoding=encoding)

    if version >= 8205:
        version_bounds = '8197-8210'

        file.write(
            ';### VERSION ###' +
            '\n%s' % (version) +
            '\n;\t<%s>\n' % (version_bounds)
            )

    else:
        file.write(
            '%s' % (version) +
            '\n%s' % (jms_scene.node_checksum) +
            '\n%s' % (len(jms_scene.nodes))
            )

    if version >= 8205:
        file.write(
            '\n;### NODES ###' +
            '\n%s' % (len(jms_scene.nodes)) +
            '\n;\t<name>' +
            '\n;\t<parent node index>' +
            '\n;\t<default rotation <i,j,k,w>>' +
            '\n;\t<default translation <x,y,z>>\n'
        )

    for idx, node in enumerate(jms_scene.nodes):
        if version >= 8205:
            file.write(
                '\n;NODE %s' % (idx) +
                '\n%s' % (node.name) +
                '\n%s' % (node.parent) +
                decimal_4 % (node.rotation) +
                decimal_3 % (node.translation) +
                '\n'
            )

        else:
            file.write(
                '\n%s' % (node.name) +
                '\n%s' % (node.child) +
                '\n%s' % (node.sibling) +
                decimal_4 % (node.rotation) +
                decimal_3 % (node.translation)
            )

    if version >= 8205:
        file.write(
            '\n;### MATERIALS ###' +
            '\n%s' % (len(jms_scene.materials)) +
            '\n;\t<name>' +
            '\n;\t<(Material Slot Index) LOD Permutation Region>\n'
        )

    else:
        file.write(
            '\n%s' % (len(jms_scene.materials))
        )

    for idx, material in enumerate(jms_scene.materials):
        if game_version == 'haloce':
            file.write(
                '\n%s' % (material.name) +
                '\n%s' % (material.texture_path)
            )

        elif game_version in jms_scene.gen_2:
            material_definition = '(%s)' % (material.slot)
            if not material.lod == None:
                material_definition += ' %s' % (material.lod)
            if not material.permutation == '':
                material_definition += ' %s' % (material.permutation)
            if not material.region == '':
                material_definition += ' %s' % (material.region)
            if version >= 8205:
                file.write(
                    '\n;MATERIAL %s' % (idx) +
                    '\n%s' % (material.name) +
                    '\n%s\n' % (material_definition)
                )

            else:
                file.write(
                    '\n%s' % (material.name) +
                    '\n%s' % (material_definition)
                )

    if version >= 8205:
        file.write(
            '\n;### MARKERS ###' +
            '\n%s' % (len(jms_scene.markers)) +
            '\n;\t<name>' +
            '\n;\t<node index>' +
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<radius>\n'
        )

    else:
        file.write(
            '\n%s' % (len(jms_scene.markers))
        )

    for idx, marker in enumerate(jms_scene.markers):
        if version >= 8205:
            file.write(
                '\n;MARKER %s' % (idx)
            )

        file.write('\n%s' % (marker.name))

        if version >= 8198 and version <= 8204:
            file.write('\n%s' % (marker.region))

        file.write(
            '\n%s' % (marker.parent) +
            decimal_4 % (marker.rotation) +
            decimal_3 % (marker.translation)
        )

        if version >= 8200:
            file.write(decimal_1 % (marker.scale))

        if version >= 8205:
            file.write('\n')

    if version <= 8204:
        file.write(
            '\n%s' % (len(jms_scene.regions))
        )

        for region in jms_scene.regions:
            file.write(
                '\n%s' % (region.name)
            )

    if version >= 8205:
        if version == 8205:
            file.write(
                '\n;### INSTANCE XREF PATHS ###' +
                '\n%s' % (len(jms_scene.xref_instances)) +
                '\n;\t<name>\n'
            )

        else:
            file.write(
                '\n;### INSTANCE XREF PATHS ###' +
                '\n%s' % (len(jms_scene.xref_instances)) +
                '\n;\t<path to asset file>' +
                '\n;\t<name>\n'
            )

        for idx, xref_instance in enumerate(jms_scene.xref_instances):
            file.write(
                '\n;XREF %s' % (idx) +
                '\n%s' % (xref_instance.path) +
                '\n%s\n' % (xref_instance.name)
            )

        file.write(
            '\n;### INSTANCE MARKERS ###' +
            '\n%s' % (len(jms_scene.xref_markers)) +
            '\n;\t<name>' +
            '\n;\t<unique identifier>' +
            '\n;\t<path index>' +
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>\n'
        )

        for idx, xref_marker in enumerate(jms_scene.xref_markers):
            file.write(
                '\n;XREF OBJECT %s' % (idx) +
                '\n%s' % (xref_marker.name) +
                '\n%s' % (xref_marker.unique_identifier) +
                '\n%s' % (xref_marker.index) +
                decimal_4 % (xref_marker.rotation) +
                decimal_3 % (xref_marker.translation) +
                '\n'
            )

    if version >= 8205:
        file.write(
            '\n;### VERTICES ###' +
            '\n%s' % (len(jms_scene.vertices)) +
            '\n;\t<position>' +
            '\n;\t<normal>' +
            '\n;\t<node influences count>' +
            '\n;\t\t<index>' +
            '\n;\t\t<weight>' +
            '\n;\t<texture coordinate count>' +
            '\n;\t\t<texture coordinates <u,v>>\n'
        )

    else:
        file.write(
            '\n%s' % (len(jms_scene.vertices))
        )

    for idx, vertex in enumerate(jms_scene.vertices):
        if version >= 8205:
            file.write(
                '\n;VERTEX %s' % (idx) +
                decimal_3 % (vertex.translation[0], vertex.translation[1], vertex.translation[2]) +
                decimal_3 % (vertex.normal[0], vertex.normal[1], vertex.normal[2]) +
                '\n%s' % (len(vertex.node_set))
            )
            for node in vertex.node_set:
                node_index = node[0]
                node_weight = node[1]
                file.write(
                    '\n%s' % (node_index) +
                    decimal_1 % (node_weight)
                )

            file.write('\n%s' % (len(vertex.uv_set)))

            for uv in vertex.uv_set:
                tex_u = uv[0]
                tex_v = uv[1]
                file.write(decimal_2 % (tex_u, tex_v))

            file.write('\n')

        else:
            uv = vertex.uv_set[0]
            tex_u = uv[0]
            tex_v = uv[1]
            if version < 8198:
                file.write(
                    '\n%s' % (vertex.region)
                )

            node0 = (int(-1), float(0.0))
            if len(vertex.node_set) > 0:
                node0 = vertex.node_set[0]

            node1 = (int(-1), float(0.0))
            if len(vertex.node_set) > 1:
                node1 = vertex.node_set[1]


            node0_index = node0[0]
            node0_weight = node0[1]
            node1_index = node1[0]
            node1_weight = 0.0
            if not node1_index == -1:
                node1_weight = 1.0 - node0_weight

            if node1_weight == 0:
                node1_index = -1

            if node1_weight == 1:
                node0_index = node1[0]
                node1_index = -1
                node1_weight = 0.0

            file.write(
                '\n%s' % (node0_index) +
                decimal_3 % (vertex.translation[0], vertex.translation[1], vertex.translation[2]) +
                decimal_3 % (vertex.normal[0], vertex.normal[1], vertex.normal[2]) +
                '\n%s' % (node1_index) +
                decimal_1 % (node1_weight)
            )

            if version >= 8200:
                file.write(
                    decimal_1 % (tex_u) +
                    decimal_1 % (tex_v)
                )

            else:
                file.write(decimal_2 % (tex_u, tex_v))

            if version >= 8199:
                unused_flag = 0
                file.write('\n%s' % (unused_flag))

    if version >= 8205:
        file.write(
            '\n;### TRIANGLES ###' +
            '\n%s' % (len(jms_scene.triangles)) +
            '\n;\t<material index>' +
            '\n;\t<vertex indices <v0,v1,v2>>\n'
        )

    else:
        file.write(
            '\n%s' % (len(jms_scene.triangles))
        )

    for idx, triangle in enumerate(jms_scene.triangles):
        if version >= 8205:
            file.write(
                '\n;TRIANGLE %s' % (idx) +
                '\n%s' % (triangle.material_index) +
                '\n%s\t%s\t%s\n' % (triangle.v0, triangle.v1, triangle.v2)
            )

        else:
            if version >= 8198:
                file.write('\n%s' % (triangle.region))

            file.write(
                '\n%s' % (triangle.material_index) +
                '\n%s\t%s\t%s' % (triangle.v0, triangle.v1, triangle.v2)
            )

    if version <= 8204:
        file.write('\n')

    if version >= 8206:
        file.write(
            '\n;### SPHERES ###' +
            '\n%s' % (len(jms_scene.spheres)) +
            '\n;\t<name>' +
            '\n;\t<parent>' +
            '\n;\t<material>' +
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<radius>\n'
        )

        #write sphere
        for idx, sphere in enumerate(jms_scene.spheres):
            file.write(
                '\n;SPHERE %s' % (idx) +
                '\n%s' % (sphere.name) +
                '\n%s' % (sphere.parent_index) +
                '\n%s' % (sphere.material_index) +
                decimal_4 % (sphere.rotation) +
                decimal_3 % (sphere.translation) +
                decimal_1 % (sphere.scale) +
                '\n'
            )

        #write boxes
        file.write(
            '\n;### BOXES ###' +
            '\n%s' % (len(jms_scene.boxes)) +
            '\n;\t<name>' +
            '\n;\t<parent>' +
            '\n;\t<material>' +
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<width (x)>' +
            '\n;\t<length (y)>' +
            '\n;\t<height (z)>\n'
        )

        for idx, box in enumerate(jms_scene.boxes):
            file.write(
                '\n;BOXES %s' % (idx) +
                '\n%s' % (box.name) +
                '\n%s' % (box.parent_index) +
                '\n%s' % (box.material_index) +
                decimal_4 % (box.rotation) +
                decimal_3 % (box.translation) +
                decimal_1 % (box.width) +
                decimal_1 % (box.length) +
                decimal_1 % (box.height) +
                '\n'
            )

        #write capsules
        file.write(
            '\n;### CAPSULES ###' +
            '\n%s' % (len(jms_scene.capsules)) +
            '\n;\t<name>' +
            '\n;\t<parent>' +
            '\n;\t<material>' +
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<height>' +
            '\n;\t<radius>\n'
             )

        for idx, capsule in enumerate(jms_scene.capsules):
            file.write(
                '\n;CAPSULES %s' % (idx) +
                '\n%s' % (capsule.name) +
                '\n%s' % (capsule.parent_index) +
                '\n%s' % (capsule.material_index) +
                decimal_4 % (capsule.rotation) +
                decimal_3 % (capsule.translation) +
                decimal_1 % (capsule.height) +
                decimal_1 % (capsule.radius) +
                '\n'
            )

        #write convex shapes
        file.write(
            '\n;### CONVEX SHAPES ###' +
            '\n%s' % (len(jms_scene.convex_shapes)) +
            '\n;\t<name>' +
            '\n;\t<parent>' +
            '\n;\t<material>' +
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<vertex count>' +
            '\n;\t<...vertices>\n'
        )

        for idx, convex_shape in enumerate(jms_scene.convex_shapes):
            file.write(
                '\n;CONVEX %s' % (idx) +
                '\n%s' % (convex_shape.name) +
                '\n%s' % (convex_shape.parent_index) +
                '\n%s' % (convex_shape.material_index) +
                decimal_4 % (convex_shape.rotation) +
                decimal_3 % (convex_shape.translation) +
                '\n%s' % (len(convex_shape.verts))
            )

            for vertex in convex_shape.verts:
                file.write(decimal_3 % (vertex.translation))

            file.write('\n')

        #write rag dolls
        file.write(
            '\n;### RAGDOLLS ###' +
            '\n%s' % (len(jms_scene.ragdolls)) +
            '\n;\t<name>' +
            '\n;\t<attached index>' +
            '\n;\t<referenced index>' +
            '\n;\t<attached transform>' +
            '\n;\t<reference transform>' +
            '\n;\t<min twist>' +
            '\n;\t<max twist>' +
            '\n;\t<min cone>' +
            '\n;\t<max cone>' +
            '\n;\t<min plane>' +
            '\n;\t<max plane>\n'
        )

        for idx, ragdoll in enumerate(jms_scene.ragdolls):
            file.write(
                '\n;RAGDOLL %s' % (idx) +
                '\n%s' % (ragdoll.name) +
                '\n%s' % (ragdoll.attached_index) +
                '\n%s' % (ragdoll.referenced_index) +
                decimal_4 % (ragdoll.attached_rotation) +
                decimal_3 % (ragdoll.attached_translation) +
                decimal_4 % (ragdoll.referenced_rotation) +
                decimal_3 % (ragdoll.referenced_translation) +
                decimal_1 % (ragdoll.min_twist) +
                decimal_1 % (ragdoll.max_twist) +
                decimal_1 % (ragdoll.min_cone) +
                decimal_1 % (ragdoll.max_cone) +
                decimal_1 % (ragdoll.min_plane) +
                decimal_1 % (ragdoll.max_plane)
            )

            file.write('\n')

        #write hinges
        file.write(
            '\n;### HINGES ###' +
            '\n%s' % (len(jms_scene.hinges)) +
            '\n;\t<name>' +
            '\n;\t<body A index>' +
            '\n;\t<body B index>' +
            '\n;\t<body A transform>' +
            '\n;\t<body B transform>' +
            '\n;\t<is limited>' +
            '\n;\t<friction limit>' +
            '\n;\t<min angle>' +
            '\n;\t<max angle>\n'
        )

        for idx, hinge in enumerate(jms_scene.hinges):
            file.write(
                '\n;HINGE %s' % (idx) +
                '\n%s' % (hinge.name) +
                '\n%s' % (hinge.body_a_index) +
                '\n%s' % (hinge.body_b_index) +
                decimal_4 % (hinge.body_a_rotation) +
                decimal_3 % (hinge.body_a_translation) +
                decimal_4 % (hinge.body_b_rotation) +
                decimal_3 % (hinge.body_b_translation) +
                '\n%s' % (hinge.is_limited) +
                decimal_1 % (hinge.friction_limit) +
                decimal_1 % (hinge.min_angle) +
                decimal_1 % (hinge.max_angle) +
                '\n'
            )

        if version > 8209:
            #write car wheel
            file.write(
                '\n;### CAR WHEEL ###' +
                '\n%s' % (len(jms_scene.car_wheels)) +
                '\n;\t<name>' +
                '\n;\t<chassis index>' +
                '\n;\t<wheel index>' +
                '\n;\t<chassis transform>' +
                '\n;\t<wheel transform>' +
                '\n;\t<suspension transform>' +
                '\n;\t<suspension min limit>' +
                '\n;\t<suspension max limit>' +
                '\n;\t<friction limit>' +
                '\n;\t<velocity>' +
                '\n;\t<gain>\n'
            )

            for idx, car_wheel in enumerate(jms_scene.car_wheels):
                file.write(
                    '\n;CAR WHEEL %s' % (idx) +
                    '\n%s' % (car_wheel.name) +
                    '\n%s' % (car_wheel.chassis_index) +
                    '\n%s' % (car_wheel.wheel_index) +
                    decimal_4 % (car_wheel.chassis_rotation) +
                    decimal_3 % (car_wheel.chassis_translation) +
                    decimal_4 % (car_wheel.wheel_rotation) +
                    decimal_3 % (car_wheel.wheel_translation) +
                    decimal_4 % (car_wheel.suspension_rotation) +
                    decimal_3 % (car_wheel.suspension_translation) +
                    decimal_1 % (car_wheel.suspension_min_limit) +
                    decimal_1 % (car_wheel.suspension_max_limit) +
                    decimal_1 % (car_wheel.friction_limit) +
                    decimal_1 % (car_wheel.velocity) +
                    decimal_1 % (car_wheel.gain) +
                    '\n'
                )

            #write point to point
            file.write(
                '\n;### POINT TO POINT ###' +
                '\n%s' % (len(jms_scene.point_to_points)) +
                '\n;\t<name>' +
                '\n;\t<body A index>' +
                '\n;\t<body B index>' +
                '\n;\t<body A transform>' +
                '\n;\t<body B transform>' +
                '\n;\t<constraint type>' +
                '\n;\t<x min limit>' +
                '\n;\t<x max limit>' +
                '\n;\t<y min limit>' +
                '\n;\t<y max limit>' +
                '\n;\t<z min limit>' +
                '\n;\t<z max limit>' +
                '\n;\t<spring length>\n'
            )

            for idx, point_to_point in enumerate(jms_scene.point_to_points):
                file.write(
                    '\n;POINT_TO_POINT %s' % (idx) +
                    '\n%s' % (point_to_point.name) +
                    '\n%s' % (point_to_point.body_a_index) +
                    '\n%s' % (point_to_point.body_b_index) +
                    decimal_4 % (point_to_point.body_b_rotation) +
                    decimal_3 % (point_to_point.body_b_translation) +
                    decimal_4 % (point_to_point.body_a_rotation) +
                    decimal_3 % (point_to_point.body_a_translation) +
                    '\n%s' % (point_to_point.constraint_type) +
                    decimal_1 % (point_to_point.x_min_limit) +
                    decimal_1 % (point_to_point.x_max_limit) +
                    decimal_1 % (point_to_point.y_min_limit) +
                    decimal_1 % (point_to_point.y_max_limit) +
                    decimal_1 % (point_to_point.z_min_limit) +
                    decimal_1 % (point_to_point.z_max_limit) +
                    decimal_1 % (point_to_point.spring_length) +
                    '\n'
                )

            #write prismatic
            file.write(
                '\n;### PRISMATIC ###' +
                '\n%s' % (len(jms_scene.prismatics)) +
                '\n;\t<name>' +
                '\n;\t<body A index>' +
                '\n;\t<body B index>' +
                '\n;\t<body A transform>' +
                '\n;\t<body B transform>' +
                '\n;\t<is limited>' +
                '\n;\t<friction limit>' +
                '\n;\t<min limit>' +
                '\n;\t<max limit>\n'
            )

            for idx, prismatic in enumerate(jms_scene.prismatics):
                file.write(
                    '\n;PRISMATIC %s' % (idx) +
                    '\n%s' % (prismatic.name) +
                    '\n%s' % (prismatic.body_a_index) +
                    '\n%s' % (prismatic.body_b_index) +
                    decimal_4 % (prismatic.body_a_rotation) +
                    decimal_3 % (prismatic.body_a_translation) +
                    decimal_4 % (prismatic.body_b_rotation) +
                    decimal_3 % (prismatic.body_b_translation) +
                    '\n%s' % (prismatic.is_limited) +
                    decimal_1 % (prismatic.friction_limit) +
                    decimal_1 % (prismatic.min_limit) +
                    decimal_1 % (prismatic.max_limit) +
                    '\n'
                )

        if version >= 8209:
            #write bounding sphere
            file.write(
                '\n;### BOUNDING SPHERE ###' +
                '\n%s' % (len(jms_scene.bounding_spheres)) +
                '\n;\t<translation <x,y,z>>' +
                '\n;\t<radius>\n'
            )

            for idx, bounding_sphere in enumerate(jms_scene.bounding_spheres):
                file.write(
                    '\n;BOUNDING SPHERE %s' % (idx) +
                    decimal_3 % (bounding_sphere.translation) +
                    decimal_1 % (bounding_sphere.scale) +
                    '\n'
                )

    report({'INFO'}, "Export completed successfully")
    file.close()

def command_queue(context, filepath, report, jms_version, jms_version_ce, jms_version_h2, folder_structure, apply_modifiers, triangulate_faces, edge_split, use_edge_angle, use_edge_sharp, split_angle, clean_normalize_weights, scale_enum, scale_float, console, permutation_ce, level_of_detail_ce, hidden_geo, export_render, export_collision, export_physics, game_version, encoding):
    global_functions.unhide_all_collections()
    gen_2 = ('halo2')
    object_properties = []
    scene = bpy.context.scene
    view_layer = bpy.context.view_layer
    object_list = list(scene.objects)
    node_count = 0
    marker_count = 0
    collision_count = 0
    physics_count = 0
    xref_count = 0
    bounding_radius_count = 0
    render_count = 0
    version = global_functions.get_version(jms_version, jms_version_ce, jms_version_h2, game_version, console)
    level_of_detail_ce = get_lod(level_of_detail_ce, game_version)
    custom_scale = global_functions.set_scale(scale_enum, scale_float)
    node_prefix_tuple = ('b ', 'b_', 'bone', 'frame', 'bip01')
    for obj in object_list:
        object_properties.append([obj.hide_get(), obj.hide_viewport])
        if hidden_geo:
            global_functions.unhide_object(obj)

        if obj.type == 'MESH':
            if global_functions.set_ignore(obj) == False or hidden_geo:
                if clean_normalize_weights:
                    if len(obj.vertex_groups) > 0:
                        view_layer.objects.active = obj
                        bpy.ops.object.mode_set(mode = 'EDIT')
                        bpy.ops.mesh.select_all(action='SELECT')
                        bpy.ops.object.vertex_group_clean(group_select_mode='ALL', limit=0.0)
                        bpy.ops.object.vertex_group_normalize_all()
                        bpy.ops.object.mode_set(mode = 'OBJECT')

                modifier_list = []
                if apply_modifiers:
                    for modifier in obj.modifiers:
                        modifier.show_render = True
                        modifier.show_viewport = True
                        modifier.show_in_editmode = True
                        modifier_list.append(modifier.type)

                if triangulate_faces:
                    if not 'TRIANGULATE' in modifier_list:
                        obj.modifiers.new("Triangulate", type='TRIANGULATE')

                if edge_split:
                    if not 'EDGE_SPLIT' in modifier_list:
                        edge_split = obj.modifiers.new("EdgeSplit", type='EDGE_SPLIT')
                        edge_split.use_edge_angle = use_edge_angle
                        edge_split.split_angle = split_angle
                        edge_split.use_edge_sharp = use_edge_sharp
                    else:
                        modifier_idx = modifier_list.index('EDGE_SPLIT')
                        obj.modifiers[modifier_idx].use_edge_angle = use_edge_angle
                        obj.modifiers[modifier_idx].split_angle = split_angle
                        obj.modifiers[modifier_idx].use_edge_sharp = use_edge_sharp

        name = obj.name.lower()
        if obj.type == 'ARMATURE':
            node_count += len(obj.data.bones)

        elif name.startswith(node_prefix_tuple):
            node_count += 1

        elif name[0:1] == '#':
            if global_functions.set_ignore(obj) == False or hidden_geo:
                marker_count += 1

        elif name[0:1] == '@' and len(obj.data.polygons) > 0:
            if global_functions.set_ignore(obj) == False or hidden_geo:
                collision_count += 1

        elif name[0:1] == '$' and game_version in gen_2:
            if global_functions.set_ignore(obj) == False or hidden_geo:
                physics_count += 1

        elif obj.type== 'MESH' and not len(obj.data.ass_jms.XREF_path) == 0 and version > 8205:
            if global_functions.set_ignore(obj) == False or hidden_geo:
                xref_count += 1

        elif obj.type== 'MESH' and obj.data.ass_jms.bounding_radius and version >= 8209:
            if global_functions.set_ignore(obj) == False or hidden_geo:
                bounding_radius_count += 1

        elif obj.type== 'MESH' and len(obj.data.polygons) > 0:
            if global_functions.set_ignore(obj) == False or hidden_geo:
                render_count += 1


    if render_count == 0 and collision_count == 0 and physics_count == 0 and marker_count == 0:
        report({'ERROR'}, "No objects in scene")
        return {'CANCELLED'}

    if export_render and render_count > 0:
        model_type = ""
        write_file(context, filepath, report, version, game_version, encoding, folder_structure, apply_modifiers, custom_scale, permutation_ce, level_of_detail_ce, hidden_geo, export_render, False, False, model_type, object_list)

    if export_collision and collision_count > 0:
        model_type = "_collision"
        write_file(context, filepath, report, version, game_version, encoding, folder_structure, apply_modifiers, custom_scale, permutation_ce, level_of_detail_ce, hidden_geo, False, export_collision, False, model_type, object_list)

    if export_physics and physics_count > 0:
        model_type = "_physics"
        write_file(context, filepath, report, version, game_version, encoding, folder_structure, apply_modifiers, custom_scale, permutation_ce, level_of_detail_ce, hidden_geo, False, False, export_physics, model_type, object_list)

    for idx, obj in enumerate(object_list):
        property_value = object_properties[idx]
        obj.hide_set(property_value[0])
        obj.hide_viewport = property_value[1]

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.export_scene.jms()
