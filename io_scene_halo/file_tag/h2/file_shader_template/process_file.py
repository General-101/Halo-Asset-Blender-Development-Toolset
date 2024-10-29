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
    ShaderTemplateAsset,
    ShaderTemplateFlags,
    AuxLayerEnum,
    PropertyEnum,
    TypeEnum,
    ParameterFlags,
    BitmapEnum,
    BitmapAnimationFlags
    )

XML_OUTPUT = False

def initilize_shader_template(SHADERTEMPLATE):
    SHADERTEMPLATE.properties = []
    SHADERTEMPLATE.categories = []
    SHADERTEMPLATE.lods = []
    SHADERTEMPLATE.external_light_response = []
    SHADERTEMPLATE.external_light_response_byte_swap = []
    SHADERTEMPLATE.postprocess_definition = []

def read_shader_template_body_retail(SHADERTEMPLATE, TAG, input_stream, tag_node, XML_OUTPUT):
    SHADERTEMPLATE.body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    SHADERTEMPLATE.documentation_tag_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(tag_node, "documentation"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    SHADERTEMPLATE.default_material_name_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    input_stream.read(2) # Padding?
    SHADERTEMPLATE.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ShaderTemplateFlags))
    SHADERTEMPLATE.properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "properties"))
    SHADERTEMPLATE.categories_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "categories"))
    SHADERTEMPLATE.light_response = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "light response"))
    SHADERTEMPLATE.lods_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "lods"))
    SHADERTEMPLATE.external_light_response_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "external light response"))
    SHADERTEMPLATE.external_light_response_byte_swap_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "external light response byte swap"))
    SHADERTEMPLATE.aux_1_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "aux 1 shader"))
    SHADERTEMPLATE.aux_1_layer = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "aux 1 layer", AuxLayerEnum))
    input_stream.read(2) # Padding?
    SHADERTEMPLATE.aux_2_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "aux 2 shader"))
    SHADERTEMPLATE.aux_2_layer = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "aux 2 layer", AuxLayerEnum))
    input_stream.read(2) # Padding?
    SHADERTEMPLATE.postprocess_definition_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "postprocess definition"))

def read_properties(SHADERTEMPLATE, TAG, input_stream, tag_node, XML_OUTPUT):
    if SHADERTEMPLATE.properties_tag_block.count > 0:
        properties_node = tag_format.get_xml_node(XML_OUTPUT, SHADERTEMPLATE.properties_tag_block.count, tag_node, "name", "properties")
        SHADERTEMPLATE.properties_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for property_idx in range(SHADERTEMPLATE.properties_tag_block.count):
            property_element_node = None
            if XML_OUTPUT:
                property_element_node = TAG.xml_doc.createElement('element')
                property_element_node.setAttribute('index', str(property_idx))
                properties_node.appendChild(property_element_node)

            shader_property = SHADERTEMPLATE.Property()
            shader_property.property_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(property_element_node, "type", PropertyEnum))
            input_stream.read(2) # Padding?

            TAG.big_endian = True
            input_stream.read(2) # Padding?
            shader_property.name_length = TAG.read_signed_short(input_stream, TAG)
            TAG.big_endian = False

            SHADERTEMPLATE.properties.append(shader_property)

        for property_idx, shader_property in enumerate(SHADERTEMPLATE.properties):
            property_element_node = None
            if XML_OUTPUT:
                property_element_node = properties_node.childNodes[property_idx]

            if shader_property.name_length > 0:
                shader_property.name = TAG.read_variable_string_no_terminator(input_stream, shader_property.name_length, TAG, tag_format.XMLData(property_element_node, "name"))

