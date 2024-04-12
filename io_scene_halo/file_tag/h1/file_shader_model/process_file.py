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

    SHADER.shader_body = SHADER.ShaderBody()
    SHADER.shader_body.radiosity_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", RadiosityFlags))
    SHADER.shader_body.detail_level = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "detail level", DetailLevelEnum))
    SHADER.shader_body.power = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "power"))
    SHADER.shader_body.color_of_emitted_light = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "color of emitted light"))
    SHADER.shader_body.tint_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "tint color"))
    input_stream.read(2) # Padding
    SHADER.shader_body.material_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "material type", MaterialTypeEnum))
    input_stream.read(4) # Padding
    SHADER.shader_body.model_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ModelFlags))
    input_stream.read(14) # Padding
    SHADER.shader_body.translucency = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "translucency"))
    input_stream.read(16) # Padding
    SHADER.shader_body.change_color_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "change color source", ChannelSourceEnum))
    input_stream.read(30) # Padding
    SHADER.shader_body.self_illumination_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", SelfIlluminationFlags))
    input_stream.read(2) # Padding
    SHADER.shader_body.self_illumination_color_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "color source", ChannelSourceEnum))
    SHADER.shader_body.self_illumination_animation_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "animation function", FunctionEnum))
    SHADER.shader_body.self_illumination_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "animation period"))
    SHADER.shader_body.self_illumination_animation_color_lower_bound = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "animation color lower bound"))
    SHADER.shader_body.self_illumination_animation_color_upper_bound = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "animation color upper bound"))
    input_stream.read(12) # Padding
    SHADER.shader_body.map_u_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "map u scale"))
    SHADER.shader_body.map_v_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "map v scale"))
    SHADER.shader_body.base_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "base map"))
    input_stream.read(8) # Padding
    SHADER.shader_body.multipurpose_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "multipurpose map"))
    input_stream.read(8) # Padding
    SHADER.shader_body.detail_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "detail function", DetailFumctionEnum))
    SHADER.shader_body.detail_mask = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "detail mask", DetailMaskEnum))
    SHADER.shader_body.detail_map_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "detail map scale"))
    SHADER.shader_body.detail_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "detail map"))
    SHADER.shader_body.detail_map_v_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "detail map v scale"))
    input_stream.read(12) # Padding
    SHADER.shader_body.u_animation_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "u animation source", ChannelSourceEnum))
    SHADER.shader_body.u_animation_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "u animation function", FunctionEnum))
    SHADER.shader_body.u_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "u animation period"))
    SHADER.shader_body.u_animation_phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "u animation phase"))
    SHADER.shader_body.u_animation_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "u animation scale"))
    SHADER.shader_body.v_animation_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "v animation source", ChannelSourceEnum))
    SHADER.shader_body.v_animation_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "v animation function", FunctionEnum))
    SHADER.shader_body.v_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "v animation period"))
    SHADER.shader_body.v_animation_phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "v animation phase"))
    SHADER.shader_body.v_animation_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "v animation scale"))
    SHADER.shader_body.rotation_animation_source = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "rotation animation source", ChannelSourceEnum))
    SHADER.shader_body.rotation_animation_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "rotation animation function", FunctionEnum))
    SHADER.shader_body.rotation_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "rotation animation period"))
    SHADER.shader_body.rotation_animation_phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "rotation animation phase"))
    SHADER.shader_body.rotation_animation_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "rotation animation scale"))
    SHADER.shader_body.rotation_animation_center = TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(tag_node, "rotation animation center"))
    input_stream.read(8) # Padding
    SHADER.shader_body.reflection_falloff_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "reflection falloff distance"))
    SHADER.shader_body.reflection_cutoff_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "reflection cutoff distance"))
    SHADER.shader_body.perpendicular_brightness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "perpendicular brightness"))
    SHADER.shader_body.perpendicular_tint_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "perpendicular tint color"))
    SHADER.shader_body.parallel_brightness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "parallel brightness"))
    SHADER.shader_body.parallel_tint_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "parallel tint color"))
    SHADER.shader_body.reflection_cube_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "reflection cube map"))
    input_stream.read(16) # Padding
    if is_stubbs_the_zombie:
        SHADER.shader_body.bump_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bump scale"))
        SHADER.shader_body.bump_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "bump map"))
        input_stream.read(40) # Padding
    else:
        input_stream.read(52) # Padding

    base_map_name_length = SHADER.shader_body.base_map.name_length
    multipurpose_map_name_length = SHADER.shader_body.multipurpose_map.name_length
    detail_map_name_length = SHADER.shader_body.detail_map.name_length
    reflection_cube_map_name_length = SHADER.shader_body.reflection_cube_map.name_length
    if base_map_name_length > 0:
        SHADER.shader_body.base_map.name = TAG.read_variable_string(input_stream, base_map_name_length, TAG)

    if multipurpose_map_name_length > 0:
        SHADER.shader_body.multipurpose_map.name = TAG.read_variable_string(input_stream, multipurpose_map_name_length, TAG)

    if detail_map_name_length > 0:
        SHADER.shader_body.detail_map.name = TAG.read_variable_string(input_stream, detail_map_name_length, TAG)

    if reflection_cube_map_name_length > 0:
        SHADER.shader_body.reflection_cube_map.name = TAG.read_variable_string(input_stream, reflection_cube_map_name_length, TAG)

    if is_stubbs_the_zombie and SHADER.shader_body.bump_map.name_length > 0:
        SHADER.shader_body.base_map.name = TAG.read_variable_string(input_stream, SHADER.shader_body.bump_map.name_length, TAG)

    if XML_OUTPUT:
        base_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "base map")
        multipurpose_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "multipurpose map")
        detail_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "detail map")
        reflection_cube_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "reflection cube map")
        SHADER.shader_body.base_map.append_xml_attributes(base_map_node)
        SHADER.shader_body.multipurpose_map.append_xml_attributes(multipurpose_map_node)
        SHADER.shader_body.detail_map.append_xml_attributes(detail_map_node)
        SHADER.shader_body.reflection_cube_map.append_xml_attributes(reflection_cube_map_node)
        if is_stubbs_the_zombie:
            bump_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "bump map")
            SHADER.shader_body.bump_map_node.append_xml_attributes(bump_map_node)

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
