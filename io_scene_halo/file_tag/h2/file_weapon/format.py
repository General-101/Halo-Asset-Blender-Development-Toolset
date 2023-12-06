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

from mathutils import Vector
from enum import Flag, Enum, auto

class ObjectFlags(Flag):
    does_not_cast_shadow = auto()
    search_cardinal_direction_lightmaps_on_failure = auto()
    unused = auto()
    not_a_pathfinding_obstacle = auto()
    extension_of_parent = auto()
    does_not_cause_collision_damage = auto()
    early_mover = auto()
    early_mover_localized_physics = auto()
    use_static_massive_lightmap_sample = auto()
    object_scales_attachments = auto()
    inherits_players_appearance = auto()
    dead_bipeds_cant_localize = auto()
    attach_to_clusters_dynamic_sphere = auto()
    effects_created_by_this_object_do_not_spawn_objects_in_multiplayer = auto()
    prophet_is_not_displayed_in_pegasus_builds = auto()

class LightmapShadowModeEnum(Enum):
    default = 0
    never = auto()
    always = auto()

class SweetenerSizeEnum(Enum):
    small = 0
    medium = auto()
    large = auto()

class ItemFlags(Flag):
    always_maintains_z_up = auto()
    destroyed_by_explosions = auto()
    unaffected_by_gravity = auto()

class WeaponFlags(Flag):
    unused_0 = auto()
    unused_1 = auto()
    unused_2 = auto()
    must_be_readied = auto()
    doesnt_count_toward_maximum = auto()
    aim_assists_only_when_zoomed = auto()
    prevents_grenade_throwing = auto()
    unused_7 = auto()
    unused_8 = auto()
    prevents_melee_attack = auto()
    detonates_when_dropped = auto()
    cannot_fire_at_maximum_age = auto()
    secondary_trigger_overrides_grenades = auto()
    unused_13 = auto()
    unused_14 = auto()
    ai_use_weapon_melee_damage = auto()
    forces_no_binoculars = auto()
    loop_fp_firing_animation = auto()
    prevents_sprinting = auto()
    cannot_fire_while_boosting = auto()
    prevents_driving = auto()
    prevents_gunning = auto()
    can_be_dual_wielded = auto()
    can_only_be_dual_wielded = auto()
    melee_only = auto()
    cant_fire_if_parent_dead = auto()
    weapon_ages_with_each_kill = auto()
    weapon_uses_old_dual_fire_error_code = auto()
    primary_trigger_melee_attacks = auto()
    cannot_be_used_by_player = auto()
    prevents_crouching = auto()
    uses_third_person_character = auto()

class SecondaryTriggerModeEnum(Enum):
    normal = 0
    slaved_to_primary = auto()
    inhibits_primary = auto()
    loads_alterate_ammunition = auto()
    loads_multiple_primary_ammunition = auto()

class MeleeDamageReportingTypeEnum(Enum):
    none = 0
    falling_damage = auto()
    generic_collision_damage = auto()
    generic_melee_damage = auto()
    generic_explosion = auto()
    magnum_pistol = auto()
    plasma_pistol = auto()
    needler = auto()
    smg = auto()
    plasma_rifle = auto()
    battle_rifle = auto()
    carbine = auto()
    shotgun = auto()
    sniper_rifle = auto()
    beam_rifle = auto()
    rocket_launcher = auto()
    flak_cannon = auto()
    brute_shot = auto()
    disintegrator = auto()
    brute_plasma_rifle = auto()
    energy_sword = auto()
    frag_grenade = auto()
    plasma_grenade = auto()
    flag_melee_damage = auto()
    bomb_melee_damage = auto()
    bomb_explosion_damage = auto()
    ball_melee_damage = auto()
    human_turret = auto()
    plasma_turret = auto()
    banshee = auto()
    ghost = auto()
    mongoose = auto()
    scorpion = auto()
    spectre_driver = auto()
    spectre_gunner = auto()
    warthog_driver = auto()
    warthog_gunner = auto()
    wraith = auto()
    tank = auto()
    sentinel_beam = auto()
    sentinel_rpg = auto()
    teleporter = auto()
    warthog_gunner_gauss = auto()
    warthog_gunner_rocket = auto()

class MovementPenalizedEnum(Enum):
    always = 0
    when_zoomed = auto()
    when_zoomed_or_reloading = auto()

class MultiplayerWeaponTypeEnum(Enum):
    none = 0
    ctf_flag = auto()
    oddball_ball = auto()
    headhunter_head = auto()
    juggernaut_powerup = auto()

