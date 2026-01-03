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

def generate_atmospheric_fog(dump_dic):
    fog_block = []

    fog_dict = {
        "color": dump_dic["Data"]["color_2"],
        "maximum density": dump_dic["Data"]["maximum density"],
        "start distance": dump_dic["Data"]["start distance"],
        "opaque distance": dump_dic["Data"]["opaque distance"]
    }

    fog_block.append(fog_dict)

    return fog_block

def generate_lights(dump_dic):
    light_block = []
    for light_element in dump_dic["Data"]["lights"]:
        light_dict = {
            "direction vector": [0.0, 0.0, 0.0],
            "direction": light_element["direction"],
            "lens flare": light_element["lens flare"],
            "fog": [],
            "fog opposite": [],
            "radiosity": [
                {
                    "flags": light_element["flags"],
                    "color": light_element["color"],
                    "power": 0.1 * light_element["power"],
                    "test distance": light_element["test distance"],
                    "diameter": light_element["diameter"]
                }
            ]
        }

        light_block.append(light_dict)

    return light_block

def upgrade_sky(h1_sky_asset, EngineTag):
    h1_sky_data = h1_sky_asset["Data"]

    h2_sky_asset = {
        "TagName": h1_sky_asset["TagName"],
        "Header": {
            "unk1": 0,
            "flags": 0,
            "tag type": 0,
            "name": "",
            "tag group": "sky ",
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
            "render model": {"group name": "mode", "path": h1_sky_data["model"]["path"]},
            "animation graph": {"group name": "jmad", "path": h1_sky_data["animation graph"]["path"]},
            "flags": 0,
            "render model scale": 0.0,
            "movement scale": 0.0,
            "cubemap": [],
            "indoor ambient color": h1_sky_data["color"],
            "outdoor ambient color": h1_sky_data["color_1"],
            "fog spread distance": 0.0,
            "atmospheric fog": generate_atmospheric_fog(h1_sky_asset),
            "secondary fog": [],
            "sky fog": [],
            "patchy fog": [],
            "amount": 0.0,
            "threshold": 0.0,
            "brightness": 0.0,
            "gamma power": 0.0,
            "lights": generate_lights(h1_sky_asset),
            "global sky rotation": 0.0,
            "shader functions": [],
            "animations": [],
            "clear color": {
                "R": 0.0,
                "G": 0.0,
                "B": 0.0
            }
        }
    }

    return h2_sky_asset
