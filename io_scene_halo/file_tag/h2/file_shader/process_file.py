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

from xml.dom import minidom
from ....global_functions import tag_format
from .format import (
    ShaderAsset, 
    ShaderFlags, 
    ShaderLODBiasEnum, 
    SpecularTypeEnum,
    LightmapTypeEnum,
    TypeEnum,
    AnimationTypeEnum,
    FunctionTypeEnum,
    TransitionExponentEnum
    )

XML_OUTPUT = True

def initilize_shader(SHADER):
    SHADER.runtime_properties = []
    SHADER.parameters = []
    SHADER.postprocess_definition = []
    SHADER.predicted_resources = []
    SHADER.postprocess_properties = []

def read_shader_body_v0(SHADER, TAG, input_stream, tag_node, XML_OUTPUT):
    SHADER.shader_body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    SHADER.shader_body = SHADER.ShaderBody()
    SHADER.shader_body.template = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "template"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    SHADER.shader_body.material_name_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    SHADER.shader_body.runtime_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "runtime properties"))
    input_stream.read(2) # Padding?
    SHADER.shader_body.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ShaderFlags))
    SHADER.shader_body.parameters_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "parameters"))
    SHADER.shader_body.postprocess_definition_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "postprocess definition"))
    input_stream.read(16) # Padding?
    SHADER.shader_body.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    SHADER.shader_body.light_response = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "light response"))
    SHADER.shader_body.shader_lod_bias = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "shader lod bias", ShaderLODBiasEnum))
    SHADER.shader_body.specular_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "specular type", SpecularTypeEnum))
    SHADER.shader_body.lightmap_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap type", LightmapTypeEnum))
    input_stream.read(2) # Padding?
    SHADER.shader_body.lightmap_specular_brightness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap specular brightness"))
    SHADER.shader_body.lightmap_ambient_bias = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap ambient bias"))
    SHADER.shader_body.postprocess_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))


def read_shader_body_retail(SHADER, TAG, input_stream, tag_node, XML_OUTPUT):
    SHADER.shader_body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    SHADER.shader_body = SHADER.ShaderBody()
    SHADER.shader_body.template = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "template"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    SHADER.shader_body.material_name_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    SHADER.shader_body.runtime_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "runtime properties"))
    input_stream.read(2) # Padding?
    SHADER.shader_body.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ShaderFlags))
    SHADER.shader_body.parameters_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "parameters"))
    SHADER.shader_body.postprocess_definition_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "postprocess definition"))
    input_stream.read(4) # Padding?
    SHADER.shader_body.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    SHADER.shader_body.light_response = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "light response"))
    SHADER.shader_body.shader_lod_bias = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "shader lod bias", ShaderLODBiasEnum))
    SHADER.shader_body.specular_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "specular type", SpecularTypeEnum))
    SHADER.shader_body.lightmap_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap type", LightmapTypeEnum))
    input_stream.read(2) # Padding?
    SHADER.shader_body.lightmap_specular_brightness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap specular brightness"))
    SHADER.shader_body.lightmap_ambient_bias = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap ambient bias"))
    SHADER.shader_body.postprocess_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    if SHADER.shader_body_header.size >= 128:
        SHADER.shader_body.added_depth_bias_offset = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "added depth bias offset"))
        SHADER.shader_body.added_depth_bias_slope = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "added depth bias slope"))

