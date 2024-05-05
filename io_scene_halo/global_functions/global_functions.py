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
import sys
import math
import colorsys
import re
import operator

from decimal import *
from math import radians
from io import TextIOWrapper
from enum import Enum, auto
from mathutils import Vector, Euler, Quaternion, Matrix

class ModelTypeEnum(Enum):
    render = 0
    collision = auto()
    physics = auto()
    animations = auto()

class JmsDimensions:
    def __init__(self, quaternion, position, scale, dimension, object_radius, pill_height):
        self.quaternion = quaternion
        self.position = position
        self.scale = scale
        self.dimension = dimension
        self.object_radius = object_radius
        self.pill_height = pill_height

class BlendScene():
    def __init__(self,
                 world_node_count,
                 armature_count,
                 mesh_frame_count,
                 render_count,
                 collision_count,
                 physics_count,
                 armature,
                 node_list,
                 render_marker_list,
                 collision_marker_list,
                 physics_marker_list,
                 marker_list,
                 xref_instances,
                 instance_markers,
                 render_geometry_list,
                 collision_geometry_list,
                 sphere_list,
                 box_list,
                 capsule_list,
                 convex_shape_list,
                 ragdoll_list,
                 hinge_list,
                 car_wheel_list,
                 point_to_point_list,
                 prismatic_list,
                 bounding_sphere_list,
                 skylight_list):
        self.world_node_count = world_node_count
        self.armature_count = armature_count
        self.mesh_frame_count = mesh_frame_count
        self.render_count = render_count
        self.collision_count = collision_count
        self.physics_count = physics_count
        self.armature = armature
        self.node_list = node_list
        self.render_marker_list = render_marker_list
        self.collision_marker_list = collision_marker_list
        self.physics_marker_list = physics_marker_list
        self.marker_list = marker_list
        self.xref_instances  = xref_instances
        self.instance_markers = instance_markers
        self.render_geometry_list = render_geometry_list
        self.collision_geometry_list = collision_geometry_list
        self.sphere_list = sphere_list
        self.box_list = box_list
        self.capsule_list = capsule_list
        self.convex_shape_list = convex_shape_list
        self.ragdoll_list = ragdoll_list
        self.hinge_list = hinge_list
        self.car_wheel_list = car_wheel_list
        self.point_to_point_list = point_to_point_list
        self.prismatic_list = prismatic_list
        self.bounding_sphere_list = bounding_sphere_list
        self.skylight_list = skylight_list

class EdgeSplit():
    def __init__(self, is_enabled, use_edge_angle, split_angle, use_edge_sharp):
        self.is_enabled = is_enabled
        self.use_edge_angle = use_edge_angle
        self.split_angle = split_angle
        self.use_edge_sharp = use_edge_sharp

class ParentIDFix():
    def __init__(self, pelvis = None, thigh0 = None, thigh1 = None, spine1 = None, clavicle0 = None, clavicle1 = None):
        self.pelvis = pelvis
        self.thigh0 = thigh0
        self.thigh1 = thigh1
        self.spine1 = spine1
        self.clavicle0 = clavicle0
        self.clavicle1 = clavicle1

def get_child(bone, bone_list, game_title, preexport_sorting):
    set_node = None
    if game_title == "halo1" and preexport_sorting:
        for node in bone_list:
            if 'pelvis' in bone.name.lower():
                thigh_list = []
                for child in bone_list:
                    if child.parent == bone and 'thigh' in child.name.lower():
                        thigh_list.append(child)

                thigh_list = sorted(thigh_list, key=lambda x: x.name)
                thigh_list.reverse()
                if len(thigh_list) > 0:
                    set_node = thigh_list[0]

            elif 'spine1' in bone.name.lower():
                clavical_list = []
                for child in bone_list:
                    if child.parent == bone and 'clavicle' in child.name.lower():
                        clavical_list.append(child)

                clavical_list = sorted(clavical_list, key=lambda x: x.name)
                clavical_list.reverse()
                if len(clavical_list) > 0:
                    set_node = clavical_list[0]

    if not set_node:
        for node in bone_list:
            if bone == node.parent:
                set_node = node
                break

    return set_node

def get_sibling(armature, bone, bone_list, game_title, preexport_sorting):
    sibling_list = []
    set_sibling = None
    for node in bone_list:
        if bone.parent == node.parent:
            sibling_list.append(node)

    if game_title == "halo1" and preexport_sorting:
        if bone.parent and 'pelvis' in bone.parent.name.lower():
            thigh_list = []
            for sibling in reversed(sibling_list):
                if 'thigh' in sibling.name.lower():
                    sibling_index = sibling_list.index(sibling)
                    thigh_list.append(sibling_list.pop(sibling_index))

            thigh_list.reverse()
            sibling_list = thigh_list + sibling_list

        elif bone.parent and 'spine1' in bone.parent.name.lower():
            clavical_list = []
            for sibling in reversed(sibling_list):
                if 'clavicle' in sibling.name.lower():
                    sibling_index = sibling_list.index(sibling)
                    clavical_list.append(sibling_list.pop(sibling_index))

            clavical_list.reverse()
            sibling_list = clavical_list + sibling_list

    if len(sibling_list) <= 1:
        set_sibling = None

    else:
        sibling_node = sibling_list.index(bone)
        next_sibling_node = sibling_node + 1
        if next_sibling_node >= len(sibling_list):
            set_sibling = None

        else:
            if armature:
                set_sibling = armature.data.bones['%s' % sibling_list[next_sibling_node].name]

            else:
                set_sibling = bpy.data.objects['%s' % sibling_list[next_sibling_node].name]

    return set_sibling

