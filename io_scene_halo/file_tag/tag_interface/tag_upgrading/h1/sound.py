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

from ....global_functions import tag_format, shader_processing
from ....file_tag.h1.file_sound.format import (
    SoundFlags as H1SoundFlags,
    ClassEnum as H1ClassEnum,
    EncodingEnum as H1EncodingEnum,
    CompressionEnum as H1CompressionEnum
    )
from ....file_tag.h2.file_sound.format import (
    SoundAsset,
    SoundFlags as H2SoundFlags,
    ClassEnum as H2ClassEnum,
    OutputEffectEnum,
    ImportTypeEnum,
    EncodingEnum as H2EncodingEnum,
    CompressionEnum as H2CompressionEnum
    )
from ....file_tag.h2.file_shader.format import FunctionTypeEnum, OutputTypeFlags

def convert_sound_flags(sound_flags):
    flags = 0
    active_h1_flags = [flag.name for flag in H1SoundFlags if flag in H1SoundFlags(sound_flags)]
    if "fit_to_adpcm_blocksize" in active_h1_flags:
        flags += H2SoundFlags.fit_to_adpcm_blocksize.value
    if "split_long_sound_into_permutations" in active_h1_flags:
        flags += H2SoundFlags.split_long_sound_into_permutations.value

    return flags

def convert_legacy_class(class_index, tag_path):
    h2_class_index = 0
    h1_class = H1ClassEnum(class_index)
    if h1_class == H1ClassEnum.projectile_impact:
        h2_class_index = H2ClassEnum.projectile_impact.value
    elif h1_class == H1ClassEnum.projectile_detonation:
        h2_class_index = H2ClassEnum.projectile_detonation.value
    elif h1_class == H1ClassEnum.weapon_fire:
        h2_class_index = H2ClassEnum.weapon_fire.value
    elif h1_class == H1ClassEnum.weapon_ready:
        h2_class_index = H2ClassEnum.weapon_ready.value
    elif h1_class == H1ClassEnum.weapon_reload:
        h2_class_index = H2ClassEnum.weapon_reload.value
    elif h1_class == H1ClassEnum.weapon_empty:
        h2_class_index = H2ClassEnum.weapon_empty.value
    elif h1_class == H1ClassEnum.weapon_charge:
        h2_class_index = H2ClassEnum.weapon_charge.value
    elif h1_class == H1ClassEnum.weapon_overheat:
        h2_class_index = H2ClassEnum.weapon_overheat.value
    elif h1_class == H1ClassEnum.weapon_idle:
        h2_class_index = H2ClassEnum.weapon_idle.value
    elif h1_class == H1ClassEnum.object_impacts:
        h2_class_index = H2ClassEnum.object_impacts.value
    elif h1_class == H1ClassEnum.particle_impacts:
        h2_class_index = H2ClassEnum.particle_impacts.value
    elif h1_class == H1ClassEnum.slow_particle_impacts:
        h2_class_index = H2ClassEnum.particle_impacts.value
    elif h1_class == H1ClassEnum.unit_footsteps:
        h2_class_index = H2ClassEnum.unit_footsteps.value
    elif h1_class == H1ClassEnum.unit_dialog:
        h2_class_index = H2ClassEnum.unit_dialog.value
    elif h1_class == H1ClassEnum.vehicle_collision:
        h2_class_index = H2ClassEnum.vehicle_collision.value
    elif h1_class == H1ClassEnum.vehicle_engine:
        h2_class_index = H2ClassEnum.vehicle_engine.value
    elif h1_class == H1ClassEnum.device_door:
        h2_class_index = H2ClassEnum.device_door.value
    elif h1_class == H1ClassEnum.device_force_field:
        h2_class_index = H2ClassEnum.device_door.value
    elif h1_class == H1ClassEnum.device_machinery:
        h2_class_index = H2ClassEnum.device_machinery.value
    elif h1_class == H1ClassEnum.device_nature:
        h2_class_index = H2ClassEnum.device_stationary.value
    elif h1_class == H1ClassEnum.device_computers:
        h2_class_index = H2ClassEnum.device_machinery.value
    elif h1_class == H1ClassEnum.music:
        h2_class_index = H2ClassEnum.music.value
    elif h1_class == H1ClassEnum.ambient_nature:
        h2_class_index = H2ClassEnum.ambient_nature.value
    elif h1_class == H1ClassEnum.ambient_machinery:
        h2_class_index = H2ClassEnum.ambient_machinery.value
    elif h1_class == H1ClassEnum.ambient_computers:
        h2_class_index = H2ClassEnum.ambient_machinery.value
    elif h1_class == H1ClassEnum.first_person_damage:
        h2_class_index = H2ClassEnum.projectile_impact.value
    elif h1_class == H1ClassEnum.scripted_dialog_player:
        h2_class_index = H2ClassEnum.cinematic_dialog.value
    elif h1_class == H1ClassEnum.scripted_effect:
        h2_class_index = H2ClassEnum.scripted_cinematic_foley.value
    elif h1_class == H1ClassEnum.scripted_dialog_other:
        h2_class_index = H2ClassEnum.cinematic_dialog.value
    elif h1_class == H1ClassEnum.scripted_dialog_force_unspatialized:
        h2_class_index = H2ClassEnum.cinematic_dialog.value
    elif h1_class == H1ClassEnum.game_event:
        h2_class_index = H2ClassEnum.game_event.value
    else:
        print("bad_value: ", tag_path)

    return h2_class_index

