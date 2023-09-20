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

import struct

from .format_retail import (
        FunctionTypeEnum
        )

def write_body(output_stream, TAG, SHADER):
    SHADER.shader_body_header.write(output_stream, TAG, True)
    SHADER.shader_body.template.write(output_stream, False, True)
    output_stream.write(struct.pack('>I', len(SHADER.shader_body.material_name)))
    SHADER.shader_body.runtime_properties.write(output_stream, False)
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<H', SHADER.shader_body.flags))
    SHADER.shader_body.parameters.write(output_stream, False)
    SHADER.shader_body.postprocess_definition.write(output_stream, False)
    output_stream.write(struct.pack('<4x'))
    SHADER.shader_body.predicted_resources.write(output_stream, False)
    SHADER.shader_body.light_response.write(output_stream, False, True)
    output_stream.write(struct.pack('<H', SHADER.shader_body.shader_lod_bias))
    output_stream.write(struct.pack('<H', SHADER.shader_body.specular_type))
    output_stream.write(struct.pack('<H', SHADER.shader_body.lightmap_type))
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<f', SHADER.shader_body.lightmap_specular_brightness))
    output_stream.write(struct.pack('<f', SHADER.shader_body.lightmap_ambient_bias))
    SHADER.shader_body.postprocess_properties.write(output_stream, False)
    output_stream.write(struct.pack('<f', SHADER.shader_body.added_depth_bias_offset))
    output_stream.write(struct.pack('<f', SHADER.shader_body.added_depth_bias_slope))

    template_name_length = len(SHADER.shader_body.template.name)
    material_name_length = len(SHADER.shader_body.material_name)
    if template_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % template_name_length, TAG.string_to_bytes(SHADER.shader_body.template.name, False)))
    if material_name_length > 0:
        output_stream.write(struct.pack('<%ss' % material_name_length, TAG.string_to_bytes(SHADER.shader_body.material_name, False)))

def write_identity(output_stream, TAG, animation_properties):
    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("tbfd", True), 0, 20, 1))
    output_stream.write(struct.pack('<B', animation_properties.function_type))
    output_stream.write(struct.pack('<B', animation_properties.range_check))
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<f', animation_properties.lower_bound))
    output_stream.write(struct.pack('<f', animation_properties.upper_bound))
    output_stream.write(struct.pack('<8x'))

