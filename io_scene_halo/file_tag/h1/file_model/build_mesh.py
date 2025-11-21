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
import json
import bmesh

from mathutils import Vector
from enum import Flag, Enum, auto
from ....file_tag.tag_interface import tag_interface, tag_common
from ....global_functions import shader_processing, mesh_processing, global_functions

class ModelFlags(Flag):
    blend_shared_normals = auto()
    parts_have_local_nodes = auto()
    ignore_skinning = auto()

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

def build_mesh(mode_asset, geometry, armature, LOD, region_name, permutation_name, is_triangle_list, random_color_gen, tag_ref, asset_cache, full_mesh, report, simple_mesh):
    mode_data = mode_asset["Data"]

    if region_name == "__unnamed":
        region_name = "unnamed"

    if permutation_name == "__base":
        permutation_name = "base"

    object_name = '%s %s %s' % (region_name, permutation_name, LOD)

    vertex_groups = []
    active_region_permutations = []
    shader_count = len(mode_data["shaders"])

    uses_local_nodes = False
    if mode_asset["Header"]["tag group"] == "mod2":
        uses_local_nodes = ModelFlags.parts_have_local_nodes in ModelFlags(mode_data["flags"])

    if simple_mesh:
        bm = bmesh.new()
        bm.from_mesh(full_mesh)

    else:
        bm = bmesh.new()
        full_mesh = bpy.data.meshes.new(object_name)
        object_mesh = bpy.data.objects.new(object_name, full_mesh)
        object_mesh.color = (1, 1, 1, 0)
        object_mesh.parent = armature
        mesh_processing.add_modifier(bpy.context, object_mesh, False, None, armature)

    node_set_0 = []
    node_set_1 = []
    vert_count = 0
    for part_idx, part in enumerate(geometry["parts"]):
        local_node_list = []
        local_node_list.append(part["local node indices"])
        for idx in range(21):
            local_node_list.append(part["local node indices_%s" % (idx + 1)])

        mesh = bpy.data.meshes.new("%s_%s" % (object_name, str(part_idx)))

        vertex_data = part["uncompressed vertices"]
        is_compressed = False
        if len(vertex_data) == 0:
            vertex_data = part["compressed vertices"]
            is_compressed = True

        triangle_indices = []
        triangles = []

        vertices = [Vector(vertex["position"]) * 100 for vertex in vertex_data]
        if is_compressed:
            vertex_normals = [decompress_normal32(vertex["normal"]) for vertex in vertex_data]
        else:
            vertex_normals = [Vector(vertex["normal"]) for vertex in vertex_data]

        if is_triangle_list:
            for triangle in part["triangle data"]:
                triangles.append([triangle["indices_2"], triangle["indices_1"], triangle["indices"]]) # Reversed order to fix facing normals

        else:
            for triangle in part["triangle data"]:
                if not triangle["indices"] == -1:
                    triangle_indices.append(triangle["indices"])
                if not triangle["indices_1"] == -1:
                    triangle_indices.append(triangle["indices_1"])
                if not triangle["indices_2"] == -1:
                    triangle_indices.append(triangle["indices_2"])

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
        mesh.normals_split_custom_set_from_vertices(vertex_normals)

        for vertex_idx, vertex in enumerate(vertex_data):
            if is_compressed:
                node_0_index = int(vertex["node0 index"] / 3)
                node_1_index = int(vertex["node1 index"] / 3)
                node_0_weight = vertex["node0 weight"] / 32767
                node_1_weight = 1 - vertex["node0 weight"]
            else:
                node_0_index = vertex["node0 index"]
                node_1_index = vertex["node1 index"]
                node_0_weight = vertex["node0 weight"]
                node_1_weight = vertex["node1 weight"]

            if not simple_mesh:
                if uses_local_nodes:
                    if not node_0_index == -1:
                        node_0_index = local_node_list[node_0_index]

                    if not node_1_index == -1:
                        node_1_index = local_node_list[node_1_index]

                if not node_0_index == -1:
                    group_name = mode_data["nodes"][node_0_index]["name"]
                    if not node_0_index in vertex_groups:
                        vertex_groups.append(node_0_index)
                        object_mesh.vertex_groups.new(name = group_name)

                    group_index = object_mesh.vertex_groups.keys().index(group_name)
                    node_set_0.append((group_index, vert_count + vertex_idx, node_0_weight))

                if not node_1_index == -1:
                    group_name = mode_data["nodes"][node_1_index]["name"]
                    if not node_1_index in vertex_groups:
                        vertex_groups.append(node_1_index)
                        object_mesh.vertex_groups.new(name = group_name)

                    group_index = object_mesh.vertex_groups.keys().index(group_name)
                    node_set_1.append((group_index, vert_count + vertex_idx, node_1_weight))

        for triangle_idx, triangle in enumerate(triangles):
            triangle_material_index = part["shader index"]
            if not triangle_material_index == -1 and triangle_material_index < shader_count:
                shader_element = mode_data["shaders"][triangle_material_index]
                shader_tag = shader_element["shader"]
                shader_group = shader_tag["group name"]
                shader_name = shader_tag["path"]
                permutation = shader_element["permutation"]

                has_permutation = permutation != 0

                base_name = os.path.basename(shader_name)
                SHAD_ASSET = asset_cache.get(shader_group, {}).get(shader_name)
                if SHAD_ASSET is not None:
                    material_name = base_name
                    if has_permutation:
                        material_name = "%s%s" % (base_name, permutation)
                        
                    mat = SHAD_ASSET["blender_assets"].get(material_name)
                    if not mat:
                        mat = bpy.data.materials.new(name=material_name)
                        shader_processing.generate_h1_shader(mat, shader_tag, permutation, asset_cache, report)
                        SHAD_ASSET["blender_assets"][material_name] = mat

                else:
                    material_name = "invalid"
                    if global_functions.string_empty_check(base_name):
                        material_name = base_name

                    if has_permutation:
                        material_name = "%s%s" % (material_name, permutation)

                    mat = bpy.data.materials.get(material_name)
                    if not mat:
                        mat = bpy.data.materials.new(name=material_name)

                if mat.name not in full_mesh.materials:
                    full_mesh.materials.append(mat)

                mat.diffuse_color = random_color_gen.next()
                material_index = full_mesh.materials.find(mat.name)
                mesh.polygons[triangle_idx].material_index = material_index

            if not simple_mesh:
                current_region_permutation = region_name
                if not current_region_permutation in active_region_permutations:
                    active_region_permutations.append(current_region_permutation)
                    object_mesh.data.region_add(current_region_permutation)

                region_index = active_region_permutations.index(current_region_permutation)
                region_attribute.data[triangle_idx].value = region_index + 1

            vertex_list = [vertex_data[triangle[0]], vertex_data[triangle[1]], vertex_data[triangle[2]]]
            for vertex_idx, vertex in enumerate(vertex_list):
                loop_index = (3 * triangle_idx) + vertex_idx
                uv_name = "UVMap_Render"
                layer_uv = mesh.uv_layers.get(uv_name)
                if layer_uv is None:
                    layer_uv = mesh.uv_layers.new(name=uv_name)


                if is_compressed:
                    U = vertex["texture coordinate u"] / 32767
                    V = vertex["texture coordinate v"] /32767
                else:
                    U, V = vertex["texture coords"]
 
                bmu_scale = mode_data["base map u scale"]
                bmv_scale = mode_data["base map v scale"]
                if not bmu_scale == 0.0:
                    U = bmu_scale * U

                if not bmv_scale == 0.0:
                    V = bmv_scale * V
                    
                layer_uv.data[loop_index].uv = (U, 1 - V)

        vert_count += len(vertex_data)

        bm.from_mesh(mesh)
        bpy.data.meshes.remove(mesh)

    bm.to_mesh(full_mesh)
    bm.free()

    if not simple_mesh:
        for idx in node_set_0:
            object_mesh.vertex_groups[idx[0]].add([idx[1]], idx[2], 'ADD')

        for idx in node_set_1:
            object_mesh.vertex_groups[idx[0]].add([idx[1]], idx[2], 'ADD')

        bpy.context.collection.objects.link(object_mesh)

    if (4, 1, 0) > bpy.app.version:
        full_mesh.use_auto_smooth = True

