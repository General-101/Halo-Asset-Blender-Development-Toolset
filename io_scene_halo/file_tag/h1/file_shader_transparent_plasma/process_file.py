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
        ChannelSourceEnum
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
    input_stream.read(8) # Padding
    SHADER.shader_body.intensity_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "intensity source", ChannelSourceEnum))
    input_stream.read(2) # Padding
    SHADER.shader_body.intensity_exponent = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "intensity exponent"))
    SHADER.shader_body.offset_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "offset source", ChannelSourceEnum))
    input_stream.read(2) # Padding
    SHADER.shader_body.offset_amount = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "offset amount"))
    SHADER.shader_body.offset_exponent = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "offset exponent"))
    input_stream.read(32) # Padding
    SHADER.shader_body.perpendicular_brightness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "perpendicular brightness"))
    SHADER.shader_body.perpendicular_tint_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "perpendicular tint color"))
    SHADER.shader_body.parallel_brightness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "parallel brightness"))
    SHADER.shader_body.parallel_tint_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "parallel tint color"))
    SHADER.shader_body.tint_color_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "tint color source", ChannelSourceEnum))
    input_stream.read(62) # Padding
    SHADER.shader_body.primary_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "primary animation period"))
    SHADER.shader_body.primary_animation_direction = TAG.read_vector(input_stream, TAG, tag_format.XMLData(tag_node, "primary animation direction"))
    SHADER.shader_body.primary_noise_map_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "primary noise map scale"))
    SHADER.shader_body.primary_noise_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "primary noise map"))
    input_stream.read(36) # Padding
    SHADER.shader_body.secondary_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "secondary animation period"))
    SHADER.shader_body.secondary_animation_direction = TAG.read_vector(input_stream, TAG, tag_format.XMLData(tag_node, "secondary animation direction"))
    SHADER.shader_body.secondary_noise_map_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "secondary noise map scale"))
    SHADER.shader_body.secondary_noise_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "secondary noise map"))
    input_stream.read(32) # Padding

    primary_noise_map_name_length = SHADER.shader_body.primary_noise_map.name_length
    secondary_noise_map_name_length = SHADER.shader_body.secondary_noise_map.name_length
    if primary_noise_map_name_length > 0:
        SHADER.shader_body.primary_noise_map.name = TAG.read_variable_string(input_stream, primary_noise_map_name_length, TAG)

    if secondary_noise_map_name_length > 0:
        SHADER.shader_body.secondary_noise_map.name = TAG.read_variable_string(input_stream, secondary_noise_map_name_length, TAG)

    if XML_OUTPUT:
        primary_noise_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "primary noise map")
        secondary_noise_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "secondary noise map")
        SHADER.shader_body.primary_noise_map.append_xml_attributes(primary_noise_map_node)
        SHADER.shader_body.secondary_noise_map.append_xml_attributes(secondary_noise_map_node)

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
