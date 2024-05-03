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
from ..file_unit.format import UnitAsset

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

class FrictionPointFlags(Flag):
    gets_damage_from_region = auto()
    powered = auto()
    front_turning = auto()
    rear_turning = auto()
    attached_to_e_brake = auto()
    can_be_destroyed = auto()

class FrictionTypeEnum(Enum):
    point = 0
    forward = auto()

class VehicleAsset(UnitAsset):
    def __init__(self):
        super().__init__()
        self.header = None
        self.vehicle_body_header = None
        self.vehicle_body = None
        self.gears_header = None
        self.gears = None
        self.anti_gravity_point_header = None
        self.anti_gravity_point = None
        self.friction_points_header = None
        self.friction_points = None
        self.phantom_shapes_header = None
        self.phantom_shapes = None

    class VehicleBody(UnitAsset.UnitBody):
        def __init__(self, vehicle_flags=0, vehicle_type=0, vehicle_control=0, maximum_forward_speed=0.0, maximum_reverse_speed=0.0, speed_acceleration=0.0, speed_deceleration=0.0,
                     maximum_left_turn=0.0, maximum_right_turn=0.0, wheel_circumference=0.0, turn_rate=0.0, blur_speed=0.0, specific_type=0, player_training_vehicle_type=0,
                     flip_message="", flip_message_length=0, turn_scale=0.0, speed_turn_penalty_power=0.0, speed_turn_penalty=0.0, maximum_left_slide=0.0, maximum_right_slide=0.0,
                     slide_acceleration=0.0, slide_deceleration=0.0, minimum_flipping_angular_velocity=0.0, maximum_flipping_angular_velocity=0.0, vehicle_size=0,
                     fixed_gun_yaw=0.0, fixed_gun_pitch=0.0, overdampen_cusp_angle=0.0, overdampen_exponent=0.0, crouch_transition_time=0.0, engine_moment=0.0,
                     engine_max_angular_velocity=0.0, gears_tag_block=None, flying_torque_scale=0.0, seat_enterance_acceleration_scale=0.0, seat_exit_acceleration_scale=0.0,
                     air_friction_deceleration=0.0, thrust_scale=0.0, suspension_sound=None, crash_sound=None, unused=None, special_effect=None, unused_effect=None,
                     physics_flags=0, ground_fricton=0.0, ground_depth=0.0, ground_damp_factor=0.0, ground_moving_friction=0.0, ground_maximum_slope_0=0.0,
                     ground_maximum_slope_1=0.0, anti_gravity_bank_lift=0.0, steering_bank_reaction_scale=0.0, gravity_scale=0.0, radius=0.0, anti_gravity_point_tag_block=None,
                     friction_points_tag_block=None, phantom_shapes_tag_block=None):
            super().__init__()
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

    class Gear:
        def __init__(self, a_min_torque=0.0, a_max_torque=0.0, a_peak_torque_scale=0.0, a_past_peak_torque_exponent=0.0, a_torque_at_max_angular_velocity=0.0,
                     a_torque_at_2x_max_angular_velocity=0.0, b_min_torque=0.0, b_max_torque=0.0, b_peak_torque_scale=0.0, b_past_peak_torque_exponent=0.0,
                     b_torque_at_max_angular_velocity=0.0, b_torque_at_2x_max_angular_velocity=0.0, min_time_to_upshift=0.0, engine_up_shift_scale=0.0, gear_ratio=0.0,
                     min_time_to_downshift=0.0, engine_down_shift_scale=0.0):
            self.a_min_torque = a_min_torque
            self.a_max_torque = a_max_torque
            self.a_peak_torque_scale = a_peak_torque_scale
            self.a_past_peak_torque_exponent = a_past_peak_torque_exponent
            self.a_torque_at_max_angular_velocity = a_torque_at_max_angular_velocity
            self.a_torque_at_2x_max_angular_velocity = a_torque_at_2x_max_angular_velocity
            self.b_min_torque = b_min_torque
            self.b_max_torque = b_max_torque
            self.b_peak_torque_scale = b_peak_torque_scale
            self.b_past_peak_torque_exponent = b_past_peak_torque_exponent
            self.b_torque_at_max_angular_velocity = b_torque_at_max_angular_velocity
            self.b_torque_at_2x_max_angular_velocity = b_torque_at_2x_max_angular_velocity
            self.min_time_to_upshift = min_time_to_upshift
            self.engine_up_shift_scale = engine_up_shift_scale
            self.gear_ratio = gear_ratio
            self.min_time_to_downshift = min_time_to_downshift
            self.engine_down_shift_scale = engine_down_shift_scale

    class AntiGravityPoint:
        def __init__(self, marker_name="", marker_name_length=0, flags=0, antigrav_strength=0.0, antigrav_offset=0.0, antigrav_height=0.0, antigrav_damp_factor=0.0,
                     antigrav_normal_k1=0.0, antigrav_normal_k0=0.0, radius=0.0, damage_source_region_name="", damage_source_region_name_length=0, default_state_error=0.0,
                     minor_damage_error=0.0, medium_damage_error=0.0, major_damage_error=0.0, destroyed_state_error=0.0):
            self.marker_name = marker_name
            self.marker_name_length = marker_name_length
            self.flags = flags
            self.antigrav_strength = antigrav_strength
            self.antigrav_offset = antigrav_offset
            self.antigrav_height = antigrav_height
            self.antigrav_damp_factor = antigrav_damp_factor
            self.antigrav_normal_k1 = antigrav_normal_k1
            self.antigrav_normal_k0 = antigrav_normal_k0
            self.radius = radius
            self.damage_source_region_name = damage_source_region_name
            self.damage_source_region_name_length = damage_source_region_name_length
            self.default_state_error = default_state_error
            self.minor_damage_error = minor_damage_error
            self.medium_damage_error = medium_damage_error
            self.major_damage_error = major_damage_error
            self.destroyed_state_error = destroyed_state_error

    class FrictionPoint:
        def __init__(self, marker_name="", marker_name_length=0, flags=0, fraction_of_total_mass=0.0, radius=0.0, damaged_radius=0.0, friction_type=0,
                     moving_friction_velocity_diff=0.0, e_brake_moving_friction=0.0, e_brake_friction=0.0, e_brake_moving_friction_vel_dif=0.0, collision_global_material_name="",
                     collision_global_material_name_length=0, model_state_destroyed=0, region_name="", region_name_length=0):
            self.marker_name = marker_name
            self.marker_name_length = marker_name_length
            self.flags = flags
            self.fraction_of_total_mass = fraction_of_total_mass
            self.radius = radius
            self.damaged_radius = damaged_radius
            self.friction_type = friction_type
            self.moving_friction_velocity_diff = moving_friction_velocity_diff
            self.e_brake_moving_friction = e_brake_moving_friction
            self.e_brake_friction = e_brake_friction
            self.e_brake_moving_friction_vel_dif = e_brake_moving_friction_vel_dif
            self.collision_global_material_name = collision_global_material_name
            self.collision_global_material_name_length = collision_global_material_name_length
            self.model_state_destroyed = model_state_destroyed
            self.region_name = region_name
            self.region_name_length = region_name_length

    class PhantomVolume:
        def __init__(self, size=0, count=0, child_shapes_size=0, child_shapes_capacity=0, multisphere_count=0, flags=0, x0=0.0, x1=0.0, y0=0.0, y1=0.0, z0=0.0, z1=0.0,
                     spheres=None):
            self.size = size
            self.count = count
            self.child_shapes_size = child_shapes_size
            self.child_shapes_capacity = child_shapes_capacity
            self.multisphere_count = multisphere_count
            self.flags = flags
            self.x0 = x0
            self.x1 = x1
            self.y0 = y0
            self.y1 = y1
            self.z0 = z0
            self.z1 = z1
            self.spheres = spheres

    class Sphere:
        def __init__(self, size=0, count=0, num_spheres=0, sphere_0=Vector(), sphere_1=Vector(), sphere_2=Vector(), sphere_3=Vector(), sphere_4=Vector(), sphere_5=Vector(),
                     sphere_6=Vector(), sphere_7=Vector()):
            self.size = size
            self.count = count
            self.num_spheres = num_spheres
            self.sphere_0 = sphere_0
            self.sphere_1 = sphere_1
            self.sphere_2 = sphere_2
            self.sphere_3 = sphere_3
            self.sphere_4 = sphere_4
            self.sphere_5 = sphere_5
            self.sphere_6 = sphere_6
            self.sphere_7 = sphere_7
