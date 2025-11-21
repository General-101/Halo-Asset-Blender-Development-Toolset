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

import bpy

from enum import Flag, Enum, auto
from mathutils import Vector
from ...global_functions import global_functions
from ...file_tag.tag_interface import tag_interface, tag_common
from .shader_helper import (
    convert_to_blender_color, 
    set_image_scale,
    get_output_material_node, 
    connect_inputs, 
    generate_image_node,
    place_node,
    HALO_1_SHADER_RESOURCES
    )

class ModelFlags(Flag):
    detail_after_reflections = auto()
    two_sided = auto()
    not_alpha_tested = auto()
    alpha_blended_decal = auto()
    true_atmospheric_fog = auto()
    disable_two_sided_culling = auto()
    multipurpose_map_uses_og_xbox_channel_order = auto()

class FunctionEnum(Enum):
    one = 0
    zero = auto()
    cosine = auto()
    cosine_variable_period = auto()
    diagonal_wave = auto()
    diagonal_wave_variable_period = auto()
    slide = auto()
    slide_variable_period = auto()
    noise = auto()
    jitter = auto()
    wander = auto()
    spark = auto()

class FormatEnum(Enum):
    compressed_with_color_key_transparency = 0
    compressed_with_explicit_alpha = auto()
    compressed_with_interpolated_alpha = auto()
    _16bit_color = auto()
    _32bit_color = auto()
    monochrome = auto()
    high_quality_compression = auto()

def get_shader_model_node(tree):
    if not bpy.data.node_groups.get("shader_model"):
        with bpy.data.libraries.load(HALO_1_SHADER_RESOURCES) as (data_from, data_to):
            data_to.node_groups.append(data_from.node_groups[data_from.node_groups.index('shader_model')])

    shader_model_node = tree.nodes.new('ShaderNodeGroup')
    shader_model_node.node_tree = bpy.data.node_groups.get("shader_model")

    return shader_model_node

