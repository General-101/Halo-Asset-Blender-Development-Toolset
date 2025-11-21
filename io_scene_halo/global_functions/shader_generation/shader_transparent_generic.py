import bpy

from enum import Flag, Enum, auto
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

class RadiosityFlags(Flag):
    simple_parameterization = auto()
    ignore_normals = auto()
    transparent_lit = auto()

class ShaderFlags(Flag):
    alpha_tested = auto()
    decal = auto()
    two_sided = auto()
    first_map_is_in_screenspace = auto()
    draw_before_water = auto()
    ignore_effect = auto()
    scale_first_map_with_distance = auto()
    numeric = auto()

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
    radiosity_flags = RadiosityFlags(shad_root["flags"])
    stg_node.inputs["Simple Parameterization"].default_value = RadiosityFlags.simple_parameterization in radiosity_flags
    stg_node.inputs["Ignore Normals"].default_value = RadiosityFlags.ignore_normals in radiosity_flags
    stg_node.inputs["Transparent Lit"].default_value = RadiosityFlags.transparent_lit in radiosity_flags
    stg_node.inputs["Detail Level"].default_value = shad_root["detail level"]["value"]
    stg_node.inputs["Power"].default_value = shad_root["power"]

    r0, g0, b0 = shad_root["color of emitted light"].values()
    r1, g1, b1 = shad_root["tint color"].values()
    stg_node.inputs["Color Of Emitted Light"].default_value = (r0, g0, b0, 1)
    stg_node.inputs["Tint Color"].default_value = (r1, g1, b1, 1)

    stg_node.inputs["Material Type"].default_value = shad_root["material type"]["value"]
    stg_node.inputs["Numeric Counter Limit"].default_value = shad_root["numeric counter limit"]

    shader_flags = ShaderFlags(shad_root["flags_1"])
    stg_node.inputs["Alpha Tested"].default_value = ShaderFlags.alpha_tested in shader_flags
    stg_node.inputs["Decal"].default_value = ShaderFlags.decal in shader_flags
    stg_node.inputs["Two Sided"].default_value = ShaderFlags.two_sided in shader_flags
    stg_node.inputs["First Map Is In Screenspace"].default_value = ShaderFlags.first_map_is_in_screenspace in shader_flags
    stg_node.inputs["Draw Before Water"].default_value = ShaderFlags.draw_before_water in shader_flags
    stg_node.inputs["Ignore Effect"].default_value = ShaderFlags.ignore_effect in shader_flags
    stg_node.inputs["Scale First Map With Distance"].default_value = ShaderFlags.scale_first_map_with_distance in shader_flags
    stg_node.inputs["Numeric"].default_value = ShaderFlags.numeric in shader_flags

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

        x, y = map_element["rotation animation center"]
        stg_node.inputs["Map %s Rotation Animation Center X" % map_key].default_value = x
        stg_node.inputs["Map %s Rotation Animation Center Y" % map_key].default_value = y

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
            #place_node(map_d_node, stage_offset - 4, 6)
            connect_inputs(node_tree, output_node, output_key, seperate_node, "Color")
            connect_inputs(node_tree, seperate_node, "Blue", input_node, input_key)
        elif field_enum == InputAlphaEnum.map_blue_1:
            output_node, output_key = stg_paths["map_b_color"]
            seperate_node = node_tree.nodes.new("ShaderNodeSeparateColor")
            #place_node(map_d_node, stage_offset - 4, 6)
            connect_inputs(node_tree, output_node, output_key, seperate_node, "Color")
            connect_inputs(node_tree, seperate_node, "Blue", input_node, input_key)
        elif field_enum == InputAlphaEnum.map_blue_2:
            output_node, output_key = stg_paths["map_c_color"]
            seperate_node = node_tree.nodes.new("ShaderNodeSeparateColor")
            #place_node(map_d_node, stage_offset - 4, 6)
            connect_inputs(node_tree, output_node, output_key, seperate_node, "Color")
            connect_inputs(node_tree, seperate_node, "Blue", input_node, input_key)
        elif field_enum == InputAlphaEnum.map_blue_3:
            output_node, output_key = stg_paths["map_d_color"]
            seperate_node = node_tree.nodes.new("ShaderNodeSeparateColor")
            #place_node(map_d_node, stage_offset - 4, 6)
            connect_inputs(node_tree, output_node, output_key, seperate_node, "Color")
            connect_inputs(node_tree, seperate_node, "Blue", input_node, input_key)
        elif field_enum == InputAlphaEnum.vertex_blue_0_blue_light:
            scratch_node = stg_paths["vertex_0_color"]
            if scratch_node is None:
                input_node.inputs[input_key].default_value = vertex_alpha
            else:
                output_node, output_key = stg_paths["vertex_0_color"]
                seperate_node = node_tree.nodes.new("ShaderNodeSeparateColor")
                #place_node(map_d_node, stage_offset - 4, 6)
                connect_inputs(node_tree, output_node, output_key, seperate_node, "Color")
                connect_inputs(node_tree, seperate_node, "Blue", input_node, input_key)
        elif field_enum == InputAlphaEnum.vertex_blue_1_fade_parallel:
            scratch_node = stg_paths["vertex_1_color"]
            if scratch_node is None:
                input_node.inputs[input_key].default_value = vertex_alpha
            else:
                output_node, output_key = stg_paths["vertex_1_color"]
                seperate_node = node_tree.nodes.new("ShaderNodeSeparateColor")
                #place_node(map_d_node, stage_offset - 4, 6)
                connect_inputs(node_tree, output_node, output_key, seperate_node, "Color")
                connect_inputs(node_tree, seperate_node, "Blue", input_node, input_key)
        elif field_enum == InputAlphaEnum.scratch_blue_0:
            scratch_node = stg_paths["scratch_0_color"]
            if scratch_node is None:
                input_node.inputs[input_key].default_value = scratch_alpha
            else:
                output_node, output_key = stg_paths["scratch_0_color"]
                seperate_node = node_tree.nodes.new("ShaderNodeSeparateColor")
                #place_node(map_d_node, stage_offset - 4, 6)
                connect_inputs(node_tree, output_node, output_key, seperate_node, "Color")
                connect_inputs(node_tree, seperate_node, "Blue", input_node, input_key)
        elif field_enum == InputAlphaEnum.scratch_blue_1:
            scratch_node = stg_paths["scratch_1_color"]
            if scratch_node is None:
                input_node.inputs[input_key].default_value = scratch_alpha
            else:
                output_node, output_key = stg_paths["scratch_1_color"]
                seperate_node = node_tree.nodes.new("ShaderNodeSeparateColor")
                #place_node(map_d_node, stage_offset - 4, 6)
                connect_inputs(node_tree, output_node, output_key, seperate_node, "Color")
                connect_inputs(node_tree, seperate_node, "Blue", input_node, input_key)
        elif field_enum == InputAlphaEnum.constant_blue_0:
            seperate_node = node_tree.nodes.new("ShaderNodeSeparateColor")
            #place_node(map_d_node, stage_offset - 4, 6)
            connect_inputs(node_tree, stg_node, "Stage %s Color" % stg_idx, seperate_node, "Color")
            connect_inputs(node_tree, seperate_node, "Blue", input_node, input_key)
        elif field_enum == InputAlphaEnum.constant_blue_1:
            seperate_node = node_tree.nodes.new("ShaderNodeSeparateColor")
            #place_node(map_d_node, stage_offset - 4, 6)
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

    c_abcd_node = get_resource_node(node_tree, get_output_mapping_name(stage_element["output mapping color"]["value"]))
    c_abcd_node.name = "color_abcd_stage"
    place_node(c_abcd_node, 1 + stage_offset)

    c_mix_abcd_node = None
    c_add_abcd_node = None
    stage_flags = StageFlags(stage_element["flags"])
    if StageFlags.color_mux in stage_flags:
        c_mix_abcd_node = get_resource_node(node_tree, "ABCD Mux")
        c_mix_abcd_node.name = "color_mix_abcd_stage"
        place_node(c_mix_abcd_node, 2 + stage_offset, 2)
    else:
        c_add_abcd_node = node_tree.nodes.new(type="ShaderNodeMix")
        c_add_abcd_node.name = "color_add_abcd_stage"
        c_add_abcd_node.data_type = 'RGBA'
        c_add_abcd_node.blend_type = 'ADD'
        c_add_abcd_node.inputs[0].default_value = 1.0
        place_node(c_add_abcd_node, 2 + stage_offset)


    c_ab_node = get_resource_node(node_tree, "Output Function")
    c_ab_node.name = "color_ab_stage"
    if OutputFunctionEnum(stage_element["output ab function"]["value"]) == OutputFunctionEnum.dot_product:
        c_ab_node.inputs["Multiply/Dot Product"].default_value = True

    place_node(c_ab_node, 3 + stage_offset)

    c_cd_node = get_resource_node(node_tree, "Output Function")
    c_cd_node.name = "color_cd_stage"
    if OutputFunctionEnum(stage_element["output cd function"]["value"]) == OutputFunctionEnum.dot_product:
        c_ab_node.inputs["Multiply/Dot Product"].default_value = True

    place_node(c_cd_node, 3 + stage_offset, 2)

    c_a_node = get_resource_node(node_tree, get_input_mapping_name(stage_element["input a mapping"]["value"]))
    c_a_node.name = "color_a_stage"
    place_node(c_a_node, 4 + stage_offset)

    c_b_node = get_resource_node(node_tree, get_input_mapping_name(stage_element["input b mapping"]["value"]))
    c_b_node.name = "color_b_stage"
    place_node(c_b_node, 4 + stage_offset, 1)

    c_c_node = get_resource_node(node_tree, get_input_mapping_name(stage_element["input c mapping"]["value"]))
    c_c_node.name = "color_c_stage"
    place_node(c_c_node, 4 + stage_offset, 2)

    c_d_node = get_resource_node(node_tree, get_input_mapping_name(stage_element["input d mapping"]["value"]))
    c_d_node.name = "color_d_stage"
    place_node(c_d_node, 4 + stage_offset, 3)

    a_abcd_node = get_resource_node(node_tree, get_output_mapping_name(stage_element["output mapping alpha"]["value"], True))
    a_abcd_node.name = "alpha_abcd_stage"
    place_node(a_abcd_node, 1 + stage_offset, 5)

    a_mix_abcd_node = None
    a_add_abcd_node = None
    if StageFlags.alpha_mux in stage_flags:
        a_mix_abcd_node = get_resource_node(node_tree, "ABCD Mux")
        a_mix_abcd_node.name = "alpha_mix_abcd_stage"
        place_node(a_mix_abcd_node, 2 + stage_offset, 7)
    else:
        a_add_abcd_node = node_tree.nodes.new(type="ShaderNodeMath")
        a_add_abcd_node.name = "alpha_add_abcd_stage"
        place_node(a_add_abcd_node, 2 + stage_offset, 5)

    a_ab_node = node_tree.nodes.new(type="ShaderNodeMath")
    a_ab_node.name = "alpha_ab_stage"
    a_ab_node.operation = 'MULTIPLY'
    place_node(a_ab_node, 3 + stage_offset, 5)

    a_cd_node = node_tree.nodes.new(type="ShaderNodeMath")
    a_cd_node.name = "alpha_cd_stage"
    a_cd_node.operation = 'MULTIPLY'
    place_node(a_cd_node, 3 + stage_offset, 7)

    a_a_node = get_resource_node(node_tree, get_input_mapping_name(stage_element["input a mapping alpha"]["value"], True))
    a_a_node.name = "alpha_a_stage"
    place_node(a_a_node, 4 + stage_offset, 5)

    a_b_node = get_resource_node(node_tree, get_input_mapping_name(stage_element["input b mapping alpha"]["value"], True))
    a_b_node.name = "alpha_b_stage"
    place_node(a_b_node, 4 + stage_offset, 6)

    a_c_node = get_resource_node(node_tree, get_input_mapping_name(stage_element["input c mapping alpha"]["value"], True))
    a_c_node.name = "alpha_c_stage"
    place_node(a_c_node, 4 + stage_offset, 7)

    a_d_node = get_resource_node(node_tree, get_input_mapping_name(stage_element["input d mapping alpha"]["value"], True))
    a_d_node.name = "alpha_d_stage"
    place_node(a_d_node, 4 + stage_offset, 8)

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

