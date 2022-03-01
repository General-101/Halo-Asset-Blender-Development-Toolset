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

from mathutils import Vector
from .format import PhysicsAsset
from ..global_functions.tag_format import TagAsset

DEBUG_PARSER = False
DEBUG_HEADER = True
DEBUG_BODY = True
DEBUG_INERTIAL_MATRIX_AND_INVERSE = True
DEBUG_POWERED_MASS_POINT = True
DEBUG_MASS_POINT = True

def process_file_retail(input_stream, report):
    TAG = TagAsset()
    PHYSICS = PhysicsAsset()

    header_struct = struct.unpack('>hbb32s4sIIIIHbb4s', input_stream.read(64))
    PHYSICS.header = TAG.Header()
    PHYSICS.header.unk1 = header_struct[0]
    PHYSICS.header.flags = header_struct[1]
    PHYSICS.header.type = header_struct[2]
    PHYSICS.header.name = header_struct[3].decode().rstrip('\x00')
    PHYSICS.header.tag_group = header_struct[4].decode().rstrip('\x00')
    PHYSICS.header.checksum = header_struct[5]
    PHYSICS.header.data_offset = header_struct[6]
    PHYSICS.header.data_length = header_struct[7]
    PHYSICS.header.unk2 = header_struct[8]
    PHYSICS.header.version = header_struct[9]
    PHYSICS.header.destination = header_struct[10]
    PHYSICS.header.plugin_handle = header_struct[11]
    PHYSICS.header.engine_tag = header_struct[12].decode().rstrip('\x00')

    if DEBUG_PARSER and DEBUG_HEADER:
        print(" ===== Tag Header ===== ")
        print("Unknown Value: ", PHYSICS.header.unk1)
        print("Flags: ", PHYSICS.header.flags)
        print("Type: ", PHYSICS.header.type)
        print("Name: ", PHYSICS.header.name)
        print("Tag Group: ", PHYSICS.header.tag_group)
        print("Checksum: ", PHYSICS.header.checksum)
        print("Data Offset: ", PHYSICS.header.data_offset)
        print("Data Length:", PHYSICS.header.data_length)
        print("Unknown Value: ", PHYSICS.header.unk2)
        print("Version: ", PHYSICS.header.version)
        print("Destination: ", PHYSICS.header.destination)
        print("Plugin Handle: ", PHYSICS.header.plugin_handle)
        print("Engine Tag: ", PHYSICS.header.engine_tag)
        print(" ")


    phys_body_struct = struct.unpack('>fffffffffffff4xfff4xf4xfffiIIiIIiII', input_stream.read(128))
    PHYSICS.phys_body = PHYSICS.PhysBody()
    PHYSICS.phys_body.radius = phys_body_struct[0]
    PHYSICS.phys_body.moment_scale = phys_body_struct[1]
    PHYSICS.phys_body.mass = phys_body_struct[2]
    PHYSICS.phys_body.center_of_mass = Vector((phys_body_struct[3], phys_body_struct[4], phys_body_struct[5]))
    PHYSICS.phys_body.density = phys_body_struct[6]
    PHYSICS.phys_body.gravity_scale = phys_body_struct[7]
    PHYSICS.phys_body.ground_friction = phys_body_struct[8]
    PHYSICS.phys_body.ground_depth = phys_body_struct[9]
    PHYSICS.phys_body.ground_damp_fraction = phys_body_struct[10]
    PHYSICS.phys_body.ground_normal_k1 = phys_body_struct[11]
    PHYSICS.phys_body.ground_normal_k0 = phys_body_struct[12]
    PHYSICS.phys_body.water_friction = phys_body_struct[13]
    PHYSICS.phys_body.water_depth = phys_body_struct[14]
    PHYSICS.phys_body.water_density = phys_body_struct[15]
    PHYSICS.phys_body.air_friction = phys_body_struct[16]
    PHYSICS.phys_body.xx_moment = phys_body_struct[17]
    PHYSICS.phys_body.yy_moment = phys_body_struct[18]
    PHYSICS.phys_body.zz_moment = phys_body_struct[19]
    PHYSICS.phys_body.inertial_matrix_and_inverse_tag_block = TAG.TagBlock(phys_body_struct[20], 2, phys_body_struct[21], phys_body_struct[22])
    PHYSICS.phys_body.powered_mass_points_tag_block = TAG.TagBlock(phys_body_struct[23], 32, phys_body_struct[24], phys_body_struct[25])
    PHYSICS.phys_body.mass_points_tag_block = TAG.TagBlock(phys_body_struct[26], 32, phys_body_struct[27], phys_body_struct[28])

    if DEBUG_PARSER and DEBUG_BODY:
        print(" ===== Phys Body ===== ")
        print("Radius: ", PHYSICS.phys_body.radius)
        print("Moment Scale: ", PHYSICS.phys_body.moment_scale)
        print("Mass: ", PHYSICS.phys_body.mass)
        print("Center of Mass: ", PHYSICS.phys_body.center_of_mass)
        print("Density: ", PHYSICS.phys_body.density)
        print("Gravity Scale: ", PHYSICS.phys_body.gravity_scale)
        print("Ground Friction: ", PHYSICS.phys_body.ground_friction)
        print("Ground Depth: ", PHYSICS.phys_body.ground_depth)
        print("Ground Damp Fraction: ", PHYSICS.phys_body.ground_damp_fraction)
        print("Ground Normal K1: ", PHYSICS.phys_body.ground_normal_k1)
        print("Ground Normal K0: ", PHYSICS.phys_body.ground_normal_k0)
        print("Water Friction: ", PHYSICS.phys_body.water_friction)
        print("Water Depth: ", PHYSICS.phys_body.water_depth)
        print("Water Density: ", PHYSICS.phys_body.water_density)
        print("Air Friction: ", PHYSICS.phys_body.air_friction)
        print("XX Moment: ", PHYSICS.phys_body.xx_moment)
        print("YY Moment: ", PHYSICS.phys_body.yy_moment)
        print("ZZ Moment: ", PHYSICS.phys_body.zz_moment)
        print("Inertial Matrix and Inverse Tag Block Count: ", PHYSICS.phys_body.inertial_matrix_and_inverse_tag_block.count)
        print("Inertial Matrix and Inverse Tag Block Maximum Count: ", PHYSICS.phys_body.inertial_matrix_and_inverse_tag_block.maximum_count)
        print("Inertial Matrix and Inverse Tag Block Address: ", PHYSICS.phys_body.inertial_matrix_and_inverse_tag_block.address)
        print("Inertial Matrix and Inverse Tag Block Definition: ", PHYSICS.phys_body.inertial_matrix_and_inverse_tag_block.definition)
        print("Powered Mass Points Tag Block Count: ", PHYSICS.phys_body.powered_mass_points_tag_block.count)
        print("Powered Mass Points Tag Block Maximum Count: ", PHYSICS.phys_body.powered_mass_points_tag_block.maximum_count)
        print("Powered Mass Points Tag Block Address: ", PHYSICS.phys_body.powered_mass_points_tag_block.address)
        print("Powered Mass Points Tag Block Definition: ", PHYSICS.phys_body.powered_mass_points_tag_block.definition)
        print("Mass Point Tag Block Count: ", PHYSICS.phys_body.mass_points_tag_block.count)
        print("Mass Point Tag Block Maximum Count: ", PHYSICS.phys_body.mass_points_tag_block.maximum_count)
        print("Mass Point Tag Block Address: ", PHYSICS.phys_body.mass_points_tag_block.address)
        print("Mass Point Tag Block Definition: ", PHYSICS.phys_body.mass_points_tag_block.definition)
        print(" ")

    for matrix_idx in range(PHYSICS.phys_body.inertial_matrix_and_inverse_tag_block.count):
        phys_inertial_matrix_and_inverse_tag_block_struct = struct.unpack('>fffffffff', input_stream.read(36))
        InertialMatrixAndInverse = PHYSICS.InertialMatrixAndInverse()
        InertialMatrixAndInverse.yy_zz_xy_zx = Vector((phys_inertial_matrix_and_inverse_tag_block_struct[0], phys_inertial_matrix_and_inverse_tag_block_struct[1], phys_inertial_matrix_and_inverse_tag_block_struct[2]))
        InertialMatrixAndInverse.xy_zz_xx_yz = Vector((phys_inertial_matrix_and_inverse_tag_block_struct[3], phys_inertial_matrix_and_inverse_tag_block_struct[4], phys_inertial_matrix_and_inverse_tag_block_struct[5]))
        InertialMatrixAndInverse.zx_yz_xx_yy = Vector((phys_inertial_matrix_and_inverse_tag_block_struct[6], phys_inertial_matrix_and_inverse_tag_block_struct[7], phys_inertial_matrix_and_inverse_tag_block_struct[8]))

        PHYSICS.inertial_matrix_and_inverse.append(InertialMatrixAndInverse)

    if DEBUG_PARSER and DEBUG_INERTIAL_MATRIX_AND_INVERSE:
        print(" ===== Inertial Matrix and Inverses ===== ")
        for matrix_idx, matrix in enumerate(PHYSICS.inertial_matrix_and_inverse):
            print(" ===== Inertial Matrix and Inverse %s ===== " % matrix_idx)
            print("yy+zz    -xy     -zx: ", matrix.yy_zz_xy_zx)
            print("-xy    zz+xx    -yz: ", matrix.xy_zz_xx_yz)
            print("-zx     -yz    xx+yy: ", matrix.zx_yz_xx_yy)
            print(" ")

    for powered_mass_point_idx in range(PHYSICS.phys_body.powered_mass_points_tag_block.count):
        phys_powered_mass_point_tag_block_struct = struct.unpack('>32siffffff68x', input_stream.read(128))
        PoweredMassPoint = PHYSICS.PoweredMassPoint()
        PoweredMassPoint.name = phys_powered_mass_point_tag_block_struct[0].decode().rstrip('\x00')
        PoweredMassPoint.flags = phys_powered_mass_point_tag_block_struct[1]
        PoweredMassPoint.antigrav_strength = phys_powered_mass_point_tag_block_struct[2]
        PoweredMassPoint.antigrav_offset = phys_powered_mass_point_tag_block_struct[3]
        PoweredMassPoint.antigrav_height = phys_powered_mass_point_tag_block_struct[4]
        PoweredMassPoint.antigrav_damp_fraction = phys_powered_mass_point_tag_block_struct[5]
        PoweredMassPoint.antigrav_normal_k1 = phys_powered_mass_point_tag_block_struct[6]
        PoweredMassPoint.antigrav_normal_k0 = phys_powered_mass_point_tag_block_struct[7]

        PHYSICS.powered_mass_points.append(PoweredMassPoint)

    if DEBUG_PARSER and DEBUG_POWERED_MASS_POINT:
        print(" ===== Powered Mass Points ===== ")
        for powered_mass_point_idx, powered_mass_point in enumerate(PHYSICS.powered_mass_points):
            print(" ===== Powered Mass Point %s ===== " % powered_mass_point_idx)
            print("Name: ", powered_mass_point.name)
            print("Flags: ", powered_mass_point.flags)
            print("Antigrav Strength: ", powered_mass_point.antigrav_strength)
            print("Antigrav Offset: ", powered_mass_point.antigrav_offset)
            print("Antigrav Height: ", powered_mass_point.antigrav_height)
            print("Antigrav Damp Fraction: ", powered_mass_point.antigrav_damp_fraction)
            print("Antigrav Normal K1: ", powered_mass_point.antigrav_normal_k1)
            print("Antigrav Normal K0: ", powered_mass_point.antigrav_normal_k0)
            print(" ")

    for mass_point_idx in range(PHYSICS.phys_body.mass_points_tag_block.count):
        phys_mass_point_tag_block_struct = struct.unpack('>32shhifffffffffffffh2xfff20x', input_stream.read(128))
        MassPoint = PHYSICS.MassPoint()
        MassPoint.name = phys_mass_point_tag_block_struct[0].decode().rstrip('\x00')
        MassPoint.powered_mass_point = phys_mass_point_tag_block_struct[1]
        MassPoint.model_node = phys_mass_point_tag_block_struct[2]
        MassPoint.flags = phys_mass_point_tag_block_struct[3]
        MassPoint.relative_mass = phys_mass_point_tag_block_struct[4]
        MassPoint.mass = phys_mass_point_tag_block_struct[5]
        MassPoint.relative_density = phys_mass_point_tag_block_struct[6]
        MassPoint.density = phys_mass_point_tag_block_struct[7]
        MassPoint.position = Vector((phys_mass_point_tag_block_struct[8], phys_mass_point_tag_block_struct[9], phys_mass_point_tag_block_struct[10])) * 100
        MassPoint.forward = Vector((phys_mass_point_tag_block_struct[11], phys_mass_point_tag_block_struct[12], phys_mass_point_tag_block_struct[13]))
        MassPoint.up = Vector((phys_mass_point_tag_block_struct[14], phys_mass_point_tag_block_struct[15], phys_mass_point_tag_block_struct[16]))
        MassPoint.friction_type = phys_mass_point_tag_block_struct[17]
        MassPoint.friction_parallel_scale = phys_mass_point_tag_block_struct[18]
        MassPoint.friction_perpendicular_scale = phys_mass_point_tag_block_struct[19]
        MassPoint.radius = phys_mass_point_tag_block_struct[20] * 100

        PHYSICS.mass_points.append(MassPoint)

    if DEBUG_PARSER and DEBUG_MASS_POINT:
        print(" ===== Mass Points ===== ")
        for mass_point_idx, mass_point in enumerate(PHYSICS.mass_points):
            print(" ===== Mass Point %s ===== " % mass_point_idx)
            print("Name: ", mass_point.name)
            print("Powered Mass Point: ", mass_point.powered_mass_point)
            print("Model Node: ", mass_point.model_node)
            print("Flags: ", mass_point.flags)
            print("Relative Mass: ", mass_point.relative_mass)
            print("Mass: ", mass_point.mass)
            print("Relative Density: ", mass_point.relative_density)
            print("Density: ", mass_point.density)
            print("Position: ", mass_point.position)
            print("Forward: ", mass_point.forward)
            print("Up: ", mass_point.up)
            print("Friction Type: ", mass_point.friction_type)
            print("Friction Parellel Scale: ", mass_point.friction_parallel_scale)
            print("Friction Perpendicular Scale: ", mass_point.friction_perpendicular_scale)
            print("Radius: ", mass_point.radius)
            print(" ")

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    return PHYSICS
