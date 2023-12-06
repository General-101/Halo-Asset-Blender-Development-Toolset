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

class VehicleFlags(Flag):
    speed_wake_physics = auto()
    turn_wake_physics = auto()
    driver_power_wakes_physics = auto()
    gunner_power_wakes_physics = auto()
    control_opposite_speed_sets_break = auto()
    slide_wakes_physics = auto()
    kills_riders_at_terminal_velocity = auto()
    causes_collision_damage = auto()
    ai_weapon_cannot_rotate = auto()
    ai_does_not_require_driver = auto()
    ai_unused = auto()
    ai_driver_enabled = auto()
    ai_driver_flying = auto()
    ai_driver_can_sidestep = auto()
    ai_driver_hovering = auto()
    vehicle_steers_directly = auto()
    unused = auto()
    has_ebrake = auto()
    noncombat_vehicle = auto()
    no_friction_with_driver = auto()
    can_trigger_automatic_opening_doors = auto()
    autoaim_when_teamless = auto()

class VehicleTypeEnum(Enum):
    human_tank = 0
    human_jeep = auto()
    human_boat = auto()
    human_plane = auto()
    alien_scout = auto()
    alien_fighter = auto()
    turret = auto()

class VehicleControlEnum(Enum):
    vehicle_control_normal = 0
    vehicle_control_unused = auto()
    vehicle_control_tank = auto()

class SpecificTypeEnum(Enum):
    none = 0
    ghost = auto()
    wraith = auto()
    spectre = auto()
    sentinel_enforcer = auto()

class PlayerTrainingVehicleTypeEnum(Enum):
    none = 0
    warthog = auto()
    warthog_turret = auto()
    ghost = auto()
    banshee = auto()
    tank = auto()
    wraith = auto()

class VehicleSizeEnum(Enum):
    small = 0
    large = auto()

class PhysicsFlags(Flag):
    invalid = auto()