def generate_shader_model(mat, shader_asset, permutation_index, asset_cache, report):
    tag_groups = tag_common.h1_tag_groups
    shader_data = shader_asset["Data"]

    mat.use_nodes = True
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node)

    shader_model_node = get_shader_model_node(mat.node_tree)
    place_node(shader_model_node, 1)
    shader_model_node.name = "Shader Model"
    shader_model_node.width = 400.0
    shader_model_node.height = 100.0

    connect_inputs(mat.node_tree, shader_model_node, "Shader", output_material_node, "Surface")

    base_map_texture = generate_image_node(mat, shader_data["base map"], permutation_index, asset_cache, "halo1", report)
    base_bitmap = None
    base_map_node = None
    if base_map_texture:
        base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        base_map_node.image = base_map_texture
        base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        place_node(base_map_node, 2)
        connect_inputs(mat.node_tree, base_map_node, "Color", shader_model_node, "Base Map")
        connect_inputs(mat.node_tree, base_map_node, "Alpha", shader_model_node, "Base Map Alpha")

        bm_u_scale = shader_data["map u scale"]
        if bm_u_scale == 0.0:
            bm_u_scale = 1.0

        bm_v_scale = shader_data["map v scale"]
        if bm_v_scale == 0.0:
            bm_v_scale = 1.0

        bm_image_scale = (bm_u_scale, bm_v_scale, 1)

        base_bitmap = tag_interface.get_disk_asset(shader_data["base map"]["path"], tag_groups.get(shader_data["base map"]["group name"]))
        set_image_scale(mat, base_map_node, bm_image_scale)

    multipurpose_map_texture = generate_image_node(mat, shader_data["multipurpose map"], permutation_index, asset_cache, "halo1", report)
    if multipurpose_map_texture:
        multipurpose_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        multipurpose_map_node.image = multipurpose_map_texture
        multipurpose_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        multipurpose_map_node.image.colorspace_settings.name = 'Non-Color'
        multipurpose_map_node.interpolation = 'Cubic'
        place_node(multipurpose_map_node, 2, 1)
        connect_inputs(mat.node_tree, multipurpose_map_node, "Color", shader_model_node, "Multipurpose Map")
        connect_inputs(mat.node_tree, multipurpose_map_node, "Alpha", shader_model_node, "Multipurpose Map Alpha")

        mm_u_scale = shader_data["map u scale"]
        if mm_u_scale == 0.0:
            mm_u_scale = 1.0

        mm_v_scale = shader_data["map v scale"]
        if mm_v_scale == 0.0:
            mm_v_scale = 1.0

        mm_image_scale = (mm_u_scale, mm_v_scale, 1)

        set_image_scale(mat, multipurpose_map_node, mm_image_scale)

    detail_map_texture = generate_image_node(mat, shader_data["detail map"], permutation_index, asset_cache, "halo1", report)
    if detail_map_texture:
        detail_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        detail_map_node.image = detail_map_texture
        detail_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        place_node(detail_map_node, 2, 2)
        connect_inputs(mat.node_tree, detail_map_node, "Color", shader_model_node, "Detail Map")
        connect_inputs(mat.node_tree, detail_map_node, "Alpha", shader_model_node, "Detail Map Alpha")

        dm_scale = shader_data["detail map scale"]
        if dm_scale == 0.0:
            dm_scale = 1.0

        dm_v_scale = shader_data["detail map v scale"]

        dm_image_scale = (dm_scale, dm_scale + dm_v_scale, 1)

        set_image_scale(mat, detail_map_node, dm_image_scale)

    cube_map_texture = generate_image_node(mat, shader_data["cube map"], permutation_index, asset_cache, "halo1", report)
    if cube_map_texture:
        cube_map_node = mat.node_tree.nodes.new("ShaderNodeTexEnvironment")
        cube_map_node.image = cube_map_texture
        cube_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        place_node(cube_map_node, 2, 3)
        connect_inputs(mat.node_tree, cube_map_node, "Color", shader_model_node, "Reflection Cube Map")

    shader_model_node.inputs["Power"].default_value = shader_data["power"]
    shader_model_node.inputs["Color of Emitted Light"].default_value = convert_to_blender_color(shader_data["color of emitted light"], True)

    shader_model_flags = ModelFlags(shader_data["flags_1"])

    if ModelFlags.detail_after_reflections in shader_model_flags:
        shader_model_node.inputs["Detail After Reflections"].default_value = True

    mat.use_backface_culling = True
    if ModelFlags.two_sided in shader_model_flags:
        shader_model_node.inputs["Two-Sided"].default_value = True
        mat.use_backface_culling = False

    if ModelFlags.not_alpha_tested in shader_model_flags:
        shader_model_node.inputs["Not Alpha-Tested"].default_value = True

    if ModelFlags.alpha_blended_decal in shader_model_flags:
        shader_model_node.inputs["Alpha-Blended Decal"].default_value = True

    if ModelFlags.multipurpose_map_uses_og_xbox_channel_order in shader_model_flags:
        shader_model_node.inputs["Multipurpose Map Uses OG Xbox Channel Order"].default_value = True

    shader_model_node.inputs["Animation Color Lower Bound"].default_value = convert_to_blender_color(shader_data["animation color lower bound"], True)
    shader_model_node.inputs["Animation Color Upper Bound"].default_value = convert_to_blender_color(shader_data["animation color upper bound"], True)
    shader_model_node.inputs["Animation Color Bound Factor"].default_value = 0
    if not FunctionEnum.one.value == shader_data["animation function"]["value"]:
        shader_model_node.inputs["Animation Color Bound Factor"].default_value = 1

    shader_model_node.inputs["Detail Function Setting"].default_value = shader_data["detail function"]["value"]
    shader_model_node.inputs["Detail Mask Setting"].default_value = shader_data["detail mask"]["value"]

    shader_model_node.inputs["Perpendicular Brightness"].default_value = shader_data["perpendicular brightness"]
    shader_model_node.inputs["Perpendicular Tint Color"].default_value = convert_to_blender_color(shader_data["perpendicular tint color"], True)
    shader_model_node.inputs["Parallel Brightness"].default_value = shader_data["parallel brightness"]
    shader_model_node.inputs["Parallel Tint Color"].default_value = convert_to_blender_color(shader_data["parallel tint color"], True)

    if base_bitmap is not None and base_map_node is not None:
        ignore_alpha_bitmap = base_bitmap["Data"]["encoding format"]["value"] is FormatEnum.compressed_with_color_key_transparency.value
        ignore_alpha_shader = ModelFlags.not_alpha_tested in shader_model_flags
        is_blended_decal = ModelFlags.alpha_blended_decal in shader_model_flags
        if ignore_alpha_bitmap or (ignore_alpha_shader and not is_blended_decal):
            base_map_node.image.alpha_mode = 'NONE'
        else:
            if bpy.app.version <= (4, 2, 0):
                mat.shadow_method = 'CLIP'
            mat.blend_method = 'HASHED'