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

class SceneTypeEnum(Enum):
    main = 0
    segment = auto()

class UbercamObjectTypeEnum(Enum):
    unit = 0
    scenery = auto()
    effect_scenery = auto()

class QUAAsset(global_functions.HaloAsset):
    def __init__(self, filepath=None):
        if filepath:
            super().__init__(filepath)

        self.version = 0
        self.scene_type = ""
        self.scene_version = 0
        self.scene_name = ""
        self.units = None
        self.scenery = None
        self.effects_scenery = None
        self.objects = None
        self.shots = None
        self.extra_cameras = None

    class Object:
        def __init__(self, export_name="", animation_id="", animation_path="", object_path="", bits=None):
            self.export_name = export_name
            self.animation_id = animation_id
            self.animation_path = animation_path
            self.object_path = object_path
            self.bits = bits

    class Shots:
        def __init__(self, frames=None, audio_data_version=0, audio_data=None, custom_script_data_version=0, custom_script_data=None, effect_data_version=0, effect_data=None):
            self.frames = frames
            self.audio_data_version = audio_data_version
            self.audio_data = audio_data
            self.custom_script_data_version = custom_script_data_version
            self.custom_script_data = custom_script_data
            self.effect_data_version = effect_data_version
            self.effect_data = effect_data

    class ExtraCamera:
        def __init__(self, name="", camera_type="", extra_shots=None):
            self.name = name
            self.camera_type = camera_type
            self.extra_shots = extra_shots

    class Frames:
        def __init__(self, camera_is_enabled=False, position=Vector(), up=Vector(), forward=Vector(), fov=0.0, aperture=0.0, focal_length=0.0, depth_of_field=False, near_focal=0.0, 
                     far_focal=0.0, focal_depth=0.0, blur_amount=0.0, near_focal_depth=0.0, far_focal_depth=0.0, near_blur_amount=0.0, far_blur_amount=0.0):
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
            self.near_focal_depth = near_focal_depth
            self.far_focal_depth = far_focal_depth
            self.near_blur_amount = near_blur_amount
            self.far_blur_amount = far_blur_amount

    class AudioData:
        def __init__(self, sound_tag="", female_sound_tag="", audio_filename="", female_audio_filename="", frame=0, character="", dialog_color=""):
            self.sound_tag = sound_tag
            self.female_sound_tag = female_sound_tag
            self.audio_filename = audio_filename
            self.female_audio_filename = female_audio_filename
            self.frame = frame
            self.character = character
            self.dialog_color = dialog_color

    class CustomScriptData:
        def __init__(self, node_id=0, sequence_id=0, script="", frame=0):
            self.node_id = node_id
            self.sequence_id = sequence_id
            self.script = script
            self.frame = frame

    class EffectData:
        def __init__(self, node_id=0, sequence_id=0, effect="", marker_name="", marker_parent="", frame=0, effect_state=0, size_scale=0.0, function_a="", function_b="", 
                     looping=0):
            self.node_id = node_id
            self.sequence_id = sequence_id
            self.effect = effect
            self.marker_name = marker_name
            self.marker_parent = marker_parent
            self.frame = frame
            self.effect_state = effect_state
            self.size_scale = size_scale
            self.function_a = function_a
            self.function_b = function_b
            self.looping = looping
