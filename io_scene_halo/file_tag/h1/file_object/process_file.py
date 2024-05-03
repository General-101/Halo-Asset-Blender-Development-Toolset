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
from .format import ScaleEnum, ColorEnum, FunctionFlags, FunctionScaleEnum, FunctionEnum, MapEnum, BoundsModeEnum, ColorChangeFlags, ResourceTypeEnum

XML_OUTPUT = False

def read_attachments(OBJECT, TAG, input_stream, tag_node, XML_OUTPUT):
    attachment_node = tag_format.get_xml_node(XML_OUTPUT, OBJECT.attachments_tag_block.count, tag_node, "name", "attachments")
    for attachment_idx in range(OBJECT.attachments_tag_block.count):
        attachment_element_node = None
        if XML_OUTPUT:
            attachment_element_node = TAG.xml_doc.createElement('element')
            attachment_element_node.setAttribute('index', str(attachment_idx))
            attachment_node.appendChild(attachment_element_node)

        attachment = OBJECT.Attachment()
        attachment.attachment_type = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(attachment_element_node, "type"))
        attachment.marker = TAG.read_string32(input_stream, TAG, tag_format.XMLData(attachment_element_node, "marker"))
        attachment.primary_scale = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(attachment_element_node, "primary scale", ScaleEnum))
        attachment.secondary_scale = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(attachment_element_node, "secondary scale", ScaleEnum))
        attachment.change_color = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(attachment_element_node, "change color", ColorEnum))
        input_stream.read(18) # Padding?

        OBJECT.attachments.append(attachment)

    for attachment_idx, attachment in enumerate(OBJECT.attachments):
        attachment_element_node = None
        if XML_OUTPUT:
            attachment_element_node = attachment_node.childNodes[attachment_idx]

        if attachment.attachment_type.name_length > 0:
            attachment.attachment_type.name = TAG.read_variable_string(input_stream, attachment.attachment_type.name_length, TAG)

        if XML_OUTPUT:
            type_node = tag_format.get_xml_node(XML_OUTPUT, 1, attachment_element_node, "name", "type")
            attachment.attachment_type.append_xml_attributes(type_node)

def read_widgets(OBJECT, TAG, input_stream, tag_node, XML_OUTPUT):
    widgets_node = tag_format.get_xml_node(XML_OUTPUT, OBJECT.widgets_tag_block.count, tag_node, "name", "widgets")
    for widget_idx in range(OBJECT.widgets_tag_block.count):
        widget_element_node = None
        if XML_OUTPUT:
            widget_element_node = TAG.xml_doc.createElement('element')
            widget_element_node.setAttribute('index', str(widget_idx))
            widgets_node.appendChild(widget_element_node)

        reference = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(widget_element_node, "reference"))
        input_stream.read(16) # Padding?

        OBJECT.widgets.append(reference)

    for widget_idx, widget in enumerate(OBJECT.widgets):
        widget_element_node = None
        if XML_OUTPUT:
            widget_element_node = widgets_node.childNodes[widget_idx]

        if widget.name_length > 0:
            widget.name = TAG.read_variable_string(input_stream, widget.name_length, TAG)

        if XML_OUTPUT:
            type_node = tag_format.get_xml_node(XML_OUTPUT, 1, widget_element_node, "name", "reference")
            widget.append_xml_attributes(type_node)

