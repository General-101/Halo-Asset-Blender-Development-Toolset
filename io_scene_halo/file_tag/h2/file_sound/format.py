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
    always_spatialize = auto()
    never_obstruct = auto()
    internal_dont_touch = auto()
    use_huge_sound_transmission = auto()
    link_count_to_owner_unit = auto()
    pitch_range_is_language = auto()
    dont_use_sound_class_speaker_flag = auto()
    dont_use_lipsync_data = auto()
    play_only_in_legacy_mode = auto()
    play_only_in_remastered_mode = auto()

class ClassEnum(Enum):
    projectile_impact = 0
    projectile_detonation = auto()
    projectile_flyby = auto()
    unk_3 = auto()
    weapon_fire = auto()
    weapon_ready = auto()
    weapon_reload = auto()
    weapon_empty = auto()
    weapon_charge = auto()
    weapon_overheat = auto()
    weapon_idle = auto()
    weapon_melee = auto()
    weapon_animation = auto()
    object_impacts = auto()
    particle_impacts = auto()
    unk_15 = auto()
    unk_16 = auto()
    unk_17 = auto()
    unit_footsteps = auto()
    unit_dialog = auto()
    unit_animation = auto()
    unk_21 = auto()
    vehicle_collision = auto()
    vehicle_engine = auto()
    vehicle_animation = auto()
    unk_25 = auto()
    device_door = auto()
    unk_27 = auto()
    device_machinery = auto()
    device_stationary = auto()
    unk_30 = auto()
    unk_31 = auto()
    music = auto()
    ambient_nature = auto()
    ambient_machinery = auto()
    unk_35 = auto()
    huge_ass = auto()
    object_looping = auto()
    cinematic_music = auto()
    unk_39 = auto()
    unk_40 = auto()
    unk_41 = auto()
    unk_42 = auto()
    unk_43 = auto()
    unk_44 = auto()
    cortana_mission = auto()
    cortana_cinematic = auto()
    mission_dialog = auto()
    cinematic_dialog = auto()
    scripted_cinematic_foley = auto()
    game_event = auto()
    ui = auto()
    test = auto()
    multilingual_test = auto()

class OutputEffectEnum(Enum):
    none = 0
    output_front_speakers = auto()
    output_rear_speakers = auto()
    output_center_speakers = auto()

class ImportTypeEnum(Enum):
    unknown = 0
    single_shot = auto()
    single_layer = auto()
    multi_layer = auto()

class EncodingEnum(Enum):
    mono = 0
    stereo = auto()
    codec = auto()
    quad = auto()

class CompressionEnum(Enum):
    none_big_endian = 0
    xbox_adpcm = auto()
    ima_adpcm = auto()
    none_little_endian = 0
    wma = 0
    opus = 0

