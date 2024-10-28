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

class ShaderTemplateFlags(Flag):
    force_active_camo = auto()
    water = auto()
    foliage = auto()
    hide_standard_parameters = auto()

class AuxLayerEnum(Enum):
    texaccum = 0
    environment_map = auto()
    self_illumination = auto()
    overlay = auto()
    transparent = auto()
    lightmap_indirect = auto()
    diffuse_specular = auto()
    shadow_generate = auto()
    shadow_apply = auto()
    bloom = auto()
    fog = auto()
    sh_prt = auto()
    active_camo = auto()
    water_edge_blend = auto()
    decal = auto()
    active_camo_stencil_modulate = auto()
    hologram = auto()
    light_albedo = auto()

class PropertyEnum(Enum):
    unused = 0
    diffuse_map = auto()
    lightmap_emissive_map = auto()
    lightmap_emissive_color = auto()
    lightmap_emissive_power = auto()
    lightmap_resolution_scale = auto()
    lightmap_half_life = auto()
    lightmap_diffuse_scale = auto()
    lightmap_alphatest_map = auto()
    lightmap_translucent_map = auto()
    lightmap_translucent_color = auto()
    lightmap_translucent_alpha = auto()
    active_camo_map = auto()
    lightmap_foliage_scale = auto()

class TypeEnum(Enum):
    bitmap = 0
    _value = auto()
    color = auto()
    switch = auto()

class ParameterFlags(Flag):
    animated = auto()
    hide_bitmap_reference = auto()

class BitmapEnum(Enum):
    _2d = 0
    _3d = auto()
    cubemap = auto()

class BitmapAnimationFlags(Flag):
    scale_uniform = auto()
    scale = auto()
    translation = auto()
    rotation = auto()
    index = auto()

class ShaderTemplateAsset():
    def __init__(self, header=None, body_header=None, documentation_tag_data=None, default_material_name="", default_material_name_length=0, flags=0, properties_header=None, 
                 properties_tag_block=None, properties=None, categories_header=None, categories_tag_block=None, categories=None, light_response=None, lods_header=None, 
                 lods_tag_block=None, lods=None, external_light_response_header=None, external_light_response_tag_block=None, external_light_response=None, 
                 external_light_response_byte_swap_header=None, external_light_response_byte_swap_tag_block=None, external_light_response_byte_swap=None, aux_1_shader=None, 
                 aux_1_layer=0, aux_2_shader=None, aux_2_layer=0, postprocess_definition_header=None, postprocess_definition_tag_block=None, postprocess_definition=None):
        self.header = header
        self.body_header = body_header
        self.documentation_tag_data = documentation_tag_data
        self.default_material_name = default_material_name
        self.default_material_name_length = default_material_name_length
        self.flags = flags
        self.properties_header = properties_header
        self.properties_tag_block = properties_tag_block
        self.properties = properties
        self.categories_header = categories_header
        self.categories_tag_block = categories_tag_block
        self.categories = categories
        self.light_response = light_response
        self.lods_header = lods_header
        self.lods_tag_block = lods_tag_block
        self.lods = lods
        self.external_light_response_header = external_light_response_header
        self.external_light_response_tag_block = external_light_response_tag_block
        self.external_light_response = external_light_response
        self.external_light_response_byte_swap_header = external_light_response_byte_swap_header
        self.external_light_response_byte_swap_tag_block = external_light_response_byte_swap_tag_block
        self.external_light_response_byte_swap = external_light_response_byte_swap
        self.aux_1_shader = aux_1_shader
        self.aux_1_layer = aux_1_layer
        self.aux_2_shader = aux_2_shader
        self.aux_2_layer = aux_2_layer
        self.postprocess_definition_header = postprocess_definition_header
        self.postprocess_definition_tag_block = postprocess_definition_tag_block
        self.postprocess_definition = postprocess_definition

    class Property:
        def __init__(self, property_type=0, name="", name_length=0):
            self.property_type = property_type
            self.name = name
            self.name_length = name_length

    class Category:
        def __init__(self, name="", name_length=0, parameters_tag_block=None, parameters_header=None, parameters=None):
            self.name = name
            self.name_length = name_length
            self.parameters_tag_block = parameters_tag_block
            self.parameters_header = parameters_header
            self.parameters = parameters

    class Parameter:
        def __init__(self, name="", name_length=0, explanation_tag_data=None, parameter_type=0, flags=0, default_bitmap=None, default_const_value=0.0, 
                     default_const_color=(0.0, 0.0, 0.0, 1.0), bitmap_type=0, bitmap_animation_flags=0, bitmap_scale=0):
            self.name = name
            self.name_length = name_length
            self.explanation_tag_data = explanation_tag_data
            self.parameter_type = parameter_type
            self.flags = flags
            self.default_bitmap = default_bitmap
            self.default_const_value = default_const_value
            self.default_const_color = default_const_color
            self.bitmap_type = bitmap_type
            self.bitmap_animation_flags = bitmap_animation_flags
            self.bitmap_scale = bitmap_scale
