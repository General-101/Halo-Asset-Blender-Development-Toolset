# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Steven Garcia
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

from .format import CameraTrackAsset
from mathutils import Vector, Quaternion
from ..global_functions.tag_format import TagAsset

DEBUG_PARSER = True
DEBUG_HEADER = True
DEBUG_BODY = True
DEBUG_CONTROL_POINTS = True

def process_file_retail(input_stream, report):
    TAG = TagAsset()
    CAMERATRACK = CameraTrackAsset()

    header_struct = struct.unpack('>hbb32s4sIIIIHbb4s', input_stream.read(64))
    CAMERATRACK.header = TAG.Header()
    CAMERATRACK.header.unk1 = header_struct[0]
    CAMERATRACK.header.flags = header_struct[1]
    CAMERATRACK.header.type = header_struct[2]
    CAMERATRACK.header.name = header_struct[3].decode().rstrip('\x00')
    CAMERATRACK.header.tag_group = header_struct[4].decode().rstrip('\x00')
    CAMERATRACK.header.checksum = header_struct[5]
    CAMERATRACK.header.data_offset = header_struct[6]
    CAMERATRACK.header.data_length = header_struct[7]
    CAMERATRACK.header.unk2 = header_struct[8]
    CAMERATRACK.header.version = header_struct[9]
    CAMERATRACK.header.destination = header_struct[10]
    CAMERATRACK.header.plugin_handle = header_struct[11]
    CAMERATRACK.header.engine_tag = header_struct[12].decode().rstrip('\x00')

    if DEBUG_PARSER and DEBUG_HEADER:
        print(" ===== Tag Header ===== ")
        print("Unknown Value: ", CAMERATRACK.header.unk1)
        print("Flags: ", CAMERATRACK.header.flags)
        print("Type: ", CAMERATRACK.header.type)
        print("Name: ", CAMERATRACK.header.name)
        print("Tag Group: ", CAMERATRACK.header.tag_group)
        print("Checksum: ", CAMERATRACK.header.checksum)
        print("Data Offset: ", CAMERATRACK.header.data_offset)
        print("Data Length:", CAMERATRACK.header.data_length)
        print("Unknown Value: ", CAMERATRACK.header.unk2)
        print("Version: ", CAMERATRACK.header.version)
        print("Destination: ", CAMERATRACK.header.destination)
        print("Plugin Handle: ", CAMERATRACK.header.plugin_handle)
        print("Engine Tag: ", CAMERATRACK.header.engine_tag)
        print(" ")

    body_struct = struct.unpack('>4xiII32x', input_stream.read(48))
    CAMERATRACK.camera_track_body = CAMERATRACK.CameraTrackBody()
    CAMERATRACK.camera_track_body.control_points_tag_block = TAG.TagBlock(body_struct[0], 16, body_struct[1], body_struct[2])

    if DEBUG_PARSER and DEBUG_BODY:
        print(" ===== Trak Body ===== ")
        print("Camera Track Tag Block Count: ", CAMERATRACK.camera_track_body.control_points_tag_block.count)
        print("Camera Track Tag Block Maximum Count: ", CAMERATRACK.camera_track_body.control_points_tag_block.maximum_count)
        print("Camera Track Tag Block Address: ", CAMERATRACK.camera_track_body.control_points_tag_block.address)
        print("Camera Track Tag Block Definition: ", CAMERATRACK.camera_track_body.control_points_tag_block.definition)
        print(" ")

    for control_point_idx in range(CAMERATRACK.camera_track_body.control_points_tag_block.count):
        control_point_struct = struct.unpack('>fffffff32x', input_stream.read(60))
        control_point = CAMERATRACK.ControlPoints()
        control_point.position = Vector((control_point_struct[0], control_point_struct[1], control_point_struct[2])) * 100
        control_point.orientation = Quaternion((control_point_struct[6], control_point_struct[3], control_point_struct[4], control_point_struct[5])).inverted()

        CAMERATRACK.control_points.append(control_point)

    if DEBUG_PARSER and DEBUG_CONTROL_POINTS:
        print(" ===== Control Points ===== ")
        for control_point_idx, control_point in enumerate(CAMERATRACK.control_points):
            print(" ===== Control Point %s ===== " % control_point_idx)
            print("Position: ", control_point.position)
            print("Orientation: ", control_point.orientation)
            print(" ")

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    return CAMERATRACK
