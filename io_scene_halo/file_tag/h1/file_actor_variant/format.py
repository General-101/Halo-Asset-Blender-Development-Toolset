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

class ActorVariantFlags(Flag):
    can_shoot_while_flying = auto()
    interpolate_color_in_hsv = auto()
    has_unlimited_grenades = auto()
    movement_switching_try_to_stay_with_friends = auto()
    active_camouflage = auto()
    super_active_camouflage = auto()
    cannot_use_ranged_weapons = auto()
    prefer_passenger_seat = auto()

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

class MovementTypeEnum(Enum):
    always_run = 0
    always_crouch = auto()
    switch_types = auto()

class SpecialFireModeEnum(Enum):
    none = 0
    overcharge = auto()
    secondary_trigger = auto()

class SpecialFireSituationEnum(Enum):
    never = 0
    enemy_visible = auto()
    enemy_out_of_sight = auto()
    strafing = auto()

class GrenadeTypeEnum(Enum):
    human_fragmentation = 0
    covenant_plasma = auto()
    grenade_type_2 = auto()
    grenade_type_3 = auto()

class TrajectoryTypeEnum(Enum):
    toss = 0
    lob = auto()
    bounce = auto()

class GrenadeStimulusEnum(Enum):
    never = 0
    visible_target = auto()
    seek_cover = auto()

