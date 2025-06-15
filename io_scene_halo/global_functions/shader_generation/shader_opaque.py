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

from mathutils import Vector
from .shader_helper import (
    get_h2_bitmap, 
    get_output_material_node, 
    connect_inputs, 
    generate_image_node,
    get_shader_node,
    set_image_scale,
    generate_parameters
    )

def get_lightmap_factor(lightmap_type):
    lightmap_factor = 0
    if lightmap_type == 1:
        lightmap_factor = 0.5

    elif lightmap_type == 2:
        lightmap_factor = 0.25

    elif lightmap_type == 3:
        lightmap_factor = 1.0

    return lightmap_factor

def generate_shader_bloom(mat, shader, shader_template, report):
    mat.use_nodes = True

    parameter_keys = ["lightmap_emissive_map", "lightmap_emissive_color", "lightmap_emissive_power"]
    parameters = generate_parameters(shader, shader_template, parameter_keys)

    lightmap_emissive_parameter = None
    lightmap_emissive_color_parameter = None
    lightmap_emissive_power_parameter = None
    for parameter in parameters:
        if parameter.name == "lightmap_emissive_map":
            lightmap_emissive_parameter = parameter
        elif parameter.name == "lightmap_emissive_color":
            lightmap_emissive_color_parameter = parameter
        elif parameter.name == "lightmap_emissive_power":
            lightmap_emissive_power_parameter = parameter

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_data_path
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))

    shader_node = get_shader_node(mat.node_tree, "bloom")
    shader_node.location = Vector((-450.0, -20.0))
    shader_node.name = "Bloom"
    shader_node.width = 400.0
    shader_node.height = 100.0

    connect_inputs(mat.node_tree, shader_node, "Shader", output_material_node, "Surface")

    if not lightmap_emissive_parameter == None:
        lightmap_emissive_map, lightmap_emissive_map_name, lightmap_emissive_bitmap = get_h2_bitmap(lightmap_emissive_parameter.bitmap, texture_root, report)
        lightmap_emissive_node = generate_image_node(mat, lightmap_emissive_map, lightmap_emissive_bitmap, lightmap_emissive_map_name)
        lightmap_emissive_node.name = "Lightmap Emissive Map"
        lightmap_emissive_node.location = Vector((-900, 525))
        if not lightmap_emissive_node.image == None:
            lightmap_emissive_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, lightmap_emissive_node, "Color", shader_node, "Lightmap Emissive Map")
        shader_node.inputs["Lightmap Emissive Color"].default_value = lightmap_emissive_color_parameter.color
        shader_node.inputs["Lightmap Emissive Power"].default_value = lightmap_emissive_power_parameter.value * 100

def generate_shader_illum(mat, shader, shader_template, report):
    mat.use_nodes = True

    parameter_keys = ["lightmap_emissive_map", "lightmap_emissive_color", "lightmap_emissive_power", "self_illum_map", "self_illum_color"]
    parameters = generate_parameters(shader, shader_template, parameter_keys)

    lightmap_emissive_parameter = None
    lightmap_emissive_color_parameter = None
    lightmap_emissive_power_parameter = None
    self_illum_parameter = None
    self_illum_color_parameter = None
    for parameter in parameters:
        if parameter.name == "lightmap_emissive_map":
            lightmap_emissive_parameter = parameter
        elif parameter.name == "lightmap_emissive_color":
            lightmap_emissive_color_parameter = parameter
        elif parameter.name == "lightmap_emissive_power":
            lightmap_emissive_power_parameter = parameter
        elif parameter.name == "self_illum_map":
            self_illum_parameter = parameter
        elif parameter.name == "self_illum_color":
            self_illum_color_parameter = parameter

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_data_path
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))

    shader_node = get_shader_node(mat.node_tree, "illum")
    shader_node.location = Vector((-450.0, -20.0))
    shader_node.name = "Illum"
    shader_node.width = 400.0
    shader_node.height = 100.0

    connect_inputs(mat.node_tree, shader_node, "Shader", output_material_node, "Surface")
    if not lightmap_emissive_parameter == None:
        lightmap_emissive_map, lightmap_emissive_map_name, lightmap_emissive_bitmap = get_h2_bitmap(lightmap_emissive_parameter.bitmap, texture_root, report)
        lightmap_emissive_node = generate_image_node(mat, lightmap_emissive_map, lightmap_emissive_bitmap, lightmap_emissive_map_name)
        lightmap_emissive_node.name = "Lightmap Emissive Map"
        lightmap_emissive_node.location = Vector((-900, 525))
        if not lightmap_emissive_node.image == None:
            lightmap_emissive_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, lightmap_emissive_node, "Color", shader_node, "Lightmap Emissive Map")
        shader_node.inputs["Lightmap Emissive Color"].default_value = lightmap_emissive_color_parameter.color
        shader_node.inputs["Lightmap Emissive Power"].default_value = lightmap_emissive_power_parameter.value * 100

    if not self_illum_parameter == None:
        self_illum_map, self_illum_map_name, self_illum_bitmap = get_h2_bitmap(self_illum_parameter.bitmap, texture_root, report)
        self_illum_node = generate_image_node(mat, self_illum_map, self_illum_bitmap, self_illum_map_name)
        self_illum_node.name = "Self Illum Map"
        self_illum_node.location = Vector((-900, 525))
        if not self_illum_node.image == None:
            self_illum_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, self_illum_node, "Color", shader_node, "Self Illum Map")
        if not self_illum_color_parameter == None:
            shader_node.inputs["Self Illum Color"].default_value = self_illum_color_parameter.color

