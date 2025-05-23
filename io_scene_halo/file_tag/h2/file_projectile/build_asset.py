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
from ..file_object.build_asset import (
    write_ai_properties,
    write_functions,
    write_attachments,
    write_tag_ref,
    write_old_functions,
    write_change_colors,
    write_predicted_resources
    )

def write_body(output_stream, TAG, PROJECTILE):
    PROJECTILE.body_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<H', 5))
    output_stream.write(struct.pack('<H', PROJECTILE.object_flags))
    output_stream.write(struct.pack('<f', PROJECTILE.bounding_radius))
    output_stream.write(struct.pack('<fff', *PROJECTILE.bounding_offset))
    output_stream.write(struct.pack('<f', PROJECTILE.acceleration_scale))
    output_stream.write(struct.pack('<h', PROJECTILE.lightmap_shadow_mode))
    output_stream.write(struct.pack('<h', PROJECTILE.sweetner_size))
    output_stream.write(struct.pack('<4x'))
    output_stream.write(struct.pack('<f', PROJECTILE.dynamic_light_sphere_radius))
    output_stream.write(struct.pack('<fff', *PROJECTILE.dynamic_light_sphere_offset))
    output_stream.write(struct.pack('>I', len(PROJECTILE.default_model_variant)))
    PROJECTILE.model.write(output_stream, False, True)
    PROJECTILE.crate_object.write(output_stream, False, True)
    PROJECTILE.modifier_shader.write(output_stream, False, True)
    PROJECTILE.creation_effect.write(output_stream, False, True)
    PROJECTILE.material_effects.write(output_stream, False, True)
    PROJECTILE.ai_properties_tag_block.write(output_stream, False)
    PROJECTILE.functions_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', PROJECTILE.apply_collision_damage_scale))
    output_stream.write(struct.pack('<f', PROJECTILE.min_game_acc))
    output_stream.write(struct.pack('<f', PROJECTILE.max_game_acc))
    output_stream.write(struct.pack('<f', PROJECTILE.min_game_scale))
    output_stream.write(struct.pack('<f', PROJECTILE.max_game_scale))
    output_stream.write(struct.pack('<f', PROJECTILE.min_abs_acc))
    output_stream.write(struct.pack('<f', PROJECTILE.max_abs_acc))
    output_stream.write(struct.pack('<f', PROJECTILE.min_abs_scale))
    output_stream.write(struct.pack('<f', PROJECTILE.max_abs_scale))
    output_stream.write(struct.pack('<H', PROJECTILE.hud_text_message_index))
    output_stream.write(struct.pack('<2x'))
    PROJECTILE.attachments_tag_block.write(output_stream, False)
    PROJECTILE.widgets_tag_block.write(output_stream, False)
    PROJECTILE.old_functions_tag_block.write(output_stream, False)
    PROJECTILE.change_colors_tag_block.write(output_stream, False)
    PROJECTILE.predicted_resources_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<I', PROJECTILE.projectile_flags))
    output_stream.write(struct.pack('<H', PROJECTILE.detonation_timer_starts))
    output_stream.write(struct.pack('<H', PROJECTILE.impact_noise))
    output_stream.write(struct.pack('<f', PROJECTILE.ai_perception_radius))
    output_stream.write(struct.pack('<f', PROJECTILE.collision_radius))
    output_stream.write(struct.pack('<f', PROJECTILE.arming_time))
    output_stream.write(struct.pack('<f', PROJECTILE.danger_radius))
    output_stream.write(struct.pack('<ff', *PROJECTILE.timer))
    output_stream.write(struct.pack('<f', PROJECTILE.minimum_velocity))
    output_stream.write(struct.pack('<f', PROJECTILE.maximum_range))
    output_stream.write(struct.pack('<H', PROJECTILE.detonation_noise))
    output_stream.write(struct.pack('<h', PROJECTILE.super_detonation_projectile_count))
    PROJECTILE.detonation_started.write(output_stream, False, True)
    PROJECTILE.detonation_effect_airborne.write(output_stream, False, True)
    PROJECTILE.detonation_effect_ground.write(output_stream, False, True)
    PROJECTILE.detonation_damage.write(output_stream, False, True)
    PROJECTILE.attached_detonation_damage.write(output_stream, False, True)
    PROJECTILE.super_detonation.write(output_stream, False, True)
    PROJECTILE.super_detonation_damage.write(output_stream, False, True)
    PROJECTILE.detonation_sound.write(output_stream, False, True)
    output_stream.write(struct.pack('<H', PROJECTILE.damage_reporting_type))
    output_stream.write(struct.pack('<2x'))
    PROJECTILE.super_attached_detonation_damage_effect.write(output_stream, False, True)
    output_stream.write(struct.pack('<f', PROJECTILE.material_effect_radius))
    PROJECTILE.flyby_sound.write(output_stream, False, True)
    PROJECTILE.impact_effect.write(output_stream, False, True)
    PROJECTILE.impact_damage.write(output_stream, False, True)
    output_stream.write(struct.pack('<f', PROJECTILE.boarding_detonation_time))
    PROJECTILE.boarding_detonation_damage_effect.write(output_stream, False, True)
    PROJECTILE.boarding_attached_detonation_damage_effect.write(output_stream, False, True)
    output_stream.write(struct.pack('<f', PROJECTILE.air_gravity_scale))
    output_stream.write(struct.pack('<ff', *PROJECTILE.air_damage_range))
    output_stream.write(struct.pack('<f', PROJECTILE.water_gravity_scale))
    output_stream.write(struct.pack('<ff', *PROJECTILE.water_damage_range))
    output_stream.write(struct.pack('<f', PROJECTILE.initial_velocity))
    output_stream.write(struct.pack('<f', PROJECTILE.final_velocity))
    output_stream.write(struct.pack('<f', radians(PROJECTILE.guided_angular_velocity_lower)))
    output_stream.write(struct.pack('<f', radians(PROJECTILE.guided_angular_velocity_upper)))
    output_stream.write(struct.pack('<ff', *PROJECTILE.acceleration_range))
    output_stream.write(struct.pack('<4x'))
    output_stream.write(struct.pack('<f', PROJECTILE.targeted_leading_fraction))
    PROJECTILE.material_responses_tag_block.write(output_stream, False)

