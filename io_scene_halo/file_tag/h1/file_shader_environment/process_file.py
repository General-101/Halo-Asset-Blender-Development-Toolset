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
        EnvironmentFlags,
        EnvironmentTypeEnum,
        DiffuseFlags,
        DiffuseFumctionEnum,
        FunctionEnum,
        SelfIlluminationFlags,
        SpecularFlags,
        ReflectionFlags,
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
    SHADER.tint_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "tint color"))
    input_stream.read(2) # Padding
    SHADER.material_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "material type", MaterialTypeEnum))
    input_stream.read(4) # Padding
    SHADER.environment_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", EnvironmentFlags))
    SHADER.environment_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "type", EnvironmentTypeEnum))
    SHADER.lens_flare_spacing = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "lens flare spacing"))
    SHADER.lens_flare = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "lens flare"))
    input_stream.read(44) # Padding
    SHADER.diffuse_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", DiffuseFlags))
    input_stream.read(26) # Padding
    SHADER.base_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "base map"))
    input_stream.read(24) # Padding
    SHADER.detail_map_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "detail map function", DiffuseFumctionEnum))
    input_stream.read(2) # Padding
    SHADER.primary_detail_map_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "primary detail map scale"))
    SHADER.primary_detail_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "primary detail map"))
    SHADER.secondary_detail_map_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "secondary detail map scale"))
    SHADER.secondary_detail_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "secondary detail map"))
    input_stream.read(24) # Padding
    SHADER.micro_detail_map_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "micro detail map function", DiffuseFumctionEnum))
    input_stream.read(2) # Padding
    SHADER.micro_detail_map_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "micro detail map scale"))
    SHADER.micro_detail_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "micro detail map"))
    SHADER.material_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "material color"))
    input_stream.read(12) # Padding
    SHADER.bump_map_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bump map scale"))
    SHADER.bump_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "bump map"))
    input_stream.read(24) # Padding
    SHADER.u_animation_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "u animation function", FunctionEnum))
    input_stream.read(2) # Padding
    SHADER.u_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "u animation period"))
    SHADER.u_animation_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "u animation scale"))
    SHADER.v_animation_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "v animation function", FunctionEnum))
    input_stream.read(2) # Padding
    SHADER.v_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "v animation period"))
    SHADER.v_animation_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "v animation scale"))
    input_stream.read(24) # Padding
    SHADER.self_illumination_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", SelfIlluminationFlags))
    input_stream.read(26) # Padding
    SHADER.primary_on_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "primary on color"))
    SHADER.primary_off_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "primary off color"))
    SHADER.primary_animation_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "primary animation function", FunctionEnum))
    input_stream.read(2) # Padding
    SHADER.primary_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "primary animation period"))
    SHADER.primary_animation_phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "primary animation phase"))
    input_stream.read(24) # Padding
    SHADER.secondary_on_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "secondary on color"))
    SHADER.secondary_off_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "secondary off color"))
    SHADER.secondary_animation_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "secondary animation function", FunctionEnum))
    input_stream.read(2) # Padding
    SHADER.secondary_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "secondary animation period"))
    SHADER.secondary_animation_phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "secondary animation phase"))
    input_stream.read(24) # Padding
    SHADER.plasma_on_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "plasma on color"))
    SHADER.plasma_off_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "plasma off color"))
    SHADER.plasma_animation_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "plasma animation function", FunctionEnum))
    input_stream.read(2) # Padding
    SHADER.plasma_animation_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "plasma animation period"))
    SHADER.plasma_animation_phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "plasma animation scale"))
    input_stream.read(24) # Padding
    SHADER.map_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "map scale"))
    SHADER.map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "map"))
    input_stream.read(24) # Padding
    SHADER.specular_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", SpecularFlags))
    input_stream.read(18) # Padding
    SHADER.brightness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "brightness"))
    input_stream.read(20) # Padding
    SHADER.perpendicular_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "perpendicular color"))
    SHADER.parallel_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "parallel color"))
    input_stream.read(16) # Padding
    SHADER.reflection_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ReflectionFlags))
    SHADER.reflection_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "type", ReflectionTypeEnum))
    SHADER.lightmap_brightness_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap brightness scale"))
    input_stream.read(28) # Padding
    SHADER.perpendicular_brightness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "perpendicular brightness"))
    SHADER.parallel_brightness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "parallel brightness"))
    input_stream.read(40) # Padding
    SHADER.reflection_cube_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "reflection cube map"))
    input_stream.read(16) # Padding

    lens_flare_name_length = SHADER.lens_flare.name_length
    base_map_name_length = SHADER.base_map.name_length
    primary_detail_map_name_length = SHADER.primary_detail_map.name_length
    secondary_detail_map_name_length = SHADER.secondary_detail_map.name_length
    micro_detail_map_name_length = SHADER.micro_detail_map.name_length
    bump_map_name_length = SHADER.bump_map.name_length
    map_name_length = SHADER.map.name_length
    reflection_cube_map_name_length = SHADER.reflection_cube_map.name_length
    if lens_flare_name_length > 0:
        SHADER.lens_flare.name = TAG.read_variable_string(input_stream, lens_flare_name_length, TAG)

    if base_map_name_length > 0:
        SHADER.base_map.name = TAG.read_variable_string(input_stream, base_map_name_length, TAG)

    if primary_detail_map_name_length > 0:
        SHADER.primary_detail_map.name = TAG.read_variable_string(input_stream, primary_detail_map_name_length, TAG)

    if secondary_detail_map_name_length > 0:
        SHADER.secondary_detail_map.name = TAG.read_variable_string(input_stream, secondary_detail_map_name_length, TAG)

    if micro_detail_map_name_length > 0:
        SHADER.micro_detail_map.name = TAG.read_variable_string(input_stream, micro_detail_map_name_length, TAG)

    if bump_map_name_length > 0:
        SHADER.bump_map.name = TAG.read_variable_string(input_stream, bump_map_name_length, TAG)

    if map_name_length > 0:
        SHADER.map.name = TAG.read_variable_string(input_stream, map_name_length, TAG)

    if reflection_cube_map_name_length > 0:
        SHADER.reflection_cube_map.name = TAG.read_variable_string(input_stream, reflection_cube_map_name_length, TAG)

    if XML_OUTPUT:
        lens_flare_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "lens flare")
        base_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "base map")
        primary_detail_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "primary detail map")
        secondary_detail_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "secondary detail map")
        micro_detail_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "micro detail map")
        bump_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "bump map")
        map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "map")
        reflection_cube_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "reflection cube map")
        SHADER.lens_flare.append_xml_attributes(lens_flare_node)
        SHADER.base_map.append_xml_attributes(base_map_node)
        SHADER.primary_detail_map.append_xml_attributes(primary_detail_map_node)
        SHADER.secondary_detail_map.append_xml_attributes(secondary_detail_map_node)
        SHADER.micro_detail_map.append_xml_attributes(micro_detail_map_node)
        SHADER.bump_map.append_xml_attributes(bump_map_node)
        SHADER.map.append_xml_attributes(map_node)
        SHADER.reflection_cube_map.append_xml_attributes(reflection_cube_map_node)

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
