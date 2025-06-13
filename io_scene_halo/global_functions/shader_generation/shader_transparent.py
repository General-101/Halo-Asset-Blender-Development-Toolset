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

def generate_shader_plasma_alpha(mat, shader, shader_template, report):
    mat.use_nodes = True

    parameter_keys = ["noise_map_a", "noise_map_b", "color_wide", "color_medium", "color_sharp", "alpha_map", "perpendicular_brightness", "fade_bias", "emissive_color", "emissive_power"]
    parameters = generate_parameters(shader, shader_template, parameter_keys)

    noise_map_a_parameter = None
    noise_map_b_parameter = None
    color_wide_parameter = None
    color_medium_parameter = None
    color_sharp_parameter = None
    alpha_map_parameter = None
    perpendicular_brightness_parameter = None
    fade_bias_parameter = None
    emissive_color_parameter = None
    emissive_power_parameter = None
    for parameter in parameters:
        if parameter.name == "noise_map_a":
            noise_map_a_parameter = parameter
        elif parameter.name == "noise_map_b":
            noise_map_b_parameter = parameter
        elif parameter.name == "color_wide":
            color_wide_parameter = parameter
        elif parameter.name == "color_medium":
            color_medium_parameter = parameter
        elif parameter.name == "color_sharp":
            color_sharp_parameter = parameter
        elif parameter.name == "alpha_map":
            alpha_map_parameter = parameter
        elif parameter.name == "perpendicular_brightness":
            perpendicular_brightness_parameter = parameter
        elif parameter.name == "fade_bias":
            fade_bias_parameter = parameter
        elif parameter.name == "emissive_color":
            emissive_color_parameter = parameter
        elif parameter.name == "emissive_power":
            emissive_power_parameter = parameter

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_data_path
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))

    shader_node = get_shader_node(mat.node_tree, "plasma_alpha")
    shader_node.location = Vector((-450.0, -20.0))
    shader_node.name = "Plasma Alpha"
    shader_node.width = 400.0
    shader_node.height = 100.0

    connect_inputs(mat.node_tree, shader_node, "Shader", output_material_node, "Surface")

    if not noise_map_a_parameter == None:
        noise_map_a, noise_map_a_name, noise_map_a_bitmap = get_h2_bitmap(noise_map_a_parameter.bitmap, texture_root, report)
        noise_node_a = generate_image_node(mat, noise_map_a, noise_map_a_bitmap, noise_map_a_name)
        noise_node_a.name = "Noise Map A"
        noise_node_a.location = Vector((-900, 525))
        noise_node_a.interpolation = 'Smart'
        if not noise_node_a.image == None:
            noise_node_a.image.colorspace_settings.name = 'Linear Rec.709'
            noise_node_a.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, noise_node_a, "Color", shader_node, "Noise Map A")
        set_image_scale(mat, noise_node_a, noise_map_a_parameter.scale)

    if not noise_map_b_parameter == None:
        noise_map_b, noise_map_b_name, noise_map_b_bitmap = get_h2_bitmap(noise_map_b_parameter.bitmap, texture_root, report)
        noise_node_b = generate_image_node(mat, noise_map_b, noise_map_b_bitmap, noise_map_b_name)
        noise_node_b.name = "Noise Map B"
        noise_node_b.location = Vector((-900, 525))
        noise_node_b.interpolation = 'Smart'
        if not noise_node_b.image == None:
            noise_node_b.image.colorspace_settings.name = 'Linear Rec.709'
            noise_node_b.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, noise_node_b, "Color", shader_node, "Noise Map B")
        set_image_scale(mat, noise_node_b, noise_map_b_parameter.scale)

    if not alpha_map_parameter == None:
        alpha_map, alpha_map_name, alpha_map_bitmap = get_h2_bitmap(alpha_map_parameter.bitmap, texture_root, report)
        alpha_node = generate_image_node(mat, alpha_map, alpha_map_bitmap, alpha_map_name)
        alpha_node.name = "Alpha Map"
        alpha_node.location = Vector((-900, 525))
        if not alpha_node.image == None:
            alpha_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, alpha_node, "Alpha", shader_node, "Alpha Map")
        set_image_scale(mat, alpha_node, alpha_map_parameter.scale)

    if not color_wide_parameter == None:
        shader_node.inputs["Color Wide"].default_value = color_wide_parameter.color
    if not color_medium_parameter == None:
        shader_node.inputs["Color Medium"].default_value = color_medium_parameter.color
    if not color_sharp_parameter == None:
        shader_node.inputs["Color Sharp"].default_value = color_sharp_parameter.color

    if not perpendicular_brightness_parameter == None:
        shader_node.inputs["Perpendicular Brightness"].default_value = perpendicular_brightness_parameter.value
    if not fade_bias_parameter == None:
        shader_node.inputs["Fade Bias"].default_value = fade_bias_parameter.value

    if not emissive_color_parameter == None:
        shader_node.inputs["Emissive Color"].default_value = emissive_color_parameter.color
    if not emissive_power_parameter == None:
        shader_node.inputs["Emissive Power"].default_value = emissive_power_parameter.value * 100

