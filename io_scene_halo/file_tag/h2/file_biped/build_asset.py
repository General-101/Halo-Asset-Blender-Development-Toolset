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
from ....global_functions import tag_format
from ..file_object.build_asset import (
    write_ai_properties,
    write_functions,
    write_attachments,
    write_tag_ref,
    write_old_functions,
    write_change_colors,
    write_predicted_resources
    )
from ..file_unit.build_asset import (
    write_postures,
    write_dialogue_variant,
    write_powered_seats,
    write_seats
    )

def write_body(output_stream, TAG, BIPED):
    BIPED.body_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<H', 0))
    output_stream.write(struct.pack('<H', BIPED.object_flags))
    output_stream.write(struct.pack('<f', BIPED.bounding_radius))
    output_stream.write(struct.pack('<fff', *BIPED.bounding_offset))
    output_stream.write(struct.pack('<f', BIPED.acceleration_scale))
    output_stream.write(struct.pack('<h', BIPED.lightmap_shadow_mode))
    output_stream.write(struct.pack('<h', BIPED.sweetner_size))
    output_stream.write(struct.pack('<4x'))
    output_stream.write(struct.pack('<f', BIPED.dynamic_light_sphere_radius))
    output_stream.write(struct.pack('<fff', *BIPED.dynamic_light_sphere_offset))
    output_stream.write(struct.pack('>I', len(BIPED.default_model_variant)))
    BIPED.model.write(output_stream, False, True)
    BIPED.crate_object.write(output_stream, False, True)
    BIPED.modifier_shader.write(output_stream, False, True)
    BIPED.creation_effect.write(output_stream, False, True)
    BIPED.material_effects.write(output_stream, False, True)
    BIPED.ai_properties_tag_block.write(output_stream, False)
    BIPED.functions_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', BIPED.apply_collision_damage_scale))
    output_stream.write(struct.pack('<f', BIPED.min_game_acc))
    output_stream.write(struct.pack('<f', BIPED.max_game_acc))
    output_stream.write(struct.pack('<f', BIPED.min_game_scale))
    output_stream.write(struct.pack('<f', BIPED.max_game_scale))
    output_stream.write(struct.pack('<f', BIPED.min_abs_acc))
    output_stream.write(struct.pack('<f', BIPED.max_abs_acc))
    output_stream.write(struct.pack('<f', BIPED.min_abs_scale))
    output_stream.write(struct.pack('<f', BIPED.max_abs_scale))
    output_stream.write(struct.pack('<H', BIPED.hud_text_message_index))
    output_stream.write(struct.pack('<2x'))
    BIPED.attachments_tag_block.write(output_stream, False)
    BIPED.widgets_tag_block.write(output_stream, False)
    BIPED.old_functions_tag_block.write(output_stream, False)
    BIPED.change_colors_tag_block.write(output_stream, False)
    BIPED.predicted_resources_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<I', BIPED.unit_flags))
    output_stream.write(struct.pack('<H', BIPED.default_team))
    output_stream.write(struct.pack('<H', BIPED.constant_sound_volume))
    BIPED.integrated_light_toggle.write(output_stream, False, True)
    output_stream.write(struct.pack('<f', radians(BIPED.camera_field_of_view)))
    output_stream.write(struct.pack('<f', BIPED.camera_stiffness))
    output_stream.write(struct.pack('>I', len(BIPED.camera_marker_name)))
    output_stream.write(struct.pack('>I', len(BIPED.camera_submerged_marker_name)))
    output_stream.write(struct.pack('<f', radians(BIPED.pitch_auto_level)))
    output_stream.write(struct.pack('<ff', radians(BIPED.pitch_range[0]), radians(BIPED.pitch_range[1])))
    BIPED.camera_tracks_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<fff', *BIPED.acceleration_range))
    output_stream.write(struct.pack('<f', BIPED.acceleration_action_scale))
    output_stream.write(struct.pack('<f', BIPED.acceleration_attach_scale))
    output_stream.write(struct.pack('<f', BIPED.soft_ping_threshold))
    output_stream.write(struct.pack('<f', BIPED.soft_ping_interrupt_time))
    output_stream.write(struct.pack('<f', BIPED.hard_ping_threshold))
    output_stream.write(struct.pack('<f', BIPED.hard_ping_interrupt_time))
    output_stream.write(struct.pack('<f', BIPED.hard_death_threshold))
    output_stream.write(struct.pack('<f', BIPED.feign_death_threshold))
    output_stream.write(struct.pack('<f', BIPED.feign_death_time))
    output_stream.write(struct.pack('<f', BIPED.distance_of_evade_anim))
    output_stream.write(struct.pack('<f', BIPED.distance_of_dive_anim))
    output_stream.write(struct.pack('<f', BIPED.stunned_movement_threshold))
    output_stream.write(struct.pack('<f', BIPED.feign_death_chance))
    output_stream.write(struct.pack('<f', BIPED.feign_repeat_chance))
    BIPED.spawned_turret_actor.write(output_stream, False, True)
    output_stream.write(struct.pack('<hh', *BIPED.spawned_actor_count))
    output_stream.write(struct.pack('<f', BIPED.spawned_velocity))
    output_stream.write(struct.pack('<f', radians(BIPED.aiming_velocity_maximum)))
    output_stream.write(struct.pack('<f', radians(BIPED.aiming_acceleration_maximum)))
    output_stream.write(struct.pack('<f', BIPED.casual_aiming_modifier))
    output_stream.write(struct.pack('<f', radians(BIPED.looking_velocity_maximum)))
    output_stream.write(struct.pack('<f', radians(BIPED.looking_acceleration_maximum)))
    output_stream.write(struct.pack('>I', len(BIPED.right_hand_node)))
    output_stream.write(struct.pack('>I', len(BIPED.left_hand_node)))
    output_stream.write(struct.pack('>I', len(BIPED.preferred_gun_node)))
    BIPED.melee_damage.write(output_stream, False, True)
    BIPED.boarding_melee_damage.write(output_stream, False, True)
    BIPED.boarding_melee_response.write(output_stream, False, True)
    BIPED.landing_melee_damage.write(output_stream, False, True)
    BIPED.flurry_melee_damage.write(output_stream, False, True)
    BIPED.obstacle_smash_damage.write(output_stream, False, True)
    output_stream.write(struct.pack('<H', BIPED.motion_sensor_blip_size))
    output_stream.write(struct.pack('<B', BIPED.unit_type))
    output_stream.write(struct.pack('<B', BIPED.unit_class))
    BIPED.postures_tag_block.write(output_stream, False)
    BIPED.new_hud_interfaces_tag_block.write(output_stream, False)
    BIPED.dialogue_variants_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', BIPED.grenade_velocity))
    output_stream.write(struct.pack('<H', BIPED.grenade_type))
    output_stream.write(struct.pack('<h', BIPED.grenade_count))
    BIPED.powered_seats_tag_block.write(output_stream, False)
    BIPED.weapons_tag_block.write(output_stream, False)
    BIPED.seats_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', BIPED.boost_peak_power))
    output_stream.write(struct.pack('<f', BIPED.boost_rise_power))
    output_stream.write(struct.pack('<f', BIPED.boost_peak_time))
    output_stream.write(struct.pack('<f', BIPED.boost_fall_power))
    output_stream.write(struct.pack('<f', BIPED.dead_time))
    output_stream.write(struct.pack('<f', BIPED.attack_weight))
    output_stream.write(struct.pack('<f', BIPED.decay_weight))
    output_stream.write(struct.pack('<f', radians(BIPED.moving_turning_speed)))
    output_stream.write(struct.pack('<I', BIPED.biped_flags))
    output_stream.write(struct.pack('<f', radians(BIPED.stationary_turning_threshold)))
    output_stream.write(struct.pack('<f', BIPED.jump_velocity))
    output_stream.write(struct.pack('<f', BIPED.maximum_soft_landing_time))
    output_stream.write(struct.pack('<f', BIPED.maximum_hard_landing_time))
    output_stream.write(struct.pack('<f', BIPED.minimum_soft_landing_velocity))
    output_stream.write(struct.pack('<f', BIPED.minimum_hard_landing_velocity))
    output_stream.write(struct.pack('<f', BIPED.maximum_hard_landing_velocity))
    output_stream.write(struct.pack('<f', BIPED.death_hard_landing_velocity))
    output_stream.write(struct.pack('<f', BIPED.stun_duration))
    output_stream.write(struct.pack('<f', BIPED.standing_camera_height))
    output_stream.write(struct.pack('<f', BIPED.crouching_camera_height))
    output_stream.write(struct.pack('<f', BIPED.crouching_transition_time))
    output_stream.write(struct.pack('<f', radians(BIPED.camera_interpolation_start)))
    output_stream.write(struct.pack('<f', radians(BIPED.camera_interpolation_end)))
    output_stream.write(struct.pack('<f', BIPED.camera_forward_movement_scale))
    output_stream.write(struct.pack('<f', BIPED.camera_side_movement_scale))
    output_stream.write(struct.pack('<f', BIPED.camera_vertical_movement_scale))
    output_stream.write(struct.pack('<f', BIPED.camera_exclusion_distance))
    output_stream.write(struct.pack('<f', BIPED.autoaim_width))
    output_stream.write(struct.pack('<I', BIPED.lock_on_flags))
    output_stream.write(struct.pack('<f', BIPED.lock_on_distance))
    output_stream.write(struct.pack('<16x'))
    output_stream.write(struct.pack('<f', BIPED.head_shot_acceleration_scale))
    BIPED.area_damage_effect.write(output_stream, False, True)
    output_stream.write(struct.pack('<I', BIPED.collision_flags))
    output_stream.write(struct.pack('<f', BIPED.height_standing))
    output_stream.write(struct.pack('<f', BIPED.height_crouching))
    output_stream.write(struct.pack('<f', BIPED.radius))
    output_stream.write(struct.pack('<f', BIPED.mass))
    output_stream.write(struct.pack('>I', len(BIPED.living_material_name)))
    output_stream.write(struct.pack('>I', len(BIPED.dead_material_name)))
    output_stream.write(struct.pack('<4x'))
    BIPED.dead_sphere_shapes_tag_block.write(output_stream, False)
    BIPED.pill_shapes_tag_block.write(output_stream, False)
    BIPED.sphere_shapes_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', radians(BIPED.maximum_slope_angle)))
    output_stream.write(struct.pack('<f', radians(BIPED.downhill_falloff_angle)))
    output_stream.write(struct.pack('<f', radians(BIPED.downhill_cuttoff_angle)))
    output_stream.write(struct.pack('<f', radians(BIPED.uphill_falloff_angle)))
    output_stream.write(struct.pack('<f', radians(BIPED.uphill_cuttoff_angle)))
    output_stream.write(struct.pack('<f', BIPED.downhill_velocity_scale))
    output_stream.write(struct.pack('<f', BIPED.uphill_velocity_scale))
    output_stream.write(struct.pack('<20x'))
    output_stream.write(struct.pack('<f', radians(BIPED.bank_angle)))
    output_stream.write(struct.pack('<f', BIPED.bank_apply_time))
    output_stream.write(struct.pack('<f', BIPED.bank_decay_time))
    output_stream.write(struct.pack('<f', BIPED.pitch_ratio))
    output_stream.write(struct.pack('<f', BIPED.max_velocity))
    output_stream.write(struct.pack('<f', BIPED.max_sidestep_velocity))
    output_stream.write(struct.pack('<f', BIPED.acceleration))
    output_stream.write(struct.pack('<f', BIPED.deceleration))
    output_stream.write(struct.pack('<f', radians(BIPED.angular_velocity_maximum)))
    output_stream.write(struct.pack('<f', radians(BIPED.angular_acceleration_maximum)))
    output_stream.write(struct.pack('<f', BIPED.crouch_velocity_modifier))
    BIPED.contact_points_tag_block.write(output_stream, False)
    BIPED.reanimation_character.write(output_stream, False, True)
    BIPED.death_spawn_character.write(output_stream, False, True)
    output_stream.write(struct.pack('<h', BIPED.death_spawn_count))
    output_stream.write(struct.pack('<2x'))

