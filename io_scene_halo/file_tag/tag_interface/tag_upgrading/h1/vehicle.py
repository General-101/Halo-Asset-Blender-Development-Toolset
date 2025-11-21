# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Steven Garcia
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

import os
import json

from math import sqrt
from mathutils import Vector
from enum import Flag, Enum, auto
from ....global_functions import tag_format, shader_processing
from ....file_tag.h2.file_object.format import AISizeEnum, LeapJumpSpeedEnum
from ....file_tag.h2_20030504.file_object.format import upgrade_e3_object_flags
from ....file_tag.h2.file_unit.format import SeatFlags
from ....file_tag.h2.file_vehicle.format import VehicleAsset, VehicleFlags, VehicleTypeEnum, SpecificTypeEnum, PlayerTrainingVehicleTypeEnum, FrictionPointFlags, FrictionTypeEnum
from ....file_tag.h2_20030504.file_object.upgrade_json import generate_attachments, generate_widgets, generate_change_colors, _20030504_ObjectFunctionsEnum
from ....file_tag.h2_20030504.file_unit.upgrade_json import (
    generate_camera_tracks,
    generate_new_hud_interface,
    generate_dialogue_variants,
    generate_powered_seats,
    generate_weapons,
    generate_seats,
    _20030504_UnitFunctionsEnum,
    get_metagame_data
    )

class _20030504_VehicleFunctionsEnum(Enum):
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
    left_tread_position = auto()
    right_tread_position = auto()
    left_tread_velocity = auto()
    right_tread_velocity = auto()
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

class _20030504_MassPointFlags(Flag):
    metallic = auto()

def generate_vehicle_points(phys_dic, TAG, VEHICLE):
    if not phys_dic == None:
        powered_mass_points_tag_block = phys_dic['Data']['Powered Mass Points']
        mass_points_tag_block = phys_dic['Data']['Mass Points']
        vehicle_type_enum = VehicleTypeEnum(VEHICLE.vehicle_type)

        if vehicle_type_enum == VehicleTypeEnum.alien_scout or vehicle_type_enum == VehicleTypeEnum.human_boat:
            for mass_point_element in mass_points_tag_block:
                powered_point_index = mass_point_element['Powered Mass Point index']
                if powered_point_index >= 0:
                    powered_mass_point_element = powered_mass_points_tag_block[powered_point_index]
                    anti_gravity_point = VEHICLE.AntiGravityPoint()
                    anti_gravity_point.marker_name = mass_point_element['Name']
                    anti_gravity_point.marker_name_length = len(anti_gravity_point.marker_name)
                    anti_gravity_point.flags = 0
                    anti_gravity_point.antigrav_strength = powered_mass_point_element['Antigrav Strength']
                    anti_gravity_point.antigrav_offset = powered_mass_point_element['Antigrav Offset']
                    anti_gravity_point.antigrav_height = powered_mass_point_element['Antigrav Height']
                    anti_gravity_point.antigrav_damp_factor = 1.0
                    anti_gravity_point.antigrav_normal_k1 = powered_mass_point_element['Antigrav Normal K1']
                    anti_gravity_point.antigrav_normal_k0 = powered_mass_point_element['Antigrav Normal K0']
                    anti_gravity_point.radius = 0.4 * powered_mass_point_element['Antigrav Height']
                    anti_gravity_point.damage_source_region_name = ""
                    anti_gravity_point.damage_source_region_name_length = len(anti_gravity_point.damage_source_region_name)
                    anti_gravity_point.default_state_error = 0.0
                    anti_gravity_point.minor_damage_error = 0.0
                    anti_gravity_point.medium_damage_error = 0.0
                    anti_gravity_point.major_damage_error = 0.0
                    anti_gravity_point.destroyed_state_error = 0.0

                    VEHICLE.anti_gravity_point.append(anti_gravity_point)

            if len(VEHICLE.anti_gravity_point) == 0:
                for powered_mass_point_element in powered_mass_points_tag_block:
                    anti_gravity_point = VEHICLE.AntiGravityPoint()
                    anti_gravity_point.marker_name = powered_mass_point_element['Name']
                    anti_gravity_point.marker_name_length = len(anti_gravity_point.marker_name)
                    anti_gravity_point.flags = 0
                    anti_gravity_point.antigrav_strength = powered_mass_point_element['Antigrav Strength']
                    anti_gravity_point.antigrav_offset = powered_mass_point_element['Antigrav Offset']
                    anti_gravity_point.antigrav_height = powered_mass_point_element['Antigrav Height']
                    anti_gravity_point.antigrav_damp_factor = powered_mass_point_element['Antigrav Damp Fraction']
                    anti_gravity_point.antigrav_normal_k1 = powered_mass_point_element['Antigrav Normal K1']
                    anti_gravity_point.antigrav_normal_k0 = powered_mass_point_element['Antigrav Normal K0']
                    anti_gravity_point.radius = 0.4 * powered_mass_point_element['Antigrav Height']
                    anti_gravity_point.damage_source_region_name = ""
                    anti_gravity_point.damage_source_region_name_length = len(anti_gravity_point.damage_source_region_name)
                    anti_gravity_point.default_state_error = 0.0
                    anti_gravity_point.minor_damage_error = 0.0
                    anti_gravity_point.medium_damage_error = 0.0
                    anti_gravity_point.major_damage_error = 0.0
                    anti_gravity_point.destroyed_state_error = 0.0

                    VEHICLE.anti_gravity_point.append(anti_gravity_point)

        if vehicle_type_enum == VehicleTypeEnum.human_tank or vehicle_type_enum == VehicleTypeEnum.human_jeep:
            for mass_point_element in mass_points_tag_block:
                if FrictionTypeEnum.forward == FrictionTypeEnum(mass_point_element['Friction Type']['Value']):
                    flags = FrictionPointFlags.powered.value
                    if "front" in mass_point_element['Name'].lower():
                        flags += FrictionPointFlags.front_turning.value
                    if "back" in mass_point_element['Name'].lower():
                        flags += FrictionPointFlags.attached_to_e_brake.value

                    friction_point = VEHICLE.FrictionPoint()
                    friction_point.marker_name = mass_point_element['Name']
                    friction_point.marker_name_length = len(friction_point.marker_name)
                    friction_point.flags = flags
                    friction_point.fraction_of_total_mass = mass_point_element['Mass']  / 30
                    friction_point.radius = mass_point_element['Radius']
                    friction_point.damaged_radius = mass_point_element['Radius']
                    friction_point.friction_type = mass_point_element['Friction Type']['Value']
                    friction_point.moving_friction_velocity_diff = 0.0
                    friction_point.e_brake_moving_friction = 0.0
                    friction_point.e_brake_friction = 0.0
                    friction_point.e_brake_moving_friction_vel_dif = 0.0
                    if _20030504_MassPointFlags.metallic in _20030504_MassPointFlags(mass_point_element['Flags']):
                        friction_point.collision_global_material_name = "hard_metal_thick_hum"
                    else:
                        friction_point.collision_global_material_name = "tough_inorganic_rubber_hum_tire"

                    friction_point.collision_global_material_name_length = len(friction_point.collision_global_material_name)
                    friction_point.model_state_destroyed = 0
                    friction_point.region_name = ""
                    friction_point.region_name_length = len(friction_point.region_name)

                    VEHICLE.friction_points.append(friction_point)

    anti_gravity_point_count = len(VEHICLE.anti_gravity_point)
    VEHICLE.anti_gravity_point_header = TAG.TagBlockHeader("tbfd", 0, anti_gravity_point_count, 76)
    VEHICLE.anti_gravity_point_tag_block = TAG.TagBlock(anti_gravity_point_count)

    friction_point_count = len(VEHICLE.friction_points)
    VEHICLE.friction_points_header = TAG.TagBlockHeader("tbfd", 0, friction_point_count, 76)
    VEHICLE.friction_points_tag_block = TAG.TagBlock(friction_point_count)