def write_material_responses(output_stream, TAG, material_responses, material_responses_header):
    if len(material_responses) > 0:
        material_responses_header.write(output_stream, TAG, True)
        for material_response_element in material_responses:
            output_stream.write(struct.pack('<H', material_response_element.flags))
            output_stream.write(struct.pack('<H', material_response_element.result_response))
            material_response_element.result_effect.write(output_stream, False, True)
            output_stream.write(struct.pack('>I', len(material_response_element.material_name)))
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('<H', material_response_element.potential_result_response))
            output_stream.write(struct.pack('<H', material_response_element.potential_result_flags))
            output_stream.write(struct.pack('<f', material_response_element.chance_fraction))
            output_stream.write(struct.pack('<ff', *material_response_element.between))
            output_stream.write(struct.pack('<ff', *material_response_element.and_bounds))
            material_response_element.potential_result_effect.write(output_stream, False, True)
            output_stream.write(struct.pack('<H', material_response_element.scale_effects_by))
            output_stream.write(struct.pack('<2x'))
            output_stream.write(struct.pack('<f', radians(material_response_element.angular_noise)))
            output_stream.write(struct.pack('<f', material_response_element.velocity_noise))
            material_response_element.detonation_effect.write(output_stream, False, True)
            output_stream.write(struct.pack('<f', material_response_element.initial_friction))
            output_stream.write(struct.pack('<f', material_response_element.maximum_distance))
            output_stream.write(struct.pack('<f', material_response_element.parallel_friction))
            output_stream.write(struct.pack('<f', material_response_element.perpendicular_friction))

        for material_response_element in material_responses:
            result_effect_length = len(material_response_element.result_effect.name)
            if result_effect_length > 0:
                output_stream.write(struct.pack('<%ssx' % result_effect_length, TAG.string_to_bytes(material_response_element.result_effect.name, False)))

            material_name_length = len(material_response_element.material_name)
            if material_name_length > 0:
                output_stream.write(struct.pack('<%ss' % material_name_length, TAG.string_to_bytes(material_response_element.material_name, False)))

            potential_result_effect_length = len(material_response_element.potential_result_effect.name)
            if potential_result_effect_length > 0:
                output_stream.write(struct.pack('<%ssx' % potential_result_effect_length, TAG.string_to_bytes(material_response_element.potential_result_effect.name, False)))

            detonation_effect_length = len(material_response_element.detonation_effect.name)
            if detonation_effect_length > 0:
                output_stream.write(struct.pack('<%ssx' % detonation_effect_length, TAG.string_to_bytes(material_response_element.detonation_effect.name, False)))

