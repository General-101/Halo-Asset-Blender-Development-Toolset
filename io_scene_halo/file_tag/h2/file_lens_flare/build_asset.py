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

from math import radians
from ....global_functions import tag_format, shader_processing

def write_body(output_stream, TAG, LENSFLARE):
    LENSFLARE.lens_flare_body_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<f', radians(LENSFLARE.lens_flare_body.falloff_angle)))
    output_stream.write(struct.pack('<f', radians(LENSFLARE.lens_flare_body.cutoff_angle)))
    output_stream.write(struct.pack('<8x'))
    output_stream.write(struct.pack('<f', LENSFLARE.lens_flare_body.occlusion_radius))
    output_stream.write(struct.pack('<H', LENSFLARE.lens_flare_body.occlusion_offset_direction))
    output_stream.write(struct.pack('<H', LENSFLARE.lens_flare_body.occlusion_inner_radius_scale))
    output_stream.write(struct.pack('<f', LENSFLARE.lens_flare_body.near_fade_distance))
    output_stream.write(struct.pack('<f', LENSFLARE.lens_flare_body.far_fade_distance))
    LENSFLARE.lens_flare_body.bitmap.write(output_stream, False, True)
    output_stream.write(struct.pack('<H', LENSFLARE.lens_flare_body.occlusion_flags))
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<H', LENSFLARE.lens_flare_body.rotation_function))
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<f', radians(LENSFLARE.lens_flare_body.rotation_function_scale)))
    output_stream.write(struct.pack('<ff', *LENSFLARE.lens_flare_body.corona_scale))
    output_stream.write(struct.pack('<H', LENSFLARE.lens_flare_body.falloff_function))
    output_stream.write(struct.pack('<2x'))
    LENSFLARE.lens_flare_body.reflections_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<H', LENSFLARE.lens_flare_body.flags))
    output_stream.write(struct.pack('<2x'))
    LENSFLARE.lens_flare_body.brightness_tag_block.write(output_stream, False)
    LENSFLARE.lens_flare_body.color_tag_block.write(output_stream, False)
    LENSFLARE.lens_flare_body.rotation_tag_block.write(output_stream, False)

def write_reflections(output_stream, TAG, reflections, reflections_header):
    if len(reflections) > 0:
        reflections_header.write(output_stream, TAG, True)
        for reflection in reflections:
            output_stream.write(struct.pack('<H', reflection.flags))
            output_stream.write(struct.pack('<2x'))
            output_stream.write(struct.pack('<H', reflection.bitmap_index))
            output_stream.write(struct.pack('<2x'))
            output_stream.write(struct.pack('<f', reflection.position))
            output_stream.write(struct.pack('<f', reflection.rotation_offset))
            output_stream.write(struct.pack('<ff', *reflection.radius))
            output_stream.write(struct.pack('<ff', *reflection.brightness))
            output_stream.write(struct.pack('<f', reflection.modulation_factor))
            output_stream.write(struct.pack('<fff', reflection.color[0], reflection.color[1], reflection.color[2]))

def write_brightness(output_stream, TAG, brightness, brightness_header):
    if len(brightness) > 0:
        brightness_header.write(output_stream, TAG, True)
        for brightness_property in brightness:
            shader_processing.write_function_size(output_stream, brightness_property)

        for brightness_property in brightness:
            output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("SCFN", True), 0, 1, 12))
            shader_processing.write_function(output_stream, TAG, brightness_property)

def write_color(output_stream, TAG, color, color_header):
    if len(color) > 0:
        color_header.write(output_stream, TAG, True)
        for color_property in color:
            shader_processing.write_function_size(output_stream, color_property)

        for color_property in color:
            output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("CLFN", True), 0, 1, 12))
            shader_processing.write_function(output_stream, TAG, color_property)

def build_asset(output_stream, LENSFLARE, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    LENSFLARE.header.write(output_stream, False, True)
    write_body(output_stream, TAG, LENSFLARE)

    bitmap_length = len(LENSFLARE.lens_flare_body.bitmap.name)
    if bitmap_length > 0:
        output_stream.write(struct.pack('<%ssx' % bitmap_length, TAG.string_to_bytes(LENSFLARE.lens_flare_body.bitmap.name, False)))

    write_reflections(output_stream, TAG, LENSFLARE.reflections, LENSFLARE.reflections_header)
    write_brightness(output_stream, TAG, LENSFLARE.brightness, LENSFLARE.brightness_header)
    write_color(output_stream, TAG, LENSFLARE.color, LENSFLARE.color_header)