def read_runtime_properties(SHADER, TAG, input_stream, tag_node, XML_OUTPUT):
    if SHADER.shader_body.runtime_properties_tag_block.count > 0:
        runtime_properties_node = tag_format.get_xml_node(XML_OUTPUT, SHADER.shader_body.runtime_properties_tag_block.count, tag_node, "name", "runtime properties")
        SHADER.runtime_properties_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for runtime_property_idx in range(SHADER.shader_body.runtime_properties_tag_block.count):
            runtime_property_element_node = None
            if XML_OUTPUT:
                runtime_property_element_node = TAG.xml_doc.createElement('element')
                runtime_property_element_node.setAttribute('index', str(runtime_property_idx))
                runtime_properties_node.appendChild(runtime_property_element_node)

            runtime_property = SHADER.RuntimeProperty()
            runtime_property.diffuse_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "diffuse map"))
            runtime_property.lightmap_emissive_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap emissive map"))
            runtime_property.lightmap_emissive_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap emissive color"))
            runtime_property.lightmap_emissive_power = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap emissive power"))
            runtime_property.lightmap_resolution_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap resolution scale"))
            runtime_property.lightmap_half_life = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap half life"))
            runtime_property.lightmap_diffuse_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap diffuse scale"))
            runtime_property.alphatest_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "alphatest map"))
            runtime_property.translucent_map = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "translucent map"))
            runtime_property.lightmap_transparent_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap transparent color"))
            runtime_property.lightmap_transparent_alpha = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap transparent alpha"))
            runtime_property.lightmap_foliage_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap foliage scale"))

            SHADER.runtime_properties.append(runtime_property)

        for runtime_property_idx, runtime_property in enumerate(SHADER.runtime_properties):
            runtime_property_element_node = None
            if XML_OUTPUT:
                runtime_property_element_node = runtime_properties_node.childNodes[runtime_property_idx]

            if runtime_property.diffuse_map.name_length > 0:
                runtime_property.diffuse_map.name = TAG.read_variable_string(input_stream, runtime_property.diffuse_map.name_length, TAG)

            if runtime_property.lightmap_emissive_map.name_length > 0:
                runtime_property.lightmap_emissive_map.name = TAG.read_variable_string(input_stream, runtime_property.lightmap_emissive_map.name_length, TAG)

            if runtime_property.alphatest_map.name_length > 0:
                runtime_property.alphatest_map.name = TAG.read_variable_string(input_stream, runtime_property.alphatest_map.name_length, TAG)

            if runtime_property.translucent_map.name_length > 0:
                runtime_property.translucent_map.name = TAG.read_variable_string(input_stream, runtime_property.translucent_map.name_length, TAG)

            if XML_OUTPUT:
                diffuse_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "diffuse map")
                lightmap_emissive_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "lightmap emissive map")
                alphatest_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "alphatest map")
                translucent_map_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "translucent map")
                runtime_property.diffuse_map.append_xml_attributes(diffuse_map_node)
                runtime_property.lightmap_emissive_map.append_xml_attributes(lightmap_emissive_map_node)
                runtime_property.alphatest_map.append_xml_attributes(alphatest_map_node)
                runtime_property.translucent_map.append_xml_attributes(translucent_map_node)

