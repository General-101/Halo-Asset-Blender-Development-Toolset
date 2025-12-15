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

class H1FormatEnum(Enum):
    compressed_with_color_key_transparency = 0
    compressed_with_explicit_alpha = auto()
    compressed_with_interpolated_alpha = auto()
    _16bit_color = auto()
    _32bit_color = auto()
    monochrome = auto()
    high_quality_compression = auto()

class H2FormatEnum(Enum):
    compressed_with_color_key_transparency = 0
    compressed_with_explicit_alpha = auto()
    compressed_with_interpolated_alpha = auto()
    _16bit_color = auto()
    _32bit_color = auto()
    monochrome = auto()

class H1ImportFlags(Flag):
    enable_diffusion_dithering = auto()
    disable_height_map_compression = auto()
    uniform_sprite_sequences = auto()
    filthy_sprite_bug_fix = auto()
    hud_scale_halved = auto()
    invert_detail_fade = auto()
    use_average_color_for_detail_fade = auto()

class H2ImportFlags(Flag):
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

def convert_format(format_index):
    h2_format_index = 0
    h1_format = H1FormatEnum(format_index)
    if h1_format == H1FormatEnum.compressed_with_color_key_transparency:
        h2_format_index = H2FormatEnum.compressed_with_color_key_transparency.value
    elif h1_format == H1FormatEnum.compressed_with_explicit_alpha:
        h2_format_index = H2FormatEnum.compressed_with_explicit_alpha.value
    elif h1_format == H1FormatEnum.compressed_with_interpolated_alpha:
        h2_format_index = H2FormatEnum.compressed_with_interpolated_alpha.value
    elif h1_format == H1FormatEnum._16bit_color:
        h2_format_index = H2FormatEnum._16bit_color.value
    elif h1_format == H1FormatEnum._32bit_color:
        h2_format_index = H2FormatEnum._32bit_color.value
    elif h1_format == H1FormatEnum.monochrome:
        h2_format_index = H2FormatEnum.monochrome.value
    elif h1_format == H1FormatEnum.high_quality_compression:
        h2_format_index = H2FormatEnum._32bit_color.value
    return h2_format_index

def convert_flags(bitmap_flags):
    flags = 0
    active_h1_flags = H1ImportFlags(bitmap_flags)
    if H1ImportFlags.enable_diffusion_dithering in active_h1_flags:
        flags += H2ImportFlags.enable_diffusion_dithering.value

    if H1ImportFlags.disable_height_map_compression in active_h1_flags:
        flags += H2ImportFlags.disable_height_map_compression.value

    if H1ImportFlags.uniform_sprite_sequences in active_h1_flags:
        flags += H2ImportFlags.uniform_sprite_sequences.value

    if H1ImportFlags.filthy_sprite_bug_fix in active_h1_flags:
        flags += H2ImportFlags.filthy_sprite_bug_fix.value

    if H1ImportFlags.invert_detail_fade in active_h1_flags:
        flags += H2ImportFlags.invert_detail_fade.value

    return flags

def upgrade_bitmap(h1_bitm_asset, report):
    repeat_value = 10
    h1_bump_height = h1_bitm_asset["Data"]["bump height"]
    str_bump_height = str(h1_bump_height).split(".", 1)[1]
    for char in str_bump_height:
        if char == "0":
            repeat_value *= 10

        else:
            break

    h2_bump_height = h1_bump_height * repeat_value

    h2_bitm_asset = {
        "Data": {
            "type": {"type": "ShortEnum", "value": h1_bitm_asset["Data"]["type"]["value"], "value name": ""},
            "format": {"type": "ShortEnum", "value": convert_format(h1_bitm_asset["Data"]["encoding format"]["value"]), "value name": ""},
            "usage": {"type": "ShortEnum", "value": h1_bitm_asset["Data"]["usage"]["value"], "value name": ""},
            "flags": convert_flags(h1_bitm_asset["Data"]["flags"]),
            "detail fade factor": h1_bitm_asset["Data"]["detail fade factor"],
            "sharpen amount": h1_bitm_asset["Data"]["sharpen amount"],
            "bump height": h2_bump_height,
            "ShortEnum": {"type": "ShortEnum", "value": h1_bitm_asset["Data"]["size"]["value"], "value name": ""},
            "ShortInteger": h1_bitm_asset["Data"]["count"],
            "blur filter size": h1_bitm_asset["Data"]["blur filter size"],
            "alpha bias": h1_bitm_asset["Data"]["alpha bias"],
            "mipmap count": h1_bitm_asset["Data"]["mipmap count"],
            "sprite usage": {"type": "ShortEnum", "value": h1_bitm_asset["Data"]["usage_1"]["value"], "value name": ""},
            "sprite spacing": h1_bitm_asset["Data"]["spacing"]
        }
    }

    return h2_bitm_asset
