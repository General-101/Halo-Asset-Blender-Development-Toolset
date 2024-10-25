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
        GlassFlags,
        ReflectionTypeEnum
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

    SHADER.radiosity_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", RadiosityFlags))
    SHADER.detail_level = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "detail level", DetailLevelEnum))
    SHADER.power = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "power"))
    SHADER.color_of_emitted_light = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "color of emitted light"))
    SHADER.light_tint_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "tint color"))
    input_stream.read(2) # Padding
    SHADER.material_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "material type", MaterialTypeEnum))
    input_stream.read(4) # Padding
    SHADER.glass_flags = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", GlassFlags))
    input_stream.read(42) # Padding
    SHADER.background_tint_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "background tint color"))
    SHADER.background_tint_map_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "background tint map scale"))
    SHADER.background_tint_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "background tint map"))
    input_stream.read(22) # Padding
    SHADER.reflection_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "reflection type", ReflectionTypeEnum))
    SHADER.perpendicular_brightness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "perpendicular brightness"))
    SHADER.perpendicular_tint_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "perpendicular tint color"))
    SHADER.parallel_brightness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "parallel brightness"))
    SHADER.parallel_tint_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "parallel tint color"))
    SHADER.reflection_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "reflection map"))
    SHADER.bump_map_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bump map scale"))
    SHADER.bump_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "bump map"))
    input_stream.read(132) # Padding
    SHADER.diffuse_map_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "diffuse map scale"))
    SHADER.diffuse_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "diffuse map"))
    SHADER.diffuse_detail_map_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "diffuse detail map scale"))
    SHADER.diffuse_detail_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "diffuse detail map"))
    input_stream.read(32) # Padding
    SHADER.specular_map_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "specular map scale"))
    SHADER.specular_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "specular map"))
    SHADER.specular_detail_map_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "specular detail map scale"))
    SHADER.specular_detail_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "specular detail map"))
    input_stream.read(28) # Padding

    background_tint_map_name_length = SHADER.background_tint_map.name_length
    reflection_map_name_length = SHADER.reflection_map.name_length
    bump_map_name_length = SHADER.bump_map.name_length
    diffuse_map_name_length = SHADER.diffuse_map.name_length
    diffuse_detail_map_name_length = SHADER.diffuse_detail_map.name_length
    specular_map_name_length = SHADER.specular_map.name_length
    specular_detail_map_name_length = SHADER.specular_detail_map.name_length
    if background_tint_map_name_length > 0:
        SHADER.background_tint_map.name = TAG.read_variable_string(input_stream, background_tint_map_name_length, TAG)

    if reflection_map_name_length > 0:
        SHADER.reflection_map.name = TAG.read_variable_string(input_stream, reflection_map_name_length, TAG)

    if bump_map_name_length > 0:
        SHADER.bump_map.name = TAG.read_variable_string(input_stream, bump_map_name_length, TAG)

    if diffuse_map_name_length > 0:
        SHADER.diffuse_map.name = TAG.read_variable_string(input_stream, diffuse_map_name_length, TAG)

    if diffuse_detail_map_name_length > 0:
        SHADER.diffuse_detail_map.name = TAG.read_variable_string(input_stream, diffuse_detail_map_name_length, TAG)

    if specular_map_name_length > 0:
        SHADER.specular_map.name = TAG.read_variable_string(input_stream, specular_map_name_length, TAG)

    if specular_detail_map_name_length > 0:
        SHADER.specular_detail_map.name = TAG.read_variable_string(input_stream, specular_detail_map_name_length, TAG)


    if XML_OUTPUT:
        background_tint_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "background tint map")
        reflection_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "reflection map")
        bump_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "bump map")
        diffuse_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "diffuse map")
        diffuse_detail_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "diffuse detail map")
        specular_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "specular map")
        specular_detail_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "specular detail map")
        SHADER.background_tint_map.append_xml_attributes(background_tint_map_node)
        SHADER.reflection_map.append_xml_attributes(reflection_map_node)
        SHADER.bump_map.append_xml_attributes(bump_map_node)
        SHADER.diffuse_map.append_xml_attributes(diffuse_map_node)
        SHADER.diffuse_detail_map.append_xml_attributes(diffuse_detail_map_node)
        SHADER.specular_map.append_xml_attributes(specular_map_node)
        SHADER.specular_detail_map.append_xml_attributes(specular_detail_map_node)

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
