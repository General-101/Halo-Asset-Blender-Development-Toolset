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
        AIFlags,
        AISizeEnum,
        LeapJumpSpeedEnum,
        FunctionFlags,
        FunctionTypeEnum,
        OutputTypeFlags,
        TransitionExponentEnum,
        ChangeColorEnum,
        ScaleFlags,
        ResourceTypeEnum
        )

XML_OUTPUT = False

def read_ai_properties_retail(OBJECT, TAG, input_stream, tag_node, XML_OUTPUT):
    if OBJECT.ai_properties_tag_block.count > 0:
        OBJECT.ai_properties_header = TAG.TagBlockHeader().read(input_stream, TAG)
        ai_properties_node = tag_format.get_xml_node(XML_OUTPUT, OBJECT.ai_properties_tag_block.count, tag_node, "name", "ai properties")
        for ai_property_idx in range(OBJECT.ai_properties_tag_block.count):
            ai_property_element_node = None
            if XML_OUTPUT:
                ai_property_element_node = TAG.xml_doc.createElement('element')
                ai_property_element_node.setAttribute('index', str(ai_property_idx))
                ai_properties_node.appendChild(ai_property_element_node)

            ai_property = OBJECT.AIProperty()
            ai_property.ai_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(tag_node, "ai flags", AIFlags))

            TAG.big_endian = True
            input_stream.read(2) # Padding?
            ai_property.ai_type_name_length = TAG.read_signed_short(input_stream, TAG)
            TAG.big_endian = False

            input_stream.read(4) # Padding?
            ai_property.ai_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "ai size", AISizeEnum))
            ai_property.leap_jump_speed = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "leap jump speed", LeapJumpSpeedEnum))

            OBJECT.ai_properties.append(ai_property)

        for ai_property_idx, ai_property in enumerate(OBJECT.ai_properties):
            ai_property_element_node = None
            if XML_OUTPUT:
                ai_property_element_node = ai_properties_node.childNodes[ai_property_idx]

            if ai_property.ai_type_name_length > 0:
                ai_property.ai_type_name = TAG.read_variable_string_no_terminator(input_stream, ai_property.ai_type_name_length, TAG, tag_format.XMLData(tag_node, "ai type name"))

