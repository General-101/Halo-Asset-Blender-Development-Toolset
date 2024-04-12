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

from ....global_functions import shader_processing

def write_ai_properties(output_stream, TAG, ai_properties, ai_properties_header):
    if len(ai_properties) > 0:
        ai_properties_header.write(output_stream, TAG, True)
        for ai_property_element in ai_properties:
            output_stream.write(struct.pack('<I', ai_property_element.ai_flags))
            output_stream.write(struct.pack('>I', len(ai_property_element.ai_type_name)))
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('<H', ai_property_element.ai_size))
            output_stream.write(struct.pack('<H', ai_property_element.leap_jump_speed))

        for ai_property_element in ai_properties:
            name_length = len(ai_property_element.ai_type_name)
            if name_length > 0:
                output_stream.write(struct.pack('<%ss' % name_length, TAG.string_to_bytes(ai_property_element.ai_type_name, False)))

def write_functions(output_stream, TAG, functions, functions_header):
    if len(functions) > 0:
        functions_header.write(output_stream, TAG, True)
        for function_element in functions:
            output_stream.write(struct.pack('<I', function_element.flags))
            output_stream.write(struct.pack('>I', len(function_element.import_name)))
            output_stream.write(struct.pack('>I', len(function_element.export_name)))
            output_stream.write(struct.pack('>I', len(function_element.turn_off_with)))
            output_stream.write(struct.pack('<f', function_element.min_value))
            shader_processing.write_function_size(output_stream, function_element.function_property)
            output_stream.write(struct.pack('>I', len(function_element.scale_by)))

        for function_element in functions:
            import_name_length = len(function_element.import_name)
            if import_name_length > 0:
                output_stream.write(struct.pack('<%ss' % import_name_length, TAG.string_to_bytes(function_element.import_name, False)))

            export_name_length = len(function_element.export_name)
            if export_name_length > 0:
                output_stream.write(struct.pack('<%ss' % export_name_length, TAG.string_to_bytes(function_element.export_name, False)))

            turn_off_with_name_length = len(function_element.turn_off_with)
            if turn_off_with_name_length > 0:
                output_stream.write(struct.pack('<%ss' % turn_off_with_name_length, TAG.string_to_bytes(function_element.turn_off_with, False)))

            shader_processing.write_function(output_stream, TAG, function_element.function_property)

            scale_by_name_length = len(function_element.scale_by)
            if scale_by_name_length > 0:
                output_stream.write(struct.pack('<%ss' % scale_by_name_length, TAG.string_to_bytes(function_element.scale_by, False)))

def write_attachments(output_stream, TAG, attachments, attachments_header):
    if len(attachments) > 0:
        attachments_header.write(output_stream, TAG, True)
        for attachment_element in attachments:
            attachment_element.attachment_type.write(output_stream, False, True)
            output_stream.write(struct.pack('>I', len(attachment_element.marker)))
            output_stream.write(struct.pack('<H', attachment_element.change_color))
            output_stream.write(struct.pack('<2x'))
            output_stream.write(struct.pack('>I', len(attachment_element.primary_scale)))
            output_stream.write(struct.pack('>I', len(attachment_element.secondary_scale)))

        for attachment_element in attachments:
            attachment_type_name_length = len(attachment_element.attachment_type.name)
            if attachment_type_name_length > 0:
                output_stream.write(struct.pack('<%ssx' % attachment_type_name_length, TAG.string_to_bytes(attachment_element.attachment_type.name, False)))

            marker_name_length = len(attachment_element.marker)
            if marker_name_length > 0:
                output_stream.write(struct.pack('<%ss' % marker_name_length, TAG.string_to_bytes(attachment_element.marker, False)))

            primary_scale_name_length = len(attachment_element.primary_scale)
            if primary_scale_name_length > 0:
                output_stream.write(struct.pack('<%ss' % primary_scale_name_length, TAG.string_to_bytes(attachment_element.primary_scale, False)))

            secondary_scale_name_length = len(attachment_element.secondary_scale)
            if secondary_scale_name_length > 0:
                output_stream.write(struct.pack('<%ss' % secondary_scale_name_length, TAG.string_to_bytes(attachment_element.secondary_scale, False)))

