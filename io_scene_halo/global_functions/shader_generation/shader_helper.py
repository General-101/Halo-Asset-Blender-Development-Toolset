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
import zlib
import numpy as np

from mathutils import Vector
from ...global_functions.parse_tags import parse_tag
from ...global_functions import global_functions
from ...file_tag.h1.file_shader_model.format import ModelFlags, DetailFumctionEnum, DetailMaskEnum, FunctionEnum
try:
    from PIL import Image
except ModuleNotFoundError:
    print("PIL not found. Unable to create image node.")
    Image = None

HALO_1_SHADER_RESOURCES = os.path.join(os.path.dirname(os.path.realpath(__file__)), "halo_1_shader_resources.blend")
HALO_2_SHADER_RESOURCES = os.path.join(os.path.dirname(os.path.realpath(__file__)), "halo_2_shader_resources.blend")

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

def get_bitmap(tag_ref, texture_root):
    texture_extensions = ("tif", "tiff")
    texture_path = None
    bitmap_name = "White"
    if not tag_ref == None and tag_ref.name_length > 0:
        bitmap_name = "%s_%s" % (global_functions.string_checksum(tag_ref.name, checksum = 0), os.path.basename(tag_ref.name))
        for extension in texture_extensions:
            check_path = os.path.join(texture_root, "%s.%s" % (tag_ref.name, extension))
            if os.path.isfile(check_path):
                texture_path = check_path
                break

        if not texture_path:
            print("data texture for the following bitmap was not found")
            print(tag_ref.name)
    else:
        print("No bitmap was set")

    return texture_path, bitmap_name

def get_h2_bitmap(tag_ref, texture_root, report):
    texture_extensions = ("tif", "tiff")
    texture_path = None
    bitmap_name = "White"
    bitmap_tag = None
    if not tag_ref == None and tag_ref.name_length > 0:
        bitmap_name = "%s_%s" % (global_functions.string_checksum(tag_ref.name, checksum = 0), os.path.basename(tag_ref.name))
        for extension in texture_extensions:
            check_path = os.path.join(texture_root, "%s.%s" % (tag_ref.name, extension))
            if os.path.isfile(check_path):
                texture_path = check_path
                break

        if not texture_path:
            print("data texture for the following bitmap was not found")
            print(tag_ref.name)

        bitmap_tag = parse_tag(tag_ref, report, "halo2", "retail")

    else:
        print("No bitmap was set")

    return texture_path, bitmap_name, bitmap_tag

def get_output_material_node(mat):
    output_material_node = None
    if not mat == None and mat.use_nodes and not mat.node_tree == None:
        for node in mat.node_tree.nodes:
            if node.type == "OUTPUT_MATERIAL" and node.is_active_output:
                output_material_node = node
                break

    if output_material_node is None:
        output_material_node = mat.node_tree.nodes.new("ShaderNodeOutputMaterial")
        output_material_node.location = (0.0, 0.0)

    return output_material_node

def get_linked_node(node, input_name, search_type):
    linked_node = None
    node_input = node.inputs[input_name]
    if node_input.is_linked:
        for node_link in node_input.links:
            if node_link.from_node.type == search_type:
                linked_node = node_link.from_node
                break

    return linked_node

def connect_inputs(tree, output_node, output_name, input_node, input_name):
    tree.links.new(output_node.outputs[output_name], input_node.inputs[input_name])

def generate_image_node(mat, texture, BITMAP=None, bitmap_name="White", is_env=False, pixel_data=None):
    if is_env:
        image_node = mat.node_tree.nodes.new("ShaderNodeTexEnvironment")
    else:
        image_node = mat.node_tree.nodes.new("ShaderNodeTexImage")

    if BITMAP and Image and BITMAP.compressed_color_plate_data.size > 0:
        image = bpy.data.images.get(bitmap_name)
        if not image:
            x = BITMAP.color_plate_width
            y = BITMAP.color_plate_height

            image = bpy.data.images.new(bitmap_name, x, y, alpha = True)
            decompressed_data = zlib.decompress(BITMAP.compressed_color_plate)
            pil_image = Image.frombytes("RGBA", (x, y), decompressed_data, 'raw', "BGRA").transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)
            pixels = list(pil_image.getdata())
            background_color = pixels[0][:3]
            divider_color = pixels[1][:3]
            dummy_color = pixels[2][:3]

            normalized = 1.0 / 255.0
            
            blender_pixels = (np.asarray(pil_image.convert('RGBA'),dtype=np.float32) * normalized).ravel()

            image.pixels[:] = blender_pixels
            image.pack()

        image_node.image = image

    else:
        if not texture == None and os.path.isfile(texture):
            print("No color plate found. Loading texture found in data directory.")
            image = bpy.data.images.load(texture, check_existing=True)
            image_node.image = image

        elif not pixel_data == None:
            print("No color plate found. Loading texture dumped from pixel data. Expect quality loss.")
            image = bpy.data.images.load(pixel_data, check_existing=True)
            image_node.image = image

        else:
            print("No color plate found. Generating white image.")
            image = bpy.data.images.get(bitmap_name)
            if not image:
                image = bpy.data.images.new(bitmap_name, 2, 2)
                image.generated_color = (1, 1, 1, 1)
                image.pack()

            image_node.image = image

        print(" ")

    return image_node

