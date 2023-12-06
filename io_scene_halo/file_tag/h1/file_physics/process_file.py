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
from .format import PhysicsAsset, PoweredMassPointFlags, MassPointFlags, FrictionTypeEnum

XML_OUTPUT = False

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    PHYSICS = PhysicsAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    PHYSICS.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    PHYSICS.phys_body = PHYSICS.PhysBody()
    PHYSICS.phys_body.radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "radius"))
    PHYSICS.phys_body.moment_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "moment"))
    PHYSICS.phys_body.mass = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "mass"))
    PHYSICS.phys_body.center_of_mass = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "center of mass"))
    PHYSICS.phys_body.density = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "density"))
    PHYSICS.phys_body.gravity_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "gravity scale"))
    PHYSICS.phys_body.ground_friction = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ground friction"))
    PHYSICS.phys_body.ground_depth = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ground depth"))
    PHYSICS.phys_body.ground_damp_fraction = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ground damp fraction"))
    PHYSICS.phys_body.ground_normal_k1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ground normal k1"))
    PHYSICS.phys_body.ground_normal_k0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ground normal k0"))
    input_stream.read(4) # Padding?
    PHYSICS.phys_body.water_friction = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "water friction"))
    PHYSICS.phys_body.water_depth = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "water depth"))
    PHYSICS.phys_body.water_density = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "water density"))
    input_stream.read(4) # Padding?
    PHYSICS.phys_body.air_friction = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "air friction"))
    input_stream.read(4) # Padding?
    PHYSICS.phys_body.xx_moment = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "xx moment"))
    PHYSICS.phys_body.yy_moment = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "yy moment"))
    PHYSICS.phys_body.zz_moment = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "zz moment"))
    PHYSICS.phys_body.inertial_matrix_and_inverse_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "inertial matrix and inverse"))
    PHYSICS.phys_body.powered_mass_points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "powered mass points"))
    PHYSICS.phys_body.mass_points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "mass points"))

    PHYSICS.inertial_matrix_and_inverse = []
    inertial_matrix_and_inverse_node = tag_format.get_xml_node(XML_OUTPUT, PHYSICS.phys_body.inertial_matrix_and_inverse_tag_block.count, tag_node, "name", "inertial matrix and inverse")
    for inertial_matrix_and_inverse_idx in range(PHYSICS.phys_body.inertial_matrix_and_inverse_tag_block.count):
        inertial_matrix_and_inverse_element_node = None
        if XML_OUTPUT:
            inertial_matrix_and_inverse_element_node = TAG.xml_doc.createElement('element')
            inertial_matrix_and_inverse_element_node.setAttribute('index', str(inertial_matrix_and_inverse_idx))
            inertial_matrix_and_inverse_node.appendChild(inertial_matrix_and_inverse_element_node)

        InertialMatrixAndInverse = PHYSICS.InertialMatrixAndInverse()
        InertialMatrixAndInverse.yy_zz_xy_zx = TAG.read_vector(input_stream, TAG, tag_format.XMLData(inertial_matrix_and_inverse_element_node, "yy+zz -xy -zx"))
        InertialMatrixAndInverse.xy_zz_xx_yz = TAG.read_vector(input_stream, TAG, tag_format.XMLData(inertial_matrix_and_inverse_element_node, "-xy zz+xx -yz"))
        InertialMatrixAndInverse.zx_yz_xx_yy = TAG.read_vector(input_stream, TAG, tag_format.XMLData(inertial_matrix_and_inverse_element_node, "-zx -yz xx+yy"))

        PHYSICS.inertial_matrix_and_inverse.append(InertialMatrixAndInverse)

    PHYSICS.powered_mass_points = []
    powered_mass_point_node = tag_format.get_xml_node(XML_OUTPUT, PHYSICS.phys_body.powered_mass_points_tag_block.count, tag_node, "name", "powered mass points")
    for powered_mass_point_idx in range(PHYSICS.phys_body.powered_mass_points_tag_block.count):
        powered_mass_point_element_node = None
        if XML_OUTPUT:
            powered_mass_point_element_node = TAG.xml_doc.createElement('element')
            powered_mass_point_element_node.setAttribute('index', str(powered_mass_point_idx))
            powered_mass_point_node.appendChild(powered_mass_point_element_node)

        powered_mass_point = PHYSICS.PoweredMassPoint()
        powered_mass_point.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(powered_mass_point_element_node, "name"))
        powered_mass_point.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(powered_mass_point_element_node, "flags", PoweredMassPointFlags))
        powered_mass_point.antigrav_strength = TAG.read_float(input_stream, TAG, tag_format.XMLData(powered_mass_point_element_node, "antigrav strength"))
        powered_mass_point.antigrav_offset = TAG.read_float(input_stream, TAG, tag_format.XMLData(powered_mass_point_element_node, "antigrav offset"))
        powered_mass_point.antigrav_height = TAG.read_float(input_stream, TAG, tag_format.XMLData(powered_mass_point_element_node, "antigrav height"))
        powered_mass_point.antigrav_damp_fraction = TAG.read_float(input_stream, TAG, tag_format.XMLData(powered_mass_point_element_node, "antigrav damp fraction"))
        powered_mass_point.antigrav_normal_k1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(powered_mass_point_element_node, "antigrav normal k1"))
        powered_mass_point.antigrav_normal_k0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(powered_mass_point_element_node, "antigrav normal k0"))
        input_stream.read(68) # Padding?

        PHYSICS.powered_mass_points.append(powered_mass_point)

    PHYSICS.mass_points = []
    mass_point_node = tag_format.get_xml_node(XML_OUTPUT, PHYSICS.phys_body.mass_points_tag_block.count, tag_node, "name", "mass points")
    for mass_point_idx in range(PHYSICS.phys_body.mass_points_tag_block.count):
        mass_point_element_node = None
        if XML_OUTPUT:
            mass_point_element_node = TAG.xml_doc.createElement('element')
            mass_point_element_node.setAttribute('index', str(mass_point_idx))
            mass_point_node.appendChild(mass_point_element_node)

        mass_point = PHYSICS.MassPoint()
        mass_point.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(mass_point_element_node, "name"))
        mass_point.powered_mass_point = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(mass_point_element_node, "powered mass point", None, PHYSICS.phys_body.powered_mass_points_tag_block.count, "powered_mass_point_block"))
        mass_point.model_node = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(mass_point_element_node, "model node"))
        mass_point.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(mass_point_element_node, "flags", MassPointFlags))
        mass_point.relative_mass = TAG.read_float(input_stream, TAG, tag_format.XMLData(mass_point_element_node, "relative mass"))
        mass_point.mass = TAG.read_float(input_stream, TAG, tag_format.XMLData(mass_point_element_node, "mass"))
        mass_point.relative_density = TAG.read_float(input_stream, TAG, tag_format.XMLData(mass_point_element_node, "relative density"))
        mass_point.density = TAG.read_float(input_stream, TAG, tag_format.XMLData(mass_point_element_node, "density"))
        mass_point.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(mass_point_element_node, "position"), True)
        mass_point.forward = TAG.read_vector(input_stream, TAG, tag_format.XMLData(mass_point_element_node, "forward"))
        mass_point.up = TAG.read_vector(input_stream, TAG, tag_format.XMLData(mass_point_element_node, "up"))
        mass_point.friction_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(mass_point_element_node, "friction type", FrictionTypeEnum))
        input_stream.read(2) # Padding?
        mass_point.friction_parallel_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(mass_point_element_node, "friction parallel scale"))
        mass_point.friction_perpendicular_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(mass_point_element_node, "friction perpendicular scale"))
        mass_point.radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(mass_point_element_node, "radius"), True)
        input_stream.read(20) # Padding?

        PHYSICS.mass_points.append(mass_point)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, PHYSICS.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return PHYSICS
