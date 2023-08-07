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

from math import radians
from mathutils import Vector, Matrix, Euler

def build_objects(object_tag_block, object_name, random_color_gen, material_count):
    for cluster_idx, cluster in enumerate(object_tag_block):
        cluster_name = "%s_%s" % (object_name, cluster_idx)
        full_mesh = bpy.data.meshes.new(cluster_name)
        object_mesh = bpy.data.objects.new(cluster_name, full_mesh)
        bm = bmesh.new()
        for cache_data in cluster.cache_data:
            for part_idx, part in enumerate(cache_data.parts):
                mesh = bpy.data.meshes.new("%s_%s" % ("part", str(part_idx)))

                triangles = []
                vertices = [raw_vertex.position for raw_vertex in cache_data.raw_vertices]

                strip_length = part.strip_length
                strip_start = part.strip_start_index

                triangle_indices = cache_data.strip_indices[strip_start : (strip_start + strip_length)]
                index_count = len(triangle_indices)

                for idx in range(int(index_count / 3)):
                    triangles.append([triangle_indices[(idx * 3) + 2], triangle_indices[(idx * 3) + 1], triangle_indices[(idx * 3) + 0]])

                # clean up any triangles that reference the same vertex multiple times
                for reversed_triangle in reversed(triangles):
                    if (reversed_triangle[0] == reversed_triangle[1]) or (reversed_triangle[1] == reversed_triangle[2]) or (reversed_triangle[0] == reversed_triangle[2]):
                        del triangles[triangles.index(reversed_triangle)]

                mesh.from_pydata(vertices, [], triangles)
                for poly in mesh.polygons:
                    poly.use_smooth = True

                for triangle_idx, triangle in enumerate(triangles):
                    triangle_material_index = part.material_index
                    if not triangle_material_index == -1 and triangle_material_index < material_count:
                        mat = -1

                    if not triangle_material_index == -1:
                        material_list = []
                        if triangle_material_index < material_count:
                            material_name = os.path.basename(mat.shader.name)

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

                    vertex_list = [cache_data.raw_vertices[triangle[0]], cache_data.raw_vertices[triangle[1]], cache_data.raw_vertices[triangle[2]]]
                    for vertex_idx, vertex in enumerate(vertex_list):
                        loop_index = (3 * triangle_idx) + vertex_idx
                        uv_name = 'UVMap_%s' % 0
                        layer_uv = mesh.uv_layers.get(uv_name)
                        if layer_uv is None:
                            layer_uv = mesh.uv_layers.new(name=uv_name)

                        layer_uv.data[loop_index].uv = (vertex.primary_lightmap_texcoord[0], 1 - vertex.primary_lightmap_texcoord[1])

                bm.from_mesh(mesh)
                bpy.data.meshes.remove(mesh)

            bm.to_mesh(full_mesh)
            bm.free()

            bpy.context.collection.objects.link(object_mesh)

def build_scene(context, LIGHTMAP, game_version, game_title, file_version, fix_rotations, empty_markers, report, mesh_processing, global_functions):
    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors

    material_count = 0
    for lightmap_groups_idx, lightmap_group in enumerate(LIGHTMAP.lightmap_groups):
        build_objects(lightmap_group.clusters, "cluster", random_color_gen, material_count)
        build_objects(lightmap_group.poop_definitions, "instance", random_color_gen, material_count)
