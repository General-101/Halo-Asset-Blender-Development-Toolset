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

from mathutils import Matrix
from ...global_functions import global_functions

def build_clusters(lightmap_group, SBSP_ASSET, level_root, random_color_gen, collection):
    if len(lightmap_group.clusters) > 0:
        material_count = 0
        if not SBSP_ASSET == None:
            material_count = len(SBSP_ASSET.materials)
        
        for cluster_idx, cluster in enumerate(lightmap_group.clusters):
            cluster_name = "cluster_%s" % cluster_idx
            full_mesh = bpy.data.meshes.new(cluster_name)
            object_mesh = bpy.data.objects.new(cluster_name, full_mesh)
            object_mesh.parent = level_root
            for cache_data in cluster.cache_data:
                triangles = []
                vertices = [raw_vertex.position for raw_vertex in cache_data.raw_vertices]

                triangle_length = int(len(cache_data.strip_indices) / 3)
                for idx in range(triangle_length):
                    triangle_index = (idx * 3)
                    v0 = cache_data.strip_indices[triangle_index]
                    v1 = cache_data.strip_indices[triangle_index + 1]
                    v2 = cache_data.strip_indices[triangle_index + 2]
                    triangles.append((v0, v1, v2))

                full_mesh.from_pydata(vertices, [], triangles)
                for poly in full_mesh.polygons:
                    poly.use_smooth = True

                uv_name = 'UVMap_%s' % 0
                layer_uv = full_mesh.uv_layers.get(uv_name)
                if layer_uv is None:
                    layer_uv = full_mesh.uv_layers.new(name=uv_name)
                
                for idx in range(triangle_length):
                    triangle_index = (idx * 3)
                    v0 = cache_data.strip_indices[triangle_index]
                    v1 = cache_data.strip_indices[triangle_index + 1]
                    v2 = cache_data.strip_indices[triangle_index + 2]
                
                    vertex_list = [cache_data.raw_vertices[v0], cache_data.raw_vertices[v1], cache_data.raw_vertices[v2]]
                    for vertex_idx, vertex in enumerate(vertex_list):
                        loop_index = triangle_index + vertex_idx

                        U = vertex.primary_lightmap_texcoord[0]
                        V = vertex.primary_lightmap_texcoord[1]

                        layer_uv.data[loop_index].uv = (U, V)

                triangle_start = 0
                for part in cache_data.parts:
                    part_indices = cache_data.strip_indices[part.strip_start_index : (part.strip_start_index + part.strip_length)]
                    part_triangle_length = int(len(part_indices) / 3)
                    material = None
                    if not part.material_index == -1 and material_count > 0:
                        material = SBSP_ASSET.materials[part.material_index]

                    if material:
                        if len(material.shader.name) > 0:
                            material_name = os.path.basename(material.shader.name)

                        else:
                            material_name = "invalid_material_%s" % part.material_index

                        mat = bpy.data.materials.get(material_name)
                        if mat is None:
                            mat = bpy.data.materials.new(name=material_name)

                        if not material_name in object_mesh.data.materials.keys():
                            object_mesh.data.materials.append(mat)

                        mat.diffuse_color = random_color_gen.next()
                        material_index = object_mesh.data.materials.keys().index(material_name)

                        for triangle_idx in range(part_triangle_length):
                            full_mesh.polygons[triangle_start + triangle_idx].material_index = material_index

                    triangle_start += part_triangle_length

                collection.objects.link(object_mesh)

