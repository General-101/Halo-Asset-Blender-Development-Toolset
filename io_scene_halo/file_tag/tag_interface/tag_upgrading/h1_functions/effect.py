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

from math import radians
from enum import Flag, Enum, auto
from mathutils import Vector, Euler
from .....global_functions import global_functions

class H1EffectFlags(Flag):
    deleted_when_attachment_deactivates = auto()
    must_be_deterministic_xbox = auto()
    must_be_deterministic_pc = auto()
    disabled_in_anniversary_by_blood_setting = auto()

class H2EffectFlags(Flag):
    deleted_when_attachment_deactivates = auto()

class H1PartFlags(Flag):
    face_down_regardless_of_location_decals = auto()
    unused = auto()
    make_effect_work = auto()

class H2PartFlags(Flag):
    face_down_regardless_of_location_decals = auto()
    offset_origin_away_from_geometry_lights = auto()
    never_attached_to_object = auto()
    disabled_for_debugging = auto()
    draw_regardless_of_distance = auto()

def convert_effect_flags(effect_flags):
    flags = 0
    active_h1_flags = H1EffectFlags(effect_flags)
    if H1EffectFlags.deleted_when_attachment_deactivates in active_h1_flags:
        flags += H2EffectFlags.deleted_when_attachment_deactivates.value

    return flags

def convert_part_flags(effect_flags):
    flags = 0
    active_h1_flags = H1PartFlags(effect_flags)
    if H1PartFlags.face_down_regardless_of_location_decals in active_h1_flags:
        flags += H2PartFlags.face_down_regardless_of_location_decals.value

    return flags

def generate_locations(h1_effe_asset):
    locations_block = []
    for location_element in h1_effe_asset["Data"]["locations"]:
        location_name = location_element["marker name"]
        if global_functions.string_empty_check(location_name):
            location_name = "root"

        locations_block.append({"marker name": location_name})

    return locations_block

