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

from decimal import *

class JmsVertex:
    node_influence_count = '0'
    node0 = '-1'
    node1 = '-1'
    node2 = '-1'
    node3 = '-1'
    node0_weight = '0.0000000000'
    node1_weight = '0.0000000000'
    node2_weight = '0.0000000000'
    node3_weight = '0.0000000000'
    pos = None
    norm = None
    uv = None

class JmsDimensions:
    quat_i_a = '0'
    quat_j_a = '0'
    quat_k_a = '0'
    quat_w_a = '0'
    pos_x_a = '0'
    pos_y_a = '0'
    pos_z_a = '0'
    scale_x_a = '0'
    scale_y_a = '0'
    scale_z_a = '0'
    radius_a = '0'
    pill_z_a = '0'
    quat_i_b = '0'
    quat_j_b = '0'
    quat_k_b = '0'
    quat_w_b = '0'
    pos_x_b = '0'
    pos_y_b = '0'
    pos_z_b = '0'
    scale_x_b = '0'
    scale_y_b = '0'
    scale_z_b = '0'
    radius_b = '0'
    pill_z_b = '0'

class JmsTriangle:
    v0 = 0
    v1 = 0
    v2 = 0
    region = 0
    material = 0

def unhide_all_collections():
    for collection_viewport in bpy.context.view_layer.layer_collection.children:
        collection_viewport.exclude = False

    for collection_hide in bpy.data.collections:
        collection_hide.hide_viewport = False

def unhide_object(mesh):
    mesh.hide_set(False)
    mesh.hide_viewport = False

def get_child(bone, bone_list = [], *args):
    set_node = None
    for node in bone_list:
        if bone == node.parent and not set_node:
            set_node = node

    return set_node

def get_sibling(armature, bone, bone_list = [], *args):
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
            if armature:
                set_sibling = armature.data.bones['%s' % sibling_list[next_sibling_node].name]

            else:
                set_sibling = bpy.data.objects['%s' % sibling_list[next_sibling_node].name]

    return set_sibling

def get_encoding(game_version):
    encoding = None
    if game_version == 'haloce':
        encoding = 'utf_8'

    elif game_version == 'halo2':
        encoding = 'utf-16le'

    return encoding

def error_pass(armature_count, report, game_version, node_count, version, extension, geometry_list, marker_list, root_node_count, animation, mesh_frame_count, object_count):
    result = False
    h2_extension_list = ['JRMX', 'JMH']
    if armature_count >= 2:
        report({'ERROR'}, 'More than one armature object. Please delete all but one.')
        result = True

    elif game_version == 'haloce' and node_count == 0: #JMSv2 files can have JMS files without a node for physics.
        report({'ERROR'}, 'No nodes in scene. Add an armature or object mesh named frame')
        result = True

    elif game_version == 'haloce' and len(geometry_list) == 0 and len(marker_list) == 0 and not animation:
        report({'ERROR'}, 'No geometry in scene.')
        result = True

    elif version >= 8201 and game_version == 'haloce':
        report({'ERROR'}, 'This version is not supported for CE. Choose from 8197-8200 if you wish to export for CE.')
        result = True

    elif extension == '.JMP' and game_version == 'halo2':
        report({'ERROR'}, 'This extension is not used in Halo 2 Vista')
        result = True

    elif root_node_count >= 2:
        report({'ERROR'}, "More than one root node. Please remove or rename objects until you only have one root frame object.")
        result = True

    elif version >= 16393 and game_version == 'haloce' and animation:
        report({'ERROR'}, 'This version is not supported for Halo CE. Choose from 16390-16392 if you wish to export for Halo CE.')
        result = True

    elif extension in h2_extension_list and game_version == 'haloce':
        report({'ERROR'}, 'This extension is not used in Halo CE')
        result = True

    elif object_count == 0:
        report({'ERROR'}, 'No objects in scene.')
        result = True

    if not animation:
        if mesh_frame_count > 0 and armature_count > 0:
            report({'ERROR'}, "Using both armature and object mesh node setup. Choose one or the other.")
            result = True

    return result

