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

def upgrade_sound_environment(h1_snde_asset, EngineTag):
    h1_snde_data = h1_snde_asset["Data"]

    h2_snde_asset = {
        "TagName": h1_snde_asset["TagName"],
        "Header": {
            "unk1": 0,
            "flags": 0,
            "tag type": 0,
            "name": "",
            "tag group": "snde",
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
            "priority": h1_snde_data["priority"],
            "room intensity": h1_snde_data["room intensity"],
            "room intensity hf": h1_snde_data["room intensity hf"],
            "room rolloff (0 to 10)": h1_snde_data["room rolloff"],
            "decay time (.1 to 20)": h1_snde_data["decay time"],
            "decay hf ratio (.1 to 2)": h1_snde_data["decay hf ratio"],
            "reflections intensity": h1_snde_data["reflections intensity"],
            "reflections delay (0 to .3)": h1_snde_data["reflections delay"],
            "reverb intensity": h1_snde_data["reverb intensity"],
            "reverb delay (0 to .1)": h1_snde_data["reverb delay"],
            "diffusion": h1_snde_data["diffusion"],
            "density": h1_snde_data["density"],
            "hf reference(20 to 20,000)": h1_snde_data["hf reference"],
            "reflection type": "",
        }
    }

    return h2_snde_asset
