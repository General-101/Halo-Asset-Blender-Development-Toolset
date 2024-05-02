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
from ....file_tag.h2.file_weapon.format import BarrelFlags

class WeaponFlags(Flag):
    unused_0 = auto()
    unused_1 = auto()
    unused_2 = auto()
    must_be_readied = auto()
    doesnt_count_towards_maximum = auto()
    aim_assists_only_when_zoomed = auto()
    prevents_grenade_throwing = auto()
    unused_7 = auto()
    unused_8 = auto()
    prevents_melee_attack = auto()
    detonates_when_dropped = auto()
    cannot_fire_at_maximum_age = auto()
    secondary_trigger_overrides_grenades = auto()
    unused_13 = auto()
    enables_integrated_night_vision = auto()
    ai_use_weapon_melee_damage = auto()
    prevents_crouching = auto()
    uses_3rd_person_camera = auto()

class SecondaryTriggerModeEnum(Enum):
    normal = 0
    slaved_to_primary = auto()
    inhibits_primary = auto()
    loads_alterate_ammunition = auto()
    loads_multiple_primary_ammunition = auto()

class WeaponFunctionEnum(Enum):
    none = 0
    heat = auto()
    primary_ammunition = auto()
    secondary_ammunition = auto()
    primary_rate_of_fire = auto()
    secondary_rate_of_fire = auto()
    ready = auto()
    primary_ejection_port = auto()
    secondary_ejection_port = auto()
    overheated = auto()
    primary_charged = auto()
    secondary_charged = auto()
    illumination = auto()
    age = auto()
    integrated_light = auto()
    primary_fire = auto()
    secondary_fire = auto()
    primary_firing_on = auto()
    secondary_firing_on = auto()

class MovementPenalizedEnum(Enum):
    always = 0
    when_zoomed = auto()
    when_zoomed_or_reloading = auto()

class WeaponTypeEnum(Enum):
    undefined = 0
    shotgun = auto()
    needler = auto()
    plasma_pistol = auto()
    plasma_rifle = auto()
    rocket_launcher = auto()

class MagazineFlags(Flag):
    wastes_rounds_when_reloaded = auto()
    every_round_must_be_chambered = auto()

class TriggerFlags(Flag):
    tracks_fired_projectile = auto()
    random_firing_effects = auto()
    can_fire_with_partial_ammo = auto()
    does_not_repeat_automatically = auto()
    locks_in_on_off_state = auto()
    projectiles_use_weapon_origin = auto()
    sticks_when_dropped = auto()
    ejects_during_chamber = auto()
    discharging_spews = auto()
    analog_rate_of_fire = auto()
    use_error_when_unzoomed = auto()
    projectile_vector_cannot_be_adjusted = auto()
    projectiles_have_identical_error = auto()
    projectile_is_client_side_only = auto()
    use_unit_adjust_projectile_ray_from_halo1 = auto()

class PredictionEnum(Enum):
    none = 0
    continuous = auto()
    instant = auto()

class FiringNoiseEnum(Enum):
    silent = 0
    medium = auto()
    loud = auto()
    shout = auto()
    quiet = auto()

class OverchargedActionEnum(Enum):
    none = 0
    explode = auto()
    discharge = auto()

class DistributionFunctionEnum(Enum):
    point = auto()
    horizontal_fan = auto()

def get_magazine(WEAPON, magazine_index):
    valid_magazine_index = -1
    if magazine_index >= 0:
        magazine_element = WEAPON.magazines[magazine_index]
        if magazine_element.rounds_loaded_maximum > 0:
            valid_magazine_index = magazine_index

    return valid_magazine_index

def upgrade_h1_barrel_flags(barrel_flags):
    flags = 0
    active_h1_flags = [flag.name for flag in TriggerFlags if flag in TriggerFlags(barrel_flags)]
    if "tracks_fired_projectile" in active_h1_flags:
        flags += BarrelFlags.tracks_fired_projectile.value
    if "random_firing_effects" in active_h1_flags:
        flags += BarrelFlags.random_firing_effects.value
    if "can_fire_with_partial_ammo" in active_h1_flags:
        flags += BarrelFlags.can_fire_with_partial_ammo.value
    if "projectiles_use_weapon_origin" in active_h1_flags:
        flags += BarrelFlags.projectiles_use_weapon_origin.value
    if "ejects_during_chamber" in active_h1_flags:
        flags += BarrelFlags.ejects_during_chamber.value
    if "use_error_when_unzoomed" in active_h1_flags:
        flags += BarrelFlags.use_error_when_unzoomed.value
    if "projectile_vector_cannot_be_adjusted" in active_h1_flags:
        flags += BarrelFlags.projectile_vector_cannot_be_adjusted.value
    if "projectiles_have_identical_error" in active_h1_flags:
        flags += BarrelFlags.projectiles_have_identical_error.value
    if "projectiles_fire_parallel" in active_h1_flags:
        flags += BarrelFlags.projectiles_fire_parallel.value

    return flags

