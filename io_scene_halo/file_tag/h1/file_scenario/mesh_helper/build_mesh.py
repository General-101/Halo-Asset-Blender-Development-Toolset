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

from mathutils import Vector
from ....h1.file_model.format import ModelFlags
from .....global_functions import shader_processing

def decompress_normal32(n):
    i = (n&1023) / 1023
    j = ((n>>11)&1023) / 1023
    k = ((n>>22)&511) / 511
    if n&(1<<10): i -= 1.0
    if n&(1<<21): j -= 1.0
    if n&(1<<31): k -= 1.0

    return Vector((i, j, k))

def uncompress_vertices(compressed_vertices):
    for vertex in compressed_vertices:
        vertex.normal = decompress_normal32(vertex.normal)
        vertex.binormal = decompress_normal32(vertex.binormal)
        vertex.tangent = decompress_normal32(vertex.tangent)
        vertex.UV = ((vertex.UV[0] / 32767), (vertex.UV[1] /32767))
        vertex.node_0_index = int(vertex.node_0_index / 3)
        vertex.node_1_index = int(vertex.node_1_index / 3)
        vertex.node_0_weight = vertex.node_0_weight / 32767
        vertex.node_1_weight = 1 - vertex.node_0_weight

def build_mesh_layout(asset, geometry, region_name, random_color_gen, object_mesh, materials):
    is_triangle_list = False
    vertex_groups = []
    active_region_permutations = []
    shader_count = len(asset.shaders)

    uses_local_nodes = False
    if asset.header.tag_group == "mod2":
        uses_local_nodes = ModelFlags.parts_have_local_nodes in ModelFlags(asset.flags)

    bm = bmesh.new()
    bm.from_mesh(object_mesh.data)
    node_set_0 = []
    node_set_1 = []
    vert_count = 0
    for part_idx, part in enumerate(geometry.parts):
        mesh = bpy.data.meshes.new("part_%s" % str(part_idx))

        vertex_data = part.uncompressed_vertices
        if len(vertex_data) == 0:
            uncompress_vertices(part.compressed_vertices)
            vertex_data = part.compressed_vertices

        triangle_indices = []
        triangles = []
        vertices = [vertex.translation for vertex in vertex_data]
        normals = [vertex.normal for vertex in vertex_data]

        if is_triangle_list:
            for triangle in part.triangles:
                triangles.append([triangle.v2, triangle.v1, triangle.v0]) # Reversed order to fix facing normals

        else:
            for triangle in part.triangles:
                if not triangle.v0 == -1:
                    triangle_indices.append(triangle.v0)
                if not triangle.v1 == -1:
                    triangle_indices.append(triangle.v1)
                if not triangle.v2 == -1:
                    triangle_indices.append(triangle.v2)

            index_count = len(triangle_indices)
            for idx in range(index_count - 2):
                triangles.append([triangle_indices[idx], triangle_indices[idx + 1], triangle_indices[idx + 2]])

            # Fix face normals on even triangle indices
            for even_triangle_idx in range(0, len(triangles), 2):
                triangles[even_triangle_idx].reverse()

            # clean up any triangles that reference the same vertex multiple times
            for reversed_triangle in reversed(triangles):
                if (reversed_triangle[0] == reversed_triangle[1]) or (reversed_triangle[1] == reversed_triangle[2]) or (reversed_triangle[0] == reversed_triangle[2]):
                    del triangles[triangles.index(reversed_triangle)]

        mesh.from_pydata(vertices, [], triangles)
        for poly in mesh.polygons:
            poly.use_smooth = True

        region_attribute = mesh.get_custom_attribute()
        mesh.normals_split_custom_set_from_vertices(normals)
        for vertex_idx, vertex in enumerate(vertex_data):
            node_0_index = vertex.node_0_index
            node_1_index = vertex.node_1_index
            node_0_weight = vertex.node_0_weight
            node_1_weight = vertex.node_1_weight
            if uses_local_nodes:
                if not node_0_index == -1:
                    node_0_index = part.local_nodes[node_0_index]

                if not node_1_index == -1:
                    node_1_index = part.local_nodes[node_1_index]

            if not node_0_index == -1:
                group_name = asset.nodes[node_0_index].name
                if not node_0_index in vertex_groups:
                    vertex_groups.append(node_0_index)
                    object_mesh.vertex_groups.new(name = asset.nodes[node_0_index].name)

                group_index = object_mesh.vertex_groups.keys().index(group_name)
                node_set_0.append((group_index, vert_count + vertex_idx, node_0_weight))

            if not node_1_index == -1:
                group_name = asset.nodes[node_1_index].name
                if not node_1_index in vertex_groups:
                    vertex_groups.append(node_1_index)
                    object_mesh.vertex_groups.new(name = group_name)

                group_index = object_mesh.vertex_groups.keys().index(group_name)
                node_set_1.append((group_index, vert_count + vertex_idx, node_1_weight))

        for triangle_idx, triangle in enumerate(triangles):
            triangle_material_index = part.shader_index
            if not triangle_material_index == -1 and triangle_material_index < shader_count:
                mat = asset.shaders[triangle_material_index]

            current_region_permutation = region_name
            if not current_region_permutation in active_region_permutations:
                active_region_permutations.append(current_region_permutation)
                object_mesh.region_add(current_region_permutation)

            if not triangle_material_index == -1:
                if triangle_material_index < shader_count:
                    mat = materials[triangle_material_index]

                    if not mat in object_mesh.data.materials.values():
                        object_mesh.data.materials.append(mat)

                    mat.diffuse_color = random_color_gen.next()
                    material_index = object_mesh.data.materials.values().index(mat)
                    mesh.polygons[triangle_idx].material_index = material_index
                else:
                    material_name = "invalid_material_%s" % triangle_material_index
                    mat = bpy.data.materials.get(material_name)
                    if mat is None:
                        mat = bpy.data.materials.new(name=material_name)

                    if not mat in object_mesh.data.materials.values():
                        object_mesh.data.materials.append(mat)

                    mat.diffuse_color = random_color_gen.next()
                    material_index = object_mesh.data.materials.values().index(mat)
                    mesh.polygons[triangle_idx].material_index = material_index

            region_index = active_region_permutations.index(current_region_permutation)
            region_attribute.data[triangle_idx].value = region_index + 1

            vertex_list = [vertex_data[triangle[0]], vertex_data[triangle[1]], vertex_data[triangle[2]]]
            for vertex_idx, vertex in enumerate(vertex_list):
                loop_index = (3 * triangle_idx) + vertex_idx
                uv_name = "UVMap_Render"
                layer_uv = mesh.uv_layers.get(uv_name)
                if layer_uv is None:
                    layer_uv = mesh.uv_layers.new(name=uv_name)

                U = vertex.UV[0]
                V = vertex.UV[1]
                if not asset.base_map_u_scale == 0.0:
                    U = asset.base_map_u_scale * U

                if not asset.base_map_v_scale == 0.0:
                    V =  asset.base_map_v_scale * V

                layer_uv.data[loop_index].uv = (U, 1 - V)

        vert_count += len(vertex_data)

        bm.from_mesh(mesh)
        bpy.data.meshes.remove(mesh)

    bm.to_mesh(object_mesh.data)
    bm.free()

    for idx in node_set_0:
        object_mesh.vertex_groups[idx[0]].add([idx[1]], idx[2], 'ADD')

    for idx in node_set_1:
        object_mesh.vertex_groups[idx[0]].add([idx[1]], idx[2], 'ADD')

    return object_mesh

