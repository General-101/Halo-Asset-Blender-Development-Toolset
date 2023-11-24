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

class ChicagoFlags(Flag):
    alpha_tested = auto()
    decal = auto()
    two_sided = auto()
    first_map_is_in_screenspace = auto()
    draw_before_water = auto()
    ignore_effect = auto()
    scale_first_map_with_distance = auto()
    numeric = auto()

class FirstMapTypeEnum(Enum):
    _2d_map = 0
    first_map_is_reflection_cube_map = auto()
    first_map_is_object_centered_cube_map = auto()
    first_map_is_viewer_centered_cube_map = auto()

class FramebufferBlendFunctionEnum(Enum):
    alpha_blend = 0
    multiply = auto()
    double_multiply = auto()
    add = auto()
    subtract = auto()
    component_min = auto()
    component_max = auto()
    alpha_multiply_add = 0

class FramebufferFadeModeEnum(Enum):
    none = 0
    fade_when_perpendicular = auto()
    fade_when_parallel = auto()

class ChannelSourceEnum(Enum):
    none = 0
    a_out = auto()
    b_out = auto()
    c_out = auto()
    d_out = auto()

class MapFlags(Flag):
    unfiltered = auto()
    alpha_replicate = auto()
    u_clamped = auto()
    v_clamped = auto()

class MapFunctionEnum(Enum):
    current = 0
    next_map = auto()
    multiply = auto()
    double_multiply = auto()
    add = auto()
    add_signed_current = auto()
    add_signed_next_map = auto()
    subtract_current = auto()
    subtract_next_map = auto()
    blend_current_alpha = auto()
    blend_current_alpha_inverse = auto()
    blend_next_map_alpha = auto()
    blend_next_map_alpha_inverse = auto()

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

class ExtraFlags(Flag):
    dont_fade_active_camouflage = auto()
    numeric_countdown_timer = auto()
    custom_edition_blending = auto()

class ShaderAsset():
    def __init__(self):
        self.header = None
        self.shader_body = None
        self.extra_layers = None
        self._4_stage_maps = None
        self._2_stage_maps = None

    class ShaderBody:
        def __init__(self, radiosity_flags=0, detail_level=0, power=0.0, color_of_emitted_light=(0.0, 0.0, 0.0, 1.0), light_tint_color=(0.0, 0.0, 0.0, 1.0), material_type=0, 
                     numeric_counter_limit=0, chicago_flags=0, first_map_type=0, framebuffer_blend_function=0, framebuffer_fade_mode=0, framebuffer_fade_source=0, 
                     lens_flare_spacing=0.0, lens_flare=None, extra_layers_tag_block=None, _4_stage_maps_tag_block=None, _2_stage_maps_tag_block=None, extra_flags=0):
            self.radiosity_flags = radiosity_flags
            self.detail_level = detail_level
            self.power = power
            self.color_of_emitted_light = color_of_emitted_light
            self.light_tint_color = light_tint_color
            self.material_type = material_type
            self.numeric_counter_limit = numeric_counter_limit
            self.chicago_flags = chicago_flags
            self.first_map_type = first_map_type
            self.framebuffer_blend_function = framebuffer_blend_function
            self.framebuffer_fade_mode = framebuffer_fade_mode
            self.framebuffer_fade_source = framebuffer_fade_source
            self.lens_flare_spacing = lens_flare_spacing
            self.lens_flare = lens_flare
            self.extra_layers_tag_block = extra_layers_tag_block
            self._4_stage_maps_tag_block = _4_stage_maps_tag_block
            self._2_stage_maps_tag_block = _2_stage_maps_tag_block
            self.extra_flags = extra_flags

    class Stage:
        def __init__(self, flags=0, color_function=0, alpha_function=0, map_u_scale=0.0, map_v_scale=0.0, map_u_offset=0.0, map_v_offset=0.0, map_rotation=0.0, mipmap_bias=0.0, 
                     map=None, u_animation_source=0, u_animation_function=0, u_animation_period=0.0, u_animation_phase=0.0, u_animation_scale=0.0, v_animation_source=0, 
                     v_animation_function=0, v_animation_period=0.0, v_animation_phase=0.0, v_animation_scale=0.0, rotation_animation_source=0, rotation_animation_function=0, 
                     rotation_animation_period=0.0, rotation_animation_phase=0.0, rotation_animation_scale=0.0, rotation_animation_center=(0.0, 0.0)):
            self.flags = flags
            self.color_function = color_function
            self.alpha_function = alpha_function
            self.map_u_scale = map_u_scale
            self.map_v_scale = map_v_scale
            self.map_u_offset = map_u_offset
            self.map_v_offset = map_v_offset
            self.map_rotation = map_rotation
            self.mipmap_bias = mipmap_bias
            self.map = map
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