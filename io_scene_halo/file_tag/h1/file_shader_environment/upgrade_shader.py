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

import os
import copy

from ....global_functions import tag_format
from .format import (
        ShaderAsset as H1ShaderAsset,
        MaterialTypeEnum as H1MaterialTypeEnum,
        EnvironmentFlags as H1EnvironmentFlags
        )

from ...h2.file_shader.format import (
        ShaderAsset,
        ShaderFlags,
        TypeEnum,
        ShaderLODBiasEnum,
        SpecularTypeEnum,
        LightmapTypeEnum,
        AnimationTypeEnum,
        FunctionTypeEnum,
        OutputTypeEnum,
        TransitionExponentEnum,
        PeriodicExponentEnum
        )

template_selction = [r"shaders\shader_templates\opaque\illum_opaque",
                    r"shaders\shader_templates\opaque\tex_bump",
                    r"shaders\shader_templates\opaque\tex_bump_dprs_env",
                    r"shaders\shader_templates\opaque\tex_bump_env_alpha_test",
                    r"shaders\shader_templates\opaque\tex_bump_dprs_env_illum",
                    r"shaders\shader_templates\opaque\tex_bump_env_illum_3_channel",
                    r"shaders\shader_templates\opaque\tex_bump_illum",
                    r"shaders\shader_templates\opaque\tex_bump_illum_3_channel"]

def conver_real_rgba_integer_bgra(material_color):
    return (round(material_color[2] * 255), round(material_color[1] * 255), round(material_color[0] * 255), 0)

def add_animation_property(SHADER, TAG, parameter, animation_type, function_type, output_value=OutputTypeEnum.scalar_intensity.value, material_color=(0, 0, 0, 0), lower_bound=0.0):
    animation_property = SHADER.AnimationProperty()

    animation_property.type = animation_type.value
    animation_property.input_name = ""
    animation_property.range_name = ""
    animation_property.map_property_header = TAG.TagBlockHeader("MAPP", 1, 1, 12)
    animation_property.function_type = function_type.value
    animation_property.input_function_data = SHADER.FunctionData()
    animation_property.range_function_data = SHADER.FunctionData()
    animation_property.range_check = output_value
    animation_property.lower_bound = lower_bound
    animation_property.upper_bound = 1
    animation_property.color_a = conver_real_rgba_integer_bgra(material_color)
    animation_property.color_b = (0, 0, 0, 0)
    animation_property.color_c = (0, 0, 0, 0)
    animation_property.color_d = (255, 255, 255, 0)

    parameter.animation_properties.append(animation_property)

def add_parameter(SHADER, TAG, parameter_name="", enum=TypeEnum.bitmap, bitmap_name="", float_value=1.0, rgba=(0.0, 0.0, 0.0, 1.0), replace_directory=True):
    parameter = SHADER.Parameter()

    path = bitmap_name
    new_directory = r"scenarios\bitmaps\solo\a10"
    if len(bitmap_name) > 0 and replace_directory:
        base_name = os.path.basename(bitmap_name).replace(" ", "_")
        path = os.path.join(new_directory, base_name)

    parameter.name = parameter_name
    parameter.type = enum.value
    parameter.bitmap = TAG.TagRef("bitm", path, len(path))
    parameter.const_value = float_value
    parameter.const_color = rgba
    parameter.animation_properties = []
    parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, 0, 28)
    parameter.animation_properties_tag_block = TAG.TagBlock()

    return parameter

def generate_illum_opaque(shader_body, TAG, SHADER):
    parameter = add_parameter(SHADER, TAG, parameter_name="self_illum_color", enum=TypeEnum.color, rgba=(1.0, 1.0, 1.0, 1.0))
    add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.color, FunctionTypeEnum.constant, 32, shader_body.color_of_emitted_light)

    parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
    parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
    SHADER.parameters.append(parameter)

