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
from ...file_tag.h1.file_shader_environment.format import EnvironmentTypeEnum, EnvironmentFlags, DiffuseFlags, ReflectionFlags, FunctionEnum
from .shader_helper import (
    get_bitmap, 
    get_output_material_node, 
    connect_inputs, 
    generate_image_node, 
    HALO_1_SHADER_RESOURCES
    )

def get_shader_environment_node(tree):
    if not bpy.data.node_groups.get("shader_environment"):
        with bpy.data.libraries.load(HALO_1_SHADER_RESOURCES) as (data_from, data_to):
            data_to.node_groups.append(data_from.node_groups[data_from.node_groups.index('shader_environment')])

    shader_environment_node = tree.nodes.new('ShaderNodeGroup')
    shader_environment_node.node_tree = bpy.data.node_groups.get("shader_environment")

    return shader_environment_node

def set_primary_detail_scale(shader, mat, primary_detail_node, base_bitmap_count, primary_detail_bitmap_count, base_bitmap, primary_detail_bitmap, permutation_index, rescale_detail):
    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-1400.0, 800.0))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", primary_detail_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-1600, 875))
    combine_xyz_node.location = Vector((-1600, 750))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.shader_body.primary_detail_map_scale
    if shader.shader_body.primary_detail_map_scale == 0.0:
        scale = 1.0

    primary_detail_rescale_i = scale
    primary_detail_rescale_j = scale
    if base_bitmap_count > 0 and primary_detail_bitmap_count > 0 and rescale_detail:
        if base_bitmap_count > permutation_index:
            base_element = base_bitmap.bitmaps[permutation_index]
        else:
            base_element = base_bitmap.bitmaps[0]

        if primary_detail_bitmap_count > permutation_index:
            primary_detail_element = primary_detail_bitmap.bitmaps[permutation_index]
        else:
            primary_detail_element = primary_detail_bitmap.bitmaps[0]

        primary_detail_rescale_i *= base_element.width / primary_detail_element.width
        primary_detail_rescale_j *= base_element.height / primary_detail_element.height

    combine_xyz_node.inputs[0].default_value = primary_detail_rescale_i
    combine_xyz_node.inputs[1].default_value = primary_detail_rescale_j
    combine_xyz_node.inputs[2].default_value = 1

def set_secondary_detail_scale(shader, mat, secondary_detail_node, base_bitmap_count, secondary_detail_bitmap_count, base_bitmap, secondary_detail_bitmap, permutation_index, rescale_detail):
    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-1400.0, 500.0))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", secondary_detail_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-1600, 575))
    combine_xyz_node.location = Vector((-1600, 450))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.shader_body.secondary_detail_map_scale
    if shader.shader_body.secondary_detail_map_scale == 0.0:
        scale = 1.0

    secondary_detail_rescale_i = scale
    secondary_detail_rescale_j = scale
    if base_bitmap_count > 0 and secondary_detail_bitmap_count > 0 and rescale_detail:
        if base_bitmap_count > permutation_index:
            base_element = base_bitmap.bitmaps[permutation_index]
        else:
            base_element = base_bitmap.bitmaps[0]
        if secondary_detail_bitmap_count > permutation_index:
            secondary_detail_element = secondary_detail_bitmap.bitmaps[permutation_index]
        else:
            secondary_detail_element = secondary_detail_bitmap.bitmaps[0]

        secondary_detail_rescale_i *= base_element.width / secondary_detail_element.width
        secondary_detail_rescale_j *= base_element.height / secondary_detail_element.height

    combine_xyz_node.inputs[0].default_value = secondary_detail_rescale_i
    combine_xyz_node.inputs[1].default_value = secondary_detail_rescale_j
    combine_xyz_node.inputs[2].default_value = 1

def set_micro_detail_scale(shader, mat, micro_detail_node, base_bitmap_count, micro_detail_bitmap_count, base_bitmap, micro_detail_bitmap, permutation_index, rescale_detail):
    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-1400.0, 200.0))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", micro_detail_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
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