def write_tag_ref(output_stream, TAG, tag_refs, tag_ref_header):
    if len(tag_refs) > 0:
        tag_ref_header.write(output_stream, TAG, True)
        for tag_ref_element in tag_refs:
            tag_ref_element.write(output_stream, False, True)

        for tag_ref_element in tag_refs:
            tag_ref_name_length = len(tag_ref_element.name)
            if tag_ref_name_length > 0:
                output_stream.write(struct.pack('<%ssx' % tag_ref_name_length, TAG.string_to_bytes(tag_ref_element.name, False)))

def write_old_functions(output_stream, TAG, old_functions, old_functions_header):
    if len(old_functions) > 0:
        old_functions_header.write(output_stream, TAG, True)
        for old_function_element in old_functions:
            output_stream.write(struct.pack('<76x'))
            output_stream.write(struct.pack('>I', len(old_function_element.name)))

        for old_function_element in old_functions:
            old_function_name_length = len(old_function_element.name)
            if old_function_name_length > 0:
                output_stream.write(struct.pack('<%ss' % old_function_name_length, TAG.string_to_bytes(old_function_element.name, False)))

def write_change_colors(output_stream, TAG, change_colors, change_colors_header):
    if len(change_colors) > 0:
        change_colors_header.write(output_stream, TAG, True)
        for change_colors_element in change_colors:
            change_colors_element.initial_permutations_tag_block.write(output_stream, False)
            change_colors_element.functions_tag_block.write(output_stream, False)

        for change_colors_element in change_colors:
            if len(change_colors_element.initial_permutations) > 0:
                change_colors_element.initial_permutations_header.write(output_stream, TAG, True)
                for initial_permutation_element in change_colors_element.initial_permutations:
                    output_stream.write(struct.pack('<f', initial_permutation_element.weight))
                    output_stream.write(struct.pack('<fff', initial_permutation_element.color_lower_bound[0], initial_permutation_element.color_lower_bound[1], initial_permutation_element.color_lower_bound[2]))
                    output_stream.write(struct.pack('<fff', initial_permutation_element.color_upper_bound[0], initial_permutation_element.color_upper_bound[1], initial_permutation_element.color_upper_bound[2]))
                    output_stream.write(struct.pack('>I', len(initial_permutation_element.variant_name)))

                for initial_permutation_element in change_colors_element.initial_permutations:
                    variant_name_length = len(initial_permutation_element.variant_name)
                    if variant_name_length > 0:
                        output_stream.write(struct.pack('<%ss' % variant_name_length, TAG.string_to_bytes(initial_permutation_element.variant_name, False)))

            if len(change_colors_element.functions) > 0:
                change_colors_element.functions_header.write(output_stream, TAG, True)
                for function_element in change_colors_element.functions:
                    output_stream.write(struct.pack('<4x'))
                    output_stream.write(struct.pack('<H', function_element.scale_flags))
                    output_stream.write(struct.pack('<2x'))
                    output_stream.write(struct.pack('<fff', function_element.color_lower_bound[0], function_element.color_lower_bound[1], function_element.color_lower_bound[2]))
                    output_stream.write(struct.pack('<fff', function_element.color_upper_bound[0], function_element.color_upper_bound[1], function_element.color_upper_bound[2]))
                    output_stream.write(struct.pack('>I', len(function_element.darken_by)))
                    output_stream.write(struct.pack('>I', len(function_element.scale_by)))

                for function_element in change_colors_element.functions:
                    darken_by_name_length = len(function_element.darken_by)
                    if darken_by_name_length > 0:
                        output_stream.write(struct.pack('<%ss' % darken_by_name_length, TAG.string_to_bytes(function_element.darken_by, False)))

                    scale_by_name_length = len(function_element.scale_by)
                    if scale_by_name_length > 0:
                        output_stream.write(struct.pack('<%ss' % scale_by_name_length, TAG.string_to_bytes(function_element.scale_by, False)))

def write_predicted_resources(output_stream, TAG, predicted_resources, predicted_resources_header):
    if len(predicted_resources) > 0:
        predicted_resources_header.write(output_stream, TAG, True)
        for predicted_resource_element in predicted_resources:
            output_stream.write(struct.pack('<H', predicted_resource_element.predicted_resources_type))
            output_stream.write(struct.pack('<h', predicted_resource_element.resource_index))
            output_stream.write(struct.pack('<i', predicted_resource_element.tag_index))