def write_sphere_shapes(output_stream, TAG, dead_sphere_shapes, dead_sphere_shapes_header):
    if len(dead_sphere_shapes) > 0:
        dead_sphere_shapes_header.write(output_stream, TAG, True)
        for dead_sphere_shape_element in dead_sphere_shapes:
            output_stream.write(struct.pack('>I', len(dead_sphere_shape_element.name)))
            output_stream.write(struct.pack('<h', dead_sphere_shape_element.material))
            output_stream.write(struct.pack('<H', dead_sphere_shape_element.flags))
            output_stream.write(struct.pack('<f', dead_sphere_shape_element.relative_mass_scale))
            output_stream.write(struct.pack('<f', dead_sphere_shape_element.friction))
            output_stream.write(struct.pack('<f', dead_sphere_shape_element.restitution))
            output_stream.write(struct.pack('<f', dead_sphere_shape_element.volume))
            output_stream.write(struct.pack('<f', dead_sphere_shape_element.mass))
            output_stream.write(struct.pack('<2x'))
            output_stream.write(struct.pack('<h', dead_sphere_shape_element.phantom))
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('<h', dead_sphere_shape_element.size_a))
            output_stream.write(struct.pack('<h', dead_sphere_shape_element.count_a))
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('<f', dead_sphere_shape_element.radius))
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('<h', dead_sphere_shape_element.size_b))
            output_stream.write(struct.pack('<h', dead_sphere_shape_element.count_b))
            output_stream.write(struct.pack('<8x'))
            output_stream.write(struct.pack('<fff', *dead_sphere_shape_element.rotation_i))
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('<fff', *dead_sphere_shape_element.rotation_j))
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('<fff', *dead_sphere_shape_element.rotation_k))
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('<fff', *dead_sphere_shape_element.translation))
            output_stream.write(struct.pack('<4x'))

        for dead_sphere_shape_element in dead_sphere_shapes:
            name_length = len(dead_sphere_shape_element.name)
            if name_length > 0:
                output_stream.write(struct.pack('<%ss' % name_length, TAG.string_to_bytes(dead_sphere_shape_element.name, False)))

