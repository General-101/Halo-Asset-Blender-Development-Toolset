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
    brute = 0
    grunt = auto()
    jackal = auto()

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

class VehicleFlags(Flag):
    speed_wakes_physics = auto()
    turn_wakes_physics = auto()
    driver_power_wakes_physics = auto()
    gunner_power_wakes_physics = auto()
    control_opposite_speed_sets_brake = auto()
    slide_wakes_physics = auto()
    kills_riders_at_terminal_velocity = auto()
    causes_collision_damage = auto()
    ai_weapon_cannot_rotate = auto()
    ai_does_not_require_driver = auto()
    ai_unused = auto()
    ai_driver_enable = auto()
    ai_driver_flying = auto()
    ai_driver_can_sidestep = auto()
    ai_driver_hovering = auto()
    vehicle_steers_directly = auto()
    unused = auto()
    has_e_brake = auto()
    noncombat_vehicle = auto()
    no_friction_with_driver = auto()
    can_trigger_automatic_opening_door = auto()
    autoaim_when_teamless = auto()

class VehicleTypeEnum(Enum):
    human_tank = 0
    human_jeep = auto()
    human_boat = auto()
    human_plane = auto()
    human_scout = auto()
    human_fighter = auto()
    turret = auto()

class VehicleFunctionEnum(Enum):
    none = 0
    speed_absolute = auto()
    speed_forward = auto()
    speed_backward = auto()
    slide_absolute = auto()
    slide_left = auto()
    slide_right = auto()
    speed_slide_maximum = auto()
    turn_absolute = auto()
    turn_left = auto()
    turn_right = auto()
    crouch = auto()
    jump = auto()
    walk = auto()
    velocity_air = auto()
    velocity_water = auto()
    velocity_ground = auto()
    velocity_forward = auto()
    velocity_left = auto()
    velocity_up = auto()
    left_thread_position = auto()
    right_thread_position = auto()
    left_thread_velocity = auto()
    right_thread_velocity = auto()
    front_left_tire_position = auto()
    front_right_tire_position = auto()
    back_left_tire_position = auto()
    back_right_tire_position = auto()
    front_left_tire_velocity = auto()
    front_right_tire_velocity = auto()
    back_left_tire_velocity = auto()
    back_right_tire_velocity = auto()
    wingtip_contrail = auto()
    hover = auto()
    thrust = auto()
    engine_hack = auto()
    wingtip_contrail_new = auto()

