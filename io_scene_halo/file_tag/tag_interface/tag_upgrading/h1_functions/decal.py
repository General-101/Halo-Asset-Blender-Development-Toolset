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

import json

from enum import Flag, Enum, auto
from ....global_functions import tag_format, shader_processing
from ....file_tag.h2.file_decal.format import DecalAsset, LayerEnum

class _20030504_FramebufferBlendFunctionEnum(Enum):
    alpha_blend = 0
    multiply = auto()
    double_multiply = auto()
    add = auto()
    subtract = auto()
    component_min = auto()
    component_max = auto()
    alpha_multiply_add = auto()

def convert_legacy_layer(blend_index):
    h2_blend_index = 0
    h1_blend = _20030504_FramebufferBlendFunctionEnum(blend_index)
    if h1_blend == _20030504_FramebufferBlendFunctionEnum.alpha_blend:
        h2_blend_index = LayerEnum.lit_alpha_blend.value
    elif h1_blend == _20030504_FramebufferBlendFunctionEnum.multiply:
        h2_blend_index = LayerEnum.multiply.value
    elif h1_blend == _20030504_FramebufferBlendFunctionEnum.double_multiply:
        h2_blend_index = LayerEnum.double_multiply.value
    elif h1_blend == _20030504_FramebufferBlendFunctionEnum.add:
        h2_blend_index = LayerEnum.add.value
    elif h1_blend == _20030504_FramebufferBlendFunctionEnum.subtract:
        h2_blend_index = LayerEnum.add.value
    elif h1_blend == _20030504_FramebufferBlendFunctionEnum.component_min:
        h2_blend_index = LayerEnum.max.value
    elif h1_blend == _20030504_FramebufferBlendFunctionEnum.component_max:
        h2_blend_index = LayerEnum.max.value
    elif h1_blend == _20030504_FramebufferBlendFunctionEnum.alpha_multiply_add:
        h2_blend_index = LayerEnum.multiply.value

    return h2_blend_index

def upgrade_decal(H2_ASSET, patch_txt_path, report):
    dump_dic = json.load(H2_ASSET)

    TAG = tag_format.TagAsset()
    DECAL = DecalAsset()
    TAG.upgrade_patches = tag_format.get_patch_set(patch_txt_path)

    DECAL.header = TAG.Header()
    DECAL.header.unk1 = 0
    DECAL.header.flags = 0
    DECAL.header.type = 0
    DECAL.header.name = ""
    DECAL.header.tag_group = "deca"
    DECAL.header.checksum = 0
    DECAL.header.data_offset = 64
    DECAL.header.data_length = 0
    DECAL.header.unk2 = 0
    DECAL.header.version = 1
    DECAL.header.destination = 0
    DECAL.header.plugin_handle = -1
    DECAL.header.engine_tag = "BLM!"

    radius = dump_dic['Data']['Radius']
    lifetime = dump_dic['Data']['Lifetime']
    decay_time = dump_dic['Data']['Decay Time']

    DECAL.body_header = TAG.TagBlockHeader("tbfd", 0, 1, 188)
    DECAL.flags = dump_dic['Data']['Flags']
    DECAL.decal_type = dump_dic['Data']['Type']['Value']
    DECAL.layer = convert_legacy_layer(dump_dic['Data']['Framebuffer Blend Function']['Value'])
    DECAL.max_overlapping_count = 8
    DECAL.next_decal_in_chain = TAG.TagRef().convert_from_json(dump_dic['Data']['Next Decal In Chain'])
    DECAL.radius = (radius["Min"], radius["Max"])
    DECAL.radius_overlap_rejection = 0.75
    DECAL.color_lower_bounds = shader_processing.get_rgb_percentage(dump_dic['Data']["Color Lower Bounds"])
    DECAL.color_upper_bounds = shader_processing.get_rgb_percentage(dump_dic['Data']["Color Upper Bounds"])
    DECAL.lifetime = (lifetime["Min"], lifetime["Max"])
    DECAL.decay_time = (decay_time["Min"], decay_time["Max"])
    DECAL.bitmap = TAG.TagRef().convert_from_json(dump_dic['Data']['Map'])
    DECAL.maximum_sprite_extent = dump_dic['Data']['Maximum Sprite Extent']

    return DECAL
