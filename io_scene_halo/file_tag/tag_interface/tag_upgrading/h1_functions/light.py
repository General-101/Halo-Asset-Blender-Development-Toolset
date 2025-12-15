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
from ....file_tag.h2.file_light.format import LightAsset, DefaultLightmapSettingEnum
from ....file_tag.h2.file_shader.format import FunctionTypeEnum

def convert_default_lightmap_setting(default_lightmap_setting_index):
    default_lightmap_setting_result = 0
    try:
        default_lightmap_setting_result = DefaultLightmapSettingEnum(default_lightmap_setting_index).value
    except:
        print("bad value")

    return default_lightmap_setting_result

def generate_brightness_animation(dump_dic, TAG, LIGHT):
    brightness_animation_tag_block = dump_dic['Data']['Brightness Animation']

    for brightness_animation_element in brightness_animation_tag_block:
        function_type = FunctionTypeEnum(brightness_animation_element["Function Type"])
        flag_value = brightness_animation_element["Flags"]
        rgb_0 = brightness_animation_element["Color 0"]
        rgb_1 = brightness_animation_element["Color 1"]
        rgb_2 = brightness_animation_element["Color 2"]
        rgb_3 = brightness_animation_element["Color 3"]
        value_0 = brightness_animation_element["Float 0"]
        value_1 = brightness_animation_element["Float 1"]
        value_2 = brightness_animation_element["Float 2"]
        value_3 = brightness_animation_element["Float 3"]
        function_0_type = brightness_animation_element["Function 1"]
        function_1_type = brightness_animation_element["Function 2"]
        function_values = [element["Value"] for element in brightness_animation_element["Values"]]

        shader_processing.convert_legacy_function(LIGHT, TAG, LIGHT.brightness_animation, 0, 0, function_type, flag_value, 0, 0, rgb_0, rgb_1, rgb_2, rgb_3, value_0, value_1,
                                                  value_2, value_3, function_0_type, function_1_type, function_values)

    brightness_animation_count = len(LIGHT.brightness_animation)
    LIGHT.brightness_animation_header = TAG.TagBlockHeader("tbfd", 0, brightness_animation_count, 12)

    return TAG.TagBlock(brightness_animation_count)

def upgrade_light(H2_ASSET, patch_txt_path, report):
    dump_dic = json.load(H2_ASSET)

    TAG = tag_format.TagAsset()
    LIGHT = LightAsset()
    TAG.upgrade_patches = tag_format.get_patch_set(patch_txt_path)

    LIGHT.header = TAG.Header()
    LIGHT.header.unk1 = 0
    LIGHT.header.flags = 0
    LIGHT.header.type = 0
    LIGHT.header.name = ""
    LIGHT.header.tag_group = "ligh"
    LIGHT.header.checksum = 0
    LIGHT.header.data_offset = 64
    LIGHT.header.data_length = 0
    LIGHT.header.unk2 = 0
    LIGHT.header.version = 4
    LIGHT.header.destination = 0
    LIGHT.header.plugin_handle = -1
    LIGHT.header.engine_tag = "BLM!"

    LIGHT.brightness_animation = []
    LIGHT.color_animation = []
    LIGHT.gel_animation = []

    size_modifer = dump_dic['Data']['Size Modifier']
    bloom_bounds = dump_dic['Data']['Bloom Bounds']
    brightness_bounds = dump_dic['Data']['Brightness Bounds']

    LIGHT.body_header = TAG.TagBlockHeader("tbfd", 0, 1, 272)
    LIGHT.flags = dump_dic['Data']['Flags']
    LIGHT.shape_type = dump_dic['Data']['Type']['Value']
    LIGHT.size_modifier = (size_modifer["Min"], size_modifer["Max"])
    LIGHT.shadow_quality_bias = 0.0
    LIGHT.shadow_tap_bias = 0
    LIGHT.radius = dump_dic['Data']['Radius']
    LIGHT.specular_radius = dump_dic['Data']['Specular Radius']
    LIGHT.near_width = dump_dic['Data']['Near Width']
    LIGHT.height_stretch = dump_dic['Data']['Height Stretch']
    LIGHT.field_of_view = dump_dic['Data']['Field Of View']
    LIGHT.falloff_distance = dump_dic['Data']['Falloff Distance']
    LIGHT.cutoff_distance = dump_dic['Data']['Cutoff Distance']
    LIGHT.interpolation_flags = dump_dic['Data']['Interpolation Flags']
    LIGHT.bloom_bounds = (bloom_bounds["Min"], bloom_bounds["Max"])
    LIGHT.specular_lower_bound = shader_processing.get_rgb_percentage(dump_dic['Data']["Specular Lower Bound"])
    LIGHT.specular_upper_bound = shader_processing.get_rgb_percentage(dump_dic['Data']["Specular Upper Bound"])
    LIGHT.diffuse_lower_bound = shader_processing.get_rgb_percentage(dump_dic['Data']["Diffuse Lower Bound"])
    LIGHT.diffuse_upper_bound = shader_processing.get_rgb_percentage(dump_dic['Data']["Diffuse Upper Bound"])
    LIGHT.brightness_bounds = (brightness_bounds["Min"], brightness_bounds["Max"])
    LIGHT.gel_map = TAG.TagRef().convert_from_json(dump_dic['Data']['Gel Map'])
    LIGHT.specular_mask = dump_dic['Data']['Specular Mask']['Value']
    LIGHT.falloff_function = dump_dic['Data']['Falloff Function']['Value']
    LIGHT.diffuse_contrast = dump_dic['Data']['Diffuse Contrast']['Value']
    LIGHT.specular_contrast = dump_dic['Data']['Specular Contrast']['Value']
    LIGHT.falloff_geometry = dump_dic['Data']['Falloff Geometry']['Value']
    LIGHT.lens_flare = TAG.TagRef().convert_from_json(dump_dic['Data']['Lens Flare'])
    LIGHT.bounding_radius = dump_dic['Data']['Bounding Radius'] # Does E3 even use this?
    LIGHT.light_volume = TAG.TagRef("MGS2")
    LIGHT.default_lightmap_setting = 0#convert_default_lightmap_setting(dump_dic['Data']['Default Lightmap Setting']['Value']) # Unused?
    LIGHT.lightmap_half_life = 0.0
    LIGHT.lightmap_light_scale = 0.0
    LIGHT.duration = dump_dic['Data']['Duration'] / 30
    LIGHT.effect_falloff_function = dump_dic['Data']['Effect Falloff Function']['Value']
    LIGHT.illumination_fade = 4#dump_dic['Data']['Illumination Fade']['Value']
    LIGHT.shadow_fade = 4#dump_dic['Data']['Stencil Shadow Fade']['Value']
    LIGHT.specular_fade = 4#dump_dic['Data']['Specular Fade']['Value']
    LIGHT.animation_flags = 0
    LIGHT.brightness_animation_tag_block = generate_brightness_animation(dump_dic, TAG, LIGHT)
    LIGHT.color_animation_tag_block = TAG.TagBlock()
    LIGHT.gel_animation_tag_block = TAG.TagBlock()
    LIGHT.shader = TAG.TagRef("shad", "", 0)

    return LIGHT