def read_functions_retail(OBJECT, TAG, input_stream, tag_node, XML_OUTPUT):
    if OBJECT.functions_tag_block.count > 0:
        OBJECT.functions_header = TAG.TagBlockHeader().read(input_stream, TAG)
        functions_node = tag_format.get_xml_node(XML_OUTPUT, OBJECT.functions_tag_block.count, tag_node, "name", "functions")
        for function_idx in range(OBJECT.functions_tag_block.count):
            function_element_node = None
            if XML_OUTPUT:
                function_element_node = TAG.xml_doc.createElement('element')
                function_element_node.setAttribute('index', str(function_idx))
                functions_node.appendChild(function_element_node)

            function = OBJECT.Function()
            function.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(tag_node, "flags", FunctionFlags))

            TAG.big_endian = True
            input_stream.read(2) # Padding?
            function.import_name_length = TAG.read_signed_short(input_stream, TAG)
            input_stream.read(2) # Padding?
            function.export_name_length = TAG.read_signed_short(input_stream, TAG)
            input_stream.read(2) # Padding?
            function.turn_off_with_length = TAG.read_signed_short(input_stream, TAG)
            TAG.big_endian = False

            function.min_value = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min value"))
            input_stream.read(12) # Padding?

            TAG.big_endian = True
            input_stream.read(2) # Padding?
            function.scale_by_length = TAG.read_signed_short(input_stream, TAG)
            TAG.big_endian = False

            OBJECT.functions.append(function)

        for function_idx, function in enumerate(OBJECT.functions):
            function_element_node = None
            if XML_OUTPUT:
                function_element_node = functions_node.childNodes[function_idx]

            if function.import_name_length > 0:
                function.import_name = TAG.read_variable_string_no_terminator(input_stream, function.import_name_length, TAG, tag_format.XMLData(tag_node, "import name"))

            if function.export_name_length > 0:
                function.export_name = TAG.read_variable_string_no_terminator(input_stream, function.export_name_length, TAG, tag_format.XMLData(tag_node, "export name"))

            if function.turn_off_with_length > 0:
                function.turn_off_with = TAG.read_variable_string_no_terminator(input_stream, function.turn_off_with_length, TAG, tag_format.XMLData(tag_node, "turn off with"))

            function.MAPP_header = TAG.TagBlockHeader().read(input_stream, TAG)
            function.function_header = TAG.TagBlockHeader().read(input_stream, TAG)

            function.function_type = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(function_element_node, "function type", FunctionTypeEnum))
            function.output_type = TAG.read_flag_unsigned_byte(input_stream, TAG, tag_format.XMLData(function_element_node, "output type", OutputTypeFlags))
            output_type_flags = OutputTypeFlags(function.output_type)
            function.points = []
            function.range_points = []
            function.exponent = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(function_element_node, "exponent", TransitionExponentEnum))
            function.range_exponent = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(function_element_node, "exponent", TransitionExponentEnum))
            if OutputTypeFlags._2_color in output_type_flags:
                function.color_a = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(function_element_node, "color a"))
                input_stream.read(8) # Padding?
                function.color_b = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(function_element_node, "color b"))
            elif OutputTypeFlags._3_color in output_type_flags:
                function.color_a = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(function_element_node, "color a"))
                function.color_b = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(function_element_node, "color b"))
                input_stream.read(4) # Padding?
                function.color_c = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(function_element_node, "color c"))
            elif OutputTypeFlags._4_color in output_type_flags:
                function.color_a = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(function_element_node, "color a"))
                function.color_b = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(function_element_node, "color b"))
                function.color_c = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(function_element_node, "color c"))
                function.color_d = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(function_element_node, "color d"))
            else:
                function.lower_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "lower bound"))
                function.upper_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "upper bound"))
                input_stream.read(8) # Padding?

            if FunctionTypeEnum.constant == FunctionTypeEnum(function.function_type):
                input_stream.read(8) # Padding?
            elif FunctionTypeEnum.transition == FunctionTypeEnum(function.function_type):
                function.function_min = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "min"))
                function.function_max = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "max"))
                function.range_function_min = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "min"))
                function.range_function_max = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "max"))
            elif FunctionTypeEnum.periodic == FunctionTypeEnum(function.function_type):
                function.frequency = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "frequency"))
                function.phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "phase"))
                function.function_min = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "min"))
                function.function_max = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "max"))
                function.range_frequency = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "frequency"))
                function.range_phase = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "phase"))
                function.range_function_min = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "min"))
                function.range_function_max = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "max"))
            elif FunctionTypeEnum.linear == FunctionTypeEnum(function.function_type):
                for point_idx in range(2):
                    function.points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(function_element_node, "position")))

                input_stream.read(8) # Padding?
                for point_idx in range(2):
                    function.range_points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(function_element_node, "position")))

                input_stream.read(8) # Padding?

            elif FunctionTypeEnum.linear_key == FunctionTypeEnum(function.function_type):
                for point_idx in range(4):
                    function.input_function_data.points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(function_element_node, "position")))

                input_stream.read(48) # Padding?
                for point_idx in range(4):
                    function.range_function_data.points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(function_element_node, "position")))

                input_stream.read(48) # Padding?

            elif FunctionTypeEnum.multi_linear_key == FunctionTypeEnum(function.function_type):
                input_stream.read(256) # Padding?

            elif FunctionTypeEnum.spline == FunctionTypeEnum(function.function_type):
                for point_idx in range(4):
                    function.input_function_data.points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(function_element_node, "position")))

                input_stream.read(16) # Padding?
                for point_idx in range(4):
                    function.range_function_data.points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(function_element_node, "position")))

                input_stream.read(16) # Padding?

            elif FunctionTypeEnum.multi_spline == FunctionTypeEnum(function.function_type):
                input_stream.read(40) # Padding?

            elif FunctionTypeEnum.exponent == FunctionTypeEnum(function.function_type):
                function.input_function_data.min = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "min"))
                function.input_function_data.max = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "max"))
                function.input_function_data.exponent = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "exponent"))

                function.range_function_data.min = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "min"))
                function.range_function_data.max = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "max"))
                function.range_function_data.exponent = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "exponent"))

            elif FunctionTypeEnum.spline2 == FunctionTypeEnum(function.function_type):
                for point_idx in range(4):
                    function.input_function_data.points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(function_element_node, "position")))

                input_stream.read(16) # Padding?
                for point_idx in range(4):
                    function.range_function_data.points.append(TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(function_element_node, "position")))

                input_stream.read(16) # Padding?

            if function.scale_by_length > 0:
                function.scale_by = TAG.read_variable_string_no_terminator(input_stream, function.scale_by_length, TAG, tag_format.XMLData(tag_node, "scale by"))

