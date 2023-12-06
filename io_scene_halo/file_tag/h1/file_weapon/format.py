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
    transparent_self_occlusion = auto()
    brighter_than_it_should_be = auto()
    not_a_pathfinding_obstacle = auto()
    extension_of_parent = auto()
    cast_shadow_by_default = auto()
    does_not_have_remastered_geometry = auto()

class ObjectFunctionEnum(Enum):
    none = 0
    body_vitality = auto()
    shield_vitality = auto()
    recent_body_damage = auto()
    recent_shield_damage = auto()
    random_constant = auto()
    umbrella_shield_vitality = auto()
    shield_stun = auto()
    recent_umbrella_shield_vitality = auto()
    umbrella_shield_stun = auto()
    region_00_damage = auto()
    region_01_damage = auto()
    region_02_damage = auto()
    region_03_damage = auto()
    region_04_damage = auto()
    region_05_damage = auto()
    region_06_damage = auto()
    region_07_damage = auto()
    alive = auto()
    compass = auto()

class ItemFlags(Flag):
    always_maintains_z_up = auto()
    destroyed_by_explosions = auto()
    unaffected_by_gravity = auto()

class ItemFunctionEnum(Enum):
    none = 0

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

class WeaponAsset():
    def __init__(self):
        self.header = None
        self.weapon_body = None
        self.attachments = None
        self.widgets = None
        self.functions = None
        self.change_colors = None
        self.object_predicted_resources = None
        self.weapon_predicted_resources = None
        self.magazines = None
        self.triggers = None

    class WeaponBody:
        def __init__(self, object_flags=0, bounding_radius=0.0, bounding_offset=Vector(), origin_offset=Vector(), acceleration_scale=0.0, model=None, animation_graph=None, 
                     collision_model=None, physics=None, modifier_shader=None, creation_effect=None, render_bounding_radius=0.0, object_a_in=0, object_b_in=0, object_c_in=0, 
                     object_d_in=0, hud_text_message_index=0, forced_shader_permutation_index=0, attachments_tag_block=None, widgets_tag_block=None, functions_tag_block=None, 
                     change_colors_tag_block=None, object_predicted_resources_tag_block=None, item_flags=0, message_index=0, sort_order=0, scale=0.0, hud_message_value_scale=0, 
                     item_a_in=0, item_b_in=0, item_c_in=0, item_d_in=0, material_effects=None, collision_sound=None, detonation_delay=(0.0, 0.0), detonating_effect=None, 
                     detonation_effect=None, weapon_flags=0, label="", secondary_trigger_mode=0, maximum_alternate_shots_loaded=0, weapon_a_in=0, weapon_b_in=0, weapon_c_in=0, 
                     weapon_d_in=0, ready_time=0.0, ready_effect=None, heat_recovery_threshold=0.0, overheated_threshold=0.0, heat_detonation_threshold=0.0, 
                     heat_detonation_fraction=0.0, heat_loss_per_second=0.0, heat_illumination=0.0, overheated=None, detonation=None, player_melee_damage=None, 
                     player_melee_response=None, actor_firing_parameters=None, near_reticle_range=0.0, far_reticle_range=0.0, intersection_reticle_range=0.0, magnification_levels=0, 
                     magnification_range=(0.0, 0.0), autoaim_angle=0.0, autoaim_range=0.0, magnetism_angle=0.0, magnetism_range=0.0, deviation_angle=0.0, movement_penalized=0, 
                     forward_movement_penalty=0.0, sideways_movement_penalty=0.0, minimum_target_range=0.0, looking_time_modifier=0.0, light_power_on_time=0.0, 
                     light_power_off_time=0.0, light_power_on_effect=None, light_power_off_effect=None, age_heat_recovery_penalty=0.0, age_rate_of_fire_penalty=0.0, 
                     age_misfire_start=0.0, age_misfire_chance=0.0, first_person_model=None, first_person_animations=None, hud_interface=None, pickup_sound=None, zoom_in_sound=None, 
                     zoom_out_sound=None, active_camo_ding=0.0, active_camo_regrowth_rate=0.0, weapon_type=0, weapon_predicted_resources_tag_block=None, magazines_tag_block=None, 
                     triggers_tag_block=None):
            self.object_flags = object_flags
            self.bounding_radius = bounding_radius
            self.bounding_offset = bounding_offset
            self.origin_offset = origin_offset
            self.acceleration_scale = acceleration_scale
            self.model = model
            self.animation_graph = animation_graph
            self.collision_model = collision_model
            self.physics = physics
            self.modifier_shader = modifier_shader
            self.creation_effect = creation_effect
            self.render_bounding_radius = render_bounding_radius
            self.object_a_in = object_a_in
            self.object_b_in = object_b_in
            self.object_c_in = object_c_in
            self.object_d_in = object_d_in
            self.hud_text_message_index = hud_text_message_index
            self.forced_shader_permutation_index = forced_shader_permutation_index
            self.attachments_tag_block = attachments_tag_block
            self.widgets_tag_block = widgets_tag_block
            self.functions_tag_block = functions_tag_block
            self.change_colors_tag_block = change_colors_tag_block
            self.object_predicted_resources_tag_block = object_predicted_resources_tag_block
            self.item_flags = item_flags
            self.message_index = message_index
            self.sort_order = sort_order
            self.scale = scale
            self.hud_message_value_scale = hud_message_value_scale
            self.item_a_in = item_a_in
            self.item_b_in = item_b_in
            self.item_c_in = item_c_in
            self.item_d_in = item_d_in
            self.material_effects = material_effects
            self.collision_sound = collision_sound
            self.detonation_delay = detonation_delay
            self.detonating_effect = detonating_effect
            self.detonation_effect = detonation_effect
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