def generate_shader_tex_bump(mat, shader, shader_template, report):
    mat.use_nodes = True

    parameter_keys = ["bump_map", "lightmap_alphatest_map", "base_map", "detail_map", "specular_color", "specular_glancing_color"]
    parameters = generate_parameters(shader, shader_template, parameter_keys)

    bump_parameter = None
    alpha_parameter = None
    base_parameter = None
    detail_parameter = None
    specular_parameter = None
    specular_glancing_parameter = None
    for parameter in parameters:
        if parameter.name == "bump_map":
            bump_parameter = parameter
        elif parameter.name == "lightmap_alphatest_map":
            alpha_parameter = parameter
        elif parameter.name == "base_map":
            base_parameter = parameter
        elif parameter.name == "detail_map":
            detail_parameter = parameter
        elif parameter.name == "specular_color":
            specular_parameter = parameter
        elif parameter.name == "specular_glancing_color":
            specular_glancing_parameter = parameter

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_data_path
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))

    tex_bump_node = get_shader_node(mat.node_tree, "tex_bump")
    tex_bump_node.location = Vector((-450.0, -20.0))
    tex_bump_node.name = "Tex Bump"
    tex_bump_node.width = 400.0
    tex_bump_node.height = 100.0

    connect_inputs(mat.node_tree, tex_bump_node, "Shader", output_material_node, "Surface")

    tex_bump_node.inputs["Lightmap Factor"].default_value = get_lightmap_factor(shader.lightmap_type)

    if not bump_parameter == None:
        bump_map, bump_map_name, bump_bitmap = get_h2_bitmap(bump_parameter.bitmap, texture_root, report)
        bump_node = generate_image_node(mat, bump_map, bump_bitmap, bump_map_name)
        bump_node.name = "Bump Map"
        bump_node.location = Vector((-900, 525))
        bump_node.interpolation = 'Cubic'
        if not bump_node.image == None:
            bump_node.image.colorspace_settings.name = 'Non-Color'
            bump_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, bump_node, "Color", tex_bump_node, "Bump Map")
        set_image_scale(mat, bump_node, bump_parameter.scale)
        if bump_bitmap:
            height_value = 0.0
            if not bump_bitmap.bump_height == 0.0:
                height_value = bump_bitmap.bump_height

            tex_bump_node.inputs["Bump Map Repeat"].default_value = height_value

    if not alpha_parameter == None:
        alpha_map, alpha_map_name, alpha_bitmap = get_h2_bitmap(alpha_parameter.bitmap, texture_root, report)
        alpha_node = generate_image_node(mat, alpha_map, alpha_bitmap, alpha_map_name)
        alpha_node.name = "Bump Map"
        alpha_node.location = Vector((-900, 225))
        if not alpha_node.image == None:
            alpha_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, alpha_node, "Alpha", tex_bump_node, "Lightmap Alphatest Map")

    if not base_parameter == None:
        base_map, base_map_name, base_bitmap = get_h2_bitmap(base_parameter.bitmap, texture_root, report)
        base_node = generate_image_node(mat, base_map, base_bitmap, base_map_name)
        base_node.name = "Base Map"
        base_node.location = Vector((-900, -75))
        if not base_node.image == None:
            base_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, base_node, "Color", tex_bump_node, "Base Map")
        connect_inputs(mat.node_tree, base_node, "Alpha", tex_bump_node, "Base Map Alpha")
        set_image_scale(mat, base_node, base_parameter.scale)

    if not detail_parameter == None:
        detail_map, detail_map_name, detail_bitmap = get_h2_bitmap(detail_parameter.bitmap, texture_root, report)
        detail_node = generate_image_node(mat, detail_map, detail_bitmap, detail_map_name)
        detail_node.name = "Detail Map"
        detail_node.location = Vector((-900, -375))
        if not detail_node.image == None:
            detail_node.image.colorspace_settings.name = 'Non-Color'
            detail_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, detail_node, "Color", tex_bump_node, "Detail Map")
        set_image_scale(mat, detail_node, detail_parameter.scale)

    if not specular_parameter == None:
        tex_bump_node.inputs["Specular Color"].default_value = specular_parameter.color
    if not specular_glancing_parameter == None:
        tex_bump_node.inputs["Specular Glancing Color"].default_value = specular_glancing_parameter.color