def generate_gears(TAG, VEHICLE):
    vehicle_type_enum = VehicleTypeEnum(VEHICLE.vehicle_type)
    if vehicle_type_enum == VehicleTypeEnum.human_jeep:
        reverse_gear = VEHICLE.FrictionPoint()
        reverse_gear.a_min_torque = 76500
        reverse_gear.a_max_torque = 85500
        reverse_gear.a_peak_torque_scale = 0.2
        reverse_gear.a_past_peak_torque_exponent = 1.5
        reverse_gear.a_torque_at_max_angular_velocity = -45000
        reverse_gear.a_torque_at_2x_max_angular_velocity = -135000
        reverse_gear.b_min_torque = 0
        reverse_gear.b_max_torque = -135000
        reverse_gear.b_peak_torque_scale = 0.1
        reverse_gear.b_past_peak_torque_exponent = 1.5
        reverse_gear.b_torque_at_max_angular_velocity = -180000
        reverse_gear.b_torque_at_2x_max_angular_velocity = -360000
        reverse_gear.min_time_to_upshift = 0
        reverse_gear.engine_up_shift_scale = 1
        reverse_gear.gear_ratio = -0.7
        reverse_gear.min_time_to_downshift = 0
        reverse_gear.engine_down_shift_scale = 0

        drive_1_gear = VEHICLE.FrictionPoint()
        drive_1_gear.a_min_torque = 76500
        drive_1_gear.a_max_torque = 85500
        drive_1_gear.a_peak_torque_scale = 0.26
        drive_1_gear.a_past_peak_torque_exponent = 1.6
        drive_1_gear.a_torque_at_max_angular_velocity = 20250
        drive_1_gear.a_torque_at_2x_max_angular_velocity = -36000
        drive_1_gear.b_min_torque = 0
        drive_1_gear.b_max_torque = -45000
        drive_1_gear.b_peak_torque_scale = 0.3
        drive_1_gear.b_past_peak_torque_exponent = 1.75
        drive_1_gear.b_torque_at_max_angular_velocity = -54000
        drive_1_gear.b_torque_at_2x_max_angular_velocity = -135000
        drive_1_gear.min_time_to_upshift = 0.2
        drive_1_gear.engine_up_shift_scale = 0.9
        drive_1_gear.gear_ratio = 0.6
        drive_1_gear.min_time_to_downshift = 0.1
        drive_1_gear.engine_down_shift_scale = 0.5

        drive_2_gear = VEHICLE.FrictionPoint()
        drive_2_gear.a_min_torque = 45000
        drive_2_gear.a_max_torque = 72000
        drive_2_gear.a_peak_torque_scale = 0.38
        drive_2_gear.a_past_peak_torque_exponent = 1.45
        drive_2_gear.a_torque_at_max_angular_velocity = 6750
        drive_2_gear.a_torque_at_2x_max_angular_velocity = -45000
        drive_2_gear.b_min_torque = 0
        drive_2_gear.b_max_torque = -36000
        drive_2_gear.b_peak_torque_scale = 0.4
        drive_2_gear.b_past_peak_torque_exponent = 1.25
        drive_2_gear.b_torque_at_max_angular_velocity = -40500
        drive_2_gear.b_torque_at_2x_max_angular_velocity = -72000
        drive_2_gear.min_time_to_upshift = 1
        drive_2_gear.engine_up_shift_scale = 0.91
        drive_2_gear.gear_ratio = 1
        drive_2_gear.min_time_to_downshift = 0.2
        drive_2_gear.engine_down_shift_scale = 0.5

        drive_3_gear = VEHICLE.FrictionPoint()
        drive_3_gear.a_min_torque = 31500
        drive_3_gear.a_max_torque = 45000
        drive_3_gear.a_peak_torque_scale = 0.5
        drive_3_gear.a_past_peak_torque_exponent = 1.25
        drive_3_gear.a_torque_at_max_angular_velocity = 4500
        drive_3_gear.a_torque_at_2x_max_angular_velocity = -9000
        drive_3_gear.b_min_torque = 0
        drive_3_gear.b_max_torque = -27000
        drive_3_gear.b_peak_torque_scale = 0.5
        drive_3_gear.b_past_peak_torque_exponent = 1
        drive_3_gear.b_torque_at_max_angular_velocity = -31500
        drive_3_gear.b_torque_at_2x_max_angular_velocity = -45000
        drive_3_gear.min_time_to_upshift = 0
        drive_3_gear.engine_up_shift_scale = 1
        drive_3_gear.gear_ratio = 1.2
        drive_3_gear.min_time_to_downshift = 0.15
        drive_3_gear.engine_down_shift_scale = 0.75

        VEHICLE.gears.append(reverse_gear)
        VEHICLE.gears.append(drive_1_gear)
        VEHICLE.gears.append(drive_2_gear)
        VEHICLE.gears.append(drive_3_gear)

    elif vehicle_type_enum == VehicleTypeEnum.human_tank:
        reverse_gear = VEHICLE.FrictionPoint()
        reverse_gear.a_min_torque = 100000
        reverse_gear.a_max_torque = 800000
        reverse_gear.a_peak_torque_scale = 0.4
        reverse_gear.a_past_peak_torque_exponent = 0.475
        reverse_gear.a_torque_at_max_angular_velocity = 1000
        reverse_gear.a_torque_at_2x_max_angular_velocity = -1000
        reverse_gear.b_min_torque = 0
        reverse_gear.b_max_torque = -225000
        reverse_gear.b_peak_torque_scale = 0.3
        reverse_gear.b_past_peak_torque_exponent = 0.475
        reverse_gear.b_torque_at_max_angular_velocity = -225000
        reverse_gear.b_torque_at_2x_max_angular_velocity = -450000
        reverse_gear.min_time_to_upshift = 0
        reverse_gear.engine_up_shift_scale = 1
        reverse_gear.gear_ratio = -1.3
        reverse_gear.min_time_to_downshift = 0
        reverse_gear.engine_down_shift_scale = 0

        drive_1_gear = VEHICLE.FrictionPoint()
        drive_1_gear.a_min_torque = 100000
        drive_1_gear.a_max_torque = 800000
        drive_1_gear.a_peak_torque_scale = 0.4
        drive_1_gear.a_past_peak_torque_exponent = 0.475
        drive_1_gear.a_torque_at_max_angular_velocity = 1000
        drive_1_gear.a_torque_at_2x_max_angular_velocity = -1000
        drive_1_gear.b_min_torque = 0
        drive_1_gear.b_max_torque = -225000
        drive_1_gear.b_peak_torque_scale = 0.4
        drive_1_gear.b_past_peak_torque_exponent = 0.475
        drive_1_gear.b_torque_at_max_angular_velocity = -225000
        drive_1_gear.b_torque_at_2x_max_angular_velocity = -450000
        drive_1_gear.min_time_to_upshift = 0.0
        drive_1_gear.engine_up_shift_scale = 1
        drive_1_gear.gear_ratio = 1.3
        drive_1_gear.min_time_to_downshift = 0.0
        drive_1_gear.engine_down_shift_scale = 0.0

        VEHICLE.gears.append(reverse_gear)
        VEHICLE.gears.append(drive_1_gear)

    gear_count = len(VEHICLE.gears)
    VEHICLE.gears_header = TAG.TagBlockHeader("tbfd", 0, gear_count, 68)

    return TAG.TagBlock(gear_count)