def read_categories(SHADERTEMPLATE, TAG, input_stream, tag_node, XML_OUTPUT):
    if SHADERTEMPLATE.categories_tag_block.count > 0:
        categories_node = tag_format.get_xml_node(XML_OUTPUT, SHADERTEMPLATE.categories_tag_block.count, tag_node, "name", "categories")
        SHADERTEMPLATE.categories_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for category_idx in range(SHADERTEMPLATE.categories_tag_block.count):
            category_element_node = None
            if XML_OUTPUT:
                category_element_node = TAG.xml_doc.createElement('element')
                category_element_node.setAttribute('index', str(category_idx))
                categories_node.appendChild(category_element_node)

            category = SHADERTEMPLATE.Category()

            TAG.big_endian = True
            input_stream.read(2) # Padding?
            category.name_length = TAG.read_signed_short(input_stream, TAG)
            TAG.big_endian = False

            category.parameters_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(category_element_node, "parameters"))

            SHADERTEMPLATE.categories.append(category)

        for category_idx, category in enumerate(SHADERTEMPLATE.categories):
            category_element_node = None
            if XML_OUTPUT:
                category_element_node = categories_node.childNodes[category_idx]

            if category.name_length > 0:
                category.name = TAG.read_variable_string_no_terminator(input_stream, category.name_length, TAG, tag_format.XMLData(category_element_node, "name"))

            category.parameters = []
            if category.parameters_tag_block.count > 0:
                parameters_node = tag_format.get_xml_node(XML_OUTPUT, category.parameters_tag_block.count, category_element_node, "name", "parameters")
                category.parameters_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for parameter_idx in range(category.parameters_tag_block.count):
                    parameter_element_node = None
                    if XML_OUTPUT:
                        parameter_element_node = TAG.xml_doc.createElement('element')
                        parameter_element_node.setAttribute('index', str(parameter_idx))
                        parameters_node.appendChild(parameter_element_node)

                    parameter = SHADERTEMPLATE.Parameter()

                    TAG.big_endian = True
                    input_stream.read(2) # Padding?
                    parameter.name_length = TAG.read_signed_short(input_stream, TAG)
                    TAG.big_endian = False

                    parameter.explanation_tag_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(parameter_element_node, "explanation"))
                    parameter.parameter_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(parameter_element_node, "type", TypeEnum))
                    parameter.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(parameter_element_node, "flags", ParameterFlags))
                    parameter.default_bitmap = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(parameter_element_node, "default bitmap"))
                    parameter.default_const_value = TAG.read_float(input_stream, TAG, tag_format.XMLData(parameter_element_node, "default const value"))
                    parameter.default_const_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(parameter_element_node, "default const color"))
                    parameter.bitmap_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(parameter_element_node, "bitmap type", BitmapEnum))
                    input_stream.read(2) # Padding?
                    parameter.bitmap_animation_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(parameter_element_node, "bitmap animation flags", BitmapAnimationFlags))
                    input_stream.read(2) # Padding?
                    parameter.bitmap_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(parameter_element_node, "bitmap scale"))

                    category.parameters.append(parameter)

                for parameter_idx, parameter in enumerate(category.parameters):
                    parameter_element_node = None
                    if XML_OUTPUT:
                        parameter_element_node = parameters_node.childNodes[parameter_idx]

                    if parameter.name_length > 0:
                        parameter.name = TAG.read_variable_string_no_terminator(input_stream, parameter.name_length, TAG, tag_format.XMLData(parameter_element_node, "name"))

                    parameter.explanation_tag_data.data = input_stream.read(parameter.explanation_tag_data.size)

                    if parameter.default_bitmap.name_length > 0:
                        parameter.default_bitmap.name = TAG.read_variable_string(input_stream, parameter.default_bitmap.name_length, TAG)

                    if XML_OUTPUT:
                        default_bitmap_node = tag_format.get_xml_node(XML_OUTPUT, 1, parameter_element_node, "name", "default bitmap")
                        parameter.default_bitmap.append_xml_attributes(default_bitmap_node)

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    SHADERTEMPLATE = ShaderTemplateAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    SHADERTEMPLATE.header = TAG.Header().read(input_stream, TAG)
    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    initilize_shader_template(SHADERTEMPLATE)
    if SHADERTEMPLATE.header.engine_tag == "LAMB":
        read_shader_template_body_retail(SHADERTEMPLATE, TAG, input_stream, tag_node, XML_OUTPUT)
        SHADERTEMPLATE.documentation_tag_data.data = input_stream.read(SHADERTEMPLATE.documentation_tag_data.size)
        if SHADERTEMPLATE.default_material_name_length > 0:
            SHADERTEMPLATE.default_material_name = TAG.read_variable_string_no_terminator(input_stream, SHADERTEMPLATE.default_material_name_length, TAG, tag_format.XMLData(tag_node, "default material name"))

        read_properties(SHADERTEMPLATE, TAG, input_stream, tag_node, XML_OUTPUT)
        read_categories(SHADERTEMPLATE, TAG, input_stream, tag_node, XML_OUTPUT)
    elif SHADERTEMPLATE.header.engine_tag == "MLAB":
        read_shader_template_body_retail(SHADERTEMPLATE, TAG, input_stream, tag_node, XML_OUTPUT)
        SHADERTEMPLATE.documentation_tag_data.data = input_stream.read(SHADERTEMPLATE.documentation_tag_data.size)
        if SHADERTEMPLATE.default_material_name_length > 0:
            SHADERTEMPLATE.default_material_name = TAG.read_variable_string_no_terminator(input_stream, SHADERTEMPLATE.default_material_name_length, TAG, tag_format.XMLData(tag_node, "default material name"))

        read_properties(SHADERTEMPLATE, TAG, input_stream, tag_node, XML_OUTPUT)
        read_categories(SHADERTEMPLATE, TAG, input_stream, tag_node, XML_OUTPUT)
    elif SHADERTEMPLATE.header.engine_tag == "BLM!":
        read_shader_template_body_retail(SHADERTEMPLATE, TAG, input_stream, tag_node, XML_OUTPUT)
        SHADERTEMPLATE.documentation_tag_data.data = input_stream.read(SHADERTEMPLATE.documentation_tag_data.size)
        if SHADERTEMPLATE.default_material_name_length > 0:
            SHADERTEMPLATE.default_material_name = TAG.read_variable_string_no_terminator(input_stream, SHADERTEMPLATE.default_material_name_length, TAG, tag_format.XMLData(tag_node, "default material name"))

        read_properties(SHADERTEMPLATE, TAG, input_stream, tag_node, XML_OUTPUT)
        read_categories(SHADERTEMPLATE, TAG, input_stream, tag_node, XML_OUTPUT)


    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, SHADERTEMPLATE.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return SHADERTEMPLATE
