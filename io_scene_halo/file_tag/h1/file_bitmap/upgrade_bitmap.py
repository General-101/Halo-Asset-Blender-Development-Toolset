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

from .format import ImportFlags as H1ImportFlags, FormatEnum as H1FormatEnum
from ...h2.file_bitmap.format import (
    BitmapAsset,
    ImportFlags,
    FormatEnum
    )
from ....global_functions import tag_format

def convert_format(format_index):
    h2_format_index = 0
    h1_format = H1FormatEnum(format_index)
    if h1_format == H1FormatEnum.compressed_with_color_key_transparency:
        h2_format_index = FormatEnum.compressed_with_color_key_transparency.value
    elif h1_format == H1FormatEnum.compressed_with_explicit_alpha:
        h2_format_index = FormatEnum.compressed_with_explicit_alpha.value
    elif h1_format == H1FormatEnum.compressed_with_interpolated_alpha:
        h2_format_index = FormatEnum.compressed_with_interpolated_alpha.value
    elif h1_format == H1FormatEnum._16bit_color:
        h2_format_index = FormatEnum._16bit_color.value
    elif h1_format == H1FormatEnum._32bit_color:
        h2_format_index = FormatEnum._32bit_color.value
    elif h1_format == H1FormatEnum.monochrome:
        h2_format_index = FormatEnum.monochrome.value
    elif h1_format == H1FormatEnum.high_quality_compression:
        h2_format_index = FormatEnum._32bit_color.value
    return h2_format_index

def convert_flags(bitmap_flags):
    flags = 0
    active_h1_flags = H1ImportFlags(bitmap_flags)
    if H1ImportFlags.enable_diffusion_dithering in active_h1_flags:
        flags += ImportFlags.enable_diffusion_dithering.value

    if H1ImportFlags.disable_height_map_compression in active_h1_flags:
        flags += ImportFlags.disable_height_map_compression.value

    if H1ImportFlags.uniform_sprite_sequences in active_h1_flags:
        flags += ImportFlags.uniform_sprite_sequences.value

    if H1ImportFlags.filthy_sprite_bug_fix in active_h1_flags:
        flags += ImportFlags.filthy_sprite_bug_fix.value

    if H1ImportFlags.invert_detail_fade in active_h1_flags:
        flags += ImportFlags.invert_detail_fade.value

    return flags

def upgrade_h2_bitmap(H1_ASSET, patch_txt_path, report):
    TAG = tag_format.TagAsset()
    BITMAP = BitmapAsset()
    TAG.upgrade_patches = tag_format.get_patch_set(patch_txt_path)

    BITMAP.header = TAG.Header()
    BITMAP.header.unk1 = 0
    BITMAP.header.flags = 0
    BITMAP.header.type = 0
    BITMAP.header.name = ""
    BITMAP.header.tag_group = "bitm"
    BITMAP.header.checksum = 0
    BITMAP.header.data_offset = 64
    BITMAP.header.data_length = 0
    BITMAP.header.unk2 = 0
    BITMAP.header.version = 7
    BITMAP.header.destination = 0
    BITMAP.header.plugin_handle = -1
    BITMAP.header.engine_tag = "BLM!"

    BITMAP.sequences = []
    BITMAP.bitmaps = []

    BITMAP.body_header = TAG.TagBlockHeader("tbfd", 0, 1, 112)
    BITMAP.bitmap_type = H1_ASSET.bitmap_type
    BITMAP.bitmap_format = convert_format(H1_ASSET.bitmap_format)
    BITMAP.usage = H1_ASSET.usage
    BITMAP.flags = convert_flags(H1_ASSET.flags)
    BITMAP.detail_fade_factor = H1_ASSET.detail_fade_factor
    BITMAP.sharpen_amount = H1_ASSET.sharpen_amount
    repeat_value = 10
    str_bump_height = str(H1_ASSET.bump_height).split(".", 1)[1]
    for char in str_bump_height:
        if char == "0":
            repeat_value *= 10

        else:
            break

    BITMAP.bump_height = H1_ASSET.bump_height * repeat_value
    BITMAP.sprite_budget_size = H1_ASSET.sprite_budget_size
    BITMAP.sprite_budget_count = H1_ASSET.sprite_budget_count
    BITMAP.color_plate_width = 0
    BITMAP.color_plate_height = 0
    BITMAP.compressed_color_plate_data = TAG.RawData()
    BITMAP.processed_pixel_data = TAG.RawData()
    BITMAP.compressed_color_plate = bytes()
    BITMAP.processed_pixels = bytes()
    BITMAP.blur_filter_size = H1_ASSET.blur_filter_size
    BITMAP.alpha_bias = H1_ASSET.alpha_bias
    BITMAP.mipmap_count = H1_ASSET.mipmap_count
    BITMAP.sprite_usage = H1_ASSET.sprite_usage
    BITMAP.sprite_spacing = H1_ASSET.sprite_spacing
    BITMAP.force_format = 0
    BITMAP.sequences_tag_block = TAG.TagBlock()
    BITMAP.bitmaps_tag_block = TAG.TagBlock()
    BITMAP.color_compression_quality = 0
    BITMAP.alpha_compression_quality = 0
    BITMAP.overlap = 0
    BITMAP.color_subsampling = 0

    return BITMAP