def generate_shader_tex_bump_illum(mat, shader, shader_template, report):
    mat.use_nodes = True

    parameter_keys = ["bump_map", "base_map", "detail_map", "self_illum_map", "self_illum_color", "emissive_power", "emissive_color", "specular_color", "specular_glancing_color"]
    parameters = generate_parameters(shader, shader_template, parameter_keys)

    bump_parameter = None
    base_parameter = None
    detail_parameter = None
    self_illum_parameter = None
    self_illum_color_parameter = None
    emissive_color_parameter = None
    emissive_power_parameter = None
    specular_parameter = None
    specular_glancing_parameter = None
    for parameter in parameters:
        if parameter.name == "bump_map":
            bump_parameter = parameter
        elif parameter.name == "base_map":
            base_parameter = parameter
        elif parameter.name == "detail_map":
            detail_parameter = parameter
        elif parameter.name == "self_illum_map":
            self_illum_parameter = parameter
        elif parameter.name == "self_illum_color":
            self_illum_color_parameter = parameter
        elif parameter.name == "emissive_color":
            emissive_color_parameter = parameter
        elif parameter.name == "emissive_power":
            emissive_power_parameter = parameter
        elif parameter.name == "specular_color":
            specular_parameter = parameter
        elif parameter.name == "specular_glancing_color":
            specular_glancing_parameter = parameter

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_data_path
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))

    tex_bump_illum_node = get_shader_node(mat.node_tree, "tex_bump_illum")
    tex_bump_illum_node.location = Vector((-450.0, -20.0))
    tex_bump_illum_node.name = "Tex Bump Illum"
    tex_bump_illum_node.width = 400.0
    tex_bump_illum_node.height = 100.0

    connect_inputs(mat.node_tree, tex_bump_illum_node, "Shader", output_material_node, "Surface")

    tex_bump_illum_node.inputs["Lightmap Factor"].default_value = get_lightmap_factor(shader.lightmap_type)

    if not bump_parameter == None:
        bump_map, bump_map_name, bump_bitmap = get_h2_bitmap(bump_parameter.bitmap, texture_root, report)
        bump_node = generate_image_node(mat, bump_map, bump_bitmap, bump_map_name)
        bump_node.name = "Bump Map"
        bump_node.location = Vector((-900, 525))
        bump_node.interpolation = 'Cubic'
        if not bump_node.image == None:
            bump_node.image.colorspace_settings.name = 'Non-Color'
            bump_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, bump_node, "Color", tex_bump_illum_node, "Bump Map")
        set_image_scale(mat, bump_node, bump_parameter.scale)
        if bump_bitmap:
            height_value = 0.0
            if not bump_bitmap.bump_height == 0.0:
                height_value = bump_bitmap.bump_height

            tex_bump_illum_node.inputs["Bump Map Repeat"].default_value = height_value

    if not base_parameter == None:
        base_map, base_map_name, base_bitmap = get_h2_bitmap(base_parameter.bitmap, texture_root, report)
        base_node = generate_image_node(mat, base_map, base_bitmap, base_map_name)
        base_node.name = "Base Map"
        base_node.location = Vector((-900, -75))
        if not base_node.image == None:
            base_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, base_node, "Color", tex_bump_illum_node, "Base Map")
        connect_inputs(mat.node_tree, base_node, "Alpha", tex_bump_illum_node, "Base Map Alpha")
        set_image_scale(mat, base_node, base_parameter.scale)

    if not self_illum_parameter == None:
        self_illum_map, self_illum_map_name, self_illum_bitmap = get_h2_bitmap(self_illum_parameter.bitmap, texture_root, report)
        self_illum_node = generate_image_node(mat, self_illum_map, self_illum_bitmap, self_illum_map_name)
        self_illum_node.name = "Self Illum Map"
        self_illum_node.location = Vector((-900, -75))
        if not self_illum_node.image == None:
            self_illum_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, self_illum_node, "Color", tex_bump_illum_node, "Self Illum Map")
        set_image_scale(mat, self_illum_node, self_illum_parameter.scale)

    if not self_illum_color_parameter == None:
        tex_bump_illum_node.inputs["Self Illum Color"].default_value = self_illum_color_parameter.color

    if not emissive_color_parameter == None:
        tex_bump_illum_node.inputs["Emissive Color"].default_value = emissive_color_parameter.color

    if not emissive_power_parameter == None:
        tex_bump_illum_node.inputs["Emissive Power"].default_value = emissive_power_parameter.value * 100

    if not detail_parameter == None:
        detail_map, detail_map_name, detail_bitmap = get_h2_bitmap(detail_parameter.bitmap, texture_root, report)
        detail_node = generate_image_node(mat, detail_map, detail_bitmap, detail_map_name)
        detail_node.name = "Detail Map"
        detail_node.location = Vector((-900, -375))
        if not detail_node.image == None:
            detail_node.image.colorspace_settings.name = 'Non-Color'
            detail_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, detail_node, "Color", tex_bump_illum_node, "Detail Map")
        set_image_scale(mat, detail_node, detail_parameter.scale)

    if not specular_parameter == None:
        tex_bump_illum_node.inputs["Specular Color"].default_value = specular_parameter.color
    if not specular_glancing_parameter == None:
        tex_bump_illum_node.inputs["Specular Glancing Color"].default_value = specular_glancing_parameter.color

