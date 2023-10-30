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
from .format_retail import (
        ShaderAsset,
        RadiosityFlags,
        DetailLevelEnum,
        MaterialTypeEnum,
        MeterFlags,
        ChannelSourceEnum
        )

XML_OUTPUT = False

def process_file_retail(input_stream, tag_format, report):
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
    input_stream.read(2)
    SHADER.shader_body.material_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "material type", MaterialTypeEnum))
    input_stream.read(4)
    SHADER.shader_body.meter_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", MeterFlags))
    input_stream.read(34)
    SHADER.shader_body.meter_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "map"))
    input_stream.read(32)
    SHADER.shader_body.gradient_min_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "gradient min color"))
    SHADER.shader_body.gradient_max_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "gradient max color"))
    SHADER.shader_body.background_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "background color"))
    SHADER.shader_body.flash_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "flash color"))
    SHADER.shader_body.tint_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "tint color"))
    SHADER.shader_body.meter_transparency = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "meter transparency"))
    SHADER.shader_body.background_transparency = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "background transparency"))
    input_stream.read(24)
    SHADER.shader_body.meter_brightness_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "meter brightness source", ChannelSourceEnum))
    SHADER.shader_body.flash_brightness_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flash brightness source", ChannelSourceEnum))
    SHADER.shader_body.value_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "value source", ChannelSourceEnum))
    SHADER.shader_body.gradient_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "gradient source", ChannelSourceEnum))
    SHADER.shader_body.flash_extension_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flash extension source", ChannelSourceEnum))
    input_stream.read(34)

    meter_map_name_length = SHADER.shader_body.meter_map.name_length
    if meter_map_name_length > 0:
        SHADER.shader_body.meter_map.name = TAG.read_variable_string(input_stream, meter_map_name_length, TAG)

    if XML_OUTPUT:
        meter_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "map")
        SHADER.shader_body.meter_map.append_xml_attributes(meter_map_node)

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
