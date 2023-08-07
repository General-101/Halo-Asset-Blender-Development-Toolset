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

def write_body(output_stream, BITMAP):
    BITMAP.bitmap_body_header.write(output_stream, False, True)
    output_stream.write(struct.pack('<H', BITMAP.bitmap_body.type))
    output_stream.write(struct.pack('<H', BITMAP.bitmap_body.format))
    output_stream.write(struct.pack('<H', BITMAP.bitmap_body.usage))
    output_stream.write(struct.pack('<H', BITMAP.bitmap_body.flags))
    output_stream.write(struct.pack('<f', BITMAP.bitmap_body.detail_fade_factor))
    output_stream.write(struct.pack('<f', BITMAP.bitmap_body.sharpen_amount))
    output_stream.write(struct.pack('<f', BITMAP.bitmap_body.bump_height))
    output_stream.write(struct.pack('<H', BITMAP.bitmap_body.sprite_budget_size))
    output_stream.write(struct.pack('<H', BITMAP.bitmap_body.sprite_budget_count))
    output_stream.write(struct.pack('<H', BITMAP.bitmap_body.color_plate_width))
    output_stream.write(struct.pack('<H', BITMAP.bitmap_body.color_plate_height))
    BITMAP.bitmap_body.compressed_color_plate_data.write(output_stream, False)
    BITMAP.bitmap_body.processed_pixel_data.write(output_stream, False)
    output_stream.write(struct.pack('<f', BITMAP.bitmap_body.blur_filter_size))
    output_stream.write(struct.pack('<f', BITMAP.bitmap_body.alpha_bias))
    output_stream.write(struct.pack('<H', BITMAP.bitmap_body.mipmap_count))
    output_stream.write(struct.pack('<H', BITMAP.bitmap_body.sprite_usage))
    output_stream.write(struct.pack('<H', BITMAP.bitmap_body.sprite_spacing))
    output_stream.write(struct.pack('<H', BITMAP.bitmap_body.force_format))
    BITMAP.bitmap_body.sequences_tag_block.write(output_stream, False)
    BITMAP.bitmap_body.bitmaps_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<b', BITMAP.bitmap_body.color_compression_quality))
    output_stream.write(struct.pack('<b', BITMAP.bitmap_body.alpha_compression_quality))
    output_stream.write(struct.pack('<b', BITMAP.bitmap_body.overlap))
    output_stream.write(struct.pack('<B', BITMAP.bitmap_body.color_subsampling))

def build_asset(output_stream, BITMAP, report):
    BITMAP.header.write(output_stream, False, True)
    write_body(output_stream, BITMAP)
