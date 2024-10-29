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
from .format import (LightAsset,
                     LightFlags,
                     ShapeTypeEnum,
                     ShadowTapBiasEnum,
                     InterpolationFlags,
                     SpecularMaskEnum,
                     FalloffFunctionEnum,
                     DiffuseContrastEnum,
                     SpecularContrastEnum,
                     FalloffGeometryEnum,
                     DefaultLightmapSettingEnum,
                     EffectFalloffFunctionEnum,
                     FadeEnum,
                     AnimationFlags)

XML_OUTPUT = False

def initilize_light(LIGHT):
    LIGHT.brightness_animation = []
    LIGHT.color_animation = []
    LIGHT.gel_animation = []

def read_light_body_v0(LIGHT, TAG, input_stream, tag_node, XML_OUTPUT):
    LIGHT.body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    LIGHT.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(tag_node, "flags", LightFlags))
    input_stream.read(16) # Padding?
    LIGHT.shape_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "type", ShapeTypeEnum))
    input_stream.read(2) # Padding?
    LIGHT.size_modifier = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "size modifier"))
    LIGHT.shadow_quality_bias = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "shadow quality bias"))
    LIGHT.shadow_tap_bias = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "shadow tap bias", ShadowTapBiasEnum))
    input_stream.read(26) # Padding?
    LIGHT.radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "radius"))
    LIGHT.specular_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "specular radius"))
    input_stream.read(32) # Padding?
    LIGHT.near_width = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "near width"))
    LIGHT.height_stretch = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "height stretch"))
    LIGHT.field_of_view = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "field of view"))
    LIGHT.falloff_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "falloff distance"))
    LIGHT.cutoff_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "cutoff distance"))
    input_stream.read(4) # Padding?
    LIGHT.interpolation_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(tag_node, "interpolation flags", InterpolationFlags))
    LIGHT.bloom_bounds = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "bloom bounds"))
    LIGHT.specular_lower_bound = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "specular lower bound"))
    LIGHT.specular_upper_bound = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "specular upper bound"))
    LIGHT.diffuse_lower_bound = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "diffuse lower bound"))
    input_stream.read(4) # Padding?
    LIGHT.diffuse_upper_bound = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "diffuse upper bound"))
    LIGHT.brightness_bounds = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "brightness bounds"))
    input_stream.read(4) # Padding?
    LIGHT.gel_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "gel map"))
    LIGHT.specular_mask = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "specular mask", SpecularMaskEnum))
    input_stream.read(150) # Padding?
    LIGHT.falloff_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "falloff function", FalloffFunctionEnum))
    LIGHT.diffuse_contrast = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "diffuse contrast", DiffuseContrastEnum))
    LIGHT.specular_contrast = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "specular contrast", SpecularContrastEnum))
    LIGHT.falloff_geometry = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "falloff geometry", FalloffGeometryEnum))
    input_stream.read(8) # Padding?
    LIGHT.lens_flare = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "lens flare"))
    LIGHT.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    LIGHT.light_volume = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "light volume"))
    input_stream.read(8) # Padding?
    LIGHT.default_lightmap_setting = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "default lightmap setting", DefaultLightmapSettingEnum))
    input_stream.read(2) # Padding?
    LIGHT.lightmap_half_life = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap half life"))
    LIGHT.lightmap_light_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap light scale"))
    input_stream.read(20) # Padding?
    LIGHT.duration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "duration"))
    input_stream.read(2) # Padding?
    LIGHT.effect_falloff_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "effect falloff function", EffectFalloffFunctionEnum))
    input_stream.read(8) # Padding?
    LIGHT.illumination_fade = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "illumination fade", FadeEnum))
    LIGHT.shadow_fade = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "shadow fade", FadeEnum))
    LIGHT.specular_fade = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "specular fade", FadeEnum))
    input_stream.read(10) # Padding?
    LIGHT.animation_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(tag_node, "flags", AnimationFlags))
    LIGHT.brightness_animation_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "brightness animation"))
    LIGHT.color_animation_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "color animation"))
    LIGHT.gel_animation_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "gel animation"))
    input_stream.read(72) # Padding?
    LIGHT.shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "shader"))

