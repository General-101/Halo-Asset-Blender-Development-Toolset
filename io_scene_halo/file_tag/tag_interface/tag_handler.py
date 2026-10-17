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
import math
import base64
import subprocess
import tag_common

from enum import Flag, Enum, auto
from tag_definitions import h1, h2, common
from tag_upgrading.h1 import upgrade_functions as h1_upgrade_functions
from tag_upgrading.h2 import upgrade_functions as h2_upgrade_functions
from tag_interface import read_file, write_file, obfuscation_buffer_prepare, check_header
from tag_postprocessing.h1 import postprocess_functions as h1_postprocess_functions
from tag_postprocessing.h2 import postprocess_functions as h2_postprocess_functions, create_function
from tag_utilities.h1_prerelease.foundation_split import dump_foundation

# SET ME
SOX_TOOL = r"C:\Program Files (x86)\sox-14-4-2\sox.exe"

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

class OldBitmapFormatEnum(Enum):
    _16_bit = 0
    _32_bit = auto()
    compressed = auto()

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
        is_prerelease = False
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

def dump_sound1(tag_dict, file_path, output_directory, field_name="permutations"):
    tag_data = tag_dict["Data"]
    sound_folder_path = os.path.join(output_directory, os.path.basename(file_path))
    for permutation_element in tag_data[field_name]:
        filename_raw = "%s.raw" % permutation_element["permutation name"]
        file_output = os.path.join(sound_folder_path, filename_raw)

        if not os.path.exists(sound_folder_path):
            os.makedirs(sound_folder_path)

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

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

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
    print(file_path)
    with open(file_path, "rb") as input_stream:
        valid_header, tag_group, checksum, engine_tag = check_header(input_stream, tag_groups)

    if not valid_header:
        print("INVALID TAG HEADER")
        return

    tag_dict = read_file(merged_defs, "", file_path, engine_tag=engine_tag, tag_groups=tag_groups, tag_extensions=tag_extensions, postprocess_functions=postprocess_functions, is_prerelease=is_prerelease)
    if tag_dict is None:
        print("FAILED TO READ TAG")
        return
    
    if game_version == 19990225:
        # snd!/sounds
        dump_sound1(tag_dict, file_path, output_directory, "sound permutations")
    elif game_version == 19990302:
        # snd!/sounds
        dump_sound1(tag_dict, file_path, output_directory, "sound permutations")
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
    print(file_path)
    with open(file_path, "rb") as input_stream:
        valid_header, tag_group, checksum, engine_tag = check_header(input_stream, tag_groups)

    if not valid_header:
        return
    
    tag_dict = read_file(merged_defs, "", file_path, engine_tag=engine_tag, tag_groups=tag_groups, tag_extensions=tag_extensions, postprocess_functions=postprocess_functions, is_prerelease=is_prerelease)
    if tag_dict is None:
        return

    if game_version == 19980319:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)
                texture_image.save(new_path, "TIFF", compression='raw')
    if game_version == 19980403:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)
                texture_image.save(new_path, "TIFF", compression='raw')
    if game_version == 19980512:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)
                texture_image.save(new_path, "TIFF", compression='raw')
    if game_version == 19980514:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)
                texture_image.save(new_path, "TIFF", compression='raw')
    if game_version == 19980624:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)
                texture_image.save(new_path, "TIFF", compression='raw')
    if game_version == 19980708:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)
                texture_image.save(new_path, "TIFF", compression='raw')
    if game_version == 19981008:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)
                texture_image.save(new_path, "TIFF", compression='raw')
    if game_version == 19981022:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)
                texture_image.save(new_path, "TIFF", compression='raw')
    if game_version == 19990225:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)
                texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19990302:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for bitmap_idx, bitmap_element in enumerate(tag_data["bitmaps"]):
            new_path = os.path.join(output_directory, "%s_%s_%s.tiff" % (file_name, OldEncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
            texture_image = dump_bitmap1(bitmap_element["width"], bitmap_element["height"], 0, base64.b64decode(bitmap_element["pixels"]["encoded"]), OldEncodingEnum(bitmap_element["format"]["value"]))
            if not texture_image == None:
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)
                texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19990426:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    if not os.path.exists(output_directory):
                        os.makedirs(output_directory)
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19990608:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    if not os.path.exists(output_directory):
                        os.makedirs(output_directory)
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19990623:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    if not os.path.exists(output_directory):
                        os.makedirs(output_directory)
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19990730:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    if not os.path.exists(output_directory):
                        os.makedirs(output_directory)
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19990924:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    if not os.path.exists(output_directory):
                        os.makedirs(output_directory)
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19990930:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    if not os.path.exists(output_directory):
                        os.makedirs(output_directory)
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 19991021:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    if not os.path.exists(output_directory):
                        os.makedirs(output_directory)
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 20000525:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, OldBitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    if not os.path.exists(output_directory):
                        os.makedirs(output_directory)
                    texture_image.save(new_path, "TIFF", compression='raw')
    elif game_version == 20001005:
        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)
        for format_element in tag_data["formats"]:
            for bitmap_idx, bitmap_element in enumerate(format_element["bitmaps"]):
                new_path = os.path.join(output_directory, "%s_%s_%s_%s.tiff" % (file_name, BitmapFormatEnum(format_element["format"]["value"]).name, EncodingEnum(bitmap_element["format"]["value"]).name, bitmap_idx))
                texture_image = dump_bitmap2(bitmap_element["width"], bitmap_element["height"], bitmap_element["pixels offset"], base64.b64decode(format_element["pixels"]["encoded"]), EncodingEnum(bitmap_element["format"]["value"]))
                if not texture_image == None:
                    if not os.path.exists(output_directory):
                        os.makedirs(output_directory)
                    texture_image.save(new_path, "TIFF", compression='raw')

