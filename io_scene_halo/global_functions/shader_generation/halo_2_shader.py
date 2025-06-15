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

from mathutils import Vector
from .shader_helper import (
    get_h2_bitmap, 
    get_output_material_node, 
    connect_inputs, 
    generate_image_node,
    get_shader_node,
    set_image_scale,
    get_bitmap, 
    get_linked_node,
    get_fallback_shader_node,
    is_group_valid
    )

from ...global_functions import global_functions
from ...global_functions.parse_tags import parse_tag
from ...file_tag.h2.file_shader.format import AnimationTypeEnum, TypeEnum

class ParameterSettings():
    def __init__(self, name="", parameter_type=0, bitmap=None, translation=Vector(), scale=Vector(), rotation=Vector(), color=(0.0, 0.0, 0.0, 1.0), value=0.0):
        self.name = name
        self.parameter_type = parameter_type
        self.bitmap = bitmap
        self.translation = translation
        self.scale = scale
        self.rotation = rotation
        self.color = color
        self.value = value

def get_lightmap_factor(lightmap_type):
    lightmap_factor = 0
    if lightmap_type == 1:
        lightmap_factor = 0.5

    elif lightmap_type == 2:
        lightmap_factor = 0.25

    elif lightmap_type == 3:
        lightmap_factor = 1.0

    return lightmap_factor

def place_node(node, col=0, row=0, spacing=100):
    width = getattr(node, 'width', 140)
    height = getattr(node, 'height', 100)

    x = -(col * (width + spacing))
    y = -row * (height + spacing)

    node.location = (x, y)

def get_shader_parameters(shader, shader_template):
    parameters = []
    for category in shader_template.categories:
        for parameter in category.parameters:
            parameter_settings = ParameterSettings()
            parameter_settings.name = parameter.name
            parameter_settings.parameter_type = parameter.parameter_type
            parameter_settings.bitmap = parameter.default_bitmap
            parameter_settings.value = parameter.default_const_value
            parameter_settings.color = global_functions.convert_color_space(parameter.default_const_color , False)
            image_scale = 1.0
            if not parameter.bitmap_scale == 0.0:
                image_scale = parameter.bitmap_scale

            parameter_settings.scale = Vector((image_scale, image_scale, image_scale))

            parameters.append(parameter_settings)

    for parameter in shader.parameters:
        for default_parameter in parameters:
            if default_parameter.name == parameter.name:
                default_parameter.parameter_type = parameter.type
                default_parameter.bitmap = parameter.bitmap
                default_parameter.value = parameter.const_value
                default_parameter.color = global_functions.convert_color_space(parameter.const_color , False)
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
                        default_parameter.color = global_functions.convert_color_space(animation_property.color_a , False)

                break

    return parameters

def generate_shader_simple(mat, shader, report):
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

def generate_shader(mat, shader, shader_template, report):
    mat.use_nodes = True

    shader_parameters = get_shader_parameters(shader, shader_template)
    shader_template_name = os.path.basename(shader.template.name)

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_data_path
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node)

    if is_group_valid(shader_template_name):
        shader_node = get_shader_node(mat.node_tree, shader_template_name)
    else:
        shader_node = get_fallback_shader_node(mat.node_tree, shader_template_name)

    shader_node.name = shader_template_name.replace('_', ' ').title()
    place_node(shader_node, 1)
    connect_inputs(mat.node_tree, shader_node, "Shader", output_material_node, "Surface")
    shader_node.inputs["Lightmap Factor"].default_value = get_lightmap_factor(shader.lightmap_type)

    row = 0
    for input_socket in shader_node.inputs:
        input_socket_name = input_socket.name
        halo_name = input_socket_name.replace(' ', '_').lower()
        for parameter in shader_parameters:
            if halo_name == parameter.name:
                parameter_type = TypeEnum(parameter.parameter_type)
                if parameter_type == TypeEnum.bitmap:
                    parameter_map, parameter_name, parameter_bitmap = get_h2_bitmap(parameter.bitmap, texture_root, report)
                    bitmap_node = generate_image_node(mat, parameter_map, parameter_bitmap, parameter_name)
                    bitmap_node.name = input_socket_name
                    place_node(bitmap_node, 2, row)

                    is_bump = False
                    is_detail = False
                    is_noise = False
                    if input_socket_name == "Bump Map":
                        is_bump = True

                    if "Detail" in input_socket_name:
                        is_detail = True

                    if "Noise" in input_socket_name:
                        is_noise = True

                    if is_bump:    
                        bitmap_node.interpolation = 'Cubic'

                    if not bitmap_node.image == None:
                        if is_bump or is_detail:
                            bitmap_node.image.colorspace_settings.name = 'Non-Color'
                        elif is_noise:
                            bitmap_node.image.colorspace_settings.name = 'Linear Rec.709'

                        bitmap_node.image.alpha_mode = 'CHANNEL_PACKED'

                    connect_inputs(mat.node_tree, bitmap_node, "Color", shader_node, input_socket_name)
                    connect_inputs(mat.node_tree, bitmap_node, "Alpha", shader_node, "%s Alpha" % input_socket_name)

                    set_image_scale(mat, bitmap_node, parameter.scale)

                    if is_bump and parameter_bitmap:
                        height_value = 0.0
                        if not parameter_bitmap.bump_height == 0.0:
                            height_value = parameter_bitmap.bump_height

                        shader_node.inputs["Bump Map Repeat"].default_value = height_value

                    row += 1

                elif parameter_type == TypeEnum._value:
                    input_socket.default_value = parameter.value
                elif parameter_type == TypeEnum.color:
                    input_socket.default_value = parameter.color
                elif parameter_type == TypeEnum.switch:
                    print("IF THIS APPEARS LET GENERAL KNOW.")