def read_light_body_retail(LIGHT, TAG, input_stream, tag_node, XML_OUTPUT):
    LIGHT.body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    LIGHT.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(tag_node, "flags", LightFlags))
    LIGHT.shape_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "type", ShapeTypeEnum))
    input_stream.read(2) # Padding?
    LIGHT.size_modifier = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "size modifier"))
    LIGHT.shadow_quality_bias = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "shadow quality bias"))
    LIGHT.shadow_tap_bias = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "shadow tap bias", ShadowTapBiasEnum))
    input_stream.read(2) # Padding?
    LIGHT.radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "radius"))
    LIGHT.specular_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "specular radius"))
    LIGHT.near_width = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "near width"))
    LIGHT.height_stretch = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "height stretch"))
    LIGHT.field_of_view = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "field of view"))
    LIGHT.falloff_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "falloff distance"))
    LIGHT.cutoff_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "cutoff distance"))
    LIGHT.interpolation_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(tag_node, "interpolation flags", InterpolationFlags))
    LIGHT.bloom_bounds = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "bloom bounds"))
    LIGHT.specular_lower_bound = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "specular lower bound"))
    LIGHT.specular_upper_bound = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "specular upper bound"))
    LIGHT.diffuse_lower_bound = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "diffuse lower bound"))
    LIGHT.diffuse_upper_bound = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "diffuse upper bound"))
    LIGHT.brightness_bounds = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "brightness bounds"))
    LIGHT.gel_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "gel map"))
    LIGHT.specular_mask = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "specular mask", SpecularMaskEnum))
    input_stream.read(6) # Padding?
    LIGHT.falloff_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "falloff function", FalloffFunctionEnum))
    LIGHT.diffuse_contrast = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "diffuse contrast", DiffuseContrastEnum))
    LIGHT.specular_contrast = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "specular contrast", SpecularContrastEnum))
    LIGHT.falloff_geometry = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "falloff geometry", FalloffGeometryEnum))
    LIGHT.lens_flare = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "lens flare"))
    LIGHT.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    LIGHT.light_volume = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "light volume"))
    LIGHT.default_lightmap_setting = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "default lightmap setting", DefaultLightmapSettingEnum))
    input_stream.read(2) # Padding?
    LIGHT.lightmap_half_life = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap half life"))
    LIGHT.lightmap_light_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap light scale"))
    LIGHT.duration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "duration"))
    input_stream.read(2) # Padding?
    LIGHT.effect_falloff_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "effect falloff function", EffectFalloffFunctionEnum))
    LIGHT.illumination_fade = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "illumination fade", FadeEnum))
    LIGHT.shadow_fade = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "shadow fade", FadeEnum))
    LIGHT.specular_fade = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "specular fade", FadeEnum))
    input_stream.read(2) # Padding?
    LIGHT.animation_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(tag_node, "flags", AnimationFlags))
    LIGHT.brightness_animation_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "brightness animation"))
    LIGHT.color_animation_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "color animation"))
    LIGHT.gel_animation_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "gel animation"))
    LIGHT.shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "shader"))
    
def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    LIGHT = LightAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    LIGHT.header = TAG.Header().read(input_stream, TAG)
    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    initilize_light(LIGHT)
    if LIGHT.header.engine_tag == "LAMB":
        read_light_body_v0(LIGHT, TAG, input_stream, tag_node, XML_OUTPUT)
    elif LIGHT.header.engine_tag == "MLAB":
        read_light_body_v0(LIGHT, TAG, input_stream, tag_node, XML_OUTPUT)
    elif LIGHT.header.engine_tag == "BLM!":
        read_light_body_retail(LIGHT, TAG, input_stream, tag_node, XML_OUTPUT)

    if LIGHT.gel_map.name_length > 0:
        LIGHT.gel_map.name = TAG.read_variable_string(input_stream, LIGHT.gel_map.name_length, TAG)

    if LIGHT.lens_flare.name_length > 0:
        LIGHT.lens_flare.name = TAG.read_variable_string(input_stream, LIGHT.lens_flare.name_length, TAG)

    if LIGHT.light_volume.name_length > 0:
        LIGHT.light_volume.name = TAG.read_variable_string(input_stream, LIGHT.light_volume.name_length, TAG)

    #if LIGHT.shader.name_length > 0:
        #LIGHT.shader.name = TAG.read_variable_string(input_stream, LIGHT.shader.name_length, TAG)

    if XML_OUTPUT:
        gel_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "gel map")
        lens_flare_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "lens flare")
        light_volume_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "light volume")
        shader_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "shader")
        LIGHT.gel_map.append_xml_attributes(gel_map_node)
        LIGHT.lens_flare.append_xml_attributes(lens_flare_node)
        LIGHT.light_volume.append_xml_attributes(light_volume_node)
        #LIGHT.shader.append_xml_attributes(shader_node)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, LIGHT.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return LIGHT