def generate_ai_properties(dump_dic, TAG, VEHICLE):
    tag_file_name = os.path.basename(dump_dic['TagName']).lower().replace(" ", "_")
    if "banshee" in tag_file_name:
        ai_property = VEHICLE.AIProperty()
        ai_property.ai_flags = 0
        ai_property.ai_type_name = ""
        ai_property.ai_type_name_length = len(ai_property.ai_type_name)
        ai_property.ai_size = AISizeEnum.large.value
        ai_property.leap_jump_speed = LeapJumpSpeedEnum.none.value
        VEHICLE.ai_properties.append(ai_property)
    elif "c_turret" in tag_file_name:
        ai_property = VEHICLE.AIProperty()
        ai_property.ai_flags = 0
        ai_property.ai_type_name = ""
        ai_property.ai_type_name_length = len(ai_property.ai_type_name)
        ai_property.ai_size = AISizeEnum.immobile.value
        ai_property.leap_jump_speed = LeapJumpSpeedEnum.none.value
        VEHICLE.ai_properties.append(ai_property)
    elif "guntower" in tag_file_name:
        ai_property = VEHICLE.AIProperty()
        ai_property.ai_flags = 0
        ai_property.ai_type_name = ""
        ai_property.ai_type_name_length = len(ai_property.ai_type_name)
        ai_property.ai_size = AISizeEnum.default.value
        ai_property.leap_jump_speed = LeapJumpSpeedEnum.none.value
        VEHICLE.ai_properties.append(ai_property)
    elif "creep" in tag_file_name:
        ai_property = VEHICLE.AIProperty()
        ai_property.ai_flags = 0
        ai_property.ai_type_name = "creep"
        ai_property.ai_type_name_length = len(ai_property.ai_type_name)
        ai_property.ai_size = AISizeEnum.huge.value
        ai_property.leap_jump_speed = LeapJumpSpeedEnum.none.value
        VEHICLE.ai_properties.append(ai_property)
    elif "falcon" in tag_file_name:
        ai_property = VEHICLE.AIProperty()
        ai_property.ai_flags = 0
        ai_property.ai_type_name = ""
        ai_property.ai_type_name_length = len(ai_property.ai_type_name)
        ai_property.ai_size = AISizeEnum.large.value
        ai_property.leap_jump_speed = LeapJumpSpeedEnum.none.value
        VEHICLE.ai_properties.append(ai_property)
    elif "ghost" in tag_file_name:
        ai_property = VEHICLE.AIProperty()
        ai_property.ai_flags = 0
        ai_property.ai_type_name = "ghost"
        ai_property.ai_type_name_length = len(ai_property.ai_type_name)
        ai_property.ai_size = AISizeEnum.medium.value
        ai_property.leap_jump_speed = LeapJumpSpeedEnum.none.value
        VEHICLE.ai_properties.append(ai_property)
    elif "gravity_thone" in tag_file_name:
        ai_property = VEHICLE.AIProperty()
        ai_property.ai_flags = 0
        ai_property.ai_type_name = ""
        ai_property.ai_type_name_length = len(ai_property.ai_type_name)
        ai_property.ai_size = AISizeEnum.medium.value
        ai_property.leap_jump_speed = LeapJumpSpeedEnum.none.value
        VEHICLE.ai_properties.append(ai_property)
    elif "h_turret" in tag_file_name:
        ai_property = VEHICLE.AIProperty()
        ai_property.ai_flags = 0
        ai_property.ai_type_name = ""
        ai_property.ai_type_name_length = len(ai_property.ai_type_name)
        ai_property.ai_size = AISizeEnum.medium.value
        ai_property.leap_jump_speed = LeapJumpSpeedEnum.none.value
        VEHICLE.ai_properties.append(ai_property)
    elif "mongoose" in tag_file_name:
        ai_property = VEHICLE.AIProperty()
        ai_property.ai_flags = 0
        ai_property.ai_type_name = "mongoose"
        ai_property.ai_type_name_length = len(ai_property.ai_type_name)
        ai_property.ai_size = AISizeEnum.medium.value
        ai_property.leap_jump_speed = LeapJumpSpeedEnum.none.value
        VEHICLE.ai_properties.append(ai_property)
    elif "pelican" in tag_file_name:
        ai_property = VEHICLE.AIProperty()
        ai_property.ai_flags = 0
        ai_property.ai_type_name = "pelican"
        ai_property.ai_type_name_length = len(ai_property.ai_type_name)
        ai_property.ai_size = AISizeEnum.huge.value
        ai_property.leap_jump_speed = LeapJumpSpeedEnum.none.value
        VEHICLE.ai_properties.append(ai_property)
    elif "phantom" in tag_file_name:
        ai_property = VEHICLE.AIProperty()
        ai_property.ai_flags = 0
        ai_property.ai_type_name = "phantom"
        ai_property.ai_type_name_length = len(ai_property.ai_type_name)
        ai_property.ai_size = AISizeEnum.huge.value
        ai_property.leap_jump_speed = LeapJumpSpeedEnum.none.value
        VEHICLE.ai_properties.append(ai_property)
    elif "scorpion" in tag_file_name:
        ai_property = VEHICLE.AIProperty()
        ai_property.ai_flags = 0
        ai_property.ai_type_name = "scorpion"
        ai_property.ai_type_name_length = len(ai_property.ai_type_name)
        ai_property.ai_size = AISizeEnum.huge.value
        ai_property.leap_jump_speed = LeapJumpSpeedEnum.none.value
        VEHICLE.ai_properties.append(ai_property)
    elif "spectre" in tag_file_name:
        ai_property = VEHICLE.AIProperty()
        ai_property.ai_flags = 0
        ai_property.ai_type_name = "spectre"
        ai_property.ai_type_name_length = len(ai_property.ai_type_name)
        ai_property.ai_size = AISizeEnum.large.value
        ai_property.leap_jump_speed = LeapJumpSpeedEnum.none.value
        VEHICLE.ai_properties.append(ai_property)
    elif "warthog" in tag_file_name:
        ai_property = VEHICLE.AIProperty()
        ai_property.ai_flags = 0
        ai_property.ai_type_name = "warthog"
        ai_property.ai_type_name_length = len(ai_property.ai_type_name)
        ai_property.ai_size = AISizeEnum.large.value
        ai_property.leap_jump_speed = LeapJumpSpeedEnum.none.value
        VEHICLE.ai_properties.append(ai_property)
    elif "wraith" in tag_file_name:
        ai_property = VEHICLE.AIProperty()
        ai_property.ai_flags = 0
        ai_property.ai_type_name = "wraith"
        ai_property.ai_type_name_length = len(ai_property.ai_type_name)
        ai_property.ai_size = AISizeEnum.huge.value
        ai_property.leap_jump_speed = LeapJumpSpeedEnum.none.value
        VEHICLE.ai_properties.append(ai_property)

    ai_property_count = len(VEHICLE.ai_properties)
    VEHICLE.ai_properties_header = TAG.TagBlockHeader("tbfd", 0, ai_property_count, 16)

    return TAG.TagBlock(ai_property_count)

