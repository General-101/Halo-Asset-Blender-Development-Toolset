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

from ... import config
from mathutils import Vector
from ...file_tag.h1.file_shader_model.format import ModelFlags, DetailFumctionEnum, DetailMaskEnum, FunctionEnum
from ...file_tag.h1.file_bitmap.format import FormatEnum
from .shader_helper import (
    get_bitmap, 
    get_output_material_node, 
    connect_inputs, 
    generate_image_node,
    HALO_1_SHADER_RESOURCES
    )

def get_shader_model_node(tree):
    if not bpy.data.node_groups.get("shader_model"):
        with bpy.data.libraries.load(HALO_1_SHADER_RESOURCES) as (data_from, data_to):
            data_to.node_groups.append(data_from.node_groups[data_from.node_groups.index('shader_model')])

    shader_model_node = tree.nodes.new('ShaderNodeGroup')
    shader_model_node.node_tree = bpy.data.node_groups.get("shader_model")

    return shader_model_node

def set_diffuse_scale(shader, mat, base_node, multipurpose_node):
    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-1775, 250))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", base_node, "Vector")
    connect_inputs(mat.node_tree, vect_math_node, "Vector", multipurpose_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-1950, 275))
    combine_xyz_node.location = Vector((-1950, 150))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    map_u_scale = shader.shader_body.map_u_scale
    if shader.shader_body.map_u_scale == 0.0:
        map_u_scale = 1.0

    map_v_scale = shader.shader_body.map_v_scale
    if shader.shader_body.map_v_scale == 0.0:
        map_v_scale = 1.0

    combine_xyz_node.inputs[0].default_value = map_u_scale
    combine_xyz_node.inputs[1].default_value = map_v_scale
    combine_xyz_node.inputs[2].default_value = 1

def set_detail_scale(shader, mat, detail_node):
    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-1775, -200))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", detail_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-1950, -175))
    combine_xyz_node.location = Vector((-1950, -300))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)
    detail_map_scale = shader.shader_body.detail_map_scale
    if shader.shader_body.detail_map_scale == 0.0:
        detail_map_scale = 1.0

    combine_xyz_node.inputs[0].default_value = detail_map_scale
    combine_xyz_node.inputs[1].default_value = detail_map_scale + shader.shader_body.detail_map_v_scale
    combine_xyz_node.inputs[2].default_value = 1

def set_micro_detail_scale(shader, mat, micro_detail_node, base_bitmap_count, micro_detail_bitmap_count, base_bitmap, micro_detail_bitmap, permutation_index, rescale_detail):
    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-1400.0, 200.0))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", micro_detail_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    uv_map_node.uv_map = "UVMap_0"
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-1600, 275))
    combine_xyz_node.location = Vector((-1600, 150))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.shader_body.micro_detail_map_scale
    if shader.shader_body.micro_detail_map_scale == 0.0:
        scale = 1.0

    micro_detail_rescale_i = scale
    micro_detail_rescale_j = scale
    if base_bitmap_count > 0 and micro_detail_bitmap_count > 0 and rescale_detail:
        if base_bitmap_count > permutation_index:
            base_element = base_bitmap.bitmaps[permutation_index]
        else:
            base_element = base_bitmap.bitmaps[0]
        if micro_detail_bitmap_count > permutation_index:
            micro_detail_element = micro_detail_bitmap.bitmaps[permutation_index]
        else:
            micro_detail_element = micro_detail_bitmap.bitmaps[0]

        micro_detail_rescale_i *= base_element.width / micro_detail_element.width
        micro_detail_rescale_j *= base_element.height / micro_detail_element.height

    combine_xyz_node.inputs[0].default_value = micro_detail_rescale_i
    combine_xyz_node.inputs[1].default_value = micro_detail_rescale_j
    combine_xyz_node.inputs[2].default_value = 1

def set_bump_scale(shader, mat, bump_node, base_bitmap_count, bump_bitmap_count, base_bitmap, bump_bitmap, permutation_index, rescale_bump_maps):
    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-1400.0, -100.0))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", bump_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    uv_map_node.uv_map = "UVMap_0"
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-1600, -25))
    combine_xyz_node.location = Vector((-1600, -150))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.shader_body.bump_map_scale
    if shader.shader_body.bump_map_scale == 0.0:
        scale = 1.0

    bump_rescale_i = scale
    bump_rescale_j = scale
    if base_bitmap_count > 0 and bump_bitmap_count > 0 and rescale_bump_maps:
        if base_bitmap_count > permutation_index:
            base_element = base_bitmap.bitmaps[permutation_index]
        else:
            base_element = base_bitmap.bitmaps[0]
        if bump_bitmap_count > permutation_index:
            bump_element = bump_bitmap.bitmaps[permutation_index]
        else:
            bump_element = bump_bitmap.bitmaps[0]

        bump_rescale_i *= base_element.width / bump_element.width
        bump_rescale_j *= base_element.height / bump_element.height

    combine_xyz_node.inputs[0].default_value = bump_rescale_i
    combine_xyz_node.inputs[1].default_value = bump_rescale_j
    combine_xyz_node.inputs[2].default_value = 1

def set_illum_scale(shader, mat, self_illumination_node):
    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-1400.0, -350.0))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", self_illumination_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    uv_map_node.uv_map = "UVMap_0"
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-1600, -325))
    combine_xyz_node.location = Vector((-1600, -450))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.shader_body.map_scale
    if shader.shader_body.map_scale == 0.0:
        scale = 1.0

    combine_xyz_node.inputs[0].default_value = scale
    combine_xyz_node.inputs[1].default_value = scale
    combine_xyz_node.inputs[2].default_value = 1

