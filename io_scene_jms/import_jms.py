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
import mathutils
from numpy import array

def test_encoding(filepath):
    UTF_8_BOM = b'\xef\xbb\xbf'
    UTF_16_BE_BOM = b'\xfe\xff'
    UTF_16_LE_BOM = b'\xff\xfe'

    data = open(filepath, 'rb')

    file_size = os.path.getsize(filepath)
    BOM = data.read(3)
    zero_count = 0

    if BOM.startswith(UTF_8_BOM) or BOM.startswith(UTF_16_BE_BOM) or BOM.startswith(UTF_16_LE_BOM):
        if file_size & 1:
            return 'utf-8-sig'

        else:
            if BOM.startswith(UTF_16_BE_BOM) or BOM.startswith(UTF_16_LE_BOM):
                return 'utf-16'

    else:
        byte = data.read(1)
        while byte != b"":
            byte = data.read(1)
            if byte == b'\x00':
                zero_count =+ 1

        if zero_count > 0:
            if not byte == b'\x00'
                return 'utf-16le'

            elif byte == b'\x00':
                return 'utf-16be'

        else:
            return 'utf-8'

def load_file(context, filepath, report):
    processed_file = []
    encode = test_encoding(filepath)
    file = open(filepath, "r", encoding=encode)
    #foutput = open("C:\\Users\\Steven\\Desktop\\Test.JMS", "w")
    for line in file:
        if not line.strip(): continue
        if not line.startswith(";"):
            processed_file.append(line.replace('\n', ''))
            foutput.write('%s' % line)

    armature = []
    node_list = []
    parent_list = []
    node_transforms = []
    translation_list = []
    node_index = 0
    vertex_index = 0
    version = int(processed_file[0])

    if not version == 8210:
        report({'ERROR'}, 'Only works with JMS 8210')
        return {'CANCELLED'}

    node_count = int(processed_file[1])
    material_count = int(processed_file[2 + (node_count * 4)])
    marker_count = int(processed_file[2 + (node_count * 4) + 1 + (material_count * 2)])
    instance_xref_path_count = int(processed_file[2 + (node_count * 4) + 1 + (material_count * 2) + 1 + (marker_count * 5)])
    instance_markers_count = int(processed_file[2 + (node_count * 4) + 1 + (material_count * 2) + 1 + (marker_count * 5) + 1 + (instance_xref_path_count * 2)])
    vert_count = int(processed_file[2 + (node_count * 4) + 1 + (material_count * 2) + 1 + (marker_count * 5) + 1 + (instance_xref_path_count * 2) + 1 + (instance_markers_count * 5)])

    armdata = bpy.data.armatures.new('Armature')
    ob_new = bpy.data.objects.new('Armature', armdata)
    bpy.context.collection.objects.link(ob_new)
    armature = ob_new
    bpy.context.view_layer.objects.active = armature

    for node in range(node_count):
        node_name = processed_file[node_index + 2]
        parent_index = processed_file[node_index + 3]
        node_list.append(node_name)
        parent_list.append(parent_index)
        node_rotation = processed_file[node_index + 4].split()
        node_translation = processed_file[node_index + 5].split()
        quat = mathutils.Quaternion((-float(node_rotation[3]), float(node_rotation[0]), float(node_rotation[1]), float(node_rotation[2])))
        transform_matrix = quat.to_matrix().to_4x4()
        transform_matrix[0][3] = float(node_translation[0])
        transform_matrix[1][3] = float(node_translation[1])
        transform_matrix[2][3] = float(node_translation[2])
        node_transforms.append(transform_matrix)
        bpy.ops.object.mode_set(mode = 'EDIT')
        armature.data.edit_bones.new('%s' % node_name)
        armature.data.edit_bones['%s' % node_name].tail[2] = 1
        node_index += 4

    for node in node_list:
        if node_list.index(node) == 0:
            parent_name = None

        else:
            parent_name = parent_list[int(node_list.index(node))]

        if not parent_name == None:
            bpy.ops.object.mode_set(mode = 'EDIT')
            armature.data.edit_bones[node].parent = armature.data.edit_bones[node_list[int(parent_name)]]

        bpy.ops.object.mode_set(mode = 'POSE')
        armature.pose.bones['%s' % node].matrix = node_transforms[int(node_list.index(node))]

    bpy.ops.pose.armature_apply(selected=False)
    bpy.ops.object.mode_set(mode = 'OBJECT')

    for vert in range(vert_count):
        starting_position = 2 + (node_count * 4) + 1 + (material_count * 2) + 1 + (marker_count * 5) + 1 + (instance_xref_path_count * 2) + 1 + (instance_markers_count * 5)
        vert_translation = processed_file[vertex_index + starting_position + 1]
        vert_normal = processed_file[vertex_index + starting_position + 2]
        vertex_group_count = processed_file[vertex_index + starting_position + 3]
        vert_translation_list = vert_translation.split()
        vert_normal_list = vert_normal.split()
        if not [vert_translation_list[0], vert_translation_list[1], vert_translation_list[2], vert_normal_list[0], vert_normal_list[1], vert_normal_list[2]] in translation_list:
            translation_list.append([vert_translation_list[0], vert_translation_list[1], vert_translation_list[2], vert_normal_list[0], vert_normal_list[1], vert_normal_list[2]])

        vertex_index += 5 + (int(vertex_group_count) * 2)

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.import_scene.jms()
