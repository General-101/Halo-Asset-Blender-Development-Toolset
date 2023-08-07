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

from enum import Flag, auto
from mathutils import Vector, Quaternion
from ..global_functions import global_functions

class JMAAsset(global_functions.HaloAsset):
    def __init__(self, filepath=None):
        """
        Reads data to sort in our JMA class
        self.version - JMA version with a range of 16390 - 16395
        self.frame_rate - Frame rate for animation. Importer does not use this value and is only for debug.
        self.frame_count - Frame count for the animation.
        self.actor_names - A hardcoded list for the actor in a scene. This is an unused feature and should be left as is.
        self.broken_skeleton - Bool property to store is the parser has determined the node graph to be incorrect.
        self.node_checksum - checksum value or -1
        self.node_count - included for 16390
        self.biped_controller_frame_type - BipedControllerFrameType enum
        self.nodes - included for 16392+
        self.transforms - 2D array of transforms [frame_idx][node_idx]
        self.biped_controller_transforms - included for 16395
        """
        if filepath:
            super().__init__(filepath)

        self.version = 0
        self.frame_rate = 30
        self.frame_count = 0
        self.actor_names = ['unnamedActor'] # Actor values are hardcoded and unused as they are in the official exporter. Leave as is.
        self.broken_skeleton = False
        self.node_checksum = -1
        self.node_count = 0
        self.biped_controller_frame_type = JMAAsset.BipedControllerFrameType.DISABLE
        self.nodes = []
        self.transforms = []
        self.biped_controller_transforms = []

    class Transform:
        def __init__(self, translation=Vector(), rotation=Quaternion(), scale=1.0):
            self.translation = translation
            self.rotation = rotation
            self.scale = scale

    class Node:
        def __init__(self, name="", parent=-1, child=-1, sibling=-1, visited=False):
            self.name = name
            self.parent = parent
            self.child = child
            self.sibling = sibling
            self.visited = visited

    class BipedControllerFrameType(Flag):
        DISABLE = 0
        DX = auto()
        DY = auto()
        DZ = auto()
        DYAW = auto()

        JMA = DX | DY
        JMT = DX | DY | DYAW
        JMRX = DX | DY | DZ | DYAW

    def are_quaternions_inverted(self):
        return self.version < 16394

    def next_transform(self):
        translation = self.next_vector()
        rotation = self.next_quaternion()
        scale = float(self.next())

        return JMAAsset.Transform(translation, rotation, scale)

    def next_transform_prerelease(self):
        rotation = self.next_quaternion()
        translation = self.next_vector()
        scale = 1.0

        return JMAAsset.Transform(translation, rotation, scale)
