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

import io
import os
import sys
import json
import base64
import subprocess
import tag_common

from enum import Flag, Enum, auto
from tag_definitions import h1, h2, common
from tag_upgrading.h1 import upgrade_functions as h1_upgrade_functions
from tag_upgrading.h2 import upgrade_functions as h2_upgrade_functions
from tag_interface import read_file, write_file, obfuscation_buffer_prepare
from tag_postprocessing.h1 import postprocess_functions as h1_postprocess_functions
from tag_postprocessing.h2 import postprocess_functions as h2_postprocess_functions, create_function

# SET ME
SOX_TOOL = r"sox.exe"

try:
    from PIL import Image
except ModuleNotFoundError:
    print("PIL not found. Unable to create image node.")
    Image = None

class OldEncodingEnum(Enum):
    _8bit = 0
    _8bit_intensity = auto()
    _16bit_555 = auto()
    _16bit_565 = auto()
    _16bit_4444 = auto()
    _16bit_8palette_plus_8alpha = auto()
    _32bit = auto()

class EncodingEnum(Enum):
    _8bit = 0
    _8bit_intensity = auto()
    _16bit_555 = auto()
    _16bit_565 = auto()
    _16bit_4444 = auto()
    _16bit_8palette_plus_8alpha = auto()
    _16bit_intensity = auto()
    _32bit_888 = auto()
    _32bit_8888 = auto()
    _32bit_compressed = auto()
    _32bit_alpha_compressed = auto()

class BitmapFormatEnum(Enum):
    _16_bit_quarter_size = 0
    _16_bit_half_size = auto()
    _32_bit_half_size = auto()
    _32_bit_full_size = auto()
    _16_bit_full_size = auto()

