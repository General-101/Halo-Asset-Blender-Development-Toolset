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

from math import radians
from ....global_functions import tag_format, shader_processing

def write_body(output_stream, TAG, SOUND):
    SOUND.sound_body_header.write(output_stream, TAG, True)
    SOUND.sound_body.remastered_sound.write(output_stream, False, True)
    output_stream.write(struct.pack('<I', SOUND.sound_body.flags))
    output_stream.write(struct.pack('<B', SOUND.sound_body.class_type))
    output_stream.write(struct.pack('<B', SOUND.sound_body.sample_rate))
    output_stream.write(struct.pack('<B', SOUND.sound_body.output_effect))
    output_stream.write(struct.pack('<B', SOUND.sound_body.import_type))
    output_stream.write(struct.pack('<f', SOUND.sound_body.minimum_distance))
    output_stream.write(struct.pack('<f', SOUND.sound_body.maximum_distance))
    output_stream.write(struct.pack('<f', SOUND.sound_body.skip_fraction))
    output_stream.write(struct.pack('<f', SOUND.sound_body.maximum_bend_per_second))
    output_stream.write(struct.pack('<f', SOUND.sound_body.gain_base))
    output_stream.write(struct.pack('<f', SOUND.sound_body.gain_variance))
    output_stream.write(struct.pack('<hh', *SOUND.sound_body.random_pitch_bounds))
    output_stream.write(struct.pack('<f', radians(SOUND.sound_body.inner_cone_angle)))
    output_stream.write(struct.pack('<f', radians(SOUND.sound_body.outer_cone_angle)))
    output_stream.write(struct.pack('<f', SOUND.sound_body.outer_cone_gain))
    output_stream.write(struct.pack('<I', SOUND.sound_body.override_flags))
    output_stream.write(struct.pack('<f', radians(SOUND.sound_body.azimuth)))
    output_stream.write(struct.pack('<f', SOUND.sound_body.positional_gain))
    output_stream.write(struct.pack('<f', SOUND.sound_body.first_person_gain))
    output_stream.write(struct.pack('<ff', *SOUND.sound_body.gain_modifier))
    output_stream.write(struct.pack('<hh', *SOUND.sound_body.pitch_modifier))
    output_stream.write(struct.pack('<ff', *SOUND.sound_body.skip_fraction_modifier))
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<B', SOUND.sound_body.encoding))
    output_stream.write(struct.pack('<B', SOUND.sound_body.compression))
    SOUND.sound_body.promotion_rules_tag_block.write(output_stream, False)
    SOUND.sound_body.runtime_timers_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<i', SOUND.sound_body.runtime_active_promotion_index))
    output_stream.write(struct.pack('<i', SOUND.sound_body.runtime_last_promotion_time))
    output_stream.write(struct.pack('<i', SOUND.sound_body.runtime_suppression_timeout))
    output_stream.write(struct.pack('<4x'))
    output_stream.write(struct.pack('<f', SOUND.sound_body.inner_silence_distance))
    output_stream.write(struct.pack('<4x'))
    SOUND.sound_body.pitch_ranges_tag_block.write(output_stream, False)
    SOUND.sound_body.platform_parameters_tag_block.write(output_stream, False)
    SOUND.sound_body.extra_sound_info_tag_block.write(output_stream, False)
    SOUND.sound_body.reflections_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', SOUND.sound_body.low_pass_minimum_distance))
    output_stream.write(struct.pack('<f', SOUND.sound_body.low_pass_maximum_distance))
    for parameter in SOUND.sound_body.parameters:
        shader_processing.write_function_size(output_stream, parameter)

def write_pitch_ranges(output_stream, TAG, pitch_ranges, pitch_ranges_header):
    if len(pitch_ranges) > 0:
        pitch_ranges_header.write(output_stream, TAG, True)
        for pitch_range_element in pitch_ranges:
            output_stream.write(struct.pack('>I', len(pitch_range_element.name)))
            output_stream.write(struct.pack('<h', round(pitch_range_element.natural_pitch)))
            output_stream.write(struct.pack('<2x'))
            output_stream.write(struct.pack('<hh', *pitch_range_element.bend_bounds))
            output_stream.write(struct.pack('<hh', *pitch_range_element.unk_0))
            output_stream.write(struct.pack('<4x'))
            pitch_range_element.permutations_tag_block.write(output_stream, False)

        for pitch_range_element in pitch_ranges:
            name_length = len(pitch_range_element.name)
            if name_length > 0:
                output_stream.write(struct.pack('<%ss' % name_length, TAG.string_to_bytes(pitch_range_element.name, False)))

            if len(pitch_range_element.permutations) > 0:
                pitch_range_element.permutations_header.write(output_stream, TAG, True)
                for permutation_element in pitch_range_element.permutations:
                    output_stream.write(struct.pack('>I', len(permutation_element.name)))
                    output_stream.write(struct.pack('<f', permutation_element.skip_fraction))
                    output_stream.write(struct.pack('<f', permutation_element.gain))
                    output_stream.write(struct.pack('<I', permutation_element.sound_data))
                    output_stream.write(struct.pack('<h', permutation_element.sound_index))
                    output_stream.write(struct.pack('<h', permutation_element.lipsync_data))
                    permutation_element.sound_permutation_chunk_tag_block.write(output_stream, False)

                for permutation_element in pitch_range_element.permutations:
                    name_length = len(permutation_element.name)
                    if name_length > 0:
                        output_stream.write(struct.pack('<%ss' % name_length, TAG.string_to_bytes(permutation_element.name, False)))

