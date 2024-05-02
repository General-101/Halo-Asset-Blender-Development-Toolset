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

class ItemFlags(Flag):
    always_maintains_z_up = auto()
    destroyed_by_explosions = auto()
    unaffected_by_gravity = auto()

class ItemAsset(ObjectAsset):
    def __init__(self):
        super().__init__()
        self.header = None
        self.item_body_header = None
        self.item_body = None
        self.predicted_bitmaps_header = None
        self.predicted_bitmaps = None

    class ItemBody(ObjectAsset.ObjectBody):
        def __init__(self, item_flags=0, old_message_index=0, sort_order=0, multiplayer_on_ground_scale=0.0, campaign_on_ground_scale=0.0, pickup_message="",
                     pickup_message_length=0, swap_message="", swap_message_length=0, pickup_or_dual_msg="", pickup_or_dual_msg_length=0, swap_or_dual_msg="",
                     swap_or_dual_msg_length=0, dual_only_msg="", dual_only_msg_length=0, picked_up_msg="", picked_up_msg_length=0, singluar_quantity_msg="",
                     singluar_quantity_msg_length=0, plural_quantity_msg="", plural_quantity_msg_length=0, switch_to_msg="", switch_to_msg_length=0, switch_to_from_ai_msg="",
                     switch_to_from_ai_msg_length=0, unused=None, collision_sound=None, predicted_bitmaps_tag_block=None, detonation_damage_effect=None, detonation_delay=(0.0, 0.0),
                     detonating_effect=None, detonation_effect=None):
            super().__init__()
            self.item_flags = item_flags
            self.old_message_index = old_message_index
            self.sort_order = sort_order
            self.multiplayer_on_ground_scale = multiplayer_on_ground_scale
            self.campaign_on_ground_scale = campaign_on_ground_scale
            self.pickup_message = pickup_message
            self.pickup_message_length = pickup_message_length
            self.swap_message = swap_message
            self.swap_message_length = swap_message_length
            self.pickup_or_dual_msg = pickup_or_dual_msg
            self.pickup_or_dual_msg_length = pickup_or_dual_msg_length
            self.swap_or_dual_msg = swap_or_dual_msg
            self.swap_or_dual_msg_length = swap_or_dual_msg_length
            self.dual_only_msg = dual_only_msg
            self.dual_only_msg_length = dual_only_msg_length
            self.picked_up_msg = picked_up_msg
            self.picked_up_msg_length = picked_up_msg_length
            self.singluar_quantity_msg = singluar_quantity_msg
            self.singluar_quantity_msg_length = singluar_quantity_msg_length
            self.plural_quantity_msg = plural_quantity_msg
            self.plural_quantity_msg_length = plural_quantity_msg_length
            self.switch_to_msg = switch_to_msg
            self.switch_to_msg_length = switch_to_msg_length
            self.switch_to_from_ai_msg = switch_to_from_ai_msg
            self.switch_to_from_ai_msg_length = switch_to_from_ai_msg_length
            self.unused = unused
            self.collision_sound = collision_sound
            self.predicted_bitmaps_tag_block = predicted_bitmaps_tag_block
            self.detonation_damage_effect = detonation_damage_effect
            self.detonation_delay = detonation_delay
            self.detonating_effect = detonating_effect
            self.detonation_effect = detonation_effect
