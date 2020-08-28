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

import bpy

from mathutils import Vector, Quaternion, Matrix
from io_scene_halo.global_functions import global_functions

def load_file(context, filepath, report):
    processed_file = []
    encode = global_functions.test_encoding(filepath)
    file = open(filepath, "r", encoding=encode)
    for line in file:
        if not line.strip(): continue
        if not line.startswith(";"):
            processed_file.append(line.replace('\n', ''))

    armature = []
    node_list = []
    child_list = []
    sibling_list = []
    parent_list = []
    node_index = 0
    frame_index = 0
    version = int(processed_file[0])

    version_list = [16390,16391,16392,16393,16394,16395]
    if not version in version_list:
        report({'ERROR'}, 'Importer does not support this %s version' % global_functions.get_true_extension(filepath, None, True))
        return {'CANCELLED'}

    if version >= 16394:
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

    armature = bpy.data.objects['Armature']
    bpy.context.view_layer.objects.active = armature
    bpy.context.scene.frame_end = transform_count
    bpy.context.scene.render.fps = frame_rate
    if version >= 16394:
        for node in range(node_count):
            node_name = processed_file[node_index + 7]
            parent_index = int(processed_file[node_index + 8])
            node_list.append(node_name)
            parent_list.append(parent_index)
            node_index += 2

    else:
        for node in range(node_count):
            node_name = processed_file[node_index + 7]
            child_node_index = int(processed_file[node_index + 8])
            sibling_node_index = int(processed_file[node_index + 9])
            node_list.append(node_name)
            child_list.append(child_node_index)
            sibling_list.append(sibling_node_index)
            node_index += 3

    for frame in range(transform_count):
        current_frame = frame + 1
        bpy.context.scene.frame_set(current_frame)
        for node in node_list:
            pose_bone = armature.pose.bones[node]
            node_translation = processed_file[frame_index + node_index + 7].split()
            node_rotation = processed_file[frame_index + node_index + 8].split()
            node_scale = processed_file[frame_index + node_index + 9]
            file_matrix = Quaternion(((float(node_rotation[3])), float(node_rotation[0]), float(node_rotation[1]), float(node_rotation[2]))).inverted().to_matrix().to_4x4()
            if version >= 16394:
                file_matrix = Quaternion(((float(node_rotation[3])), float(node_rotation[0]), float(node_rotation[1]), float(node_rotation[2]))).to_matrix().to_4x4()

            file_matrix[0][3] = float(node_translation[0])
            file_matrix[1][3] = float(node_translation[1])
            file_matrix[2][3] = float(node_translation[2])
            if version >= 16394:
                matrix = file_matrix

            else:
                matrix = file_matrix
                if pose_bone.parent:
                    matrix = pose_bone.parent.matrix @ file_matrix

            armature.pose.bones[node].matrix = matrix
            bpy.context.view_layer.update()
            armature.pose.bones[node].keyframe_insert('location')
            armature.pose.bones[node].keyframe_insert('rotation_quaternion')
            frame_index += 3

    if version == 16395:
        biped_controller = processed_file[frame_index + node_index + 7]

    bpy.context.scene.frame_set(1)

    report({'INFO'}, "Import completed successfully")
    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.import_scene.jma()
