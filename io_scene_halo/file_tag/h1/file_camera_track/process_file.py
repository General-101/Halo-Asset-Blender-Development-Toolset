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
from .format import CameraTrackAsset

XML_OUTPUT = False

def process_file(input_stream, tag_format, report):
    TAG = tag_format.TagAsset()
    CAMERATRACK = CameraTrackAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    CAMERATRACK.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    CAMERATRACK.camera_track_body = CAMERATRACK.CameraTrackBody()
    input_stream.read(4) # Padding?
    CAMERATRACK.camera_track_body.control_points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "control points"))
    input_stream.read(32) # Padding?

    CAMERATRACK.control_points = []
    control_point_node = tag_format.get_xml_node(XML_OUTPUT, CAMERATRACK.camera_track_body.control_points_tag_block.count, tag_node, "name", "control points")
    for control_point_idx in range(CAMERATRACK.camera_track_body.control_points_tag_block.count):
        control_point_element_node = None
        if XML_OUTPUT:
            control_point_element_node = TAG.xml_doc.createElement('element')
            control_point_element_node.setAttribute('index', str(control_point_idx))
            control_point_node.appendChild(control_point_element_node)

        control_point = CAMERATRACK.ControlPoints()
        control_point.position = TAG.read_point_3d(input_stream, TAG,  tag_format.XMLData(control_point_element_node, "position"), True)
        control_point.orientation = TAG.read_quaternion(input_stream, TAG,  tag_format.XMLData(control_point_element_node, "orientation"), True)
        input_stream.read(32) # Padding?

        CAMERATRACK.control_points.append(control_point)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, CAMERATRACK.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return CAMERATRACK
