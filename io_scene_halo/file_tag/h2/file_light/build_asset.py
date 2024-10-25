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

import struct

from ....global_functions import tag_format, shader_processing

def write_body(output_stream, TAG, LIGHT):
    LIGHT.body_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<I', LIGHT.flags))
    output_stream.write(struct.pack('<H', LIGHT.shape_type))
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<ff', *LIGHT.size_modifier))
    output_stream.write(struct.pack('<f', LIGHT.shadow_quality_bias))
    output_stream.write(struct.pack('<H', LIGHT.shadow_tap_bias))
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<f', LIGHT.radius))
    output_stream.write(struct.pack('<f', LIGHT.specular_radius))
    output_stream.write(struct.pack('<f', LIGHT.near_width))
    output_stream.write(struct.pack('<f', LIGHT.height_stretch))
    output_stream.write(struct.pack('<f', LIGHT.field_of_view))
    output_stream.write(struct.pack('<f', LIGHT.falloff_distance))
    output_stream.write(struct.pack('<f', LIGHT.cutoff_distance))
    output_stream.write(struct.pack('<I', LIGHT.interpolation_flags))
    output_stream.write(struct.pack('<ff', *LIGHT.bloom_bounds))
    output_stream.write(struct.pack('<fff', LIGHT.specular_lower_bound[0], LIGHT.specular_lower_bound[1], LIGHT.specular_lower_bound[2]))
    output_stream.write(struct.pack('<fff', LIGHT.specular_upper_bound[0], LIGHT.specular_upper_bound[1], LIGHT.specular_upper_bound[2]))
    output_stream.write(struct.pack('<fff', LIGHT.diffuse_lower_bound[0], LIGHT.diffuse_lower_bound[1], LIGHT.diffuse_lower_bound[2]))
    output_stream.write(struct.pack('<fff', LIGHT.diffuse_upper_bound[0], LIGHT.diffuse_upper_bound[1], LIGHT.diffuse_upper_bound[2]))
    output_stream.write(struct.pack('<ff', *LIGHT.brightness_bounds))
    LIGHT.gel_map.write(output_stream, False, True)
    output_stream.write(struct.pack('<H', LIGHT.specular_mask))
    output_stream.write(struct.pack('<6x'))
    output_stream.write(struct.pack('<H', LIGHT.falloff_function))
    output_stream.write(struct.pack('<H', LIGHT.diffuse_contrast))
    output_stream.write(struct.pack('<H', LIGHT.specular_contrast))
    output_stream.write(struct.pack('<H', LIGHT.falloff_geometry))
    LIGHT.lens_flare.write(output_stream, False, True)
    output_stream.write(struct.pack('<f', LIGHT.bounding_radius))
    LIGHT.light_volume.write(output_stream, False, True)
    output_stream.write(struct.pack('<H', LIGHT.default_lightmap_setting))
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<f', LIGHT.lightmap_half_life))
    output_stream.write(struct.pack('<f', LIGHT.lightmap_light_scale))
    output_stream.write(struct.pack('<f', LIGHT.duration))
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<H', LIGHT.effect_falloff_function))
    output_stream.write(struct.pack('<H', LIGHT.illumination_fade))
    output_stream.write(struct.pack('<H', LIGHT.shadow_fade))
    output_stream.write(struct.pack('<H', LIGHT.specular_fade))
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<I', LIGHT.animation_flags))
    LIGHT.brightness_animation_tag_block.write(output_stream, False)
    LIGHT.color_animation_tag_block.write(output_stream, False)
    LIGHT.gel_animation_tag_block.write(output_stream, False)
    LIGHT.shader.write(output_stream, False, True)

def write_brightness_animation(output_stream, TAG, brightness_animation, brightness_animation_header):
    if len(brightness_animation) > 0:
        brightness_animation_header.write(output_stream, TAG, True)
        for brightness_property in brightness_animation:
            shader_processing.write_function_size(output_stream, brightness_property)

        for brightness_property in brightness_animation:
            shader_processing.write_function(output_stream, TAG, brightness_property)

def build_asset(output_stream, LIGHT, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    LIGHT.header.write(output_stream, False, True)
    write_body(output_stream, TAG, LIGHT)

    gel_map_length = len(LIGHT.gel_map.name)
    if gel_map_length > 0:
        output_stream.write(struct.pack('<%ssx' % gel_map_length, TAG.string_to_bytes(LIGHT.gel_map.name, False)))

    lens_flare_length = len(LIGHT.lens_flare.name)
    if lens_flare_length > 0:
        output_stream.write(struct.pack('<%ssx' % lens_flare_length, TAG.string_to_bytes(LIGHT.lens_flare.name, False)))

    light_volume_length = len(LIGHT.light_volume.name)
    if light_volume_length > 0:
        output_stream.write(struct.pack('<%ssx' % light_volume_length, TAG.string_to_bytes(LIGHT.light_volume.name, False)))

    write_brightness_animation(output_stream, TAG, LIGHT.brightness_animation, LIGHT.brightness_animation_header)

    shader_length = len(LIGHT.shader.name)
    if shader_length > 0:
        output_stream.write(struct.pack('<%ssx' % shader_length, TAG.string_to_bytes(LIGHT.shader.name, False)))
