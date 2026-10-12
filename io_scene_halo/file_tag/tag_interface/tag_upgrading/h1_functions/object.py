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

class H1ObjectFlags(Flag):
    does_not_cast_shadow = auto()
    transparent_self_occlusion = auto()
    brighter_than_it_should_be = auto()
    not_a_pathfinding_obstacle = auto()
    extension_of_parent = auto()
    cast_shadow_by_default = auto()
    does_not_have_anniversary_geometry = auto()

class H2ObjectFlags(Flag):
    does_not_cast_shadow = auto()
    search_cardinal_direction_lightmaps_on_failure = auto()
    unused2 = auto()
    not_a_pathfinding_obstacle = auto()
    extension_of_parent = auto()
    does_not_cause_collision_damage = auto()
    early_mover = auto()
    early_mover_localized_physics = auto()
    use_static_massive_lightmap_sample = auto()
    object_scales_attachments = auto()
    inherits_players_appearance = auto()
    dead_bipeds_cant_localize = auto()
    attach_to_clusters_by_dynamic_sphere = auto()
    effects_created_by_this_object_do_not_spawn_objects_in_multiplayer = auto()
    prophet_is_not_displayed_in_pegasus_builds = auto()

class AISizeEnum(Enum):
    default = 0
    tiny = auto()
    small = auto()
    medium = auto()
    large = auto()
    huge = auto()
    immobile = auto()

class LeapJumpSpeedEnum(Enum):
    none = 0
    down = auto()
    step = auto()
    crouch = auto()
    stand = auto()
    storey = auto()
    tower = auto()
    infinite = auto()

class FunctionScaleEnum(Enum):
    none = 0
    a_in = auto()
    b_in = auto()
    c_in = auto()
    d_in = auto()
    a_out = auto()
    b_out = auto()
    c_out = auto()
    d_out = auto()

class FunctionEnum(Enum):
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

def convert_object_flags(object_flags):
    flags = 0
    active_h1_flags = H1ObjectFlags(object_flags)
    if H1ObjectFlags.does_not_cast_shadow in active_h1_flags:
        flags += H2ObjectFlags.does_not_cast_shadow.value

    if H1ObjectFlags.not_a_pathfinding_obstacle in active_h1_flags:
        flags += H2ObjectFlags.not_a_pathfinding_obstacle.value

    if H1ObjectFlags.extension_of_parent in active_h1_flags:
        flags += H2ObjectFlags.extension_of_parent.value

    return flags

def generate_ai_properties(dump_dic): 
    tag_file_name = os.path.basename(dump_dic["TagName"]).lower().replace(" ", "_")
    ai_size = 0
    leap_jump_speed = 0
    if "brute" in tag_file_name:
        ai_size = AISizeEnum.large.value
        leap_jump_speed = LeapJumpSpeedEnum.none.value
    elif "elite" in tag_file_name:
        ai_size = AISizeEnum.large.value
        leap_jump_speed = LeapJumpSpeedEnum.none.value
    elif "grunt" in tag_file_name:
        ai_size = AISizeEnum.medium.value
        leap_jump_speed = LeapJumpSpeedEnum.none.value
    elif "jackal" in tag_file_name:
        ai_size = AISizeEnum.medium.value
        leap_jump_speed = LeapJumpSpeedEnum.none.value
    elif "marine" in tag_file_name:
        ai_size = AISizeEnum.medium.value
        leap_jump_speed = LeapJumpSpeedEnum.none.value
    elif "masterchief" in tag_file_name:
        ai_size = AISizeEnum.large.value
        leap_jump_speed = LeapJumpSpeedEnum.none.value

    ai_property_element = {
        "ai flags": 0,
        "ai type name": "",
        "ai type name_pad": 0,
        "ai size": {
            "type": "ShortEnum",
            "value": ai_size,
            "value name": ""
        },
        "leap jump speed": {
            "type": "ShortEnum",
            "value": leap_jump_speed,
            "value name": ""
        }
    }

    return [ai_property_element]

def get_valid_h1_object_functions(function_name):
    valid_function_name = ""
    if function_name == "body_vitality":
        valid_function_name = "body_vitality"
    elif function_name == "shield_vitality":
        valid_function_name = "shield_vitality"
    elif function_name == "alive":
        valid_function_name = "alive"
    elif function_name == "compass":
        valid_function_name = "compass"

    return valid_function_name

def get_valid_h1_weapon_functions(function_name):
    valid_function_name = ""
    if function_name == "ready":
        valid_function_name = "ready"
    elif function_name == "heat":
        valid_function_name = "heat"
    elif function_name == "overheated":
        valid_function_name = "overheated"
    elif function_name == "illumination":
        valid_function_name = "illumination"
    elif function_name == "primary_ammunition":
        valid_function_name = "primary_ammunition"
    elif function_name == "secondary_ammunition":
        valid_function_name = "secondary_ammunition"
    elif function_name == "primary_ejection_port":
        valid_function_name = "primary_ejection_port"
    elif function_name == "secondary_ejection_port":
        valid_function_name = "secondary_ejection_port"
    elif function_name == "primary_rate_of_fire":
        valid_function_name = "primary_rate_of_fire"
    elif function_name == "secondary_rate_of_fire":
        valid_function_name = "secondary_rate_of_fire"
    elif function_name == "primary_firing_on":
        valid_function_name = "primary_firing"
    elif function_name == "secondary_firing_on":
        valid_function_name = "secondary_firing"
    elif function_name == "primary_charged":
        valid_function_name = "primary_charged"
    elif function_name == "secondary_charged":
        valid_function_name = "secondary_charged"
    elif function_name == "integrated_light":
        valid_function_name = "integrated_light"
    elif function_name == "age":
        valid_function_name = "age"
    return valid_function_name