def decode_island(pixel_data, encoding=OldEncodingEnum._16bit_565, image_dimensions=(64, 64)):
    image = None
    if Image:
        x = image_dimensions[0]
        y = image_dimensions[1]
        image = Image.new('RGB', (x, y), color=0)
        if encoding == OldEncodingEnum._16bit_565:
            pixels = list(DecodeBitmap565(x, y, 0, pixel_data))
        elif encoding == OldEncodingEnum._32bit:
            pixels = list(DecodeBitmap8888(x, y, 0, pixel_data))
        elif encoding == OldEncodingEnum._16bit_4444:
            pixels = list(DecodeBitmap4444(x, y, 0, pixel_data))
        elif encoding == OldEncodingEnum._8bit_intensity:
            pixels = list(DecodeBitmap8BitIntensity(x, y, 0, pixel_data))
        
        image.putdata(pixels)
        image.putalpha(255)

    return image

def stitch_cells(cell_textures, file_name, output_directory, texture_type=None):
    image_count = len(cell_textures)
    if image_count > 0:
        columns = math.ceil(math.sqrt(image_count))
        rows = math.ceil(image_count / columns)

        missing_cells = (rows - (image_count % rows)) % rows

        width, height = cell_textures[0].size

        result_width = columns * width
        result_height = rows * height

        island_image = Image.new("RGBA",(result_width, result_height), color=(0, 0, 0, 0))

        for column_idx in range(columns):
            for row_idx in range(rows):
                cell_index = (column_idx * columns) + row_idx
                if cell_index >= image_count:
                    break

                cell_image = cell_textures[cell_index]
                x = height * column_idx
                if column_idx == columns - 1 and missing_cells > 0:
                    y = width * (row_idx + missing_cells)
                else:
                    y = width * row_idx

                island_image.paste(cell_image, (x, y))

        world_name = file_name.rsplit(" ", 1)[0]
        final_name = "overhead_map_%s.tiff" % world_name
        if texture_type is not None:
            final_name = "%s_%s.tiff" % (texture_type, world_name)

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        new_path = os.path.join(output_directory, final_name) 
        island_image.save(new_path, "TIFF", compression='raw')

