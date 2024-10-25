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
from ..file_object.format import ObjectAsset

class UnitFlags(Flag):
    circular_aiming = auto()
    destroyed_after_dying = auto()
    half_speed_interpolation = auto()
    fires_from_camera = auto()
    entrance_inside_bounding_sphere = auto()
    doesnt_show_readid_weapon = auto()
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
    unused_17 = auto()
    runs_around_flaming = auto()
    inconsequential = auto()
    special_cinematic_unit = auto()
    ignored_by_autoaiming = auto()
    shields_fry_infection_forms = auto()
    unused_23 = auto()
    unused_24 = auto()
    acts_as_gunner_for_parent = auto()
    controlled_by_parent_gunner = auto()
    parents_primary_weapon = auto()
    unit_has_boost = auto()

class TeamsEnum(Enum):
    default = 0
    player = auto()
    human = auto()
    covenant = auto()
    flood = auto()
    sentinel = auto()
    heretic = auto()
    prophet = auto()
    unused_8 = auto()
    unused_9 = auto()
    unused_10 = auto()
    unused_11 = auto()
    unused_12 = auto()
    unused_13 = auto()
    unused_14 = auto()
    unused_15 = auto()

class ConstantSoundVolumeEnum(Enum):
    silent = 0
    medium = auto()
    loud = auto()
    shout = auto()
    quiet = auto()

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

class SeatFlags(Flag):
    invisible = auto()
    unused1 = auto()
    driver = auto()
    gunner = auto()
    third_person_camera = auto()
    allows_weapons = auto()
    third_person_on_enter = auto()
    first_person_camera_slaved_to_gun = auto()
    unused8 = auto()
    not_valid_without_driver = auto()
    allow_al_noncombatants = auto()
    boarding_seat = auto()
    ai_firing_disabled_by_max_acceleration = auto()
    boarding_enters_seat = auto()
    boarding_need_any_passenger = auto()
    controls_open_and_close = auto()
    invalid_for_player = auto()
    invalid_for_non_player = auto()
    gunner_player_only = auto()
    invisible_under_major_damage = auto()