def generate_biased_multiply_node(tree):
    biased_multiply_logic_group = bpy.data.node_groups.get("Biased Multiply")
    if not biased_multiply_logic_group:
        biased_multiply_logic_group = bpy.data.node_groups.new(type="ShaderNodeTree", name="Biased Multiply")

        base_color_socket = biased_multiply_logic_group.interface.new_socket(name="Color", in_out='INPUT', socket_type="NodeSocketColor")
        detail_color_socket = biased_multiply_logic_group.interface.new_socket(name="Detail", in_out='INPUT', socket_type="NodeSocketColor")
        reflection_mask_socket = biased_multiply_logic_group.interface.new_socket(name="Mask", in_out='INPUT', socket_type="NodeSocketColor")
        input_node = biased_multiply_logic_group.nodes.new("NodeGroupInput")
        input_node.location = Vector((-1100, 0))

        base_color_socket.default_value = (0.5, 0.5, 0.5, 1)
        detail_color_socket.default_value = (0.0, 0.0, 0.0, 1)
        reflection_mask_socket.default_value = (0.0, 0.0, 0.0, 1)

        color_socket = biased_multiply_logic_group.interface.new_socket(name="Color", in_out='OUTPUT', socket_type="NodeSocketColor")
        output_node = biased_multiply_logic_group.nodes.new("NodeGroupOutput")
        output_node.location = Vector((0.0, 0.0))

        color_socket.default_value = (0, 0, 0, 0)

        mix_node = biased_multiply_logic_group.nodes.new("ShaderNodeMix")
        mix_node.data_type = 'RGBA'
        mix_node.blend_type = "MULTIPLY"
        mix_node.clamp_result = True
        mix_node.location = Vector((-850, -175))
        mix_node.inputs[0].default_value = 1

        connect_inputs(biased_multiply_logic_group, input_node, "Detail", mix_node, 6)
        connect_inputs(biased_multiply_logic_group, input_node, "Mask", mix_node, 7)

        base_seperate_node = biased_multiply_logic_group.nodes.new("ShaderNodeSeparateColor")
        base_seperate_node.location = Vector((-850, 175))
        connect_inputs(biased_multiply_logic_group, input_node, "Color", base_seperate_node, "Color")

        detail_seperate_node = biased_multiply_logic_group.nodes.new("ShaderNodeSeparateColor")
        detail_seperate_node.location = Vector((-600, -175))
        connect_inputs(biased_multiply_logic_group, mix_node, 2, detail_seperate_node, "Color")

        x_node = biased_multiply_logic_group.nodes.new("ShaderNodeValue")
        x_node.location = Vector((-850, 325))
        x_node.outputs[0].default_value = 2

        multiply_node_a_0 = biased_multiply_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_a_0.operation = 'MULTIPLY'
        multiply_node_a_0.use_clamp = True
        multiply_node_a_0.location = Vector((-600, 525))
        connect_inputs(biased_multiply_logic_group, base_seperate_node, "Red", multiply_node_a_0, 0)
        connect_inputs(biased_multiply_logic_group, x_node, "Value", multiply_node_a_0, 1)

        multiply_node_a_1 = biased_multiply_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_a_1.operation = 'MULTIPLY'
        multiply_node_a_1.use_clamp = True
        multiply_node_a_1.location = Vector((-600, 350))
        connect_inputs(biased_multiply_logic_group, base_seperate_node, "Green", multiply_node_a_1, 0)
        connect_inputs(biased_multiply_logic_group, x_node, "Value", multiply_node_a_1, 1)

        multiply_node_a_2 = biased_multiply_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_a_2.operation = 'MULTIPLY'
        multiply_node_a_2.use_clamp = True
        multiply_node_a_2.location = Vector((-600, 175))
        connect_inputs(biased_multiply_logic_group, base_seperate_node, "Blue", multiply_node_a_2, 0)
        connect_inputs(biased_multiply_logic_group, x_node, "Value", multiply_node_a_2, 1)

        multiply_node_b_0 = biased_multiply_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_b_0.operation = 'MULTIPLY'
        multiply_node_b_0.use_clamp = True
        multiply_node_b_0.location = Vector((-350, 175))
        connect_inputs(biased_multiply_logic_group, multiply_node_a_0, "Value", multiply_node_b_0, 0)
        connect_inputs(biased_multiply_logic_group, detail_seperate_node, "Red", multiply_node_b_0, 1)

        multiply_node_b_1 = biased_multiply_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_b_1.operation = 'MULTIPLY'
        multiply_node_b_1.use_clamp = True
        multiply_node_b_1.location = Vector((-350, 0))
        connect_inputs(biased_multiply_logic_group, multiply_node_a_1, "Value", multiply_node_b_1, 0)
        connect_inputs(biased_multiply_logic_group, detail_seperate_node, "Green", multiply_node_b_1, 1)

        multiply_node_b_2 = biased_multiply_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_b_2.operation = 'MULTIPLY'
        multiply_node_b_2.use_clamp = True
        multiply_node_b_2.location = Vector((-350, -175))
        connect_inputs(biased_multiply_logic_group, multiply_node_a_2, "Value", multiply_node_b_2, 0)
        connect_inputs(biased_multiply_logic_group, detail_seperate_node, "Blue", multiply_node_b_2, 1)

        combine_rgb_node = biased_multiply_logic_group.nodes.new("ShaderNodeCombineColor")
        combine_rgb_node.location = Vector((-175, 0))
        connect_inputs(biased_multiply_logic_group, multiply_node_b_0, "Value", combine_rgb_node, "Red")
        connect_inputs(biased_multiply_logic_group, multiply_node_b_1, "Value", combine_rgb_node, "Green")
        connect_inputs(biased_multiply_logic_group, multiply_node_b_2, "Value", combine_rgb_node, "Blue")
        connect_inputs(biased_multiply_logic_group, combine_rgb_node, "Color", output_node, "Color")

    biased_multiply_node = tree.nodes.new('ShaderNodeGroup')
    biased_multiply_node.node_tree = biased_multiply_logic_group

    return biased_multiply_node