def get_function_list(dump_dic, function_list, keyword, FunctionsEnum):
    if "Object" == keyword:
        a_scale_function = FunctionsEnum(dump_dic["Data"]["a in"]["value"])
        b_scale_function = FunctionsEnum(dump_dic["Data"]["b in"]["value"])
        c_scale_function = FunctionsEnum(dump_dic["Data"]["c in"]["value"])
        d_scale_function = FunctionsEnum(dump_dic["Data"]["d in"]["value"])
        if a_scale_function != FunctionsEnum.none:
            function_list[0] = get_valid_h1_object_functions(a_scale_function.name)
        if b_scale_function != FunctionsEnum.none:
            function_list[1] = get_valid_h1_object_functions(b_scale_function.name)
        if c_scale_function != FunctionsEnum.none:
            function_list[2] = get_valid_h1_object_functions(c_scale_function.name)
        if d_scale_function != FunctionsEnum.none:
            function_list[3] = get_valid_h1_object_functions(d_scale_function.name)
    elif "Weapon" == keyword:
        a_scale_function = FunctionsEnum(dump_dic["Data"]["weapon a in"]["value"])
        b_scale_function = FunctionsEnum(dump_dic["Data"]["weapon b in"]["value"])
        c_scale_function = FunctionsEnum(dump_dic["Data"]["weapon c in"]["value"])
        d_scale_function = FunctionsEnum(dump_dic["Data"]["weapon d in"]["value"])
        if a_scale_function != FunctionsEnum.none:
            function_list[0] = get_valid_h1_weapon_functions(a_scale_function.name)
        if b_scale_function != FunctionsEnum.none:
            function_list[1] = get_valid_h1_weapon_functions(b_scale_function.name)
        if c_scale_function != FunctionsEnum.none:
            function_list[2] = get_valid_h1_weapon_functions(c_scale_function.name)
        if d_scale_function != FunctionsEnum.none:
            function_list[3] = get_valid_h1_weapon_functions(d_scale_function.name)

def get_scale_function(function_tag_block, function_index, function_list):
    scale_name = ""
    function_count = len(function_tag_block)
    function_element = function_tag_block[function_index]
    scale_function = FunctionScaleEnum(function_element["scale function by"]["value"])
    if scale_function != FunctionScaleEnum.none and scale_function.value < 5:
        if scale_function.value == 1 and function_count >= 1:
            scale_name = function_list[0]
        elif scale_function.value == 2 and function_count >= 2:
            scale_name = function_list[1]
        elif scale_function.value == 3 and function_count >= 3:
            scale_name = function_list[2]
        elif scale_function.value == 4 and function_count >= 4:
            scale_name = function_list[3]

    return scale_name

def convert_attachment_scale(dump_dic, function_channel, function_keywords):
    function_list = ["", "", "", ""]
    for function_keyword in function_keywords:
        get_function_list(dump_dic, function_list, function_keyword[0], function_keyword[1])

    scale_name = ""
    function_tag_block = dump_dic["Data"]["functions"]
    function_count = len(function_tag_block)
    if function_channel == 1 and function_count >= 1:
        scale_name = get_scale_function(function_tag_block, 0, function_list)
    elif function_channel == 2 and function_count >= 2:
        scale_name = get_scale_function(function_tag_block, 1, function_list)
    elif function_channel == 3 and function_count >= 3:
        scale_name = get_scale_function(function_tag_block, 2, function_list)
    elif function_channel == 4 and function_count >= 4:
        scale_name = get_scale_function(function_tag_block, 3, function_list)

    return scale_name

def generate_attachments(dump_dic, function_keywords):
    attachment_block = []
    for attachment_element in dump_dic["Data"]["attachments"]:
        attachment_dict = {
            "type": attachment_element["type"],
            "marker": attachment_element["marker"],
            "change color": {
                "type": "ShortEnum",
                "value": attachment_element["change color"]["value"],
                "value name": ""
            },
            "primary scale": convert_attachment_scale(dump_dic, attachment_element["primary scale"]["value"], function_keywords),
            "secondary scale": convert_attachment_scale(dump_dic, attachment_element["secondary scale"]["value"], function_keywords)
        }

        attachment_block.append(attachment_dict)

    return attachment_block

def generate_widgets(dump_dic):
    widget_block = []
    for widget_element in dump_dic["Data"]["widgets"]:
        widget_dict = {
            "type": widget_element["reference"]
        }

        widget_block.append(widget_dict)

    return widget_block

def generate_change_colors(dump_dic, function_keywords):
    color_change_block = []
    for change_color_element in dump_dic["Data"]["change colors"]:
        color_change_dict = {
            "initial permutations": [],
            "functions": []
        }

        for permutation_element in change_color_element["permutations"]:
            permutation_dict = {
                "weight": permutation_element["weight"],
                "color lower bound": permutation_element["color lower bound"],
                "color upper bound": permutation_element["color upper bound"],
                "variant name": ""
            }

            color_change_dict["initial permutations"].append(permutation_dict)

        function_dict = {
            "scale flags": change_color_element["flags"],
            "color lower bound": change_color_element["color lower bound"],
            "color upper bound": change_color_element["color upper bound"],
            "darken by": convert_attachment_scale(dump_dic, change_color_element["darken by"]["value"], function_keywords),
            "scale by": convert_attachment_scale(dump_dic, change_color_element["scale by"]["value"], function_keywords)
        }

        color_change_dict["functions"].append(function_dict)

        color_change_block.append(color_change_dict)

    return color_change_block
