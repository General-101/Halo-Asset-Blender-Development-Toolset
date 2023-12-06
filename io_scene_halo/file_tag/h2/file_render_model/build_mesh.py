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
import bmesh

from ....global_functions import global_functions, mesh_processing
from .format import PartFlags

def build_mesh_layout(context, import_file, geometry, current_region_permutation, armature):
    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors

    vertex_groups = []
    active_region_permutations = []
    vertex_normals = []

    materials_count = len(import_file.materials)
    full_mesh = bpy.data.meshes.new(current_region_permutation)
    object_mesh = bpy.data.objects.new(current_region_permutation, full_mesh)
    bm = bmesh.new()
    vertex_weights_sets = []
    for section_idx, section_data in enumerate(geometry.section_data):
        mesh = bpy.data.meshes.new("%s_%s" % ("part", str(section_idx)))

        triangles = []
        triangle_mat_indices = []
        vertices = [raw_vertex.position for raw_vertex in section_data.raw_vertices]
        for raw_vertex in section_data.raw_vertices:
            vertex_normals.append(raw_vertex.normal)

        for part_idx, part in enumerate(section_data.parts):
            triangle_part = []

            strip_length = part.strip_length
            strip_start = part.strip_start_index

            triangle_indices = section_data.strip_indices[strip_start : (strip_start + strip_length)]
            if PartFlags.override_triangle_list in PartFlags(part.flags):
                triangle_length = int(len(triangle_indices) / 3)
                for idx in range(triangle_length):
                    triangle_index = (idx * 3)
                    v0 = section_data.strip_indices[triangle_index]
                    v1 = section_data.strip_indices[triangle_index + 1]
                    v2 = section_data.strip_indices[triangle_index + 2]
                    triangle_part.append((v0, v1, v2))

                for tri in triangle_part:
                    triangle_mat_indices.append(part.material_index)
                    triangles.append(tri)

            else:
                index_count = len(triangle_indices)
                for idx in range(index_count - 2):
                    triangle_part.append([triangle_indices[idx], triangle_indices[idx + 1], triangle_indices[idx + 2]])

                # Fix face normals on uneven triangle indices
                for triangle_idx in range(len(triangle_part)):
                    if not triangle_idx % 2 == 0:
                        triangle_part[triangle_idx].reverse()

                # clean up any triangles that reference the same vertex multiple times
                for reversed_triangle in reversed(triangle_part):
                    if (reversed_triangle[0] == reversed_triangle[1]) or (reversed_triangle[1] == reversed_triangle[2]) or (reversed_triangle[0] == reversed_triangle[2]):
                        del triangle_part[triangle_part.index(reversed_triangle)]

                for tri in triangle_part:
                    triangle_mat_indices.append(part.material_index)
                    triangles.append(tri)

        mesh.from_pydata(vertices, [], triangles)
        for tri_idx, poly in enumerate(mesh.polygons):
            poly.use_smooth = True

        region_attribute = mesh.get_custom_attribute()
        for vertex_idx, vertex in enumerate(section_data.raw_vertices):
            node_sets = []
            node_0_index = vertex.node_index_0_new
            node_1_index = vertex.node_index_1_new
            node_2_index = vertex.node_index_2_new
            node_3_index = vertex.node_index_3_new
            node_0_weight = vertex.node_weight_0
            node_1_weight = vertex.node_weight_1
            node_2_weight = vertex.node_weight_2
            node_3_weight = vertex.node_weight_3
            if not node_0_index == -1:
                group_name = import_file.nodes[node_0_index].name
                if not node_0_index in vertex_groups:
                    vertex_groups.append(node_0_index)
                    object_mesh.vertex_groups.new(name = import_file.nodes[node_0_index].name)

                group_index = object_mesh.vertex_groups.keys().index(group_name)
                node_sets.append((group_index, vertex_idx, node_0_weight))

            if not node_1_index == -1:
                group_name = import_file.nodes[node_1_index].name
                if not node_1_index in vertex_groups:
                    vertex_groups.append(node_1_index)
                    object_mesh.vertex_groups.new(name = group_name)

                group_index = object_mesh.vertex_groups.keys().index(group_name)
                node_sets.append((group_index, vertex_idx, node_1_weight))

            if not node_2_index == -1:
                group_name = import_file.nodes[node_2_index].name
                if not node_2_index in vertex_groups:
                    vertex_groups.append(node_2_index)
                    object_mesh.vertex_groups.new(name = import_file.nodes[node_2_index].name)

                group_index = object_mesh.vertex_groups.keys().index(group_name)
                node_sets.append((group_index, vertex_idx, node_2_weight))

            if not node_3_index == -1:
                group_name = import_file.nodes[node_3_index].name
                if not node_3_index in vertex_groups:
                    vertex_groups.append(node_3_index)
                    object_mesh.vertex_groups.new(name = group_name)

                group_index = object_mesh.vertex_groups.keys().index(group_name)
                node_sets.append((group_index, vertex_idx, node_3_weight))

            vertex_weights_sets.append(node_sets)

        for triangle_idx, triangle in enumerate(triangles):
            triangle_material_index = triangle_mat_indices[triangle_idx]
            if not triangle_material_index == -1 and triangle_material_index < materials_count:
                mat = import_file.materials[triangle_material_index]

            if not current_region_permutation in active_region_permutations:
                active_region_permutations.append(current_region_permutation)
                object_mesh.region_add(current_region_permutation)

            if not triangle_material_index == -1:
                material_list = []
                if triangle_material_index < materials_count:
                    material_name = "%s" % (os.path.basename(mat.shader.name))

                else:
                    material_name = "invalid_material_%s" % triangle_material_index

                mat = bpy.data.materials.get(material_name)
                if mat is None:
                    mat = bpy.data.materials.new(name=material_name)

                for slot in object_mesh.material_slots:
                    material_list.append(slot.material)

                if not mat in material_list:
                    material_list.append(mat)
                    object_mesh.data.materials.append(mat)

                mat.diffuse_color = random_color_gen.next()
                material_index = material_list.index(mat)
                mesh.polygons[triangle_idx].material_index = material_index

            region_index = active_region_permutations.index(current_region_permutation)
            region_attribute.data[triangle_idx].value = region_index + 1

            vertex_list = [section_data.raw_vertices[triangle[0]], section_data.raw_vertices[triangle[1]], section_data.raw_vertices[triangle[2]]]
            for vertex_idx, vertex in enumerate(vertex_list):
                loop_index = (3 * triangle_idx) + vertex_idx
                uv_name = 'UVMap_%s' % 0
                layer_uv = mesh.uv_layers.get(uv_name)
                if layer_uv is None:
                    layer_uv = mesh.uv_layers.new(name=uv_name)

                layer_uv.data[loop_index].uv = (vertex.texcoord[0], 1 - vertex.texcoord[1])

        bm.from_mesh(mesh)
        bpy.data.meshes.remove(mesh)

    bm.to_mesh(full_mesh)
    bm.free()

    bpy.context.collection.objects.link(object_mesh)

    for vertex_weights_set_idx, vertex_weights_set in enumerate(vertex_weights_sets):
        for node_set in vertex_weights_set:
            group_index = node_set[0]
            vertex_index = node_set[1]
            node_weight = node_set[2]
            object_mesh.vertex_groups[group_index].add([vertex_weights_set_idx], node_weight, 'ADD')

    object_mesh.parent = armature
    mesh_processing.add_modifier(context, object_mesh, False, None, armature)