class VehicleAsset():
    def __init__(self):
        self.header = None
        self.vehicle_body_header = None
        self.vehicle_body = None
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
        self.camera_tracks_header = None
        self.camera_tracks = None
        self.camera_tracks_header = None
        self.postures_header = None
        self.postures = None
        self.new_hud_interface_header = None
        self.new_hud_interface = None
        self.dialogue_variants_header = None
        self.dialogue_variants = None
        self.powered_seats_header = None
        self.powered_seats = None
        self.weapons_header = None
        self.weapons = None
        self.seats_header = None
        self.seats = None
        self.gears_header = None
        self.gears = None
        self.anti_gravity_point_header = None
        self.anti_gravity_point = None
        self.friction_points_header = None
        self.friction_points = None
        self.phantom_shapes_header = None
        self.phantom_shapes = None

    class VehicleBody:
        def __init__(self, object_flags=0, bounding_radius=0.0, bounding_offset=Vector(), acceleration_scale=0.0, lightmap_shadow_mode=0, sweetner_size=0, 
                     dynamic_light_sphere_radius=0.0, dynamic_light_sphere_offset=Vector(), default_model_variant="", default_model_variant_length=0, model=None, crate_object=None, 
                     modifier_shader=None, creation_effect=None, material_effects=None, ai_properties_tag_block=None, functions_tag_block=None, apply_collision_damage_scale=0.0, 
                     min_game_acc=0.0, max_game_acc=0.0, min_game_scale=0.0, max_game_scale=0.0, min_abs_acc=0.0, max_abs_acc=0.0, min_abs_scale=0.0, max_abs_scale=0.0, 
                     hud_text_message_index=0, attachments_tag_block=None, widgets_tag_block=None, old_functions_tag_block=None, change_colors_tag_block=None, 
                     predicted_resources_tag_block=None, unit_flags=0, default_team=0, constant_sound_volume=0, integrated_light_toggle=None, camera_field_of_view=0.0, 
                     camera_stiffness=0.0, camera_marker_name="", camera_marker_name_length=0, camera_submerged_marker_name="", camera_submerged_marker_name_length=0, 
                     pitch_auto_level=0.0, pitch_range=(0.0, 0.0), camera_tracks_tag_block=None, acceleration_range=Vector(), acceleration_action_scale=0.0, 
                     acceleration_attach_scale=0.0, soft_ping_threshold=0.0, soft_ping_interrupt_time=0.0, hard_ping_threshold=0.0, hard_ping_interrupt_time=0.0, 
                     hard_death_threshold=0.0, feign_death_threshold=0.0, feign_death_time=0.0, distance_of_evade_anim=0.0, distance_of_dive_anim=0.0, 
                     stunned_movement_threshold=0.0, feign_death_chance=0.0, feign_repeat_chance=0.0, spawned_turret_actor=None, spawned_actor_count=(0, 0), 
                     spawned_velocity=0.0, aiming_velocity_maximum=0.0, aiming_acceleration_maximum=0.0, casual_aiming_modifier=0.0, looking_velocity_maximum=0.0, 
                     looking_acceleration_maximum=0.0, right_hand_node="", right_hand_node_length=0, left_hand_node="", left_hand_node_length=0, preferred_gun_node="", 
                     preferred_gun_node_length=0, melee_damage=None, boarding_melee_damage=None, boarding_melee_response=None, landing_melee_damage=None, 
                     flurry_melee_damage=None, obstacle_smash_damage=None, motion_sensor_blip_size=0, unit_type=0, unit_class=0, postures_tag_block=None, 
                     new_hud_interfaces_tag_block=None, dialogue_variants_tag_block=None, grenade_velocity=0.0, grenade_type=0, grenade_count=0, powered_seats_tag_block=None, 
                     weapons_tag_block=None, seats_tag_block=None, boost_peak_power=0.0, boost_rise_power=0.0, boost_peak_time=0.0, boost_fall_power=0.0, dead_time=0.0, 
                     attack_weight=0.0, decay_weight=0.0, vehicle_flags=0, vehicle_type=0, vehicle_control=0, maximum_forward_speed=0.0, maximum_reverse_speed=0.0, 
                     speed_acceleration=0.0, speed_deceleration=0.0, maximum_left_turn=0.0, maximum_right_turn=0.0, wheel_circumference=0.0, turn_rate=0.0, blur_speed=0.0, 
                     specific_type=0, player_training_vehicle_type=0, flip_message="", flip_message_length=0, turn_scale=0.0, speed_turn_penalty_power=0.0, speed_turn_penalty=0.0, 
                     maximum_left_slide=0.0, maximum_right_slide=0.0, slide_acceleration=0.0, slide_deceleration=0.0, minimum_flipping_angular_velocity=0.0, 
                     maximum_flipping_angular_velocity=0.0, vehicle_size=0, fixed_gun_yaw=0.0, fixed_gun_pitch=0.0, overdampen_cusp_angle=0.0, overdampen_exponent=0.0, 
                     crouch_transition_time=0.0, engine_moment=0.0, engine_max_angular_velocity=0.0, gears_tag_block=None, gears_header=None, flying_torque_scale=0.0, 
                     seat_enterance_acceleration_scale=0.0, seat_exit_acceleration_scale=0.0, air_friction_deceleration=0.0, thrust_scale=0.0, suspension_sound=None, 
                     crash_sound=None, unused=None, special_effect=None, unused_effect=None, physics_flags=0, ground_fricton=0.0, ground_depth=0.0, ground_damp_factor=0.0, 
                     ground_moving_friction=0.0, ground_maximum_slope_0=0.0, ground_maximum_slope_1=0.0, anti_gravity_bank_lift=0.0, steering_bank_reaction_scale=0.0, 
                     gravity_scale=0.0, radius=0.0, anti_gravity_point_tag_block=None, anti_gravity_point_header=None, friction_points_tag_block=None, friction_points_header=None, 
                     phantom_shapes_tag_block=None, phantom_shapes_header=None, gears=None, anti_gravity_point=None, friction_points=None, phantom_shapes=None):
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
            self.vehicle_flags = vehicle_flags
            self.vehicle_type = vehicle_type
            self.vehicle_control = vehicle_control
            self.maximum_forward_speed = maximum_forward_speed
            self.maximum_reverse_speed = maximum_reverse_speed
            self.speed_acceleration = speed_acceleration
            self.speed_deceleration = speed_deceleration
            self.maximum_left_turn = maximum_left_turn
            self.maximum_right_turn = maximum_right_turn
            self.wheel_circumference = wheel_circumference
            self.turn_rate = turn_rate
            self.blur_speed = blur_speed
            self.specific_type = specific_type
            self.player_training_vehicle_type = player_training_vehicle_type
            self.flip_message = flip_message
            self.flip_message_length = flip_message_length
            self.turn_scale = turn_scale
            self.speed_turn_penalty_power = speed_turn_penalty_power
            self.speed_turn_penalty = speed_turn_penalty
            self.maximum_left_slide = maximum_left_slide
            self.maximum_right_slide = maximum_right_slide
            self.slide_acceleration = slide_acceleration
            self.slide_deceleration = slide_deceleration
            self.minimum_flipping_angular_velocity = minimum_flipping_angular_velocity
            self.maximum_flipping_angular_velocity = maximum_flipping_angular_velocity
            self.vehicle_size = vehicle_size
            self.fixed_gun_yaw = fixed_gun_yaw
            self.fixed_gun_pitch = fixed_gun_pitch
            self.overdampen_cusp_angle = overdampen_cusp_angle
            self.overdampen_exponent = overdampen_exponent
            self.crouch_transition_time = crouch_transition_time
            self.engine_moment = engine_moment
            self.engine_max_angular_velocity = engine_max_angular_velocity
            self.gears_tag_block = gears_tag_block
            self.flying_torque_scale = flying_torque_scale
            self.seat_enterance_acceleration_scale = seat_enterance_acceleration_scale
            self.seat_exit_acceleration_scale = seat_exit_acceleration_scale
            self.air_friction_deceleration = air_friction_deceleration
            self.thrust_scale = thrust_scale
            self.suspension_sound = suspension_sound
            self.crash_sound = crash_sound
            self.unused = unused
            self.special_effect = special_effect
            self.unused_effect = unused_effect
            self.physics_flags = physics_flags
            self.ground_fricton = ground_fricton
            self.ground_depth = ground_depth
            self.ground_damp_factor = ground_damp_factor
            self.ground_moving_friction = ground_moving_friction
            self.ground_maximum_slope_0 = ground_maximum_slope_0
            self.ground_maximum_slope_1 = ground_maximum_slope_1
            self.anti_gravity_bank_lift = anti_gravity_bank_lift
            self.steering_bank_reaction_scale = steering_bank_reaction_scale
            self.gravity_scale = gravity_scale
            self.radius = radius
            self.anti_gravity_point_tag_block = anti_gravity_point_tag_block
            self.friction_points_tag_block = friction_points_tag_block
            self.phantom_shapes_tag_block = phantom_shapes_tag_block
