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
import json

from collections import defaultdict
from mathutils import Vector, Matrix
from ...global_functions import mesh_processing, global_functions
from ...file_tag.tag_interface import tag_interface, tag_common

def generate_camera_track_skeleton(armature, bone_name):
    bpy.ops.object.mode_set(mode = 'EDIT')
    current_bone = armature.data.edit_bones.new(bone_name)
    current_bone.tail[2] = 5

    current_bone.matrix = Matrix.Translation(Vector())

    bpy.ops.object.mode_set(mode = 'OBJECT')

def build_scene(context, tag_ref, asset_cache, game_title, fix_rotations, empty_markers, report):
    if game_title == "halo1":
        tag_groups = tag_common.h1_tag_groups
    elif game_title == "halo2":
        tag_groups = tag_common.h2_tag_groups
    else:
        print("%s is not supported." % game_title)

    track_data = tag_interface.get_disk_asset(tag_ref["path"], tag_groups.get(tag_ref["group name"]))["Data"]

    node_name = "frame_root"

    scene = context.scene
    collection = context.collection

    armdata = bpy.data.armatures.new('Armature')
    armature = bpy.data.objects.new('Armature', armdata)
    armature.color = (1, 1, 1, 0)
    collection.objects.link(armature)

    mesh_processing.select_object(context, armature)

    generate_camera_track_skeleton(armature, node_name)

    fcurve_map = defaultdict(lambda: defaultdict(dict))
    data_paths = {
        "location": 3,
        "rotation_euler": 3,
        "rotation_quaternion": 4,
        "scale": 3
    }

    anim_name = os.path.basename(tag_ref["path"])
    action = bpy.data.actions.get(anim_name)
    if action is None:
        action = bpy.data.actions.new(name=anim_name)

    armature.animation_data_create()
    armature.animation_data.action = action
    for bone in armature.pose.bones:
        bone_name = bone.name
        for path, count in data_paths.items():
            for index in range(count):
                fcurve_data_path = f'pose.bones["{bone_name}"].{path}'
                fcurve = global_functions.get_fcurve(action.fcurves, fcurve_data_path, index)
                if not fcurve:
                    fcurve = action.fcurves.new(data_path=fcurve_data_path, index=index, action_group=bone_name)

                fcurve_map[bone_name][path][index] = fcurve

    scene.frame_end = len(track_data["control points"])
    for control_point_idx, control_point in enumerate(track_data["control points"]):
        frame_number = control_point_idx + 1
        pose_bone = armature.pose.bones[0]

        rotation_quaternion = global_functions.convert_quaternion(control_point["orientation"]).inverted()

        matrix_rotation = rotation_quaternion.to_matrix().to_4x4()
        matrix_translation = Matrix.Translation(Vector(control_point["position"]) * 100)
        transform_matrix = matrix_translation @ matrix_rotation

        pose_bone = global_functions.get_pose_bone(armature, node_name)
        rotation_mode = 'QUATERNION'
        if pose_bone is not None:
            rotation_mode = pose_bone.rotation_mode

        loc, rot_quat, scl = transform_matrix.decompose()
        if rotation_mode !='QUATERNION':
            rot_euler = rot_quat.to_euler('XYZ')

        for i in range(3):
            fcurve_map[node_name]['location'][i].keyframe_points.insert(frame_number, loc[i], options={'FAST'})
            fcurve_map[node_name]['scale'][i].keyframe_points.insert(frame_number, scl[i], options={'FAST'})
            if rotation_mode == 'QUATERNION':
                fcurve_map[node_name]['rotation_quaternion'][i].keyframe_points.insert(frame_number, rot_quat[i], options={'FAST'})
            else:
                fcurve_map[node_name]['rotation_euler'][i].keyframe_points.insert(frame_number, rot_euler[i], options={'FAST'})

        if rotation_mode == 'QUATERNION':
            fcurve_map[node_name]['rotation_quaternion'][3].keyframe_points.insert(frame_number, rot_quat[3], options={'FAST'})

    if (4, 4, 0) <= bpy.app.version:
        armature.animation_data.action_slot = action.slots[0]
