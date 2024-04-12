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

from math import radians
from ....global_functions import tag_format, shader_processing
from ....file_tag.h2.file_shader.format import FunctionTypeEnum

def write_body(output_stream, TAG, CAMERATRACK):
    CAMERATRACK.camera_track_body_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<4x'))
    CAMERATRACK.camera_track_body.control_points_tag_block.write(output_stream, False)

def write_control_points(output_stream, TAG, control_points, control_points_header):
    if len(control_points) > 0:
        control_points_header.write(output_stream, TAG, True)
        for control_point_element in control_points:
            output_stream.write(struct.pack('<fff', *control_point_element.position))
            output_stream.write(struct.pack('<ffff', *control_point_element.orientation))

def build_asset(output_stream, CAMERATRACK, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    CAMERATRACK.header.write(output_stream, False, True)
    write_body(output_stream, TAG, CAMERATRACK)

    write_control_points(output_stream, TAG, CAMERATRACK.control_points, CAMERATRACK.control_points_header)
