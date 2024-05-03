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

from enum import Flag, Enum, auto

class ImportTypeEnum(Enum):
    _2d_textures = 0
    _3d_textures = auto()
    cube_maps = auto()
    sprites = auto()
    interface_bitmaps = auto()

class FormatEnum(Enum):
    compressed_with_color_key_transparency = 0
    compressed_with_explicit_alpha = auto()
    compressed_with_interpolated_alpha = auto()
    _16bit_color = auto()
    _32bit_color = auto()
    monochrome = auto()

class UsageEnum(Enum):
    alpha_blend = 0
    default = auto()
    height_map = auto()
    detail_map = auto()
    light_map = auto()
    vector_map = auto()
    height_map_blue_255 = auto()
    embm = auto()
    height_map_a8l8 = auto()
    height_map_g8b8 = auto()
    height_map_g8b8_with_alpha = auto()

class ImportFlags(Flag):
    enable_diffusion_dithering = auto()
    disable_height_map_compression = auto()
    uniform_sprite_sequences = auto()
    filthy_sprite_bug_fix = auto()
    use_sharp_bump_filter = auto()
    wdp_compression = auto()
    use_clamped_mirrored_bump_filter = auto()
    invert_detail_fade = auto()
    swap_x_y_vector_components = auto()
    convert_from_signed = auto()
    convert_to_signed = auto()
    import_mipmap_chains = auto()
    intentionally_true_color = auto()
    og_xbox_mipmap_selection = auto()

class SpriteBudgetSizeEnum(Enum):
    _32x32 = 0
    _64x64 = auto()
    _128x128 = auto()
    _256x256 = auto()
    _512x512 = auto()
    _1024x1024 = auto()

class SpriteUsageEnum(Enum):
    blend_add_subtract_max = 0
    multiply_min = auto()
    double_multiply = auto()

class ForceFormatEnum(Enum):
    default = 0
    force_g8b8 = auto()
    force_dxt1 = auto()
    force_dxt3 = auto()
    force_dxt5 = auto()
    force_alpha_lumincance8 = auto()
    force_a4r4g4b4 = auto()

class MoreFlags(Flag):
    delete_from_cache_file = auto()
    bitmap_create_attempted = auto()
    bitmap_recreate_allowed = auto()
    bitmap_sampling_allowed = auto()

class BitmapTypeEnum(Enum):
    _2d_texture = 0
    _3d_texture = auto()
    cube_map = auto()

class BitmapFormatEnum(Enum):
    a8 = 0
    y8 = auto()
    ay8 = auto()
    a8y8 = auto()
    unused1 = auto()
    unused2 = auto()
    r5g6b5 = auto()
    unused3 = auto()
    a1r5g5b5 = auto()
    a4r4g4b4 = auto()
    x8r8g8b8 = auto()
    a8r8g8b8 = auto()
    unused4 = auto()
    unused5 = auto()
    dxt1 = auto()
    dxt3 = auto()
    dxt5 = auto()
    p8_bump = auto()
    p8 = auto()
    argbfb32 = auto()
    rgbfb32 = auto()
    rgbfb16 = auto()
    v8u8 = auto()
    g8b8 = auto()

class BitmapFlags(Flag):
    power_of_two_dimensions = auto()
    compressed = auto()
    palettized = auto()
    swizzled = auto()
    linear = auto()
    v16u16 = auto()
    mipmap_debug_level = auto()
    prefer_stutter = auto()

class CacheUsageEnum(Enum):
    default = 0
    environment = auto()
    environment_bump = auto()
    environment_lightmap = auto()
    scenery = auto()
    scenery_bump = auto()
    weapon = auto()
    weapon_bump = auto()
    vehicle = auto()
    vehicle_bump = auto()
    biped = auto()
    biped_bump = auto()
    object = auto()
    object_bump = auto()
    effect = auto()
    hud = auto()
    ui = auto()
    sky = auto()
    first_person = auto()
    rasterizer = auto()

