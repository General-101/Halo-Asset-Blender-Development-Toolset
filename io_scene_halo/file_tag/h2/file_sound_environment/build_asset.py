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

def write_body(output_stream, TAG, SOUNDENV):
    SOUNDENV.sound_environment_body_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<4x'))
    output_stream.write(struct.pack('<h', SOUNDENV.sound_environment_body.priority))
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<f', SOUNDENV.sound_environment_body.room_intensity))
    output_stream.write(struct.pack('<f', SOUNDENV.sound_environment_body.room_intensity_hf))
    output_stream.write(struct.pack('<f', SOUNDENV.sound_environment_body.room_rolloff))
    output_stream.write(struct.pack('<f', SOUNDENV.sound_environment_body.decay_time))
    output_stream.write(struct.pack('<f', SOUNDENV.sound_environment_body.decay_hf_ratio))
    output_stream.write(struct.pack('<f', SOUNDENV.sound_environment_body.reflections_intensity))
    output_stream.write(struct.pack('<f', SOUNDENV.sound_environment_body.reflections_delay))
    output_stream.write(struct.pack('<f', SOUNDENV.sound_environment_body.reverb_intensity))
    output_stream.write(struct.pack('<f', SOUNDENV.sound_environment_body.reverb_delay))
    output_stream.write(struct.pack('<f', SOUNDENV.sound_environment_body.diffusion))
    output_stream.write(struct.pack('<f', SOUNDENV.sound_environment_body.density))
    output_stream.write(struct.pack('<f', SOUNDENV.sound_environment_body.hf_reference))
    output_stream.write(struct.pack('>I', len(SOUNDENV.sound_environment_body.reflection_type)))
    output_stream.write(struct.pack('<12x'))

def build_asset(output_stream, SOUNDENV, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    SOUNDENV.header.write(output_stream, False, True)
    write_body(output_stream, TAG, SOUNDENV)

    reflection_type_length = len(SOUNDENV.sound_environment_body.reflection_type)
    if reflection_type_length > 0:
        output_stream.write(struct.pack('<%ss' % reflection_type_length, TAG.string_to_bytes(SOUNDENV.sound_environment_body.reflection_type, False)))
