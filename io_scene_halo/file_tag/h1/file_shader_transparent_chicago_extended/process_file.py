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
from ....global_functions import tag_format
from .format import (
        ShaderAsset,
        RadiosityFlags,
        DetailLevelEnum,
        MaterialTypeEnum,
        ChicagoFlags,
        FirstMapTypeEnum,
        FramebufferBlendFunctionEnum,
        FramebufferFadeModeEnum,
        ChannelSourceEnum,
        MapFlags,
        MapFunctionEnum,
        FunctionEnum,
        ExtraFlags,
        )

XML_OUTPUT = False

def process_file(input_stream, report):
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
    SHADER.shader_body.chicago_flags = TAG.read_flag_unsigned_byte(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ChicagoFlags))
    SHADER.shader_body.first_map_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "first map type", FirstMapTypeEnum))
    SHADER.shader_body.framebuffer_blend_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "framebuffer blend function", FramebufferBlendFunctionEnum))
    SHADER.shader_body.framebuffer_fade_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "framebuffer fade mode", FramebufferFadeModeEnum))
    SHADER.shader_body.framebuffer_fade_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "framebuffer fade source", ChannelSourceEnum))
    input_stream.read(2) # Padding
    SHADER.shader_body.lens_flare_spacing = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "lens flare spacing"))
    SHADER.shader_body.lens_flare = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "lens flare"))
    SHADER.shader_body.extra_layers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "extra layers"))
    SHADER.shader_body._4_stage_maps_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "4 stage maps"))
    SHADER.shader_body._2_stage_maps_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "2 stage maps"))
    input_stream.read(2) # Padding
    SHADER.shader_body.extra_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "extra flags", ExtraFlags))
    input_stream.read(8) # Padding

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

    SHADER._4_stage_maps = []
    _4_stage_maps_node = tag_format.get_xml_node(XML_OUTPUT, SHADER.shader_body._4_stage_maps_tag_block.count, tag_node, "name", "4 stage maps")
    for _4_stage_map_idx in range(SHADER.shader_body._4_stage_maps_tag_block.count):
        _4_stage_map_element_node = None
        if XML_OUTPUT:
            _4_stage_map_element_node = TAG.xml_doc.createElement('element')
            _4_stage_map_element_node.setAttribute('index', str(_4_stage_map_idx))
            _4_stage_maps_node.appendChild(_4_stage_map_element_node)

        _4_stage_map = SHADER.Stage()
        _4_stage_map.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "flags", MapFlags))
        input_stream.read(42) # Padding
        _4_stage_map.color_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "color function", MapFunctionEnum))
        _4_stage_map.alpha_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "alpha function", MapFunctionEnum))
        input_stream.read(36) # Padding
        _4_stage_map.map_u_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "map u scale"))
        _4_stage_map.map_v_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "map v scale"))
        _4_stage_map.map_u_offset = TAG.read_float(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "map u offset"))
        _4_stage_map.map_v_offset = TAG.read_float(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "map v offset"))
        _4_stage_map.map_rotation = TAG.read_float(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "map rotation"))
        _4_stage_map.mipmap_bias = TAG.read_float(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "mipmap bias"))
        _4_stage_map.map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "map"))
        input_stream.read(40) # Padding
        _4_stage_map.u_animation_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "u animation source", ChannelSourceEnum))
        _4_stage_map.u_animation_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "u animation function", FunctionEnum))
        _4_stage_map.u_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "u animation period"))
        _4_stage_map.u_animation_phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "u animation phase"))
        _4_stage_map.u_animation_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "u animation scale"))
        _4_stage_map.v_animation_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "v animation source", ChannelSourceEnum))
        _4_stage_map.v_animation_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "v animation function", FunctionEnum))
        _4_stage_map.v_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "v animation period"))
        _4_stage_map.v_animation_phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "v animation phase"))
        _4_stage_map.v_animation_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "v animation scale"))
        _4_stage_map.rotation_animation_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "rotation animation source", ChannelSourceEnum))
        _4_stage_map.rotation_animation_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "rotation animation function", FunctionEnum))
        _4_stage_map.rotation_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "rotation animation period"))
        _4_stage_map.rotation_animation_phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "rotation animation phase"))
        _4_stage_map.rotation_animation_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "rotation animation scale"))
        _4_stage_map.rotation_animation_center = TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(_4_stage_map_element_node, "rotation animation center"))

        SHADER._4_stage_maps.append(_4_stage_map)

    for _4_stage_map_idx, _4_stage_map in enumerate(SHADER._4_stage_maps):
        _4_stage_map_element_node = None
        if XML_OUTPUT:
            _4_stage_map_element_node = _4_stage_maps_node.childNodes[_4_stage_map_idx]

        if _4_stage_map.map.name_length > 0:
            _4_stage_map.map.name = TAG.read_variable_string(input_stream, _4_stage_map.map.name_length, TAG)

        if XML_OUTPUT:
            map_node = tag_format.get_xml_node(XML_OUTPUT, 1, _4_stage_map_element_node, "name", "map")
            _4_stage_map.map.append_xml_attributes(map_node)

    SHADER._2_stage_maps = []
    _2_stage_maps_node = tag_format.get_xml_node(XML_OUTPUT, SHADER.shader_body._2_stage_maps_tag_block.count, tag_node, "name", "2 stage maps")
    for _2_stage_map_idx in range(SHADER.shader_body._2_stage_maps_tag_block.count):
        _2_stage_map_element_node = None
        if XML_OUTPUT:
            _2_stage_map_element_node = TAG.xml_doc.createElement('element')
            _2_stage_map_element_node.setAttribute('index', str(_2_stage_map_idx))
            _2_stage_maps_node.appendChild(_2_stage_map_element_node)

        _2_stage_map = SHADER.Stage()
        _2_stage_map.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "flags", MapFlags))
        input_stream.read(42) # Padding
        _2_stage_map.color_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "color function", MapFunctionEnum))
        _2_stage_map.alpha_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "alpha function", MapFunctionEnum))
        input_stream.read(36) # Padding
        _2_stage_map.map_u_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "map u scale"))
        _2_stage_map.map_v_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "map v scale"))
        _2_stage_map.map_u_offset = TAG.read_float(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "map u offset"))
        _2_stage_map.map_v_offset = TAG.read_float(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "map v offset"))
        _2_stage_map.map_rotation = TAG.read_float(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "map rotation"))
        _2_stage_map.mipmap_bias = TAG.read_float(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "mipmap bias"))
        _2_stage_map.map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "map"))
        input_stream.read(40) # Padding
        _2_stage_map.u_animation_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "u animation source", ChannelSourceEnum))
        _2_stage_map.u_animation_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "u animation function", FunctionEnum))
        _2_stage_map.u_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "u animation period"))
        _2_stage_map.u_animation_phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "u animation phase"))
        _2_stage_map.u_animation_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "u animation scale"))
        _2_stage_map.v_animation_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "v animation source", ChannelSourceEnum))
        _2_stage_map.v_animation_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "v animation function", FunctionEnum))
        _2_stage_map.v_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "v animation period"))
        _2_stage_map.v_animation_phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "v animation phase"))
        _2_stage_map.v_animation_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "v animation scale"))
        _2_stage_map.rotation_animation_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "rotation animation source", ChannelSourceEnum))
        _2_stage_map.rotation_animation_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "rotation animation function", FunctionEnum))
        _2_stage_map.rotation_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "rotation animation period"))
        _2_stage_map.rotation_animation_phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "rotation animation phase"))
        _2_stage_map.rotation_animation_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "rotation animation scale"))
        _2_stage_map.rotation_animation_center = TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(_2_stage_map_element_node, "rotation animation center"))

        SHADER._2_stage_maps.append(_2_stage_map)

    for _2_stage_map_idx, _2_stage_map in enumerate(SHADER._2_stage_maps):
        _2_stage_map_element_node = None
        if XML_OUTPUT:
            _2_stage_map_element_node = _2_stage_maps_node.childNodes[_2_stage_map_idx]

        if _2_stage_map.map.name_length > 0:
            _2_stage_map.map.name = TAG.read_variable_string(input_stream, _2_stage_map.map.name_length, TAG)

        if XML_OUTPUT:
            map_node = tag_format.get_xml_node(XML_OUTPUT, 1, _2_stage_map_element_node, "name", "map")
            _2_stage_map.map.append_xml_attributes(map_node)

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
