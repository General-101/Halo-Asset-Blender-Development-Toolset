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

from xml.dom import minidom
from .format import (
        ShaderAsset,
        RadiosityFlags,
        DetailLevelEnum,
        MaterialTypeEnum,
        GenericFlags,
        FirstMapTypeEnum,
        FramebufferBlendFunctionEnum,
        FramebufferFadeModeEnum,
        ChannelSourceEnum,
        MapFlags,
        FunctionEnum,
        StageFlags,
        ColorSourceEnum,
        ColorInputEnum,
        InputMappingEnum,
        ColorOutputEnum,
        ColorOutputFunctionEnum,
        OutputMappingEnum,
        AlphaInputEnum,
        AlphaOutputEnum
        )

XML_OUTPUT = False

def process_file(input_stream, tag_format, report):
    TAG = tag_format.TagAsset()
    SHADER = ShaderAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    SHADER.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    SHADER.shader_body = SHADER.ShaderBody()
    SHADER.shader_body.radiosity_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", RadiosityFlags))
    SHADER.shader_body.detail_level = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "detail level", DetailLevelEnum))
    SHADER.shader_body.power = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "power"))
    SHADER.shader_body.color_of_emitted_light = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "color of emitted light"))
    SHADER.shader_body.light_tint_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "tint color"))
    input_stream.read(2) # Padding
    SHADER.shader_body.material_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "material type", MaterialTypeEnum))
    input_stream.read(4) # Padding
    SHADER.shader_body.numeric_counter_limit = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(tag_node, "numeric counter limit"))
    SHADER.shader_body.chicago_flags = TAG.read_flag_unsigned_byte(input_stream, TAG, tag_format.XMLData(tag_node, "flags", GenericFlags))
    SHADER.shader_body.first_map_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "first map type", FirstMapTypeEnum))
    SHADER.shader_body.framebuffer_blend_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "framebuffer blend function", FramebufferBlendFunctionEnum))
    SHADER.shader_body.framebuffer_fade_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "framebuffer fade mode", FramebufferFadeModeEnum))
    SHADER.shader_body.framebuffer_fade_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "framebuffer fade source", ChannelSourceEnum))
    input_stream.read(2) # Padding
    SHADER.shader_body.lens_flare_spacing = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "lens flare spacing"))
    SHADER.shader_body.lens_flare = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "lens flare"))
    SHADER.shader_body.extra_layers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "extra layers"))
    SHADER.shader_body.maps_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "maps"))
    SHADER.shader_body.stages_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "stages"))

    lens_flare_name_length = SHADER.shader_body.lens_flare.name_length
    if lens_flare_name_length > 0:
        SHADER.shader_body.lens_flare.name = TAG.read_variable_string(input_stream, lens_flare_name_length, TAG)

    if XML_OUTPUT:
        lens_flare_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "lens flare")
        SHADER.shader_body.lens_flare.append_xml_attributes(lens_flare_node)

    SHADER.extra_layers = []
    extra_layers_node = tag_format.get_xml_node(XML_OUTPUT, SHADER.shader_body.extra_layers_tag_block.count, tag_node, "name", "extra layers")
    for extra_layer_idx in range(SHADER.shader_body.extra_layers_tag_block.count):
        extra_layer_element_node = None
        if XML_OUTPUT:
            extra_layer_element_node = TAG.xml_doc.createElement('element')
            extra_layer_element_node.setAttribute('index', str(extra_layer_idx))
            extra_layers_node.appendChild(extra_layer_element_node)

        SHADER.extra_layers.append(TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(extra_layer_element_node, "shader")))

    for extra_layer_idx, extra_layer in enumerate(SHADER.extra_layers):
        extra_layer_element_node = None
        if XML_OUTPUT:
            extra_layer_element_node = extra_layers_node.childNodes[extra_layer_idx]

        if extra_layer.name_length > 0:
            extra_layer.name = TAG.read_variable_string(input_stream, extra_layer.name_length, TAG)

        if XML_OUTPUT:
            shader_node = tag_format.get_xml_node(XML_OUTPUT, 1, extra_layer_element_node, "name", "shader")
            extra_layer.append_xml_attributes(shader_node)

    SHADER.maps = []
    maps_node = tag_format.get_xml_node(XML_OUTPUT, SHADER.shader_body.maps_tag_block.count, tag_node, "name", "maps")
    for map_idx in range(SHADER.shader_body.maps_tag_block.count):
        map_element_node = None
        if XML_OUTPUT:
            map_element_node = TAG.xml_doc.createElement('element')
            map_element_node.setAttribute('index', str(map_idx))
            maps_node.appendChild(map_element_node)

        map = SHADER.Map()
        map.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(map_element_node, "flags", MapFlags))
        input_stream.read(2) # Padding
        map.map_u_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(map_element_node, "map u scale"))
        map.map_v_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(map_element_node, "map v scale"))
        map.map_u_offset = TAG.read_float(input_stream, TAG, tag_format.XMLData(map_element_node, "map u offset"))
        map.map_v_offset = TAG.read_float(input_stream, TAG, tag_format.XMLData(map_element_node, "map v offset"))
        map.map_rotation = TAG.read_float(input_stream, TAG, tag_format.XMLData(map_element_node, "map rotation"))
        map.mipmap_bias = TAG.read_float(input_stream, TAG, tag_format.XMLData(map_element_node, "mipmap bias"))
        map.map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(map_element_node, "map"))
        map.u_animation_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(map_element_node, "u animation source", ChannelSourceEnum))
        map.u_animation_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(map_element_node, "u animation function", FunctionEnum))
        map.u_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(map_element_node, "u animation period"))
        map.u_animation_phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(map_element_node, "u animation phase"))
        map.u_animation_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(map_element_node, "u animation scale"))
        map.v_animation_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(map_element_node, "v animation source", ChannelSourceEnum))
        map.v_animation_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(map_element_node, "v animation function", FunctionEnum))
        map.v_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(map_element_node, "v animation period"))
        map.v_animation_phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(map_element_node, "v animation phase"))
        map.v_animation_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(map_element_node, "v animation scale"))
        map.rotation_animation_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(map_element_node, "rotation animation source", ChannelSourceEnum))
        map.rotation_animation_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(map_element_node, "rotation animation function", FunctionEnum))
        map.rotation_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(map_element_node, "rotation animation period"))
        map.rotation_animation_phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(map_element_node, "rotation animation phase"))
        map.rotation_animation_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(map_element_node, "rotation animation scale"))
        map.rotation_animation_center = TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(map_element_node, "rotation animation center"))

        SHADER.maps.append(map)

    for map_idx, map in enumerate(SHADER.maps):
        map_element_node = None
        if XML_OUTPUT:
            map_element_node = maps_node.childNodes[map_idx]

        if map.map.name_length > 0:
            map.map.name = TAG.read_variable_string(input_stream, map.map.name_length, TAG)

        if XML_OUTPUT:
            map_node = tag_format.get_xml_node(XML_OUTPUT, 1, map_element_node, "name", "map")
            map.map.append_xml_attributes(map_node)

    SHADER.stages = []
    stages_node = tag_format.get_xml_node(XML_OUTPUT, SHADER.shader_body.stages_tag_block.count, tag_node, "name", "stages")
    for stage_idx in range(SHADER.shader_body.stages_tag_block.count):
        stage_element_node = None
        if XML_OUTPUT:
            stage_element_node = TAG.xml_doc.createElement('element')
            stage_element_node.setAttribute('index', str(stage_idx))
            stages_node.appendChild(stage_element_node)

        stage = SHADER.Stage()
        stage.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "flags", StageFlags))
        input_stream.read(2) # Padding
        stage.color0_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "color0 source", ColorSourceEnum))
        stage.color0_animation_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "color0 animation function", FunctionEnum))
        stage.color0_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(stage_element_node, "color0 animation period"))
        stage.color0_animation_lower_bound = TAG.read_argb(input_stream, TAG, tag_format.XMLData(stage_element_node, "color0 animation lower bound"))
        stage.color0_animation_upper_bound = TAG.read_argb(input_stream, TAG, tag_format.XMLData(stage_element_node, "color0 animation upper bound"))
        stage.color1 = TAG.read_argb(input_stream, TAG, tag_format.XMLData(stage_element_node, "color1"))
        stage.color_input_a = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "color input a", ColorInputEnum))
        stage.color_input_a_mapping = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "color input a mapping", InputMappingEnum))
        stage.color_input_b = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "color input b", ColorInputEnum))
        stage.color_input_b_mapping = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "color input b mapping", InputMappingEnum))
        stage.color_input_c = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "color input c", ColorInputEnum))
        stage.color_input_c_mapping = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "color input c mapping", InputMappingEnum))
        stage.color_input_d = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "color input d", ColorInputEnum))
        stage.color_input_d_mapping = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "color input d mapping", InputMappingEnum))
        stage.color_output_ab = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "color output ab", ColorOutputEnum))
        stage.color_output_ab_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "color output ab function", ColorOutputFunctionEnum))
        stage.color_output_cd = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "color output cd", ColorOutputEnum))
        stage.color_output_cd_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "color output cd function", ColorOutputFunctionEnum))
        stage.color_output_ab_cd = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "color output ab cd", ColorOutputEnum))
        stage.color_output_mapping = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "color output mapping", OutputMappingEnum))
        stage.alpha_input_a = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "alpha input a", AlphaInputEnum))
        stage.alpha_input_a_mapping = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "alpha input a mapping", InputMappingEnum))
        stage.alpha_input_b = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "alpha input b", AlphaInputEnum))
        stage.alpha_input_b_mapping = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "alpha input b mapping", InputMappingEnum))
        stage.alpha_input_c = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "alpha input c", AlphaInputEnum))
        stage.alpha_input_c_mapping = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "alpha input c mapping", InputMappingEnum))
        stage.alpha_input_d = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "alpha input d", AlphaInputEnum))
        stage.alpha_input_d_mapping = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "alpha input d mapping", InputMappingEnum))
        stage.alpha_output_ab = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "alpha output ab", AlphaOutputEnum))
        stage.alpha_output_cd = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "alpha output cd", AlphaOutputEnum))
        stage.alpha_output_ab_cd = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "alpha output ab cd", AlphaOutputEnum))
        stage.alpha_output_mapping = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(stage_element_node, "alpha output mapping", OutputMappingEnum))

        SHADER.stages.append(stage)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, SHADER.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return SHADER
