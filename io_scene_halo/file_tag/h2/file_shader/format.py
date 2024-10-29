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
from ....file_tag.h2.file_functions.format import Function

class ShaderFlags(Flag):
    water = auto()
    sort_first = auto()
    no_active_camo = auto()

class ShaderLODBiasEnum(Enum):
    none = 0
    four_times_size = auto()
    two_times_size = auto()
    half_size = auto()
    quarter_size = auto()
    never = auto()
    cinematic = auto()
    lowest = auto()

class SpecularTypeEnum(Enum):
    none = 0
    default = auto()
    dull = auto()
    shiny = auto()

class LightmapTypeEnum(Enum):
    diffuse = 0
    default_specular = auto()
    dull_specular = auto()
    shiny_specular = auto()

class TypeEnum(Enum):
    bitmap = 0
    _value = auto()
    color = auto()
    switch = auto()

class AnimationTypeEnum(Enum):
    bitmap_scale_uniform = 0
    bitmap_scale_x = auto()
    bitmap_scale_y = auto()
    bitmap_scale_z = auto()
    bitmap_translation_x = auto()
    bitmap_translation_y = auto()
    bitmap_translation_z = auto()
    bitmap_rotation_angle = auto()
    bitmap_rotation_axis_x = auto()
    bitmap_rotation_axis_y = auto()
    bitmap_rotation_axis_z = auto()
    _value = auto()
    color = auto()
    bitmap_index = auto()

class FunctionTypeEnum(Enum):
    identity = 0
    constant = auto()
    transition = auto()
    periodic = auto()
    linear = auto()
    linear_key = auto()
    multi_linear_key = auto()
    spline = auto()
    multi_spline = auto()
    exponent = auto()
    spline2 = auto()

class OutputTypeFlags(Flag):
    range = auto()
    _2_color = 32
    _3_color = 48
    _4_color = 64

class TransitionExponentEnum(Enum):
    linear = 0
    early = auto()
    very_early = auto()
    late = auto()
    very_late = auto()
    cosine = auto()
    one = auto()
    zero = auto()

class PeriodicExponentEnum(Enum):
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

class ShaderAsset():
    def __init__(self, header=None, body_header=None, runtime_properties_header=None, runtime_properties=None, parameters_header=None, parameters=None, 
                 postprocess_definition_header=None, postprocess_definition=None, predicted_resources_header=None, predicted_resources=None, 
                 postprocess_properties_header=None, postprocess_properties=None, template=None, material_name="", material_name_length=0, runtime_properties_tag_block=None, 
                 flags=0, parameters_tag_block=None, postprocess_definition_tag_block=None, predicted_resources_tag_block=None, light_response=None, shader_lod_bias=0, 
                 specular_type=0, lightmap_type=0, lightmap_specular_brightness=0.0, lightmap_ambient_bias=0.0, postprocess_properties_tag_block=None, 
                 added_depth_bias_offset=0.0, added_depth_bias_slope=0.0):
        self.header = header
        self.body_header = body_header
        self.runtime_properties_header = runtime_properties_header
        self.runtime_properties = runtime_properties
        self.parameters_header = parameters_header
        self.parameters = parameters
        self.postprocess_definition_header = postprocess_definition_header
        self.postprocess_definition = postprocess_definition
        self.predicted_resources_header = predicted_resources_header
        self.predicted_resources = predicted_resources
        self.postprocess_properties_header = postprocess_properties_header
        self.postprocess_properties = postprocess_properties
        self.template = template
        self.material_name = material_name
        self.material_name_length = material_name_length
        self.runtime_properties_tag_block = runtime_properties_tag_block
        self.flags = flags
        self.parameters_tag_block = parameters_tag_block
        self.postprocess_definition_tag_block = postprocess_definition_tag_block
        self.predicted_resources_tag_block = predicted_resources_tag_block
        self.light_response = light_response
        self.shader_lod_bias = shader_lod_bias
        self.specular_type = specular_type
        self.lightmap_type = lightmap_type
        self.lightmap_specular_brightness = lightmap_specular_brightness
        self.lightmap_ambient_bias = lightmap_ambient_bias
        self.postprocess_properties_tag_block = postprocess_properties_tag_block
        self.added_depth_bias_offset = added_depth_bias_offset
        self.added_depth_bias_slope = added_depth_bias_slope

    class RuntimeProperty:
        def __init__(self, diffuse_map=None, lightmap_emissive_map=None, lightmap_emissive_color=(0.0, 0.0, 0.0, 1.0), lightmap_emissive_power=0.0, lightmap_resolution_scale=0.0,
                     lightmap_half_life=0.0, lightmap_diffuse_scale=0.0, alphatest_map=None, translucent_map=None, lightmap_transparent_color=(0.0, 0.0, 0.0, 1.0),
                     lightmap_transparent_alpha=0.0, lightmap_foliage_scale=0.0):
            self.diffuse_map = diffuse_map
            self.lightmap_emissive_map = lightmap_emissive_map
            self.lightmap_emissive_color = lightmap_emissive_color
            self.lightmap_emissive_power = lightmap_emissive_power
            self.lightmap_resolution_scale = lightmap_resolution_scale
            self.lightmap_half_life = lightmap_half_life
            self.lightmap_diffuse_scale = lightmap_diffuse_scale
            self.alphatest_map = alphatest_map
            self.translucent_map = translucent_map
            self.lightmap_transparent_color = lightmap_transparent_color
            self.lightmap_transparent_alpha = lightmap_transparent_alpha
            self.lightmap_foliage_scale = lightmap_foliage_scale

    class Parameter:
        def __init__(self, name="", name_length=0, type=0, bitmap=None, const_value=0.0, const_color=(0.0, 0.0, 0.0, 1.0), animation_properties_tag_block=None,
                     animation_properties_header=None, animation_properties=None):
            self.name = name
            self.name_length = name_length
            self.type = type
            self.bitmap = bitmap
            self.const_value = const_value
            self.const_color = const_color
            self.animation_properties_tag_block = animation_properties_tag_block
            self.animation_properties_header = animation_properties_header
            self.animation_properties = animation_properties

    class AnimationProperty(Function):
        def __init__(self, type=0, input_name="", input_name_length=0, input_type=0, range_name="", range_name_length=0, range_type=0, time_period=0.0, output_modifier=0,
                     output_modifier_input=0):
            super().__init__()
            self.type = type
            self.input_name = input_name
            self.input_name_length = input_name_length
            self.input_type = input_type
            self.range_name = range_name
            self.range_name_length = range_name_length
            self.range_type = range_type
            self.time_period = time_period
            self.output_modifier = output_modifier
            self.output_modifier_input = output_modifier_input

    class FunctionData:
        def __init__(self, min=0.0, max=1.0, exponent=0, frequency=1.0, phase=0.0, points=None):
            self.min = min
            self.max = max
            self.exponent = exponent
            self.frequency = frequency
            self.phase = phase
            self.points = points
