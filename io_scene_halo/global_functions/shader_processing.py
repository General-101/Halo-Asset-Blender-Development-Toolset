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
import json
import subprocess

from mathutils import Vector
from enum import Flag, Enum, auto
from . import global_functions, mesh_processing
from .shader_generation.shader_helper import (
    get_linked_node, 
    get_output_material_node, 
    connect_inputs, 
    generate_image_node, 
    place_node
    )

from .shader_generation.shader_transparent_generic import generate_shader_transparent_generic
from .shader_generation.shader_environment import generate_shader_environment
from .shader_generation.shader_model import generate_shader_model
from .shader_generation.halo_2_shader import generate_shader, generate_shader_simple
from ..file_tag.tag_interface import tag_interface, tag_common

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

def generate_shader_environment_simple(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node)

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    place_node(bdsf_principled, 1)

    base_map_texture = generate_image_node(mat, shader_data["base map"], permutation_index, asset_cache, "halo1", report)
    if base_map_texture:
        base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        base_map_node.image = base_map_texture
        base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        place_node(base_map_node, 2)
        connect_inputs(mat.node_tree, base_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_model_simple(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node)

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    place_node(bdsf_principled, 1)

    base_map_texture = generate_image_node(mat, shader_data["base map"], permutation_index, asset_cache, "halo1", report)
    if base_map_texture:
        base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        base_map_node.image = base_map_texture
        base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        place_node(base_map_node, 2)
        connect_inputs(mat.node_tree, base_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_chicago_simple(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node)

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    place_node(bdsf_principled, 1)

    if len(shader_data["maps"]) > 0:
        base_map = shader_data["maps"][0]["map"]
        base_map_texture = generate_image_node(mat, base_map, permutation_index, asset_cache, "halo1", report)
        if base_map_texture:
            base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            base_map_node.image = base_map_texture
            base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
            place_node(base_map_node, 2)
            connect_inputs(mat.node_tree, base_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_chicago_extended_simple(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node)

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    place_node(bdsf_principled, 1)

    if len(shader_data["4 stage maps"]) > 0:
        base_map = shader_data["4 stage maps"][0]["map"]
        base_map_texture = generate_image_node(mat, base_map, permutation_index, asset_cache, "halo1", report)
        if base_map_texture:
            base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            base_map_node.image = base_map_texture
            base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
            place_node(base_map_node, 2)
            connect_inputs(mat.node_tree, base_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_generic_simple(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node)

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    place_node(bdsf_principled, 1)

    if len(shader_data["maps"]) > 0:
        base_map = shader_data["maps"][0]["map"]
        base_map_texture = generate_image_node(mat, base_map, permutation_index, asset_cache, "halo1", report)
        if base_map_texture:
            base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            base_map_node.image = base_map_texture
            base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
            place_node(base_map_node, 2)
            connect_inputs(mat.node_tree, base_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_glass_simple(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node)

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    place_node(bdsf_principled, 1)

    base_map_texture = generate_image_node(mat, shader_data["diffuse map"], permutation_index, asset_cache, "halo1", report)
    if base_map_texture:
        base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        base_map_node.image = base_map_texture
        base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        place_node(base_map_node, 2)
        connect_inputs(mat.node_tree, base_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_meter_simple(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node)

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    place_node(bdsf_principled, 1)

    base_map_texture = generate_image_node(mat, shader_data["meter map"], permutation_index, asset_cache, "halo1", report)
    if base_map_texture:
        base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        base_map_node.image = base_map_texture
        base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        place_node(base_map_node, 2)
        connect_inputs(mat.node_tree, base_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_plasma_simple(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node)

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    place_node(bdsf_principled, 1)

    base_map_texture = generate_image_node(mat, shader_data["primary noise map"], permutation_index, asset_cache, "halo1", report)
    if base_map_texture:
        base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        base_map_node.image = base_map_texture
        base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        place_node(base_map_node, 2)
        connect_inputs(mat.node_tree, base_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_water_simple(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node)

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    place_node(bdsf_principled, 1)

    base_map_texture = generate_image_node(mat, shader_data["base map"], permutation_index, asset_cache, "halo1", report)
    if base_map_texture:
        base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        base_map_node.image = base_map_texture
        base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        place_node(base_map_node, 2)
        connect_inputs(mat.node_tree, base_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_meter(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node)

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    place_node(bdsf_principled, 1)

    base_map_texture = generate_image_node(mat, shader_data["map"], permutation_index, asset_cache, "halo1", report)
    if base_map_texture:
        base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        base_map_node.image = base_map_texture
        base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        place_node(base_map_node, 2)
        connect_inputs(mat.node_tree, base_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_glass(mat, shader_asset, permutation_index, asset_cache, report):
    shader_data = shader_asset["Data"]

    mat.use_nodes = True

    output_material_node = get_output_material_node(mat)
    place_node(output_material_node)

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    place_node(bdsf_principled, 1)

    base_map_texture = generate_image_node(mat, shader_data["diffuse map"], permutation_index, asset_cache, "halo1", report)
    if base_map_texture:
        base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        base_map_node.image = base_map_texture
        base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        place_node(base_map_node, 2)
        connect_inputs(mat.node_tree, base_map_node, "Color", bdsf_principled, "Base Color")

def generate_h1_shader(mat, tag_ref, permutation_index, asset_cache, report):
    # 0 = Shader generation is disabled
    # 1 = Simple shader generation. Only the base map is generated
    # 2 = Full Shader generation
    if not int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 0:
        tag_groups = tag_common.h1_tag_groups
        shader_asset = tag_interface.get_disk_asset(tag_ref["path"], tag_groups.get(tag_ref["group name"]))
        if not shader_asset == None:
            if shader_asset["Header"]["tag group"] == "senv":
                if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                    generate_shader_environment_simple(mat, shader_asset, permutation_index, asset_cache, report)
                else:
                    generate_shader_environment(mat, shader_asset, permutation_index, asset_cache, report)

            elif shader_asset["Header"]["tag group"] == "soso":
                if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                    generate_shader_model_simple(mat, shader_asset, permutation_index, asset_cache, report)
                else:
                    generate_shader_model(mat, shader_asset, permutation_index, asset_cache, report)

            elif shader_asset["Header"]["tag group"] == "schi":
                # TODO: Needs a proper shader node group
                if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                    generate_shader_transparent_chicago_simple(mat, shader_asset, permutation_index, asset_cache, report)
                else:
                    generate_shader_transparent_chicago_simple(mat, shader_asset, permutation_index, asset_cache, report)

            elif shader_asset["Header"]["tag group"] == "scex":
                # TODO: Needs a proper shader node group
                if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                    generate_shader_transparent_chicago_extended_simple(mat, shader_asset, permutation_index, asset_cache, report)
                else:
                    generate_shader_transparent_chicago_extended_simple(mat, shader_asset, permutation_index, asset_cache, report)

            elif shader_asset["Header"]["tag group"] == "sotr":
                # TODO: Needs a proper shader node group
                if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                    generate_shader_transparent_generic_simple(mat, shader_asset, permutation_index, asset_cache, report)
                else:
                    generate_shader_transparent_generic(mat, shader_asset, permutation_index, asset_cache, report)

            elif shader_asset["Header"]["tag group"] == "sgla":
                # TODO: Needs a proper shader node group
                if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                    generate_shader_transparent_glass_simple(mat, shader_asset, permutation_index, asset_cache, report)
                else:
                    generate_shader_transparent_glass(mat, shader_asset, permutation_index, asset_cache, report)

            elif shader_asset["Header"]["tag group"] == "smet":
                # TODO: Needs a proper shader node group
                if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                    generate_shader_transparent_meter_simple(mat, shader_asset, permutation_index, asset_cache, report)
                else:
                    generate_shader_transparent_meter(mat, shader_asset, permutation_index, asset_cache, report)

            elif shader_asset["Header"]["tag group"] == "spla":
                # TODO: Needs a proper shader node group
                if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                    generate_shader_transparent_plasma_simple(mat, shader_asset, permutation_index, asset_cache, report)
                else:
                    generate_shader_transparent_plasma_simple(mat, shader_asset, permutation_index, asset_cache, report)

            elif shader_asset["Header"]["tag group"] == "swat":
                # TODO: Needs a proper shader node group
                if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                    generate_shader_transparent_water_simple(mat, shader_asset, permutation_index, asset_cache, report)
                else:
                    generate_shader_transparent_water_simple(mat, shader_asset, permutation_index, asset_cache, report)

        else:
            print("Halo 1 parsed shader tag returned as none. Something went horribly wrong")

    else:
        print("Shader generation is disabled. Skipping")

def generate_h2_shader(mat, tag_ref, asset_cache, report):
    # 0 = Shader generation is disabled
    # 1 = Simple shader generation. Only the base map is generated
    # 2 = Full Shader generation
    if not int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 0:
        tag_groups = tag_common.h2_tag_groups
        shader_asset = tag_interface.get_disk_asset(tag_ref["path"], tag_groups.get(tag_ref["group name"]))
        template_asset = tag_interface.get_disk_asset(shader_asset["Data"]["template"]["path"], tag_groups.get(shader_asset["Data"]["template"]["group name"]))
        if not shader_asset == None:
            if shader_asset["Header"]["tag group"] == "shad":
                if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1 or template_asset is None:
                    generate_shader_simple(mat, shader_asset, asset_cache, report)
                else:
                    generate_shader(mat, shader_asset, template_asset, asset_cache, report)

        else:
            print("Halo 2 parsed shader tag returned as none. Something went horribly wrong")

    else:
        print("Shader generation is disabled. Skipping")

def config_is_valid(data_directory, tags_directory, report, game_title="halo3"):
    is_valid = True
    if Image == None:
        is_valid = False
        report({'ERROR'}, "You are missing required libraries. Please instal Pillow. No textures will be imported")

    if not os.path.isdir(data_directory):
        is_valid = False
        report({'ERROR'}, "Your defined %s data directory does not exist. No textures will be imported" % game_title)

    if not os.path.isdir(tags_directory):
        is_valid = False
        report({'ERROR'}, "Your defined %s tags directory does not exist. No textures will be imported" % game_title)

    if not os.path.isfile(os.path.join(os.path.dirname(os.path.dirname(data_directory)), "tool.exe")):
        is_valid = False
        report({'ERROR'}, "Your defined %s tool.exe can't be found. No textures will be imported" % game_title)

    return is_valid

def generate_h3_shader_simple(mat, shader_path, asset_cache, report):
    mat.use_nodes = True

    data_directory = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_3_data_path
    tags_directory = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_3_tag_path
    bitmap_file = None
    bitm_ref = {"group name": None, "path": ""}
    input_file = ""
    if config_is_valid(data_directory, tags_directory, report):
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

            bitm_ref = {"group name": "bitm", "path": input_file}

            if asset_cache.get("bitm") is None:
                asset_cache["bitm"] = {}

            if asset_cache["bitm"].get(input_file) is None:
                asset_cache["bitm"][input_file] = {"blender_assets": {}, "has_disk_asset": False, "matching_checksum": False}
        
            bitmap_file = os.path.join(output_directory, bitmap_directory, "pixel_data_%s%s" % (bitmap_name, "_00_00.tga"))

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

    base_map_texture = generate_image_node(mat, bitm_ref, 0, asset_cache, "halo3", report)
    if base_map_texture:
        base_map_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        base_map_node.image = base_map_texture
        base_map_node.image.alpha_mode = 'CHANNEL_PACKED'
        base_map_node.location = Vector((-1600, 500))
        connect_inputs(mat.node_tree, base_map_node, "Color", bdsf_principled, "Base Color")

def generate_h3_shader(mat, shader_path, asset_cache, report):
    # 0 = Shader generation is disabled
    # 1 = Simple shader generation. Only the base map is generated
    # 2 = Full Shader generation
    if not int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 0:
        if not shader_path == None:
            if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                generate_h3_shader_simple(mat, shader_path, asset_cache, report)
            else:
                generate_h3_shader_simple(mat, shader_path, asset_cache, report)
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
    shader_tag = {"group name": None, "path": ""}
    shader_extension = None
    if not global_functions.string_empty_check(data_path) and not global_functions.string_empty_check(tag_path):
        import_directory = os.path.dirname(os.path.dirname(import_filepath)).lower()
        result = import_directory.split(data_path)
        local_path = None
        if len(result) == 2:
            local_path = result[1]

        if local_path:
            import_directory = os.path.join(tag_path, local_path)
            for root, dirs, files in os.walk(import_directory):
                for file in files:
                    file_name = os.path.basename(file).lower()
                    result = file_name.rsplit(".", 1)
                    if len(result) == 2:
                        file_name = result[0]
                        extension = result[1]

                    if processed_name == file_name and extension in shader_extensions:
                        shader_path = os.path.join(root, file)
                        shader_extension = extension
                        break

                    if not shader_path == None and shader_extension in shader_extensions:
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

                    if processed_name == file_name and extension in shader_extensions:
                        shader_path = file
                        shader_extension = extension
                        break

        if not shader_path == None:
            tag_group = ""
            local_path = ""
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

            result = shader_path.split(tag_path)
            if len(result) > 1:
                local_path = result[1].rsplit(".", 1)[0]

            shader_tag = {"group name": tag_group, "path": local_path}

        else:
            print("Halo 1 Shader path wasn't set. Something went terribly wrong when trying to find %s shader" % material_name)

    else:
       print("Your Halo 1 data and tag paths are not set. Please set them in preferences and restart Blender") 

    return shader_tag

def find_h2_shader_tag(import_filepath, material_name):
    data_path = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_data_path.lower()
    tag_path = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_tag_path.lower()
    shader_path = None
    shader_tag = {"group name": None, "path": ""}

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

            shader_tag = {"group name": "shad", "path": local_path}

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
