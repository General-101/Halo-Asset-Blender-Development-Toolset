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

from enum import Flag, Enum, auto

class H1LightFlags(Flag):
    dynamic = auto()
    no_specular = auto()
    dont_light_own_object = auto()
    supersize_in_first_person = auto()
    first_person_flashlight = auto()
    dont_fade_active_camouflage = auto()

class H2LightFlags(Flag):
    no_illumination = auto()
    no_specular = auto()
    force_cast_environment_shadows_through_portals = auto()
    no_shadow = auto()
    force_frustum_visibility_on_small_light = auto()
    only_render_in_first_person = auto()
    only_render_in_third_person = auto()
    dont_fade_when_invisible = auto()
    multiplayer_override = auto()
    animated_gel = auto()
    only_in_dynamic_envmap = auto()
    ignore_parent_object = auto()
    dont_shadow_parent = auto()
    ignore_all_parents = auto()
    march_milestone_hack = auto()
    force_light_inside_world = auto()
    environment_doesnt_cast_stencil_shadows = auto()
    objects_dont_cast_stencil_shadows = auto()
    first_person_from_camera = auto()
    texture_camera_gel = auto()
    light_framerate_killer = auto()
    allowed_in_split_screen = auto()
    only_on_parent_bipeds = auto()

class DefaultLightmapSettingEnum(Enum):
    dynamic_only = 0
    dynamic_with_lightmaps = auto()
    lightmaps_only = auto()

def convert_light_flags(object_flags):
    flags = 0
    active_h1_flags = H1LightFlags(object_flags)
    if H1LightFlags.no_specular in active_h1_flags:
        flags += H2LightFlags.no_specular.value

    if H1LightFlags.dont_fade_active_camouflage in active_h1_flags:
        flags += H2LightFlags.dont_fade_when_invisible.value

    return flags

def upgrade_light(h1_ligh_asset, EngineTag):
    h1_lens_data = h1_ligh_asset["Data"]

    light_flags = H1LightFlags(h1_lens_data["flags"])

    lightmap_setting = DefaultLightmapSettingEnum.lightmaps_only.value
    if H1LightFlags.dynamic in light_flags:
        lightmap_setting = DefaultLightmapSettingEnum.dynamic_only.value

    h2_lens_asset = {
        "TagName": h1_ligh_asset["TagName"],
        "Header": {
            "unk1": 0,
            "flags": 0,
            "tag type": 0,
            "name": "",
            "tag group": "ligh",
            "checksum": 0,
            "data offset": 64,
            "data length": 0,
            "unk2": 0,
            "version": 4,
            "destination": 0,
            "plugin handle": -1,
            "engine tag": EngineTag.H2Latest.value
        },
        "Data": {
            "flags": convert_light_flags(h1_lens_data["flags"]),
            "type": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "size modifer": h1_lens_data["radius modifer"],
            "shadow quality bias": 0,
            "shadow tap bias": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "radius": h1_lens_data["radius"],
            "specular radius": 0.0,
            "near width": 0.0,
            "height stretch": 0.0,
            "field of view": 0.0,
            "falloff distance": 0.0,
            "cutoff distance": 0.0,
            "interpolation flags": h1_lens_data["interpolation flags"],
            "bloom bounds": {
                "Min": 0.0,
                "Max": 0.0
            },
            "specular lower bound": h1_lens_data["color lower bound"],
            "specular upper bound": h1_lens_data["color upper bound"],
            "diffuse lower bound": h1_lens_data["color lower bound"],
            "diffuse upper bound": h1_lens_data["color upper bound"],
            "brightness bounds": {
                "Min": 0.0,
                "Max": 0.0
            },
            "gel map": {
                "group name": "bitm",
                "unk1": 0,
                "length": 0,
                "unk2": -1,
                "path": ""
            },
            "specular mask": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "falloff function": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "diffuse contrast": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "specular contrast": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "falloff geometry": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "lens flare": h1_lens_data["lens flare"],
            "bounding radius": 0.0,
            "light volume": {
                "group name": "MGS2",
                "unk1": 0,
                "length": 0,
                "unk2": -1,
                "path": ""
            },
            "default lightmap setting": {
                "type": "ShortEnum",
                "value": lightmap_setting,
                "value name": ""
            },
            "lightmap half life": h1_lens_data["intensity"],
            "lightmap light scale": 0.0,
            "duration": h1_lens_data["duration"],
            "falloff function_1": {
                "type": "ShortEnum",
                "value": h1_lens_data["falloff function"]["value"],
                "value name": ""
            },
            "illumination fade": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "shadow fade": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "specular fade": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "flags_1": 0
        }
    }

    return h2_lens_asset