def generate_shader_environment(mat, shader, permutation_index, report):
    mat.use_nodes = True

    texture_root = config.HALO_1_DATA_PATH
    base_map, base_map_name = get_bitmap(shader.shader_body.base_map, texture_root)
    primary_detail_map, primary_detail_map_name = get_bitmap(shader.shader_body.primary_detail_map, texture_root)
    secondary_detail_map, secondary_detail_map_name = get_bitmap(shader.shader_body.secondary_detail_map, texture_root)
    micro_detail_map, micro_detail_map_name = get_bitmap(shader.shader_body.micro_detail_map, texture_root)
    bump_map, bump_map_name = get_bitmap(shader.shader_body.bump_map, texture_root)
    illum_map, illum_map_name = get_bitmap(shader.shader_body.map, texture_root)
    reflection_map, reflection_map_name = get_bitmap(shader.shader_body.reflection_cube_map, texture_root)

    base_bitmap = shader.shader_body.base_map.parse_tag(report, "halo1", "retail")
    primary_detail_bitmap = shader.shader_body.primary_detail_map.parse_tag(report, "halo1", "retail")
    secondary_detail_bitmap = shader.shader_body.secondary_detail_map.parse_tag(report, "halo1", "retail")
    micro_detail_bitmap = shader.shader_body.micro_detail_map.parse_tag(report, "halo1", "retail")
    base_bitmap = shader.shader_body.base_map.parse_tag(report, "halo1", "retail")
    bump_bitmap = shader.shader_body.bump_map.parse_tag(report, "halo1", "retail")
    illum_bitmap = shader.shader_body.map.parse_tag(report, "halo1", "retail")
    reflection_bitmap = shader.shader_body.reflection_cube_map.parse_tag(report, "halo1", "retail")

    rescale_detail = DiffuseFlags.rescale_detail_maps in DiffuseFlags(shader.shader_body.diffuse_flags)
    rescale_bump_maps = DiffuseFlags.rescale_bump_maps in DiffuseFlags(shader.shader_body.diffuse_flags)

    base_bitmap_count = 0
    primary_detail_bitmap_count = 0
    secondary_detail_bitmap_count = 0
    micro_detail_bitmap_count = 0
    bump_bitmap_count = 0
    if base_bitmap:
        base_bitmap_count = len(base_bitmap.bitmaps)
    if primary_detail_bitmap:
        primary_detail_bitmap_count = len(primary_detail_bitmap.bitmaps)
    if secondary_detail_bitmap:
        secondary_detail_bitmap_count = len(secondary_detail_bitmap.bitmaps)
    if micro_detail_bitmap:
        micro_detail_bitmap_count = len(micro_detail_bitmap.bitmaps)
    if bump_bitmap:
        bump_bitmap_count = len(bump_bitmap.bitmaps)

    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))

    shader_environment_node = get_shader_environment_node(mat.node_tree)
    shader_environment_node.location = Vector((-450.0, -20.0))
    shader_environment_node.name = "Shader Environment"
    shader_environment_node.width = 400.0
    shader_environment_node.height = 100.0

    connect_inputs(mat.node_tree, shader_environment_node, "Shader", output_material_node, "Surface")

    base_node = generate_image_node(mat, base_map, base_bitmap, base_map_name)
    base_node.name = "Base Map"
    base_node.location = Vector((-1200, 1200))
    if not base_node.image == None:
        base_node.image.alpha_mode = 'CHANNEL_PACKED'

    primary_detail_node = generate_image_node(mat, primary_detail_map, primary_detail_bitmap, primary_detail_map_name)
    primary_detail_node.name = "Primary Detail Map"
    primary_detail_node.location = Vector((-1200, 900))
    if not primary_detail_node.image == None:
        primary_detail_node.image.alpha_mode = 'CHANNEL_PACKED'

    secondary_detail_node = generate_image_node(mat, secondary_detail_map, secondary_detail_bitmap, secondary_detail_map_name)
    secondary_detail_node.name = "Secondary Detail Map"
    secondary_detail_node.location = Vector((-1200, 600))
    if not secondary_detail_node.image == None:
        secondary_detail_node.image.alpha_mode = 'CHANNEL_PACKED'

    micro_detail_node = generate_image_node(mat, micro_detail_map, micro_detail_bitmap, micro_detail_map_name)
    micro_detail_node.name = "Micro Detail Map"
    micro_detail_node.location = Vector((-1200, 300))
    if not micro_detail_node.image == None:
        micro_detail_node.image.alpha_mode = 'CHANNEL_PACKED'

    bump_node = generate_image_node(mat, bump_map, bump_bitmap, bump_map_name)
    bump_node.name = "Bump Map"
    bump_node.location = Vector((-1200, 0))
    bump_node.interpolation = 'Cubic'
    if not bump_node.image == None:
        bump_node.image.colorspace_settings.name = 'Non-Color'

    self_illumination_node = generate_image_node(mat, illum_map, illum_bitmap, illum_map_name)
    self_illumination_node.name = "Self-Illumination Map"
    self_illumination_node.location = Vector((-1200, -300))

    reflection_node = generate_image_node(mat, reflection_map, reflection_bitmap, reflection_map_name, True)
    reflection_node.name = "Reflection Map"
    reflection_node.location = Vector((-1200, -600))

    connect_inputs(mat.node_tree, base_node, "Color", shader_environment_node, "Base Map")
    connect_inputs(mat.node_tree, base_node, "Alpha", shader_environment_node, "Base Map Alpha")
    connect_inputs(mat.node_tree, primary_detail_node, "Color", shader_environment_node, "Primary Detail Map")
    connect_inputs(mat.node_tree, primary_detail_node, "Alpha", shader_environment_node, "Primary Detail Map Alpha")
    connect_inputs(mat.node_tree, secondary_detail_node, "Color", shader_environment_node, "Secondary Detail Map")
    connect_inputs(mat.node_tree, secondary_detail_node, "Alpha", shader_environment_node, "Secondary Detail Map Alpha")
    connect_inputs(mat.node_tree, micro_detail_node, "Color", shader_environment_node, "Micro Detail Map")
    connect_inputs(mat.node_tree, micro_detail_node, "Alpha", shader_environment_node, "Micro Detail Map Alpha")
    connect_inputs(mat.node_tree, bump_node, "Color", shader_environment_node, "Bump Map")
    connect_inputs(mat.node_tree, bump_node, "Alpha", shader_environment_node, "Bump Map Alpha")
    connect_inputs(mat.node_tree, self_illumination_node, "Color", shader_environment_node, "Self-Illumination Map")
    connect_inputs(mat.node_tree, reflection_node, "Color", shader_environment_node, "Reflection Cube Map")

    set_primary_detail_scale(shader, mat, primary_detail_node, base_bitmap_count, primary_detail_bitmap_count, base_bitmap, primary_detail_bitmap, permutation_index, rescale_detail)
    set_secondary_detail_scale(shader, mat, secondary_detail_node, base_bitmap_count, secondary_detail_bitmap_count, base_bitmap, secondary_detail_bitmap, permutation_index, rescale_detail)
    set_micro_detail_scale(shader, mat, micro_detail_node, base_bitmap_count, micro_detail_bitmap_count, base_bitmap, micro_detail_bitmap, permutation_index, rescale_detail)
    set_bump_scale(shader, mat, bump_node, base_bitmap_count, bump_bitmap_count, base_bitmap, bump_bitmap, permutation_index, rescale_bump_maps)
    set_illum_scale(shader, mat, self_illumination_node)

    shader_environment_node.inputs["Power"].default_value = shader.shader_body.power
    shader_environment_node.inputs["Color of Emitted Light"].default_value = shader.shader_body.color_of_emitted_light
    alpha_shader = EnvironmentFlags.alpha_tested in EnvironmentFlags(shader.shader_body.environment_flags)
    if alpha_shader:
        shader_environment_node.inputs["Alpha Tested"].default_value = True
        mat.shadow_method = 'CLIP'
        mat.blend_method = 'HASHED'

    mat.use_backface_culling = True
    shader_environment_node.inputs["Blend Type"].default_value = shader.shader_body.environment_type
    shader_environment_node.inputs["Detail Map Function"].default_value = shader.shader_body.detail_map_function
    shader_environment_node.inputs["Micro Detail Map Function"].default_value = shader.shader_body.micro_detail_map_function

    if bump_bitmap:
        shader_environment_node.inputs["Bump Strength"].default_value = bump_bitmap.bitmap_body.bump_height * 15

    shader_environment_node.inputs["Primary On Color"].default_value = shader.shader_body.primary_on_color
    shader_environment_node.inputs["Primary Off Color"].default_value = shader.shader_body.primary_off_color
    shader_environment_node.inputs["Primary Self-Illumination Activation Level"].default_value = 0
    if not FunctionEnum.one.value == shader.shader_body.primary_animation_function:
        shader_environment_node.inputs["Primary Self-Illumination Activation Level"].default_value = 1

    shader_environment_node.inputs["Secondary On Color"].default_value = shader.shader_body.secondary_on_color
    shader_environment_node.inputs["Secondary Off Color"].default_value = shader.shader_body.secondary_off_color
    shader_environment_node.inputs["Secondary Self-Illumination Activation Level"].default_value = 0
    if not FunctionEnum.one.value == shader.shader_body.secondary_animation_function:
        shader_environment_node.inputs["Secondary Self-Illumination Activation Level"].default_value = 1

    shader_environment_node.inputs["Plasma On Color"].default_value = shader.shader_body.plasma_on_color
    shader_environment_node.inputs["Plasma Off Color"].default_value = shader.shader_body.plasma_off_color
    shader_environment_node.inputs["Plasma Self-Illumination Activation Level"].default_value = 0
    if not FunctionEnum.one.value == shader.shader_body.plasma_animation_function:
        shader_environment_node.inputs["Plasma Self-Illumination Activation Level"].default_value = 1

    shader_environment_node.inputs["Brightness"].default_value = shader.shader_body.brightness
    shader_environment_node.inputs["Perpendicular Color"].default_value = shader.shader_body.perpendicular_color
    shader_environment_node.inputs["Parallel Color"].default_value = shader.shader_body.parallel_color

    shader_environment_node.inputs["Perpendicular Brightness"].default_value = shader.shader_body.perpendicular_brightness
    shader_environment_node.inputs["Parallel Brightness"].default_value = shader.shader_body.parallel_brightness
