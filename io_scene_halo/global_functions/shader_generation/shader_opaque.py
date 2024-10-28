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
    HALO_2_SHADER_RESOURCES
    )

from ...file_tag.h2.file_shader.format import AnimationTypeEnum

def get_shader_node(tree, shader_name):
    if not bpy.data.node_groups.get(shader_name):
        with bpy.data.libraries.load(HALO_2_SHADER_RESOURCES) as (data_from, data_to):
            data_to.node_groups.append(data_from.node_groups[data_from.node_groups.index(shader_name)])

    tex_bump_node = tree.nodes.new('ShaderNodeGroup')
    tex_bump_node.node_tree = bpy.data.node_groups.get(shader_name)

    return tex_bump_node

def set_image_scale(mat, image_node, image_parameter, default_scale):
    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-200, -125)) + image_node.location

    connect_inputs(mat.node_tree, vect_math_node, "Vector", image_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-400, -100)) + image_node.location
    combine_xyz_node.location = Vector((-400, -225)) + image_node.location
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    x_scale = default_scale
    y_scale = default_scale
    if not image_parameter == None:
        for animation_property in image_parameter.animation_properties:
            property_type = AnimationTypeEnum(animation_property.type)
            if property_type == AnimationTypeEnum.bitmap_scale_x and not animation_property.lower_bound == 0.0:
                x_scale = animation_property.lower_bound

            elif property_type == AnimationTypeEnum.bitmap_scale_y and not animation_property.lower_bound == 0.0:
                y_scale = animation_property.lower_bound

    combine_xyz_node.inputs[0].default_value = x_scale
    combine_xyz_node.inputs[1].default_value = y_scale
    combine_xyz_node.inputs[2].default_value = 1

def generate_shader_tex_bump(mat, shader, shader_template, report):
    mat.use_nodes = True

    bump_parameter = None
    alpha_parameter = None
    base_parameter = None
    detail_parameter = None
    specular_parameter = None
    specular_glancing_parameter = None

    bump_value = None
    base_value = None
    detail_value = None
    specular_value = None
    specular_glancing_value = None
    for parameter in shader.parameters:
        if parameter.name == "bump_map":
            bump_parameter = parameter
            bump_value = parameter.bitmap
        elif parameter.name == "lightmap_alphatest_map":
            alpha_parameter = parameter
            alpha_value = parameter.bitmap
        elif parameter.name == "base_map":
            base_parameter = parameter
            base_value = parameter.bitmap
        elif parameter.name == "detail_map":
            detail_parameter = parameter
            detail_value = parameter.bitmap
        elif parameter.name == "specular_color":
            specular_parameter = parameter
            specular_value = parameter.const_color
        elif parameter.name == "specular_glancing_color":
            specular_glancing_parameter = parameter
            specular_glancing_value = parameter.const_color

    for category in shader_template.categories:
        for parameter in category.parameters:
            if parameter.name == "bump_map" and bump_value == None:
                bump_value = parameter.default_bitmap
            elif parameter.name == "base_map" and base_value == None:
                base_value = parameter.default_bitmap
            elif parameter.name == "detail_map" and detail_value == None:
                detail_value = parameter.default_bitmap
            elif parameter.name == "specular_color" and specular_value == None:
                specular_value = parameter.default_const_color
            elif parameter.name == "specular_glancing_color" and specular_glancing_value == None:
                specular_glancing_value = parameter.default_const_color

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

    if not bump_value == None:
        bump_map, bump_map_name, bump_bitmap = get_h2_bitmap(bump_value, texture_root, report)
        bump_node = generate_image_node(mat, bump_map, bump_bitmap, bump_map_name)
        bump_node.name = "Bump Map"
        bump_node.location = Vector((-900, 525))
        bump_node.interpolation = 'Cubic'
        if not bump_node.image == None:
            bump_node.image.colorspace_settings.name = 'Non-Color'
            bump_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, bump_node, "Color", tex_bump_node, "Bump Map")
        set_image_scale(mat, bump_node, bump_parameter, 1)
        if bump_bitmap:
            height_value = 0.0
            if not bump_bitmap.bump_height == 0.0:
                height_value = bump_bitmap.bump_height / 10
            tex_bump_node.inputs["Bump Map Repeat"].default_value = height_value

    if not alpha_parameter == None:
        alpha_map, alpha_map_name, alpha_bitmap = get_h2_bitmap(alpha_parameter.bitmap, texture_root, report)
        alpha_node = generate_image_node(mat, alpha_map, alpha_bitmap, alpha_map_name)
        alpha_node.name = "Bump Map"
        alpha_node.location = Vector((-900, 225))
        if not alpha_node.image == None:
            alpha_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, alpha_node, "Alpha", tex_bump_node, "Lightmap Alphatest Map")

    if not base_value == None:
        base_map, base_map_name, base_bitmap = get_h2_bitmap(base_value, texture_root, report)
        base_node = generate_image_node(mat, base_map, base_bitmap, base_map_name)
        base_node.name = "Base Map"
        base_node.location = Vector((-900, -75))
        if not base_node.image == None:
            base_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, base_node, "Color", tex_bump_node, "Base Map")
        connect_inputs(mat.node_tree, base_node, "Alpha", tex_bump_node, "Base Map Alpha")
        set_image_scale(mat, base_node, base_parameter, 1)

    if not detail_value == None:
        detail_map, detail_map_name, detail_bitmap = get_h2_bitmap(detail_value, texture_root, report)
        detail_node = generate_image_node(mat, detail_map, detail_bitmap, detail_map_name)
        detail_node.name = "Detail Map"
        detail_node.location = Vector((-900, -375))
        if not detail_node.image == None:
            detail_node.image.colorspace_settings.name = 'Non-Color'
            detail_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, detail_node, "Color", tex_bump_node, "Detail Map")
        set_image_scale(mat, detail_node, detail_parameter, 16)

    if not specular_value == None:
        tex_bump_node.inputs["Specular Color"].default_value = specular_value
    if not specular_glancing_value == None:
        tex_bump_node.inputs["Specular Glancing Color"].default_value = specular_glancing_value