def generate_tex_bump(shader_body, TAG, SHADER):
    if not shader_body.bump_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="bump_map", bitmap_name=shader_body.bump_map.name, float_value=0.0)
        if shader_body.bump_map_scale > 0.0:
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_x, FunctionTypeEnum.constant, lower_bound=shader_body.bump_map_scale)
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_y, FunctionTypeEnum.constant, lower_bound=shader_body.bump_map_scale)

        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    if not shader_body.base_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="base_map", bitmap_name=shader_body.base_map.name, float_value=0.0)
        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    if not shader_body.primary_detail_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="detail_map", bitmap_name=shader_body.primary_detail_map.name, float_value=0.0)
        if shader_body.primary_detail_map_scale > 0.0:
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_x, FunctionTypeEnum.constant, lower_bound=shader_body.primary_detail_map_scale)
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_y, FunctionTypeEnum.constant, lower_bound=shader_body.primary_detail_map_scale)

        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    add_parameter(SHADER, TAG, parameter_name="specular_color", enum=TypeEnum.color, float_value=0.0, rgba=shader_body.perpendicular_color)
    add_parameter(SHADER, TAG, parameter_name="specular_glancing_color", enum=TypeEnum.color, float_value=0.0, rgba=shader_body.parallel_color)

def generate_tex_bump_dprs_env(shader_body, TAG, SHADER):
    if not shader_body.bump_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="bump_map", bitmap_name=shader_body.bump_map.name, float_value=0.0)
        if shader_body.bump_map_scale > 0.0:
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_x, FunctionTypeEnum.constant, lower_bound=shader_body.bump_map_scale)
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_y, FunctionTypeEnum.constant, lower_bound=shader_body.bump_map_scale)

        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    if not shader_body.base_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="base_map", bitmap_name=shader_body.base_map.name, float_value=0.0)
        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    if not shader_body.primary_detail_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="detail_map", bitmap_name=shader_body.primary_detail_map.name, float_value=0.0)
        if shader_body.primary_detail_map_scale > 0.0:
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_x, FunctionTypeEnum.constant, lower_bound=shader_body.primary_detail_map_scale)
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_y, FunctionTypeEnum.constant, lower_bound=shader_body.primary_detail_map_scale)

        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    if not shader_body.reflection_cube_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="environment_map", bitmap_name=shader_body.reflection_cube_map.name, float_value=0.0)
        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="env_tint_color", enum=TypeEnum.color, rgba=shader_body.perpendicular_color))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="env_glancing_tint_color", enum=TypeEnum.color, rgba=shader_body.parallel_color))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="env_brightness", enum=TypeEnum._value, float_value=shader_body.perpendicular_brightness))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="env_glancing_brightness", enum=TypeEnum._value, float_value=shader_body.parallel_brightness))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="specular_color", enum=TypeEnum.color, float_value=0.0, rgba=shader_body.perpendicular_color))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="specular_glancing_color", enum=TypeEnum.color, float_value=0.0, rgba=shader_body.parallel_color))

def generate_tex_bump_env_alpha_test(shader_body, TAG, SHADER):
    if not shader_body.bump_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="bump_map", bitmap_name=shader_body.bump_map.name, float_value=0.0)
        if shader_body.bump_map_scale > 0.0:
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_x, FunctionTypeEnum.constant, lower_bound=shader_body.bump_map_scale)
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_y, FunctionTypeEnum.constant, lower_bound=shader_body.bump_map_scale)

        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

        alpha_test_map = copy.deepcopy(parameter)
        alpha_test_map.name = "alpha_test_map"
        SHADER.parameters.append(alpha_test_map)
        lightmap_alpha_test_map = copy.deepcopy(parameter)
        lightmap_alpha_test_map.name = "lightmap_alpha_test_map"
        SHADER.parameters.append(lightmap_alpha_test_map)

    if not shader_body.base_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="base_map", bitmap_name=shader_body.base_map.name, float_value=0.0)
        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    if not shader_body.primary_detail_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="detail_map", bitmap_name=shader_body.primary_detail_map.name, float_value=0.0)
        if shader_body.primary_detail_map_scale > 0.0:
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_x, FunctionTypeEnum.constant, lower_bound=shader_body.primary_detail_map_scale)
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_y, FunctionTypeEnum.constant, lower_bound=shader_body.primary_detail_map_scale)

        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    if not shader_body.reflection_cube_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="environment_map", bitmap_name=shader_body.reflection_cube_map.name, float_value=0.0)
        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="env_tint_color", enum=TypeEnum.color, rgba=shader_body.perpendicular_color))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="env_glancing_tint_color", enum=TypeEnum.color, rgba=shader_body.parallel_color))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="env_brightness", enum=TypeEnum._value, float_value=shader_body.perpendicular_brightness))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="env_glancing_brightness", enum=TypeEnum._value, float_value=shader_body.parallel_brightness))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="specular_color", enum=TypeEnum.color, float_value=0.0, rgba=shader_body.perpendicular_color))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="specular_glancing_color", enum=TypeEnum.color, float_value=0.0, rgba=shader_body.parallel_color))

