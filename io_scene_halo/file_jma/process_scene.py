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

from math import radians
from .format import JMAAsset
from mathutils import Vector, Euler, Quaternion, Matrix
from ..global_functions import mesh_processing, global_functions, resource_management

def sort_by_parent(node_list):
    sorted_nodes = []
    visited = set()

    def visit(node_idx):
        if node_idx in visited:
            return
        parent_idx = node_list[node_idx].parent
        if parent_idx != -1:
            visit(parent_idx)
        visited.add(node_idx)
        sorted_nodes.append(node_idx)

    for idx in range(len(node_list)):
        visit(idx)

    return sorted_nodes

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
    resource_management.gather_scene_resources(context, layer_collection_list, object_list, hidden_geo, nonrender_geo)

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
    if active_object and active_object.animation_data:
        action = active_object.animation_data.action
        if action and action.use_frame_range:
            first_frame = int(action.frame_start)
            last_frame = int(action.frame_end) + 1
            JMA.frame_count = last_frame - first_frame

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

    local_matrices = []
    absolute_matrices = []
    armature_matrix = [armature.matrix_world]
    for node in joined_list:
        is_bone = armature and isinstance(node, bpy.types.Bone)
        if is_bone:
            data_bone = global_functions.get_data_bone(armature, node.name)
            if data_bone is None:
                continue

            absolute_matrix = data_bone.matrix_local
            local_matrix = absolute_matrix
            if data_bone.parent:
                local_matrix = data_bone.parent.matrix_local.inverted() @ absolute_matrix

            local_matrices.append(local_matrix)
            absolute_matrices.append(absolute_matrix)
        else:
            absolute_matrix = node.matrix_world
            local_matrix = absolute_matrix
            if node.parent:
                local_matrix = node.parent.matrix_world.inverted() @ absolute_matrix
            
            local_matrices.append(local_matrix)
            absolute_matrices.append(absolute_matrix)

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
        if not node.parent == None and not node.parent.name.startswith('!'):
            if armature:
                if node.parent.use_deform:
                    parent_node = joined_list.index(node.parent)
            else:
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

    if generate_checksum and len(JMA.nodes) > 0:
        JMA.node_checksum = global_functions.node_hierarchy_checksum(JMA.nodes, JMA.nodes[0], JMA.node_checksum)

    if armature:
        action = None
        fcurves = []
        if armature and armature.animation_data:
            action = armature.animation_data.action 
        if action:
            fcurves = action.fcurves

        fcurve_dict = {}
        for fc in fcurves:
            if fc.data_path.startswith('pose.bones["'):
                bone_name = fc.data_path.split('"')[1]
                key = ('bone', bone_name)
                fcurve_dict.setdefault(key, []).append(fc)

    temp_local_matrices = []
    for frame in range(first_frame, last_frame):
        frame_matrices = []
        for node_idx, node in enumerate(joined_list):
            local_matrix = global_functions.export_fcurve_data(action, fcurve_dict, armature, node, node_idx, frame, local_matrices)
            frame_matrices.append(local_matrix)
        temp_local_matrices.append(frame_matrices)

    unordered_map = sort_by_parent(JMA.nodes)
    absolute_matrices = []
    for frame_matrices in temp_local_matrices:
        abs_frame = []
        for node_idx, node in enumerate(JMA.nodes):
            local_matrix = frame_matrices[unordered_map[node_idx]]
            if node.parent is not None and node.parent != -1:
                parent_abs = abs_frame[node.parent]
                abs_matrix = parent_abs @ local_matrix
            else:
                abs_matrix = local_matrix
            abs_frame.append(abs_matrix)
        absolute_matrices.append(abs_frame)

    if fix_rotations:
        correction_rot_mat = Matrix.Rotation(radians(90.0), 4, 'Z')
        for frame_abs in absolute_matrices:
            for idx, abs_matrix in enumerate(frame_abs):
                loc, rot, scale = abs_matrix.decompose()
                rot_mat = rot.to_matrix().to_4x4()
                corrected_rot_mat = rot_mat @ correction_rot_mat
                corrected_matrix = Matrix.LocRotScale(loc, corrected_rot_mat.to_quaternion(), scale)
                frame_abs[idx] = corrected_matrix

    final_transforms = []
    if jma_version < 16394:
        for frame_abs in absolute_matrices:
            local_frame = []
            for node_idx, node in enumerate(JMA.nodes):
                if node.parent is not None and node.parent != -1:
                    parent_matrix = frame_abs[node.parent]
                    child_matrix = frame_abs[node_idx]
                    local_matrix = parent_matrix.inverted() @ child_matrix
                else:
                    local_matrix = frame_abs[node_idx]  # root node

                bone = joined_list[unordered_map[node_idx]]
                is_bone = armature and isinstance(bone, bpy.types.Bone)
                mesh_dimensions = global_functions.get_dimensions(local_matrix, bone, jma_version, is_bone, 'JMA', scale_value)
                local_frame.append(JMA.Transform(mesh_dimensions.position, mesh_dimensions.quaternion, mesh_dimensions.scale[0]))
            final_transforms.append(local_frame)

    else:
        for frame_abs in absolute_matrices:
            local_frame = []
            for node_idx, node in enumerate(JMA.nodes):
                local_matrix = frame_abs[node_idx]
                bone = joined_list[unordered_map[node_idx]]
                is_bone = armature and isinstance(bone, bpy.types.Bone)
                mesh_dimensions = global_functions.get_dimensions(local_matrix, bone, jma_version, is_bone, 'JMA', scale_value)
                local_frame.append(JMA.Transform(mesh_dimensions.position, mesh_dimensions.quaternion, mesh_dimensions.scale[0]))
            final_transforms.append(local_frame)

    JMA.transforms = final_transforms

    armature_transform = False
    if jma_version > 16394 and armature_transform:
        for frame in range(JMA.frame_count):
            transform_matrix = global_functions.export_fcurve_data(action, fcurve_dict, armature, armature, 0, frame, armature_matrix)
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
