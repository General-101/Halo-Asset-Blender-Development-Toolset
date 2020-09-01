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
    node_transforms = []
    translation_list = []
    node_line_index = 0
    vertex_index = 0
    version = int(processed_file[0])

    version_list = [8197, 8198, 8199, 8200, 8201, 8202, 8203, 8204, 8205, 8206, 8207, 8208, 8209, 8210]
    if not version in version_list:
        report({'ERROR'}, 'Importer does not support this %s version' % global_functions.get_true_extension(filepath, None, True))
        return {'CANCELLED'}

    if version >= 8205:
        node_start = 1
        node_count = int(processed_file[node_start])
        material_start = 2 + (node_count * 4)
        material_count = int(processed_file[material_start])
        marker_start = material_start + 1 + (material_count * 2)
        marker_count = int(processed_file[marker_start])
        instance_xref_path_start = marker_start + 1 + (marker_count * 5)
        instance_xref_path_count = int(processed_file[instance_xref_path_start])
        instance_markers_start = instance_xref_path_start + 1 + (instance_xref_path_count * 2)
        instance_markers_count = int(processed_file[instance_markers_start])
        vertex_start = instance_markers_start + 1 + (instance_markers_count * 5)
        vertex_count = int(processed_file[vertex_start])
        for count in range(vertex_count):
            vertex_group_count = int(processed_file[vertex_index + vertex_start + 3])
            vertex_uv_count = int(processed_file[vertex_index + vertex_start + (vertex_group_count * 2) + 4])
            total_uv_lines = 0
            for x in range(vertex_uv_count):
                total_uv_lines += 1

            vertex_index += 4 + (vertex_group_count * 2) + total_uv_lines

        triangle_start = vertex_start + vertex_index + 1
        triangle_count = int(processed_file[triangle_start])

    else:
        node_start = 2
        node_count = int(processed_file[node_start])
        material_start = 3 + (node_count * 5)
        material_count = int(processed_file[material_start])
        marker_start = material_start + 1 + (material_count * 2)
        marker_count = int(processed_file[marker_start])
        region_start = marker_start + 1 + (marker_count * 6)
        region_count = int(processed_file[region_start])
        vertex_start = region_start + 1 + region_count
        vertex_count = int(processed_file[vertex_start])
        triangle_start = vertex_start + (vertex_count * 8) + 1
        triangle_count = int(processed_file[triangle_start])

    if version >= 8205:
        for node in range(node_count):
            node_name = processed_file[node_line_index + 2]
            parent_index = int(processed_file[node_line_index + 3])
            node_list.append(node_name)
            parent_list.append(parent_index)
            node_line_index += 4

    else:
        for node in range(node_count):
            node_name = processed_file[node_line_index + 3]
            child_node_index = int(processed_file[node_line_index + 4])
            sibling_node_index = int(processed_file[node_line_index + 5])
            node_list.append(node_name)
            child_list.append(child_node_index)
            sibling_list.append(sibling_node_index)
            node_line_index += 5

    armdata = bpy.data.armatures.new('Armature')
    ob_new = bpy.data.objects.new('Armature', armdata)
    bpy.context.collection.objects.link(ob_new)
    armature = ob_new
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode = 'EDIT')
    global_functions.create_skeleton(armature, node_list)
    node_line_index = 0
    if version <= 8204:
        for node in node_list:
            node_index = node_list.index(node)
            children_names = global_functions.find_children(node_list, child_list, sibling_list, node_index)
            for child in children_names:
                armature.data.edit_bones[child].parent = armature.data.edit_bones[node]

    for node in node_list:
        if version >= 8205:
            node_rotation = processed_file[node_line_index + 4].split()
            node_translation = processed_file[node_line_index + 5].split()
            parent_name = parent_list[node_list.index(node)]
            node_set = 4

        else:
            node_rotation = processed_file[node_line_index + 6].split()
            node_translation = processed_file[node_line_index + 7].split()
            parent_name = -1
            node_set = 5

        file_matrix = Quaternion(((float(node_rotation[3])), float(node_rotation[0]), float(node_rotation[1]), float(node_rotation[2]))).inverted().to_matrix().to_4x4()
        if version >= 8205:
            file_matrix = Quaternion(((float(node_rotation[3])), float(node_rotation[0]), float(node_rotation[1]), float(node_rotation[2]))).to_matrix().to_4x4()

        file_matrix[0][3] = float(node_translation[0])
        file_matrix[1][3] = float(node_translation[1])
        file_matrix[2][3] = float(node_translation[2])

        bpy.ops.object.mode_set(mode = 'POSE')
        pose_bone = armature.pose.bones[node]
        if version >= 8205:
            matrix = file_matrix

        else:
            matrix = file_matrix
            if pose_bone.parent:
                matrix = pose_bone.parent.matrix @ file_matrix

        if not parent_name == -1:
            bpy.ops.object.mode_set(mode = 'EDIT')
            armature.data.edit_bones[node].parent = armature.data.edit_bones[node_list[parent_name]]

        bpy.ops.object.mode_set(mode = 'POSE')
        armature.pose.bones[node].matrix = matrix
        node_line_index += node_set

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

    vertex_index = 0
    for vert in range(vertex_count):
        if version >= 8205:
            vert_translation = processed_file[vertex_index + vertex_start + 1]
            vert_normal = processed_file[vertex_index + vertex_start + 2]
            vertex_group_count = processed_file[vertex_index + vertex_start + 3]
            vertex_uv_count = processed_file[vertex_index + vertex_start + (int(vertex_group_count) * 2) + 4]
            vert_translation_list = vert_translation.split()
            vert_normal_list = vert_normal.split()
            verts.append([float(vert_translation_list[0]), float(vert_translation_list[1]), float(vert_translation_list[2])])
            total_uv_lines = 0
            for x in range(int(vertex_uv_count)):
                total_uv_lines += 1

            vertex_index += 4 + (int(vertex_group_count) * 2 + total_uv_lines)

        else:
            vert_translation = processed_file[vertex_index + vertex_start + 2]
            vert_normal = processed_file[vertex_index + vertex_start + 3]
            vert_translation_list = vert_translation.split()
            vert_normal_list = vert_normal.split()
            verts.append([float(vert_translation_list[0]), float(vert_translation_list[1]), float(vert_translation_list[2])])

            vertex_index += 8

    vertex_index = 0
    for tri in range(triangle_count):
        p1 = verts[0 + vertex_index]
        p2 = verts[1 + vertex_index]
        p3 = verts[2 + vertex_index] 
        v1 = bm.verts.new((float(p1[0]), float(p1[1]), float(p1[2])))
        v2 = bm.verts.new((float(p2[0]), float(p2[1]), float(p2[2])))
        v3 = bm.verts.new((float(p3[0]), float(p3[1]), float(p3[2])))
        bm.faces.new((v1, v2, v3))
        vertex_index += 3

    bm.to_mesh(mesh)
    bm.free()

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.import_scene.jms()