def get_resource_node(tree, group_name):
    if not bpy.data.node_groups.get(group_name):
        with bpy.data.libraries.load(HALO_1_SHADER_RESOURCES) as (data_from, data_to):
            data_to.node_groups.append(data_from.node_groups[data_from.node_groups.index(group_name)])

    group_node = tree.nodes.new('ShaderNodeGroup')
    group_node.node_tree = bpy.data.node_groups.get(group_name)

    return group_node

def generate_alpha_blend_output(node_tree, stg_paths, output_material_node):
    transparent_node = node_tree.nodes.new("ShaderNodeBsdfTransparent")
    diffuse_node = node_tree.nodes.new("ShaderNodeBsdfDiffuse")
    mix_node = node_tree.nodes.new("ShaderNodeMixShader")

    #place_node(map_d_node, stage_offset - 4, 6)
    #place_node(map_d_node, stage_offset - 4, 6)
    #place_node(map_d_node, stage_offset - 4, 6)

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
    connect_inputs(node_tree, mix_node, "Shader", output_material_node, "Surface")

def generate_add_blend_output(node_tree, stg_paths, output_material_node):
    emission_node = node_tree.nodes.new("ShaderNodeEmission")
    transparent_node = node_tree.nodes.new("ShaderNodeBsdfTransparent")
    add_node = node_tree.nodes.new("ShaderNodeAddShader")

    #place_node(map_d_node, stage_offset - 4, 6)
    #place_node(map_d_node, stage_offset - 4, 6)
    #place_node(map_d_node, stage_offset - 4, 6)

    if stg_paths["scratch_0_color"] is None:
        emission_node.inputs["Color"].default_value = (0, 0, 0, 1)
    else:
        output_node, output_key = stg_paths["scratch_0_color"]
        connect_inputs(node_tree, output_node, output_key, emission_node, "Color")

    connect_inputs(node_tree, emission_node, "Emission", add_node, 0)
    connect_inputs(node_tree, transparent_node, "BSDF", add_node, 1)
    connect_inputs(node_tree, add_node, "Shader", output_material_node, "Surface")