def generate_particle_properties(dump_dic, prt2_dic, effect_dic, TAG, EFFECT, emitter, particle_system_element, charge_effects, script_effects):
    dic_data = dump_dic["Data"]

    emission_rate_results = shader_processing.get_property_values("Emission Rate", dic_data, dic_data)
    emission_rate_input_type = emission_rate_results[0]
    emission_rate_range_type = emission_rate_results[1]
    emission_rate_output_modifier = emission_rate_results[2]
    emission_rate_output_modifier_input = emission_rate_results[3]
    emission_rate_function_type = emission_rate_results[4]
    emission_rate_flag_value = emission_rate_results[5]
    emission_rate_rgb_0 = emission_rate_results[6]
    emission_rate_rgb_1 = emission_rate_results[7]
    emission_rate_rgb_2 = emission_rate_results[8]
    emission_rate_rgb_3 = emission_rate_results[9]
    max_particle_rate = dic_data['Max Particle Count']
    emission_rate_value_0 = emission_rate_results[10]
    emission_rate_value_1 = emission_rate_results[11]
    if True:
        emission_rate_value_0 = emission_rate_results[11]
        emission_rate_value_1 = emission_rate_results[10]

    if emission_rate_value_0 > max_particle_rate:
        emission_rate_value_0 = max_particle_rate
    if emission_rate_value_1 > max_particle_rate:
        emission_rate_value_1 = max_particle_rate

    # Emission rate changes from seconds to ticks in E3 to retail.
    if emission_rate_value_0 > 0 and not effect_dic['TagName'] in charge_effects:
        emission_rate_value_0 /= 30

    if emission_rate_value_1 > 0 and not effect_dic['TagName'] in charge_effects:
        emission_rate_value_1 /= 30

    if not emission_rate_value_0 == 0.0 and emission_rate_value_0 < 0.035:
        emission_rate_value_0 = 0.035

    if not emission_rate_value_1 == 0.0 and emission_rate_value_1 < 0.035:
        emission_rate_value_1 = 0.035

    emission_rate_value_2 = emission_rate_results[12]
    emission_rate_value_3 = emission_rate_results[13]
    emission_rate_function_0_type = emission_rate_results[14]
    emission_rate_function_1_type = emission_rate_results[15]
    emission_rate_function_values = emission_rate_results[16]
    if not prt2_dic == None:
        prt2_data = prt2_dic["Data"]
        lifespan_results = shader_processing.get_property_values("Lifetime", prt2_data, prt2_data)
    else:
        lifespan_results = shader_processing.get_property_values("Lifespan", dic_data, dic_data)

    lifespan_input_type = lifespan_results[0]
    lifespan_range_type = lifespan_results[1]
    lifespan_output_modifier = lifespan_results[2]
    lifespan_output_modifier_input = lifespan_results[3]
    lifespan_function_type = lifespan_results[4]
    lifespan_flag_value = lifespan_results[5]
    lifespan_rgb_0 = lifespan_results[6]
    lifespan_rgb_1 = lifespan_results[7]
    lifespan_rgb_2 = lifespan_results[8]
    lifespan_rgb_3 = lifespan_results[9]
    lifespan_value_0 = lifespan_results[10]
    lifespan_value_1 = lifespan_results[11]
    if True:
        lifespan_value_0 = lifespan_results[11]
        lifespan_value_1 = lifespan_results[10]

    if lifespan_value_0 < 0.1:
        lifespan_value_0 = 0.1

    if lifespan_value_1 < 0.1:
        lifespan_value_1 = 0.1

    lifespan_value_2 = lifespan_results[12]
    lifespan_value_3 = lifespan_results[13]
    lifespan_function_0_type = lifespan_results[14]
    lifespan_function_1_type = lifespan_results[15]
    lifespan_function_values = lifespan_results[16]

    particle_velocity_results = shader_processing.get_property_values("Particle Velocity", dic_data, dic_data)
    particle_velocity_input_type = particle_velocity_results[0]
    particle_velocity_range_type = particle_velocity_results[1]
    particle_velocity_output_modifier = particle_velocity_results[2]
    particle_velocity_output_modifier_input = particle_velocity_results[3]
    particle_velocity_function_type = particle_velocity_results[4]
    particle_velocity_flag_value = particle_velocity_results[5]
    particle_velocity_rgb_0 = particle_velocity_results[6]
    particle_velocity_rgb_1 = particle_velocity_results[7]
    particle_velocity_rgb_2 = particle_velocity_results[8]
    particle_velocity_rgb_3 = particle_velocity_results[9]
    particle_velocity_value_0 = particle_velocity_results[10]
    particle_velocity_value_1 = particle_velocity_results[11]
    if FunctionTypeEnum.constant == FunctionTypeEnum(particle_velocity_function_type) and particle_velocity_value_0 == 0.0:
        particle_velocity_value_0 = particle_velocity_results[11]
        particle_velocity_value_1 = particle_velocity_results[10]

    particle_velocity_value_2 = particle_velocity_results[12]
    particle_velocity_value_3 = particle_velocity_results[13]
    particle_velocity_function_0_type = particle_velocity_results[14]
    particle_velocity_function_1_type = particle_velocity_results[15]
    particle_velocity_function_values = particle_velocity_results[16]

    emitter.particle_properties = []

    shader_processing.convert_legacy_function(EFFECT, TAG, emitter.particle_properties, emission_rate_input_type, emission_rate_range_type, emission_rate_function_type,
                                              emission_rate_flag_value, emission_rate_output_modifier, emission_rate_output_modifier_input, emission_rate_rgb_0, emission_rate_rgb_1,
                                              emission_rate_rgb_2, emission_rate_rgb_3, emission_rate_value_0,
                                              emission_rate_value_1, emission_rate_value_2, emission_rate_value_3, emission_rate_function_0_type,
                                              emission_rate_function_1_type, emission_rate_function_values, TAG.TagBlockHeader("PRPS", 0, 1, 20))
    shader_processing.convert_legacy_function(EFFECT, TAG, emitter.particle_properties, lifespan_input_type, lifespan_range_type, lifespan_function_type, lifespan_flag_value,
                                              lifespan_output_modifier, lifespan_output_modifier_input, lifespan_rgb_0, lifespan_rgb_1, lifespan_rgb_2, lifespan_rgb_3,
                                              lifespan_value_0, lifespan_value_1, lifespan_value_2, lifespan_value_3, lifespan_function_0_type, lifespan_function_1_type,
                                              lifespan_function_values, TAG.TagBlockHeader("PRPS", 0, 1, 20))
    shader_processing.convert_legacy_function(EFFECT, TAG, emitter.particle_properties, particle_velocity_input_type, particle_velocity_range_type, particle_velocity_function_type,
                                              particle_velocity_flag_value, particle_velocity_output_modifier, particle_velocity_output_modifier_input, particle_velocity_rgb_0,
                                              particle_velocity_rgb_1, particle_velocity_rgb_2, particle_velocity_rgb_3, particle_velocity_value_0, particle_velocity_value_1,
                                              particle_velocity_value_2, particle_velocity_value_3, particle_velocity_function_0_type, particle_velocity_function_1_type,
                                              particle_velocity_function_values, TAG.TagBlockHeader("PRPS", 0, 1, 20))
    shader_processing.convert_legacy_function(EFFECT, TAG, emitter.particle_properties, value_0=1.0, value_1=1.0, function_header=TAG.TagBlockHeader("PRPS", 0, 1, 20))
    shader_processing.convert_legacy_function(EFFECT, TAG, emitter.particle_properties, value_0=1.0, value_1=1.0, function_header=TAG.TagBlockHeader("PRPS", 0, 1, 20))
    shader_processing.convert_legacy_function(EFFECT, TAG, emitter.particle_properties, flag_value=OutputTypeFlags._2_color.value, function_header=TAG.TagBlockHeader("PRPC", 0, 1, 20))
    shader_processing.convert_legacy_function(EFFECT, TAG, emitter.particle_properties, value_0=1.0, value_1=1.0, function_header=TAG.TagBlockHeader("PRPS", 0, 1, 20))

