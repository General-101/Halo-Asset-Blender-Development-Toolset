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

from ....global_functions import tag_format, shader_processing
from .format import (
        ShaderAsset as H1ShaderAsset,
        MaterialTypeEnum as H1MaterialTypeEnum,
        EnvironmentFlags as H1EnvironmentFlags,
        EnvironmentTypeEnum,
        DiffuseFlags
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
        TransitionExponentEnum,
        PeriodicExponentEnum,
        OutputTypeFlags
        )

def generate_base_map_parameters(H1_ASSET, TAG, SHADER, template, permutation_index):
    parameter = shader_processing.add_parameter(SHADER, TAG, parameter_name="base_map", bitmap_name=H1_ASSET.shader_body.base_map.name, float_value=0.0)
    parameter.animation_properties = []
    parameter.animation_properties_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
    parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
    SHADER.parameters.append(parameter)

    parameter_count = len(SHADER.parameters)
    SHADER.parameters_header = TAG.TagBlockHeader("tbfd", 0, parameter_count, 52)

    return TAG.TagBlock(parameter_count)

def generate_detail_map_parameters(H1_ASSET, TAG, SHADER, template, permutation_index):
    base_bitmap = H1_ASSET.shader_body.base_map.parse_tag(print, "halo1", "retail")
    primary_detail_bitmap = H1_ASSET.shader_body.primary_detail_map.parse_tag(print, "halo1", "retail")
    secondary_detail_bitmap = H1_ASSET.shader_body.secondary_detail_map.parse_tag(print, "halo1", "retail")
    micro_detail_bitmap = H1_ASSET.shader_body.micro_detail_map.parse_tag(print, "halo1", "retail")

    base_bitmap_count = 0
    primary_detail_bitmap_count = 0
    secondary_detail_bitmap_count = 0
    micro_detail_bitmap_count = 0
    if base_bitmap:
        base_bitmap_count = len(base_bitmap.bitmaps)
    if primary_detail_bitmap:
        primary_detail_bitmap_count = len(primary_detail_bitmap.bitmaps)
    if secondary_detail_bitmap:
        secondary_detail_bitmap_count = len(secondary_detail_bitmap.bitmaps)
    if micro_detail_bitmap:
        micro_detail_bitmap_count = len(micro_detail_bitmap.bitmaps)

    detail_map = None
    detail_map_scale = 0.0
    detail_map_count = 0
    detail_bitmap = None
    secondary_detail_map = None
    secondary_detail_map_scale = 0.0
    secondary_detail_map_count = 0
    secondary_detail_bitmap = None
    if not H1_ASSET.shader_body.primary_detail_map.name == "":
        if detail_map == None:
            detail_map = H1_ASSET.shader_body.primary_detail_map
            detail_map_scale = H1_ASSET.shader_body.primary_detail_map_scale
            detail_map_count = primary_detail_bitmap_count
            detail_bitmap = primary_detail_bitmap
        elif secondary_detail_map == None:
            secondary_detail_map = H1_ASSET.shader_body.primary_detail_map
            secondary_detail_map_scale = H1_ASSET.shader_body.primary_detail_map_scale
            secondary_detail_map_count = primary_detail_bitmap_count
            secondary_detail_bitmap = primary_detail_bitmap

    if not H1_ASSET.shader_body.secondary_detail_map.name == "":
        if detail_map == None:
            detail_map = H1_ASSET.shader_body.secondary_detail_map
            detail_map_scale = H1_ASSET.shader_body.secondary_detail_map_scale
            detail_map_count = secondary_detail_bitmap_count
            detail_bitmap = secondary_detail_bitmap
        elif secondary_detail_map == None:
            secondary_detail_map = H1_ASSET.shader_body.secondary_detail_map
            secondary_detail_map_scale = H1_ASSET.shader_body.secondary_detail_map_scale
            secondary_detail_map_count = secondary_detail_bitmap_count
            secondary_detail_bitmap = secondary_detail_bitmap

    if not H1_ASSET.shader_body.micro_detail_map.name == "":
        if detail_map == None:
            detail_map = H1_ASSET.shader_body.micro_detail_map
            detail_map_scale = H1_ASSET.shader_body.micro_detail_map_scale
            detail_map_count = micro_detail_bitmap_count
            detail_bitmap = micro_detail_bitmap
        elif secondary_detail_map == None:
            secondary_detail_map = H1_ASSET.shader_body.micro_detail_map
            secondary_detail_map_scale = H1_ASSET.shader_body.micro_detail_map_scale
            secondary_detail_map_count = micro_detail_bitmap_count
            secondary_detail_bitmap = micro_detail_bitmap

    if detail_map and not detail_map.name == "":
        parameter = shader_processing.add_parameter(SHADER, TAG, parameter_name="detail_map", bitmap_name=detail_map.name, float_value=0.0)
        parameter.animation_properties = []
        if detail_map_scale > 0.0:
            if detail_map_scale == 0.0:
                detail_map_scale = 1.0

            detail_rescale_i = detail_map_scale
            detail_rescale_j = detail_map_scale
            if base_bitmap_count > 0 and detail_map_count > 0 and DiffuseFlags.rescale_detail_maps in DiffuseFlags(H1_ASSET.shader_body.diffuse_flags):
                if base_bitmap_count > permutation_index:
                    base_element = base_bitmap.bitmaps[permutation_index]
                else:
                    base_element = base_bitmap.bitmaps[0]

                if detail_map_count > permutation_index:
                    detail_element = detail_bitmap.bitmaps[permutation_index]
                else:
                    detail_element = detail_bitmap.bitmaps[0]

                detail_rescale_i *= base_element.width / detail_element.width
                detail_rescale_j *= base_element.height / detail_element.height

            shader_processing.add_animation_property(SHADER, TAG, parameter.animation_properties, AnimationTypeEnum.bitmap_scale_x, function_type=FunctionTypeEnum.constant, lower_bound=detail_rescale_i)
            shader_processing.add_animation_property(SHADER, TAG, parameter.animation_properties, AnimationTypeEnum.bitmap_scale_y, function_type=FunctionTypeEnum.constant, lower_bound=detail_rescale_j)

        parameter.animation_properties_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

    if secondary_detail_map and not secondary_detail_map.name == "":
        parameter = shader_processing.add_parameter(SHADER, TAG, parameter_name="secondary_detail_map", bitmap_name=secondary_detail_map.name, float_value=0.0)
        parameter.animation_properties = []
        if secondary_detail_map_scale > 0.0:
            if secondary_detail_map_scale == 0.0:
                secondary_detail_map_scale = 1.0

            detail_rescale_i = secondary_detail_map_scale
            detail_rescale_j = secondary_detail_map_scale
            if base_bitmap_count > 0 and detail_map_count > 0 and DiffuseFlags.rescale_detail_maps in DiffuseFlags(H1_ASSET.shader_body.diffuse_flags):
                if base_bitmap_count > permutation_index:
                    base_element = base_bitmap.bitmaps[permutation_index]
                else:
                    base_element = base_bitmap.bitmaps[0]

                if secondary_detail_map_count > permutation_index:
                    detail_element = secondary_detail_bitmap.bitmaps[permutation_index]
                else:
                    detail_element = secondary_detail_bitmap.bitmaps[0]

                detail_rescale_i *= base_element.width / detail_element.width
                detail_rescale_j *= base_element.height / detail_element.height

            shader_processing.add_animation_property(SHADER, TAG, parameter.animation_properties, AnimationTypeEnum.bitmap_scale_x, function_type=FunctionTypeEnum.constant, lower_bound=detail_rescale_i)
            shader_processing.add_animation_property(SHADER, TAG, parameter.animation_properties, AnimationTypeEnum.bitmap_scale_y, function_type=FunctionTypeEnum.constant, lower_bound=detail_rescale_j)

        parameter.animation_properties_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
        parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
        SHADER.parameters.append(parameter)

