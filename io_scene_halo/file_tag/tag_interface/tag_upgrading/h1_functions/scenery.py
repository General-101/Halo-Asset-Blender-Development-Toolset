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

from ..h1_functions.object import (
    convert_object_flags, 
    generate_ai_properties, 
    generate_attachments, 
    generate_widgets, 
    generate_change_colors, 
    FunctionEnum as ObjectFunctionsEnum
    )

def upgrade_scenery(h1_scen_asset, EngineTag):
    h1_scen_data = h1_scen_asset["Data"]

    function_keywords = [("Object", ObjectFunctionsEnum)]

    h2_scen_asset = {
        "TagName": h1_scen_asset["TagName"],
        "Header": {
            "unk1": 0,
            "flags": 0,
            "tag type": 0,
            "name": "",
            "tag group": "scen",
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
            "flags": convert_object_flags(h1_scen_data["flags"]),
            "bounding radius": h1_scen_data["bounding radius"],
            "bounding offset": h1_scen_data["bounding offset"],
            "acceleration scale": h1_scen_data["acceleration scale"],
            "model": {"group name": "hlmt", "path": ""},
            "ai properties": generate_ai_properties(h1_scen_asset),
            "hud text message index": h1_scen_data["hud text message index"],
            "attachments": generate_attachments(h1_scen_asset, function_keywords),
            "widgets": generate_widgets(h1_scen_asset),
            "change colors": generate_change_colors(h1_scen_asset, function_keywords),
            "pathfinding policy": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "flags_1": 0,
            "lightmapping policy": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            }
        }
    }

    return h2_scen_asset
