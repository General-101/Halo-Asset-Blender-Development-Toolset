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
        WaterFlags
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
    SHADER.shader_body.water_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", WaterFlags))
    input_stream.read(34) # Padding
    SHADER.shader_body.base_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "base map"))
    input_stream.read(16) # Padding
    SHADER.shader_body.view_perpendicular_brightness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "view perpendicular brightness"))
    SHADER.shader_body.view_perpendicular_tint_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "view perpendicular tint color"))
    SHADER.shader_body.view_parallel_brightness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "view parallel brightness"))
    SHADER.shader_body.view_parallel_tint_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "view parallel tint color"))
    input_stream.read(16) # Padding
    SHADER.shader_body.reflection_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "reflection map"))
    input_stream.read(16) # Padding
    SHADER.shader_body.ripple_animation_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "ripple animation angle"))
    SHADER.shader_body.ripple_animation_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ripple animation velocity"))
    SHADER.shader_body.ripple_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ripple scale"))
    SHADER.shader_body.ripple_maps = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "ripple maps"))
    SHADER.shader_body.ripple_mipmap_levels = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "ripple mipmap levels"))
    input_stream.read(2) # Padding
    SHADER.shader_body.ripple_mipmap_fade_factor = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "view parallel brightness"))
    SHADER.shader_body.ripple_mipmap_detail_bias = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "view parallel brightness"))
    input_stream.read(64) # Padding
    SHADER.shader_body.ripples_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ripples"))
    input_stream.read(16) # Padding

    base_map_name_length = SHADER.shader_body.base_map.name_length
    reflection_map_name_length = SHADER.shader_body.reflection_map.name_length
    ripple_maps_name_length = SHADER.shader_body.ripple_maps.name_length
    if base_map_name_length > 0:
        SHADER.shader_body.base_map.name = TAG.read_variable_string(input_stream, base_map_name_length, TAG)

    if reflection_map_name_length > 0:
        SHADER.shader_body.reflection_map.name = TAG.read_variable_string(input_stream, reflection_map_name_length, TAG)

    if ripple_maps_name_length > 0:
        SHADER.shader_body.ripple_maps.name = TAG.read_variable_string(input_stream, ripple_maps_name_length, TAG)

    if XML_OUTPUT:
        base_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "base map")
        reflection_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "reflection map")
        ripple_maps_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "ripple maps")
        SHADER.shader_body.base_map.append_xml_attributes(base_map_node)
        SHADER.shader_body.reflection_map.append_xml_attributes(reflection_map_node)
        SHADER.shader_body.ripple_maps.append_xml_attributes(ripple_maps_node)
        
    SHADER.ripples = []
    ripples_node = tag_format.get_xml_node(XML_OUTPUT, SHADER.shader_body.ripples_tag_block.count, tag_node, "name", "ripples")
    for ripple_idx in range(SHADER.shader_body.ripples_tag_block.count):
        ripple_element_node = None
        if XML_OUTPUT:
            ripple_element_node = TAG.xml_doc.createElement('element')
            ripple_element_node.setAttribute('index', str(ripple_idx))
            ripples_node.appendChild(ripple_element_node)

        ripple = SHADER.Ripple()
        input_stream.read(4) # Padding
        ripple.contribution_factor = TAG.read_float(input_stream, TAG, tag_format.XMLData(ripple_element_node, "contribution factor"))
        input_stream.read(32) # Padding
        ripple.animation_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(ripple_element_node, "animation angle"))
        ripple.animation_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(ripple_element_node, "animation velocity"))
        ripple.map_offset = TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(ripple_element_node, "map offset"))
        ripple.map_repeat = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(ripple_element_node, "map repeat"))
        ripple.map_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(ripple_element_node, "map index"))
        input_stream.read(16) # Padding

        SHADER.ripples.append(ripple)

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