def convert_legacy_compression(class_index):
    h2_class_index = 0
    h1_class = H1CompressionEnum(class_index)
    if h1_class == H1CompressionEnum.none:
        h2_class_index = H2CompressionEnum.none_big_endian.value
    elif h1_class == H1CompressionEnum.xbox_adpcm:
        h2_class_index = H2CompressionEnum.xbox_adpcm.value
    elif h1_class == H1CompressionEnum.ima_adpcm:
        h2_class_index = H2CompressionEnum.ima_adpcm.value
    elif h1_class == H1CompressionEnum.ogg:
        h2_class_index = H2CompressionEnum.none_big_endian.value

    return h2_class_index

def generate_pitch_ranges(H1_ASSET, TAG, SOUND):
    for pitch_range_element in H1_ASSET.pitch_ranges:
        pitch_range = SOUND.PitchRange()
        pitch_range.name = pitch_range_element.name
        pitch_range.name_length = len(pitch_range.name)
        pitch_range.natural_pitch = pitch_range_element.natural_pitch
        pitch_range.bend_bounds = (round(pitch_range_element.bend_bounds[0]), round(pitch_range_element.bend_bounds[1]))
        pitch_range.unk_0 = (0, 0)

        pitch_range.permutations = []
        unique_perms = []
        MAX_BLOCK_COUNT = 32
        if not len(pitch_range.permutations) > MAX_BLOCK_COUNT:
            for permutation_element in pitch_range.permutations:
                permutation_name = permutation_element.name
                if not permutation_name in unique_perms:
                    unique_perms.append(permutation_name)
                    permutation = SOUND.Permutation()
                    permutation.name = permutation_name
                    permutation.name_length = len(permutation.name)
                    permutation.skip_fraction = permutation_element.skip_fraction
                    permutation.gain = permutation_element.gain
                    permutation.sound_data = 1
                    permutation.sound_index = 0
                    permutation.lipsync_data = 0

                    permutation.sound_permutation_chunk = []
                    permutation.sound_permutation_chunk_header = TAG.TagBlockHeader("tbfd", 0, 0, 16)
                    permutation.sound_permutation_chunk_tag_block = TAG.TagBlock()

                    pitch_range.permutations.append(permutation)

        permutation_count = len(pitch_range.permutations)
        pitch_range.permutations_header = TAG.TagBlockHeader("tbfd", 0, permutation_count, 32)
        pitch_range.permutations_tag_block = TAG.TagBlock(permutation_count)

        SOUND.pitch_ranges.append(pitch_range)

    pitch_range_count = len(SOUND.pitch_ranges)
    SOUND.pitch_ranges_header = TAG.TagBlockHeader("tbfd", 0, pitch_range_count, 32)

    return TAG.TagBlock(pitch_range_count)

