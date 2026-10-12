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

def upgrade_machine(h1_mach_asset, EngineTag):
    h1_mach_data = h1_mach_asset["Data"]

    function_keywords = [("Object", ObjectFunctionsEnum)]

    h2_mach_asset = {
        "TagName": h1_mach_asset["TagName"],
        "Header": {
            "unk1": 0,
            "flags": 0,
            "tag type": 0,
            "name": "",
            "tag group": "mach",
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
            "flags": convert_object_flags(h1_mach_data["flags"]),
            "bounding radius": h1_mach_data["bounding radius"],
            "bounding offset": h1_mach_data["bounding offset"],
            "acceleration scale": h1_mach_data["acceleration scale"],
            "model": {"group name": "hlmt", "path": ""},
            "ai properties": generate_ai_properties(h1_mach_asset),
            "hud text message index": h1_mach_data["hud text message index"],
            "attachments": generate_attachments(h1_mach_asset, function_keywords),
            "widgets": generate_widgets(h1_mach_asset),
            "change colors": generate_change_colors(h1_mach_asset, function_keywords),
            "flags_1": h1_mach_data["flags_1"],
            "power transition time": h1_mach_data["power transition time"],
            "power acceleration time": h1_mach_data["power acceleration time"],
            "position transition time": h1_mach_data["position transition time"],
            "position acceleration time": h1_mach_data["position acceleration time"],
            "depowered position transition time": h1_mach_data["depowered position transition time"],
            "depowered position acceleration time": h1_mach_data["depowered position acceleration time"],
            "lightmap flags": 0,
            "open (up)": h1_mach_data["open"],
            "close (down)": h1_mach_data["close"],
            "opened": h1_mach_data["opened"],
            "closed": h1_mach_data["closed"],
            "depowered": h1_mach_data["depowered"],
            "repowered": h1_mach_data["repowered"],
            "delay time": h1_mach_data["delay time"],
            "delay effect": h1_mach_data["delay effect"],
            "automatic activation radius": h1_mach_data["automatic activation radius"],
            "type": {
                "type": "ShortEnum",
                "value": h1_mach_data["type_1"]["value"],
                "value name": ""
            },
            "flags_2": h1_mach_data["flags_2"],
            "door open time": h1_mach_data["door open time"],
            "door occlusion bounds": {
                "Min": 0.0,
                "Max": 0.0
            },
            "collision response": {
                "type": "ShortEnum",
                "value": h1_mach_data["collision response"]["value"],
                "value name": ""
            },
            "elevator node": h1_mach_data["elevator node"],
            "pathfinding policy": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            }
        }
    }

    return h2_mach_asset