def generate_tex_bump_dprs_env_illum(shader_body, TAG, SHADER):
    if not shader_body.bump_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="bump_map", bitmap_name=shader_body.bump_map.name, float_value=0.0)
        if shader_body.bump_map_scale > 0.0:
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_x, FunctionTypeEnum.constant, lower_bound=shader_body.bump_map_scale)
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_y, FunctionTypeEnum.constant, lower_bound=shader_body.bump_map_scale)

        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    if not shader_body.base_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="base_map", bitmap_name=shader_body.base_map.name, float_value=0.0)
        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    if not shader_body.primary_detail_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="detail_map", bitmap_name=shader_body.primary_detail_map.name, float_value=0.0)
        if shader_body.primary_detail_map_scale > 0.0:
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_x, FunctionTypeEnum.constant, lower_bound=shader_body.primary_detail_map_scale)
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_y, FunctionTypeEnum.constant, lower_bound=shader_body.primary_detail_map_scale)

        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    if not shader_body.reflection_cube_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="environment_map", bitmap_name=shader_body.reflection_cube_map.name, float_value=0.0)
        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="env_tint_color", enum=TypeEnum.color, rgba=shader_body.perpendicular_color))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="env_glancing_tint_color", enum=TypeEnum.color, rgba=shader_body.parallel_color))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="env_brightness", enum=TypeEnum._value, float_value=shader_body.perpendicular_brightness))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="env_glancing_brightness", enum=TypeEnum._value, float_value=shader_body.parallel_brightness))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="specular_color", enum=TypeEnum.color, float_value=0.0, rgba=shader_body.perpendicular_color))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="specular_glancing_color", enum=TypeEnum.color, float_value=0.0, rgba=shader_body.parallel_color))

    parameter = add_parameter(SHADER, TAG, parameter_name="self_illum_color", enum=TypeEnum.color, rgba=(1.0, 1.0, 1.0, 1.0))
    add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.color, FunctionTypeEnum.constant, 32, shader_body.color_of_emitted_light)

    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="emissive_color", enum=TypeEnum.color, rgba=shader_body.color_of_emitted_light))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="emissive_power", enum=TypeEnum._value, float_value=shader_body.power / 1000))

    parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
    parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
    SHADER.parameters.append(parameter)

def generate_tex_bump_env_illum_3_channel(shader_body, TAG, SHADER):
    if not shader_body.bump_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="bump_map", bitmap_name=shader_body.bump_map.name, float_value=0.0)
        if shader_body.bump_map_scale > 0.0:
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_x, FunctionTypeEnum.constant, lower_bound=shader_body.bump_map_scale)
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_y, FunctionTypeEnum.constant, lower_bound=shader_body.bump_map_scale)

        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    if not shader_body.base_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="base_map", bitmap_name=shader_body.base_map.name, float_value=0.0)
        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    if not shader_body.primary_detail_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="detail_map", bitmap_name=shader_body.primary_detail_map.name, float_value=0.0)
        if shader_body.primary_detail_map_scale > 0.0:
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_x, FunctionTypeEnum.constant, lower_bound=shader_body.primary_detail_map_scale)
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_y, FunctionTypeEnum.constant, lower_bound=shader_body.primary_detail_map_scale)

        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    if not shader_body.reflection_cube_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="environment_map", bitmap_name=shader_body.reflection_cube_map.name, float_value=0.0)
        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="env_tint_color", enum=TypeEnum.color, rgba=shader_body.perpendicular_color))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="env_glancing_tint_color", enum=TypeEnum.color, rgba=shader_body.parallel_color))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="env_brightness", enum=TypeEnum._value, float_value=shader_body.perpendicular_brightness))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="env_glancing_brightness", enum=TypeEnum._value, float_value=shader_body.parallel_brightness))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="specular_color", enum=TypeEnum.color, float_value=0.0, rgba=shader_body.perpendicular_color))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="specular_glancing_color", enum=TypeEnum.color, float_value=0.0, rgba=shader_body.parallel_color))

    if shader_body.power > 0:
        parameter = add_parameter(SHADER, TAG, parameter_name="self_illum_map", bitmap_name=shader_body.map.name, float_value=0.0)
        if shader_body.map_scale > 0.0:
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_x, FunctionTypeEnum.constant, lower_bound=shader_body.map_scale)
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_y, FunctionTypeEnum.constant, lower_bound=shader_body.map_scale)

        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)
        SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="lightmap_emmisive_map", bitmap_name=shader_body.map.name, float_value=0.0))

    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="emissive_color", enum=TypeEnum.color, rgba=shader_body.color_of_emitted_light))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="emissive_power", enum=TypeEnum._value, float_value=shader_body.power / 1000))

