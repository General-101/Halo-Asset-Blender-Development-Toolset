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

class WaterFlags(Flag):
    base_map_alpha_modulates_reflection = auto()
    base_map_color_modulates_background = auto()
    atmospheric_fog = auto()
    draw_before_fog = auto()

class ShaderAsset():
    def __init__(self):
        self.header = None
        self.shader_body = None
        self.ripples = None

    class ShaderBody:
        def __init__(self, radiosity_flags=0, detail_level=0, power=0.0, color_of_emitted_light=(0.0, 0.0, 0.0, 1.0), light_tint_color=(0.0, 0.0, 0.0, 1.0), material_type=0,
                     water_flags=0, base_map=None, view_perpendicular_brightness=0.0, view_perpendicular_tint_color=(0.0, 0.0, 0.0, 1.0), view_parallel_brightness=0.0,
                     view_parallel_tint_color=(0.0, 0.0, 0.0, 1.0), reflection_map=None, ripple_animation_angle=0.0, ripple_animation_velocity=0.0, ripple_scale=0.0,
                     ripple_maps=None, ripple_mipmap_levels=0, ripple_mipmap_fade_factor=0.0, ripple_mipmap_detail_bias=0.0, ripples_tag_block=None):
            self.radiosity_flags = radiosity_flags
            self.detail_level = detail_level
            self.power = power
            self.color_of_emitted_light = color_of_emitted_light
            self.light_tint_color = light_tint_color
            self.material_type = material_type
            self.water_flags = water_flags
            self.base_map = base_map
            self.view_perpendicular_brightness = view_perpendicular_brightness
            self.view_perpendicular_tint_color = view_perpendicular_tint_color
            self.view_parallel_brightness = view_parallel_brightness
            self.view_parallel_tint_color = view_parallel_tint_color
            self.reflection_map = reflection_map
            self.ripple_animation_angle = ripple_animation_angle
            self.ripple_animation_velocity = ripple_animation_velocity
            self.ripple_scale = ripple_scale
            self.ripple_maps = ripple_maps
            self.ripple_mipmap_levels = ripple_mipmap_levels
            self.ripple_mipmap_fade_factor = ripple_mipmap_fade_factor
            self.ripple_mipmap_detail_bias = ripple_mipmap_detail_bias
            self.ripples_tag_block = ripples_tag_block

    class Ripple:
        def __init__(self, contribution_factor=0.0, animation_angle=0.0, animation_velocity=0.0, map_offset=(0.0, 0.0), map_repeat=0, map_index=0):
            self.contribution_factor = contribution_factor
            self.animation_angle = animation_angle
            self.animation_velocity = animation_velocity
            self.map_offset = map_offset
            self.map_repeat = map_repeat
            self.map_index = map_index
