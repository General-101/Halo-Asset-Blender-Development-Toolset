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
from ..file_object.build_asset import (
    write_ai_properties,
    write_functions,
    write_attachments,
    write_tag_ref,
    write_old_functions,
    write_change_colors,
    write_predicted_resources
    )
from ..file_item.build_asset import write_predicted_bitmaps

def write_body(output_stream, TAG, WEAPON):
    WEAPON.body_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<H', 2))
    output_stream.write(struct.pack('<H', WEAPON.object_flags))
    output_stream.write(struct.pack('<f', WEAPON.bounding_radius))
    output_stream.write(struct.pack('<fff', *WEAPON.bounding_offset))
    output_stream.write(struct.pack('<f', WEAPON.acceleration_scale))
    output_stream.write(struct.pack('<h', WEAPON.lightmap_shadow_mode))
    output_stream.write(struct.pack('<h', WEAPON.sweetner_size))
    output_stream.write(struct.pack('<4x'))
    output_stream.write(struct.pack('<f', WEAPON.dynamic_light_sphere_radius))
    output_stream.write(struct.pack('<fff', *WEAPON.dynamic_light_sphere_offset))
    output_stream.write(struct.pack('>I', len(WEAPON.default_model_variant)))
    WEAPON.model.write(output_stream, False, True)
    WEAPON.crate_object.write(output_stream, False, True)
    WEAPON.modifier_shader.write(output_stream, False, True)
    WEAPON.creation_effect.write(output_stream, False, True)
    WEAPON.material_effects.write(output_stream, False, True)
    WEAPON.ai_properties_tag_block.write(output_stream, False)
    WEAPON.functions_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', WEAPON.apply_collision_damage_scale))
    output_stream.write(struct.pack('<f', WEAPON.min_game_acc))
    output_stream.write(struct.pack('<f', WEAPON.max_game_acc))
    output_stream.write(struct.pack('<f', WEAPON.min_game_scale))
    output_stream.write(struct.pack('<f', WEAPON.max_game_scale))
    output_stream.write(struct.pack('<f', WEAPON.min_abs_acc))
    output_stream.write(struct.pack('<f', WEAPON.max_abs_acc))
    output_stream.write(struct.pack('<f', WEAPON.min_abs_scale))
    output_stream.write(struct.pack('<f', WEAPON.max_abs_scale))
    output_stream.write(struct.pack('<H', WEAPON.hud_text_message_index))
    output_stream.write(struct.pack('<2x'))
    WEAPON.attachments_tag_block.write(output_stream, False)
    WEAPON.widgets_tag_block.write(output_stream, False)
    WEAPON.old_functions_tag_block.write(output_stream, False)
    WEAPON.change_colors_tag_block.write(output_stream, False)
    WEAPON.predicted_resources_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<I', WEAPON.item_flags))
    output_stream.write(struct.pack('<h', WEAPON.old_message_index))
    output_stream.write(struct.pack('<h', WEAPON.sort_order))
    output_stream.write(struct.pack('<f', WEAPON.multiplayer_on_ground_scale))
    output_stream.write(struct.pack('<f', WEAPON.campaign_on_ground_scale))
    output_stream.write(struct.pack('>I', len(WEAPON.pickup_message)))
    output_stream.write(struct.pack('>I', len(WEAPON.swap_message)))
    output_stream.write(struct.pack('>I', len(WEAPON.pickup_or_dual_msg)))
    output_stream.write(struct.pack('>I', len(WEAPON.swap_or_dual_msg)))
    output_stream.write(struct.pack('>I', len(WEAPON.dual_only_msg)))
    output_stream.write(struct.pack('>I', len(WEAPON.picked_up_msg)))
    output_stream.write(struct.pack('>I', len(WEAPON.singluar_quantity_msg)))
    output_stream.write(struct.pack('>I', len(WEAPON.plural_quantity_msg)))
    output_stream.write(struct.pack('>I', len(WEAPON.switch_to_msg)))
    output_stream.write(struct.pack('>I', len(WEAPON.switch_to_from_ai_msg)))
    WEAPON.unused.write(output_stream, False, True)
    WEAPON.collision_sound.write(output_stream, False, True)
    WEAPON.predicted_bitmaps_tag_block.write(output_stream, False)
    WEAPON.detonation_damage_effect.write(output_stream, False, True)
    output_stream.write(struct.pack('<ff', *WEAPON.detonation_delay))
    WEAPON.detonating_effect.write(output_stream, False, True)
    WEAPON.detonation_effect.write(output_stream, False, True)
    output_stream.write(struct.pack('<I', WEAPON.weapon_flags))
    output_stream.write(struct.pack('>I', len(WEAPON.unknown)))
    output_stream.write(struct.pack('<H', WEAPON.secondary_trigger_mode))
    output_stream.write(struct.pack('<h', WEAPON.maximum_alternate_shots_loaded))
    output_stream.write(struct.pack('<f', WEAPON.turn_on_time))
    output_stream.write(struct.pack('<f', WEAPON.ready_time))
    WEAPON.ready_effect.write(output_stream, False, True)
    WEAPON.ready_damage_effect.write(output_stream, False, True)
    output_stream.write(struct.pack('<f', WEAPON.heat_recovery_threshold))
    output_stream.write(struct.pack('<f', WEAPON.overheated_threshold))
    output_stream.write(struct.pack('<f', WEAPON.heat_detonation_threshold))
    output_stream.write(struct.pack('<f', WEAPON.heat_detonation_fraction))
    output_stream.write(struct.pack('<f', WEAPON.heat_loss_per_second))
    output_stream.write(struct.pack('<f', WEAPON.heat_illumination))
    output_stream.write(struct.pack('<f', WEAPON.overheated_loss_per_second))
    WEAPON.overheated.write(output_stream, False, True)
    WEAPON.overheated_damage_effect.write(output_stream, False, True)
    WEAPON.detonation.write(output_stream, False, True)
    WEAPON.weapon_detonation_damage_effect.write(output_stream, False, True)
    WEAPON.player_melee_damage.write(output_stream, False, True)
    WEAPON.player_melee_response.write(output_stream, False, True)
    output_stream.write(struct.pack('<f', radians(WEAPON.magnetism_angle)))
    output_stream.write(struct.pack('<f', WEAPON.magnetism_range))
    output_stream.write(struct.pack('<f', WEAPON.throttle_magnitude))
    output_stream.write(struct.pack('<f', WEAPON.throttle_minimum_distance))
    output_stream.write(struct.pack('<f', radians(WEAPON.throttle_maximum_adjustment_angle)))
    output_stream.write(struct.pack('<ff', radians(WEAPON.damage_pyramid_angles[0]), radians(WEAPON.damage_pyramid_angles[1])))
    output_stream.write(struct.pack('<f', WEAPON.damage_pyramid_depth))
    WEAPON.first_hit_melee_damage.write(output_stream, False, True)
    WEAPON.first_hit_melee_response.write(output_stream, False, True)
    WEAPON.second_hit_melee_damage.write(output_stream, False, True)
    WEAPON.second_hit_melee_response.write(output_stream, False, True)
    WEAPON.third_hit_melee_damage.write(output_stream, False, True)
    WEAPON.third_hit_melee_response.write(output_stream, False, True)
    WEAPON.lunge_melee_damage.write(output_stream, False, True)
    WEAPON.lunge_melee_response.write(output_stream, False, True)
    output_stream.write(struct.pack('<B', WEAPON.melee_damage_reporting_type))
    output_stream.write(struct.pack('<1x'))
    output_stream.write(struct.pack('<h', WEAPON.magnification_levels))
    output_stream.write(struct.pack('<ff', *WEAPON.magnification_range))
    output_stream.write(struct.pack('<f', radians(WEAPON.autoaim_angle)))
    output_stream.write(struct.pack('<f', WEAPON.autoaim_range))
    output_stream.write(struct.pack('<f', radians(WEAPON.weapon_aim_assist_magnetism_angle)))
    output_stream.write(struct.pack('<f', WEAPON.weapon_aim_assist_magnetism_range))
    output_stream.write(struct.pack('<f', radians(WEAPON.deviation_angle)))
    output_stream.write(struct.pack('<16x'))
    output_stream.write(struct.pack('<H', WEAPON.movement_penalized))
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<f', WEAPON.forward_movement_penalty))
    output_stream.write(struct.pack('<f', WEAPON.sideways_movement_penalty))
    output_stream.write(struct.pack('<f', WEAPON.ai_scariness))
    output_stream.write(struct.pack('<f', WEAPON.weapon_power_on_time))
    output_stream.write(struct.pack('<f', WEAPON.weapon_power_off_time))
    WEAPON.weapon_power_on_effect.write(output_stream, False, True)
    WEAPON.weapon_power_off_effect.write(output_stream, False, True)
    output_stream.write(struct.pack('<f', WEAPON.age_heat_recovery_penalty))
    output_stream.write(struct.pack('<f', WEAPON.age_rate_of_fire_penalty))
    output_stream.write(struct.pack('<f', WEAPON.age_misfire_start))
    output_stream.write(struct.pack('<f', WEAPON.age_misfire_chance))
    WEAPON.pickup_sound.write(output_stream, False, True)
    WEAPON.zoom_in_sound.write(output_stream, False, True)
    WEAPON.zoom_out_sound.write(output_stream, False, True)
    output_stream.write(struct.pack('<f', WEAPON.active_camo_ding))
    output_stream.write(struct.pack('<f', WEAPON.active_camo_regrowth_rate))
    output_stream.write(struct.pack('>I', len(WEAPON.handle_node)))
    output_stream.write(struct.pack('>I', len(WEAPON.weapon_class)))
    output_stream.write(struct.pack('>I', len(WEAPON.weapon_name)))
    output_stream.write(struct.pack('<H', WEAPON.multiplayer_weapon_type))
    output_stream.write(struct.pack('<H', WEAPON.weapon_type))
    output_stream.write(struct.pack('<H', WEAPON.tracking_type))
    output_stream.write(struct.pack('<18x'))
    WEAPON.first_person_tag_block.write(output_stream, False)
    WEAPON.new_hud_interface.write(output_stream, False, True)
    WEAPON.weapon_predicted_resources_tag_block.write(output_stream, False)
    WEAPON.magazines_tag_block.write(output_stream, False)
    WEAPON.new_triggers_tag_block.write(output_stream, False)
    WEAPON.barrels_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<8x'))
    output_stream.write(struct.pack('<f', WEAPON.max_movement_acceleration))
    output_stream.write(struct.pack('<f', WEAPON.max_movement_velocity))
    output_stream.write(struct.pack('<f', WEAPON.max_turning_acceleration))
    output_stream.write(struct.pack('<f', WEAPON.max_turning_velocity))
    WEAPON.deployed_vehicle.write(output_stream, False, True)
    WEAPON.age_effect.write(output_stream, False, True)
    WEAPON.aged_weapon.write(output_stream, False, True)
    output_stream.write(struct.pack('<fff', *WEAPON.first_person_weapon_offset))
    output_stream.write(struct.pack('<ff', *WEAPON.first_person_scope_size))