def get_vehicle_training_data(dump_dic):
    specific_type = SpecificTypeEnum.none.value
    player_training_vehicle_type = PlayerTrainingVehicleTypeEnum.none.value
    flip_message = ""
    tag_file_name = os.path.basename(dump_dic['TagName']).lower().replace(" ", "_")
    if "banshee" in tag_file_name:
        player_training_vehicle_type = PlayerTrainingVehicleTypeEnum.banshee.value
        flip_message = "banshee_flip"
    elif "creep" in tag_file_name:
        flip_message = "shadow_flip"
    elif "ghost" in tag_file_name:
        specific_type = SpecificTypeEnum.ghost.value
        player_training_vehicle_type = PlayerTrainingVehicleTypeEnum.ghost.value
        flip_message = "ghost_flip"
    elif "gravity_throne" in tag_file_name:
        specific_type = SpecificTypeEnum.sentinel_enforcer.value
    elif "pelican" in tag_file_name:
        flip_message = "banshee_flip"
    elif "phantom" in tag_file_name:
        flip_message = "banshee_flip"
    elif "scorpion" in tag_file_name:
        flip_message = "scorpion_flip"
    elif "spectre" in tag_file_name:
        specific_type = SpecificTypeEnum.spectre.value
        flip_message = "spectre_flip"
    elif "warthog" in tag_file_name:
        player_training_vehicle_type = PlayerTrainingVehicleTypeEnum.warthog.value
        flip_message = "warthog_flip"
    elif "wraith" in tag_file_name:
        specific_type = SpecificTypeEnum.wraith.value
        flip_message = "wraith_flip"

    return specific_type, player_training_vehicle_type, flip_message

