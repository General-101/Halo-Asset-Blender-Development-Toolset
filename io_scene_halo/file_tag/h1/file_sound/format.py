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

class SoundFlags(Flag):
    fit_to_adpcm_blocksize = auto()
    split_long_sound_into_permutations = auto()
    thirty_grunt = auto()

class ClassEnum(Enum):
    projectile_impact = 0
    projectile_detonation = auto()
    unk_2 = auto()
    unk_3 = auto()
    weapon_fire = auto()
    weapon_ready = auto()
    weapon_reload = auto()
    weapon_empty = auto()
    weapon_charge = auto()
    weapon_overheat = auto()
    weapon_idle = auto()
    unk_11 = auto()
    unk_12 = auto()
    object_impacts = auto()
    particle_impacts = auto()
    slow_particle_impacts = auto()
    unk_16 = auto()
    unk_17 = auto()
    unit_footsteps = auto()
    unit_dialog = auto()
    unk_20 = auto()
    unk_21 = auto()
    vehicle_collision = auto()
    vehicle_engine = auto()
    unk_24 = auto()
    unk_25 = auto()
    device_door = auto()
    device_force_field = auto()
    device_machinery = auto()
    device_nature = auto()
    device_computers = auto()
    unk_31 = auto()
    music = auto()
    ambient_nature = auto()
    ambient_machinery = auto()
    ambient_computers = auto()
    unk_36 = auto()
    unk_37 = auto()
    unk_38 = auto()
    first_person_damage = auto()
    unk_40 = auto()
    unk_41 = auto()
    unk_42 = auto()
    unk_43 = auto()
    scripted_dialog_player = auto()
    scripted_effect = auto()
    scripted_dialog_other = auto()
    scripted_dialog_force_unspatialized = auto()
    unk_48 = auto()
    unk_49 = auto()
    game_event = auto()

class SampleRateEnum(Enum):
    _22khz = 0
    _44khz = auto()

class EncodingEnum(Enum):
    mono = 0
    stereo = auto()

class CompressionEnum(Enum):
    none = 0
    xbox_adpcm = auto()
    ima_adpcm = auto()
    ogg = auto()

class SoundAsset():
    def __init__(self, header=None, pitch_ranges=None, flags=0, class_type=0, sample_rate=0, minimum_distance=0.0, maximum_distance=0.0, skip_fraction=0.0, 
                 random_pitch_bounds=(0.0, 0.0), inner_cone_angle=0.0, outer_cone_angle=0.0, outer_cone_gain=0.0, randomization_gain_modifier=0.0, 
                 maximum_bend_per_second=0.0, scale_zero_skip_fraction_modifier=0.0, scale_zero_gain_modifier=0.0, scale_zero_pitch_modifier=0.0, 
                 scale_one_skip_fraction_modifier=0.0, scale_one_gain_modifier=0.0, scale_one_pitch_modifier=0.0, encoding=0, compression=0, promotion_sound=None, 
                 promotion_count=0, pitch_ranges_tag_block=None):
        self.header = header
        self.pitch_ranges = pitch_ranges
        self.flags = flags
        self.class_type = class_type
        self.sample_rate = sample_rate
        self.minimum_distance = minimum_distance
        self.maximum_distance = maximum_distance
        self.skip_fraction = skip_fraction
        self.random_pitch_bounds = random_pitch_bounds
        self.inner_cone_angle = inner_cone_angle
        self.outer_cone_angle = outer_cone_angle
        self.outer_cone_gain = outer_cone_gain
        self.randomization_gain_modifier = randomization_gain_modifier
        self.maximum_bend_per_second = maximum_bend_per_second
        self.scale_zero_skip_fraction_modifier = scale_zero_skip_fraction_modifier
        self.scale_zero_gain_modifier = scale_zero_gain_modifier
        self.scale_zero_pitch_modifier = scale_zero_pitch_modifier
        self.scale_one_skip_fraction_modifier = scale_one_skip_fraction_modifier
        self.scale_one_gain_modifier = scale_one_gain_modifier
        self.scale_one_pitch_modifier = scale_one_pitch_modifier
        self.encoding = encoding
        self.compression = compression
        self.promotion_sound = promotion_sound
        self.promotion_count = promotion_count
        self.pitch_ranges_tag_block = pitch_ranges_tag_block

    class PitchRange:
        def __init__(self, name="", natural_pitch=0.0, bend_bounds=(0.0, 0.0), actual_permutation_count=0, permutations_tag_block=None, permutations=None):
            self.name = name
            self.natural_pitch = natural_pitch
            self.bend_bounds = bend_bounds
            self.actual_permutation_count = actual_permutation_count
            self.permutations_tag_block = permutations_tag_block
            self.permutations = permutations

    class Permutation:
        def __init__(self, name="", skip_fraction=0.0, gain=0.0, compression=0, next_permutation_index=0, samples=None, mouth_data=None, subtitle_data=None):
            self.name = name
            self.skip_fraction = skip_fraction
            self.gain = gain
            self.compression = compression
            self.next_permutation_index = next_permutation_index
            self.samples = samples
            self.mouth_data = mouth_data
            self.subtitle_data = subtitle_data