def generate_fire_recovery(trigger_element):
    rate_of_fire = trigger_element.rounds_per_second[1]

    result = 0.0
    if rate_of_fire > 0.0001:
        result = (30 / rate_of_fire) / 30
        if result < 0.1:
            result = 0

    return result

def get_valid_h1_weapon_functions(function_name):
    valid_function_name = ""
    if function_name == "ready":
        valid_function_name = "ready"
    elif function_name == "heat":
        valid_function_name = "heat"
    elif function_name == "overheated":
        valid_function_name = "overheated"
    elif function_name == "illumination":
        valid_function_name = "illumination"
    elif function_name == "primary_ammunition":
        valid_function_name = "primary_ammunition"
    elif function_name == "secondary_ammunition":
        valid_function_name = "secondary_ammunition"
    elif function_name == "primary_ejection_port":
        valid_function_name = "primary_ejection_port"
    elif function_name == "secondary_ejection_port":
        valid_function_name = "secondary_ejection_port"
    elif function_name == "primary_rate_of_fire":
        valid_function_name = "primary_rate_of_fire"
    elif function_name == "secondary_rate_of_fire":
        valid_function_name = "secondary_rate_of_fire"
    elif function_name == "primary_firing_on":
        valid_function_name = "primary_firing"
    elif function_name == "secondary_firing_on":
        valid_function_name = "secondary_firing"
    elif function_name == "primary_charged":
        valid_function_name = "primary_charged"
    elif function_name == "secondary_charged":
        valid_function_name = "secondary_charged"
    elif function_name == "integrated_light":
        valid_function_name = "integrated_light"
    elif function_name == "age":
        valid_function_name = "age"
    return valid_function_name

