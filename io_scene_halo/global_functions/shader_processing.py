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
import bpy
import struct
import numpy as np
import subprocess

from mathutils import Vector
from enum import Flag, Enum, auto
from ..file_tag.h1.file_shader_environment.format import EnvironmentTypeEnum, EnvironmentFlags, DiffuseFlags, ReflectionFlags
from ..file_tag.h1.file_shader_model.format import ModelFlags, DetailFumctionEnum, DetailMaskEnum, FunctionEnum
from ..file_tag.h1.file_bitmap.format import FormatEnum, BitmapFormatEnum
from ..file_tag.h2.file_functions.format import OutputTypeFlags
from ..file_tag.h2.file_shader.format import (
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
        )
from ..global_functions.parse_tags import parse_tag
from . import tag_format, global_functions, mesh_processing
from ..file_tag.h2.file_particle.format import OutputModifierInputEnum
from .shader_generation.shader_helper import (
    get_bitmap, 
    get_linked_node, 
    get_output_material_node, 
    connect_inputs, 
    generate_image_node, 
    generate_reflection_tint_logic_node, 
    generate_multiply_node, 
    generate_biased_multiply_node,
    generate_multipurpose_logic_node,
    generate_detail_logic_node
    )

from .shader_generation.shader_environment import generate_shader_environment
from .shader_generation.shader_model import generate_shader_model
from .shader_generation import shader_opaque

try:
    from PIL import Image
except ModuleNotFoundError:
    print("PIL not found. Unable to create image node.")
    Image = None

try:
    import lxml.etree as ET
except ModuleNotFoundError:
    print("lxml not found. Unable to generate bitmaps for Halo 3 era imports.")
    ET = None


def generate_shader_environment_simple(mat, shader, permutation_index, report):
    mat.use_nodes = True

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_data_path
    base_map, base_bitmap_name = get_bitmap(shader.base_map, texture_root)
    base_bitmap = parse_tag(shader.base_map, report, "halo1", "retail")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    base_node = generate_image_node(mat, base_map, base_bitmap, base_bitmap_name)
    base_node.name = "Base Map"
    base_node.location = Vector((-2100, 475))
    if not base_node.image == None:
        base_node.image.alpha_mode = 'CHANNEL_PACKED'

    alpha_shader = EnvironmentFlags.alpha_tested in EnvironmentFlags(shader.environment_flags)
    if alpha_shader:
        mat.shadow_method = 'CLIP'
        mat.blend_method = 'CLIP'

    mat.use_backface_culling = True

    connect_inputs(mat.node_tree, base_node, "Color", bdsf_principled, "Base Color")

def generate_shader_model_simple(mat, shader, report):
    mat.use_nodes = True

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_data_path
    base_map, base_map_name = get_bitmap(shader.base_map, texture_root)
    base_bitmap = parse_tag(shader.base_map, report, "halo1", "retail")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    base_node = generate_image_node(mat, base_map, base_bitmap, base_map_name)
    if not base_node.image == None:
        base_node.image.alpha_mode = 'CHANNEL_PACKED'

    base_node.location = Vector((-1600, 500))
    shader_model_flags = ModelFlags(shader.model_flags)
    if base_bitmap:
        ignore_alpha_bitmap = True
        for bitmap_element in base_bitmap.bitmaps:
            bitmap_format = BitmapFormatEnum(bitmap_element.bitmap_format)
            if bitmap_format == BitmapFormatEnum.a8:
                ignore_alpha_bitmap = False
                break
            elif bitmap_format == BitmapFormatEnum.ay8:
                ignore_alpha_bitmap = False
                break
            elif bitmap_format == BitmapFormatEnum.a8y8:
                ignore_alpha_bitmap = False
                break
            elif bitmap_format == BitmapFormatEnum.a1r5g5b5:
                ignore_alpha_bitmap = False
                break
            elif bitmap_format == BitmapFormatEnum.a4r4g4b4:
                ignore_alpha_bitmap = False
                break
            elif bitmap_format == BitmapFormatEnum.a8r8g8b8:
                ignore_alpha_bitmap = False
                break
            elif bitmap_format == BitmapFormatEnum.dxt3:
                ignore_alpha_bitmap = False
                break
            elif bitmap_format == BitmapFormatEnum.dxt5:
                ignore_alpha_bitmap = False
                break
            elif bitmap_format == BitmapFormatEnum.bc7:
                ignore_alpha_bitmap = False
                break


        ignore_alpha_shader = ModelFlags.not_alpha_tested in shader_model_flags
        if ignore_alpha_shader or ignore_alpha_bitmap:
            base_node.image.alpha_mode = 'NONE'
        else:
            connect_inputs(mat.node_tree, base_node, "Alpha", bdsf_principled, "Alpha")
            mat.shadow_method = 'CLIP'
            mat.blend_method = 'CLIP'

    mat.use_backface_culling = False
    if not ModelFlags.two_sided in shader_model_flags:
        mat.use_backface_culling = True

    connect_inputs(mat.node_tree, base_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_chicago_simple(mat, shader, report):
    mat.use_nodes = True

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_data_path
    first_map = None
    first_map_bitmap = None
    first_map_name = "White"
    if len(shader.maps) > 0:
        first_map, first_map_name = get_bitmap(shader.maps[0].map, texture_root)
        first_map_bitmap = parse_tag(shader.maps[0].map, report, "halo1", "retail")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    first_map_node = generate_image_node(mat, first_map, first_map_bitmap, first_map_name)

    connect_inputs(mat.node_tree, first_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_chicago_extended_simple(mat, shader, report):
    mat.use_nodes = True

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_data_path
    first_map = None
    first_map_bitmap = None
    first_map_name = "White"
    if len(shader._4_stage_maps) > 0:
        first_map, first_map_name = get_bitmap(shader._4_stage_maps[0].map, texture_root)
        first_map_bitmap = parse_tag(shader._4_stage_maps[0].map, report, "halo1", "retail")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    first_map_node = generate_image_node(mat, first_map, first_map_bitmap, first_map_name)

    connect_inputs(mat.node_tree, first_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_generic_simple(mat, shader, report):
    mat.use_nodes = True

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_data_path
    first_map = None
    first_map_bitmap = None
    first_map_name = "White"
    if len(shader.maps) > 0:
        first_map, first_map_name = get_bitmap(shader.maps[0].map, texture_root)
        first_map_bitmap = parse_tag(shader.maps[0].map, report, "halo1", "retail")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    first_map_node = generate_image_node(mat, first_map, first_map_bitmap, first_map_name)

    connect_inputs(mat.node_tree, first_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_glass_simple(mat, shader, report):
    mat.use_nodes = True

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_data_path
    diffuse_map, diffuse_map_name = get_bitmap(shader.diffuse_map, texture_root)
    diffuse_bitmap = parse_tag(shader.diffuse_map, report, "halo1", "retail")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    diffuse_node = generate_image_node(mat, diffuse_map, diffuse_bitmap, diffuse_map_name)

    diffuse_node.location = Vector((-1600, 500))

    connect_inputs(mat.node_tree, diffuse_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_meter_simple(mat, shader, report):
    mat.use_nodes = True

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_data_path
    meter_map, meter_map_name = get_bitmap(shader.meter_map, texture_root)
    meter_bitmap = parse_tag(shader.meter_map, report, "halo1", "retail")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    meter_node = generate_image_node(mat, meter_map, meter_bitmap, meter_map_name)

    meter_node.location = Vector((-1600, 500))

    connect_inputs(mat.node_tree, meter_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_plasma_simple(mat, shader, report):
    mat.use_nodes = True

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_data_path
    primary_noise_map, primary_noise_map_name = get_bitmap(shader.primary_noise_map, texture_root)
    primary_noise_bitmap = parse_tag(shader.primary_noise_map, report, "halo1", "retail")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    primary_noise_node = generate_image_node(mat, primary_noise_map, primary_noise_bitmap, primary_noise_map_name)

    connect_inputs(mat.node_tree, primary_noise_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_water_simple(mat, shader, report):
    mat.use_nodes = True

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_data_path
    base_map, base_map_name = get_bitmap(shader.base_map, texture_root)
    base_bitmap = parse_tag(shader.base_map, report, "halo1", "retail")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    base_node = generate_image_node(mat, base_map, base_bitmap, base_map_name)

    connect_inputs(mat.node_tree, base_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_meter(mat, shader, report):
    mat.use_nodes = True

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_data_path
    meter_map, meter_map_name = get_bitmap(shader.meter_map, texture_root)
    meter_bitmap = parse_tag(shader.meter_map, report, "halo1", "retail")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    mat.node_tree.nodes.remove(bdsf_principled)

    shader_mix_node = mat.node_tree.nodes.new("ShaderNodeMixShader")
    shader_mix_node.location = Vector((-175, 0))
    connect_inputs(mat.node_tree, shader_mix_node, "Shader", output_material_node, "Surface")

    invert_node = mat.node_tree.nodes.new("ShaderNodeInvert")
    emission_node = mat.node_tree.nodes.new("ShaderNodeEmission")
    bsdf_transparent_node = mat.node_tree.nodes.new("ShaderNodeBsdfTransparent")
    invert_node.location = Vector((-350, 125))
    emission_node.location = Vector((-350, 0))
    bsdf_transparent_node.location = Vector((-350, -125))
    invert_node.inputs[0].default_value = 1
    connect_inputs(mat.node_tree, invert_node, "Color", shader_mix_node, 0)
    connect_inputs(mat.node_tree, emission_node, "Emission", shader_mix_node, 1)
    connect_inputs(mat.node_tree, bsdf_transparent_node, "BSDF", shader_mix_node, 2)

    gamma_node = mat.node_tree.nodes.new("ShaderNodeGamma")
    gamma_node.location = Vector((-525, -125))
    gamma_node.inputs[1].default_value = 2.2

    meter_node = generate_image_node(mat, meter_map, meter_bitmap, meter_map_name)
    meter_node.image.alpha_mode = 'CHANNEL_PACKED'
    meter_node.location = Vector((-650, 175))
    connect_inputs(mat.node_tree, gamma_node, "Color", emission_node, "Color")
    connect_inputs(mat.node_tree, meter_node, "Alpha", emission_node, "Strength")
    connect_inputs(mat.node_tree, meter_node, "Alpha", invert_node, "Color")

    rgb_node = mat.node_tree.nodes.new("ShaderNodeRGB")
    rgb_node.location = Vector((-725, -125))
    rgb_node.outputs[0].default_value = shader.background_color
    connect_inputs(mat.node_tree, rgb_node, "Color", gamma_node, "Color")

    mat.blend_method = 'BLEND'

def generate_shader_transparent_glass(mat, shader, report):
    mat.use_nodes = True

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_data_path
    background_tint_map, background_tint_map_name = get_bitmap(shader.background_tint_map, texture_root)
    reflection_map, reflection_map_name = get_bitmap(shader.reflection_map, texture_root)
    bump_map, bump_map_name = get_bitmap(shader.bump_map, texture_root)
    diffuse_map, diffuse_map_name = get_bitmap(shader.diffuse_map, texture_root)
    diffuse_detail_map, diffuse_detail_map_name = get_bitmap(shader.diffuse_detail_map, texture_root)
    specular_map, specular_map_name = get_bitmap(shader.specular_map, texture_root)
    specular_detail_map, specular_detail_map_name = get_bitmap(shader.specular_detail_map, texture_root)

    background_tint_bitmap = parse_tag(shader.background_tint_map, report, "halo1", "retail")
    reflection_bitmap = parse_tag(shader.reflection_map, report, "halo1", "retail")
    bump_bitmap = parse_tag(shader.bump_map, report, "halo1", "retail")
    diffuse_bitmap = parse_tag(shader.diffuse_map, report, "halo1", "retail")
    diffuse_detail_bitmap = parse_tag(shader.diffuse_detail_map, report, "halo1", "retail")
    specular_bitmap = parse_tag(shader.specular_map, report, "halo1", "retail")
    specular_detail_bitmap = parse_tag(shader.specular_detail_map, report, "halo1", "retail")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    background_tint_node = generate_image_node(mat, background_tint_map, background_tint_bitmap, background_tint_map_name)
    reflection_node = generate_image_node(mat, reflection_map, reflection_bitmap, reflection_map_name)
    bump_node = generate_image_node(mat, bump_map, bump_bitmap, bump_map_name)

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-875, -800))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", bump_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    height_node = mat.node_tree.nodes.new("ShaderNodeBump")
    uv_map_node.location = Vector((-1075, -800))
    combine_xyz_node.location = Vector((-1075, -925))
    height_node.location = Vector((-425, -600))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)
    connect_inputs(mat.node_tree, bump_node, "Color", height_node, "Height")
    connect_inputs(mat.node_tree, height_node, "Normal", bdsf_principled, "Normal")

    if bump_bitmap:
        height_node.inputs[0].default_value = bump_bitmap.bump_height

    scale = shader.bump_map_scale
    if shader.bump_map_scale == 0.0:
        scale = 1.0

    combine_xyz_node.inputs[0].default_value = scale
    combine_xyz_node.inputs[1].default_value = scale
    combine_xyz_node.inputs[2].default_value = 1

    diffuse_node = generate_image_node(mat, diffuse_map, diffuse_bitmap, diffuse_map_name)

    connect_inputs(mat.node_tree, diffuse_node, "Color", bdsf_principled, "Base Color")

    if diffuse_bitmap:
        ignore_alpha_bitmap = diffuse_bitmap.bitmap_format is FormatEnum.compressed_with_color_key_transparency.value
        if ignore_alpha_bitmap:
            diffuse_node.image.alpha_mode = 'NONE'
        else:
            connect_inputs(mat.node_tree, diffuse_node, "Alpha", bdsf_principled, "Alpha")
            mat.shadow_method = 'CLIP'
            mat.blend_method = 'BLEND'

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-2275, 1250))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", diffuse_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-2450, 1325))
    combine_xyz_node.location = Vector((-2450, 1175))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.diffuse_map_scale
    if shader.diffuse_map_scale == 0.0:
        scale = 1.0

    combine_xyz_node.inputs[0].default_value = scale
    combine_xyz_node.inputs[1].default_value = scale
    combine_xyz_node.inputs[2].default_value = 1

    diffuse_detail_node = generate_image_node(mat, diffuse_detail_map, diffuse_detail_bitmap, diffuse_detail_map_name)

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-2275, 1250))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", diffuse_detail_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-2450, 1325))
    combine_xyz_node.location = Vector((-2450, 1175))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.diffuse_detail_map_scale
    if shader.diffuse_detail_map_scale == 0.0:
        scale = 1.0

    combine_xyz_node.inputs[0].default_value = scale
    combine_xyz_node.inputs[1].default_value = scale
    combine_xyz_node.inputs[2].default_value = 1

    specular_node = generate_image_node(mat, specular_map, specular_bitmap, specular_map_name)

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-2275, 1250))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", specular_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-2450, 1325))
    combine_xyz_node.location = Vector((-2450, 1175))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.specular_map_scale
    if shader.specular_map_scale == 0.0:
        scale = 1.0

    combine_xyz_node.inputs[0].default_value = scale
    combine_xyz_node.inputs[1].default_value = scale
    combine_xyz_node.inputs[2].default_value = 1

    specular_detail_node = generate_image_node(mat, specular_detail_map, specular_detail_bitmap, specular_detail_map_name)

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-2275, 1250))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", specular_detail_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-2450, 1325))
    combine_xyz_node.location = Vector((-2450, 1175))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.specular_detail_map_scale
    if shader.specular_detail_map_scale == 0.0:
        scale = 1.0

    combine_xyz_node.inputs[0].default_value = scale
    combine_xyz_node.inputs[1].default_value = scale
    combine_xyz_node.inputs[2].default_value = 1