def generate_bump_parameters(H1_ASSET, TAG, SHADER, template, permutation_index):
    base_bitmap = H1_ASSET.shader_body.base_map.parse_tag(print, "halo1", "retail")
    bump_bitmap = H1_ASSET.shader_body.bump_map.parse_tag(print, "halo1", "retail")

    base_bitmap_count = 0
    bump_bitmap_count = 0
    if base_bitmap:
        base_bitmap_count = len(base_bitmap.bitmaps)
    if bump_bitmap:
        bump_bitmap_count = len(bump_bitmap.bitmaps)

    parameter = shader_processing.add_parameter(SHADER, TAG, parameter_name="bump_map", bitmap_name=H1_ASSET.shader_body.bump_map.name, float_value=0.0)
    parameter.animation_properties = []
    if H1_ASSET.shader_body.bump_map_scale > 0.0:
        scale = H1_ASSET.shader_body.bump_map_scale
        if H1_ASSET.shader_body.bump_map_scale == 0.0:
            scale = 1.0

        bump_rescale_i = scale
        bump_rescale_j = scale
        if base_bitmap_count > 0 and bump_bitmap_count > 0 and DiffuseFlags.rescale_bump_maps in DiffuseFlags(H1_ASSET.shader_body.diffuse_flags):
            if base_bitmap_count > permutation_index:
                base_element = base_bitmap.bitmaps[permutation_index]
            else:
                base_element = base_bitmap.bitmaps[0]
            if bump_bitmap_count > permutation_index:
                bump_element = bump_bitmap.bitmaps[permutation_index]
            else:
                bump_element = bump_bitmap.bitmaps[0]

            bump_rescale_i *= base_element.width / bump_element.width
            bump_rescale_j *= base_element.height / bump_element.height

        shader_processing.add_animation_property(SHADER, TAG, parameter.animation_properties, AnimationTypeEnum.bitmap_scale_x, function_type=FunctionTypeEnum.constant, lower_bound=bump_rescale_i)
        shader_processing.add_animation_property(SHADER, TAG, parameter.animation_properties, AnimationTypeEnum.bitmap_scale_y, function_type=FunctionTypeEnum.constant, lower_bound=bump_rescale_j)

    parameter.animation_properties_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
    parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
    SHADER.parameters.append(parameter)