def generate_emission_properties(dump_dic, emit_dic, TAG, EFFECT, emitter):
    dic_data = dump_dic["Data"]

    radius_results = shader_processing.get_property_values("Radius", emit_dic, dic_data)
    radius_input_type = radius_results[0]
    radius_range_type = radius_results[1]
    radius_output_modifier = radius_results[2]
    radius_output_modifier_input = radius_results[3]
    radius_function_type = radius_results[4]
    radius_flag_value = radius_results[5]
    radius_rgb_0 = radius_results[6]
    radius_rgb_1 = radius_results[7]
    radius_rgb_2 = radius_results[8]
    radius_rgb_3 = radius_results[9]
    radius_value_0 = radius_results[10]
    radius_value_1 = radius_results[11]
    if FunctionTypeEnum.constant == FunctionTypeEnum(radius_function_type) and radius_value_0 == 0.0:
        radius_value_0 = radius_results[11]
        radius_value_1 = radius_results[10]

    radius_value_2 = radius_results[12]
    radius_value_3 = radius_results[13]
    radius_function_0_type = radius_results[14]
    radius_function_1_type = radius_results[15]
    radius_function_values = radius_results[16]

    cone_angle_results = shader_processing.get_property_values("Cone Angle", emit_dic, dic_data)
    cone_angle_input_type = cone_angle_results[0]
    cone_angle_range_type = cone_angle_results[1]
    cone_angle_output_modifier = cone_angle_results[2]
    cone_angle_output_modifier_input = cone_angle_results[3]
    cone_angle_function_type = cone_angle_results[4]
    cone_angle_flag_value = cone_angle_results[5]
    cone_angle_rgb_0 = cone_angle_results[6]
    cone_angle_rgb_1 = cone_angle_results[7]
    cone_angle_rgb_2 = cone_angle_results[8]
    cone_angle_rgb_3 = cone_angle_results[9]
    cone_angle_value_0 = cone_angle_results[10]
    cone_angle_value_1 = cone_angle_results[11]
    if FunctionTypeEnum.constant == FunctionTypeEnum(cone_angle_function_type) and cone_angle_value_0 == 0.0:
        cone_angle_value_0 = cone_angle_results[11]
        cone_angle_value_1 = cone_angle_results[10]

    cone_angle_value_2 = cone_angle_results[12]
    cone_angle_value_3 = cone_angle_results[13]
    cone_angle_function_0_type = cone_angle_results[14]
    cone_angle_function_1_type = cone_angle_results[15]
    cone_angle_function_values = cone_angle_results[16]

    emitter.emission_properties = []
    shader_processing.convert_legacy_function(EFFECT, TAG, emitter.emission_properties, radius_input_type, radius_range_type, radius_function_type, radius_flag_value,
                                              radius_output_modifier, radius_output_modifier_input, radius_rgb_0, radius_rgb_1, radius_rgb_2, radius_rgb_3, radius_value_0,
                                              radius_value_1, radius_value_2, radius_value_3, radius_function_0_type, radius_function_1_type, radius_function_values,
                                              TAG.TagBlockHeader("PRPS", 0, 1, 20))
    shader_processing.convert_legacy_function(EFFECT, TAG, emitter.emission_properties, cone_angle_input_type, cone_angle_range_type, cone_angle_function_type, cone_angle_flag_value,
                                              cone_angle_output_modifier, cone_angle_output_modifier_input, cone_angle_rgb_0, cone_angle_rgb_1, cone_angle_rgb_2, cone_angle_rgb_3,
                                              cone_angle_value_0, cone_angle_value_1, cone_angle_value_2, cone_angle_value_3, cone_angle_function_0_type, cone_angle_function_1_type,
                                              cone_angle_function_values, TAG.TagBlockHeader("PRPS", 0, 1, 20))

