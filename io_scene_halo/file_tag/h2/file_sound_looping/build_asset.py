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
from ....file_tag.h2.file_shader.format import FunctionTypeEnum

def write_body(output_stream, TAG, SOUNDLOOP):
    SOUNDLOOP.sound_looping_body_header.write(output_stream, TAG, True)
    SOUNDLOOP.sound_looping_body.remastered_looping_sound.write(output_stream, False, True)
    output_stream.write(struct.pack('<I', SOUNDLOOP.sound_looping_body.flags))
    output_stream.write(struct.pack('<f', SOUNDLOOP.sound_looping_body.martys_music_time))
    output_stream.write(struct.pack('<f', SOUNDLOOP.sound_looping_body.unk_0))
    output_stream.write(struct.pack('<8x'))
    SOUNDLOOP.sound_looping_body.unk_1.write(output_stream, False, True)
    SOUNDLOOP.sound_looping_body.tracks_tag_block.write(output_stream, False)
    SOUNDLOOP.sound_looping_body.detail_sounds_tag_block.write(output_stream, False)

def write_tracks(output_stream, TAG, tracks, tracks_header):
    if len(tracks) > 0:
        tracks_header.write(output_stream, TAG, True)
        for track_element in tracks:
            output_stream.write(struct.pack('>I', len(track_element.name)))
            output_stream.write(struct.pack('<I', track_element.flags))
            output_stream.write(struct.pack('<f', track_element.gain))
            output_stream.write(struct.pack('<f', track_element.fade_in_duration))
            output_stream.write(struct.pack('<f', track_element.fade_out_duration))
            track_element.in_sound.write(output_stream, False, True)
            track_element.loop_sound.write(output_stream, False, True)
            track_element.out_sound.write(output_stream, False, True)
            track_element.alt_loop.write(output_stream, False, True)
            track_element.alt_out.write(output_stream, False, True)
            output_stream.write(struct.pack('<h', track_element.output_effect))
            output_stream.write(struct.pack('<2x'))
            track_element.alt_trans_in.write(output_stream, False, True)
            track_element.alt_trans_out.write(output_stream, False, True)
            output_stream.write(struct.pack('<f', track_element.alt_crossfade_duration))
            output_stream.write(struct.pack('<f', track_element.alt_fade_out_duration))

        for track_element in tracks:
            name_length = len(track_element.name)
            if name_length > 0:
                output_stream.write(struct.pack('<%ss' % name_length, TAG.string_to_bytes(track_element.name, False)))

            in_sound_length = len(track_element.in_sound.name)
            if in_sound_length > 0:
                output_stream.write(struct.pack('<%ssx' % in_sound_length, TAG.string_to_bytes(track_element.in_sound.name, False)))

            loop_sound_length = len(track_element.loop_sound.name)
            if loop_sound_length > 0:
                output_stream.write(struct.pack('<%ssx' % loop_sound_length, TAG.string_to_bytes(track_element.loop_sound.name, False)))

            out_sound_length = len(track_element.out_sound.name)
            if out_sound_length > 0:
                output_stream.write(struct.pack('<%ssx' % out_sound_length, TAG.string_to_bytes(track_element.out_sound.name, False)))

            alt_loop_length = len(track_element.alt_loop.name)
            if alt_loop_length > 0:
                output_stream.write(struct.pack('<%ssx' % alt_loop_length, TAG.string_to_bytes(track_element.alt_loop.name, False)))

            alt_out_length = len(track_element.alt_out.name)
            if alt_out_length > 0:
                output_stream.write(struct.pack('<%ssx' % alt_out_length, TAG.string_to_bytes(track_element.alt_out.name, False)))

            alt_trans_in_length = len(track_element.alt_trans_in.name)
            if alt_trans_in_length > 0:
                output_stream.write(struct.pack('<%ssx' % alt_trans_in_length, TAG.string_to_bytes(track_element.alt_trans_in.name, False)))

            alt_trans_out_length = len(track_element.alt_trans_out.name)
            if alt_trans_out_length > 0:
                output_stream.write(struct.pack('<%ssx' % alt_trans_out_length, TAG.string_to_bytes(track_element.alt_trans_out.name, False)))

def write_detail_sounds(output_stream, TAG, detail_sounds, detail_sounds_header):
    if len(detail_sounds) > 0:
        detail_sounds_header.write(output_stream, TAG, True)
        for detail_sound_element in detail_sounds:
            output_stream.write(struct.pack('>I', len(detail_sound_element.name)))
            detail_sound_element.sound.write(output_stream, False, True)
            output_stream.write(struct.pack('<ff', *detail_sound_element.random_period_bounds))
            output_stream.write(struct.pack('<f', detail_sound_element.unk_0))
            output_stream.write(struct.pack('<I', detail_sound_element.flags))
            output_stream.write(struct.pack('<ff', radians(detail_sound_element.yaw_bounds[0]), radians(detail_sound_element.yaw_bounds[1])))
            output_stream.write(struct.pack('<ff', radians(detail_sound_element.pitch_bounds[0]), radians(detail_sound_element.pitch_bounds[1])))
            output_stream.write(struct.pack('<ff', *detail_sound_element.distance_bounds))

        for detail_sound_element in detail_sounds:
            name_length = len(detail_sound_element.name)
            if name_length > 0:
                output_stream.write(struct.pack('<%ss' % name_length, TAG.string_to_bytes(detail_sound_element.name, False)))

            sound_length = len(detail_sound_element.sound.name)
            if sound_length > 0:
                output_stream.write(struct.pack('<%ssx' % sound_length, TAG.string_to_bytes(detail_sound_element.sound.name, False)))

def build_asset(output_stream, SOUNDLOOP, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    SOUNDLOOP.header.write(output_stream, False, True)
    write_body(output_stream, TAG, SOUNDLOOP)

    remastered_looping_sound_length = len(SOUNDLOOP.sound_looping_body.remastered_looping_sound.name)
    if remastered_looping_sound_length > 0:
        output_stream.write(struct.pack('<%ssx' % remastered_looping_sound_length, TAG.string_to_bytes(SOUNDLOOP.sound_looping_body.remastered_looping_sound.name, False)))

    unk_1_length = len(SOUNDLOOP.sound_looping_body.unk_1.name)
    if unk_1_length > 0:
        output_stream.write(struct.pack('<%ssx' % unk_1_length, TAG.string_to_bytes(SOUNDLOOP.sound_looping_body.unk_1.name, False)))

    write_tracks(output_stream, TAG, SOUNDLOOP.tracks, SOUNDLOOP.tracks_header)
    write_detail_sounds(output_stream, TAG, SOUNDLOOP.detail_sounds, SOUNDLOOP.detail_sounds_header)