class WeaponTypeEnum(Enum):
    undefined = 0
    shotgun = auto()
    needler = auto()
    plasma_pistol = auto()
    plasma_rifle = auto()
    rocket_launcher = auto()

class TrackingTypeEnum(Enum):
    no_tracking = 0
    human_tracking = auto()
    plasma_tracking = auto()

class WeaponAsset():
    def __init__(self):
        self.header = None
        self.weapon_body_header = None
        self.weapon_body = None
        self.ai_properties_header = None
        self.ai_properties = None
        self.functions_header = None
        self.functions = None
        self.attachments_header = None
        self.attachments = None
        self.widgets_header = None
        self.widgets = None
        self.old_functions_header = None
        self.old_functions = None
        self.change_colors_header = None
        self.change_colors = None
        self.predicted_resources_header = None
        self.predicted_resources = None
        self.predicted_bitmaps_header = None
        self.predicted_bitmaps = None
        self.first_person_header = None
        self.first_person = None
        self.weapon_predicted_resources_header = None
        self.weapon_predicted_resources = None
        self.magazines_header = None
        self.magazines = None
        self.new_triggers_header = None
        self.new_triggers = None
        self.barrels_header = None
        self.barrels = None

    class WeaponBody:
        def __init__(self, object_flags=0, bounding_radius=0.0, bounding_offset=Vector(), acceleration_scale=0.0, lightmap_shadow_mode=0, sweetner_size=0, 
                     dynamic_light_sphere_radius=0.0, dynamic_light_sphere_offset=Vector(), default_model_variant="", default_model_variant_length=0, model=None, crate_object=None, 
                     modifier_shader=None, creation_effect=None, material_effects=None, ai_properties_tag_block=None, functions_tag_block=None, apply_collision_damage_scale=0.0, 
                     min_game_acc=0.0, max_game_acc=0.0, min_game_scale=0.0, max_game_scale=0.0, min_abs_acc=0.0, max_abs_acc=0.0, min_abs_scale=0.0, max_abs_scale=0.0, 
                     hud_text_message_index=0, attachments_tag_block=None, widgets_tag_block=None, old_functions_tag_block=None, change_colors_tag_block=None, 
                     predicted_resources_tag_block=None, equipment_flags=0, old_message_index=0, sort_order=0, multiplayer_on_ground_scale=0.0, campaign_on_ground_scale=0.0, 
                     pickup_message="", pickup_message_length=0, swap_message="", swap_message_length=0, pickup_or_dual_message="", pickup_or_dual_message_length=0, 
                     swap_or_dual_message="", swap_or_dual_message_length=0, dual_only_message="", dual_only_message_length=0, picked_up_message="", picked_up_message_length=0, 
                     singluar_quantity_message="", singluar_quantity_message_length=0, plural_quantity_message="", plural_quantity_message_length=0, switch_to_message="", 
                     switch_to_message_length=0, switch_to_from_ai_message="", switch_to_from_ai_message_length=0, unused=None, collision_sound=None, 
                     predicted_bitmaps_tag_block=None, detonation_damage_effect=None, detonation_delay=(0.0, 0.0), detonating_effect=None, detonation_effect=None, weapon_flags=0, 
                     unknown="", unknown_length=0, secondary_trigger_mode=0, maximum_alternate_shots_loaded=0, turn_on_time=0.0, ready_time=0.0, ready_effect=None, 
                     ready_damage_effect=None, heat_recovery_threshold=0.0, overheated_threshold=0.0, heat_detonation_threshold=0.0, heat_detonation_fraction=0.0, 
                     heat_loss_per_second=0.0, heat_illumination=0.0, overheated_loss_per_second=0.0, overheated=None, overheated_damage_effect=None, detonation=None, 
                     weapon_detonation_damage_effect=None, player_melee_damage=None, player_melee_response=None, magnetism_angle=0.0, magnetism_range=0.0, throttle_magnitude=0.0, 
                     throttle_minimum_distance=0.0, throttle_maximum_adjustment_angle=0.0, damage_pyramid_angles=(0.0, 0.0), damage_pyramid_depth=0.0, first_hit_melee_damage=None, 
                     first_hit_melee_response=None, second_hit_melee_damage=None, second_hit_melee_response=None, third_hit_melee_damage=None, third_hit_melee_response=None, 
                     lunge_melee_damage=None, lunge_melee_response=None, melee_damage_reporting_type=0, magnification_levels=0, magnification_range=(0.0, 0.0), autoaim_angle=0.0, 
                     autoaim_range=0.0, weapon_aim_assist_magnetism_angle=0.0, weapon_aim_assist_magnetism_range=0.0, deviation_angle=0.0, movement_penalized=0, 
                     forward_movement_penalty=0.0, sideways_movement_penalty=0.0, ai_scariness=0.0, weapon_power_on_time=0.0, weapon_power_off_time=0.0, 
                     weapon_power_on_effect=None, weapon_power_off_effect=None, age_heat_recovery_penalty=0.0, age_rate_of_fire_penalty=0.0, age_misfire_start=0.0, 
                     age_misfire_chance=0.0, pickup_sound=None, zoom_in_sound=None, zoom_out_sound=None, active_camo_ding=0.0, active_camo_regrowth_rate=0.0, handle_node="", 
                     handle_node_length=0, weapon_class="", weapon_class_length=0, weapon_name="", weapon_name_length=0, multiplayer_weapon_type=0, weapon_type=0, 
                     tracking_type=0, first_person_tag_block=None, new_hud_interface=None, weapon_predicted_resources_tag_block=None, magazines_tag_block=None, 
                     new_triggers_tag_block=None, barrels_tag_block=None, max_movement_acceleration=0.0, max_movement_velocity=0.0, max_turning_acceleration=0.0, 
                     max_turning_velocity=0.0, deployed_vehicle=None, age_effect=None, aged_weapon=None, first_person_weapon_offset=Vector(), first_person_scope_size=(0.0, 0.0)):
            self.object_flags = object_flags
            self.bounding_radius = bounding_radius
            self.bounding_offset = bounding_offset
            self.acceleration_scale = acceleration_scale
            self.lightmap_shadow_mode = lightmap_shadow_mode
            self.sweetner_size = sweetner_size
            self.dynamic_light_sphere_radius = dynamic_light_sphere_radius
            self.dynamic_light_sphere_offset = dynamic_light_sphere_offset
            self.default_model_variant = default_model_variant
            self.default_model_variant_length = default_model_variant_length
            self.model = model
            self.crate_object = crate_object
            self.modifier_shader = modifier_shader
            self.creation_effect = creation_effect
            self.material_effects = material_effects
            self.ai_properties_tag_block = ai_properties_tag_block
            self.functions_tag_block = functions_tag_block
            self.apply_collision_damage_scale = apply_collision_damage_scale
            self.min_game_acc = min_game_acc
            self.max_game_acc = max_game_acc
            self.min_game_scale = min_game_scale
            self.max_game_scale = max_game_scale
            self.min_abs_acc = min_abs_acc
            self.max_abs_acc = max_abs_acc
            self.min_abs_scale = min_abs_scale
            self.max_abs_scale = max_abs_scale
            self.hud_text_message_index = hud_text_message_index
            self.attachments_tag_block = attachments_tag_block
            self.widgets_tag_block = widgets_tag_block
            self.old_functions_tag_block = old_functions_tag_block
            self.change_colors_tag_block = change_colors_tag_block
            self.predicted_resources_tag_block = predicted_resources_tag_block
            self.equipment_flags = equipment_flags
            self.old_message_index = old_message_index
            self.sort_order = sort_order
            self.multiplayer_on_ground_scale = multiplayer_on_ground_scale
            self.campaign_on_ground_scale = campaign_on_ground_scale
            self.pickup_message = pickup_message
            self.pickup_message_length = pickup_message_length
            self.swap_message = swap_message
            self.swap_message_length = swap_message_length
            self.pickup_or_dual_message = pickup_or_dual_message
            self.pickup_or_dual_message_length = pickup_or_dual_message_length
            self.swap_or_dual_message = swap_or_dual_message
            self.swap_or_dual_message_length = swap_or_dual_message_length
            self.dual_only_message = dual_only_message
            self.dual_only_message_length = dual_only_message_length
            self.picked_up_message = picked_up_message
            self.picked_up_message_length = picked_up_message_length
            self.singluar_quantity_message = singluar_quantity_message
            self.singluar_quantity_message_length = singluar_quantity_message_length
            self.plural_quantity_message = plural_quantity_message
            self.plural_quantity_message_length = plural_quantity_message_length
            self.switch_to_message = switch_to_message
            self.switch_to_message_length = switch_to_message_length
            self.switch_to_from_ai_message = switch_to_from_ai_message
            self.switch_to_from_ai_message_length = switch_to_from_ai_message_length
            self.unused = unused
            self.collision_sound = collision_sound
            self.predicted_bitmaps_tag_block = predicted_bitmaps_tag_block
            self.detonation_damage_effect = detonation_damage_effect
            self.detonation_delay = detonation_delay
            self.detonating_effect = detonating_effect
            self.detonation_effect = detonation_effect
            self.weapon_flags = weapon_flags
            self.unknown = unknown
            self.unknown_length = unknown_length
            self.secondary_trigger_mode = secondary_trigger_mode
            self.maximum_alternate_shots_loaded = maximum_alternate_shots_loaded
            self.turn_on_time = turn_on_time
            self.ready_time = ready_time
            self.ready_effect = ready_effect
            self.ready_damage_effect = ready_damage_effect
            self.heat_recovery_threshold = heat_recovery_threshold
            self.overheated_threshold = overheated_threshold
            self.heat_detonation_threshold = heat_detonation_threshold
            self.heat_detonation_fraction = heat_detonation_fraction
            self.heat_loss_per_second = heat_loss_per_second
            self.heat_illumination = heat_illumination
            self.overheated_loss_per_second = overheated_loss_per_second
            self.overheated = overheated
            self.overheated_damage_effect = overheated_damage_effect
            self.detonation = detonation
            self.weapon_detonation_damage_effect = weapon_detonation_damage_effect
            self.player_melee_damage = player_melee_damage
            self.player_melee_response = player_melee_response
            self.magnetism_angle = magnetism_angle
            self.magnetism_range = magnetism_range
            self.throttle_magnitude = throttle_magnitude
            self.throttle_minimum_distance = throttle_minimum_distance
            self.throttle_maximum_adjustment_angle = throttle_maximum_adjustment_angle
            self.damage_pyramid_angles = damage_pyramid_angles
            self.damage_pyramid_depth = damage_pyramid_depth
            self.first_hit_melee_damage = first_hit_melee_damage
            self.first_hit_melee_response = first_hit_melee_response
            self.second_hit_melee_damage = second_hit_melee_damage
            self.second_hit_melee_response = second_hit_melee_response
            self.third_hit_melee_damage = third_hit_melee_damage
            self.third_hit_melee_response = third_hit_melee_response
            self.lunge_melee_damage = lunge_melee_damage
            self.lunge_melee_response = lunge_melee_response
            self.melee_damage_reporting_type = melee_damage_reporting_type
            self.magnification_levels = magnification_levels
            self.magnification_range = magnification_range
            self.autoaim_angle = autoaim_angle
            self.autoaim_range = autoaim_range
            self.weapon_aim_assist_magnetism_angle = weapon_aim_assist_magnetism_angle
            self.weapon_aim_assist_magnetism_range = weapon_aim_assist_magnetism_range
            self.deviation_angle = deviation_angle
            self.movement_penalized = movement_penalized
            self.forward_movement_penalty = forward_movement_penalty
            self.sideways_movement_penalty = sideways_movement_penalty
            self.ai_scariness = ai_scariness
            self.weapon_power_on_time = weapon_power_on_time
            self.weapon_power_off_time = weapon_power_off_time
            self.weapon_power_on_effect = weapon_power_on_effect
            self.weapon_power_off_effect = weapon_power_off_effect
            self.age_heat_recovery_penalty = age_heat_recovery_penalty
            self.age_rate_of_fire_penalty = age_rate_of_fire_penalty
            self.age_misfire_start = age_misfire_start
            self.age_misfire_chance = age_misfire_chance
            self.pickup_sound = pickup_sound
            self.zoom_in_sound = zoom_in_sound
            self.zoom_out_sound = zoom_out_sound
            self.active_camo_ding = active_camo_ding
            self.active_camo_regrowth_rate = active_camo_regrowth_rate
            self.handle_node = handle_node
            self.handle_node_length = handle_node_length
            self.weapon_class = weapon_class
            self.weapon_class_length = weapon_class_length
            self.weapon_name = weapon_name
            self.weapon_name_length = weapon_name_length
            self.multiplayer_weapon_type = multiplayer_weapon_type
            self.weapon_type = weapon_type
            self.tracking_type = tracking_type
            self.first_person_tag_block = first_person_tag_block
            self.new_hud_interface = new_hud_interface
            self.weapon_predicted_resources_tag_block = weapon_predicted_resources_tag_block
            self.magazines_tag_block = magazines_tag_block
            self.new_triggers_tag_block = new_triggers_tag_block
            self.barrels_tag_block = barrels_tag_block
            self.max_movement_acceleration = max_movement_acceleration
            self.max_movement_velocity = max_movement_velocity
            self.max_turning_acceleration = max_turning_acceleration
            self.max_turning_velocity = max_turning_velocity
            self.deployed_vehicle = deployed_vehicle
            self.age_effect = age_effect
            self.aged_weapon = aged_weapon
            self.first_person_weapon_offset = first_person_weapon_offset
            self.first_person_scope_size = first_person_scope_size
