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

class PathfindingPolicyEnum(Enum):
    pathfinding_cut_out = 0
    pathfinding_static = auto()
    pathfinding_dynamic = auto()
    pathfinding_none = auto()

class SceneryFlags(Flag):
    physically_stimulates = auto()

class LightmappingPolicyEnum(Enum):
    per_vertex = 0
    per_pixel = auto()
    dynamic = auto()

class SceneryAsset(ObjectAsset):
    def __init__(self, pathfinding_policy=0, scenery_flags=0, lightmapping_policy=0):
        super().__init__()
        self.pathfinding_policy = pathfinding_policy
        self.scenery_flags = scenery_flags
        self.lightmapping_policy = lightmapping_policy