def read_functions(OBJECT, TAG, input_stream, tag_node, XML_OUTPUT):
    functions_node = tag_format.get_xml_node(XML_OUTPUT, OBJECT.functions_tag_block.count, tag_node, "name", "functions")
    for function_idx in range(OBJECT.functions_tag_block.count):
        function_element_node = None
        if XML_OUTPUT:
            function_element_node = TAG.xml_doc.createElement('element')
            function_element_node.setAttribute('index', str(function_idx))
            functions_node.appendChild(function_element_node)

        function_class = OBJECT.Function()
        function_class.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(function_element_node, "flags", FunctionFlags))
        function_class.period = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "period"))
        function_class.scale_period_by = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(function_element_node, "scale period by", FunctionScaleEnum))
        function_class.function_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(function_element_node, "function", FunctionEnum))
        function_class.scale_function_by = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(function_element_node, "scale function by", FunctionScaleEnum))
        function_class.wobble_function_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(function_element_node, "wobble function type", FunctionEnum))
        function_class.wobble_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "wobble period"))
        function_class.wobble_magnitude = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "wobble magnitude"))
        function_class.square_wave_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "square wave threshold"))
        function_class.step_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(function_element_node, "step count"))
        function_class.map_to = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(function_element_node, "map to", MapEnum))
        function_class.sawtooth_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(function_element_node, "sawtooth count"))
        function_class.add_by = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(function_element_node, "add by", FunctionScaleEnum))
        function_class.scale_result_by = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(function_element_node, "scale result by", FunctionScaleEnum))
        function_class.bounds_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(function_element_node, "bounds mode", BoundsModeEnum))
        function_class.bounds = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(function_element_node, "bounds"))
        input_stream.read(6) # Padding?
        function_class.turn_off_with = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(function_element_node, "turn off with", None, OBJECT.functions_tag_block.count, "function_block"))
        function_class.scale_by = TAG.read_float(input_stream, TAG, tag_format.XMLData(function_element_node, "scale"))
        input_stream.read(268) # Padding?
        function_class.usage = TAG.read_string32(input_stream, TAG, tag_format.XMLData(function_element_node, "usage"))

        OBJECT.functions.append(function_class)

def read_change_colors(OBJECT, TAG, input_stream, tag_node, XML_OUTPUT):
    change_colors_node = tag_format.get_xml_node(XML_OUTPUT, OBJECT.change_colors_tag_block.count, tag_node, "name", "change colors")
    for change_color_idx in range(OBJECT.change_colors_tag_block.count):
        change_color_element_node = None
        if XML_OUTPUT:
            change_color_element_node = TAG.xml_doc.createElement('element')
            change_color_element_node.setAttribute('index', str(change_color_idx))
            change_colors_node.appendChild(change_color_element_node)

        change_color = OBJECT.ChangeColor()
        change_color.darken_by = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(change_color_element_node, "darken by", FunctionScaleEnum))
        change_color.scale_by = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(change_color_element_node, "scale by", FunctionScaleEnum))
        change_color.scale_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(change_color_element_node, "scale flags", ColorChangeFlags))
        change_color.color_lower_bound = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(change_color_element_node, "color lower bound"))
        change_color.color_upper_bound = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(change_color_element_node, "color upper bound"))
        change_color.permutations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(change_color_element_node, "permutations"))

        OBJECT.change_colors.append(change_color)

    for change_color_idx, change_color in enumerate(OBJECT.change_colors):
        change_color_element_node = None
        if XML_OUTPUT:
            change_color_element_node = change_colors_node.childNodes[change_color_idx]

        change_color.permutations = []
        permutations_node = tag_format.get_xml_node(XML_OUTPUT, change_color.permutations_tag_block.count, change_color_element_node, "name", "permutations")
        for permutation_idx in range(change_color.permutations_tag_block.count):
            permutation_element_node = None
            if XML_OUTPUT:
                permutation_element_node = TAG.xml_doc.createElement('element')
                permutation_element_node.setAttribute('index', str(permutation_idx))
                permutations_node.appendChild(permutation_element_node)

            permutation = OBJECT.Permutation()
            permutation.weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(permutation_element_node, "weight"))
            permutation.color_lower_bound = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(permutation_element_node, "color lower bound"))
            permutation.color_upper_bound = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(permutation_element_node, "color upper bound"))

            change_color.permutations.append(permutation)

def read_predicted_resources(OBJECT, TAG, input_stream, tag_node, XML_OUTPUT):
    predicted_resources_node = tag_format.get_xml_node(XML_OUTPUT, OBJECT.predicted_resources_tag_block.count, tag_node, "name", "predicted resources")
    for predicted_resource_idx in range(OBJECT.predicted_resources_tag_block.count):
        predicted_resource_element_node = None
        if XML_OUTPUT:
            predicted_resource_element_node = TAG.xml_doc.createElement('element')
            predicted_resource_element_node.setAttribute('index', str(predicted_resource_idx))
            predicted_resources_node.appendChild(predicted_resource_element_node)

        predicted_resource = OBJECT.PredictedResource()
        predicted_resource.predicted_resources_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(predicted_resource_element_node, "type", ResourceTypeEnum))
        predicted_resource.resource_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(predicted_resource_element_node, "resource index"))
        predicted_resource.tag_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(predicted_resource_element_node, "tag index"))

        OBJECT.predicted_resources.append(predicted_resource)
