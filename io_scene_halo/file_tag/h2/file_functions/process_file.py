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

from ....global_functions import tag_format
from .format import (
        FunctionTypeEnum,
        OutputTypeFlags,
        TransitionExponentEnum,
        FunctionData
        )

def read_function(TAG, input_stream, xml_node, halo_function):
    halo_function.input_function_data = FunctionData()
    halo_function.range_function_data = FunctionData()
    halo_function.input_function_data.points = []
    halo_function.range_function_data.points = []

    halo_function.MAPP_header = TAG.TagBlockHeader().read(input_stream, TAG)
    halo_function.function_header = TAG.TagBlockHeader().read(input_stream, TAG)
    halo_function.function_type = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(xml_node, "function type", FunctionTypeEnum))
    halo_function.output_type = TAG.read_flag_unsigned_byte(input_stream, TAG, tag_format.XMLData(xml_node, "output type", OutputTypeFlags))
    halo_function.input_function_data.exponent = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(xml_node, "exponent", TransitionExponentEnum))
    halo_function.range_function_data.exponent = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(xml_node, "exponent", TransitionExponentEnum))

    output_type_flags = OutputTypeFlags(halo_function.output_type)
    if OutputTypeFlags._2_color in output_type_flags:
        halo_function.color_a = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(xml_node, "color a"))
        input_stream.read(8) # Padding?
        halo_function.color_b = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(xml_node, "color b"))

    elif OutputTypeFlags._3_color in output_type_flags:
        halo_function.color_a = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(xml_node, "color a"))
        halo_function.color_b = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(xml_node, "color b"))
        input_stream.read(4) # Padding?
        halo_function.color_c = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(xml_node, "color c"))

    elif OutputTypeFlags._4_color in output_type_flags:
        halo_function.color_a = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(xml_node, "color a"))
        halo_function.color_b = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(xml_node, "color b"))
        halo_function.color_c = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(xml_node, "color c"))
        halo_function.color_d = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(xml_node, "color d"))

    else:
        halo_function.lower_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(xml_node, "lower bound"))
        halo_function.upper_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(xml_node, "upper bound"))
        input_stream.read(8) # Padding?

    if FunctionTypeEnum.constant == FunctionTypeEnum(halo_function.function_type):
        input_stream.read(8) # Padding?

    elif FunctionTypeEnum.transition == FunctionTypeEnum(halo_function.function_type):
        halo_function.input_function_data.function_min = TAG.read_float(input_stream, TAG, tag_format.XMLData(xml_node, "min"))
        halo_function.input_function_data.function_max = TAG.read_float(input_stream, TAG, tag_format.XMLData(xml_node, "max"))
        halo_function.range_function_data.function_min = TAG.read_float(input_stream, TAG, tag_format.XMLData(xml_node, "min"))
        halo_function.range_function_data.function_max = TAG.read_float(input_stream, TAG, tag_format.XMLData(xml_node, "max"))

    elif FunctionTypeEnum.periodic == FunctionTypeEnum(halo_function.function_type):
        halo_function.input_function_data.frequency = TAG.read_float(input_stream, TAG, tag_format.XMLData(xml_node, "frequency"))
        halo_function.input_function_data.phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(xml_node, "phase"))
        halo_function.input_function_data.function_min = TAG.read_float(input_stream, TAG, tag_format.XMLData(xml_node, "min"))
        halo_function.input_function_data.function_max = TAG.read_float(input_stream, TAG, tag_format.XMLData(xml_node, "max"))
        halo_function.range_function_data.frequency = TAG.read_float(input_stream, TAG, tag_format.XMLData(xml_node, "frequency"))
        halo_function.range_function_data.phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(xml_node, "phase"))
        halo_function.range_function_data.function_min = TAG.read_float(input_stream, TAG, tag_format.XMLData(xml_node, "min"))
        halo_function.range_function_data.function_max = TAG.read_float(input_stream, TAG, tag_format.XMLData(xml_node, "max"))

    elif FunctionTypeEnum.linear == FunctionTypeEnum(halo_function.function_type):
        for point_idx in range(2):
            halo_function.input_function_data.points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(xml_node, "position")))

        input_stream.read(8) # Padding?
        for point_idx in range(2):
            halo_function.range_function_data.points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(xml_node, "position")))

        input_stream.read(8) # Padding?

    elif FunctionTypeEnum.linear_key == FunctionTypeEnum(halo_function.function_type):
        for point_idx in range(4):
            halo_function.input_function_data.points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(xml_node, "position")))

        input_stream.read(48) # Padding?
        for point_idx in range(4):
            halo_function.range_function_data.points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(xml_node, "position")))

        input_stream.read(48) # Padding?

    elif FunctionTypeEnum.multi_linear_key == FunctionTypeEnum(halo_function.function_type):
        input_stream.read(256) # Padding?

    elif FunctionTypeEnum.spline == FunctionTypeEnum(halo_function.function_type):
        for point_idx in range(4):
            halo_function.input_function_data.points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(xml_node, "position")))

        input_stream.read(16) # Padding?
        for point_idx in range(4):
            halo_function.range_function_data.points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(xml_node, "position")))

        input_stream.read(16) # Padding?

    elif FunctionTypeEnum.multi_spline == FunctionTypeEnum(halo_function.function_type):
        input_stream.read(40) # Padding?

    elif FunctionTypeEnum.exponent == FunctionTypeEnum(halo_function.function_type):
        halo_function.input_function_data.function_min = TAG.read_float(input_stream, TAG, tag_format.XMLData(xml_node, "min"))
        halo_function.input_function_data.function_max = TAG.read_float(input_stream, TAG, tag_format.XMLData(xml_node, "max"))
        halo_function.input_function_data.exponent = TAG.read_float(input_stream, TAG, tag_format.XMLData(xml_node, "exponent"))
        halo_function.range_function_data.function_min = TAG.read_float(input_stream, TAG, tag_format.XMLData(xml_node, "min"))
        halo_function.range_function_data.function_max = TAG.read_float(input_stream, TAG, tag_format.XMLData(xml_node, "max"))
        halo_function.range_function_data.exponent = TAG.read_float(input_stream, TAG, tag_format.XMLData(xml_node, "exponent"))

    elif FunctionTypeEnum.spline2 == FunctionTypeEnum(halo_function.function_type):
        for point_idx in range(4):
            halo_function.input_function_data.points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(xml_node, "position")))

        input_stream.read(16) # Padding?
        for point_idx in range(4):
            halo_function.range_function_data.points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(xml_node, "position")))

        input_stream.read(16) # Padding?