def get_version_args(game_version):
    engine_tag = None
    tag_defs = None
    tag_groups = None
    tag_extensions = None
    postprocess_functions = None
    is_prerelease = False
    if game_version == 19980319:
        game_defs = h1
        engine_tag = tag_common.EngineTag.H1Latest.value
        tag_defs = tag_common.h1_19980319_defs_directory
        tag_groups = tag_common.h1_19980319_tag_groups
        tag_extensions = tag_common.h1_19980319_tag_extensions
        postprocess_functions = None
        is_prerelease = True
    elif game_version == 19980403:
        game_defs = h1
        engine_tag = tag_common.EngineTag.H1Latest.value
        tag_defs = tag_common.h1_19980403_defs_directory
        tag_groups = tag_common.h1_19980403_tag_groups
        tag_extensions = tag_common.h1_19980403_tag_extensions
        postprocess_functions = None
        is_prerelease = True
    elif game_version == 19980512:
        game_defs = h1
        engine_tag = tag_common.EngineTag.H1Latest.value
        tag_defs = tag_common.h1_19980512_defs_directory
        tag_groups = tag_common.h1_19980512_tag_groups
        tag_extensions = tag_common.h1_19980512_tag_extensions
        postprocess_functions = None
        is_prerelease = True
    elif game_version == 19980514:
        game_defs = h1
        engine_tag = tag_common.EngineTag.H1Latest.value
        tag_defs = tag_common.h1_19980514_defs_directory
        tag_groups = tag_common.h1_19980514_tag_groups
        tag_extensions = tag_common.h1_19980514_tag_extensions
        postprocess_functions = None
        is_prerelease = True
    elif game_version == 19980624:
        game_defs = h1
        engine_tag = tag_common.EngineTag.H1Latest.value
        tag_defs = tag_common.h1_19980624_defs_directory
        tag_groups = tag_common.h1_19980624_tag_groups
        tag_extensions = tag_common.h1_19980624_tag_extensions
        postprocess_functions = None
        is_prerelease = True
    elif game_version == 19980708:
        game_defs = h1
        engine_tag = tag_common.EngineTag.H1Latest.value
        tag_defs = tag_common.h1_19980708_defs_directory
        tag_groups = tag_common.h1_19980708_tag_groups
        tag_extensions = tag_common.h1_19980708_tag_extensions
        postprocess_functions = None
        is_prerelease = True
    elif game_version == 19981008:
        game_defs = h1
        engine_tag = tag_common.EngineTag.H1Latest.value
        tag_defs = tag_common.h1_19981008_defs_directory
        tag_groups = tag_common.h1_19981008_tag_groups
        tag_extensions = tag_common.h1_19981008_tag_extensions
        postprocess_functions = None
        is_prerelease = True
    elif game_version == 19981022:
        game_defs = h1
        engine_tag = tag_common.EngineTag.H1Latest.value
        tag_defs = tag_common.h1_19981022_defs_directory
        tag_groups = tag_common.h1_19981022_tag_groups
        tag_extensions = tag_common.h1_19981022_tag_extensions
        postprocess_functions = None
        is_prerelease = True
    elif game_version == 19990225:
        game_defs = h1
        engine_tag = tag_common.EngineTag.H1Latest.value
        tag_defs = tag_common.h1_19990225_defs_directory
        tag_groups = tag_common.h1_19990225_tag_groups
        tag_extensions = tag_common.h1_19990225_tag_extensions
        postprocess_functions = None
        is_prerelease = True
    elif game_version == 19990302:
        game_defs = h1
        engine_tag = tag_common.EngineTag.H1Latest.value
        tag_defs = tag_common.h1_19990302_defs_directory
        tag_groups = tag_common.h1_19990302_tag_groups
        tag_extensions = tag_common.h1_19990302_tag_extensions
        postprocess_functions = None
        is_prerelease = True
    elif game_version == 19990426:
        game_defs = h1
        engine_tag = tag_common.EngineTag.H1Latest.value
        tag_defs = tag_common.h1_19990426_defs_directory
        tag_groups = tag_common.h1_19990426_tag_groups
        tag_extensions = tag_common.h1_19990426_tag_extensions
        postprocess_functions = None
        is_prerelease = True
    elif game_version == 19990608:
        game_defs = h1
        engine_tag = tag_common.EngineTag.H1Latest.value
        tag_defs = tag_common.h1_19990608_defs_directory
        tag_groups = tag_common.h1_19990608_tag_groups
        tag_extensions = tag_common.h1_19990608_tag_extensions
        postprocess_functions = None
        is_prerelease = True
    elif game_version == 19990623:
        game_defs = h1
        engine_tag = tag_common.EngineTag.H1Latest.value
        tag_defs = tag_common.h1_19990623_defs_directory
        tag_groups = tag_common.h1_19990623_tag_groups
        tag_extensions = tag_common.h1_19990623_tag_extensions
        postprocess_functions = None
        is_prerelease = True
    elif game_version == 19990730:
        game_defs = h1
        engine_tag = tag_common.EngineTag.H1Latest.value
        tag_defs = tag_common.h1_19990730_defs_directory
        tag_groups = tag_common.h1_19990730_tag_groups
        tag_extensions = tag_common.h1_19990730_tag_extensions
        postprocess_functions = None
        is_prerelease = True
    elif game_version == 19990924:
        game_defs = h1
        engine_tag = tag_common.EngineTag.H1Latest.value
        tag_defs = tag_common.h1_19990924_defs_directory
        tag_groups = tag_common.h1_19990924_tag_groups
        tag_extensions = tag_common.h1_19990924_tag_extensions
        postprocess_functions = None
        is_prerelease = True
    elif game_version == 19990930:
        game_defs = h1
        engine_tag = tag_common.EngineTag.H1Latest.value
        tag_defs = tag_common.h1_19990930_defs_directory
        tag_groups = tag_common.h1_19990930_tag_groups
        tag_extensions = tag_common.h1_19990930_tag_extensions
        postprocess_functions = None
        is_prerelease = True
    elif game_version == 19991021:
        game_defs = h1
        engine_tag = tag_common.EngineTag.H1Latest.value
        tag_defs = tag_common.h1_19991021_defs_directory
        tag_groups = tag_common.h1_19991021_tag_groups
        tag_extensions = tag_common.h1_19991021_tag_extensions
        postprocess_functions = None
        is_prerelease = True
    elif game_version == 20000525:
        game_defs = h1
        engine_tag = tag_common.EngineTag.H1Latest.value
        tag_defs = tag_common.h1_20000525_defs_directory
        tag_groups = tag_common.h1_20000525_tag_groups
        tag_extensions = tag_common.h1_20000525_tag_extensions
        postprocess_functions = None
        is_prerelease = True
    elif game_version == 20001005:
        game_defs = h1
        engine_tag = tag_common.EngineTag.H1Latest.value
        tag_defs = tag_common.h1_20001005_defs_directory
        tag_groups = tag_common.h1_20001005_tag_groups
        tag_extensions = tag_common.h1_20001005_tag_extensions
        postprocess_functions = None
        is_prerelease = True
    elif game_version == 20001116:
        game_defs = h1
        engine_tag = tag_common.EngineTag.H1Latest.value
        tag_defs = tag_common.h1_20001116_defs_directory
        tag_groups = tag_common.h1_20001116_tag_groups
        tag_extensions = tag_common.h1_20001116_tag_extensions
        postprocess_functions = None
        is_prerelease = True
    elif game_version == 20011115:
        game_defs = h1
        engine_tag = tag_common.EngineTag.H1Latest.value
        tag_defs = tag_common.h1_defs_directory
        tag_groups = tag_common.h1_tag_groups
        tag_extensions = tag_common.h1_tag_extensions
        postprocess_functions = h1_postprocess_functions
        is_prerelease = False
    elif game_version == 20041109:
        game_defs = h2
        engine_tag = tag_common.EngineTag.H2Latest.value
        tag_defs = tag_common.h2_defs_directory
        tag_groups = tag_common.h2_tag_groups
        tag_extensions = tag_common.h2_tag_extensions
        postprocess_functions = h2_postprocess_functions
        is_prerelease = False

    return game_defs, engine_tag, tag_defs, tag_groups, tag_extensions, postprocess_functions, is_prerelease

