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

from .format import (
        BitmapAsset as H1BitmapAsset,
        BitmapTypeEnum as H1BitmapTypeEnum,
        FormatEnum as H1FormatEnum,
        UsageEnum as H1UsageEnum,
        BitmapFlags as H1BitmapFlags,
        SpriteBudgetSizeEnum as H1SpriteBudgetSizeEnum,
        SpriteUsageEnum as H1SpriteUsageEnum
        )

from ...h2.file_bitmap.format import (
        BitmapAsset,
        BitmapTypeEnum,
        FormatEnum,
        UsageEnum,
        BitmapFlags,
        SpriteBudgetSizeEnum,
        SpriteUsageEnum,
        ForceFormatEnum,
        ColorSubsamplingEnum
        )

def convert_flags(bitmap_flags):
    flags = 0
    active_h1_flags = H1BitmapFlags(bitmap_flags)
    if H1BitmapFlags.enable_diffusion_dithering in active_h1_flags:
        flags += BitmapFlags.enable_diffusion_dithering.value

    if H1BitmapFlags.disable_height_map_compression in active_h1_flags:
        flags += BitmapFlags.disable_height_map_compression.value

    if H1BitmapFlags.uniform_sprite_sequences in active_h1_flags:
        flags += BitmapFlags.uniform_sprite_sequences.value

    if H1BitmapFlags.filthy_sprite_bug_fix in active_h1_flags:
        flags += BitmapFlags.filthy_sprite_bug_fix.value

    if H1BitmapFlags.invert_detail_fade in active_h1_flags:
        flags += BitmapFlags.invert_detail_fade.value

    return flags

def upgrade_h2_bitmap(H1_ASSET, patch_txt_path, tag_format, report):
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

    BITMAP.bitmap_body_header = TAG.TagBlockHeader("tbfd", 0, 1, 112)
    BITMAP.bitmap_body = BITMAP.BitmapBody()
    BITMAP.bitmap_body.type = H1_ASSET.bitmap_body.type
    BITMAP.bitmap_body.format = H1_ASSET.bitmap_body.format
    BITMAP.bitmap_body.usage = H1_ASSET.bitmap_body.usage
    BITMAP.bitmap_body.flags = convert_flags(H1_ASSET.bitmap_body.flags)
    BITMAP.bitmap_body.detail_fade_factor = H1_ASSET.bitmap_body.detail_fade_factor
    BITMAP.bitmap_body.sharpen_amount = H1_ASSET.bitmap_body.sharpen_amount
    repeat_value = 10
    str_bump_height = str(H1_ASSET.bitmap_body.bump_height).split(".", 1)[1]
    for char in str_bump_height:
        if char == "0":
            repeat_value *= 10

        else:
            break

    BITMAP.bitmap_body.bump_height = H1_ASSET.bitmap_body.bump_height * repeat_value
    BITMAP.bitmap_body.sprite_budget_size = H1_ASSET.bitmap_body.sprite_budget_size
    BITMAP.bitmap_body.sprite_budget_count = H1_ASSET.bitmap_body.sprite_budget_count
    BITMAP.bitmap_body.color_plate_width = 0
    BITMAP.bitmap_body.color_plate_height = 0
    BITMAP.bitmap_body.compressed_color_plate_data = TAG.RawData()
    BITMAP.bitmap_body.processed_pixel_data = TAG.RawData()
    BITMAP.bitmap_body.blur_filter_size = H1_ASSET.bitmap_body.blur_filter_size
    BITMAP.bitmap_body.alpha_bias = H1_ASSET.bitmap_body.alpha_bias
    BITMAP.bitmap_body.mipmap_count = H1_ASSET.bitmap_body.mipmap_count
    BITMAP.bitmap_body.sprite_usage = H1_ASSET.bitmap_body.sprite_usage
    BITMAP.bitmap_body.sprite_spacing = H1_ASSET.bitmap_body.sprite_spacing
    BITMAP.bitmap_body.force_format = 0
    BITMAP.bitmap_body.sequences_tag_block = TAG.TagBlock()
    BITMAP.bitmap_body.bitmaps_tag_block = TAG.TagBlock()
    BITMAP.bitmap_body.color_compression_quality = 0
    BITMAP.bitmap_body.alpha_compression_quality = 0
    BITMAP.bitmap_body.overlap = 0
    BITMAP.bitmap_body.color_subsampling = 0

    return BITMAP