class VehicleAsset():
    def __init__(self):
        self.header = None
        self.vehicle_body = None
        self.attachments = None
        self.widgets = None
        self.functions = None
        self.change_colors = None
        self.predicted_resources = None
        self.camera_tracks = None
        self.new_hud_interface = None
        self.dialogue_variants = None
        self.powered_seats = None
        self.weapons = None
        self.seats = None

    class VehicleBody:
        def __init__(self, object_flags=0, bounding_radius=0.0, bounding_offset=Vector(), origin_offset=Vector(), acceleration_scale=0.0, model=None, animation_graph=None,
                     collision_model=None, physics=None, modifier_shader=None, creation_effect=None, render_bounding_radius=0.0, object_a_in=0, object_b_in=0, object_c_in=0,
                     object_d_in=0, hud_text_message_index=0, forced_shader_permutation_index=0, attachments_tag_block=None, widgets_tag_block=None, functions_tag_block=None,
                     change_colors_tag_block=None, predicted_resources_tag_block=None, unit_flags=0, default_team=0, constant_sound_volume=0, rider_damage_fraction=0.0,
                     integrated_light_toggle=None, unit_a_in=0, unit_b_in=0, unit_c_in=0, unit_d_in=0, camera_field_of_view=0.0, camera_stiffness=0.0, camera_marker_name="",
                     camera_submerged_marker_name="", pitch_auto_level=0.0, pitch_range=(0.0, 0.0), camera_tracks_tag_block=None, seat_acceleration_scale=Vector(),
                     soft_ping_threshold=0.0, soft_ping_interrupt_time=0.0, hard_ping_threshold=0.0, hard_ping_interrupt_time=0.0, hard_death_threshold=0.0, feign_death_threshold=0.0,
                     feign_death_time=0.0, distance_of_evade_anim=0.0, distance_of_dive_anim=0.0, stunned_movement_threshold=0.0, feign_death_chance=0.0, feign_repeat_chance=0.0,
                     spawned_actor=None, spawned_actor_count=(0, 0), spawned_velocity=0.0, aiming_velocity_maximum=0.0, aiming_acceleration_maximum=0.0, casual_aiming_modifier=0.0,
                     looking_velocity_maximum=0.0, looking_acceleration_maximum=0.0, ai_vehicle_radius=0.0, ai_danger_radius=0.0, melee_damage=None, motion_sensor_blip_size=0,
                     metagame_type=0, metagame_class=0, new_hud_interfaces_tag_block=None, dialogue_variants_tag_block=None, grenade_velocity=0.0, grenade_type=0, grenade_count=0,
                     powered_seats_tag_block=None, weapons_tag_block=None, seats_tag_block=None, vehicle_flags=0, vehicle_type=0, maximum_forward_speed=0.0, maximum_reverse_speed=0.0,
                     speed_acceleration=0.0, speed_deceleration=0.0, maximum_left_turn=0.0, maximum_right_turn_negative=0.0, wheel_circumference=0.0, turn_rate=0.0, blur_speed=0.0,
                     vehicle_a_in=0, vehicle_b_in=0, vehicle_c_in=0, vehicle_d_in=0, maximum_left_slide=0.0, maximum_right_slide=0.0, slide_acceleration=0.0, slide_deceleration=0.0,
                     minimum_flipping_angular_velocity=0.0, maximum_flipping_angular_velocity=0.0, fixed_gun_yaw=0.0, fixed_gun_pitch=0.0, ai_sideslip_distance=0.0,
                     ai_destination_radius=0.0, ai_avoidance_distance=0.0, ai_pathfinding_radius=0.0, ai_charge_repeat_timeout=0.0, ai_strafing_abort_range=0.0,
                     ai_overstepping_bounds=0.0, ai_steering_maximum=0.0, ai_throttle_maximum=0.0, ai_move_position_time=0.0, suspension_sound=None, crash_sound=None,
                     material_effects=None, effect=None):
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
            self.vehicle_flags = vehicle_flags
            self.vehicle_type = vehicle_type
            self.maximum_forward_speed = maximum_forward_speed
            self.maximum_reverse_speed = maximum_reverse_speed
            self.speed_acceleration = speed_acceleration
            self.speed_deceleration = speed_deceleration
            self.maximum_left_turn = maximum_left_turn
            self.maximum_right_turn_negative = maximum_right_turn_negative
            self.wheel_circumference = wheel_circumference
            self.turn_rate = turn_rate
            self.blur_speed = blur_speed
            self.vehicle_a_in = vehicle_a_in
            self.vehicle_b_in = vehicle_b_in
            self.vehicle_c_in = vehicle_c_in
            self.vehicle_d_in = vehicle_d_in
            self.maximum_left_slide = maximum_left_slide
            self.maximum_right_slide = maximum_right_slide
            self.slide_acceleration = slide_acceleration
            self.slide_deceleration = slide_deceleration
            self.minimum_flipping_angular_velocity = minimum_flipping_angular_velocity
            self.maximum_flipping_angular_velocity = maximum_flipping_angular_velocity
            self.fixed_gun_yaw = fixed_gun_yaw
            self.fixed_gun_pitch = fixed_gun_pitch
            self.ai_sideslip_distance = ai_sideslip_distance
            self.ai_destination_radius = ai_destination_radius
            self.ai_avoidance_distance = ai_avoidance_distance
            self.ai_pathfinding_radius = ai_pathfinding_radius
            self.ai_charge_repeat_timeout = ai_charge_repeat_timeout
            self.ai_strafing_abort_range = ai_strafing_abort_range
            self.ai_overstepping_bounds = ai_overstepping_bounds
            self.ai_steering_maximum = ai_steering_maximum
            self.ai_throttle_maximum = ai_throttle_maximum
            self.ai_move_position_time = ai_move_position_time
            self.suspension_sound = suspension_sound
            self.crash_sound = crash_sound
            self.material_effects = material_effects
            self.effect = effect
