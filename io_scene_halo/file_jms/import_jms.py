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
import random

from mathutils import Vector, Quaternion, Matrix
from io_scene_halo.global_functions import global_functions
from io_scene_halo.global_functions.global_functions import JmsVertex
from io_scene_halo.global_functions.global_functions import JmsTriangle
from io_scene_halo.global_functions.global_functions import JmsMaterial

def get_random_color():
    r, g, b = [random.random() for i in range(3)]
    return r, g, b, 1

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
    collection = bpy.context.collection
    scene = bpy.context.scene
    view_layer = bpy.context.view_layer
    armature = None
    node_list = []
    child_list = []
    sibling_list = []
    parent_list = []
    node_transforms = []
    translation_list = []
    region_list = []
    xref_path_list = []
    xref_file_name_list = []
    region_permutation_list = []
    materials = []
    triangles = []
    vertices = []
    object_list = list(scene.objects)
    node_line_index = 0
    node_index = 0
    vertex_line_index = 0
    vertex_index = 0
    triangle_index = 0
    total_convex_shape_vertex_index = 0
    total_convex_shape_vertex_count = 0
    version = int(processed_file[0])
    game_version = None
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
            capsule_count = int(processed_file[capsule_start])
            convex_shape_start = capsule_start + 1 + (capsule_count * 7)
            convex_shape_count = int(processed_file[convex_shape_start])
            for count in range(convex_shape_count):
                convex_shape_vertex_count = int(processed_file[convex_shape_start + 6 + ((count * 6) + total_convex_shape_vertex_index)])
                total_convex_shape_vertex_index += convex_shape_vertex_count

            ragdoll_start = convex_shape_start + 1 + (convex_shape_count * 6) + total_convex_shape_vertex_index
            ragdoll_count = int(processed_file[ragdoll_start])
            hinge_start = ragdoll_start + 1 + (ragdoll_count * 13)
            hinge_count = int(processed_file[hinge_start])
            if version >= 8206:
                car_wheel_start = hinge_start + 1 + (hinge_count * 11)
                car_wheel_count = int(processed_file[car_wheel_start])
                point_to_point_start = car_wheel_start + 1 + (car_wheel_count * 11)
                point_to_point_count = int(processed_file[point_to_point_start])
                prismatic_start = point_to_point_start + 1 + (point_to_point_count * 15)
                prismatic_count = int(processed_file[prismatic_start])
                bounding_sphere_start = prismatic_start + 1 + (prismatic_count * 9)
                bounding_sphere_count = int(processed_file[bounding_sphere_start])

            else:
                bounding_sphere_start = hinge_start + 1 + (hinge_count * 11)
                bounding_sphere_count = int(processed_file[bounding_sphere_start])

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

    #gather materials
    for material in range(material_count):
        jms_material = JmsMaterial()
        materials.append(jms_material)
        material_name = processed_file[material_start + 1 + + (2 * material)]
        material_definition = processed_file[material_start + 2 + (2 * material)]
        is_drive = os.path.splitdrive(material_definition)
        jms_material.name = material_name
        if material_definition.startswith("<none>") or material_definition.startswith("/") or not is_drive[0] == '':
            game_version = 'haloce'
            jms_material.texture_path = material_definition

        else:
            game_version = 'halo2'
            material_definition_items = material_definition.split()
            jms_material.slot_index = material_definition_items[0]
            jms_material.lod = material_definition_items[1]
            jms_material.permutation = material_definition_items[2]
            jms_material.region = material_definition_items[3]

    #gather triangles
    for triangle in range(triangle_count):
        jms_triangle = JmsTriangle()
        triangles.append(jms_triangle)
        if version >= 8205:
            triangle_material_index = int(processed_file[triangle_start + 1 + (triangle * 2)])
            triangle_verts = processed_file[triangle_start + 2 + (triangle * 2)].split()
            material = materials[triangle_material_index]
            region = material.region
            permutation = material.permutation
            if not [region, permutation] in region_permutation_list:
                region_permutation_list.append([region, permutation])

        else:
            triangle_region_index = int(processed_file[triangle_start + 1 + (triangle * 3)])
            triangle_material_index = int(processed_file[triangle_start + 2 + (triangle * 3)])
            triangle_verts = processed_file[triangle_start + 3 + (triangle * 3)].split()
            jms_triangle.region = triangle_region_index
            if not region_list[triangle_region_index] in region_permutation_list:
                region_permutation_list.append(region)

        jms_triangle.v0 = int(triangle_verts[0])
        jms_triangle.v1 = int(triangle_verts[1])
        jms_triangle.v2 = int(triangle_verts[2])
        jms_triangle.material = triangle_material_index

    #gather vertices
    for vert in range(vertex_count):
        jms_vertex = JmsVertex()
        vertices.append(jms_vertex)
        vertex_group_index = []
        vertex_group_weight = []
        vertex_uv = []
        if version >= 8205:
            vert_translation = processed_file[vertex_index + vertex_start + 1].split()
            vert_normal = processed_file[vertex_index + vertex_start + 2].split()
            vertex_group_count = int(processed_file[vertex_index + vertex_start + 3])
            for group in range(vertex_group_count):
                vertex_group_index.append(int(processed_file[vertex_index + vertex_start + 4 + (group * 2)]))
                vertex_group_weight.append(float(processed_file[vertex_index + vertex_start + 5 + (group * 2)]))

            vertex_uv_count = int(processed_file[vertex_index + vertex_start + (vertex_group_count * 2) + 4])
            for uv in range(vertex_uv_count):
                vertex_uv.append(processed_file[vertex_index + vertex_start + (uv * 2) + 5].split())

            total_uv_lines = 0
            for x in range(int(vertex_uv_count)):
                total_uv_lines += 1

            vertex_index += 4 + (vertex_group_count * 2) + total_uv_lines

        else:
            node_count = 0
            node_0 = int(processed_file[vertex_index + vertex_start + 1])
            vert_translation = processed_file[vertex_index + vertex_start + 2].split()
            vert_normal = processed_file[vertex_index + vertex_start + 3].split()
            node_1 = int(processed_file[vertex_index + vertex_start + 4])
            node_1_weight = float(processed_file[vertex_index + vertex_start + 5])
            node_0_weight = 1 - node_1_weight
            vertex_uv_count = 1
            tex_u = float(processed_file[vertex_index + vertex_start + 6])
            tex_v = float(processed_file[vertex_index + vertex_start + 7])
            vertex_uv.append((tex_u, tex_v))
            if not node_0 == -1:
                node_count += 1
                vertex_group_index.append(node_0)
                vertex_group_weight.append(node_0_weight)

            if not node_1 == -1:
                node_count += 1
                vertex_group_index.append(node_1)
                vertex_group_weight.append(node_1_weight)

            vertex_group_count = node_count
            vertex_index += 8

        jms_vertex.pos = vert_translation
        jms_vertex.norm = vert_normal
        if vertex_uv_count >= 1:
            jms_vertex.uv = vertex_uv[0]

        if vertex_uv_count >= 2:
            jms_vertex.uv_2 = vertex_uv[1]

        jms_vertex.node_influence_count = vertex_group_count
        if vertex_group_count >= 1:
            jms_vertex.node0 = vertex_group_index[0]
            jms_vertex.node0_weight = vertex_group_weight[0]

        if vertex_group_count >= 2:
            jms_vertex.node1 = vertex_group_index[1]
            jms_vertex.node1_weight = vertex_group_weight[1]

        if vertex_group_count >= 3:
            jms_vertex.node2 = vertex_group_index[2]
            jms_vertex.node2_weight = vertex_group_weight[2]

        if vertex_group_count >= 4:
            jms_vertex.node3 = vertex_group_index[3]
            jms_vertex.node3_weight = vertex_group_weight[3]

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

    for obj in object_list:
        if armature is None:
            if obj.type == 'ARMATURE':
                exist_count = 0
                armature_bone_list = []
                armature_bone_list = list(obj.data.bones)
                for node in armature_bone_list:
                    if node.name in node_list:
                        exist_count += 1

                if exist_count == len(node_list):
                    armature = obj
                    view_layer.objects.active = armature

    if armature == None:
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

        if not node_count == 0:
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

        bpy.ops.object.select_all(action='DESELECT')
        if not marker_parent_index == -1:
            parent_name = node_list[marker_parent_index]

        object_name_prefix = '#%s' % marker_name
        mesh = bpy.data.meshes.new(object_name_prefix)
        object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
        collection.objects.link(object_mesh)
        view_layer.objects.active = object_mesh
        object_mesh.select_set(True)
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, diameter=1)
        bm.to_mesh(mesh)
        bm.free()
        armature.select_set(True)
        view_layer.objects.active = armature
        if not marker_parent_index == -1:
            bpy.ops.object.mode_set(mode='EDIT')
            armature.data.edit_bones.active = armature.data.edit_bones[parent_name]
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.parent_set(type='BONE', keep_transform=True)

        else:
            bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)

        file_matrix = Quaternion(((float(marker_rotation[3])), float(marker_rotation[0]), float(marker_rotation[1]), float(marker_rotation[2]))).inverted().to_matrix().to_4x4()
        if version >= 8205:
            file_matrix = Quaternion(((float(marker_rotation[3])), float(marker_rotation[0]), float(marker_rotation[1]), float(marker_rotation[2]))).to_matrix().to_4x4()

        file_matrix[0][3] = float(marker_translation[0])
        file_matrix[1][3] = float(marker_translation[1])
        file_matrix[2][3] = float(marker_translation[2])
        matrix = file_matrix
        if not marker_parent_index == -1:
            bpy.ops.object.mode_set(mode = 'POSE')
            pose_bone = armature.pose.bones[parent_name]
            matrix = pose_bone.matrix @ file_matrix

        object_mesh.matrix_world = matrix
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        object_mesh.select_set(True)
        view_layer.objects.active = object_mesh
        if version <= 8204:
            object_mesh.jms.Region = region_list[marker_region_index]

        object_mesh.jms.Object_Type = 'SPHERE'
        object_dimension = marker_radius * 2
        object_mesh.dimensions = (object_dimension, object_dimension, object_dimension)
        bpy.ops.object.select_all(action='DESELECT')

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

            bpy.ops.object.select_all(action='DESELECT')
            mesh = bpy.data.meshes.new(xref_object_name)
            object_mesh = bpy.data.objects.new(xref_object_name, mesh)
            collection.objects.link(object_mesh)
            view_layer.objects.active = object_mesh
            object_mesh.select_set(True)
            bm = bmesh.new()
            bmesh.ops.create_cube(bm, size=1.0)
            bm.to_mesh(mesh)
            bm.free()
            armature.select_set(True)
            view_layer.objects.active = armature
            bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)
            file_matrix = Quaternion(((float(xref_object_rotation[3])), float(xref_object_rotation[0]), float(xref_object_rotation[1]), float(xref_object_rotation[2]))).inverted().to_matrix().to_4x4()
            if version >= 8205:
                file_matrix = Quaternion(((float(xref_object_rotation[3])), float(xref_object_rotation[0]), float(xref_object_rotation[1]), float(xref_object_rotation[2]))).to_matrix().to_4x4()

            file_matrix[0][3] = float(xref_object_translation[0])
            file_matrix[1][3] = float(xref_object_translation[1])
            file_matrix[2][3] = float(xref_object_translation[2])
            matrix = file_matrix
            object_mesh.matrix_world = matrix
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            object_mesh.select_set(True)
            view_layer.objects.active = object_mesh
            object_mesh.jms.Object_Type = 'BOX'
            if version >= 8205:
                object_mesh.jms.XREF_path = xref_path_list[xref_path_index]

            bpy.ops.object.select_all(action='DESELECT')

    #generate mesh object
    if not vertex_count == 0:
        for region_permutation in region_permutation_list:
            vertex_groups = []
            object_region = object_name
            if game_version == 'haloce':
                object_region = '%s_%s' % (object_name, region_permutation)

            elif game_version == 'halo2':
                object_region = '%s_%s_%s' % (object_name, region_permutation[0], region_permutation[1])

            bpy.ops.object.select_all(action='DESELECT')
            mesh = bpy.data.meshes.new(object_region)
            object_mesh = bpy.data.objects.new(object_region, mesh)
            collection.objects.link(object_mesh)
            view_layer.objects.active = object_mesh
            object_mesh.select_set(True)
            bm = bmesh.new()
            for triangle in range(triangle_count):
                tri = triangles[triangle]
                mat = materials[tri.material]
                if version >= 8201 or game_version == 'halo2':
                    region = mat.region
                    permutation = mat.permutation
                    current_region_permutation = [region, permutation]

                else:
                    region = tri.region
                    current_region_permutation = region

                if region_permutation == current_region_permutation:
                    p1 = vertices[tri.v0].pos
                    p2 = vertices[tri.v1].pos
                    p3 = vertices[tri.v2].pos
                    for index in range(3):
                        if index == 0:
                            vert_index = tri.v0

                        elif index == 1:
                            vert_index = tri.v1

                        elif index == 2:
                            vert_index = tri.v2

                        if not vertices[vert_index].node0 == -1 and not vertices[vert_index].node0 in vertex_groups:
                            vertex_groups.append( vertices[vert_index].node0)

                        if not vertices[vert_index].node1 == -1 and not vertices[vert_index].node1 in vertex_groups:
                            vertex_groups.append( vertices[vert_index].node1)

                        if not vertices[vert_index].node2 == -1 and not vertices[vert_index].node2 in vertex_groups:
                            vertex_groups.append( vertices[vert_index].node2)

                        if not vertices[vert_index].node3 == -1 and not vertices[vert_index].node3 in vertex_groups:
                            vertex_groups.append( vertices[vert_index].node3)

                    v1 = bm.verts.new((float(p1[0]), float(p1[1]), float(p1[2])))
                    v2 = bm.verts.new((float(p2[0]), float(p2[1]), float(p2[2])))
                    v3 = bm.verts.new((float(p3[0]), float(p3[1]), float(p3[2])))
                    bm.faces.new((v1, v2, v3))
                    if not tri.material == -1:
                        material_list = []
                        material_name = mat.name
                        mat = bpy.data.materials.get(material_name)
                        if mat is None:
                            mat = bpy.data.materials.new(name=material_name)

                        for slot in object_mesh.material_slots:
                            material_list.append(slot.material)

                        if not mat in material_list:
                            object_mesh.data.materials.append(mat)

                        mat.diffuse_color = get_random_color()

            bm.to_mesh(mesh)
            bm.free()
            triangle_index = 0
            for triangle in range(triangle_count):
                tri = triangles[triangle]
                mat = materials[tri.material]
                if version >= 8201 or game_version == 'halo2':
                    region = mat.region
                    permutation = mat.permutation
                    current_region_permutation = [region, permutation]

                else:
                    region = tri.region
                    current_region_permutation = region

                if region_permutation == current_region_permutation:
                    if not tri.material == -1:
                        material_list = []
                        material_name = mat.name
                        for slot in object_mesh.material_slots:
                            material_list.append(slot.material)

                        material_index = material_list.index(bpy.data.materials[material_name])
                        object_mesh.data.polygons[triangle_index].material_index = material_index

                    triangle_index += 1

            for group in vertex_groups:
                object_mesh.vertex_groups.new(name = node_list[int(group)])

            if game_version == 'haloce':
                object_mesh.jms.Region = region

            elif game_version == 'halo2':
                object_mesh.jms.Region = region
                object_mesh.jms.Permutation = permutation

            armature.select_set(True)
            view_layer.objects.active = armature
            bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)
            bpy.ops.object.select_all(action='DESELECT')

    if version >= 8206:
        #generate sphere objects
        for sphere in range(sphere_count):
            sphere_object_name = processed_file[sphere_start + 1 + (sphere * 6)]
            sphere_parent_index = int(processed_file[sphere_start + 2 + (sphere * 6)])
            sphere_material_index = int(processed_file[sphere_start + 3 + (sphere * 6)])
            sphere_object_rotation = processed_file[sphere_start + 4 + (sphere * 6)].split()
            sphere_object_translation = processed_file[sphere_start + 5 + (sphere * 6)].split()
            sphere_object_radius = float(processed_file[sphere_start + 6 + (sphere * 6)])

            bpy.ops.object.select_all(action='DESELECT')
            if not sphere_parent_index == -1:
                parent_name = node_list[sphere_parent_index]

            object_name_prefix = '$%s' % sphere_object_name
            mesh = bpy.data.meshes.new(object_name_prefix)
            object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
            collection.objects.link(object_mesh)
            view_layer.objects.active = object_mesh
            object_mesh.select_set(True)
            bm = bmesh.new()
            bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, diameter=1)
            bm.to_mesh(mesh)
            bm.free()
            armature.select_set(True)
            view_layer.objects.active = armature
            if not sphere_parent_index == -1:
                bpy.ops.object.mode_set(mode='EDIT')
                armature.data.edit_bones.active = armature.data.edit_bones[parent_name]
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.parent_set(type='BONE', keep_transform=True)

            else:
                bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)

            file_matrix = Quaternion(((float(sphere_object_rotation[3])), float(sphere_object_rotation[0]), float(sphere_object_rotation[1]), float(sphere_object_rotation[2]))).inverted().to_matrix().to_4x4()
            if version >= 8205:
                file_matrix = Quaternion(((float(sphere_object_rotation[3])), float(sphere_object_rotation[0]), float(sphere_object_rotation[1]), float(sphere_object_rotation[2]))).to_matrix().to_4x4()

            file_matrix[0][3] = float(sphere_object_translation[0])
            file_matrix[1][3] = float(sphere_object_translation[1])
            file_matrix[2][3] = float(sphere_object_translation[2])
            matrix = file_matrix
            if not sphere_parent_index == -1:
                bpy.ops.object.mode_set(mode = 'POSE')
                pose_bone = armature.pose.bones[parent_name]
                matrix = pose_bone.matrix @ file_matrix

            object_mesh.matrix_world = matrix
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            object_mesh.select_set(True)
            view_layer.objects.active = object_mesh
            if not sphere_material_index == -1:
                material_name = material_name_list[sphere_material_index]
                material_definition = material_definition_list[sphere_material_index]
                mat = bpy.data.materials.get(material_name)
                if mat is None:
                    mat = bpy.data.materials.new(name=material_name)

                if object_mesh.data.materials:
                    object_mesh.data.materials[0] = mat

                else:
                    object_mesh.data.materials.append(mat)

                mat.diffuse_color = get_random_color()
                if game_version == 'halo2':
                    material_parts = material_definition.split()
                    object_mesh.jms.Region = material_parts[-1]
                    object_mesh.jms.Permutation = material_parts[-2]

            object_mesh.jms.Object_Type = 'SPHERE'
            object_dimension = sphere_object_radius * 2
            object_mesh.dimensions = (object_dimension, object_dimension, object_dimension)
            bpy.ops.object.select_all(action='DESELECT')

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

            bpy.ops.object.select_all(action='DESELECT')
            if not box_parent_index == -1:
                parent_name = node_list[box_parent_index]

            object_name_prefix = '$%s' % box_object_name
            mesh = bpy.data.meshes.new(object_name_prefix)
            object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
            collection.objects.link(object_mesh)
            view_layer.objects.active = object_mesh
            object_mesh.select_set(True)
            bm = bmesh.new()
            bmesh.ops.create_cube(bm, size=1.0)
            bm.to_mesh(mesh)
            bm.free()
            armature.select_set(True)
            view_layer.objects.active = armature
            if not box_parent_index == -1:
                bpy.ops.object.mode_set(mode='EDIT')
                armature.data.edit_bones.active = armature.data.edit_bones[parent_name]
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.parent_set(type='BONE', keep_transform=True)

            else:
                bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)

            file_matrix = Quaternion(((float(box_object_rotation[3])), float(box_object_rotation[0]), float(box_object_rotation[1]), float(box_object_rotation[2]))).inverted().to_matrix().to_4x4()
            if version >= 8205:
                file_matrix = Quaternion(((float(box_object_rotation[3])), float(box_object_rotation[0]), float(box_object_rotation[1]), float(box_object_rotation[2]))).to_matrix().to_4x4()

            file_matrix[0][3] = float(box_object_translation[0])
            file_matrix[1][3] = float(box_object_translation[1])
            file_matrix[2][3] = float(box_object_translation[2])
            matrix = file_matrix
            if not box_parent_index == -1:
                bpy.ops.object.mode_set(mode = 'POSE')
                pose_bone = armature.pose.bones[parent_name]
                matrix = pose_bone.matrix @ file_matrix

            object_mesh.matrix_world = matrix

            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            object_mesh.select_set(True)
            view_layer.objects.active = object_mesh
            if not box_material_index == -1:
                material_name = material_name_list[box_material_index]
                material_definition = material_definition_list[box_material_index]
                mat = bpy.data.materials.get(material_name)
                if mat is None:
                    mat = bpy.data.materials.new(name=material_name)

                if object_mesh.data.materials:
                    object_mesh.data.materials[0] = mat

                else:
                    object_mesh.data.materials.append(mat)

                mat.diffuse_color = get_random_color()
                if game_version == 'halo2':
                    material_parts = material_definition.split()
                    object_mesh.jms.Region = material_parts[-1]
                    object_mesh.jms.Permutation = material_parts[-2]

            object_mesh.jms.Object_Type = 'BOX'
            object_mesh.dimensions = (box_object_x_scale, box_object_y_scale, box_object_z_scale)
            bpy.ops.object.select_all(action='DESELECT')

        #generate pill objects
        for capsule in range(capsule_count):
            pill_object_name = processed_file[capsule_start + 1 + (capsule * 7)]
            pill_parent_index = int(processed_file[capsule_start + 2 + (capsule * 7)])
            pill_material_index = int(processed_file[capsule_start + 3 + (capsule * 7)])
            pill_object_rotation = processed_file[capsule_start + 4 + (capsule * 7)].split()
            pill_object_translation = processed_file[capsule_start + 5 + (capsule * 7)].split()
            pill_object_height = float(processed_file[capsule_start + 6 + (capsule * 7)])
            pill_object_radius = float(processed_file[capsule_start + 7 + (capsule * 7)])

            bpy.ops.object.select_all(action='DESELECT')
            if not pill_parent_index == -1:
                parent_name = node_list[pill_parent_index]

            object_name_prefix = '$%s' % pill_object_name
            mesh = bpy.data.meshes.new(object_name_prefix)
            object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
            collection.objects.link(object_mesh)
            view_layer.objects.active = object_mesh
            object_mesh.select_set(True)
            bm = bmesh.new()
            bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=12, diameter1=3, diameter2=3, depth=5)
            bm.transform(Matrix.Translation((0, 0, 2.5)))
            bm.to_mesh(mesh)
            bm.free()
            armature.select_set(True)
            view_layer.objects.active = armature
            if not pill_parent_index == -1:
                bpy.ops.object.mode_set(mode='EDIT')
                armature.data.edit_bones.active = armature.data.edit_bones[parent_name]
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.parent_set(type='BONE', keep_transform=True)

            else:
                bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)

            file_matrix = Quaternion(((float(pill_object_rotation[3])), float(pill_object_rotation[0]), float(pill_object_rotation[1]), float(pill_object_rotation[2]))).inverted().to_matrix().to_4x4()
            if version >= 8205:
                file_matrix = Quaternion(((float(pill_object_rotation[3])), float(pill_object_rotation[0]), float(pill_object_rotation[1]), float(pill_object_rotation[2]))).to_matrix().to_4x4()

            file_matrix[0][3] = float(pill_object_translation[0])
            file_matrix[1][3] = float(pill_object_translation[1])
            file_matrix[2][3] = float(pill_object_translation[2])
            matrix = file_matrix
            if not pill_parent_index == -1:
                bpy.ops.object.mode_set(mode = 'POSE')
                pose_bone = armature.pose.bones[parent_name]
                matrix = pose_bone.matrix @ file_matrix

            object_mesh.matrix_world = matrix
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            object_mesh.select_set(True)
            view_layer.objects.active = object_mesh
            if not pill_material_index == -1:
                material_name = material_name_list[pill_material_index]
                material_definition = material_definition_list[pill_material_index]
                mat = bpy.data.materials.get(material_name)
                if mat is None:
                    mat = bpy.data.materials.new(name=material_name)

                if object_mesh.data.materials:
                    object_mesh.data.materials[0] = mat

                else:
                    object_mesh.data.materials.append(mat)

                mat.diffuse_color = get_random_color()
                if game_version == 'halo2':
                    material_parts = material_definition.split()
                    object_mesh.jms.Region = material_parts[-1]
                    object_mesh.jms.Permutation = material_parts[-2]

            object_mesh.jms.Object_Type = 'CAPSULES'
            object_dimension = pill_object_radius * 2
            object_mesh.dimensions = (object_dimension, object_dimension, (object_dimension + pill_object_height))
            bpy.ops.object.select_all(action='DESELECT')

        #generate convex shape objects
        for convex_shape in range(convex_shape_count):
            convex_shape_object_name = processed_file[convex_shape_start + 1 + (convex_shape * 6) + total_convex_shape_vertex_count]
            convex_shape_parent_index = int(processed_file[convex_shape_start + 2 + (convex_shape * 6) + total_convex_shape_vertex_count])
            convex_shape_material_index = int(processed_file[convex_shape_start + 3 + (convex_shape * 6) + total_convex_shape_vertex_count])
            convex_shape_object_rotation = processed_file[convex_shape_start + 4 + (convex_shape * 6) + total_convex_shape_vertex_count].split()
            convex_shape_object_translation = processed_file[convex_shape_start + 5 + (convex_shape * 6) + total_convex_shape_vertex_count].split()
            convex_shape_vertex_count_start = convex_shape_start + 6 + (convex_shape * 6) + total_convex_shape_vertex_count
            convex_shape_vertex_count = int(processed_file[convex_shape_vertex_count_start])
            total_convex_shape_vertex_count += convex_shape_vertex_count
            convex_shape_vertex_index = 0

            bpy.ops.object.select_all(action='DESELECT')
            if not convex_shape_parent_index == -1:
                parent_name = node_list[convex_shape_parent_index]

            object_name_prefix = '$%s' % convex_shape_object_name
            mesh = bpy.data.meshes.new(object_name_prefix)
            object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
            collection.objects.link(object_mesh)
            view_layer.objects.active = object_mesh
            object_mesh.select_set(True)
            bm = bmesh.new()
            for vert in range(convex_shape_vertex_count):
                vert_translation = processed_file[convex_shape_vertex_count_start + 1 + convex_shape_vertex_index]
                vert_translation_list = vert_translation.split()
                bm.verts.new((float(vert_translation_list[0]), float(vert_translation_list[1]), float(vert_translation_list[2])))
                convex_shape_vertex_index += 1

            bm.to_mesh(mesh)
            bm.free()
            armature.select_set(True)
            view_layer.objects.active = armature
            if not convex_shape_parent_index == -1:
                bpy.ops.object.mode_set(mode='EDIT')
                armature.data.edit_bones.active = armature.data.edit_bones[parent_name]
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.parent_set(type='BONE', keep_transform=True)

            else:
                bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)

            file_matrix = Quaternion(((float(convex_shape_object_rotation[3])), float(convex_shape_object_rotation[0]), float(convex_shape_object_rotation[1]), float(convex_shape_object_rotation[2]))).inverted().to_matrix().to_4x4()
            if version >= 8205:
                file_matrix = Quaternion(((float(convex_shape_object_rotation[3])), float(convex_shape_object_rotation[0]), float(convex_shape_object_rotation[1]), float(convex_shape_object_rotation[2]))).to_matrix().to_4x4()

            file_matrix[0][3] = float(convex_shape_object_translation[0])
            file_matrix[1][3] = float(convex_shape_object_translation[1])
            file_matrix[2][3] = float(convex_shape_object_translation[2])
            matrix = file_matrix
            if not convex_shape_parent_index == -1:
                bpy.ops.object.mode_set(mode = 'POSE')
                pose_bone = armature.pose.bones[parent_name]
                matrix = pose_bone.matrix @ file_matrix

            object_mesh.matrix_world = matrix
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            object_mesh.select_set(True)
            view_layer.objects.active = object_mesh
            if not convex_shape_material_index == -1:
                material_name = material_name_list[convex_shape_material_index]
                material_definition = material_definition_list[convex_shape_material_index]
                mat = bpy.data.materials.get(material_name)
                if mat is None:
                    mat = bpy.data.materials.new(name=material_name)

                if object_mesh.data.materials:
                    object_mesh.data.materials[0] = mat

                else:
                    object_mesh.data.materials.append(mat)

                mat.diffuse_color = get_random_color()
                if game_version == 'halo2':
                    material_parts = material_definition.split()
                    object_mesh.jms.Region = material_parts[-1]
                    object_mesh.jms.Permutation = material_parts[-2]

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.convex_hull(delete_unused=True, use_existing_faces=True, join_triangles=True)
            bpy.ops.object.mode_set(mode='OBJECT')
            object_mesh.jms.Object_Type = 'CONVEX SHAPES'
            bpy.ops.object.select_all(action='DESELECT')

        #generate ragdoll objects
        for ragdoll in range(ragdoll_count):
            ragdoll_object_name = processed_file[ragdoll_start + 1 + (ragdoll * 13)]
            ragdoll_attached_index = int(processed_file[ragdoll_start + 2 + (ragdoll * 13)])
            ragdoll_referenced_index = int(processed_file[ragdoll_start + 3 + (ragdoll * 13)])
            ragdoll_attached_object_rotation = processed_file[ragdoll_start + 4 + (ragdoll * 13)].split()
            ragdoll_attached_object_translation = processed_file[ragdoll_start + 5 + (ragdoll * 13)].split()
            ragdoll_referenced_object_rotation = processed_file[ragdoll_start + 6 + (ragdoll * 13)].split()
            ragdoll_referenced_object_translation = processed_file[ragdoll_start + 7 + (ragdoll * 13)].split()
            ragdoll_object_min_twist = float(processed_file[ragdoll_start + 8 + (ragdoll * 13)])
            ragdoll_object_max_twist = float(processed_file[ragdoll_start + 9 + (ragdoll * 13)])
            ragdoll_object_min_cone = float(processed_file[ragdoll_start + 10 + (ragdoll * 13)])
            ragdoll_object_max_cone = float(processed_file[ragdoll_start + 11 + (ragdoll * 13)])
            ragdoll_object_min_plane = float(processed_file[ragdoll_start + 12 + (ragdoll * 13)])
            ragdoll_object_max_plane = float(processed_file[ragdoll_start + 13 + (ragdoll * 13)])

            bpy.ops.object.select_all(action='DESELECT')
            if not ragdoll_attached_index == -1:
                attached_index = node_list[ragdoll_attached_index]

            if not ragdoll_referenced_index == -1:
                referenced_index = node_list[ragdoll_referenced_index]

            object_name_prefix = '$%s' % ragdoll_object_name
            object_empty = bpy.data.objects.new(object_name_prefix, None)
            collection.objects.link(object_empty)
            object_empty.empty_display_size = 2
            object_empty.empty_display_type = 'ARROWS'
            view_layer.objects.active = object_empty
            object_empty.select_set(True)
            armature.select_set(True)
            view_layer.objects.active = armature
            bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)
            file_matrix = Quaternion(((float(ragdoll_attached_object_rotation[3])), float(ragdoll_attached_object_rotation[0]), float(ragdoll_attached_object_rotation[1]), float(ragdoll_attached_object_rotation[2]))).inverted().to_matrix().to_4x4()
            if version >= 8205:
                file_matrix = Quaternion(((float(ragdoll_attached_object_rotation[3])), float(ragdoll_attached_object_rotation[0]), float(ragdoll_attached_object_rotation[1]), float(ragdoll_attached_object_rotation[2]))).to_matrix().to_4x4()

            file_matrix[0][3] = float(ragdoll_attached_object_translation[0])
            file_matrix[1][3] = float(ragdoll_attached_object_translation[1])
            file_matrix[2][3] = float(ragdoll_attached_object_translation[2])
            matrix = file_matrix
            if not ragdoll_attached_index == -1:
                bpy.ops.object.mode_set(mode = 'POSE')
                pose_bone = armature.pose.bones[attached_index]
                matrix = pose_bone.matrix @ file_matrix

            object_empty.matrix_world = matrix
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')

        #generate hinge objects
        for hinge in range(hinge_count):
            hinge_object_name = processed_file[hinge_start + 1 + (hinge * 11)]
            hinge_attached_index = int(processed_file[hinge_start + 2 + (hinge * 11)])
            hinge_referenced_index = int(processed_file[hinge_start + 3 + (hinge * 11)])
            hinge_attached_object_rotation = processed_file[hinge_start + 4 + (hinge * 11)].split()
            hinge_attached_object_translation = processed_file[hinge_start + 5 + (hinge * 11)].split()
            hinge_referenced_object_rotation = processed_file[hinge_start + 6 + (hinge * 11)].split()
            hinge_referenced_object_translation = processed_file[hinge_start + 7 + (hinge * 11)].split()
            hinge_object_is_limited = int(processed_file[hinge_start + 8 + (hinge * 11)])
            hinge_object_friction_limit = float(processed_file[hinge_start + 9 + (hinge * 11)])
            hinge_object_min_angle = float(processed_file[hinge_start + 10 + (hinge * 11)])
            hinge_object_max_angle = float(processed_file[hinge_start + 11 + (hinge * 11)])

            bpy.ops.object.select_all(action='DESELECT')
            if not hinge_attached_index == -1:
                attached_index = node_list[hinge_attached_index]

            if not hinge_referenced_index == -1:
                referenced_index = node_list[hinge_referenced_index]

            object_name_prefix = '$%s' % hinge_object_name
            object_empty = bpy.data.objects.new(object_name_prefix, None)
            collection.objects.link(object_empty)
            object_empty.empty_display_size = 2
            object_empty.empty_display_type = 'ARROWS'
            view_layer.objects.active = object_empty
            object_empty.select_set(True)
            armature.select_set(True)
            view_layer.objects.active = armature
            bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)
            file_matrix = Quaternion(((float(hinge_attached_object_rotation[3])), float(hinge_attached_object_rotation[0]), float(hinge_attached_object_rotation[1]), float(hinge_attached_object_rotation[2]))).inverted().to_matrix().to_4x4()
            if version >= 8205:
                file_matrix = Quaternion(((float(hinge_attached_object_rotation[3])), float(hinge_attached_object_rotation[0]), float(hinge_attached_object_rotation[1]), float(hinge_attached_object_rotation[2]))).to_matrix().to_4x4()

            file_matrix[0][3] = float(hinge_attached_object_translation[0])
            file_matrix[1][3] = float(hinge_attached_object_translation[1])
            file_matrix[2][3] = float(hinge_attached_object_translation[2])
            matrix = file_matrix
            if not hinge_attached_index == -1:
                bpy.ops.object.mode_set(mode = 'POSE')
                pose_bone = armature.pose.bones[attached_index]
                matrix = pose_bone.matrix @ file_matrix

            object_empty.matrix_world = matrix
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.import_scene.jms()
