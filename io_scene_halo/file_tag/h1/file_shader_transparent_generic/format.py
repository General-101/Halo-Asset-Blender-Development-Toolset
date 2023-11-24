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

class GenericFlags(Flag):
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
    reflection_cube_map = auto()
    object_centered_cube_map = auto()
    viewer_centered_cube_map = auto()

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
    u_clamped = auto()
    v_clamped = auto()

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

class StageFlags(Flag):
    color_max = auto()
    alpha_max = auto()
    a_out_controls_color0_animation = auto()

class ColorSourceEnum(Enum):
    none = 0
    a = auto()
    b = auto()
    c = auto()
    d = auto()

class ColorInputEnum(Enum):
    zero = 0
    one = auto()
    one_half = auto()
    negative_one = auto()
    negative_one_half = auto()
    map_color_0 = auto()
    map_color_1 = auto()
    map_color_2 = auto()
    map_color_3 = auto()
    vertex_color0_divided_by_diffuse_light = auto()
    vertex_color1_divided_by_fade_perpendicular = auto()
    scratch_color_0 = auto()
    scratch_color_1 = auto()
    constant_color_0 = auto()
    constant_color_1 = auto()
    map_alpha_0 = auto()
    map_alpha_1 = auto()
    map_alpha_2 = auto()
    map_alpha_3 = auto()
    vertex_alpha_0_divided_by_fade_none = auto()
    vertex_alpha_1_divided_by_fade_perpendicular = auto()
    scratch_alpha_0 = auto()
    scratch_alpha_1 = auto()
    constant_alpha_0 = auto()
    constant_alpha_1 = auto()

class InputMappingEnum(Enum):
    clamp_x = 0
    one_minus_clamp_x = auto()
    two_times_clamp_x_minus_one = auto()
    one_minus_two_times_clamp_x = auto()
    clamp_x_minus_one_divided_by_two = auto()
    one_divided_by_two_minus_clamp_x = auto()
    x = auto()
    negative_x = auto()

class ColorOutputEnum(Enum):
    discard = 0
    scratch_color0_divided_by_final_color = auto()
    scratch_color1 = auto()
    vertex_color0 = auto()
    vertex_color1 = auto()
    map_color_0 = auto()
    map_color_1 = auto()
    map_color_2 = auto()
    map_color_3 = auto()

class ColorOutputFunctionEnum(Enum):
    multiply = 0
    dot_product = auto()

class OutputMappingEnum(Enum):
    identity = 0
    scale_by_half = auto()
    scale_by_two = auto()
    scale_by_four = auto()
    bias_by_negative_half = auto()
    expand_normal = auto()

class AlphaInputEnum(Enum):
    zero = 0
    one = auto()
    one_half = auto()
    negative_one = auto()
    negative_one_half = auto()
    map_alpha_0 = auto()
    map_alpha_1 = auto()
    map_alpha_2 = auto()
    map_alpha_3 = auto()
    vertex_alpha0_divided_by_fade_none = auto()
    vertex_alpha1_divided_by_fade_perpendicular = auto()
    scratch_alpha_0 = auto()
    scratch_alpha_1 = auto()
    constant_alpha_0 = auto()
    constant_alpha_1 = auto()
    map_blue_0 = auto()
    map_blue_1 = auto()
    map_blue_2 = auto()
    map_blue_3 = auto()
    vertex_blue_0_divided_by_blue_light = auto()
    vertex_blue_1_divided_by_fade_parellel = auto()
    scratch_blue_0 = auto()
    scratch_blue_1 = auto()
    constant_blue_0 = auto()
    constant_blue_1 = auto()

class AlphaOutputEnum(Enum):
    discard = 0
    scratch_alpha0_divided_by_final_alpha = auto()
    scratch_alpha1 = auto()
    vertex_alpha0_divided_by_fog = auto()
    vertex_alpha1 = auto()
    map_alpha_0 = auto()
    map_alpha_1 = auto()
    map_alpha_2 = auto()
    map_alpha_3 = auto()

class ShaderAsset():
    def __init__(self):
        self.header = None
        self.shader_body = None
        self.extra_layers = None
        self.maps = None
        self.stages = None

    class ShaderBody:
        def __init__(self, radiosity_flags=0, detail_level=0, power=0.0, color_of_emitted_light=(0.0, 0.0, 0.0, 1.0), light_tint_color=(0.0, 0.0, 0.0, 1.0), material_type=0, 
                     numeric_counter_limit=0, chicago_flags=0, first_map_type=0, framebuffer_blend_function=0, framebuffer_fade_mode=0, framebuffer_fade_source=0, 
                     lens_flare_spacing=0.0, lens_flare=None, extra_layers_tag_block=None, maps_tag_block=None, stages_tag_block=None):
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
            self.maps_tag_block = maps_tag_block
            self.stages_tag_block = stages_tag_block

    class Map:
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

    class Stage:
        def __init__(self, flags=0, color0_source=0, color0_animation_function=0, color0_animation_period=0.0, color0_animation_lower_bound=(0.0, 0.0, 0.0, 1.0), 
                     color0_animation_upper_bound=(0.0, 0.0, 0.0, 1.0), color1=(0.0, 0.0, 0.0, 1.0), color_input_a=0, color_input_a_mapping=0, color_input_b=0, color_input_b_mapping=0, 
                     color_input_c=0, color_input_c_mapping=0, color_input_d=0, color_input_d_mapping=0, color_output_ab=0, color_output_ab_function=0, color_output_cd=0, 
                     color_output_cd_function=0, color_output_ab_cd=0, color_output_mapping=0, alpha_input_a=0, alpha_input_a_mapping=0, alpha_input_b=0, alpha_input_b_mapping=0, 
                     alpha_input_c=0, alpha_input_c_mapping=0, alpha_input_d=0, alpha_input_d_mapping=0, alpha_output_ab=0, alpha_output_cd=0, alpha_output_ab_cd=0, 
                     alpha_output_mapping=0):
            self.flags = flags
            self.color0_source = color0_source
            self.color0_animation_function = color0_animation_function
            self.color0_animation_period = color0_animation_period
            self.color0_animation_lower_bound = color0_animation_lower_bound
            self.color0_animation_upper_bound = color0_animation_upper_bound
            self.color1 = color1
            self.color_input_a = color_input_a
            self.color_input_a_mapping = color_input_a_mapping
            self.color_input_b = color_input_b
            self.color_input_b_mapping = color_input_b_mapping
            self.color_input_c = color_input_c
            self.color_input_c_mapping = color_input_c_mapping
            self.color_input_d = color_input_d
            self.color_input_d_mapping = color_input_d_mapping
            self.color_output_ab = color_output_ab
            self.color_output_ab_function = color_output_ab_function
            self.color_output_cd = color_output_cd
            self.color_output_cd_function = color_output_cd_function
            self.color_output_ab_cd = color_output_ab_cd
            self.color_output_mapping = color_output_mapping
            self.alpha_input_a = alpha_input_a
            self.alpha_input_a_mapping = alpha_input_a_mapping
            self.alpha_input_b = alpha_input_b
            self.alpha_input_b_mapping = alpha_input_b_mapping
            self.alpha_input_c = alpha_input_c
            self.alpha_input_c_mapping = alpha_input_c_mapping
            self.alpha_input_d = alpha_input_d
            self.alpha_input_d_mapping = alpha_input_d_mapping
            self.alpha_output_ab = alpha_output_ab
            self.alpha_output_cd = alpha_output_cd
            self.alpha_output_ab_cd = alpha_output_ab_cd
            self.alpha_output_mapping = alpha_output_mapping