def generate_extra_sound_info(TAG, SOUND):
    sound_extra_info = SOUND.SoundExtraInfo()
    sound_extra_info.block_offset = 0
    sound_extra_info.block_size = 0
    sound_extra_info.section_data_size = 0
    sound_extra_info.resource_data_size = 0
    sound_extra_info.owner_tag_section_offset = 0
    sound_extra_info.blok_header = TAG.TagBlockHeader("BLOK", 0, 1, 40)

    sound_extra_info.language_permutation_info = []
    language_permutation_info = SOUND.LanguagePermutationInfo()

    language_permutation_info.raw_info_block = []

    sample_data = TAG.RawData()
    sample_data.data = bytes()

    unk_1_data = TAG.RawData()
    unk_1_data.data = bytes()

    unk_2_data = TAG.RawData()
    unk_2_data.data = bytes()

    raw_info_block = SOUND.RawInfoBlock()
    raw_info_block.skip_fraction_name = ""
    raw_info_block.skip_fraction_name_length = 0
    raw_info_block.samples_tag_data = sample_data
    raw_info_block.unk_1_tag_data = unk_1_data
    raw_info_block.unk_2_tag_data = unk_2_data
    raw_info_block.compression = 0
    raw_info_block.language = 0
    raw_info_block.remaining_data = 1

    raw_info_block.markers = []
    raw_info_block.markers_header = TAG.TagBlockHeader("tbfd", 0, 1, 12)
    raw_info_block.markers_tag_block = TAG.TagBlock()

    raw_info_block.sound_permutation_chunk = []
    raw_info_block.sound_permutation_chunk_header = TAG.TagBlockHeader("tbfd", 0, 1, 16)
    raw_info_block.sound_permutation_chunk_tag_block = TAG.TagBlock()

    language_permutation_info.raw_info_block.append(raw_info_block)

    raw_info_block_count = len(language_permutation_info.raw_info_block)
    language_permutation_info.raw_info_block_header = TAG.TagBlockHeader("tbfd", 0, raw_info_block_count, 96)
    language_permutation_info.raw_info_block_tag_block = TAG.TagBlock(raw_info_block_count)

    sound_extra_info.language_permutation_info.append(language_permutation_info)

    language_permutation_info_count = len(sound_extra_info.language_permutation_info)
    sound_extra_info.language_permutation_info_header = TAG.TagBlockHeader("tbfd", 2, language_permutation_info_count, 12)
    sound_extra_info.language_permutation_info_tag_block = TAG.TagBlock(language_permutation_info_count)


    sound_extra_info.encoded_permutation_section = []
    sound_extra_info.encoded_permutation_section_header = TAG.TagBlockHeader("tbfd", 0, 0, 16)
    sound_extra_info.encoded_permutation_section_tag_block = TAG.TagBlock()

    sound_extra_info.resources = []
    sound_extra_info.resources_header = TAG.TagBlockHeader("tbfd", 0, 0, 16)
    sound_extra_info.resources_tag_block = TAG.TagBlock()

    SOUND.extra_sound_info.append(sound_extra_info)
    extra_sound_info_count = len(SOUND.extra_sound_info)
    SOUND.extra_sound_info_header = TAG.TagBlockHeader("tbfd", 0, extra_sound_info_count, 64)

    return TAG.TagBlock(extra_sound_info_count)