def build_object(context, collection, geometry, armature, LOD, region_name, permutation_name, import_file):
    if region_name == "__unnamed":
        region_name = "unnamed"

    if permutation_name == "__base":
        permutation_name = "base"

    object_name = '%s %s %s' % (LOD, permutation_name, region_name)

    build_mesh_layout(context, import_file, geometry, object_name, armature)

def get_geometry_layout(context, collection, import_file, armature):
    for region in import_file.regions:
        for permutation in region.permutations:
            l1_geometry_index = permutation.l1_section_index
            l2_geometry_index = permutation.l2_section_index
            l3_geometry_index = permutation.l3_section_index
            l4_geometry_index = permutation.l4_section_index
            l5_geometry_index = permutation.l5_section_index
            l6_geometry_index = permutation.l6_section_index

            geometry_count = len(import_file.sections)
            if not l6_geometry_index == -1 and l6_geometry_index < geometry_count and not import_file.sections[l6_geometry_index].visited:
                import_file.sections[l6_geometry_index].visited = True
                l6_geometry = import_file.sections[l6_geometry_index]
                build_object(context, collection, l6_geometry, armature, 'L6', region.name, permutation.name, import_file)

            if not l5_geometry_index == -1 and l5_geometry_index < geometry_count and not import_file.sections[l5_geometry_index].visited:
                import_file.sections[l5_geometry_index].visited = True
                l5_geometry = import_file.sections[l5_geometry_index]
                build_object(context, collection, l5_geometry, armature, 'L5', region.name, permutation.name, import_file)

            if not l4_geometry_index == -1 and l4_geometry_index < geometry_count and not import_file.sections[l4_geometry_index].visited:
                import_file.sections[l4_geometry_index].visited = True
                l4_geometry = import_file.sections[l4_geometry_index]
                build_object(context, collection, l4_geometry, armature, 'L4', region.name, permutation.name, import_file)

            if not l3_geometry_index == -1 and l3_geometry_index < geometry_count and not import_file.sections[l3_geometry_index].visited:
                import_file.sections[l3_geometry_index].visited = True
                l3_geometry = import_file.sections[l3_geometry_index]
                build_object(context, collection, l3_geometry, armature, 'L3', region.name, permutation.name, import_file)

            if not l2_geometry_index == -1 and l2_geometry_index < geometry_count and not import_file.sections[l2_geometry_index].visited:
                import_file.sections[l2_geometry_index].visited = True
                l2_geometry = import_file.sections[l2_geometry_index]
                build_object(context, collection, l2_geometry, armature, 'L2', region.name, permutation.name, import_file)

            if not l1_geometry_index == -1 and l1_geometry_index < geometry_count and not import_file.sections[l1_geometry_index].visited:
                import_file.sections[l1_geometry_index].visited = True
                l1_geometry = import_file.sections[l1_geometry_index]
                build_object(context, collection, l1_geometry, armature, 'L1', region.name, permutation.name, import_file)
