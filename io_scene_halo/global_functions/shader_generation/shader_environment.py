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

import bpy

from enum import Flag, Enum, auto
from mathutils import Vector
from ...global_functions import global_functions
from ...file_tag.tag_interface import tag_interface, tag_common
from .shader_helper import (
    convert_to_blender_color, 
    set_image_scale, 
    get_output_material_node, 
    connect_inputs, 
    generate_image_node,
    place_node,
    HALO_1_SHADER_RESOURCES
    )

class DiffuseFlags(Flag):
    rescale_detail_maps = auto()
    rescale_bump_maps = auto()

class EnvironmentFlags(Flag):
    alpha_tested = auto()
    bump_map_is_specular_mask = auto()
    true_atmospheric_fog = auto()
    use_alternate_bump_attenuation = auto()

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

def get_shader_environment_node(tree):
    if not bpy.data.node_groups.get("shader_environment"):
        with bpy.data.libraries.load(HALO_1_SHADER_RESOURCES) as (data_from, data_to):
            data_to.node_groups.append(data_from.node_groups[data_from.node_groups.index('shader_environment')])

    shader_environment_node = tree.nodes.new('ShaderNodeGroup')
    shader_environment_node.node_tree = bpy.data.node_groups.get("shader_environment")

    return shader_environment_node