class ActorVariantAsset():
    def __init__(self, header=None, change_color=None, flags=0, actor_definition=None, unit=None, major_variant=None, metagame_type=0, metagame_class=0, movement_type=0, 
                 initial_crouch_distance=0.0, crouch_time=(0.0, 0.0), run_time=(0.0, 0.0), weapon=None, maximum_firing_distance=0.0, rate_of_Fire=0.0, projectile_error=0.0, 
                 first_burst_delay_time=(0.0, 0.0), new_target_firing_pattern_time=0.0, surprise_delay_time=0.0, surprise_fire_wildly_time=0.0, death_fire_wildly_chance=0.0, 
                 death_fire_wildly_time=0.0, desired_combat_range=(0.0, 0.0), custom_stand_gun_offset=Vector(), custom_crouch_gun_offset=Vector(), target_tracking=0.0, 
                 target_leading=0.0, weapon_damage_modifier=0.0, damage_per_second=0.0, burst_origin_radius=0.0, burst_origin_angle=0.0, burst_return_length=(0.0, 0.0), 
                 burst_return_angle=0.0, burst_duration=(0.0, 0.0), burst_seperation=(0.0, 0.0), burst_angular_velocity=0.0, special_damage_modifier=0.0, 
                 speical_projectile_error=0.0, new_target_burst_duration=0.0, new_target_burst_seperation=0.0, new_target_rate_of_fire=0.0, new_target_projectile_error=0.0, 
                 moving_burst_duration=0.0, moving_burst_seperation=0.0, moving_rate_of_fire=0.0, moving_projectile_error=0.0, berserk_burst_duration=0.0, 
                 berserk_burst_seperation=0.0, berserk_rate_of_fire=0.0, berserk_projectile_error=0.0, super_ballistic_range=0.0, bombardment_range=0.0, 
                 modified_vision_range=0.0, special_fire_mode=0, special_fire_situation=0, special_fire_chance=0.0, special_fire_delay=0.0, melee_range=0.0, 
                 melee_abort_range=0, berserk_firing_ranges=(0.0, 0.0), berserk_melee_range=0.0, berserk_melee_abort_range=0.0, grenade_type=0, trajectory_type=0, 
                 grenade_stimulus=0, minimum_enemy_count=0.0, enemy_radius=0.0, grenade_velocity=0.0, grenade_ranges=(0.0, 0.0), collateral_damage_radius=0.0, 
                 grenade_chance=0.0, grenade_check_time=0.0, encounter_grenade_timeout=0.0, equipment=None, grenade_count=(0, 0), dont_drop_grenades_chance=0.0, 
                 drop_weapon_loaded=(0.0, 0.0), drop_weapon_ammo=(0, 0), body_vitality=0.0, shield_vitality=0.0, shield_sapping_radius=0.0, forced_shader_permutation=0, 
                 change_colors_tag_block=None):
        self.header = header
        self.change_color = change_color
        self.flags = flags
        self.actor_definition = actor_definition
        self.unit = unit
        self.major_variant = major_variant
        self.metagame_type = metagame_type
        self.metagame_class = metagame_class
        self.movement_type = movement_type
        self.initial_crouch_distance = initial_crouch_distance
        self.crouch_time = crouch_time
        self.run_time = run_time
        self.weapon = weapon
        self.maximum_firing_distance = maximum_firing_distance
        self.rate_of_Fire = rate_of_Fire
        self.projectile_error = projectile_error
        self.first_burst_delay_time = first_burst_delay_time
        self.new_target_firing_pattern_time = new_target_firing_pattern_time
        self.surprise_delay_time = surprise_delay_time
        self.surprise_fire_wildly_time = surprise_fire_wildly_time
        self.death_fire_wildly_chance = death_fire_wildly_chance
        self.death_fire_wildly_time = death_fire_wildly_time
        self.desired_combat_range = desired_combat_range
        self.custom_stand_gun_offset = custom_stand_gun_offset
        self.custom_crouch_gun_offset = custom_crouch_gun_offset
        self.target_tracking = target_tracking
        self.target_leading = target_leading
        self.weapon_damage_modifier = weapon_damage_modifier
        self.damage_per_second = damage_per_second
        self.burst_origin_radius = burst_origin_radius
        self.burst_origin_angle = burst_origin_angle
        self.burst_return_length = burst_return_length
        self.burst_return_angle = burst_return_angle
        self.burst_duration = burst_duration
        self.burst_seperation = burst_seperation
        self.burst_angular_velocity = burst_angular_velocity
        self.special_damage_modifier = special_damage_modifier
        self.speical_projectile_error = speical_projectile_error
        self.new_target_burst_duration = new_target_burst_duration
        self.new_target_burst_seperation = new_target_burst_seperation
        self.new_target_rate_of_fire = new_target_rate_of_fire
        self.new_target_projectile_error = new_target_projectile_error
        self.moving_burst_duration = moving_burst_duration
        self.moving_burst_seperation = moving_burst_seperation
        self.moving_rate_of_fire = moving_rate_of_fire
        self.moving_projectile_error = moving_projectile_error
        self.berserk_burst_duration = berserk_burst_duration
        self.berserk_burst_seperation = berserk_burst_seperation
        self.berserk_rate_of_fire = berserk_rate_of_fire
        self.berserk_projectile_error = berserk_projectile_error
        self.super_ballistic_range = super_ballistic_range
        self.bombardment_range = bombardment_range
        self.modified_vision_range = modified_vision_range
        self.special_fire_mode = special_fire_mode
        self.special_fire_situation = special_fire_situation
        self.special_fire_chance = special_fire_chance
        self.special_fire_delay = special_fire_delay
        self.melee_range = melee_range
        self.melee_abort_range = melee_abort_range
        self.berserk_firing_ranges = berserk_firing_ranges
        self.berserk_melee_range = berserk_melee_range
        self.berserk_melee_abort_range = berserk_melee_abort_range
        self.grenade_type = grenade_type
        self.trajectory_type = trajectory_type
        self.grenade_stimulus = grenade_stimulus
        self.minimum_enemy_count = minimum_enemy_count
        self.enemy_radius = enemy_radius
        self.grenade_velocity = grenade_velocity
        self.grenade_ranges = grenade_ranges
        self.collateral_damage_radius = collateral_damage_radius
        self.grenade_chance = grenade_chance
        self.grenade_check_time = grenade_check_time
        self.encounter_grenade_timeout = encounter_grenade_timeout
        self.equipment = equipment
        self.grenade_count = grenade_count
        self.dont_drop_grenades_chance = dont_drop_grenades_chance
        self.drop_weapon_loaded = drop_weapon_loaded
        self.drop_weapon_ammo = drop_weapon_ammo
        self.body_vitality = body_vitality
        self.shield_vitality = shield_vitality
        self.shield_sapping_radius = shield_sapping_radius
        self.forced_shader_permutation = forced_shader_permutation
        self.change_colors_tag_block = change_colors_tag_block
