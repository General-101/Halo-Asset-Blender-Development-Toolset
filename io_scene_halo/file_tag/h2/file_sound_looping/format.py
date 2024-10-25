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

class SoundLoopingAsset():
    def __init__(self, header=None, body_header=None, tracks_header=None, tracks=None, detail_sounds_header=None, detail_sounds=None, remastered_looping_sound=None, flags=0, 
                 martys_music_time=0.0, unk_0=0.0, unk_1=None, tracks_tag_block=None, detail_sounds_tag_block=None):
        self.header = header
        self.body_header = body_header
        self.tracks_header = tracks_header
        self.tracks = tracks
        self.detail_sounds_header = detail_sounds_header
        self.detail_sounds = detail_sounds
        self.remastered_looping_sound = remastered_looping_sound
        self.flags = flags
        self.martys_music_time = martys_music_time
        self.unk_0 = unk_0
        self.unk_1 = unk_1
        self.tracks_tag_block = tracks_tag_block
        self.detail_sounds_tag_block = detail_sounds_tag_block

    class Track:
        def __init__(self, name="", name_length=0, flags=0, gain=0.0, fade_in_duration=0.0, fade_out_duration=0.0, in_sound=None, loop_sound=None, out_sound=None, alt_loop=None,
                     alt_out=None, output_effect=0, alt_trans_in=None, alt_trans_out=None, alt_crossfade_duration=0.0, alt_fade_out_duration=0.0):
            self.name = name
            self.name_length = name_length
            self.flags = flags
            self.gain = gain
            self.fade_in_duration = fade_in_duration
            self.fade_out_duration = fade_out_duration
            self.in_sound = in_sound
            self.loop_sound = loop_sound
            self.out_sound = out_sound
            self.alt_loop = alt_loop
            self.alt_out = alt_out
            self.output_effect = output_effect
            self.alt_trans_in = alt_trans_in
            self.alt_trans_out = alt_trans_out
            self.alt_crossfade_duration = alt_crossfade_duration
            self.alt_fade_out_duration = alt_fade_out_duration

    class DetailSound:
        def __init__(self, name="", name_length=0, sound=None, random_period_bounds=(0.0, 0.0), unk_0=0.0, flags=0, yaw_bounds=(0.0, 0.0), pitch_bounds=(0.0, 0.0),
                     distance_bounds=(0.0, 0.0)):
            self.name = name
            self.name_length = name_length
            self.sound = sound
            self.random_period_bounds = random_period_bounds
            self.unk_0 = unk_0
            self.flags = flags
            self.yaw_bounds = yaw_bounds
            self.pitch_bounds = pitch_bounds
            self.distance_bounds = distance_bounds
