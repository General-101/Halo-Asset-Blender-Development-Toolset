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

class AnimationFunctionEnum(Enum):
    one = 0
    zero = auto()
    cosine = auto()
    cosine_variable_period = auto()
    diagonal_wave = auto()
    diagonal_wave_variable_period = auto()
    slide = auto()
    slide_variable_period = auto()
    noise = auto()
    jitter = auto()
    wander = auto()
    spark = auto()

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