def get_engine_defaults(dump_dic):
    overdampen_cusp_angle = 0
    overdampen_exponent = 0
    seat_enterance_acceleration_scale = 0.0
    seat_exit_acceleration_scale = 0.0
    engine_moment = 0
    engine_max_angular_velocity = 0
    flying_torque_scale = 0
    air_friction_deceleration = 0.0
    thrust_scale = 0.0
    tag_file_name = os.path.basename(dump_dic['TagName']).lower().replace(" ", "_")
    if "banshee" in tag_file_name:
        overdampen_cusp_angle = 10
        overdampen_exponent = 1.2
        seat_enterance_acceleration_scale = 4.0
        seat_exit_acceleration_scale = 3.0
    elif "c_turret" in tag_file_name:
        overdampen_cusp_angle = 4
        overdampen_exponent = 1.6
        seat_enterance_acceleration_scale = 4.0
        seat_exit_acceleration_scale = 3.0
    elif "creep" in tag_file_name:
        seat_enterance_acceleration_scale = 4.0
        seat_exit_acceleration_scale = 3.0
    elif "falcon" in tag_file_name:
        flying_torque_scale = 0.1
    elif "ghost" in tag_file_name:
        overdampen_cusp_angle = 10
        overdampen_exponent = 1.2
        seat_enterance_acceleration_scale = 3.0
        seat_exit_acceleration_scale = 4.0
    elif "gravity_throne" in tag_file_name:
        flying_torque_scale = 0.01
        air_friction_deceleration = 1
        thrust_scale = 2
    elif "h_turret" in tag_file_name:
        seat_enterance_acceleration_scale = 4.0
        seat_exit_acceleration_scale = 3.0
    elif "mongoose" in tag_file_name:
        overdampen_cusp_angle = 15
        overdampen_exponent = 1.8
        engine_moment = 1500
        engine_max_angular_velocity = 8
        seat_enterance_acceleration_scale = 4.0
        seat_exit_acceleration_scale = 3.0
    elif "pelican" in tag_file_name:
        flying_torque_scale = 2
        seat_enterance_acceleration_scale = 4.0
        seat_exit_acceleration_scale = 3.0
        air_friction_deceleration = 0.25
        thrust_scale = 1.5
    elif "phantom" in tag_file_name:
        flying_torque_scale = 2
        seat_enterance_acceleration_scale = 4.0
        seat_exit_acceleration_scale = 3.0
        air_friction_deceleration = 0.25
        thrust_scale = 1.5
    elif "scorpion" in tag_file_name:
        overdampen_cusp_angle = 4
        overdampen_exponent = 1.3
        engine_moment = 12000
        engine_max_angular_velocity = 2
        seat_enterance_acceleration_scale = 4.0
        seat_exit_acceleration_scale = 3.0
    elif "spectre" in tag_file_name:
        seat_enterance_acceleration_scale = 4.0
        seat_exit_acceleration_scale = 3.0
    elif "warthog" in tag_file_name:
        overdampen_cusp_angle = 5
        overdampen_exponent = 1.2
        engine_moment = 3000
        engine_max_angular_velocity = 7.75
        seat_enterance_acceleration_scale = 3.0
        seat_exit_acceleration_scale = 4.0
    elif "wraith" in tag_file_name:
        overdampen_cusp_angle = 10
        overdampen_exponent = 1.4
        seat_enterance_acceleration_scale = 4.0
        seat_exit_acceleration_scale = 3.0

    return overdampen_cusp_angle, overdampen_exponent, engine_moment, engine_max_angular_velocity, flying_torque_scale, seat_enterance_acceleration_scale, seat_exit_acceleration_scale, air_friction_deceleration, thrust_scale

def get_physics_defaults(dump_dic):
    ground_fricton = 0.0
    ground_depth = 0.0
    ground_damp_factor = 0.0
    ground_moving_friction = 0.0
    ground_maximum_slope_0 = 0.0
    ground_maximum_slope_1 = 0.0
    anti_gravity_bank_lift = 0.0
    steering_bank_reaction_scale = 0.0
    gravity_scale = 0.0
    tag_file_name = os.path.basename(dump_dic['TagName']).lower().replace(" ", "_")
    if "banshee" in tag_file_name:
        gravity_scale = 0.75
    elif "ghost" in tag_file_name:
        anti_gravity_bank_lift = 0.7
        steering_bank_reaction_scale = 9.0
    elif "gravity_throne" in tag_file_name:
        anti_gravity_bank_lift = 0.5
        steering_bank_reaction_scale = 6
        gravity_scale = 0.0000000000000001
    elif "pelican" in tag_file_name:
        gravity_scale = 0.0001
    elif "phantom" in tag_file_name:
        gravity_scale = 0.0001
    elif "scorpion" in tag_file_name:
        ground_fricton = 0.95
        ground_depth = 1
        ground_damp_factor = 1
        ground_moving_friction = 1
        ground_maximum_slope_0 = 60
        ground_maximum_slope_1 = 70
    elif "spectre" in tag_file_name:
        anti_gravity_bank_lift = 0.5
        steering_bank_reaction_scale = 2.5
    elif "warthog" in tag_file_name:
        ground_fricton = 0.85
        ground_depth = 0.15
        ground_damp_factor = 1.5
        ground_moving_friction = 0.014
        ground_maximum_slope_0 = 40
        ground_maximum_slope_1 = 50
    elif "wraith" in tag_file_name:
        anti_gravity_bank_lift = 0.2
        steering_bank_reaction_scale = 6

    return ground_fricton, ground_depth, ground_damp_factor, ground_moving_friction, ground_maximum_slope_0, ground_maximum_slope_1, anti_gravity_bank_lift, steering_bank_reaction_scale, gravity_scale

