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
    DECAL.decal_body_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<H', DECAL.decal_body.flags))
    output_stream.write(struct.pack('<H', DECAL.decal_body.decal_type))
    output_stream.write(struct.pack('<H', DECAL.decal_body.layer))
    output_stream.write(struct.pack('<h', DECAL.decal_body.max_overlapping_count))
    DECAL.decal_body.next_decal_in_chain.write(output_stream, False, True)
    output_stream.write(struct.pack('<ff', *DECAL.decal_body.radius))
    output_stream.write(struct.pack('<f', DECAL.decal_body.radius_overlap_rejection))
    output_stream.write(struct.pack('<fff', DECAL.decal_body.color_lower_bounds[0], DECAL.decal_body.color_lower_bounds[1], DECAL.decal_body.color_lower_bounds[2]))
    output_stream.write(struct.pack('<fff', DECAL.decal_body.color_upper_bounds[0], DECAL.decal_body.color_upper_bounds[1], DECAL.decal_body.color_upper_bounds[2]))
    output_stream.write(struct.pack('<ff', *DECAL.decal_body.lifetime))
    output_stream.write(struct.pack('<ff', *DECAL.decal_body.decay_time))
    output_stream.write(struct.pack('<68x'))
    DECAL.decal_body.bitmap.write(output_stream, False, True)
    output_stream.write(struct.pack('<20x'))
    output_stream.write(struct.pack('<f', DECAL.decal_body.maximum_sprite_extent))
    output_stream.write(struct.pack('<4x'))

def build_asset(output_stream, DECAL, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    DECAL.header.write(output_stream, False, True)
    write_body(output_stream, TAG, DECAL)

    next_decal_in_chain_length = len(DECAL.decal_body.next_decal_in_chain.name)
    if next_decal_in_chain_length > 0:
        output_stream.write(struct.pack('<%ssx' % next_decal_in_chain_length, TAG.string_to_bytes(DECAL.decal_body.next_decal_in_chain.name, False)))

    bitmap_length = len(DECAL.decal_body.bitmap.name)
    if bitmap_length > 0:
        output_stream.write(struct.pack('<%ssx' % bitmap_length, TAG.string_to_bytes(DECAL.decal_body.bitmap.name, False)))
