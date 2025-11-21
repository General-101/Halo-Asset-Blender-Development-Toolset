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

from math import radians
from mathutils import Matrix
from ..global_functions import mesh_processing, global_functions, resource_management

from ..file_tag.tag_interface import tag_interface, tag_common
from ..file_tag.tag_interface.tag_definitions import h1, h2
from ..file_tag.h1.file_model_animations.animation_parser import JMA_RETAIL_NODES

def generate_jms_skeleton(JMS_A_nodes, JMS_A, JMS_B_nodes, JMS_B, JMA, armature, fix_rotations, game_version):
    created_bone_list = []
    file_version = JMA.version
    r_hand_idx = None
    is_fp_root_file_a = False
    file_type = "JMS"

    bpy.ops.object.mode_set(mode = 'EDIT')
    for idx, jma_node in enumerate(JMA.nodes):
        created_bone_list.append(jma_node.name)
        current_bone = armature.data.edit_bones.new(jma_node.name)
        if "r_hand" == global_functions.remove_node_prefix(jma_node.name).lower() or "r hand" == global_functions.remove_node_prefix(jma_node.name).lower():
            r_hand_idx = idx

        parent = None
        parent_name = None
        jms_node = None
        bone_distance = 5

        for a_idx, jms_a_node in enumerate(JMS_A_nodes):
            if global_functions.remove_node_prefix(jma_node.name).lower() == global_functions.remove_node_prefix(jms_a_node).lower():
                if global_functions.remove_node_prefix(JMA.nodes[0].name).lower() == global_functions.remove_node_prefix(JMS_A_nodes[0]).lower():
                    is_fp_root_file_a = True

                file_version = JMS_A.version
                parent_idx = JMS_A.nodes[a_idx].parent
                parent_name = JMS_A.nodes[parent_idx].name
                rest_position = JMS_A.transforms[0]
                jms_node = rest_position[a_idx]
                bone_distance = mesh_processing.get_bone_distance(JMS_A, a_idx, "JMS")
                break

        for b_idx, jms_b_node in enumerate(JMS_B_nodes):
            if global_functions.remove_node_prefix(jma_node.name).lower() == global_functions.remove_node_prefix(jms_b_node).lower():
                file_version = JMS_B.version
                parent_idx = JMS_B.nodes[b_idx].parent
                parent_name = JMS_B.nodes[parent_idx].name
                rest_position = JMS_B.transforms[0]
                jms_node = rest_position[b_idx]
                bone_distance = mesh_processing.get_bone_distance(JMS_B, b_idx, "JMS")
                break

        if not jms_node:
            if is_fp_root_file_a:
                rest_position = JMS_A.transforms[0]

            else:
                rest_position = JMS_B.transforms[0]

            jms_node = rest_position[0]

        current_bone.tail[2] = bone_distance

        for bone_idx, bone in enumerate(created_bone_list):
            if not parent_name == None:
                if global_functions.remove_node_prefix(bone).lower == global_functions.remove_node_prefix(parent_name).lower:
                    parent = armature.data.edit_bones[bone_idx]

            else:
                parent = armature.data.edit_bones[0]

        matrix_translate = Matrix.Translation(jms_node.translation)
        matrix_rotation = jms_node.rotation.to_matrix().to_4x4()

        if not parent == None:
            current_bone.parent = parent

        elif "gun" in global_functions.remove_node_prefix(jma_node.name).lower():
            current_bone.parent = armature.data.edit_bones[r_hand_idx]

        is_root = False
        if JMS_A:
            if global_functions.remove_node_prefix(jma_node.name).lower() == global_functions.remove_node_prefix(JMS_A.nodes[0].name).lower():
                is_root = True

        if JMS_B:
            if global_functions.remove_node_prefix(jma_node.name).lower() == global_functions.remove_node_prefix(JMS_B.nodes[0].name).lower():
                is_root = True

        transform_matrix = matrix_translate @ matrix_rotation
        if fix_rotations:
            if file_version < global_functions.get_version_matrix_check(file_type) and current_bone.parent and not is_root:
                transform_matrix = (current_bone.parent.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix

            current_bone.matrix = transform_matrix @ Matrix.Rotation(radians(-90.0), 4, 'Z')

        else:
            if file_version < global_functions.get_version_matrix_check(file_type) and current_bone.parent and not is_root:
                transform_matrix = current_bone.parent.matrix @ transform_matrix

            current_bone.matrix = transform_matrix

def generate_jma_skeleton(JMS_A_nodes, JMS_A, JMS_A_invalid, JMS_B_nodes, JMS_B, JMS_B_invalid, JMA, armature, parent_id_class, fix_rotations, game_version):
    file_version = JMA.version
    first_frame = JMA.transforms[0]

    file_type = "JMA"
    if JMS_A and not JMS_A_invalid:
        file_type = "JMS"

    bpy.ops.object.mode_set(mode = 'EDIT')
    for idx, jma_node in enumerate(JMA.nodes):
        current_bone = armature.data.edit_bones.new(jma_node.name)
        parent_idx = jma_node.parent

        if not parent_idx == -1 and not parent_idx == None:
            if 'thigh' in jma_node.name and not parent_id_class.pelvis == None and not parent_id_class.thigh0 == None and not parent_id_class.thigh1 == None:
                parent_idx = parent_id_class.pelvis

            elif 'clavicle' in jma_node.name and not parent_id_class.spine1 == None and not parent_id_class.clavicle0 == None and not parent_id_class.clavicle1 == None:
                parent_idx = parent_id_class.spine1

            parent = JMA.nodes[parent_idx].name
            current_bone.parent = armature.data.edit_bones[parent]

        bone_distance = mesh_processing.get_bone_distance(JMA, idx, "JMA")

        matrix_translate = Matrix.Translation(first_frame[idx].translation)
        matrix_rotation = first_frame[idx].rotation.to_matrix().to_4x4()

        if JMS_A and not JMS_A_invalid and not JMS_B_invalid:
            for a_idx, jms_a_node in enumerate(JMS_A_nodes):
                if global_functions.remove_node_prefix(jma_node.name).lower() == global_functions.remove_node_prefix(jms_a_node).lower():
                    file_version = JMS_A.version
                    rest_position = JMS_A.transforms[0]
                    jms_node = rest_position[a_idx]
                    bone_distance = mesh_processing.get_bone_distance(JMS_A, a_idx, "JMS")
                    break

            for b_idx, jms_b_node in enumerate(JMS_B_nodes):
                if global_functions.remove_node_prefix(jma_node.name).lower() == global_functions.remove_node_prefix(jms_b_node).lower():
                    file_version = JMS_B.version
                    rest_position = JMS_B.transforms[0]
                    jms_node = rest_position[b_idx]
                    bone_distance = mesh_processing.get_bone_distance(JMS_B, b_idx, "JMS")
                    break

            matrix_translate = Matrix.Translation(jms_node.translation)
            matrix_rotation = jms_node.rotation.to_matrix().to_4x4()

        current_bone.tail[2] = bone_distance

        is_root = False
        if JMS_A and not JMS_A_invalid:
            if global_functions.remove_node_prefix(jma_node.name).lower() == global_functions.remove_node_prefix(JMS_A.nodes[0].name).lower():
                is_root = True

        if JMS_B and not JMS_B_invalid:
            if global_functions.remove_node_prefix(jma_node.name).lower() == global_functions.remove_node_prefix(JMS_B.nodes[0].name).lower():
                is_root = True

        transform_matrix = matrix_translate @ matrix_rotation
        if fix_rotations:
            if file_version < global_functions.get_version_matrix_check(file_type) and current_bone.parent and not is_root:
                transform_matrix = (current_bone.parent.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix

            current_bone.matrix = transform_matrix @ Matrix.Rotation(radians(-90.0), 4, 'Z')

        else:
            if file_version < global_functions.get_version_matrix_check(file_type) and current_bone.parent and not is_root:
                transform_matrix = current_bone.parent.matrix @ transform_matrix

            current_bone.matrix = transform_matrix

    bpy.ops.object.mode_set(mode = 'OBJECT')

def set_parent_id_class(JMA, parent_id_class):
    for idx, jma_node in enumerate(JMA.nodes):
        if 'pelvis' in jma_node.name:
            parent_id_class.pelvis = idx

        if 'thigh' in jma_node.name:
            if parent_id_class.thigh0 == None:
                parent_id_class.thigh0 = idx

            else:
                parent_id_class.thigh1 = idx

        elif 'spine1' in jma_node.name:
            parent_id_class.spine1 = idx

        elif 'clavicle' in jma_node.name:
            if parent_id_class.clavicle0 == None:
                parent_id_class.clavicle0 = idx

            else:
                parent_id_class.clavicle1 = idx

def jms_file_check(JMS_A, JMS_B, JMA_nodes, report):
    JMS_A_nodes = []
    JMS_A_invalid = False
    JMS_B_nodes = []
    JMS_B_invalid = False
    if JMS_A and not JMS_B:
        for jms_node in JMS_A.nodes:
            JMS_A_nodes.append(global_functions.remove_node_prefix(jms_node.name).lower())

        for jms_node_name in JMS_A_nodes:
            if not jms_node_name in JMA_nodes:
                JMS_A_invalid = True
                report({'WARNING'}, "Node '%s' from JMS skeleton not found in JMA skeleton." % jms_node_name)

        report({'WARNING'}, "No valid armature detected. Attempting to created one and the referenced JMS will be used for the rest position")

    elif JMS_A and JMS_B:
        for jms_node in JMS_A.nodes:
            JMS_A_nodes.append(global_functions.remove_node_prefix(jms_node.name).lower())

        for jms_node in JMS_B.nodes:
            JMS_B_nodes.append(global_functions.remove_node_prefix(jms_node.name).lower())

        jms_nodes = JMS_A_nodes + JMS_B_nodes

        for jms_node_name in jms_nodes:
            if not jms_node_name in JMA_nodes:
                JMS_B_invalid = True
                report({'WARNING'}, "Node '%s' from JMS skeleton not found in JMA skeleton." % jms_node_name)

        report({'WARNING'}, "No valid armature detected. Attempting to created one and the referenced JMS files will be used for the rest position")

    return JMS_A_nodes, JMS_B_nodes, JMS_A_invalid, JMS_B_invalid

def find_valid_armature(context, JMA, obj):
    is_armature_good = False
    valid_armature = None
    scene_nodes = []
    if JMA.version == 16390:
        if len(obj.data.bones) == JMA.node_count:
            is_armature_good = True

    else:
        armature_bone_list = list(obj.data.bones)
        for node in armature_bone_list:
            for jma_node in JMA.nodes:
                if node.name.lower() == jma_node.name.lower():
                    scene_nodes.append(global_functions.remove_node_prefix(node.name).lower())

        if len(scene_nodes) == len(JMA.nodes):
            is_armature_good = True

    if is_armature_good:
        valid_armature = obj
        mesh_processing.select_object(context, valid_armature)

    return scene_nodes, valid_armature

def build_scene(context, JMA, JMS_A, JMS_B, filepath, game_version, fix_parents, fix_rotations, report):
    collection = context.collection
    scene = context.scene
    view_layer = context.view_layer
    armature = None
    hidden_geo = False
    nonrender_geo = True
    active_object = view_layer.objects.active

    layer_collection_list = []
    object_list = []

    # Gather all scene resources that fit export criteria
    resource_management.gather_scene_resources(context, layer_collection_list, object_list, hidden_geo, nonrender_geo)

    if active_object and active_object.type == 'ARMATURE':
        armature = active_object
    
    game_title = "halo1"
    if len(JMA.nodes) == 0:
        asset_cache = {}

        output_dir = os.path.join(os.path.dirname(tag_common.h1_defs_directory), "h1_merged_output")
        tag_groups = tag_common.h1_tag_groups
        tag_extensions = tag_common.h1_tag_extensions
        engine_tag = tag_interface.EngineTag.H1Latest.value
        merged_defs = h1.generate_defs(tag_common.h1_defs_directory, output_dir)
        tags_directory = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_tag_path
        data_directory = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_data_path

        if not global_functions.string_empty_check(data_directory):
            result = filepath.split(data_directory, 1)
            if len(result) > 1:
                local_path = result[1]
                output_directory = os.path.dirname(os.path.dirname(local_path))
                output_filename = os.path.basename(output_directory)

                tag_ref = {"group name": "mod2", "path": os.path.join(output_directory, output_filename)}
                tag_interface.generate_tag_dictionary(game_title, tag_ref, tags_directory, tag_groups, engine_tag, merged_defs, asset_cache)

                gbxmodel_asset = tag_interface.get_disk_asset(tag_ref["path"], tag_groups.get(tag_ref["group name"]))
                if gbxmodel_asset is not None:
                    nodes = []
                    for node in gbxmodel_asset["Data"]["nodes"]:
                        name = node["name"]
                        sibling = node["next sibling node"]
                        child = node["first child node"]
                        parent = node["parent node"]

                        JMA.nodes.append(JMA.Node(name, parent, child, sibling))

            else:
                report({'ERROR'}, "Invalid input provided. Check your data directory settings and make sure the file exists in your data directory.")
        else:
            report({'ERROR'}, "Invalid data directory path provided. Check your data directory settings.")

    if len(JMA.nodes) == 0:
        anim_nodes = JMA_RETAIL_NODES.get((JMA.node_count, JMA.node_checksum))
        if anim_nodes is not None:
            nodes = []
            for node in anim_nodes:
                name = node[0]
                sibling = node[2]
                child = node[1]
                parent = node[3]

                JMA.nodes.append(JMA.Node(name, parent, child, sibling))

    if len(JMA.nodes) == 0 and armature is not None:
        nodes = []
        sorted_list = global_functions.sort_by_layer(list(armature.data.bones), armature)
        joined_list = sorted_list[0]
        reversed_joined_list = sorted_list[1]

        for node in joined_list:
            is_bone = False
            if armature:
                is_bone = True

            find_child_node = global_functions.get_child(node, reversed_joined_list, game_title, False)
            find_sibling_node = global_functions.get_sibling(armature, node, reversed_joined_list, game_title, False)

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

    nodes = JMA.nodes
    scene_nodes = []
    jma_nodes = [global_functions.remove_node_prefix(n.name).lower() for n in JMA.nodes]

    if armature:
        armature_bone_list = list(armature.data.bones)
        for node in armature_bone_list:
            for jma_node in JMA.nodes:
                if node.name.lower() == jma_node.name.lower():
                    scene_nodes.append(global_functions.remove_node_prefix(node.name).lower())

    else:
        for obj in object_list:
            if obj.type == 'ARMATURE':
                scene_nodes, armature = find_valid_armature(context, JMA, obj)
                if armature:
                    break

    if armature:
        for jma_node in jma_nodes:
            if jma_node not in scene_nodes:
                report({'WARNING'}, f"Node '{jma_node}' not found in an existing armature")
    else:
        parent_id_class = global_functions.ParentIDFix()
        JMS_A_nodes, JMS_B_nodes, JMS_A_invalid, JMS_B_invalid = jms_file_check(JMS_A, JMS_B, jma_nodes, report)

        if not JMA.broken_skeleton and JMA.version >= 16392:
            armdata = bpy.data.armatures.new('Armature')
            armature = bpy.data.objects.new('Armature', armdata)
            armature.color = (1, 1, 1, 0)
            collection.objects.link(armature)
            mesh_processing.select_object(context, armature)

            if fix_parents and game_version in {"halo2", "halo3"}:
                set_parent_id_class(JMA, parent_id_class)

            generate_jma_skeleton(JMS_A_nodes, JMS_A, JMS_A_invalid, JMS_B_nodes, JMS_B, JMS_B_invalid, JMA, armature, parent_id_class, fix_rotations, game_version)

        elif JMS_A:
            armdata = bpy.data.armatures.new('Armature')
            armature = bpy.data.objects.new('Armature', armdata)
            armature.color = (1, 1, 1, 0)
            collection.objects.link(armature)
            mesh_processing.select_object(context, armature)
            generate_jms_skeleton(JMS_A_nodes, JMS_A, JMS_B_nodes, JMS_B, JMA, armature, fix_rotations, game_version)

        else:
            report({'ERROR'}, "No valid armature detected and animation graph is invalid. Import will now be aborted")
            return {'CANCELLED'}

    scene.render.fps = JMA.frame_rate
    animation_filename = bpy.path.basename(filepath).rsplit('.', 1)[0]
    action = bpy.data.actions.get(animation_filename) or bpy.data.actions.new(name=animation_filename)

    action.use_frame_range = True
    action.frame_start = 1
    action.frame_end = JMA.frame_count

    armature.animation_data_create()
    armature.animation_data.action = action

    global_functions.import_fcurve_data(action, armature, nodes, JMA.transforms, JMA, fix_rotations)
    if (4, 4, 0) <= bpy.app.version:
        armature.animation_data.action_slot = action.slots[0]

    report({'INFO'}, "Import completed successfully")
    return {'FINISHED'}