def generate_shader_model(mat, shader, report):
    mat.use_nodes = True

    texture_root = config.HALO_1_DATA_PATH
    base_map, base_map_name = get_bitmap(shader.shader_body.base_map, texture_root)
    multipurpose_map, multipurpose_map_name = get_bitmap(shader.shader_body.multipurpose_map, texture_root)
    detail_map, detail_map_name = get_bitmap(shader.shader_body.detail_map, texture_root)
    reflection_map, reflection_map_name = get_bitmap(shader.shader_body.reflection_cube_map, texture_root)

    base_bitmap = shader.shader_body.base_map.parse_tag(report, "halo1", "retail")
    multipurpose_bitmap = shader.shader_body.multipurpose_map.parse_tag(report, "halo1", "retail")
    detail_bitmap = shader.shader_body.detail_map.parse_tag(report, "halo1", "retail")
    reflection_bitmap = shader.shader_body.reflection_cube_map.parse_tag(report, "halo1", "retail")

    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))

    shader_model_node = get_shader_model_node(mat.node_tree)
    shader_model_node.location = Vector((-450.0, -20.0))
    shader_model_node.name = "Shader Model"
    shader_model_node.width = 400.0
    shader_model_node.height = 100.0

    connect_inputs(mat.node_tree, shader_model_node, "Shader", output_material_node, "Surface")

    base_node = generate_image_node(mat, base_map, base_bitmap, base_map_name)
    base_node.name = "Base Map"
    base_node.location = Vector((-1200, 1200))
    if not base_node.image == None:
        base_node.image.alpha_mode = 'CHANNEL_PACKED'

    multipurpose_node = generate_image_node(mat, multipurpose_map, multipurpose_bitmap, multipurpose_map_name)
    multipurpose_node.name = "Multipurpose Map"
    multipurpose_node.location = Vector((-1200, 900))
    multipurpose_node.interpolation = 'Cubic'
    if not multipurpose_node.image == None:
        multipurpose_node.image.alpha_mode = 'CHANNEL_PACKED'
        multipurpose_node.image.colorspace_settings.name = 'Non-Color'

    detail_node = generate_image_node(mat, detail_map, detail_bitmap, detail_map_name)
    detail_node.name = "Detail Map"
    detail_node.location = Vector((-1200, 600))
    if not detail_node.image == None:
        detail_node.image.alpha_mode = 'CHANNEL_PACKED'

    reflection_node = generate_image_node(mat, reflection_map, reflection_bitmap, reflection_map_name, True)
    reflection_node.name = "Reflection Map"
    reflection_node.location = Vector((-1200, -600))

    connect_inputs(mat.node_tree, base_node, "Color", shader_model_node, "Base Map")
    connect_inputs(mat.node_tree, base_node, "Alpha", shader_model_node, "Base Map Alpha")
    connect_inputs(mat.node_tree, multipurpose_node, "Color", shader_model_node, "Multipurpose Map")
    connect_inputs(mat.node_tree, multipurpose_node, "Alpha", shader_model_node, "Multipurpose Map Alpha")
    connect_inputs(mat.node_tree, detail_node, "Color", shader_model_node, "Detail Map")
    connect_inputs(mat.node_tree, detail_node, "Alpha", shader_model_node, "Detail Map Alpha")
    connect_inputs(mat.node_tree, reflection_node, "Color", shader_model_node, "Reflection Cube Map")

    texture_coordinate_node = mat.node_tree.nodes.new("ShaderNodeTexCoord")
    texture_coordinate_node.location = Vector((-1775.0, 750.0))
    connect_inputs(mat.node_tree, texture_coordinate_node, "Reflection", reflection_node, "Vector")

    set_diffuse_scale(shader, mat, base_node, multipurpose_node)
    set_detail_scale(shader, mat, detail_node)

    shader_model_node.inputs["Power"].default_value = shader.shader_body.power
    shader_model_node.inputs["Color of Emitted Light"].default_value = shader.shader_body.color_of_emitted_light

    shader_model_flags = ModelFlags(shader.shader_body.model_flags)

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

    shader_model_node.inputs["Animation Color Lower Bound"].default_value = shader.shader_body.self_illumination_animation_color_lower_bound
    shader_model_node.inputs["Animation Color Upper Bound"].default_value = shader.shader_body.self_illumination_animation_color_upper_bound
    shader_model_node.inputs["Animation Color Bound Factor"].default_value = 0
    if not FunctionEnum.one.value == shader.shader_body.self_illumination_animation_function:
        shader_model_node.inputs["Animation Color Bound Factor"].default_value = 1

    shader_model_node.inputs["Detail Function Setting"].default_value = shader.shader_body.detail_function
    shader_model_node.inputs["Detail Mask Setting"].default_value = shader.shader_body.detail_mask

    shader_model_node.inputs["Perpendicular Brightness"].default_value = shader.shader_body.perpendicular_brightness
    shader_model_node.inputs["Perpendicular Tint Color"].default_value = shader.shader_body.perpendicular_tint_color
    shader_model_node.inputs["Parallel Brightness"].default_value = shader.shader_body.parallel_brightness
    shader_model_node.inputs["Parallel Tint Color"].default_value = shader.shader_body.parallel_tint_color

    if base_bitmap:
        ignore_alpha_bitmap = base_bitmap.bitmap_body.format is FormatEnum.compressed_with_color_key_transparency.value
        ignore_alpha_shader = ModelFlags.not_alpha_tested in shader_model_flags
        is_blended_decal = ModelFlags.alpha_blended_decal in shader_model_flags
        if ignore_alpha_bitmap or (ignore_alpha_shader and not is_blended_decal):
            base_node.image.alpha_mode = 'NONE'
        else:
            mat.shadow_method = 'CLIP'
            mat.blend_method = 'HASHED'






