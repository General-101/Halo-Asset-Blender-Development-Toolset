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

def upgrade_equipment(h1_effe_asset, EngineTag):
    h1_effe_data = h1_effe_asset["Data"]

    function_keywords = [("Object", ObjectFunctionsEnum)]

    h2_effe_asset = {
        "TagName": h1_effe_asset["TagName"],
        "Header": {
            "unk1": 0,
            "flags": 0,
            "tag type": 0,
            "name": "",
            "tag group": "eqip",
            "checksum": 0,
            "data offset": 64,
            "data length": 0,
            "unk2": 0,
            "version": 2,
            "destination": 0,
            "plugin handle": -1,
            "engine tag": EngineTag.H2Latest.value
        },
        "Data": {
           "flags": convert_object_flags(h1_effe_data["flags"]),
            "bounding radius": h1_effe_data["bounding radius"],
            "bounding offset": h1_effe_data["bounding offset"],
            "acceleration scale": h1_effe_data["acceleration scale"],
            "model": {"group name": "hlmt", "path": ""},
            "ai properties": generate_ai_properties(h1_effe_data),
            "hud text message index": h1_effe_data["hud text message index"],
            "attachments": generate_attachments(h1_effe_data, function_keywords),
            "widgets": generate_widgets(h1_effe_data),
            "change colors": generate_change_colors(h1_effe_data, function_keywords),
            "flags_1": h1_effe_data["flags_1"],
            "OLD message index": h1_effe_data["pickup text index"],
            "sort order": h1_effe_data["sort order"],
            "multiplayer on-ground scale": h1_effe_data["scale"],
            "campaign on-ground scale": h1_effe_data["scale"],
            "pickup message": "",
            "swap message": "",
            "pickup or dual msg": "",
            "swap or dual msg": "",
            "dual-only msg": "",
            "picked up msg": "",
            "singluar quantity msg": "",
            "plural quantity msg": "",
            "switch-to msg": "",
            "switch-to from ai msg": "",
            "UNUSED": h1_effe_data["material effects"],
            "collision sound": h1_effe_data["collision sound"],
            "detonation damage effect": {"group name": "jpt!", "path": ""},
            "detonation delay": h1_effe_data["detonation delay"],
            "detonating effect": h1_effe_data["detonating effect"],
            "detonation effect": h1_effe_data["detonation effect"],
            "powerup type": {
                "type": "ShortEnum",
                "value": h1_effe_data["powerup type"]["value"],
                "value name": ""
            },
            "grenade type": {
                "type": "ShortEnum",
                "value": h1_effe_data["grenade type"]["value"],
                "value name": ""
            },
            "powerup time": h1_effe_data["powerup time"],
            "pickup sound": h1_effe_data["pickup sound"]
        }
    }
    
    return h2_effe_asset