def sort_by_layer(node_list, armature):
    layer_count = []
    layer_root = []
    root_list = []
    children_list = []
    reversed_children_list = []
    joined_list = []
    reversed_joined_list = []
    sort_list = []
    reversed_sort_list = []
    for node in node_list:
        if node.parent == None and not node.name[0:1] == '!' or node.parent.name[0:1] == '!' and node.parent.parent == None:
            layer_count.append(None)
            layer_root.append(node)

        else:
            if not node.parent in layer_count:
                layer_count.append(node.parent)

    for layer in layer_count:
        joined_list = root_list + children_list
        reversed_joined_list = root_list + reversed_children_list
        layer_index = layer_count.index(layer)
        if layer_index == 0:
            if armature:
                root_list.append(armature.data.bones[0])

            else:
                root_list.append(layer_root[0])

        else:
            for node in node_list:
                if armature:
                    if node.parent != None:
                        if armature.data.bones['%s' % node.parent.name] in joined_list and not node in children_list:
                            sort_list.append(node.name)
                            reversed_sort_list.append(node.name)

                else:
                    if node.parent != None:
                        if node.parent in joined_list and not node in children_list:
                            sort_list.append(node.name)
                            reversed_sort_list.append(node.name)

            sort_list.sort()
            reversed_sort_list.sort()
            reversed_sort_list.reverse()
            for sort in sort_list:
                if armature:
                    if not armature.data.bones['%s' % sort] in children_list:
                        children_list.append(armature.data.bones['%s' % sort])

                else:
                    if not bpy.data.objects[sort] in children_list:
                        children_list.append(bpy.data.objects[sort])

            for sort in reversed_sort_list:
                if armature:
                    if not armature.data.bones['%s' % sort] in reversed_children_list:
                        reversed_children_list.append(armature.data.bones['%s' % sort])

                else:
                    if not bpy.data.objects[sort] in reversed_children_list:
                        reversed_children_list.append(bpy.data.objects[sort])

        joined_list = root_list + children_list
        reversed_joined_list = root_list + reversed_children_list

    return (joined_list, reversed_joined_list)

def sort_by_index(node_list):
    root_node = []
    child_nodes = []
    for node in node_list:
        if node.parent == None:
            root_node.append(node)

        else:
            child_nodes.append(node)

    sorted_list = root_node + child_nodes

    return (sorted_list, sorted_list)

def sort_list(node_list, armature, game_version, version, animation):
    version = int(version)
    sorted_list = []
    if game_version == "halo1":
        sorted_list = sort_by_layer(node_list, armature)

    elif game_version == "halo2" or game_version == "halo3":
        if animation:
            if version <= 16394:
                sorted_list = sort_by_layer(node_list, armature)

            else:
                sorted_list = sort_by_index(node_list)

        else:
            if version <= 8204:
                sorted_list = sort_by_layer(node_list, armature)

            else:
                sorted_list = sort_by_index(node_list)

    return sorted_list

def get_child_batch(bone, reversed_joined_list, node_list):
    set_node = None
    for node in reversed_joined_list:
        if not node.parent == None and not node.parent == -1 and bone == node_list[node.parent]:
            set_node = node
            break

    return set_node

def get_sibling_batch(bone, bone_list):
    sibling_list = []
    set_sibling = None
    for node in bone_list:
        if bone.parent == node.parent:
            sibling_list.append(node)

    if len(sibling_list) <= 1:
        set_sibling = None

    else:
        sibling_node = sibling_list.index(bone)
        next_sibling_node = sibling_node + 1
        if next_sibling_node >= len(sibling_list):
            set_sibling = None

        else:
            set_sibling = sibling_list[next_sibling_node]

    return set_sibling

def sort_by_layer_batch(node_list):
    layer_count = []
    layer_root = []
    root_list = []
    children_list = []
    reversed_children_list = []
    joined_list = []
    reversed_joined_list = []
    sort_list = []
    reversed_sort_list = []
    for node in node_list:
        if node.parent == None or node.parent == -1:
            layer_count.append(None)
            layer_root.append(node)

        else:
            if not node_list[node.parent] in layer_count:
                layer_count.append(node_list[node.parent])

    for layer in layer_count:
        joined_list = root_list + children_list
        reversed_joined_list = root_list + reversed_children_list
        layer_index = layer_count.index(layer)
        if layer_index == 0:
            root_list.append(layer_root[0])

        else:
            for node in node_list:
                if not node.parent == None and node.parent != -1:
                    if node_list[node.parent] in joined_list and not node in children_list:
                        sort_list.append(node)
                        reversed_sort_list.append(node)

            sort_list.sort(key=operator.attrgetter('name'))
            reversed_sort_list.sort(key=operator.attrgetter('name'))
            reversed_sort_list.reverse()
            for sort in sort_list:
                if not sort in children_list:
                    children_list.append(sort)

            for sort in reversed_sort_list:
                if not sort in reversed_children_list:
                    reversed_children_list.append(sort)

        joined_list = root_list + children_list
        reversed_joined_list = root_list + reversed_children_list

    return (joined_list, reversed_joined_list)