def write_first_person(output_stream, TAG, first_person, first_person_header):
    if len(first_person) > 0:
        first_person_header.write(output_stream, TAG, True)
        for first_person_element in first_person:
            first_person_element.first_person_model.write(output_stream, False, True)
            first_person_element.first_person_animations.write(output_stream, False, True)

        for first_person_element in first_person:
            first_person_model_length = len(first_person_element.first_person_model.name)
            if first_person_model_length > 0:
                output_stream.write(struct.pack('<%ssx' % first_person_model_length, TAG.string_to_bytes(first_person_element.first_person_model.name, False)))

            first_person_animations_length = len(first_person_element.first_person_animations.name)
            if first_person_animations_length > 0:
                output_stream.write(struct.pack('<%ssx' % first_person_animations_length, TAG.string_to_bytes(first_person_element.first_person_animations.name, False)))

def write_magazines(output_stream, TAG, magazines, magazines_header):
    if len(magazines) > 0:
        magazines_header.write(output_stream, TAG, True)
        for magazine_stat_element in magazines:
            output_stream.write(struct.pack('<I', magazine_stat_element.flags))
            output_stream.write(struct.pack('<h', magazine_stat_element.rounds_recharged))
            output_stream.write(struct.pack('<h', magazine_stat_element.rounds_total_initial))
            output_stream.write(struct.pack('<h', magazine_stat_element.rounds_total_maximum))
            output_stream.write(struct.pack('<h', magazine_stat_element.rounds_loaded_maximum))
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('<f', magazine_stat_element.reload_time))
            output_stream.write(struct.pack('<h', magazine_stat_element.rounds_reloaded))
            output_stream.write(struct.pack('<2x'))
            output_stream.write(struct.pack('<f', magazine_stat_element.chamber_time))
            output_stream.write(struct.pack('<24x'))
            magazine_stat_element.reloading_effect.write(output_stream, False, True)
            magazine_stat_element.reloading_damage_effect.write(output_stream, False, True)
            magazine_stat_element.chambering_effect.write(output_stream, False, True)
            magazine_stat_element.chambering_damage_effect.write(output_stream, False, True)
            magazine_stat_element.magazines_tag_block.write(output_stream, False)

        for magazine_stat_element in magazines:
            reloading_effect_length = len(magazine_stat_element.reloading_effect.name)
            if reloading_effect_length > 0:
                output_stream.write(struct.pack('<%ssx' % reloading_effect_length, TAG.string_to_bytes(magazine_stat_element.reloading_effect.name, False)))

            reloading_damage_effect_length = len(magazine_stat_element.reloading_damage_effect.name)
            if reloading_damage_effect_length > 0:
                output_stream.write(struct.pack('<%ssx' % reloading_damage_effect_length, TAG.string_to_bytes(magazine_stat_element.reloading_damage_effect.name, False)))

            chambering_effect_length = len(magazine_stat_element.chambering_effect.name)
            if chambering_effect_length > 0:
                output_stream.write(struct.pack('<%ssx' % chambering_effect_length, TAG.string_to_bytes(magazine_stat_element.chambering_effect.name, False)))

            chambering_damage_effect_length = len(magazine_stat_element.chambering_damage_effect.name)
            if chambering_damage_effect_length > 0:
                output_stream.write(struct.pack('<%ssx' % chambering_damage_effect_length, TAG.string_to_bytes(magazine_stat_element.chambering_damage_effect.name, False)))

            if len(magazine_stat_element.magazines) > 0:
                magazine_stat_element.magazines_header.write(output_stream, TAG, True)
                for magazine_element in magazine_stat_element.magazines:
                    output_stream.write(struct.pack('<h', magazine_element.rounds))
                    output_stream.write(struct.pack('<2x'))
                    magazine_element.equipment.write(output_stream, False, True)

                for magazine_element in magazine_stat_element.magazines:
                    equipment_length = len(magazine_element.equipment.name)
                    if equipment_length > 0:
                        output_stream.write(struct.pack('<%ssx' % equipment_length, TAG.string_to_bytes(magazine_element.equipment.name, False)))