def dump_texture_pages(file_path, output_directory, merged_defs, engine_tag, tag_groups, tag_extensions, postprocess_functions, is_prerelease):
    directory_path = os.path.dirname(file_path)
    submesh_textures = []
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if not os.path.isfile(file_path):
            continue

        with open(file_path, "rb") as input_stream:
            valid_header, tag_group, checksum, engine_tag = check_header(input_stream, tag_groups)

        if not valid_header:
            continue

        tag_dict = read_file(merged_defs, "", file_path, engine_tag=engine_tag, tag_groups=tag_groups, tag_extensions=tag_extensions, postprocess_functions=postprocess_functions, is_prerelease=is_prerelease)
        if tag_dict == None:
            continue

        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)

        pixel_bytes = base64.b64decode(tag_data["submesh textures"]["encoded"])
        pixel_data = io.BytesIO(pixel_bytes)

        bytes_per_cell = 8192
        cells_per_submesh = 16
        bytes_per_submesh = bytes_per_cell * cells_per_submesh

        submesh_count = len(pixel_bytes) // bytes_per_submesh
        submeshes_per_row = math.isqrt(submesh_count)
        submeshes_per_column = math.ceil(submesh_count / submeshes_per_row)

        cell_size = 64
        cells_per_side = 4
        submesh_size = cell_size * cells_per_side

        image_width = submeshes_per_row * submesh_size
        image_height = submeshes_per_column * submesh_size

        island_image = Image.new("RGB",(image_width, image_height), color=0)
        for submesh_idx in range(submesh_count):
            x_index = submesh_idx // submeshes_per_column
            y_index = submesh_idx % submeshes_per_column
            for column_idx in range(cells_per_side):
                for row_idx in range(cells_per_side):
                    cell_data = pixel_data.read(bytes_per_cell)
                    if len(cell_data) != bytes_per_cell:
                        raise ValueError("Unexpected end of pixel data")

                    cell_image = decode_island(cell_data)
                    x = y_index * submesh_size + row_idx * cell_size
                    y = x_index * submesh_size + column_idx * cell_size

                    island_image.paste(cell_image, (x, y))

        submesh_textures.append(island_image)

    stitch_cells(submesh_textures, file_name, output_directory)

def dump_texture_pages_data(file_path, output_directory, game_version):
    game_defs, engine_tag, tag_defs, tag_groups, tag_extensions, postprocess_functions, is_prerelease = get_version_args(game_version)
    output_dir = os.path.join(os.path.dirname(tag_defs), "%s_merged_output" % os.path.basename(tag_defs))
    merged_defs = game_defs.generate_defs(tag_defs, output_dir, tag_groups, tag_extensions)
    if game_version == 19981008:
        dump_texture_pages(file_path, output_directory, merged_defs, engine_tag, tag_groups, tag_extensions, postprocess_functions, is_prerelease)
    if game_version == 19981022:
        dump_texture_pages(file_path, output_directory, merged_defs, engine_tag, tag_groups, tag_extensions, postprocess_functions, is_prerelease)
    if game_version == 19990225:
        dump_texture_pages(file_path, output_directory, merged_defs, engine_tag, tag_groups, tag_extensions, postprocess_functions, is_prerelease)
    elif game_version == 19990302:
        dump_texture_pages(file_path, output_directory, merged_defs, engine_tag, tag_groups, tag_extensions, postprocess_functions, is_prerelease)

def dump_static_pages(file_path, output_directory, merged_defs, engine_tag, tag_groups, tag_extensions, postprocess_functions, is_prerelease):
    directory_path = os.path.dirname(file_path)
    low_detail_textures = []
    overhead_map_textures = []
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if not os.path.isfile(file_path):
            continue

        print(file_path)
        with open(file_path, "rb") as input_stream:
            valid_header, tag_group, checksum, engine_tag = check_header(input_stream, tag_groups)

        if not valid_header:
            continue

        tag_dict = read_file(merged_defs, "", file_path, engine_tag=engine_tag, tag_groups=tag_groups, tag_extensions=tag_extensions, postprocess_functions=postprocess_functions, is_prerelease=is_prerelease)
        if tag_dict == None:
            continue

        tag_data = tag_dict["Data"]
        file_name = os.path.basename(file_path)

        image_count = tag_data["low detail texture"]["length"] / 32768
        pixel_bytes = base64.b64decode(tag_data["low detail texture"]["encoded"])
        pixel_data = io.BytesIO(pixel_bytes)
        for row_idx in range(int(image_count)):
            cell_data = pixel_data.read(32768)
            cell_image = decode_island(cell_data, OldEncodingEnum._16bit_565, image_dimensions=(128, 128))

            low_detail_textures.append(cell_image)

        image_count = tag_data["overhead map texture"]["length"] / 8192
        pixel_bytes = base64.b64decode(tag_data["overhead map texture"]["encoded"])
        pixel_data = io.BytesIO(pixel_bytes)
        for row_idx in range(int(image_count)):
            cell_data = pixel_data.read(8192)
            cell_image = decode_island(cell_data, OldEncodingEnum._16bit_4444, image_dimensions=(64, 64))

            overhead_map_textures.append(cell_image)

    stitch_cells(low_detail_textures, file_name, output_directory, "low_detail")
    stitch_cells(overhead_map_textures, file_name, output_directory, "overhead_map")

