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
from ..file_object.format import ObjectAsset

class DeviceFlags(Flag):
    position_loops = auto()
    unused = auto()
    allow_interpolation = auto()

class LightmapFlags(Flag):
    dont_use_in_lightmap = auto()
    dont_use_in_lightprobe = auto()

class DeviceAsset(ObjectAsset):
    def __init__(self):
        super().__init__()
        self.header = None
        self.device_body_header = None
        self.device_body = None

    class DeviceBody(ObjectAsset.ObjectBody):
        def __init__(self, device_flags=0, power_transition_time=0.0, power_acceleration_time=0.0, position_transition_time=0.0, position_acceleration_time=0.0,
                     depowered_position_transition_time=0.0, depowered_position_acceleration_time=0.0, lightmap_flags=0, open_up=None, close_down=None, opened=None, closed=None,
                     depowered=None, repowered=None, delay_time=0.0, delay_effect=None, automatic_activation_radius=0.0):
            super().__init__()
            self.device_flags = device_flags
            self.power_transition_time = power_transition_time
            self.power_acceleration_time = power_acceleration_time
            self.position_transition_time = position_transition_time
            self.position_acceleration_time = position_acceleration_time
            self.depowered_position_transition_time = depowered_position_transition_time
            self.depowered_position_acceleration_time = depowered_position_acceleration_time
            self.lightmap_flags = lightmap_flags
            self.open_up = open_up
            self.close_down = close_down
            self.opened = opened
            self.closed = closed
            self.depowered = depowered
            self.repowered = repowered
            self.delay_time = delay_time
            self.delay_effect = delay_effect
            self.automatic_activation_radius = automatic_activation_radius
