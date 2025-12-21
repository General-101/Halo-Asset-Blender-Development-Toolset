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

def generate_point_states(dump_dic):
    point_states_block = []
    for point_state_element in dump_dic["Data"]["point states"]:
        point_state_dict = {
            "duration": point_state_element["duration"],
            "transition duration": point_state_element["transition duration"],
            "physics": point_state_element["physics"],
            "width": point_state_element["width"],
            "color lower bound": point_state_element["color lower bound"],
            "color upper bound": point_state_element["color upper bound"],
            "scale flags": point_state_element["scale flags"]
        }
        
        point_states_block.append(point_state_dict)

    return point_states_block

def upgrade_contrail(h1_cont_asset, EngineTag):
    h1_cont_data = h1_cont_asset["Data"]

    h2_cont_asset = {
        "TagName": h1_cont_asset["TagName"],
        "Header": {
            "unk1": 0, 
            "flags": 0, 
            "tag type": 0, 
            "name": "", 
            "tag group": "cont", 
            "checksum": 0, 
            "data offset": 64, 
            "data length": 0, 
            "unk2": 0, 
            "version": 3, 
            "destination": 0, 
            "plugin handle": -1, 
            "engine tag": EngineTag.H2Latest.value
        },
        "Data": {
            "flags": h1_cont_data["flags"],
            "scale flags": h1_cont_data["scale flags"],
            "point generation rate": h1_cont_data["point generation rate"],
            "point velocity": h1_cont_data["point velocity"],
            "point velocity cone angle": h1_cont_data["point velocity cone angle"],
            "inherited velocity fraction": h1_cont_data["inherited velocity fraction"],
            "render type": {
                "type": "ShortEnum",
                "value": h1_cont_data["render type"]["value"],
                "value name": ""
            },
            "texture repeats u": h1_cont_data["texture repeats u"],
            "texture repeats v": h1_cont_data["texture repeats v"],
            "texture animation u": h1_cont_data["texture animation u"],
            "texture animation v": h1_cont_data["texture animation v"],
            "animation rate": h1_cont_data["animation rate"],
            "bitmap": h1_cont_data["bitmap"],
            "first sequence index": h1_cont_data["first sequence index"],
            "sequence count": h1_cont_data["sequence count"],
            "shader flags": h1_cont_data["shader flags"],
            "framebuffer blend function": {
                "type": "ShortEnum",
                "value": h1_cont_data["framebuffer blend function"]["value"],
                "value name": ""
            },
            "framebuffer fade mode": {
                "type": "ShortEnum",
                "value": h1_cont_data["framebuffer fade mode"]["value"],
                "value name": ""
            },
            "map flags": h1_cont_data["map flags"],
            "bitmap_1": h1_cont_data["bitmap_1"],
            "anchor": {
                "type": "ShortEnum",
                "value": h1_cont_data["anchor"]["value"],
                "value name": ""
            },
            "flags_1": h1_cont_data["flags_2"],
            "u-animation function": {
                "type": "ShortEnum",
                "value": h1_cont_data["u animation function"]["value"],
                "value name": ""
            },
            "u-animation period": h1_cont_data["u animation period"],
            "u-animation phase": h1_cont_data["u animation phase"],
            "u-animation scale": h1_cont_data["u animation scale"],
            "v-animation function": {
                "type": "ShortEnum",
                "value": h1_cont_data["v animation function"]["value"],
                "value name": ""
            },
            "v-animation period": h1_cont_data["v animation period"],
            "v-animation phase": h1_cont_data["v animation phase"],
            "v-animation scale": h1_cont_data["v animation scale"],
            "rotation-animation function": {
                "type": "ShortEnum",
                "value": h1_cont_data["rotation animation function"]["value"],
                "value name": ""
            },
            "rotation-animation period": h1_cont_data["rotation animation period"],
            "rotation-animation phase": h1_cont_data["rotation animation phase"],
            "rotation-animation scale": h1_cont_data["rotation animation scale"],
            "rotation-animation center": h1_cont_data["rotation animation center"],
            "zsprite radius scale": h1_cont_data["zsprite radius scale"],
            "point states": generate_point_states(h1_cont_asset)
        }
    }

    return h2_cont_asset