def write_new_triggers(output_stream, TAG, new_triggers, new_triggers_header):
    if len(new_triggers) > 0:
        new_triggers_header.write(output_stream, TAG, True)
        for new_trigger_element in new_triggers:
            output_stream.write(struct.pack('<I', new_trigger_element.flags))
            output_stream.write(struct.pack('<H', new_trigger_element.input_type))
            output_stream.write(struct.pack('<H', new_trigger_element.behavior))
            output_stream.write(struct.pack('<h', new_trigger_element.primary_barrel))
            output_stream.write(struct.pack('<h', new_trigger_element.secondary_barrel))
            output_stream.write(struct.pack('<H', new_trigger_element.prediction))
            output_stream.write(struct.pack('<2x'))
            output_stream.write(struct.pack('<f', new_trigger_element.autofire_time))
            output_stream.write(struct.pack('<f', new_trigger_element.autofire_throw))
            output_stream.write(struct.pack('<H', new_trigger_element.secondary_action))
            output_stream.write(struct.pack('<H', new_trigger_element.primary_action))
            output_stream.write(struct.pack('<f', new_trigger_element.charging_time))
            output_stream.write(struct.pack('<f', new_trigger_element.charged_time))
            output_stream.write(struct.pack('<H', new_trigger_element.overcharged_action))
            output_stream.write(struct.pack('<2x'))
            output_stream.write(struct.pack('<f', new_trigger_element.charged_illumination))
            output_stream.write(struct.pack('<f', new_trigger_element.spew_time))
            new_trigger_element.charging_effect.write(output_stream, False, True)
            new_trigger_element.charging_damage_effect.write(output_stream, False, True)

        for new_trigger_element in new_triggers:
            charging_effect_length = len(new_trigger_element.charging_effect.name)
            if charging_effect_length > 0:
                output_stream.write(struct.pack('<%ssx' % charging_effect_length, TAG.string_to_bytes(new_trigger_element.charging_effect.name, False)))

            charging_damage_effect_length = len(new_trigger_element.charging_damage_effect.name)
            if charging_damage_effect_length > 0:
                output_stream.write(struct.pack('<%ssx' % charging_damage_effect_length, TAG.string_to_bytes(new_trigger_element.charging_damage_effect.name, False)))