def build_asset(output_stream, PROJECTILE, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    PROJECTILE.header.write(output_stream, False, True)
    write_body(output_stream, TAG, PROJECTILE)

    default_model_variant_name_length = len(PROJECTILE.default_model_variant)
    if default_model_variant_name_length > 0:
        output_stream.write(struct.pack('<%ss' % default_model_variant_name_length, TAG.string_to_bytes(PROJECTILE.default_model_variant, False)))

    model_name_length = len(PROJECTILE.model.name)
    if model_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % model_name_length, TAG.string_to_bytes(PROJECTILE.model.name, False)))

    crate_object_name_length = len(PROJECTILE.crate_object.name)
    if crate_object_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % crate_object_name_length, TAG.string_to_bytes(PROJECTILE.crate_object.name, False)))

    modifier_shader_name_length = len(PROJECTILE.modifier_shader.name)
    if modifier_shader_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % modifier_shader_name_length, TAG.string_to_bytes(PROJECTILE.modifier_shader.name, False)))

    creation_effect_name_length = len(PROJECTILE.creation_effect.name)
    if creation_effect_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % creation_effect_name_length, TAG.string_to_bytes(PROJECTILE.creation_effect.name, False)))

    material_effects_name_length = len(PROJECTILE.material_effects.name)
    if material_effects_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % material_effects_name_length, TAG.string_to_bytes(PROJECTILE.material_effects.name, False)))

    write_ai_properties(output_stream, TAG, PROJECTILE.ai_properties, PROJECTILE.ai_properties_header)
    write_functions(output_stream, TAG, PROJECTILE.functions, PROJECTILE.functions_header)
    write_attachments(output_stream, TAG, PROJECTILE.attachments, PROJECTILE.attachments_header)
    write_tag_ref(output_stream, TAG, PROJECTILE.widgets, PROJECTILE.widgets_header)
    write_old_functions(output_stream, TAG, PROJECTILE.old_functions, PROJECTILE.old_functions_header)
    write_change_colors(output_stream, TAG, PROJECTILE.change_colors, PROJECTILE.change_colors_header)
    write_predicted_resources(output_stream, TAG, PROJECTILE.predicted_resources, PROJECTILE.predicted_resources_header)

    detonation_started_length = len(PROJECTILE.detonation_started.name)
    if detonation_started_length > 0:
        output_stream.write(struct.pack('<%ssx' % detonation_started_length, TAG.string_to_bytes(PROJECTILE.detonation_started.name, False)))

    detonation_effect_airborne_length = len(PROJECTILE.detonation_effect_airborne.name)
    if detonation_effect_airborne_length > 0:
        output_stream.write(struct.pack('<%ssx' % detonation_effect_airborne_length, TAG.string_to_bytes(PROJECTILE.detonation_effect_airborne.name, False)))

    detonation_effect_ground_length = len(PROJECTILE.detonation_effect_ground.name)
    if detonation_effect_ground_length > 0:
        output_stream.write(struct.pack('<%ssx' % detonation_effect_ground_length, TAG.string_to_bytes(PROJECTILE.detonation_effect_ground.name, False)))

    detonation_damage_length = len(PROJECTILE.detonation_damage.name)
    if detonation_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % detonation_damage_length, TAG.string_to_bytes(PROJECTILE.detonation_damage.name, False)))

    attached_detonation_damage_length = len(PROJECTILE.attached_detonation_damage.name)
    if attached_detonation_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % attached_detonation_damage_length, TAG.string_to_bytes(PROJECTILE.attached_detonation_damage.name, False)))

    super_detonation_length = len(PROJECTILE.super_detonation.name)
    if super_detonation_length > 0:
        output_stream.write(struct.pack('<%ssx' % super_detonation_length, TAG.string_to_bytes(PROJECTILE.super_detonation.name, False)))

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("sd2s", True), 1, 1, 16))

    super_detonation_damage_length = len(PROJECTILE.super_detonation_damage.name)
    if super_detonation_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % super_detonation_damage_length, TAG.string_to_bytes(PROJECTILE.super_detonation_damage.name, False)))

    detonation_sound_length = len(PROJECTILE.detonation_sound.name)
    if detonation_sound_length > 0:
        output_stream.write(struct.pack('<%ssx' % detonation_sound_length, TAG.string_to_bytes(PROJECTILE.detonation_sound.name, False)))

    super_attached_detonation_damage_effect_length = len(PROJECTILE.super_attached_detonation_damage_effect.name)
    if super_attached_detonation_damage_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % super_attached_detonation_damage_effect_length, TAG.string_to_bytes(PROJECTILE.super_attached_detonation_damage_effect.name, False)))

    flyby_sound_length = len(PROJECTILE.flyby_sound.name)
    if flyby_sound_length > 0:
        output_stream.write(struct.pack('<%ssx' % flyby_sound_length, TAG.string_to_bytes(PROJECTILE.flyby_sound.name, False)))

    impact_effect_length = len(PROJECTILE.impact_effect.name)
    if impact_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % impact_effect_length, TAG.string_to_bytes(PROJECTILE.impact_effect.name, False)))

    impact_damage_length = len(PROJECTILE.impact_damage.name)
    if impact_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % impact_damage_length, TAG.string_to_bytes(PROJECTILE.impact_damage.name, False)))

    boarding_detonation_damage_effect_length = len(PROJECTILE.boarding_detonation_damage_effect.name)
    if boarding_detonation_damage_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % boarding_detonation_damage_effect_length, TAG.string_to_bytes(PROJECTILE.boarding_detonation_damage_effect.name, False)))

    boarding_attached_detonation_damage_effect_length = len(PROJECTILE.boarding_attached_detonation_damage_effect.name)
    if boarding_attached_detonation_damage_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % boarding_attached_detonation_damage_effect_length, TAG.string_to_bytes(PROJECTILE.boarding_attached_detonation_damage_effect.name, False)))

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("avlb", True), 1, 1, 4))

    write_material_responses(output_stream, TAG, PROJECTILE.material_responses, PROJECTILE.material_responses_header)