def get_object(collection, import_file, game_version, object_name, random_color_gen, report):
    geometry_count = len(import_file.geometries)
    materials = []
    for shader in import_file.shaders:
        permutation_index = ""
        if game_version == "retail" and not shader.permutation_index == 0:
            permutation_index = "%s" % shader.permutation_index

        material_name = "%s%s" % (os.path.basename(shader.tag_ref.name), permutation_index)
        mat = bpy.data.materials.get(material_name)
        if mat == None:
            mat = bpy.data.materials.new(name=material_name)
            shader_processing.generate_h1_shader(mat, shader.tag_ref, shader.permutation_index, report)

        materials.append(mat)

    full_mesh = bpy.data.meshes.new(object_name)
    object_mesh = bpy.data.objects.new(object_name, full_mesh)
    collection.objects.link(object_mesh)
    if (4, 1, 0) > bpy.app.version:
        object_mesh.data.use_auto_smooth = True

    for region in import_file.regions:
        region_name = "unnamed"
        if not region_name == "__unnamed":
            region_name = region.name

        for permutation in region.permutations:
            superhigh_geometry_index = permutation.superhigh_geometry_block
            if not superhigh_geometry_index == -1 and superhigh_geometry_index < geometry_count and not import_file.geometries[superhigh_geometry_index].visited:
                import_file.geometries[superhigh_geometry_index].visited = True
                superhigh_geometry = import_file.geometries[superhigh_geometry_index]
                build_mesh_layout(import_file, superhigh_geometry, region_name, random_color_gen, object_mesh, materials)

            break

    return object_mesh