def generate_multiply_node(tree):
    multiply_logic_group = bpy.data.node_groups.get("Multiply")
    if not multiply_logic_group:
        multiply_logic_group = bpy.data.node_groups.new(type="ShaderNodeTree", name="Multiply")

        base_color_socket = multiply_logic_group.interface.new_socket(name="Color", in_out='INPUT', socket_type="NodeSocketColor")
        detail_color_socket = multiply_logic_group.interface.new_socket(name="Detail", in_out='INPUT', socket_type="NodeSocketColor")
        reflection_mask_socket = multiply_logic_group.interface.new_socket(name="Mask", in_out='INPUT', socket_type="NodeSocketColor")
        input_node = multiply_logic_group.nodes.new("NodeGroupInput")
        input_node.location = Vector((-350, 0))

        base_color_socket.default_value = (1, 1, 1, 1)
        detail_color_socket.default_value = (1, 1, 1, 1)
        reflection_mask_socket.default_value = (1, 1, 1, 1)

        color_socket = multiply_logic_group.interface.new_socket(name="Color", in_out='OUTPUT', socket_type="NodeSocketColor")
        output_node = multiply_logic_group.nodes.new("NodeGroupOutput")
        output_node.location = Vector((0, 0))

        color_socket.default_value = (0, 0, 0, 0)

        mix_node_0 = multiply_logic_group.nodes.new("ShaderNodeMix")
        mix_node_0.data_type = 'RGBA'
        mix_node_0.blend_type = "MULTIPLY"
        mix_node_0.clamp_result = True
        mix_node_0.location = Vector((-175, 0))
        mix_node_0.inputs[0].default_value = 1
        connect_inputs(multiply_logic_group, input_node, "Color", mix_node_0, 6)
        connect_inputs(multiply_logic_group, input_node, "Detail", mix_node_0, 7)
        connect_inputs(multiply_logic_group, input_node, "Mask", mix_node_0, 0)
        connect_inputs(multiply_logic_group, mix_node_0, 2, output_node, "Color")

    multiply_node = tree.nodes.new('ShaderNodeGroup')
    multiply_node.node_tree = multiply_logic_group

    return multiply_node

def generate_biased_add_node(tree):
    biased_add_logic_group = bpy.data.node_groups.get("Biased Add")
    if not biased_add_logic_group:
        biased_add_logic_group = bpy.data.node_groups.new(type="ShaderNodeTree", name="Biased Add")

        base_color_socket = biased_add_logic_group.interface.new_socket(name="Color", in_out='INPUT', socket_type="NodeSocketColor")
        detail_color_socket = biased_add_logic_group.interface.new_socket(name="Detail", in_out='INPUT', socket_type="NodeSocketColor")
        reflection_mask_socket = biased_add_logic_group.interface.new_socket(name="Mask", in_out='INPUT', socket_type="NodeSocketColor")
        input_node = biased_add_logic_group.nodes.new("NodeGroupInput")
        input_node.location = Vector((-1100, 0))

        base_color_socket.default_value = (0.5, 0.5, 0.5, 1)
        detail_color_socket.default_value = (0.0, 0.0, 0.0, 1)
        reflection_mask_socket.default_value = (0.0, 0.0, 0.0, 1)

        color_socket = biased_add_logic_group.interface.new_socket(name="Color", in_out='OUTPUT', socket_type="NodeSocketColor")
        output_node = biased_add_logic_group.nodes.new("NodeGroupOutput")
        output_node.location = Vector((0.0, 0.0))

        color_socket.default_value = (0, 0, 0, 0)

        mix_node = biased_add_logic_group.nodes.new("ShaderNodeMix")
        mix_node.data_type = 'RGBA'
        mix_node.blend_type = "MULTIPLY"
        mix_node.clamp_result = True
        mix_node.location = Vector((-850, -175))
        mix_node.inputs[0].default_value = 1

        connect_inputs(biased_add_logic_group, input_node, "Detail", mix_node, 6)
        connect_inputs(biased_add_logic_group, input_node, "Mask", mix_node, 7)

        base_seperate_node = biased_add_logic_group.nodes.new("ShaderNodeSeparateColor")
        base_seperate_node.location = Vector((-850, 175))
        connect_inputs(biased_add_logic_group, input_node, "Color", base_seperate_node, "Color")

        detail_seperate_node = biased_add_logic_group.nodes.new("ShaderNodeSeparateColor")
        detail_seperate_node.location = Vector((-600, -175))
        connect_inputs(biased_add_logic_group, mix_node, 2, detail_seperate_node, "Color")

        x_node = biased_add_logic_group.nodes.new("ShaderNodeValue")
        x_node.location = Vector((-850, 325))
        x_node.outputs[0].default_value = 2

        multiply_node_a_0 = biased_add_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_a_0.operation = 'MULTIPLY'
        multiply_node_a_0.use_clamp = True
        multiply_node_a_0.location = Vector((-600, 525))
        connect_inputs(biased_add_logic_group, base_seperate_node, "Red", multiply_node_a_0, 0)
        connect_inputs(biased_add_logic_group, x_node, "Value", multiply_node_a_0, 1)

        multiply_node_a_1 = biased_add_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_a_1.operation = 'MULTIPLY'
        multiply_node_a_1.use_clamp = True
        multiply_node_a_1.location = Vector((-600, 350))
        connect_inputs(biased_add_logic_group, base_seperate_node, "Green", multiply_node_a_1, 0)
        connect_inputs(biased_add_logic_group, x_node, "Value", multiply_node_a_1, 1)

        multiply_node_a_2 = biased_add_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_a_2.operation = 'MULTIPLY'
        multiply_node_a_2.use_clamp = True
        multiply_node_a_2.location = Vector((-600, 175))
        connect_inputs(biased_add_logic_group, base_seperate_node, "Blue", multiply_node_a_2, 0)
        connect_inputs(biased_add_logic_group, x_node, "Value", multiply_node_a_2, 1)

        multiply_node_b_0 = biased_add_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_b_0.operation = 'ADD'
        multiply_node_b_0.use_clamp = True
        multiply_node_b_0.location = Vector((-350, 175))
        connect_inputs(biased_add_logic_group, multiply_node_a_0, "Value", multiply_node_b_0, 0)
        connect_inputs(biased_add_logic_group, detail_seperate_node, "Red", multiply_node_b_0, 1)

        multiply_node_b_1 = biased_add_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_b_1.operation = 'ADD'
        multiply_node_b_1.use_clamp = True
        multiply_node_b_1.location = Vector((-350, 0))
        connect_inputs(biased_add_logic_group, multiply_node_a_1, "Value", multiply_node_b_1, 0)
        connect_inputs(biased_add_logic_group, detail_seperate_node, "Green", multiply_node_b_1, 1)

        multiply_node_b_2 = biased_add_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_b_2.operation = 'ADD'
        multiply_node_b_2.use_clamp = True
        multiply_node_b_2.location = Vector((-350, -175))
        connect_inputs(biased_add_logic_group, multiply_node_a_2, "Value", multiply_node_b_2, 0)
        connect_inputs(biased_add_logic_group, detail_seperate_node, "Blue", multiply_node_b_2, 1)

        combine_rgb_node = biased_add_logic_group.nodes.new("ShaderNodeCombineColor")
        combine_rgb_node.location = Vector((-175, 0))
        connect_inputs(biased_add_logic_group, multiply_node_b_0, "Value", combine_rgb_node, "Red")
        connect_inputs(biased_add_logic_group, multiply_node_b_1, "Value", combine_rgb_node, "Green")
        connect_inputs(biased_add_logic_group, multiply_node_b_2, "Value", combine_rgb_node, "Blue")
        connect_inputs(biased_add_logic_group, combine_rgb_node, "Color", output_node, "Color")

    biased_add_node = tree.nodes.new('ShaderNodeGroup')
    biased_add_node.node_tree = biased_add_logic_group

    return biased_add_node