def generate_h1_shader(mat, tag_ref, shader_permutation_index, report):
    # 0 = Shader generation is disabled
    # 1 = Simple shader generation. Only the base map is generated
    # 2 = Full Shader generation
    if not int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 0:
        shader = parse_tag(tag_ref, report, "halo1", "retail")
        if not shader == None:
            if shader.header.tag_group == "senv":
                if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                    generate_shader_environment_simple(mat, shader, shader_permutation_index, report)
                else:
                    generate_shader_environment(mat, shader, shader_permutation_index, report)

            elif shader.header.tag_group == "soso":
                if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                    generate_shader_model_simple(mat, shader, report)
                else:
                    generate_shader_model(mat, shader, report)

            elif shader.header.tag_group == "schi":
                if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                    generate_shader_transparent_chicago_simple(mat, shader, report)
                else:
                    print("Skipping shader_transparent_chicago")
                    #generate_shader_transparent_chicago(mat, shader, report)

            elif shader.header.tag_group == "scex":
                if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                    generate_shader_transparent_chicago_extended_simple(mat, shader, report)
                else:
                    print("Skipping shader_transparent_chicago_extended")
                    #generate_shader_transparent_chicago_extended(mat, shader, report)

            elif shader.header.tag_group == "sotr":
                if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                    generate_shader_transparent_generic_simple(mat, shader, report)
                else:
                    print("Skipping shader_transparent_generic")
                    #generate_shader_transparent_generic(mat, shader, report)

            elif shader.header.tag_group == "sgla":
                if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                    generate_shader_transparent_glass_simple(mat, shader, report)
                else:
                    generate_shader_transparent_glass(mat, shader, report)

            elif shader.header.tag_group == "smet":
                if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                    generate_shader_transparent_meter_simple(mat, shader, report)
                else:
                    generate_shader_transparent_meter(mat, shader, report)

            elif shader.header.tag_group == "spla":
                if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                    generate_shader_transparent_plasma_simple(mat, shader, report)
                else:
                    print("Skipping shader_transparent_plasma")
                    #generate_shader_transparent_plasma(mat, shader, report)

            elif shader.header.tag_group == "swat":
                if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                    generate_shader_transparent_water_simple(mat, shader, report)
                else:
                    print("Skipping shader_transparent_water")
                    #generate_shader_transparent_water(mat, shader, report)

        else:
            print("Halo 1 parsed shader tag returned as none. Something went horribly wrong")

    else:
        print("Shader generation is disabled. Skipping")

def generate_shader_simple(mat, shader, report):
    mat.use_nodes = True

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_data_path
    base_parameter = None
    if len(shader.parameters) > 0:
        for parameter in shader.parameters:
            if base_parameter == None and len(parameter.bitmap.name) > 0:
                base_parameter = parameter

            if parameter.name == "base_map":
                base_parameter = parameter
                break

    base_map = None
    base_map_name = "White"
    base_bitmap = None
    if base_parameter:
        base_map, base_map_name = get_bitmap(base_parameter.bitmap, texture_root)
        base_bitmap = parse_tag(base_parameter.bitmap, report, "halo2", "retail")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    base_node = generate_image_node(mat, base_map, base_bitmap, base_map_name)
    if not base_node.image == None:
        base_node.image.alpha_mode = 'CHANNEL_PACKED'

    base_node.location = Vector((-1600, 500))

    connect_inputs(mat.node_tree, base_node, "Color", bdsf_principled, "Base Color")