def generate_shader_tex_bump_plasma_one_channel_illum(mat, shader, shader_template, report):
    mat.use_nodes = True

    parameter_keys = ["bump_map", "base_map", "detail_map", "multichannel_map", "channel_A_color", "channel_B_color", "channel_C_color", "time", "emissive_power", "emissive_color", "specular_color", "specular_glancing_color"]
    parameters = generate_parameters(shader, shader_template, parameter_keys)

    bump_parameter = None
    base_parameter = None
    detail_parameter = None
    multichannel_parameter = None
    channel_A_color_parameter = None
    channel_B_color_parameter = None
    channel_C_color_parameter = None
    time_parameter = None
    emissive_color_parameter = None
    emissive_power_parameter = None
    specular_parameter = None
    specular_glancing_parameter = None

    for parameter in parameters:
        if parameter.name == "bump_map":
            bump_parameter = parameter
        elif parameter.name == "base_map":
            base_parameter = parameter
        elif parameter.name == "detail_map":
            detail_parameter = parameter
        elif parameter.name == "multichannel_map":
            multichannel_parameter = parameter
        elif parameter.name == "channel_A_color":
            channel_A_color_parameter = parameter
        elif parameter.name == "channel_B_color":
            channel_B_color_parameter = parameter
        elif parameter.name == "channel_C_color":
            channel_C_color_parameter = parameter
        elif parameter.name == "time":
            time_parameter = parameter
        elif parameter.name == "emissive_color":
            emissive_color_parameter = parameter
        elif parameter.name == "emissive_power":
            emissive_power_parameter = parameter
        elif parameter.name == "specular_color":
            specular_parameter = parameter
        elif parameter.name == "specular_glancing_color":
            specular_glancing_parameter = parameter

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_data_path
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))

    tex_bump_illum_node = get_shader_node(mat.node_tree, "tex_bump_plasma_one_channel_illum")
    tex_bump_illum_node.location = Vector((-450.0, -20.0))
    tex_bump_illum_node.name = "Tex Bump Plasma One Channel Illum"
    tex_bump_illum_node.width = 400.0
    tex_bump_illum_node.height = 100.0

    connect_inputs(mat.node_tree, tex_bump_illum_node, "Shader", output_material_node, "Surface")

    tex_bump_illum_node.inputs["Lightmap Factor"].default_value = get_lightmap_factor(shader.lightmap_type)

    if not bump_parameter == None:
        bump_map, bump_map_name, bump_bitmap = get_h2_bitmap(bump_parameter.bitmap, texture_root, report)
        bump_node = generate_image_node(mat, bump_map, bump_bitmap, bump_map_name)
        bump_node.name = "Bump Map"
        bump_node.location = Vector((-900, 525))
        bump_node.interpolation = 'Cubic'
        if not bump_node.image == None:
            bump_node.image.colorspace_settings.name = 'Non-Color'
            bump_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, bump_node, "Color", tex_bump_illum_node, "Bump Map")
        set_image_scale(mat, bump_node, bump_parameter.scale)
        if bump_bitmap:
            height_value = 0.0
            if not bump_bitmap.bump_height == 0.0:
                height_value = bump_bitmap.bump_height

            tex_bump_illum_node.inputs["Bump Map Repeat"].default_value = height_value

    if not base_parameter == None:
        base_map, base_map_name, base_bitmap = get_h2_bitmap(base_parameter.bitmap, texture_root, report)
        base_node = generate_image_node(mat, base_map, base_bitmap, base_map_name)
        base_node.name = "Base Map"
        base_node.location = Vector((-900, -75))
        if not base_node.image == None:
            base_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, base_node, "Color", tex_bump_illum_node, "Base Map")
        connect_inputs(mat.node_tree, base_node, "Alpha", tex_bump_illum_node, "Base Map Alpha")
        set_image_scale(mat, base_node, base_parameter.scale)

    if not multichannel_parameter == None:
        multi_map, multi_map_name, multi_bitmap = get_h2_bitmap(multichannel_parameter.bitmap, texture_root, report)
        multi_node = generate_image_node(mat, multi_map, multi_bitmap, multi_map_name)
        multi_node.name = "Multichannel Map"
        multi_node.location = Vector((-900, -225))
        if not multi_node.image == None:
            multi_node.image.colorspace_settings.name = 'Non-Color'
            multi_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, multi_node, "Color", tex_bump_illum_node, "Multichannel Map")
        set_image_scale(mat, multi_node, multichannel_parameter.scale)

    if not channel_A_color_parameter == None:
        tex_bump_illum_node.inputs["Channel A Color"].default_value = channel_A_color_parameter.color
    if not channel_B_color_parameter == None:
        tex_bump_illum_node.inputs["Channel B Color"].default_value = channel_B_color_parameter.color
    if not channel_C_color_parameter == None:
        tex_bump_illum_node.inputs["Channel C Color"].default_value = channel_C_color_parameter.color

    if not time_parameter == None:
        tex_bump_illum_node.inputs["Time"].default_value = time_parameter.value

    if not emissive_color_parameter == None:
        tex_bump_illum_node.inputs["Emissive Color"].default_value = emissive_color_parameter.color

    if not emissive_power_parameter == None:
        tex_bump_illum_node.inputs["Emissive Power"].default_value = emissive_power_parameter.value * 100

    if not detail_parameter == None:
        detail_map, detail_map_name, detail_bitmap = get_h2_bitmap(detail_parameter.bitmap, texture_root, report)
        detail_node = generate_image_node(mat, detail_map, detail_bitmap, detail_map_name)
        detail_node.name = "Detail Map"
        detail_node.location = Vector((-900, -375))
        if not detail_node.image == None:
            detail_node.image.colorspace_settings.name = 'Non-Color'
            detail_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, detail_node, "Color", tex_bump_illum_node, "Detail Map")
        set_image_scale(mat, detail_node, detail_parameter.scale)

    if not specular_parameter == None:
        tex_bump_illum_node.inputs["Specular Color"].default_value = specular_parameter.color
    if not specular_glancing_parameter == None:
        tex_bump_illum_node.inputs["Specular Glancing Color"].default_value = specular_glancing_parameter.color

