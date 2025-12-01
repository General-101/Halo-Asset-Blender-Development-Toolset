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

from mathutils import Vector
from math import radians
from enum import Flag, Enum, auto
from ...file_tag.tag_interface import tag_interface, tag_common
from ..shader_generation.shader_helper import (
    place_node,
    connect_inputs, 
    get_linked_node, 
    set_image_scale, 
    get_shader_node,
    generate_image_node, 
    convert_to_blender_color,
    get_output_material_node, 
    HALO_1_SHADER_RESOURCES
    )

class ShaderFlags(Flag):
    simple_parameterization = auto()
    ignore_normals = auto()
    transparent_lit = auto()

class EnvironmentPropertiesFlags(Flag):
    alpha_tested = auto()
    bump_map_is_specular_mask = auto()
    true_atmospheric_fog = auto()
    use_alternate_bump_attenuation = auto()

class DiffuseFlags(Flag):
    rescale_detail_maps = auto()
    rescale_bump_map = auto()

class EnvironmentSelfIlluminationFlags(Flag):
    unfiltered = auto()

class SpecularFlags(Flag):
    overbright = auto()
    extra_shiny = auto()
    lightmap_is_specular = auto()

class ReflectionFlags(Flag):
    dynamic_mirror = auto()

    simple_parameterization = auto()
    ignore_normals = auto()
    transparent_lit = auto()

class ModelPropertiesFlags(Flag):
    detail_after_reflection = auto()
    two_sided = auto()
    not_alpha_tested = auto()
    alpha_blended_decal = auto()
    true_atmospheric_fog = auto()
    disable_two_sided_culling = auto()
    use_xbox_multipurpose_channel_order = auto()

class ModelSelfIlluminationFlags(Flag):
    no_random_phase = auto()

class ShaderTransparentPropertiesFlags(Flag):
    alpha_tested = auto()
    decal = auto()
    two_sided = auto()
    first_map_is_in_screenspace = auto()
    draw_before_water = auto()
    ignore_effect = auto()
    scale_first_map_with_distance = auto()
    numeric = auto()

class ChicagoMapFlags(Flag):
    unfiltered = auto()
    alpha_replicate = auto()
    u_clamped = auto()
    v_clamped = auto()

class ExtraFlags(Flag):
    dont_fade_active_camouflage = auto()
    numeric_countdown_timer = auto()
    custom_edition_blending = auto()

class GlassPropertiesFlags(Flag):
    alpha_tested = auto()
    decal = auto()
    two_sided = auto()
    bump_map_is_specular_mask = auto()

class MeterPropertiesFlags(Flag):
    decal = auto()
    two_sided = auto()
    flash_color_is_negative = auto()
    tint_mode_2 = auto()
    unfiltered = auto()

class WaterPropertiesFlags(Flag):
    base_map_alpha_modulates_reflection = auto()
    base_map_color_modulates_background = auto()
    atmospheric_fog = auto()
    draw_before_fog = auto()

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

class FramebufferBlendFunctionEnum(Enum):
    alpha_blend = 0
    multiply = auto()
    double_multiply = auto()
    add = auto()
    subtract = auto()
    component_min = auto()
    component_max = auto()
    alpha_multiply_add = auto()

class MapFlags(Flag):
    unfiltered = auto()
    u_clamped = auto()
    v_clamped = auto()

class StageFlags(Flag):
    color_mux = auto()
    alpha_mux = auto()
    a_out_controls_color0_animation = auto()

class InputEnum(Enum):
    zero = 0
    one = auto()
    one_half = auto()
    negative_one = auto()
    negative_one_half = auto()
    map_color_0 = auto()
    map_color_1 = auto()
    map_color_2 = auto()
    map_color_3 = auto()
    vertex_color_0_diffuse_light = auto()
    vertex_color_1_fade_perpendicular = auto()
    scratch_color_0 = auto()
    scratch_color_1 = auto()
    constant_color_0 = auto()
    constant_color_1 = auto()
    map_alpha_0 = auto()
    map_alpha_1 = auto()
    map_alpha_2 = auto()
    map_alpha_3 = auto()
    vertex_alpha_0_fade_none = auto()
    vertex_alpha_1_fade_perpendicular = auto()
    scratch_alpha_0 = auto()
    scratch_alpha_1 = auto()
    constant_alpha_0 = auto()
    constant_alpha_1 = auto()

class InputMappingEnum(Enum):
    clamp_x = 0
    _1_clamp_x = auto()
    _2 = auto()
    _1_2 = auto()
    clamp_x_1_2 = auto()
    _1_2_clamp_x = auto()
    x = auto()
    x_1 = auto()

class InputAlphaEnum(Enum):
    zero = 0
    one = auto()
    one_half = auto()
    negative_one = auto()
    negative_one_half = auto()
    map_alpha_0 = auto()
    map_alpha_1 = auto()
    map_alpha_2 = auto()
    map_alpha_3 = auto()
    vertex_alpha_0_fade_none = auto()
    vertex_alpha_1_fade_perpendicular = auto()
    scratch_alpha_0 = auto()
    scratch_alpha_1 = auto()
    constant_alpha_0 = auto()
    constant_alpha_1 = auto()
    map_blue_0 = auto()
    map_blue_1 = auto()
    map_blue_2 = auto()
    map_blue_3 = auto()
    vertex_blue_0_blue_light = auto()
    vertex_blue_1_fade_parallel = auto()
    scratch_blue_0 = auto()
    scratch_blue_1 = auto()
    constant_blue_0 = auto()
    constant_blue_1 = auto()

class OutputFunctionEnum(Enum):
    multiply = 0
    dot_product = auto()

class OutputABCDMaxSumEnum(Enum):
    discard = 0
    scratch_color_0_final_color = auto()
    scratch_color_1 = auto()
    vertex_color_0 = auto()
    vertex_color_1 = auto()
    map_color_0 = auto()
    map_color_1 = auto()
    map_color_2 = auto()
    map_color_3 = auto()

class OutputABCDMaxSumAlphaEnum(Enum):
    discard = 0
    scratch_alpha_0_final_alpha = auto()
    scratch_alpha_1 = auto()
    vertex_alpha_0 = auto()
    vertex_alpha_1 = auto()
    map_alpha_0 = auto()
    map_alpha_1 = auto()
    map_alpha_2 = auto()
    map_alpha_3 = auto()

class OutputMapping(Enum):
    color_identity = 0
    color_scale_by_1_2 = auto()
    color_scale_by_2 = auto()
    color_scale_by_4 = auto()
    color_bias_by_1_2 = auto()
    color_expand_normal = auto()

def set_stg_values(shad_root, stg_node):
    radiosity_flags = ShaderFlags(shad_root["flags"])
    stg_node.inputs["Simple Parameterization"].default_value = ShaderFlags.simple_parameterization in radiosity_flags
    stg_node.inputs["Ignore Normals"].default_value = ShaderFlags.ignore_normals in radiosity_flags
    stg_node.inputs["Transparent Lit"].default_value = ShaderFlags.transparent_lit in radiosity_flags
    stg_node.inputs["Detail Level"].default_value = shad_root["detail level"]["value"]
    stg_node.inputs["Power"].default_value = shad_root["power"]

    r0, g0, b0 = shad_root["color of emitted light"].values()
    r1, g1, b1 = shad_root["tint color"].values()
    stg_node.inputs["Color Of Emitted Light"].default_value = (r0, g0, b0, 1)
    stg_node.inputs["Tint Color"].default_value = (r1, g1, b1, 1)

    stg_node.inputs["Material Type"].default_value = shad_root["material type"]["value"]
    stg_node.inputs["Numeric Counter Limit"].default_value = shad_root["numeric counter limit"]

    shader_flags = ShaderTransparentPropertiesFlags(shad_root["flags_1"])
    stg_node.inputs["Alpha Tested"].default_value = ShaderTransparentPropertiesFlags.alpha_tested in shader_flags
    stg_node.inputs["Decal"].default_value = ShaderTransparentPropertiesFlags.decal in shader_flags
    stg_node.inputs["Two Sided"].default_value = ShaderTransparentPropertiesFlags.two_sided in shader_flags
    stg_node.inputs["First Map Is In Screenspace"].default_value = ShaderTransparentPropertiesFlags.first_map_is_in_screenspace in shader_flags
    stg_node.inputs["Draw Before Water"].default_value = ShaderTransparentPropertiesFlags.draw_before_water in shader_flags
    stg_node.inputs["Ignore Effect"].default_value = ShaderTransparentPropertiesFlags.ignore_effect in shader_flags
    stg_node.inputs["Scale First Map With Distance"].default_value = ShaderTransparentPropertiesFlags.scale_first_map_with_distance in shader_flags
    stg_node.inputs["Numeric"].default_value = ShaderTransparentPropertiesFlags.numeric in shader_flags

    stg_node.inputs["First Map Type"].default_value = shad_root["first map type"]["value"]
    stg_node.inputs["Framebuffer Blend Function"].default_value = shad_root["framebuffer blend function"]["value"]
    stg_node.inputs["Framebuffer Fade Mode"].default_value = shad_root["framebuffer fade mode"]["value"]
    stg_node.inputs["Framebuffer Fade Source"].default_value = shad_root["framebuffer fade source"]["value"]

    stg_node.inputs["Lens Flare Spacing"].default_value = shad_root["lens flare spacing"]

    map_keys = ["A", "B", "C", "D"]
    for map_idx, map_element in enumerate(shad_root["maps"]):
        map_key = map_keys[map_idx]
        stg_node.inputs["Map %s" % map_key].default_value = True

        map_flags = MapFlags(map_element["flags"])
        stg_node.inputs["Map %s Unfiltered" % map_key].default_value = MapFlags.unfiltered in map_flags
        stg_node.inputs["Map %s U Clamped" % map_key].default_value = MapFlags.u_clamped in map_flags
        stg_node.inputs["Map %s V Clamped" % map_key].default_value = MapFlags.v_clamped in map_flags

        stg_node.inputs["Map %s U Scale" % map_key].default_value = map_element["map u scale"]
        stg_node.inputs["Map %s V Scale" % map_key].default_value = map_element["map v scale"]
        stg_node.inputs["Map %s U Offset" % map_key].default_value = map_element["map u offset"]
        stg_node.inputs["Map %s V Offset" % map_key].default_value = map_element["map v offset"]
        stg_node.inputs["Map %s Rotation" % map_key].default_value = map_element["map rotation"]
        stg_node.inputs["Map %s Mipmap Bias" % map_key].default_value = map_element["mipmap bias"]

        stg_node.inputs["Map %s U Animation Source" % map_key].default_value = map_element["u animation source"]["value"]
        stg_node.inputs["Map %s U Animation Function" % map_key].default_value = map_element["u animation function"]["value"]
        stg_node.inputs["Map %s U Animation Period" % map_key].default_value = map_element["u animation period"]
        stg_node.inputs["Map %s U Animation Phase" % map_key].default_value = map_element["u animation phase"]
        stg_node.inputs["Map %s U Animation Scale" % map_key].default_value = map_element["u animation scale"]

        stg_node.inputs["Map %s V Animation Source" % map_key].default_value = map_element["v animation source"]["value"]
        stg_node.inputs["Map %s V Animation Function" % map_key].default_value = map_element["v animation function"]["value"]
        stg_node.inputs["Map %s V Animation Period" % map_key].default_value = map_element["v animation period"]
        stg_node.inputs["Map %s V Animation Phase" % map_key].default_value = map_element["v animation phase"]
        stg_node.inputs["Map %s V Animation Scale" % map_key].default_value = map_element["v animation scale"]

        stg_node.inputs["Map %s Rotation Animation Source" % map_key].default_value = map_element["rotation animation source"]["value"]
        stg_node.inputs["Map %s Rotation Animation Function" % map_key].default_value = map_element["rotation animation function"]["value"]
        stg_node.inputs["Map %s Rotation Animation Period" % map_key].default_value = map_element["rotation animation period"]
        stg_node.inputs["Map %s Rotation Animation Phase" % map_key].default_value = map_element["rotation animation phase"]
        stg_node.inputs["Map %s Rotation Animation Scale" % map_key].default_value = map_element["rotation animation scale"]

        stg_node.inputs["Map %s Rotation Animation Center" % map_key].default_value = map_element["rotation animation center"]

    for stage_idx, stage_element in enumerate(shad_root["stages"]):
        stg_node.inputs["Stage %s" % stage_idx].default_value = True

        stage_flags = StageFlags(stage_element["flags"])
        stg_node.inputs["Stage %s Color Mux" % stage_idx].default_value = StageFlags.color_mux in stage_flags
        stg_node.inputs["Stage %s Alpha Mux" % stage_idx].default_value = StageFlags.alpha_mux in stage_flags
        stg_node.inputs["Stage %s A Out Controls Color 0 Animation" % stage_idx].default_value = StageFlags.a_out_controls_color0_animation in stage_flags

        stg_node.inputs["Stage %s Color 0 Source" % stage_idx].default_value = stage_element["color0 source"]["value"]
        stg_node.inputs["Stage %s Color 0 Animation Function" % stage_idx].default_value = stage_element["color0 animation function"]["value"]
        stg_node.inputs["Stage %s Color 0 Animation Period" % stage_idx].default_value = stage_element["color0 animation period"]

        r0, g0, b0, a0  = convert_to_blender_color(stage_element["color0 animation lower bound"], True)
        r1, g1, b1, a1  = convert_to_blender_color(stage_element["color0 animation upper bound"], True)
        r2, g2, b2, a2 = convert_to_blender_color(stage_element["color1"], True)
        stg_node.inputs["Stage %s Color 0 Animation Lower Bound" % stage_idx].default_value = (r0, g0, b0, 1)
        stg_node.inputs["Stage %s Color 0 Animation Lower Bound Alpha" % stage_idx].default_value = a0
        stg_node.inputs["Stage %s Color 0 Animation Upper Bound" % stage_idx].default_value = (r1, g1, b1, 1)
        stg_node.inputs["Stage %s Color 0 Animation Upper Bound Alpha" % stage_idx].default_value = a1
        stg_node.inputs["Stage %s Color 1" % stage_idx].default_value = (r2, g2, b2, 1)
        stg_node.inputs["Stage %s Color 1 Alpha" % stage_idx].default_value = a2

        stg_node.inputs["Stage %s Input A" % stage_idx].default_value = stage_element["input a"]["value"]
        stg_node.inputs["Stage %s Input A Mapping" % stage_idx].default_value = stage_element["input a mapping"]["value"]
        stg_node.inputs["Stage %s Input B" % stage_idx].default_value = stage_element["input b"]["value"]
        stg_node.inputs["Stage %s Input B Mapping" % stage_idx].default_value = stage_element["input b mapping"]["value"]
        stg_node.inputs["Stage %s Input C" % stage_idx].default_value = stage_element["input c"]["value"]
        stg_node.inputs["Stage %s Input C Mapping" % stage_idx].default_value = stage_element["input c mapping"]["value"]
        stg_node.inputs["Stage %s Input D" % stage_idx].default_value = stage_element["input d"]["value"]
        stg_node.inputs["Stage %s Input D Mapping" % stage_idx].default_value = stage_element["input d mapping"]["value"]

        stg_node.inputs["Stage %s Output Ab" % stage_idx].default_value = stage_element["output ab"]["value"]
        stg_node.inputs["Stage %s Output Ab Function" % stage_idx].default_value = stage_element["output ab function"]["value"]
        stg_node.inputs["Stage %s Output Cd" % stage_idx].default_value = stage_element["output bc"]["value"]
        stg_node.inputs["Stage %s Output Cd Function" % stage_idx].default_value = stage_element["output cd function"]["value"]
        stg_node.inputs["Stage %s Output Ab Cd Mux Sum" % stage_idx].default_value = stage_element["output ab cd mux sum"]["value"]
        stg_node.inputs["Stage %s Output Mapping Color" % stage_idx].default_value = stage_element["output mapping color"]["value"]

        stg_node.inputs["Stage %s Input A Alpha" % stage_idx].default_value = stage_element["input a alpha"]["value"]
        stg_node.inputs["Stage %s Input A Mapping Alpha" % stage_idx].default_value = stage_element["input a mapping alpha"]["value"]
        stg_node.inputs["Stage %s Input B Alpha" % stage_idx].default_value = stage_element["input b alpha"]["value"]
        stg_node.inputs["Stage %s Input B Mapping Alpha" % stage_idx].default_value = stage_element["input b mapping alpha"]["value"]
        stg_node.inputs["Stage %s Input C Alpha" % stage_idx].default_value = stage_element["input c alpha"]["value"]
        stg_node.inputs["Stage %s Input C Mapping Alpha" % stage_idx].default_value = stage_element["input c mapping alpha"]["value"]
        stg_node.inputs["Stage %s Input D Alpha" % stage_idx].default_value = stage_element["input d alpha"]["value"]
        stg_node.inputs["Stage %s Input D Mapping Alpha" % stage_idx].default_value = stage_element["input d mapping alpha"]["value"]

        stg_node.inputs["Stage %s Output Ab Alpha" % stage_idx].default_value = stage_element["output ab alpha"]["value"]
        stg_node.inputs["Stage %s Output Cd Alpha" % stage_idx].default_value = stage_element["output cd alpha"]["value"]
        stg_node.inputs["Stage %s Output Ab Cd Mux Sum Alpha" % stage_idx].default_value = stage_element["output ab cd mux sum alpha"]["value"]
        stg_node.inputs["Stage %s Output Mapping Alpha" % stage_idx].default_value = stage_element["output mapping alpha"]["value"]