class BitmapAsset():
    def __init__(self):
        self.header = None
        self.bitmap_body_header = None
        self.bitmap_body = None
        self.sequence_header = None
        self.sequences = None
        self.bitmap_header = None
        self.bitmaps = None

    class BitmapBody:
        def __init__(self, type=0, format=0, usage=0, flags=0, detail_fade_factor=0.0, sharpen_amount=0.0, bump_height=0.0, sprite_budget_size=0, sprite_budget_count=0,
                     color_plate_width=0, color_plate_height=0, compressed_color_plate_data=None, compressed_color_plate=None, processed_pixel_data=None, processed_pixels=None,
                     blur_filter_size=0.0, alpha_bias=0.0, mipmap_count=0, sprite_usage=0, sprite_spacing=0, force_format=0, sequences_tag_block=None, bitmaps_tag_block=None,
                     color_compression_quality=0, alpha_compression_quality=0, overlap=0, color_subsampling=0):
            self.type = type
            self.format = format
            self.usage = usage
            self.flags = flags
            self.detail_fade_factor = detail_fade_factor
            self.sharpen_amount = sharpen_amount
            self.bump_height = bump_height
            self.sprite_budget_size = sprite_budget_size
            self.sprite_budget_count = sprite_budget_count
            self.color_plate_width = color_plate_width
            self.color_plate_height = color_plate_height
            self.compressed_color_plate_data = compressed_color_plate_data
            self.compressed_color_plate = compressed_color_plate
            self.processed_pixel_data = processed_pixel_data
            self.processed_pixels = processed_pixels
            self.blur_filter_size = blur_filter_size
            self.alpha_bias = alpha_bias
            self.mipmap_count = mipmap_count
            self.sprite_usage = sprite_usage
            self.sprite_spacing = sprite_spacing
            self.force_format = force_format
            self.sequences_tag_block = sequences_tag_block
            self.bitmaps_tag_block = bitmaps_tag_block
            self.color_compression_quality = color_compression_quality
            self.alpha_compression_quality = alpha_compression_quality
            self.overlap = overlap
            self.color_subsampling = color_subsampling

    class Sequence:
        def __init__(self, name="", first_bitmap_index=0, bitmap_count=0, sprites_tag_block=None, sprites_header=None, sprites=None):
            self.name = name
            self.first_bitmap_index = first_bitmap_index
            self.bitmap_count = bitmap_count
            self.sprites_tag_block = sprites_tag_block
            self.sprites_header = sprites_header
            self.sprites = sprites

    class Sprite:
        def __init__(self, bitmap_index=0, left=0, right=0, top=0, bottom=0, registration_point=(0.0, 0.0)):
            self.bitmap_index = bitmap_index
            self.left = left
            self.right = right
            self.top = top
            self.bottom = bottom
            self.registration_point = registration_point

    class Bitmap:
        def __init__(self, signature="", width=0, height=0, depth=0, more_flags=0, bitmap_type=0, bitmap_format=0, flags=0, registration_point=(0, 0), mipmap_count=0,
                     lod_adjust=0, cache_usage=0, pixels_offset=0, native_mipmap_info_tag_block=None, native_mipmap_info_header=None, native_mipmap_info=None, native_size=0,
                     tile_mode=0, nbmi_header=None):
            self.signature = signature
            self.width = width
            self.height = height
            self.depth = depth
            self.more_flags = more_flags
            self.bitmap_type = bitmap_type
            self.bitmap_format = bitmap_format
            self.flags = flags
            self.registration_point = registration_point
            self.mipmap_count = mipmap_count
            self.lod_adjust = lod_adjust
            self.cache_usage = cache_usage
            self.pixels_offset = pixels_offset
            self.native_mipmap_info_tag_block = native_mipmap_info_tag_block
            self.native_mipmap_info_header = native_mipmap_info_header
            self.native_mipmap_info = native_mipmap_info
            self.native_size = native_size
            self.tile_mode = tile_mode
            self.nbmi_header = nbmi_header

    class NativeMipMapInfo:
        def __init__(self, offset=0, pitch_row=0, pitch_slice=0):
            self.offset = offset
            self.pitch_row = pitch_row
            self.pitch_slice = pitch_slice
