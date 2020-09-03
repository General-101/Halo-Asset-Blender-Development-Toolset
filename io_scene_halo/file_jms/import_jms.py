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

def generate_object(node_list, object_parent_index, object_type, object_name, object_radius, create_type, version, armature, object_rotation, object_translation, object_region, region_list, xref_path_list, xref_path_index, vertex_start, vertex_count, triangle_count, processed_file, box_object_x_scale, box_object_y_scale, box_object_z_scale):
    verts = []
    vertex_index = 0
    triangle_index = 0
    collection = bpy.context.collection
    view_layer = bpy.context.view_layer
    bpy.ops.object.select_all(action='DESELECT')
    if not object_parent_index == -1 and not object_parent_index == None:
        parent_name = node_list[object_parent_index]

    object_name_prefix = object_name
    if object_type == 'marker':
        object_name_prefix = '#%s' % object_name

    elif object_type == 'collision':
        object_name_prefix = '@%s' % object_name

    elif object_type == 'physics':
        object_name_prefix = '$%s' % object_name

    mesh = bpy.data.meshes.new(object_name_prefix)
    object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
    collection.objects.link(object_mesh)
    view_layer.objects.active = object_mesh
    object_mesh.select_set(True)
    bm = bmesh.new()

    if create_type == 'sphere':
        object_deminsion = object_radius * 2
        object_mesh.jms.Object_Type = 'SPHERE'
        bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, diameter=1)

    elif create_type == 'cube':
        bmesh.ops.create_cube(bm, size=1.0)

    elif create_type == 'mesh':
        for vert in range(vertex_count):
            if version >= 8205:
                vert_translation = processed_file[vertex_index + vertex_start + 1]
                vert_normal = processed_file[vertex_index + vertex_start + 2]
                vertex_group_count = int(processed_file[vertex_index + vertex_start + 3])
                vertex_uv_count = processed_file[vertex_index + vertex_start + (vertex_group_count * 2) + 4]
                vert_translation_list = vert_translation.split()
                vert_normal_list = vert_normal.split()
                verts.append([float(vert_translation_list[0]), float(vert_translation_list[1]), float(vert_translation_list[2])])
                total_uv_lines = 0
                for x in range(int(vertex_uv_count)):
                    total_uv_lines += 1

                vertex_index += 4 + (vertex_group_count * 2) + total_uv_lines

            else:
                vert_translation = processed_file[vertex_index + vertex_start + 2]
                vert_normal = processed_file[vertex_index + vertex_start + 3]
                vert_translation_list = vert_translation.split()
                vert_normal_list = vert_normal.split()
                verts.append([float(vert_translation_list[0]), float(vert_translation_list[1]), float(vert_translation_list[2])])
                vertex_index += 8

        for tri in range(triangle_count):
            p1 = verts[0 + triangle_index]
            p2 = verts[1 + triangle_index]
            p3 = verts[2 + triangle_index]
            v1 = bm.verts.new((float(p1[0]), float(p1[1]), float(p1[2])))
            v2 = bm.verts.new((float(p2[0]), float(p2[1]), float(p2[2])))
            v3 = bm.verts.new((float(p3[0]), float(p3[1]), float(p3[2])))
            bm.faces.new((v1, v2, v3))
            triangle_index += 3

    bm.to_mesh(mesh)
    bm.free()
    if object_type == 'marker':
        if version <= 8204:
            object_mesh.jms.Region = region_list[object_region]

    elif object_type == 'xref':
        if version >= 8205:
            object_mesh.jms.XREF_path = xref_path_list[xref_path_index]

    armature.select_set(True)
    view_layer.objects.active = armature
    if not object_parent_index == -1 and not object_parent_index == None:
        bpy.ops.object.mode_set(mode='EDIT')
        armature.data.edit_bones.active = armature.data.edit_bones[parent_name]
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.parent_set(type='BONE', keep_transform=True)

    else:
        bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)

    if not object_type == 'mesh':
        file_matrix = Quaternion(((float(object_rotation[3])), float(object_rotation[0]), float(object_rotation[1]), float(object_rotation[2]))).inverted().to_matrix().to_4x4()
        if version >= 8205:
            file_matrix = Quaternion(((float(object_rotation[3])), float(object_rotation[0]), float(object_rotation[1]), float(object_rotation[2]))).to_matrix().to_4x4()

        file_matrix[0][3] = float(object_translation[0])
        file_matrix[1][3] = float(object_translation[1])
        file_matrix[2][3] = float(object_translation[2])
        matrix = file_matrix
        if not object_parent_index == -1 and not object_parent_index == None:
            bpy.ops.object.mode_set(mode = 'POSE')
            pose_bone = armature.pose.bones[parent_name]
            matrix = pose_bone.matrix @ file_matrix

        object_mesh.matrix_world = matrix

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    object_mesh.select_set(True)
    view_layer.objects.active = object_mesh
    if create_type == 'sphere':
        object_mesh.dimensions = (object_deminsion, object_deminsion, object_deminsion)

    elif create_type == 'cube' and not box_object_x_scale is None:
        object_mesh.jms.Object_Type = 'BOX'
        object_mesh.dimensions = (box_object_x_scale, box_object_y_scale, box_object_z_scale)


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

    #foutput.close()
    armature = []
    node_list = []
    child_list = []
    sibling_list = []
    parent_list = []
    node_transforms = []
    translation_list = []
    region_list = []
    xref_path_list = []
    xref_file_name_list = []
    node_line_index = 0
    node_index = 0
    vertex_line_index = 0
    version = int(processed_file[0])
    collection = bpy.context.collection
    view_layer = bpy.context.view_layer
    object_name = bpy.path.basename(filepath).rsplit('.', 1)[0]
    version_list = [8197, 8198, 8199, 8200, 8201, 8202, 8203, 8204, 8205, 8206, 8207, 8208, 8209, 8210]
    if not version in version_list:
        report({'ERROR'}, 'Importer does not support this %s version' % global_functions.get_true_extension(filepath, None, True))
        return {'CANCELLED'}

    #gather the position of all item counts in the file
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
            vertex_group_count = int(processed_file[vertex_line_index + vertex_start + 3])
            vertex_uv_count = int(processed_file[vertex_line_index + vertex_start + (vertex_group_count * 2) + 4])
            total_uv_lines = 0
            for x in range(vertex_uv_count):
                total_uv_lines += 1

            vertex_line_index += 4 + (vertex_group_count * 2) + total_uv_lines

        triangle_start = vertex_start + vertex_line_index + 1
        triangle_count = int(processed_file[triangle_start])
        if version >= 8206:
            sphere_start = triangle_start + 1 + (triangle_count * 2)
            sphere_count = int(processed_file[sphere_start])
            box_start = sphere_start + 1 + (sphere_count * 6)
            box_count = int(processed_file[box_start])
            capsule_start = box_start + 1 + (box_count * 8)
            print(capsule_start)
            capsule_count = int(processed_file[capsule_start])
            convex_shape_start = vertex_start + vertex_line_index + 1
            print(convex_shape_start)
            convex_shape_count = int(processed_file[triangle_start])
            ragdoll_start = vertex_start + vertex_line_index + 1
            ragdoll_count = int(processed_file[triangle_start])
            hinge_start = vertex_start + vertex_line_index + 1
            hinge_count = int(processed_file[triangle_start])
            car_wheel_start = vertex_start + vertex_line_index + 1
            car_wheel_count = int(processed_file[triangle_start])
            point_to_point_start = vertex_start + vertex_line_index + 1
            point_to_point_count = int(processed_file[triangle_start])
            prismatic_start = vertex_start + vertex_line_index + 1
            prismatic_count = int(processed_file[triangle_start])
            bounding_sphere_start = vertex_start + vertex_line_index + 1
            bounding_sphere_count = int(processed_file[triangle_start])

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

    #gather node details
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

    #generate armature from node list
    bpy.ops.object.select_all(action='DESELECT')
    armdata = bpy.data.armatures.new('Armature')
    ob_new = bpy.data.objects.new('Armature', armdata)
    collection.objects.link(ob_new)
    armature = ob_new
    view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode = 'EDIT')
    global_functions.create_skeleton(armature, node_list)
    if version <= 8204:
        for node in node_list:
            node_list_index = node_list.index(node)
            children_names = global_functions.find_children(node_list, child_list, sibling_list, node_list_index)
            for child in children_names:
                armature.data.edit_bones[child].parent = armature.data.edit_bones[node]

    for node in node_list:
        if version >= 8205:
            node_rotation = processed_file[node_index + 4].split()
            node_translation = processed_file[node_index + 5].split()
            parent_name = parent_list[node_list.index(node)]
            node_set = 4

        else:
            node_rotation = processed_file[node_index + 6].split()
            node_translation = processed_file[node_index + 7].split()
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
        node_index += node_set

    bpy.ops.pose.armature_apply(selected=False)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    #gather regions
    if version <= 8204:
        for region in range(region_count):
            region_list.append(processed_file[region_start + 1 + region])

    #generate marker objects
    for marker in range(marker_count):
        if version >= 8205:
            marker_name = processed_file[marker_start + 1 + (5 * marker)]
            marker_parent_index = int(processed_file[marker_start + 2 + (5 * marker)])
            marker_region_index = None
            marker_rotation = processed_file[marker_start + 3 + (5 * marker)].split()
            marker_translation = processed_file[marker_start + 4 + (5 * marker)].split()
            marker_radius = float(processed_file[marker_start + 5 + (5 * marker)])

        else:
            marker_name = processed_file[marker_start + 1 + (6 * marker)]
            marker_parent_index = int(processed_file[marker_start + 2 + (6 * marker)])
            marker_region_index = int(processed_file[marker_start + 3 + (6 * marker)])
            marker_rotation = processed_file[marker_start + 4 + (6 * marker)].split()
            marker_translation = processed_file[marker_start + 5 + (6 * marker)].split()
            marker_radius = float(processed_file[marker_start + 6 + (6 * marker)])

        generate_object(node_list, marker_parent_index, 'marker', marker_name, marker_radius, 'sphere', version, armature, marker_rotation, marker_translation, marker_region_index, region_list, None, None, None, None, None, None, None, None, None)

    if version >= 8205:
        #gather xref paths
        for xref_path in range(instance_xref_path_count):
            xref_path_list.append(processed_file[instance_xref_path_start + 1 + (xref_path * 2)])
            xref_file_name_list.append(processed_file[instance_xref_path_start + 2 + (xref_path * 2)])

        #generate xref objects
        for xref_marker in range(instance_markers_count):
            xref_object_name = processed_file[instance_markers_start + 1 + (xref_marker * 5)]
            xref_path_index = int(processed_file[instance_markers_start + 3 + (xref_marker * 5)])
            xref_object_rotation = processed_file[instance_markers_start + 4 + (xref_marker * 5)].split()
            xref_object_translation = processed_file[instance_markers_start + 5 + (xref_marker * 5)].split()

            generate_object(node_list, None, 'xref', xref_object_name, None, 'cube', version, armature, xref_object_rotation, xref_object_translation, None, None, xref_path_list, xref_path_index, None, None, None, None, None, None, None)

    #generate mesh object
    generate_object(node_list, None, 'mesh', object_name, None, 'mesh', version, armature, None, None, None, None, None, None, vertex_start, vertex_count, triangle_count, processed_file, None, None, None)

    if version >= 8206:
        #generate sphere objects
        for sphere in range(sphere_count):
            sphere_object_name = processed_file[sphere_start + 1 + (sphere * 6)]
            sphere_parent_index = int(processed_file[sphere_start + 2 + (sphere * 6)])
            sphere_material_index = int(processed_file[sphere_start + 3 + (sphere * 6)])
            sphere_object_rotation = processed_file[sphere_start + 4 + (sphere * 6)].split()
            sphere_object_translation = processed_file[sphere_start + 5 + (sphere * 6)].split()
            sphere_object_radius = float(processed_file[sphere_start + 6 + (sphere * 6)])

            generate_object(node_list, sphere_parent_index, 'physics', sphere_object_name, sphere_object_radius, 'sphere', version, armature, sphere_object_rotation, sphere_object_translation, None, None, None, None, None, None, None, None, None, None, None)

        #generate box objects
        for box in range(box_count):
            box_object_name = processed_file[box_start + 1 + (box * 8)]
            box_parent_index = int(processed_file[box_start + 2 + (box * 8)])
            box_material_index = int(processed_file[box_start + 3 + (box * 8)])
            box_object_rotation = processed_file[box_start + 4 + (box * 8)].split()
            box_object_translation = processed_file[box_start + 5 + (box * 8)].split()
            box_object_x_scale = float(processed_file[box_start + 6 + (box * 8)])
            box_object_y_scale = float(processed_file[box_start + 7 + (box * 8)])
            box_object_z_scale = float(processed_file[box_start + 8 + (box * 8)])

            generate_object(node_list, box_parent_index, 'physics', box_object_name, None, 'cube', version, armature, box_object_rotation, box_object_translation, None, None, None, None, None, None, None, None, box_object_x_scale, box_object_y_scale, box_object_z_scale)

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.import_scene.jms()