def get_field_input_instructions(node_tree, field_value, stg_paths, stg_node, stg_idx, input_node=None, input_key=None, is_alpha=False):
    if is_alpha:
        scratch_color = (0, 0, 0, 1)
        scratch_alpha = 0.0
        vertex_color = (1, 1, 1, 1)
        vertex_alpha = 0.0
        field_enum = InputAlphaEnum(field_value)

        if field_enum == InputAlphaEnum.zero:
            input_node.inputs[input_key].default_value = 0.0
        elif field_enum == InputAlphaEnum.one:
            input_node.inputs[input_key].default_value = 1.0
        elif field_enum == InputAlphaEnum.one_half:
            input_node.inputs[input_key].default_value = 0.5
        elif field_enum == InputAlphaEnum.negative_one:
            input_node.inputs[input_key].default_value = 1.0
        elif field_enum == InputAlphaEnum.negative_one_half:
            input_node.inputs[input_key].default_value = 0.5
        elif field_enum == InputAlphaEnum.map_alpha_0:
            output_node, output_key = stg_paths["map_a_alpha"]
            connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputAlphaEnum.map_alpha_1:
            output_node, output_key = stg_paths["map_b_alpha"]
            connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputAlphaEnum.map_alpha_2:
            output_node, output_key = stg_paths["map_c_alpha"]
            connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputAlphaEnum.map_alpha_3:
            output_node, output_key = stg_paths["map_d_alpha"]
            connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputAlphaEnum.vertex_alpha_0_fade_none:
            scratch_node = stg_paths["vertex_0_alpha"]
            if scratch_node is None:
                input_node.inputs[input_key].default_value = vertex_alpha
            else:
                output_node, output_key = stg_paths["vertex_0_alpha"]
                connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputAlphaEnum.vertex_alpha_1_fade_perpendicular:
            scratch_node = stg_paths["vertex_1_alpha"]
            if scratch_node is None:
                input_node.inputs[input_key].default_value = vertex_alpha
            else:
                output_node, output_key = stg_paths["vertex_1_alpha"]
                connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputAlphaEnum.scratch_alpha_0:
            scratch_node = stg_paths["scratch_0_alpha"]
            if scratch_node is None:
                input_node.inputs[input_key].default_value = scratch_alpha
            else:
                output_node, output_key = stg_paths["scratch_0_alpha"]
                connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputAlphaEnum.scratch_alpha_1:
            scratch_node = stg_paths["scratch_1_alpha"]
            if scratch_node is None:
                input_node.inputs[input_key].default_value = scratch_alpha
            else:
                output_node, output_key = stg_paths["scratch_1_alpha"]
                connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputAlphaEnum.constant_alpha_0:
            connect_inputs(node_tree, stg_node, "Stage %s Color Alpha" % stg_idx, input_node, input_key)
        elif field_enum == InputAlphaEnum.constant_alpha_1:
            connect_inputs(node_tree, stg_node, "Stage %s Color 1 Alpha" % stg_idx, input_node, input_key)
        elif field_enum == InputAlphaEnum.map_blue_0:
            output_node, output_key = stg_paths["map_a_color"]
            seperate_node = node_tree.nodes.new("ShaderNodeSeparateColor")
            seperate_node.location = Vector(((-720.0 + (-900 * stg_idx)), 0.0))
            connect_inputs(node_tree, output_node, output_key, seperate_node, "Color")
            connect_inputs(node_tree, seperate_node, "Blue", input_node, input_key)
        elif field_enum == InputAlphaEnum.map_blue_1:
            output_node, output_key = stg_paths["map_b_color"]
            seperate_node = node_tree.nodes.new("ShaderNodeSeparateColor")
            seperate_node.location = Vector(((-720.0 + (-900 * stg_idx)), -180.0))
            connect_inputs(node_tree, output_node, output_key, seperate_node, "Color")
            connect_inputs(node_tree, seperate_node, "Blue", input_node, input_key)
        elif field_enum == InputAlphaEnum.map_blue_2:
            output_node, output_key = stg_paths["map_c_color"]
            seperate_node = node_tree.nodes.new("ShaderNodeSeparateColor")
            seperate_node.location = Vector(((-720.0 + (-900 * stg_idx)), -360.0))
            connect_inputs(node_tree, output_node, output_key, seperate_node, "Color")
            connect_inputs(node_tree, seperate_node, "Blue", input_node, input_key)
        elif field_enum == InputAlphaEnum.map_blue_3:
            output_node, output_key = stg_paths["map_d_color"]
            seperate_node = node_tree.nodes.new("ShaderNodeSeparateColor")
            seperate_node.location = Vector(((-720.0 + (-900 * stg_idx)), -540.0))
            connect_inputs(node_tree, output_node, output_key, seperate_node, "Color")
            connect_inputs(node_tree, seperate_node, "Blue", input_node, input_key)
        elif field_enum == InputAlphaEnum.vertex_blue_0_blue_light:
            scratch_node = stg_paths["vertex_0_color"]
            if scratch_node is None:
                input_node.inputs[input_key].default_value = vertex_alpha
            else:
                output_node, output_key = stg_paths["vertex_0_color"]
                seperate_node = node_tree.nodes.new("ShaderNodeSeparateColor")
                seperate_node.location = Vector((-180, 0.0)) + input_node.location
                connect_inputs(node_tree, output_node, output_key, seperate_node, "Color")
                connect_inputs(node_tree, seperate_node, "Blue", input_node, input_key)
        elif field_enum == InputAlphaEnum.vertex_blue_1_fade_parallel:
            scratch_node = stg_paths["vertex_1_color"]
            if scratch_node is None:
                input_node.inputs[input_key].default_value = vertex_alpha
            else:
                output_node, output_key = stg_paths["vertex_1_color"]
                seperate_node = node_tree.nodes.new("ShaderNodeSeparateColor")
                seperate_node.location = Vector((-180, 0.0)) + input_node.location
                connect_inputs(node_tree, output_node, output_key, seperate_node, "Color")
                connect_inputs(node_tree, seperate_node, "Blue", input_node, input_key)
        elif field_enum == InputAlphaEnum.scratch_blue_0:
            scratch_node = stg_paths["scratch_0_color"]
            if scratch_node is None:
                input_node.inputs[input_key].default_value = scratch_alpha
            else:
                output_node, output_key = stg_paths["scratch_0_color"]
                seperate_node = node_tree.nodes.new("ShaderNodeSeparateColor")
                seperate_node.location = Vector((-180, 0.0)) + input_node.location
                connect_inputs(node_tree, output_node, output_key, seperate_node, "Color")
                connect_inputs(node_tree, seperate_node, "Blue", input_node, input_key)
        elif field_enum == InputAlphaEnum.scratch_blue_1:
            scratch_node = stg_paths["scratch_1_color"]
            if scratch_node is None:
                input_node.inputs[input_key].default_value = scratch_alpha
            else:
                output_node, output_key = stg_paths["scratch_1_color"]
                seperate_node = node_tree.nodes.new("ShaderNodeSeparateColor")
                seperate_node.location = Vector((-180, 0.0)) + input_node.location
                connect_inputs(node_tree, output_node, output_key, seperate_node, "Color")
                connect_inputs(node_tree, seperate_node, "Blue", input_node, input_key)
        elif field_enum == InputAlphaEnum.constant_blue_0:
            seperate_node = node_tree.nodes.new("ShaderNodeSeparateColor")
            seperate_node.location = Vector((-180, 0.0)) + input_node.location
            connect_inputs(node_tree, stg_node, "Stage %s Color" % stg_idx, seperate_node, "Color")
            connect_inputs(node_tree, seperate_node, "Blue", input_node, input_key)
        elif field_enum == InputAlphaEnum.constant_blue_1:
            seperate_node = node_tree.nodes.new("ShaderNodeSeparateColor")
            seperate_node.location = Vector((-180, 0.0)) + input_node.location
            connect_inputs(node_tree, stg_node, "Stage %s Color 1" % stg_idx, seperate_node, "Color")
            connect_inputs(node_tree, seperate_node, "Blue", input_node, input_key)

    else:
        scratch_color = (0, 0, 0, 1)
        scratch_alpha = (0.0, 0.0, 0.0, 1.0)
        vertex_color = (1, 1, 1, 1)
        vertex_alpha = (0.0, 0.0, 0.0, 1.0)
        field_enum = InputEnum(field_value)

        if field_enum == InputEnum.zero:
            input_node.inputs[input_key].default_value = (0.0, 0.0, 0.0, 1.0)
        elif field_enum == InputEnum.one:
            input_node.inputs[input_key].default_value = (1.0, 1.0, 1.0, 1.0)
        elif field_enum == InputEnum.one_half:
            input_node.inputs[input_key].default_value = (0.5, 0.5, 0.5, 1.0)
        elif field_enum == InputEnum.negative_one:
            input_node.inputs[input_key].default_value = (1.0, 1.0, 1.0, 1.0)
        elif field_enum == InputEnum.negative_one_half:
             input_node.inputs[input_key].default_value = (0.5, 0.5, 0.5, 1.0)
        elif field_enum == InputEnum.map_color_0:
            output_node, output_key = stg_paths["map_a_color"]
            connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputEnum.map_color_1:
            output_node, output_key = stg_paths["map_b_color"]
            connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputEnum.map_color_2:
            output_node, output_key = stg_paths["map_c_color"]
            connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputEnum.map_color_3:
            output_node, output_key = stg_paths["map_d_color"]
            connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputEnum.vertex_color_0_diffuse_light:
            scratch_node = stg_paths["vertex_0_color"]
            if scratch_node is None:
                input_node.inputs[input_key].default_value = vertex_color
            else:
                output_node, output_key = stg_paths["vertex_0_color"]
                connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputEnum.vertex_color_1_fade_perpendicular:
            scratch_node = stg_paths["vertex_1_color"]
            if scratch_node is None:
                input_node.inputs[input_key].default_value = vertex_color
            else:
                output_node, output_key = stg_paths["vertex_1_color"]
                connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputEnum.scratch_color_0:
            scratch_node = stg_paths["scratch_0_color"]
            if scratch_node is None:
                input_node.inputs[input_key].default_value = scratch_color
            else:
                output_node, output_key = stg_paths["scratch_0_color"]
                connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputEnum.scratch_color_1:
            scratch_node = stg_paths["scratch_1_color"]
            if scratch_node is None:
                input_node.inputs[input_key].default_value = scratch_color
            else:
                output_node, output_key = stg_paths["scratch_1_color"]
                connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputEnum.constant_color_0:
            connect_inputs(node_tree, stg_node, "Stage %s Color" % stg_idx, input_node, input_key)
        elif field_enum == InputEnum.constant_color_1:
            connect_inputs(node_tree, stg_node, "Stage %s Color 1" % stg_idx, input_node, input_key)
        elif field_enum == InputEnum.map_alpha_0:
            output_node, output_key = stg_paths["map_a_alpha"]
            connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputEnum.map_alpha_1:
            output_node, output_key = stg_paths["map_b_alpha"]
            connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputEnum.map_alpha_2:
            output_node, output_key = stg_paths["map_c_alpha"]
            connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputEnum.map_alpha_3:
            output_node, output_key = stg_paths["map_d_alpha"]
            connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputEnum.vertex_alpha_0_fade_none:
            scratch_node = stg_paths["vertex_0_alpha"]
            if scratch_node is None:
                input_node.inputs[input_key].default_value = vertex_alpha
            else:
                output_node, output_key = stg_paths["vertex_0_alpha"]
                connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputEnum.vertex_alpha_1_fade_perpendicular:
            scratch_node = stg_paths["vertex_1_alpha"]
            if scratch_node is None:
                input_node.inputs[input_key].default_value = vertex_alpha
            else:
                output_node, output_key = stg_paths["vertex_1_alpha"]
                connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputEnum.scratch_alpha_0:
            scratch_node = stg_paths["scratch_0_alpha"]
            if scratch_node is None:
                input_node.inputs[input_key].default_value = scratch_alpha
            else:
                output_node, output_key = stg_paths["scratch_0_alpha"]
                connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputEnum.scratch_alpha_1:
            scratch_node = stg_paths["scratch_1_alpha"]
            if scratch_node is None:
                input_node.inputs[input_key].default_value = scratch_alpha
            else:
                output_node, output_key = stg_paths["scratch_1_alpha"]
                connect_inputs(node_tree, output_node, output_key, input_node, input_key)
        elif field_enum == InputEnum.constant_alpha_0:
            connect_inputs(node_tree, stg_node, "Stage %s Color Alpha" % stg_idx, input_node, input_key)
        elif field_enum == InputEnum.constant_alpha_1:
            connect_inputs(node_tree, stg_node, "Stage %s Color 1 Alpha" % stg_idx, input_node, input_key)

def get_field_output_instructions(field_value, stg_paths, input_node=None, input_key=None, is_alpha=False):
    if is_alpha:
        field_enum = OutputABCDMaxSumEnum(field_value)
        if field_enum == OutputABCDMaxSumEnum.scratch_color_0_final_color:
            stg_paths["scratch_0_alpha"] = [input_node, input_key]
        elif field_enum == OutputABCDMaxSumEnum.scratch_color_1:
            stg_paths["scratch_1_alpha"] = [input_node, input_key]
        elif field_enum == OutputABCDMaxSumEnum.vertex_color_0:
            stg_paths["vertex_0_alpha"] = [input_node, input_key]
        elif field_enum == OutputABCDMaxSumEnum.vertex_color_1:
            stg_paths["vertex_1_alpha"] = [input_node, input_key]
        elif field_enum == OutputABCDMaxSumEnum.map_color_0:
            stg_paths["map_a_alpha"] = [input_node, input_key]
        elif field_enum == OutputABCDMaxSumEnum.map_color_1:
            stg_paths["map_b_alpha"] = [input_node, input_key]
        elif field_enum == OutputABCDMaxSumEnum.map_color_2:
            stg_paths["map_c_alpha"] = [input_node, input_key]
        elif field_enum == OutputABCDMaxSumEnum.map_color_3:
            stg_paths["map_d_alpha"] = [input_node, input_key]
    else:
        field_enum = OutputABCDMaxSumAlphaEnum(field_value)
        if field_enum == OutputABCDMaxSumAlphaEnum.scratch_alpha_0_final_alpha:
            stg_paths["scratch_0_color"] = [input_node, input_key]
        elif field_enum == OutputABCDMaxSumAlphaEnum.scratch_alpha_1:
            stg_paths["scratch_1_color"] = [input_node, input_key]
        elif field_enum == OutputABCDMaxSumAlphaEnum.vertex_alpha_0:
            stg_paths["vertex_0_color"] = [input_node, input_key]
        elif field_enum == OutputABCDMaxSumAlphaEnum.vertex_alpha_1:
            stg_paths["vertex_1_color"] = [input_node, input_key]
        elif field_enum == OutputABCDMaxSumAlphaEnum.map_alpha_0:
            stg_paths["map_a_color"] = [input_node, input_key]
        elif field_enum == OutputABCDMaxSumAlphaEnum.map_alpha_1:
            stg_paths["map_b_color"] = [input_node, input_key]
        elif field_enum == OutputABCDMaxSumAlphaEnum.map_alpha_2:
            stg_paths["map_c_color"] = [input_node, input_key]
        elif field_enum == OutputABCDMaxSumAlphaEnum.map_alpha_3:
            stg_paths["map_d_color"] = [input_node, input_key]