def import_tag(file_path, game_version=20011115):
    game_defs, engine_tag, tag_defs, tag_groups, tag_extensions, postprocess_functions, is_prerelease = get_version_args(game_version)
    output_dir = os.path.join(os.path.dirname(tag_defs), "%s_merged_output" % os.path.basename(tag_defs))
    merged_defs = game_defs.generate_defs(tag_defs, output_dir, tag_groups, tag_extensions)
    tag_dict = read_file(merged_defs, "", file_path, engine_tag=engine_tag, tag_groups=tag_groups, tag_extensions=tag_extensions, postprocess_functions=postprocess_functions, 
                         is_prerelease=is_prerelease)
    with open(os.path.join(os.path.dirname(file_path), "%s.json" % os.path.basename(file_path).rsplit(".", 1)[0]), 'w', encoding ='utf8') as json_file:
        json.dump(tag_dict, json_file, ensure_ascii = True, indent=4)

def export_tag(file_path, game_version=20011115):
    game_defs, engine_tag, tag_defs, tag_groups, tag_extensions, postprocess_functions, is_prerelease = get_version_args(game_version)

    output_dir = os.path.join(os.path.dirname(tag_defs), "%s_merged_output" % os.path.basename(tag_defs))
    merged_defs = game_defs.generate_defs(tag_defs, output_dir, tag_groups, tag_extensions)

    output_path = file_path.rsplit(".", 1)[0]
    with open(file_path, "r", encoding="utf8") as json_file:
        tag_dict = json.load(json_file)

        write_file(merged_defs, tag_dict, obfuscation_buffer_prepare(), output_path, engine_tag=engine_tag, tag_groups=tag_groups, tag_extensions=tag_extensions, 
                   postprocess_functions=postprocess_functions, is_prerelease=is_prerelease)

def dump_sound1(tag_dict, file_path, output_directory):
    tag_data = tag_dict["Data"]
    sound_folder_path = os.path.join(output_directory, os.path.basename(file_path))
    for permutation_element in tag_data["permutations"]:
        filename_raw = "%s.raw" % permutation_element["permutation name"]
        file_output = os.path.join(sound_folder_path, filename_raw)

        with open(file_output, "wb") as output_stream:
            output_stream.write(base64.b64decode(permutation_element["sound samples"]["encoded"]))

        if permutation_element["sample rate"] == 0:
            rate = "11025"

        elif permutation_element["sample rate"] == 1:
            rate = "22050"

        elif permutation_element["sample rate"] == 2:
            rate = "44100"

        channel_count = str(permutation_element["channel count"])
        filename_wav = "%s.wav" % permutation_element["permutation name"]
        wav_output = os.path.join(sound_folder_path, filename_wav)

        args = [SOX_TOOL, "-t", "raw", "-r", rate, "-b", "16", "-c", channel_count, "-L", "-e", "signed-integer", file_output, wav_output]

        subprocess.check_call(args)

        os.remove(file_output)

