# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Steven Garcia
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

import os
import json

from mathutils import Vector
from ....global_functions import tag_format, shader_processing, global_functions
from ....file_tag.h2.file_sound_looping.format import SoundLoopingAsset
from ....file_tag.h2.file_shader.format import FunctionTypeEnum, OutputTypeFlags

def generate_tracks(dump_dic, TAG, SOUNDLOOP):
    tracks_tag_block = dump_dic['Data']['Tracks']

    for track_element in tracks_tag_block:
        track = SOUNDLOOP.Track()
        track.name = track_element["Name"]
        track.name_length = len(track.name)
        track.flags = track_element["Flags"]
        track.gain = track_element["Gain"]
        track.fade_in_duration = track_element["Fade In Duration"]
        track.fade_out_duration = track_element["Fade Out Duration"]
        track.in_sound = TAG.TagRef().convert_from_json(track_element["Start"])
        track.loop_sound = TAG.TagRef().convert_from_json(track_element["Loop"])
        track.out_sound = TAG.TagRef().convert_from_json(track_element["End"])
        track.alt_loop = TAG.TagRef().convert_from_json(track_element["Alternate Loop"])
        track.alt_out = TAG.TagRef().convert_from_json(track_element["Alternate End"])
        track.output_effect = track_element["Output Effect"]["Value"]
        track.alt_trans_in = TAG.TagRef()
        track.alt_trans_out = TAG.TagRef()
        track.alt_crossfade_duration = 0.0
        track.alt_fade_out_duration = 0.0

        SOUNDLOOP.tracks.append(track)

    track_count = len(SOUNDLOOP.tracks)
    SOUNDLOOP.tracks_header = TAG.TagBlockHeader("tbfd", 1, track_count, 144)

    return TAG.TagBlock(track_count)

def generate_detail_sounds(dump_dic, TAG, SOUNDLOOP):
    detail_sounds_tag_block = dump_dic['Data']['Detail Sounds']

    for detail_sound_element in detail_sounds_tag_block:
        random_period_bounds = detail_sound_element['Random Period Bounds']
        yaw_bound = detail_sound_element['Yaw Bounds']
        pitch_bounds = detail_sound_element['Pitch Bounds']
        distance_bounds = detail_sound_element['Distance Bounds']

        detail_sound = SOUNDLOOP.DetailSound()
        detail_sound.name = detail_sound_element["Name"]
        detail_sound.name_length = len(detail_sound.name)
        detail_sound.sound = TAG.TagRef().convert_from_json(detail_sound_element["Sound"])
        detail_sound.random_period_bounds = (random_period_bounds["Min"], random_period_bounds["Max"])
        detail_sound.unk_0 = 0.0
        detail_sound.flags = detail_sound_element['Flags']
        detail_sound.yaw_bounds = (yaw_bound["Min"], yaw_bound["Max"])
        detail_sound.pitch_bounds = (pitch_bounds["Min"], pitch_bounds["Max"])
        detail_sound.distance_bounds = (distance_bounds["Min"], distance_bounds["Max"])

        SOUNDLOOP.detail_sounds.append(detail_sound)

    detail_sound_count = len(SOUNDLOOP.detail_sounds)
    SOUNDLOOP.detail_sounds_header = TAG.TagBlockHeader("tbfd", 1, detail_sound_count, 60)

    return TAG.TagBlock(detail_sound_count)

def upgrade_sound_looping(H2_ASSET, patch_txt_path, report, json_directory=None):
    dump_dic = json.load(H2_ASSET)

    TAG = tag_format.TagAsset()
    SOUNDLOOP = SoundLoopingAsset()
    TAG.upgrade_patches = tag_format.get_patch_set(patch_txt_path)

    SOUNDLOOP.header = TAG.Header()
    SOUNDLOOP.header.unk1 = 0
    SOUNDLOOP.header.flags = 0
    SOUNDLOOP.header.type = 0
    SOUNDLOOP.header.name = ""
    SOUNDLOOP.header.tag_group = "lsnd"
    SOUNDLOOP.header.checksum = 0
    SOUNDLOOP.header.data_offset = 64
    SOUNDLOOP.header.data_length = 0
    SOUNDLOOP.header.unk2 = 0
    SOUNDLOOP.header.version = 3
    SOUNDLOOP.header.destination = 0
    SOUNDLOOP.header.plugin_handle = -1
    SOUNDLOOP.header.engine_tag = "BLM!"

    SOUNDLOOP.tracks = []
    SOUNDLOOP.detail_sounds = []

    SOUNDLOOP.body_header = TAG.TagBlockHeader("tbfd", 3, 1, 76)
    SOUNDLOOP.remastered_looping_sound = TAG.TagRef()
    SOUNDLOOP.flags = dump_dic['Data']['Flags']
    SOUNDLOOP.martys_music_time = 0.0
    SOUNDLOOP.unk_0 = 0.0
    SOUNDLOOP.unk_1 = TAG.TagRef()
    SOUNDLOOP.tracks_tag_block = generate_tracks(dump_dic, TAG, SOUNDLOOP)
    SOUNDLOOP.detail_sounds_tag_block = generate_detail_sounds(dump_dic, TAG, SOUNDLOOP)

    return SOUNDLOOP
