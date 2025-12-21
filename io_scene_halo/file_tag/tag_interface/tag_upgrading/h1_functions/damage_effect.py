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

import io
import struct

from enum import Flag, Enum, auto

class FunctionTypeEnum(Enum):
    identity = 0
    constant = auto()
    transition = auto()
    periodic = auto()
    linear = auto()
    linear_key = auto()
    multi_linear_key = auto()
    spline = auto()
    multi_spline = auto()
    exponent = auto()
    spline2 = auto()

class MappingFlags(Flag):
    scalar_intensity = 0
    _range = 1
    constant = 16
    _2_color = 32
    _3_color = 48
    _4_color = 64

def read_byte(function_stream, endian_override):
    struct_string = '%sb' % endian_override
    return (struct.unpack(struct_string, function_stream.read(1)))[0]

def read_real(function_stream, endian_override):
    struct_string = '%sf' % endian_override
    return (struct.unpack(struct_string, function_stream.read(4)))[0]

def read_bgra(function_stream, endian_override):
    struct_string = '%s4B' % endian_override
    a, r, g, b = struct.unpack(struct_string, function_stream.read(4))[::-1]
    return {"A": a/255,"R": r/255, "G": g/255, "B": b/255}

def read_real_point_2d(function_stream, endian_override):
    struct_string = '%s2f' % endian_override
    return (struct.unpack(struct_string, function_stream.read(8)))

def write_real(function_stream, endian_override, value):
    struct_string = '%sf' % endian_override
    function_stream.write(struct.pack(struct_string, value))

def write_bgra(function_stream, endian_override, argb):
    struct_string = '%s4B' % endian_override
    function_stream.write(struct.pack(struct_string, *reversed(argb.values())))

def write_real_point_2d(function_stream, endian_override, value):
    struct_string = '%s2f' % endian_override
    function_stream.write(struct.pack(struct_string, *value))

def normalize_list(value, size, default=0):
    if not isinstance(value, list):
        return [default] * size
    
    return (value + [default] * size)[:size]

