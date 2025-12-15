# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Steven Garcia
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

import json

from ....global_functions import tag_format, shader_processing
from ....file_tag.h2.file_lens_flare.format import LensFlareAsset
from ....file_tag.h2.file_shader.format import FunctionTypeEnum, OutputTypeFlags

def generate_reflections(dump_dic, TAG, LENSFLARE):
    reflections_tag_block = dump_dic['Data']['Reflections']

    for reflection_element in reflections_tag_block:
        radius = reflection_element['Radius']
        brightness = reflection_element['Brightness']
        tint_color = shader_processing.get_rgb_percentage(reflection_element["Tint Color"])

        reflection = LENSFLARE.Reflection()
        reflection.flags = reflection_element['Flags']
        reflection.bitmap_index = reflection_element['Bitmap Index']
        reflection.position = reflection_element['Position']
        reflection.rotation_offset = reflection_element['Rotation Offset']
        reflection.radius = (radius["Min"], radius["Max"])
        reflection.brightness = (brightness["Min"], brightness["Max"])
        reflection.modulation_factor = tint_color[3]
        reflection.color = tint_color

        LENSFLARE.reflections.append(reflection)

    reflections_count = len(LENSFLARE.reflections)
    LENSFLARE.reflections_header = TAG.TagBlockHeader("tbfd", 0, reflections_count, 48)

    return TAG.TagBlock(reflections_count)

def generate_brightness(dump_dic, TAG, LENSFLARE):
    reflections_tag_block = dump_dic['Data']['Reflections']

    reflection_first_element = None
    for reflection_element in reflections_tag_block:
        reflection_first_element = reflection_element
        break

    if reflection_first_element:
        color_0 = shader_processing.get_rgb_percentage(reflection_first_element["Color Lower Bound"])
        color_1 = shader_processing.get_rgb_percentage(reflection_first_element["Color Upper Bound"])
        function_index = reflection_first_element["Animation Function"]["Value"]
        is_black = False
        if (color_0[0] + color_0[1] + color_0[2]) == 0.0 and (color_1[0] + color_1[1] + color_1[2]) == 0.0:
            is_black = True

        is_animated = False
        if not function_index == 0 and not function_index == 1:
            is_animated = True

        if not is_black and is_animated:
            function_type = FunctionTypeEnum.periodic
            rgb_0 = None
            rgb_1 = None
            rgb_2 = None
            rgb_3 = None
            value_0 = color_0[3]
            value_1 = color_1[3]
            value_2 = 0
            value_3 = 0
            function_0_type = function_index
            function_1_type = 0
            function_values = [reflection_first_element["Animation Phase"], reflection_first_element["Animation Period"], 0, 1, 0, 0, 0, 0]

            shader_processing.convert_legacy_function(LENSFLARE, TAG, LENSFLARE.brightness, 0, 0, function_type, 0, 0, 0, rgb_0, rgb_1, rgb_2, rgb_3, value_0, value_1,
                                                        value_2, value_3, function_0_type, function_1_type, function_values)

    brightness_count = len(LENSFLARE.brightness)
    LENSFLARE.brightness_header = TAG.TagBlockHeader("tbfd", 0, brightness_count, 12)

    return TAG.TagBlock(brightness_count)

def generate_color(dump_dic, TAG, LENSFLARE):
    reflections_tag_block = dump_dic['Data']['Reflections']

    reflection_first_element = None
    for reflection_element in reflections_tag_block:
        reflection_first_element = reflection_element
        break

    if reflection_first_element:
        color_0 = shader_processing.get_rgb_percentage(reflection_first_element["Color Lower Bound"])
        color_1 = shader_processing.get_rgb_percentage(reflection_first_element["Color Upper Bound"])
        function_index = reflection_first_element["Animation Function"]["Value"]
        is_black = False
        if (color_0[0] + color_0[1] + color_0[2]) == 0.0 and (color_1[0] + color_1[1] + color_1[2]) == 0.0:
            is_black = True

        is_animated = False
        if not function_index == 0 and not function_index == 1:
            is_animated = True

        if not is_black and is_animated:
            function_type = FunctionTypeEnum.periodic
            flag_value = OutputTypeFlags._2_color.value
            rgb_0 = reflection_first_element["Color Lower Bound"]
            rgb_1 = reflection_first_element["Color Upper Bound"]
            rgb_2 = None
            rgb_3 = None
            value_0 = 0
            value_1 = 0
            value_2 = 0
            value_3 = 0
            function_0_type = function_index
            function_1_type = 0
            function_values = [reflection_first_element["Animation Phase"], reflection_first_element["Animation Period"], 0, 1, 0, 0, 0, 0]

            shader_processing.convert_legacy_function(LENSFLARE, TAG, LENSFLARE.color, 0, 0, function_type, flag_value, 0, 0, rgb_0, rgb_1, rgb_2, rgb_3, value_0, value_1,
                                                        value_2, value_3, function_0_type, function_1_type, function_values)

    color_count = len(LENSFLARE.color)
    LENSFLARE.color_header = TAG.TagBlockHeader("tbfd", 0, color_count, 12)

    return TAG.TagBlock(color_count)

