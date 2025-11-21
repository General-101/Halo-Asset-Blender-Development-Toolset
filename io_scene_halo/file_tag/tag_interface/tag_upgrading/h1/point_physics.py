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

from ....global_functions import tag_format, shader_processing
from ....file_tag.h2.file_point_physics.format import PointPhysicsAsset

def upgrade_point_physics(H2_ASSET, patch_txt_path, report):
    dump_dic = json.load(H2_ASSET)

    TAG = tag_format.TagAsset()
    POINTPHYSICS = PointPhysicsAsset()
    TAG.upgrade_patches = tag_format.get_patch_set(patch_txt_path)

    POINTPHYSICS.header = TAG.Header()
    POINTPHYSICS.header.unk1 = 0
    POINTPHYSICS.header.flags = 0
    POINTPHYSICS.header.type = 0
    POINTPHYSICS.header.name = ""
    POINTPHYSICS.header.tag_group = "pphy"
    POINTPHYSICS.header.checksum = 0
    POINTPHYSICS.header.data_offset = 64
    POINTPHYSICS.header.data_length = 0
    POINTPHYSICS.header.unk2 = 0
    POINTPHYSICS.header.version = 1
    POINTPHYSICS.header.destination = 0
    POINTPHYSICS.header.plugin_handle = -1
    POINTPHYSICS.header.engine_tag = "BLM!"

    POINTPHYSICS.body_header = TAG.TagBlockHeader("tbfd", 0, 1, 64)
    POINTPHYSICS.flags = dump_dic['Data']['Flags']
    POINTPHYSICS.density = dump_dic['Data']['Density']
    POINTPHYSICS.air_friction = dump_dic['Data']['Air Friction'] / 10000
    POINTPHYSICS.water_friction = dump_dic['Data']['Water Friction'] / 10000
    POINTPHYSICS.surface_friction = dump_dic['Data']['Surface Friction']
    POINTPHYSICS.elasticity = dump_dic['Data']['Elasticity']

    return POINTPHYSICS
