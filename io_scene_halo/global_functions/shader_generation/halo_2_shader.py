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

from enum import Enum, auto
from mathutils import Vector
from .shader_helper import (
    convert_to_blender_color, 
    get_output_material_node, 
    connect_inputs, 
    generate_image_node,
    get_shader_node,
    set_image_scale,
    get_linked_node,
    get_fallback_shader_node,
    is_group_valid,
    place_node
    )

from ...global_functions import global_functions
from ...file_tag.tag_interface import tag_interface, tag_common
from ...file_tag.tag_interface.tag_postprocessing.h2 import unpack_function_buffer

class TypeEnum(Enum):
    bitmap = 0
    _value = auto()
    color = auto()
    switch = auto()

class AnimationTypeEnum(Enum):
    bitmap_scale_uniform = 0
    bitmap_scale_x = auto()
    bitmap_scale_y = auto()
    bitmap_scale_z = auto()
    bitmap_translation_x = auto()
    bitmap_translation_y = auto()
    bitmap_translation_z = auto()
    bitmap_rotation_angle = auto()
    bitmap_rotation_axis_x = auto()
    bitmap_rotation_axis_y = auto()
    bitmap_rotation_axis_z = auto()
    _value = auto()
    color = auto()
    bitmap_index = auto()

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

def get_shader_parameters(shader, shader_template):
    parameters = []
    for category in shader_template["categories"]:
        for parameter in category["parameters"]:
            parameter_settings = ParameterSettings()
            parameter_settings.name = parameter["name"]
            parameter_settings.parameter_type = parameter["type"]
            parameter_settings.bitmap = parameter["default bitmap"]
            parameter_settings.value = parameter["default const value"]
            parameter_settings.color = convert_to_blender_color(parameter["default const color"], True) 
            image_scale = 1.0
            if not parameter["bitmap scale"] == 0.0:
                image_scale = parameter["bitmap scale"]

            parameter_settings.scale = Vector((image_scale, image_scale, image_scale))

            parameters.append(parameter_settings)

    for parameter in shader["parameters"]:
        for default_parameter in parameters:
            if default_parameter.name == parameter["name"]:
                default_parameter.parameter_type = parameter["type"]
                default_parameter.bitmap = parameter["bitmap"]
                default_parameter.value = parameter["const value"]
                default_parameter.color = convert_to_blender_color(parameter["const color"], True)
                for animation_property in parameter["animation properties"]:
                    property_type = AnimationTypeEnum(animation_property["type"]["value"])
                    function_dict = unpack_function_buffer(animation_property["data"])
                    value_a = function_dict["Color 0"]
                    if property_type == AnimationTypeEnum.bitmap_scale_uniform and not value_a == 0.0:
                        default_parameter.scale = Vector((value_a, value_a, value_a))

                    elif property_type == AnimationTypeEnum.bitmap_scale_x and not value_a == 0.0:
                        default_parameter.scale[0] = value_a

                    elif property_type == AnimationTypeEnum.bitmap_scale_y and not value_a == 0.0:
                        default_parameter.scale[1] = value_a

                    elif property_type == AnimationTypeEnum.bitmap_scale_z and not value_a == 0.0:
                        default_parameter.scale[2] = value_a

                    elif property_type == AnimationTypeEnum.color:
                        default_parameter.color = convert_to_blender_color(value_a, True)

                break

    return parameters

def generate_shader_simple(mat, shader_asset, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    base_parameter = None
    if len(shader_data["parameters"]) > 0:
        for parameter in shader_data["parameters"]:
            if base_parameter == None and len(parameter["bitmap"]["path"]) > 0:
                base_parameter = parameter

            if parameter["name"] == "base_map" and len(parameter["bitmap"]["path"]) > 0:
                base_parameter = parameter
                break

    output_material_node = get_output_material_node(mat)
    if output_material_node is None:
        place_node(output_material_node)

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        place_node(bdsf_principled, 1)
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    if base_parameter is not None:
        base_map_texture = generate_image_node(mat, base_parameter["bitmap"], 0, asset_cache, "halo2", report)
        if base_map_texture:
            base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            base_map_node.image = base_map_texture
            base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
            place_node(base_map_node, 2)
            connect_inputs(mat.node_tree, base_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader(mat, shader_asset, template_asset, asset_cache, report):
    shader_data = shader_asset["Data"]
    template_data = template_asset["Data"]

    mat.use_nodes = True

    shader_parameters = get_shader_parameters(shader_data, template_data)
    shader_template_name = os.path.basename(shader_data["template"]["path"])

    texture_root = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_data_path
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node)

    if is_group_valid(shader_template_name):
        shader_node = get_shader_node(mat.node_tree, shader_template_name)
    else:
        shader_node = get_fallback_shader_node(mat.node_tree, shader_template_name)

    if shader_node:
        shader_node.name = shader_template_name.replace('_', ' ').title()
        place_node(shader_node, 1)
        connect_inputs(mat.node_tree, shader_node, "Shader", output_material_node, "Surface")
        shader_node.inputs["Lightmap Factor"].default_value = get_lightmap_factor(shader_data["lightmap type"]["value"])

        row = 0
        for input_socket in shader_node.inputs:
            input_socket_name = input_socket.name
            halo_name = input_socket_name.replace(' ', '_').lower()
            for parameter in shader_parameters:
                if halo_name == parameter.name:
                    parameter_type = TypeEnum(parameter.parameter_type["value"])
                    if parameter_type == TypeEnum.bitmap:
                        bitmap_texture = generate_image_node(mat, parameter.bitmap, 0, asset_cache, "halo2", report)
                        if bitmap_texture:
                            tag_groups = tag_common.h2_tag_groups
                            bitmap_asset = tag_interface.get_disk_asset(parameter.bitmap["path"], tag_groups.get(parameter.bitmap["group name"]))
                            bitmap_data = bitmap_asset["Data"]

                            bitmap_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
                            bitmap_node.image = bitmap_texture
                            bitmap_node.image.alpha_mode = 'CHANNEL_PACKED'
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

                            if is_bump and bitmap_asset:
                                height_value = 0.0
                                if not bitmap_data["bump height"] == 0.0:
                                    height_value = bitmap_data["bump height"]

                                shader_node.inputs["Bump Map Repeat"].default_value = height_value

                            row += 1

                    elif parameter_type == TypeEnum._value:
                        input_socket.default_value = parameter.value
                        if "emissive_power" in parameter.name:
                            input_socket.default_value *= 100

                    elif parameter_type == TypeEnum.color:
                        input_socket.default_value = parameter.color

                    elif parameter_type == TypeEnum.switch:
                        print("IF THIS APPEARS LET GENERAL KNOW.")

    else:
        generate_shader_simple(mat, shader_asset, asset_cache, report)