def generate_shader_tex_bump_illum_3_channel(mat, shader, shader_template, report):
    mat.use_nodes = True

    parameter_keys = ["bump_map", "base_map", "detail_map", "self_illum_map","channel_a_color", "channel_b_color", "channel_c_color","channel_a_brightness", "channel_b_brightness", "channel_c_brightness","emissive_power", "emissive_color","specular_color", "specular_glancing_color"]
    parameters = generate_parameters(shader, shader_template, parameter_keys)

    bump_parameter = None
    base_parameter = None
    detail_parameter = None
    self_illum_parameter = None
    channel_a_color_parameter = None
    channel_b_color_parameter = None
    channel_c_color_parameter = None
    channel_a_brightness_parameter = None
    channel_b_brightness_parameter = None
    channel_c_brightness_parameter = None
    emissive_color_parameter = None
    emissive_power_parameter = None
    specular_parameter = None
    specular_glancing_parameter = None

    for parameter in parameters:
        if parameter.name == "bump_map":
            bump_parameter = parameter
        elif parameter.name == "base_map":
            base_parameter = parameter
        elif parameter.name == "detail_map":
            detail_parameter = parameter
        elif parameter.name == "self_illum_map":
            self_illum_parameter = parameter
        elif parameter.name == "channel_a_color":
            channel_a_color_parameter = parameter
        elif parameter.name == "channel_b_color":
            channel_b_color_parameter = parameter
        elif parameter.name == "channel_c_color":
            channel_c_color_parameter = parameter
        elif parameter.name == "channel_a_brightness":
            channel_a_brightness_parameter = parameter
        elif parameter.name == "channel_b_brightness":
            channel_b_brightness_parameter = parameter
        elif parameter.name == "channel_c_brightness":
            channel_c_brightness_parameter = parameter
        elif parameter.name == "emissive_color":
            emissive_color_parameter = parameter
        elif parameter.name == "emissive_power":
            emissive_power_parameter = parameter
        elif parameter.name == "specular_color":
            specular_parameter = parameter
        elif parameter.name == "specular_glancing_color":
            specular_glancing_parameter = parameter

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_data_path
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))

    tex_bump_illum_node = get_shader_node(mat.node_tree, "tex_bump_illum_3_channel")
    tex_bump_illum_node.location = Vector((-450.0, -20.0))
    tex_bump_illum_node.name = "Tex Bump Illum 3 Channel"
    tex_bump_illum_node.width = 400.0
    tex_bump_illum_node.height = 100.0

    connect_inputs(mat.node_tree, tex_bump_illum_node, "Shader", output_material_node, "Surface")

    tex_bump_illum_node.inputs["Lightmap Factor"].default_value = get_lightmap_factor(shader.lightmap_type)

    if not bump_parameter == None:
        bump_map, bump_map_name, bump_bitmap = get_h2_bitmap(bump_parameter.bitmap, texture_root, report)
        bump_node = generate_image_node(mat, bump_map, bump_bitmap, bump_map_name)
        bump_node.name = "Bump Map"
        bump_node.location = Vector((-900, 525))
        bump_node.interpolation = 'Cubic'
        if not bump_node.image == None:
            bump_node.image.colorspace_settings.name = 'Non-Color'
            bump_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, bump_node, "Color", tex_bump_illum_node, "Bump Map")
        set_image_scale(mat, bump_node, bump_parameter.scale)
        if bump_bitmap:
            height_value = 0.0
            if not bump_bitmap.bump_height == 0.0:
                height_value = bump_bitmap.bump_height

            tex_bump_illum_node.inputs["Bump Map Repeat"].default_value = height_value

    if not base_parameter == None:
        base_map, base_map_name, base_bitmap = get_h2_bitmap(base_parameter.bitmap, texture_root, report)
        base_node = generate_image_node(mat, base_map, base_bitmap, base_map_name)
        base_node.name = "Base Map"
        base_node.location = Vector((-900, -75))
        if not base_node.image == None:
            base_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, base_node, "Color", tex_bump_illum_node, "Base Map")
        connect_inputs(mat.node_tree, base_node, "Alpha", tex_bump_illum_node, "Base Map Alpha")
        set_image_scale(mat, base_node, base_parameter.scale)

    if not self_illum_parameter == None:
        self_illum_map, self_illum_map_name, self_illum_bitmap = get_h2_bitmap(self_illum_parameter.bitmap, texture_root, report)
        self_illum_node = generate_image_node(mat, self_illum_map, self_illum_bitmap, self_illum_map_name)
        self_illum_node.name = "Self Illum Map"
        self_illum_node.location = Vector((-900, -75))
        if not self_illum_node.image == None:
            self_illum_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, self_illum_node, "Color", tex_bump_illum_node, "Self Illum Map")
        set_image_scale(mat, self_illum_node, self_illum_parameter.scale)

    if not channel_a_color_parameter == None:
        tex_bump_illum_node.inputs["Channel A Color"].default_value = channel_a_color_parameter.color
    if not channel_b_color_parameter == None:
        tex_bump_illum_node.inputs["Channel B Color"].default_value = channel_b_color_parameter.color
    if not channel_c_color_parameter == None:
        tex_bump_illum_node.inputs["Channel C Color"].default_value = channel_c_color_parameter.color

    if not channel_a_brightness_parameter == None:
        tex_bump_illum_node.inputs["Channel A Brightness"].default_value = channel_a_brightness_parameter.value
    if not channel_b_brightness_parameter == None:
        tex_bump_illum_node.inputs["Channel B Brightness"].default_value = channel_b_brightness_parameter.value
    if not channel_c_brightness_parameter == None:
        tex_bump_illum_node.inputs["Channel C Brightness"].default_value = channel_c_brightness_parameter.value

    if not emissive_color_parameter == None:
        tex_bump_illum_node.inputs["Emissive Color"].default_value = emissive_color_parameter.color

    if not emissive_power_parameter == None:
        tex_bump_illum_node.inputs["Emissive Power"].default_value = emissive_power_parameter.value * 100

    if not detail_parameter == None:
        detail_map, detail_map_name, detail_bitmap = get_h2_bitmap(detail_parameter.bitmap, texture_root, report)
        detail_node = generate_image_node(mat, detail_map, detail_bitmap, detail_map_name)
        detail_node.name = "Detail Map"
        detail_node.location = Vector((-900, -375))
        if not detail_node.image == None:
            detail_node.image.colorspace_settings.name = 'Non-Color'
            detail_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, detail_node, "Color", tex_bump_illum_node, "Detail Map")
        set_image_scale(mat, detail_node, detail_parameter.scale)

    if not specular_parameter == None:
        tex_bump_illum_node.inputs["Specular Color"].default_value = specular_parameter.color
    if not specular_glancing_parameter == None:
        tex_bump_illum_node.inputs["Specular Glancing Color"].default_value = specular_glancing_parameter.color