def generate_tex_bump_illum(shader_body, TAG, SHADER):
    if not shader_body.bump_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="bump_map", bitmap_name=shader_body.bump_map.name, float_value=0.0)
        if shader_body.bump_map_scale > 0.0:
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_x, FunctionTypeEnum.constant, lower_bound=shader_body.bump_map_scale)
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_y, FunctionTypeEnum.constant, lower_bound=shader_body.bump_map_scale)

        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    if not shader_body.base_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="base_map", bitmap_name=shader_body.base_map.name, float_value=0.0)
        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    if not shader_body.primary_detail_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="detail_map", bitmap_name=shader_body.primary_detail_map.name, float_value=0.0)
        if shader_body.primary_detail_map_scale > 0.0:
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_x, FunctionTypeEnum.constant, lower_bound=shader_body.primary_detail_map_scale)
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_y, FunctionTypeEnum.constant, lower_bound=shader_body.primary_detail_map_scale)

        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="specular_color", enum=TypeEnum.color, float_value=0.0, rgba=shader_body.perpendicular_color))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="specular_glancing_color", enum=TypeEnum.color, float_value=0.0, rgba=shader_body.parallel_color))

    parameter = add_parameter(SHADER, TAG, parameter_name="self_illum_color", enum=TypeEnum.color, rgba=(1.0, 1.0, 1.0, 1.0))
    add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.color, FunctionTypeEnum.constant, 32, shader_body.color_of_emitted_light)

    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="emissive_color", enum=TypeEnum.color, rgba=shader_body.color_of_emitted_light))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="emissive_power", enum=TypeEnum._value, float_value=shader_body.power / 1000))

    parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
    parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
    SHADER.parameters.append(parameter)

def generate_tex_bump_illum_3_channel(shader_body, TAG, SHADER):
    if not shader_body.bump_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="bump_map", bitmap_name=shader_body.bump_map.name, float_value=0.0)
        if shader_body.bump_map_scale > 0.0:
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_x, FunctionTypeEnum.constant, lower_bound=shader_body.bump_map_scale)
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_y, FunctionTypeEnum.constant, lower_bound=shader_body.bump_map_scale)

        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    if not shader_body.base_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="base_map", bitmap_name=shader_body.base_map.name, float_value=0.0)
        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    if not shader_body.primary_detail_map.name == "":
        parameter = add_parameter(SHADER, TAG, parameter_name="detail_map", bitmap_name=shader_body.primary_detail_map.name, float_value=0.0)
        if shader_body.primary_detail_map_scale > 0.0:
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_x, FunctionTypeEnum.constant, lower_bound=shader_body.primary_detail_map_scale)
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_y, FunctionTypeEnum.constant, lower_bound=shader_body.primary_detail_map_scale)

        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="specular_color", enum=TypeEnum.color, float_value=0.0, rgba=shader_body.perpendicular_color))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="specular_glancing_color", enum=TypeEnum.color, float_value=0.0, rgba=shader_body.parallel_color))

    if shader_body.power > 0:
        parameter = add_parameter(SHADER, TAG, parameter_name="self_illum_map", bitmap_name=shader_body.map.name, float_value=0.0)
        if shader_body.map_scale > 0.0:
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_x, FunctionTypeEnum.constant, lower_bound=shader_body.map_scale)
            add_animation_property(SHADER, TAG, parameter, AnimationTypeEnum.bitmap_scale_y, FunctionTypeEnum.constant, lower_bound=shader_body.map_scale)

        parameter.animation_properties_tag_block_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)
        SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="lightmap_emmisive_map", bitmap_name=shader_body.map.name, float_value=0.0))

    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="emissive_color", enum=TypeEnum.color, rgba=shader_body.color_of_emitted_light))
    SHADER.parameters.append(add_parameter(SHADER, TAG, parameter_name="emissive_power", enum=TypeEnum._value, float_value=shader_body.power / 1000))