def upgrade_vehicle(H2_ASSET, patch_txt_path, report, json_directory=None):
    dump_dic = json.load(H2_ASSET)
    phys_dic = None
    model_ref = dump_dic['Data']['Model']["Path"]
    hlmt_path = "%s[%s].json" % (os.path.join(json_directory, model_ref), "hlmt")
    if os.path.isfile(hlmt_path):
        hlmt_stream = open(hlmt_path, 'r')
        hlmt_dic = json.load(hlmt_stream)
        hlmt_stream.close()
        physics_ref = hlmt_dic['Data']['Physics']["Path"]
        phys_path = "%s[%s].json" % (os.path.join(json_directory, physics_ref), "phys")
        if os.path.isfile(phys_path):
            phys_stream = open(phys_path, 'r')
            phys_dic = json.load(phys_stream)
            phys_stream.close()

    TAG = tag_format.TagAsset()
    VEHICLE = VehicleAsset()
    TAG.upgrade_patches = tag_format.get_patch_set(patch_txt_path)

    VEHICLE.header = TAG.Header()
    VEHICLE.header.unk1 = 0
    VEHICLE.header.flags = 0
    VEHICLE.header.type = 0
    VEHICLE.header.name = ""
    VEHICLE.header.tag_group = "vehi"
    VEHICLE.header.checksum = 0
    VEHICLE.header.data_offset = 64
    VEHICLE.header.data_length = 0
    VEHICLE.header.unk2 = 0
    VEHICLE.header.version = 1
    VEHICLE.header.destination = 0
    VEHICLE.header.plugin_handle = -1
    VEHICLE.header.engine_tag = "BLM!"

    VEHICLE.ai_properties = []
    VEHICLE.functions = []
    VEHICLE.attachments = []
    VEHICLE.widgets = []
    VEHICLE.old_functions = []
    VEHICLE.change_colors = []
    VEHICLE.predicted_resources = []
    VEHICLE.camera_tracks = []
    VEHICLE.postures = []
    VEHICLE.new_hud_interface = []
    VEHICLE.dialogue_variants = []
    VEHICLE.powered_seats = []
    VEHICLE.weapons = []
    VEHICLE.seats = []
    VEHICLE.gears = []
    VEHICLE.anti_gravity_point = []
    VEHICLE.friction_points = []
    VEHICLE.phantom_shapes = []

    pitch_range = dump_dic['Data']['Pitch Range']
    seat_acceleration_scale = dump_dic['Data']['Seat Acceleration Scale']
    spawned_actor_count = dump_dic['Data']['Spawned Actor Count']

    unit_type, unit_class = get_metagame_data(dump_dic)
    specific_type, player_training_vehicle_type, flip_message = get_vehicle_training_data(dump_dic)
    overdampen_cusp_angle, overdampen_exponent, engine_moment, engine_max_angular_velocity, flying_torque_scale, seat_enterance_acceleration_scale, seat_exit_acceleration_scale, air_friction_deceleration, thrust_scale = get_engine_defaults(dump_dic)
    ground_fricton, ground_depth, ground_damp_factor, ground_moving_friction, ground_maximum_slope_0, ground_maximum_slope_1, anti_gravity_bank_lift, steering_bank_reaction_scale, gravity_scale = get_physics_defaults(dump_dic)

    function_keywords = [("Object", _20030504_ObjectFunctionsEnum), ("Unit", _20030504_UnitFunctionsEnum), ("Vehicle", _20030504_VehicleFunctionsEnum)]

    VEHICLE.body_header = TAG.TagBlockHeader("tbfd", 0, 1, 984)
    VEHICLE.object_flags = upgrade_e3_object_flags(dump_dic['Data']['Flags'])
    VEHICLE.bounding_radius = dump_dic['Data']['Bounding Radius']
    VEHICLE.bounding_offset = dump_dic['Data']['Bounding Offset']
    VEHICLE.acceleration_scale = dump_dic['Data']['Acceleration Scale']
    VEHICLE.lightmap_shadow_mode = 0
    VEHICLE.sweetner_size = 0
    VEHICLE.dynamic_light_sphere_radius = 0.0
    VEHICLE.dynamic_light_sphere_offset = Vector()
    VEHICLE.default_model_variant = dump_dic['Data']['Default Model Variant']
    VEHICLE.default_model_variant_length = len(dump_dic['Data']['Default Model Variant'])
    VEHICLE.model = TAG.TagRef().convert_from_json(dump_dic['Data']['Model'])
    VEHICLE.crate_object = TAG.TagRef()
    VEHICLE.modifier_shader = TAG.TagRef()
    VEHICLE.creation_effect = TAG.TagRef()
    VEHICLE.material_effects = TAG.TagRef()
    VEHICLE.ai_properties_tag_block = generate_ai_properties(dump_dic, TAG, VEHICLE)
    VEHICLE.functions_tag_block = TAG.TagBlock()
    VEHICLE.apply_collision_damage_scale = 0.0
    VEHICLE.min_game_acc = 0.0
    VEHICLE.max_game_acc = 0.0
    VEHICLE.min_game_scale = 0.0
    VEHICLE.max_game_scale = 0.0
    VEHICLE.min_abs_acc = 0.0
    VEHICLE.max_abs_acc = 0.0
    VEHICLE.min_abs_scale = 0.0
    VEHICLE.max_abs_scale = 0.0
    VEHICLE.hud_text_message_index = dump_dic['Data']['Hud Text Message Index']
    VEHICLE.attachments_tag_block = generate_attachments(dump_dic, TAG, VEHICLE, function_keywords)
    VEHICLE.widgets_tag_block = generate_widgets(dump_dic, TAG, VEHICLE)
    VEHICLE.old_functions_tag_block = TAG.TagBlock()
    VEHICLE.change_colors_tag_block = generate_change_colors(dump_dic, TAG, VEHICLE, function_keywords)
    VEHICLE.predicted_resources_tag_block = TAG.TagBlock()
    VEHICLE.unit_flags = dump_dic['Data']['Unit Flags']
    VEHICLE.default_team = dump_dic['Data']['Default Team']['Value']
    VEHICLE.constant_sound_volume = dump_dic['Data']['Constant Sound Volume']['Value']
    VEHICLE.integrated_light_toggle = TAG.TagRef().convert_from_json(dump_dic['Data']['Integrated Light Toggle'])
    VEHICLE.camera_field_of_view = dump_dic['Data']['Camera Field Of View']
    VEHICLE.camera_stiffness = dump_dic['Data']['Camera Stiffness']
    VEHICLE.camera_marker_name = dump_dic['Data']['Camera Marker Name']
    VEHICLE.camera_marker_name_length = len(VEHICLE.camera_marker_name)
    VEHICLE.camera_submerged_marker_name = dump_dic['Data']['Camera Submerged Marker Name']
    VEHICLE.camera_submerged_marker_name_length = len(VEHICLE.camera_submerged_marker_name)
    VEHICLE.pitch_auto_level = dump_dic['Data']['Pitch Auto-Level']
    VEHICLE.pitch_range = (pitch_range["Min"], pitch_range["Max"])
    VEHICLE.camera_tracks_tag_block = generate_camera_tracks(dump_dic, TAG, VEHICLE)
    VEHICLE.acceleration_range = Vector((seat_acceleration_scale[0], seat_acceleration_scale[1], seat_acceleration_scale[2])) / 30
    VEHICLE.acceleration_action_scale = 0.0
    VEHICLE.acceleration_attach_scale = 0.0
    VEHICLE.soft_ping_threshold = dump_dic['Data']['Soft Ping Threshold']
    VEHICLE.soft_ping_interrupt_time = dump_dic['Data']['Soft Ping Interrupt Time']
    VEHICLE.hard_ping_threshold = dump_dic['Data']['Hard Ping Threshold']
    VEHICLE.hard_ping_interrupt_time = dump_dic['Data']['Hard Ping Interrupt Time']
    VEHICLE.hard_death_threshold = dump_dic['Data']['Hard Death Threshold']
    VEHICLE.feign_death_threshold = dump_dic['Data']['Feign Death Threshold']
    VEHICLE.feign_death_time = dump_dic['Data']['Feign Death Time']
    VEHICLE.distance_of_evade_anim = dump_dic['Data']['Distance Of Evade Anim']
    VEHICLE.distance_of_dive_anim = dump_dic['Data']['Distance Of Dive Anim']
    VEHICLE.stunned_movement_threshold = dump_dic['Data']['Stunned Movement Threshold']
    VEHICLE.feign_death_chance = dump_dic['Data']['Feign Death Chance']
    VEHICLE.feign_repeat_chance = dump_dic['Data']['Feign Repeat Chance']
    VEHICLE.spawned_turret_actor = TAG.TagRef().convert_from_json(dump_dic['Data']['Spawned Actor'], "char")
    VEHICLE.spawned_actor_count = (spawned_actor_count["Min"], spawned_actor_count["Max"])
    VEHICLE.spawned_velocity = dump_dic['Data']['Spawned Velocity']
    VEHICLE.aiming_velocity_maximum = dump_dic['Data']['Aiming Velocity Maximum']
    VEHICLE.aiming_acceleration_maximum = dump_dic['Data']['Aiming Acceleration Maximum']
    VEHICLE.casual_aiming_modifier = dump_dic['Data']['Casual Aiming Modifier']
    VEHICLE.looking_velocity_maximum = dump_dic['Data']['Looking Velocity Maximum']
    VEHICLE.looking_acceleration_maximum = dump_dic['Data']['Looking Acceleration Maximum']
    VEHICLE.right_hand_node = ""
    VEHICLE.right_hand_node_length = len(VEHICLE.right_hand_node)
    VEHICLE.left_hand_node = ""
    VEHICLE.left_hand_node_length = len(VEHICLE.left_hand_node)
    VEHICLE.preferred_gun_node = ""
    VEHICLE.preferred_gun_node_length = len(VEHICLE.preferred_gun_node)
    VEHICLE.melee_damage = TAG.TagRef().convert_from_json(dump_dic['Data']['Melee Damage'])
    VEHICLE.boarding_melee_damage = TAG.TagRef()
    VEHICLE.boarding_melee_response = TAG.TagRef()
    VEHICLE.landing_melee_damage = TAG.TagRef()
    VEHICLE.flurry_melee_damage = TAG.TagRef()
    VEHICLE.obstacle_smash_damage = TAG.TagRef()
    VEHICLE.motion_sensor_blip_size = dump_dic['Data']['Motion Sensor Blip Size']['Value']
    VEHICLE.unit_type = unit_type
    VEHICLE.unit_class = unit_class
    VEHICLE.postures_tag_block = TAG.TagBlock()
    VEHICLE.new_hud_interfaces_tag_block = generate_new_hud_interface(dump_dic, TAG, VEHICLE)
    VEHICLE.dialogue_variants_tag_block = generate_dialogue_variants(dump_dic, TAG, VEHICLE)
    VEHICLE.grenade_velocity = dump_dic['Data']['Grenade Velocity']
    VEHICLE.grenade_type = dump_dic['Data']['Grenade Type']['Value']
    VEHICLE.grenade_count = dump_dic['Data']['Grenade Count']
    VEHICLE.powered_seats_tag_block = generate_powered_seats(dump_dic, TAG, VEHICLE)
    VEHICLE.weapons_tag_block = generate_weapons(dump_dic, TAG, VEHICLE)
    VEHICLE.seats_tag_block = generate_seats(dump_dic, TAG, VEHICLE)
    VEHICLE.boost_peak_power = 0.0
    VEHICLE.boost_rise_power = 0.0
    VEHICLE.boost_peak_time = 0.0
    VEHICLE.boost_fall_power = 0.0
    VEHICLE.dead_time = 0.0
    VEHICLE.attack_weight = 0.0
    VEHICLE.decay_weight = 0.0
    VEHICLE.vehicle_flags = dump_dic['Data']['Vehicle Flags']
    if not VehicleFlags.can_trigger_automatic_opening_doors in VehicleFlags(VEHICLE.vehicle_flags):
        VEHICLE.vehicle_flags += VehicleFlags.can_trigger_automatic_opening_doors.value

    VEHICLE.vehicle_type = dump_dic['Data']['Type']['Value']
    VEHICLE.vehicle_control = dump_dic['Data']['Control']['Value']

    if VehicleTypeEnum(VEHICLE.vehicle_type) == VehicleTypeEnum.turret:
        for seat_element in VEHICLE.seats:
            if SeatFlags.driver in SeatFlags(seat_element.flags):
                seat_element.flags -= SeatFlags.driver.value

    VEHICLE.maximum_forward_speed = dump_dic['Data']['Maximum Forward Speed'] * 30
    VEHICLE.maximum_reverse_speed = dump_dic['Data']['Maximum Reverse Speed'] * 30
    VEHICLE.speed_acceleration = dump_dic['Data']['Speed Acceleration'] * 30**2
    VEHICLE.speed_deceleration = dump_dic['Data']['Speed Deceleration'] * 30**2
    VEHICLE.maximum_left_turn = dump_dic['Data']['Maximum Left Turn']
    VEHICLE.maximum_right_turn = dump_dic['Data']['Maximum Right Turn (Negative)']
    VEHICLE.wheel_circumference = dump_dic['Data']['Wheel Circumference']
    VEHICLE.turn_rate = dump_dic['Data']['Turn Rate']
    VEHICLE.blur_speed = dump_dic['Data']['Blur Speed']
    VEHICLE.specific_type = specific_type
    VEHICLE.player_training_vehicle_type = player_training_vehicle_type
    VEHICLE.flip_message = flip_message
    VEHICLE.flip_message_length = len(VEHICLE.flip_message)
    VEHICLE.turn_scale = dump_dic['Data']['Turn Scale']
    VEHICLE.speed_turn_penalty_power = dump_dic['Data']['Speed Turn Penalty Power (0.5 .. 2)']
    VEHICLE.speed_turn_penalty = dump_dic['Data']["Speed Turn Penalty (0 = None, 1 = Can't Turn At Top Speed)"]

    slide_speed = VEHICLE.maximum_forward_speed / 2
    maximum_left_slide = 0.0
    maximum_right_slide = 0.0
    if not dump_dic['Data']['Maximum Left Slide'] == 0.0:
        maximum_left_slide = slide_speed
    if not dump_dic['Data']['Maximum Right Slide'] == 0.0:
        maximum_right_slide = slide_speed

    VEHICLE.maximum_left_slide = maximum_left_slide
    VEHICLE.maximum_right_slide = maximum_right_slide
    VEHICLE.slide_acceleration = dump_dic['Data']['Slide Acceleration'] * 30
    VEHICLE.slide_deceleration = dump_dic['Data']['Slide Deceleration'] * 30
    VEHICLE.minimum_flipping_angular_velocity = dump_dic['Data']['Minimum Flipping Angular Velocity']
    VEHICLE.maximum_flipping_angular_velocity = dump_dic['Data']['Maximum Flipping Angular Velocity']
    VEHICLE.vehicle_size = dump_dic['Data']['Vehicle Size']['Value']
    VEHICLE.fixed_gun_yaw = dump_dic['Data']['Fixed Gun Yaw']
    VEHICLE.fixed_gun_pitch = dump_dic['Data']['Fixed Gun Pitch']
    VEHICLE.overdampen_cusp_angle = overdampen_cusp_angle
    VEHICLE.overdampen_exponent = overdampen_exponent
    VEHICLE.crouch_transition_time = 0.0
    VEHICLE.engine_moment = engine_moment
    VEHICLE.engine_max_angular_velocity = engine_max_angular_velocity
    VEHICLE.gears_tag_block = generate_gears(TAG, VEHICLE)
    VEHICLE.flying_torque_scale = flying_torque_scale
    VEHICLE.seat_enterance_acceleration_scale = seat_enterance_acceleration_scale
    VEHICLE.seat_exit_acceleration_scale = seat_exit_acceleration_scale
    VEHICLE.air_friction_deceleration = air_friction_deceleration
    VEHICLE.thrust_scale = thrust_scale
    VEHICLE.suspension_sound = TAG.TagRef().convert_from_json(dump_dic['Data']['Suspension Sound'])
    VEHICLE.crash_sound = TAG.TagRef().convert_from_json(dump_dic['Data']['Crash Sound'])
    VEHICLE.unused = TAG.TagRef().convert_from_json(dump_dic['Data']['Material Effects'])
    VEHICLE.special_effect = TAG.TagRef().convert_from_json(dump_dic['Data']['Effect'])
    VEHICLE.unused_effect = TAG.TagRef()
    VEHICLE.physics_flags = 0
    VEHICLE.ground_fricton = ground_fricton
    VEHICLE.ground_depth = ground_depth
    VEHICLE.ground_damp_factor = ground_damp_factor
    VEHICLE.ground_moving_friction = ground_moving_friction
    VEHICLE.ground_maximum_slope_0 = ground_maximum_slope_0
    VEHICLE.ground_maximum_slope_1 = ground_maximum_slope_1
    VEHICLE.anti_gravity_bank_lift = anti_gravity_bank_lift
    VEHICLE.steering_bank_reaction_scale = steering_bank_reaction_scale
    VEHICLE.gravity_scale = gravity_scale
    VEHICLE.radius = 0.0

    generate_vehicle_points(phys_dic, TAG, VEHICLE)
    VEHICLE.phantom_shapes_tag_block = TAG.TagBlock()

    return VEHICLE