def generate_shader_environment(mat, shader_asset, permutation_index, asset_cache, report):
    tag_groups = tag_common.h1_tag_groups
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    diffuse_flags = DiffuseFlags(shader_data["flags_2"])
    rescale_detail = DiffuseFlags.rescale_detail_maps in diffuse_flags
    rescale_bump = DiffuseFlags.rescale_bump_maps in diffuse_flags
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node, 0)

    shader_environment_node = get_shader_environment_node(mat.node_tree)
    place_node(shader_environment_node, 1)
    shader_environment_node.name = "Shader Environment"
    shader_environment_node.width = 400.0
    shader_environment_node.height = 100.0

    connect_inputs(mat.node_tree, shader_environment_node, "Shader", output_material_node, "Surface")

    base_map_texture = generate_image_node(mat, shader_data["base map"], permutation_index, asset_cache, "halo1", report)
    base_bitmap = tag_interface.get_disk_asset(shader_data["base map"]["path"], tag_groups.get(shader_data["base map"]["group name"]))
    if base_map_texture:
        base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        base_map_node.image = base_map_texture
        base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        place_node(base_map_node, 2)
        connect_inputs(mat.node_tree, base_map_node, "Color", shader_environment_node, "Base Map")
        connect_inputs(mat.node_tree, base_map_node, "Alpha", shader_environment_node, "Base Map Alpha")

    primary_detail_texture = generate_image_node(mat, shader_data["primary detail map"], permutation_index, asset_cache, "halo1", report)
    if primary_detail_texture:
        primary_detail_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        primary_detail_node.image = primary_detail_texture
        primary_detail_node.image.alpha_mode = 'CHANNEL_PACKED'
        place_node(primary_detail_node, 2, 1)
        connect_inputs(mat.node_tree, primary_detail_node, "Color", shader_environment_node, "Primary Detail Map")
        connect_inputs(mat.node_tree, primary_detail_node, "Alpha", shader_environment_node, "Primary Detail Map Alpha")

        pdm_scale = shader_data["primary detail map scale"]
        if pdm_scale == 0.0:
            pdm_scale = 1.0

        pdm_image_scale = (pdm_scale, pdm_scale, pdm_scale)

        primary_detail_bitmap = tag_interface.get_disk_asset(shader_data["primary detail map"]["path"], tag_groups.get(shader_data["primary detail map"]["group name"]))
        set_image_scale(mat, primary_detail_node, pdm_image_scale, rescale_detail, base_bitmap, primary_detail_bitmap, permutation_index)

    secondary_detail_texture = generate_image_node(mat, shader_data["secondary detail map"], permutation_index, asset_cache, "halo1", report)
    if secondary_detail_texture:
        secondary_detail_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        secondary_detail_node.image = secondary_detail_texture
        secondary_detail_node.image.alpha_mode = 'CHANNEL_PACKED'
        place_node(secondary_detail_node, 2, 2)
        connect_inputs(mat.node_tree, secondary_detail_node, "Color", shader_environment_node, "Secondary Detail Map")
        connect_inputs(mat.node_tree, secondary_detail_node, "Alpha", shader_environment_node, "Secondary Detail Map Alpha")

        sdm_scale = shader_data["secondary detail map scale"]
        if sdm_scale == 0.0:
            sdm_scale = 1.0

        sdm_image_scale = (sdm_scale, sdm_scale, sdm_scale)

        secondary_detail_bitmap = tag_interface.get_disk_asset(shader_data["secondary detail map"]["path"], tag_groups.get(shader_data["secondary detail map"]["group name"]))
        set_image_scale(mat, secondary_detail_node, sdm_image_scale, rescale_detail, base_bitmap, secondary_detail_bitmap, permutation_index)

    micro_detail_texture = generate_image_node(mat, shader_data["micro detail map"], permutation_index, asset_cache, "halo1", report)
    if micro_detail_texture:
        micro_detail_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        micro_detail_node.image = micro_detail_texture
        micro_detail_node.image.alpha_mode = 'CHANNEL_PACKED'
        place_node(micro_detail_node, 2, 3)
        connect_inputs(mat.node_tree, micro_detail_node, "Color", shader_environment_node, "Micro Detail Map")
        connect_inputs(mat.node_tree, micro_detail_node, "Alpha", shader_environment_node, "Micro Detail Map Alpha")

        mdm_scale = shader_data["micro detail map scale"]
        if mdm_scale == 0.0:
            mdm_scale = 1.0

        mdm_image_scale = (mdm_scale, mdm_scale, mdm_scale)

        micro_detail_bitmap = tag_interface.get_disk_asset(shader_data["micro detail map"]["path"], tag_groups.get(shader_data["micro detail map"]["group name"]))
        set_image_scale(mat, micro_detail_node, mdm_image_scale, rescale_detail, base_bitmap, micro_detail_bitmap, permutation_index)

    bump_texture = generate_image_node(mat, shader_data["bump map"], permutation_index, asset_cache, "halo1", report)
    bump_bitmap = None
    if bump_texture:
        bump_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        bump_node.image = bump_texture
        bump_node.image.alpha_mode = 'CHANNEL_PACKED'
        bump_node.interpolation = 'Cubic'
        bump_node.image.colorspace_settings.name = 'Non-Color'
        place_node(bump_node, 2, 4)
        connect_inputs(mat.node_tree, bump_node, "Color", shader_environment_node, "Bump Map")
        connect_inputs(mat.node_tree, bump_node, "Alpha", shader_environment_node, "Bump Map Alpha")

        bm_scale = shader_data["bump map scale"]
        if bm_scale == 0.0:
            bm_scale = 1.0

        bm_image_scale = (bm_scale, bm_scale, bm_scale)

        bump_bitmap = tag_interface.get_disk_asset(shader_data["bump map"]["path"], tag_groups.get(shader_data["bump map"]["group name"]))
        set_image_scale(mat, bump_node, bm_image_scale, rescale_bump, base_bitmap, bump_bitmap, permutation_index)

    self_illumination_texture = generate_image_node(mat, shader_data["map"], permutation_index, asset_cache, "halo1", report)
    if self_illumination_texture:
        self_illumination_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        self_illumination_node.image = self_illumination_texture
        place_node(self_illumination_node, 2, 5)
        connect_inputs(mat.node_tree, self_illumination_node, "Color", shader_environment_node, "Self-Illumination Map")

        sim_scale = shader_data["map scale"]
        if sim_scale == 0.0:
            sim_scale = 1.0

        sim_image_scale = (sim_scale, sim_scale, sim_scale)

        set_image_scale(mat, self_illumination_node, sim_image_scale)

    reflection_texture = generate_image_node(mat, shader_data["reflection cube map"], permutation_index, asset_cache, "halo1", report)
    if reflection_texture:
        reflection_node = mat.node_tree.nodes.new("ShaderNodeTexEnvironment")
        reflection_node.image = reflection_texture
        place_node(reflection_node, 2, 6)
        connect_inputs(mat.node_tree, reflection_node, "Color", shader_environment_node, "Reflection Cube Map")

    shader_environment_node.inputs["Power"].default_value = shader_data["power"]
    shader_environment_node.inputs["Color of Emitted Light"].default_value = convert_to_blender_color(shader_data["color of emitted light"], True)
    alpha_shader = EnvironmentFlags.alpha_tested in EnvironmentFlags(shader_data["flags_1"])
    if alpha_shader:
        shader_environment_node.inputs["Alpha Tested"].default_value = True
        if bpy.app.version <= (4, 2, 0):
            mat.shadow_method = 'CLIP'
        mat.blend_method = 'HASHED'

    mat.use_backface_culling = True
    shader_environment_node.inputs["Blend Type"].default_value = shader_data["shader environment type"]["value"]
    shader_environment_node.inputs["Detail Map Function"].default_value = shader_data["detail map function"]["value"]
    shader_environment_node.inputs["Micro Detail Map Function"].default_value = shader_data["micro detail map function"]["value"]
    if bump_bitmap is not None:
        shader_environment_node.inputs["Bump Strength"].default_value = bump_bitmap["Data"]["bump height"] * 15

    shader_environment_node.inputs["Primary On Color"].default_value = convert_to_blender_color(shader_data["primary on color"], True)
    shader_environment_node.inputs["Primary Off Color"].default_value = convert_to_blender_color(shader_data["primary off color"], True)
    shader_environment_node.inputs["Primary Self-Illumination Activation Level"].default_value = 0
    if not FunctionEnum.one.value == shader_data["primary animation function"]:
        shader_environment_node.inputs["Primary Self-Illumination Activation Level"].default_value = 1

    shader_environment_node.inputs["Secondary On Color"].default_value = convert_to_blender_color(shader_data["secondary on color"], True)
    shader_environment_node.inputs["Secondary Off Color"].default_value = convert_to_blender_color(shader_data["secondary off color"], True)
    shader_environment_node.inputs["Secondary Self-Illumination Activation Level"].default_value = 0
    if not FunctionEnum.one.value == shader_data["secondary animation function"]:
        shader_environment_node.inputs["Secondary Self-Illumination Activation Level"].default_value = 1

    shader_environment_node.inputs["Plasma On Color"].default_value = convert_to_blender_color(shader_data["plasma on color"], True)
    shader_environment_node.inputs["Plasma Off Color"].default_value = convert_to_blender_color(shader_data["plasma off color"], True)
    shader_environment_node.inputs["Plasma Self-Illumination Activation Level"].default_value = 0
    if not FunctionEnum.one.value == shader_data["plasma animation function"]:
        shader_environment_node.inputs["Plasma Self-Illumination Activation Level"].default_value = 1

    shader_environment_node.inputs["Brightness"].default_value = shader_data["brightness"]
    shader_environment_node.inputs["Perpendicular Color"].default_value = convert_to_blender_color(shader_data["perpendicular color"], True)
    shader_environment_node.inputs["Parallel Color"].default_value = convert_to_blender_color(shader_data["parallel color"], True)

    shader_environment_node.inputs["Perpendicular Brightness"].default_value = shader_data["perpendicular brightness"]
    shader_environment_node.inputs["Parallel Brightness"].default_value = shader_data["parallel brightness"]