def dump_sound2(tag_dict, file_path, output_directory):
        tag_data = tag_dict["Data"]

        filename = "%s.raw" % os.path.basename(file_path)
        file_output = os.path.join(output_directory, filename)

        with open(file_output, "wb") as output_stream:
            output_stream.write(base64.b64decode(tag_data["sound samples"]["encoded"]))

        if tag_data["sample rate"] == 0:
            rate = "11025"

        elif tag_data["sample rate"] == 1:
            rate = "22050"

        elif tag_data["sample rate"] == 2:
            rate = "44100"

        if tag_data["sound encoding"] == 0:
            channel_count = "1"

        elif tag_data["sound encoding"] == 1:
            channel_count = "2"

        filename_wav = "%s.wav" % os.path.basename(file_path)
        wav_output = os.path.join(output_directory, filename_wav)

        if tag_data["compression type"] == 0:
            args = [SOX_TOOL, "-t", "raw", "-r", rate, "-b", "16", "-c", channel_count, "-L", "-e", "signed-integer", file_output, wav_output]

        elif tag_data["compression type"] == 1:
            args = [SOX_TOOL, "-t", "ima", "-r", rate, "-c", channel_count, "-e", "ima-adpcm", file_output, "-b", "16", "-e", "signed-integer", wav_output]

        subprocess.check_call(args)

        os.remove(file_output)

def dump_sound3(tag_dict, file_path, output_directory):
    tag_data = tag_dict["Data"]

    sound_folder_path = os.path.join(output_directory, os.path.basename(file_path))

    if tag_data["encoding"]["value"] == 0:
        channel_count = "1"

    elif tag_data["encoding"]["value"] == 1:
        channel_count = "2"

    for pitch_range_element in tag_data["pitch ranges"]:
        pitch_range_folder_path = os.path.join(sound_folder_path, pitch_range_element["name"])
        if not os.path.exists(pitch_range_folder_path):
            os.makedirs(pitch_range_folder_path)

        for permutation_element in pitch_range_element["permutations"]:
            filename = "%s.raw" % permutation_element["name"]
            filename_wav = "%s.wav" % permutation_element["name"]
            file_output = os.path.join(pitch_range_folder_path, filename)

            with open(file_output, "wb") as output_stream:
                output_stream.write(base64.b64decode(permutation_element["samples"]["encoded"]))
            wav_output = os.path.join(pitch_range_folder_path, filename_wav)

            if permutation_element["compression"]["value"] == 0:
                args = [SOX_TOOL, "-t", "raw", "-r", "22050", "-b", "16", "-c", channel_count, "-L", "-e", "signed-integer", file_output, wav_output]

            elif permutation_element["compression"]["value"] == 1:
                args = [SOX_TOOL, "-t", "ima", "-r", "22050", "-c", channel_count, "-e", "ima-adpcm", file_output, "-b", "16", "-e", "signed-integer", wav_output]

            subprocess.check_call(args)

            os.remove(file_output)

