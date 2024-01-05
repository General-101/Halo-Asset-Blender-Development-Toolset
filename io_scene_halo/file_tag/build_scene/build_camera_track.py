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

from mathutils import Vector, Matrix
from ...global_functions import mesh_processing

def generate_camera_track_skeleton(armature):

    bpy.ops.object.mode_set(mode = 'EDIT')
    current_bone = armature.data.edit_bones.new("frame_root")
    current_bone.tail[2] = 5

    current_bone.matrix = Matrix.Translation(Vector())

    bpy.ops.object.mode_set(mode = 'OBJECT')

def build_scene(context, CAMERATRACK, game_version, game_title, file_version, fix_rotations, empty_markers, report):
    scene = context.scene
    view_layer = context.view_layer
    collection = context.collection

    armdata = bpy.data.armatures.new('Armature')
    armature = bpy.data.objects.new('Armature', armdata)
    collection.objects.link(armature)

    mesh_processing.select_object(context, armature)

    generate_camera_track_skeleton(armature)

    scene.frame_end = len(CAMERATRACK.control_points)
    for control_point_idx, control_point in enumerate(CAMERATRACK.control_points):
        scene.frame_set(control_point_idx + 1)
        pose_bone = armature.pose.bones[0]

        matrix_rotation = control_point.orientation.to_matrix().to_4x4()
        matrix_translation = Matrix.Translation(control_point.position)
        transform_matrix = matrix_translation @ matrix_rotation

        pose_bone.matrix = transform_matrix
        pose_bone.rotation_euler = transform_matrix.to_euler()

        view_layer.update()

        pose_bone.keyframe_insert(data_path='location', group=pose_bone.name)
        pose_bone.keyframe_insert(data_path='rotation_euler', group=pose_bone.name)
        pose_bone.keyframe_insert(data_path='rotation_quaternion', group=pose_bone.name)
        pose_bone.keyframe_insert(data_path='scale', group=pose_bone.name)
