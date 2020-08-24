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
import bmesh
import mathutils

from numpy import array
from io_scene_halo.global_functions import global_functions

def load_file(context, filepath, report):
    processed_file = []
    encode = global_functions.test_encoding(filepath)
    file = open(filepath, "r", encoding=encode)
    foutput = open("C:\\Users\\Steven\\Desktop\\Test.JMA", "w")
    for line in file:
        if not line.strip(): continue
        if not line.startswith(";"):
            processed_file.append(line.replace('\n', ''))
            foutput.write('%s' % line)

    armature = []
    node_list = []
    parent_list = []
    node_matrix = []
    translation_list = []
    node_index = 0
    frame_index = 0
    version = int(processed_file[0])

    version_list = [16390,16391,16392,16393,16394,16395]
    if not version in version_list:
        report({'ERROR'}, 'Importer does not support this %s version' % global_functions.get_true_extension(filepath, None, True))
        return {'CANCELLED'}

    if version > 16394:
        node_checksum = int(processed_file[1])
        transform_count = int(processed_file[2])
        frame_rate = int(processed_file[3])
        actor_count = int(processed_file[4])
        actor_name = processed_file[5]
        node_count = int(processed_file[6])

    else:
        transform_count = int(processed_file[1])
        frame_rate = int(processed_file[2])
        actor_count = int(processed_file[3])
        actor_name = processed_file[4]
        node_count = int(processed_file[5])
        node_checksum = int(processed_file[6])

    armdata = bpy.data.armatures.new('Armature')
    ob_new = bpy.data.objects.new('Armature', armdata)
    bpy.context.collection.objects.link(ob_new)
    armature = ob_new
    bpy.context.view_layer.objects.active = armature
    bpy.context.scene.frame_end = transform_count
    bpy.context.scene.render.fps = frame_rate
    for node in range(node_count):
        node_name = processed_file[node_index + 7]
        parent_index = int(processed_file[node_index + 8])
        node_list.append(node_name)
        parent_list.append(parent_index)
        node_index += 2

    for frame in range(transform_count):
        for node in node_list:
            transform_matrix = None
            node_rotation = processed_file[frame_index + node_index + 7].split()
            node_translation = processed_file[frame_index + node_index + 8].split()
            node_scale = processed_file[frame_index + node_index + 9]
            quat = mathutils.Quaternion(((float(node_rotation[3]) * -1), float(node_rotation[0]), float(node_rotation[1]), float(node_rotation[2])))
            transform_matrix = quat.inverted().to_matrix().to_4x4()
            transform_matrix[0][3] = float(node_translation[0])
            transform_matrix[1][3] = float(node_translation[1])
            transform_matrix[2][3] = float(node_translation[2])
            node_matrix.append(transform_matrix)
            frame_index += 3

    for node in node_list:
        bpy.ops.object.mode_set(mode = 'EDIT')
        armature.data.edit_bones.new(node)
        armature.data.edit_bones[node].tail[2] = 5
        parent_name = None
        if not parent_list[node_list.index(node)] == -1:
            parent_name = parent_list[node_list.index(node)]

        if not parent_name == None:
            armature.data.edit_bones[node].parent = armature.data.edit_bones[node_list[int(parent_name)]]

        bpy.ops.object.mode_set(mode = 'POSE')
        armature.pose.bones[node].matrix = node_matrix[node_list.index(node)]

    bpy.ops.pose.armature_apply(selected=False)
    frame_index = 0
    frame_set = 0
    previous_frame_set = 0
    bpy.ops.object.mode_set(mode = 'POSE')
    for frame in range(transform_count):
        current_frame = frame + 1
        bpy.context.scene.frame_set(current_frame)
        if not frame == 0:
            previous_frame_set += 1

        for node in node_list:
            pose_bone = armature.pose.bones[node]
            node_matrix_index = node_list.index(pose_bone.name)
            node_matrix_set = node_count * frame_set
            node_matrix_previous_set = node_count * previous_frame_set
            #print(node_matrix_index + node_matrix_set)
            #local_matrix = node_matrix[node_matrix_index + node_matrix_previous_set].inverted() @ node_matrix[node_matrix_index + node_matrix_set]
            #global_matrix = node_matrix[node_matrix_index + node_matrix_set]
            armature.pose.bones[node].matrix = node_matrix[node_matrix_index + node_matrix_set]
            armature.pose.bones[node].keyframe_insert('location', index=-1)
            armature.pose.bones[node].keyframe_insert('rotation_quaternion', index=-1)

        frame_set += 1

    for bone in armature.pose.bones:
        bone.location.zero()
        bone.rotation_quaternion.identity()

    biped_controller = processed_file[frame_index + node_index + 7]
    bpy.context.scene.frame_set(1)

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.import_scene.jma()