def sort_list_batch(node_list, game_version, version, animation):
    version = int(version)
    sorted_list = []
    if game_version == "halo1":
        sorted_list = sort_by_layer_batch(node_list)

    elif game_version == "halo2" or game_version == "halo3":
        if animation:
            if version <= 16394:
                sorted_list = sort_by_layer_batch(node_list)

            else:
                sorted_list = sort_by_index(node_list)

        else:
            if version <= 8204:
                sorted_list = sort_by_layer_batch(node_list)

            else:
                sorted_list = sort_by_index(node_list)

    return sorted_list

def test_encoding(filepath):
    UTF_8_BOM = b'\xef\xbb\xbf'
    UTF_16_BE_BOM = b'\xfe\xff'
    UTF_16_LE_BOM = b'\xff\xfe'
    data = open(filepath, 'rb')
    file_size = os.path.getsize(filepath)
    BOM = data.read(3)
    encoding = None
    # first check the boms
    if BOM.startswith(UTF_8_BOM):
        encoding = 'utf-8-sig'

    elif BOM.startswith(UTF_16_BE_BOM) or BOM.startswith(UTF_16_LE_BOM):
        encoding = 'utf-16'

    else:
        if file_size % 2: # can't be USC-2/UTF-16 if the number of bytes is odd
            encoding = 'utf-8'

        else:
            # get the first half a kilobyte
            data.seek(0)
            sample_bytes = data.read(0x200)

            even_zeros = 0
            odd_zeros = 0

            for idx, byte in enumerate(sample_bytes):
                if byte != 0:
                    continue

                if idx % 2:
                    odd_zeros += 1

                else:
                    even_zeros += 1

            ## if there are no null bytes we assume we are dealing with a utf-8 file
            ## if there are null bytes, assume utf-16 and guess endianness based on where the null bytes are
            if even_zeros == 0 and odd_zeros == 0:
                encoding = 'utf-8'

            elif odd_zeros > even_zeros:
                encoding = 'utf-16-le'

            else:
                encoding = 'utf-16-be'

    data.close()

    return encoding

def get_true_extension(filepath, extension, is_import):
    extension_list = ['.jma', '.jmm', '.jmt', '.jmo', '.jmr', '.jmrx', '.jmh', '.jmz', '.jmw', '.jms', '.jmp']
    true_extension = ''
    if is_import:
        true_extension = filepath.rsplit('.', 1)[1].lower()

    else:
        extension_char = (len(extension))
        if not filepath[-(extension_char):].lower() in extension_list or not filepath[-(extension_char):].lower() in extension.lower():
            true_extension = extension

    return true_extension

def generate_fcurve_matrix(bone, action, frame_idx):
    dpath_loc = bone.path_from_id("location")
    dpath_rot_quat = bone.path_from_id("rotation_quaternion")
    dpath_rot_euler = bone.path_from_id("rotation_euler")
    dpath_sca = bone.path_from_id("scale")

    translation = Vector((0.0, 0.0, 0.0))
    rotation = Quaternion((1.0, 0.0, 0.0, 0.0))
    scale = Vector((1.0, 1.0, 1.0))
    if not action == None:
        x_pos = action.fcurves.find(dpath_loc, index=0)
        y_pos = action.fcurves.find(dpath_loc, index=1)
        z_pos = action.fcurves.find(dpath_loc, index=2)
        if x_pos:
            translation[0] = x_pos.evaluate(frame_idx)
        if y_pos:
            translation[1] = y_pos.evaluate(frame_idx)
        if z_pos:
            translation[2] = z_pos.evaluate(frame_idx)

        if bone.rotation_mode == 'QUATERNION':
            w_rot = action.fcurves.find(dpath_rot_quat, index=0)
            i_rot = action.fcurves.find(dpath_rot_quat, index=1)
            j_rot = action.fcurves.find(dpath_rot_quat, index=2)
            k_rot = action.fcurves.find(dpath_rot_quat, index=3)
            if w_rot:
                rotation[0] = w_rot.evaluate(frame_idx)
            if i_rot:
                rotation[1] = i_rot.evaluate(frame_idx)
            if j_rot:
                rotation[2] = j_rot.evaluate(frame_idx)
            if k_rot:
                rotation[3] = k_rot.evaluate(frame_idx)

        else:
            rotation = Euler((0.0, 0.0, 0.0))
            x_rot = action.fcurves.find(dpath_rot_euler, index=0)
            y_rot = action.fcurves.find(dpath_rot_euler, index=1)
            z_rot = action.fcurves.find(dpath_rot_euler, index=2)
            if x_rot:
                rotation[0] = x_rot.evaluate(frame_idx)
            if y_rot:
                rotation[1] = y_rot.evaluate(frame_idx)
            if z_rot:
                rotation[2] = z_rot.evaluate(frame_idx)

            rotation = rotation.to_quaternion()

        x_sca = action.fcurves.find(dpath_sca, index=0)
        y_sca = action.fcurves.find(dpath_sca, index=1)
        z_sca = action.fcurves.find(dpath_sca, index=2)
        if x_sca:
            scale[0] = x_sca.evaluate(frame_idx)
        if y_sca:
            scale[1] = y_sca.evaluate(frame_idx)
        if z_sca:
            scale[2] = z_sca.evaluate(frame_idx)

    matrix_translation = Matrix.Translation(translation)
    matrix_rotation = rotation.to_matrix().to_4x4()
    matrix_scale = Matrix.Scale(scale[0], 4)

    return matrix_translation @ matrix_rotation @ matrix_scale

