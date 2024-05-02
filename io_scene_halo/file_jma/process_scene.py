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

import bpy

from .format import JMAAsset
from ..global_functions import mesh_processing, global_functions, resource_management

def find_valid_armature(context, obj):
    valid_armature = None
    node_list = []

    if obj.type == 'ARMATURE':
        armature_bones = obj.data.bones
        for bone in armature_bones:
            if bone.use_deform:
                node_list.append(bone)

        if len(node_list) > 0:
            valid_armature = obj

        mesh_processing.select_object(context, obj)

    return node_list, valid_armature

def process_scene(context, extension, jma_version, game_title, generate_checksum, fix_rotations, use_maya_sorting, scale_value):
    JMA = JMAAsset()
    JMA.node_checksum = 0

    hidden_geo = False
    nonrender_geo = True

    layer_collection_list = []
    object_list = []

    # Gather all scene resources that fit export criteria
    resource_management.gather_scene_resources(context, layer_collection_list, object_list, hidden_geo)

    # Store visibility for all relevant resources
    stored_collection_visibility = resource_management.store_collection_visibility(layer_collection_list)
    stored_object_visibility = resource_management.store_object_visibility(object_list)
    stored_modifier_visibility = resource_management.store_modifier_visibility(object_list)

    # Unhide all relevant resources for exporting
    resource_management.unhide_relevant_resources(layer_collection_list, object_list)

    armature = None
    node_list = []
    armature_count = 0
    first_frame = context.scene.frame_start
    last_frame = context.scene.frame_end + 1
    JMA.frame_count = context.scene.frame_end - first_frame + 1
    active_object = context.view_layer.objects.active
    mesh_frame_count = 0
    world_node_count = 0
    node_prefix_tuple = ('b ', 'b_', 'bone', 'frame', 'bip01')

    if not active_object == None and active_object in object_list:
        node_list, armature = find_valid_armature(context, active_object)
        if not armature == None:
            armature_count += 1

    if armature is None:
        for obj in object_list:
            name = obj.name.lower()
            if name[0:1] == '!':
                world_node_count += 1

            elif obj.type == 'ARMATURE':
                armature_bones = obj.data.bones
                for bone in armature_bones:
                    if bone.use_deform:
                        node_list.append(bone)

                if len(node_list) > 0:
                    armature = obj
                    armature_count += 1

            elif name.startswith(node_prefix_tuple):
                mesh_frame_count += 1
                node_list.append(obj)

    JMA.node_count = len(node_list)
    sorted_list = global_functions.sort_list(node_list, armature, game_title, jma_version, True)
    joined_list = sorted_list[0]
    reversed_joined_list = sorted_list[1]

    for node in joined_list:
        is_bone = False
        if armature:
            is_bone = True

        find_child_node = global_functions.get_child(node, reversed_joined_list, game_title, use_maya_sorting)
        find_sibling_node = global_functions.get_sibling(armature, node, reversed_joined_list, game_title, use_maya_sorting)

        first_child_node = -1
        first_sibling_node = -1
        parent_node = -1

        if not find_child_node == None:
            first_child_node = joined_list.index(find_child_node)
        if not find_sibling_node == None:
            first_sibling_node = joined_list.index(find_sibling_node)
        if not node.parent == None and node.parent.use_deform and not node.parent.name.startswith('!'):
            parent_node = joined_list.index(node.parent)

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

        JMA.nodes.append(JMA.Node(name, parent, child, sibling))

    if generate_checksum:
        JMA.node_checksum = global_functions.node_hierarchy_checksum(JMA.nodes, JMA.nodes[0], JMA.node_checksum)

    for frame in range(first_frame, last_frame):
        transforms_for_frame = []
        for node in joined_list:
            context.scene.frame_set(frame)
            is_bone = False
            if armature:
                is_bone = True
            armature_matrix = global_functions.get_matrix(armature, armature, True, None, joined_list, False, jma_version, 'JMA', False, scale_value, fix_rotations)
            bone_matrix = global_functions.get_matrix(node, node, True, armature, joined_list, True, jma_version, 'JMA', False, scale_value, fix_rotations)
            full_matrix = armature_matrix @ bone_matrix
            mesh_dimensions = global_functions.get_dimensions(full_matrix, node, jma_version, is_bone, 'JMA', scale_value)
            rotation = (mesh_dimensions.quaternion[0], mesh_dimensions.quaternion[1], mesh_dimensions.quaternion[2], mesh_dimensions.quaternion[3])
            translation = (mesh_dimensions.position[0], mesh_dimensions.position[1], mesh_dimensions.position[2])
            scale = (mesh_dimensions.scale[0])

            transforms_for_frame.append(JMA.Transform(translation, rotation, scale))

        JMA.transforms.append(transforms_for_frame)

    armature_transform = False
    if jma_version > 16394 and armature_transform:
        for frame in range(JMA.frame_count):
            context.scene.frame_set(frame)
            armature_matrix = global_functions.get_matrix(armature, armature, True, None, joined_list, False, jma_version, 'JMA', False, scale_value, fix_rotations)
            mesh_dimensions = global_functions.get_dimensions(armature_matrix, armature, jma_version, False, 'JMA', scale_value)

            rotation = (mesh_dimensions.quaternion[0], mesh_dimensions.quaternion[1], mesh_dimensions.quaternion[2], mesh_dimensions.quaternion[3])
            translation = (mesh_dimensions.position[0], mesh_dimensions.position[1], mesh_dimensions.position[2])
            scale = (mesh_dimensions.scale[0])

            JMA.biped_controller_transforms.append(JMA.Transform(translation, rotation, scale))

    # Restore visibility status for all resources
    resource_management.restore_collection_visibility(stored_collection_visibility)
    resource_management.restore_object_visibility(stored_object_visibility)
    resource_management.restore_modifier_visibility(stored_modifier_visibility)

    return JMA