def sort_by_layer(node_list, armature, reversed_list):
    layer_count = []
    layer_root = []
    root_list = []
    children_list = []
    reversed_children_list = []
    joined_list = []
    reversed_joined_list = []
    sort_list = []
    reversed_sort_list = []
    sorted_list = []
    for node in node_list:
        if node.parent == None:
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

    if reversed_list:
        sorted_list = reversed_joined_list

    else:
        sorted_list = joined_list

    return sorted_list

def sort_list(node_list, armature, reversed_list, game_version, version, animation):
    version = int(version)
    sorted_list = []
    if game_version == 'haloce':
        sorted_list = sort_by_layer(node_list, armature, reversed_list)

    elif game_version == 'halo2':
        if animation:
            if version <= 16394:
                sorted_list = sort_by_layer(node_list, armature, reversed_list)

            else:
                sorted_list = node_list

        else:
            if version <= 8204:
                sorted_list = sort_by_layer(node_list, armature, reversed_list)

            else:
                sorted_list = node_list

    return sorted_list

def test_encoding(filepath):
    UTF_8_BOM = b'\xef\xbb\xbf'
    UTF_16_BE_BOM = b'\xfe\xff'
    UTF_16_LE_BOM = b'\xff\xfe'

    data = open(filepath, 'rb')

    file_size = os.path.getsize(filepath)
    BOM = data.read(3)
    zero_count = 0

    encoding = None

    if BOM.startswith(UTF_8_BOM) or BOM.startswith(UTF_16_BE_BOM) or BOM.startswith(UTF_16_LE_BOM):
        if file_size & 1:
            encoding = 'utf-8-sig'

        else:
            if BOM.startswith(UTF_16_BE_BOM) or BOM.startswith(UTF_16_LE_BOM):
                encoding = 'utf-16'

    else:
        byte = data.read(1)
        while byte != b"":
            byte = data.read(1)
            if byte == b'\x00':
                zero_count =+ 1

        if zero_count > 0:
            if not byte == b'\x00':
                encoding = 'utf-16le'

            elif byte == b'\x00':
                encoding = 'utf-16be'

        else:
            encoding = 'utf-8'

    return encoding

def get_version(jms_version_console, jms_version_ce, jms_version_h2, game_version, console):
    version = None
    if console:
        version = int(jms_version_console)

    else:
        if game_version == 'haloce':
            version = int(jms_version_ce)

        if game_version == 'halo2':
            version = int(jms_version_h2)

    return version

def get_true_extension(filepath, extension, is_import):
    extension_list = ['.jma', '.jmm', '.jmt', '.jmo', '.jmr', '.jmrx', '.jmh', '.jmz', '.jmw', '.jms', '.jmp']
    true_extension = ''
    if is_import:
        true_extension = filepath.rsplit('.', 1)[1]

    else:
        extension_char = (len(extension))
        if not filepath[-(extension_char):].lower() in extension_list or not filepath[-(extension_char):].lower() in extension.lower():
            true_extension = extension

    return true_extension

def get_matrix(obj_a, obj_b, is_local, armature, joined_list, is_node, version):
    object_matrix = None
    if is_node:
        if armature:
            pose_bone = armature.pose.bones['%s' % (obj_a.name)]
            object_matrix = pose_bone.matrix
            if pose_bone.parent and not version >= 8205:
                #Files at or above 8205 use absolute transform instead of local transform for nodes
                object_matrix = pose_bone.parent.matrix.inverted() @ pose_bone.matrix

        else:
            object_matrix = obj_a.matrix_world
            if obj_a.parent and not version >= 8205:
                #Files at or above 8205 use absolute transform instead of local transform for nodes
                object_matrix = obj_a.parent.matrix_local @ obj_a.matrix_world

    else:
        if armature:
            object_matrix = obj_a.matrix_world
            if obj_b.parent_bone and is_local:
                parent_object = get_parent(armature, obj_b, joined_list, -1, False)
                object_matrix = parent_object.matrix_local.inverted() @ obj_a.matrix_world

        else:
            object_matrix = obj_a.matrix_world
            if obj_b.parent and is_local:
                parent_object = get_parent(armature, obj_b, joined_list, -1, False)
                object_matrix = parent_object.matrix_local.inverted() @ obj_a.matrix_world

    return object_matrix

