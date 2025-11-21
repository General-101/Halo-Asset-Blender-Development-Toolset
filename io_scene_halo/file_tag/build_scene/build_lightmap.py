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

from enum import Flag, Enum, auto
from mathutils import Matrix, Vector
from ...global_functions import global_functions, mesh_processing
from ...file_tag.tag_interface import tag_interface, tag_common

class ClusterPortalFlags(Flag):
    ai_cant_hear_through_this = auto()
    one_way = auto()
    door = auto()
    no_way = auto()
    one_way_reversed = auto()
    no_one_can_hear_through_this = auto()

class SurfaceFlags(Flag):
    two_sided = auto()
    invisible = auto()
    climbable = auto()
    breakable = auto()
    invalid = auto()
    conveyor = auto()

class PartFlags(Flag):
    decalable = auto()
    new_part_type = auto()
    dislikes_photons = auto()
    override_triangle_list = auto()
    ignored_by_lightmapper = auto()

class PropertyTypeEnum(Enum):
    lightmap_resolution = 0
    lightmap_power = auto()
    lightmap_half_life = auto()
    lightmap_diffuse_scale = auto()

class PartTypeEnum(Enum):
    not_drawn = 0
    opaque_shadow_only = auto()
    opaque_shadow_casting = auto()
    opaque_non_shadowing = auto()
    transparent = auto()
    lightmap_only = auto()

def process_mesh(sbsp_data, asset_cache, random_color_gen, tag_block, poop_name, material_count, shader_collection_dic):
    mesh = None
    for render_data in tag_block["cache data"]:
        triangles = []
        vertices = [Vector(raw_vertex["position"]) * 100 for raw_vertex in render_data["raw vertices"]]
        normals = [Vector(raw_vertex["normal"]) for raw_vertex in render_data["raw vertices"]]

        triangle_length = int(len(render_data["strip indices"]) / 3)
        for idx in range(triangle_length):
            triangle_index = (idx * 3)
            v0 = render_data["strip indices"][triangle_index]["index"]
            v1 = render_data["strip indices"][triangle_index + 1]["index"]
            v2 = render_data["strip indices"][triangle_index + 2]["index"]
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
            for part in render_data["parts"]:
                strip_length = part["strip length"]
                strip_start = part["strip start index"]

                triangle_indices = render_data["strip indices"][strip_start : (strip_start + strip_length)]
                triangle_length = int(len(triangle_indices) / 3)
                for idx in range(triangle_length):
                    triangle_index = (idx * 3)
                    v0 = triangle_indices[triangle_index]["index"]
                    v1 = triangle_indices[triangle_index + 1]["index"]
                    v2 = triangle_indices[triangle_index + 2]["index"]

                    vertex_list = [render_data["raw vertices"][v0], render_data["raw vertices"][v1], render_data["raw vertices"][v2]]
                    for vertex_idx, vertex in enumerate(vertex_list):
                        loop_index = (triangle_start * 3) + triangle_index + vertex_idx

                        u_0, v_0 = vertex["texcoord"]
                        u_1, v_1 = vertex["primary lightmap texcoord"]

                        render_layer_uv.data[loop_index].uv = (u_0, 1 - v_0)
                        lightmap_layer_uv.data[loop_index].uv = (u_1, v_1)

                tag_element = None
                if not part["material"] == -1 and material_count > 0 and part["material"] < material_count:
                    tag_element = sbsp_data["materials"][part["material"]]

                if tag_element:
                    mat = mesh_processing.get_material(tag_element, asset_cache, "halo2", shader_collection_dic)

                    if not mat in mesh.materials.values():
                        mesh.materials.append(mat)

                    mat.diffuse_color = random_color_gen.next()
                    material_index = mesh.materials.values().index(mat)
                    for triangle_idx in range(triangle_length):
                        mesh.polygons[triangle_start + triangle_idx].material_index = material_index

                triangle_start += triangle_length

    return mesh

