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

def upgrade_point_physics(h1_pphy_asset, EngineTag):
    h1_pphy_data = h1_pphy_asset["Data"]

    h2_pphy_asset = {
        "TagName": h1_pphy_asset["TagName"],
        "Header": {
            "unk1": 0,
            "flags": 0,
            "tag type": 0,
            "name": "",
            "tag group": "pphy",
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
            "flags": h1_pphy_data["flags"],
            "density": h1_pphy_data["density"],
            "air friction": h1_pphy_data["air friction"] / 10000, # No idea why I'm doing this. I think it was from a fix_tags.cpp file but I don't have that stuff anymore.
            "water friction": h1_pphy_data["water friction"] / 10000, # Same as above. - Gen
            "surface friction": h1_pphy_data["surface friction"],
            "elasticity": h1_pphy_data["elasticity"]
        }
    }

    return h2_pphy_asset