def read_parameters(SHADER, TAG, input_stream, tag_node, XML_OUTPUT):
    if SHADER.shader_body.parameters_tag_block.count > 0:
        parameters_node = tag_format.get_xml_node(XML_OUTPUT, SHADER.shader_body.parameters_tag_block.count, tag_node, "name", "parameters")
        SHADER.parameters_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for parameter_idx in range(SHADER.shader_body.parameters_tag_block.count):
            parameter_element_node = None
            if XML_OUTPUT:
                parameter_element_node = TAG.xml_doc.createElement('element')
                parameter_element_node.setAttribute('index', str(parameter_idx))
                parameters_node.appendChild(parameter_element_node)

            parameter = SHADER.Parameter()

            TAG.big_endian = True
            input_stream.read(2) # Padding?
            parameter.name_length = TAG.read_signed_short(input_stream, TAG)
            TAG.big_endian = False

            parameter.type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(parameter_element_node, "type", TypeEnum))
            input_stream.read(2) # Padding?
            parameter.bitmap = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(parameter_element_node, "bitmap"))
            parameter.const_value = TAG.read_float(input_stream, TAG, tag_format.XMLData(parameter_element_node, "const value"))
            parameter.const_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(parameter_element_node, "const color"))
            parameter.animation_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(parameter_element_node, "animation properties"))

            SHADER.parameters.append(parameter)

        for parameter_idx, parameter in enumerate(SHADER.parameters):
            parameter_element_node = None
            if XML_OUTPUT:
                parameter_element_node = parameters_node.childNodes[parameter_idx]

            if parameter.name_length > 0:
                parameter.name = TAG.read_variable_string_no_terminator(input_stream, parameter.name_length, TAG, tag_format.XMLData(parameter_element_node, "name"))

            if parameter.bitmap.name_length > 0:
                parameter.bitmap.name = TAG.read_variable_string(input_stream, parameter.bitmap.name_length, TAG)

            if XML_OUTPUT:
                bitmap_node = tag_format.get_xml_node(XML_OUTPUT, 1, parameter_element_node, "name", "bitmap")
                parameter.bitmap.append_xml_attributes(bitmap_node)

            parameter.animation_properties = []
            if parameter.animation_properties_tag_block.count > 0:
                animation_properties_node = tag_format.get_xml_node(XML_OUTPUT, parameter.animation_properties_tag_block.count, parameter_element_node, "name", "animation properties")
                parameter.animation_properties_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for animation_property_idx in range(parameter.animation_properties_tag_block.count):
                    animation_property_element_node = None
                    if XML_OUTPUT:
                        animation_property_element_node = TAG.xml_doc.createElement('element')
                        animation_property_element_node.setAttribute('index', str(animation_property_idx))
                        animation_properties_node.appendChild(animation_property_element_node)

                    animation_property = SHADER.AnimationProperty()
                    animation_property.type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "type", AnimationTypeEnum))
                    input_stream.read(2) # Padding?

                    TAG.big_endian = True
                    input_stream.read(2) # Padding?
                    animation_property.input_name_length = TAG.read_signed_short(input_stream, TAG)
                    input_stream.read(2) # Padding?
                    animation_property.range_name_length = TAG.read_signed_short(input_stream, TAG)
                    TAG.big_endian = False

                    animation_property.time_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "time period"))
                    input_stream.read(12) # Padding?

                    parameter.animation_properties.append(animation_property)

                for animation_property_idx, animation_property in enumerate(parameter.animation_properties):
                    animation_property_element_node = None
                    if XML_OUTPUT:
                        animation_property_element_node = animation_properties_node.childNodes[animation_property_idx]

                    if animation_property.input_name_length > 0:
                        animation_property.input_name = TAG.read_variable_string_no_terminator(input_stream, animation_property.input_name_length, TAG, tag_format.XMLData(animation_property_element_node, "input name"))
                    if animation_property.range_name_length > 0:
                        animation_property.range_name = TAG.read_variable_string_no_terminator(input_stream, animation_property.range_name_length, TAG, tag_format.XMLData(animation_property_element_node, "range name"))

                    animation_property.map_property_header = TAG.TagBlockHeader().read(input_stream, TAG)
                    animation_property.function_header = TAG.TagBlockHeader().read(input_stream, TAG)
                    animation_property.function_type = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "type", FunctionTypeEnum))
                    animation_property.range_check = bool(TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "range")))
                    if FunctionTypeEnum.identity == FunctionTypeEnum(animation_property.function_type):
                        input_stream.read(2) # Padding?
                        animation_property.lower_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "lower bound"))
                        animation_property.upper_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "upper bound"))
                        input_stream.read(8) # Padding?
                    elif FunctionTypeEnum.constant == FunctionTypeEnum(animation_property.function_type):
                        input_stream.read(2) # Padding?
                        animation_property.lower_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "lower bound"))
                        animation_property.upper_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "upper bound"))
                        input_stream.read(16) # Padding?

                    elif FunctionTypeEnum.transition == FunctionTypeEnum(animation_property.function_type):
                        animation_property.input_function_data = SHADER.FunctionData()
                        animation_property.range_function_data = SHADER.FunctionData()
                        animation_property.input_function_data.points = []
                        animation_property.range_function_data.points = []

                        animation_property.input_function_data.exponent = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "exponent", TransitionExponentEnum))
                        animation_property.range_function_data.exponent = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "function", TransitionExponentEnum))
                        animation_property.lower_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "lower bound"))
                        animation_property.upper_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "upper bound"))
                        input_stream.read(8) # Padding?
                        animation_property.input_function_data.min = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "min"))
                        animation_property.input_function_data.max = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "max"))
                        animation_property.range_function_data.min = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "min"))
                        animation_property.range_function_data.max = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "max"))

                    elif FunctionTypeEnum.periodic == FunctionTypeEnum(animation_property.function_type):
                        animation_property.input_function_data = SHADER.FunctionData()
                        animation_property.range_function_data = SHADER.FunctionData()
                        animation_property.input_function_data.points = []
                        animation_property.range_function_data.points = []

                        animation_property.input_function_data.exponent = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "exponent", TransitionExponentEnum))
                        animation_property.range_function_data.exponent = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "function", TransitionExponentEnum))
                        animation_property.lower_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "lower bound"))
                        animation_property.upper_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "upper bound"))
                        input_stream.read(8) # Padding?

                        animation_property.input_function_data.frequency = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "frequency"))
                        animation_property.input_function_data.phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "phase"))
                        animation_property.input_function_data.min = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "min"))
                        animation_property.input_function_data.max = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "max"))

                        animation_property.range_function_data.frequency = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "frequency"))
                        animation_property.range_function_data.phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "phase"))
                        animation_property.range_function_data.min = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "min"))
                        animation_property.range_function_data.max = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "max"))

                    elif FunctionTypeEnum.linear == FunctionTypeEnum(animation_property.function_type):
                        animation_property.input_function_data = SHADER.FunctionData()
                        animation_property.range_function_data = SHADER.FunctionData()
                        animation_property.input_function_data.points = []
                        animation_property.range_function_data.points = []
                        
                        input_stream.read(2) # Padding?
                        animation_property.lower_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "lower bound"))
                        animation_property.upper_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "upper bound"))
                        input_stream.read(8) # Padding?
                        for point_idx in range(2):
                            animation_property.input_function_data.points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "position")))

                        input_stream.read(8) # Padding?
                        for point_idx in range(2):
                            animation_property.range_function_data.points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "position")))

                        input_stream.read(8) # Padding?

                    elif FunctionTypeEnum.linear_key == FunctionTypeEnum(animation_property.function_type):
                        animation_property.input_function_data = SHADER.FunctionData()
                        animation_property.range_function_data = SHADER.FunctionData()
                        animation_property.input_function_data.points = []
                        animation_property.range_function_data.points = []
                        
                        input_stream.read(2) # Padding?
                        animation_property.lower_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "lower bound"))
                        animation_property.upper_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "upper bound"))
                        input_stream.read(8) # Padding?
                        for point_idx in range(4):
                            animation_property.input_function_data.points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "position")))

                        input_stream.read(48) # Padding?
                        for point_idx in range(4):
                            animation_property.range_function_data.points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "position")))

                        input_stream.read(48) # Padding?

                    elif FunctionTypeEnum.multi_linear_key == FunctionTypeEnum(animation_property.function_type):
                        input_stream.read(2) # Padding?
                        animation_property.lower_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "lower bound"))
                        animation_property.upper_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "upper bound"))
                        input_stream.read(264) # Padding?

                    elif FunctionTypeEnum.spline == FunctionTypeEnum(animation_property.function_type):
                        animation_property.input_function_data = SHADER.FunctionData()
                        animation_property.range_function_data = SHADER.FunctionData()
                        animation_property.input_function_data.points = []
                        animation_property.range_function_data.points = []
                        
                        input_stream.read(2) # Padding?
                        animation_property.lower_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "lower bound"))
                        animation_property.upper_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "upper bound"))
                        input_stream.read(8) # Padding?
                        for point_idx in range(4):
                            animation_property.input_function_data.points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "position")))

                        input_stream.read(16) # Padding?
                        for point_idx in range(4):
                            animation_property.range_function_data.points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "position")))

                        input_stream.read(16) # Padding?

                    elif FunctionTypeEnum.multi_spline == FunctionTypeEnum(animation_property.function_type):
                        input_stream.read(2) # Padding?
                        animation_property.lower_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "lower bound"))
                        animation_property.upper_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "upper bound"))
                        input_stream.read(40) # Padding?

                    elif FunctionTypeEnum.exponent == FunctionTypeEnum(animation_property.function_type):
                        animation_property.input_function_data = SHADER.FunctionData()
                        animation_property.range_function_data = SHADER.FunctionData()
                        animation_property.input_function_data.points = []
                        animation_property.range_function_data.points = []

                        input_stream.read(2) # Padding?
                        animation_property.lower_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "lower bound"))
                        animation_property.upper_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "upper bound"))
                        input_stream.read(8) # Padding?

                        animation_property.input_function_data.min = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "min"))
                        animation_property.input_function_data.max = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "max"))
                        animation_property.input_function_data.exponent = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "exponent"))

                        animation_property.range_function_data.min = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "min"))
                        animation_property.range_function_data.max = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "max"))
                        animation_property.range_function_data.exponent = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "exponent"))

                    elif FunctionTypeEnum.spline2 == FunctionTypeEnum(animation_property.function_type):
                        animation_property.input_function_data = SHADER.FunctionData()
                        animation_property.range_function_data = SHADER.FunctionData()
                        animation_property.input_function_data.points = []
                        animation_property.range_function_data.points = []
                        
                        input_stream.read(2) # Padding?
                        animation_property.lower_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "lower bound"))
                        animation_property.upper_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "upper bound"))
                        input_stream.read(8) # Padding?
                        for point_idx in range(4):
                            animation_property.input_function_data.points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "position")))

                        input_stream.read(16) # Padding?
                        for point_idx in range(4):
                            animation_property.range_function_data.points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(animation_property_element_node, "position")))

                        input_stream.read(16) # Padding?

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    SHADER = ShaderAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    SHADER.header = TAG.Header().read(input_stream, TAG)
    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    initilize_shader(SHADER)
    if SHADER.header.engine_tag == "LAMB":
        read_shader_body_v0(SHADER, TAG, input_stream, tag_node, XML_OUTPUT)

        if SHADER.shader_body.template.name_length > 0:
            SHADER.shader_body.template.name = TAG.read_variable_string(input_stream, SHADER.shader_body.template.name_length, TAG)

        if SHADER.shader_body.material_name_length > 0:
            SHADER.shader_body.material_name = TAG.read_variable_string_no_terminator(input_stream, SHADER.shader_body.material_name_length, TAG, tag_format.XMLData(tag_node, "material name"))

        if XML_OUTPUT:
            template_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "template")
            SHADER.shader_body.template.append_xml_attributes(template_node)

        read_runtime_properties(SHADER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_parameters(SHADER, TAG, input_stream, tag_node, XML_OUTPUT)

    elif SHADER.header.engine_tag == "MLAB":
        read_shader_body_v0(SHADER, TAG, input_stream, tag_node, XML_OUTPUT)

        if SHADER.shader_body.template.name_length > 0:
            SHADER.shader_body.template.name = TAG.read_variable_string(input_stream, SHADER.shader_body.template.name_length, TAG)

        if SHADER.shader_body.material_name_length > 0:
            SHADER.shader_body.material_name = TAG.read_variable_string_no_terminator(input_stream, SHADER.shader_body.material_name_length, TAG, tag_format.XMLData(tag_node, "material name"))

        if XML_OUTPUT:
            template_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "template")
            SHADER.shader_body.template.append_xml_attributes(template_node)

        read_runtime_properties(SHADER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_parameters(SHADER, TAG, input_stream, tag_node, XML_OUTPUT)

    elif SHADER.header.engine_tag == "BLM!":
        read_shader_body_retail(SHADER, TAG, input_stream, tag_node, XML_OUTPUT)

        if SHADER.shader_body.template.name_length > 0:
            SHADER.shader_body.template.name = TAG.read_variable_string(input_stream, SHADER.shader_body.template.name_length, TAG)

        if SHADER.shader_body.material_name_length > 0:
            SHADER.shader_body.material_name = TAG.read_variable_string_no_terminator(input_stream, SHADER.shader_body.material_name_length, TAG, tag_format.XMLData(tag_node, "material name"))

        if XML_OUTPUT:
            template_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "template")
            SHADER.shader_body.template.append_xml_attributes(template_node)

        read_runtime_properties(SHADER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_parameters(SHADER, TAG, input_stream, tag_node, XML_OUTPUT)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, SHADER.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return SHADER
