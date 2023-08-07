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

import bpy

from ..global_functions import global_functions

class QUAAsset(global_functions.HaloAsset):
    class Scene:
        def __init__(self, version, name):
            self.version = version
            self.name = name

    class Units:
        def __init__(self, name, path, bit_0, bit_1, bit_2):
            self.name = name
            self.path = path
            self.bit_0 = bit_0
            self.bit_1 = bit_1
            self.bit_2 = bit_2

    class Scenery:
        def __init__(self, name, path, bit_0, bit_1, bit_2):
            self.name = name
            self.path = path
            self.bit_0 = bit_0
            self.bit_1 = bit_1
            self.bit_2 = bit_2

    class EffectsScenery:
        def __init__(self, name, path, bit_0, bit_1, bit_2):
            self.name = name
            self.path = path
            self.bit_0 = bit_0
            self.bit_1 = bit_1
            self.bit_2 = bit_2

    class Shots:
        def __init__(self, frames, audio_data):
            self.frames = frames
            self.audio_data = audio_data

    class ExtraShots:
        def __init__(self, frames, audio_data):
            self.frames = frames
            self.audio_data = audio_data

    class Frames:
        def __init__(self, position, up, forward, fov, aperture, focal_length, depth_of_field, near_focal, far_focal, focal_depth, blur_amount):
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
        def __init__(self, filepath, frame, name):
            self.filepath = filepath
            self.frame = frame
            self.name = name

    def __init__(self, context):
        self.version = 5
        self.name = "placeholder"
        self.shots = []
        self.units = []
        self.scenery = []
        self.effects_scenery = []
        self.extra_cameras = []
        self.extra_shots = []


        if self.left() != 0: # is something wrong with the parser?
            raise RuntimeError("%s elements left after parse end" % self.left())

def load_file(context, filepath, report):
    ass_file = QUAAsset(filepath)

    report({'INFO'}, "Import completed successfully")
    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.import_scene.qua()