def generate_multipurpose_logic_node(tree):
    multipurpose_logic_group = bpy.data.node_groups.get("Multipurpose Logic")
    if not multipurpose_logic_group:
        multipurpose_logic_group = bpy.data.node_groups.new(type="ShaderNodeTree", name="Multipurpose Logic")

        xbox_socket = multipurpose_logic_group.interface.new_socket(name="Xbox", in_out='INPUT', socket_type="NodeSocketFloat")
        multipurpose_logic_group.interface.new_socket(name="RGB", in_out='INPUT', socket_type="NodeSocketVector")
        multipurpose_logic_group.interface.new_socket(name="A", in_out='INPUT', socket_type="NodeSocketFloat")
        input_node = multipurpose_logic_group.nodes.new("NodeGroupInput")
        input_node.location = Vector((-1250.0, 0))

        xbox_socket.default_value = 0.5
        xbox_socket.min_value = -10000.0
        xbox_socket.max_value = 10000.0

        multipurpose_logic_group.interface.new_socket(name="Reflective Mask", in_out='OUTPUT', socket_type="NodeSocketFloat")
        multipurpose_logic_group.interface.new_socket(name="Self Illumination", in_out='OUTPUT', socket_type="NodeSocketFloat")
        multipurpose_logic_group.interface.new_socket(name="Change Color", in_out='OUTPUT', socket_type="NodeSocketFloat")
        multipurpose_logic_group.interface.new_socket(name="Auxiliary", in_out='OUTPUT', socket_type="NodeSocketFloat")
        output_node = multipurpose_logic_group.nodes.new("NodeGroupOutput")
        output_node.location = Vector((0, 0))

        seperate_node = multipurpose_logic_group.nodes.new("ShaderNodeSeparateColor")
        seperate_node.location = Vector((-1000.0, 0))
        connect_inputs(multipurpose_logic_group, input_node, "RGB", seperate_node, "Color")

        greater_than_node = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        greater_than_node.operation = 'GREATER_THAN'
        greater_than_node.use_clamp = True
        greater_than_node.inputs[1].default_value = 0
        greater_than_node.location = Vector((-650.0, 300.0))
        connect_inputs(multipurpose_logic_group, input_node, "Xbox", greater_than_node, "Value")

        multiply_greater_node_0 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        multiply_greater_node_0.operation = 'MULTIPLY'
        multiply_greater_node_0.use_clamp = True
        multiply_greater_node_0.location = Vector((-425.0, 825.0))
        connect_inputs(multipurpose_logic_group, greater_than_node, "Value", multiply_greater_node_0, 0)
        connect_inputs(multipurpose_logic_group, seperate_node, "Red", multiply_greater_node_0, 1)

        multiply_greater_node_1 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        multiply_greater_node_1.operation = 'MULTIPLY'
        multiply_greater_node_1.use_clamp = True
        multiply_greater_node_1.location = Vector((-425.0, 650.0))
        connect_inputs(multipurpose_logic_group, greater_than_node, "Value", multiply_greater_node_1, 0)
        connect_inputs(multipurpose_logic_group, seperate_node, "Green", multiply_greater_node_1, 1)

        multiply_greater_node_2 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        multiply_greater_node_2.operation = 'MULTIPLY'
        multiply_greater_node_2.use_clamp = True
        multiply_greater_node_2.location = Vector((-425.0, 475.0))
        connect_inputs(multipurpose_logic_group, greater_than_node, "Value", multiply_greater_node_2, 0)
        connect_inputs(multipurpose_logic_group, seperate_node, "Blue", multiply_greater_node_2, 1)

        multiply_greater_node_3 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        multiply_greater_node_3.operation = 'MULTIPLY'
        multiply_greater_node_3.use_clamp = True
        multiply_greater_node_3.location = Vector((-425.0, 300.0))
        connect_inputs(multipurpose_logic_group, greater_than_node, "Value", multiply_greater_node_3, 0)
        connect_inputs(multipurpose_logic_group, input_node, "A", multiply_greater_node_3, 1)

        less_than_node = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        less_than_node.operation = 'LESS_THAN'
        less_than_node.use_clamp = True
        less_than_node.inputs[1].default_value = 1
        less_than_node.location = Vector((-650.0, -225.0))
        connect_inputs(multipurpose_logic_group, input_node, "Xbox", less_than_node, "Value")

        multiply_less_node_0 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        multiply_less_node_0.operation = 'MULTIPLY'
        multiply_less_node_0.use_clamp = True
        multiply_less_node_0.location = Vector((-425.0, -225))
        connect_inputs(multipurpose_logic_group, less_than_node, "Value", multiply_less_node_0, 0)
        connect_inputs(multipurpose_logic_group, input_node, "A", multiply_less_node_0, 1)

        multiply_less_node_1 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        multiply_less_node_1.operation = 'MULTIPLY'
        multiply_less_node_1.use_clamp = True
        multiply_less_node_1.location = Vector((-425.0, -400))
        connect_inputs(multipurpose_logic_group, less_than_node, "Value", multiply_less_node_1, 0)
        connect_inputs(multipurpose_logic_group, seperate_node, "Green", multiply_less_node_1, 1)

        multiply_less_node_2 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        multiply_less_node_2.operation = 'MULTIPLY'
        multiply_less_node_2.use_clamp = True
        multiply_less_node_2.location = Vector((-425.0, -575))
        connect_inputs(multipurpose_logic_group, less_than_node, "Value", multiply_less_node_2, 0)
        connect_inputs(multipurpose_logic_group, seperate_node, "Red", multiply_less_node_2, 1)

        multiply_less_node_3 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        multiply_less_node_3.operation = 'MULTIPLY'
        multiply_less_node_3.use_clamp = True
        multiply_less_node_3.location = Vector((-425.0, -750))
        connect_inputs(multipurpose_logic_group, less_than_node, "Value", multiply_less_node_3, 0)
        connect_inputs(multipurpose_logic_group, seperate_node, "Blue", multiply_less_node_3, 1)

        add_node_0 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        add_node_0.operation = 'ADD'
        add_node_0.use_clamp = True
        add_node_0.location = Vector((-200, 300))
        connect_inputs(multipurpose_logic_group, multiply_greater_node_0, "Value", add_node_0, 0)
        connect_inputs(multipurpose_logic_group, multiply_less_node_0, "Value", add_node_0, 1)

        add_node_1 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        add_node_1.operation = 'ADD'
        add_node_1.use_clamp = True
        add_node_1.location = Vector((-200, 125))
        connect_inputs(multipurpose_logic_group, multiply_greater_node_1, "Value", add_node_1, 0)
        connect_inputs(multipurpose_logic_group, multiply_less_node_1, "Value", add_node_1, 1)

        add_node_2 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        add_node_2.operation = 'ADD'
        add_node_2.use_clamp = True
        add_node_2.location = Vector((-200, -50))
        connect_inputs(multipurpose_logic_group, multiply_greater_node_2, "Value", add_node_2, 0)
        connect_inputs(multipurpose_logic_group, multiply_less_node_2, "Value", add_node_2, 1)

        add_node_3 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        add_node_3.operation = 'ADD'
        add_node_3.use_clamp = True
        add_node_3.location = Vector((-200, -225))
        connect_inputs(multipurpose_logic_group, multiply_greater_node_3, "Value", add_node_3, 0)
        connect_inputs(multipurpose_logic_group, multiply_less_node_3, "Value", add_node_3, 1)

        connect_inputs(multipurpose_logic_group, add_node_0, "Value", output_node, "Reflective Mask")
        connect_inputs(multipurpose_logic_group, add_node_1, "Value", output_node, "Self Illumination")
        connect_inputs(multipurpose_logic_group, add_node_2, "Value", output_node, "Change Color")
        connect_inputs(multipurpose_logic_group, add_node_3, "Value", output_node, "Auxiliary")

    mutipurpose_logic_node = tree.nodes.new('ShaderNodeGroup')
    mutipurpose_logic_node.node_tree = multipurpose_logic_group

    return mutipurpose_logic_node