def generate_parameters(shader_body, TAG, SHADER, template_index):
    if template_index == 0:
        generate_illum_opaque(shader_body, TAG, SHADER)

    elif template_index == 1:
        generate_tex_bump(shader_body, TAG, SHADER)

    elif template_index == 2:
        generate_tex_bump_dprs_env(shader_body, TAG, SHADER)

    elif template_index == 3:
        generate_tex_bump_env_alpha_test(shader_body, TAG, SHADER)

    elif template_index == 4:
        generate_tex_bump_dprs_env_illum(shader_body, TAG, SHADER)

    elif template_index == 5:
        generate_tex_bump_env_illum_3_channel(shader_body, TAG, SHADER)

    elif template_index == 6:
        generate_tex_bump_illum(shader_body, TAG, SHADER)

    elif template_index == 7:
        generate_tex_bump_illum_3_channel(shader_body, TAG, SHADER)

    parameter_count = len(SHADER.parameters)
    SHADER.parameters_header = TAG.TagBlockHeader("tbfd", 0, parameter_count, 52)

    return TAG.TagBlock(parameter_count)

def get_template(H1_ASSET):
    shader_template = 0
    if not H1_ASSET.shader_body.base_map.name == "":
        shader_template = 1
        if not H1_ASSET.shader_body.reflection_cube_map.name == "":
            shader_template = 2
            if H1EnvironmentFlags.alpha_tested in H1EnvironmentFlags(H1_ASSET.shader_body.environment_flags):
                shader_template = 3

            else:
                if H1_ASSET.shader_body.power > 0.0:
                    shader_template = 4
                    if not H1_ASSET.shader_body.map.name == "":
                        shader_template = 5

        else:
            if H1_ASSET.shader_body.power > 0.0:
                shader_template = 6
                if not H1_ASSET.shader_body.map.name == "":
                    shader_template = 7

    return shader_template

def get_material_name(material_type):
    h1_material = H1MaterialTypeEnum(material_type)
    h2_name = ""
    if h1_material == H1MaterialTypeEnum.dirt:
        h2_name = "tough_terrain_dirt"
    elif h1_material == H1MaterialTypeEnum.sand:
        h2_name = "tough_terrain_sand"
    elif h1_material == H1MaterialTypeEnum.stone:
        h2_name = "hard_terrain_stone"
    elif h1_material == H1MaterialTypeEnum.snow:
        h2_name = "soft_terrain_snow"
    elif h1_material == H1MaterialTypeEnum.wood:
        h2_name = "tough_organic_wood"
    elif h1_material == H1MaterialTypeEnum.metal_hollow:
        h2_name = "hard_metal_solid"
    elif h1_material == H1MaterialTypeEnum.metal_thin:
        h2_name = "hard_metal_thin"
    elif h1_material == H1MaterialTypeEnum.metal_thick:
        h2_name = "hard_metal_thick"
    elif h1_material == H1MaterialTypeEnum.rubber:
        h2_name = "tough_inorganic_rubber"
    elif h1_material == H1MaterialTypeEnum.glass:
        h2_name = "brittle_glass"
    elif h1_material == H1MaterialTypeEnum.force_field:
        h2_name = "energy_shield_invincible"
    elif h1_material == H1MaterialTypeEnum.grunt:
        h2_name = "soft_organic_flesh_grunt"
    elif h1_material == H1MaterialTypeEnum.hunter_armor:
        h2_name = "hard_metal_solid_cov_hunter"
    elif h1_material == H1MaterialTypeEnum.hunter_skin:
        h2_name = "soft_organic_flesh_hunter"
    elif h1_material == H1MaterialTypeEnum.elite:
        h2_name = "soft_organic_flesh_elite"
    elif h1_material == H1MaterialTypeEnum.jackal:
        h2_name = "soft_organic_flesh_jackal"
    elif h1_material == H1MaterialTypeEnum.jackal_energy_shield:
        h2_name = "energy_shield_thick_cov_jackal"
    elif h1_material == H1MaterialTypeEnum.engineer_skin:
        h2_name = "soft_organic_flesh_elite"
    elif h1_material == H1MaterialTypeEnum.enngineer_force_field:
        h2_name = "energy_shield_thick_cov_jackal"
    elif h1_material == H1MaterialTypeEnum.flood_combat_form:
        h2_name = "tough_floodflesh_combatform"
    elif h1_material == H1MaterialTypeEnum.flood_carrier_form:
        h2_name = "tough_floodflesh_carrierform"
    elif h1_material == H1MaterialTypeEnum.cyborg_armor:
        h2_name = "hard_metal_thin_hum_masterchief"
    elif h1_material == H1MaterialTypeEnum.cyborg_energy_shield:
        h2_name = "energy_shield_thin_hum_masterchief"
    elif h1_material == H1MaterialTypeEnum.human_armor:
        h2_name = "tough_inorganic_armor_hum"
    elif h1_material == H1MaterialTypeEnum.human_skin:
        h2_name = "soft_organic_flesh_human"
    elif h1_material == H1MaterialTypeEnum.sentinel:
        h2_name = "hard_metal_thin_for_sentinel_aggressor"
    elif h1_material == H1MaterialTypeEnum.monitor:
        h2_name = "hard_metal_thin_for_monitor"
    elif h1_material == H1MaterialTypeEnum.plastic:
        h2_name = "tough_inorganic_plastic"
    elif h1_material == H1MaterialTypeEnum.water:
        h2_name = "liquid_thin_water"
    elif h1_material == H1MaterialTypeEnum.leaves:
        h2_name = "soft_organic_plant_leafy"
    elif h1_material == H1MaterialTypeEnum.elite_energy_shield:
        h2_name = "energy_shield_thin_cov_elite"
    elif h1_material == H1MaterialTypeEnum.ice:
        h2_name = "hard_terrain_ice"
    elif h1_material == H1MaterialTypeEnum.hunter_shield:
        h2_name = "hard_metal_solid_cov_hunter"

    return h2_name

