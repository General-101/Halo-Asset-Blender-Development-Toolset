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

class FramebufferBlendFunctionEnum(Enum):
    alpha_blend = 0
    multiply = auto()
    double_multiply = auto()
    add = auto()
    subtract = auto()
    component_min = auto()
    component_max = auto()
    alpha_multiply_add = auto()

class LayerEnum(Enum):
    lit_alpha_blend_prelight = 0
    lit_alpha_blend = auto()
    double_multiply = auto()
    multiply = auto()
    max_layer = auto()
    add = auto()
    error = auto()

def convert_legacy_layer(blend_index):
    h2_blend_index = 0
    h1_blend = FramebufferBlendFunctionEnum(blend_index)
    if h1_blend == FramebufferBlendFunctionEnum.alpha_blend:
        h2_blend_index = LayerEnum.lit_alpha_blend.value
    elif h1_blend == FramebufferBlendFunctionEnum.multiply:
        h2_blend_index = LayerEnum.multiply.value
    elif h1_blend == FramebufferBlendFunctionEnum.double_multiply:
        h2_blend_index = LayerEnum.double_multiply.value
    elif h1_blend == FramebufferBlendFunctionEnum.add:
        h2_blend_index = LayerEnum.add.value
    elif h1_blend == FramebufferBlendFunctionEnum.subtract:
        h2_blend_index = LayerEnum.add.value
    elif h1_blend == FramebufferBlendFunctionEnum.component_min:
        h2_blend_index = LayerEnum.max_layer.value
    elif h1_blend == FramebufferBlendFunctionEnum.component_max:
        h2_blend_index = LayerEnum.max_layer.value
    elif h1_blend == FramebufferBlendFunctionEnum.alpha_multiply_add:
        h2_blend_index = LayerEnum.multiply.value

    return h2_blend_index

def upgrade_decal(h1_deca_asset, EngineTag):
    h1_deca_data = h1_deca_asset["Data"]

    h2_deca_asset = {
        "TagName": h1_deca_asset["TagName"],
        "Header": {
            "unk1": 0,
            "flags": 0,
            "tag type": 0,
            "name": "",
            "tag group": "deca",
            "checksum": 0,
            "data offset": 64,
            "data length": 0,
            "unk2": 0,
            "version": 1,
            "destination": 0,
            "plugin handle": -1,
            "engine tag": EngineTag.H2Latest.value
        },
        "Data": {
            "flags": h1_deca_data["flags"],
            "type": {
                "type": "ShortEnum",
                "value": h1_deca_data["type"]["value"],
                "value name": ""
            },
            "layer": {
                "type": "ShortEnum",
                "value": convert_legacy_layer(h1_deca_data["framebuffer blend function"]["value"]),
                "value name": ""
            },
            "max overlapping count": 8,
            "next decal in chain": h1_deca_data["next decal in chain"],
            "radius": h1_deca_data["radius"],
            "radius overlap rejection": 0.75,
            "color lower bounds": h1_deca_data["color lower bound"],
            "color upper bounds": h1_deca_data["color upper bound"],
            "lifetime": h1_deca_data["lifetime"],
            "decay time": h1_deca_data["decay time"],
            "bitmap": h1_deca_data["map"],
            "maximum sprite extent": h1_deca_data["maximum sprite extent"]
        }
    }

    return h2_deca_asset