def generate_reflection_tint_logic_node(tree):
    reflection_tint_logic_group = bpy.data.node_groups.get("Reflection Tint Logic")
    if not reflection_tint_logic_group:
        reflection_tint_logic_group = bpy.data.node_groups.new(type="ShaderNodeTree", name="Reflection Tint Logic")

        perpendicular_tint_socket = reflection_tint_logic_group.interface.new_socket(name="Perpendicular Tint", in_out='INPUT', socket_type="NodeSocketVector")
        reflection_tint_logic_group.interface.new_socket(name="Perpendicular Brightness", in_out='INPUT', socket_type="NodeSocketFloat")
        parallel_tint_socket = reflection_tint_logic_group.interface.new_socket(name="Parallel Tint", in_out='INPUT', socket_type="NodeSocketVector")
        reflection_tint_logic_group.interface.new_socket(name="Parallel Brightness", in_out='INPUT', socket_type="NodeSocketFloat")
        input_node = reflection_tint_logic_group.nodes.new("NodeGroupInput")
        input_node.location = Vector((-700, -200))

        perpendicular_tint_socket.min_value = -10000.0
        perpendicular_tint_socket.max_value = 10000.0

        parallel_tint_socket.min_value = -10000.0
        parallel_tint_socket.max_value = 10000.0

        reflection_tint_socket = reflection_tint_logic_group.interface.new_socket(name="Color", in_out='OUTPUT', socket_type="NodeSocketColor")
        reflection_tint_socket.default_value = (0, 0, 0, 0)

        output_node = reflection_tint_logic_group.nodes.new("NodeGroupOutput")
        output_node.location = Vector((0.0, 0.0))

        perpendicular_vect_math_node = reflection_tint_logic_group.nodes.new("ShaderNodeVectorMath")
        perpendicular_vect_math_node.operation = 'MULTIPLY'
        perpendicular_vect_math_node.location = Vector((-525, -125))
        connect_inputs(reflection_tint_logic_group, input_node, "Perpendicular Tint", perpendicular_vect_math_node, 0)
        connect_inputs(reflection_tint_logic_group, input_node, "Perpendicular Brightness", perpendicular_vect_math_node, 1)

        parallel_vect_math_node = reflection_tint_logic_group.nodes.new("ShaderNodeVectorMath")
        parallel_vect_math_node.operation = 'MULTIPLY'
        parallel_vect_math_node.location = Vector((-525, -275))
        connect_inputs(reflection_tint_logic_group, input_node, "Parallel Tint", parallel_vect_math_node, 0)
        connect_inputs(reflection_tint_logic_group, input_node, "Parallel Brightness", parallel_vect_math_node, 1)

        perpendicular_gamma_node = reflection_tint_logic_group.nodes.new('ShaderNodeGamma')
        perpendicular_gamma_node.inputs[1].default_value = 2.2
        perpendicular_gamma_node.location = Vector((-350, -125))
        connect_inputs(reflection_tint_logic_group, perpendicular_vect_math_node, "Vector", perpendicular_gamma_node, "Color")

        parallel_gamma_node = reflection_tint_logic_group.nodes.new('ShaderNodeGamma')
        parallel_gamma_node.inputs[1].default_value = 2.2
        parallel_gamma_node.location = Vector((-350, -275))
        connect_inputs(reflection_tint_logic_group, parallel_vect_math_node, "Vector", parallel_gamma_node, "Color")

        camera_data_node = reflection_tint_logic_group.nodes.new('ShaderNodeCameraData')
        dot_product_node = reflection_tint_logic_group.nodes.new('ShaderNodeVectorMath')
        dot_product_node.operation = 'DOT_PRODUCT'
        camera_data_node.location = Vector((-875, 125))
        dot_product_node.location = Vector((-700, 50))
        connect_inputs(reflection_tint_logic_group, camera_data_node, "View Vector", dot_product_node, 0)

        new_geometry_node = reflection_tint_logic_group.nodes.new('ShaderNodeNewGeometry')
        vector_transform_node = reflection_tint_logic_group.nodes.new('ShaderNodeVectorTransform')
        vector_transform_node.convert_to = 'CAMERA'
        new_geometry_node.location = Vector((-1050, 75))
        vector_transform_node.location = Vector((-875, 0))
        connect_inputs(reflection_tint_logic_group, new_geometry_node, "Normal", vector_transform_node, "Vector")
        connect_inputs(reflection_tint_logic_group, vector_transform_node, "Vector", dot_product_node, 1)

        absolute_node = reflection_tint_logic_group.nodes.new('ShaderNodeMath')
        absolute_node.operation = 'ABSOLUTE'
        absolute_node.use_clamp = True
        absolute_node.location = Vector((-525, 50))
        connect_inputs(reflection_tint_logic_group, dot_product_node, "Value", absolute_node, "Value")

        camera_gamma_node = reflection_tint_logic_group.nodes.new('ShaderNodeGamma')
        camera_gamma_node.inputs[1].default_value = 2.2
        camera_gamma_node.location = Vector((-350, 50))
        connect_inputs(reflection_tint_logic_group, absolute_node, "Value", camera_gamma_node, "Color")

        mix_node = reflection_tint_logic_group.nodes.new("ShaderNodeMix")
        mix_node.data_type = 'RGBA'
        mix_node.blend_type = "MIX"
        mix_node.clamp_result = True
        mix_node.location = Vector((-175, 0))
        connect_inputs(reflection_tint_logic_group, camera_gamma_node, "Color", mix_node, 0)
        connect_inputs(reflection_tint_logic_group, parallel_gamma_node, "Color", mix_node, 6)
        connect_inputs(reflection_tint_logic_group, perpendicular_gamma_node, "Color", mix_node, 7)
        connect_inputs(reflection_tint_logic_group, mix_node, 2, output_node, "Color")

    reflection_tint_node = tree.nodes.new('ShaderNodeGroup')
    reflection_tint_node.node_tree = reflection_tint_logic_group

    return reflection_tint_node