def get_scale(field_value):
    scale_value = 1.0
    if field_value == 0.0:
        scale_value = field_value
    return scale_value

def generate_texture_mapping(node_tree, stg_node, map_idx, input_node, input_key):
    mapping_node = node_tree.nodes.new("ShaderNodeMapping")
    uv_node = node_tree.nodes.new("ShaderNodeUVMap")
    texture_pan_node = get_resource_node(node_tree, "Halo Texture Pan")

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

def generate_shader_transparent_generic(mat, shader_asset, permutation_index, asset_cache, report):
    tag_groups = tag_common.h1_tag_groups
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node, 0)

    stg_node = get_resource_node(mat.node_tree, "shader_transparent_generic")
    stg_node.name = "Shader Transparent Generic"
    set_stg_values(shader_data, stg_node)
    stage_groups = []
    stage_idx = 0
    for stage_idx, stage_element in enumerate(reversed(shader_data["stages"])):
        stage_groups.append(create_stages(mat.node_tree, stage_element, stage_idx))

    stage_offset = (stage_idx + 1) * 4
    place_node(stg_node, stage_offset + 1)

    map_tag_refs = [None, None, None, None]
    for map_idx, map_element in enumerate(shader_data["maps"]):
        map_tag_refs[map_idx] = map_element["map"]

    if map_tag_refs[0] is not None:
        map_a_texture = generate_image_node(mat, map_tag_refs[0], permutation_index, asset_cache, "halo1", report)
        if map_a_texture:
            map_a_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            map_a_node.image = map_a_texture
            map_a_node.image.alpha_mode = 'CHANNEL_PACKED'
            place_node(map_a_node, stage_offset - 4)
            connect_inputs(mat.node_tree, map_a_node, "Color", stg_node, "Map A Color")
            connect_inputs(mat.node_tree, map_a_node, "Alpha", stg_node, "Map A Alpha")
            generate_texture_mapping(mat.node_tree, stg_node, "A", map_a_node, "Vector")

    if map_tag_refs[1] is not None:
        map_b_texture = generate_image_node(mat, map_tag_refs[1], permutation_index, asset_cache, "halo1", report)
        if map_b_texture:
            map_b_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            map_b_node.image = map_b_texture
            map_b_node.image.alpha_mode = 'CHANNEL_PACKED'
            place_node(map_b_node, stage_offset - 4, 2)
            connect_inputs(mat.node_tree, map_b_node, "Color", stg_node, "Map B Color")
            connect_inputs(mat.node_tree, map_b_node, "Alpha", stg_node, "Map B Alpha")
            generate_texture_mapping(mat.node_tree, stg_node, "B", map_b_node, "Vector")

    if map_tag_refs[2] is not None:
        map_c_texture = generate_image_node(mat, map_tag_refs[2], permutation_index, asset_cache, "halo1", report)
        if map_c_texture:
            map_c_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            map_c_node.image = map_c_texture
            map_c_node.image.alpha_mode = 'CHANNEL_PACKED'
            place_node(map_c_node, stage_offset - 4, 4)
            connect_inputs(mat.node_tree, map_c_node, "Color", stg_node, "Map C Color")
            connect_inputs(mat.node_tree, map_c_node, "Alpha", stg_node, "Map C Alpha")
            generate_texture_mapping(mat.node_tree, stg_node, "C", map_c_node, "Vector")

    if map_tag_refs[3] is not None:
        map_d_texture = generate_image_node(mat, map_tag_refs[3], permutation_index, asset_cache, "halo1", report)
        if map_d_texture:
            map_d_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            map_d_node.image = map_d_texture
            map_d_node.image.alpha_mode = 'CHANNEL_PACKED'
            place_node(map_d_node, stage_offset - 4, 6)
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

    fbf_enum = FramebufferBlendFunctionEnum(stg_node.inputs["Framebuffer Blend Function"].default_value)
    if fbf_enum == FramebufferBlendFunctionEnum.alpha_blend:
        generate_alpha_blend_output(mat.node_tree, stg_paths, output_material_node)
    elif fbf_enum == FramebufferBlendFunctionEnum.multiply:
        generate_add_blend_output(mat.node_tree, stg_paths, output_material_node)
    elif fbf_enum == FramebufferBlendFunctionEnum.double_multiply:
        generate_add_blend_output(mat.node_tree, stg_paths, output_material_node)
    elif fbf_enum == FramebufferBlendFunctionEnum.add:
        generate_add_blend_output(mat.node_tree, stg_paths, output_material_node)
    elif fbf_enum == FramebufferBlendFunctionEnum.subtract:
        generate_add_blend_output(mat.node_tree, stg_paths, output_material_node)
    elif fbf_enum == FramebufferBlendFunctionEnum.component_min:
        generate_add_blend_output(mat.node_tree, stg_paths, output_material_node)
    elif fbf_enum == FramebufferBlendFunctionEnum.component_max:
        generate_add_blend_output(mat.node_tree, stg_paths, output_material_node)
    elif fbf_enum == FramebufferBlendFunctionEnum.alpha_multiply_add:
        generate_alpha_blend_output(mat.node_tree, stg_paths, output_material_node)
