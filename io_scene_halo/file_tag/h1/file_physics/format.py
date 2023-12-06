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

from mathutils import Vector
from enum import Flag, Enum, auto

class PoweredMassPointFlags(Flag):
    ground_friction = auto()
    water_friction = auto()
    air_friction = auto()
    water_lift = auto()
    air_lift = auto()
    thrust = auto()
    antigrav = auto()

class MassPointFlags(Flag):
    metallic = auto()

class FrictionTypeEnum(Enum):
    point = 0
    forward = auto()
    left = auto()
    up = auto()

class PhysicsAsset():
    def __init__(self):
        self.header = None
        self.phys_body = None
        self.inertial_matrix_and_inverse = None
        self.powered_mass_points = None
        self.mass_points = None

    class PhysBody:
        def __init__(self, radius=0.0, moment_scale=0.0, mass=0.0, center_of_mass=Vector(), density=0.0, gravity_scale=0.0, ground_friction=0.0, ground_depth=0.0,
                     ground_damp_fraction=0.0, ground_normal_k1=0.0, ground_normal_k0=0.0, water_friction=0.0, water_depth=0.0, water_density=0.0, air_friction=0.0,
                     xx_moment=0.0, yy_moment=0.0, zz_moment=0.0, inertial_matrix_and_inverse_tag_block=None, powered_mass_points_tag_block=None, mass_points_tag_block=None,
                     inertial_matrix_and_inverse=None, powered_mass_points=None, mass_points=None):
            self.radius = radius
            self.moment_scale = moment_scale
            self.mass = mass
            self.center_of_mass = center_of_mass
            self.density = density
            self.gravity_scale = gravity_scale
            self.ground_friction = ground_friction
            self.ground_depth = ground_depth
            self.ground_damp_fraction = ground_damp_fraction
            self.ground_normal_k1 = ground_normal_k1
            self.ground_normal_k0 = ground_normal_k0
            self.water_friction = water_friction
            self.water_depth = water_depth
            self.water_density = water_density
            self.air_friction = air_friction
            self.xx_moment = xx_moment
            self.yy_moment = yy_moment
            self.zz_moment = zz_moment
            self.inertial_matrix_and_inverse_tag_block = inertial_matrix_and_inverse_tag_block
            self.powered_mass_points_tag_block = powered_mass_points_tag_block
            self.mass_points_tag_block = mass_points_tag_block
            self.inertial_matrix_and_inverse = inertial_matrix_and_inverse
            self.powered_mass_points = powered_mass_points
            self.mass_points = mass_points

    class InertialMatrixAndInverse:
        def __init__(self, yy_zz_xy_zx=Vector(), xy_zz_xx_yz=Vector(), zx_yz_xx_yy=Vector()):
            self.yy_zz_xy_zx = yy_zz_xy_zx
            self.xy_zz_xx_yz = xy_zz_xx_yz
            self.zx_yz_xx_yy = zx_yz_xx_yy

    class PoweredMassPoint:
        def __init__(self, name="", flags=0, antigrav_strength=0.0, antigrav_offset=0.0, antigrav_height=0.0, antigrav_damp_fraction=0.0, antigrav_normal_k1=0.0,
                     antigrav_normal_k0=0.0):
            self.name = name
            self.flags = flags
            self.antigrav_strength = antigrav_strength
            self.antigrav_offset = antigrav_offset
            self.antigrav_height = antigrav_height
            self.antigrav_damp_fraction = antigrav_damp_fraction
            self.antigrav_normal_k1 = antigrav_normal_k1
            self.antigrav_normal_k0 = antigrav_normal_k0

    class MassPoint:
        def __init__(self, name="", powered_mass_point=0, model_node=0, flags=0, relative_mass=0.0, mass=0.0, relative_density=0.0, density=0.0, position=Vector(),
                     forward=Vector(), up=Vector(), friction_type=0, friction_parallel_scale=0.0, friction_perpendicular_scale=0.0, radius=0.0):
            self.name = name
            self.powered_mass_point = powered_mass_point
            self.model_node = model_node
            self.flags = flags
            self.relative_mass = relative_mass
            self.mass = mass
            self.relative_density = relative_density
            self.density = density
            self.position = position
            self.forward = forward
            self.up = up
            self.friction_type = friction_type
            self.friction_parallel_scale = friction_parallel_scale
            self.friction_perpendicular_scale = friction_perpendicular_scale
            self.radius = radius