def get_dimensions(mesh_a_matrix, mesh_a, mesh_b_matrix, mesh_b, invert, custom_scale, version, jms_vertex, is_vertex, is_bone, armature):
    object_dimensions = JmsDimensions()
    if is_vertex:
        pos = jms_vertex.pos
        JmsDimensions.pos_x_a = Decimal(pos[0] * custom_scale).quantize(Decimal('1.0000000000'))
        JmsDimensions.pos_y_a = Decimal(pos[1] * custom_scale).quantize(Decimal('1.0000000000'))
        JmsDimensions.pos_z_a = Decimal(pos[2] * custom_scale).quantize(Decimal('1.0000000000'))

    else:
        if mesh_a:
            pos  = mesh_a_matrix.translation
            quat = mesh_a_matrix.to_quaternion().inverted()
            if is_bone:
                pose_bone = armature.pose.bones[mesh_a.name]
                scale = pose_bone.scale

            else:
                scale = mesh_a.scale

            if not is_bone:
                dimension = mesh_a.dimensions

                #The reason this code exists is to try to copy how capsules work in 3DS Max.
                #To get original height for 3DS Max do (radius_jms * 2) + height_jms
                #The maximum value of radius is height / 2
                pill_radius = ((dimension[0] / 2) * custom_scale)
                pill_height = (dimension[2] * custom_scale) - (pill_radius * 2)
                if pill_height <= 0:
                    pill_height = 0

            JmsDimensions.quat_i_a = Decimal(quat[1]).quantize(Decimal('1.0000000000'))
            JmsDimensions.quat_j_a = Decimal(quat[2]).quantize(Decimal('1.0000000000'))
            JmsDimensions.quat_k_a = Decimal(quat[3]).quantize(Decimal('1.0000000000'))
            JmsDimensions.quat_w_a = Decimal(quat[0] * invert).quantize(Decimal('1.0000000000'))
            JmsDimensions.pos_x_a = Decimal(pos[0] * custom_scale).quantize(Decimal('1.0000000000'))
            JmsDimensions.pos_y_a = Decimal(pos[1] * custom_scale).quantize(Decimal('1.0000000000'))
            JmsDimensions.pos_z_a = Decimal(pos[2] * custom_scale).quantize(Decimal('1.0000000000'))
            JmsDimensions.scale_x_a = Decimal(scale[0]).quantize(Decimal('1.0000000000'))
            JmsDimensions.scale_y_a = Decimal(scale[1]).quantize(Decimal('1.0000000000'))
            JmsDimensions.scale_z_a = Decimal(scale[2]).quantize(Decimal('1.0000000000'))
            if not is_bone:
                JmsDimensions.dimension_x_a = Decimal(dimension[0] * custom_scale).quantize(Decimal('1.0000000000'))
                JmsDimensions.dimension_y_a = Decimal(dimension[1] * custom_scale).quantize(Decimal('1.0000000000'))
                JmsDimensions.dimension_z_a = Decimal(dimension[2] * custom_scale).quantize(Decimal('1.0000000000'))
                JmsDimensions.radius_a = Decimal(pill_radius).quantize(Decimal('1.0000000000'))
                JmsDimensions.pill_z_a = Decimal(pill_height).quantize(Decimal('1.0000000000'))

        if mesh_b:
            pos  = mesh_b_matrix.translation
            quat = mesh_b_matrix.to_quaternion().inverted()
            if is_bone:
                pose_bone = armature.pose.bones[mesh_b.name]
                scale = pose_bone.scale

            else:
                scale = mesh_b.scale

            if not is_bone:
                dimension = mesh_b.dimensions

                #The reason this code exists is to try to copy how capsules work in 3DS Max.
                #To get original height for 3DS Max do (radius_jms * 2) + height_jms
                #The maximum value of radius is height / 2
                pill_radius = ((dimension[0] / 2) * custom_scale)
                pill_height = (dimension[2] * custom_scale) - (pill_radius * 2)
                if pill_height <= 0:
                    pill_height = 0

            JmsDimensions.quat_i_b = Decimal(quat[1]).quantize(Decimal('1.0000000000'))
            JmsDimensions.quat_j_b = Decimal(quat[2]).quantize(Decimal('1.0000000000'))
            JmsDimensions.quat_k_b = Decimal(quat[3]).quantize(Decimal('1.0000000000'))
            JmsDimensions.quat_w_b = Decimal(quat[0] * invert).quantize(Decimal('1.0000000000'))
            JmsDimensions.pos_x_b = Decimal(pos[0] * custom_scale).quantize(Decimal('1.0000000000'))
            JmsDimensions.pos_y_b = Decimal(pos[1] * custom_scale).quantize(Decimal('1.0000000000'))
            JmsDimensions.pos_z_b = Decimal(pos[2] * custom_scale).quantize(Decimal('1.0000000000'))
            JmsDimensions.scale_x_b = Decimal(scale[0]).quantize(Decimal('1.0000000000'))
            JmsDimensions.scale_y_b = Decimal(scale[1]).quantize(Decimal('1.0000000000'))
            JmsDimensions.scale_z_b = Decimal(scale[2]).quantize(Decimal('1.0000000000'))
            if not is_bone:
                JmsDimensions.dimension_x_b = Decimal(dimension[0] * custom_scale).quantize(Decimal('1.0000000000'))
                JmsDimensions.dimension_y_b = Decimal(dimension[1] * custom_scale).quantize(Decimal('1.0000000000'))
                JmsDimensions.dimension_z_b = Decimal(dimension[2] * custom_scale).quantize(Decimal('1.0000000000'))
                JmsDimensions.radius_b = Decimal(pill_radius).quantize(Decimal('1.0000000000'))
                JmsDimensions.pill_z_b = Decimal(pill_height).quantize(Decimal('1.0000000000'))

    return object_dimensions