def dump_sound_data(file_path, output_directory, game_version):
    game_defs, engine_tag, tag_defs, tag_groups, tag_extensions, postprocess_functions, is_prerelease = get_version_args(game_version)
    output_dir = os.path.join(os.path.dirname(tag_defs), "%s_merged_output" % os.path.basename(tag_defs))
    merged_defs = game_defs.generate_defs(tag_defs, output_dir, tag_groups, tag_extensions)

    tag_dict = read_file(merged_defs, "", file_path, engine_tag=engine_tag, tag_groups=tag_groups, tag_extensions=tag_extensions, postprocess_functions=postprocess_functions, is_prerelease=is_prerelease)
    if game_version == 19990225:
        # snd!/sounds
        dump_sound1(tag_dict, file_path, output_directory)
    elif game_version == 19990302:
        # snd!/sounds
        dump_sound1(tag_dict, file_path, output_directory)
    elif game_version == 19990426:
        # snd!/sounds
        dump_sound1(tag_dict, file_path, output_directory)
    elif game_version == 19990608:
        #snpm/sounds.samples
        dump_sound2(tag_dict, file_path, output_directory)
    elif game_version == 19990623:
        #snpm/sounds.samples
        dump_sound2(tag_dict, file_path, output_directory)
    elif game_version == 19990730:
        #snpm/sounds.samples
        dump_sound2(tag_dict, file_path, output_directory)
    elif game_version == 19990924:
        #snpm/sounds.samples
        dump_sound2(tag_dict, file_path, output_directory)
    elif game_version == 19990930:
        #snpm/sounds.samples
        dump_sound2(tag_dict, file_path, output_directory)
    elif game_version == 19991021:
        #snpm/sounds.samples
        dump_sound2(tag_dict, file_path, output_directory)
    elif game_version == 20000525:
        # snd!/sounds
        dump_sound3(tag_dict, file_path, output_directory)
    elif game_version == 20001005:
        #snpm/sounds.samples
        dump_sound2(tag_dict, file_path, output_directory)
    elif game_version == 20001116:
        # snd!/sounds
        dump_sound3(tag_dict, file_path, output_directory)

def DecodeBitmap565(WIDTH, HEIGHT, pixels_offset, pixel_data, big_endian=True):
    for height_idx in range(HEIGHT):
        for width_idx in range(WIDTH):
            a = pixel_data[pixels_offset + (2 * (width_idx + WIDTH * height_idx))]
            b = pixel_data[pixels_offset + (2 * (width_idx + WIDTH * height_idx) + 1)]
            if big_endian:
                value = ((a << 8) | b)
            else:
                value = (a | (b << 8))

            red = (((value & 63488) >> 11) << 3)
            green = (((value & 2016) >> 5) << 2)
            blue = ((value & 31) << 3)

            yield (red, green, blue)

def DecodeBitmap8BitIntensity(WIDTH, HEIGHT, pixels_offset, pixel_data, big_endian=True):
    for width_idx in range(WIDTH):
        for height_idx in range(HEIGHT):
            value = pixel_data[pixels_offset + (height_idx + HEIGHT * width_idx)]
            yield (value, value, value)

def DecodeBitmap888(WIDTH, HEIGHT, pixels_offset, pixel_data, big_endian=True):
    for height_idx in range(HEIGHT):
        for width_idx in range(WIDTH):
            a = pixel_data[pixels_offset + (4 * (width_idx + WIDTH * height_idx) + 0)]
            b = pixel_data[pixels_offset + (4 * (width_idx + WIDTH * height_idx) + 1)]
            c = pixel_data[pixels_offset + (4 * (width_idx + WIDTH * height_idx) + 2)]
            d = pixel_data[pixels_offset + (4 * (width_idx + WIDTH * height_idx) + 3)]

            if big_endian:
                color_tuple = (b, c, d)
            else:
                color_tuple = (d, c, b)

            yield color_tuple

def DecodeBitmap8888(WIDTH, HEIGHT, pixels_offset, pixel_data, big_endian=True):
    for height_idx in range(HEIGHT):
        for width_idx in range(WIDTH):
            a = pixel_data[pixels_offset + (4 * (width_idx + WIDTH * height_idx) + 0)]
            b = pixel_data[pixels_offset + (4 * (width_idx + WIDTH * height_idx) + 1)]
            c = pixel_data[pixels_offset + (4 * (width_idx + WIDTH * height_idx) + 2)]
            d = pixel_data[pixels_offset + (4 * (width_idx + WIDTH * height_idx) + 3)]

            if big_endian:
                color_tuple = (b, c, d, a)
            else:
                color_tuple = (a, d, c, b)

            yield color_tuple

def DecodeBitmap4444(WIDTH, HEIGHT, pixels_offset, pixel_data, big_endian=True):
    for height_idx in range(HEIGHT):
        for width_idx in range(WIDTH):
            a = (pixel_data[pixels_offset + (2 * (width_idx + WIDTH * height_idx) + 0)] & 240)
            b = ((pixel_data[pixels_offset + (2 * (width_idx + WIDTH * height_idx) + 0)] & 15) << 4)
            c = (pixel_data[pixels_offset + (2 * (width_idx + WIDTH * height_idx) + 1)] & 240)
            d = ((pixel_data[pixels_offset + (2 * (width_idx + WIDTH * height_idx) + 1)] & 15) << 4)

            if big_endian:
                color_tuple = (b, c, d, a)
            else:
                color_tuple = (a, d, c, b)

            yield color_tuple

