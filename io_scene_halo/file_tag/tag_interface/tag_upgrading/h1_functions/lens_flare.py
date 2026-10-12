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

from .functions import create_function, FunctionTypeEnum, MappingFlags, AnimationFunctionEnum

def generate_reflections(dump_dic):
    reflections_block = []
    for reflection_element in dump_dic["Data"]["reflections"]:
        reflection_dict = {
            "flags": reflection_element["flags"],
            "bitmap index": reflection_element["bitmap index"],
            "position": reflection_element["position"],
            "rotation offset": reflection_element["rotation offset"],
            "radius": reflection_element["radius"],
            "brightness": reflection_element["brightness"],
            "modulation factor": reflection_element["tint color"].get("A", 1.0),
            "color": {
                "R": reflection_element["tint color"].get("R", 0.0),
                "G": reflection_element["tint color"].get("G", 0.0),
                "B": reflection_element["tint color"].get("B", 0.0)
            }
        }

        reflections_block.append(reflection_dict)

    return reflections_block

def generate_brightness(dump_dic):
    brightness_block = []
    for reflection_element in dump_dic["Data"]["reflections"]:
        color_0 = reflection_element["color lower bound"]
        color_1 = reflection_element["color upper bound"]

        R0 = color_0.get("R", 0.0)
        G0 = color_0.get("G", 0.0)
        B0 = color_0.get("B", 0.0)
        A0 = color_0.get("A", 0.0)
        R1 = color_1.get("R", 0.0)
        G1 = color_1.get("G", 0.0)
        B1 = color_1.get("B", 0.0)
        A1 = color_1.get("A", 0.0)

        animation_function = AnimationFunctionEnum(reflection_element["animation function"]["value"])

        is_black = False
        if (R0 + G0 + B0) == 0.0 and (R1 + G1 + B1) == 0.0:
            is_black = True

        is_animated = False
        if not animation_function == AnimationFunctionEnum.one and not animation_function == AnimationFunctionEnum.zero:
            is_animated = True

        if not is_black and is_animated:
            function_type = FunctionTypeEnum.periodic.value
            mapping_inputs = [A0, A1]
            function_inputs = [reflection_element["animation phase"], reflection_element["animation period"], 0, 1]

            brightness_dict = {
                "data": create_function(function_type=function_type, function_1=animation_function.value, mapping_inputs=mapping_inputs, function_inputs=function_inputs),
            }

            brightness_block.append(brightness_dict)

        break

    return brightness_block

def generate_color(dump_dic):
    color_block = []
    for reflection_element in dump_dic["Data"]["reflections"]:
        color_0 = reflection_element["color lower bound"]
        color_1 = reflection_element["color upper bound"]

        R0 = color_0.get("R", 0.0)
        G0 = color_0.get("G", 0.0)
        B0 = color_0.get("B", 0.0)
        A0 = color_0.get("A", 0.0)
        R1 = color_1.get("R", 0.0)
        G1 = color_1.get("G", 0.0)
        B1 = color_1.get("B", 0.0)
        A1 = color_1.get("A", 0.0)

        animation_function = AnimationFunctionEnum(reflection_element["animation function"]["value"])

        is_black = False
        if (R0 + G0 + B0) == 0.0 and (R1 + G1 + B1) == 0.0:
            is_black = True

        is_animated = False
        if not animation_function == AnimationFunctionEnum.one and not animation_function == AnimationFunctionEnum.zero:
            is_animated = True

        if not is_black and is_animated:
            function_type = FunctionTypeEnum.periodic.value
            flag_value = MappingFlags._2_color.value
            mapping_inputs = [color_0, color_1]
            function_inputs = [reflection_element["animation phase"], reflection_element["animation period"], 0, 1]

            color_dict = {
                "data": create_function(function_type=function_type, flags=flag_value, function_1=animation_function.value, mapping_inputs=mapping_inputs, function_inputs=function_inputs),
            }

            color_block.append(color_dict)

        break

    return color_block

def upgrade_lens_flare(h1_lens_asset, EngineTag):
    h1_lens_data = h1_lens_asset["Data"]

    h2_lens_asset = {
        "TagName": h1_lens_asset["TagName"],
        "Header": {
            "unk1": 0,
            "flags": 0,
            "tag type": 0,
            "name": "",
            "tag group": "lens",
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
            "falloff angle": h1_lens_data["falloff angle"],
            "cutoff angle": h1_lens_data["cutoff angle"],
            "occlusion radius": h1_lens_data["occlusion radius"],
            "occlusion offset direction": {
                "type": "ShortEnum",
                "value": h1_lens_data["occlusion offset direction"]["value"],
                "value name": ""
            },
            "occlusion inner radius scale": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "near fade distance": h1_lens_data["near fade distance"],
            "far fade distance": h1_lens_data["far fade distance"],
            "bitmap": h1_lens_data["bitmap"],
            "flags": h1_lens_data["flags"],
            "rotation function": {
                "type": "ShortEnum",
                "value": h1_lens_data["rotation function"]["value"],
                "value name": ""
            },
            "rotation function scale": h1_lens_data["rotation function scale"],
            "corona scale": [h1_lens_data["horizontal scale"], h1_lens_data["vertical scale"]],
            "falloff function": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "reflections": generate_reflections(h1_lens_asset),
            "flags_1": 0,
            "brightness": generate_brightness(h1_lens_asset),
            "color": generate_color(h1_lens_asset),
            "rotation": []
        }
    }

    return h2_lens_asset
