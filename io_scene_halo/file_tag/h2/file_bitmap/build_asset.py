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
from ....global_functions import tag_format

def write_body(output_stream, BITMAP, TAG):
    BITMAP.bitmap_body_header.write(output_stream, TAG, True)
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
    output_stream.write(struct.pack('<B', BITMAP.bitmap_body.color_compression_quality))
    output_stream.write(struct.pack('<B', BITMAP.bitmap_body.alpha_compression_quality))
    output_stream.write(struct.pack('<B', BITMAP.bitmap_body.overlap))
    output_stream.write(struct.pack('<B', BITMAP.bitmap_body.color_subsampling))

def write_sequences(output_stream, BITMAP, TAG):
    if len(BITMAP.sequences) > 0:
        BITMAP.sequence_header.write(output_stream, TAG, True)
        for sequence in BITMAP.sequences:
            output_stream.write(struct.pack('<31sx', tag_format.string_to_bytes(sequence.name, False)))
            output_stream.write(struct.pack('<h', sequence.first_bitmap_index))
            output_stream.write(struct.pack('<h', sequence.bitmap_count))
            output_stream.write(struct.pack('<16x'))
            sequence.sprites_tag_block.write(output_stream, False)

        for sequence in BITMAP.sequences:
            if len(sequence.sprites) > 0:
                sequence.sprites_header.write(output_stream, TAG, True)
                for sprite in sequence.sprites:
                    output_stream.write(struct.pack('<h', sprite.bitmap_index))
                    output_stream.write(struct.pack('<6x'))
                    output_stream.write(struct.pack('<f', sprite.left))
                    output_stream.write(struct.pack('<f', sprite.right))
                    output_stream.write(struct.pack('<f', sprite.top))
                    output_stream.write(struct.pack('<f', sprite.bottom))
                    output_stream.write(struct.pack('<ff', sprite.registration_point[0], sprite.registration_point[1]))

def write_bitmaps(output_stream, BITMAP, TAG):
    if len(BITMAP.bitmaps) > 0:
        BITMAP.bitmap_header.write(output_stream, TAG, True)
        for bitmap in BITMAP.bitmaps:
            output_stream.write(struct.pack('<4s', tag_format.string_to_bytes(bitmap.signature, True)))
            output_stream.write(struct.pack('<h', bitmap.width))
            output_stream.write(struct.pack('<h', bitmap.height))
            output_stream.write(struct.pack('<b', bitmap.depth))
            output_stream.write(struct.pack('<b', bitmap.more_flags))
            output_stream.write(struct.pack('<h', bitmap.bitmap_type))
            output_stream.write(struct.pack('<h', bitmap.bitmap_format))
            output_stream.write(struct.pack('<h', bitmap.flags))
            output_stream.write(struct.pack('<hh', bitmap.registration_point[0], bitmap.registration_point[1]))
            output_stream.write(struct.pack('<h', bitmap.mipmap_count))
            output_stream.write(struct.pack('<b', bitmap.lod_adjust))
            output_stream.write(struct.pack('<b', bitmap.cache_usage))
            output_stream.write(struct.pack('<i', bitmap.pixels_offset))
            output_stream.write(struct.pack('<4x'))
            bitmap.native_mipmap_info_tag_block.write(output_stream, False)
            output_stream.write(struct.pack('<i', bitmap.native_size))
            output_stream.write(struct.pack('<i', bitmap.tile_mode))
            output_stream.write(struct.pack('<88x'))

        for bitmap in BITMAP.bitmaps:
            bitmap.nbmi_header.write(output_stream, TAG, True)
            if len(bitmap.native_mipmap_info) > 0:
                bitmap.native_mipmap_info_header.write(output_stream, TAG, True)
                for native_mipmap_info in bitmap.native_mipmap_info:
                    output_stream.write(struct.pack('<i', native_mipmap_info.offset))
                    output_stream.write(struct.pack('<i', native_mipmap_info.pitch_row))
                    output_stream.write(struct.pack('<i', native_mipmap_info.pitch_slice))

def build_asset(output_stream, BITMAP, report):
    TAG = tag_format.TagAsset()
    TAG.big_endian = False

    BITMAP.header.write(output_stream, TAG.big_endian, True)
    write_body(output_stream, BITMAP, TAG)

    output_stream.write(BITMAP.bitmap_body.compressed_color_plate)
    output_stream.write(BITMAP.bitmap_body.processed_pixels)

    write_sequences(output_stream, BITMAP, TAG)
    write_bitmaps(output_stream, BITMAP, TAG)
