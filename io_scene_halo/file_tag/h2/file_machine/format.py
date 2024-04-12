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
from ..file_device.format import DeviceAsset

class MachineTypeEnum(Enum):
    door = 0
    platform = auto()
    gear = auto()

class MachineFlags(Flag):
    pathfinding_obstacle = auto()
    but_not_when_open = auto()
    elevator = auto()

class CollisionResponseEnum(Enum):
    pause_until_crushed = 0
    reverse_directions = auto()

class PathfindingPolicyEnum(Enum):
    discs = 0
    sectors = auto()
    cut_out = auto()
    none = auto()

class MachineAsset(DeviceAsset):
    def __init__(self):
        super().__init__()
        self.header = None
        self.machine_body_header = None
        self.machine_body = None

    class MachineBody(DeviceAsset.DeviceBody):
        def __init__(self, machine_type=0, machine_flags=0, door_open_time=0.0, door_occlusion_time=(0.0, 0.0), collision_response=0, elevator_node=0, pathfinding_policy=0):
            super().__init__()
            self.machine_type = machine_type
            self.machine_flags = machine_flags
            self.door_open_time = door_open_time
            self.door_occlusion_time = door_occlusion_time
            self.collision_response = collision_response
            self.elevator_node = elevator_node
            self.pathfinding_policy = pathfinding_policy
