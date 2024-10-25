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

class UnitFlags(Flag):
    circular_aiming = auto()
    destroyed_after_dying = auto()
    half_speed_interpolation = auto()
    fires_from_camera = auto()
    entrance_inside_bounding_sphere = auto()
    unused = auto()
    causes_passenger_dialogue = auto()
    resists_ping = auto()
    melee_attack_is_fatal = auto()
    dont_reface_during_pings = auto()
    has_no_aiming = auto()
    simple_creature = auto()
    impact_melee_attaches_to_unit = auto()
    impact_melee_dies_on_shield = auto()
    cannot_open_doors_automatically = auto()
    melee_attackers_cannot_attach = auto()
    not_instantly_killed_by_melee = auto()
    shield_sapping = auto()
    runs_around_flaming = auto()
    inconsequential = auto()
    special_cinematic_unit = auto()
    ignored_by_autoaiming = auto()
    shields_fry_infection_forms = auto()
    integrated_light_controls_weapon = auto()
    integrated_light_lasts_forever = auto()

class TeamsEnum(Enum):
    none = 0
    player = auto()
    human = auto()
    covenant = auto()
    flood = auto()
    sentinel = auto()
    unused_6 = auto()
    unused_7 = auto()
    unused_8 = auto()
    unused_9 = auto()

class ConstantSoundVolumeEnum(Enum):
    silent = 0
    medium = auto()
    loud = auto()
    shout = auto()
    quiet = auto()

class UnitFunctionEnum(Enum):
    none = 0
    driver_seat_power = auto()
    gunner_seat_power = auto()
    aiming_change = auto()
    mouth_aperture = auto()
    integrated_light_power = auto()
    can_blink = auto()
    shield_sapping = auto()

class MotionSensorBlipSizeEnum(Enum):
    medium = 0
    small = auto()
    large = auto()

class MetaGameTypeEnum(Enum):
    brute = 0
    grunt = auto()
    jackal = auto()
    skirmisher = auto()
    marine = auto()
    spartan = auto()
    bugger = auto()
    hunter = auto()
    flood_infection = auto()
    flood_carrier = auto()
    flood_combat = auto()
    flood_pure = auto()
    sentinel = auto()
    elite = auto()
    engineer = auto()
    mule = auto()
    turret = auto()
    mongoose = auto()
    warthog = auto()
    scorpion = auto()
    hornet = auto()
    pelican = auto()
    revenant = auto()
    seraph = auto()
    shade = auto()
    watchtower = auto()
    ghost = auto()
    chopper = auto()
    mauler = auto()
    wraith = auto()
    banshee = auto()
    phantom = auto()
    scarab = auto()
    guntower = auto()
    tuning_fork = auto()
    broadsword = auto()
    mammoth = auto()
    lich = auto()
    mantis = auto()
    wasp = auto()
    phaeton = auto()
    bishop = auto()
    knight = auto()
    pawn = auto()

class MetaGameClassEnum(Enum):
    infantry = 0
    leader = auto()
    hero = auto()
    specialist = auto()
    light_vehicle = auto()
    heavy_vehicle = auto()
    giant_vehicle = auto()
    standard_vehicle = auto()

class GrenadeTypeEnum(Enum):
    human_fragmentation = 0
    covenant_plasma = auto()
    grenade_type_2 = auto()
    grenade_type_3 = auto()

class BipedFlags(Flag):
    turns_without_animating = auto()
    uses_player_physics = auto()
    flying = auto()
    physics_pill_centered_at_origin = auto()
    spherical = auto()
    passes_through_other_bipeds = auto()
    can_climb_any_surface = auto()
    immune_to_falling_damage = auto()
    rotate_while_airborne = auto()
    uses_limp_body_physics = auto()
    has_no_dying_airborne = auto()
    random_speed_increase = auto()
    unit_uses_old_ntsc_player_physics = auto()

class BipedFunctionEnum(Enum):
    none = 0
    flying_velocity = auto()