def write_constant(output_stream, TAG, animation_properties):
    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("tbfd", True), 0, 28, 1))
    output_stream.write(struct.pack('<B', animation_properties.function_type))
    output_stream.write(struct.pack('<B', animation_properties.range_check))
    output_stream.write(struct.pack('<2x'))
    if animation_properties.range_check > 1:
        output_stream.write(struct.pack('<BBBB', animation_properties.color_a[0], animation_properties.color_a[1], animation_properties.color_a[2], animation_properties.color_a[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_b[0], animation_properties.color_b[1], animation_properties.color_b[2], animation_properties.color_b[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_c[0], animation_properties.color_c[1], animation_properties.color_c[2], animation_properties.color_c[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_d[0], animation_properties.color_d[1], animation_properties.color_d[2], animation_properties.color_d[3]))
    else:
        output_stream.write(struct.pack('<f', animation_properties.lower_bound))
        output_stream.write(struct.pack('<f', animation_properties.upper_bound))
        output_stream.write(struct.pack('<8x'))

    output_stream.write(struct.pack('<f', 1))
    output_stream.write(struct.pack('<f', 1))

def write_parameters(output_stream, TAG, parameters, parameters_header):
    if len(parameters) > 0:
        parameters_header.write(output_stream, TAG, True)
        for parameter_element in parameters:
            output_stream.write(struct.pack('>I', len(parameter_element.name)))
            output_stream.write(struct.pack('<H', parameter_element.type))
            output_stream.write(struct.pack('<2x'))
            parameter_element.bitmap.write(output_stream, False, True)
            output_stream.write(struct.pack('<f', parameter_element.const_value))
            output_stream.write(struct.pack('<fff', parameter_element.const_color[0], parameter_element.const_color[1], parameter_element.const_color[2]))
            parameter_element.animation_properties_tag_block.write(output_stream, False)

        for parameter_element in parameters:
            name_length = len(parameter_element.name)
            bitmap_name_length = len(parameter_element.bitmap.name)
            if name_length > 0:
                output_stream.write(struct.pack('<%ss' % name_length, TAG.string_to_bytes(parameter_element.name, False)))
            if bitmap_name_length > 0:
                output_stream.write(struct.pack('<%ssx' % bitmap_name_length, TAG.string_to_bytes(parameter_element.bitmap.name, False)))

            if len(parameter_element.animation_properties) > 0:
                parameter_element.animation_properties_tag_block_header.write(output_stream, TAG, True)
                for animation_properties in parameter_element.animation_properties:
                    output_stream.write(struct.pack('<H', animation_properties.type))
                    output_stream.write(struct.pack('<2x'))
                    output_stream.write(struct.pack('>I', len(animation_properties.input_name)))
                    output_stream.write(struct.pack('>I', len(animation_properties.range_name)))
                    output_stream.write(struct.pack('<f', animation_properties.time_period))

                    function_type = FunctionTypeEnum(animation_properties.function_type)
                    if FunctionTypeEnum.identity == function_type:
                        output_stream.write(struct.pack('<I', 20))
                    elif FunctionTypeEnum.constant == function_type:
                        output_stream.write(struct.pack('<I', 28))
                    elif FunctionTypeEnum.transition == function_type:
                        output_stream.write(struct.pack('<I', 36))
                    elif FunctionTypeEnum.periodic == function_type:
                        output_stream.write(struct.pack('<I', 52))
                    elif FunctionTypeEnum.linear == function_type:
                        output_stream.write(struct.pack('<I', 68))
                    elif FunctionTypeEnum.linear_key == function_type:
                        output_stream.write(struct.pack('<I', 180))
                    elif FunctionTypeEnum.multi_linear_key == function_type:
                        output_stream.write(struct.pack('<I', 276))
                    elif FunctionTypeEnum.spline == function_type:
                        output_stream.write(struct.pack('<I', 116))
                    elif FunctionTypeEnum.multi_spline == function_type:
                        output_stream.write(struct.pack('<I', 52))
                    elif FunctionTypeEnum.exponent == function_type:
                        output_stream.write(struct.pack('<I', 44))
                    elif FunctionTypeEnum.spline2 == function_type:
                        output_stream.write(struct.pack('<I', 116))

                    output_stream.write(struct.pack('<8x'))

                for animation_properties in parameter_element.animation_properties:
                    input_name_length = len(animation_properties.input_name)
                    range_name_length = len(animation_properties.range_name)
                    if input_name_length > 0:
                        output_stream.write(struct.pack('<%ss' % input_name_length, TAG.string_to_bytes(animation_properties.input_name, False)))
                    if range_name_length > 0:
                        output_stream.write(struct.pack('<%ss' % range_name_length, TAG.string_to_bytes(animation_properties.range_name, False)))

                    animation_properties.map_property_header.write(output_stream, TAG, True)
                    function_type = FunctionTypeEnum(animation_properties.function_type)
                    if FunctionTypeEnum.identity == function_type:
                        write_identity(output_stream, TAG, animation_properties)
                    elif FunctionTypeEnum.constant == function_type:
                        write_constant(output_stream, TAG, animation_properties)
                    elif FunctionTypeEnum.transition == function_type:
                        write_constant(output_stream, TAG, animation_properties)
                    elif FunctionTypeEnum.periodic == function_type:
                        write_constant(output_stream, TAG, animation_properties)
                    elif FunctionTypeEnum.linear == function_type:
                        write_constant(output_stream, TAG, animation_properties)
                    elif FunctionTypeEnum.linear_key == function_type:
                        write_constant(output_stream, TAG, animation_properties)
                    elif FunctionTypeEnum.multi_linear_key == function_type:
                        write_constant(output_stream, TAG, animation_properties)
                    elif FunctionTypeEnum.spline == function_type:
                        write_constant(output_stream, TAG, animation_properties)
                    elif FunctionTypeEnum.multi_spline == function_type:
                        write_constant(output_stream, TAG, animation_properties)
                    elif FunctionTypeEnum.exponent == function_type:
                        write_constant(output_stream, TAG, animation_properties)
                    elif FunctionTypeEnum.spline2 == function_type:
                        write_constant(output_stream, TAG, animation_properties)

def build_asset(output_stream, tag_format, SHADER, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    SHADER.header.write(output_stream, False, True)
    write_body(output_stream, TAG, SHADER)

    write_parameters(output_stream, TAG, SHADER.parameters, SHADER.parameters_header)
