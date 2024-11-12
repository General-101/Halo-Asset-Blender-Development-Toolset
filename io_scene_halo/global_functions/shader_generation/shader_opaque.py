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
from ...file_tag.h2.file_shader_template.format import TypeEnum

class ParameterSettings():
    def __init__(self, name="", bitmap=None, translation=Vector(), scale=Vector(), rotation=Vector(), color=(0.0, 0.0, 0.0, 1.0), value=0.0):
        self.name = name
        self.bitmap = bitmap
        self.translation = translation
        self.scale = scale
        self.rotation = rotation
        self.color = color
        self.value = value

def get_shader_node(tree, shader_name):
    if not bpy.data.node_groups.get(shader_name):
        with bpy.data.libraries.load(HALO_2_SHADER_RESOURCES) as (data_from, data_to):
            data_to.node_groups.append(data_from.node_groups[data_from.node_groups.index(shader_name)])

    tex_bump_node = tree.nodes.new('ShaderNodeGroup')
    tex_bump_node.node_tree = bpy.data.node_groups.get(shader_name)

    return tex_bump_node

def set_image_scale(mat, image_node, image_scale):
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

    combine_xyz_node.inputs[0].default_value = image_scale[0]
    combine_xyz_node.inputs[1].default_value = image_scale[1]
    combine_xyz_node.inputs[2].default_value = image_scale[2]

def generate_parameters(shader, shader_template, parameter_keys):
    parameters = []
    for category in shader_template.categories:
        for parameter in category.parameters:
            if parameter.name in parameter_keys:
                parameter_settings = ParameterSettings()
                parameter_settings.name = parameter.name
                parameter_settings.bitmap = parameter.default_bitmap
                parameter_settings.value = parameter.default_const_value
                parameter_settings.color = parameter.default_const_color
                image_scale = 1.0
                if not parameter.bitmap_scale == 0.0:
                    image_scale = parameter.bitmap_scale

                parameter_settings.scale = Vector((image_scale, image_scale, image_scale))

                parameters.append(parameter_settings)

    for parameter in shader.parameters:
        for default_parameter in parameters:
            if default_parameter.name == parameter.name:
                default_parameter.bitmap = parameter.bitmap
                default_parameter.value = parameter.const_value
                default_parameter.color = parameter.const_color
                for animation_property in parameter.animation_properties:
                    property_type = AnimationTypeEnum(animation_property.type)
                    if property_type == AnimationTypeEnum.bitmap_scale_uniform and not animation_property.lower_bound == 0.0:
                        default_parameter.scale = Vector((animation_property.lower_bound, animation_property.lower_bound, animation_property.lower_bound))

                    elif property_type == AnimationTypeEnum.bitmap_scale_x and not animation_property.lower_bound == 0.0:
                        default_parameter.scale[0] = animation_property.lower_bound

                    elif property_type == AnimationTypeEnum.bitmap_scale_y and not animation_property.lower_bound == 0.0:
                        default_parameter.scale[1] = animation_property.lower_bound

                    elif property_type == AnimationTypeEnum.bitmap_scale_z and not animation_property.lower_bound == 0.0:
                        default_parameter.scale[2] = animation_property.lower_bound

                    elif property_type == AnimationTypeEnum.color:
                        default_parameter.color = animation_property.color_a

                break

    return parameters

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
                height_value = bump_bitmap.bump_height / 10

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
                height_value = bump_bitmap.bump_height / 10

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