def generate_channel_parameters(H1_ASSET, TAG, SHADER, template, permutation_index):
    parameter = shader_processing.add_parameter(SHADER, TAG, parameter_name="channel_a_color", enum=TypeEnum.color, rgba=(0.0, 0.0, 0.0, 1.0))

    parameter.animation_properties = []
    colors = ((0, 0, 0, 1), (0, 0, 0, 1), (0, 0, 0, 1), (1, 1, 1, 1))
    shader_processing.add_animation_property(SHADER, TAG, parameter.animation_properties, AnimationTypeEnum.color, function_type=FunctionTypeEnum.constant, 
                                             output_modifier=OutputTypeFlags._2_color.value, material_colors=colors)

    animation_property_count = len(parameter.animation_properties)
    parameter.animation_properties_header = TAG.TagBlockHeader("tbfd", 0, animation_property_count, 28)
    parameter.animation_properties_tag_block = TAG.TagBlock(animation_property_count)

    parameter = shader_processing.add_parameter(SHADER, TAG, parameter_name="channel_a_brightness", enum=TypeEnum.color, rgba=(0.0, 0.0, 0.0, 1.0))

    parameter.animation_properties = []
    colors = ((0, 0, 0, 1), (0, 0, 0, 1), (0, 0, 0, 1), (1, 1, 1, 1))
    shader_processing.add_animation_property(SHADER, TAG, parameter.animation_properties, AnimationTypeEnum._value, function_type=FunctionTypeEnum.constant, 
                                             material_colors=colors, lower_bound=1.0, upper_bound=1.0)

    animation_property_count = len(parameter.animation_properties)
    parameter.animation_properties_header = TAG.TagBlockHeader("tbfd", 0, animation_property_count, 28)
    parameter.animation_properties_tag_block = TAG.TagBlock(animation_property_count)

def generate_illum_parameters(H1_ASSET, TAG, SHADER, template, permutation_index):
    parameter = shader_processing.add_parameter(SHADER, TAG, parameter_name="self_illum_map", bitmap_name=H1_ASSET.shader_body.map.name, float_value=0.0)
    parameter.animation_properties = []
    if H1_ASSET.shader_body.map_scale > 0.0:
        shader_processing.add_animation_property(SHADER, TAG, parameter.animation_properties, AnimationTypeEnum.bitmap_scale_x, function_type=FunctionTypeEnum.constant, lower_bound=H1_ASSET.shader_body.map_scale)
        shader_processing.add_animation_property(SHADER, TAG, parameter.animation_properties, AnimationTypeEnum.bitmap_scale_y, function_type=FunctionTypeEnum.constant, lower_bound=H1_ASSET.shader_body.map_scale)

    parameter.animation_properties_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
    parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
    SHADER.parameters.append(parameter)
    SHADER.parameters.append(shader_processing.add_parameter(SHADER, TAG, parameter_name="lightmap_emmisive_map", bitmap_name=H1_ASSET.shader_body.map.name, float_value=0.0))

    SHADER.parameters.append(shader_processing.add_parameter(SHADER, TAG, parameter_name="emissive_color", enum=TypeEnum.color, rgba=H1_ASSET.shader_body.color_of_emitted_light))
    SHADER.parameters.append(shader_processing.add_parameter(SHADER, TAG, parameter_name="emissive_power", enum=TypeEnum._value, float_value= 0.10 * H1_ASSET.shader_body.power))