def generate_shader_tex_bump_detail_blend(mat, shader, shader_template, report):
    mat.use_nodes = True

    parameter_keys = ["bump_map", "base_map", "detail_map", "secondary_detail_map", "specular_color", "specular_glancing_color"]
    parameters = generate_parameters(shader, shader_template, parameter_keys)

    bump_parameter = None
    base_parameter = None
    detail_parameter = None
    secondary_detail_parameter = None
    specular_parameter = None
    specular_glancing_parameter = None
    for parameter in parameters:
        if parameter.name == "bump_map":
            bump_parameter = parameter
        elif parameter.name == "base_map":
            base_parameter = parameter
        elif parameter.name == "detail_map":
            detail_parameter = parameter
        elif parameter.name == "secondary_detail_map":
            secondary_detail_parameter = parameter
        elif parameter.name == "specular_color":
            specular_parameter = parameter
        elif parameter.name == "specular_glancing_color":
            specular_glancing_parameter = parameter

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_data_path
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))

    tex_bump_node = get_shader_node(mat.node_tree, "tex_bump_detail_blend")
    tex_bump_node.location = Vector((-450.0, -20.0))
    tex_bump_node.name = "Tex Bump Detail Blend"
    tex_bump_node.width = 400.0
    tex_bump_node.height = 100.0

    connect_inputs(mat.node_tree, tex_bump_node, "Shader", output_material_node, "Surface")

    tex_bump_node.inputs["Lightmap Factor"].default_value = get_lightmap_factor(shader.lightmap_type)

    if not bump_parameter == None:
        bump_map, bump_map_name, bump_bitmap = get_h2_bitmap(bump_parameter.bitmap, texture_root, report)
        bump_node = generate_image_node(mat, bump_map, bump_bitmap, bump_map_name)
        bump_node.name = "Bump Map"
        bump_node.location = Vector((-900, 525))
        bump_node.interpolation = 'Cubic'
        if not bump_node.image == None:
            bump_node.image.colorspace_settings.name = 'Non-Color'
            bump_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, bump_node, "Color", tex_bump_node, "Bump Map")
        set_image_scale(mat, bump_node, bump_parameter.scale)
        if bump_bitmap:
            height_value = 0.0
            if not bump_bitmap.bump_height == 0.0:
                height_value = bump_bitmap.bump_height

            tex_bump_node.inputs["Bump Map Repeat"].default_value = height_value

    if not base_parameter == None:
        base_map, base_map_name, base_bitmap = get_h2_bitmap(base_parameter.bitmap, texture_root, report)
        base_node = generate_image_node(mat, base_map, base_bitmap, base_map_name)
        base_node.name = "Base Map"
        base_node.location = Vector((-900, -75))
        if not base_node.image == None:
            base_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, base_node, "Color", tex_bump_node, "Base Map")
        connect_inputs(mat.node_tree, base_node, "Alpha", tex_bump_node, "Base Map Alpha")
        set_image_scale(mat, base_node, base_parameter.scale)

    if not detail_parameter == None:
        detail_map, detail_map_name, detail_bitmap = get_h2_bitmap(detail_parameter.bitmap, texture_root, report)
        detail_node = generate_image_node(mat, detail_map, detail_bitmap, detail_map_name)
        detail_node.name = "Detail Map"
        detail_node.location = Vector((-900, -375))
        if not detail_node.image == None:
            detail_node.image.colorspace_settings.name = 'Non-Color'
            detail_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, detail_node, "Color", tex_bump_node, "Detail Map")
        set_image_scale(mat, detail_node, detail_parameter.scale)

    if not secondary_detail_parameter == None:
        detail_map, detail_map_name, detail_bitmap = get_h2_bitmap(secondary_detail_parameter.bitmap, texture_root, report)
        detail_node = generate_image_node(mat, detail_map, detail_bitmap, detail_map_name)
        detail_node.name = "Secondary Detail Map"
        detail_node.location = Vector((-900, -375))
        if not detail_node.image == None:
            detail_node.image.colorspace_settings.name = 'Non-Color'
            detail_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, detail_node, "Color", tex_bump_node, "Secondary Detail Map")
        set_image_scale(mat, detail_node, secondary_detail_parameter.scale)

    if not specular_parameter == None:
        tex_bump_node.inputs["Specular Color"].default_value = specular_parameter.color
    if not specular_glancing_parameter == None:
        tex_bump_node.inputs["Specular Glancing Color"].default_value = specular_glancing_parameter.color