def dump_static_pages_data(file_path, output_directory, game_version):
    game_defs, engine_tag, tag_defs, tag_groups, tag_extensions, postprocess_functions, is_prerelease = get_version_args(game_version)
    output_dir = os.path.join(os.path.dirname(tag_defs), "%s_merged_output" % os.path.basename(tag_defs))
    merged_defs = game_defs.generate_defs(tag_defs, output_dir, tag_groups, tag_extensions)
    if game_version == 19981008:
        dump_static_pages(file_path, output_directory, merged_defs, engine_tag, tag_groups, tag_extensions, postprocess_functions, is_prerelease)
    if game_version == 19981022:
        dump_static_pages(file_path, output_directory, merged_defs, engine_tag, tag_groups, tag_extensions, postprocess_functions, is_prerelease)
    if game_version == 19990225:
        dump_static_pages(file_path, output_directory, merged_defs, engine_tag, tag_groups, tag_extensions, postprocess_functions, is_prerelease)
    elif game_version == 19990302:
        dump_static_pages(file_path, output_directory, merged_defs, engine_tag, tag_groups, tag_extensions, postprocess_functions, is_prerelease)

def dump_island_texture(tag_dict, file_path, output_directory):
    tag_data = tag_dict["Data"]
    file_name = os.path.basename(file_path)

    pixel_bytes = base64.b64decode(tag_data["pixels"]["encoded"])
    pixel_data = io.BytesIO(pixel_bytes)

    bytes_per_cell = 8192
    cells_per_submesh = 16
    bytes_per_submesh = bytes_per_cell * cells_per_submesh

    submesh_count = len(pixel_bytes) // bytes_per_submesh
    submeshes_per_row = math.isqrt(submesh_count)
    submeshes_per_column = math.ceil(submesh_count / submeshes_per_row)

    cell_size = 64
    cells_per_side = 4
    submesh_size = cell_size * cells_per_side

    image_width = submeshes_per_row * submesh_size
    image_height = submeshes_per_column * submesh_size

    island_image = Image.new("RGB",(image_width, image_height), color=0)
    for submesh_idx in range(submesh_count):
        x_index = submesh_idx // submeshes_per_column
        y_index = submesh_idx % submeshes_per_column
        for column_idx in range(cells_per_side):
            for row_idx in range(cells_per_side):
                cell_data = pixel_data.read(bytes_per_cell)
                if len(cell_data) != bytes_per_cell:
                    raise ValueError("Unexpected end of pixel data")

                cell_image = decode_island(cell_data)
                x = y_index * submesh_size + row_idx * cell_size
                y = x_index * submesh_size + column_idx * cell_size

                island_image.paste(cell_image, (x, y))

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    new_path = os.path.join(output_directory, "%s.tiff" % file_name) 
    island_image.save(new_path, "TIFF", compression='raw')