def upgrade_h2_shader(H1_ASSET, patch_txt_path, report):
    TAG = tag_format.TagAsset()
    SHADER = ShaderAsset()
    TAG.upgrade_patches = tag_format.get_patch_set(patch_txt_path)

    SHADER.header = TAG.Header()
    SHADER.header.unk1 = 0
    SHADER.header.flags = 0
    SHADER.header.type = 0
    SHADER.header.name = ""
    SHADER.header.tag_group = "shad"
    SHADER.header.checksum = 0
    SHADER.header.data_offset = 64
    SHADER.header.data_length = 0
    SHADER.header.unk2 = 0
    SHADER.header.version = 1
    SHADER.header.destination = 0
    SHADER.header.plugin_handle = -1
    SHADER.header.engine_tag = "BLM!"

    SHADER.runtime_properties = []
    SHADER.parameters = []
    SHADER.postprocess_definition = []
    SHADER.predicted_resources = []
    SHADER.postprocess_properties = []

    template_index = get_template(H1_ASSET)
    template_path = template_selction[template_index]

    SHADER.shader_body_header = TAG.TagBlockHeader("tbfd", 0, 1, 128)
    SHADER.shader_body = SHADER.ShaderBody()
    SHADER.shader_body.template = TAG.TagRef("stem", template_path, len(template_path))
    SHADER.shader_body.material_name = get_material_name(H1_ASSET.shader_body.material_type)
    SHADER.shader_body.runtime_properties = TAG.TagBlock()
    SHADER.shader_body.flags = 0
    SHADER.shader_body.parameters = generate_parameters(H1_ASSET.shader_body, TAG, SHADER, template_index)
    SHADER.shader_body.postprocess_definition = TAG.TagBlock()
    SHADER.shader_body.predicted_resources = TAG.TagBlock()
    SHADER.shader_body.light_response = TAG.TagRef("slit")
    SHADER.shader_body.shader_lod_bias = 0
    SHADER.shader_body.specular_type = SpecularTypeEnum.default.value
    SHADER.shader_body.lightmap_type = LightmapTypeEnum.diffuse.value
    SHADER.shader_body.lightmap_specular_brightness = 1.0
    SHADER.shader_body.lightmap_ambient_bias = 0.0
    SHADER.shader_body.postprocess_properties = TAG.TagBlock()
    SHADER.shader_body.added_depth_bias_offset = 0.0
    SHADER.shader_body.added_depth_bias_slope = 0.0

    return SHADER
