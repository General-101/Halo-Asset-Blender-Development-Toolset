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

class LayerEnum(Enum):
    lit_alpha_blend_prelight = 0
    lit_alpha_blend = auto()
    double_multiply = auto()
    multiply = auto()
    max = auto()
    add = auto()
    error = auto()

class DecalAsset():
    def __init__(self, header=None, body_header=None, flags=0, decal_type=0, layer=3, max_overlapping_count=8, next_decal_in_chain=None, radius=(0.1, 0.1), 
                 radius_overlap_rejection=0.75, color_lower_bounds=(1.0, 1.0, 1.0, 1.0), color_upper_bounds=(1.0, 1.0, 1.0, 1.0), lifetime=(10.0, 10.0), 
                 decay_time=(1.0, 1.0), bitmap=None, maximum_sprite_extent=0.0):
        self.header = header
        self.body_header = body_header
        self.flags = flags
        self.decal_type = decal_type
        self.layer = layer
        self.max_overlapping_count = max_overlapping_count
        self.next_decal_in_chain = next_decal_in_chain
        self.radius = radius
        self.radius_overlap_rejection = radius_overlap_rejection
        self.color_lower_bounds = color_lower_bounds
        self.color_upper_bounds = color_upper_bounds
        self.lifetime = lifetime
        self.decay_time = decay_time
        self.bitmap = bitmap
        self.maximum_sprite_extent = maximum_sprite_extent
