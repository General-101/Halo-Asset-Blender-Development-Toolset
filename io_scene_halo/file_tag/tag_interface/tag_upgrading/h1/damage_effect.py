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

import json

from enum import Flag, Enum, auto
from ....global_functions import tag_format, shader_processing
from ....file_tag.h2.file_damage_effect.format import DamageEffectAsset, FunctionTypeEnum as DamageFunctionTypeEnum
from ....file_tag.h2.file_shader.format import FunctionTypeEnum

class _20030504_FunctionEnum(Enum):
    linear = 0
    early = auto()
    very_early = auto()
    late = auto()
    very_late = auto()
    cosine = auto()

def convert_legacy_function(function_index):
    h2_function_index = 0
    h1_function = _20030504_FunctionEnum(function_index)
    if h1_function == _20030504_FunctionEnum.linear:
        h2_function_index = DamageFunctionTypeEnum.linear.value
    elif h1_function == _20030504_FunctionEnum.early:
        h2_function_index = DamageFunctionTypeEnum.early.value
    elif h1_function == _20030504_FunctionEnum.very_early:
        h2_function_index = DamageFunctionTypeEnum.very_early.value
    elif h1_function == _20030504_FunctionEnum.late:
        h2_function_index = DamageFunctionTypeEnum.late.value
    elif h1_function == _20030504_FunctionEnum.very_late:
        h2_function_index = DamageFunctionTypeEnum.very_late.value
    elif h1_function == _20030504_FunctionEnum.cosine:
        h2_function_index = DamageFunctionTypeEnum.cosine.value

    return h2_function_index

