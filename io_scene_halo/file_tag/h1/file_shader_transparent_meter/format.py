# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2023 Steven Garcia
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

class RadiosityFlags(Flag):
    simple_parameterization = auto()
    ignore_normals = auto()
    transparent_lit = auto()

class DetailLevelEnum(Enum):
    high = 0
    medium = auto()
    low = auto()
    turd = auto()

class MaterialTypeEnum(Enum):
    dirt = 0
    sand = auto()
    stone = auto()
    snow = auto()
    wood = auto()
    metal_hollow = auto()
    metal_thin = auto()
    metal_thick = auto()
    rubber = auto()
    glass = auto()
    force_field = auto()
    grunt = auto()
    hunter_armor = auto()
    hunter_skin = auto()
    elite = auto()
    jackal = auto()
    jackal_energy_shield = auto()
    engineer_skin = auto()
    enngineer_force_field = auto()
    flood_combat_form = auto()
    flood_carrier_form = auto()
    cyborg_armor = auto()
    cyborg_energy_shield = auto()
    human_armor = auto()
    human_skin = auto()
    sentinel = auto()
    monitor = auto()
    plastic = auto()
    water = auto()
    leaves = auto()
    elite_energy_shield = auto()
    ice = auto()
    hunter_shield = auto()

class MeterFlags(Flag):
    decal = auto()
    two_sided = auto()
    flash_color_is_negative = auto()
    tint_mode_2 = auto()
    unfiltered = auto()

class ChannelSourceEnum(Enum):
    none = 0
    a_out = auto()
    b_out = auto()
    c_out = auto()
    d_out = auto()

class ShaderAsset():
    def __init__(self):
        self.header = None
        self.shader_body = None

    class ShaderBody:
        def __init__(self, radiosity_flags=0, detail_level=0, power=0.0, color_of_emitted_light=(0.0, 0.0, 0.0, 1.0), light_tint_color=(0.0, 0.0, 0.0, 1.0), material_type=0,
                     meter_flags=0, meter_map=None, gradient_min_color=(0.0, 0.0, 0.0, 1.0), gradient_max_color=(0.0, 0.0, 0.0, 1.0), background_color=(0.0, 0.0, 0.0, 1.0),
                     flash_color=(0.0, 0.0, 0.0, 1.0), tint_color=(0.0, 0.0, 0.0, 1.0), meter_transparency=0.0, background_transparency=0.0, meter_brightness_source=0,
                     flash_brightness_source=0, value_source=0, gradient_source=0, flash_extension_source=0):
            self.radiosity_flags = radiosity_flags
            self.detail_level = detail_level
            self.power = power
            self.color_of_emitted_light = color_of_emitted_light
            self.light_tint_color = light_tint_color
            self.material_type = material_type
            self.meter_flags = meter_flags
            self.meter_map = meter_map
            self.gradient_min_color = gradient_min_color
            self.gradient_max_color = gradient_max_color
            self.background_color = background_color
            self.flash_color = flash_color
            self.tint_color = tint_color
            self.meter_transparency = meter_transparency
            self.background_transparency = background_transparency
            self.meter_brightness_source = meter_brightness_source
            self.flash_brightness_source = flash_brightness_source
            self.value_source = value_source
            self.gradient_source = gradient_source
            self.flash_extension_source = flash_extension_source
