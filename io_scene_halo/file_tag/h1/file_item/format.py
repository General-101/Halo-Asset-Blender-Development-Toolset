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
from ..file_object.format import ObjectAsset

class ItemFlags(Flag):
    always_maintains_z_up = auto()
    destroyed_by_explosions = auto()
    unaffected_by_gravity = auto()

class ItemFunctionEnum(Enum):
    none = 0

class ItemAsset(ObjectAsset):
    def __init__(self, item_flags=0, message_index=0, sort_order=0, scale=0.0, hud_message_value_scale=0.0, item_a_in=0, item_b_in=0, item_c_in=0, item_d_in=0,
                 material_effects=None, collision_sound=None, detonation_delay=(0.0, 0.0), detonating_effect=None, detonation_effect=None):
        super().__init__()
        self.header = None
        self.item_flags = item_flags
        self.message_index = message_index
        self.sort_order = sort_order
        self.scale = scale
        self.hud_message_value_scale = hud_message_value_scale
        self.item_a_in = item_a_in
        self.item_b_in = item_b_in
        self.item_c_in = item_c_in
        self.item_d_in = item_d_in
        self.material_effects = material_effects
        self.collision_sound = collision_sound
        self.detonation_delay = detonation_delay
        self.detonating_effect = detonating_effect
        self.detonation_effect = detonation_effect
