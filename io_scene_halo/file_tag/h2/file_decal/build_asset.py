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

def write_body(output_stream, TAG, DECAL):
    DECAL.body_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<H', DECAL.flags))
    output_stream.write(struct.pack('<H', DECAL.decal_type))
    output_stream.write(struct.pack('<H', DECAL.layer))
    output_stream.write(struct.pack('<h', DECAL.max_overlapping_count))
    DECAL.next_decal_in_chain.write(output_stream, False, True)
    output_stream.write(struct.pack('<ff', *DECAL.radius))
    output_stream.write(struct.pack('<f', DECAL.radius_overlap_rejection))
    output_stream.write(struct.pack('<fff', DECAL.color_lower_bounds[0], DECAL.color_lower_bounds[1], DECAL.color_lower_bounds[2]))
    output_stream.write(struct.pack('<fff', DECAL.color_upper_bounds[0], DECAL.color_upper_bounds[1], DECAL.color_upper_bounds[2]))
    output_stream.write(struct.pack('<ff', *DECAL.lifetime))
    output_stream.write(struct.pack('<ff', *DECAL.decay_time))
    output_stream.write(struct.pack('<68x'))
    DECAL.bitmap.write(output_stream, False, True)
    output_stream.write(struct.pack('<20x'))
    output_stream.write(struct.pack('<f', DECAL.maximum_sprite_extent))
    output_stream.write(struct.pack('<4x'))

def build_asset(output_stream, DECAL, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    DECAL.header.write(output_stream, False, True)
    write_body(output_stream, TAG, DECAL)

    next_decal_in_chain_length = len(DECAL.next_decal_in_chain.name)
    if next_decal_in_chain_length > 0:
        output_stream.write(struct.pack('<%ssx' % next_decal_in_chain_length, TAG.string_to_bytes(DECAL.next_decal_in_chain.name, False)))

    bitmap_length = len(DECAL.bitmap.name)
    if bitmap_length > 0:
        output_stream.write(struct.pack('<%ssx' % bitmap_length, TAG.string_to_bytes(DECAL.bitmap.name, False)))