def upgrade_sound(H1_ASSET, patch_txt_path, report):
    TAG = tag_format.TagAsset()
    SOUND = SoundAsset()
    TAG.upgrade_patches = tag_format.get_patch_set(patch_txt_path)

    SOUND.header = TAG.Header()
    SOUND.header.unk1 = 0
    SOUND.header.flags = 0
    SOUND.header.type = 0
    SOUND.header.name = ""
    SOUND.header.tag_group = "snd!"
    SOUND.header.checksum = 0
    SOUND.header.data_offset = 64
    SOUND.header.data_length = 0
    SOUND.header.unk2 = 0
    SOUND.header.version = 4
    SOUND.header.destination = 0
    SOUND.header.plugin_handle = -1
    SOUND.header.engine_tag = "BLM!"

    SOUND.promotion_rules = []
    SOUND.runtime_timers = []
    SOUND.pitch_ranges = []
    SOUND.platform_parameters = []
    SOUND.extra_sound_info = []
    SOUND.reflections = []

    SOUND.body_header = TAG.TagBlockHeader("tbfd", 7, 1, 220)
    SOUND.remastered_sound = TAG.TagRef("snd!")
    SOUND.flags = convert_sound_flags(H1_ASSET.flags)
    SOUND.class_type = convert_legacy_class(H1_ASSET.class_type, "")
    SOUND.sample_rate = H1_ASSET.sample_rate
    SOUND.output_effect = OutputEffectEnum.none.value
    SOUND.import_type = ImportTypeEnum.single_layer.value
    SOUND.minimum_distance = H1_ASSET.minimum_distance
    SOUND.maximum_distance = H1_ASSET.maximum_distance
    SOUND.skip_fraction = H1_ASSET.skip_fraction
    SOUND.maximum_bend_per_second = H1_ASSET.maximum_bend_per_second
    SOUND.gain_base = 0.0
    SOUND.gain_variance = H1_ASSET.randomization_gain_modifier
    SOUND.random_pitch_bounds = (round(H1_ASSET.random_pitch_bounds[0]), round(H1_ASSET.random_pitch_bounds[1]))
    SOUND.inner_cone_angle = H1_ASSET.inner_cone_angle
    SOUND.outer_cone_angle = H1_ASSET.outer_cone_angle
    SOUND.outer_cone_gain = H1_ASSET.outer_cone_gain
    SOUND.override_flags = 0
    SOUND.azimuth = 0.0
    SOUND.positional_gain = 0.0
    SOUND.first_person_gain = 0.0
    SOUND.gain_modifier = (H1_ASSET.scale_zero_gain_modifier, H1_ASSET.scale_one_gain_modifier)
    SOUND.pitch_modifier = (round(H1_ASSET.scale_zero_pitch_modifier), round(H1_ASSET.scale_one_pitch_modifier))
    SOUND.skip_fraction_modifier = (H1_ASSET.scale_zero_skip_fraction_modifier, H1_ASSET.scale_one_skip_fraction_modifier)
    SOUND.encoding = H1_ASSET.encoding
    SOUND.compression = convert_legacy_compression(H1_ASSET.compression)
    SOUND.promotion_rules_tag_block = TAG.TagBlock()
    SOUND.runtime_timers_tag_block = TAG.TagBlock()
    SOUND.runtime_active_promotion_index = 0
    SOUND.runtime_last_promotion_time = 0
    SOUND.runtime_suppression_timeout = 0
    SOUND.inner_silence_distance = 0.0
    SOUND.pitch_ranges_tag_block = generate_pitch_ranges(H1_ASSET, TAG, SOUND)
    SOUND.platform_parameters_tag_block = TAG.TagBlock()
    SOUND.extra_sound_info_tag_block = generate_extra_sound_info(TAG, SOUND)
    SOUND.reflections_tag_block = TAG.TagBlock()
    SOUND.low_pass_minimum_distance = 0.0
    SOUND.low_pass_maximum_distance = 1.0
    SOUND.parameters = []
    shader_processing.convert_legacy_function(SOUND, TAG, SOUND.parameters, value_0=0.0, value_1=0.0, value_2=0, value_3=0)

    return SOUND