def dump_island_texture_data(file_path, output_directory, game_version):
    game_defs, engine_tag, tag_defs, tag_groups, tag_extensions, postprocess_functions, is_prerelease = get_version_args(game_version)
    output_dir = os.path.join(os.path.dirname(tag_defs), "%s_merged_output" % os.path.basename(tag_defs))
    merged_defs = game_defs.generate_defs(tag_defs, output_dir, tag_groups, tag_extensions)

    print(file_path)
    with open(file_path, "rb") as input_stream:
        valid_header, tag_group, checksum, engine_tag = check_header(input_stream, tag_groups)

    if not valid_header:
        return
    
    tag_dict = read_file(merged_defs, "", file_path, engine_tag=engine_tag, tag_groups=tag_groups, tag_extensions=tag_extensions, postprocess_functions=postprocess_functions, is_prerelease=is_prerelease)
    if tag_dict is None:
        return

    if game_version == 19990426:
        dump_island_texture(tag_dict, file_path, output_directory)
    elif game_version == 19990608:
        dump_island_texture(tag_dict, file_path, output_directory)
    elif game_version == 19990623:
        dump_island_texture(tag_dict, file_path, output_directory)
    elif game_version == 19990730:
        dump_island_texture(tag_dict, file_path, output_directory)
    elif game_version == 19990924:
        dump_island_texture(tag_dict, file_path, output_directory)
    elif game_version == 19990930:
        dump_island_texture(tag_dict, file_path, output_directory)
    elif game_version == 19991021:
        dump_island_texture(tag_dict, file_path, output_directory)
    elif game_version == 20001005:
        dump_island_texture(tag_dict, file_path, output_directory)