def get_extension(extension_console, extension_ce, extension_h2, game_version, console):
    extension = None
    if console:
        extension = extension_console

    else:
        if game_version == 'haloce':
            extension = extension_ce

        if game_version == 'halo2':
            extension = extension_h2

    return extension

def get_hierarchy(mesh):
    no_parent = False
    hierarchy_list = []
    current_mesh = mesh
    while no_parent == False:
        hierarchy_list.append(current_mesh)
        if not current_mesh.parent == None:
            current_mesh = current_mesh.parent

        else:
            no_parent = True

    return hierarchy_list

def get_parent(armature, mesh, joined_list, default_parent, get_index):
    parent_object = None
    parent_index = default_parent
    parent = None
    if armature:
        if mesh:
            if mesh.parent_bone:
                parent_object = armature.data.bones[mesh.parent_bone]
                parent_index = joined_list.index(parent_object)

    else:
        if mesh:
            if mesh.parent:
                if mesh.parent.hide_viewport == False and mesh.hide_get() == False and mesh.parent in joined_list:
                    parent_object = bpy.data.objects[mesh.parent.name]
                    parent_index = joined_list.index(parent_object)

                else:
                    done = False
                    mesh_hierarchy = get_hierarchy(mesh)
                    for item in mesh_hierarchy:
                        if item.hide_viewport == False and mesh_hierarchy.index(item) >= 1 and item in joined_list and done == False:
                            done = True
                            parent_object = bpy.data.objects[item.name]
                            parent_index = joined_list.index(parent_object)

    if get_index:
        parent = parent_index

    else:
        parent = parent_object

    return parent

def set_scale(scale_enum, scale_float):
    scale = 1
    if scale_enum == '1':
        scale = 100

    if scale_enum == '2':
        scale = scale_float

    return scale

def count_root_nodes(node_list):
    root_node_count = 0
    for node in node_list:
        if node.parent == None:
            root_node_count += 1

    return root_node_count