def get_fcurve_matrix(node, node_idx, fcurve_matrices, jma_version):
    object_matrix = fcurve_matrices[node_idx]
    if not node.parent == -1 and not jma_version >= get_version_matrix_check("JMA", None):
        #Files at or above 8205 use absolute transform instead of local transform for nodes
        object_matrix = fcurve_matrices[node.parent].inverted() @ object_matrix

    return object_matrix

def get_matrix(obj_a, obj_b, is_local, armature, joined_list, is_node, version, file_type, constraint, custom_scale, fix_rotation, default_parent=-1):
    object_matrix = Matrix.Translation((0, 0, 0))
    rotation_matrix = Matrix.Rotation(0, 4, 'Z')
    if file_type == 'ASS':
        scale_matrix = Matrix.Scale(1, 4)

    else:
        rotation = 0.0
        if fix_rotation:
            rotation = 90.0

        rotation_matrix = Matrix.Rotation(radians(rotation), 4, 'Z')
        scale_matrix = Matrix.Scale(custom_scale, 4)

    if is_node:
        if armature:
            pose_bone = armature.pose.bones['%s' % (obj_a.name)]
            object_matrix = (pose_bone.matrix @ rotation_matrix) @ scale_matrix
            if pose_bone.parent and not version >= get_version_matrix_check(file_type, None):
                #Files at or above 8205 use absolute transform instead of local transform for nodes
                object_matrix = ((pose_bone.parent.matrix @ rotation_matrix).inverted() @ (pose_bone.matrix @ rotation_matrix)) @ scale_matrix

        else:
            object_matrix = obj_a.matrix_world @ scale_matrix
            if obj_a.parent and not version >= get_version_matrix_check(file_type, None):
                #Files at or above 8205 use absolute transform instead of local transform for nodes
                object_matrix = (obj_a.parent.matrix_world.inverted() @ obj_a.matrix_world) @ scale_matrix

    else:
        object_matrix = obj_a.matrix_world @ scale_matrix
        if is_local:
            parent_object = get_parent(armature, obj_b, joined_list, default_parent)
            if parent_object[1]:
                if type(parent_object[1]).__name__ == 'Bone':
                    pose_bone = armature.pose.bones['%s' % (parent_object[1].name)]
                    object_matrix = ((pose_bone.matrix @ rotation_matrix).inverted() @ obj_a.matrix_world) @ scale_matrix

                else:
                    object_matrix = (parent_object[1].matrix_world.inverted() @ obj_a.matrix_world) @ scale_matrix

    return object_matrix

def get_dimensions(mesh_matrix, original_geo, version, is_bone, file_type, custom_scale):
    quaternion = (0.0, 0.0, 0.0, 1.0)
    position = (0.0, 0.0, 0.0)
    scale = (0.0, 0.0, 0.0)
    dimension = (0.0, 0.0, 0.0)
    object_radius = 0.0
    pill_height = 0.0
    if original_geo:
        pos, rot, scale = mesh_matrix.decompose()
        quat = rot.inverted()
        if not invert_rotations(file_type, version):
            quat = rot

        quaternion = (quat[1], quat[2], quat[3], quat[0])
        position = mesh_matrix.to_translation()
        if file_type == 'JMS':
            scale_matrix = Matrix.Scale(custom_scale, 4)

            position = position @ scale_matrix

        if not is_bone:
            dimension_x = original_geo.dimensions[0]
            dimension_y = original_geo.dimensions[1]
            dimension_z = original_geo.dimensions[2]
            if not original_geo.dimensions[0] == 0.0:
                dimension_x = original_geo.dimensions[0] / scale[0]

            if not original_geo.dimensions[1] == 0.0:
                dimension_y = original_geo.dimensions[1] / scale[1]

            if not original_geo.dimensions[2] == 0.0:
                dimension_z = original_geo.dimensions[2] / scale[2]

            dimension = (dimension_x, dimension_y, dimension_z)
            if file_type == 'JMS':
                dimension = ((original_geo.dimensions[0] * custom_scale), (original_geo.dimensions[1] * custom_scale), (original_geo.dimensions[2] * custom_scale))

            #The reason this code exists is to try to copy how capsules work in 3DS Max.
            #To get original height for 3DS Max do (radius_jms * 2) + height_jms
            #The maximum value of radius is height / 2
            pill_radius = ((dimension[0] / 2))
            pill_height = (dimension[2]) - (pill_radius * 2)
            if pill_height <= 0:
                pill_height = 0

            dimension = (dimension[0], dimension[1], dimension[2])
            object_radius = pill_radius
            pill_height = pill_height

    return JmsDimensions(quaternion, position, scale, dimension, object_radius, pill_height)

def get_hierarchy(mesh):
    hierarchy_list = [mesh]
    while mesh.parent:
        mesh = mesh.parent
        hierarchy_list.append(mesh)

    return hierarchy_list

def get_children(world_node):
    children_hierarchy = [world_node]
    for node in children_hierarchy:
        for child in node.children:
            children_hierarchy.append(child)

    return children_hierarchy

