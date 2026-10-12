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

from enum import Flag, Enum, auto

from ..h1_functions.object import (
    convert_object_flags, 
    generate_ai_properties, 
    generate_attachments, 
    generate_widgets, 
    generate_change_colors, 
    FunctionEnum as ObjectFunctionsEnum
    )
from ..h1_functions.unit import (
    get_hand_defaults,
    generate_new_hud_interface,
    generate_dialogue_variants,
    generate_powered_seats,
    generate_weapons,
    generate_seats,
    FunctionEnum as UnitFunctionsEnum,
    get_metagame_data
    )

class VehicleFunctionsEnum(Enum):
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

class MassPointFlags(Flag):
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

def upgrade_vehicle(h1_vehi_asset, EngineTag):
    h1_vehi_data = h1_vehi_asset["Data"]

    right_hand_node, left_hand_node, preferred_gun_node = get_hand_defaults(h1_vehi_asset)
    unit_type, unit_class = get_metagame_data(h1_vehi_asset)
    specific_type, player_training_vehicle_type, flip_message = get_vehicle_training_data(h1_vehi_asset)
    overdampen_cusp_angle, overdampen_exponent, engine_moment, engine_max_angular_velocity, flying_torque_scale, seat_enterance_acceleration_scale, seat_exit_acceleration_scale, air_friction_deceleration, thrust_scale = get_engine_defaults(h1_vehi_asset)
    ground_fricton, ground_depth, ground_damp_factor, ground_moving_friction, ground_maximum_slope_0, ground_maximum_slope_1, anti_gravity_bank_lift, steering_bank_reaction_scale, gravity_scale = get_physics_defaults(h1_vehi_asset)

    function_keywords = [("Object", ObjectFunctionsEnum), ("Unit", UnitFunctionsEnum), ("Vehicle", VehicleFunctionsEnum)]
    i, j, k = h1_vehi_data["seat acceleration scale"]

    h2_vehi_asset = {
        "TagName": h1_vehi_asset["TagName"],
        "Header": {
            "unk1": 0,
            "flags": 0,
            "tag type": 0,
            "name": "",
            "tag group": "vehi",
            "checksum": 0,
            "data offset": 64,
            "data length": 0,
            "unk2": 0,
            "version": 1,
            "destination": 0,
            "plugin handle": -1,
            "engine tag": EngineTag.H2Latest.value
        },
        "Data": {
            "flags": convert_object_flags(h1_vehi_data["flags"]),
            "bounding radius": h1_vehi_data["bounding radius"],
            "bounding offset": h1_vehi_data["bounding offset"],
            "acceleration scale": h1_vehi_data["acceleration scale"],
            "model": {"group name": "hlmt", "path": ""},
            "ai properties": generate_ai_properties(h1_vehi_asset),
            "hud text message index": h1_vehi_data["hud text message index"],
            "attachments": generate_attachments(h1_vehi_asset, function_keywords),
            "widgets": generate_widgets(h1_vehi_asset),
            "change colors": generate_change_colors(h1_vehi_asset, function_keywords),
            "flags_1": h1_vehi_data["flags_1"],
            "default team": {
                "type": "ShortEnum",
                "value": h1_vehi_data["default team"]["value"],
                "value name": ""
            },
            "constant sound volume": {
                "type": "ShortEnum",
                "value": h1_vehi_data["constant sound volume"]["value"],
                "value name": ""
            },
            "integrated light toggle": h1_vehi_data["integrated light toggle"],
            "camera field of view": h1_vehi_data["camera field of view"],
            "camera stiffness": h1_vehi_data["camera stiffness"],
            "camera marker name": h1_vehi_data["camera marker name"],
            "camera submerged marker name": h1_vehi_data["camera submerged marker name"],
            "pitch auto-level": h1_vehi_data["pitch auto level"],
            "pitch range": h1_vehi_data["pitch range"],
            "camera tracks": h1_vehi_data["camera tracks"],
            
            "acceleration range": [(i * 30), (j * 30), (k * 30)],
            "accel action scale": 0.0,
            "accel attach scale": 0.0,
            "soft ping threshold": h1_vehi_data["soft ping threshold"],
            "soft ping interrupt time": h1_vehi_data["soft ping interrupt time"],
            "hard ping threshold": h1_vehi_data["hard ping threshold"],
            "hard ping interrupt time": h1_vehi_data["hard ping interrupt time"],
            "hard death threshold": h1_vehi_data["hard death threshold"],
            "feign death threshold": h1_vehi_data["feign death threshold"],
            "feign death time": h1_vehi_data["feign death time"],
            "distance of evade anim": h1_vehi_data["distance of evade anim"],
            "distance of dive anim": h1_vehi_data["distance of dive anim"],
            "stunned movement threshold": h1_vehi_data["stunned movement threshold"],
            "feign death chance": h1_vehi_data["feign death chance"],
            "feign repeat chance": h1_vehi_data["feign repeat chance"],
            "spawned velocity": h1_vehi_data["spawned velocity"],
            "aiming velocity maximum": h1_vehi_data["aiming velocity maximum"],
            "aiming acceleration maximum": h1_vehi_data["aiming acceleration maximum"],
            "casual aiming modifier": h1_vehi_data["casual aiming modifier"],
            "looking velocity maximum": h1_vehi_data["looking velocity maximum"],
            "looking acceleration maximum": h1_vehi_data["looking acceleration maximum"],
            "right_hand_node": right_hand_node,
            "left_hand_node": left_hand_node,
            "preferred_gun_node": preferred_gun_node,
            "melee damage": h1_vehi_data["melee damage"],
            "motion sensor blip size": {
                "type": "ShortEnum",
                "value": h1_vehi_data["motion sensor blip size"]["value"],
                "value name": ""
            },
            "type": {
                "type": "CharEnum",
                "value": unit_type,
                "value name": ""
            },
            "class": {
                "type": "CharEnum",
                "value": unit_class,
                "value name": ""
            },
            "NEW HUD INTERFACES": generate_new_hud_interface(h1_vehi_asset),
            "dialogue variants": generate_dialogue_variants(h1_vehi_asset),
            "grenade velocity": h1_vehi_data["grenade velocity"],
            "grenade type": {
                "type": "ShortEnum",
                "value": h1_vehi_data["grenade type"]["value"],
                "value name": ""
            },
            "grenade count": h1_vehi_data["grenade count"],
            "powered seats": generate_powered_seats(h1_vehi_asset),
            "weapons": generate_weapons(h1_vehi_asset),
            "seats": generate_seats(h1_vehi_asset),
            "flags_2": 0,
            "type": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "control": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "maximum forward speed": 0.0,
            "maximum reverse speed": 0.0,
            "speed acceleration": 0.0,
            "speed deceleration": 0.0,
            "maximum left turn": 0.0,
            "maximum right turn (negative)": 0.0,
            "wheel circumference": 0.0,
            "turn rate": 0.0,
            "blur speed": 0.0,
            "specific type": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "player training vehicle type": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "flip message": "",
            "flip message_pad": 0,
            "turn scale": 0.0,
            "speed turn penalty power (0.5 .. 2)": 0.0,
            "speed turn penalty (0 = none, 1 = can't turn at top speed)": 0.0,
            "maximum left slide": 0.0,
            "maximum right slide": 0.0,
            "slide acceleration": 0.0,
            "slide deceleration": 0.0,
            "minimum flipping angular velocity": 0.0,
            "maximum flipping angular velocity": 0.0,
            "vehicle size": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "fixed gun yaw": 0.0,
            "fixed gun pitch": 0.0,
            "overdampen cusp angle": 0.0,
            "overdampen exponent": 0.0,
            "crouch transition time": 0.0,
            "engine moment": 0.0,
            "engine max angular velocity": 0.0,
            "gears": [
                {
                    "StructHeader_loaded torque curve": {
                        "name": "trcv",
                        "version": 0,
                        "size": 24
                    },
                    "min torque": 0.0,
                    "max torque": 0.0,
                    "peak torque scale": 0.0,
                    "past peak torque exponent": 0.0,
                    "torque at max angular velocity": 0.0,
                    "torque at 2x max angular velocity": 0.0,
                    "StructHeader_cruising torque curve": {
                        "name": "trcv",
                        "version": 0,
                        "size": 24
                    },
                    "min torque_1": 0.0,
                    "max torque_1": 0.0,
                    "peak torque scale_1": 0.0,
                    "past peak torque exponent_1": 0.0,
                    "torque at max angular velocity_1": 0.0,
                    "torque at 2x max angular velocity_1": 0.0,
                    "min time to upshift": 0.0,
                    "engine up-shift scale": 0.0,
                    "gear ratio": 0.0,
                    "min time to downshift": 0.0,
                    "engine down-shift scale": 0.0
                }
            ],
            "flying torque scale": 0.0,
            "seat enterance acceleration scale": 0.0,
            "seat exit accelersation scale": 0.0,
            "air friction deceleration": 0.0,
            "thrust scale": 0.0,
            "suspension sound": {
                "group name": "snd!",
                "unk1": 0,
                "length": 0,
                "unk2": -1,
                "path": ""
            },
            "crash sound": {
                "group name": "snd!",
                "unk1": 0,
                "length": 0,
                "unk2": -1,
                "path": ""
            },
            "UNUSED": {
                "group name": "foot",
                "unk1": 0,
                "length": 0,
                "unk2": -1,
                "path": ""
            },
            "special effect": {
                "group name": "effe",
                "unk1": 0,
                "length": 0,
                "unk2": -1,
                "path": ""
            },
            "unused effect": {
                "group name": "effe",
                "unk1": 0,
                "length": 0,
                "unk2": -1,
                "path": ""
            },
            "flags_3": 0,
            "ground friction": 0.0,
            "ground depth": 0.0,
            "ground damp factor": 0.0,
            "ground moving friction": 0.0,
            "ground maximum slope 0": 0.0,
            "ground maximum slope 1": 0.0,
            "anti_gravity_bank_lift": 0.0,
            "steering_bank_reaction_scale": 0.0,
            "gravity scale": 0.0,
            "radius": 0.0,
            "anti gravity points": [
                {
                    "marker name": "",
                    "marker name_pad": 0,
                    "flags": 0,
                    "antigrav strength": 0.0,
                    "antigrav offset": 0.0,
                    "antigrav height": 0.0,
                    "antigrav damp factor": 0.0,
                    "antigrav normal k1": 0.0,
                    "antigrav normal k0": 0.0,
                    "radius": 0.0,
                    "damage source region name": "",
                    "damage source region name_pad": 0,
                    "default state error": 0.0,
                    "minor damage error": 0.0,
                    "medium damage error": 0.0,
                    "major damage error": 0.0,
                    "destroyed state error": 0.0
                }
            ],
            "friction points": [
                {
                    "marker name": "",
                    "marker name_pad": 0,
                    "flags": 0,
                    "fraction of total mass": 0.0,
                    "radius": 0.0,
                    "damaged radius": 0.0,
                    "friction type": {
                        "type": "ShortEnum",
                        "value": 0,
                        "value name": ""
                    },
                    "moving friction velocity diff": 0.0,
                    "e-brake moving friction": 0.0,
                    "e-brake friction": 0.0,
                    "e-brake moving friction vel diff": 0.0,
                    "collision global material name": "",
                    "collision global material name_pad": 0,
                    "model state destroyed": {
                        "type": "ShortEnum",
                        "value": 0,
                        "value name": ""
                    },
                    "region name": "",
                    "region name_pad": 0
                }
            ],
            "shape phantom shape": []
        }
    }

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
