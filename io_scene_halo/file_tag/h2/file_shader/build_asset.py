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

from .format import FunctionTypeEnum
from ....global_functions import tag_format, shader_processing

def write_body(output_stream, TAG, SHADER):
    SHADER.body_header.write(output_stream, TAG, True)
    SHADER.template.write(output_stream, False, True)
    output_stream.write(struct.pack('>I', len(SHADER.material_name)))
    SHADER.runtime_properties_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<H', SHADER.flags))
    SHADER.parameters_tag_block.write(output_stream, False)
    SHADER.postprocess_definition_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<4x'))
    SHADER.predicted_resources_tag_block.write(output_stream, False)
    SHADER.light_response.write(output_stream, False, True)
    output_stream.write(struct.pack('<H', SHADER.shader_lod_bias))
    output_stream.write(struct.pack('<H', SHADER.specular_type))
    output_stream.write(struct.pack('<H', SHADER.lightmap_type))
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<f', SHADER.lightmap_specular_brightness))
    output_stream.write(struct.pack('<f', SHADER.lightmap_ambient_bias))
    SHADER.postprocess_properties_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', SHADER.added_depth_bias_offset))
    output_stream.write(struct.pack('<f', SHADER.added_depth_bias_slope))

    template_name_length = len(SHADER.template.name)
    material_name_length = len(SHADER.material_name)
    if template_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % template_name_length, TAG.string_to_bytes(SHADER.template.name, False)))
    if material_name_length > 0:
        output_stream.write(struct.pack('<%ss' % material_name_length, TAG.string_to_bytes(SHADER.material_name, False)))

def build_asset(output_stream, SHADER, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    SHADER.header.write(output_stream, False, True)
    write_body(output_stream, TAG, SHADER)

    shader_processing.write_parameters(output_stream, TAG, SHADER.parameters, SHADER.parameters_header)