def get_input_mapping_name(mapping_enum, is_alpha=False):
    omc_enum = InputMappingEnum(mapping_enum)
    if is_alpha:
        group_name = "Alpha Clamp(x)"
        if InputMappingEnum.clamp_x == omc_enum:
            group_name = "Alpha Clamp(x)"
        elif InputMappingEnum._1_clamp_x == omc_enum:
            group_name = "Alpha 1 - Clamp(x)"
        elif InputMappingEnum._2 == omc_enum:
            group_name = "Alpha 2*Clamp(x) - 1"
        elif InputMappingEnum._1_2 == omc_enum:
            group_name = "Alpha 1 - 2*Clamp(x)"
        elif InputMappingEnum.clamp_x_1_2 == omc_enum:
            group_name = "Alpha Clamp(x) - 1/2"
        elif InputMappingEnum._1_2_clamp_x == omc_enum:
            group_name = "Alpha 1/2 - Clamp(x)"
        elif InputMappingEnum.x == omc_enum:
            group_name = "Alpha x"
        elif InputMappingEnum.x_1 == omc_enum:
            group_name = "Alpha -x"

    else:
        group_name = "Color Clamp(x)"
        if InputMappingEnum.clamp_x == omc_enum:
            group_name = "Color Clamp(x)"
        elif InputMappingEnum._1_clamp_x == omc_enum:
            group_name = "Color 1 - Clamp(x)"
        elif InputMappingEnum._2 == omc_enum:
            group_name = "Color 2*Clamp(x) - 1"
        elif InputMappingEnum._1_2 == omc_enum:
            group_name = "Color 1 - 2*Clamp(x)"
        elif InputMappingEnum.clamp_x_1_2 == omc_enum:
            group_name = "Color Clamp(x) - 1/2"
        elif InputMappingEnum._1_2_clamp_x == omc_enum:
            group_name = "Color 1/2 - Clamp(x)"
        elif InputMappingEnum.x == omc_enum:
            group_name = "Color x"
        elif InputMappingEnum.x_1 == omc_enum:
            group_name = "Color -x"

    return group_name

def get_output_mapping_name(mapping_enum, is_alpha=False):
    omc_enum = OutputMapping(mapping_enum)
    if is_alpha:
        group_name = "Alpha Output Identity"
        if OutputMapping.color_identity == omc_enum:
            group_name = "Alpha Output Identity"
        elif OutputMapping.color_scale_by_1_2 == omc_enum:
            group_name = "Alpha Output Scale by 1/2"
        elif OutputMapping.color_scale_by_2 == omc_enum:
            group_name = "Alpha Output Scale by 2"
        elif OutputMapping.color_scale_by_4 == omc_enum:
            group_name = "Alpha Output Scale by 4"
        elif OutputMapping.color_bias_by_1_2 == omc_enum:
            group_name = "Alpha Output Bias by -1/2"
        elif OutputMapping.color_expand_normal == omc_enum:
            group_name = "Alpha Output Expand Normal"
        
    else:
        group_name = "Color Output Identity"
        if OutputMapping.color_identity == omc_enum:
            group_name = "Color Output Identity"
        elif OutputMapping.color_scale_by_1_2 == omc_enum:
            group_name = "Color Output Scale by 1/2"
        elif OutputMapping.color_scale_by_2 == omc_enum:
            group_name = "Color Output Scale by 2"
        elif OutputMapping.color_scale_by_4 == omc_enum:
            group_name = "Color Output Scale by 4"
        elif OutputMapping.color_bias_by_1_2 == omc_enum:
            group_name = "Color Output Bias by -1/2"
        elif OutputMapping.color_expand_normal == omc_enum:
            group_name = "Color Output Expand Normal"

    return group_name

def create_stages(node_tree, stage_element, offset=0):
    stage_offset = (4 * offset)
    stage_list = {}

    c_abcd_node = get_shader_node(node_tree, HALO_1_SHADER_RESOURCES, get_output_mapping_name(stage_element["output mapping color"]["value"]))
    c_abcd_node.name = "color_abcd_stage"
    c_abcd_node.location = Vector(((-900.0 + (-900 * offset)), 0.0))

    c_mix_abcd_node = None
    c_add_abcd_node = None
    stage_flags = StageFlags(stage_element["flags"])
    if StageFlags.color_mux in stage_flags:
        c_mix_abcd_node = get_shader_node(node_tree, HALO_1_SHADER_RESOURCES, "ABCD Mux")
        c_mix_abcd_node.name = "color_mix_abcd_stage"
        c_mix_abcd_node.location = Vector((-1080.0 + (-900 * offset), -280.0))
    else:
        c_add_abcd_node = node_tree.nodes.new(type="ShaderNodeMix")
        c_add_abcd_node.name = "color_add_abcd_stage"
        c_add_abcd_node.data_type = 'RGBA'
        c_add_abcd_node.blend_type = 'ADD'
        c_add_abcd_node.inputs[0].default_value = 1.0
        c_add_abcd_node.location = Vector((-1080.0 + (-900 * offset), 0.0))

    c_ab_node = get_shader_node(node_tree, HALO_1_SHADER_RESOURCES, "Output Function")
    c_ab_node.name = "color_ab_stage"
    if OutputFunctionEnum(stage_element["output ab function"]["value"]) == OutputFunctionEnum.dot_product:
        c_ab_node.inputs["Multiply/Dot Product"].default_value = True

    c_ab_node.location = Vector((-1260.0 + (-900 * offset), 0.0))

    c_cd_node = get_shader_node(node_tree, HALO_1_SHADER_RESOURCES, "Output Function")
    c_cd_node.name = "color_cd_stage"
    if OutputFunctionEnum(stage_element["output cd function"]["value"]) == OutputFunctionEnum.dot_product:
        c_cd_node.inputs["Multiply/Dot Product"].default_value = True

    c_cd_node.location = Vector((-1260.0 + (-900 * offset), -280.0))

    c_a_node = get_shader_node(node_tree, HALO_1_SHADER_RESOURCES, get_input_mapping_name(stage_element["input a mapping"]["value"]))
    c_a_node.name = "color_a_stage"
    c_a_node.location = Vector((-1440.0 + (-900 * offset), 0.0))

    c_b_node = get_shader_node(node_tree, HALO_1_SHADER_RESOURCES, get_input_mapping_name(stage_element["input b mapping"]["value"]))
    c_b_node.name = "color_b_stage"
    c_b_node.location = Vector((-1440.0 + (-900 * offset), -140.0))

    c_c_node = get_shader_node(node_tree, HALO_1_SHADER_RESOURCES, get_input_mapping_name(stage_element["input c mapping"]["value"]))
    c_c_node.name = "color_c_stage"
    c_c_node.location = Vector((-1440.0 + (-900 * offset), -280.0))

    c_d_node = get_shader_node(node_tree, HALO_1_SHADER_RESOURCES, get_input_mapping_name(stage_element["input d mapping"]["value"]))
    c_d_node.name = "color_d_stage"
    c_d_node.location = Vector((-1440.0 + (-900 * offset), -420.0))

    a_abcd_node = get_shader_node(node_tree, HALO_1_SHADER_RESOURCES, get_output_mapping_name(stage_element["output mapping alpha"]["value"], True))
    a_abcd_node.name = "alpha_abcd_stage"
    a_abcd_node.location = Vector((-900.0 + (-900 * offset), -720.0))

    a_mix_abcd_node = None
    a_add_abcd_node = None
    if StageFlags.alpha_mux in stage_flags:
        a_mix_abcd_node = get_shader_node(node_tree, HALO_1_SHADER_RESOURCES, "ABCD Mux")
        a_mix_abcd_node.name = "alpha_mix_abcd_stage"
        a_mix_abcd_node.location = Vector((-1080.0 + (-900 * offset), -1000.0))
    else:
        a_add_abcd_node = node_tree.nodes.new(type="ShaderNodeMath")
        a_add_abcd_node.name = "alpha_add_abcd_stage"
        a_add_abcd_node.location = Vector((-1080.0 + (-900 * offset), -720.0))

    a_ab_node = node_tree.nodes.new(type="ShaderNodeMath")
    a_ab_node.name = "alpha_ab_stage"
    a_ab_node.operation = 'MULTIPLY'
    a_ab_node.location = Vector((-1260.0 + (-900 * offset), -720.0))

    a_cd_node = node_tree.nodes.new(type="ShaderNodeMath")
    a_cd_node.name = "alpha_cd_stage"
    a_cd_node.operation = 'MULTIPLY'
    a_cd_node.location = Vector((-1260.0 + (-900 * offset), -1000.0))

    a_a_node = get_shader_node(node_tree, HALO_1_SHADER_RESOURCES, get_input_mapping_name(stage_element["input a mapping alpha"]["value"], True))
    a_a_node.name = "alpha_a_stage"
    a_a_node.location = Vector((-1440.0 + (-900 * offset), -720.0))

    a_b_node = get_shader_node(node_tree, HALO_1_SHADER_RESOURCES, get_input_mapping_name(stage_element["input b mapping alpha"]["value"], True))
    a_b_node.name = "alpha_b_stage"
    a_b_node.location = Vector((-1440.0 + (-900 * offset), -860.0))

    a_c_node = get_shader_node(node_tree, HALO_1_SHADER_RESOURCES, get_input_mapping_name(stage_element["input c mapping alpha"]["value"], True))
    a_c_node.name = "alpha_c_stage"
    a_c_node.location = Vector((-1440.0 + (-900 * offset), -1000.0))

    a_d_node = get_shader_node(node_tree, HALO_1_SHADER_RESOURCES, get_input_mapping_name(stage_element["input d mapping alpha"]["value"], True))
    a_d_node.name = "alpha_d_stage"
    a_d_node.location = Vector((-1440.0 + (-900 * offset), -1140.0))

    stage_list["c_abcd_node"] = c_abcd_node
    stage_list["c_add_abcd_node"] = c_add_abcd_node
    stage_list["c_mix_abcd_node"] = c_mix_abcd_node
    stage_list["c_ab_node"] = c_ab_node
    stage_list["c_cd_node"] = c_cd_node
    stage_list["c_a_node"] = c_a_node
    stage_list["c_b_node"] = c_b_node
    stage_list["c_c_node"] = c_c_node
    stage_list["c_d_node"] = c_d_node
    stage_list["a_abcd_node"] = a_abcd_node
    stage_list["a_add_abcd_node"] = a_add_abcd_node
    stage_list["a_mix_abcd_node"] = a_mix_abcd_node
    stage_list["a_ab_node"] = a_ab_node
    stage_list["a_cd_node"] = a_cd_node
    stage_list["a_a_node"] = a_a_node
    stage_list["a_b_node"] = a_b_node
    stage_list["a_c_node"] = a_c_node
    stage_list["a_d_node"] = a_d_node

    return stage_list

def generate_alpha_blend_output(shader_data, stg_node, node_tree, stg_paths, output_material_node):
    transparent_node = node_tree.nodes.new("ShaderNodeBsdfTransparent")
    diffuse_node = node_tree.nodes.new("ShaderNodeBsdfDiffuse")
    mix_node = node_tree.nodes.new("ShaderNodeMixShader")

    transparent_node.location = Vector((-540.0, 0.0))
    diffuse_node.location = Vector((-540.0, -140.0))
    mix_node.location = Vector((-360.0, 0.0))

    if stg_paths["scratch_0_color"] is None:
        diffuse_node.inputs["Color"].default_value = (0, 0, 0, 1)
    else:
        output_node, output_key = stg_paths["scratch_0_color"]
        connect_inputs(node_tree, output_node, output_key, diffuse_node, "Color")

    if stg_paths["scratch_0_alpha"] is None:
        mix_node.inputs["Fac"].default_value = 0.0
    else:
        output_node, output_key = stg_paths["scratch_0_alpha"]
        connect_inputs(node_tree, output_node, output_key, mix_node, "Fac")

    connect_inputs(node_tree, transparent_node, "BSDF", mix_node, 1)
    connect_inputs(node_tree, diffuse_node, "BSDF", mix_node, 2)

    if len(shader_data["stages"]) == 0:
        connect_inputs(node_tree, stg_node, "Map A", diffuse_node, "Color")

    return mix_node

def generate_add_blend_output(shader_data, stg_node, node_tree, stg_paths, output_material_node):
    emission_node = node_tree.nodes.new("ShaderNodeEmission")
    transparent_node = node_tree.nodes.new("ShaderNodeBsdfTransparent")
    add_node = node_tree.nodes.new("ShaderNodeAddShader")

    emission_node.location = Vector((-540.0, 0.0))
    transparent_node.location = Vector((-540.0, -140.0))
    add_node.location = Vector((-360.0, 0.0))

    if stg_paths["scratch_0_color"] is None:
        emission_node.inputs["Color"].default_value = (0, 0, 0, 1)
    else:
        output_node, output_key = stg_paths["scratch_0_color"]
        connect_inputs(node_tree, output_node, output_key, emission_node, "Color")

    connect_inputs(node_tree, emission_node, "Emission", add_node, 0)
    connect_inputs(node_tree, transparent_node, "BSDF", add_node, 1)

    if len(shader_data["stages"]) == 0:
        connect_inputs(node_tree, stg_node, "Map A", emission_node, "Color")

    return add_node

def get_scale(field_value):
    scale_value = 1.0
    if field_value == 0.0:
        scale_value = field_value
    return scale_value

def generate_texture_mapping(node_tree, stg_node, map_idx, input_node, input_key):
    mapping_node = node_tree.nodes.new("ShaderNodeMapping")
    uv_node = node_tree.nodes.new("ShaderNodeUVMap")
    texture_pan_node = get_shader_node(node_tree, HALO_1_SHADER_RESOURCES, "Halo Texture Pan")

    mapping_node.location = Vector((-180.0, 0.0)) + input_node.location
    uv_node.location = Vector((-360.0, 0.0)) + input_node.location
    texture_pan_node.location = Vector((-360.0, -140.0)) + input_node.location

    x_scale = get_scale(stg_node.inputs["Map %s U Scale" % map_idx].default_value)
    y_scale = get_scale(stg_node.inputs["Map %s V Scale" % map_idx].default_value)
    texture_pan_node.inputs["X Speed"].default_value = (stg_node.inputs["Map %s U Animation Period" % map_idx].default_value * x_scale)
    texture_pan_node.inputs["X Offset"].default_value = stg_node.inputs["Map %s U Offset" % map_idx].default_value
    texture_pan_node.inputs["X Scale"].default_value = x_scale
    texture_pan_node.inputs["Y Speed"].default_value = (stg_node.inputs["Map %s V Animation Period" % map_idx].default_value * y_scale)
    texture_pan_node.inputs["Y Offset"].default_value = stg_node.inputs["Map %s V Offset" % map_idx].default_value
    texture_pan_node.inputs["Y Scale"].default_value = y_scale

    connect_inputs(node_tree, uv_node, "UV", mapping_node, "Vector")
    connect_inputs(node_tree, texture_pan_node, "Vector", mapping_node, "Location")
    connect_inputs(node_tree, mapping_node, "Vector", input_node, input_key)

