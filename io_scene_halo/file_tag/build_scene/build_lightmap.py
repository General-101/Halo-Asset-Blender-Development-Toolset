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
from ..h2.file_scenario_structure_bsp.format import ClusterPortalFlags as H2ClusterPortalFlags, SurfaceFlags as H2SurfaceFlags, PartFlags, PropertyTypeEnum
from ..h2.file_scenario_structure_lightmap.format import PartTypeEnum
from ...global_functions import global_functions

def process_mesh(SBSP_ASSET, random_color_gen, tag_block, poop_name, material_count, shader_collection_dic):
    mesh = None
    for render_data in tag_block.cache_data:
        triangles = []
        vertices = [raw_vertex.position * 100 for raw_vertex in render_data.raw_vertices]
        normals = [raw_vertex.normal for raw_vertex in render_data.raw_vertices]

        triangle_length = int(len(render_data.strip_indices) / 3)
        for idx in range(triangle_length):
            triangle_index = (idx * 3)
            v0 = render_data.strip_indices[triangle_index]
            v1 = render_data.strip_indices[triangle_index + 1]
            v2 = render_data.strip_indices[triangle_index + 2]
            triangles.append((v0, v1, v2))

        if len(vertices) > 0:
            mesh = bpy.data.meshes.new(poop_name)
            mesh.from_pydata(vertices, [], triangles)
            for poly in mesh.polygons:
                poly.use_smooth = True

            mesh.normals_split_custom_set_from_vertices(normals)
            uv_name_render = 'UVMap_Render'
            uv_name_lightmap = 'UVMap_Lightmap'
            render_layer_uv = mesh.uv_layers.get(uv_name_render)
            if render_layer_uv is None:
                render_layer_uv = mesh.uv_layers.new(name=uv_name_render)

            lightmap_layer_uv = mesh.uv_layers.get(uv_name_lightmap)
            if lightmap_layer_uv is None:
                lightmap_layer_uv = mesh.uv_layers.new(name=uv_name_lightmap)

            triangle_start = 0
            for part in render_data.parts:
                strip_length = part.strip_length
                strip_start = part.strip_start_index

                triangle_indices = render_data.strip_indices[strip_start : (strip_start + strip_length)]
                triangle_length = int(len(triangle_indices) / 3)
                for idx in range(triangle_length):
                    triangle_index = (idx * 3)
                    v0 = triangle_indices[triangle_index]
                    v1 = triangle_indices[triangle_index + 1]
                    v2 = triangle_indices[triangle_index + 2]

                    vertex_list = [render_data.raw_vertices[v0], render_data.raw_vertices[v1], render_data.raw_vertices[v2]]
                    for vertex_idx, vertex in enumerate(vertex_list):
                        loop_index = (triangle_start * 3) + triangle_index + vertex_idx

                        U0 = vertex.texcoord[0]
                        V0 = vertex.texcoord[1]
                        U1 = vertex.primary_lightmap_texcoord[0]
                        V1 = vertex.primary_lightmap_texcoord[1]

                        render_layer_uv.data[loop_index].uv = (U0, 1 - V0)
                        lightmap_layer_uv.data[loop_index].uv = (U1, V1)

                material = None
                if not part.material_index == -1 and material_count > 0 and part.material_index < material_count:
                    material = SBSP_ASSET.materials[part.material_index]

                if material:
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

                    mat = bpy.data.materials.get(material_name)
                    if mat is None:
                        mat = bpy.data.materials.new(name=material_name)

                    if not mat in mesh.materials.values():
                        mesh.materials.append(mat)

                    mat.diffuse_color = random_color_gen.next()
                    material_index = mesh.materials.values().index(mat)
                    for triangle_idx in range(triangle_length):
                        mesh.polygons[triangle_start + triangle_idx].material_index = material_index

                triangle_start += triangle_length

    return mesh

def build_clusters(lightmap_group, SBSP_ASSET, level_root, random_color_gen, collection, shader_collection_dic):
    if len(lightmap_group.clusters) > 0:
        material_count = 0
        if not SBSP_ASSET == None:
            material_count = len(SBSP_ASSET.materials)

        for cluster_idx, cluster in enumerate(lightmap_group.clusters):
            cluster_name = "cluster_%s" % cluster_idx
            mesh = process_mesh(SBSP_ASSET, random_color_gen, cluster, cluster_name, material_count, shader_collection_dic)
            if not mesh == None:
                object_mesh = bpy.data.objects.new(cluster_name, mesh)
                collection.objects.link(object_mesh)
                object_mesh.parent = level_root

                if (4, 1, 0) > bpy.app.version:
                    object_mesh.data.use_auto_smooth = True

def build_poops(lightmap_group, SBSP_ASSET, level_root, random_color_gen, collection, shader_collection_dic):
    lightmap_instance_count = len(lightmap_group.poop_definitions)
    if lightmap_instance_count > 0:
        bsp_name = collection.name.split("_", 1)[0]
        intances_name = "%s_lightmap_instances" % bsp_name
        instance_collection = bpy.data.collections.get(intances_name)
        if instance_collection == None:
            instance_collection = bpy.data.collections.new(intances_name)
            collection.children.link(instance_collection)

        meshes = []
        material_count = 0
        if not SBSP_ASSET == None:
            material_count = len(SBSP_ASSET.materials)

        for poop_definition_idx, poop_definition in enumerate(lightmap_group.poop_definitions):
            poop_name = "instanced_geometry_definition_%s" % poop_definition_idx
            mesh = process_mesh(SBSP_ASSET, random_color_gen, poop_definition, poop_name, material_count, shader_collection_dic)
            meshes.append(mesh)

        for instanced_geometry_instance in SBSP_ASSET.instanced_geometry_instances:
            if not instanced_geometry_instance.instance_definition == -1 and instanced_geometry_instance.instance_definition < lightmap_instance_count:
                mesh = meshes[instanced_geometry_instance.instance_definition]
                ob_name = instanced_geometry_instance.name
                if not mesh == None:
                    object_mesh = bpy.data.objects.new(ob_name, mesh)
                    object_mesh.parent = level_root
                    instance_collection.objects.link(object_mesh)

                    object_mesh.tag_mesh.instance_lightmap_policy_enum = str(instanced_geometry_instance.lightmapping_policy)

                    matrix_scale = Matrix.Scale(instanced_geometry_instance.scale, 4)
                    matrix_rotation = Matrix()
                    matrix_rotation[0] = *instanced_geometry_instance.forward, 0
                    matrix_rotation[1] = *instanced_geometry_instance.left, 0
                    matrix_rotation[2] = *instanced_geometry_instance.up, 0
                    matrix_rotation = matrix_rotation.inverted()
                    matrix_translation = Matrix.Translation(instanced_geometry_instance.position)
                    transform_matrix = (matrix_translation @ matrix_rotation @ matrix_scale)
                    object_mesh.matrix_world = transform_matrix

                    if (4, 1, 0) > bpy.app.version:
                        object_mesh.data.use_auto_smooth = True

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

    for lightmap_groups_idx, lightmap_group in enumerate(LTMP_ASSET.lightmap_groups):
        build_clusters(lightmap_group, SBSP_ASSET, level_root, random_color_gen, cluster_collection_override, shader_collection_dic)
        build_poops(lightmap_group, SBSP_ASSET, level_root, random_color_gen, cluster_collection_override, shader_collection_dic)