def create_function(function_type=0, flags=0, function_1=0, function_2=0, mapping_inputs=[], function_inputs=[]):
    data_field = []
    endian_override = "<"
    function_stream = io.BytesIO()
    function_stream.write(struct.pack('%sb' % endian_override, function_type))
    function_stream.write(struct.pack('%sb' % endian_override, flags))
    function_stream.write(struct.pack('%sb' % endian_override, function_1))
    function_stream.write(struct.pack('%sb' % endian_override, function_2))
    mapping_flags = MappingFlags(flags)
    if MappingFlags._2_color in mapping_flags:
        color_inputs = normalize_list(mapping_inputs, 2, (0, 0, 0, 0))
        write_bgra(function_stream, endian_override, color_inputs[0]) # Color A
        function_stream.write(bytes(8))
        write_bgra(function_stream, endian_override, color_inputs[1]) # Color B

    elif MappingFlags._3_color in mapping_flags:
        color_inputs = normalize_list(mapping_inputs, 3, (0, 0, 0, 0))
        write_bgra(function_stream, endian_override, color_inputs[0]) # Color A
        write_bgra(function_stream, endian_override, color_inputs[1]) # Color B
        function_stream.write(bytes(4))
        write_bgra(function_stream, endian_override, color_inputs[2]) # Color C

    elif MappingFlags._4_color in mapping_flags:
        color_inputs = normalize_list(mapping_inputs, 4, (0, 0, 0, 0))
        write_bgra(function_stream, endian_override, color_inputs[0]) # Color A
        write_bgra(function_stream, endian_override, color_inputs[1]) # Color B
        write_bgra(function_stream, endian_override, color_inputs[2]) # Color C
        write_bgra(function_stream, endian_override, color_inputs[4]) # Color D

    else:
        float_inputs = normalize_list(mapping_inputs, 2, 0.0)
        write_real(function_stream, endian_override, float_inputs[0]) # Lower Bound
        write_real(function_stream, endian_override, float_inputs[1]) # Upper Bound
        function_stream.write(bytes(8))

    if FunctionTypeEnum.constant == FunctionTypeEnum(function_type):
        function_stream.write(bytes(8))

    elif FunctionTypeEnum.transition == FunctionTypeEnum(function_type):
        float_inputs = normalize_list(function_inputs, 4, 0.0)
        write_real(function_stream, endian_override, float_inputs[0]) # Function Min
        write_real(function_stream, endian_override, float_inputs[1]) # Function Max
        write_real(function_stream, endian_override, float_inputs[2]) # Range Function Min
        write_real(function_stream, endian_override, float_inputs[3]) # Range Function Max

    elif FunctionTypeEnum.periodic == FunctionTypeEnum(function_type):
        float_inputs = normalize_list(function_inputs, 8, 0.0)
        write_real(function_stream, endian_override, float_inputs[0]) # Frequency
        write_real(function_stream, endian_override, float_inputs[1]) # Phase
        write_real(function_stream, endian_override, float_inputs[2]) # Function Min
        write_real(function_stream, endian_override, float_inputs[3]) # Function Max
        write_real(function_stream, endian_override, float_inputs[4]) # Range Frequency
        write_real(function_stream, endian_override, float_inputs[5]) # Range Phase
        write_real(function_stream, endian_override, float_inputs[6]) # Range Function Min
        write_real(function_stream, endian_override, float_inputs[7]) # Range Function Max

    elif FunctionTypeEnum.linear == FunctionTypeEnum(function_type):
        point_inputs = normalize_list(function_inputs, 4, (0.0, 0.0))
        for point_input in point_inputs[0:2]:
            write_real_point_2d(function_stream, endian_override, point_input)

        function_stream.write(bytes(8))
        for point_input in point_inputs[2:4]:
            write_real_point_2d(function_stream, endian_override, point_input)

        function_stream.write(bytes(8))

    elif FunctionTypeEnum.linear_key == FunctionTypeEnum(function_type):
        point_inputs = normalize_list(function_inputs, 8, (0.0, 0.0))
        for point_input in point_inputs[0:4]:
            write_real_point_2d(function_stream, endian_override, point_input)

        function_stream.write(bytes(48))
        for point_input in point_inputs[4:8]:
           write_real_point_2d(function_stream, endian_override, point_input)

        function_stream.write(bytes(48))

    elif FunctionTypeEnum.multi_linear_key == FunctionTypeEnum(function_type):
        function_stream.write(bytes(256))

    elif FunctionTypeEnum.spline == FunctionTypeEnum(function_type):
        point_inputs = normalize_list(function_inputs, 8, (0.0, 0.0))
        for point_input in point_inputs[0:4]:
            write_real_point_2d(function_stream, endian_override, point_input)

        function_stream.write(bytes(16))
        for point_input in point_inputs[4:8]:
            write_real_point_2d(function_stream, endian_override, point_input)

        function_stream.write(bytes(16))

    elif FunctionTypeEnum.multi_spline == FunctionTypeEnum(function_type):
        function_stream.write(bytes(40))

    elif FunctionTypeEnum.exponent == FunctionTypeEnum(function_type):
        float_inputs = normalize_list(function_inputs, 6, 0.0)
        write_real(function_stream, endian_override, float_inputs[0]) # Function Min
        write_real(function_stream, endian_override, float_inputs[1]) # Function Max
        write_real(function_stream, endian_override, float_inputs[2]) # Exponent
        write_real(function_stream, endian_override, float_inputs[3]) # Range Function Min
        write_real(function_stream, endian_override, float_inputs[4]) # Range Function Max
        write_real(function_stream, endian_override, float_inputs[5]) # Range Exponent

    elif FunctionTypeEnum.spline2 == FunctionTypeEnum(function_type):
        point_inputs = normalize_list(function_inputs, 8, (0.0, 0.0))
        for point_input in point_inputs[0:4]:
            write_real_point_2d(function_stream, endian_override, point_input)

        function_stream.write(bytes(16))
        for point_input in point_inputs[4:8]:
            write_real_point_2d(function_stream, endian_override, point_input)

        function_stream.write(bytes(16))

    for byte in function_stream.getbuffer():
        signed_byte = byte if byte < 128 else byte - 256
        data_field.append({"Value": signed_byte})

    return data_field