def generate_shader_environment_simple(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node)

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    place_node(bdsf_principled, 1)

    base_map_texture = generate_image_node(mat, shader_data["base map"], permutation_index, asset_cache, "halo1", report)
    if base_map_texture:
        base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        base_map_node.image = base_map_texture
        base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        place_node(base_map_node, 2)
        connect_inputs(mat.node_tree, base_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_environment(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    environment_flags = ShaderFlags(shader_data["flags"])
    environment_properties_flags = EnvironmentPropertiesFlags(shader_data["flags_1"])
    diffuse_flags = DiffuseFlags(shader_data["flags_2"])
    self_illumination_flags = EnvironmentSelfIlluminationFlags(shader_data["flags_3"])
    specular_flags = SpecularFlags(shader_data["flags_4"])
    reflection_flags = ReflectionFlags(shader_data["flags_5"])

    output_material_node = get_output_material_node(mat)
    output_material_node.location = (0.0, 0.0)

    shader_environment_node = get_shader_node(mat.node_tree, HALO_1_SHADER_RESOURCES, "shader_environment")
    shader_environment_node.location = (-440.0, 0.0)
    shader_environment_node.name = "Shader Environment"

    connect_inputs(mat.node_tree, shader_environment_node, "Shader", output_material_node, "Surface")

    shader_environment_node.inputs["Simple Parameterization"].default_value = ShaderFlags.simple_parameterization in environment_flags
    shader_environment_node.inputs["Ignore Normals"].default_value = ShaderFlags.ignore_normals in environment_flags
    shader_environment_node.inputs["Transparent Lit"].default_value = ShaderFlags.transparent_lit in environment_flags
    shader_environment_node.inputs["Detail Level"].default_value = shader_data["detail level"]["value"]
    shader_environment_node.inputs["Power"].default_value = shader_data["power"]
    shader_environment_node.inputs["Color Of Emitted Light"].default_value = convert_to_blender_color(shader_data["color of emitted light"], True)
    shader_environment_node.inputs["Tint Color"].default_value = convert_to_blender_color(shader_data["tint color"], True)

    shader_environment_node.inputs["Material Type"].default_value = shader_data["material type"]["value"]

    shader_environment_node.inputs["Alpha Tested"].default_value = EnvironmentPropertiesFlags.alpha_tested in environment_properties_flags
    shader_environment_node.inputs["Bump Map Is Specular Mask"].default_value = EnvironmentPropertiesFlags.bump_map_is_specular_mask in environment_properties_flags
    shader_environment_node.inputs["True Atmospheric Fog"].default_value = EnvironmentPropertiesFlags.true_atmospheric_fog in environment_properties_flags
    shader_environment_node.inputs["Use Alternate Bump Attenuation"].default_value = EnvironmentPropertiesFlags.use_alternate_bump_attenuation in environment_properties_flags

    shader_environment_node.inputs["Blend Type"].default_value = shader_data["shader environment type"]["value"]

    shader_environment_node.inputs["Lens Flare Spacing"].default_value = shader_data["lens flare spacing"]

    shader_environment_node.inputs["Rescale Detail Maps"].default_value = DiffuseFlags.rescale_detail_maps in diffuse_flags
    shader_environment_node.inputs["Rescale Bump Map"].default_value = DiffuseFlags.rescale_bump_map in diffuse_flags
    shader_environment_node.inputs["Detail Map Function"].default_value = shader_data["detail map function"]["value"]
    shader_environment_node.inputs["Primary Detail Map Scale"].default_value = shader_data["primary detail map scale"]
    shader_environment_node.inputs["Secondary Detail Map Scale"].default_value = shader_data["secondary detail map scale"]
    shader_environment_node.inputs["Micro Detail Map Function"].default_value = shader_data["micro detail map function"]["value"]
    shader_environment_node.inputs["Micro Detail Map Scale"].default_value = shader_data["micro detail map scale"]
    shader_environment_node.inputs["Material Color"].default_value = convert_to_blender_color(shader_data["material color"], True)

    shader_environment_node.inputs["Bump Map Scale"].default_value = shader_data["bump map scale"]

    shader_environment_node.inputs["U Animation Function"].default_value = shader_data["u animation function"]["value"]
    shader_environment_node.inputs["U Animation Period"].default_value = shader_data["u animation period"]
    shader_environment_node.inputs["U Animation Scale"].default_value = shader_data["u animation scale"]
    shader_environment_node.inputs["V Animation Function"].default_value = shader_data["v animation function"]["value"]
    shader_environment_node.inputs["V Animation Period"].default_value = shader_data["v animation period"]
    shader_environment_node.inputs["V Animation Scale"].default_value = shader_data["v animation scale"]

    shader_environment_node.inputs["Unfiltered"].default_value = EnvironmentSelfIlluminationFlags.unfiltered in self_illumination_flags
    shader_environment_node.inputs["Primary On Color"].default_value = convert_to_blender_color(shader_data["primary on color"], True)
    shader_environment_node.inputs["Primary Off Color"].default_value = convert_to_blender_color(shader_data["primary off color"], True)
    shader_environment_node.inputs["Primary Animation Function"].default_value = shader_data["primary animation function"]["value"]
    shader_environment_node.inputs["Primary Animation Period"].default_value = shader_data["primary animation period"]
    shader_environment_node.inputs["Primary Animation Phase"].default_value = shader_data["primary animation phase"]
    shader_environment_node.inputs["Secondary On Color"].default_value = convert_to_blender_color(shader_data["secondary on color"], True)
    shader_environment_node.inputs["Secondary Off Color"].default_value = convert_to_blender_color(shader_data["secondary off color"], True)
    shader_environment_node.inputs["Secondary Animation Function"].default_value = shader_data["secondary animation function"]["value"]
    shader_environment_node.inputs["Secondary Animation Period"].default_value = shader_data["secondary animation period"]
    shader_environment_node.inputs["Secondary Animation Phase"].default_value = shader_data["secondary animation phase"]
    shader_environment_node.inputs["Plasma On Color"].default_value = convert_to_blender_color(shader_data["plasma on color"], True)
    shader_environment_node.inputs["Plasma Off Color"].default_value = convert_to_blender_color(shader_data["plasma off color"], True)
    shader_environment_node.inputs["Plasma Animation Function"].default_value = shader_data["plasma animation function"]["value"]
    shader_environment_node.inputs["Plasma Animation Period"].default_value = shader_data["plasma animation period"]
    shader_environment_node.inputs["Plasma Animation Phase"].default_value = shader_data["plasma animation phase"]
    shader_environment_node.inputs["Self Illumination Map Scale"].default_value = shader_data["map scale"]
    if not FunctionEnum.one.value == shader_environment_node.inputs["Primary Animation Function"].default_value:
        shader_environment_node.inputs["Primary Self Illumination Activation Level"].default_value = 1

    if not FunctionEnum.one.value == shader_environment_node.inputs["Secondary Animation Function"].default_value:
        shader_environment_node.inputs["Secondary Self Illumination Activation Level"].default_value = 1

    if not FunctionEnum.one.value == shader_environment_node.inputs["Plasma Animation Function"].default_value:
        shader_environment_node.inputs["Plasma Self Illumination Activation Level"].default_value = 1

    shader_environment_node.inputs["Overbright"].default_value = SpecularFlags.overbright in specular_flags
    shader_environment_node.inputs["Extra Shiny"].default_value = SpecularFlags.extra_shiny in specular_flags
    shader_environment_node.inputs["Lightmap Is Specular"].default_value = SpecularFlags.lightmap_is_specular in specular_flags
    shader_environment_node.inputs["Brightness"].default_value = shader_data["brightness"]
    shader_environment_node.inputs["Perpendicular Color"].default_value = convert_to_blender_color(shader_data["perpendicular color"], True)
    shader_environment_node.inputs["Parallel Color"].default_value = convert_to_blender_color(shader_data["parallel color"], True)

    shader_environment_node.inputs["Dynamic Mirror"].default_value = ReflectionFlags.dynamic_mirror in reflection_flags
    shader_environment_node.inputs["Type"].default_value = shader_data["type_1"]["value"]
    shader_environment_node.inputs["Lightmap Brightness Scale"].default_value = shader_data["lightmap brightness scale"]
    shader_environment_node.inputs["Perpendicular Brightness"].default_value = shader_data["perpendicular brightness"]
    shader_environment_node.inputs["Parallel Brightness"].default_value = shader_data["parallel brightness"]

    base_map_texture = generate_image_node(mat, shader_data["base map"], permutation_index, asset_cache, "halo1", report)
    base_bitmap = tag_interface.get_disk_asset(shader_data["base map"]["path"], tag_common.h1_tag_groups.get(shader_data["base map"]["group name"]))
    if base_map_texture:
        base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        base_map_node.image = base_map_texture
        base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        base_map_node.location = (-720.0, 0.0)
        connect_inputs(mat.node_tree, base_map_node, "Color", shader_environment_node, "Base Map")
        connect_inputs(mat.node_tree, base_map_node, "Alpha", shader_environment_node, "Base Map Alpha")

    primary_detail_texture = generate_image_node(mat, shader_data["primary detail map"], permutation_index, asset_cache, "halo1", report)
    if primary_detail_texture:
        primary_detail_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        primary_detail_node.image = primary_detail_texture
        primary_detail_node.image.alpha_mode = 'CHANNEL_PACKED'
        primary_detail_node.location = (-720.0, -300.0)
        connect_inputs(mat.node_tree, primary_detail_node, "Color", shader_environment_node, "Primary Detail Map")
        connect_inputs(mat.node_tree, primary_detail_node, "Alpha", shader_environment_node, "Primary Detail Map Alpha")

        pdm_scale = shader_data["primary detail map scale"]
        if pdm_scale == 0.0:
            pdm_scale = 1.0

        pdm_image_scale = (pdm_scale, pdm_scale, pdm_scale)

        primary_detail_bitmap = tag_interface.get_disk_asset(shader_data["primary detail map"]["path"], tag_common.h1_tag_groups.get(shader_data["primary detail map"]["group name"]))
        set_image_scale(mat, primary_detail_node, pdm_image_scale, shader_environment_node.inputs["Rescale Detail Maps"].default_value, base_bitmap, primary_detail_bitmap, permutation_index)

    secondary_detail_texture = generate_image_node(mat, shader_data["secondary detail map"], permutation_index, asset_cache, "halo1", report)
    if secondary_detail_texture:
        secondary_detail_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        secondary_detail_node.image = secondary_detail_texture
        secondary_detail_node.image.alpha_mode = 'CHANNEL_PACKED'
        secondary_detail_node.location = (-720.0, -600.0)
        connect_inputs(mat.node_tree, secondary_detail_node, "Color", shader_environment_node, "Secondary Detail Map")
        connect_inputs(mat.node_tree, secondary_detail_node, "Alpha", shader_environment_node, "Secondary Detail Map Alpha")

        sdm_scale = shader_data["secondary detail map scale"]
        if sdm_scale == 0.0:
            sdm_scale = 1.0

        sdm_image_scale = (sdm_scale, sdm_scale, sdm_scale)

        secondary_detail_bitmap = tag_interface.get_disk_asset(shader_data["secondary detail map"]["path"], tag_common.h1_tag_groups.get(shader_data["secondary detail map"]["group name"]))
        set_image_scale(mat, secondary_detail_node, sdm_image_scale, shader_environment_node.inputs["Rescale Detail Maps"].default_value, base_bitmap, secondary_detail_bitmap, permutation_index)

    micro_detail_texture = generate_image_node(mat, shader_data["micro detail map"], permutation_index, asset_cache, "halo1", report)
    if micro_detail_texture:
        micro_detail_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        micro_detail_node.image = micro_detail_texture
        micro_detail_node.image.alpha_mode = 'CHANNEL_PACKED'
        micro_detail_node.location = (-720.0, -900.0)
        connect_inputs(mat.node_tree, micro_detail_node, "Color", shader_environment_node, "Micro Detail Map")
        connect_inputs(mat.node_tree, micro_detail_node, "Alpha", shader_environment_node, "Micro Detail Map Alpha")

        mdm_scale = shader_data["micro detail map scale"]
        if mdm_scale == 0.0:
            mdm_scale = 1.0

        mdm_image_scale = (mdm_scale, mdm_scale, mdm_scale)

        micro_detail_bitmap = tag_interface.get_disk_asset(shader_data["micro detail map"]["path"], tag_common.h1_tag_groups.get(shader_data["micro detail map"]["group name"]))
        set_image_scale(mat, micro_detail_node, mdm_image_scale, shader_environment_node.inputs["Rescale Detail Maps"].default_value, base_bitmap, micro_detail_bitmap, permutation_index)

    bump_texture = generate_image_node(mat, shader_data["bump map"], permutation_index, asset_cache, "halo1", report)
    if bump_texture:
        bump_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        bump_node.image = bump_texture
        bump_node.image.alpha_mode = 'CHANNEL_PACKED'
        bump_node.interpolation = 'Cubic'
        bump_node.image.colorspace_settings.name = 'Non-Color'
        bump_node.location = (-720.0, -1200.0)
        connect_inputs(mat.node_tree, bump_node, "Color", shader_environment_node, "Bump Map")
        connect_inputs(mat.node_tree, bump_node, "Alpha", shader_environment_node, "Bump Map Alpha")

        bm_scale = shader_data["bump map scale"]
        if bm_scale == 0.0:
            bm_scale = 1.0

        bm_image_scale = (bm_scale, bm_scale, bm_scale)

        bump_bitmap = tag_interface.get_disk_asset(shader_data["bump map"]["path"], tag_common.h1_tag_groups.get(shader_data["bump map"]["group name"]))
        set_image_scale(mat, bump_node, bm_image_scale, shader_environment_node.inputs["Rescale Bump Map"].default_value, base_bitmap, bump_bitmap, permutation_index)
        shader_environment_node.inputs["Bump Map Strength"].default_value = bump_bitmap["Data"]["bump height"] * 15

    self_illumination_texture = generate_image_node(mat, shader_data["map"], permutation_index, asset_cache, "halo1", report)
    if self_illumination_texture:
        self_illumination_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        self_illumination_node.image = self_illumination_texture
        self_illumination_node.location = (-720.0, -1500.0)
        connect_inputs(mat.node_tree, self_illumination_node, "Color", shader_environment_node, "Self Illumination Map")

        sim_scale = shader_data["map scale"]
        if sim_scale == 0.0:
            sim_scale = 1.0

        sim_image_scale = (sim_scale, sim_scale, sim_scale)

        set_image_scale(mat, self_illumination_node, sim_image_scale)

    reflection_texture = generate_image_node(mat, shader_data["reflection cube map"], permutation_index, asset_cache, "halo1", report)
    if reflection_texture:
        reflection_node = mat.node_tree.nodes.new("ShaderNodeTexEnvironment")
        texcoord_node = mat.node_tree.nodes.new("ShaderNodeTexCoord")
        reflection_node.image = reflection_texture
        reflection_node.location = (-720.0, -1800.0)
        texcoord_node.location = (-900.0, -1800.0)
        connect_inputs(mat.node_tree, reflection_node, "Color", shader_environment_node, "Reflection Cube Map")
        connect_inputs(mat.node_tree, texcoord_node, "Reflection", reflection_node, "Vector")

    if shader_environment_node.inputs["Alpha Tested"].default_value:
        if bpy.app.version <= (4, 2, 0):
            mat.shadow_method = 'CLIP'
        mat.blend_method = 'HASHED'

    mat.use_backface_culling = True

def generate_shader_model_simple(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node)

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    place_node(bdsf_principled, 1)

    base_map_texture = generate_image_node(mat, shader_data["base map"], permutation_index, asset_cache, "halo1", report)
    if base_map_texture:
        base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        base_map_node.image = base_map_texture
        base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        place_node(base_map_node, 2)
        connect_inputs(mat.node_tree, base_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_model(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    model_flags = ShaderFlags(shader_data["flags"])
    model_properties_flags = ModelPropertiesFlags(shader_data["flags_1"])
    self_illumination_flags = ModelSelfIlluminationFlags(shader_data["flags_2"])

    output_material_node = get_output_material_node(mat)
    output_material_node.location = (0.0, 0.0)

    shader_model_node = get_shader_node(mat.node_tree, HALO_1_SHADER_RESOURCES, "shader_model")
    shader_model_node.location = (-440.0, 0.0)
    shader_model_node.name = "Shader Model"

    connect_inputs(mat.node_tree, shader_model_node, "Shader", output_material_node, "Surface")

    shader_model_node.inputs["Simple Parameterization"].default_value = ShaderFlags.simple_parameterization in model_flags
    shader_model_node.inputs["Ignore Normals"].default_value = ShaderFlags.ignore_normals in model_flags
    shader_model_node.inputs["Transparent Lit"].default_value = ShaderFlags.transparent_lit in model_flags
    shader_model_node.inputs["Detail Level"].default_value = shader_data["detail level"]["value"]
    shader_model_node.inputs["Power"].default_value = shader_data["power"]
    shader_model_node.inputs["Color Of Emitted Light"].default_value = convert_to_blender_color(shader_data["color of emitted light"], True)
    shader_model_node.inputs["Tint Color"].default_value = convert_to_blender_color(shader_data["tint color"], True)

    shader_model_node.inputs["Material Type"].default_value = shader_data["material type"]["value"]

    shader_model_node.inputs["Detail After Reflections"].default_value = ModelPropertiesFlags.detail_after_reflection in model_properties_flags
    shader_model_node.inputs["Two Sided"].default_value = ModelPropertiesFlags.two_sided in model_properties_flags
    shader_model_node.inputs["Not Alpha Tested"].default_value = ModelPropertiesFlags.not_alpha_tested in model_properties_flags
    shader_model_node.inputs["Alpha Blended Decal"].default_value = ModelPropertiesFlags.alpha_blended_decal in model_properties_flags
    shader_model_node.inputs["True Atmospheric Fog"].default_value = ModelPropertiesFlags.true_atmospheric_fog in model_properties_flags
    shader_model_node.inputs["Disable Two Sided Culling"].default_value = ModelPropertiesFlags.disable_two_sided_culling in model_properties_flags
    shader_model_node.inputs["Use Xbox Multipurpose Channel Order"].default_value = ModelPropertiesFlags.use_xbox_multipurpose_channel_order in model_properties_flags
    shader_model_node.inputs["Translucency"].default_value = shader_data["translucency"]

    shader_model_node.inputs["Change Color Source"].default_value = shader_data["change color source"]["value"]

    shader_model_node.inputs["No Random Phase"].default_value = ModelSelfIlluminationFlags.no_random_phase in self_illumination_flags
    shader_model_node.inputs["Color Source"].default_value = shader_data["color source"]["value"]
    shader_model_node.inputs["Animation Function"].default_value = shader_data["animation function"]["value"]
    shader_model_node.inputs["Animation Period"].default_value = shader_data["animation period"]
    shader_model_node.inputs["Animation Color Lower Bound"].default_value = convert_to_blender_color(shader_data["animation color lower bound"], True)
    shader_model_node.inputs["Animation Color Upper Bound"].default_value = convert_to_blender_color(shader_data["animation color upper bound"], True)
    if not FunctionEnum.one.value == shader_model_node.inputs["Animation Function"].default_value:
        shader_model_node.inputs["Animation Color Bound Factor"].default_value = 1

    shader_model_node.inputs["Map U Scale"].default_value = shader_data["map u scale"]
    shader_model_node.inputs["Map V Scale"].default_value = shader_data["map v scale"]
    shader_model_node.inputs["Detail Function"].default_value = shader_data["detail function"]["value"]
    shader_model_node.inputs["Detail Mask"].default_value = shader_data["detail mask"]["value"]
    shader_model_node.inputs["Detail Map Scale"].default_value = shader_data["detail map scale"]
    shader_model_node.inputs["Detail Map V Scale"].default_value = shader_data["detail map v scale"]

    shader_model_node.inputs["U Animation Source"].default_value = shader_data["u animation source"]["value"]
    shader_model_node.inputs["U Animation Function"].default_value = shader_data["u animation function"]["value"]
    shader_model_node.inputs["U Animation Period"].default_value = shader_data["u animation period"]
    shader_model_node.inputs["U Animation Phase"].default_value = shader_data["u animation phase"]
    shader_model_node.inputs["U Animation Scale"].default_value = shader_data["u animation scale"]
    shader_model_node.inputs["V Animation Source"].default_value = shader_data["v animation source"]["value"]
    shader_model_node.inputs["V Animation Function"].default_value = shader_data["v animation function"]["value"]
    shader_model_node.inputs["V Animation Period"].default_value = shader_data["v animation period"]
    shader_model_node.inputs["V Animation Phase"].default_value = shader_data["v animation phase"]
    shader_model_node.inputs["V Animation Scale"].default_value = shader_data["v animation scale"]
    shader_model_node.inputs["Rotation Animation Source"].default_value = shader_data["rotation animation source"]["value"]
    shader_model_node.inputs["Rotation Animation Function"].default_value = shader_data["rotation animation function"]["value"]
    shader_model_node.inputs["Rotation Animation Period"].default_value = shader_data["rotation animation period"]
    shader_model_node.inputs["Rotation Animation Phase"].default_value = shader_data["rotation animation phase"]
    shader_model_node.inputs["Rotation Animation Scale"].default_value = shader_data["rotation animation scale"]
    shader_model_node.inputs["Rotation Animation Center"].default_value = shader_data["rotation animation center"]

    shader_model_node.inputs["Reflection Falloff Distance"].default_value = shader_data["falloff distance"]
    shader_model_node.inputs["Reflection Cutoff Distance"].default_value = shader_data["cutoff distance"]
    shader_model_node.inputs["Perpendicular Brightness"].default_value = shader_data["perpendicular brightness"]
    shader_model_node.inputs["Perpendicular Tint Color"].default_value = convert_to_blender_color(shader_data["perpendicular tint color"], True)
    shader_model_node.inputs["Parallel Brightness"].default_value = shader_data["parallel brightness"]
    shader_model_node.inputs["Parallel Tint Color"].default_value = convert_to_blender_color(shader_data["parallel tint color"], True)

    base_map_texture = generate_image_node(mat, shader_data["base map"], permutation_index, asset_cache, "halo1", report)
    base_bitmap = None
    base_map_node = None
    if base_map_texture:
        base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        base_map_node.image = base_map_texture
        base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        base_map_node.location = (-720.0, 0.0)
        connect_inputs(mat.node_tree, base_map_node, "Color", shader_model_node, "Base Map")
        connect_inputs(mat.node_tree, base_map_node, "Alpha", shader_model_node, "Base Map Alpha")

        bm_u_scale = shader_data["map u scale"]
        if bm_u_scale == 0.0:
            bm_u_scale = 1.0

        bm_v_scale = shader_data["map v scale"]
        if bm_v_scale == 0.0:
            bm_v_scale = 1.0

        bm_image_scale = (bm_u_scale, bm_v_scale, 1)

        base_bitmap = tag_interface.get_disk_asset(shader_data["base map"]["path"], tag_common.h1_tag_groups.get(shader_data["base map"]["group name"]))
        set_image_scale(mat, base_map_node, bm_image_scale)

    multipurpose_map_texture = generate_image_node(mat, shader_data["multipurpose map"], permutation_index, asset_cache, "halo1", report)
    if multipurpose_map_texture:
        multipurpose_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        multipurpose_map_node.image = multipurpose_map_texture
        multipurpose_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        multipurpose_map_node.image.colorspace_settings.name = 'Non-Color'
        multipurpose_map_node.interpolation = 'Cubic'
        multipurpose_map_node.location = (-720.0, -320.0)
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
        detail_map_node.location = (-720.0, -640.0)
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
        texcoord_node = mat.node_tree.nodes.new("ShaderNodeTexCoord")
        cube_map_node.image = cube_map_texture
        cube_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        cube_map_node.location = (-720.0, -960.0)
        texcoord_node.location = (-900.0, -960.0)
        connect_inputs(mat.node_tree, cube_map_node, "Color", shader_model_node, "Reflection Cube Map")
        connect_inputs(mat.node_tree, texcoord_node, "Reflection", cube_map_node, "Vector")

    mat.use_backface_culling = True
    if shader_model_node.inputs["Two Sided"].default_value:
        mat.use_backface_culling = False

    if base_bitmap is not None and base_map_node is not None:
        ignore_alpha_bitmap = base_bitmap["Data"]["encoding format"]["value"] is FormatEnum.compressed_with_color_key_transparency.value
        ignore_alpha_shader = shader_model_node.inputs["Not Alpha Tested"].default_value
        is_blended_decal = shader_model_node.inputs["Alpha Blended Decal"].default_value
        if ignore_alpha_bitmap or (ignore_alpha_shader and not is_blended_decal):
            base_map_node.image.alpha_mode = 'NONE'
        else:
            if bpy.app.version <= (4, 2, 0):
                mat.shadow_method = 'CLIP'
            mat.blend_method = 'HASHED'

def generate_shader_transparent_chicago_simple(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node)

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    place_node(bdsf_principled, 1)

    if len(shader_data["maps"]) > 0:
        base_map = shader_data["maps"][0]["map"]
        base_map_texture = generate_image_node(mat, base_map, permutation_index, asset_cache, "halo1", report)
        if base_map_texture:
            base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            base_map_node.image = base_map_texture
            base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
            place_node(base_map_node, 2)
            connect_inputs(mat.node_tree, base_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_chicago(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    shader_flags = ShaderFlags(shader_data["flags"])
    shader_property_flags = ShaderTransparentPropertiesFlags(shader_data["flags_1"])
    extra_flags = ExtraFlags(shader_data["extra flags"])

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))

    mix_node = mat.node_tree.nodes.new("ShaderNodeMixShader")
    mix_node.location = Vector((-180.0, 0.0))
    connect_inputs(mat.node_tree, mix_node, "Shader", output_material_node, "Surface")

    emission_view_node = mat.node_tree.nodes.new("ShaderNodeEmission")
    emission_view_node.location = Vector((-360.0, 0.0))
    connect_inputs(mat.node_tree, emission_view_node, "Emission", mix_node, 2)

    emission_light_node = mat.node_tree.nodes.new("ShaderNodeEmission")
    emission_light_node.location = Vector((-360.0, -140.0))
    connect_inputs(mat.node_tree, emission_light_node, "Emission", mix_node, 1)

    light_path_node = mat.node_tree.nodes.new("ShaderNodeLightPath")
    light_path_node.location = Vector((-360.0, 400.0))
    connect_inputs(mat.node_tree, light_path_node, 0, mix_node, 0)

    stc_node = get_shader_node(mat.node_tree, HALO_1_SHADER_RESOURCES, "shader_transparent_chicago")
    stc_node.name = "Shader Transparent Chicago"
    stc_node.location = Vector((-800.0, 0.0))

    connect_inputs(mat.node_tree, stc_node, "Power", emission_light_node, "Strength")
    connect_inputs(mat.node_tree, stc_node, "Color Of Emitted Light", emission_light_node, "Color")
    connect_inputs(mat.node_tree, stc_node, "Map A", emission_view_node, "Color")

    stc_node.inputs["Simple Parameterization"].default_value = ShaderFlags.simple_parameterization in shader_flags
    stc_node.inputs["Ignore Normals"].default_value = ShaderFlags.ignore_normals in shader_flags
    stc_node.inputs["Transparent Lit"].default_value = ShaderFlags.transparent_lit in shader_flags
    stc_node.inputs["Detail Level"].default_value = shader_data["detail level"]["value"]
    stc_node.inputs["Power"].default_value = shader_data["power"]
    stc_node.inputs["Color Of Emitted Light"].default_value = convert_to_blender_color(shader_data["color of emitted light"], True)
    stc_node.inputs["Tint Color"].default_value = convert_to_blender_color(shader_data["tint color"], True)

    stc_node.inputs["Material Type"].default_value = shader_data["material type"]["value"]

    stc_node.inputs["Numeric Counter Limit"].default_value = shader_data["numeric counter limit"]
    stc_node.inputs["Alpha Tested"].default_value = ShaderTransparentPropertiesFlags.alpha_tested in shader_property_flags
    stc_node.inputs["Decal"].default_value = ShaderTransparentPropertiesFlags.decal in shader_property_flags
    stc_node.inputs["Two Sided"].default_value = ShaderTransparentPropertiesFlags.two_sided in shader_property_flags
    stc_node.inputs["First Map Is In Screenspace"].default_value = ShaderTransparentPropertiesFlags.first_map_is_in_screenspace in shader_property_flags
    stc_node.inputs["Draw Before Water"].default_value = ShaderTransparentPropertiesFlags.draw_before_water in shader_property_flags
    stc_node.inputs["Ignore Effect"].default_value = ShaderTransparentPropertiesFlags.ignore_effect in shader_property_flags
    stc_node.inputs["Scale First Map With Distance"].default_value = ShaderTransparentPropertiesFlags.scale_first_map_with_distance in shader_property_flags
    stc_node.inputs["Numeric"].default_value = ShaderTransparentPropertiesFlags.numeric in shader_property_flags
    stc_node.inputs["First Map Type"].default_value = shader_data["first map type"]["value"]
    stc_node.inputs["Framebuffer Blend Function"].default_value = shader_data["framebuffer blend function"]["value"]
    stc_node.inputs["Framebuffer Fade Mode"].default_value = shader_data["framebuffer fade mode"]["value"]
    stc_node.inputs["Framebuffer Fade Source"].default_value = shader_data["framebuffer fade source"]["value"]

    stc_node.inputs["Lens Flare Spacing"].default_value = shader_data["lens flare spacing"]

    stc_node.inputs["Dont Fade Active Camouflage"].default_value = ExtraFlags.dont_fade_active_camouflage in extra_flags
    stc_node.inputs["Numeric Countdown Timer"].default_value = ExtraFlags.numeric_countdown_timer in extra_flags
    stc_node.inputs["Custom Edition Blending"].default_value = ExtraFlags.custom_edition_blending in extra_flags

    map_slots = ("A", "B", "C", "D")
    map_positions = (Vector((-1080.0, 0.0)), Vector((-1080.0, -300.0)), Vector((-1080.0, -600.0)), Vector((-1080.0, -900.0)))
    for map_idx, map_element in enumerate(shader_data["maps"]):
        map_flags = ChicagoMapFlags(map_element["flags"])

        stc_node.inputs["Map %s" % map_slots[map_idx]].default_value = True
        stc_node.inputs["Map %s Unfiltered" % map_slots[map_idx]].default_value = ChicagoMapFlags.unfiltered in map_flags
        stc_node.inputs["Map %s Alpha Replicate" % map_slots[map_idx]].default_value = ChicagoMapFlags.alpha_replicate in map_flags
        stc_node.inputs["Map %s U Clamped" % map_slots[map_idx]].default_value = ChicagoMapFlags.u_clamped in map_flags
        stc_node.inputs["Map %s V Clamped" % map_slots[map_idx]].default_value = ChicagoMapFlags.v_clamped in map_flags
        stc_node.inputs["Map %s Color Function" % map_slots[map_idx]].default_value = map_element["color function"]["value"]
        stc_node.inputs["Map %s Alpha Function" % map_slots[map_idx]].default_value = map_element["alpha function"]["value"]
        stc_node.inputs["Map %s U Scale" % map_slots[map_idx]].default_value = map_element["map u scale"]
        stc_node.inputs["Map %s V Scale" % map_slots[map_idx]].default_value = map_element["map v scale"]
        stc_node.inputs["Map %s U Offset" % map_slots[map_idx]].default_value = map_element["map u offset"]
        stc_node.inputs["Map %s V Offset" % map_slots[map_idx]].default_value = map_element["map v offset"]
        stc_node.inputs["Map %s Rotation" % map_slots[map_idx]].default_value = map_element["map rotation"]
        stc_node.inputs["Map %s Mipmap Bias" % map_slots[map_idx]].default_value = map_element["mipmap bias"]
 
        stc_node.inputs["Map %s U Animation Source" % map_slots[map_idx]].default_value = map_element["u animation source"]["value"]
        stc_node.inputs["Map %s U Animation Function" % map_slots[map_idx]].default_value = map_element["u animation function"]["value"]
        stc_node.inputs["Map %s U Animation Period" % map_slots[map_idx]].default_value = map_element["u animation period"]
        stc_node.inputs["Map %s U Animation Phase" % map_slots[map_idx]].default_value = map_element["u animation phase"]
        stc_node.inputs["Map %s U Animation Scale" % map_slots[map_idx]].default_value = map_element["u animation scale"]
        stc_node.inputs["Map %s V Animation Source" % map_slots[map_idx]].default_value = map_element["v animation source"]["value"]
        stc_node.inputs["Map %s V Animation Function" % map_slots[map_idx]].default_value = map_element["v animation function"]["value"]
        stc_node.inputs["Map %s V Animation Period" % map_slots[map_idx]].default_value = map_element["v animation period"]
        stc_node.inputs["Map %s V Animation Phase" % map_slots[map_idx]].default_value = map_element["v animation phase"]
        stc_node.inputs["Map %s V Animation Scale" % map_slots[map_idx]].default_value = map_element["v animation scale"]
        stc_node.inputs["Map %s Rotation Animation Source" % map_slots[map_idx]].default_value = map_element["rotation animation source"]["value"]
        stc_node.inputs["Map %s Rotation Animation Function" % map_slots[map_idx]].default_value = map_element["rotation animation function"]["value"]
        stc_node.inputs["Map %s Rotation Animation Period" % map_slots[map_idx]].default_value = map_element["rotation animation period"]
        stc_node.inputs["Map %s Rotation Animation Phase" % map_slots[map_idx]].default_value = map_element["rotation animation phase"]
        stc_node.inputs["Map %s Rotation Animation Scale" % map_slots[map_idx]].default_value = map_element["rotation animation scale"]
        stc_node.inputs["Map %s Rotation Animation Center" % map_slots[map_idx]].default_value = map_element["rotation animation center"]

        map_texture = generate_image_node(mat, map_element["map"], permutation_index, asset_cache, "halo1", report)
        if map_texture:
            map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            map_node.image = map_texture
            map_node.image.alpha_mode = 'CHANNEL_PACKED'
            map_node.location = map_positions[map_idx]
            connect_inputs(mat.node_tree, map_node, "Color", stc_node, "Map %s Color" % map_slots[map_idx])
            connect_inputs(mat.node_tree, map_node, "Alpha", stc_node, "Map %s Alpha" % map_slots[map_idx])

def generate_shader_transparent_chicago_extended_simple(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node)

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    place_node(bdsf_principled, 1)

    if len(shader_data["4 stage maps"]) > 0:
        base_map = shader_data["4 stage maps"][0]["map"]
        base_map_texture = generate_image_node(mat, base_map, permutation_index, asset_cache, "halo1", report)
        if base_map_texture:
            base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            base_map_node.image = base_map_texture
            base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
            place_node(base_map_node, 2)
            connect_inputs(mat.node_tree, base_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_chicago_extended(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    shader_flags = ShaderFlags(shader_data["flags"])
    shader_property_flags = ShaderTransparentPropertiesFlags(shader_data["flags_1"])
    extra_flags = ExtraFlags(shader_data["extra flags"])

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))

    mix_node = mat.node_tree.nodes.new("ShaderNodeMixShader")
    mix_node.location = Vector((-180.0, 0.0))
    connect_inputs(mat.node_tree, mix_node, "Shader", output_material_node, "Surface")

    emission_view_node = mat.node_tree.nodes.new("ShaderNodeEmission")
    emission_view_node.location = Vector((-360.0, 0.0))
    connect_inputs(mat.node_tree, emission_view_node, "Emission", mix_node, 2)

    emission_light_node = mat.node_tree.nodes.new("ShaderNodeEmission")
    emission_light_node.location = Vector((-360.0, -140.0))
    connect_inputs(mat.node_tree, emission_light_node, "Emission", mix_node, 1)

    light_path_node = mat.node_tree.nodes.new("ShaderNodeLightPath")
    light_path_node.location = Vector((-360.0, 400.0))
    connect_inputs(mat.node_tree, light_path_node, 0, mix_node, 0)

    stce_node = get_shader_node(mat.node_tree, HALO_1_SHADER_RESOURCES, "shader_transparent_chicago_extended")
    stce_node.name = "Shader Transparent Chicago Extended"
    stce_node.location = Vector((-800.0, 0.0))

    connect_inputs(mat.node_tree, stce_node, "Power", emission_light_node, "Strength")
    connect_inputs(mat.node_tree, stce_node, "Color Of Emitted Light", emission_light_node, "Color")
    connect_inputs(mat.node_tree, stce_node, "4 Stage Map A", emission_view_node, "Color")

    stce_node.inputs["Simple Parameterization"].default_value = ShaderFlags.simple_parameterization in shader_flags
    stce_node.inputs["Ignore Normals"].default_value = ShaderFlags.ignore_normals in shader_flags
    stce_node.inputs["Transparent Lit"].default_value = ShaderFlags.transparent_lit in shader_flags
    stce_node.inputs["Detail Level"].default_value = shader_data["detail level"]["value"]
    stce_node.inputs["Power"].default_value = shader_data["power"]
    stce_node.inputs["Color Of Emitted Light"].default_value = convert_to_blender_color(shader_data["color of emitted light"], True)
    stce_node.inputs["Tint Color"].default_value = convert_to_blender_color(shader_data["tint color"], True)

    stce_node.inputs["Material Type"].default_value = shader_data["material type"]["value"]

    stce_node.inputs["Numeric Counter Limit"].default_value = shader_data["numeric counter limit"]
    stce_node.inputs["Alpha Tested"].default_value = ShaderTransparentPropertiesFlags.alpha_tested in shader_property_flags
    stce_node.inputs["Decal"].default_value = ShaderTransparentPropertiesFlags.decal in shader_property_flags
    stce_node.inputs["Two Sided"].default_value = ShaderTransparentPropertiesFlags.two_sided in shader_property_flags
    stce_node.inputs["First Map Is In Screenspace"].default_value = ShaderTransparentPropertiesFlags.first_map_is_in_screenspace in shader_property_flags
    stce_node.inputs["Draw Before Water"].default_value = ShaderTransparentPropertiesFlags.draw_before_water in shader_property_flags
    stce_node.inputs["Ignore Effect"].default_value = ShaderTransparentPropertiesFlags.ignore_effect in shader_property_flags
    stce_node.inputs["Scale First Map With Distance"].default_value = ShaderTransparentPropertiesFlags.scale_first_map_with_distance in shader_property_flags
    stce_node.inputs["Numeric"].default_value = ShaderTransparentPropertiesFlags.numeric in shader_property_flags
    stce_node.inputs["First Map Type"].default_value = shader_data["first map type"]["value"]
    stce_node.inputs["Framebuffer Blend Function"].default_value = shader_data["framebuffer blend function"]["value"]
    stce_node.inputs["Framebuffer Fade Mode"].default_value = shader_data["framebuffer fade mode"]["value"]
    stce_node.inputs["Framebuffer Fade Source"].default_value = shader_data["framebuffer fade source"]["value"]

    stce_node.inputs["Lens Flare Spacing"].default_value = shader_data["lens flare spacing"]

    stce_node.inputs["Dont Fade Active Camouflage"].default_value = ExtraFlags.dont_fade_active_camouflage in extra_flags
    stce_node.inputs["Numeric Countdown Timer"].default_value = ExtraFlags.numeric_countdown_timer in extra_flags
    stce_node.inputs["Custom Edition Blending"].default_value = ExtraFlags.custom_edition_blending in extra_flags

    map0_slots = ("A", "B", "C", "D")
    map0_positions = (Vector((-1080.0, 0.0)), Vector((-1080.0, -300.0)), Vector((-1080.0, -600.0)), Vector((-1080.0, -900.0)))
    map1_slots = ("A", "B")
    map1_positions = (Vector((-1080.0, -1200.0)), Vector((-1080.0, -1500.0)))
    for map_idx, map_element in enumerate(shader_data["4 stage maps"]):
        map_flags = ChicagoMapFlags(map_element["flags"])

        stce_node.inputs["4 Stage Map %s" % map0_slots[map_idx]].default_value = True
        stce_node.inputs["4 Stage Map %s Unfiltered" % map0_slots[map_idx]].default_value = ChicagoMapFlags.unfiltered in map_flags
        stce_node.inputs["4 Stage Map %s Alpha Replicate" % map0_slots[map_idx]].default_value = ChicagoMapFlags.alpha_replicate in map_flags
        stce_node.inputs["4 Stage Map %s U Clamped" % map0_slots[map_idx]].default_value = ChicagoMapFlags.u_clamped in map_flags
        stce_node.inputs["4 Stage Map %s V Clamped" % map0_slots[map_idx]].default_value = ChicagoMapFlags.v_clamped in map_flags
        stce_node.inputs["4 Stage Map %s Color Function" % map0_slots[map_idx]].default_value = map_element["color function"]["value"]
        stce_node.inputs["4 Stage Map %s Alpha Function" % map0_slots[map_idx]].default_value = map_element["alpha function"]["value"]
        stce_node.inputs["4 Stage Map %s U Scale" % map0_slots[map_idx]].default_value = map_element["map u scale"]
        stce_node.inputs["4 Stage Map %s V Scale" % map0_slots[map_idx]].default_value = map_element["map v scale"]
        stce_node.inputs["4 Stage Map %s U Offset" % map0_slots[map_idx]].default_value = map_element["map u offset"]
        stce_node.inputs["4 Stage Map %s V Offset" % map0_slots[map_idx]].default_value = map_element["map v offset"]
        stce_node.inputs["4 Stage Map %s Rotation" % map0_slots[map_idx]].default_value = map_element["map rotation"]
        stce_node.inputs["4 Stage Map %s Mipmap Bias" % map0_slots[map_idx]].default_value = map_element["mipmap bias"]
 
        stce_node.inputs["4 Stage Map %s U Animation Source" % map0_slots[map_idx]].default_value = map_element["u animation source"]["value"]
        stce_node.inputs["4 Stage Map %s U Animation Function" % map0_slots[map_idx]].default_value = map_element["u animation function"]["value"]
        stce_node.inputs["4 Stage Map %s U Animation Period" % map0_slots[map_idx]].default_value = map_element["u animation period"]
        stce_node.inputs["4 Stage Map %s U Animation Phase" % map0_slots[map_idx]].default_value = map_element["u animation phase"]
        stce_node.inputs["4 Stage Map %s U Animation Scale" % map0_slots[map_idx]].default_value = map_element["u animation scale"]
        stce_node.inputs["4 Stage Map %s V Animation Source" % map0_slots[map_idx]].default_value = map_element["v animation source"]["value"]
        stce_node.inputs["4 Stage Map %s V Animation Function" % map0_slots[map_idx]].default_value = map_element["v animation function"]["value"]
        stce_node.inputs["4 Stage Map %s V Animation Period" % map0_slots[map_idx]].default_value = map_element["v animation period"]
        stce_node.inputs["4 Stage Map %s V Animation Phase" % map0_slots[map_idx]].default_value = map_element["v animation phase"]
        stce_node.inputs["4 Stage Map %s V Animation Scale" % map0_slots[map_idx]].default_value = map_element["v animation scale"]
        stce_node.inputs["4 Stage Map %s Rotation Animation Source" % map0_slots[map_idx]].default_value = map_element["rotation animation source"]["value"]
        stce_node.inputs["4 Stage Map %s Rotation Animation Function" % map0_slots[map_idx]].default_value = map_element["rotation animation function"]["value"]
        stce_node.inputs["4 Stage Map %s Rotation Animation Period" % map0_slots[map_idx]].default_value = map_element["rotation animation period"]
        stce_node.inputs["4 Stage Map %s Rotation Animation Phase" % map0_slots[map_idx]].default_value = map_element["rotation animation phase"]
        stce_node.inputs["4 Stage Map %s Rotation Animation Scale" % map0_slots[map_idx]].default_value = map_element["rotation animation scale"]
        stce_node.inputs["4 Stage Map %s Rotation Animation Center" % map0_slots[map_idx]].default_value = map_element["rotation animation center"]

        map_texture = generate_image_node(mat, map_element["map"], permutation_index, asset_cache, "halo1", report)
        if map_texture:
            map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            map_node.image = map_texture
            map_node.image.alpha_mode = 'CHANNEL_PACKED'
            map_node.location = map0_positions[map_idx]
            connect_inputs(mat.node_tree, map_node, "Color", stce_node, "4 Stage Map %s Color" % map0_slots[map_idx])
            connect_inputs(mat.node_tree, map_node, "Alpha", stce_node, "4 Stage Map %s Alpha" % map0_slots[map_idx])

    for map_idx, map_element in enumerate(shader_data["2 stage maps"]):
        map_flags = ChicagoMapFlags(map_element["flags"])

        stce_node.inputs["2 Stage Map %s" % map1_slots[map_idx]].default_value = True
        stce_node.inputs["2 Stage Map %s Unfiltered" % map1_slots[map_idx]].default_value = ChicagoMapFlags.unfiltered in map_flags
        stce_node.inputs["2 Stage Map %s Alpha Replicate" % map1_slots[map_idx]].default_value = ChicagoMapFlags.alpha_replicate in map_flags
        stce_node.inputs["2 Stage Map %s U Clamped" % map1_slots[map_idx]].default_value = ChicagoMapFlags.u_clamped in map_flags
        stce_node.inputs["2 Stage Map %s V Clamped" % map1_slots[map_idx]].default_value = ChicagoMapFlags.v_clamped in map_flags
        stce_node.inputs["2 Stage Map %s Color Function" % map1_slots[map_idx]].default_value = map_element["color function"]["value"]
        stce_node.inputs["2 Stage Map %s Alpha Function" % map1_slots[map_idx]].default_value = map_element["alpha function"]["value"]
        stce_node.inputs["2 Stage Map %s U Scale" % map1_slots[map_idx]].default_value = map_element["map u scale"]
        stce_node.inputs["2 Stage Map %s V Scale" % map1_slots[map_idx]].default_value = map_element["map v scale"]
        stce_node.inputs["2 Stage Map %s U Offset" % map1_slots[map_idx]].default_value = map_element["map u offset"]
        stce_node.inputs["2 Stage Map %s V Offset" % map1_slots[map_idx]].default_value = map_element["map v offset"]
        stce_node.inputs["2 Stage Map %s Rotation" % map1_slots[map_idx]].default_value = map_element["map rotation"]
        stce_node.inputs["2 Stage Map %s Mipmap Bias" % map1_slots[map_idx]].default_value = map_element["mipmap bias"]
 
        stce_node.inputs["2 Stage Map %s U Animation Source" % map1_slots[map_idx]].default_value = map_element["u animation source"]["value"]
        stce_node.inputs["2 Stage Map %s U Animation Function" % map1_slots[map_idx]].default_value = map_element["u animation function"]["value"]
        stce_node.inputs["2 Stage Map %s U Animation Period" % map1_slots[map_idx]].default_value = map_element["u animation period"]
        stce_node.inputs["2 Stage Map %s U Animation Phase" % map1_slots[map_idx]].default_value = map_element["u animation phase"]
        stce_node.inputs["2 Stage Map %s U Animation Scale" % map1_slots[map_idx]].default_value = map_element["u animation scale"]
        stce_node.inputs["2 Stage Map %s V Animation Source" % map1_slots[map_idx]].default_value = map_element["v animation source"]["value"]
        stce_node.inputs["2 Stage Map %s V Animation Function" % map1_slots[map_idx]].default_value = map_element["v animation function"]["value"]
        stce_node.inputs["2 Stage Map %s V Animation Period" % map1_slots[map_idx]].default_value = map_element["v animation period"]
        stce_node.inputs["2 Stage Map %s V Animation Phase" % map1_slots[map_idx]].default_value = map_element["v animation phase"]
        stce_node.inputs["2 Stage Map %s V Animation Scale" % map1_slots[map_idx]].default_value = map_element["v animation scale"]
        stce_node.inputs["2 Stage Map %s Rotation Animation Source" % map1_slots[map_idx]].default_value = map_element["rotation animation source"]["value"]
        stce_node.inputs["2 Stage Map %s Rotation Animation Function" % map1_slots[map_idx]].default_value = map_element["rotation animation function"]["value"]
        stce_node.inputs["2 Stage Map %s Rotation Animation Period" % map1_slots[map_idx]].default_value = map_element["rotation animation period"]
        stce_node.inputs["2 Stage Map %s Rotation Animation Phase" % map1_slots[map_idx]].default_value = map_element["rotation animation phase"]
        stce_node.inputs["2 Stage Map %s Rotation Animation Scale" % map1_slots[map_idx]].default_value = map_element["rotation animation scale"]
        stce_node.inputs["2 Stage Map %s Rotation Animation Center" % map1_slots[map_idx]].default_value = map_element["rotation animation center"]

        map_texture = generate_image_node(mat, map_element["map"], permutation_index, asset_cache, "halo1", report)
        if map_texture:
            map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            map_node.image = map_texture
            map_node.image.alpha_mode = 'CHANNEL_PACKED'
            map_node.location = map1_positions[map_idx]
            connect_inputs(mat.node_tree, map_node, "Color", stce_node, "2 Stage Map %s Color" % map1_slots[map_idx])
            connect_inputs(mat.node_tree, map_node, "Alpha", stce_node, "2 Stage Map %s Alpha" % map1_slots[map_idx])

def generate_shader_transparent_generic_simple(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node)

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    place_node(bdsf_principled, 1)

    if len(shader_data["maps"]) > 0:
        base_map = shader_data["maps"][0]["map"]
        base_map_texture = generate_image_node(mat, base_map, permutation_index, asset_cache, "halo1", report)
        if base_map_texture:
            base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            base_map_node.image = base_map_texture
            base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
            place_node(base_map_node, 2)
            connect_inputs(mat.node_tree, base_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_generic(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    output_material_node = get_output_material_node(mat)
    output_material_node.location = (0.0, 0.0)

    stg_node = get_shader_node(mat.node_tree, HALO_1_SHADER_RESOURCES, "shader_transparent_generic")
    stg_node.name = "Shader Transparent Generic"
    set_stg_values(shader_data, stg_node)
    stage_groups = []
    stage_idx = 0
    for stage_idx, stage_element in enumerate(reversed(shader_data["stages"])):
        stage_groups.append(create_stages(mat.node_tree, stage_element, stage_idx))

    stg_node.location = (-7200.0, 0.0)

    map_tag_refs = [None, None, None, None]
    for map_idx, map_element in enumerate(shader_data["maps"]):
        map_tag_refs[map_idx] = map_element["map"]

    if map_tag_refs[0] is not None:
        map_a_texture = generate_image_node(mat, map_tag_refs[0], permutation_index, asset_cache, "halo1", report)
        if map_a_texture:
            map_a_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            map_a_node.image = map_a_texture
            map_a_node.image.alpha_mode = 'CHANNEL_PACKED'
            map_a_node.location = Vector((-7480.0, 0.0))
            connect_inputs(mat.node_tree, map_a_node, "Color", stg_node, "Map A Color")
            connect_inputs(mat.node_tree, map_a_node, "Alpha", stg_node, "Map A Alpha")
            generate_texture_mapping(mat.node_tree, stg_node, "A", map_a_node, "Vector")

    if map_tag_refs[1] is not None:
        map_b_texture = generate_image_node(mat, map_tag_refs[1], permutation_index, asset_cache, "halo1", report)
        if map_b_texture:
            map_b_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            map_b_node.image = map_b_texture
            map_b_node.image.alpha_mode = 'CHANNEL_PACKED'
            map_b_node.location = Vector((-7480.0, -380.0))
            connect_inputs(mat.node_tree, map_b_node, "Color", stg_node, "Map B Color")
            connect_inputs(mat.node_tree, map_b_node, "Alpha", stg_node, "Map B Alpha")
            generate_texture_mapping(mat.node_tree, stg_node, "B", map_b_node, "Vector")

    if map_tag_refs[2] is not None:
        map_c_texture = generate_image_node(mat, map_tag_refs[2], permutation_index, asset_cache, "halo1", report)
        if map_c_texture:
            map_c_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            map_c_node.image = map_c_texture
            map_c_node.image.alpha_mode = 'CHANNEL_PACKED'
            map_c_node.location = Vector((-7480.0, -760.0))
            connect_inputs(mat.node_tree, map_c_node, "Color", stg_node, "Map C Color")
            connect_inputs(mat.node_tree, map_c_node, "Alpha", stg_node, "Map C Alpha")
            generate_texture_mapping(mat.node_tree, stg_node, "C", map_c_node, "Vector")

    if map_tag_refs[3] is not None:
        map_d_texture = generate_image_node(mat, map_tag_refs[3], permutation_index, asset_cache, "halo1", report)
        if map_d_texture:
            map_d_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            map_d_node.image = map_d_texture
            map_d_node.image.alpha_mode = 'CHANNEL_PACKED'
            map_d_node.location = Vector((-7480.0, -1140.0))
            connect_inputs(mat.node_tree, map_d_node, "Color", stg_node, "Map D Color")
            connect_inputs(mat.node_tree, map_d_node, "Alpha", stg_node, "Map D Alpha")
            generate_texture_mapping(mat.node_tree, stg_node, "D", map_d_node, "Vector")

    stg_paths = {
        "scratch_0_color": None,
        "scratch_0_alpha": None,
        "scratch_1_color": None,
        "scratch_1_alpha": None,
        "vertex_0_color": None,
        "vertex_0_alpha": None,
        "vertex_1_color": None,
        "vertex_1_alpha": None,
        "map_a_color": [stg_node, "Map A"],
        "map_a_alpha": [stg_node, "Map A Alpha"],
        "map_b_color": [stg_node, "Map B"],
        "map_b_alpha": [stg_node, "Map B Alpha"],
        "map_c_color": [stg_node, "Map C"],
        "map_c_alpha": [stg_node, "Map C Alpha"],
        "map_d_color": [stg_node, "Map D"],
        "map_d_alpha": [stg_node, "Map D Alpha"],
    }
    for stage_idx, stage in enumerate(reversed(stage_groups)):
        get_field_input_instructions(mat.node_tree, stg_node.inputs["Stage %s Input A" % stage_idx].default_value, stg_paths, stg_node, stage_idx, stage["c_a_node"], "Color")
        get_field_input_instructions(mat.node_tree, stg_node.inputs["Stage %s Input B" % stage_idx].default_value, stg_paths, stg_node, stage_idx, stage["c_b_node"], "Color")
        get_field_input_instructions(mat.node_tree, stg_node.inputs["Stage %s Input C" % stage_idx].default_value, stg_paths, stg_node, stage_idx, stage["c_c_node"], "Color")
        get_field_input_instructions(mat.node_tree, stg_node.inputs["Stage %s Input D" % stage_idx].default_value, stg_paths, stg_node, stage_idx, stage["c_d_node"], "Color")

        if stage["c_add_abcd_node"] is None:
            connect_inputs(mat.node_tree, stage["c_mix_abcd_node"], "Value", stage["c_abcd_node"], "Color")
            if stg_paths["scratch_0_alpha"] is None:
                stage["c_mix_abcd_node"].inputs["Scratch0 Alpha"].default_value = 0.0
            else:
                output_node, output_key = stg_paths["scratch_0_alpha"]
                connect_inputs(mat.node_tree, output_node, output_key, stage["c_mix_abcd_node"], "Scratch0 Alpha")
            connect_inputs(mat.node_tree, stage["c_ab_node"], "Result", stage["c_mix_abcd_node"], "AB")
            connect_inputs(mat.node_tree, stage["c_cd_node"], "Result", stage["c_mix_abcd_node"], "CD")
        else:
            connect_inputs(mat.node_tree, stage["c_add_abcd_node"], "Result", stage["c_abcd_node"], "Color")
            connect_inputs(mat.node_tree, stage["c_ab_node"], "Result", stage["c_add_abcd_node"], "A")
            connect_inputs(mat.node_tree, stage["c_cd_node"], "Result", stage["c_add_abcd_node"], "B")

        connect_inputs(mat.node_tree, stage["c_a_node"], "Color", stage["c_ab_node"], "A")
        connect_inputs(mat.node_tree, stage["c_b_node"], "Color", stage["c_ab_node"], "B")
        connect_inputs(mat.node_tree, stage["c_c_node"], "Color", stage["c_cd_node"], "A")
        connect_inputs(mat.node_tree, stage["c_d_node"], "Color", stage["c_cd_node"], "B")

        get_field_input_instructions(mat.node_tree, stg_node.inputs["Stage %s Input A Alpha" % stage_idx].default_value, stg_paths, stg_node, stage_idx, stage["a_a_node"], "Value", is_alpha=True)
        get_field_input_instructions(mat.node_tree, stg_node.inputs["Stage %s Input B Alpha" % stage_idx].default_value, stg_paths, stg_node, stage_idx, stage["a_b_node"], "Value", is_alpha=True)
        get_field_input_instructions(mat.node_tree, stg_node.inputs["Stage %s Input C Alpha" % stage_idx].default_value, stg_paths, stg_node, stage_idx, stage["a_c_node"], "Value", is_alpha=True)
        get_field_input_instructions(mat.node_tree, stg_node.inputs["Stage %s Input D Alpha" % stage_idx].default_value, stg_paths, stg_node, stage_idx, stage["a_d_node"], "Value", is_alpha=True)

        if stage["a_add_abcd_node"] is None:
            connect_inputs(mat.node_tree, stage["a_mix_abcd_node"], "Value", stage["a_abcd_node"], "Input")
            if stg_paths["scratch_0_alpha"] is None:
                stage["a_mix_abcd_node"].inputs["Scratch0 Alpha"].default_value = 0.0
            else:
                output_node, output_key = stg_paths["scratch_0_alpha"]
                connect_inputs(mat.node_tree, output_node, output_key, stage["a_mix_abcd_node"], "Scratch0 Alpha")
            connect_inputs(mat.node_tree, stage["a_ab_node"], "Value", stage["a_mix_abcd_node"], "AB")
            connect_inputs(mat.node_tree, stage["a_cd_node"], "Value", stage["a_mix_abcd_node"], "CD")
        else:
            connect_inputs(mat.node_tree, stage["a_add_abcd_node"], "Value", stage["a_abcd_node"], "Input")
            connect_inputs(mat.node_tree, stage["a_ab_node"], "Value", stage["a_add_abcd_node"], 0)
            connect_inputs(mat.node_tree, stage["a_cd_node"], "Value", stage["a_add_abcd_node"], 1)


        connect_inputs(mat.node_tree, stage["a_a_node"], "Value", stage["a_ab_node"], 0)
        connect_inputs(mat.node_tree, stage["a_b_node"], "Value", stage["a_ab_node"], 1)
        connect_inputs(mat.node_tree, stage["a_c_node"], "Value", stage["a_cd_node"], 0)
        connect_inputs(mat.node_tree, stage["a_d_node"], "Value", stage["a_cd_node"], 1)

        get_field_output_instructions(stg_node.inputs["Stage %s Output Ab" % stage_idx].default_value, stg_paths, stage["c_ab_node"], input_key="Result", is_alpha=False)
        get_field_output_instructions(stg_node.inputs["Stage %s Output Cd" % stage_idx].default_value, stg_paths, stage["c_cd_node"], input_key="Result", is_alpha=False)
        get_field_output_instructions(stg_node.inputs["Stage %s Output Ab Cd Mux Sum" % stage_idx].default_value, stg_paths, stage["c_abcd_node"], input_key="Color", is_alpha=False)

        get_field_output_instructions(stg_node.inputs["Stage %s Output Ab Alpha" % stage_idx].default_value, stg_paths, stage["a_ab_node"], input_key="Value", is_alpha=True)
        get_field_output_instructions(stg_node.inputs["Stage %s Output Cd Alpha" % stage_idx].default_value, stg_paths, stage["a_cd_node"], input_key="Value", is_alpha=True)
        get_field_output_instructions(stg_node.inputs["Stage %s Output Ab Cd Mux Sum Alpha" % stage_idx].default_value, stg_paths, stage["a_abcd_node"], input_key="A", is_alpha=True)

    final_node = None
    fbf_enum = FramebufferBlendFunctionEnum(stg_node.inputs["Framebuffer Blend Function"].default_value)
    if fbf_enum == FramebufferBlendFunctionEnum.alpha_blend:
        final_node = generate_alpha_blend_output(shader_data, stg_node, mat.node_tree, stg_paths, output_material_node)
    elif fbf_enum == FramebufferBlendFunctionEnum.multiply:
        final_node = generate_add_blend_output(shader_data, stg_node, mat.node_tree, stg_paths, output_material_node)
    elif fbf_enum == FramebufferBlendFunctionEnum.double_multiply:
        final_node = generate_add_blend_output(shader_data, stg_node, mat.node_tree, stg_paths, output_material_node)
    elif fbf_enum == FramebufferBlendFunctionEnum.add:
        final_node = generate_add_blend_output(shader_data, stg_node, mat.node_tree, stg_paths, output_material_node)
    elif fbf_enum == FramebufferBlendFunctionEnum.subtract:
        final_node = generate_add_blend_output(shader_data, stg_node, mat.node_tree, stg_paths, output_material_node)
    elif fbf_enum == FramebufferBlendFunctionEnum.component_min:
        final_node = generate_add_blend_output(shader_data, stg_node, mat.node_tree, stg_paths, output_material_node)
    elif fbf_enum == FramebufferBlendFunctionEnum.component_max:
        final_node = generate_add_blend_output(shader_data, stg_node, mat.node_tree, stg_paths, output_material_node)
    elif fbf_enum == FramebufferBlendFunctionEnum.alpha_multiply_add:
        final_node = generate_alpha_blend_output(shader_data, stg_node, mat.node_tree, stg_paths, output_material_node)

    if final_node is not None:
        emission_node = mat.node_tree.nodes.new("ShaderNodeEmission")
        light_path_node = mat.node_tree.nodes.new("ShaderNodeLightPath")
        mix_node = mat.node_tree.nodes.new("ShaderNodeMixShader")

        emission_node.location = Vector((-360.0, -140.0))
        light_path_node.location = Vector((-360.0, 380.0))
        mix_node.location = Vector((-180.0, 0.0))

        connect_inputs(mat.node_tree, light_path_node, "Is Camera Ray", mix_node, 0)
        connect_inputs(mat.node_tree, final_node, "Shader", mix_node, 2)
        connect_inputs(mat.node_tree, emission_node, "Emission", mix_node, 1)
        connect_inputs(mat.node_tree, mix_node, "Shader", output_material_node, "Surface")
        
        connect_inputs(mat.node_tree, stg_node, "Power", emission_node, 1)
        

        if len(shader_data["stages"]) == 0:
            connect_inputs(mat.node_tree, stg_node, "Map A", emission_node, 0)
        else:
            connect_inputs(mat.node_tree, stg_node, "Color Of Emitted Light", emission_node, 0)

def generate_shader_transparent_glass_simple(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node)

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    place_node(bdsf_principled, 1)

    base_map_texture = generate_image_node(mat, shader_data["diffuse map"], permutation_index, asset_cache, "halo1", report)
    if base_map_texture:
        base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        base_map_node.image = base_map_texture
        base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        place_node(base_map_node, 2)
        connect_inputs(mat.node_tree, base_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_glass(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    shader_flags = ShaderFlags(shader_data["flags"])
    shader_property_flags = GlassPropertiesFlags(shader_data["shader transparent glass flags"])

    output_material_node = get_output_material_node(mat)
    output_material_node.location = (0.0, 0.0)

    shader_transparent_glass = get_shader_node(mat.node_tree, HALO_1_SHADER_RESOURCES, "shader_transparent_glass")
    shader_transparent_glass.location = (-440.0, 0.0)
    shader_transparent_glass.name = "Shader Transparent Glass"

    connect_inputs(mat.node_tree, shader_transparent_glass, "Shader", output_material_node, "Surface")

    shader_transparent_glass.inputs["Simple Parameterization"].default_value = ShaderFlags.simple_parameterization in shader_flags
    shader_transparent_glass.inputs["Ignore Normals"].default_value = ShaderFlags.ignore_normals in shader_flags
    shader_transparent_glass.inputs["Transparent Lit"].default_value = ShaderFlags.transparent_lit in shader_flags
    shader_transparent_glass.inputs["Detail Level"].default_value = shader_data["detail level"]["value"]
    shader_transparent_glass.inputs["Power"].default_value = shader_data["power"]
    shader_transparent_glass.inputs["Color Of Emitted Light"].default_value = convert_to_blender_color(shader_data["color of emitted light"], True)
    shader_transparent_glass.inputs["Tint Color"].default_value = convert_to_blender_color(shader_data["tint color"], True)

    shader_transparent_glass.inputs["Material Type"].default_value = shader_data["material type"]["value"]

    shader_transparent_glass.inputs["Alpha Tested"].default_value = GlassPropertiesFlags.alpha_tested in shader_property_flags
    shader_transparent_glass.inputs["Decal"].default_value = GlassPropertiesFlags.decal in shader_property_flags
    shader_transparent_glass.inputs["Two Sided"].default_value = GlassPropertiesFlags.two_sided in shader_property_flags
    shader_transparent_glass.inputs["Bump Map Is Specular Mask"].default_value = GlassPropertiesFlags.bump_map_is_specular_mask in shader_property_flags

    shader_transparent_glass.inputs["Background Tint Color"].default_value = convert_to_blender_color(shader_data["background tint color"], True)
    shader_transparent_glass.inputs["Background Tint Map Scale"].default_value = shader_data["background tint map scale"]

    shader_transparent_glass.inputs["Reflection Type"].default_value = shader_data["reflection type"]["value"]
    shader_transparent_glass.inputs["Perpendicular Brightness"].default_value = shader_data["perpendicular brightness"]
    shader_transparent_glass.inputs["Perpendicular Tint Color"].default_value = convert_to_blender_color(shader_data["perpendicular tint color"], True)
    shader_transparent_glass.inputs["Parallel Brightness"].default_value = shader_data["parallel brightness"]
    shader_transparent_glass.inputs["Parallel Tint Color"].default_value = convert_to_blender_color(shader_data["parallel tint color"], True)
    shader_transparent_glass.inputs["Bump Map Scale"].default_value = shader_data["bump map scale"]

    shader_transparent_glass.inputs["Diffuse Map Scale"].default_value = shader_data["diffuse map scale"]
    shader_transparent_glass.inputs["Diffuse Detail Map Scale"].default_value = shader_data["diffuse detail map scale"]

    shader_transparent_glass.inputs["Specular Map Scale"].default_value = shader_data["specular map scale"]
    shader_transparent_glass.inputs["Specular Detail Map Scale"].default_value = shader_data["specular detail map scale"]

    background_tint_map_texture = generate_image_node(mat, shader_data["background tint map"], permutation_index, asset_cache, "halo1", report)
    if background_tint_map_texture:
        background_tint_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        background_tint_map_node.image = background_tint_map_texture
        background_tint_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        background_tint_map_node.location = Vector((-720.0, 0.0))
        connect_inputs(mat.node_tree, background_tint_map_node, "Color", shader_transparent_glass, "Background Tint Map")
        connect_inputs(mat.node_tree, background_tint_map_node, "Alpha", shader_transparent_glass, "Background Tint Map Alpha")

    reflection_map_texture = generate_image_node(mat, shader_data["reflection map"], permutation_index, asset_cache, "halo1", report)
    if reflection_map_texture:
        reflection_map_node = mat.node_tree.nodes.new("ShaderNodeTexEnvironment")
        texcoord_node = mat.node_tree.nodes.new("ShaderNodeTexCoord")
        reflection_map_node.image = reflection_map_texture
        reflection_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        reflection_map_node.location = Vector((-720.0, -300.0))
        texcoord_node.location = Vector((-900.0, -300.0))
        connect_inputs(mat.node_tree, reflection_map_node, "Color", shader_transparent_glass, "Reflection Map")
        connect_inputs(mat.node_tree, texcoord_node, "Reflection", reflection_map_node, "Vector")

    bump_map_texture = generate_image_node(mat, shader_data["bump map"], permutation_index, asset_cache, "halo1", report)
    bump_bitmap = None
    if bump_map_texture:
        bump_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        bump_map_node.image = bump_map_texture
        bump_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        bump_map_node.interpolation = 'Cubic'
        bump_map_node.image.colorspace_settings.name = 'Non-Color'
        bump_map_node.location = Vector((-720.0, -600.0))
        connect_inputs(mat.node_tree, bump_map_node, "Color", shader_transparent_glass, "Bump Map")
        connect_inputs(mat.node_tree, bump_map_node, "Alpha", shader_transparent_glass, "Bump Map Alpha")

        bump_bitmap = tag_interface.get_disk_asset(shader_data["bump map"]["path"], tag_common.h1_tag_groups.get(shader_data["bump map"]["group name"]))

    diffuse_map_texture = generate_image_node(mat, shader_data["diffuse map"], permutation_index, asset_cache, "halo1", report)
    if diffuse_map_texture:
        diffuse_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        diffuse_map_node.image = diffuse_map_texture
        diffuse_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        diffuse_map_node.location = Vector((-720.0, -900.0))
        connect_inputs(mat.node_tree, diffuse_map_node, "Color", shader_transparent_glass, "Diffuse Map")
        connect_inputs(mat.node_tree, diffuse_map_node, "Alpha", shader_transparent_glass, "Diffuse Map Alpha")

    diffuse_detail_map_texture = generate_image_node(mat, shader_data["diffuse detail map"], permutation_index, asset_cache, "halo1", report)
    if diffuse_detail_map_texture:
        diffuse_detail_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        diffuse_detail_map_node.image = diffuse_detail_map_texture
        diffuse_detail_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        diffuse_detail_map_node.location = Vector((-720.0, -1200.0))
        connect_inputs(mat.node_tree, diffuse_detail_map_node, "Color", shader_transparent_glass, "Diffuse Detail Map")
        connect_inputs(mat.node_tree, diffuse_detail_map_node, "Alpha", shader_transparent_glass, "Diffuse Detail Map Alpha")

    specular_map_texture = generate_image_node(mat, shader_data["specular map"], permutation_index, asset_cache, "halo1", report)
    if specular_map_texture:
        specular_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        specular_map_node.image = specular_map_texture
        specular_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        specular_map_node.location = Vector((-720.0, -1500.0))
        connect_inputs(mat.node_tree, specular_map_node, "Color", shader_transparent_glass, "Specular Map")
        connect_inputs(mat.node_tree, specular_map_node, "Alpha", shader_transparent_glass, "Specular Map Alpha")

    specular_detail_map_texture = generate_image_node(mat, shader_data["specular detail map"], permutation_index, asset_cache, "halo1", report)
    if specular_detail_map_texture:
        specular_detail_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        specular_detail_map_node.image = specular_detail_map_texture
        specular_detail_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        specular_detail_map_node.location = Vector((-720.0, -1800.0))
        connect_inputs(mat.node_tree, specular_detail_map_node, "Color", shader_transparent_glass, "Specular Detail Map")
        connect_inputs(mat.node_tree, specular_detail_map_node, "Alpha", shader_transparent_glass, "Specular Detail Map Alpha")

    if bump_bitmap is not None:
        shader_transparent_glass.inputs["Bump Map Strength"].default_value = bump_bitmap["Data"]["bump height"] * 15

def generate_shader_transparent_meter_simple(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node)

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    place_node(bdsf_principled, 1)

    base_map_texture = generate_image_node(mat, shader_data["meter map"], permutation_index, asset_cache, "halo1", report)
    if base_map_texture:
        base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        base_map_node.image = base_map_texture
        base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        place_node(base_map_node, 2)
        connect_inputs(mat.node_tree, base_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_meter(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    shader_flags = ShaderFlags(shader_data["flags"])
    shader_property_flags = MeterPropertiesFlags(shader_data["flags_1"])

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))

    stm_node = get_shader_node(mat.node_tree, HALO_1_SHADER_RESOURCES, "shader_transparent_meter")
    stm_node.name = "Shader Transparent Meter"
    stm_node.location = (-440.0, 0.0)

    connect_inputs(mat.node_tree, stm_node, "Shader", output_material_node, "Surface")

    stm_node.inputs["Simple Parameterization"].default_value = ShaderFlags.simple_parameterization in shader_flags
    stm_node.inputs["Ignore Normals"].default_value = ShaderFlags.ignore_normals in shader_flags
    stm_node.inputs["Transparent Lit"].default_value = ShaderFlags.transparent_lit in shader_flags
    stm_node.inputs["Detail Level"].default_value = shader_data["detail level"]["value"]
    stm_node.inputs["Power"].default_value = shader_data["power"]
    stm_node.inputs["Color Of Emitted Light"].default_value = convert_to_blender_color(shader_data["color of emitted light"], True)
    stm_node.inputs["Tint Color"].default_value = convert_to_blender_color(shader_data["tint color"], True)

    stm_node.inputs["Material Type"].default_value = shader_data["material type"]["value"]

    stm_node.inputs["Decal"].default_value = MeterPropertiesFlags.decal in shader_property_flags
    stm_node.inputs["Two Sided"].default_value = MeterPropertiesFlags.two_sided in shader_property_flags
    stm_node.inputs["Flash Color Is Negative"].default_value = MeterPropertiesFlags.flash_color_is_negative in shader_property_flags
    stm_node.inputs["Tint Mode 2"].default_value = MeterPropertiesFlags.tint_mode_2 in shader_property_flags
    stm_node.inputs["Unfiltered"].default_value = MeterPropertiesFlags.unfiltered in shader_property_flags

    stm_node.inputs["Gradient Min Color"].default_value = convert_to_blender_color(shader_data["gradient min color"], True)
    stm_node.inputs["Gradient Max Color"].default_value = convert_to_blender_color(shader_data["gradient max color"], True)
    stm_node.inputs["Background Color"].default_value = convert_to_blender_color(shader_data["background color"], True)
    stm_node.inputs["Flash Color"].default_value = convert_to_blender_color(shader_data["flash color"], True)
    stm_node.inputs["Meter Tint Color"].default_value = convert_to_blender_color(shader_data["meter tint color"], True)
    stm_node.inputs["Meter Transparency"].default_value = shader_data["meter transparency"]
    stm_node.inputs["Background Transparency"].default_value = shader_data["background transparency"]

    stm_node.inputs["Meter Brightness Source"].default_value = shader_data["meter brightness source"]["value"]
    stm_node.inputs["Flash Brightness Source"].default_value = shader_data["flash brightness source"]["value"]
    stm_node.inputs["Value Source"].default_value = shader_data["value source"]["value"]
    stm_node.inputs["Gradient Source"].default_value = shader_data["gradient source"]["value"]
    stm_node.inputs["Flash Extension Source"].default_value = shader_data["flash extension source"]["value"]

    base_map_texture = generate_image_node(mat, shader_data["map"], permutation_index, asset_cache, "halo1", report)
    if base_map_texture:
        base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        base_map_node.image = base_map_texture
        base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        base_map_node.location = Vector((-720.0, 0.0))
        connect_inputs(mat.node_tree, base_map_node, "Color", stm_node, "Meter Map")
        connect_inputs(mat.node_tree, base_map_node, "Alpha", stm_node, "Meter Map Alpha")

def generate_shader_transparent_plasma_simple(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node)

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    place_node(bdsf_principled, 1)

    base_map_texture = generate_image_node(mat, shader_data["primary noise map"], permutation_index, asset_cache, "halo1", report)
    if base_map_texture:
        base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        base_map_node.image = base_map_texture
        base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        place_node(base_map_node, 2)
        connect_inputs(mat.node_tree, base_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_plasma(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    shader_flags = ShaderFlags(shader_data["flags"])

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))

    stp_node = get_shader_node(mat.node_tree, HALO_1_SHADER_RESOURCES, "shader_transparent_plasma")
    stp_node.name = "Shader Transparent Plasma"
    stp_node.location = (-440.0, 0.0)

    connect_inputs(mat.node_tree, stp_node, "Shader", output_material_node, "Surface")

    stp_node.inputs["Simple Parameterization"].default_value = ShaderFlags.simple_parameterization in shader_flags
    stp_node.inputs["Ignore Normals"].default_value = ShaderFlags.ignore_normals in shader_flags
    stp_node.inputs["Transparent Lit"].default_value = ShaderFlags.transparent_lit in shader_flags
    stp_node.inputs["Detail Level"].default_value = shader_data["detail level"]["value"]
    stp_node.inputs["Power"].default_value = shader_data["power"]
    stp_node.inputs["Color Of Emitted Light"].default_value = convert_to_blender_color(shader_data["color of emitted light"], True)
    stp_node.inputs["Tint Color"].default_value = convert_to_blender_color(shader_data["tint color"], True)

    stp_node.inputs["Material Type"].default_value = shader_data["material type"]["value"]

    stp_node.inputs["Intensity Source"].default_value = shader_data["intensity source"]["value"]
    stp_node.inputs["Intensity Exponent"].default_value = shader_data["intensity exponent"]

    stp_node.inputs["Offset Source"].default_value = shader_data["offset source"]["value"]
    stp_node.inputs["Offset Amount"].default_value = shader_data["offset amount"]
    stp_node.inputs["Offset Exponent"].default_value = shader_data["offset exponent"]

    stp_node.inputs["Perpendicular Brightness"].default_value = shader_data["perpendicular brightness"]
    stp_node.inputs["Perpendicular Tint Color"].default_value = convert_to_blender_color(shader_data["perpendicular tint color"], True)
    stp_node.inputs["Parallel Brightness"].default_value = shader_data["parallel brightness"]
    stp_node.inputs["Parallel Tint Color"].default_value = convert_to_blender_color(shader_data["parallel tint color"], True)
    stp_node.inputs["Tint Color Source"].default_value = shader_data["tint color source"]["value"]

    stp_node.inputs["Primary Animation Period"].default_value = shader_data["animation period"]
    stp_node.inputs["Primary Animation Direction"].default_value = shader_data["animation direction"]
    stp_node.inputs["Primary Noise Map Scale"].default_value = shader_data["noise map scale"]

    stp_node.inputs["Secondary Animation Period"].default_value = shader_data["animation period_1"]
    stp_node.inputs["Secondary Animation Direction"].default_value = shader_data["animation direction_1"]
    stp_node.inputs["Secondary Noise Map Scale"].default_value = shader_data["noise map scale_1"]

    noise_map_texture = generate_image_node(mat, shader_data["noise map"], permutation_index, asset_cache, "halo1", report)
    if noise_map_texture:
        noise_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        noise_map_node.image = noise_map_texture
        noise_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        noise_map_node.location = Vector((-720.0, 0.0))
        connect_inputs(mat.node_tree, noise_map_node, "Color", stp_node, "Primary Noise Map")
        connect_inputs(mat.node_tree, noise_map_node, "Alpha", stp_node, "Primary Noise Map Alpha")

    noise1_map_texture = generate_image_node(mat, shader_data["noise map_1"], permutation_index, asset_cache, "halo1", report)
    if noise1_map_texture:
        noise1_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        noise1_map_node.image = noise1_map_texture
        noise1_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        noise1_map_node.location = Vector((-720.0, -300.0))
        connect_inputs(mat.node_tree, noise1_map_node, "Color", stp_node, "Secondary Noise Map")
        connect_inputs(mat.node_tree, noise1_map_node, "Alpha", stp_node, "Secondary Noise Map Alpha")

def generate_shader_transparent_water_simple(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node)

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    place_node(bdsf_principled, 1)

    base_map_texture = generate_image_node(mat, shader_data["base map"], permutation_index, asset_cache, "halo1", report)
    if base_map_texture:
        base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        base_map_node.image = base_map_texture
        base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        place_node(base_map_node, 2)
        connect_inputs(mat.node_tree, base_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_water(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    shader_flags = ShaderFlags(shader_data["flags"])
    shader_property_flags = WaterPropertiesFlags(shader_data["water flags"])

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))

    stw_node = get_shader_node(mat.node_tree, HALO_1_SHADER_RESOURCES, "shader_transparent_water")
    stw_node.name = "Shader Transparent Plasma"
    stw_node.location = (-440.0, 0.0)

    connect_inputs(mat.node_tree, stw_node, "Shader", output_material_node, "Surface")

    stw_node.inputs["Simple Parameterization"].default_value = ShaderFlags.simple_parameterization in shader_flags
    stw_node.inputs["Ignore Normals"].default_value = ShaderFlags.ignore_normals in shader_flags
    stw_node.inputs["Transparent Lit"].default_value = ShaderFlags.transparent_lit in shader_flags
    stw_node.inputs["Detail Level"].default_value = shader_data["detail level"]["value"]
    stw_node.inputs["Power"].default_value = shader_data["power"]
    stw_node.inputs["Color Of Emitted Light"].default_value = convert_to_blender_color(shader_data["color of emitted light"], True)
    stw_node.inputs["Tint Color"].default_value = convert_to_blender_color(shader_data["tint color"], True)

    stw_node.inputs["Material Type"].default_value = shader_data["material type"]["value"]

    stw_node.inputs["Base Map Alpha Modulates Reflection"].default_value = WaterPropertiesFlags.base_map_alpha_modulates_reflection in shader_property_flags
    stw_node.inputs["Base Map Color Modulates Background"].default_value = WaterPropertiesFlags.base_map_color_modulates_background in shader_property_flags
    stw_node.inputs["Atmospheric Fog"].default_value = WaterPropertiesFlags.atmospheric_fog in shader_property_flags
    stw_node.inputs["Draw Before Fog"].default_value = WaterPropertiesFlags.draw_before_fog in shader_property_flags
    stw_node.inputs["View Perpendicular Brightness"].default_value = shader_data["perpendicular brightness"]
    stw_node.inputs["View Perpendicular Tint Color"].default_value = convert_to_blender_color(shader_data["perpendicular tint color"], True)
    stw_node.inputs["View Parallel Brightness"].default_value = shader_data["parallel brightness"]
    stw_node.inputs["View Parallel Tint Color"].default_value = convert_to_blender_color(shader_data["parallel tint color"], True)
    stw_node.inputs["Ripple Animation Angle"].default_value = radians(shader_data["animation angle"])
    stw_node.inputs["Ripple Animation Velocity"].default_value = shader_data["animation velocity"]
    stw_node.inputs["Ripple Animation Scale"].default_value = shader_data["scale"]
    stw_node.inputs["Ripple Mipmap Levels"].default_value = shader_data["mipmap levels"]
    stw_node.inputs["Ripple Mipmap Fade Factor"].default_value = shader_data["mipmap fade factor"]
    stw_node.inputs["Ripple Mipmap Detail Bias"].default_value = shader_data["mipmap detail bias"]

    base_map_texture = generate_image_node(mat, shader_data["base map"], permutation_index, asset_cache, "halo1", report)
    if base_map_texture:
        base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        base_map_node.image = base_map_texture
        base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        base_map_node.extension = 'EXTEND'

        base_map_node.location = Vector((-720.0, 0.0))
        connect_inputs(mat.node_tree, base_map_node, "Color", stw_node, "Base Map")
        connect_inputs(mat.node_tree, base_map_node, "Alpha", stw_node, "Base Map Alpha")

    reflection_map_texture = generate_image_node(mat, shader_data["reflection map"], permutation_index, asset_cache, "halo1", report)
    if reflection_map_texture:
        reflection_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        reflection_map_node.image = reflection_map_texture
        reflection_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        reflection_map_node.location = Vector((-720.0, -300.0))
        connect_inputs(mat.node_tree, reflection_map_node, "Color", stw_node, "Reflection Map")
        connect_inputs(mat.node_tree, reflection_map_node, "Alpha", stw_node, "Reflection Map Alpha")

    ripple_map_texture = generate_image_node(mat, shader_data["maps"], permutation_index, asset_cache, "halo1", report)
    if ripple_map_texture:
        ripple_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        ripple_map_node.image = ripple_map_texture
        ripple_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        ripple_map_node.location = Vector((-720.0, -600.0))
        connect_inputs(mat.node_tree, ripple_map_node, "Color", stw_node, "Ripple Maps")
        connect_inputs(mat.node_tree, ripple_map_node, "Alpha", stw_node, "Ripple Maps Alpha")

    ripple_slots = ("A", "B", "C", "D")
    for ripple_idx, ripple_element in enumerate(shader_data["ripples"]):
        stw_node.inputs["Ripple %s" % ripple_slots[ripple_idx]].default_value = True
        stw_node.inputs["Ripple %s Contribution Factor" % ripple_slots[ripple_idx]].default_value = ripple_element["contribution factor"]
        stw_node.inputs["Ripple %s Animation Angle" % ripple_slots[ripple_idx]].default_value = radians(ripple_element["animation angle"])
        stw_node.inputs["Ripple %s Animation Velocity" % ripple_slots[ripple_idx]].default_value = ripple_element["animation velocity"]
        stw_node.inputs["Ripple %s Map Offset" % ripple_slots[ripple_idx]].default_value = ripple_element["map offset"]
        stw_node.inputs["Ripple %s Map Repeats" % ripple_slots[ripple_idx]].default_value = ripple_element["map repeats"]
        stw_node.inputs["Ripple %s Map Index" % ripple_slots[ripple_idx]].default_value = ripple_element["map index"]

