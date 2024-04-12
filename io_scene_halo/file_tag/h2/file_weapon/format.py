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
from ..file_item.format import ItemAsset

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

class BehaviorEnum(Enum):
    spew = 0
    latch = auto()
    latch_autofire = auto()
    charge = auto()
    latch_zoom = auto()
    latch_rocketlauncher = auto()

class TriggerPredictionEnum(Enum):
    none = 0
    spew = auto()
    charge = auto()

class BarrelFlags(Flag):
    tracks_fired_projectile = auto()
    random_firing_effects = auto()
    can_fire_with_partial_ammo = auto()
    projectiles_use_weapon_origin = auto()
    ejects_during_chamber = auto()
    use_error_when_unzoomed = auto()
    projectile_vector_cannot_be_adjusted = auto()
    projectiles_have_identical_error = auto()
    projectiles_fire_parallel = auto()
    cant_fire_when_others_firing_ = auto()
    cant_fire_when_others_recovering = auto()
    dont_clear_fire_bit_after_recovering = auto()
    stagger_fire_across_multiple_markers = auto()
    fires_locked_projectiles = auto()
    can_fire_at_maximum_age = auto()

class BarrelPredictionEnum(Enum):
    none = 0
    continuous = auto()
    instant = auto()

class WeaponAsset(ItemAsset):
    def __init__(self):
        super().__init__()
        self.header = None
        self.weapon_body_header = None
        self.weapon_body = None
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

    class WeaponBody(ItemAsset.ItemBody):
        def __init__(self, weapon_flags=0, unknown="", unknown_length=0, secondary_trigger_mode=0, maximum_alternate_shots_loaded=0, turn_on_time=0.0, ready_time=0.0, 
                     ready_effect=None, ready_damage_effect=None, heat_recovery_threshold=0.0, overheated_threshold=0.0, heat_detonation_threshold=0.0, heat_detonation_fraction=0.0, 
                     heat_loss_per_second=0.0, heat_illumination=0.0, overheated_loss_per_second=0.0, overheated=None, overheated_damage_effect=None, detonation=None, 
                     weapon_detonation_damage_effect=None, player_melee_damage=None, player_melee_response=None, magnetism_angle=0.0, magnetism_range=0.0, throttle_magnitude=0.0, 
                     throttle_minimum_distance=0.0, throttle_maximum_adjustment_angle=0.0, damage_pyramid_angles=(0.0, 0.0), damage_pyramid_depth=0.0, first_hit_melee_damage=None, 
                     first_hit_melee_response=None, second_hit_melee_damage=None, second_hit_melee_response=None, third_hit_melee_damage=None, third_hit_melee_response=None, 
                     lunge_melee_damage=None, lunge_melee_response=None, melee_damage_reporting_type=0, magnification_levels=0, magnification_range=(0.0, 0.0), autoaim_angle=0.0, 
                     autoaim_range=0.0, weapon_aim_assist_magnetism_angle=0.0, weapon_aim_assist_magnetism_range=0.0, deviation_angle=0.0, movement_penalized=0, 
                     forward_movement_penalty=0.0, sideways_movement_penalty=0.0, ai_scariness=0.0, weapon_power_on_time=0.0, weapon_power_off_time=0.0, weapon_power_on_effect=None, 
                     weapon_power_off_effect=None, age_heat_recovery_penalty=0.0, age_rate_of_fire_penalty=0.0, age_misfire_start=0.0, age_misfire_chance=0.0, pickup_sound=None, 
                     zoom_in_sound=None, zoom_out_sound=None, active_camo_ding=0.0, active_camo_regrowth_rate=0.0, handle_node="", handle_node_length=0, weapon_class="", 
                     weapon_class_length=0, weapon_name="", weapon_name_length=0, multiplayer_weapon_type=0, weapon_type=0, tracking_type=0, first_person_tag_block=None, 
                     new_hud_interface=None, weapon_predicted_resources_tag_block=None, magazines_tag_block=None, new_triggers_tag_block=None, barrels_tag_block=None, 
                     max_movement_acceleration=0.0, max_movement_velocity=0.0, max_turning_acceleration=0.0, max_turning_velocity=0.0, deployed_vehicle=None, age_effect=None, 
                     aged_weapon=None, first_person_weapon_offset=Vector(), first_person_scope_size=(0.0, 0.0)):
            super().__init__()
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

    class FirstPerson:
        def __init__(self, first_person_model=None, first_person_animations=None):
            self.first_person_model = first_person_model
            self.first_person_animations = first_person_animations

    class MagazineStats:
        def __init__(self, flags=0, rounds_recharged=0, rounds_total_initial=0, rounds_total_maximum=0, rounds_loaded_maximum=0, reload_time=0.0, 
                     rounds_reloaded=0, chamber_time=0.0, reloading_effect=None, reloading_damage_effect=None, chambering_effect=None, 
                     chambering_damage_effect=None, magazines_tag_block=None, magazines_header=None, magazines=None):
            self.flags = flags
            self.rounds_recharged = rounds_recharged
            self.rounds_total_initial = rounds_total_initial
            self.rounds_total_maximum = rounds_total_maximum
            self.rounds_loaded_maximum = rounds_loaded_maximum
            self.reload_time = reload_time
            self.rounds_reloaded = rounds_reloaded
            self.chamber_time = chamber_time
            self.reloading_effect = reloading_effect
            self.reloading_damage_effect = reloading_damage_effect
            self.chambering_effect = chambering_effect
            self.chambering_damage_effect = chambering_damage_effect
            self.magazines_tag_block = magazines_tag_block
            self.magazines_header = magazines_header
            self.magazines = magazines

    class Magazine:
        def __init__(self, rounds=0, equipment=None):
            self.rounds = rounds
            self.equipment = equipment

    class NewTrigger:
        def __init__(self, flags=0, input_type=0, behavior=0, primary_barrel=0, secondary_barrel=0, prediction=0, autofire_time=0.0, autofire_throw=0.0, 
                     secondary_action=0, primary_action=0, charging_time=0.0, charged_time=0.0, overcharged_action=0, charged_illumination=0.0, spew_time=0.0, 
                     charging_effect=None, charging_damage_effect=None):
            self.flags = flags
            self.input_type = input_type
            self.behavior = behavior
            self.primary_barrel = primary_barrel
            self.secondary_barrel = secondary_barrel
            self.prediction = prediction
            self.autofire_time = autofire_time
            self.autofire_throw = autofire_throw
            self.secondary_action = secondary_action
            self.primary_action = primary_action
            self.charging_time = charging_time
            self.charged_time = charged_time
            self.overcharged_action = overcharged_action
            self.charged_illumination = charged_illumination
            self.spew_time = spew_time
            self.charging_effect = charging_effect
            self.charging_damage_effect = charging_damage_effect

    class Barrel:
        def __init__(self, flags=0, rounds_per_second=(0.0, 0.0), firing_acceleration_time=0.0, firing_deceleration_time=0.0, barrel_spin_scale=0.0, 
                     blurred_rate_of_fire=0.0, shots_per_fire=(0, 0), fire_recovery_time=0.0, soft_recovery_fraction=0.0, magazine=0, rounds_per_shot=0, 
                     minimum_rounds_loaded=0, rounds_between_tracers=0, optional_barrel_marker_name="", optional_barrel_marker_name_length=0, prediction_type=0, 
                     firing_noise=0, error_acceleration_time=0.0, error_deceleration_time=0.0, damage_error=(0.0, 0.0), dual_acceleration_time=0.0, 
                     dual_deceleration_time=0.0, dual_minimum_error=0.0, dual_error_angle=(0.0, 0.0), dual_wield_damage_scale=0.0, distribution_function=0, 
                     projectiles_per_shot=0, distribution_angle=0.0, projectile_minimum_error=0.0, projectile_error_angle=(0.0, 0.0), 
                     first_person_offset=Vector(), damage_effect_reporting_type=0, projectile=None, damage_effect=None, ejection_port_recovery_time=0.0, 
                     illumination_recovery_time=0.0, heat_generated_per_round=0.0, age_generated_per_round=0.0, overload_time=0.0, 
                     angle_change_per_shot=(0.0, 0.0), recoil_acceleration_time=0.0, recoil_deceleration_time=0.0, angle_change_function=0, 
                     firing_effects_tag_block=None, firing_effects_header=None, firing_effects=None):
            self.flags = flags
            self.rounds_per_second = rounds_per_second
            self.firing_acceleration_time = firing_acceleration_time
            self.firing_deceleration_time = firing_deceleration_time
            self.barrel_spin_scale = barrel_spin_scale
            self.blurred_rate_of_fire = blurred_rate_of_fire
            self.shots_per_fire = shots_per_fire
            self.fire_recovery_time = fire_recovery_time
            self.soft_recovery_fraction = soft_recovery_fraction
            self.magazine = magazine
            self.rounds_per_shot = rounds_per_shot
            self.minimum_rounds_loaded = minimum_rounds_loaded
            self.rounds_between_tracers = rounds_between_tracers
            self.optional_barrel_marker_name = optional_barrel_marker_name
            self.optional_barrel_marker_name_length = optional_barrel_marker_name_length
            self.prediction_type = prediction_type
            self.firing_noise = firing_noise
            self.error_acceleration_time = error_acceleration_time
            self.error_deceleration_time = error_deceleration_time
            self.damage_error = damage_error
            self.dual_acceleration_time = dual_acceleration_time
            self.dual_deceleration_time = dual_deceleration_time
            self.dual_minimum_error = dual_minimum_error
            self.dual_error_angle = dual_error_angle
            self.dual_wield_damage_scale = dual_wield_damage_scale
            self.distribution_function = distribution_function
            self.projectiles_per_shot = projectiles_per_shot
            self.distribution_angle = distribution_angle
            self.projectile_minimum_error = projectile_minimum_error
            self.projectile_error_angle = projectile_error_angle
            self.first_person_offset = first_person_offset
            self.damage_effect_reporting_type = damage_effect_reporting_type
            self.projectile = projectile
            self.damage_effect = damage_effect
            self.ejection_port_recovery_time = ejection_port_recovery_time
            self.illumination_recovery_time = illumination_recovery_time
            self.heat_generated_per_round = heat_generated_per_round
            self.age_generated_per_round = age_generated_per_round
            self.overload_time = overload_time
            self.angle_change_per_shot = angle_change_per_shot
            self.recoil_acceleration_time = recoil_acceleration_time
            self.recoil_deceleration_time = recoil_deceleration_time
            self.angle_change_function = angle_change_function
            self.firing_effects_tag_block = firing_effects_tag_block
            self.firing_effects_header = firing_effects_header
            self.firing_effects = firing_effects

    class FiringEffect:
        def __init__(self, shot_count_lower_bound=0, shot_count_upper_bound=0, firing_effect=None, misfire_effect=None, empty_effect=None, firing_damage=None, 
                     misfire_damage=None, empty_damage=None):
            self.shot_count_lower_bound = shot_count_lower_bound
            self.shot_count_upper_bound = shot_count_upper_bound
            self.firing_effect = firing_effect
            self.misfire_effect = misfire_effect
            self.empty_effect = empty_effect
            self.firing_damage = firing_damage
            self.misfire_damage = misfire_damage
            self.empty_damage = empty_damage
