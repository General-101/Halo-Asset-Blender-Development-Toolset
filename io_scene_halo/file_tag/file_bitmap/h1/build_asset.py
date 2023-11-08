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

def write_body(output_stream, BITMAP, TAG):
    output_stream.write(struct.pack('>H', BITMAP.bitmap_body.type))
    output_stream.write(struct.pack('>H', BITMAP.bitmap_body.format))
    output_stream.write(struct.pack('>H', BITMAP.bitmap_body.usage))
    output_stream.write(struct.pack('>H', BITMAP.bitmap_body.flags))
    output_stream.write(struct.pack('>f', BITMAP.bitmap_body.detail_fade_factor))
    output_stream.write(struct.pack('>f', BITMAP.bitmap_body.sharpen_amount))
    output_stream.write(struct.pack('>f', BITMAP.bitmap_body.bump_height))
    output_stream.write(struct.pack('>H', BITMAP.bitmap_body.sprite_budget_size))
    output_stream.write(struct.pack('>H', BITMAP.bitmap_body.sprite_budget_count))
    output_stream.write(struct.pack('>H', BITMAP.bitmap_body.color_plate_width))
    output_stream.write(struct.pack('>H', BITMAP.bitmap_body.color_plate_height))
    BITMAP.bitmap_body.compressed_color_plate_data.write(output_stream, True)
    BITMAP.bitmap_body.processed_pixel_data.write(output_stream, True)
    output_stream.write(struct.pack('>f', BITMAP.bitmap_body.blur_filter_size))
    output_stream.write(struct.pack('>f', BITMAP.bitmap_body.alpha_bias))
    output_stream.write(struct.pack('>H', BITMAP.bitmap_body.mipmap_count))
    output_stream.write(struct.pack('>H', BITMAP.bitmap_body.sprite_usage))
    output_stream.write(struct.pack('>H', BITMAP.bitmap_body.sprite_spacing))
    output_stream.write(struct.pack('>2x'))
    BITMAP.bitmap_body.sequences_tag_block.write(output_stream, True)
    BITMAP.bitmap_body.bitmaps_tag_block.write(output_stream, True)

def write_sequences(output_stream, BITMAP, TAG):
    for sequence in BITMAP.sequences:
        output_stream.write(struct.pack('>31sx', TAG.string_to_bytes(sequence.name, False)))
        output_stream.write(struct.pack('>h', sequence.first_bitmap_index))
        output_stream.write(struct.pack('>h', sequence.bitmap_count))
        output_stream.write(struct.pack('>16x'))
        sequence.sprites_tag_block.write(output_stream, True)

    for sequence in BITMAP.sequences:
        for sprite in sequence.sprites:
            output_stream.write(struct.pack('>h', sprite.bitmap_index))
            output_stream.write(struct.pack('>6x'))
            output_stream.write(struct.pack('>f', sprite.left))
            output_stream.write(struct.pack('>f', sprite.right))
            output_stream.write(struct.pack('>f', sprite.top))
            output_stream.write(struct.pack('>f', sprite.bottom))
            output_stream.write(struct.pack('>ff', sprite.registration_point[0], sprite.registration_point[1]))

def write_bitmaps(output_stream, BITMAP, TAG):
    for bitmap in BITMAP.bitmaps:
        output_stream.write(struct.pack('>4s', TAG.string_to_bytes(bitmap.signature, False)))
        output_stream.write(struct.pack('>h', bitmap.width))
        output_stream.write(struct.pack('>h', bitmap.height))
        output_stream.write(struct.pack('>h', bitmap.depth))
        output_stream.write(struct.pack('>h', bitmap.bitmap_type))
        output_stream.write(struct.pack('>h', bitmap.bitmap_format))
        output_stream.write(struct.pack('>h', bitmap.flags))
        output_stream.write(struct.pack('>hh', bitmap.registration_point[0], bitmap.registration_point[1]))
        output_stream.write(struct.pack('>h', bitmap.mipmap_count))
        output_stream.write(struct.pack('>2x'))
        output_stream.write(struct.pack('>i', bitmap.pixels_offset))
        output_stream.write(struct.pack('>20x'))

def build_asset(output_stream, BITMAP, tag_format, report):
    TAG = tag_format.TagAsset()

    BITMAP.header.write(output_stream, True)
    write_body(output_stream, BITMAP, TAG)

    output_stream.write(BITMAP.bitmap_body.compressed_color_plate)
    output_stream.write(BITMAP.bitmap_body.processed_pixels)

    write_sequences(output_stream, BITMAP, TAG)

    write_bitmaps(output_stream, BITMAP, TAG)