def generate_detail_logic_node(tree, shader):
    detail_logic_group = bpy.data.node_groups.get("Detail Logic")
    if not detail_logic_group:
        detail_logic_group = bpy.data.node_groups.new(type="ShaderNodeTree", name="Detail Logic")

        detail_after_reflection_socket = detail_logic_group.interface.new_socket(name="Detail After Reflection", in_out='INPUT', socket_type="NodeSocketFloat")
        reflection_color_socket = detail_logic_group.interface.new_socket(name="Reflection Color", in_out='INPUT', socket_type="NodeSocketColor")
        detail_socket = detail_logic_group.interface.new_socket(name="Detail", in_out='INPUT', socket_type="NodeSocketColor")
        mask_socket = detail_logic_group.interface.new_socket(name="Mask", in_out='INPUT', socket_type="NodeSocketColor")
        base_color_socket = detail_logic_group.interface.new_socket(name="Base Color", in_out='INPUT', socket_type="NodeSocketColor")
        reflection_only_socket = detail_logic_group.interface.new_socket(name="Reflection Only", in_out='INPUT', socket_type="NodeSocketColor")
        reflection_mask_socket = detail_logic_group.interface.new_socket(name="Reflection Mask", in_out='INPUT', socket_type="NodeSocketColor")
        input_node = detail_logic_group.nodes.new("NodeGroupInput")
        input_node.location = Vector((-1500.0, 0.0))

        detail_after_reflection_socket.default_value = 0.5
        detail_after_reflection_socket.min_value = -10000.0
        detail_after_reflection_socket.max_value = 10000.0

        detail_after_reflection_socket.default_value = 0.5
        reflection_color_socket.default_value = (0.5, 0.5, 0.5, 1)
        detail_socket.default_value = (0.5, 0.5, 0.5, 1)
        mask_socket.default_value = (0.5, 0.5, 0.5, 1)
        base_color_socket.default_value = (0.5, 0.5, 0.5, 1)
        reflection_only_socket.default_value = (0.0, 0.0, 0.0, 1)
        reflection_mask_socket.default_value = (0.0, 0.0, 0.0, 1)

        color_socket = detail_logic_group.interface.new_socket(name="Color", in_out='OUTPUT', socket_type="NodeSocketColor")
        color_socket.default_value = (0, 0, 0, 0)
        output_node = detail_logic_group.nodes.new("NodeGroupOutput")
        output_node.location = Vector((0, 0))

        detail_before_function_node = None
        if shader.detail_function == DetailFumctionEnum.double_biased_multiply.value:
            detail_before_function_node = generate_biased_multiply_node(detail_logic_group)
        elif shader.detail_function == DetailFumctionEnum.multiply.value:
            detail_before_function_node = generate_multiply_node(detail_logic_group)
        elif shader.detail_function == DetailFumctionEnum.double_biased_add.value:
            detail_before_function_node = generate_biased_add_node(detail_logic_group)

        detail_before_function_node.location = Vector((-1250.0, -400.0))
        connect_inputs(detail_logic_group, input_node, "Detail", detail_before_function_node, "Detail")
        connect_inputs(detail_logic_group, input_node, "Mask", detail_before_function_node, "Mask")
        connect_inputs(detail_logic_group, input_node, "Base Color", detail_before_function_node, "Color")

        reflection_before_mix_node = detail_logic_group.nodes.new("ShaderNodeMix")
        reflection_before_mix_node.data_type = 'RGBA'
        reflection_before_mix_node.blend_type = "ADD"
        reflection_before_mix_node.clamp_result = True
        reflection_before_mix_node.location = Vector((-1050.0, -150.0))
        connect_inputs(detail_logic_group, input_node, "Reflection Mask", reflection_before_mix_node, 0)
        connect_inputs(detail_logic_group, detail_before_function_node, "Color", reflection_before_mix_node, 6)
        connect_inputs(detail_logic_group, input_node, "Reflection Only", reflection_before_mix_node, 7)

        before_less_than_node = detail_logic_group.nodes.new("ShaderNodeMath")
        before_less_than_node.operation = 'LESS_THAN'
        before_less_than_node.use_clamp = True
        before_less_than_node.inputs[1].default_value = 1
        before_less_than_node.location = Vector((-850.0, -225.0))
        connect_inputs(detail_logic_group, input_node, "Detail After Reflection", before_less_than_node, "Value")

        detail_seperate_before_node = detail_logic_group.nodes.new("ShaderNodeSeparateColor")
        detail_seperate_before_node.location = Vector((-850.0, -400.0))
        connect_inputs(detail_logic_group, reflection_before_mix_node, 2, detail_seperate_before_node, "Color")

        detail_multiply_node_before_0 = detail_logic_group.nodes.new("ShaderNodeMath")
        detail_multiply_node_before_0.operation = 'MULTIPLY'
        detail_multiply_node_before_0.use_clamp = True
        detail_multiply_node_before_0.location = Vector((-600.0, -175.0))
        connect_inputs(detail_logic_group, before_less_than_node, "Value", detail_multiply_node_before_0, 0)
        connect_inputs(detail_logic_group, detail_seperate_before_node, "Red", detail_multiply_node_before_0, 1)

        detail_multiply_node_before_1 = detail_logic_group.nodes.new("ShaderNodeMath")
        detail_multiply_node_before_1.operation = 'MULTIPLY'
        detail_multiply_node_before_1.use_clamp = True
        detail_multiply_node_before_1.location = Vector((-600.0, -350.0))
        connect_inputs(detail_logic_group, before_less_than_node, "Value", detail_multiply_node_before_1, 0)
        connect_inputs(detail_logic_group, detail_seperate_before_node, "Green", detail_multiply_node_before_1, 1)

        detail_multiply_node_before_2 = detail_logic_group.nodes.new("ShaderNodeMath")
        detail_multiply_node_before_2.operation = 'MULTIPLY'
        detail_multiply_node_before_2.use_clamp = True
        detail_multiply_node_before_2.location = Vector((-600.0, -525.0))
        connect_inputs(detail_logic_group, before_less_than_node, "Value", detail_multiply_node_before_2, 0)
        connect_inputs(detail_logic_group, detail_seperate_before_node, "Blue", detail_multiply_node_before_2, 1)

        detail_after_function_node = None
        if shader.detail_function == DetailFumctionEnum.double_biased_multiply.value:
            detail_after_function_node = generate_biased_multiply_node(detail_logic_group)
        elif shader.detail_function == DetailFumctionEnum.multiply.value:
            detail_after_function_node = generate_multiply_node(detail_logic_group)
        elif shader.detail_function == DetailFumctionEnum.double_biased_add.value:
            detail_after_function_node = generate_biased_add_node(detail_logic_group)

        detail_after_function_node.location = Vector((-1025, 225))
        connect_inputs(detail_logic_group, input_node, "Detail", detail_after_function_node, "Detail")
        connect_inputs(detail_logic_group, input_node, "Mask", detail_after_function_node, "Mask")
        connect_inputs(detail_logic_group, input_node, "Reflection Color", detail_after_function_node, "Color")

        after_greater_than_node = detail_logic_group.nodes.new("ShaderNodeMath")
        after_greater_than_node.operation = 'GREATER_THAN'
        after_greater_than_node.use_clamp = True
        after_greater_than_node.inputs[1].default_value = 0
        after_greater_than_node.location = Vector((-850, 400))
        connect_inputs(detail_logic_group, input_node, "Detail After Reflection", after_greater_than_node, "Value")

        detail_seperate_after_node = detail_logic_group.nodes.new("ShaderNodeSeparateColor")
        detail_seperate_after_node.location = Vector((-850, 225))
        connect_inputs(detail_logic_group, detail_after_function_node, "Color", detail_seperate_after_node, "Color")

        detail_multiply_node_after_0 = detail_logic_group.nodes.new("ShaderNodeMath")
        detail_multiply_node_after_0.operation = 'MULTIPLY'
        detail_multiply_node_after_0.use_clamp = True
        detail_multiply_node_after_0.location = Vector((-600, 525))
        connect_inputs(detail_logic_group, after_greater_than_node, "Value", detail_multiply_node_after_0, 0)
        connect_inputs(detail_logic_group, detail_seperate_after_node, "Red", detail_multiply_node_after_0, 1)

        detail_multiply_node_after_1 = detail_logic_group.nodes.new("ShaderNodeMath")
        detail_multiply_node_after_1.operation = 'MULTIPLY'
        detail_multiply_node_after_1.use_clamp = True
        detail_multiply_node_after_1.location = Vector((-600, 350))
        connect_inputs(detail_logic_group, after_greater_than_node, "Value", detail_multiply_node_after_1, 0)
        connect_inputs(detail_logic_group, detail_seperate_after_node, "Green", detail_multiply_node_after_1, 1)

        detail_multiply_node_after_2 = detail_logic_group.nodes.new("ShaderNodeMath")
        detail_multiply_node_after_2.operation = 'MULTIPLY'
        detail_multiply_node_after_2.use_clamp = True
        detail_multiply_node_after_2.location = Vector((-600, 175))
        connect_inputs(detail_logic_group, after_greater_than_node, "Value", detail_multiply_node_after_2, 0)
        connect_inputs(detail_logic_group, detail_seperate_after_node, "Blue", detail_multiply_node_after_2, 1)

        detail_add_node_0 = detail_logic_group.nodes.new("ShaderNodeMath")
        detail_add_node_0.operation = 'ADD'
        detail_add_node_0.use_clamp = True
        detail_add_node_0.location = Vector((-350, 175))
        connect_inputs(detail_logic_group, detail_multiply_node_after_0, "Value", detail_add_node_0, 0)
        connect_inputs(detail_logic_group, detail_multiply_node_before_0, "Value", detail_add_node_0, 1)

        detail_add_node_1 = detail_logic_group.nodes.new("ShaderNodeMath")
        detail_add_node_1.operation = 'ADD'
        detail_add_node_1.use_clamp = True
        detail_add_node_1.location = Vector((-350, 0))
        connect_inputs(detail_logic_group, detail_multiply_node_after_1, "Value", detail_add_node_1, 0)
        connect_inputs(detail_logic_group, detail_multiply_node_before_1, "Value", detail_add_node_1, 1)

        detail_add_node_2 = detail_logic_group.nodes.new("ShaderNodeMath")
        detail_add_node_2.operation = 'ADD'
        detail_add_node_2.use_clamp = True
        detail_add_node_2.location = Vector((-350, -175))
        connect_inputs(detail_logic_group, detail_multiply_node_after_2, "Value", detail_add_node_2, 0)
        connect_inputs(detail_logic_group, detail_multiply_node_before_2, "Value", detail_add_node_2, 1)

        combine_rgb_node = detail_logic_group.nodes.new("ShaderNodeCombineColor")
        combine_rgb_node.location = Vector((-175, 0))
        connect_inputs(detail_logic_group, detail_add_node_0, "Value", combine_rgb_node, "Red")
        connect_inputs(detail_logic_group, detail_add_node_1, "Value", combine_rgb_node, "Green")
        connect_inputs(detail_logic_group, detail_add_node_2, "Value", combine_rgb_node, "Blue")
        connect_inputs(detail_logic_group, combine_rgb_node, "Color", output_node, "Color")

    detail_logic_node = tree.nodes.new('ShaderNodeGroup')
    detail_logic_node.node_tree = detail_logic_group

    return detail_logic_node

