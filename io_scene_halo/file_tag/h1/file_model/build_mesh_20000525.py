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
from enum import Flag, Enum, auto
from mathutils import Matrix, Vector
from ....file_tag.tag_interface import tag_interface, tag_common
from ....global_functions import mesh_processing, global_functions

class EncodingEnum(Enum):
    _8bit = 0
    _8bit_intensity = auto()
    _16bit_555 = auto()
    _16bit_565 = auto()
    _16bit_4444 = auto()
    _16bit_8palette_plus_8alpha = auto()
    _16bit_intensity = auto()
    _32bit_888 = auto()
    _32bit_8888 = auto()
    _32bit_compressed = auto()
    _32bit_alpha_compressed = auto()

class TypeEnum(Enum):
    diffuse = 0
    transparent_alpha_blend = auto()
    self_illuminated_add = auto()
    gel_double_multiply = auto()
    detail_double_multiply = auto()
    specular_additive = auto()
    pre_diffuse_gloss = auto()
    halt_and_catch_fire = auto()
    light_double_multiply = auto()
    multitexture_color_mask = auto()
    multitexture_projection_multiply = auto()
    multitexture_local_alpha_blend = auto()
    multitexture_other_alpha_blend = auto()
    multitexture_alpha_mask = auto()
    custom_pattern_multitexture_alpha_blend = auto()
    custom_decal_alpha_blend = auto()
    bump_diffuse = auto()
    bump_specular = auto()
    specular_opaque = auto()
    mirror = auto()
    multitexture_alpha_replace = auto()

class RasterizerFlags(Flag):
    unfiltered = auto()
    undithered = auto()
    clamped = auto()
    trilinear_filtered = auto()
    alpha_replicate = auto()
    not_mipmapped = auto()
    alpha_test = auto()

def generate_legacy_material_simple_b(mat, map, RasterizerFlags, EncodingEnum, report):
    mat.use_nodes = True

    base_bitmap = parse_tag(map.texture, report, "halo1", "20000525")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    base_node = bitmap_processing.generate_legacy_image_node(mat, "", base_bitmap, map.texture.name, False, EncodingEnum)
    base_node.location = Vector((-1600, 500))

    connect_inputs(mat.node_tree, base_node, "Color", bdsf_principled, "Base Color")

    if not base_node.image == None:
        base_node.image.alpha_mode = 'CHANNEL_PACKED'

    if base_bitmap:
        rasterizer_flags_result = RasterizerFlags(map.rasterizer_flags)
        if RasterizerFlags.alpha_test == rasterizer_flags_result:
            connect_inputs(mat.node_tree, base_node, "Alpha", bdsf_principled, "Alpha")
            mat.blend_method = 'HASHED'
        else:
            mat.blend_method = 'OPAQUE'

    connect_inputs(mat.node_tree, base_node, "Color", bdsf_principled, "Base Color")

class TriangleStrips:
    def __init__(self, strips):
        self.strips = strips
        self.index = 0
        self.count = len(strips)

    def next(self):
        self.index += 1
        return self.strips[self.index - 1]

    def next_array(self, count):
        start = self.index
        self.index += count
        return self.strips[start:(start+count)]

    def reached_end(self) -> bool:
        return self.index >= self.count

