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

class ShaderFlags(Flag):
    water = auto()
    sort_first = auto()
    no_active_camo = auto()

class TypeEnum(Enum):
    bitmap = 0
    _value = auto()
    color = auto()
    switch = auto()

class ShaderLODBiasEnum(Enum):
    none = 0
    four_times_size = auto()
    two_times_size = auto()
    one_and_a_half_size = auto()
    one_fourth_size = auto()
    never = auto()
    cinematic = auto()
    lowest = auto()

class SpecularTypeEnum(Enum):
    none = 0
    default = auto()
    dull = auto()
    shiney = auto()

class LightmapTypeEnum(Enum):
    diffuse = 0
    default_specular = auto()
    dull_specular = auto()
    shiny_specular = auto()

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
    value = auto()
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

class OutputTypeEnum(Enum):
    scalar_intensity = 0

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
    def __init__(self):
        self.header = None
        self.shader_body_header = None
        self.shader_body = None
        self.runtime_properties_header = None
        self.runtime_properties = None
        self.parameters_header = None
        self.parameters = None
        self.postprocess_definition_header = None
        self.postprocess_definition = None
        self.predicted_resources_header = None
        self.predicted_resources = None
        self.postprocess_properties_header = None
        self.postprocess_properties = None

    class ShaderBody:
        def __init__(self, template=None, material_name="", runtime_properties=None, flags=0, parameters=None, postprocess_definition=None, predicted_resources=None,
                     light_response=None, shader_lod_bias=0, specular_type=0, lightmap_type=0, lightmap_specular_brightness=0.0, lightmap_ambient_bias=0.0,
                     postprocess_properties=None, added_depth_bias_offset=0.0, added_depth_bias_slope=0.0):
            self.template = template
            self.material_name = material_name
            self.runtime_properties = runtime_properties
            self.flags = flags
            self.parameters = parameters
            self.postprocess_definition = postprocess_definition
            self.predicted_resources = predicted_resources
            self.light_response = light_response
            self.shader_lod_bias = shader_lod_bias
            self.specular_type = specular_type
            self.lightmap_type = lightmap_type
            self.lightmap_specular_brightness = lightmap_specular_brightness
            self.lightmap_ambient_bias = lightmap_ambient_bias
            self.postprocess_properties = postprocess_properties
            self.added_depth_bias_offset = added_depth_bias_offset
            self.added_depth_bias_slope = added_depth_bias_slope

    class Parameter:
        def __init__(self, name="", type=0, bitmap=None, const_value=0.0, const_color=(0.0, 0.0, 0.0, 1.0), animation_properties_tag_block_header=None,
                     animation_properties_tag_block=None, animation_properties=None):
            self.name = name
            self.type = type
            self.bitmap = bitmap
            self.const_value = const_value
            self.const_color = const_color
            self.animation_properties_tag_block_header = animation_properties_tag_block_header
            self.animation_properties_tag_block = animation_properties_tag_block
            self.animation_properties = animation_properties

    class AnimationProperty:
        def __init__(self, type=0, input_name="", range_name="", time_period=0.0, map_property_header=None, function_type=0, input_function_data=None,
                     range_check=False, range_function_data=None, output_type=0, x=0.0, y=0.0, upper_bound=1.0, lower_bound=0.0, color_a=(0.0, 0.0, 0.0, 1.0),
                     color_b=(0.0, 0.0, 0.0, 1.0), color_c=(0.0, 0.0, 0.0, 1.0), color_d=(0.0, 0.0, 0.0, 1.0)):
            self.type = type
            self.input_name = input_name
            self.range_name = range_name
            self.time_period = time_period
            self.map_property_header = map_property_header
            self.function_type = function_type
            self.input_function_data = input_function_data
            self.range_check = range_check
            self.range_function_data = range_function_data
            self.output_type = output_type
            self.x = x
            self.y = y
            self.upper_bound = upper_bound
            self.lower_bound = lower_bound
            self.color_a = color_a
            self.color_b = color_b
            self.color_c = color_c
            self.color_d = color_d

    class FunctionData:
        def __init__(self, min=0.0, max=1.0, exponent=0, frequency=1.0, phase=0.0):
            self.min = min
            self.max = max
            self.exponent = exponent
            self.frequency = frequency
            self.phase = phase