def read_attachments_retail(OBJECT, TAG, input_stream, tag_node, XML_OUTPUT):
    if OBJECT.attachments_tag_block.count > 0:
        OBJECT.ai_properties_header = TAG.TagBlockHeader().read(input_stream, TAG)
        attachments_node = tag_format.get_xml_node(XML_OUTPUT, OBJECT.attachments_tag_block.count, tag_node, "name", "attachments")
        for attachment_idx in range(OBJECT.attachments_tag_block.count):
            attachment_element_node = None
            if XML_OUTPUT:
                attachment_element_node = TAG.xml_doc.createElement('element')
                attachment_element_node.setAttribute('index', str(attachment_idx))
                attachments_node.appendChild(attachment_element_node)

            attachment = OBJECT.Attachment()
            attachment.attachment_type = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(attachment_element_node, "type"))

            TAG.big_endian = True
            input_stream.read(2) # Padding?
            attachment.marker_length = TAG.read_signed_short(input_stream, TAG)
            TAG.big_endian = False

            attachment.change_color = TAG.read_enum_unsigned_integer(input_stream, TAG, tag_format.XMLData(attachment_element_node, "change color", ChangeColorEnum))

            TAG.big_endian = True
            input_stream.read(2) # Padding?
            attachment.primary_scale_length = TAG.read_signed_short(input_stream, TAG)
            input_stream.read(2) # Padding?
            attachment.secondary_scale_length = TAG.read_signed_short(input_stream, TAG)
            TAG.big_endian = False

            OBJECT.attachments.append(attachment)

        for attachment_idx, attachment in enumerate(OBJECT.attachments):
            attachment_element_node = None
            if XML_OUTPUT:
                attachment_element_node = attachments_node.childNodes[attachment_idx]

            if attachment.attachment_type.name_length > 0:
                attachment.attachment_type.name = TAG.read_variable_string(input_stream, attachment.attachment_type.name_length, TAG)
            if attachment.marker_length > 0:
                attachment.marker = TAG.read_variable_string_no_terminator(input_stream, attachment.marker_length, TAG, tag_format.XMLData(attachment_element_node, "marker"))
            if attachment.primary_scale_length > 0:
                attachment.primary_scale = TAG.read_variable_string_no_terminator(input_stream, attachment.primary_scale_length, TAG, tag_format.XMLData(attachment_element_node, "primary scale"))
            if attachment.secondary_scale_length > 0:
                attachment.secondary_scale = TAG.read_variable_string_no_terminator(input_stream, attachment.secondary_scale_length, TAG, tag_format.XMLData(attachment_element_node, "secondary scale"))

def read_widgets_retail(OBJECT, TAG, input_stream, tag_node, XML_OUTPUT):
    if OBJECT.widgets_tag_block.count > 0:
        OBJECT.widgets_header = TAG.TagBlockHeader().read(input_stream, TAG)
        widgets_node = tag_format.get_xml_node(XML_OUTPUT, OBJECT.widgets_tag_block.count, tag_node, "name", "wdigets")
        for widget_idx in range(OBJECT.widgets_tag_block.count):
            widget_element_node = None
            if XML_OUTPUT:
                widget_element_node = TAG.xml_doc.createElement('element')
                widget_element_node.setAttribute('index', str(widget_idx))
                widgets_node.appendChild(widget_element_node)

            widget_ref = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(widget_element_node, "type"))

            OBJECT.widgets.append(widget_ref)

        for widget_idx, widget in enumerate(OBJECT.widgets):
            widget_element_node = None
            if XML_OUTPUT:
                widget_element_node = widgets_node.childNodes[widget_idx]

            if widget.name_length > 0:
                widget.name = TAG.read_variable_string(input_stream, widget.name_length, TAG)

def read_old_functions_retail(OBJECT, TAG, input_stream, tag_node, XML_OUTPUT):
    if OBJECT.old_functions_tag_block.count > 0:
        OBJECT.old_functions_header = TAG.TagBlockHeader().read(input_stream, TAG)
        old_functions_node = tag_format.get_xml_node(XML_OUTPUT, OBJECT.old_functions_tag_block.count, tag_node, "name", "wdigets")
        for old_function_idx in range(OBJECT.old_functions_tag_block.count):
            old_function_element_node = None
            if XML_OUTPUT:
                old_function_element_node = TAG.xml_doc.createElement('element')
                old_function_element_node.setAttribute('index', str(old_function_idx))
                old_functions_node.appendChild(old_function_element_node)

            string_entry = OBJECT.StringEntry()
            input_stream.read(76) # Padding?
            TAG.big_endian = True
            input_stream.read(2) # Padding?
            string_entry.name_length = TAG.read_signed_short(input_stream, TAG)
            TAG.big_endian = False

            OBJECT.old_functions.append(string_entry)

        for old_function_idx, old_function in enumerate(OBJECT.old_functions):
            old_function_element_node = None
            if XML_OUTPUT:
                old_function_element_node = old_functions_node.childNodes[old_function_idx]

            if old_function.name_length > 0:
                old_function.name = TAG.read_variable_string_no_terminator(input_stream, old_function.name_length, TAG, tag_format.XMLData(old_function_element_node, "name"))