def upgrade_lens_flare(H2_ASSET, patch_txt_path, report):
    dump_dic = json.load(H2_ASSET)

    TAG = tag_format.TagAsset()
    LENSFLARE = LensFlareAsset()
    TAG.upgrade_patches = tag_format.get_patch_set(patch_txt_path)

    LENSFLARE.header = TAG.Header()
    LENSFLARE.header.unk1 = 0
    LENSFLARE.header.flags = 0
    LENSFLARE.header.type = 0
    LENSFLARE.header.name = ""
    LENSFLARE.header.tag_group = "lens"
    LENSFLARE.header.checksum = 0
    LENSFLARE.header.data_offset = 64
    LENSFLARE.header.data_length = 0
    LENSFLARE.header.unk2 = 0
    LENSFLARE.header.version = 2
    LENSFLARE.header.destination = 0
    LENSFLARE.header.plugin_handle = -1
    LENSFLARE.header.engine_tag = "BLM!"

    LENSFLARE.reflections = []
    LENSFLARE.brightness = []
    LENSFLARE.color = []
    LENSFLARE.rotation = []

    LENSFLARE.body_header = TAG.TagBlockHeader("tbfd", 0, 1, 124)
    LENSFLARE.falloff_angle = dump_dic['Data']['Falloff Angle']
    LENSFLARE.cutoff_angle = dump_dic['Data']['Cutoff Angle']
    LENSFLARE.occlusion_radius = dump_dic['Data']['Occlusion Radius']
    LENSFLARE.occlusion_offset_direction = dump_dic['Data']['Occlusion Offset Direction']['Value']
    LENSFLARE.occlusion_inner_radius_scale = 0
    LENSFLARE.near_fade_distance = dump_dic['Data']['Near Fade Distance']
    LENSFLARE.far_fade_distance = dump_dic['Data']['Far Fade Distance']
    LENSFLARE.bitmap = TAG.TagRef().convert_from_json(dump_dic['Data']['Bitmap'])
    LENSFLARE.occlusion_flags = dump_dic['Data']['Flags']
    LENSFLARE.rotation_function = dump_dic['Data']['Rotation Function']['Value']
    float_count = len(str(dump_dic['Data']["Rotation Function Scale Float"]).split(".", 1)[1])
    degree_count = len(str(dump_dic['Data']["Rotation Function Scale Degree"]).split(".", 1)[1])
    scale_result = 0.0
    if float_count < degree_count:
        scale_result = dump_dic['Data']['Rotation Function Scale Float']
    elif float_count > degree_count:
        scale_result = dump_dic['Data']['Rotation Function Scale Degree']
    else:
        scale_result = dump_dic['Data']['Rotation Function Scale Float']

    LENSFLARE.rotation_function_scale = scale_result
    LENSFLARE.corona_scale = (dump_dic['Data']['Horizontal Scale'], dump_dic['Data']['Vertical Scale'])
    LENSFLARE.falloff_function = 0
    LENSFLARE.reflections_tag_block = generate_reflections(dump_dic, TAG, LENSFLARE)
    LENSFLARE.flags = 0
    LENSFLARE.brightness_tag_block = generate_brightness(dump_dic, TAG, LENSFLARE)
    LENSFLARE.color_tag_block = generate_color(dump_dic, TAG, LENSFLARE)
    LENSFLARE.rotation_tag_block = TAG.TagBlock()

    return LENSFLARE