def write_barrels(output_stream, TAG, barrels, barrels_header):
    if len(barrels) > 0:
        barrels_header.write(output_stream, TAG, True)
        for barrel_element in barrels:
            output_stream.write(struct.pack('<I', barrel_element.flags))
            output_stream.write(struct.pack('<ff', *barrel_element.rounds_per_second))
            output_stream.write(struct.pack('<f', barrel_element.firing_acceleration_time))
            output_stream.write(struct.pack('<f', barrel_element.firing_deceleration_time))
            output_stream.write(struct.pack('<f', barrel_element.barrel_spin_scale))
            output_stream.write(struct.pack('<f', barrel_element.blurred_rate_of_fire))
            output_stream.write(struct.pack('<hh', *barrel_element.shots_per_fire))
            output_stream.write(struct.pack('<f', barrel_element.fire_recovery_time))
            output_stream.write(struct.pack('<f', barrel_element.soft_recovery_fraction))
            output_stream.write(struct.pack('<h', barrel_element.magazine))
            output_stream.write(struct.pack('<h', barrel_element.rounds_per_shot))
            output_stream.write(struct.pack('<h', barrel_element.minimum_rounds_loaded))
            output_stream.write(struct.pack('<h', barrel_element.rounds_between_tracers))
            output_stream.write(struct.pack('>I', len(barrel_element.optional_barrel_marker_name)))
            output_stream.write(struct.pack('<H', barrel_element.prediction_type))
            output_stream.write(struct.pack('<H', barrel_element.firing_noise))
            output_stream.write(struct.pack('<f', barrel_element.error_acceleration_time))
            output_stream.write(struct.pack('<f', barrel_element.error_deceleration_time))
            output_stream.write(struct.pack('<ff', *barrel_element.damage_error))
            output_stream.write(struct.pack('<f', barrel_element.dual_acceleration_time))
            output_stream.write(struct.pack('<f', barrel_element.dual_deceleration_time))
            output_stream.write(struct.pack('<8x'))
            output_stream.write(struct.pack('<f', radians(barrel_element.dual_minimum_error)))
            output_stream.write(struct.pack('<ff', radians(barrel_element.dual_error_angle[0]), radians(barrel_element.dual_error_angle[1])))
            output_stream.write(struct.pack('<f', barrel_element.dual_wield_damage_scale))
            output_stream.write(struct.pack('<H', barrel_element.distribution_function))
            output_stream.write(struct.pack('<h', barrel_element.projectiles_per_shot))
            output_stream.write(struct.pack('<f', barrel_element.distribution_angle))
            output_stream.write(struct.pack('<f', radians(barrel_element.projectile_minimum_error)))
            output_stream.write(struct.pack('<ff', radians(barrel_element.projectile_error_angle[0]), radians(barrel_element.projectile_error_angle[1])))
            output_stream.write(struct.pack('<fff', *barrel_element.first_person_offset))
            output_stream.write(struct.pack('<B', barrel_element.damage_effect_reporting_type))
            output_stream.write(struct.pack('<3x'))
            barrel_element.projectile.write(output_stream, False, True)
            barrel_element.damage_effect.write(output_stream, False, True)
            output_stream.write(struct.pack('<f', barrel_element.ejection_port_recovery_time))
            output_stream.write(struct.pack('<f', barrel_element.illumination_recovery_time))
            output_stream.write(struct.pack('<f', barrel_element.heat_generated_per_round))
            output_stream.write(struct.pack('<f', barrel_element.age_generated_per_round))
            output_stream.write(struct.pack('<f', barrel_element.overload_time))
            output_stream.write(struct.pack('<ff', radians(barrel_element.angle_change_per_shot[0]), radians(barrel_element.angle_change_per_shot[1])))
            output_stream.write(struct.pack('<f', barrel_element.recoil_acceleration_time))
            output_stream.write(struct.pack('<f', barrel_element.recoil_deceleration_time))
            output_stream.write(struct.pack('<H', barrel_element.angle_change_function))
            output_stream.write(struct.pack('<34x'))
            barrel_element.firing_effects_tag_block.write(output_stream, False)

        for barrel_element in barrels:
            optional_barrel_marker_name_length = len(barrel_element.optional_barrel_marker_name)
            if optional_barrel_marker_name_length > 0:
                output_stream.write(struct.pack('<%ss' % optional_barrel_marker_name_length, TAG.string_to_bytes(barrel_element.optional_barrel_marker_name, False)))

            projectile_length = len(barrel_element.projectile.name)
            if projectile_length > 0:
                output_stream.write(struct.pack('<%ssx' % projectile_length, TAG.string_to_bytes(barrel_element.projectile.name, False)))

            output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("wbde", True), 1, 1, 16))

            damage_effect_length = len(barrel_element.damage_effect.name)
            if damage_effect_length > 0:
                output_stream.write(struct.pack('<%ssx' % damage_effect_length, TAG.string_to_bytes(barrel_element.damage_effect.name, False)))

            if len(barrel_element.firing_effects) > 0:
                barrel_element.firing_effects_header.write(output_stream, TAG, True)
                for firing_effect_element in barrel_element.firing_effects:
                    output_stream.write(struct.pack('<h', firing_effect_element.shot_count_lower_bound))
                    output_stream.write(struct.pack('<h', firing_effect_element.shot_count_upper_bound))
                    firing_effect_element.firing_effect.write(output_stream, False, True)
                    firing_effect_element.misfire_effect.write(output_stream, False, True)
                    firing_effect_element.empty_effect.write(output_stream, False, True)
                    firing_effect_element.firing_damage.write(output_stream, False, True)
                    firing_effect_element.misfire_damage.write(output_stream, False, True)
                    firing_effect_element.empty_damage.write(output_stream, False, True)

                for firing_effect_element in barrel_element.firing_effects:
                    firing_effect_length = len(firing_effect_element.firing_effect.name)
                    if firing_effect_length > 0:
                        output_stream.write(struct.pack('<%ssx' % firing_effect_length, TAG.string_to_bytes(firing_effect_element.firing_effect.name, False)))

                    misfire_effect_length = len(firing_effect_element.misfire_effect.name)
                    if misfire_effect_length > 0:
                        output_stream.write(struct.pack('<%ssx' % misfire_effect_length, TAG.string_to_bytes(firing_effect_element.misfire_effect.name, False)))

                    empty_effect_length = len(firing_effect_element.empty_effect.name)
                    if empty_effect_length > 0:
                        output_stream.write(struct.pack('<%ssx' % empty_effect_length, TAG.string_to_bytes(firing_effect_element.empty_effect.name, False)))

                    firing_damage_length = len(firing_effect_element.firing_damage.name)
                    if firing_damage_length > 0:
                        output_stream.write(struct.pack('<%ssx' % firing_damage_length, TAG.string_to_bytes(firing_effect_element.firing_damage.name, False)))

                    misfire_damage_length = len(firing_effect_element.misfire_damage.name)
                    if misfire_damage_length > 0:
                        output_stream.write(struct.pack('<%ssx' % misfire_damage_length, TAG.string_to_bytes(firing_effect_element.misfire_damage.name, False)))

                    empty_damage_length = len(firing_effect_element.empty_damage.name)
                    if empty_damage_length > 0:
                        output_stream.write(struct.pack('<%ssx' % empty_damage_length, TAG.string_to_bytes(firing_effect_element.empty_damage.name, False)))

