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

class ModelFlags(Flag):
    detail_after_reflections = auto()
    two_sided = auto()
    not_alpha_tested = auto()
    alpha_blended_decal = auto()
    true_atmospheric_fog = auto()
    disable_two_sided_culling = auto()
    multipurpose_map_uses_og_xbox_channel_order = auto()

class SelfIlluminationFlags(Flag):
    no_random_phase = auto()

class ChannelSourceEnum(Enum):
    none = 0
    a = auto()
    b = auto()
    c = auto()
    d = auto()

class FunctionEnum(Enum):
    one = 0
    zero = auto()
    cosine = auto()
    cosine_variable_period = auto()
    diagonal_wave = auto()
    diagonal_wave_variable_period = auto()
    slide = auto()
    slide_variable_period = auto()
    noise = auto()
    jitter = auto()
    wander = auto()
    spark = auto()

class DetailFumctionEnum(Enum):
    double_biased_multiply = 0
    multiply = auto()
    double_biased_add = auto()

class DetailMaskEnum(Enum):
    none = 0
    reflection_mask_inverse = auto()
    reflection_mask = auto()
    self_illumination_mask_inverse = auto()
    self_illumination_mask = auto()
    change_color_mask_inverse = auto()
    change_color_mask = auto()
    multipurpose_map_alpha_inverse = auto()
    multipurpose_map_alpha = auto()

class ShaderAsset():
    def __init__(self, header=None, radiosity_flags=0, detail_level=0, power=0.0, color_of_emitted_light=(0.0, 0.0, 0.0, 1.0), tint_color=(0.0, 0.0, 0.0, 1.0), 
                 material_type=0, model_flags=0, translucency=0.0, change_color_source=0, self_illumination_flags=0, self_illumination_color_source=0, 
                 self_illumination_animation_function=0, self_illumination_animation_period=0.0, self_illumination_animation_color_lower_bound=(0.0, 0.0, 0.0, 1.0), 
                 self_illumination_animation_color_upper_bound=(0.0, 0.0, 0.0, 1.0), map_u_scale=0.0, map_v_scale=0.0, base_map=None, multipurpose_map=None, 
                 detail_function=0, detail_mask=0, detail_map_scale=0.0, detail_map=None, detail_map_v_scale=0.0, u_animation_source=0, u_animation_function=0, 
                 u_animation_period=0.0, u_animation_phase=0.0, u_animation_scale=0.0, v_animation_source=0, v_animation_function=0, v_animation_period=0.0, 
                 v_animation_phase=0.0, v_animation_scale=0.0, rotation_animation_source=0, rotation_animation_function=0, rotation_animation_period=0.0, 
                 rotation_animation_phase=0.0, rotation_animation_scale=0.0, rotation_animation_center=(0.0, 0.0), reflection_falloff_distance=0.0, 
                 reflection_cutoff_distance=0.0, perpendicular_brightness=0.0, perpendicular_tint_color=(0.0, 0.0, 0.0, 1.0), parallel_brightness=0.0, 
                 parallel_tint_color=(0.0, 0.0, 0.0, 1.0), reflection_cube_map=None, bump_scale=1.0, bump_map=None):
        self.header = header
        self.radiosity_flags = radiosity_flags
        self.detail_level = detail_level
        self.power = power
        self.color_of_emitted_light = color_of_emitted_light
        self.tint_color = tint_color
        self.material_type = material_type
        self.model_flags = model_flags
        self.translucency = translucency
        self.change_color_source = change_color_source
        self.self_illumination_flags = self_illumination_flags
        self.self_illumination_color_source = self_illumination_color_source
        self.self_illumination_animation_function = self_illumination_animation_function
        self.self_illumination_animation_period = self_illumination_animation_period
        self.self_illumination_animation_color_lower_bound = self_illumination_animation_color_lower_bound
        self.self_illumination_animation_color_upper_bound = self_illumination_animation_color_upper_bound
        self.map_u_scale = map_u_scale
        self.map_v_scale = map_v_scale
        self.base_map = base_map
        self.multipurpose_map = multipurpose_map
        self.detail_function = detail_function
        self.detail_mask = detail_mask
        self.detail_map_scale = detail_map_scale
        self.detail_map = detail_map
        self.detail_map_v_scale = detail_map_v_scale
        self.u_animation_source = u_animation_source
        self.u_animation_function = u_animation_function
        self.u_animation_period = u_animation_period
        self.u_animation_phase = u_animation_phase
        self.u_animation_scale = u_animation_scale
        self.v_animation_source = v_animation_source
        self.v_animation_function = v_animation_function
        self.v_animation_period = v_animation_period
        self.v_animation_phase = v_animation_phase
        self.v_animation_scale = v_animation_scale
        self.rotation_animation_source = rotation_animation_source
        self.rotation_animation_function = rotation_animation_function
        self.rotation_animation_period = rotation_animation_period
        self.rotation_animation_phase = rotation_animation_phase
        self.rotation_animation_scale = rotation_animation_scale
        self.rotation_animation_center = rotation_animation_center
        self.reflection_falloff_distance = reflection_falloff_distance
        self.reflection_cutoff_distance = reflection_cutoff_distance
        self.perpendicular_brightness = perpendicular_brightness
        self.perpendicular_tint_color = perpendicular_tint_color
        self.parallel_brightness = parallel_brightness
        self.parallel_tint_color = parallel_tint_color
        self.reflection_cube_map = reflection_cube_map
        self.bump_scale = bump_scale
        self.bump_map = bump_map