class UnitAsset(ObjectAsset):
    def __init__(self, camera_tracks_header=None, camera_tracks=None, postures_header=None, postures=None, new_hud_interface_header=None, new_hud_interface=None, 
                 dialogue_variants_header=None, dialogue_variants=None, powered_seats_header=None, powered_seats=None, weapons_header=None, weapons=None, seats_header=None, 
                 seats=None, unit_flags=0, default_team=0, constant_sound_volume=0, integrated_light_toggle=None, camera_field_of_view=0.0, camera_stiffness=0.0, 
                 camera_marker_name="", camera_marker_name_length=0, camera_submerged_marker_name="", camera_submerged_marker_name_length=0, pitch_auto_level=0.0, 
                 pitch_range=(0.0, 0.0), camera_tracks_tag_block=None, acceleration_range=Vector(), acceleration_action_scale=0.0, acceleration_attach_scale=0.0, 
                 soft_ping_threshold=0.0, soft_ping_interrupt_time=0.0, hard_ping_threshold=0.0, hard_ping_interrupt_time=0.0, hard_death_threshold=0.0, 
                 feign_death_threshold=0.0, feign_death_time=0.0, distance_of_evade_anim=0.0, distance_of_dive_anim=0.0, stunned_movement_threshold=0.0, 
                 feign_death_chance=0.0, feign_repeat_chance=0.0, spawned_turret_actor=None, spawned_actor_count=(0, 0), spawned_velocity=0.0, aiming_velocity_maximum=0.0, 
                 aiming_acceleration_maximum=0.0, casual_aiming_modifier=0.0, looking_velocity_maximum=0.0, looking_acceleration_maximum=0.0, right_hand_node="", 
                 right_hand_node_length=0, left_hand_node="", left_hand_node_length=0, preferred_gun_node="", preferred_gun_node_length=0, melee_damage=None, 
                 boarding_melee_damage=None, boarding_melee_response=None, landing_melee_damage=None, flurry_melee_damage=None, obstacle_smash_damage=None, 
                 motion_sensor_blip_size=0, unit_type=0, unit_class=0, postures_tag_block=None, new_hud_interfaces_tag_block=None, dialogue_variants_tag_block=None, 
                 grenade_velocity=0.0, grenade_type=0, grenade_count=0, powered_seats_tag_block=None, weapons_tag_block=None, seats_tag_block=None, boost_peak_power=0.0, 
                 boost_rise_power=0.0, boost_peak_time=0.0, boost_fall_power=0.0, dead_time=0.0, attack_weight=0.0, decay_weight=0.0):
        super().__init__()
        self.camera_tracks_header = camera_tracks_header
        self.camera_tracks = camera_tracks
        self.postures_header = postures_header
        self.postures = postures
        self.new_hud_interface_header = new_hud_interface_header
        self.new_hud_interface = new_hud_interface
        self.dialogue_variants_header = dialogue_variants_header
        self.dialogue_variants = dialogue_variants
        self.powered_seats_header = powered_seats_header
        self.powered_seats = powered_seats
        self.weapons_header = weapons_header
        self.weapons = weapons
        self.seats_header = seats_header
        self.seats = seats
        self.unit_flags = unit_flags
        self.default_team = default_team
        self.constant_sound_volume = constant_sound_volume
        self.integrated_light_toggle = integrated_light_toggle
        self.camera_field_of_view = camera_field_of_view
        self.camera_stiffness = camera_stiffness
        self.camera_marker_name = camera_marker_name
        self.camera_marker_name_length = camera_marker_name_length
        self.camera_submerged_marker_name = camera_submerged_marker_name
        self.camera_submerged_marker_name_length = camera_submerged_marker_name_length
        self.pitch_auto_level = pitch_auto_level
        self.pitch_range = pitch_range
        self.camera_tracks_tag_block = camera_tracks_tag_block
        self.acceleration_range = acceleration_range
        self.acceleration_action_scale = acceleration_action_scale
        self.acceleration_attach_scale = acceleration_attach_scale
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
        self.spawned_turret_actor = spawned_turret_actor
        self.spawned_actor_count = spawned_actor_count
        self.spawned_velocity = spawned_velocity
        self.aiming_velocity_maximum = aiming_velocity_maximum
        self.aiming_acceleration_maximum = aiming_acceleration_maximum
        self.casual_aiming_modifier = casual_aiming_modifier
        self.looking_velocity_maximum = looking_velocity_maximum
        self.looking_acceleration_maximum = looking_acceleration_maximum
        self.right_hand_node = right_hand_node
        self.right_hand_node_length = right_hand_node_length
        self.left_hand_node = left_hand_node
        self.left_hand_node_length = left_hand_node_length
        self.preferred_gun_node = preferred_gun_node
        self.preferred_gun_node_length = preferred_gun_node_length
        self.melee_damage = melee_damage
        self.boarding_melee_damage = boarding_melee_damage
        self.boarding_melee_response = boarding_melee_response
        self.landing_melee_damage = landing_melee_damage
        self.flurry_melee_damage = flurry_melee_damage
        self.obstacle_smash_damage = obstacle_smash_damage
        self.motion_sensor_blip_size = motion_sensor_blip_size
        self.unit_type = unit_type
        self.unit_class = unit_class
        self.postures_tag_block = postures_tag_block
        self.new_hud_interfaces_tag_block = new_hud_interfaces_tag_block
        self.dialogue_variants_tag_block = dialogue_variants_tag_block
        self.grenade_velocity = grenade_velocity
        self.grenade_type = grenade_type
        self.grenade_count = grenade_count
        self.powered_seats_tag_block = powered_seats_tag_block
        self.weapons_tag_block = weapons_tag_block
        self.seats_tag_block = seats_tag_block
        self.boost_peak_power = boost_peak_power
        self.boost_rise_power = boost_rise_power
        self.boost_peak_time = boost_peak_time
        self.boost_fall_power = boost_fall_power
        self.dead_time = dead_time
        self.attack_weight = attack_weight
        self.decay_weight = decay_weight

    class Posture:
        def __init__(self, name="", name_length=0, pill_offset=Vector()):
            self.name = name
            self.name_length = name_length
            self.pill_offset = pill_offset

    class DialogueVariant:
        def __init__(self, variant_number=0, dialogue=None):
            self.variant_number = variant_number
            self.dialogue = dialogue

    class PoweredSeat:
        def __init__(self, driver_powerup_time=0.0, driver_powerdown_time=0.0):
            self.driver_powerup_time = driver_powerup_time
            self.driver_powerdown_time = driver_powerdown_time

    class Seat:
        def __init__(self, flags=0, label="", label_length=0, marker_name="", marker_name_length=0, entry_marker_name="", entry_marker_name_length=0, boarding_grenade_marker="",
                     boarding_grenade_marker_length=0, boarding_grenade_string="", boarding_grenade_string_length=0, boarding_melee_string="", boarding_melee_string_length=0,
                     ping_scale=0.0, turnover_time=0.0, acceleration_range=Vector(), acceleration_action_scale=0.0, acceleration_attach_scale=0.0, ai_scariness=0.0,
                     ai_seat_type=0, boarding_seat=-1, listener_interpolation_factor=0.0, yaw_rate_bounds=(0.0, 0.0), pitch_rate_bounds=(0.0, 0.0), min_speed_reference=0.0,
                     max_speed_reference=0.0, speed_exponent=0.0, camera_marker_name="", camera_marker_name_length=0, camera_submerged_marker_name="",
                     camera_submerged_marker_name_length=0, pitch_auto_level=0.0, pitch_range=(0.0, 0.0), camera_tracks_tag_block=None, camera_tracks_header=None, camera_tracks=None,
                     unit_hud_interface_tag_block=None, unit_hud_interface_header=None, unit_hud_interface=None, enter_seat_string="", enter_seat_string_length=0, yaw_minimum=0.0,
                     yaw_maximum=0.0, built_in_gunner=None, entry_radius=0.0, entry_marker_cone_angle=0.0, entry_marker_facing_angle=0.0, maximum_relative_velocity=0.0,
                     invisible_seat_region="", invisible_seat_region_length=0, runtime_invisible_seat_region_index=0):
            self.flags = flags
            self.label = label
            self.label_length = label_length
            self.marker_name = marker_name
            self.marker_name_length = marker_name_length
            self.entry_marker_name = entry_marker_name
            self.entry_marker_name_length = entry_marker_name_length
            self.boarding_grenade_marker = boarding_grenade_marker
            self.boarding_grenade_marker_length = boarding_grenade_marker_length
            self.boarding_grenade_string = boarding_grenade_string
            self.boarding_grenade_string_length = boarding_grenade_string_length
            self.boarding_melee_string = boarding_melee_string
            self.boarding_melee_string_length = boarding_melee_string_length
            self.ping_scale = ping_scale
            self.turnover_time = turnover_time
            self.acceleration_range = acceleration_range
            self.acceleration_action_scale = acceleration_action_scale
            self.acceleration_attach_scale = acceleration_attach_scale
            self.ai_scariness = ai_scariness
            self.ai_seat_type = ai_seat_type
            self.boarding_seat = boarding_seat
            self.listener_interpolation_factor = listener_interpolation_factor
            self.yaw_rate_bounds = yaw_rate_bounds
            self.pitch_rate_bounds = pitch_rate_bounds
            self.min_speed_reference = min_speed_reference
            self.max_speed_reference = max_speed_reference
            self.speed_exponent = speed_exponent
            self.camera_marker_name = camera_marker_name
            self.camera_marker_name_length = camera_marker_name_length
            self.camera_submerged_marker_name = camera_submerged_marker_name
            self.camera_submerged_marker_name_length = camera_submerged_marker_name_length
            self.pitch_auto_level = pitch_auto_level
            self.pitch_range = pitch_range
            self.camera_tracks_tag_block = camera_tracks_tag_block
            self.camera_tracks_header = camera_tracks_header
            self.camera_tracks = camera_tracks
            self.unit_hud_interface_tag_block = unit_hud_interface_tag_block
            self.unit_hud_interface_header = unit_hud_interface_header
            self.unit_hud_interface = unit_hud_interface
            self.enter_seat_string = enter_seat_string
            self.enter_seat_string_length = enter_seat_string_length
            self.yaw_minimum = yaw_minimum
            self.yaw_maximum = yaw_maximum
            self.built_in_gunner = built_in_gunner
            self.entry_radius = entry_radius
            self.entry_marker_cone_angle = entry_marker_cone_angle
            self.entry_marker_facing_angle = entry_marker_facing_angle
            self.maximum_relative_velocity = maximum_relative_velocity
            self.invisible_seat_region = invisible_seat_region
            self.invisible_seat_region_length = invisible_seat_region_length
            self.runtime_invisible_seat_region_index = runtime_invisible_seat_region_index