def build_clusters(lightmap_group, sbsp_data, asset_cache, level_root, random_color_gen, collection, shader_collection_dic, material_count):
    if len(lightmap_group["clusters"]) > 0:
        for cluster_idx, cluster in enumerate(lightmap_group["clusters"]):
            cluster_name = "cluster_%s" % cluster_idx
            mesh = process_mesh(sbsp_data, asset_cache, random_color_gen, cluster, cluster_name, material_count, shader_collection_dic)
            if not mesh == None:
                object_mesh = bpy.data.objects.new(cluster_name, mesh)
                object_mesh.color = (1, 1, 1, 0)
                collection.objects.link(object_mesh)
                object_mesh.parent = level_root

                if (4, 1, 0) > bpy.app.version:
                    object_mesh.data.use_auto_smooth = True

def build_poops(lightmap_group, sbsp_data, asset_cache, level_root, random_color_gen, collection, shader_collection_dic, material_count):
    lightmap_instance_count = len(lightmap_group["poop definitions"])
    if lightmap_instance_count > 0:
        bsp_name = collection.name.rsplit("_", 1)[0]
        intances_name = "%s_lightmap_instances" % bsp_name
        instance_collection = bpy.data.collections.get(intances_name)
        if instance_collection == None:
            instance_collection = bpy.data.collections.new(intances_name)
            collection.children.link(instance_collection)

        meshes = []
        for poop_definition_idx, poop_definition in enumerate(lightmap_group["poop definitions"]):
            poop_name = "instanced_geometry_definition_%s" % poop_definition_idx
            mesh = process_mesh(sbsp_data, asset_cache, random_color_gen, poop_definition, poop_name, material_count, shader_collection_dic)
            meshes.append(mesh)

        if sbsp_data is not None:
            for instanced_geometry_instance in sbsp_data["instanced geometry instances"]:
                if not instanced_geometry_instance["instance definition"] == -1 and instanced_geometry_instance["instance definition"] < lightmap_instance_count:
                    mesh = meshes[instanced_geometry_instance["instance definition"]]
                    ob_name = instanced_geometry_instance["name"]
                    if not mesh == None:
                        object_mesh = bpy.data.objects.new(ob_name, mesh)
                        object_mesh.color = (1, 1, 1, 0)
                        object_mesh.parent = level_root
                        instance_collection.objects.link(object_mesh)

                        object_mesh.tag_mesh.instance_lightmap_policy_enum = str(instanced_geometry_instance["lightmapping policy"]["value"])

                        matrix_scale = Matrix.Scale(instanced_geometry_instance["scale"], 4)
                        matrix_rotation = Matrix()
                        matrix_rotation[0] = *Vector(instanced_geometry_instance["forward"]), 0
                        matrix_rotation[1] = *Vector(instanced_geometry_instance["left"]), 0
                        matrix_rotation[2] = *Vector(instanced_geometry_instance["up"]), 0
                        matrix_rotation = matrix_rotation.inverted()
                        matrix_translation = Matrix.Translation(Vector(instanced_geometry_instance["position"]) * 100)
                        transform_matrix = (matrix_translation @ matrix_rotation @ matrix_scale)
                        object_mesh.matrix_world = transform_matrix

                        if (4, 1, 0) > bpy.app.version:
                            object_mesh.data.use_auto_smooth = True

def build_scene(context, tag_ref, asset_cache, game_title, fix_rotations, empty_markers, report, collection_override=None, cluster_collection_override=None, sbsp_tag_ref=None):
    if game_title == "halo1":
        tag_groups = tag_common.h1_tag_groups
    elif game_title == "halo2":
        tag_groups = tag_common.h2_tag_groups
    else:
        print("%s is not supported." % game_title)

    sbsp_data = None
    ltmp_data = tag_interface.get_disk_asset(tag_ref["path"], tag_groups.get(tag_ref["group name"]))["Data"]
    if sbsp_tag_ref is not None:
        sbsp_data = tag_interface.get_disk_asset(sbsp_tag_ref["path"], tag_groups.get(sbsp_tag_ref["group name"]))["Data"]
    
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
        level_root.color = (1, 1, 1, 0)
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

    material_count = 0
    if not sbsp_data == None:
        material_count = len(sbsp_data["materials"])

    for lightmap_group in ltmp_data["lightmap groups"]:
        build_clusters(lightmap_group, sbsp_data, asset_cache, level_root, random_color_gen, cluster_collection_override, shader_collection_dic, material_count)
        build_poops(lightmap_group, sbsp_data, asset_cache, level_root, random_color_gen, cluster_collection_override, shader_collection_dic, material_count)