def get_geometry_layout(tag_ref, asset_cache, armature, is_triangle_list, report, simple_mesh=False):
    tag_groups = tag_common.h1_tag_groups
    mode_asset = tag_interface.get_disk_asset(tag_ref["path"], tag_groups.get(tag_ref["group name"]))
    mode_data = mode_asset["Data"]

    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors
    for shader in mode_data["shaders"]:
        shad_tag_ref = shader["shader"]
        SHAD_ASSET = asset_cache[shad_tag_ref["group name"]][shad_tag_ref["path"]]

        material_name = os.path.basename(shad_tag_ref["path"])
        if shader["permutation"] != 0:
            material_name = "%s%s" % (material_name, shader["permutation"])

        mat = SHAD_ASSET["blender_assets"].get(material_name)
        if not mat:
            mat = bpy.data.materials.new(name=material_name)
            SHAD_ASSET["blender_assets"][material_name] = mat

        shader_processing.generate_h1_shader(mat, shad_tag_ref, shader["permutation"], asset_cache, report)

    full_mesh = None
    if simple_mesh:
        object_name = os.path.basename(tag_ref["path"])
        full_mesh = bpy.data.meshes.new(object_name)
        asset_cache[tag_ref["group name"]][tag_ref["path"]]["blender_assets"]["blender_asset"] = full_mesh

    visited_geo = set()
    for region in mode_data["regions"]:
        for permutation in region["permutations"]:
            superlow_geometry_index = permutation["super low"]
            low_geometry_index = permutation["low"]
            medium_geometry_index = permutation["medium"]
            high_geometry_index = permutation["high"]
            superhigh_geometry_index = permutation["super high"]

            geometry_count = len(mode_data["geometries"])
            if not superhigh_geometry_index == -1 and superhigh_geometry_index < geometry_count and not superhigh_geometry_index in visited_geo:
                visited_geo.add(superhigh_geometry_index)
                superhigh_geometry = mode_data["geometries"][superhigh_geometry_index]
                build_mesh(mode_asset, superhigh_geometry, armature, 'superhigh', region["name"], permutation["name"], is_triangle_list, random_color_gen, tag_ref, asset_cache, full_mesh, report, simple_mesh)

            if not simple_mesh:
                if not high_geometry_index == -1 and high_geometry_index < geometry_count and not high_geometry_index in visited_geo:
                    visited_geo.add(high_geometry_index)
                    high_geometry = mode_data["geometries"][high_geometry_index]
                    build_mesh(mode_asset, high_geometry, armature, 'high', region["name"], permutation["name"], is_triangle_list, random_color_gen, tag_ref, asset_cache, full_mesh, report, simple_mesh)

                if not medium_geometry_index == -1 and medium_geometry_index < geometry_count and not medium_geometry_index in visited_geo:
                    visited_geo.add(medium_geometry_index)
                    medium_geometry = mode_data["geometries"][medium_geometry_index]
                    build_mesh(mode_asset, medium_geometry, armature, 'medium', region["name"], permutation["name"], is_triangle_list, random_color_gen, tag_ref, asset_cache, full_mesh, report, simple_mesh)

                if not low_geometry_index == -1 and low_geometry_index < geometry_count and not low_geometry_index in visited_geo:
                    visited_geo.add(low_geometry_index)
                    low_geometry = mode_data["geometries"][low_geometry_index]
                    build_mesh(mode_asset, low_geometry, armature, 'low', region["name"], permutation["name"], is_triangle_list, random_color_gen, tag_ref, asset_cache, full_mesh, report, simple_mesh)

                if not superlow_geometry_index == -1 and superlow_geometry_index < geometry_count and not superlow_geometry_index in visited_geo:
                    visited_geo.add(superlow_geometry_index)
                    superlow_geometry = mode_data["geometries"][superlow_geometry_index]
                    build_mesh(mode_asset, superlow_geometry, armature, 'superlow', region["name"], permutation["name"], is_triangle_list, random_color_gen, tag_ref, asset_cache, full_mesh, report, simple_mesh)

            else:
                break