def generate_h2_shader(mat, tag_ref, report):
    # 0 = Shader generation is disabled
    # 1 = Simple shader generation. Only the base map is generated
    # 2 = Full Shader generation
    if not int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 0:
        shader = parse_tag(tag_ref, report, "halo2", "retail")
        if not shader == None:
            if shader.header.tag_group == "shad":
                if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                    generate_shader_simple(mat, shader, report)
                else:
                    if not shader.template == None:
                        shader_template = parse_tag(shader.template, report, "halo2", "retail")
                        shader_name = os.path.basename(shader.template.name)
                        if shader_name == "active_camo_opaque":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "bloom":
                            shader_opaque.generate_shader_bloom(mat, shader, shader_template, report)
                        elif shader_name == "decal_simple":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "emblem_flag":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "emblem_opaque":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "emblem_overlay":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "emblem_overlay_simple":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "illum":
                            shader_opaque.generate_shader_illum(mat, shader, shader_template, report)
                        elif shader_name == "illum_3_channel":
                            shader_opaque.generate_shader_illum(mat, shader, shader_template, report)
                        elif shader_name == "illum_3_channel_opaque":
                            shader_opaque.generate_shader_illum(mat, shader, shader_template, report)
                        elif shader_name == "illum_3_channel_plasma":
                            shader_opaque.generate_shader_illum(mat, shader, shader_template, report)
                        elif shader_name == "illum_bloom":
                            shader_opaque.generate_shader_illum(mat, shader, shader_template, report)
                        elif shader_name == "illum_bloom_3_channel":
                            shader_opaque.generate_shader_illum(mat, shader, shader_template, report)
                        elif shader_name == "illum_bloom_3_channel_opaque":
                            shader_opaque.generate_shader_illum(mat, shader, shader_template, report)
                        elif shader_name == "illum_bloom_masked":
                            shader_opaque.generate_shader_illum(mat, shader, shader_template, report)
                        elif shader_name == "illum_bloom_opaque":
                            shader_opaque.generate_shader_illum(mat, shader, shader_template, report)
                        elif shader_name == "illum_clamped":
                            shader_opaque.generate_shader_illum(mat, shader, shader_template, report)
                        elif shader_name == "illum_detail":
                            shader_opaque.generate_shader_illum(mat, shader, shader_template, report)
                        elif shader_name == "illum_opaque":
                            shader_opaque.generate_shader_illum(mat, shader, shader_template, report)
                        elif shader_name == "illum_opaque_index":
                            shader_opaque.generate_shader_illum(mat, shader, shader_template, report)
                        elif shader_name == "illum_wrap":
                            shader_opaque.generate_shader_illum(mat, shader, shader_template, report)
                        elif shader_name == "overlay":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "prt_lightmap":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "prt_scarab":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "prt_simple":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "prt_simple_lm_emissive":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "render_layer_disabled":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_alpha_test":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_alpha_test_clamped":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_active_camo":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_alpha_test":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_alpha_test_clamped":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_alpha_test_clamped_single_pass":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_alpha_test_detail":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_alpha_test_single_pass":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_bloom":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_clamped_multiply_map":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_detail_blend":
                            shader_opaque.generate_shader_tex_bump_detail_blend(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_detail_blend_detail":
                            shader_opaque.generate_shader_tex_bump_detail_blend_detail(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_detail_blend_specular":
                            shader_opaque.generate_shader_tex_bump_detail_blend(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_detail_blend_specular_combined":
                            shader_opaque.generate_shader_tex_bump_detail_blend(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_detail_blend_specular_dblmult":
                            shader_opaque.generate_shader_tex_bump_detail_blend(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_detail_keep":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_detail_keep_blend":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_detail_mask":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_detail_overlay":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_dprs_env":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_dprs_env_illum":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_dprs_env_illum_emissive":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_alpha_test":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_alpha_test_combined":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_alpha_test_indexed":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_clamped":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_clamped_combined":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_combined":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_dbl_spec":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_detail_blend":
                            shader_opaque.generate_shader_tex_bump_detail_blend(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_detail_blend_specular":
                            shader_opaque.generate_shader_tex_bump_detail_blend(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_detail_mask":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_detail_mask_combined":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_detail_overlay":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_detail_overlay_combined":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_fast_masked":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_four_change_color":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_four_change_color_combined":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_illum":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_illum_3_channel":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_illum_3_channel_combined":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_illum_3_channel_combined_unfucked":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_illum_3_channel_occlusion":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_illum_3_channel_occlusion_combined":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_illum_combined":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_illum_combined_emmisive_map":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_illum_detail_honor_guard":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_illum_detail_honor_guard_base":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_illum_emmisive_map":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_illum_four_change_color":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_illum_four_change_color_no_lod":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_illum_tiling_specular":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_illum_trace":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_illum_two_change_color":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_illum_two_change_color_combined":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_no_detail":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_tiling_specular":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_two_change_color":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_two_change_color_combined":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_two_change_color_indexed":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_two_change_color_multiply_map_self_illum":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_two_detail":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_env_two_detail_combined":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_foliage":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_four_change_color":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_illum":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_illum_3_channel":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_illum_alpha_test":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_illum_alpha_test_illum":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_illum_alpha_test_single_pass":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_illum_bloom":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_illum_bloom_3_channel":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_illum_detail":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_illum_detail_honor_guard":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_illum_no_specular":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_illum_trace":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_illum_two_detail":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_meter_illum":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_multiply_map":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_no_alpha":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_no_specular":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_one_change_color":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_plasma":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_plasma_one_channel_illum":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_shiny":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_terrain":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_three_detail_blend":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_tiling_specular":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_two_change_color":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_two_change_color_multiply_map":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_two_change_color_multiply_map_self_illum":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_two_detail":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_bump_two_detail_tint":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_detail_blend":
                            shader_opaque.generate_shader_tex_bump_detail_blend(mat, shader, shader_template, report)
                        elif shader_name == "tex_env":
                            shader_opaque.generate_shader_tex_bump(mat, shader, shader_template, report)
                        elif shader_name == "tex_env_3_channel_illum":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_illum":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)
                        elif shader_name == "tex_illum_bloom":
                            shader_opaque.generate_shader_tex_bump_illum(mat, shader, shader_template, report)

        else:
            print("Halo 2 parsed shader tag returned as none. Something went horribly wrong")

    else:
        print("Shader generation is disabled. Skipping")

def generate_h3_shader_simple(mat, shader_path, report):
    mat.use_nodes = True

    data_directory = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_3_data_path
    tags_directory = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_3_tag_path
    bitmap_file = None
    input_file = ""
    if not ET == None:
        tool_directory = os.path.dirname(os.path.dirname(data_directory))
        output_directory = os.path.join(tool_directory, "blender_dumps")
        tool_path = os.path.join(tool_directory, "tool.exe")

        local_path_no_ext = shader_path.split(tags_directory.lower(), 1)[1].rsplit(".", 1)[0]
        xml_output = os.path.join(output_directory, "%s.xml" % local_path_no_ext)

        xml_command = "export-tag-to-xml"
        args = [tool_path, xml_command, shader_path, xml_output]
        subprocess.call(args, cwd=tool_directory)

        xmlp = ET.XMLParser(encoding="ISO-8859-10", recover=True)
        xml = ET.parse(xml_output, parser=xmlp)
        root = xml.getroot() 
        bitmap_parameter = None
        bitmap_path = None
        for root_fields in root:
            if root_fields.attrib.get('name') == "parameters":
                for parameter_fields in root_fields:
                    if parameter_fields.attrib.get('name') == "base_map":
                        parameter_type_field = None
                        bitmap_field = None
                        for field in parameter_fields:
                            if field.attrib.get('name') == "parameter type" and field.attrib.get('value') == "bitmap":
                                parameter_type_field = field
                            if field.attrib.get('name') == "bitmap":
                                bitmap_field = field

                        if parameter_type_field is not None:
                            bitmap_tag_path = os.path.join(tags_directory, "%s.%s" % (bitmap_field.attrib.get('value').rsplit(",", 1)[0], "bitmap"))
                            if os.path.isfile(bitmap_tag_path):
                                bitmap_parameter = parameter_fields

                                break

                    else:
                        if bitmap_parameter == None:
                            parameter_type_field = None
                            bitmap_field = None
                            for field in parameter_fields:
                                if field.attrib.get('name') == "parameter type" and field.attrib.get('value') == "bitmap":
                                    parameter_type_field = field
                                if field.attrib.get('name') == "bitmap":
                                    bitmap_field = field

                            if parameter_type_field is not None:
                                bitmap_tag_path = os.path.join(tags_directory, "%s.%s" % (bitmap_field.attrib.get('value').rsplit(",", 1)[0], "bitmap"))
                                print(bitmap_tag_path)
                                if os.path.isfile(bitmap_tag_path):
                                    bitmap_parameter = parameter_fields

                        
        if bitmap_parameter is not None:
            for field in bitmap_parameter:
                if field.attrib.get('name') == "bitmap":
                    bitmap_path = field.attrib.get('value')

        if bitmap_path is not None:
            bitmap_command = "export-bitmap-tga"
            input_file = bitmap_path.rsplit(",", 1)[0]
            bitmap_directory = os.path.dirname(input_file)
            bitmap_name = os.path.basename(input_file)
            bitmap_output = os.path.join(output_directory, bitmap_directory, "pixel_data_")
            if not os.path.exists(os.path.dirname(bitmap_output)):
                os.makedirs(os.path.dirname(bitmap_output))

            args = [tool_path, bitmap_command, input_file, bitmap_output]

            subprocess.call(args, cwd=tool_directory)

            bitmap_file = os.path.join(output_directory, bitmap_directory, "pixel_data_%s%s" % (bitmap_name, "_00_00.tga"))

        else:
            print("No valid bitmap found. Skipping")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    texture_extensions = ("tif", "tiff", "dss")
    texture_path = None
    for extension in texture_extensions:
        check_path = os.path.join(data_directory, "%s.%s" % (input_file, extension))
        if os.path.isfile(check_path):
            texture_path = check_path
            break

    base_node = generate_image_node(mat, texture_path, pixel_data=bitmap_file)
    if not base_node.image == None:
        base_node.image.alpha_mode = 'CHANNEL_PACKED'

    base_node.location = Vector((-1600, 500))

    connect_inputs(mat.node_tree, base_node, "Color", bdsf_principled, "Base Color")

def generate_h3_shader(mat, shader_path, report):
    # 0 = Shader generation is disabled
    # 1 = Simple shader generation. Only the base map is generated
    # 2 = Full Shader generation
    if not int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 0:
        if not shader_path == None:
            if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                generate_h3_shader_simple(mat, shader_path, report)
            else:
                print("Skipping shader")
                #generate_shader_environment(mat, shader, report)

        else:
            print("Halo 3 xml shader path returned as none. Something went horribly wrong")

    else:
        print("Shader generation is disabled. Skipping")

def find_h1_shader_tag(import_filepath, material_name):
    shader_extensions = ["shader_environment", 
                         "shader_model", 
                         "shader_transparent_chicago", 
                         "shader_transparent_chicago_extended", 
                         "shader_transparent_generic", 
                         "shader_transparent_glass", 
                         "shader_transparent_meter",
                         "shader_transparent_plasma", 
                         "shader_transparent_water"]

    material_name = material_name.lower()
    symbols_list, processed_name = mesh_processing.gather_symbols("", material_name, "halo1")
    symbols_list, processed_name = mesh_processing.gather_symbols(symbols_list, reversed(processed_name), "halo1")
    processed_name, permutation_index = mesh_processing.get_shader_permutation(processed_name)

    data_path = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_data_path.lower()
    tag_path = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_tag_path.lower()

    shader_path = None
    shader_tag = None
    shader_extension = None

    if not global_functions.string_empty_check(data_path) and not global_functions.string_empty_check(tag_path):
        import_directory = os.path.dirname(os.path.dirname(import_filepath)).lower()
        result = import_directory.split(data_path)
        local_path = None
        if len(result) == 2:
            local_path = result[1]

        if local_path:
            import_shader_directory = os.path.join(tag_path, local_path, "shaders")
            if os.path.exists(import_shader_directory):
                for file in os.listdir(import_shader_directory):
                    file_name = os.path.basename(file).lower()
                    result = file_name.rsplit(".", 1)
                    if len(result) == 2:
                        file_name = result[0]
                        extension = result[1]

                    if material_name == file_name and extension in shader_extensions:
                        shader_path = os.path.join(import_shader_directory, file)
                        shader_extension = extension
                        break
                        
        if shader_path == None:
            for root, dirs, filenames in os.walk(tag_path):
                for filename in filenames:
                    file = os.path.join(root, filename).lower()

                    file_name = os.path.basename(file)
                    extension = None
                    result = file_name.rsplit(".", 1)
                    if len(result) == 2:
                        file_name = result[0]
                        extension = result[1]

                    if material_name == file_name and extension in shader_extensions:
                        shader_path = file
                        shader_extension = extension
                        break

        if not shader_path == None:
            tag_group = ""
            if shader_extension == "shader_environment":
                tag_group = "senv"

            elif shader_extension == "shader_model":
                tag_group = "soso"

            elif shader_extension == "shader_transparent_chicago":
                tag_group = "schi"

            elif shader_extension == "shader_transparent_chicago_extended":
                tag_group = "scex"

            elif shader_extension == "shader_transparent_generic":
                tag_group = "sotr"

            elif shader_extension == "shader_transparent_glass":
                tag_group = "sgla"

            elif shader_extension == "shader_transparent_meter":
                tag_group = "smet"

            elif shader_extension == "spla":
                tag_group = "shader_transparent_plasma"

            elif shader_extension == "swat":
                tag_group = "shader_transparent_water"

            local_path = shader_path.split(tag_path)[1].rsplit(".", 1)[0]

            shader_tag = tag_format.TagAsset.TagRef(tag_group, local_path, len(local_path))

        else:
            print("Halo 1 Shader path wasn't set. Something went terribly wrong when trying to find %s shader" % material_name)

    else:
       print("Your Halo 1 data and tag paths are not set. Please set them in preferences and restart Blender") 

    return shader_tag

def find_h2_shader_tag(import_filepath, material_name):
    data_path = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_data_path.lower()
    tag_path = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_tag_path.lower()
    shader_path = None
    shader_tag = None

    if not global_functions.string_empty_check(data_path) and not global_functions.string_empty_check(tag_path):
        shader_collection_dic = {}
        shader_collection_path = os.path.join(bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_tag_path, r"scenarios\shaders\shader_collections.shader_collections")
        if os.path.isfile(shader_collection_path):
            shader_collection_file = open(shader_collection_path, "r")
            for line in shader_collection_file.readlines():
                if not global_functions.string_empty_check(line) and not line.startswith(";"):
                    split_result = line.split()
                    if len(split_result) == 2:
                        prefix = split_result[0]
                        path = split_result[1]
                        shader_collection_dic[prefix] = path

        processed_name, processed_parameters = mesh_processing.gather_parameters(material_name.lower())
        symbols_list, processed_name = mesh_processing.gather_symbols("", processed_name, "halo2")
        symbols_list, processed_name = mesh_processing.gather_symbols(symbols_list, reversed(processed_name), "halo2")
        processed_name = "".join(reversed(processed_name)).strip()
        result = processed_name.split(" ", 1)
        collection = None
        shader_name = None
        if len(result) >= 2:
            collection = result[0]
            shader_name = result[1]
        else:
            shader_name = processed_name

        if not collection == None:
            shader_directory = shader_collection_dic.get(collection)
            if not shader_directory == None:
                import_shader_directory = os.path.join(tag_path, shader_directory.lower())
                for root, dirs, filenames in os.walk(import_shader_directory):
                    for filename in filenames:
                        file = os.path.join(root, filename).lower()

                        file_name = os.path.basename(file)
                        extension = None
                        result = file_name.rsplit(".", 1)
                        if len(result) == 2:
                            file_name = result[0]
                            extension = result[1]

                        if shader_name == file_name and extension == "shader":
                            shader_path = file
                            break

        if shader_path == None:
            import_directory = os.path.dirname(os.path.dirname(import_filepath)).lower()
            result = import_directory.split(data_path)
            local_path = None
            if len(result) == 2:
                local_path = result[1]

            if local_path:
                import_shader_directory = os.path.join(tag_path, local_path, "shaders")
                if os.path.exists(import_shader_directory):
                    for file in os.listdir(import_shader_directory):
                        file_name = os.path.basename(file).lower()
                        extension = None
                        result = file_name.rsplit(".", 1)
                        if len(result) == 2:
                            file_name = result[0]
                            extension = result[1]

                        if shader_name == file_name and extension in "shader":
                            shader_path = os.path.join(import_shader_directory, file)
                            break
                        
        if shader_path == None:
            for root, dirs, filenames in os.walk(tag_path):
                for filename in filenames:
                    file = os.path.join(root, filename).lower()

                    file_name = os.path.basename(file)
                    extension = None
                    result = file_name.rsplit(".", 1)
                    if len(result) == 2:
                        file_name = result[0]
                        extension = result[1]

                    if shader_name == file_name and extension in "shader":
                        shader_path = file
                        break

        if not shader_path == None:
            local_path = shader_path.split(tag_path)[1].rsplit(".", 1)[0]

            shader_tag = tag_format.TagAsset.TagRef("shad", local_path, len(local_path))

        else:
            print("Halo 2 Shader path wasn't set. Something went terribly wrong when trying to find %s shader" % material_name)

    else:
       print("Your Halo 2 data and tag paths are not set. Please set them in preferences and restart Blender") 

    return shader_tag

def find_h3_shader_tag(import_filepath, material_name):
    shader_extensions = ["shader", 
                         "shader_cortana", 
                         "shader_custom", 
                         "shader_decal", 
                         "shader_foliage", 
                         "shader_halogram", 
                         "shader_skin",
                         "shader_terrain", 
                         "shader_water"]

    data_path = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_3_data_path.lower()
    tag_path = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_3_tag_path.lower()
    shader_path = None

    if not global_functions.string_empty_check(data_path) and not global_functions.string_empty_check(tag_path):
        shader_collection_dic = {}
        shader_collection_path = os.path.join(bpy.context.preferences.addons["io_scene_halo"].preferences.halo_3_tag_path, r"levels\shader_collections.txt")
        if os.path.isfile(shader_collection_path):
            shader_collection_file = open(shader_collection_path, "r")
            for line in shader_collection_file.readlines():
                if not global_functions.string_empty_check(line) and not line.startswith(";"):
                    split_result = line.split()
                    if len(split_result) == 2:
                        prefix = split_result[0]
                        path = split_result[1]
                        shader_collection_dic[prefix] = path

        processed_name, processed_parameters = mesh_processing.gather_parameters(material_name.lower())
        symbols_list, processed_name = mesh_processing.gather_symbols("", processed_name, "halo3")
        symbols_list, processed_name = mesh_processing.gather_symbols(symbols_list, reversed(processed_name), "halo3")
        processed_name = "".join(reversed(processed_name)).strip()
        result = processed_name.split(" ", 1)
        collection = None
        shader_name = None
        if len(result) >= 2:
            collection = result[0]
            shader_name = result[1]
        else:
            shader_name = processed_name

        if not collection == None:
            shader_directory = shader_collection_dic.get(collection)
            if not shader_directory == None:
                import_shader_directory = os.path.join(tag_path, shader_directory.lower())
                for root, dirs, filenames in os.walk(import_shader_directory):
                    for filename in filenames:
                        file = os.path.join(root, filename).lower()

                        file_name = os.path.basename(file)
                        extension = None
                        result = file_name.rsplit(".", 1)
                        if len(result) == 2:
                            file_name = result[0]
                            extension = result[1]

                        if shader_name == file_name and extension in shader_extensions:
                            shader_path = file
                            break

        if shader_path == None:
            import_directory = os.path.dirname(os.path.dirname(import_filepath)).lower()
            result = import_directory.split(data_path)
            local_path = None
            if len(result) == 2:
                local_path = result[1]

            if local_path:
                import_shader_directory = os.path.join(tag_path, local_path, "shaders")
                if os.path.exists(import_shader_directory):
                    for file in os.listdir(import_shader_directory):
                        file_name = os.path.basename(file).lower()
                        extension = None
                        result = file_name.rsplit(".", 1)
                        if len(result) == 2:
                            file_name = result[0]
                            extension = result[1]

                        if shader_name == file_name and extension in shader_extensions:
                            shader_path = os.path.join(import_shader_directory, file)
                            break
                        
        if shader_path == None:
            for root, dirs, filenames in os.walk(tag_path):
                for filename in filenames:
                    file = os.path.join(root, filename).lower()

                    file_name = os.path.basename(file)
                    extension = None
                    result = file_name.rsplit(".", 1)
                    if len(result) == 2:
                        file_name = result[0]
                        extension = result[1]

                    if shader_name == file_name and extension in shader_extensions:
                        shader_path = file
                        break

        if not shader_path == None:
            local_path = shader_path.split(tag_path)[1].rsplit(".", 1)[0]

        else:
            print("Halo 3 Shader path wasn't set. Something went terribly wrong when trying to find %s shader" % material_name)

    else:
       print("Your Halo 3 data and tag paths are not set. Please set them in preferences and restart Blender") 

    return shader_path

class OpaqueTemplateEnum(Enum):
    active_camo_opaque = r'shaders\shader_templates\opaque\active_camo_opaque'
    bloom = r'shaders\shader_templates\opaque\bloom'
    decal_simple = r'shaders\shader_templates\opaque\decal_simple'
    emblem_flag = r'shaders\shader_templates\opaque\emblem_flag'
    emblem_opaque = r'shaders\shader_templates\opaque\emblem_opaque'
    emblem_overlay = r'shaders\shader_templates\opaque\emblem_overlay'
    emblem_overlay_simple = r'shaders\shader_templates\opaque\emblem_overlay_simple'
    illum = r'shaders\shader_templates\opaque\illum'
    illum_3_channel = r'shaders\shader_templates\opaque\illum_3_channel'
    illum_3_channel_opaque = r'shaders\shader_templates\opaque\illum_3_channel_opaque'
    illum_3_channel_plasma = r'shaders\shader_templates\opaque\illum_3_channel_plasma'
    illum_bloom = r'shaders\shader_templates\opaque\illum_bloom'
    illum_bloom_3_channel = r'shaders\shader_templates\opaque\illum_bloom_3_channel'
    illum_bloom_3_channel_opaque = r'shaders\shader_templates\opaque\illum_bloom_3_channel_opaque'
    illum_bloom_masked = r'shaders\shader_templates\opaque\illum_bloom_masked'
    illum_bloom_opaque = r'shaders\shader_templates\opaque\illum_bloom_opaque'
    illum_clamped = r'shaders\shader_templates\opaque\illum_clamped'
    illum_detail = r'shaders\shader_templates\opaque\illum_detail'
    illum_opaque = r'shaders\shader_templates\opaque\illum_opaque'
    illum_opaque_index = r'shaders\shader_templates\opaque\illum_opaque_index'
    illum_wrap = r'shaders\shader_templates\opaque\illum_wrap'
    overlay = r'shaders\shader_templates\opaque\overlay'
    prt_lightmap = r'shaders\shader_templates\opaque\prt_lightmap'
    prt_scarab = r'shaders\shader_templates\opaque\prt_scarab'
    prt_simple = r'shaders\shader_templates\opaque\prt_simple'
    prt_simple_lm_emissive = r'shaders\shader_templates\opaque\prt_simple_lm_emissive'
    render_layer_disabled = r'shaders\shader_templates\opaque\render_layer_disabled'
    tex_alpha_test = r'shaders\shader_templates\opaque\tex_alpha_test'
    tex_alpha_test_clamped = r'shaders\shader_templates\opaque\tex_alpha_test_clamped'
    tex_bump = r'shaders\shader_templates\opaque\tex_bump'
    tex_bump_active_camo = r'shaders\shader_templates\opaque\tex_bump_active_camo'
    tex_bump_alpha_test = r'shaders\shader_templates\opaque\tex_bump_alpha_test'
    tex_bump_alpha_test_clamped = r'shaders\shader_templates\opaque\tex_bump_alpha_test_clamped'
    tex_bump_alpha_test_clamped_single_pass = r'shaders\shader_templates\opaque\tex_bump_alpha_test_clamped_single_pass'
    tex_bump_alpha_test_detail = r'shaders\shader_templates\opaque\tex_bump_alpha_test_detail'
    tex_bump_alpha_test_single_pass = r'shaders\shader_templates\opaque\tex_bump_alpha_test_single_pass'
    tex_bump_bloom = r'shaders\shader_templates\opaque\tex_bump_bloom'
    tex_bump_clamped_multiply_map = r'shaders\shader_templates\opaque\tex_bump_clamped_multiply_map'
    tex_bump_detail_blend = r'shaders\shader_templates\opaque\tex_bump_detail_blend'
    tex_bump_detail_blend_detail = r'shaders\shader_templates\opaque\tex_bump_detail_blend_detail'
    tex_bump_detail_blend_specular = r'shaders\shader_templates\opaque\tex_bump_detail_blend_specular'
    tex_bump_detail_blend_specular_combined = r'shaders\shader_templates\opaque\tex_bump_detail_blend_specular_combined'
    tex_bump_detail_blend_specular_dblmult = r'shaders\shader_templates\opaque\tex_bump_detail_blend_specular_dblmult'
    tex_bump_detail_keep = r'shaders\shader_templates\opaque\tex_bump_detail_keep'
    tex_bump_detail_keep_blend = r'shaders\shader_templates\opaque\tex_bump_detail_keep_blend'
    tex_bump_detail_mask = r'shaders\shader_templates\opaque\tex_bump_detail_mask'
    tex_bump_detail_overlay = r'shaders\shader_templates\opaque\tex_bump_detail_overlay'
    tex_bump_dprs_env = r'shaders\shader_templates\opaque\tex_bump_dprs_env'
    tex_bump_dprs_env_illum = r'shaders\shader_templates\opaque\tex_bump_dprs_env_illum'
    tex_bump_dprs_env_illum_emissive = r'shaders\shader_templates\opaque\tex_bump_dprs_env_illum_emissive'
    tex_bump_env = r'shaders\shader_templates\opaque\tex_bump_env'
    tex_bump_env_alpha_test = r'shaders\shader_templates\opaque\tex_bump_env_alpha_test'
    tex_bump_env_alpha_test_combined = r'shaders\shader_templates\opaque\tex_bump_env_alpha_test_combined'
    tex_bump_env_alpha_test_indexed = r'shaders\shader_templates\opaque\tex_bump_env_alpha_test_indexed'
    tex_bump_env_clamped = r'shaders\shader_templates\opaque\tex_bump_env_clamped'
    tex_bump_env_clamped_combined = r'shaders\shader_templates\opaque\tex_bump_env_clamped_combined'
    tex_bump_env_combined = r'shaders\shader_templates\opaque\tex_bump_env_combined'
    tex_bump_env_dbl_spec = r'shaders\shader_templates\opaque\tex_bump_env_dbl_spec'
    tex_bump_env_detail_blend = r'shaders\shader_templates\opaque\tex_bump_env_detail_blend'
    tex_bump_env_detail_blend_specular = r'shaders\shader_templates\opaque\tex_bump_env_detail_blend_specular'
    tex_bump_env_detail_mask = r'shaders\shader_templates\opaque\tex_bump_env_detail_mask'
    tex_bump_env_detail_mask_combined = r'shaders\shader_templates\opaque\tex_bump_env_detail_mask_combined'
    tex_bump_env_detail_overlay = r'shaders\shader_templates\opaque\tex_bump_env_detail_overlay'
    tex_bump_env_detail_overlay_combined = r'shaders\shader_templates\opaque\tex_bump_env_detail_overlay_combined'
    tex_bump_env_fast_masked = r'shaders\shader_templates\opaque\tex_bump_env_fast_masked'
    tex_bump_env_four_change_color = r'shaders\shader_templates\opaque\tex_bump_env_four_change_color'
    tex_bump_env_four_change_color_combined = r'shaders\shader_templates\opaque\tex_bump_env_four_change_color_combined'
    tex_bump_env_illum = r'shaders\shader_templates\opaque\tex_bump_env_illum'
    tex_bump_env_illum_3_channel = r'shaders\shader_templates\opaque\tex_bump_env_illum_3_channel'
    tex_bump_env_illum_3_channel_combined = r'shaders\shader_templates\opaque\tex_bump_env_illum_3_channel_combined'
    tex_bump_env_illum_3_channel_combined_unfucked = r'shaders\shader_templates\opaque\tex_bump_env_illum_3_channel_combined_unfucked'
    tex_bump_env_illum_3_channel_occlusion = r'shaders\shader_templates\opaque\tex_bump_env_illum_3_channel_occlusion'
    tex_bump_env_illum_3_channel_occlusion_combined = r'shaders\shader_templates\opaque\tex_bump_env_illum_3_channel_occlusion_combined'
    tex_bump_env_illum_combined = r'shaders\shader_templates\opaque\tex_bump_env_illum_combined'
    tex_bump_env_illum_combined_emmisive_map = r'shaders\shader_templates\opaque\tex_bump_env_illum_combined_emmisive_map'
    tex_bump_env_illum_detail_honor_guard = r'shaders\shader_templates\opaque\tex_bump_env_illum_detail_honor_guard'
    tex_bump_env_illum_detail_honor_guard_base = r'shaders\shader_templates\opaque\tex_bump_env_illum_detail_honor_guard_base'
    tex_bump_env_illum_emmisive_map = r'shaders\shader_templates\opaque\tex_bump_env_illum_emmisive_map'
    tex_bump_env_illum_four_change_color = r'shaders\shader_templates\opaque\tex_bump_env_illum_four_change_color'
    tex_bump_env_illum_four_change_color_no_lod = r'shaders\shader_templates\opaque\tex_bump_env_illum_four_change_color_no_lod'
    tex_bump_env_illum_tiling_specular = r'shaders\shader_templates\opaque\tex_bump_env_illum_tiling_specular'
    tex_bump_env_illum_trace = r'shaders\shader_templates\opaque\tex_bump_env_illum_trace'
    tex_bump_env_illum_two_change_color = r'shaders\shader_templates\opaque\tex_bump_env_illum_two_change_color'
    tex_bump_env_illum_two_change_color_combined = r'shaders\shader_templates\opaque\tex_bump_env_illum_two_change_color_combined'
    tex_bump_env_no_detail = r'shaders\shader_templates\opaque\tex_bump_env_no_detail'
    tex_bump_env_tiling_specular = r'shaders\shader_templates\opaque\tex_bump_env_tiling_specular'
    tex_bump_env_two_change_color = r'shaders\shader_templates\opaque\tex_bump_env_two_change_color'
    tex_bump_env_two_change_color_combined = r'shaders\shader_templates\opaque\tex_bump_env_two_change_color_combined'
    tex_bump_env_two_change_color_indexed = r'shaders\shader_templates\opaque\tex_bump_env_two_change_color_indexed'
    tex_bump_env_two_change_color_multiply_map_self_illum = r'shaders\shader_templates\opaque\tex_bump_env_two_change_color_multiply_map_self_illum'
    tex_bump_env_two_detail = r'shaders\shader_templates\opaque\tex_bump_env_two_detail'
    tex_bump_env_two_detail_combined = r'shaders\shader_templates\opaque\tex_bump_env_two_detail_combined'
    tex_bump_foliage = r'shaders\shader_templates\opaque\tex_bump_foliage'
    tex_bump_four_change_color = r'shaders\shader_templates\opaque\tex_bump_four_change_color'
    tex_bump_illum = r'shaders\shader_templates\opaque\tex_bump_illum'
    tex_bump_illum_3_channel = r'shaders\shader_templates\opaque\tex_bump_illum_3_channel'
    tex_bump_illum_alpha_test = r'shaders\shader_templates\opaque\tex_bump_illum_alpha_test'
    tex_bump_illum_alpha_test_illum = r'shaders\shader_templates\opaque\tex_bump_illum_alpha_test_illum'
    tex_bump_illum_alpha_test_single_pass = r'shaders\shader_templates\opaque\tex_bump_illum_alpha_test_single_pass'
    tex_bump_illum_bloom = r'shaders\shader_templates\opaque\tex_bump_illum_bloom'
    tex_bump_illum_bloom_3_channel = r'shaders\shader_templates\opaque\tex_bump_illum_bloom_3_channel'
    tex_bump_illum_detail = r'shaders\shader_templates\opaque\tex_bump_illum_detail'
    tex_bump_illum_detail_honor_guard = r'shaders\shader_templates\opaque\tex_bump_illum_detail_honor_guard'
    tex_bump_illum_no_specular = r'shaders\shader_templates\opaque\tex_bump_illum_no_specular'
    tex_bump_illum_trace = r'shaders\shader_templates\opaque\tex_bump_illum_trace'
    tex_bump_illum_two_detail = r'shaders\shader_templates\opaque\tex_bump_illum_two_detail'
    tex_bump_meter_illum = r'shaders\shader_templates\opaque\tex_bump_meter_illum'
    tex_bump_multiply_map = r'shaders\shader_templates\opaque\tex_bump_multiply_map'
    tex_bump_no_alpha = r'shaders\shader_templates\opaque\tex_bump_no_alpha'
    tex_bump_no_specular = r'shaders\shader_templates\opaque\tex_bump_no_specular'
    tex_bump_one_change_color = r'shaders\shader_templates\opaque\tex_bump_one_change_color'
    tex_bump_plasma = r'shaders\shader_templates\opaque\tex_bump_plasma'
    tex_bump_plasma_one_channel_illum = r'shaders\shader_templates\opaque\tex_bump_plasma_one_channel_illum'
    tex_bump_shiny = r'shaders\shader_templates\opaque\tex_bump_shiny'
    tex_bump_terrain = r'shaders\shader_templates\opaque\tex_bump_terrain'
    tex_bump_three_detail_blend = r'shaders\shader_templates\opaque\tex_bump_three_detail_blend'
    tex_bump_tiling_specular = r'shaders\shader_templates\opaque\tex_bump_tiling_specular'
    tex_bump_two_change_color = r'shaders\shader_templates\opaque\tex_bump_two_change_color'
    tex_bump_two_change_color_multiply_map = r'shaders\shader_templates\opaque\tex_bump_two_change_color_multiply_map'
    tex_bump_two_change_color_multiply_map_self_illum = r'shaders\shader_templates\opaque\tex_bump_two_change_color_multiply_map_self_illum'
    tex_bump_two_detail = r'shaders\shader_templates\opaque\tex_bump_two_detail'
    tex_bump_two_detail_tint = r'shaders\shader_templates\opaque\tex_bump_two_detail_tint'
    tex_detail_blend = r'shaders\shader_templates\opaque\tex_detail_blend'
    tex_env = r'shaders\shader_templates\opaque\tex_env'
    tex_env_3_channel_illum = r'shaders\shader_templates\opaque\tex_env_3_channel_illum'
    tex_illum = r'shaders\shader_templates\opaque\tex_illum'
    tex_illum_bloom = r'shaders\shader_templates\opaque\tex_illum_bloom'

class TransparentTemplateEnum(Enum):
    add_illum_detail = r'shaders\shader_templates\transparent\add_illum_detail'
    bumped_environment_additive = r'shaders\shader_templates\transparent\bumped_environment_additive'
    bumped_environment_blended = r'shaders\shader_templates\transparent\bumped_environment_blended'
    bumped_environment_darkened = r'shaders\shader_templates\transparent\bumped_environment_darkened'
    bumped_environment_masked = r'shaders\shader_templates\transparent\bumped_environment_masked'
    bumped_environment_mask_colored = r'shaders\shader_templates\transparent\bumped_environment_mask_colored'
    cortana = r'shaders\shader_templates\transparent\cortana'
    cortana_holographic_active_camo = r'shaders\shader_templates\transparent\cortana_holographic_active_camo'
    lit = r'shaders\shader_templates\transparent\lit'
    meter = r'shaders\shader_templates\transparent\meter'
    meter_active_camo = r'shaders\shader_templates\transparent\meter_active_camo'
    one_add_changecolor_screenspace_xform2 = r'shaders\shader_templates\transparent\one_add_changecolor_screenspace_xform2'
    one_add_env_illum = r'shaders\shader_templates\transparent\one_add_env_illum'
    one_add_env_illum_clamped = r'shaders\shader_templates\transparent\one_add_env_illum_clamped'
    one_add_env_illum_trace = r'shaders\shader_templates\transparent\one_add_env_illum_trace'
    one_add_illum = r'shaders\shader_templates\transparent\one_add_illum'
    one_add_illum_detail = r'shaders\shader_templates\transparent\one_add_illum_detail'
    one_add_illum_no_fog = r'shaders\shader_templates\transparent\one_add_illum_no_fog'
    one_add_illum_screenspace_xform2 = r'shaders\shader_templates\transparent\one_add_illum_screenspace_xform2'
    one_add_two_plus_two = r'shaders\shader_templates\transparent\one_add_two_plus_two'
    one_alpha_env = r'shaders\shader_templates\transparent\one_alpha_env'
    one_alpha_env_active_camo = r'shaders\shader_templates\transparent\one_alpha_env_active_camo'
    one_alpha_env_clamped = r'shaders\shader_templates\transparent\one_alpha_env_clamped'
    one_alpha_env_fixed = r'shaders\shader_templates\transparent\one_alpha_env_fixed'
    one_alpha_env_illum = r'shaders\shader_templates\transparent\one_alpha_env_illum'
    one_alpha_env_illum_specular_mask = r'shaders\shader_templates\transparent\one_alpha_env_illum_specular_mask'
    one_alpha_env_plasma = r'shaders\shader_templates\transparent\one_alpha_env_plasma'
    one_alpha_env_trace = r'shaders\shader_templates\transparent\one_alpha_env_trace'
    overshield = r'shaders\shader_templates\transparent\overshield'
    overshield_tartarus = r'shaders\shader_templates\transparent\overshield_tartarus'
    particle_additive = r'shaders\shader_templates\transparent\particle_additive'
    particle_additive_tint = r'shaders\shader_templates\transparent\particle_additive_tint'
    particle_alpha_blend = r'shaders\shader_templates\transparent\particle_alpha_blend'
    particle_alpha_blend_tint = r'shaders\shader_templates\transparent\particle_alpha_blend_tint'
    particle_alpha_multiply_add = r'shaders\shader_templates\transparent\particle_alpha_multiply_add'
    particle_alpha_multiply_add_tint = r'shaders\shader_templates\transparent\particle_alpha_multiply_add_tint'
    particle_alpha_test = r'shaders\shader_templates\transparent\particle_alpha_test'
    particle_alpha_test_no_lighting = r'shaders\shader_templates\transparent\particle_alpha_test_no_lighting'
    particle_alpha_test_no_lighting_fixed_for_glass = r'shaders\shader_templates\transparent\particle_alpha_test_no_lighting_fixed_for_glass'
    particle_alpha_test_tint = r'shaders\shader_templates\transparent\particle_alpha_test_tint'
    particle_alpha_test_tint_no_lighting = r'shaders\shader_templates\transparent\particle_alpha_test_tint_no_lighting'
    particle_plasma = r'shaders\shader_templates\transparent\particle_plasma'
    plasma_1_channel = r'shaders\shader_templates\transparent\plasma_1_channel'
    plasma_alpha = r'shaders\shader_templates\transparent\plasma_alpha'
    plasma_alpha_active_camo = r'shaders\shader_templates\transparent\plasma_alpha_active_camo'
    plasma_mask_offset = r'shaders\shader_templates\transparent\plasma_mask_offset'
    plasma_mask_offset_active_camo = r'shaders\shader_templates\transparent\plasma_mask_offset_active_camo'
    plasma_shield = r'shaders\shader_templates\transparent\plasma_shield'
    plasma_shield_change_color = r'shaders\shader_templates\transparent\plasma_shield_change_color'
    plasma_time = r'shaders\shader_templates\transparent\plasma_time'
    roadsign_glass_newmombasa = r'shaders\shader_templates\transparent\roadsign_glass_newmombasa'
    sky_one_add_illum_detail = r'shaders\shader_templates\transparent\sky_one_add_illum_detail'
    sky_one_add_two_plus_two = r'shaders\shader_templates\transparent\sky_one_add_two_plus_two'
    sky_one_alpha_env = r'shaders\shader_templates\transparent\sky_one_alpha_env'
    sky_one_alpha_env_clamped = r'shaders\shader_templates\transparent\sky_one_alpha_env_clamped'
    sky_one_alpha_env_illum = r'shaders\shader_templates\transparent\sky_one_alpha_env_illum'
    sky_two_add_clouds = r'shaders\shader_templates\transparent\sky_two_add_clouds'
    sky_two_add_clouds_clamped = r'shaders\shader_templates\transparent\sky_two_add_clouds_clamped'
    sky_two_add_detail_masked = r'shaders\shader_templates\transparent\sky_two_add_detail_masked'
    sky_two_alpha_clouds = r'shaders\shader_templates\transparent\sky_two_alpha_clouds'
    tartarus_shield = r'shaders\shader_templates\transparent\tartarus_shield'
    trace = r'shaders\shader_templates\transparent\trace'
    transparent_glass = r'shaders\shader_templates\transparent\transparent_glass'
    two_add_clouds = r'shaders\shader_templates\transparent\two_add_clouds'
    two_add_detail_masked = r'shaders\shader_templates\transparent\two_add_detail_masked'
    two_add_detail_masked_prepass = r'shaders\shader_templates\transparent\two_add_detail_masked_prepass'
    two_add_detail_masked_trace = r'shaders\shader_templates\transparent\two_add_detail_masked_trace'
    two_add_env_illum = r'shaders\shader_templates\transparent\two_add_env_illum'
    two_add_env_illum_3_channel = r'shaders\shader_templates\transparent\two_add_env_illum_3_channel'
    two_add_env_illum_active_camo = r'shaders\shader_templates\transparent\two_add_env_illum_active_camo'
    two_add_tint = r'shaders\shader_templates\transparent\two_add_tint'
    two_alpha_clouds = r'shaders\shader_templates\transparent\two_alpha_clouds'
    two_alpha_detail_masked = r'shaders\shader_templates\transparent\two_alpha_detail_masked'
    two_alpha_env_detail = r'shaders\shader_templates\transparent\two_alpha_env_detail'
    two_alpha_env_illum = r'shaders\shader_templates\transparent\two_alpha_env_illum'
    two_alpha_env_illum_bumped_environment_masked = r'shaders\shader_templates\transparent\two_alpha_env_illum_bumped_environment_masked'
    two_alpha_env_multichannel = r'shaders\shader_templates\transparent\two_alpha_env_multichannel'
    two_alpha_env_two_change_color = r'shaders\shader_templates\transparent\two_alpha_env_two_change_color'
    two_alpha_two_change_color = r'shaders\shader_templates\transparent\two_alpha_two_change_color'
    waterfall = r'shaders\shader_templates\transparent\waterfall'
    waves = r'shaders\shader_templates\transparent\waves'
    z_only_active_camo = r'shaders\shader_templates\transparent\z_only_active_camo'

def conver_real_rgba_integer_bgra(material_color):
    return (round(material_color[2] * 255), round(material_color[1] * 255), round(material_color[0] * 255), 0)

def add_animation_property(SHADER, TAG, property_list, animation_type=AnimationTypeEnum.bitmap_index, input_name="", input_type=0, range_name="", range_type=0, time=0,
                           output_modifier=0, output_modifier_input=0, function_header=None, function_type=FunctionTypeEnum.constant, output_value=0,
                           material_colors=((0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)), lower_bound=0.0, upper_bound=1.0,
                           input_function=(0.0, 0.0, 0, 0.0, 0.0, []), range_function=(0.0, 0.0, 0, 0.0, 0.0, []), range_lower_bound=1.0, range_upper_bound=1.0):
    animation_property = ShaderAsset.AnimationProperty()

    animation_property.type = animation_type.value
    animation_property.input_name = input_name
    animation_property.input_name_length = len(input_name)
    animation_property.input_type = input_type
    animation_property.range_name = range_name
    animation_property.range_name_length = len(range_name)
    animation_property.range_type = range_type
    animation_property.time_period = time
    animation_property.output_modifier = output_modifier
    animation_property.output_modifier_input = output_modifier_input
    animation_property.map_property_header = TAG.TagBlockHeader("MAPP", 1, 1, 12)
    animation_property.function_header = function_header
    animation_property.function_type = function_type.value
    animation_property.range_check = output_value
    animation_property.input_function_data = ShaderAsset.FunctionData()
    animation_property.range_function_data = ShaderAsset.FunctionData()
    animation_property.upper_bound = upper_bound
    animation_property.lower_bound = lower_bound
    animation_property.range_upper_bound = range_lower_bound
    animation_property.range_lower_bound = range_upper_bound
    animation_property.color_a = conver_real_rgba_integer_bgra(material_colors[0])
    animation_property.color_b = conver_real_rgba_integer_bgra(material_colors[1])
    animation_property.color_c = conver_real_rgba_integer_bgra(material_colors[2])
    animation_property.color_d = conver_real_rgba_integer_bgra(material_colors[3])

    animation_property.input_function_data.points = []
    animation_property.range_function_data.points = []
    if FunctionTypeEnum.transition == function_type:
        animation_property.input_function_data.min = input_function[0]
        animation_property.input_function_data.max = input_function[1]
        animation_property.input_function_data.exponent = input_function[2]
        animation_property.input_function_data.frequency = input_function[3]
        animation_property.input_function_data.phase = input_function[4]

        animation_property.range_function_data.min = range_function[0]
        animation_property.range_function_data.max = range_function[1]
        animation_property.range_function_data.exponent = range_function[2]
        animation_property.range_function_data.frequency = range_function[3]
        animation_property.range_function_data.phase = range_function[4]

    elif FunctionTypeEnum.periodic == function_type:
        animation_property.input_function_data.min = input_function[0]
        animation_property.input_function_data.max = input_function[1]
        animation_property.input_function_data.exponent = input_function[2]
        animation_property.input_function_data.frequency = input_function[3]
        animation_property.input_function_data.phase = input_function[4]

        animation_property.range_function_data.min = range_function[0]
        animation_property.range_function_data.max = range_function[1]
        animation_property.range_function_data.exponent = range_function[2]
        animation_property.range_function_data.frequency = range_function[3]
        animation_property.range_function_data.phase = range_function[4]

    elif FunctionTypeEnum.linear == function_type:
        animation_property.input_function_data.points = input_function[5]
        animation_property.range_function_data.points = range_function[5]
    elif FunctionTypeEnum.linear_key == function_type:
        animation_property.input_function_data.points = input_function[5]
        animation_property.range_function_data.points = range_function[5]
    elif FunctionTypeEnum.multi_linear_key == function_type:
        animation_property.input_function_data.points = input_function[5]
        animation_property.range_function_data.points = range_function[5]
    elif FunctionTypeEnum.spline == function_type:
        animation_property.input_function_data.points = input_function[5]
        animation_property.range_function_data.points = range_function[5]
    elif FunctionTypeEnum.multi_spline == function_type:
        animation_property.input_function_data.points = input_function[5]
        animation_property.range_function_data.points = range_function[5]

    property_list.append(animation_property)

def add_parameter(SHADER, TAG, parameter_name="", enum=TypeEnum.bitmap, bitmap_name="", float_value=1.0, rgba=(0.0, 0.0, 0.0, 1.0)):
    parameter = ShaderAsset.Parameter()

    path = bitmap_name
    if len(bitmap_name) > 0 :
        path = tag_format.get_patched_name(TAG.upgrade_patches, bitmap_name).replace(" ", "_")

    parameter.name = parameter_name
    parameter.type = enum.value
    parameter.bitmap = TAG.TagRef("bitm", path, len(path))
    parameter.const_value = float_value
    parameter.const_color = rgba

    return parameter

def get_percentage(channel):
    value = 0.0
    if not channel == 0:
        value = channel / 255

    return value

def get_rgb_percentage(rgb, has_alpha=True):
    if has_alpha:
        result = (1, 1, 1, 0)
        if rgb:
            r = get_percentage(rgb["R"])
            g = get_percentage(rgb["G"])
            b = get_percentage(rgb["B"])
            a = 0

            a_dic = rgb.get("A")
            if a_dic:
                a = get_percentage(a_dic)

            result = (r, g, b, a)

    else:
        result = (1, 1, 1)
        if rgb:
            r = get_percentage(rgb["R"])
            g = get_percentage(rgb["G"])
            b = get_percentage(rgb["B"])
            result = (r, g, b)

    return result

def convert_legacy_function(PARTICLE, TAG, properties, input_type=0, range_type=0, function_type=FunctionTypeEnum.constant, flag_value=0, output_modifier=0,
                            output_modifier_input=0, rgb_0=None, rgb_1=None, rgb_2=None, rgb_3=None, value_0=0, value_1=0, value_2=0, value_3=0, function_0_type=0,
                            function_1_type=0, function_values=[], function_header=None):
    input_function=(0.0, 0.0, 0, 0.0, 0.0, [])
    range_function=(0.0, 0.0, 0, 0.0, 0.0, [])
    if FunctionTypeEnum.transition == function_type:
        min = function_values[0]
        max = function_values[1]
        exponent = function_0_type
        frequency = 0.0
        phase = 0.0

        range_min = function_values[2]
        range_max = function_values[3]
        range_exponent = function_1_type
        range_frequency = 0.0
        range_phase = 0.0

        input_function=(min, max, exponent, frequency, phase, [])
        range_function=(range_min, range_max, range_exponent, range_frequency, range_phase, [])

    elif FunctionTypeEnum.periodic == function_type:
        min = function_values[2]
        max = function_values[3]
        exponent = function_0_type
        frequency = function_values[0]
        phase = function_values[1]

        range_min = function_values[6]
        range_max = function_values[7]
        range_exponent = function_1_type
        range_frequency = function_values[4]
        range_phase = function_values[5]

        input_function=(min, max, exponent, frequency, phase, [])
        range_function=(range_min, range_max, range_exponent, range_frequency, range_phase, [])

    elif FunctionTypeEnum.linear == function_type:
        points = []
        range_points = []
        for point_idx in range(2):
            point_index = (point_idx * 2)
            x = function_values[point_index]
            y = function_values[point_index + 1]
            points.append((x, y))

        for point_idx in range(2):
            point_index = (6 + (point_idx * 2))
            x = function_values[point_index]
            y = function_values[point_index + 1]
            range_points.append((x, y))

        input_function=(0.0, 0.0, 0, 0.0, 0.0, points)
        range_function=(0.0, 0.0, 0, 0.0, 0.0, range_points)

    elif FunctionTypeEnum.linear_key == function_type:
        points = []
        range_points = []
        for point_idx in range(4):
            point_index = (point_idx * 2)
            x = function_values[point_index]
            y = function_values[point_index + 1]
            points.append((x, y))

        for point_idx in range(4):
            point_index = (20 + (point_idx * 2))
            x = function_values[point_index]
            y = function_values[point_index + 1]
            range_points.append((x, y))

        input_function=(0.0, 0.0, 0, 0.0, 0.0, points)
        range_function=(0.0, 0.0, 0, 0.0, 0.0, range_points)

    elif FunctionTypeEnum.multi_linear_key == function_type:
        points = []
        range_points = []
        for point_idx in range(2):
            point_index = (point_idx * 2)
            x = function_values[point_index]
            y = function_values[point_index + 1]
            points.append((x, y))

        for point_idx in range(2):
            point_index = (4 + (point_idx * 2))
            x = function_values[point_index]
            y = function_values[point_index + 1]
            range_points.append((x, y))

        input_function=(0.0, 0.0, 0, 0.0, 0.0, points)
        range_function=(0.0, 0.0, 0, 0.0, 0.0, range_points)

    elif FunctionTypeEnum.spline == function_type:
        points = []
        range_points = []
        for point_idx in range(4):
            point_index = (point_idx * 2)
            x = function_values[point_index]
            y = function_values[point_index + 1]
            points.append((x, y))

        for point_idx in range(4):
            point_index = (12 + (point_idx * 2))
            x = function_values[point_index]
            y = function_values[point_index + 1]
            range_points.append((x, y))

        input_function=(0.0, 0.0, 0, 0.0, 0.0, points)
        range_function=(0.0, 0.0, 0, 0.0, 0.0, range_points)

    elif FunctionTypeEnum.multi_spline == function_type:
        points = []
        range_points = []
        for point_idx in range(2):
            point_index = (point_idx * 2)
            x = function_values[point_index]
            y = function_values[point_index + 1]
            points.append((x, y))

        for point_idx in range(2):
            point_index = (4 + (point_idx * 2))
            x = function_values[point_index]
            y = function_values[point_index + 1]
            range_points.append((x, y))

        input_function=(0.0, 0.0, 0, 0.0, 0.0, points)
        range_function=(0.0, 0.0, 0, 0.0, 0.0, range_points)

    colors = (get_rgb_percentage(rgb_0), get_rgb_percentage(rgb_1), get_rgb_percentage(rgb_2), get_rgb_percentage(rgb_3))
    add_animation_property(PARTICLE, TAG, properties, animation_type=AnimationTypeEnum.bitmap_scale_x, input_type=input_type, range_type=range_type, output_modifier=output_modifier,
                           output_modifier_input=output_modifier_input, function_header=function_header, function_type=function_type, output_value=flag_value,
                           material_colors=colors, lower_bound=value_0, upper_bound=value_1, input_function=input_function, range_function=range_function, range_lower_bound=value_2,
                           range_upper_bound=value_3)

def function_uses_color(shader_function):
    uses_color = False
    if OutputTypeFlags._2_color in OutputTypeFlags(shader_function.output_type):
        uses_color = True
    elif OutputTypeFlags._3_color in OutputTypeFlags(shader_function.output_type):
        uses_color = True
    elif OutputTypeFlags._4_color in OutputTypeFlags(shader_function.output_type):
        uses_color = True

    return uses_color

def write_identity(output_stream, TAG, animation_properties):
    animation_properties.function_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<B', animation_properties.function_type))
    output_stream.write(struct.pack('<B', animation_properties.output_type))
    output_stream.write(struct.pack('<B', animation_properties.input_function_data.exponent))
    output_stream.write(struct.pack('<B', animation_properties.range_function_data.exponent))
    if function_uses_color(animation_properties):
        output_stream.write(struct.pack('<BBBB', animation_properties.color_a[0], animation_properties.color_a[1], animation_properties.color_a[2], animation_properties.color_a[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_b[0], animation_properties.color_b[1], animation_properties.color_b[2], animation_properties.color_b[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_c[0], animation_properties.color_c[1], animation_properties.color_c[2], animation_properties.color_c[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_d[0], animation_properties.color_d[1], animation_properties.color_d[2], animation_properties.color_d[3]))

    else:
        output_stream.write(struct.pack('<f', animation_properties.lower_bound))
        output_stream.write(struct.pack('<f', animation_properties.upper_bound))
        output_stream.write(struct.pack('<8x'))

def write_constant(output_stream, TAG, animation_properties):
    animation_properties.function_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<B', animation_properties.function_type))
    output_stream.write(struct.pack('<B', animation_properties.output_type))
    output_stream.write(struct.pack('<B', animation_properties.input_function_data.exponent))
    output_stream.write(struct.pack('<B', animation_properties.range_function_data.exponent))
    if function_uses_color(animation_properties):
        output_stream.write(struct.pack('<BBBB', animation_properties.color_a[0], animation_properties.color_a[1], animation_properties.color_a[2], animation_properties.color_a[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_b[0], animation_properties.color_b[1], animation_properties.color_b[2], animation_properties.color_b[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_c[0], animation_properties.color_c[1], animation_properties.color_c[2], animation_properties.color_c[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_d[0], animation_properties.color_d[1], animation_properties.color_d[2], animation_properties.color_d[3]))

    else:
        output_stream.write(struct.pack('<f', animation_properties.lower_bound))
        output_stream.write(struct.pack('<f', animation_properties.upper_bound))
        output_stream.write(struct.pack('<8x'))

    output_stream.write(struct.pack('<8x'))

def write_transition(output_stream, TAG, animation_properties):
    animation_properties.function_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<B', animation_properties.function_type))
    output_stream.write(struct.pack('<B', animation_properties.output_type))
    output_stream.write(struct.pack('<B', animation_properties.input_function_data.exponent))
    output_stream.write(struct.pack('<B', animation_properties.range_function_data.exponent))
    if function_uses_color(animation_properties):
        output_stream.write(struct.pack('<BBBB', animation_properties.color_a[0], animation_properties.color_a[1], animation_properties.color_a[2], animation_properties.color_a[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_b[0], animation_properties.color_b[1], animation_properties.color_b[2], animation_properties.color_b[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_c[0], animation_properties.color_c[1], animation_properties.color_c[2], animation_properties.color_c[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_d[0], animation_properties.color_d[1], animation_properties.color_d[2], animation_properties.color_d[3]))

    else:
        output_stream.write(struct.pack('<f', animation_properties.lower_bound))
        output_stream.write(struct.pack('<f', animation_properties.upper_bound))
        output_stream.write(struct.pack('<8x'))

    output_stream.write(struct.pack('<f', animation_properties.input_function_data.function_min))
    output_stream.write(struct.pack('<f', animation_properties.input_function_data.function_max))
    output_stream.write(struct.pack('<f', animation_properties.range_function_data.function_min))
    output_stream.write(struct.pack('<f', animation_properties.range_function_data.function_max))

def write_periodic(output_stream, TAG, animation_properties):
    animation_properties.function_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<B', animation_properties.function_type))
    output_stream.write(struct.pack('<B', animation_properties.output_type))
    output_stream.write(struct.pack('<B', animation_properties.input_function_data.exponent))
    output_stream.write(struct.pack('<B', animation_properties.range_function_data.exponent))
    if function_uses_color(animation_properties):
        output_stream.write(struct.pack('<BBBB', animation_properties.color_a[0], animation_properties.color_a[1], animation_properties.color_a[2], animation_properties.color_a[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_b[0], animation_properties.color_b[1], animation_properties.color_b[2], animation_properties.color_b[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_c[0], animation_properties.color_c[1], animation_properties.color_c[2], animation_properties.color_c[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_d[0], animation_properties.color_d[1], animation_properties.color_d[2], animation_properties.color_d[3]))

    else:
        output_stream.write(struct.pack('<f', animation_properties.lower_bound))
        output_stream.write(struct.pack('<f', animation_properties.upper_bound))
        output_stream.write(struct.pack('<8x'))

    output_stream.write(struct.pack('<f', animation_properties.input_function_data.frequency))
    output_stream.write(struct.pack('<f', animation_properties.input_function_data.phase))
    output_stream.write(struct.pack('<f', animation_properties.input_function_data.function_min))
    output_stream.write(struct.pack('<f', animation_properties.input_function_data.function_max))
    output_stream.write(struct.pack('<f', animation_properties.range_function_data.frequency))
    output_stream.write(struct.pack('<f', animation_properties.range_function_data.phase))
    output_stream.write(struct.pack('<f', animation_properties.range_function_data.function_min))
    output_stream.write(struct.pack('<f', animation_properties.range_function_data.function_max))

def write_linear(output_stream, TAG, animation_properties):
    animation_properties.function_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<B', animation_properties.function_type))
    output_stream.write(struct.pack('<B', animation_properties.output_type))
    output_stream.write(struct.pack('<B', animation_properties.input_function_data.exponent))
    output_stream.write(struct.pack('<B', animation_properties.range_function_data.exponent))
    if function_uses_color(animation_properties):
        output_stream.write(struct.pack('<BBBB', animation_properties.color_a[0], animation_properties.color_a[1], animation_properties.color_a[2], animation_properties.color_a[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_b[0], animation_properties.color_b[1], animation_properties.color_b[2], animation_properties.color_b[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_c[0], animation_properties.color_c[1], animation_properties.color_c[2], animation_properties.color_c[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_d[0], animation_properties.color_d[1], animation_properties.color_d[2], animation_properties.color_d[3]))

    else:
        output_stream.write(struct.pack('<f', animation_properties.lower_bound))
        output_stream.write(struct.pack('<f', animation_properties.upper_bound))
        output_stream.write(struct.pack('<8x'))

    for point in animation_properties.input_function_data.points:
        output_stream.write(struct.pack('<ff', point[0], point[1]))

    output_stream.write(struct.pack('<8x'))
    for point in animation_properties.range_function_data.points:
        output_stream.write(struct.pack('<ff', point[0], point[1]))

    output_stream.write(struct.pack('<8x'))

def write_linear_key(output_stream, TAG, animation_properties):
    animation_properties.function_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<B', animation_properties.function_type))
    output_stream.write(struct.pack('<B', animation_properties.output_type))
    output_stream.write(struct.pack('<B', animation_properties.input_function_data.exponent))
    output_stream.write(struct.pack('<B', animation_properties.range_function_data.exponent))
    if function_uses_color(animation_properties):
        output_stream.write(struct.pack('<BBBB', animation_properties.color_a[0], animation_properties.color_a[1], animation_properties.color_a[2], animation_properties.color_a[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_b[0], animation_properties.color_b[1], animation_properties.color_b[2], animation_properties.color_b[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_c[0], animation_properties.color_c[1], animation_properties.color_c[2], animation_properties.color_c[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_d[0], animation_properties.color_d[1], animation_properties.color_d[2], animation_properties.color_d[3]))

    else:
        output_stream.write(struct.pack('<f', animation_properties.lower_bound))
        output_stream.write(struct.pack('<f', animation_properties.upper_bound))
        output_stream.write(struct.pack('<8x'))

    for point in animation_properties.input_function_data.points:
        output_stream.write(struct.pack('<ff', point[0], point[1]))

    output_stream.write(struct.pack('<48x'))
    for point in animation_properties.range_function_data.points:
        output_stream.write(struct.pack('<ff', point[0], point[1]))

    output_stream.write(struct.pack('<48x'))

def write_multi_linear_key(output_stream, TAG, animation_properties):
    animation_properties.function_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<B', animation_properties.function_type))
    output_stream.write(struct.pack('<B', animation_properties.output_type))
    output_stream.write(struct.pack('<B', animation_properties.input_function_data.exponent))
    output_stream.write(struct.pack('<B', animation_properties.range_function_data.exponent))
    if function_uses_color(animation_properties):
        output_stream.write(struct.pack('<BBBB', animation_properties.color_a[0], animation_properties.color_a[1], animation_properties.color_a[2], animation_properties.color_a[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_b[0], animation_properties.color_b[1], animation_properties.color_b[2], animation_properties.color_b[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_c[0], animation_properties.color_c[1], animation_properties.color_c[2], animation_properties.color_c[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_d[0], animation_properties.color_d[1], animation_properties.color_d[2], animation_properties.color_d[3]))

    else:
        output_stream.write(struct.pack('<f', animation_properties.lower_bound))
        output_stream.write(struct.pack('<f', animation_properties.upper_bound))
        output_stream.write(struct.pack('<8x'))

    output_stream.write(struct.pack('<256x'))

def write_spline(output_stream, TAG, animation_properties):
    animation_properties.function_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<B', animation_properties.function_type))
    output_stream.write(struct.pack('<B', animation_properties.output_type))
    output_stream.write(struct.pack('<B', animation_properties.input_function_data.exponent))
    output_stream.write(struct.pack('<B', animation_properties.range_function_data.exponent))
    if function_uses_color(animation_properties):
        output_stream.write(struct.pack('<BBBB', animation_properties.color_a[0], animation_properties.color_a[1], animation_properties.color_a[2], animation_properties.color_a[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_b[0], animation_properties.color_b[1], animation_properties.color_b[2], animation_properties.color_b[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_c[0], animation_properties.color_c[1], animation_properties.color_c[2], animation_properties.color_c[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_d[0], animation_properties.color_d[1], animation_properties.color_d[2], animation_properties.color_d[3]))

    else:
        output_stream.write(struct.pack('<f', animation_properties.lower_bound))
        output_stream.write(struct.pack('<f', animation_properties.upper_bound))
        output_stream.write(struct.pack('<8x'))

    for point in animation_properties.input_function_data.points:
        output_stream.write(struct.pack('<ff', point[0], point[1]))

    output_stream.write(struct.pack('<16x'))
    for point in animation_properties.range_function_data.points:
        output_stream.write(struct.pack('<ff', point[0], point[1]))

    output_stream.write(struct.pack('<16x'))

def write_multi_spline(output_stream, TAG, animation_properties):
    animation_properties.function_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<B', animation_properties.function_type))
    output_stream.write(struct.pack('<B', animation_properties.output_type))
    output_stream.write(struct.pack('<B', animation_properties.input_function_data.exponent))
    output_stream.write(struct.pack('<B', animation_properties.range_function_data.exponent))
    if function_uses_color(animation_properties):
        output_stream.write(struct.pack('<BBBB', animation_properties.color_a[0], animation_properties.color_a[1], animation_properties.color_a[2], animation_properties.color_a[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_b[0], animation_properties.color_b[1], animation_properties.color_b[2], animation_properties.color_b[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_c[0], animation_properties.color_c[1], animation_properties.color_c[2], animation_properties.color_c[3]))
        output_stream.write(struct.pack('<BBBB', animation_properties.color_d[0], animation_properties.color_d[1], animation_properties.color_d[2], animation_properties.color_d[3]))

    else:
        output_stream.write(struct.pack('<f', animation_properties.lower_bound))
        output_stream.write(struct.pack('<f', animation_properties.upper_bound))
        output_stream.write(struct.pack('<8x'))

    output_stream.write(struct.pack('<32x'))

def write_parameters(output_stream, TAG, parameters, parameters_header):
    if len(parameters) > 0:
        parameters_header.write(output_stream, TAG, True)
        for parameter_element in parameters:
            output_stream.write(struct.pack('>I', len(parameter_element.name)))
            output_stream.write(struct.pack('<H', parameter_element.type))
            output_stream.write(struct.pack('<2x'))
            parameter_element.bitmap.write(output_stream, False, True)
            output_stream.write(struct.pack('<f', parameter_element.const_value))
            output_stream.write(struct.pack('<fff', parameter_element.const_color[0], parameter_element.const_color[1], parameter_element.const_color[2]))
            parameter_element.animation_properties_tag_block.write(output_stream, False)

        for parameter_element in parameters:
            name_length = len(parameter_element.name)
            bitmap_name_length = len(parameter_element.bitmap.name)
            if name_length > 0:
                output_stream.write(struct.pack('<%ss' % name_length, TAG.string_to_bytes(parameter_element.name, False)))
            if bitmap_name_length > 0:
                output_stream.write(struct.pack('<%ssx' % bitmap_name_length, TAG.string_to_bytes(parameter_element.bitmap.name, False)))

            if len(parameter_element.animation_properties) > 0:
                parameter_element.animation_properties_header.write(output_stream, TAG, True)
                for animation_properties in parameter_element.animation_properties:
                    output_stream.write(struct.pack('<H', animation_properties.type))
                    output_stream.write(struct.pack('<2x'))
                    output_stream.write(struct.pack('>I', len(animation_properties.input_name)))
                    output_stream.write(struct.pack('>I', len(animation_properties.range_name)))
                    output_stream.write(struct.pack('<f', animation_properties.time_period))

                    write_function_size(output_stream, animation_properties)

                for animation_properties in parameter_element.animation_properties:
                    input_name_length = len(animation_properties.input_name)
                    range_name_length = len(animation_properties.range_name)
                    if input_name_length > 0:
                        output_stream.write(struct.pack('<%ss' % input_name_length, TAG.string_to_bytes(animation_properties.input_name, False)))
                    if range_name_length > 0:
                        output_stream.write(struct.pack('<%ss' % range_name_length, TAG.string_to_bytes(animation_properties.range_name, False)))

                    write_function(output_stream, TAG, animation_properties)

def write_function_size(output_stream, function_property):
    function_type = FunctionTypeEnum(function_property.function_type)
    if FunctionTypeEnum.identity == function_type:
        output_stream.write(struct.pack('<I', 20))

    elif FunctionTypeEnum.constant == function_type:
        output_stream.write(struct.pack('<I', 28))

    elif FunctionTypeEnum.transition == function_type:
        output_stream.write(struct.pack('<I', 36))

    elif FunctionTypeEnum.periodic == function_type:
        output_stream.write(struct.pack('<I', 52))

    elif FunctionTypeEnum.linear == function_type:
        output_stream.write(struct.pack('<I', 68))

    elif FunctionTypeEnum.linear_key == function_type:
        output_stream.write(struct.pack('<I', 180))

    elif FunctionTypeEnum.multi_linear_key == function_type:
        output_stream.write(struct.pack('<I', 276))

    elif FunctionTypeEnum.spline == function_type:
        output_stream.write(struct.pack('<I', 116))

    elif FunctionTypeEnum.multi_spline == function_type:
        output_stream.write(struct.pack('<I', 52))

    elif FunctionTypeEnum.exponent == function_type:
        output_stream.write(struct.pack('<I', 44))

    elif FunctionTypeEnum.spline2 == function_type:
        output_stream.write(struct.pack('<I', 116))

    output_stream.write(struct.pack('<8x'))

def write_function(output_stream, TAG, function_property):
    function_property.MAPP_header.write(output_stream, TAG, True)
    function_type = FunctionTypeEnum(function_property.function_type)
    if FunctionTypeEnum.identity == function_type:
        write_identity(output_stream, TAG, function_property)
    elif FunctionTypeEnum.constant == function_type:
        write_constant(output_stream, TAG, function_property)
    elif FunctionTypeEnum.transition == function_type:
        write_transition(output_stream, TAG, function_property)
    elif FunctionTypeEnum.periodic == function_type:
        write_periodic(output_stream, TAG, function_property)
    elif FunctionTypeEnum.linear == function_type:
        write_linear(output_stream, TAG, function_property)
    elif FunctionTypeEnum.linear_key == function_type:
        write_linear_key(output_stream, TAG, function_property)
    elif FunctionTypeEnum.multi_linear_key == function_type:
        write_multi_linear_key(output_stream, TAG, function_property)
    elif FunctionTypeEnum.spline == function_type:
        write_spline(output_stream, TAG, function_property)
    elif FunctionTypeEnum.multi_spline == function_type:
        write_multi_spline(output_stream, TAG, function_property)
    elif FunctionTypeEnum.exponent == function_type:
        write_constant(output_stream, TAG, function_property)
    elif FunctionTypeEnum.spline2 == function_type:
        write_constant(output_stream, TAG, function_property)