class SoundAsset():
    def __init__(self, header=None, body_header=None, promotion_rules_header=None, promotion_rules=None, runtime_timers_header=None, runtime_timers=None, 
                 pitch_ranges_header=None, pitch_ranges=None, platform_parameters_header=None, platform_parameters=None, extra_sound_info_header=None, extra_sound_info=None, 
                 reflections_header=None, reflections=None, remastered_sound=None, flags=0, class_type=0, sample_rate=0, output_effect=0, import_type=0, 
                 minimum_distance=0.0, maximum_distance=0.0, skip_fraction=0.0, maximum_bend_per_second=0.0, gain_base=0.0, gain_variance=0.0, random_pitch_bounds=(0, 0), 
                 inner_cone_angle=0.0, outer_cone_angle=0.0, outer_cone_gain=0.0, override_flags=0, azimuth=0.0, positional_gain=0.0, first_person_gain=0.0, 
                 gain_modifier=(0.0, 0.0), pitch_modifier=(0, 0), skip_fraction_modifier=(0.0, 0.0), encoding=0, compression=0, promotion_rules_tag_block=None, 
                 runtime_timers_tag_block=None, runtime_active_promotion_index=0, runtime_last_promotion_time=0, runtime_suppression_timeout=0, inner_silence_distance=0.0, 
                 pitch_ranges_tag_block=None, platform_parameters_tag_block=None, extra_sound_info_tag_block=None, reflections_tag_block=None, low_pass_minimum_distance=0.0, 
                 low_pass_maximum_distance=1.0, parameters=None):
        self.header = header
        self.body_header = body_header
        self.promotion_rules_header = promotion_rules_header
        self.promotion_rules = promotion_rules
        self.runtime_timers_header = runtime_timers_header
        self.runtime_timers = runtime_timers
        self.pitch_ranges_header = pitch_ranges_header
        self.pitch_ranges = pitch_ranges
        self.platform_parameters_header = platform_parameters_header
        self.platform_parameters = platform_parameters
        self.extra_sound_info_header = extra_sound_info_header
        self.extra_sound_info = extra_sound_info
        self.reflections_header = reflections_header
        self.reflections = reflections
        self.remastered_sound = remastered_sound
        self.flags = flags
        self.class_type = class_type
        self.sample_rate = sample_rate
        self.output_effect = output_effect
        self.import_type = import_type
        self.minimum_distance = minimum_distance
        self.maximum_distance = maximum_distance
        self.skip_fraction = skip_fraction
        self.maximum_bend_per_second = maximum_bend_per_second
        self.gain_base = gain_base
        self.gain_variance = gain_variance
        self.random_pitch_bounds = random_pitch_bounds
        self.inner_cone_angle = inner_cone_angle
        self.outer_cone_angle = outer_cone_angle
        self.outer_cone_gain = outer_cone_gain
        self.override_flags = override_flags
        self.azimuth = azimuth
        self.positional_gain = positional_gain
        self.first_person_gain = first_person_gain
        self.gain_modifier = gain_modifier
        self.pitch_modifier = pitch_modifier
        self.skip_fraction_modifier = skip_fraction_modifier
        self.encoding = encoding
        self.compression = compression
        self.promotion_rules_tag_block = promotion_rules_tag_block
        self.runtime_timers_tag_block = runtime_timers_tag_block
        self.runtime_active_promotion_index = runtime_active_promotion_index
        self.runtime_last_promotion_time = runtime_last_promotion_time
        self.runtime_suppression_timeout = runtime_suppression_timeout
        self.inner_silence_distance = inner_silence_distance
        self.pitch_ranges_tag_block = pitch_ranges_tag_block
        self.platform_parameters_tag_block = platform_parameters_tag_block
        self.extra_sound_info_tag_block = extra_sound_info_tag_block
        self.reflections_tag_block = reflections_tag_block
        self.low_pass_minimum_distance = low_pass_minimum_distance
        self.low_pass_maximum_distance = low_pass_maximum_distance
        self.parameters = parameters

    class PitchRange:
        def __init__(self, name="", name_length=0, natural_pitch=0, bend_bounds=(0, 0), unk_0=(0, 0), permutations_tag_block=None, permutations_header=None, permutations=None):
            self.name = name
            self.name_length = name_length
            self.natural_pitch = natural_pitch
            self.bend_bounds = bend_bounds
            self.unk_0 = unk_0
            self.permutations_tag_block = permutations_tag_block
            self.permutations_header = permutations_header
            self.permutations = permutations

    class Permutation:
        def __init__(self, name="", name_length=0, skip_fraction=0.0, gain=0.0, sound_data=0, sound_index=0, lipsync_data=0, sound_permutation_chunk_tag_block=None,
                     sound_permutation_chunk_header=None, sound_permutation_chunk=None):
            self.name = name
            self.name_length = name_length
            self.skip_fraction = skip_fraction
            self.gain = gain
            self.sound_data = sound_data
            self.sound_index = sound_index
            self.lipsync_data = lipsync_data
            self.sound_permutation_chunk_tag_block = sound_permutation_chunk_tag_block
            self.sound_permutation_chunk_header = sound_permutation_chunk_header
            self.sound_permutation_chunk = sound_permutation_chunk

    class SoundExtraInfo:
        def __init__(self, language_permutation_info_tag_block=None, language_permutation_info_header=None, language_permutation_info=None, encoded_permutation_section_tag_block=None,
                     encoded_permutation_section_header=None, encoded_permutation_section=None, block_offset=0, block_size=0, section_data_size=0, resource_data_size=0,
                     resources_tag_block=None, resources_header=None, resources=None, owner_tag_section_offset=0):
            self.language_permutation_info_tag_block = language_permutation_info_tag_block
            self.language_permutation_info_header = language_permutation_info_header
            self.language_permutation_info = language_permutation_info
            self.encoded_permutation_section_tag_block = encoded_permutation_section_tag_block
            self.encoded_permutation_section_header = encoded_permutation_section_header
            self.encoded_permutation_section = encoded_permutation_section
            self.block_offset = block_offset
            self.block_size = block_size
            self.section_data_size = section_data_size
            self.resource_data_size = resource_data_size
            self.resources_tag_block = resources_tag_block
            self.resources_header = resources_header
            self.resources = resources
            self.owner_tag_section_offset = owner_tag_section_offset

    class SoundExtraInfo:
        def __init__(self, language_permutation_info_tag_block=None, language_permutation_info_header=None, language_permutation_info=None, encoded_permutation_section_tag_block=None,
                     encoded_permutation_section_header=None, encoded_permutation_section=None, block_offset=0, block_size=0, section_data_size=0, resource_data_size=0,
                     resources_tag_block=None, resources_header=None, resources=None, owner_tag_section_offset=0, blok_header=None):
            self.language_permutation_info_tag_block = language_permutation_info_tag_block
            self.language_permutation_info_header = language_permutation_info_header
            self.language_permutation_info = language_permutation_info
            self.encoded_permutation_section_tag_block = encoded_permutation_section_tag_block
            self.encoded_permutation_section_header = encoded_permutation_section_header
            self.encoded_permutation_section = encoded_permutation_section
            self.block_offset = block_offset
            self.block_size = block_size
            self.section_data_size = section_data_size
            self.resource_data_size = resource_data_size
            self.resources_tag_block = resources_tag_block
            self.resources_header = resources_header
            self.resources = resources
            self.owner_tag_section_offset = owner_tag_section_offset
            self.blok_header = blok_header

    class LanguagePermutationInfo:
        def __init__(self, raw_info_block_tag_block=None, raw_info_block_header=None, raw_info_block=None):
            self.raw_info_block_tag_block = raw_info_block_tag_block
            self.raw_info_block_header = raw_info_block_header
            self.raw_info_block = raw_info_block

    class RawInfoBlock:
        def __init__(self, skip_fraction_name="", skip_fraction_name_length=0, samples_tag_data=None, unk_1_tag_data=None, unk_2_tag_data=None, markers_tag_block=None,
                     markers_header=None, markers=None, compression=0, language=0, sound_permutation_chunk_tag_block=None, sound_permutation_chunk_header=None,
                     sound_permutation_chunk=None, remaining_data=0):
            self.skip_fraction_name = skip_fraction_name
            self.skip_fraction_name_length = skip_fraction_name_length
            self.samples_tag_data = samples_tag_data
            self.unk_1_tag_data = unk_1_tag_data
            self.unk_2_tag_data = unk_2_tag_data
            self.markers_tag_block = markers_tag_block
            self.markers_header = markers_header
            self.markers = markers
            self.compression = compression
            self.language = language
            self.sound_permutation_chunk_tag_block = sound_permutation_chunk_tag_block
            self.sound_permutation_chunk_header = sound_permutation_chunk_header
            self.sound_permutation_chunk = sound_permutation_chunk
            self.remaining_data = remaining_data
