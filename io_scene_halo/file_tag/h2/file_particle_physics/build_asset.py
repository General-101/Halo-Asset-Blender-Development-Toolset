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

from ....global_functions import tag_format, shader_processing

def write_body(output_stream, TAG, PARTICLEPHYSICS):
    PARTICLEPHYSICS.body_header.write(output_stream, TAG, True)
    PARTICLEPHYSICS.template.write(output_stream, False, True)
    output_stream.write(struct.pack('<I', PARTICLEPHYSICS.flags))
    PARTICLEPHYSICS.movements_tag_block.write(output_stream, False)

    template_name_length = len(PARTICLEPHYSICS.template.name)
    if template_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % template_name_length, TAG.string_to_bytes(PARTICLEPHYSICS.template.name, False)))

def write_movements(output_stream, TAG, movements, movements_header):
    if len(movements) > 0:
        movements_header.write(output_stream, TAG, True)
        for movement_element in movements:
            output_stream.write(struct.pack('<H', movement_element.movement_type))
            output_stream.write(struct.pack('<2x'))
            movement_element.parameters_tag_block.write(output_stream, False)
            output_stream.write(struct.pack('<8x'))

        for movement_element in movements:
            if len(movement_element.parameters) > 0:
                movement_element.parameters_header.write(output_stream, TAG, True)
                for parameter_element in movement_element.parameters:
                    output_stream.write(struct.pack('<i', parameter_element.parameter_id))
                    output_stream.write(struct.pack('<H', parameter_element.animation_property[0].input_type))
                    output_stream.write(struct.pack('<H', parameter_element.animation_property[0].range_type))
                    output_stream.write(struct.pack('<H', parameter_element.animation_property[0].output_modifier))
                    output_stream.write(struct.pack('<H', parameter_element.animation_property[0].output_modifier_input))
                    shader_processing.write_function_size(output_stream, parameter_element.animation_property[0])

                for parameter_element in movement_element.parameters:
                    parameter_element.animation_property[0].function_header.write(output_stream, TAG, True)
                    shader_processing.write_function(output_stream, TAG, parameter_element.animation_property[0])

def build_asset(output_stream, PARTICLEPHYSICS, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    PARTICLEPHYSICS.header.write(output_stream, False, True)
    write_body(output_stream, TAG, PARTICLEPHYSICS)

    write_movements(output_stream, TAG, PARTICLEPHYSICS.movements, PARTICLEPHYSICS.movements_header)