def generate_env_parameters(H1_ASSET, TAG, SHADER, template, permutation_index):
    parameter = shader_processing.add_parameter(SHADER, TAG, parameter_name="environment_map", bitmap_name=H1_ASSET.shader_body.reflection_cube_map.name, float_value=0.0)
    parameter.animation_properties = []
    parameter.animation_properties_header = TAG.TagBlockHeader("tbfd", 0, len(parameter.animation_properties), 28)
    parameter.animation_properties_tag_block = TAG.TagBlock(len(parameter.animation_properties))
    SHADER.parameters.append(parameter)

    SHADER.parameters.append(shader_processing.add_parameter(SHADER, TAG, parameter_name="env_tint_color", enum=TypeEnum.color, rgba=H1_ASSET.shader_body.perpendicular_color))
    SHADER.parameters.append(shader_processing.add_parameter(SHADER, TAG, parameter_name="env_glancing_tint_color", enum=TypeEnum.color, rgba=H1_ASSET.shader_body.parallel_color))
    SHADER.parameters.append(shader_processing.add_parameter(SHADER, TAG, parameter_name="env_brightness", enum=TypeEnum._value, float_value=H1_ASSET.shader_body.perpendicular_brightness))
    SHADER.parameters.append(shader_processing.add_parameter(SHADER, TAG, parameter_name="env_glancing_brightness", enum=TypeEnum._value, float_value=H1_ASSET.shader_body.parallel_brightness))

def generate_specular_parameters(H1_ASSET, TAG, SHADER, template, permutation_index):
    SHADER.parameters.append(shader_processing.add_parameter(SHADER, TAG, parameter_name="specular_color", enum=TypeEnum.color, float_value=0.0, rgba=H1_ASSET.shader_body.perpendicular_color))
    SHADER.parameters.append(shader_processing.add_parameter(SHADER, TAG, parameter_name="specular_glancing_color", enum=TypeEnum.color, float_value=0.0, rgba=H1_ASSET.shader_body.parallel_color))

def generate_parameters(H1_ASSET, TAG, SHADER, template, permutation_index):
    if not H1_ASSET.shader_body.bump_map.name == "":
        generate_bump_parameters(H1_ASSET, TAG, SHADER, template, permutation_index)
    if not H1_ASSET.shader_body.base_map.name == "":
        generate_base_map_parameters(H1_ASSET, TAG, SHADER, template, permutation_index)
    if not H1_ASSET.shader_body.reflection_cube_map.name == "":
        generate_env_parameters(H1_ASSET, TAG, SHADER, template, permutation_index)
    if H1_ASSET.shader_body.power > 0.0:
        generate_illum_parameters(H1_ASSET, TAG, SHADER, template, permutation_index)
    if not H1_ASSET.shader_body.primary_detail_map.name == "" or not H1_ASSET.shader_body.secondary_detail_map.name == "" or not H1_ASSET.shader_body.micro_detail_map.name == "":
        generate_detail_map_parameters(H1_ASSET, TAG, SHADER, template, permutation_index)
    if not H1_ASSET.shader_body.map.name == "":
        generate_channel_parameters(H1_ASSET, TAG, SHADER, template, permutation_index)

    generate_specular_parameters(H1_ASSET, TAG, SHADER, template, permutation_index)
    for parameter in SHADER.parameters:
        if parameter.animation_properties == None:
            parameter.animation_properties = []
            parameter.animation_properties_header = TAG.TagBlockHeader("tbfd", 0, 0, 28)
            parameter.animation_properties_tag_block = TAG.TagBlock(0)

    parameter_count = len(SHADER.parameters)
    SHADER.parameters_header = TAG.TagBlockHeader("tbfd", 0, parameter_count, 52)

    return TAG.TagBlock(parameter_count)

