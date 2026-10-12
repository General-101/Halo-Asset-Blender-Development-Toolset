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

from enum import Flag, Enum, auto

class H1SoundLoopingFlags(Flag):
    deafening_to_ais = auto()
    not_a_loop = auto()
    stops_music = auto()
    siege_of_madrigal = auto()

class H2SoundLoopingFlags(Flag):
    deafening_to_ais = auto()
    not_a_loop = auto()
    stops_music = auto()
    always_spatialize = auto()
    synchronize_playback = auto()
    synchronize_tracks = auto()
    fake_spatialization_with_distance = auto()
    combine_all_3d_playback = auto()
    legacy_only = auto()
    remastered_only = auto()

def convert_sound_looping_flags(object_flags):
    flags = 0
    active_h1_flags = H1SoundLoopingFlags(object_flags)
    if H1SoundLoopingFlags.deafening_to_ais in active_h1_flags:
        flags += H2SoundLoopingFlags.deafening_to_ais.value

    if H1SoundLoopingFlags.not_a_loop in active_h1_flags:
        flags += H2SoundLoopingFlags.not_a_loop.value

    if H1SoundLoopingFlags.stops_music in active_h1_flags:
        flags += H2SoundLoopingFlags.stops_music.value

    return flags


def generate_tracks(dump_dic):
    tracks_block = []
    for track_idx, track_element in enumerate(dump_dic["Data"]["tracks"]):
        track_dict = {
            "name": "track_%s" % track_idx,
            "flags": track_element["flags"],
            "gain": track_element["gain"],
            "fade in duration": track_element["fade in duration"],
            "fade out duration": track_element["fade out duration"],
            "in": track_element["start"],
            "loop": track_element["loop"],
            "out": track_element["end"],
            "alt loop": track_element["alternate loop"],
            "alt out": track_element["alternate end"],
            "output effect": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "alt trans in": {"group name": "snd!", "path": ""},
            "alt trans out": {"group name": "snd!", "path": ""},
            "alt crossfade duration": 0.0,
            "alt fade out duration": 0.0
        }

        tracks_block.append(track_dict)

    return tracks_block

def generate_detail_sounds(dump_dic):
    detail_sounds_block = []
    for detail_sound_idx, detail_sound_element in enumerate(dump_dic["Data"]["detail sounds"]):
        detail_sound_dict = {
            "name": "detail_sound_%s" % detail_sound_idx,
            "sound": detail_sound_element["sound"],
            "random period bounds": detail_sound_element["random period bounds"],
            "Real": detail_sound_element["gain"],
            "flags": detail_sound_element["flags"],
            "yaw bounds": detail_sound_element["yaw bounds"],
            "pitch bounds": detail_sound_element["pitch bounds"],
            "distance bounds": detail_sound_element["distance bounds"],
        }

        detail_sounds_block.append(detail_sound_dict)

    return detail_sounds_block

def upgrade_sound_looping(h1_lsnd_asset, EngineTag):
    h1_lsnd_data = h1_lsnd_asset["Data"]

    h2_lsnd_asset = {
        "TagName": h1_lsnd_asset["TagName"],
        "Header": {
            "unk1": 0,
            "flags": 0,
            "tag type": 0,
            "name": "",
            "tag group": "lsnd",
            "checksum": 0,
            "data offset": 64,
            "data length": 0,
            "unk2": 0,
            "version": 3,
            "destination": 0,
            "plugin handle": -1,
            "engine tag": EngineTag.H2Latest.value
        },
        "Data": {
            "remastered looping sound": {"group name": "lsnd", "path": ""},
            "flags": convert_sound_looping_flags(h1_lsnd_data["flags"]),
            "marty's music time": 0.0,
            "Real": 0.0,
            "TagReference": {"group name": None, "path": ""},
            "tracks": generate_tracks(h1_lsnd_asset),
            "detail sounds": []
        }
    }

    return h2_lsnd_asset
