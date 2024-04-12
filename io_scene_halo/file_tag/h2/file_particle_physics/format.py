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

from enum import Flag, Enum, auto

class MovementTypeEnum(Enum):
    physics = 0
    collider = auto()
    swarm = auto()
    wind = auto()

class ParticlePhysicsFlags(Flag):
    physics = auto()
    collide_with_structure = auto()
    collide_with_media = auto()
    collide_with_scenery = auto()
    collide_with_vehicles = auto()
    collide_with_bipeds = auto()
    swarm = auto()
    wind = auto()

class ParticlePhysicsAsset():
    def __init__(self):
        self.header = None
        self.particle_physics_body_header = None
        self.particle_physics_body = None
        self.movements_header = None
        self.movements = None

    class ParticlePhysicsBody:
        def __init__(self, template=None, flags=0, movements_tag_block=None):
            self.template = template
            self.flags = flags
            self.movements_tag_block = movements_tag_block

    class Movement:
        def __init__(self, movement_type=0, parameters_tag_block=None, parameters_header=None, parameters=None):
            self.movement_type = movement_type
            self.parameters_tag_block = parameters_tag_block
            self.parameters_header = parameters_header
            self.parameters = parameters

    class Parameter:
        def __init__(self, parameter_id=0, animation_property=None):
            self.parameter_id = parameter_id
            self.animation_property = animation_property