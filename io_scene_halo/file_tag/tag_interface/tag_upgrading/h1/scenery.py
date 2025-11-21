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
from ....file_tag.h2.file_scenery.format import SceneryAsset, PathfindingPolicyEnum
from ....file_tag.h2_20030504.file_object.upgrade_json import generate_attachments, generate_widgets, generate_change_colors, _20030504_ObjectFunctionsEnum

class _20030504_PathfindingTypeEnum(Enum):
    pathfinding_off = 0
    pathfinding_on = auto()

def convert_pathfinding_policy(pathfinding_index):
    h2_pathfinding_index = 0
    h1_pathfinding = _20030504_PathfindingTypeEnum(pathfinding_index)
    if h1_pathfinding == _20030504_PathfindingTypeEnum.pathfinding_off:
        h2_pathfinding_index = PathfindingPolicyEnum.pathfinding_none.value
    elif h1_pathfinding == _20030504_PathfindingTypeEnum.pathfinding_on:
        h2_pathfinding_index = PathfindingPolicyEnum.pathfinding_static.value
    return h2_pathfinding_index

def upgrade_scenery(H2_ASSET, patch_txt_path, report):
    dump_dic = json.load(H2_ASSET)

    TAG = tag_format.TagAsset()
    SCENERY = SceneryAsset()
    TAG.upgrade_patches = tag_format.get_patch_set(patch_txt_path)

    SCENERY.header = TAG.Header()
    SCENERY.header.unk1 = 0
    SCENERY.header.flags = 0
    SCENERY.header.type = 0
    SCENERY.header.name = ""
    SCENERY.header.tag_group = "scen"
    SCENERY.header.checksum = 0
    SCENERY.header.data_offset = 64
    SCENERY.header.data_length = 0
    SCENERY.header.unk2 = 0
    SCENERY.header.version = 1
    SCENERY.header.destination = 0
    SCENERY.header.plugin_handle = -1
    SCENERY.header.engine_tag = "BLM!"

    SCENERY.ai_properties = []
    SCENERY.functions = []
    SCENERY.attachments = []
    SCENERY.widgets = []
    SCENERY.old_functions = []
    SCENERY.change_colors = []
    SCENERY.predicted_resources = []

    function_keywords = [("Object", _20030504_ObjectFunctionsEnum)]

    SCENERY.body_header = TAG.TagBlockHeader("tbfd", 2, 1, 264)
    SCENERY.object_flags = upgrade_e3_object_flags(dump_dic['Data']['Flags'])
    SCENERY.bounding_radius = dump_dic['Data']['Bounding Radius']
    SCENERY.bounding_offset = dump_dic['Data']['Bounding Offset']
    SCENERY.acceleration_scale = dump_dic['Data']['Acceleration Scale']
    SCENERY.lightmap_shadow_mode = 0
    SCENERY.sweetner_size = 0
    SCENERY.dynamic_light_sphere_radius = 0.0
    SCENERY.dynamic_light_sphere_offset = Vector()
    SCENERY.default_model_variant = dump_dic['Data']['Default Model Variant']
    SCENERY.default_model_variant_length = len(dump_dic['Data']['Default Model Variant'])
    SCENERY.model = TAG.TagRef().convert_from_json(dump_dic['Data']['Model'])
    SCENERY.crate_object = TAG.TagRef()
    SCENERY.modifier_shader = TAG.TagRef()
    SCENERY.creation_effect = TAG.TagRef()
    SCENERY.material_effects = TAG.TagRef()
    SCENERY.ai_properties_tag_block = TAG.TagBlock()
    SCENERY.functions_tag_block = TAG.TagBlock()
    SCENERY.apply_collision_damage_scale = 0.0
    SCENERY.min_game_acc = 0.0
    SCENERY.max_game_acc = 0.0
    SCENERY.min_game_scale = 0.0
    SCENERY.max_game_scale = 0.0
    SCENERY.min_abs_acc = 0.0
    SCENERY.max_abs_acc = 0.0
    SCENERY.min_abs_scale = 0.0
    SCENERY.max_abs_scale = 0.0
    SCENERY.hud_text_message_index = dump_dic['Data']['Hud Text Message Index']
    SCENERY.attachments_tag_block = generate_attachments(dump_dic, TAG, SCENERY, function_keywords)
    SCENERY.widgets_tag_block = generate_widgets(dump_dic, TAG, SCENERY)
    SCENERY.old_functions_tag_block = TAG.TagBlock()
    SCENERY.change_colors_tag_block = generate_change_colors(dump_dic, TAG, SCENERY, function_keywords)
    SCENERY.predicted_resources_tag_block = TAG.TagBlock()
    SCENERY.pathfinding_policy = convert_pathfinding_policy(dump_dic['Data']['Pathfinding Policy']["Value"])
    SCENERY.scenery_flags = dump_dic['Data']['Flags']
    SCENERY.lightmapping_policy = 0

    return SCENERY
