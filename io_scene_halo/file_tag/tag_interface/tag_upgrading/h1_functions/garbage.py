# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Steven Garcia
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

import os
import json

from mathutils import Vector
from enum import Flag, Enum, auto
from ....global_functions import tag_format, shader_processing
from ....file_tag.h2_20030504.file_object.format import upgrade_e3_object_flags
from ....file_tag.h2.file_garbage.format import GarbageAsset
from ....file_tag.h2_20030504.file_object.upgrade_json import generate_attachments, generate_widgets, generate_change_colors, _20030504_ObjectFunctionsEnum

def upgrade_garbage(H2_ASSET, patch_txt_path, report):
    dump_dic = json.load(H2_ASSET)

    TAG = tag_format.TagAsset()
    GARBAGE = GarbageAsset()
    TAG.upgrade_patches = tag_format.get_patch_set(patch_txt_path)

    GARBAGE.header = TAG.Header()
    GARBAGE.header.unk1 = 0
    GARBAGE.header.flags = 0
    GARBAGE.header.type = 0
    GARBAGE.header.name = ""
    GARBAGE.header.tag_group = "garb"
    GARBAGE.header.checksum = 0
    GARBAGE.header.data_offset = 64
    GARBAGE.header.data_length = 0
    GARBAGE.header.unk2 = 0
    GARBAGE.header.version = 1
    GARBAGE.header.destination = 0
    GARBAGE.header.plugin_handle = -1
    GARBAGE.header.engine_tag = "BLM!"

    GARBAGE.ai_properties = []
    GARBAGE.functions = []
    GARBAGE.attachments = []
    GARBAGE.widgets = []
    GARBAGE.old_functions = []
    GARBAGE.change_colors = []
    GARBAGE.predicted_resources = []
    GARBAGE.predicted_bitmaps = []

    detonation_delay = dump_dic['Data']['Detonation Delay']

    function_keywords = [("Object", _20030504_ObjectFunctionsEnum)]

    GARBAGE.body_header = TAG.TagBlockHeader("tbfd", 0, 1, 580)
    GARBAGE.object_flags = upgrade_e3_object_flags(dump_dic['Data']['Flags'])
    GARBAGE.bounding_radius = dump_dic['Data']['Bounding Radius']
    GARBAGE.bounding_offset = dump_dic['Data']['Bounding Offset']
    GARBAGE.acceleration_scale = dump_dic['Data']['Acceleration Scale']
    GARBAGE.lightmap_shadow_mode = 0
    GARBAGE.sweetner_size = 0
    GARBAGE.dynamic_light_sphere_radius = 0.0
    GARBAGE.dynamic_light_sphere_offset = Vector()
    GARBAGE.default_model_variant = dump_dic['Data']['Default Model Variant']
    GARBAGE.default_model_variant_length = len(dump_dic['Data']['Default Model Variant'])
    GARBAGE.model = TAG.TagRef().convert_from_json(dump_dic['Data']['Model'])
    GARBAGE.crate_object = TAG.TagRef()
    GARBAGE.modifier_shader = TAG.TagRef()
    GARBAGE.creation_effect = TAG.TagRef()
    GARBAGE.material_effects = TAG.TagRef()
    GARBAGE.ai_properties_tag_block = TAG.TagBlock()
    GARBAGE.functions_tag_block = TAG.TagBlock()
    GARBAGE.apply_collision_damage_scale = 0.0
    GARBAGE.min_game_acc = 0.0
    GARBAGE.max_game_acc = 0.0
    GARBAGE.min_game_scale = 0.0
    GARBAGE.max_game_scale = 0.0
    GARBAGE.min_abs_acc = 0.0
    GARBAGE.max_abs_acc = 0.0
    GARBAGE.min_abs_scale = 0.0
    GARBAGE.max_abs_scale = 0.0
    GARBAGE.hud_text_message_index = dump_dic['Data']['Hud Text Message Index']
    GARBAGE.attachments_tag_block = generate_attachments(dump_dic, TAG, GARBAGE, function_keywords)
    GARBAGE.widgets_tag_block = generate_widgets(dump_dic, TAG, GARBAGE)
    GARBAGE.old_functions_tag_block = TAG.TagBlock()
    GARBAGE.change_colors_tag_block = generate_change_colors(dump_dic, TAG, GARBAGE, function_keywords)
    GARBAGE.predicted_resources_tag_block = TAG.TagBlock()
    GARBAGE.item_flags = dump_dic['Data']['Item Flags']
    GARBAGE.old_message_index = dump_dic['Data']['Message Index']
    GARBAGE.sort_order = dump_dic['Data']['Sort Order']
    GARBAGE.multiplayer_on_ground_scale = dump_dic['Data']['Scale']
    GARBAGE.campaign_on_ground_scale = dump_dic['Data']['Scale']
    GARBAGE.pickup_message = ""
    GARBAGE.pickup_message_length = 0
    GARBAGE.swap_message = ""
    GARBAGE.swap_message_length = 0
    GARBAGE.pickup_or_dual_msg = ""
    GARBAGE.pickup_or_dual_msg_length = 0
    GARBAGE.swap_or_dual_msg = ""
    GARBAGE.swap_or_dual_msg_length = 0
    GARBAGE.dual_only_msg = ""
    GARBAGE.dual_only_msg_length = 0
    GARBAGE.picked_up_msg = ""
    GARBAGE.picked_up_msg_length = 0
    GARBAGE.singluar_quantity_msg = ""
    GARBAGE.singluar_quantity_msg_length = 0
    GARBAGE.plural_quantity_msg = ""
    GARBAGE.plural_quantity_msg_length = 0
    GARBAGE.switch_to_msg = ""
    GARBAGE.switch_to_msg_length = 0
    GARBAGE.switch_to_from_ai_msg = ""
    GARBAGE.switch_to_from_ai_msg_length = 0
    GARBAGE.unused = TAG.TagRef().convert_from_json(dump_dic['Data']['Material Effects'])
    GARBAGE.collision_sound = TAG.TagRef().convert_from_json(dump_dic['Data']['Collision Sound'])
    GARBAGE.predicted_bitmaps_tag_block = TAG.TagBlock()
    GARBAGE.detonation_damage_effect = TAG.TagRef()
    GARBAGE.detonation_delay = (detonation_delay["Min"], detonation_delay["Max"])
    GARBAGE.detonating_effect = TAG.TagRef().convert_from_json(dump_dic['Data']['Detonating Effect'])
    GARBAGE.detonation_effect = TAG.TagRef().convert_from_json(dump_dic['Data']['Detonation Effect'])

    return GARBAGE