def generate_shader_one_alpha_env(mat, shader, shader_template, report):
    mat.use_nodes = True

    parameter_keys = ["environment_map", 
                      "environment_color", 
                      "specular_map", 
                      "alpha_blend_map", 
                      "alpha_blend_color", 
                      "alpha_blend_opacity", 
                      "tint_color", 
                      "glancing_tint_color", 
                      "brightness", 
                      "glancing_brightness",
                      "lightmap_translucent_map",
                      "lightmap_translucent_color",
                      "lightmap_translucent_alpha"]
    parameters = generate_parameters(shader, shader_template, parameter_keys)

    environment_map_parameter = None
    environment_color_parameter = None
    specular_map_parameter = None
    alpha_blend_map_parameter = None
    alpha_blend_color_parameter = None
    alpha_blend_opacity_parameter = None
    tint_color_parameter = None
    glancing_tint_color_parameter = None
    brightness_parameter = None
    glancing_brightness_parameter = None
    lightmap_translucent_map_parameter = None
    lightmap_translucent_color_parameter = None
    lightmap_translucent_alpha_parameter = None
    for parameter in parameters:
        if parameter.name == "environment_map":
            environment_map_parameter = parameter
        elif parameter.name == "environment_color":
            environment_color_parameter = parameter
        elif parameter.name == "specular_map":
            specular_map_parameter = parameter
        elif parameter.name == "alpha_blend_map":
            alpha_blend_map_parameter = parameter
        elif parameter.name == "alpha_blend_color":
            alpha_blend_color_parameter = parameter
        elif parameter.name == "alpha_blend_opacity":
            alpha_blend_opacity_parameter = parameter
        elif parameter.name == "tint_color":
            tint_color_parameter = parameter
        elif parameter.name == "glancing_tint_color":
            glancing_tint_color_parameter = parameter
        elif parameter.name == "brightness":
            brightness_parameter = parameter
        elif parameter.name == "glancing_brightness":
            glancing_brightness_parameter = parameter
        elif parameter.name == "lightmap_translucent_map":
            lightmap_translucent_map_parameter = parameter
        elif parameter.name == "lightmap_translucent_color":
            lightmap_translucent_color_parameter = parameter
        elif parameter.name == "lightmap_translucent_alpha":
            lightmap_translucent_alpha_parameter = parameter

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_data_path
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))

    shader_node = get_shader_node(mat.node_tree, "one_alpha_env")
    shader_node.location = Vector((-450.0, -20.0))
    shader_node.name = "Plasma Alpha"
    shader_node.width = 400.0
    shader_node.height = 100.0

    connect_inputs(mat.node_tree, shader_node, "Shader", output_material_node, "Surface")

    if not environment_map_parameter == None:
        environment_map, environment_map_name, environment_map_bitmap = get_h2_bitmap(environment_map_parameter.bitmap, texture_root, report)
        environment_node = generate_image_node(mat, environment_map, environment_map_bitmap, environment_map_name)
        environment_node.name = "Environment Map"
        environment_node.location = Vector((-900, 525))
        if not environment_node.image == None:
            environment_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, environment_node, "Color", shader_node, "Environment Map")

    if not environment_color_parameter == None:
        shader_node.inputs["Environment Color"].default_value = environment_color_parameter.color

    if not specular_map_parameter == None:
        specular_map, specular_map_name, specular_map_bitmap = get_h2_bitmap(specular_map_parameter.bitmap, texture_root, report)
        specular_node = generate_image_node(mat, specular_map, specular_map_bitmap, specular_map_name)
        specular_node.name = "Specular Map"
        specular_node.location = Vector((-900, 525))
        if not specular_node.image == None:
            specular_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, specular_node, "Color", shader_node, "Specular Map")
        set_image_scale(mat, specular_node, specular_map_parameter.scale)

    if not alpha_blend_map_parameter == None:
        alpha_blend_map, alpha_blend_map_name, alpha_blend_map_bitmap = get_h2_bitmap(alpha_blend_map_parameter.bitmap, texture_root, report)
        alpha_blend_node = generate_image_node(mat, alpha_blend_map, alpha_blend_map_bitmap, alpha_blend_map_name)
        alpha_blend_node.name = "Alpha Blend Map"
        alpha_blend_node.location = Vector((-900, 525))
        if not alpha_blend_node.image == None:
            alpha_blend_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, alpha_blend_node, "Color", shader_node, "Alpha Blend Map")
        connect_inputs(mat.node_tree, alpha_blend_node, "Alpha", shader_node, "Alpha Blend Map Alpha")
        set_image_scale(mat, alpha_blend_node, alpha_blend_map_parameter.scale)

    if not alpha_blend_color_parameter == None:
        shader_node.inputs["Alpha Blend Color"].default_value = alpha_blend_color_parameter.color

    if not alpha_blend_opacity_parameter == None:
        shader_node.inputs["Alpha Blend Opacity"].default_value = alpha_blend_opacity_parameter.value

    if not tint_color_parameter == None:
        shader_node.inputs["Tint Color"].default_value = tint_color_parameter.color

    if not glancing_tint_color_parameter == None:
        shader_node.inputs["Glancing Tint Color"].default_value = glancing_tint_color_parameter.color
        
    if not brightness_parameter == None:
        shader_node.inputs["Brightness"].default_value = brightness_parameter.value

    if not glancing_brightness_parameter == None:
        shader_node.inputs["Glancing Brightness"].default_value = glancing_brightness_parameter.value

    if not lightmap_translucent_map_parameter == None:
        lightmap_translucent_map, lightmap_translucent_map_name, lightmap_translucent_map_bitmap = get_h2_bitmap(lightmap_translucent_map_parameter.bitmap, texture_root, report)
        lightmap_translucent_node = generate_image_node(mat, lightmap_translucent_map, lightmap_translucent_map_bitmap, lightmap_translucent_map_name)
        lightmap_translucent_node.name = "Lightmap Translucent Map"
        lightmap_translucent_node.location = Vector((-900, 525))
        if not lightmap_translucent_node.image == None:
            lightmap_translucent_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, lightmap_translucent_node, "Color", shader_node, "Lightmap Translucent Map")
        
    if not lightmap_translucent_color_parameter == None:
        shader_node.inputs["Lightmap Translucent Color"].default_value = lightmap_translucent_color_parameter.color

    if not lightmap_translucent_alpha_parameter == None:
        shader_node.inputs["Lightmap Translucent Alpha"].default_value = lightmap_translucent_alpha_parameter.value