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

from .....global_functions import shader_processing, global_functions
from .....file_tag.h2.file_render_model.format import PartFlags, PropertyTypeEnum

def build_mesh_layout(asset, section, region_name, random_color_gen, object_mesh, materials):
    vertex_groups = []
    active_region_permutations = []
    vertex_weights_sets = []
    shader_count = len(asset.materials)
    bm = bmesh.new()
    bm.from_mesh(object_mesh.data)
    for section_idx, section_data in enumerate(section.section_data):
        mesh = bpy.data.meshes.new("%s_%s" % ("part", str(section_idx)))

        triangles = []
        triangle_mat_indices = []
        vertices = [raw_vertex.position for raw_vertex in section_data.raw_vertices]
        vertex_normals = [raw_vertex.normal for raw_vertex in section_data.raw_vertices]
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
        mesh.normals_split_custom_set_from_vertices(vertex_normals)
        for triangle_idx, triangle in enumerate(triangles):
            triangle_material_index = triangle_mat_indices[triangle_idx]
            if not triangle_material_index == -1 and triangle_material_index < shader_count:
                mat = asset.materials[triangle_material_index]

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

    bm.to_mesh(object_mesh.data)
    bm.free()

def get_object(collection, import_file, game_version, object_name, random_color_gen, report):
    section_count = len(import_file.sections)
    materials = []
    shader_collection_dic = {}
    shader_collection_path = os.path.join(bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_tag_path, r"scenarios\shaders\shader_collections.shader_collections")
    if os.path.isfile(shader_collection_path):
        shader_collection_file = open(shader_collection_path, "r")
        for line in shader_collection_file.readlines():
            if not global_functions.string_empty_check(line) and not line.startswith(";"):
                split_result = line.split()
                if len(split_result) == 2:
                    prefix = split_result[0]
                    path = split_result[1]
                    shader_collection_dic[path] = prefix

    for material in import_file.materials:
        material_path = material.shader.name
        if global_functions.string_empty_check(material_path):
            material_path = material.old_shader.name

        material_directory = os.path.dirname(material_path)
        material_name = os.path.basename(material_path)

        collection_prefix = shader_collection_dic.get(material_directory)
        if not collection_prefix == None:
            material_name = "%s %s" % (collection_prefix, material_name)
        else:
            print("Could not find a collection for: %s" % material_path)

        for material_property in material.properties:
            property_enum = PropertyTypeEnum(material_property.property_type)
            property_value = material_property.real_value
            if PropertyTypeEnum.lightmap_resolution == property_enum:
                material_name += " lm:%s" % property_value

            elif PropertyTypeEnum.lightmap_power == property_enum:
                material_name += " lp:%s" % property_value

            elif PropertyTypeEnum.lightmap_half_life == property_enum:
                material_name += " hl:%s" % property_value

            elif PropertyTypeEnum.lightmap_diffuse_scale == property_enum:
                material_name += " ds:%s" % property_value

        mat = bpy.data.materials.new(name=material_name)
        shader_processing.generate_h2_shader(mat, material.shader, report)

        materials.append(mat)

    full_mesh = bpy.data.meshes.new(object_name)
    object_mesh = bpy.data.objects.new(object_name, full_mesh)
    collection.objects.link(object_mesh)
    try:
        object_mesh.data.use_auto_smooth = True
    except:
        print()
    
    for region in import_file.regions:
        region_name = "unnamed"
        if not region_name == "__unnamed":
            region_name = region.name

        for permutation in region.permutations:
            l6_section_index = permutation.l6_section_index
            if not l6_section_index == -1 and l6_section_index < section_count and not import_file.sections[l6_section_index].visited:
                import_file.sections[l6_section_index].visited = True
                l6_section = import_file.sections[l6_section_index]
                build_mesh_layout(import_file, l6_section, region_name, random_color_gen, object_mesh, materials)

            break

    return object_mesh
