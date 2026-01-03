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
import subprocess

from mathutils import Vector
from ..shader_generation.shader_helper import (
    connect_inputs, 
    get_linked_node, 
    generate_image_node, 
    get_output_material_node, 
    )

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
    if config_is_valid(data_directory, tags_directory, report) and shader_path.startswith(tags_directory):
        tool_directory = os.path.dirname(os.path.dirname(data_directory))
        output_directory = os.path.join(tool_directory, "blender_dumps")
        tool_path = os.path.join(tool_directory, "tool.exe")

        local_path_no_ext = os.path.relpath(shader_path, tags_directory).rsplit(".", 1)[0]

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