def write_pill_shapes(output_stream, TAG, pill_shapes, pill_shapes_header):
    if len(pill_shapes) > 0:
        pill_shapes_header.write(output_stream, TAG, True)
        for pill_shape_element in pill_shapes:
            output_stream.write(struct.pack('>I', len(pill_shape_element.name)))
            output_stream.write(struct.pack('<h', pill_shape_element.material))
            output_stream.write(struct.pack('<H', pill_shape_element.flags))
            output_stream.write(struct.pack('<f', pill_shape_element.relative_mass_scale))
            output_stream.write(struct.pack('<f', pill_shape_element.friction))
            output_stream.write(struct.pack('<f', pill_shape_element.restitution))
            output_stream.write(struct.pack('<f', pill_shape_element.volume))
            output_stream.write(struct.pack('<f', pill_shape_element.mass))
            output_stream.write(struct.pack('<2x'))
            output_stream.write(struct.pack('<h', pill_shape_element.phantom))
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('<h', pill_shape_element.size_a))
            output_stream.write(struct.pack('<h', pill_shape_element.count_a))
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('<f', pill_shape_element.radius))
            output_stream.write(struct.pack('<fff', *pill_shape_element.bottom))
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('<fff', *pill_shape_element.top))
            output_stream.write(struct.pack('<4x'))

        for pill_shape_element in pill_shapes:
            name_length = len(pill_shape_element.name)
            if name_length > 0:
                output_stream.write(struct.pack('<%ss' % name_length, TAG.string_to_bytes(pill_shape_element.name, False)))