def build_mesh(mode_asset, geometry, armature, LOD, region_name, permutation_name, full_mesh, simple_mesh, model_materials):
    mode_data = mode_asset["Data"]

    if region_name == "__unnamed":
        region_name = "unnamed"

    if permutation_name == "__base":
        permutation_name = "base"

    object_name = '%s %s %s' % (region_name, permutation_name, LOD)

    vertex_groups = []
    active_region_permutations = []
    shader_count = len(mode_data["shaders"])

    if simple_mesh:
        bm = bmesh.new()
        bm.from_mesh(full_mesh)

    else:
        bm = bmesh.new()
        full_mesh = bpy.data.meshes.new(object_name)
        object_mesh = bpy.data.objects.new(object_name, full_mesh)
        object_mesh.color = (1, 1, 1, 0)
        object_mesh.parent = armature
        mesh_processing.add_modifier(bpy.context, object_mesh, False, None, None, armature)

    node_set_0 = []
    node_set_1 = []
    vert_count = 0
    point_index = 0
    for part_idx, part in enumerate(geometry["parts"]):
        mesh = bpy.data.meshes.new("%s_%s" % (object_name, str(part_idx)))

        ngon_list = []
        vertices = [Vector(vertex["point"]) * 100 for vertex in part["points"]]
        vertex_normals = [Vector(vertex["vector"]) for vertex in part["normals"]]

        if not simple_mesh:
            weight_index = 0
            for vertex_group in part["vertex groups"]:
                for index in range(vertex_group["vertex count"]):
                    node_0_index = vertex_group["node index"]
                    node_1_index = vertex_group["secondary node index"]
                    node_0_weight = 1
                    node_1_weight = 0
                    if not node_1_index == -1:
                        weight_value = part["weights"][weight_index]["weight"]
                        node_0_weight = (1 - weight_value)
                        node_1_weight = weight_value

                    if not node_0_index == -1:
                        group_name = mode_data["nodes"][node_0_index]["name"]
                        if not node_0_index in vertex_groups:
                            vertex_groups.append(node_0_index)
                            object_mesh.vertex_groups.new(name = group_name)

                        group_index = object_mesh.vertex_groups.keys().index(group_name)
                        node_set_0.append((group_index, point_index, node_0_weight))

                    if not node_1_index == -1:
                        group_name = mode_data["nodes"][node_1_index]["name"]
                        if not node_1_index in vertex_groups:
                            vertex_groups.append(node_1_index)
                            object_mesh.vertex_groups.new(name = group_name)

                        group_index = object_mesh.vertex_groups.keys().index(group_name)
                        node_set_1.append((group_index, point_index, node_1_weight))
                        weight_index += 1

                    point_index += 1

        triangle_strips = TriangleStrips([triangle_strip["index"] for triangle_strip in part["triangle strip vertex indices"]])
        while not triangle_strips.reached_end():
            count = triangle_strips.next()
            strip = triangle_strips.next_array(count)
            for offset in range(count - 2):
                triangle = strip[offset:offset+3]
                if offset % 2 == 0: # even triangles in the strip need to be flipped for reasons
                    triangle.reverse()

                ngon_list.append(triangle)

        mesh.from_pydata(vertices, [], ngon_list)
        for poly in mesh.polygons:
            poly.use_smooth = True

        region_attribute = mesh.get_custom_attribute()
        mesh.normals_split_custom_set_from_vertices(vertex_normals)

        uv_name = 'UVMap_%s' % 0
        layer_uv = mesh.uv_layers.get(uv_name)
        if layer_uv is None:
            layer_uv = mesh.uv_layers.new(name=uv_name)

        for ngon_idx, ngon in enumerate(ngon_list):
            ngon_material_index = part["material"]
            if not ngon_material_index == -1 and ngon_material_index < shader_count:
                mat = model_materials[ngon_material_index]
                if mat.name not in full_mesh.materials:
                    full_mesh.materials.append(mat)

                material_index = full_mesh.materials.find(mat.name)
                mesh.polygons[ngon_idx].material_index = material_index

            if not simple_mesh:
                current_region_permutation = region_name
                if not current_region_permutation in active_region_permutations:
                    active_region_permutations.append(current_region_permutation)
                    object_mesh.data.region_add(current_region_permutation)

                region_index = active_region_permutations.index(current_region_permutation)
                region_attribute.data[ngon_idx].value = region_index + 1

            for point_idx, point in enumerate(ngon):
                loop_index = (3 * ngon_idx) + point_idx

                uv = part["texture uv"][point]
                layer_uv.data[loop_index].uv = (uv["u"], 1 - uv["v"])

        vert_count += len(vertices)

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

def get_geometry_layout(tag_ref, asset_cache, armature, is_triangle_list, shader_gen_override, report, simple_mesh=False, permutation_indicies=None):
    tag_groups = tag_common.h1_20000525_tag_groups
    mode_asset = tag_interface.get_disk_asset(tag_ref["path"], tag_groups.get(tag_ref["group name"]))
    mode_data = mode_asset["Data"]

    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors
    model_materials = []
    for shader in mode_data["shaders"]:
        mat = bpy.data.materials.new(name=shader["name"])
        diffuse_map = None
        for map in shader["maps"]:
            if TypeEnum.diffuse == TypeEnum(map["type"]["value"]):
                diffuse_map = map
                break
        if diffuse_map == None:
            for map in shader["maps"]:
                diffuse_map = map
                break

        #if not diffuse_map == None:
            #generate_legacy_material_simple_b(mat, diffuse_map, RasterizerFlags, EncodingEnum, print)

        model_materials.append(mat)

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
                build_mesh(mode_asset, superhigh_geometry, armature, 'superhigh', region["name"], permutation["name"], full_mesh, simple_mesh, model_materials)

            if not simple_mesh:
                if not high_geometry_index == -1 and high_geometry_index < geometry_count and not high_geometry_index in visited_geo:
                    visited_geo.add(high_geometry_index)
                    high_geometry = mode_data["geometries"][high_geometry_index]
                    build_mesh(mode_asset, high_geometry, armature, 'high', region["name"], permutation["name"], full_mesh, simple_mesh, model_materials)

                if not medium_geometry_index == -1 and medium_geometry_index < geometry_count and not medium_geometry_index in visited_geo:
                    visited_geo.add(medium_geometry_index)
                    medium_geometry = mode_data["geometries"][medium_geometry_index]
                    build_mesh(mode_asset, medium_geometry, armature, 'medium', region["name"], permutation["name"], full_mesh, simple_mesh, model_materials)

                if not low_geometry_index == -1 and low_geometry_index < geometry_count and not low_geometry_index in visited_geo:
                    visited_geo.add(low_geometry_index)
                    low_geometry = mode_data["geometries"][low_geometry_index]
                    build_mesh(mode_asset, low_geometry, armature, 'low', region["name"], permutation["name"], full_mesh, simple_mesh, model_materials)

                if not superlow_geometry_index == -1 and superlow_geometry_index < geometry_count and not superlow_geometry_index in visited_geo:
                    visited_geo.add(superlow_geometry_index)
                    superlow_geometry = mode_data["geometries"][superlow_geometry_index]
                    build_mesh(mode_asset, superlow_geometry, armature, 'superlow', region["name"], permutation["name"], full_mesh, simple_mesh, model_materials)

            else:
                break