class WeaponAsset(ItemAsset):
    def __init__(self, weapon_flags=0, label="", secondary_trigger_mode=0, maximum_alternate_shots_loaded=0, weapon_a_in=0, weapon_b_in=0, weapon_c_in=0, weapon_d_in=0,
                     ready_time=0.0, ready_effect=None, heat_recovery_threshold=0.0, overheated_threshold=0.0, heat_detonation_threshold=0.0, heat_detonation_fraction=0.0,
                     heat_loss_per_second=0.0, heat_illumination=0.0, overheated=None, detonation=None, player_melee_damage=None, player_melee_response=None,
                     actor_firing_parameters=None, near_reticle_range=0.0, far_reticle_range=0.0, intersection_reticle_range=0.0, magnification_levels=0,
                     magnification_range=(0.0, 0.0), autoaim_angle=0.0, autoaim_range=0.0, magnetism_angle=0.0, magnetism_range=0.0, deviation_angle=0.0, movement_penalized=0,
                     forward_movement_penalty=0.0, sideways_movement_penalty=0.0, minimum_target_range=0.0, looking_time_modifier=0.0, light_power_on_time=0.0,
                     light_power_off_time=0.0, light_power_on_effect=None, light_power_off_effect=None, age_heat_recovery_penalty=0.0, age_rate_of_fire_penalty=0.0,
                     age_misfire_start=0.0, age_misfire_chance=0.0, first_person_model=None, first_person_animations=None, hud_interface=None, pickup_sound=None,
                     zoom_in_sound=None, zoom_out_sound=None, active_camo_ding=0.0, active_camo_regrowth_rate=0.0, weapon_type=0, weapon_predicted_resources_tag_block=None,
                     magazines_tag_block=None, triggers_tag_block=None, weapon_predicted_resources=None, magazines=None, triggers=None):
        super().__init__()
        self.header = None
        self.weapon_flags = weapon_flags
        self.label = label
        self.secondary_trigger_mode = secondary_trigger_mode
        self.maximum_alternate_shots_loaded = maximum_alternate_shots_loaded
        self.weapon_a_in = weapon_a_in
        self.weapon_b_in = weapon_b_in
        self.weapon_c_in = weapon_c_in
        self.weapon_d_in = weapon_d_in
        self.ready_time = ready_time
        self.ready_effect = ready_effect
        self.heat_recovery_threshold = heat_recovery_threshold
        self.overheated_threshold = overheated_threshold
        self.heat_detonation_threshold = heat_detonation_threshold
        self.heat_detonation_fraction = heat_detonation_fraction
        self.heat_loss_per_second = heat_loss_per_second
        self.heat_illumination = heat_illumination
        self.overheated = overheated
        self.detonation = detonation
        self.player_melee_damage = player_melee_damage
        self.player_melee_response = player_melee_response
        self.actor_firing_parameters = actor_firing_parameters
        self.near_reticle_range = near_reticle_range
        self.far_reticle_range = far_reticle_range
        self.intersection_reticle_range = intersection_reticle_range
        self.magnification_levels = magnification_levels
        self.magnification_range = magnification_range
        self.autoaim_angle = autoaim_angle
        self.autoaim_range = autoaim_range
        self.magnetism_angle = magnetism_angle
        self.magnetism_range = magnetism_range
        self.deviation_angle = deviation_angle
        self.movement_penalized = movement_penalized
        self.forward_movement_penalty = forward_movement_penalty
        self.sideways_movement_penalty = sideways_movement_penalty
        self.minimum_target_range = minimum_target_range
        self.looking_time_modifier = looking_time_modifier
        self.light_power_on_time = light_power_on_time
        self.light_power_off_time = light_power_off_time
        self.light_power_on_effect = light_power_on_effect
        self.light_power_off_effect = light_power_off_effect
        self.age_heat_recovery_penalty = age_heat_recovery_penalty
        self.age_rate_of_fire_penalty = age_rate_of_fire_penalty
        self.age_misfire_start = age_misfire_start
        self.age_misfire_chance = age_misfire_chance
        self.first_person_model = first_person_model
        self.first_person_animations = first_person_animations
        self.hud_interface = hud_interface
        self.pickup_sound = pickup_sound
        self.zoom_in_sound = zoom_in_sound
        self.zoom_out_sound = zoom_out_sound
        self.active_camo_ding = active_camo_ding
        self.active_camo_regrowth_rate = active_camo_regrowth_rate
        self.weapon_type = weapon_type
        self.weapon_predicted_resources_tag_block = weapon_predicted_resources_tag_block
        self.magazines_tag_block = magazines_tag_block
        self.triggers_tag_block = triggers_tag_block
        self.weapon_predicted_resources = weapon_predicted_resources
        self.magazines = magazines
        self.triggers = triggers

    class MagazineStats:
        def __init__(self, flags=0, rounds_recharged=0, rounds_total_initial=0, rounds_total_maximum=0, rounds_loaded_maximum=0, reload_time=0.0,
                     rounds_reloaded=0, chamber_time=0.0, reloading_effect=None, chambering_effect=None, magazines_tag_block=None, magazines=None):
            self.flags = flags
            self.rounds_recharged = rounds_recharged
            self.rounds_total_initial = rounds_total_initial
            self.rounds_total_maximum = rounds_total_maximum
            self.rounds_loaded_maximum = rounds_loaded_maximum
            self.reload_time = reload_time
            self.rounds_reloaded = rounds_reloaded
            self.chamber_time = chamber_time
            self.reloading_effect = reloading_effect
            self.chambering_effect = chambering_effect
            self.magazines_tag_block = magazines_tag_block
            self.magazines = magazines

    class Magazine:
        def __init__(self, rounds=0, equipment=None):
            self.rounds = rounds
            self.equipment = equipment

    class Trigger:
        def __init__(self, flags=0, rounds_per_second=(0.0, 0.0), firing_acceleration_time=0.0, firing_deceleration_time=0.0, blurred_rate_of_fire=0.0, magazine=0,
                     rounds_per_shot=0, minimum_rounds_loaded=0, rounds_between_tracers=0, prediction_type=0, firing_noise=0, error=(0.0, 0.0), error_acceleration_time=0.0,
                     error_deceleration_time=0.0, charging_time=0.0, charged_time=0.0, overcharged_action=0, charged_illumination=0.0, spew_time=0.0, charging_effect=None,
                     distribution_function=0, projectiles_per_shot=0, distribution_angle=0.0, minimum_error=0.0, error_angle=(0.0, 0.0), first_person_offset=Vector(),
                     projectile=None, ejection_port_recovery_time=0.0, illumination_recovery_time=0.0, heat_generated_per_round=0.0, age_generated_per_round=0.0,
                     overload_time=0.0, firing_effects_tag_block=None, firing_effects=None):
            self.flags = flags
            self.rounds_per_second = rounds_per_second
            self.firing_acceleration_time = firing_acceleration_time
            self.firing_deceleration_time = firing_deceleration_time
            self.blurred_rate_of_fire = blurred_rate_of_fire
            self.magazine = magazine
            self.rounds_per_shot = rounds_per_shot
            self.minimum_rounds_loaded = minimum_rounds_loaded
            self.rounds_between_tracers = rounds_between_tracers
            self.prediction_type = prediction_type
            self.firing_noise = firing_noise
            self.error = error
            self.error_acceleration_time = error_acceleration_time
            self.error_deceleration_time = error_deceleration_time
            self.charging_time = charging_time
            self.charged_time = charged_time
            self.overcharged_action = overcharged_action
            self.charged_illumination = charged_illumination
            self.spew_time = spew_time
            self.charging_effect = charging_effect
            self.distribution_function = distribution_function
            self.projectiles_per_shot = projectiles_per_shot
            self.distribution_angle = distribution_angle
            self.minimum_error = minimum_error
            self.error_angle = error_angle
            self.first_person_offset = first_person_offset
            self.projectile = projectile
            self.ejection_port_recovery_time = ejection_port_recovery_time
            self.illumination_recovery_time = illumination_recovery_time
            self.heat_generated_per_round = heat_generated_per_round
            self.age_generated_per_round = age_generated_per_round
            self.overload_time = overload_time
            self.firing_effects_tag_block = firing_effects_tag_block
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