def get_parent(armature, node, joined_list, default_parent):
    valid_parent_idx = -1
    valid_parent = None
    if node and node.parent:
        node_parent = node.parent
        if node_parent.type == 'ARMATURE':
            node_parent = node.parent_bone
            while valid_parent == None:
                if type(node_parent).__name__ == 'Bone':
                    if node_parent != None:
                        if node_parent in joined_list and node_parent.use_deform:
                            valid_parent = node_parent
                            valid_parent_idx = joined_list.index(node_parent)

                        else:
                            node_parent = node_parent.parent

                    else:
                        break

                else:
                    if not string_empty_check(node_parent):
                        node_parent = armature.data.bones[node_parent]
                        if node_parent in joined_list and node_parent.use_deform:
                            valid_parent = node_parent
                            valid_parent_idx = joined_list.index(node_parent)

                        else:
                            node_parent = node_parent.parent

                    else:
                        break

        else:
            while valid_parent == None:
                if node_parent != None:
                    if node_parent in joined_list and node_parent.hide_viewport == False and node_parent.hide_get() == False:
                        valid_parent = node_parent
                        valid_parent_idx = joined_list.index(node_parent)

                    else:
                        node_parent = node_parent.parent

                else:
                    break

    if valid_parent == None and default_parent >= 0:
        valid_parent = joined_list[default_parent]
        valid_parent_idx = default_parent

    return (valid_parent_idx, valid_parent)

def set_scale(scale_enum, scale_float):
    scale = 1
    if scale_enum == '1':
        scale = float(100)

    if scale_enum == '2':
        scale = float(scale_float)

    return scale

def set_framerate(frame_rate_enum, frame_rate_float):
    frame_rate_value = 30
    if frame_rate_enum == 'CUSTOM':
        frame_rate_value = math.floor(frame_rate_float)

    else:
        frame_rate_value = math.floor(float(frame_rate_enum))

    return frame_rate_value

def get_version_matrix_check(filetype, game_version):
    matrix_version = 0
    if filetype == 'JMA':
        matrix_version = 16394

    elif filetype == 'JMS':
        matrix_version = 8205

    elif filetype == 'ASS':
        matrix_version = 8

    return matrix_version

def invert_rotations(filetype, file_version):
    invert_rotations = True
    if filetype == 'JMA' and file_version >= 16394:
        invert_rotations = False

    elif filetype == 'JMS' and file_version >= 8205:
        invert_rotations = False

    elif filetype == 'ASS':
        invert_rotations = False

    return invert_rotations

def gather_materials(game_version, material, material_list, export_type):
    assigned_materials_list = []
    if material is not None:
        if material not in assigned_materials_list:
            assigned_materials_list.append(material)

    else:
        if game_version == "halo1" and not None in material_list:
            material_list.append(None)

    if game_version == "halo1":
        if material not in material_list:
            material_list.append(material)

    elif game_version == "halo2" or game_version == "halo3":
        if export_type == "JMS":
            if material not in material_list and material in assigned_materials_list:
                material_list.append(material)

        if export_type == "ASS":
            if material not in material_list and material in assigned_materials_list:
                material_list.append(material)

    else:
        if game_version == "halo1" and not None in material_list:
            material_list.append(None)

    return material_list

def get_face_material(original_geo, face):
    object_materials = len(original_geo.material_slots)
    face_material_index = face.material_index
    assigned_material = -1
    if not object_materials <= 0 and not face_material_index <= -1 and not face_material_index >= object_materials:
        assigned_material = face_material_index

    return assigned_material

def get_material(game_version, original_geo, face, geometry, lod, region, permutation):
    object_materials = len(original_geo.material_slots)
    mat = None
    assigned_material = None
    face_material_index = face.material_index
    if game_version == "halo1":
        if not object_materials <= 0 and not face_material_index >= object_materials:
            mat_slot = original_geo.material_slots[face_material_index]
            if mat_slot.link == 'OBJECT':
                if mat_slot is not None:
                    mat = mat_slot.material

            else:
                if geometry.materials[face_material_index] is not None:
                    mat = geometry.materials[face_material_index]

            if mat:
                assigned_material = mat

    elif game_version == "halo2" or game_version == "halo3":
        assigned_material = -1
        if  not object_materials <= 0 and not face_material_index >= object_materials:
            mat_slot = original_geo.material_slots[face_material_index]
            if mat_slot.link == 'OBJECT':
                if mat_slot is not None:
                    mat = mat_slot.material

            else:
                if geometry.materials[face_material_index] is not None:
                    mat = geometry.materials[face_material_index]

            if mat:
                assigned_material = [mat, lod, region, permutation]

    return assigned_material

class ParseError(Exception):
    pass

class HaloAsset:
    """Helper class for reading in JMS/JMA/ASS files"""

    __comment_regex = re.compile("[^\"]*?;(?!.*\")")

    def __init__(self, file):
        self._elements = []
        self._index = 0
        if not isinstance(file, TextIOWrapper):
            with open(file, "r", encoding=test_encoding(file)) as file:
                self.__init_from_textio(file)

        else:
            self.__init_from_textio(file)

    def __init_from_textio(self, io):
        for line in io:
            for element in line.strip().split("\t"):
                if element != '':
                    comment_match = re.search(self.__comment_regex, element)
                    if comment_match is None:
                        self._elements.append(element)

                    else:
                        processed_element = element[: comment_match.end() - 1]
                        if processed_element != '':
                            self._elements.append(element)

                        break # ignore the rest of the line if we found a comment
    def left(self):
        """Returns the number of elements left"""
        if self._index < len(self._elements):
            return len(self._elements) - self._index

        else:
            return 0

    def skip(self, count):
        """Skip forwards n elements"""
        self._index += count

    def next(self):
        """Return the next element, raises AssetParseError on error"""
        try:
            self._index += 1
            return self._elements[self._index - 1]

        except:
            raise ParseError()

    def get_first_line(self):
        """Return the first line in the file, raises AssetParseError on error"""
        try:
            return self._elements[0]

        except:
            raise ParseError()

    def next_multiple(self, count):
        """Returns an array of the next n elements, raises AssetParseError on error"""
        try:
            list = self._elements[self._index: self._index + count]
            self._index += count
            return list

        except:
            raise ParseError()

    def next_vector(self):
        """Return the next vector as mathutils.Vector, raises AssetParseError on error"""
        next_p0 = self.next()
        next_p1 = self.next()
        next_p2 = self.next()
        try:
            p0 = float(next_p0.replace(",", "."))
            p1 = float(next_p1.replace(",", "."))
            p2 = float(next_p2.replace(",", "."))

        except ValueError:
            p0 = float(next_p0.rsplit('.', 1)[0])
            p1 = float(next_p1.rsplit('.', 1)[0])
            p2 = float(next_p2.rsplit('.', 1)[0])

        return Vector((p0, p1, p2))

    def are_quaternions_inverted(self):
        """Override this to enable quaternion inversion for next_quaternion()"""
        return False

    def next_quaternion(self):
        """Return the next quaternion as mathutils.Quaternion, raises AssetParseError on error"""
        x = float(self.next().replace(",", "."))
        y = float(self.next().replace(",", "."))
        z = float(self.next().replace(",", "."))
        w = float(self.next().replace(",", "."))
        quat = Quaternion((w, x, y, z))
        if self.are_quaternions_inverted():
            quat.invert()

        return quat

