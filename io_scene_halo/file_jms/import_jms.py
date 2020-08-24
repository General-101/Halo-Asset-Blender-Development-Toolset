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
    #foutput = open("C:\\Users\\Steven\\Desktop\\Test.JMS", "w")
    for line in file:
        if not line.strip(): continue
        if not line.startswith(";"):
            processed_file.append(line.replace('\n', ''))
            #foutput.write('%s' % line)

    armature = []
    node_list = []
    parent_list = []
    node_transforms = []
    translation_list = []
    node_index = 0
    vertex_index = 0
    version = int(processed_file[0])

    version_list = [8209, 8210]
    if not version in version_list:
        report({'ERROR'}, 'Importer does not support this JMS version')
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
        quat = mathutils.Quaternion((float(node_rotation[3]), float(node_rotation[0]), float(node_rotation[1]), float(node_rotation[2])))
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

    verts = []
    mesh = bpy.data.meshes.new("mesh")
    obj = bpy.data.objects.new("MyObject", mesh)

    collection = bpy.context.collection
    view_layer = bpy.context.view_layer
    collection.objects.link(obj)
    view_layer.objects.active = obj
    obj.select_set(True)

    mesh = bpy.context.object.data
    bm = bmesh.new()

    for vert in range(vert_count):
        starting_position = 2 + (node_count * 4) + 1 + (material_count * 2) + 1 + (marker_count * 5) + 1 + (instance_xref_path_count * 2) + 1 + (instance_markers_count * 5)
        vert_translation = processed_file[vertex_index + starting_position + 1]
        vert_normal = processed_file[vertex_index + starting_position + 2]
        vertex_group_count = processed_file[vertex_index + starting_position + 3]
        vertex_uv_count = processed_file[vertex_index + starting_position + (int(vertex_group_count) * 2) + 4]
#        print('vert index: ', vert)
#        print('starting line position: ', starting_position + 1)
#        print('line position translation: ', vertex_index + starting_position + 1 + 1)
#        print('translation: ', vert_translation)
#        print('line position normal: ', vertex_index + starting_position + 2 + 1)
#        print('normal: ', vert_normal)
#        print('line position group count: ', vertex_index + starting_position + 3 + 1)
#        print('group count: ', vertex_group_count)
#        print('line position uv count: ', vertex_index + starting_position + (int(vertex_group_count) * 2) + 4 + 1)
#        print('uv count: ', vertex_uv_count)
#        print(' ')
        vert_translation_list = vert_translation.split()
        vert_normal_list = vert_normal.split()
        verts.append([float(vert_translation_list[0]), float(vert_translation_list[1]), float(vert_translation_list[2])])
        if not [vert_translation_list[0], vert_translation_list[1], vert_translation_list[2], vert_normal_list[0], vert_normal_list[1], vert_normal_list[2]] in translation_list:
            translation_list.append([vert_translation_list[0], vert_translation_list[1], vert_translation_list[2], vert_normal_list[0], vert_normal_list[1], vert_normal_list[2]])

        total_uv_lines = 0
        for x in range(int(vertex_uv_count)):
            total_uv_lines += 1

        vertex_index += 4 + (int(vertex_group_count) * 2 + total_uv_lines)

    for v in verts:
        bm.verts.new(v)

    bm.to_mesh(mesh)
    bm.free()

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.import_scene.jms()
