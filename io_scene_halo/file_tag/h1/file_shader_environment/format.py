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

class EnvironmentFlags(Flag):
    alpha_tested = auto()
    bump_map_is_specular_mask = auto()
    true_atmospheric_fog = auto()
    use_alternate_bump_attenuation = auto()

class EnvironmentTypeEnum(Enum):
    normal = 0
    blended = auto()
    blended_base_specular = auto()

class DiffuseFlags(Flag):
    rescale_detail_maps = auto()
    rescale_bump_maps = auto()

class DiffuseFumctionEnum(Enum):
    double_biased_multiply = 0
    multiply = auto()
    double_biased_add = auto()

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

class SelfIlluminationFlags(Flag):
    unfiltered = auto()

class SpecularFlags(Flag):
    overbright = auto()
    extra_shiny = auto()
    lightmaps_is_specular = auto()

class ReflectionFlags(Flag):
    dynamic_mirror = auto()

class ReflectionTypeEnum(Enum):
    bumped_cubemap = 0
    flat_cubemap = auto()
    bumped_radiosity = auto()

class ShaderAsset():
    def __init__(self, header=None, radiosity_flags=0, detail_level=0, power=0.0, color_of_emitted_light=(0.0, 0.0, 0.0, 1.0), tint_color=(0.0, 0.0, 0.0, 1.0), 
                 material_type=0, environment_flags=0, environment_type=0, lens_flare_spacing=0.0, lens_flare=None, diffuse_flags=0, base_map=None, detail_map_function=0, 
                 primary_detail_map_scale=0.0, primary_detail_map=None, secondary_detail_map_scale=0.0, secondary_detail_map=None, micro_detail_map_function=0, 
                 micro_detail_map_scale=0.0, micro_detail_map=None, material_color=(0.0, 0.0, 0.0, 1.0), bump_map_scale=0.0, bump_map=None, u_animation_function=0, 
                 u_animation_period=0.0, u_animation_scale=0.0, v_animation_function=0, v_animation_period=0.0, v_animation_scale=0.0, self_illumination_flags=0, 
                 primary_on_color=(0.0, 0.0, 0.0, 1.0), primary_off_color=(0.0, 0.0, 0.0, 1.0), primary_animation_function=0, primary_animation_period=0.0, 
                 primary_animation_phase=0.0, secondary_on_color=(0.0, 0.0, 0.0, 1.0), secondary_off_color=(0.0, 0.0, 0.0, 1.0), secondary_animation_function=0, 
                 secondary_animation_period=0.0, secondary_animation_phase=0.0, plasma_on_color=(0.0, 0.0, 0.0, 1.0), plasma_off_color=(0.0, 0.0, 0.0, 1.0), 
                 plasma_animation_function=0, plasma_animation_period=0.0, plasma_animation_phase=0.0, map_scale=0.0, map=None, specular_flags=0, brightness=0, 
                 perpendicular_color=(0.0, 0.0, 0.0, 1.0), parallel_color=(0.0, 0.0, 0.0, 1.0), reflection_flags=0, reflection_type=0, lightmap_brightness_scale=0.0, 
                 perpendicular_brightness=0.0, parallel_brightness=0.0, reflection_cube_map=None):
        self.header = header
        self.radiosity_flags = radiosity_flags
        self.detail_level = detail_level
        self.power = power
        self.color_of_emitted_light = color_of_emitted_light
        self.tint_color = tint_color
        self.material_type = material_type
        self.environment_flags = environment_flags
        self.environment_type = environment_type
        self.lens_flare_spacing = lens_flare_spacing
        self.lens_flare = lens_flare
        self.diffuse_flags = diffuse_flags
        self.base_map = base_map
        self.detail_map_function = detail_map_function
        self.primary_detail_map_scale = primary_detail_map_scale
        self.primary_detail_map = primary_detail_map
        self.secondary_detail_map_scale = secondary_detail_map_scale
        self.secondary_detail_map = secondary_detail_map
        self.micro_detail_map_function = micro_detail_map_function
        self.micro_detail_map_scale = micro_detail_map_scale
        self.micro_detail_map = micro_detail_map
        self.material_color = material_color
        self.bump_map_scale = bump_map_scale
        self.bump_map = bump_map
        self.u_animation_function = u_animation_function
        self.u_animation_period = u_animation_period
        self.u_animation_scale = u_animation_scale
        self.v_animation_function =  v_animation_function
        self.v_animation_period = v_animation_period
        self.v_animation_scale = v_animation_scale
        self.self_illumination_flags = self_illumination_flags
        self.primary_on_color = primary_on_color
        self.primary_off_color = primary_off_color
        self.primary_animation_function = primary_animation_function
        self.primary_animation_period = primary_animation_period
        self.primary_animation_phase = primary_animation_phase
        self.secondary_on_color = secondary_on_color
        self.secondary_off_color = secondary_off_color
        self.secondary_animation_function = secondary_animation_function
        self.secondary_animation_period = secondary_animation_period
        self.secondary_animation_phase = secondary_animation_phase
        self.plasma_on_color = plasma_on_color
        self.plasma_off_color = plasma_off_color
        self.plasma_animation_function = plasma_animation_function
        self.plasma_animation_period = plasma_animation_period
        self.plasma_animation_phase = plasma_animation_phase
        self.map_scale = map_scale
        self.map = map
        self.specular_flags = specular_flags
        self.brightness = brightness
        self.perpendicular_color = perpendicular_color
        self.parallel_color = parallel_color
        self.reflection_flags = reflection_flags
        self.reflection_type = reflection_type
        self.lightmap_brightness_scale = lightmap_brightness_scale
        self.perpendicular_brightness = perpendicular_brightness
        self.parallel_brightness = parallel_brightness
        self.reflection_cube_map = reflection_cube_map
