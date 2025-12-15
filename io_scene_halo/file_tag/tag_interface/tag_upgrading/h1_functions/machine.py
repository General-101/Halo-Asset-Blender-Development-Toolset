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
from ....file_tag.h2.file_machine.format import MachineAsset
from ....file_tag.h2_20030504.file_object.upgrade_json import generate_attachments, generate_widgets, generate_change_colors, _20030504_ObjectFunctionsEnum

class _20030504_DeviceFunctionsEnum(Enum):
    none = 0
    power = auto()
    change_in_power = auto()
    position = auto()
    change_in_position = auto()
    locked = auto()
    delay = auto()

def upgrade_machine(H2_ASSET, patch_txt_path, report):
    dump_dic = json.load(H2_ASSET)

    TAG = tag_format.TagAsset()
    MACHINE = MachineAsset()
    TAG.upgrade_patches = tag_format.get_patch_set(patch_txt_path)

    MACHINE.header = TAG.Header()
    MACHINE.header.unk1 = 0
    MACHINE.header.flags = 0
    MACHINE.header.type = 0
    MACHINE.header.name = ""
    MACHINE.header.tag_group = "mach"
    MACHINE.header.checksum = 0
    MACHINE.header.data_offset = 64
    MACHINE.header.data_length = 0
    MACHINE.header.unk2 = 0
    MACHINE.header.version = 1
    MACHINE.header.destination = 0
    MACHINE.header.plugin_handle = -1
    MACHINE.header.engine_tag = "BLM!"

    MACHINE.ai_properties = []
    MACHINE.functions = []
    MACHINE.attachments = []
    MACHINE.widgets = []
    MACHINE.old_functions = []
    MACHINE.change_colors = []
    MACHINE.predicted_resources = []

    function_keywords = [("Object", _20030504_ObjectFunctionsEnum), ("Device", _20030504_DeviceFunctionsEnum)]

    MACHINE.body_header = TAG.TagBlockHeader("tbfd", 0, 1, 432)
    MACHINE.object_flags = upgrade_e3_object_flags(dump_dic['Data']['Flags'])
    MACHINE.bounding_radius = dump_dic['Data']['Bounding Radius']
    MACHINE.bounding_offset = dump_dic['Data']['Bounding Offset']
    MACHINE.acceleration_scale = dump_dic['Data']['Acceleration Scale']
    MACHINE.lightmap_shadow_mode = 0
    MACHINE.sweetner_size = 0
    MACHINE.dynamic_light_sphere_radius = 0.0
    MACHINE.dynamic_light_sphere_offset = Vector()
    MACHINE.default_model_variant = dump_dic['Data']['Default Model Variant']
    MACHINE.default_model_variant_length = len(dump_dic['Data']['Default Model Variant'])
    MACHINE.model = TAG.TagRef().convert_from_json(dump_dic['Data']['Model'])
    MACHINE.crate_object = TAG.TagRef()
    MACHINE.modifier_shader = TAG.TagRef()
    MACHINE.creation_effect = TAG.TagRef()
    MACHINE.material_effects = TAG.TagRef()
    MACHINE.ai_properties_tag_block = TAG.TagBlock()
    MACHINE.functions_tag_block = TAG.TagBlock()
    MACHINE.apply_collision_damage_scale = 0.0
    MACHINE.min_game_acc = 0.0
    MACHINE.max_game_acc = 0.0
    MACHINE.min_game_scale = 0.0
    MACHINE.max_game_scale = 0.0
    MACHINE.min_abs_acc = 0.0
    MACHINE.max_abs_acc = 0.0
    MACHINE.min_abs_scale = 0.0
    MACHINE.max_abs_scale = 0.0
    MACHINE.hud_text_message_index = dump_dic['Data']['Hud Text Message Index']
    MACHINE.attachments_tag_block = generate_attachments(dump_dic, TAG, MACHINE, function_keywords)
    MACHINE.widgets_tag_block = generate_widgets(dump_dic, TAG, MACHINE)
    MACHINE.old_functions_tag_block = TAG.TagBlock()
    MACHINE.change_colors_tag_block = generate_change_colors(dump_dic, TAG, MACHINE, function_keywords)
    MACHINE.predicted_resources_tag_block = TAG.TagBlock()
    MACHINE.device_flags = dump_dic['Data']['Device Flags']
    MACHINE.power_transition_time = dump_dic['Data']['Power Transition Time']
    MACHINE.power_acceleration_time = dump_dic['Data']['Power Acceleration Time']
    MACHINE.position_transition_time = dump_dic['Data']['Position Transition Time']
    MACHINE.position_acceleration_time = dump_dic['Data']['Position Acceleration Time']
    MACHINE.depowered_position_transition_time = dump_dic['Data']['Depowered Position Transition Time']
    MACHINE.depowered_position_acceleration_time = dump_dic['Data']['Depowered Position Acceleration Time']
    MACHINE.lightmap_flags = 0
    MACHINE.open_up = TAG.TagRef().convert_from_json(dump_dic['Data']['Open (Up)'])
    MACHINE.close_down = TAG.TagRef().convert_from_json(dump_dic['Data']['Close (Down)'])
    MACHINE.opened = TAG.TagRef().convert_from_json(dump_dic['Data']['Opened'])
    MACHINE.closed = TAG.TagRef().convert_from_json(dump_dic['Data']['Closed'])
    MACHINE.depowered = TAG.TagRef().convert_from_json(dump_dic['Data']['Depowered'])
    MACHINE.repowered = TAG.TagRef().convert_from_json(dump_dic['Data']['Repowered'])
    MACHINE.delay_time = dump_dic['Data']['Delay Time']
    MACHINE.delay_effect = TAG.TagRef().convert_from_json(dump_dic['Data']['Delay Effect'])
    MACHINE.automatic_activation_radius = dump_dic['Data']['Automatic Activation Radius']
    MACHINE.machine_type = dump_dic['Data']['Type']['Value']
    MACHINE.machine_flags = dump_dic['Data']['Machine Flags']
    MACHINE.door_open_time = dump_dic['Data']['Door Open Time']
    MACHINE.door_occlusion_time = (0.0, 0.0)
    MACHINE.collision_response = dump_dic['Data']['Collision Response']['Value']
    MACHINE.elevator_node = dump_dic['Data']['Elevator Node']
    MACHINE.pathfinding_policy = 0

    return MACHINE
