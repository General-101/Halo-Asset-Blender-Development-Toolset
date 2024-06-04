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
from ..global_functions import global_functions

class UbercamObjectTypeEnum(Enum):
    unit = 0
    scenery = auto()
    effect_scenery = auto()

class QUAAsset(global_functions.HaloAsset):
    def __init__(self, filepath=None):
        if filepath:
            super().__init__(filepath)

        self.version = 0
        self.name = ""
        self.units = []
        self.scenery = []
        self.effects_scenery = []
        self.shots = []
        self.extra_cameras = []

    class Scene:
        def __init__(self, version=0, name=""):
            self.version = version
            self.name = name

    class Object:
        def __init__(self, name="", path="", bits=None):
            self.name = name
            self.path = path
            self.bits = bits

    class Shots:
        def __init__(self, frames=None, audio_data=None):
            self.frames = frames
            self.audio_data = audio_data

    class ExtraCamera:
        def __init__(self, name="", camera_type="", extra_shots=None):
            self.name = name
            self.camera_type = camera_type
            self.extra_shots = extra_shots

    class Frames:
        def __init__(self, camera_is_enabled=False, position=Vector(), up=Vector(), forward=Vector(), fov=0.0, aperture=0.0, focal_length=0.0, depth_of_field=False, near_focal=0.0, 
                     far_focal=0.0, focal_depth=0.0, blur_amount=0.0):
            self.camera_is_enabled = camera_is_enabled
            self.position = position
            self.up = up
            self.forward = forward
            self.fov = fov
            self.aperture = aperture
            self.focal_length = focal_length
            self.depth_of_field = depth_of_field
            self.near_focal = near_focal
            self.far_focal = far_focal
            self.focal_depth = focal_depth
            self.blur_amount = blur_amount

    class AudioData:
        def __init__(self, filepath="", frame=0, name=""):
            self.filepath = filepath
            self.frame = frame
            self.name = name
