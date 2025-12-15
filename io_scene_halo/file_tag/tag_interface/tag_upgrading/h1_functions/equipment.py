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
from ....file_tag.h2.file_equipment.format import EquipmentAsset
from ....file_tag.h2_20030504.file_object.upgrade_json import generate_attachments, generate_widgets, generate_change_colors, _20030504_ObjectFunctionsEnum

def upgrade_equipment(H2_ASSET, patch_txt_path, report):
    dump_dic = json.load(H2_ASSET)

    TAG = tag_format.TagAsset()
    EQUIPMENT = EquipmentAsset()
    TAG.upgrade_patches = tag_format.get_patch_set(patch_txt_path)

    EQUIPMENT.header = TAG.Header()
    EQUIPMENT.header.unk1 = 0
    EQUIPMENT.header.flags = 0
    EQUIPMENT.header.type = 0
    EQUIPMENT.header.name = ""
    EQUIPMENT.header.tag_group = "eqip"
    EQUIPMENT.header.checksum = 0
    EQUIPMENT.header.data_offset = 64
    EQUIPMENT.header.data_length = 0
    EQUIPMENT.header.unk2 = 0
    EQUIPMENT.header.version = 2
    EQUIPMENT.header.destination = 0
    EQUIPMENT.header.plugin_handle = -1
    EQUIPMENT.header.engine_tag = "BLM!"

    EQUIPMENT.ai_properties = []
    EQUIPMENT.functions = []
    EQUIPMENT.attachments = []
    EQUIPMENT.widgets = []
    EQUIPMENT.old_functions = []
    EQUIPMENT.change_colors = []
    EQUIPMENT.predicted_resources = []
    EQUIPMENT.predicted_bitmaps = []

    detonation_delay = dump_dic['Data']['Detonation Delay']

    function_keywords = [("Object", _20030504_ObjectFunctionsEnum)]

    EQUIPMENT.body_header = TAG.TagBlockHeader("tbfd", 0, 1, 436)
    EQUIPMENT.object_flags = upgrade_e3_object_flags(dump_dic['Data']['Flags'])
    EQUIPMENT.bounding_radius = dump_dic['Data']['Bounding Radius']
    EQUIPMENT.bounding_offset = dump_dic['Data']['Bounding Offset']
    EQUIPMENT.acceleration_scale = dump_dic['Data']['Acceleration Scale']
    EQUIPMENT.lightmap_shadow_mode = 0
    EQUIPMENT.sweetner_size = 0
    EQUIPMENT.dynamic_light_sphere_radius = 0.0
    EQUIPMENT.dynamic_light_sphere_offset = Vector()
    EQUIPMENT.default_model_variant = dump_dic['Data']['Default Model Variant']
    EQUIPMENT.default_model_variant_length = len(dump_dic['Data']['Default Model Variant'])
    EQUIPMENT.model = TAG.TagRef().convert_from_json(dump_dic['Data']['Model'])
    EQUIPMENT.crate_object = TAG.TagRef()
    EQUIPMENT.modifier_shader = TAG.TagRef()
    EQUIPMENT.creation_effect = TAG.TagRef()
    EQUIPMENT.material_effects = TAG.TagRef()
    EQUIPMENT.ai_properties_tag_block = TAG.TagBlock()
    EQUIPMENT.functions_tag_block = TAG.TagBlock()
    EQUIPMENT.apply_collision_damage_scale = 0.0
    EQUIPMENT.min_game_acc = 0.0
    EQUIPMENT.max_game_acc = 0.0
    EQUIPMENT.min_game_scale = 0.0
    EQUIPMENT.max_game_scale = 0.0
    EQUIPMENT.min_abs_acc = 0.0
    EQUIPMENT.max_abs_acc = 0.0
    EQUIPMENT.min_abs_scale = 0.0
    EQUIPMENT.max_abs_scale = 0.0
    EQUIPMENT.hud_text_message_index = dump_dic['Data']['Hud Text Message Index']
    EQUIPMENT.attachments_tag_block = generate_attachments(dump_dic, TAG, EQUIPMENT, function_keywords)
    EQUIPMENT.widgets_tag_block = generate_widgets(dump_dic, TAG, EQUIPMENT)
    EQUIPMENT.old_functions_tag_block = TAG.TagBlock()
    EQUIPMENT.change_colors_tag_block = generate_change_colors(dump_dic, TAG, EQUIPMENT, function_keywords)
    EQUIPMENT.predicted_resources_tag_block = TAG.TagBlock()
    EQUIPMENT.item_flags = dump_dic['Data']['Item Flags']
    EQUIPMENT.old_message_index = dump_dic['Data']['Message Index']
    EQUIPMENT.sort_order = dump_dic['Data']['Sort Order']
    EQUIPMENT.multiplayer_on_ground_scale = dump_dic['Data']['Scale']
    EQUIPMENT.campaign_on_ground_scale = dump_dic['Data']['Scale']
    EQUIPMENT.pickup_message = ""
    EQUIPMENT.pickup_message_length = 0
    EQUIPMENT.swap_message = ""
    EQUIPMENT.swap_message_length = 0
    EQUIPMENT.pickup_or_dual_msg = ""
    EQUIPMENT.pickup_or_dual_msg_length = 0
    EQUIPMENT.swap_or_dual_msg = ""
    EQUIPMENT.swap_or_dual_msg_length = 0
    EQUIPMENT.dual_only_msg = ""
    EQUIPMENT.dual_only_msg_length = 0
    EQUIPMENT.picked_up_msg = ""
    EQUIPMENT.picked_up_msg_length = 0
    EQUIPMENT.singluar_quantity_msg = ""
    EQUIPMENT.singluar_quantity_msg_length = 0
    EQUIPMENT.plural_quantity_msg = ""
    EQUIPMENT.plural_quantity_msg_length = 0
    EQUIPMENT.switch_to_msg = ""
    EQUIPMENT.switch_to_msg_length = 0
    EQUIPMENT.switch_to_from_ai_msg = ""
    EQUIPMENT.switch_to_from_ai_msg_length = 0
    EQUIPMENT.unused = TAG.TagRef().convert_from_json(dump_dic['Data']['Material Effects'])
    EQUIPMENT.collision_sound = TAG.TagRef().convert_from_json(dump_dic['Data']['Collision Sound'])
    EQUIPMENT.predicted_bitmaps_tag_block = TAG.TagBlock()
    EQUIPMENT.detonation_damage_effect = TAG.TagRef()
    EQUIPMENT.detonation_delay = (detonation_delay["Min"], detonation_delay["Max"])
    EQUIPMENT.detonating_effect = TAG.TagRef().convert_from_json(dump_dic['Data']['Detonating Effect'])
    EQUIPMENT.detonation_effect = TAG.TagRef().convert_from_json(dump_dic['Data']['Detonation Effect'])
    EQUIPMENT.powerup_type = dump_dic['Data']['Powerup Type']['Value']
    EQUIPMENT.grenade_type = dump_dic['Data']['Grenade Type']['Value']
    EQUIPMENT.powerup_time = dump_dic['Data']['Powerup Time']
    EQUIPMENT.pickup_sound = TAG.TagRef().convert_from_json(dump_dic['Data']['Pickup Sound'])

    return EQUIPMENT
