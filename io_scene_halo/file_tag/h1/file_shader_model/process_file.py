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
        ModelFlags,
        ChannelSourceEnum,
        SelfIlluminationFlags,
        FunctionEnum,
        DetailFumctionEnum,
        DetailMaskEnum
        )

XML_OUTPUT = False

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    SHADER = ShaderAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    SHADER.header = TAG.Header().read(input_stream, TAG)
    is_stubbs_the_zombie = (SHADER.header.version == 3)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    SHADER.radiosity_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", RadiosityFlags))
    SHADER.detail_level = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "detail level", DetailLevelEnum))
    SHADER.power = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "power"))
    SHADER.color_of_emitted_light = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "color of emitted light"))
    SHADER.tint_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "tint color"))
    input_stream.read(2) # Padding
    SHADER.material_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "material type", MaterialTypeEnum))
    input_stream.read(4) # Padding
    SHADER.model_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ModelFlags))
    input_stream.read(14) # Padding
    SHADER.translucency = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "translucency"))
    input_stream.read(16) # Padding
    SHADER.change_color_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "change color source", ChannelSourceEnum))
    input_stream.read(30) # Padding
    SHADER.self_illumination_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", SelfIlluminationFlags))
    input_stream.read(2) # Padding
    SHADER.self_illumination_color_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "color source", ChannelSourceEnum))
    SHADER.self_illumination_animation_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "animation function", FunctionEnum))
    SHADER.self_illumination_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "animation period"))
    SHADER.self_illumination_animation_color_lower_bound = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "animation color lower bound"))
    SHADER.self_illumination_animation_color_upper_bound = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "animation color upper bound"))
    input_stream.read(12) # Padding
    SHADER.map_u_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "map u scale"))
    SHADER.map_v_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "map v scale"))
    SHADER.base_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "base map"))
    input_stream.read(8) # Padding
    SHADER.multipurpose_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "multipurpose map"))
    input_stream.read(8) # Padding
    SHADER.detail_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "detail function", DetailFumctionEnum))
    SHADER.detail_mask = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "detail mask", DetailMaskEnum))
    SHADER.detail_map_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "detail map scale"))
    SHADER.detail_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "detail map"))
    SHADER.detail_map_v_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "detail map v scale"))
    input_stream.read(12) # Padding
    SHADER.u_animation_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "u animation source", ChannelSourceEnum))
    SHADER.u_animation_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "u animation function", FunctionEnum))
    SHADER.u_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "u animation period"))
    SHADER.u_animation_phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "u animation phase"))
    SHADER.u_animation_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "u animation scale"))
    SHADER.v_animation_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "v animation source", ChannelSourceEnum))
    SHADER.v_animation_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "v animation function", FunctionEnum))
    SHADER.v_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "v animation period"))
    SHADER.v_animation_phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "v animation phase"))
    SHADER.v_animation_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "v animation scale"))
    SHADER.rotation_animation_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "rotation animation source", ChannelSourceEnum))
    SHADER.rotation_animation_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "rotation animation function", FunctionEnum))
    SHADER.rotation_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "rotation animation period"))
    SHADER.rotation_animation_phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "rotation animation phase"))
    SHADER.rotation_animation_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "rotation animation scale"))
    SHADER.rotation_animation_center = TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(tag_node, "rotation animation center"))
    input_stream.read(8) # Padding
    SHADER.reflection_falloff_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "reflection falloff distance"))
    SHADER.reflection_cutoff_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "reflection cutoff distance"))
    SHADER.perpendicular_brightness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "perpendicular brightness"))
    SHADER.perpendicular_tint_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "perpendicular tint color"))
    SHADER.parallel_brightness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "parallel brightness"))
    SHADER.parallel_tint_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "parallel tint color"))
    SHADER.reflection_cube_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "reflection cube map"))
    input_stream.read(16) # Padding
    if is_stubbs_the_zombie:
        SHADER.bump_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bump scale"))
        SHADER.bump_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "bump map"))
        input_stream.read(40) # Padding
    else:
        input_stream.read(52) # Padding

    base_map_name_length = SHADER.base_map.name_length
    multipurpose_map_name_length = SHADER.multipurpose_map.name_length
    detail_map_name_length = SHADER.detail_map.name_length
    reflection_cube_map_name_length = SHADER.reflection_cube_map.name_length
    if base_map_name_length > 0:
        SHADER.base_map.name = TAG.read_variable_string(input_stream, base_map_name_length, TAG)

    if multipurpose_map_name_length > 0:
        SHADER.multipurpose_map.name = TAG.read_variable_string(input_stream, multipurpose_map_name_length, TAG)

    if detail_map_name_length > 0:
        SHADER.detail_map.name = TAG.read_variable_string(input_stream, detail_map_name_length, TAG)

    if reflection_cube_map_name_length > 0:
        SHADER.reflection_cube_map.name = TAG.read_variable_string(input_stream, reflection_cube_map_name_length, TAG)

    if is_stubbs_the_zombie and SHADER.bump_map.name_length > 0:
        SHADER.base_map.name = TAG.read_variable_string(input_stream, SHADER.bump_map.name_length, TAG)

    if XML_OUTPUT:
        base_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "base map")
        multipurpose_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "multipurpose map")
        detail_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "detail map")
        reflection_cube_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "reflection cube map")
        SHADER.base_map.append_xml_attributes(base_map_node)
        SHADER.multipurpose_map.append_xml_attributes(multipurpose_map_node)
        SHADER.detail_map.append_xml_attributes(detail_map_node)
        SHADER.reflection_cube_map.append_xml_attributes(reflection_cube_map_node)
        if is_stubbs_the_zombie:
            bump_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "bump map")
            SHADER.bump_map_node.append_xml_attributes(bump_map_node)

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