def build_asset(output_stream, WEAPON, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    WEAPON.header.write(output_stream, False, True)
    write_body(output_stream, TAG, WEAPON)

    default_model_variant_name_length = len(WEAPON.default_model_variant)
    if default_model_variant_name_length > 0:
        output_stream.write(struct.pack('<%ss' % default_model_variant_name_length, TAG.string_to_bytes(WEAPON.default_model_variant, False)))

    model_name_length = len(WEAPON.model.name)
    if model_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % model_name_length, TAG.string_to_bytes(WEAPON.model.name, False)))

    crate_object_name_length = len(WEAPON.crate_object.name)
    if crate_object_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % crate_object_name_length, TAG.string_to_bytes(WEAPON.crate_object.name, False)))

    modifier_shader_name_length = len(WEAPON.modifier_shader.name)
    if modifier_shader_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % modifier_shader_name_length, TAG.string_to_bytes(WEAPON.modifier_shader.name, False)))

    creation_effect_name_length = len(WEAPON.creation_effect.name)
    if creation_effect_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % creation_effect_name_length, TAG.string_to_bytes(WEAPON.creation_effect.name, False)))

    material_effects_name_length = len(WEAPON.material_effects.name)
    if material_effects_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % material_effects_name_length, TAG.string_to_bytes(WEAPON.material_effects.name, False)))

    write_ai_properties(output_stream, TAG, WEAPON.ai_properties, WEAPON.ai_properties_header)
    write_functions(output_stream, TAG, WEAPON.functions, WEAPON.functions_header)
    write_attachments(output_stream, TAG, WEAPON.attachments, WEAPON.attachments_header)
    write_tag_ref(output_stream, TAG, WEAPON.widgets, WEAPON.widgets_header)
    write_old_functions(output_stream, TAG, WEAPON.old_functions, WEAPON.old_functions_header)
    write_change_colors(output_stream, TAG, WEAPON.change_colors, WEAPON.change_colors_header)
    write_predicted_resources(output_stream, TAG, WEAPON.predicted_resources, WEAPON.predicted_resources_header)

    pickup_message_length = len(WEAPON.pickup_message)
    if pickup_message_length > 0:
        output_stream.write(struct.pack('<%ss' % pickup_message_length, TAG.string_to_bytes(WEAPON.pickup_message, False)))

    swap_message_length = len(WEAPON.swap_message)
    if swap_message_length > 0:
        output_stream.write(struct.pack('<%ss' % swap_message_length, TAG.string_to_bytes(WEAPON.swap_message, False)))

    pickup_or_dual_msg_length = len(WEAPON.pickup_or_dual_msg)
    if pickup_or_dual_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % pickup_or_dual_msg_length, TAG.string_to_bytes(WEAPON.pickup_or_dual_msg, False)))

    swap_or_dual_msg_length = len(WEAPON.swap_or_dual_msg)
    if swap_or_dual_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % swap_or_dual_msg_length, TAG.string_to_bytes(WEAPON.swap_or_dual_msg, False)))

    dual_only_msg_length = len(WEAPON.dual_only_msg)
    if dual_only_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % dual_only_msg_length, TAG.string_to_bytes(WEAPON.dual_only_msg, False)))

    picked_up_msg_length = len(WEAPON.picked_up_msg)
    if picked_up_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % picked_up_msg_length, TAG.string_to_bytes(WEAPON.picked_up_msg, False)))

    singluar_quantity_msg_length = len(WEAPON.singluar_quantity_msg)
    if singluar_quantity_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % singluar_quantity_msg_length, TAG.string_to_bytes(WEAPON.singluar_quantity_msg, False)))

    plural_quantity_msg_length = len(WEAPON.plural_quantity_msg)
    if plural_quantity_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % plural_quantity_msg_length, TAG.string_to_bytes(WEAPON.plural_quantity_msg, False)))

    switch_to_msg_length = len(WEAPON.switch_to_msg)
    if switch_to_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % switch_to_msg_length, TAG.string_to_bytes(WEAPON.switch_to_msg, False)))

    switch_to_from_ai_msg_length = len(WEAPON.switch_to_from_ai_msg)
    if switch_to_from_ai_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % switch_to_from_ai_msg_length, TAG.string_to_bytes(WEAPON.switch_to_from_ai_msg, False)))

    unused_length = len(WEAPON.unused.name)
    if unused_length > 0:
        output_stream.write(struct.pack('<%ssx' % unused_length, TAG.string_to_bytes(WEAPON.unused.name, False)))

    collision_sound_length = len(WEAPON.collision_sound.name)
    if collision_sound_length > 0:
        output_stream.write(struct.pack('<%ssx' % collision_sound_length, TAG.string_to_bytes(WEAPON.collision_sound.name, False)))

    write_predicted_bitmaps(output_stream, TAG, WEAPON.predicted_bitmaps, WEAPON.predicted_bitmaps_header)

    detonation_damage_effect_length = len(WEAPON.detonation_damage_effect.name)
    if detonation_damage_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % detonation_damage_effect_length, TAG.string_to_bytes(WEAPON.detonation_damage_effect.name, False)))

    detonating_effect_length = len(WEAPON.detonating_effect.name)
    if detonating_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % detonating_effect_length, TAG.string_to_bytes(WEAPON.detonating_effect.name, False)))

    detonation_effect_length = len(WEAPON.detonation_effect.name)
    if detonation_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % detonation_effect_length, TAG.string_to_bytes(WEAPON.detonation_effect.name, False)))

    unknown_length = len(WEAPON.unknown)
    if unknown_length > 0:
        output_stream.write(struct.pack('<%ss' % unknown_length, TAG.string_to_bytes(WEAPON.unknown, False)))

    ready_effect_length = len(WEAPON.ready_effect.name)
    if ready_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % ready_effect_length, TAG.string_to_bytes(WEAPON.ready_effect.name, False)))

    ready_damage_effect_length = len(WEAPON.ready_damage_effect.name)
    if ready_damage_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % ready_damage_effect_length, TAG.string_to_bytes(WEAPON.ready_damage_effect.name, False)))

    overheated_length = len(WEAPON.overheated.name)
    if overheated_length > 0:
        output_stream.write(struct.pack('<%ssx' % overheated_length, TAG.string_to_bytes(WEAPON.overheated.name, False)))

    overheated_damage_effect_length = len(WEAPON.overheated_damage_effect.name)
    if overheated_damage_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % overheated_damage_effect_length, TAG.string_to_bytes(WEAPON.overheated_damage_effect.name, False)))

    detonation_length = len(WEAPON.detonation.name)
    if detonation_length > 0:
        output_stream.write(struct.pack('<%ssx' % detonation_length, TAG.string_to_bytes(WEAPON.detonation.name, False)))

    weapon_detonation_damage_effect_length = len(WEAPON.weapon_detonation_damage_effect.name)
    if weapon_detonation_damage_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % weapon_detonation_damage_effect_length, TAG.string_to_bytes(WEAPON.weapon_detonation_damage_effect.name, False)))

    player_melee_damage_length = len(WEAPON.player_melee_damage.name)
    if player_melee_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % player_melee_damage_length, TAG.string_to_bytes(WEAPON.player_melee_damage.name, False)))

    player_melee_response_length = len(WEAPON.player_melee_response.name)
    if player_melee_response_length > 0:
        output_stream.write(struct.pack('<%ssx' % player_melee_response_length, TAG.string_to_bytes(WEAPON.player_melee_response.name, False)))

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("masd", True), 1, 1, 20))
    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("mdps", True), 1, 1, 140))

    first_hit_melee_damage_length = len(WEAPON.first_hit_melee_damage.name)
    if first_hit_melee_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % first_hit_melee_damage_length, TAG.string_to_bytes(WEAPON.first_hit_melee_damage.name, False)))

    first_hit_melee_response_length = len(WEAPON.first_hit_melee_response.name)
    if first_hit_melee_response_length > 0:
        output_stream.write(struct.pack('<%ssx' % first_hit_melee_response_length, TAG.string_to_bytes(WEAPON.first_hit_melee_response.name, False)))

    second_hit_melee_damage_length = len(WEAPON.second_hit_melee_damage.name)
    if second_hit_melee_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % second_hit_melee_damage_length, TAG.string_to_bytes(WEAPON.second_hit_melee_damage.name, False)))

    second_hit_melee_response_length = len(WEAPON.second_hit_melee_response.name)
    if second_hit_melee_response_length > 0:
        output_stream.write(struct.pack('<%ssx' % second_hit_melee_response_length, TAG.string_to_bytes(WEAPON.second_hit_melee_response.name, False)))

    third_hit_melee_damage_length = len(WEAPON.third_hit_melee_damage.name)
    if third_hit_melee_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % third_hit_melee_damage_length, TAG.string_to_bytes(WEAPON.third_hit_melee_damage.name, False)))

    third_hit_melee_response_length = len(WEAPON.third_hit_melee_response.name)
    if third_hit_melee_response_length > 0:
        output_stream.write(struct.pack('<%ssx' % third_hit_melee_response_length, TAG.string_to_bytes(WEAPON.third_hit_melee_response.name, False)))

    lunge_melee_damage_length = len(WEAPON.lunge_melee_damage.name)
    if lunge_melee_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % lunge_melee_damage_length, TAG.string_to_bytes(WEAPON.lunge_melee_damage.name, False)))

    lunge_melee_response_length = len(WEAPON.lunge_melee_response.name)
    if lunge_melee_response_length > 0:
        output_stream.write(struct.pack('<%ssx' % lunge_melee_response_length, TAG.string_to_bytes(WEAPON.lunge_melee_response.name, False)))

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("easd", True), 0, 1, 36))
    weapon_power_on_effect_length = len(WEAPON.weapon_power_on_effect.name)
    if weapon_power_on_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % weapon_power_on_effect_length, TAG.string_to_bytes(WEAPON.weapon_power_on_effect.name, False)))

    weapon_power_off_effect_length = len(WEAPON.weapon_power_off_effect.name)
    if weapon_power_off_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % weapon_power_off_effect_length, TAG.string_to_bytes(WEAPON.weapon_power_off_effect.name, False)))

    pickup_sound_length = len(WEAPON.pickup_sound.name)
    if pickup_sound_length > 0:
        output_stream.write(struct.pack('<%ssx' % pickup_sound_length, TAG.string_to_bytes(WEAPON.pickup_sound.name, False)))

    zoom_in_sound_length = len(WEAPON.zoom_in_sound.name)
    if zoom_in_sound_length > 0:
        output_stream.write(struct.pack('<%ssx' % zoom_in_sound_length, TAG.string_to_bytes(WEAPON.zoom_in_sound.name, False)))

    zoom_out_sound_length = len(WEAPON.zoom_out_sound.name)
    if zoom_out_sound_length > 0:
        output_stream.write(struct.pack('<%ssx' % zoom_out_sound_length, TAG.string_to_bytes(WEAPON.zoom_out_sound.name, False)))

    handle_node_length = len(WEAPON.handle_node)
    if handle_node_length > 0:
        output_stream.write(struct.pack('<%ss' % handle_node_length, TAG.string_to_bytes(WEAPON.handle_node, False)))

    weapon_class_length = len(WEAPON.weapon_class)
    if weapon_class_length > 0:
        output_stream.write(struct.pack('<%ss' % weapon_class_length, TAG.string_to_bytes(WEAPON.weapon_class, False)))

    weapon_name_length = len(WEAPON.weapon_name)
    if weapon_name_length > 0:
        output_stream.write(struct.pack('<%ss' % weapon_name_length, TAG.string_to_bytes(WEAPON.weapon_name, False)))

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("wtsf", True), 1, 1, 4))
    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("wItS", True), 0, 1, 44))
    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("wSiS", True), 0, 1, 16))

    write_first_person(output_stream, TAG, WEAPON.first_person, WEAPON.first_person_header)

    new_hud_interface_length = len(WEAPON.new_hud_interface.name)
    if new_hud_interface_length > 0:
        output_stream.write(struct.pack('<%ssx' % new_hud_interface_length, TAG.string_to_bytes(WEAPON.new_hud_interface.name, False)))

    write_magazines(output_stream, TAG, WEAPON.magazines, WEAPON.magazines_header)
    write_new_triggers(output_stream, TAG, WEAPON.new_triggers, WEAPON.new_triggers_header)
    write_barrels(output_stream, TAG, WEAPON.barrels, WEAPON.barrels_header)

    deployed_vehicle_length = len(WEAPON.deployed_vehicle.name)
    if deployed_vehicle_length > 0:
        output_stream.write(struct.pack('<%ssx' % deployed_vehicle_length, TAG.string_to_bytes(WEAPON.deployed_vehicle.name, False)))

    age_effect_length = len(WEAPON.age_effect.name)
    if age_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % age_effect_length, TAG.string_to_bytes(WEAPON.age_effect.name, False)))

    aged_weapon_length = len(WEAPON.aged_weapon.name)
    if aged_weapon_length > 0:
        output_stream.write(struct.pack('<%ssx' % aged_weapon_length, TAG.string_to_bytes(WEAPON.aged_weapon.name, False)))
