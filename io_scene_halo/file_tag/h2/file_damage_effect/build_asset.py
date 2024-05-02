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

def write_body(output_stream, TAG, DAMAGEFFECT):
    DAMAGEFFECT.damage_effect_body_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<ff', *DAMAGEFFECT.damage_effect_body.radius))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.cutoff_scale))
    output_stream.write(struct.pack('<I', DAMAGEFFECT.damage_effect_body.flags))
    output_stream.write(struct.pack('<H', DAMAGEFFECT.damage_effect_body.side_effect))
    output_stream.write(struct.pack('<H', DAMAGEFFECT.damage_effect_body.category))
    output_stream.write(struct.pack('<I', DAMAGEFFECT.damage_effect_body.damage_flags))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.aoe_core_radius))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.damage_lower_bound))
    output_stream.write(struct.pack('<ff', *DAMAGEFFECT.damage_effect_body.damage_upper_bound))
    output_stream.write(struct.pack('<f', radians(DAMAGEFFECT.damage_effect_body.dmg_inner_cone_angle)))
    output_stream.write(struct.pack('<f', radians(DAMAGEFFECT.damage_effect_body.dmg_outer_cone_angle)))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.active_camouflage_damage))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.stun))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.maximum_stun))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.stun_time))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.instantaneous_acceleration))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.rider_direct_damage_scale))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.rider_maximum_transfer_damage_scale))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.rider_minimum_transfer_damage_scale))
    output_stream.write(struct.pack('>I', len(DAMAGEFFECT.damage_effect_body.general_damage)))
    output_stream.write(struct.pack('>I', len(DAMAGEFFECT.damage_effect_body.specific_damage)))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.ai_stun_radius))
    output_stream.write(struct.pack('<ff', *DAMAGEFFECT.damage_effect_body.ai_stun_bounds))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.shake_radius))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.emp_radius))
    DAMAGEFFECT.damage_effect_body.player_responses_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.impulse_duration))
    output_stream.write(struct.pack('<H', DAMAGEFFECT.damage_effect_body.fade_function))
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<f', radians(DAMAGEFFECT.damage_effect_body.rotation)))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.pushback))
    output_stream.write(struct.pack('<ff', *DAMAGEFFECT.damage_effect_body.jitter))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.shaking_duration))
    output_stream.write(struct.pack('<H', DAMAGEFFECT.damage_effect_body.falloff_function))
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.random_translation))
    output_stream.write(struct.pack('<f', radians(DAMAGEFFECT.damage_effect_body.random_rotation)))
    output_stream.write(struct.pack('<H', DAMAGEFFECT.damage_effect_body.wobble_function))
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.wobble_function_period))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.wobble_weight))
    DAMAGEFFECT.damage_effect_body.sound.write(output_stream, False, True)
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.forward_velocity))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.forward_radius))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.forward_exponent))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.outward_velocity))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.outward_radius))
    output_stream.write(struct.pack('<f', DAMAGEFFECT.damage_effect_body.outward_exponent))

def write_player_responses(output_stream, TAG, player_responses, player_response_header):
    if len(player_responses) > 0:
        player_response_header.write(output_stream, TAG, True)
        for player_response_element in player_responses:
            output_stream.write(struct.pack('<H', player_response_element.response_type))
            output_stream.write(struct.pack('<2x'))
            output_stream.write(struct.pack('<H', player_response_element.flash_type))
            output_stream.write(struct.pack('<H', player_response_element.priority))
            output_stream.write(struct.pack('<f', player_response_element.flash_duration))
            output_stream.write(struct.pack('<H', player_response_element.fade_function))
            output_stream.write(struct.pack('<2x'))
            output_stream.write(struct.pack('<f', player_response_element.maximum_intensity))
            output_stream.write(struct.pack('<ffff', player_response_element.color[3], player_response_element.color[0], player_response_element.color[1], player_response_element.color[2]))
            output_stream.write(struct.pack('<f', player_response_element.low_vibration_duration))
            shader_processing.write_function_size(output_stream, player_response_element.functions[0])
            output_stream.write(struct.pack('<f', player_response_element.high_vibration_duration))
            shader_processing.write_function_size(output_stream, player_response_element.functions[1])
            output_stream.write(struct.pack('>I', len(player_response_element.effect_name)))
            output_stream.write(struct.pack('<f', player_response_element.sound_duration))
            shader_processing.write_function_size(output_stream, player_response_element.functions[2])

        for player_response_element in player_responses:
            output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("SFDS", True), 0, 1, 32))
            output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("RBDS", True), 0, 1, 32))
            output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("RFDS", True), 0, 1, 16))
            shader_processing.write_function(output_stream, TAG, player_response_element.functions[0])

            output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("RFDS", True), 0, 1, 16))
            shader_processing.write_function(output_stream, TAG, player_response_element.functions[1])
            effect_name_length = len(player_response_element.effect_name)
            if effect_name_length > 0:
                output_stream.write(struct.pack('<%ssx' % effect_name_length, TAG.string_to_bytes(player_response_element.effect_name, False)))

            output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("dsfx", True), 0, 1, 20))

            effect_name_length = len(player_response_element.effect_name)
            if effect_name_length > 0:
                output_stream.write(struct.pack('<%ss' % effect_name_length, TAG.string_to_bytes(player_response_element.effect_name, False)))

            shader_processing.write_function(output_stream, TAG, player_response_element.functions[2])

def build_asset(output_stream, DAMAGEFFECT, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    DAMAGEFFECT.header.write(output_stream, False, True)
    write_body(output_stream, TAG, DAMAGEFFECT)

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("masd", True), 1, 1, 4))

    general_damage_length = len(DAMAGEFFECT.damage_effect_body.general_damage)
    if general_damage_length > 0:
        output_stream.write(struct.pack('<%ss' % general_damage_length, TAG.string_to_bytes(DAMAGEFFECT.damage_effect_body.general_damage, False)))

    specific_damage_length = len(DAMAGEFFECT.damage_effect_body.specific_damage)
    if specific_damage_length > 0:
        output_stream.write(struct.pack('<%ss' % specific_damage_length, TAG.string_to_bytes(DAMAGEFFECT.damage_effect_body.specific_damage, False)))

    write_player_responses(output_stream, TAG, DAMAGEFFECT.player_responses, DAMAGEFFECT.player_response_header)

    sound_length = len(DAMAGEFFECT.damage_effect_body.sound.name)
    if sound_length > 0:
        output_stream.write(struct.pack('<%ssx' % sound_length, TAG.string_to_bytes(DAMAGEFFECT.damage_effect_body.sound.name, False)))