def write_contact_points(output_stream, TAG, contact_points, contact_points_header):
    if len(contact_points) > 0:
        contact_points_header.write(output_stream, TAG, True)
        for contact_point_element in contact_points:
            output_stream.write(struct.pack('>I', len(contact_point_element.name)))

        for contact_point_element in contact_points:
            name_length = len(contact_point_element.name)
            if name_length > 0:
                output_stream.write(struct.pack('<%ss' % name_length, TAG.string_to_bytes(contact_point_element.name, False)))

def build_asset(output_stream, BIPED, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    BIPED.header.write(output_stream, False, True)
    write_body(output_stream, TAG, BIPED)

    default_model_variant_name_length = len(BIPED.default_model_variant)
    if default_model_variant_name_length > 0:
        output_stream.write(struct.pack('<%ss' % default_model_variant_name_length, TAG.string_to_bytes(BIPED.default_model_variant, False)))

    model_name_length = len(BIPED.model.name)
    if model_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % model_name_length, TAG.string_to_bytes(BIPED.model.name, False)))

    crate_object_name_length = len(BIPED.crate_object.name)
    if crate_object_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % crate_object_name_length, TAG.string_to_bytes(BIPED.crate_object.name, False)))

    modifier_shader_name_length = len(BIPED.modifier_shader.name)
    if modifier_shader_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % modifier_shader_name_length, TAG.string_to_bytes(BIPED.modifier_shader.name, False)))

    creation_effect_name_length = len(BIPED.creation_effect.name)
    if creation_effect_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % creation_effect_name_length, TAG.string_to_bytes(BIPED.creation_effect.name, False)))

    material_effects_name_length = len(BIPED.material_effects.name)
    if material_effects_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % material_effects_name_length, TAG.string_to_bytes(BIPED.material_effects.name, False)))

    write_ai_properties(output_stream, TAG, BIPED.ai_properties, BIPED.ai_properties_header)
    write_functions(output_stream, TAG, BIPED.functions, BIPED.functions_header)
    write_attachments(output_stream, TAG, BIPED.attachments, BIPED.attachments_header)
    write_tag_ref(output_stream, TAG, BIPED.widgets, BIPED.widgets_header)
    write_old_functions(output_stream, TAG, BIPED.old_functions, BIPED.old_functions_header)
    write_change_colors(output_stream, TAG, BIPED.change_colors, BIPED.change_colors_header)
    write_predicted_resources(output_stream, TAG, BIPED.predicted_resources, BIPED.predicted_resources_header)

    integrated_light_toggle_length = len(BIPED.integrated_light_toggle.name)
    if integrated_light_toggle_length > 0:
        output_stream.write(struct.pack('<%ssx' % integrated_light_toggle_length, TAG.string_to_bytes(BIPED.integrated_light_toggle.name, False)))

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("uncs", True), 0, 1, 32))

    camera_marker_name_length = len(BIPED.camera_marker_name)
    if camera_marker_name_length > 0:
        output_stream.write(struct.pack('<%ss' % camera_marker_name_length, TAG.string_to_bytes(BIPED.camera_marker_name, False)))

    camera_submerged_marker_name_length = len(BIPED.camera_submerged_marker_name)
    if camera_submerged_marker_name_length > 0:
        output_stream.write(struct.pack('<%ss' % camera_submerged_marker_name_length, TAG.string_to_bytes(BIPED.camera_submerged_marker_name, False)))

    write_tag_ref(output_stream, TAG, BIPED.camera_tracks, BIPED.camera_tracks_header)

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("usas", True), 0, 1, 20))

    spawned_turret_actor_length = len(BIPED.spawned_turret_actor.name)
    if spawned_turret_actor_length > 0:
        output_stream.write(struct.pack('<%ssx' % spawned_turret_actor_length, TAG.string_to_bytes(BIPED.spawned_turret_actor.name, False)))

    right_hand_node_length = len(BIPED.right_hand_node)
    if right_hand_node_length > 0:
        output_stream.write(struct.pack('<%ss' % right_hand_node_length, TAG.string_to_bytes(BIPED.right_hand_node, False)))

    left_hand_node_length = len(BIPED.left_hand_node)
    if left_hand_node_length > 0:
        output_stream.write(struct.pack('<%ss' % left_hand_node_length, TAG.string_to_bytes(BIPED.left_hand_node, False)))

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("uHnd", True), 1, 1, 4))

    preferred_gun_node_length = len(BIPED.preferred_gun_node)
    if preferred_gun_node_length > 0:
        output_stream.write(struct.pack('<%ss' % preferred_gun_node_length, TAG.string_to_bytes(BIPED.preferred_gun_node, False)))

    melee_damage_length = len(BIPED.melee_damage.name)
    if melee_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % melee_damage_length, TAG.string_to_bytes(BIPED.melee_damage.name, False)))

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("ubms", True), 1, 1, 80))

    boarding_melee_damage_length = len(BIPED.boarding_melee_damage.name)
    if boarding_melee_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % boarding_melee_damage_length, TAG.string_to_bytes(BIPED.boarding_melee_damage.name, False)))

    boarding_melee_response_length = len(BIPED.boarding_melee_response.name)
    if boarding_melee_response_length > 0:
        output_stream.write(struct.pack('<%ssx' % boarding_melee_response_length, TAG.string_to_bytes(BIPED.boarding_melee_response.name, False)))

    landing_melee_damage_length = len(BIPED.landing_melee_damage.name)
    if landing_melee_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % landing_melee_damage_length, TAG.string_to_bytes(BIPED.landing_melee_damage.name, False)))

    flurry_melee_damage_length = len(BIPED.flurry_melee_damage.name)
    if flurry_melee_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % flurry_melee_damage_length, TAG.string_to_bytes(BIPED.flurry_melee_damage.name, False)))

    obstacle_smash_damage_length = len(BIPED.obstacle_smash_damage.name)
    if obstacle_smash_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % obstacle_smash_damage_length, TAG.string_to_bytes(BIPED.obstacle_smash_damage.name, False)))

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("cmtb", True), 0, 1, 2))

    write_postures(output_stream, TAG, BIPED.postures, BIPED.postures_header)
    write_tag_ref(output_stream, TAG, BIPED.new_hud_interface, BIPED.new_hud_interface_header)
    write_dialogue_variant(output_stream, TAG, BIPED.dialogue_variants, BIPED.dialogue_variants_header)
    write_powered_seats(output_stream, TAG, BIPED.powered_seats, BIPED.powered_seats_header)
    write_tag_ref(output_stream, TAG, BIPED.weapons, BIPED.weapons_header)
    write_seats(output_stream, TAG, BIPED.seats, BIPED.seats_header)

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("!@#$", True), 0, 1, 20))
    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("ulYc", True), 1, 1, 8))
    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("blod", True), 1, 1, 8))

    area_damage_effect_length = len(BIPED.area_damage_effect.name)
    if area_damage_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % area_damage_effect_length, TAG.string_to_bytes(BIPED.area_damage_effect.name, False)))

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("chpy", True), 0, 1, 160))

    living_material_name_length = len(BIPED.living_material_name)
    if living_material_name_length > 0:
        output_stream.write(struct.pack('<%ss' % living_material_name_length, TAG.string_to_bytes(BIPED.living_material_name, False)))

    dead_material_name_length = len(BIPED.dead_material_name)
    if dead_material_name_length > 0:
        output_stream.write(struct.pack('<%ss' % dead_material_name_length, TAG.string_to_bytes(BIPED.dead_material_name, False)))

    write_sphere_shapes(output_stream, TAG, BIPED.dead_sphere_shapes, BIPED.dead_sphere_shapes_header)
    write_pill_shapes(output_stream, TAG, BIPED.pill_shapes, BIPED.pill_shapes_header)
    write_sphere_shapes(output_stream, TAG, BIPED.sphere_shapes, BIPED.sphere_shapes_header)

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("chgr", True), 0, 1, 48))
    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("chfl", True), 0, 1, 44))
    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("chdd", True), 0, 1, 0))
    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("chsn", True), 0, 1, 0))

    write_contact_points(output_stream, TAG, BIPED.contact_points, BIPED.contact_points_header)

    reanimation_character_length = len(BIPED.reanimation_character.name)
    if reanimation_character_length > 0:
        output_stream.write(struct.pack('<%ssx' % reanimation_character_length, TAG.string_to_bytes(BIPED.reanimation_character.name, False)))

    death_spawn_character_length = len(BIPED.death_spawn_character.name)
    if death_spawn_character_length > 0:
        output_stream.write(struct.pack('<%ssx' % death_spawn_character_length, TAG.string_to_bytes(BIPED.death_spawn_character.name, False)))