def build_poops(lightmap_group, SBSP_ASSET, level_root, random_color_gen, collection):
    if len(lightmap_group.poop_definitions) > 0:
        meshes = []
        material_count = 0
        if not SBSP_ASSET == None:
            material_count = len(SBSP_ASSET.materials)

        for poop_definition_idx, poop_definition in enumerate(lightmap_group.poop_definitions):
            cluster_name = "instanced_geometry_definition_%s" % poop_definition_idx
            mesh = bpy.data.meshes.new(cluster_name)
            for render_data in poop_definition.cache_data:
                triangles = []
                vertices = [raw_vertex.position for raw_vertex in render_data.raw_vertices]

                triangle_length = int(len(render_data.strip_indices) / 3)
                for idx in range(triangle_length):
                    triangle_index = (idx * 3)
                    v0 = render_data.strip_indices[triangle_index]
                    v1 = render_data.strip_indices[triangle_index + 1]
                    v2 = render_data.strip_indices[triangle_index + 2]
                    triangles.append((v0, v1, v2))

                mesh.from_pydata(vertices, [], triangles)
                for poly in mesh.polygons:
                    poly.use_smooth = True

                uv_name = 'UVMap_%s' % 0
                layer_uv = mesh.uv_layers.get(uv_name)
                if layer_uv is None:
                    layer_uv = mesh.uv_layers.new(name=uv_name)
                
                for idx in range(triangle_length):
                    triangle_index = (idx * 3)
                    v0 = render_data.strip_indices[triangle_index]
                    v1 = render_data.strip_indices[triangle_index + 1]
                    v2 = render_data.strip_indices[triangle_index + 2]
                
                    vertex_list = [render_data.raw_vertices[v0], render_data.raw_vertices[v1], render_data.raw_vertices[v2]]
                    for vertex_idx, vertex in enumerate(vertex_list):
                        loop_index = triangle_index + vertex_idx

                        U = vertex.primary_lightmap_texcoord[0]
                        V = vertex.primary_lightmap_texcoord[1]

                        layer_uv.data[loop_index].uv = (U, V)

                triangle_start = 0
                for part in render_data.parts:
                    part_indices = render_data.strip_indices[part.strip_start_index : (part.strip_start_index + part.strip_length)]
                    part_triangle_length = int(len(part_indices) / 3)
                    material = None
                    if not part.material_index == -1  and material_count > 0:
                        material = SBSP_ASSET.materials[part.material_index]

                    if material:
                        if len(material.shader.name) > 0:
                            material_name = os.path.basename(material.shader.name)

                        else:
                            material_name = "invalid_material_%s" % part.material_index

                        mat = bpy.data.materials.get(material_name)
                        if mat is None:
                            mat = bpy.data.materials.new(name=material_name)

                        if not material_name in mesh.materials.keys():
                            mesh.materials.append(mat)

                        mat.diffuse_color = random_color_gen.next()
                        material_index = mesh.materials.keys().index(material_name)

                        for triangle_idx in range(part_triangle_length):
                            mesh.polygons[triangle_start + triangle_idx].material_index = material_index

                    triangle_start += part_triangle_length

            meshes.append(mesh)

        for instanced_geometry_instance_idx, instanced_geometry_instance in enumerate(SBSP_ASSET.instanced_geometry_instances):
            mesh = meshes[instanced_geometry_instance.instance_definition]
            ob_name = instanced_geometry_instance.name

            object_mesh = bpy.data.objects.new(ob_name, mesh)
            object_mesh.parent = level_root
            collection.objects.link(object_mesh)

            matrix_scale = Matrix.Scale(instanced_geometry_instance.scale, 4)
            matrix_rotation = Matrix()
            matrix_rotation[0] = *instanced_geometry_instance.forward, 0
            matrix_rotation[1] = *instanced_geometry_instance.left, 0
            matrix_rotation[2] = *instanced_geometry_instance.up, 0
            matrix_rotation = matrix_rotation.inverted()
            matrix_translation = Matrix.Translation(instanced_geometry_instance.position)
            transform_matrix = (matrix_translation @ matrix_rotation @ matrix_scale)
            object_mesh.matrix_world = transform_matrix

def build_scene(context, LTMP_ASSET, game_version, game_title, file_version, fix_rotations, empty_markers, report, collection_override=None, cluster_collection_override=None, SBSP_ASSET=None):
    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors

    collection = context.collection
    if not collection_override == None:
        collection = collection_override

    if cluster_collection_override == None:
        cluster_collection_override = collection

    level_root = bpy.data.objects.get("frame_root")
    if level_root == None:
        level_mesh = bpy.data.meshes.new("frame_root")
        level_root = bpy.data.objects.new("frame_root", level_mesh)
        collection.objects.link(level_root)

    for lightmap_groups_idx, lightmap_group in enumerate(LTMP_ASSET.lightmap_groups):
        build_clusters(lightmap_group, SBSP_ASSET, level_root, random_color_gen, cluster_collection_override)
        build_poops(lightmap_group, SBSP_ASSET, level_root, random_color_gen, cluster_collection_override)
