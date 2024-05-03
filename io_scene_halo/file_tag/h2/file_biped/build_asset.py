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
from ..file_unit.build_asset import (
    write_postures,
    write_dialogue_variant,
    write_powered_seats,
    write_seats
    )

def write_body(output_stream, TAG, BIPED):
    BIPED.biped_body_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<H', 0))
    output_stream.write(struct.pack('<H', BIPED.biped_body.object_flags))
    output_stream.write(struct.pack('<f', BIPED.biped_body.bounding_radius))
    output_stream.write(struct.pack('<fff', *BIPED.biped_body.bounding_offset))
    output_stream.write(struct.pack('<f', BIPED.biped_body.acceleration_scale))
    output_stream.write(struct.pack('<h', BIPED.biped_body.lightmap_shadow_mode))
    output_stream.write(struct.pack('<h', BIPED.biped_body.sweetner_size))
    output_stream.write(struct.pack('<4x'))
    output_stream.write(struct.pack('<f', BIPED.biped_body.dynamic_light_sphere_radius))
    output_stream.write(struct.pack('<fff', *BIPED.biped_body.dynamic_light_sphere_offset))
    output_stream.write(struct.pack('>I', len(BIPED.biped_body.default_model_variant)))
    BIPED.biped_body.model.write(output_stream, False, True)
    BIPED.biped_body.crate_object.write(output_stream, False, True)
    BIPED.biped_body.modifier_shader.write(output_stream, False, True)
    BIPED.biped_body.creation_effect.write(output_stream, False, True)
    BIPED.biped_body.material_effects.write(output_stream, False, True)
    BIPED.biped_body.ai_properties_tag_block.write(output_stream, False)
    BIPED.biped_body.functions_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', BIPED.biped_body.apply_collision_damage_scale))
    output_stream.write(struct.pack('<f', BIPED.biped_body.min_game_acc))
    output_stream.write(struct.pack('<f', BIPED.biped_body.max_game_acc))
    output_stream.write(struct.pack('<f', BIPED.biped_body.min_game_scale))
    output_stream.write(struct.pack('<f', BIPED.biped_body.max_game_scale))
    output_stream.write(struct.pack('<f', BIPED.biped_body.min_abs_acc))
    output_stream.write(struct.pack('<f', BIPED.biped_body.max_abs_acc))
    output_stream.write(struct.pack('<f', BIPED.biped_body.min_abs_scale))
    output_stream.write(struct.pack('<f', BIPED.biped_body.max_abs_scale))
    output_stream.write(struct.pack('<H', BIPED.biped_body.hud_text_message_index))
    output_stream.write(struct.pack('<2x'))
    BIPED.biped_body.attachments_tag_block.write(output_stream, False)
    BIPED.biped_body.widgets_tag_block.write(output_stream, False)
    BIPED.biped_body.old_functions_tag_block.write(output_stream, False)
    BIPED.biped_body.change_colors_tag_block.write(output_stream, False)
    BIPED.biped_body.predicted_resources_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<I', BIPED.biped_body.unit_flags))
    output_stream.write(struct.pack('<H', BIPED.biped_body.default_team))
    output_stream.write(struct.pack('<H', BIPED.biped_body.constant_sound_volume))
    BIPED.biped_body.integrated_light_toggle.write(output_stream, False, True)
    output_stream.write(struct.pack('<f', radians(BIPED.biped_body.camera_field_of_view)))
    output_stream.write(struct.pack('<f', BIPED.biped_body.camera_stiffness))
    output_stream.write(struct.pack('>I', len(BIPED.biped_body.camera_marker_name)))
    output_stream.write(struct.pack('>I', len(BIPED.biped_body.camera_submerged_marker_name)))
    output_stream.write(struct.pack('<f', radians(BIPED.biped_body.pitch_auto_level)))
    output_stream.write(struct.pack('<ff', radians(BIPED.biped_body.pitch_range[0]), radians(BIPED.biped_body.pitch_range[1])))
    BIPED.biped_body.camera_tracks_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<fff', *BIPED.biped_body.acceleration_range))
    output_stream.write(struct.pack('<f', BIPED.biped_body.acceleration_action_scale))
    output_stream.write(struct.pack('<f', BIPED.biped_body.acceleration_attach_scale))
    output_stream.write(struct.pack('<f', BIPED.biped_body.soft_ping_threshold))
    output_stream.write(struct.pack('<f', BIPED.biped_body.soft_ping_interrupt_time))
    output_stream.write(struct.pack('<f', BIPED.biped_body.hard_ping_threshold))
    output_stream.write(struct.pack('<f', BIPED.biped_body.hard_ping_interrupt_time))
    output_stream.write(struct.pack('<f', BIPED.biped_body.hard_death_threshold))
    output_stream.write(struct.pack('<f', BIPED.biped_body.feign_death_threshold))
    output_stream.write(struct.pack('<f', BIPED.biped_body.feign_death_time))
    output_stream.write(struct.pack('<f', BIPED.biped_body.distance_of_evade_anim))
    output_stream.write(struct.pack('<f', BIPED.biped_body.distance_of_dive_anim))
    output_stream.write(struct.pack('<f', BIPED.biped_body.stunned_movement_threshold))
    output_stream.write(struct.pack('<f', BIPED.biped_body.feign_death_chance))
    output_stream.write(struct.pack('<f', BIPED.biped_body.feign_repeat_chance))
    BIPED.biped_body.spawned_turret_actor.write(output_stream, False, True)
    output_stream.write(struct.pack('<hh', *BIPED.biped_body.spawned_actor_count))
    output_stream.write(struct.pack('<f', BIPED.biped_body.spawned_velocity))
    output_stream.write(struct.pack('<f', radians(BIPED.biped_body.aiming_velocity_maximum)))
    output_stream.write(struct.pack('<f', radians(BIPED.biped_body.aiming_acceleration_maximum)))
    output_stream.write(struct.pack('<f', BIPED.biped_body.casual_aiming_modifier))
    output_stream.write(struct.pack('<f', radians(BIPED.biped_body.looking_velocity_maximum)))
    output_stream.write(struct.pack('<f', radians(BIPED.biped_body.looking_acceleration_maximum)))
    output_stream.write(struct.pack('>I', len(BIPED.biped_body.right_hand_node)))
    output_stream.write(struct.pack('>I', len(BIPED.biped_body.left_hand_node)))
    output_stream.write(struct.pack('>I', len(BIPED.biped_body.preferred_gun_node)))
    BIPED.biped_body.melee_damage.write(output_stream, False, True)
    BIPED.biped_body.boarding_melee_damage.write(output_stream, False, True)
    BIPED.biped_body.boarding_melee_response.write(output_stream, False, True)
    BIPED.biped_body.landing_melee_damage.write(output_stream, False, True)
    BIPED.biped_body.flurry_melee_damage.write(output_stream, False, True)
    BIPED.biped_body.obstacle_smash_damage.write(output_stream, False, True)
    output_stream.write(struct.pack('<H', BIPED.biped_body.motion_sensor_blip_size))
    output_stream.write(struct.pack('<B', BIPED.biped_body.unit_type))
    output_stream.write(struct.pack('<B', BIPED.biped_body.unit_class))
    BIPED.biped_body.postures_tag_block.write(output_stream, False)
    BIPED.biped_body.new_hud_interfaces_tag_block.write(output_stream, False)
    BIPED.biped_body.dialogue_variants_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', BIPED.biped_body.grenade_velocity))
    output_stream.write(struct.pack('<H', BIPED.biped_body.grenade_type))
    output_stream.write(struct.pack('<h', BIPED.biped_body.grenade_count))
    BIPED.biped_body.powered_seats_tag_block.write(output_stream, False)
    BIPED.biped_body.weapons_tag_block.write(output_stream, False)
    BIPED.biped_body.seats_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', BIPED.biped_body.boost_peak_power))
    output_stream.write(struct.pack('<f', BIPED.biped_body.boost_rise_power))
    output_stream.write(struct.pack('<f', BIPED.biped_body.boost_peak_time))
    output_stream.write(struct.pack('<f', BIPED.biped_body.boost_fall_power))
    output_stream.write(struct.pack('<f', BIPED.biped_body.dead_time))
    output_stream.write(struct.pack('<f', BIPED.biped_body.attack_weight))
    output_stream.write(struct.pack('<f', BIPED.biped_body.decay_weight))
    output_stream.write(struct.pack('<f', radians(BIPED.biped_body.moving_turning_speed)))
    output_stream.write(struct.pack('<I', BIPED.biped_body.biped_flags))
    output_stream.write(struct.pack('<f', radians(BIPED.biped_body.stationary_turning_threshold)))
    output_stream.write(struct.pack('<f', BIPED.biped_body.jump_velocity))
    output_stream.write(struct.pack('<f', BIPED.biped_body.maximum_soft_landing_time))
    output_stream.write(struct.pack('<f', BIPED.biped_body.maximum_hard_landing_time))
    output_stream.write(struct.pack('<f', BIPED.biped_body.minimum_soft_landing_velocity))
    output_stream.write(struct.pack('<f', BIPED.biped_body.minimum_hard_landing_velocity))
    output_stream.write(struct.pack('<f', BIPED.biped_body.maximum_hard_landing_velocity))
    output_stream.write(struct.pack('<f', BIPED.biped_body.death_hard_landing_velocity))
    output_stream.write(struct.pack('<f', BIPED.biped_body.stun_duration))
    output_stream.write(struct.pack('<f', BIPED.biped_body.standing_camera_height))
    output_stream.write(struct.pack('<f', BIPED.biped_body.crouching_camera_height))
    output_stream.write(struct.pack('<f', BIPED.biped_body.crouching_transition_time))
    output_stream.write(struct.pack('<f', radians(BIPED.biped_body.camera_interpolation_start)))
    output_stream.write(struct.pack('<f', radians(BIPED.biped_body.camera_interpolation_end)))
    output_stream.write(struct.pack('<f', BIPED.biped_body.camera_forward_movement_scale))
    output_stream.write(struct.pack('<f', BIPED.biped_body.camera_side_movement_scale))
    output_stream.write(struct.pack('<f', BIPED.biped_body.camera_vertical_movement_scale))
    output_stream.write(struct.pack('<f', BIPED.biped_body.camera_exclusion_distance))
    output_stream.write(struct.pack('<f', BIPED.biped_body.autoaim_width))
    output_stream.write(struct.pack('<I', BIPED.biped_body.lock_on_flags))
    output_stream.write(struct.pack('<f', BIPED.biped_body.lock_on_distance))
    output_stream.write(struct.pack('<16x'))
    output_stream.write(struct.pack('<f', BIPED.biped_body.head_shot_acceleration_scale))
    BIPED.biped_body.area_damage_effect.write(output_stream, False, True)
    output_stream.write(struct.pack('<I', BIPED.biped_body.collision_flags))
    output_stream.write(struct.pack('<f', BIPED.biped_body.height_standing))
    output_stream.write(struct.pack('<f', BIPED.biped_body.height_crouching))
    output_stream.write(struct.pack('<f', BIPED.biped_body.radius))
    output_stream.write(struct.pack('<f', BIPED.biped_body.mass))
    output_stream.write(struct.pack('>I', len(BIPED.biped_body.living_material_name)))
    output_stream.write(struct.pack('>I', len(BIPED.biped_body.dead_material_name)))
    output_stream.write(struct.pack('<4x'))
    BIPED.biped_body.dead_sphere_shapes_tag_block.write(output_stream, False)
    BIPED.biped_body.pill_shapes_tag_block.write(output_stream, False)
    BIPED.biped_body.sphere_shapes_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', radians(BIPED.biped_body.maximum_slope_angle)))
    output_stream.write(struct.pack('<f', radians(BIPED.biped_body.downhill_falloff_angle)))
    output_stream.write(struct.pack('<f', radians(BIPED.biped_body.downhill_cuttoff_angle)))
    output_stream.write(struct.pack('<f', radians(BIPED.biped_body.uphill_falloff_angle)))
    output_stream.write(struct.pack('<f', radians(BIPED.biped_body.uphill_cuttoff_angle)))
    output_stream.write(struct.pack('<f', BIPED.biped_body.downhill_velocity_scale))
    output_stream.write(struct.pack('<f', BIPED.biped_body.uphill_velocity_scale))
    output_stream.write(struct.pack('<20x'))
    output_stream.write(struct.pack('<f', radians(BIPED.biped_body.bank_angle)))
    output_stream.write(struct.pack('<f', BIPED.biped_body.bank_apply_time))
    output_stream.write(struct.pack('<f', BIPED.biped_body.bank_decay_time))
    output_stream.write(struct.pack('<f', BIPED.biped_body.pitch_ratio))
    output_stream.write(struct.pack('<f', BIPED.biped_body.max_velocity))
    output_stream.write(struct.pack('<f', BIPED.biped_body.max_sidestep_velocity))
    output_stream.write(struct.pack('<f', BIPED.biped_body.acceleration))
    output_stream.write(struct.pack('<f', BIPED.biped_body.deceleration))
    output_stream.write(struct.pack('<f', radians(BIPED.biped_body.angular_velocity_maximum)))
    output_stream.write(struct.pack('<f', radians(BIPED.biped_body.angular_acceleration_maximum)))
    output_stream.write(struct.pack('<f', BIPED.biped_body.crouch_velocity_modifier))
    BIPED.biped_body.contact_points_tag_block.write(output_stream, False)
    BIPED.biped_body.reanimation_character.write(output_stream, False, True)
    BIPED.biped_body.death_spawn_character.write(output_stream, False, True)
    output_stream.write(struct.pack('<h', BIPED.biped_body.death_spawn_count))
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

    default_model_variant_name_length = len(BIPED.biped_body.default_model_variant)
    if default_model_variant_name_length > 0:
        output_stream.write(struct.pack('<%ss' % default_model_variant_name_length, TAG.string_to_bytes(BIPED.biped_body.default_model_variant, False)))

    model_name_length = len(BIPED.biped_body.model.name)
    if model_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % model_name_length, TAG.string_to_bytes(BIPED.biped_body.model.name, False)))

    crate_object_name_length = len(BIPED.biped_body.crate_object.name)
    if crate_object_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % crate_object_name_length, TAG.string_to_bytes(BIPED.biped_body.crate_object.name, False)))

    modifier_shader_name_length = len(BIPED.biped_body.modifier_shader.name)
    if modifier_shader_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % modifier_shader_name_length, TAG.string_to_bytes(BIPED.biped_body.modifier_shader.name, False)))

    creation_effect_name_length = len(BIPED.biped_body.creation_effect.name)
    if creation_effect_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % creation_effect_name_length, TAG.string_to_bytes(BIPED.biped_body.creation_effect.name, False)))

    material_effects_name_length = len(BIPED.biped_body.material_effects.name)
    if material_effects_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % material_effects_name_length, TAG.string_to_bytes(BIPED.biped_body.material_effects.name, False)))

    write_ai_properties(output_stream, TAG, BIPED.ai_properties, BIPED.ai_properties_header)
    write_functions(output_stream, TAG, BIPED.functions, BIPED.functions_header)
    write_attachments(output_stream, TAG, BIPED.attachments, BIPED.attachments_header)
    write_tag_ref(output_stream, TAG, BIPED.widgets, BIPED.widgets_header)
    write_old_functions(output_stream, TAG, BIPED.old_functions, BIPED.old_functions_header)
    write_change_colors(output_stream, TAG, BIPED.change_colors, BIPED.change_colors_header)
    write_predicted_resources(output_stream, TAG, BIPED.predicted_resources, BIPED.predicted_resources_header)

    integrated_light_toggle_length = len(BIPED.biped_body.integrated_light_toggle.name)
    if integrated_light_toggle_length > 0:
        output_stream.write(struct.pack('<%ssx' % integrated_light_toggle_length, TAG.string_to_bytes(BIPED.biped_body.integrated_light_toggle.name, False)))

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("uncs", True), 0, 1, 32))

    camera_marker_name_length = len(BIPED.biped_body.camera_marker_name)
    if camera_marker_name_length > 0:
        output_stream.write(struct.pack('<%ss' % camera_marker_name_length, TAG.string_to_bytes(BIPED.biped_body.camera_marker_name, False)))

    camera_submerged_marker_name_length = len(BIPED.biped_body.camera_submerged_marker_name)
    if camera_submerged_marker_name_length > 0:
        output_stream.write(struct.pack('<%ss' % camera_submerged_marker_name_length, TAG.string_to_bytes(BIPED.biped_body.camera_submerged_marker_name, False)))

    write_tag_ref(output_stream, TAG, BIPED.camera_tracks, BIPED.camera_tracks_header)

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("usas", True), 0, 1, 20))

    spawned_turret_actor_length = len(BIPED.biped_body.spawned_turret_actor.name)
    if spawned_turret_actor_length > 0:
        output_stream.write(struct.pack('<%ssx' % spawned_turret_actor_length, TAG.string_to_bytes(BIPED.biped_body.spawned_turret_actor.name, False)))

    right_hand_node_length = len(BIPED.biped_body.right_hand_node)
    if right_hand_node_length > 0:
        output_stream.write(struct.pack('<%ss' % right_hand_node_length, TAG.string_to_bytes(BIPED.biped_body.right_hand_node, False)))

    left_hand_node_length = len(BIPED.biped_body.left_hand_node)
    if left_hand_node_length > 0:
        output_stream.write(struct.pack('<%ss' % left_hand_node_length, TAG.string_to_bytes(BIPED.biped_body.left_hand_node, False)))

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("uHnd", True), 1, 1, 4))

    preferred_gun_node_length = len(BIPED.biped_body.preferred_gun_node)
    if preferred_gun_node_length > 0:
        output_stream.write(struct.pack('<%ss' % preferred_gun_node_length, TAG.string_to_bytes(BIPED.biped_body.preferred_gun_node, False)))

    melee_damage_length = len(BIPED.biped_body.melee_damage.name)
    if melee_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % melee_damage_length, TAG.string_to_bytes(BIPED.biped_body.melee_damage.name, False)))

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("ubms", True), 1, 1, 80))

    boarding_melee_damage_length = len(BIPED.biped_body.boarding_melee_damage.name)
    if boarding_melee_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % boarding_melee_damage_length, TAG.string_to_bytes(BIPED.biped_body.boarding_melee_damage.name, False)))

    boarding_melee_response_length = len(BIPED.biped_body.boarding_melee_response.name)
    if boarding_melee_response_length > 0:
        output_stream.write(struct.pack('<%ssx' % boarding_melee_response_length, TAG.string_to_bytes(BIPED.biped_body.boarding_melee_response.name, False)))

    landing_melee_damage_length = len(BIPED.biped_body.landing_melee_damage.name)
    if landing_melee_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % landing_melee_damage_length, TAG.string_to_bytes(BIPED.biped_body.landing_melee_damage.name, False)))

    flurry_melee_damage_length = len(BIPED.biped_body.flurry_melee_damage.name)
    if flurry_melee_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % flurry_melee_damage_length, TAG.string_to_bytes(BIPED.biped_body.flurry_melee_damage.name, False)))

    obstacle_smash_damage_length = len(BIPED.biped_body.obstacle_smash_damage.name)
    if obstacle_smash_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % obstacle_smash_damage_length, TAG.string_to_bytes(BIPED.biped_body.obstacle_smash_damage.name, False)))

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

    area_damage_effect_length = len(BIPED.biped_body.area_damage_effect.name)
    if area_damage_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % area_damage_effect_length, TAG.string_to_bytes(BIPED.biped_body.area_damage_effect.name, False)))

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("chpy", True), 0, 1, 160))

    living_material_name_length = len(BIPED.biped_body.living_material_name)
    if living_material_name_length > 0:
        output_stream.write(struct.pack('<%ss' % living_material_name_length, TAG.string_to_bytes(BIPED.biped_body.living_material_name, False)))

    dead_material_name_length = len(BIPED.biped_body.dead_material_name)
    if dead_material_name_length > 0:
        output_stream.write(struct.pack('<%ss' % dead_material_name_length, TAG.string_to_bytes(BIPED.biped_body.dead_material_name, False)))

    write_sphere_shapes(output_stream, TAG, BIPED.dead_sphere_shapes, BIPED.dead_sphere_shapes_header)
    write_pill_shapes(output_stream, TAG, BIPED.pill_shapes, BIPED.pill_shapes_header)
    write_sphere_shapes(output_stream, TAG, BIPED.sphere_shapes, BIPED.sphere_shapes_header)

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("chgr", True), 0, 1, 48))
    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("chfl", True), 0, 1, 44))
    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("chdd", True), 0, 1, 0))
    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("chsn", True), 0, 1, 0))

    write_contact_points(output_stream, TAG, BIPED.contact_points, BIPED.contact_points_header)

    reanimation_character_length = len(BIPED.biped_body.reanimation_character.name)
    if reanimation_character_length > 0:
        output_stream.write(struct.pack('<%ssx' % reanimation_character_length, TAG.string_to_bytes(BIPED.biped_body.reanimation_character.name, False)))

    death_spawn_character_length = len(BIPED.biped_body.death_spawn_character.name)
    if death_spawn_character_length > 0:
        output_stream.write(struct.pack('<%ssx' % death_spawn_character_length, TAG.string_to_bytes(BIPED.biped_body.death_spawn_character.name, False)))