def generate_shader_tex_bump_detail_blend_detail(mat, shader, shader_template, report):
    mat.use_nodes = True

    parameter_keys = ["bump_map", "base_map", "blend_detail_map_1", "blend_detail_map_2", "overlay_detail_map", "specular_color", "specular_glancing_color"]
    parameters = generate_parameters(shader, shader_template, parameter_keys)

    bump_parameter = None
    base_parameter = None
    blend_detail_map_1_parameter = None
    blend_detail_map_2_parameter = None
    overlay_detail_map_parameter = None
    specular_parameter = None
    specular_glancing_parameter = None
    for parameter in parameters:
        if parameter.name == "bump_map":
            bump_parameter = parameter
        elif parameter.name == "base_map":
            base_parameter = parameter
        elif parameter.name == "blend_detail_map_1":
            blend_detail_map_1_parameter = parameter
        elif parameter.name == "blend_detail_map_2":
            blend_detail_map_2_parameter = parameter
        elif parameter.name == "overlay_detail_map":
            overlay_detail_map_parameter = parameter
        elif parameter.name == "specular_color":
            specular_parameter = parameter
        elif parameter.name == "specular_glancing_color":
            specular_glancing_parameter = parameter

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_data_path
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))

    tex_bump_node = get_shader_node(mat.node_tree, "tex_bump_detail_blend_detail")
    tex_bump_node.location = Vector((-450.0, -20.0))
    tex_bump_node.name = "Tex Bump Detail Blend Detail"
    tex_bump_node.width = 400.0
    tex_bump_node.height = 100.0

    connect_inputs(mat.node_tree, tex_bump_node, "Shader", output_material_node, "Surface")

    tex_bump_node.inputs["Lightmap Factor"].default_value = get_lightmap_factor(shader.lightmap_type)

    if not bump_parameter == None:
        bump_map, bump_map_name, bump_bitmap = get_h2_bitmap(bump_parameter.bitmap, texture_root, report)
        bump_node = generate_image_node(mat, bump_map, bump_bitmap, bump_map_name)
        bump_node.name = "Bump Map"
        bump_node.location = Vector((-900, 525))
        bump_node.interpolation = 'Cubic'
        if not bump_node.image == None:
            bump_node.image.colorspace_settings.name = 'Non-Color'
            bump_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, bump_node, "Color", tex_bump_node, "Bump Map")
        set_image_scale(mat, bump_node, bump_parameter.scale)
        if bump_bitmap:
            height_value = 0.0
            if not bump_bitmap.bump_height == 0.0:
                height_value = bump_bitmap.bump_height

            tex_bump_node.inputs["Bump Map Repeat"].default_value = height_value

    if not base_parameter == None:
        base_map, base_map_name, base_bitmap = get_h2_bitmap(base_parameter.bitmap, texture_root, report)
        base_node = generate_image_node(mat, base_map, base_bitmap, base_map_name)
        base_node.name = "Base Map"
        base_node.location = Vector((-900, -75))
        if not base_node.image == None:
            base_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, base_node, "Color", tex_bump_node, "Base Map")
        connect_inputs(mat.node_tree, base_node, "Alpha", tex_bump_node, "Base Map Alpha")
        set_image_scale(mat, base_node, base_parameter.scale)

    if not blend_detail_map_1_parameter == None:
        detail_map, detail_map_name, detail_bitmap = get_h2_bitmap(blend_detail_map_1_parameter.bitmap, texture_root, report)
        detail_node = generate_image_node(mat, detail_map, detail_bitmap, detail_map_name)
        detail_node.name = "Detail Map 1"
        detail_node.location = Vector((-900, -375))
        if not detail_node.image == None:
            detail_node.image.colorspace_settings.name = 'Non-Color'
            detail_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, detail_node, "Color", tex_bump_node, "Detail Map 1")
        set_image_scale(mat, detail_node, blend_detail_map_1_parameter.scale)

    if not blend_detail_map_2_parameter == None:
        detail_map, detail_map_name, detail_bitmap = get_h2_bitmap(blend_detail_map_2_parameter.bitmap, texture_root, report)
        detail_node = generate_image_node(mat, detail_map, detail_bitmap, detail_map_name)
        detail_node.name = "Detail Map 1"
        detail_node.location = Vector((-900, -375))
        if not detail_node.image == None:
            detail_node.image.colorspace_settings.name = 'Non-Color'
            detail_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, detail_node, "Color", tex_bump_node, "Detail Map 2")
        set_image_scale(mat, detail_node, blend_detail_map_2_parameter.scale)

    if not overlay_detail_map_parameter == None:
        detail_map, detail_map_name, detail_bitmap = get_h2_bitmap(overlay_detail_map_parameter.bitmap, texture_root, report)
        detail_node = generate_image_node(mat, detail_map, detail_bitmap, detail_map_name)
        detail_node.name = "Overlay Detail Map"
        detail_node.location = Vector((-900, -375))
        if not detail_node.image == None:
            detail_node.image.colorspace_settings.name = 'Non-Color'
            detail_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, detail_node, "Color", tex_bump_node, "Overlay Detail Map")
        set_image_scale(mat, detail_node, overlay_detail_map_parameter.scale)

    if not specular_parameter == None:
        tex_bump_node.inputs["Specular Color"].default_value = specular_parameter.color
    if not specular_glancing_parameter == None:
        tex_bump_node.inputs["Specular Glancing Color"].default_value = specular_glancing_parameter.color