def generate_shader_tex_bump_detail_blend_detail(mat, shader, shader_template, report):
    mat.use_nodes = True

    bump_parameter = None
    base_parameter = None
    detail_1_parameter = None
    detail_2_parameter = None
    overlay_parameter = None
    specular_parameter = None
    specular_glancing_parameter = None

    bump_value = None
    base_value = None
    detail_1_value = None
    detail_2_value = None
    overlay_value = None
    specular_value = None
    specular_glancing_value = None
    for parameter in shader.parameters:
        if parameter.name == "bump_map":
            bump_parameter = parameter
            bump_value = parameter.bitmap
        elif parameter.name == "base_map":
            base_parameter = parameter
            base_value = parameter.bitmap
        elif parameter.name == "blend_detail_map_1":
            detail_1_parameter = parameter
            detail_1_value = parameter.bitmap
        elif parameter.name == "blend_detail_map_2":
            detail_2_parameter = parameter
            detail_2_value = parameter.bitmap
        elif parameter.name == "overlay_detail_map":
            overlay_parameter = parameter
            overlay_value = parameter.bitmap
        elif parameter.name == "specular_color":
            specular_parameter = parameter
            specular_value = parameter.const_color
        elif parameter.name == "specular_glancing_color":
            specular_glancing_parameter = parameter
            specular_glancing_value = parameter.const_color

    for category in shader_template.categories:
        for parameter in category.parameters:
            if parameter.name == "bump_map" and bump_value == None:
                bump_value = parameter.default_bitmap
            elif parameter.name == "base_map" and base_value == None:
                base_value = parameter.default_bitmap
            elif parameter.name == "blend_detail_map_1" and detail_1_value == None:
                detail_1_value = parameter.default_bitmap
            elif parameter.name == "blend_detail_map_2" and detail_2_value == None:
                detail_2_value = parameter.default_bitmap
            elif parameter.name == "overlay_detail_map" and overlay_value == None:
                overlay_value = parameter.default_bitmap
            elif parameter.name == "specular_color" and specular_value == None:
                specular_value = parameter.default_const_color
            elif parameter.name == "specular_glancing_color" and specular_glancing_value == None:
                specular_glancing_value = parameter.default_const_color

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

    if not bump_value == None:
        bump_map, bump_map_name, bump_bitmap = get_h2_bitmap(bump_value, texture_root, report)
        bump_node = generate_image_node(mat, bump_map, bump_bitmap, bump_map_name)
        bump_node.name = "Bump Map"
        bump_node.location = Vector((-900, 525))
        bump_node.interpolation = 'Cubic'
        if not bump_node.image == None:
            bump_node.image.colorspace_settings.name = 'Non-Color'
            bump_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, bump_node, "Color", tex_bump_node, "Bump Map")
        set_image_scale(mat, bump_node, bump_parameter, 1)
        if bump_bitmap:
            height_value = 0.0
            if not bump_bitmap.bump_height == 0.0:
                height_value = bump_bitmap.bump_height / 10
            tex_bump_node.inputs["Bump Map Repeat"].default_value = height_value

    if not base_value == None:
        base_map, base_map_name, base_bitmap = get_h2_bitmap(base_value, texture_root, report)
        base_node = generate_image_node(mat, base_map, base_bitmap, base_map_name)
        base_node.name = "Base Map"
        base_node.location = Vector((-900, -75))
        if not base_node.image == None:
            base_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, base_node, "Color", tex_bump_node, "Base Map")
        connect_inputs(mat.node_tree, base_node, "Alpha", tex_bump_node, "Base Map Alpha")
        set_image_scale(mat, base_node, base_parameter, 1)

    if not detail_1_value == None:
        detail_map, detail_map_name, detail_bitmap = get_h2_bitmap(detail_1_value, texture_root, report)
        detail_node = generate_image_node(mat, detail_map, detail_bitmap, detail_map_name)
        detail_node.name = "Detail Map 1"
        detail_node.location = Vector((-900, -375))
        if not detail_node.image == None:
            detail_node.image.colorspace_settings.name = 'Non-Color'
            detail_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, detail_node, "Color", tex_bump_node, "Detail Map 1")
        set_image_scale(mat, detail_node, detail_1_parameter, 16)

    if not detail_2_value == None:
        detail_map, detail_map_name, detail_bitmap = get_h2_bitmap(detail_2_value, texture_root, report)
        detail_node = generate_image_node(mat, detail_map, detail_bitmap, detail_map_name)
        detail_node.name = "Detail Map 1"
        detail_node.location = Vector((-900, -375))
        if not detail_node.image == None:
            detail_node.image.colorspace_settings.name = 'Non-Color'
            detail_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, detail_node, "Color", tex_bump_node, "Detail Map 2")
        set_image_scale(mat, detail_node, detail_2_parameter, 16)

    if not overlay_value == None:
        detail_map, detail_map_name, detail_bitmap = get_h2_bitmap(overlay_value, texture_root, report)
        detail_node = generate_image_node(mat, detail_map, detail_bitmap, detail_map_name)
        detail_node.name = "Overlay Detail Map"
        detail_node.location = Vector((-900, -375))
        if not detail_node.image == None:
            detail_node.image.colorspace_settings.name = 'Non-Color'
            detail_node.image.alpha_mode = 'CHANNEL_PACKED'

        connect_inputs(mat.node_tree, detail_node, "Color", tex_bump_node, "Overlay Detail Map")
        set_image_scale(mat, detail_node, overlay_parameter, 16)

    if not specular_value == None:
        tex_bump_node.inputs["Specular Color"].default_value = specular_value
    if not specular_glancing_value == None:
        tex_bump_node.inputs["Specular Glancing Color"].default_value = specular_glancing_value