def upgrade_damage_effect(H2_ASSET, patch_txt_path, report):
    dump_dic = json.load(H2_ASSET)

    TAG = tag_format.TagAsset()
    DAMAGEEFFECT = DamageEffectAsset()
    TAG.upgrade_patches = tag_format.get_patch_set(patch_txt_path)

    DAMAGEEFFECT.header = TAG.Header()
    DAMAGEEFFECT.header.unk1 = 0
    DAMAGEEFFECT.header.flags = 0
    DAMAGEEFFECT.header.type = 0
    DAMAGEEFFECT.header.name = ""
    DAMAGEEFFECT.header.tag_group = "jpt!"
    DAMAGEEFFECT.header.checksum = 0
    DAMAGEEFFECT.header.data_offset = 64
    DAMAGEEFFECT.header.data_length = 0
    DAMAGEEFFECT.header.unk2 = 0
    DAMAGEEFFECT.header.version = 6
    DAMAGEEFFECT.header.destination = 0
    DAMAGEEFFECT.header.plugin_handle = -1
    DAMAGEEFFECT.header.engine_tag = "BLM!"

    DAMAGEEFFECT.player_responses = []

    radius = dump_dic['Data']['Radius']
    damage_upper_bound = dump_dic['Data']['Damage Upper Bound']
    ai_stun_bounds = dump_dic['Data']['Ai Stun Bounds']
    jitter = dump_dic['Data']['Jitter']

    DAMAGEEFFECT.body_header = TAG.TagBlockHeader("tbfd", 1, 1, 212)
    DAMAGEEFFECT.radius = (radius["Min"], radius["Max"])
    DAMAGEEFFECT.cutoff_scale = dump_dic['Data']['Cutoff Scale']
    DAMAGEEFFECT.flags = dump_dic['Data']['Flags']
    DAMAGEEFFECT.side_effect = dump_dic['Data']['Side Effect']['Value']
    DAMAGEEFFECT.category = dump_dic['Data']['Category']['Value']
    DAMAGEEFFECT.damage_flags = dump_dic['Data']['Damage Flags']
    DAMAGEEFFECT.aoe_core_radius = dump_dic['Data']['Aoe Core Radius']
    DAMAGEEFFECT.damage_lower_bound = dump_dic['Data']['Damage Lower Bound']
    DAMAGEEFFECT.damage_upper_bound = (damage_upper_bound["Min"], damage_upper_bound["Max"])
    DAMAGEEFFECT.dmg_inner_cone_angle = 0.0
    DAMAGEEFFECT.dmg_outer_cone_angle = 0.0
    DAMAGEEFFECT.active_camouflage_damage = dump_dic['Data']['Active Camouflage Damage']
    DAMAGEEFFECT.stun = dump_dic['Data']['Stun']
    DAMAGEEFFECT.maximum_stun = dump_dic['Data']['Maximum Stun']
    DAMAGEEFFECT.stun_time = dump_dic['Data']['Stun Time']
    DAMAGEEFFECT.instantaneous_acceleration = dump_dic['Data']['Instantaneous Acceleration']
    DAMAGEEFFECT.rider_direct_damage_scale = 0.0
    DAMAGEEFFECT.rider_maximum_transfer_damage_scale = 0.0
    DAMAGEEFFECT.rider_minimum_transfer_damage_scale = 0.0
    DAMAGEEFFECT.general_damage = dump_dic['Data']['General Damage']
    DAMAGEEFFECT.general_damage_length = len(DAMAGEEFFECT.general_damage)
    DAMAGEEFFECT.specific_damage = dump_dic['Data']['Specific Damage']
    DAMAGEEFFECT.specific_damage_length = len(DAMAGEEFFECT.specific_damage)
    DAMAGEEFFECT.ai_stun_radius = dump_dic['Data']['Ai Stun Radius']
    DAMAGEEFFECT.ai_stun_bounds = (ai_stun_bounds["Min"], ai_stun_bounds["Max"])
    DAMAGEEFFECT.shake_radius = 0.0
    DAMAGEEFFECT.emp_radius = 0.0

    player_response = DAMAGEEFFECT.PlayerResponse()
    player_response.response_type = 0
    player_response.flash_type = dump_dic['Data']['Type']['Value']
    player_response.priority = dump_dic['Data']['Priority']['Value']
    player_response.flash_duration = dump_dic['Data']['Flash Duration']
    player_response.fade_function = convert_legacy_function(dump_dic['Data']['Flash Fade Function']['Value'])
    player_response.maximum_intensity = dump_dic['Data']['Maximum Intensity']
    player_response.color = shader_processing.get_rgb_percentage(dump_dic['Data']["Color"])
    player_response.low_vibration_duration = dump_dic['Data']['Low Rumble Duration']
    player_response.high_vibration_duration = dump_dic['Data']['High Rumble Duration']
    player_response.effect_name = ""
    player_response.effect_name_length = len(player_response.effect_name)
    player_response.sound_duration = 0.0
    player_response.functions = []

    low_rumble_frequency = dump_dic['Data']['Low Rumble Frequency']
    low_rumble_fade = dump_dic['Data']['Low Rumble Fade Function']['Value']
    high_rumble_frequency = dump_dic['Data']['High Rumble Frequency']
    high_rumble_fade = dump_dic['Data']['High Rumble Fade Function']['Value']

    shader_processing.convert_legacy_function(DAMAGEEFFECT, TAG, player_response.functions, function_type=FunctionTypeEnum.transition, function_0_type=low_rumble_fade, function_values=[0.0, low_rumble_frequency, 0.0, 1.0])
    shader_processing.convert_legacy_function(DAMAGEEFFECT, TAG, player_response.functions, function_type=FunctionTypeEnum.transition, function_0_type=high_rumble_fade, function_values=[0.0, high_rumble_frequency, 0.0, 1.0])
    shader_processing.convert_legacy_function(DAMAGEEFFECT, TAG, player_response.functions, function_type=FunctionTypeEnum.constant)

    DAMAGEEFFECT.player_responses.append(player_response)

    player_responses_count = len(DAMAGEEFFECT.player_responses)
    DAMAGEEFFECT.player_response_header = TAG.TagBlockHeader("tbfd", 0, player_responses_count, 88)
    DAMAGEEFFECT.player_responses_tag_block = TAG.TagBlock(player_responses_count)

    DAMAGEEFFECT.impulse_duration = dump_dic['Data']['Impulse Duration']
    DAMAGEEFFECT.fade_function = dump_dic['Data']['Fade Function']['Value']
    DAMAGEEFFECT.rotation = dump_dic['Data']['Rotation']
    DAMAGEEFFECT.pushback = dump_dic['Data']['Pushback']
    DAMAGEEFFECT.jitter = (jitter["Min"], jitter["Max"])
    DAMAGEEFFECT.shaking_duration = dump_dic['Data']['Shaking Duration']
    DAMAGEEFFECT.falloff_function = dump_dic['Data']['Falloff Function']['Value']
    DAMAGEEFFECT.random_translation = dump_dic['Data']['Random Translation']
    DAMAGEEFFECT.random_rotation = dump_dic['Data']['Random Rotation']
    DAMAGEEFFECT.wobble_function = dump_dic['Data']['Wobble Function']['Value']
    DAMAGEEFFECT.wobble_function_period = dump_dic['Data']['Wobble Function Period']
    DAMAGEEFFECT.wobble_weight = dump_dic['Data']['Wobble Weight']
    DAMAGEEFFECT.sound = TAG.TagRef().convert_from_json(dump_dic['Data']['Sound'])
    DAMAGEEFFECT.forward_velocity = dump_dic['Data']['Forward Velocity']
    DAMAGEEFFECT.forward_radius = dump_dic['Data']['Forward Radius']
    DAMAGEEFFECT.forward_exponent = dump_dic['Data']['Forward Exponent']
    DAMAGEEFFECT.outward_velocity = dump_dic['Data']['Outward Velocity']
    DAMAGEEFFECT.outward_radius = dump_dic['Data']['Outward Radius']
    DAMAGEEFFECT.outward_exponent = dump_dic['Data']['Outward Exponent']

    return DAMAGEEFFECT