def generate_shader_tex_bump_alpha_test(mat, shader, shader_template, report):
    mat.use_nodes = True

    parameter_keys = ["bump_map", "alpha_test_map", "lightmap_alphatest_map", "lightmap_foliage_scale", "base_map", "detail_map", "specular_color", "specular_glancing_color"]
    parameters = generate_parameters(shader, shader_template, parameter_keys)

    bump_parameter = None
    alpha_test_parameter = None
    lightmap_alphatest_parameter = None
    lightmap_foliage_scale_parameter = None
    base_parameter = None
    detail_parameter = None
    specular_parameter = None
    specular_glancing_parameter = None
    for parameter in parameters:
        if parameter.name == "bump_map":
            bump_parameter = parameter
        elif parameter.name == "alpha_test_map":
            alpha_test_parameter = parameter
        elif parameter.name == "lightmap_alphatest_map":
            lightmap_alphatest_parameter = parameter
        elif parameter.name == "lightmap_foliage_scale":
            lightmap_foliage_scale_parameter = parameter
        elif parameter.name == "base_map":
            base_parameter = parameter
        elif parameter.name == "detail_map":
            detail_parameter = parameter
        elif parameter.name == "specular_color":
            specular_parameter = parameter
        elif parameter.name == "specular_glancing_color":
            specular_glancing_parameter = parameter

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_data_path
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))

    shader_node = get_shader_node(mat.node_tree, "tex_bump_alpha_test")
    shader_node.location = Vector((-450.0, -20.0))
    shader_node.name = "Tex Bump Alpha Test"
    shader_node.width = 400.0
    shader_node.height = 100.0

    connect_inputs(mat.node_tree, shader_node, "Shader", output_material_node, "Surface")

    shader_node.inputs["Lightmap Factor"].default_value = get_lightmap_factor(shader.lightmap_type)

    if not bump_parameter == None:
        bump_map, bump_map_name, bump_bitmap = get_h2_bitmap(bump_parameter.bitmap, texture_root, report)
        bump_node = generate_image_node(mat, bump_map, bump_bitmap, bump_map_name)
        bump_node.name = "Bump Map"
        bump_node.location = Vector((-900, 525))
        bump_node.interpolation = 'Cubic'
        if not bump_node.image == None:
            bump_node.image.colorspace_settings.name = 'Non-Color'
            bump_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, bump_node, "Color", shader_node, "Bump Map")
        connect_inputs(mat.node_tree, bump_node, "Alpha", shader_node, "Bump Map Alpha")
        set_image_scale(mat, bump_node, bump_parameter.scale)
        if bump_bitmap:
            height_value = 0.0
            if not bump_bitmap.bump_height == 0.0:
                height_value = bump_bitmap.bump_height

            shader_node.inputs["Bump Map Repeat"].default_value = height_value

    if not alpha_test_parameter == None:
        alpha_test_map, alpha_test_map_name, alpha_test_bitmap = get_h2_bitmap(alpha_test_parameter.bitmap, texture_root, report)
        alpha_test_node = generate_image_node(mat, alpha_test_map, alpha_test_bitmap, alpha_test_map_name)
        alpha_test_node.name = "Alpha Test Map"
        alpha_test_node.location = Vector((-900, 525))
        if not alpha_test_node.image == None:
            alpha_test_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, alpha_test_node, "Color", shader_node, "Alpha Test Map")
        connect_inputs(mat.node_tree, alpha_test_node, "Alpha", shader_node, "Alpha Test Map Alpha")
        set_image_scale(mat, alpha_test_node, alpha_test_parameter.scale)

    if not lightmap_alphatest_parameter == None:
        lightmap_alpha_test_map, lightmap_alpha_test_map_name, lightmap_alpha_test_bitmap = get_h2_bitmap(lightmap_alphatest_parameter.bitmap, texture_root, report)
        lightmap_alpha_test_node = generate_image_node(mat, lightmap_alpha_test_map, lightmap_alpha_test_bitmap, lightmap_alpha_test_map_name)
        lightmap_alpha_test_node.name = "Lightmap Alpha Test Map"
        lightmap_alpha_test_node.location = Vector((-900, 525))
        if not lightmap_alpha_test_node.image == None:
            lightmap_alpha_test_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, lightmap_alpha_test_node, "Color", shader_node, "Lightmap Alpha Test Map")
        connect_inputs(mat.node_tree, lightmap_alpha_test_node, "Alpha", shader_node, "Lightmap Alpha Test Map Alpha")

    if not lightmap_foliage_scale_parameter == None:
        shader_node.inputs["Lightmap Foliage Scale"].default_value = lightmap_foliage_scale_parameter.value

    if not base_parameter == None:
        base_map, base_map_name, base_bitmap = get_h2_bitmap(base_parameter.bitmap, texture_root, report)
        base_node = generate_image_node(mat, base_map, base_bitmap, base_map_name)
        base_node.name = "Base Map"
        base_node.location = Vector((-900, -75))
        if not base_node.image == None:
            base_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, base_node, "Color", shader_node, "Base Map")
        connect_inputs(mat.node_tree, base_node, "Alpha", shader_node, "Base Map Alpha")
        set_image_scale(mat, base_node, base_parameter.scale)

    if not detail_parameter == None:
        detail_map, detail_map_name, detail_bitmap = get_h2_bitmap(detail_parameter.bitmap, texture_root, report)
        detail_node = generate_image_node(mat, detail_map, detail_bitmap, detail_map_name)
        detail_node.name = "Detail Map"
        detail_node.location = Vector((-900, -375))
        if not detail_node.image == None:
            detail_node.image.colorspace_settings.name = 'Non-Color'
            detail_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, detail_node, "Color", shader_node, "Detail Map")
        set_image_scale(mat, detail_node, detail_parameter.scale)

    if not specular_parameter == None:
        shader_node.inputs["Specular Color"].default_value = specular_parameter.color
    if not specular_glancing_parameter == None:
        shader_node.inputs["Specular Glancing Color"].default_value = specular_glancing_parameter.color