def add_shader_group(shader_name):
    if not bpy.data.node_groups.get(shader_name):
        with bpy.data.libraries.load(HALO_2_SHADER_RESOURCES) as (data_from, data_to):
            if shader_name in data_from.node_groups:
                data_to.node_groups.append(data_from.node_groups[data_from.node_groups.index(shader_name)])

def is_group_valid(shader_name):
    found_group = False
    with bpy.data.libraries.load(HALO_2_SHADER_RESOURCES) as (data_from, data_to):
        if shader_name in data_from.node_groups:
            found_group = True

    return found_group

def get_shader_node(tree, shader_name):
    shader_node = None
    add_shader_group(shader_name)

    template_node = bpy.data.node_groups.get(shader_name)
    if template_node:
        shader_node = tree.nodes.new('ShaderNodeGroup')
        shader_node.node_tree = template_node
        shader_node.name = shader_name.replace('_', ' ').title()

    return shader_node

def get_fallback_shader_node(tree, shader_name):
    shader_node = None
    node_group = None
    node_group_hits_list = []

    with bpy.data.libraries.load(HALO_2_SHADER_RESOURCES) as (data_from, data_to):
        features = shader_name.split("_")
        for lib_node_group in data_from.node_groups:
            hits = 0
            for feature in features:
                if feature in lib_node_group:
                    hits += 1

            node_group_hits_list.append(hits)

        node_group_index = node_group_hits_list.index(max(node_group_hits_list))
        node_group_match = data_from.node_groups[node_group_index]

        node_group = node_group_match
        if not node_group_match in bpy.data.node_groups:
            data_to.node_groups.append(node_group_match)

    if node_group:
        shader_node = tree.nodes.new("ShaderNodeGroup")
        shader_node.node_tree = bpy.data.node_groups[node_group]

    return shader_node


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