def generate_events(h1_effe_asset):
    events_block = []
    for h1_event_element in h1_effe_asset["Data"]["events"]:
        duration_min = h1_event_element["duration bounds"]["Min"]
        if duration_min > 0:
            duration_min /= 30

        duration_max = h1_event_element["duration bounds"]["Max"]
        if duration_max > 0:
            duration_max /= 30

        if not duration_min == 0.0 and duration_min < 0.25:
            duration_min = 0.25

        if not duration_max == 0.0 and duration_max < 0.25:
            duration_max = 0.25

        part_block = []
        particle_systems = []
        for part in h1_event_element["parts"]:
            part_element = {
                "create in": {
                    "type": "ShortEnum",
                    "value": part["create in"]["value"],
                    "value name": ""
                },
                "create in_1": {
                    "type": "ShortEnum",
                    "value": part["violence mode"]["value"],
                    "value name": ""
                },
                "location": part["location"],
                "flags": convert_part_flags(part["flags"]),
                "type": part["type"],
                "velocity bounds": part["velocity bounds"],
                "velocity cone angle": part["velocity cone angle"],
                "angular velocity bounds": part["angular velocity bounds"],
                "radius modifier bounds": part["radius modifier bounds"],
                "A scales values": part["a scales values"],
                "B scales values": part["b scales values"]
            }

            part_block.append(part_element)

        for particle in h1_event_element["particles"]:
            particle["particle type"]["path"]
            particle_element = {
                        "particle": {
                            "group name": "prt3",
                            "path": "effects\\generic\\smoke\\smoke_fiery_small"
                        },
                        "location": 0,
                        "coordinate system": {
                            "type": "ShortEnum",
                            "value": 1,
                            "value name": ""
                        },
                        "environment": {
                            "type": "ShortEnum",
                            "value": 0,
                            "value name": ""
                        },
                        "disposition": {
                            "type": "ShortEnum",
                            "value": 0,
                            "value name": ""
                        },
                        "camera mode": {
                            "type": "ShortEnum",
                            "value": 0,
                            "value name": ""
                        },
                        "sort bias": 5,
                        "flags": 2,
                        "LOD in distance": 0.0,
                        "LOD feather in delta": 0.0,
                        "LOD out distance": 1000.0,
                        "LOD feather out delta": 0.0,
                        "emitters": []
                    }

            particle_systems.append(particle_element)

        h2_event_element = {
            "skip fraction": h1_event_element["skip fraction"],
            "delay bounds": h1_event_element["delay bounds"],
            "duration bounds": {"Min": duration_min, "Max": duration_max},
            "parts": part_block,
            "beams": [],
            "accelerations": [],
            "particle systems": particle_systems
        },
    
        events_block.append(h2_event_element)

    return events_block

def upgrade_effect(h1_effe_asset, report):
    locations_block = generate_locations(h1_effe_asset)
    events_block = generate_events(h1_effe_asset)
    h2_effe_asset = {
        "Data": {
            "flags": convert_effect_flags(h1_effe_asset["Data"]["flags"]),
            "loop start event": h1_effe_asset["Data"]["loop start event"],
            "loop stop event": -1,
            "maximum damage radius": 0.0,
            "locations": locations_block,
            "events": events_block
        }
    }

    return h2_effe_asset