def process_tag_directory(game_directory, game_version):
    output_path = os.path.join(game_directory, "output")
    local_path = os.path.join(game_directory, "local")
    foundation_path = os.path.join(game_directory, "foundation")
    tag_path = os.path.join(game_directory, "tags")
    large_install = os.path.join(tag_path, "large install")
    medium_install = os.path.join(tag_path, "medium install")
    small_install = os.path.join(tag_path, "small install")
    if os.path.isfile(large_install):
        dump_foundation(large_install, game_version, foundation_path)
    if os.path.isfile(medium_install):
        dump_foundation(medium_install, game_version, foundation_path)
    if os.path.isfile(small_install):
        dump_foundation(small_install, game_version, foundation_path)

    if not game_version == 20001116: 
        bitmaps_local_directory = os.path.join(local_path, "bitmaps")
        bitmaps_foundation_directory = os.path.join(foundation_path, "bitmaps")
        bitmaps_local_output = os.path.join(output_path, "local", "bitmaps")
        bitmaps_foundation_output = os.path.join(output_path, "foundation", "bitmaps")
        if os.path.isdir(bitmaps_local_directory):
            for file_name in os.listdir(bitmaps_local_directory):
                file_path = os.path.join(bitmaps_local_directory, file_name)
                if os.path.isfile(file_path):
                    dump_bitmap_data(file_path, bitmaps_local_output, game_version)

        if os.path.isdir(bitmaps_foundation_directory):
            issues = []
            for file_name in os.listdir(bitmaps_foundation_directory):
                file_path = os.path.join(bitmaps_foundation_directory, file_name)
                if os.path.isfile(file_path):
                    dump_bitmap_data(file_path, bitmaps_foundation_output, game_version)

    static_pages_local_directory = os.path.join(local_path, "worlds.static pages")
    static_pages_foundation_directory = os.path.join(foundation_path, "worlds.static pages")
    static_pages_local_output = os.path.join(output_path, "local", "worlds.static pages")
    static_pages_foundation_output = os.path.join(output_path, "foundation", "worlds.static pages")
    if os.path.isdir(static_pages_local_directory):
        for file_name in os.listdir(static_pages_local_directory):
            file_path = os.path.join(static_pages_local_directory, file_name)
            if os.path.isfile(file_path):
                dump_static_pages_data(file_path, static_pages_local_output, game_version)

    if os.path.isdir(static_pages_foundation_directory):
        for file_name in os.listdir(static_pages_foundation_directory):
            file_path = os.path.join(static_pages_foundation_directory, file_name)
            if os.path.isfile(file_path):
                dump_static_pages_data(file_path, static_pages_foundation_output, game_version)

    texture_pages_local_directory = os.path.join(local_path, "worlds.texture pages")
    texture_pages_foundation_directory = os.path.join(foundation_path, "worlds.texture pages")
    texture_pages_local_output = os.path.join(output_path, "local", "worlds.texture pages")
    texture_pages_foundation_output = os.path.join(output_path, "foundation", "worlds.texture pages")
    if os.path.isdir(texture_pages_local_directory):
        for file_name in os.listdir(texture_pages_local_directory):
            file_path = os.path.join(texture_pages_local_directory, file_name)
            if os.path.isfile(file_path):
                dump_texture_pages_data(file_path, texture_pages_local_output, game_version)

    if os.path.isdir(texture_pages_foundation_directory):
        for file_name in os.listdir(texture_pages_foundation_directory):
            file_path = os.path.join(texture_pages_foundation_directory, file_name)
            if os.path.isfile(file_path):
                dump_texture_pages_data(file_path, texture_pages_foundation_output, game_version)

    islands_textures_local_directory = os.path.join(local_path, "islands.textures")
    islands_textures_foundation_directory = os.path.join(foundation_path, "islands.textures")
    islands_textures_local_output = os.path.join(output_path, "local", "islands.textures")
    islands_textures_foundation_output = os.path.join(output_path, "foundation", "islands.textures")
    if os.path.isdir(islands_textures_local_directory):
        for file_name in os.listdir(islands_textures_local_directory):
            file_path = os.path.join(islands_textures_local_directory, file_name)
            if os.path.isfile(file_path):
                dump_island_texture_data(file_path, islands_textures_local_output, game_version)

    if os.path.isdir(islands_textures_foundation_directory):
        for file_name in os.listdir(islands_textures_foundation_directory):
            file_path = os.path.join(islands_textures_foundation_directory, file_name)
            if os.path.isfile(file_path):
                dump_island_texture_data(file_path, islands_textures_foundation_output, game_version)

    sound_set = (19990225, 19990302, 19990426, 20000525, 20001116)
    if game_version in sound_set: 
        sounds_local_directory = os.path.join(local_path, "sounds")
        sounds_foundation_directory = os.path.join(foundation_path, "sounds")
        sounds_local_output = os.path.join(output_path, "local", "sounds")
        sounds_foundation_output = os.path.join(output_path, "foundation", "sounds")
        if os.path.isdir(sounds_local_directory):
            for file_name in os.listdir(sounds_local_directory):
                file_path = os.path.join(sounds_local_directory, file_name)
                if os.path.isfile(file_path):
                    dump_sound_data(file_path, sounds_local_output, game_version)

        if os.path.isdir(sounds_foundation_directory):
            for file_name in os.listdir(sounds_foundation_directory):
                file_path = os.path.join(sounds_foundation_directory, file_name)
                if os.path.isfile(file_path):
                    dump_sound_data(file_path, sounds_foundation_output, game_version)
    else:
        sounds_samples_local_directory = os.path.join(local_path, "sounds.samples")
        sounds_samples_foundation_directory = os.path.join(foundation_path, "sounds.samples")
        sounds_samples_local_output = os.path.join(output_path, "local", "sounds.samples")
        sounds_samples_foundation_output = os.path.join(output_path, "foundation", "sounds.samples")
        if os.path.isdir(sounds_samples_local_directory):
            for file_name in os.listdir(sounds_samples_local_directory):
                file_path = os.path.join(sounds_samples_local_directory, file_name)
                if os.path.isfile(file_path):
                    dump_sound_data(file_path, sounds_samples_local_output, game_version)

        if os.path.isdir(sounds_samples_foundation_directory):
            for file_name in os.listdir(sounds_samples_foundation_directory):
                file_path = os.path.join(sounds_samples_foundation_directory, file_name)
                if os.path.isfile(file_path):
                    dump_sound_data(file_path, sounds_samples_foundation_output, game_version)

def main():
    if len(sys.argv) < 2:
        print("Drag a file onto this script.")
        return

    file_path = sys.argv[1]
    game_version = 20011115
    if len(sys.argv) >= 3:
        game_version = int(sys.argv[2])

    if file_path.lower().endswith(".json"):
        export_tag(file_path, game_version)
    else:
        import_tag(file_path, game_version)

if __name__ == "__main__":
        main()
        input("\nPress Enter to close...")