def write_extra_sound_info(output_stream, TAG, extra_sound_info, extra_sound_info_header):
    if len(extra_sound_info) > 0:
        extra_sound_info_header.write(output_stream, TAG, True)
        for extra_sound_info_element in extra_sound_info:
            extra_sound_info_element.language_permutation_info_tag_block.write(output_stream, False)
            extra_sound_info_element.encoded_permutation_section_tag_block.write(output_stream, False)
            output_stream.write(struct.pack('<I', extra_sound_info_element.block_offset))
            output_stream.write(struct.pack('<I', extra_sound_info_element.block_size))
            output_stream.write(struct.pack('<I', extra_sound_info_element.section_data_size))
            output_stream.write(struct.pack('<I', extra_sound_info_element.resource_data_size))
            extra_sound_info_element.resources_tag_block.write(output_stream, False)
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('<h', extra_sound_info_element.owner_tag_section_offset))
            output_stream.write(struct.pack('<6x'))

        for extra_sound_info_element in extra_sound_info:
            if len(extra_sound_info_element.language_permutation_info) > 0:
                extra_sound_info_element.language_permutation_info_header.write(output_stream, TAG, True)
                for language_permutation_info_element in extra_sound_info_element.language_permutation_info:
                    language_permutation_info_element.raw_info_block_tag_block.write(output_stream, False)

                for language_permutation_info_element in extra_sound_info_element.language_permutation_info:
                    if len(language_permutation_info_element.raw_info_block) > 0:
                        language_permutation_info_element.raw_info_block_header.write(output_stream, TAG, True)
                        for raw_info_block_element in language_permutation_info_element.raw_info_block:
                            output_stream.write(struct.pack('>I', len(raw_info_block_element.skip_fraction_name)))
                            raw_info_block_element.samples_tag_data.write(output_stream, False)
                            raw_info_block_element.unk_1_tag_data.write(output_stream, False)
                            raw_info_block_element.unk_2_tag_data.write(output_stream, False)
                            raw_info_block_element.markers_tag_block.write(output_stream, False)
                            output_stream.write(struct.pack('<H', raw_info_block_element.compression))
                            output_stream.write(struct.pack('<H', raw_info_block_element.language))
                            raw_info_block_element.sound_permutation_chunk_tag_block.write(output_stream, False)
                            output_stream.write(struct.pack('<i', raw_info_block_element.remaining_data))

                        for raw_info_block_element in language_permutation_info_element.raw_info_block:
                            skip_fraction_name_length = len(raw_info_block_element.skip_fraction_name)
                            if skip_fraction_name_length > 0:
                                output_stream.write(struct.pack('<%ss' % skip_fraction_name_length, TAG.string_to_bytes(raw_info_block_element.skip_fraction_name, False)))

                            output_stream.write(raw_info_block_element.samples_tag_data.data)
                            output_stream.write(raw_info_block_element.unk_1_tag_data.data)
                            output_stream.write(raw_info_block_element.unk_2_tag_data.data)

        extra_sound_info[0].blok_header.write(output_stream, TAG, True)

def build_asset(output_stream, SOUND, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    SOUND.header.write(output_stream, False, True)
    write_body(output_stream, TAG, SOUND)

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("snpl", True), 0, 1, 56))
    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("snsc", True), 0, 1, 20))
    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("snpr", True), 1, 1, 36))

    write_pitch_ranges(output_stream, TAG, SOUND.pitch_ranges, SOUND.pitch_ranges_header)
    write_extra_sound_info(output_stream, TAG, SOUND.extra_sound_info, SOUND.extra_sound_info_header)

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("srpr", True), 0, 1, 12))
    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("slpp", True), 0, 1, 20))
    for parameter in SOUND.sound_body.parameters:
        shader_processing.write_function(output_stream, TAG, parameter)