def generate_player_responses(dump_dic):
    player_responses_block = []
    player_response_dict = {
        "response type": {
            "type": "ShortEnum",
            "value": 0,
            "value name": ""
        },
        "type": {
            "type": "ShortEnum",
            "value": dump_dic["type"]["value"],
            "value name": ""
        },
        "priority": {
            "type": "ShortEnum",
            "value": dump_dic["priority"]["value"],
            "value name": ""
        },
        "duration": dump_dic["duration"],
        "fade function": {
            "type": "ShortEnum",
            "value": dump_dic["fade function"]["value"],
            "value name": ""
        },
        "maximum intensity": dump_dic["maximum intensity"],
        "color": dump_dic["color"],
        "duration_1": dump_dic["duration_1"],
        "data": create_function(function_type=FunctionTypeEnum.transition.value, function_1=dump_dic["fade function_1"]["value"], function_inputs=[dump_dic["frequency"], 0.0]),
        "duration_2": dump_dic["duration_2"],
        "data_1": create_function(function_type=FunctionTypeEnum.transition.value, function_1=dump_dic["fade function_2"]["value"], function_inputs=[dump_dic["frequency_1"], 0.0]),
        "effect name": "",
        "duration_3": 0.0,
        "data_2": create_function()
    }
        
    player_responses_block.append(player_response_dict)

    return player_responses_block

def upgrade_damage_effect(h1_jpt_asset, EngineTag):
    h1_jpt_data = h1_jpt_asset["Data"]

    h2_jpt_asset = {
        "TagName": h1_jpt_asset["TagName"],
        "Header": {
            "unk1": 0, 
            "flags": 0, 
            "tag type": 0, 
            "name": "", 
            "tag group": "jpt!", 
            "checksum": 0, 
            "data offset": 64, 
            "data length": 0, 
            "unk2": 0, 
            "version": 6, 
            "destination": 0, 
            "plugin handle": -1, 
            "engine tag": EngineTag.H2Latest.value
        },
        "Data": {
            "radius": h1_jpt_data["radius"],
            "cutoff scale": h1_jpt_data["cutoff scale"],
            "flags": h1_jpt_data["flags"],
            "side effect": {
                "type": "ShortEnum",
                "value": h1_jpt_data["side effect"]["value"],
                "value name": ""
            },
            "category": {
                "type": "ShortEnum",
                "value": h1_jpt_data["category"]["value"],
                "value name": ""
            },
            "flags_1": h1_jpt_data["flags_1"],
            "AOE core radius": h1_jpt_data["AOE core radius"],
            "damage lower bound": h1_jpt_data["lower bound"],
            "damage upper bound": h1_jpt_data["upper bound"],
            "dmg inner cone angle": 0.0,
            "dmg outer cone angle": 0.0,
            "active camouflage damage": h1_jpt_data["active camouflage damage"],
            "stun": h1_jpt_data["stun"],
            "maximum stun": h1_jpt_data["maximum stun"],
            "stun time": h1_jpt_data["stun time"],
            "instantaneous acceleration": h1_jpt_data["instantaneous acceleration"][0],
            "rider direct damage scale": 0.0,
            "rider maximum transfer damage scale": 0.0,
            "rider minimum transfer damage scale": 0.0,
            "general_damage": "",
            "specific_damage": "",
            "AI stun radius": 0.0,
            "AI stun bounds": {
                "Min": 0.0,
                "Max": 0.0
            },
            "shake radius": 0.0,
            "EMP radius": 0.0,
            "player responses": generate_player_responses(h1_jpt_data),
            "duration": h1_jpt_data["duration_3"],
            "fade function": {
                "type": "ShortEnum",
                "value": h1_jpt_data["fade function_3"]["value"],
                "value name": ""
            },
            "rotation": h1_jpt_data["rotation"],
            "pushback": h1_jpt_data["pushback"],
            "jitter": h1_jpt_data["jitter"],
            "duration_1": h1_jpt_data["duration_4"],
            "falloff function": {
                "type": "ShortEnum",
                "value": h1_jpt_data["falloff function"]["value"],
                "value name": ""
            },
            "random translation": h1_jpt_data["random translation"],
            "random rotation": h1_jpt_data["random rotation"],
            "wobble function": {
                "type": "ShortEnum",
                "value": h1_jpt_data["wobble function"]["value"],
                "value name": ""
            },
            "wobble function period": h1_jpt_data["wobble period"],
            "wobble weight": h1_jpt_data["wobble weight"],
            "sound": h1_jpt_data["sound"],
            "forward velocity": h1_jpt_data["forward velocity"],
            "forward radius": h1_jpt_data["forward radius"],
            "forward exponent": h1_jpt_data["forward exponent"],
            "outward velocity": h1_jpt_data["outward velocity"],
            "outward radius": h1_jpt_data["outward radius"],
            "outward exponent": h1_jpt_data["outward exponent"]
        }
    }

    return h2_jpt_asset
