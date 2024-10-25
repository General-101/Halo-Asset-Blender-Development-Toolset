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

from mathutils import Vector
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

class ChannelSourceEnum(Enum):
    none = 0
    a_out = auto()
    b_out = auto()
    c_out = auto()
    d_out = auto()

class ShaderAsset():
    def __init__(self, header=None, radiosity_flags=0, detail_level=0, power=0.0, color_of_emitted_light=(0.0, 0.0, 0.0, 1.0), light_tint_color=(0.0, 0.0, 0.0, 1.0), 
                 material_type=0, intensity_source=0, intensity_exponent=0.0, offset_source=0, offset_amount=0.0, offset_exponent=0.0, perpendicular_brightness=0.0, 
                 perpendicular_tint_color=(0.0, 0.0, 0.0, 1.0), parallel_brightness=0.0, parallel_tint_color=(0.0, 0.0, 0.0, 1.0), tint_color_source=0, 
                 primary_animation_period=0.0, primary_animation_direction=Vector(), primary_noise_map_scale=0.0, primary_noise_map=None, secondary_animation_period=0.0, 
                 secondary_animation_direction=Vector(), secondary_noise_map_scale=0.0, secondary_noise_map=None):
        self.header = header
        self.radiosity_flags = radiosity_flags
        self.detail_level = detail_level
        self.power = power
        self.color_of_emitted_light = color_of_emitted_light
        self.light_tint_color = light_tint_color
        self.material_type = material_type
        self.intensity_source = intensity_source
        self.intensity_exponent = intensity_exponent
        self.offset_source = offset_source
        self.offset_amount = offset_amount
        self.offset_exponent = offset_exponent
        self.perpendicular_brightness = perpendicular_brightness
        self.perpendicular_tint_color = perpendicular_tint_color
        self.parallel_brightness = parallel_brightness
        self.parallel_tint_color = parallel_tint_color
        self.tint_color_source = tint_color_source
        self.primary_animation_period = primary_animation_period
        self.primary_animation_direction = primary_animation_direction
        self.primary_noise_map_scale = primary_noise_map_scale
        self.primary_noise_map = primary_noise_map
        self.secondary_animation_period = secondary_animation_period
        self.secondary_animation_direction = secondary_animation_direction
        self.secondary_noise_map_scale = secondary_noise_map_scale
        self.secondary_noise_map = secondary_noise_map