def dump_bitmap1(WIDTH, HEIGHT, pixels_offset, pixel_data, encoding):
    image = None
    if Image:
        if encoding == OldEncodingEnum._16bit_565:
            image = Image.new('RGB', (WIDTH, HEIGHT), color=0)
            pixels = list(DecodeBitmap565(WIDTH, HEIGHT, pixels_offset, pixel_data))
            image.putdata(pixels)
            image.putalpha(255)

        elif encoding == OldEncodingEnum._32bit:
            image = Image.new('RGBA', (WIDTH, HEIGHT), color=0)
            pixels = list(DecodeBitmap8888(WIDTH, HEIGHT, pixels_offset, pixel_data))
            image.putdata(pixels)

        elif encoding == OldEncodingEnum._16bit_4444:
            image = Image.new('RGBA', (WIDTH, HEIGHT), color=0)
            pixels = list(DecodeBitmap4444(WIDTH, HEIGHT, pixels_offset, pixel_data))
            image.putdata(pixels)

        elif encoding == OldEncodingEnum._8bit_intensity:
            image = Image.new('RGB', (WIDTH, HEIGHT), color=0)
            pixels = list(DecodeBitmap8BitIntensity(WIDTH, HEIGHT, pixels_offset, pixel_data))
            image.putdata(pixels)
            image.putalpha(255)

        else:
            print("Unsupported format %s" % encoding)

    return image

def dump_bitmap2(WIDTH, HEIGHT, pixels_offset, pixel_data, encoding):
    image = None
    if Image:
        if encoding == EncodingEnum._16bit_565:
            image = Image.new('RGB', (WIDTH, HEIGHT), color=0)
            pixels = list(DecodeBitmap565(WIDTH, HEIGHT, pixels_offset, pixel_data))
            image.putdata(pixels)
            image.putalpha(255)

        elif encoding == EncodingEnum._32bit_888:
            image = Image.new('RGB', (WIDTH, HEIGHT), color=0)
            pixels = list(DecodeBitmap888(WIDTH, HEIGHT, pixels_offset, pixel_data))
            image.putdata(pixels)
            image.putalpha(255)

        elif encoding == EncodingEnum._32bit_8888:
            image = Image.new('RGBA', (WIDTH, HEIGHT), color=0)
            pixels = list(DecodeBitmap8888(WIDTH, HEIGHT, pixels_offset, pixel_data))
            image.putdata(pixels)

        elif encoding == EncodingEnum._16bit_4444:
            image = Image.new('RGBA', (WIDTH, HEIGHT), color=0)
            pixels = list(DecodeBitmap4444(WIDTH, HEIGHT, pixels_offset, pixel_data))
            image.putdata(pixels)

        elif encoding == EncodingEnum._8bit_intensity:
            image = Image.new('RGB', (WIDTH, HEIGHT), color=0)
            pixels = list(DecodeBitmap8BitIntensity(WIDTH, HEIGHT, pixels_offset, pixel_data))
            image.putdata(pixels)
            image.putalpha(255)

        else:
            print("Unsupported format %s" % encoding)

    return image