class BipedAsset():
    def __init__(self, header=None, attachments=None, widgets=None, functions=None, change_colors=None, predicted_resources=None, camera_tracks=None, new_hud_interface=None, 
                 dialogue_variants=None, powered_seats=None, weapons=None, seats=None, contact_points=None, object_flags=0, bounding_radius=0.0, bounding_offset=Vector(), 
                 origin_offset=Vector(), acceleration_scale=0.0, model=None, animation_graph=None, collision_model=None, physics=None, modifier_shader=None, 
                 creation_effect=None, render_bounding_radius=0.0, object_a_in=0, object_b_in=0, object_c_in=0, object_d_in=0, hud_text_message_index=0, 
                 forced_shader_permutation_index=0, attachments_tag_block=None, widgets_tag_block=None, functions_tag_block=None, change_colors_tag_block=None, 
                 predicted_resources_tag_block=None, unit_flags=0, default_team=0, constant_sound_volume=0, rider_damage_fraction=0.0, integrated_light_toggle=None, 
                 unit_a_in=0, unit_b_in=0, unit_c_in=0, unit_d_in=0, camera_field_of_view=0.0, camera_stiffness=0.0, camera_marker_name="", camera_submerged_marker_name="", 
                 pitch_auto_level=0.0, pitch_range=(0.0, 0.0), camera_tracks_tag_block=None, seat_acceleration_scale=Vector(), soft_ping_threshold=0.0, 
                 soft_ping_interrupt_time=0.0, hard_ping_threshold=0.0, hard_ping_interrupt_time=0.0, hard_death_threshold=0.0, feign_death_threshold=0.0, 
                 feign_death_time=0.0, distance_of_evade_anim=0.0, distance_of_dive_anim=0.0, stunned_movement_threshold=0.0, feign_death_chance=0.0, 
                 feign_repeat_chance=0.0, spawned_actor=None, spawned_actor_count=(0, 0), spawned_velocity=0.0, aiming_velocity_maximum=0.0, aiming_acceleration_maximum=0.0, 
                 casual_aiming_modifier=0.0, looking_velocity_maximum=0.0, looking_acceleration_maximum=0.0, ai_vehicle_radius=0.0, ai_danger_radius=0.0, melee_damage=None, 
                 motion_sensor_blip_size=0, metagame_type=0, metagame_class=0, new_hud_interfaces_tag_block=None, dialogue_variants_tag_block=None, grenade_velocity=0.0, 
                 grenade_type=0, grenade_count=0, powered_seats_tag_block=None, weapons_tag_block=None, seats_tag_block=None, moving_turning_speed=0.0, biped_flags=0, 
                 stationary_turning_threshold=0.0, biped_a_in=0, biped_b_in=0, biped_c_in=0, biped_d_in=0, dont_use=None, bank_angle=0.0, bank_apply_time=0.0, 
                 bank_decay_time=0.0, pitch_ratio=0.0, max_velocity=0.0, max_sidestep_velocity=0.0, acceleration=0.0, deceleration=0.0, angular_velocity_maximum=0.0, 
                 angular_acceleration_maximum=0.0, crouch_velocity_modifier=0.0, maximum_slope_angle=0.0, downhill_falloff_angle=0.0, downhill_cuttoff_angle=0.0, 
                 downhill_velocity_scale=0.0, uphill_falloff_angle=0.0, uphill_cuttoff_angle=0.0, uphill_velocity_scale=0.0, footsteps=None, jump_velocity=0.0, 
                 maximum_soft_landing_time=0.0, maximum_hard_landing_time=0.0, minimum_soft_landing_velocity=0.0, minimum_hard_landing_velocity=0.0, 
                 maximum_hard_landing_velocity=0.0, death_hard_landing_velocity=0.0, standing_camera_height=0.0, crouching_camera_height=0.0, crouch_transition_time=0.0, 
                 standing_collision_height=0.0, crouching_collision_height=0.0, collision_radius=0.0, autoaim_width=0.0, contact_points_tag_block=None):
        self.header = header
        self.attachments = attachments
        self.widgets = widgets
        self.functions = functions
        self.change_colors = change_colors
        self.predicted_resources = predicted_resources
        self.camera_tracks = camera_tracks
        self.new_hud_interface = new_hud_interface
        self.dialogue_variants = dialogue_variants
        self.powered_seats = powered_seats
        self.weapons = weapons
        self.seats = seats
        self.contact_points = contact_points
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
        self.predicted_resources_tag_block = predicted_resources_tag_block
        self.unit_flags = unit_flags
        self.default_team = default_team
        self.constant_sound_volume = constant_sound_volume
        self.rider_damage_fraction = rider_damage_fraction
        self.integrated_light_toggle = integrated_light_toggle
        self.unit_a_in = unit_a_in
        self.unit_b_in = unit_b_in
        self.unit_c_in = unit_c_in
        self.unit_d_in = unit_d_in
        self.camera_field_of_view = camera_field_of_view
        self.camera_stiffness = camera_stiffness
        self.camera_marker_name = camera_marker_name
        self.camera_submerged_marker_name = camera_submerged_marker_name
        self.pitch_auto_level = pitch_auto_level
        self.pitch_range = pitch_range
        self.camera_tracks_tag_block = camera_tracks_tag_block
        self.seat_acceleration_scale = seat_acceleration_scale
        self.soft_ping_threshold = soft_ping_threshold
        self.soft_ping_interrupt_time = soft_ping_interrupt_time
        self.hard_ping_threshold = hard_ping_threshold
        self.hard_ping_interrupt_time = hard_ping_interrupt_time
        self.hard_death_threshold = hard_death_threshold
        self.feign_death_threshold = feign_death_threshold
        self.feign_death_time = feign_death_time
        self.distance_of_evade_anim = distance_of_evade_anim
        self.distance_of_dive_anim = distance_of_dive_anim
        self.stunned_movement_threshold = stunned_movement_threshold
        self.feign_death_chance = feign_death_chance
        self.feign_repeat_chance = feign_repeat_chance
        self.spawned_actor = spawned_actor
        self.spawned_actor_count = spawned_actor_count
        self.spawned_velocity = spawned_velocity
        self.aiming_velocity_maximum = aiming_velocity_maximum
        self.aiming_acceleration_maximum = aiming_acceleration_maximum
        self.casual_aiming_modifier = casual_aiming_modifier
        self.looking_velocity_maximum = looking_velocity_maximum
        self.looking_acceleration_maximum = looking_acceleration_maximum
        self.ai_vehicle_radius = ai_vehicle_radius
        self.ai_danger_radius = ai_danger_radius
        self.melee_damage = melee_damage
        self.motion_sensor_blip_size = motion_sensor_blip_size
        self.metagame_type = metagame_type
        self.metagame_class = metagame_class
        self.new_hud_interfaces_tag_block = new_hud_interfaces_tag_block
        self.dialogue_variants_tag_block = dialogue_variants_tag_block
        self.grenade_velocity = grenade_velocity
        self.grenade_type = grenade_type
        self.grenade_count = grenade_count
        self.powered_seats_tag_block = powered_seats_tag_block
        self.weapons_tag_block = weapons_tag_block
        self.seats_tag_block = seats_tag_block
        self.moving_turning_speed = moving_turning_speed
        self.biped_flags = biped_flags
        self.stationary_turning_threshold = stationary_turning_threshold
        self.biped_a_in = biped_a_in
        self.biped_b_in = biped_b_in
        self.biped_c_in = biped_c_in
        self.biped_d_in = biped_d_in
        self.dont_use = dont_use
        self.bank_angle = bank_angle
        self.bank_apply_time = bank_apply_time
        self.bank_decay_time = bank_decay_time
        self.pitch_ratio = pitch_ratio
        self.max_velocity = max_velocity
        self.max_sidestep_velocity = max_sidestep_velocity
        self.acceleration = acceleration
        self.deceleration = deceleration
        self.angular_velocity_maximum = angular_velocity_maximum
        self.angular_acceleration_maximum = angular_acceleration_maximum
        self.crouch_velocity_modifier = crouch_velocity_modifier
        self.maximum_slope_angle = maximum_slope_angle
        self.downhill_falloff_angle = downhill_falloff_angle
        self.downhill_cuttoff_angle = downhill_cuttoff_angle
        self.downhill_velocity_scale = downhill_velocity_scale
        self.uphill_falloff_angle = uphill_falloff_angle
        self.uphill_cuttoff_angle = uphill_cuttoff_angle
        self.uphill_velocity_scale = uphill_velocity_scale
        self.footsteps = footsteps
        self.jump_velocity = jump_velocity
        self.maximum_soft_landing_time = maximum_soft_landing_time
        self.maximum_hard_landing_time = maximum_hard_landing_time
        self.minimum_soft_landing_velocity = minimum_soft_landing_velocity
        self.minimum_hard_landing_velocity = minimum_hard_landing_velocity
        self.maximum_hard_landing_velocity = maximum_hard_landing_velocity
        self.death_hard_landing_velocity = death_hard_landing_velocity
        self.standing_camera_height = standing_camera_height
        self.crouching_camera_height = crouching_camera_height
        self.crouch_transition_time = crouch_transition_time
        self.standing_collision_height = standing_collision_height
        self.crouching_collision_height = crouching_collision_height
        self.collision_radius = collision_radius
        self.autoaim_width = autoaim_width
        self.contact_points_tag_block = contact_points_tag_block