def get_template(H1_ASSET):
    shader_template = shader_processing.OpaqueTemplateEnum.tex_bump

    is_emissive = False
    has_alpha = False
    has_cc = False
    has_diffuse = False
    detail_map_count = 0
    has_bump = False
    has_channels = False
    has_env_map = False
    if H1_ASSET.shader_body.power > 0.0:
        is_emissive = True
    if H1EnvironmentFlags.alpha_tested in H1EnvironmentFlags(H1_ASSET.shader_body.environment_flags):
        has_alpha = True
    if not EnvironmentTypeEnum(H1_ASSET.shader_body.environment_type) == EnvironmentTypeEnum.normal:
        is_blended = True
    if not H1_ASSET.shader_body.base_map.name == "":
        has_diffuse = True
    if not H1_ASSET.shader_body.primary_detail_map.name == "":
        detail_map_count += 1
    if not H1_ASSET.shader_body.secondary_detail_map.name == "":
        detail_map_count += 1
    if not H1_ASSET.shader_body.micro_detail_map.name == "":
        detail_map_count += 1
    if not H1_ASSET.shader_body.bump_map.name == "":
        has_bump = True
    if not H1_ASSET.shader_body.map.name == "":
        has_channels = True
    if not H1_ASSET.shader_body.reflection_cube_map.name == "":
        has_env_map = True

    valid_shader_templates = [shader_template for shader_template in shader_processing.OpaqueTemplateEnum]
    if has_diffuse:
        gathered_template_list = []
        for valid_shader_template in valid_shader_templates:
            if "tex" in valid_shader_template.name:
                gathered_template_list.append(valid_shader_template)

        valid_shader_templates = gathered_template_list

    if has_bump:
        gathered_template_list = []
        for valid_shader_template in valid_shader_templates:
            if "bump" in valid_shader_template.name:
                gathered_template_list.append(valid_shader_template)

        valid_shader_templates = gathered_template_list

    if has_alpha:
        gathered_template_list = []
        for valid_shader_template in valid_shader_templates:
            if "alpha" in valid_shader_template.name:
                gathered_template_list.append(valid_shader_template)

        valid_shader_templates = gathered_template_list

    if is_emissive:
        gathered_template_list = []
        for valid_shader_template in valid_shader_templates:
            if "illum" in valid_shader_template.name:
                gathered_template_list.append(valid_shader_template)

        valid_shader_templates = gathered_template_list

    if has_channels:
        gathered_template_list = []
        for valid_shader_template in valid_shader_templates:
            if "channel" in valid_shader_template.name:
                gathered_template_list.append(valid_shader_template)

        valid_shader_templates = gathered_template_list

    if has_env_map:
        gathered_template_list = []
        for valid_shader_template in valid_shader_templates:
            if "env" in valid_shader_template.name:
                gathered_template_list.append(valid_shader_template)

        valid_shader_templates = gathered_template_list

    if detail_map_count >= 2:
        gathered_template_list = []
        if is_blended:
            for valid_shader_template in valid_shader_templates:
                if "detail_blend" in valid_shader_template.name:
                    gathered_template_list.append(valid_shader_template)

            valid_shader_templates = gathered_template_list
        else:
            for valid_shader_template in valid_shader_templates:
                if "two_detail" in valid_shader_template.name:
                    gathered_template_list.append(valid_shader_template)

            valid_shader_templates = gathered_template_list

    if len(valid_shader_templates) > 0:
        shader_template = valid_shader_templates[0]

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

def upgrade_shader(H1_ASSET, patch_txt_path, report, permutation_index=0):
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

    template = get_template(H1_ASSET)

    SHADER.shader_body_header = TAG.TagBlockHeader("tbfd", 0, 1, 128)
    SHADER.shader_body = SHADER.ShaderBody()
    SHADER.shader_body.template = TAG.TagRef("stem", template.value, len(template.value))
    SHADER.shader_body.material_name = get_material_name(H1_ASSET.shader_body.material_type)
    SHADER.shader_body.runtime_properties_tag_block = TAG.TagBlock()
    SHADER.shader_body.flags = 0
    SHADER.shader_body.parameters_tag_block = generate_parameters(H1_ASSET, TAG, SHADER, template, permutation_index)
    SHADER.shader_body.postprocess_definition_tag_block = TAG.TagBlock()
    SHADER.shader_body.predicted_resources_tag_block = TAG.TagBlock()
    SHADER.shader_body.light_response = TAG.TagRef("slit")
    SHADER.shader_body.shader_lod_bias = 0
    SHADER.shader_body.specular_type = SpecularTypeEnum.default.value
    SHADER.shader_body.lightmap_type = LightmapTypeEnum.diffuse.value
    SHADER.shader_body.lightmap_specular_brightness = H1_ASSET.shader_body.brightness
    SHADER.shader_body.lightmap_ambient_bias = 0.0
    SHADER.shader_body.postprocess_properties_tag_block = TAG.TagBlock()
    SHADER.shader_body.added_depth_bias_offset = 0.0
    SHADER.shader_body.added_depth_bias_slope = 0.0

    return SHADER