def dump_bitmap_data(file_path, output_directory, game_version):
    game_defs, engine_tag, tag_defs, tag_groups, tag_extensions, postprocess_functions, is_prerelease = get_version_args(game_version)
    output_dir = os.path.join(os.path.dirname(tag_defs), "%s_merged_output" % os.path.basename(tag_defs))
    merged_defs = game_defs.generate_defs(tag_defs, output_dir, tag_groups, tag_extensions)
    
    tag_dict = read_file(merged_defs, "", file_path, engine_tag=engine_tag, tag_groups=tag_groups, tag_extensions=tag_extensions, postprocess_functions=postprocess_functions, is_prerelease=is_prerelease)
    if game_version == 19980319:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                texture_image.save(new_path, "TIFF", compression='raw')
    if game_version == 19980403:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                texture_image.save(new_path, "TIFF", compression='raw')
    if game_version == 19980512:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                texture_image.save(new_path, "TIFF", compression='raw')
    if game_version == 19980514:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                texture_image.save(new_path, "TIFF", compression='raw')
    if game_version == 19980624:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                texture_image.save(new_path, "TIFF", compression='raw')
    if game_version == 19980708:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                texture_image.save(new_path, "TIFF", compression='raw')
    if game_version == 19981008:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                texture_image.save(new_path, "TIFF", compression='raw')
    if game_version == 19981022:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                texture_image.save(new_path, "TIFF", compression='raw')
    if game_version == 19990225:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19990302:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19990426:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19990608:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19990623:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19990730:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19990924:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19990930:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19991021:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 20000525:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 20001005:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    texture_image.save(new_path, "TIFF", compression='raw')

def DecodeIsland565(WIDTH, HEIGHT, pixels_offset, pixel_data, big_endian=True):
    for width_idx in range(WIDTH):
        for height_idx in range(HEIGHT):
            a = pixel_data[pixels_offset + (2 * (width_idx + WIDTH * height_idx))]
            b = pixel_data[pixels_offset + (2 * (width_idx + WIDTH * height_idx) + 1)]
            if big_endian:
                value = ((a << 8) | b)
            else:
                value = (a | (b << 8))

            red = (((value & 63488) >> 11) << 3)
            green = (((value & 2016) >> 5) << 2)
            blue = ((value & 31) << 3)

            yield (red, green, blue)

def decode_island(pixel_data):
    image = None
    if Image:
        image = Image.new('RGB', (64, 64), color=0)
        pixels = list(DecodeIsland565(64, 64, 0, pixel_data))
        image.putdata(pixels)
        image.putalpha(255)

    return image

def dump_island_texture_data(file_path, output_directory, game_version):
    game_defs, engine_tag, tag_defs, tag_groups, tag_extensions, postprocess_functions, is_prerelease = get_version_args(game_version)
    output_dir = os.path.join(os.path.dirname(tag_defs), "%s_merged_output" % os.path.basename(tag_defs))
    merged_defs = game_defs.generate_defs(tag_defs, output_dir, tag_groups, tag_extensions)
    
    tag_dict = read_file(merged_defs, "", file_path, engine_tag=engine_tag, tag_groups=tag_groups, tag_extensions=tag_extensions, postprocess_functions=postprocess_functions, is_prerelease=is_prerelease)
    if game_version == 19981008:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                texture_image.save(new_path, "TIFF", compression='raw')
    if game_version == 19981022:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                texture_image.save(new_path, "TIFF", compression='raw')
    if game_version == 19990225:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19990302:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19990426:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19990608:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19990623:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19990730:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19990924:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19990930:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19991021:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 20000525:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 20001005:

        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        pixel_data = io.BytesIO(base64.b64decode(tag_data["pixels"]["encoded"]))
        submesh_count = int(tag_data["pixels"]["length"] / 131072)
        island_image = Image.new('RGB', (2048, 2048), color=0)
        x_index = 0
        y_index = 0
        for submesh_idx in range(16):
            for column_idx in range(4):
                for row_idx in range(4):
                    cell_image = decode_island(pixel_data.read(8192))
                    island_image.paste(cell_image, ((x_index * 256) + (column_idx * 64), (y_index * 256) + (row_idx * 64)))

            y_index += 1
            if y_index >= 4:
                y_index = 0
                x_index += 1

        new_path = os.path.join(output_directory, "%s.tiff" % "island_texture")
        island_image.save(new_path, "TIFF", compression='raw')

def main():
    if len(sys.argv) < 2:
        print("Drag a file onto this script.")
        return

    file_path = sys.argv[1]
    game_version = 20011115
    if len(sys.argv) >= 3:
        game_version = int(sys.argv[2])

    if not os.path.isfile(file_path):
        return print("Not a valid file path. Check that the file exists on your system.")
    if file_path.lower().endswith(".json"):
        export_tag(file_path, game_version)
    else:
        import_tag(file_path, game_version)

if __name__ == "__main__":
        main()
        input("\nPress Enter to close...")