def get_game_title(asset_version, filetype):
    game_title = None
    if filetype == "JMS":
        if asset_version >= 8211:
            game_title = "halo3"

        elif asset_version >= 8201:
            game_title = "halo2"

        else:
            game_title = "halo1"

    elif filetype == "JMA":
        if asset_version >= 16393:
            game_title = "halo2"

        else:
            game_title = "halo1"

    return game_title

def lim32(n):
    """Simulate a 32 bit unsigned interger overflow"""
    return n & 0xFFFFFFFF

def rotl_32(x, n):
    """Rotate x left n-tims as a 32 bit interger"""
    return lim32(x << n) | (x >> 32 - n)

def rotr_32(x, n):
    """Rotate x right n-times as a 32 bit interger"""
    return (x >> n) | lim32(x << 32 - n)

def halo_string_checksum(string):
    """String checksum function matching halo exporter"""
    checksum = 0
    for byte in string.encode():
        checksum = rotl_32(checksum, 1)
        checksum += byte

    return lim32(checksum)

# Ported from https://github.com/preshing/RandomSequence
class PreshingSequenceGenerator32:
    """Peusdo-random sequence generator that repeats every 2**32 elements"""
    @staticmethod
    def __permuteQPR(x):
        prime = 4294967291
        if x >= prime: # The 5 integers out of range are mapped to themselves.
            return x

        residue = lim32(x**2 % prime)
        if x <= (prime // 2):
            return residue

        else:
            return lim32(prime - residue)

    def __init__(self, seed_base = None, seed_offset = None):
        import time
        if seed_base == None:
            seed_base = lim32(int(time.time() * 100000000)) ^ 0xac1fd838

        if seed_offset == None:
            seed_offset = lim32(int(time.time() * 100000000)) ^ 0x0b8dedd3

        self.__index = PreshingSequenceGenerator32.__permuteQPR(lim32(PreshingSequenceGenerator32.__permuteQPR(seed_base) + 0x682f0161))
        self.__intermediate_offset = PreshingSequenceGenerator32.__permuteQPR(lim32(PreshingSequenceGenerator32.__permuteQPR(seed_offset) + 0x46790905))

    def next(self):
        self.__index = lim32(self.__index + 1)
        index_permut = PreshingSequenceGenerator32.__permuteQPR(self.__index)
        return PreshingSequenceGenerator32.__permuteQPR(lim32(index_permut + self.__intermediate_offset) ^ 0x5bf03635)

class RandomColorGenerator(PreshingSequenceGenerator32):
    def next(self):
        rng = super().next()
        h = (rng >> 16) / 0xFFF # [0, 1]
        saturation_raw = (rng & 0xFF) / 0xFF
        brightness_raw = (rng >> 8 & 0xFF) / 0xFF
        v = brightness_raw * 0.3 + 0.5 # [0.5, 0.8]
        s = saturation_raw * 0.4 + 0.6 # [0.3, 1]
        rgb = colorsys.hsv_to_rgb(h, s, v)
        colors = (rgb[0], rgb[1] , rgb[2], 1)
        return colors

def node_checksum(node, checksum = 0):
    checksum = lim32(rotl_32(checksum, 1) + halo_string_checksum(node.name))
    checksum = rotl_32(checksum, 2)

    return rotr_32(checksum, 2)

def string_checksum(string_value, checksum = 0):
    checksum = lim32(rotl_32(checksum, 1) + halo_string_checksum(string_value))
    checksum = rotl_32(checksum, 2)

    return rotr_32(checksum, 2)

def node_hierarchy_checksum(nodes, node, checksum = 0):
    checksum = lim32(rotl_32(checksum, 1) + halo_string_checksum(node.name))
    checksum = rotl_32(checksum, 2)
    child_idx = node.child
    child_node = nodes[child_idx]
    while child_idx != -1:
        checksum = node_hierarchy_checksum(nodes, child_node, checksum)
        child_idx = nodes[child_idx].sibling
        child_node = nodes[child_idx]

    # we undo the rotation state from the recursion, but we leave
    # in the rotation from adding the string for this node.  This
    # way, the order of siblings matters to the checksum.
    return rotr_32(checksum, 2)

def get_filename(game_title, permutation_ce, level_of_detail_ce, folder_structure, asset_type, is_jmi, filepath):
    ce_settings = ''
    extension = '.JMS'
    if is_jmi:
        extension = '.JMI'

    filename = filepath.rsplit(os.sep, 1)[1]

    if filename.lower().endswith('.jms') or filename.lower().endswith('.jmp') or filename.lower().endswith('.jmi'):
        filename = filename.rsplit('.', 1)[0]

    if game_title == "halo1":
        if not permutation_ce == '' or not level_of_detail_ce == None:
            if not permutation_ce == '':
                permutation_string = permutation_ce
                if not game_title == "halo1":
                    permutation_string = permutation_ce.replace(' ', '_').replace('\t', '_')

                ce_settings += '%s ' % (permutation_string)

            else:
                ce_settings += '%s ' % ('unnamed')

            if not level_of_detail_ce == None:
                ce_settings += '%s' % (level_of_detail_ce)

            else:
                ce_settings += '%s' % ('superhigh')

            filename = ce_settings

    model_string = ""
    if asset_type == ModelTypeEnum.collision:
        model_string = "_collision"

    elif asset_type == ModelTypeEnum.physics:
        model_string = "_physics"

    model_name = model_string
    if folder_structure:
        if game_title == "halo1":
            if not asset_type == ModelTypeEnum.physics:
                model_name = ""
        else:
            model_name = ""

    filename = filename + model_name + extension

    return filename

def get_directory(context, game_title, asset_type, folder_structure, is_bsp, is_jmi, filepath):
    directory = filepath.rsplit(os.sep, 1)[0]
    blend_filename = bpy.path.basename(context.blend_data.filepath)

    parent_folder = 'default'
    if len(blend_filename) > 0:
        parent_folder = blend_filename.rsplit('.', 1)[0]

    if asset_type == ModelTypeEnum.render:
        if game_title == "halo1":
            folder_type = "models"

        else:
            if is_bsp:
                folder_type = "structure"

            else:
                folder_type = "render"

    elif asset_type == ModelTypeEnum.collision:
        if game_title == "halo1":
            folder_type = "physics"

        else:
            folder_type = "collision"

    elif asset_type == ModelTypeEnum.physics:
        folder_type = "physics"

    elif asset_type == ModelTypeEnum.animations:
        folder_type = "animations"

    root_directory = directory

    if is_jmi:
        root_directory = directory + os.sep + folder_type
        if not os.path.exists(root_directory):
            os.makedirs(root_directory)

    if folder_structure and not is_jmi:
        folder_subdirectories = ("models", "structure", "render", "collision", "physics", "animations")
        true_directory = directory
        if not os.path.basename(directory).lower() in folder_subdirectories: # Check if last folder in file path is not a valid source import folder
            if os.path.basename(directory).lower() == parent_folder.lower(): # Check if last folder in file path matches the Blend filename
                true_directory = os.path.dirname(directory)

            # This bit is pointless since true_directory is already set to directory which is what this would have done anyways. Leaving it here in case I need it in the future.
            #else: # Otherwise check if a folder in directory matches the Blend filename
                #for name in os.listdir(directory):
                    #if os.path.isdir(os.path.join(directory, name)) and name.lower() == parent_folder.lower():
                        #break

        else: # Otherwise check if the parent of the source import directory matches our Blend filename
            if os.path.basename(os.path.dirname(directory)).lower() == parent_folder.lower():
                true_directory = os.path.dirname(os.path.dirname(directory))

        root_directory = true_directory + os.sep + parent_folder + os.sep + folder_type
        if not os.path.exists(root_directory):
            os.makedirs(root_directory)

    return root_directory

def string_empty_check(string):
    is_empty = False
    if not string == None and (len(string) == 0 or string.isspace()):
        is_empty = True

    return is_empty

def material_definition_helper(triangle_material_index, mat):
    lod = None
    region = None
    permutation = None
    material_definition = ""
    if not triangle_material_index == -1:
        lod = mat.lod
        region = mat.region
        permutation = mat.permutation
        if not lod == None:
            material_definition += mat.lod

        if not permutation == None and not string_empty_check(permutation):
            if not string_empty_check(material_definition):
                material_definition += " "

            material_definition += permutation

        if not region == None and not string_empty_check(region):
            if not string_empty_check(material_definition):
                material_definition += " "

            material_definition += region

    return material_definition

def material_definition_parser(is_import, material_definition_items, default_region, default_permutation):
    lod_list = ['l1', 'l2', 'l3', 'l4', 'l5', 'l6']
    slot_index = None
    lod = None
    region = None
    permutation = None

    if len(material_definition_items) == 1:
        item_0 = material_definition_items[0].lower()
        if item_0.startswith("(") and item_0.endswith(')'):
            slot_index = material_definition_items[0]

        elif item_0 in lod_list:
            lod = material_definition_items[0]

        else:
            permutation = material_definition_items[0]

    elif len(material_definition_items) == 2:
        item_0 = material_definition_items[0].lower()
        item_1 = material_definition_items[1].lower()
        if item_0.startswith("(") and item_0.endswith(')'):
            slot_index = material_definition_items[0]

        elif item_0 in lod_list:
            lod = material_definition_items[0]

        else:
            permutation = material_definition_items[0]

        if item_1.startswith("(") and item_1.endswith(')'):
            slot_index = material_definition_items[1]

        elif item_1 in lod_list:
            lod = material_definition_items[1]

        else:
            if permutation == None:
                permutation = material_definition_items[1]

            else:
                region = material_definition_items[1]

    elif len(material_definition_items) == 3:
        item_0 = material_definition_items[0].lower()
        item_1 = material_definition_items[1].lower()
        item_2 = material_definition_items[2].lower()
        if item_0.startswith("(") and item_0.endswith(')'):
            slot_index = material_definition_items[0]

        elif item_0 in lod_list:
            lod = material_definition_items[0]

        else:
            permutation = material_definition_items[0]

        if item_1.startswith("(") and item_1.endswith(')'):
            slot_index = material_definition_items[1]

        elif item_1 in lod_list:
            lod = material_definition_items[1]

        else:
            if permutation == None:
                permutation = material_definition_items[1]

            else:
                region = material_definition_items[1]

        if item_2.startswith("(") and item_2.endswith(')'):
            slot_index = material_definition_items[2]

        elif item_2 in lod_list:
            lod = material_definition_items[2]

        else:
            if permutation == None:
                permutation = material_definition_items[2]

            else:
                region = material_definition_items[2]

    elif len(material_definition_items) == 4:
        slot_index = material_definition_items[0]
        lod = material_definition_items[1]
        permutation = material_definition_items[2]
        region = material_definition_items[3]

    if not is_import:
        if permutation == None:
            permutation = default_permutation

        if region == None:
            region = default_region

    return lod, permutation, region

def get_import_matrix(transform):
    translation = Matrix.Translation(transform.translation)
    rotation = transform.rotation.to_matrix().to_4x4()
    scale = Matrix.Scale(transform.scale, 4)

    transform_matrix = translation @ rotation @ scale

    return transform_matrix

def get_absolute_matrix(node_list, frame, transforms):
    absolute_matrices = []
    for node_idx, node in enumerate(node_list):
        transform = transforms[frame][node_idx]
        transform_matrix = get_import_matrix(transform)
        if not node.parent == None and node.parent != -1:
            parent_node_idx = node.parent
            parent_transform_matrix = absolute_matrices[parent_node_idx]
            transform_matrix = parent_transform_matrix @ transform_matrix

        absolute_matrices.append(transform_matrix)

    return absolute_matrices

def get_transform(import_version, export_version, node, frame, node_list, transforms, absolute_matrix):
    node_idx = node_list.index(node)
    transform = transforms[frame][node_idx]

    transform_matrix = get_import_matrix(transform)

    if import_version >= 16394 and export_version < 16394:
        if not node.parent == None and node.parent != -1:
            parent_node_idx = node_list.index(node_list[node.parent])
            parent_transform = transforms[frame][parent_node_idx]

            parent_transform_matrix = get_import_matrix(parent_transform)
            transform_matrix = parent_transform_matrix.inverted() @ transform_matrix

    elif import_version < 16394 and export_version >= 16394:
        if not node.parent == None and node.parent != -1:
            parent_node_idx = node_list.index(node_list[node.parent])
            parent_transform_matrix = absolute_matrix[parent_node_idx]
            transform_matrix = parent_transform_matrix @ transform_matrix

    return transform_matrix

def build_bounds_list(SCNR_ASSET, bsp_bounds_list):
    for structure_bsp_element in SCNR_ASSET.structure_bsps:
        bsp_bounds = []
        BSP_ASSET = structure_bsp_element.structure_bsp.parse_tag(print, "halo2", "retail")
        if BSP_ASSET:
            bsp_bounds.append(BSP_ASSET.level_body.world_bounds_x)
            bsp_bounds.append(BSP_ASSET.level_body.world_bounds_y)
            bsp_bounds.append(BSP_ASSET.level_body.world_bounds_z)

            bsp_bounds_list.append(bsp_bounds)

def get_origin_bsp(bsp_bounds_list, object_element):
    bsp_index = -1
    for bsp_idx, bsp_bounds in enumerate(bsp_bounds_list):
        x_min, x_max = bsp_bounds[0]
        y_min, y_max = bsp_bounds[1]
        z_min, z_max = bsp_bounds[2]
        x, y, z = object_element.position
        if x_min < x and x_max > x and y_min < y and y_max > y and z_min < z and z_max > z:
            bsp_index = bsp_idx
            break

    return bsp_index

def run_code(code_string):
    from .. import config
    def toolset_exec(code):
        if config.ENABLE_PROFILING:
            import cProfile
            cProfile.runctx(code, globals(), caller_locals)

        elif config.ENABLE_DEBUG:
            import pdb
            pdb.runctx(code, globals(), caller_locals)

        else:
            exec(code, globals(), caller_locals)

    import inspect
    from .. import crash_report
    frame = inspect.currentframe()
    try:
        caller_locals = frame.f_back.f_locals
        report = caller_locals['self'].report

        # this hack is horrible but it works??
        toolset_exec(f"""locals()['__this_is_a_horrible_hack'] = {code_string}""")
        result = caller_locals['__this_is_a_horrible_hack']
        caller_locals.pop('__this_is_a_horrible_hack', None)
        return result

    except ParseError as parse_error:
        crash_report.report_crash()
        report({'ERROR'}, "Bad data: {0}".format(parse_error))
        return {'CANCELLED'}

    except:
        crash_report.report_crash()
        info = sys.exc_info()
        report({'ERROR'}, "Internal error: {1}({0})".format(info[1], info[0]))
        return {'CANCELLED'}

    finally:
        del frame
