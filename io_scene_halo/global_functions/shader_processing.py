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

from .. import config
from PIL import Image
from mathutils import Vector
from ..file_tag.h1.file_shader_environment.format import EnvironmentTypeEnum, EnvironmentFlags, DiffuseFlags, ReflectionFlags
from ..file_tag.h1.file_shader_model.format import ModelFlags, DetailFumctionEnum, DetailMaskEnum, FunctionEnum
from ..file_tag.h1.file_bitmap.format import FormatEnum

def get_bitmap(tag_ref, texture_root):
    texture_extensions = ("tif", "tiff")
    texture_path = None
    bitmap_name = "White"
    if tag_ref.name_length > 0:
        bitmap_name = os.path.basename(tag_ref.name)
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

def generate_image_node(mat, texture, BITMAP=None, bitmap_name="White", is_env=False):
    if is_env:
        image_node = mat.node_tree.nodes.new("ShaderNodeTexEnvironment")
    else:
        image_node = mat.node_tree.nodes.new("ShaderNodeTexImage")

    if BITMAP and BITMAP.bitmap_body.compressed_color_plate_data.size > 0:
        image = bpy.data.images.get(bitmap_name)
        if not image:
            x = BITMAP.bitmap_body.color_plate_width
            y = BITMAP.bitmap_body.color_plate_height
            
            image = bpy.data.images.new(bitmap_name, x, y)
            decompressed_data = zlib.decompress(BITMAP.bitmap_body.compressed_color_plate)
            pil_image = Image.frombytes("RGBA", (x, y), decompressed_data, 'raw', "BGRA").transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)
            normalized = 1.0 / 255.0
            image.pixels[:] = (np.asarray(pil_image.convert('RGBA'),dtype=np.float32) * normalized).ravel()
            image.pack()

        image_node.image = image

    else:
        if not texture == None:
            print("No color plate found. Loading texture found in data directory.")
            image = bpy.data.images.load(texture, check_existing=True)
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
        if shader.shader_body.detail_function == DetailFumctionEnum.double_biased_multiply.value:
            detail_before_function_node = generate_biased_multiply_node(detail_logic_group)
        elif shader.shader_body.detail_function == DetailFumctionEnum.multiply.value:
            detail_before_function_node = generate_multiply_node(detail_logic_group)
        elif shader.shader_body.detail_function == DetailFumctionEnum.double_biased_add.value:
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
        if shader.shader_body.detail_function == DetailFumctionEnum.double_biased_multiply.value:
            detail_after_function_node = generate_biased_multiply_node(detail_logic_group)
        elif shader.shader_body.detail_function == DetailFumctionEnum.multiply.value:
            detail_after_function_node = generate_multiply_node(detail_logic_group)
        elif shader.shader_body.detail_function == DetailFumctionEnum.double_biased_add.value:
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

def generate_shader_environment_simple(mat, shader, permutation_index, report):
    mat.use_nodes = True

    texture_root = config.HALO_1_DATA_PATH
    base_map, base_bitmap_name = get_bitmap(shader.shader_body.base_map, texture_root)
    base_bitmap = shader.shader_body.base_map.parse_tag(report, "halo1", "retail")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    base_node = generate_image_node(mat, base_map, base_bitmap, base_bitmap_name)
    base_node.name = "Base Map"
    base_node.location = Vector((-2100, 475))
    if not base_node.image == None:
        base_node.image.alpha_mode = 'CHANNEL_PACKED'

    alpha_shader = EnvironmentFlags.alpha_tested in EnvironmentFlags(shader.shader_body.environment_flags)
    if alpha_shader:
        mat.shadow_method = 'CLIP'
        mat.blend_method = 'CLIP'

    mat.use_backface_culling = True

    connect_inputs(mat.node_tree, base_node, "Color", bdsf_principled, "Base Color")

def generate_shader_model_simple(mat, shader, report):
    mat.use_nodes = True

    texture_root = config.HALO_1_DATA_PATH
    base_map, base_map_name = get_bitmap(shader.shader_body.base_map, texture_root)
    base_bitmap = shader.shader_body.base_map.parse_tag(report, "halo1", "retail")

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
    shader_model_flags = ModelFlags(shader.shader_body.model_flags)
    if base_bitmap:
        ignore_alpha_bitmap = base_bitmap.bitmap_body.format is FormatEnum.compressed_with_color_key_transparency.value
        ignore_alpha_shader = ModelFlags.not_alpha_tested in shader_model_flags
        if ignore_alpha_shader or ignore_alpha_bitmap:
            base_node.image.alpha_mode = 'NONE'
        else:
            connect_inputs(mat.node_tree, base_node, "Alpha", bdsf_principled, "Alpha")
            mat.shadow_method = 'CLIP'
            mat.blend_method = 'CLIP'

    mat.use_backface_culling = False
    if not ModelFlags.two_sided in shader_model_flags:
        mat.use_backface_culling = True

    connect_inputs(mat.node_tree, base_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_chicago_simple(mat, shader, report):
    mat.use_nodes = True

    texture_root = config.HALO_1_DATA_PATH
    first_map = None
    first_map_bitmap = None
    first_map_name = "White"
    if len(shader.maps) > 0:
        first_map, first_map_name = get_bitmap(shader.maps[0].map, texture_root)
        first_map_bitmap = shader.maps[0].map.parse_tag(report, "halo1", "retail")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    first_map_node = generate_image_node(mat, first_map, first_map_bitmap, first_map_name)

    connect_inputs(mat.node_tree, first_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_chicago_extended_simple(mat, shader, report):
    mat.use_nodes = True

    texture_root = config.HALO_1_DATA_PATH
    first_map = None
    first_map_bitmap = None
    first_map_name = "White"
    if len(shader._4_stage_maps) > 0:
        first_map, first_map_name = get_bitmap(shader._4_stage_maps[0].map, texture_root)
        first_map_bitmap = shader._4_stage_maps[0].map.parse_tag(report, "halo1", "retail")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    first_map_node = generate_image_node(mat, first_map, first_map_bitmap, first_map_name)

    connect_inputs(mat.node_tree, first_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_generic_simple(mat, shader, report):
    mat.use_nodes = True

    texture_root = config.HALO_1_DATA_PATH
    first_map = None
    first_map_bitmap = None
    first_map_name = "White"
    if len(shader.maps) > 0:
        first_map, first_map_name = get_bitmap(shader.maps[0].map, texture_root)
        first_map_bitmap = shader.maps[0].map.parse_tag(report, "halo1", "retail")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    first_map_node = generate_image_node(mat, first_map, first_map_bitmap, first_map_name)

    connect_inputs(mat.node_tree, first_map_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_glass_simple(mat, shader, report):
    mat.use_nodes = True

    texture_root = config.HALO_1_DATA_PATH
    diffuse_map, diffuse_map_name = get_bitmap(shader.shader_body.diffuse_map, texture_root)
    diffuse_bitmap = shader.shader_body.diffuse_map.parse_tag(report, "halo1", "retail")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    diffuse_node = generate_image_node(mat, diffuse_map, diffuse_bitmap, diffuse_map_name)

    diffuse_node.location = Vector((-1600, 500))

    connect_inputs(mat.node_tree, diffuse_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_meter_simple(mat, shader, report):
    mat.use_nodes = True

    texture_root = config.HALO_1_DATA_PATH
    meter_map, meter_map_name = get_bitmap(shader.shader_body.meter_map, texture_root)
    meter_bitmap = shader.shader_body.meter_map.parse_tag(report, "halo1", "retail")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    meter_node = generate_image_node(mat, meter_map, meter_bitmap, meter_map_name)

    meter_node.location = Vector((-1600, 500))

    connect_inputs(mat.node_tree, meter_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_plasma_simple(mat, shader, report):
    mat.use_nodes = True

    texture_root = config.HALO_1_DATA_PATH
    primary_noise_map, primary_noise_map_name = get_bitmap(shader.shader_body.primary_noise_map, texture_root)
    primary_noise_bitmap = shader.shader_body.primary_noise_map.parse_tag(report, "halo1", "retail")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    primary_noise_node = generate_image_node(mat, primary_noise_map, primary_noise_bitmap, primary_noise_map_name)

    connect_inputs(mat.node_tree, primary_noise_node, "Color", bdsf_principled, "Base Color")

def generate_shader_transparent_water_simple(mat, shader, report):
    mat.use_nodes = True

    texture_root = config.HALO_1_DATA_PATH
    base_map, base_map_name = get_bitmap(shader.shader_body.base_map, texture_root)
    base_bitmap = shader.shader_body.base_map.parse_tag(report, "halo1", "retail")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    base_node = generate_image_node(mat, base_map, base_bitmap, base_map_name)

    connect_inputs(mat.node_tree, base_node, "Color", bdsf_principled, "Base Color")

def generate_shader_model(mat, shader, report):
    mat.use_nodes = True

    texture_root = config.HALO_1_DATA_PATH
    base_map, base_map_name = get_bitmap(shader.shader_body.base_map, texture_root)
    multipurpose_map, multipurpose_map_name = get_bitmap(shader.shader_body.multipurpose_map, texture_root)
    detail_map, detail_map_name = get_bitmap(shader.shader_body.detail_map, texture_root)
    reflection_map, reflection_map_name = get_bitmap(shader.shader_body.reflection_cube_map, texture_root)

    base_bitmap = shader.shader_body.base_map.parse_tag(report, "halo1", "retail")
    multipurpose_bitmap = shader.shader_body.multipurpose_map.parse_tag(report, "halo1", "retail")
    detail_bitmap = shader.shader_body.detail_map.parse_tag(report, "halo1", "retail")
    reflection_bitmap = shader.shader_body.reflection_cube_map.parse_tag(report, "halo1", "retail")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    bdsf_principled.inputs[7].default_value = 0
    bdsf_principled.inputs[9].default_value = 1

    base_node = generate_image_node(mat, base_map, base_bitmap, base_map_name)
    if not base_node.image == None:
        base_node.image.alpha_mode = 'CHANNEL_PACKED'

    base_node.location = Vector((-1600, 500))
    shader_model_flags = ModelFlags(shader.shader_body.model_flags)
    if base_bitmap:
        ignore_alpha_bitmap = base_bitmap.bitmap_body.format is FormatEnum.compressed_with_color_key_transparency.value
        ignore_alpha_shader = ModelFlags.not_alpha_tested in shader_model_flags
        if ignore_alpha_shader or ignore_alpha_bitmap:
            base_node.image.alpha_mode = 'NONE'
        else:
            connect_inputs(mat.node_tree, base_node, "Alpha", bdsf_principled, "Alpha")
            mat.shadow_method = 'CLIP'
            mat.blend_method = 'CLIP'

    mat.use_backface_culling = False
    if not ModelFlags.two_sided in shader_model_flags:
        mat.use_backface_culling = True

    multipurpose_node = generate_image_node(mat, multipurpose_map, multipurpose_bitmap, multipurpose_map_name)
    multipurpose_node.location = Vector((-1600, 200))
    if not multipurpose_node.image == None:
        multipurpose_node.image.alpha_mode = 'CHANNEL_PACKED'
        multipurpose_node.image.colorspace_settings.name = 'Non-Color'

    multipurpose_node.interpolation = 'Cubic'

    detail_node = generate_image_node(mat, detail_map, detail_bitmap, detail_map_name)
    if not detail_node.image == None:
        detail_node.image.alpha_mode = 'CHANNEL_PACKED'

    detail_node.location = Vector((-1600, -100))

    reflection_node = generate_image_node(mat, reflection_map, reflection_bitmap, reflection_map_name, True)
    reflection_node.location = Vector((-1600.0, 750.0))
    texture_coordinate_node = mat.node_tree.nodes.new("ShaderNodeTexCoord")
    texture_coordinate_node.location = Vector((-1775.0, 750.0))
    connect_inputs(mat.node_tree, texture_coordinate_node, "Reflection", reflection_node, "Vector")
    
    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-1775, 250))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", base_node, "Vector")
    connect_inputs(mat.node_tree, vect_math_node, "Vector", multipurpose_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-1950, 275))
    combine_xyz_node.location = Vector((-1950, 150))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    map_u_scale = shader.shader_body.map_u_scale
    if shader.shader_body.map_u_scale == 0.0:
        map_u_scale = 1.0

    map_v_scale = shader.shader_body.map_v_scale
    if shader.shader_body.map_v_scale == 0.0:
        map_v_scale = 1.0

    combine_xyz_node.inputs[0].default_value = map_u_scale
    combine_xyz_node.inputs[1].default_value = map_v_scale
    combine_xyz_node.inputs[2].default_value = 1

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-1775, -200))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", detail_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-1950, -175))
    combine_xyz_node.location = Vector((-1950, -300))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)
    detail_map_scale = shader.shader_body.detail_map_scale
    if shader.shader_body.detail_map_scale == 0.0:
        detail_map_scale = 1.0

    combine_xyz_node.inputs[0].default_value = detail_map_scale
    combine_xyz_node.inputs[1].default_value = detail_map_scale + shader.shader_body.detail_map_v_scale
    combine_xyz_node.inputs[2].default_value = 1

    mutipurpose_logic_node = generate_multipurpose_logic_node(mat.node_tree)
    mutipurpose_logic_node.location = Vector((-1125, -240.0))
    is_xbox = 0
    if ModelFlags.multipurpose_map_uses_og_xbox_channel_order in ModelFlags(shader.shader_body.model_flags):
        is_xbox = 1

    mutipurpose_logic_node.inputs[0].default_value = is_xbox
    connect_inputs(mat.node_tree, multipurpose_node, "Color", mutipurpose_logic_node, "RGB")
    connect_inputs(mat.node_tree, multipurpose_node, "Alpha", mutipurpose_logic_node, "A")
    connect_inputs(mat.node_tree, mutipurpose_logic_node, "Self Illumination", bdsf_principled, "Emission Strength")

    reflection_tint_node = generate_reflection_tint_logic_node(mat.node_tree)
    reflection_tint_node.location = Vector((-1125, -475.0))

    perpendicular_tint_node = mat.node_tree.nodes.new('ShaderNodeRGB')
    perpendicular_tint_node.outputs[0].default_value = shader.shader_body.perpendicular_tint_color
    perpendicular_tint_node.location = Vector((-1300, -525.0))
    connect_inputs(mat.node_tree, perpendicular_tint_node, "Color", reflection_tint_node, "Perpendicular Tint")
    reflection_tint_node.inputs["Perpendicular Brightness"].default_value = shader.shader_body.perpendicular_brightness

    parallel_tint_node = mat.node_tree.nodes.new('ShaderNodeRGB')
    parallel_tint_node.outputs[0].default_value = shader.shader_body.parallel_tint_color
    parallel_tint_node.location = Vector((-1300, -725.0))
    connect_inputs(mat.node_tree, parallel_tint_node, "Color", reflection_tint_node, "Parallel Tint")
    reflection_tint_node.inputs["Parallel Brightness"].default_value = shader.shader_body.parallel_brightness

    reflection_mix_node = mat.node_tree.nodes.new("ShaderNodeMix")
    reflection_mix_node.data_type = 'RGBA'
    reflection_mix_node.blend_type = "MULTIPLY"
    reflection_mix_node.clamp_result = True
    reflection_mix_node.inputs[0].default_value = 1
    reflection_mix_node.location = Vector((-950, -240.0))
    connect_inputs(mat.node_tree, reflection_tint_node, "Color", reflection_mix_node, 6)
    connect_inputs(mat.node_tree, reflection_node, "Color", reflection_mix_node, 7)

    multipurpose_mix_node = mat.node_tree.nodes.new("ShaderNodeMix")
    multipurpose_mix_node.data_type = 'RGBA'
    multipurpose_mix_node.blend_type = "MULTIPLY"
    multipurpose_mix_node.clamp_result = True
    multipurpose_mix_node.inputs[0].default_value = 1
    multipurpose_mix_node.location = Vector((-775.0, -240.0))
    connect_inputs(mat.node_tree, mutipurpose_logic_node, "Reflective Mask", multipurpose_mix_node, 6)
    connect_inputs(mat.node_tree, reflection_mix_node, 2, multipurpose_mix_node, 7)

    diffuse_mix_node = mat.node_tree.nodes.new("ShaderNodeMix")
    diffuse_mix_node.data_type = 'RGBA'
    diffuse_mix_node.blend_type = "ADD"
    diffuse_mix_node.clamp_result = True
    diffuse_mix_node.inputs[0].default_value = 1
    diffuse_mix_node.location = Vector((-600.0, -240.0))
    connect_inputs(mat.node_tree, base_node, "Color", diffuse_mix_node, 6)
    connect_inputs(mat.node_tree, multipurpose_mix_node, 2, diffuse_mix_node, 7)

    detail_logic_node = generate_detail_logic_node(mat.node_tree, shader)
    detail_logic_node.location = Vector((-425.0, 0.0))
    detail_logic_node.inputs[3].default_value = (1, 1, 1, 1)
    detail_after_reflections = 0
    if ModelFlags.detail_after_reflections in ModelFlags(shader.shader_body.model_flags):
        connect_inputs(mat.node_tree, mutipurpose_logic_node, "Reflective Mask", detail_logic_node, "Mask")
        detail_after_reflections = 1

    detail_logic_node.inputs[0].default_value = detail_after_reflections
    connect_inputs(mat.node_tree, diffuse_mix_node, 2, detail_logic_node, "Reflection Color")
    connect_inputs(mat.node_tree, detail_node, "Color", detail_logic_node, "Detail")
    connect_inputs(mat.node_tree, base_node, "Color", detail_logic_node, "Base Color")
    connect_inputs(mat.node_tree, reflection_mix_node, 2, detail_logic_node, "Reflection Only")
    connect_inputs(mat.node_tree, mutipurpose_logic_node, "Reflective Mask", detail_logic_node, "Reflection Mask")
    connect_inputs(mat.node_tree, detail_logic_node, "Color", bdsf_principled, "Base Color")

    animation_color_lower_bound_node = mat.node_tree.nodes.new('ShaderNodeRGB')
    animation_color_lower_bound_node.outputs[0].default_value = shader.shader_body.self_illumination_animation_color_lower_bound
    animation_color_lower_bound_node.location = Vector((-775, -550))

    animation_color_upper_bound_node = mat.node_tree.nodes.new('ShaderNodeRGB')
    animation_color_upper_bound_node.outputs[0].default_value = shader.shader_body.self_illumination_animation_color_upper_bound
    animation_color_upper_bound_node.location = Vector((-775, -750))

    animation_color_lower_bound_gamma_node = mat.node_tree.nodes.new('ShaderNodeGamma')
    animation_color_lower_bound_gamma_node.inputs[1].default_value = 2.2
    animation_color_lower_bound_gamma_node.location = Vector((-600, -600))
    connect_inputs(mat.node_tree, animation_color_lower_bound_node, "Color", animation_color_lower_bound_gamma_node, "Color")

    animation_color_upper_bound_gamma_node = mat.node_tree.nodes.new('ShaderNodeGamma')
    animation_color_upper_bound_gamma_node.inputs[1].default_value = 2.2
    animation_color_upper_bound_gamma_node.location = Vector((-600, -750))
    connect_inputs(mat.node_tree, animation_color_upper_bound_node, "Color", animation_color_upper_bound_gamma_node, "Color")

    mix_factor = 1
    if shader.shader_body.self_illumination_animation_function == FunctionEnum.one.value:
        mix_factor = 0

    animation_color_mix_node = mat.node_tree.nodes.new("ShaderNodeMix")
    animation_color_mix_node.data_type = 'RGBA'
    animation_color_mix_node.blend_type = "MULTIPLY"
    animation_color_mix_node.clamp_result = True
    animation_color_mix_node.inputs[0].default_value = mix_factor
    animation_color_mix_node.location = Vector((-425, -600))
    connect_inputs(mat.node_tree, animation_color_lower_bound_gamma_node, "Color", animation_color_mix_node, 6)
    connect_inputs(mat.node_tree, animation_color_upper_bound_gamma_node, "Color", animation_color_mix_node, 7)
    connect_inputs(mat.node_tree, animation_color_mix_node, 2, bdsf_principled, "Emission Color")

def generate_shader_environment(mat, shader, permutation_index, report):
    mat.use_nodes = True

    texture_root = config.HALO_1_DATA_PATH
    base_map, base_map_name = get_bitmap(shader.shader_body.base_map, texture_root)
    primary_detail_map, primary_detail_map_name = get_bitmap(shader.shader_body.primary_detail_map, texture_root)
    secondary_detail_map, secondary_detail_map_name = get_bitmap(shader.shader_body.secondary_detail_map, texture_root)
    micro_detail_map, micro_detail_map_name = get_bitmap(shader.shader_body.micro_detail_map, texture_root)
    bump_map, bump_map_name = get_bitmap(shader.shader_body.bump_map, texture_root)
    illum_map, illum_map_name = get_bitmap(shader.shader_body.map, texture_root)
    reflection_map, reflection_map_name = get_bitmap(shader.shader_body.reflection_cube_map, texture_root)

    base_bitmap = shader.shader_body.base_map.parse_tag(report, "halo1", "retail")
    primary_detail_bitmap = shader.shader_body.primary_detail_map.parse_tag(report, "halo1", "retail")
    secondary_detail_bitmap = shader.shader_body.secondary_detail_map.parse_tag(report, "halo1", "retail")
    micro_detail_bitmap = shader.shader_body.micro_detail_map.parse_tag(report, "halo1", "retail")
    base_bitmap = shader.shader_body.base_map.parse_tag(report, "halo1", "retail")
    bump_bitmap = shader.shader_body.bump_map.parse_tag(report, "halo1", "retail")
    illum_bitmap = shader.shader_body.map.parse_tag(report, "halo1", "retail")
    reflection_bitmap = shader.shader_body.reflection_cube_map.parse_tag(report, "halo1", "retail")

    rescale_detail = DiffuseFlags.rescale_detail_maps in DiffuseFlags(shader.shader_body.diffuse_flags)
    rescale_bump_maps = DiffuseFlags.rescale_bump_maps in DiffuseFlags(shader.shader_body.diffuse_flags)

    base_bitmap_count = 0
    primary_detail_bitmap_count = 0
    secondary_detail_bitmap_count = 0
    micro_detail_bitmap_count = 0
    bump_bitmap_count = 0
    if base_bitmap:
        base_bitmap_count = len(base_bitmap.bitmaps)
    if primary_detail_bitmap:
        primary_detail_bitmap_count = len(primary_detail_bitmap.bitmaps)
    if secondary_detail_bitmap:
        secondary_detail_bitmap_count = len(secondary_detail_bitmap.bitmaps)
    if micro_detail_bitmap:
        micro_detail_bitmap_count = len(micro_detail_bitmap.bitmaps)
    if bump_bitmap:
        bump_bitmap_count = len(bump_bitmap.bitmaps)

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    bdsf_principled.inputs[7].default_value = 0.0
    bdsf_principled.inputs[9].default_value = 1

    base_node = generate_image_node(mat, base_map, base_bitmap, base_map_name)
    base_node.name = "Base Map"
    base_node.location = Vector((-2100, 475))
    if not base_node.image == None:
        base_node.image.alpha_mode = 'CHANNEL_PACKED'

    primary_detail_node = generate_image_node(mat, primary_detail_map, primary_detail_bitmap, primary_detail_map_name)
    if not primary_detail_node.image == None:
        primary_detail_node.image.alpha_mode = 'CHANNEL_PACKED'

    primary_detail_node.name = "Primary Detail Map"
    primary_detail_node.location = Vector((-2100, 1350))

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-2275, 1250))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", primary_detail_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-2450, 1325))
    combine_xyz_node.location = Vector((-2450, 1175))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.shader_body.primary_detail_map_scale
    if shader.shader_body.primary_detail_map_scale == 0.0:
        scale = 1.0

    primary_detail_rescale_i = scale
    primary_detail_rescale_j = scale
    if base_bitmap_count > 0 and primary_detail_bitmap_count > 0 and rescale_detail:
        if base_bitmap_count > permutation_index:
            base_element = base_bitmap.bitmaps[permutation_index]
        else:
            base_element = base_bitmap.bitmaps[0]

        if primary_detail_bitmap_count > permutation_index:
            primary_detail_element = primary_detail_bitmap.bitmaps[permutation_index]
        else:
            primary_detail_element = primary_detail_bitmap.bitmaps[0]

        primary_detail_rescale_i *= base_element.width / primary_detail_element.width
        primary_detail_rescale_j *= base_element.height / primary_detail_element.height

    combine_xyz_node.inputs[0].default_value = primary_detail_rescale_i
    combine_xyz_node.inputs[1].default_value = primary_detail_rescale_j
    combine_xyz_node.inputs[2].default_value = 1

    secondary_detail_node = generate_image_node(mat, secondary_detail_map, secondary_detail_bitmap, secondary_detail_map_name)
    if not secondary_detail_node.image == None:
        secondary_detail_node.image.alpha_mode = 'CHANNEL_PACKED'

    secondary_detail_node.name = "Secondary Detail Map"
    secondary_detail_node.location = Vector((-2100, 1050))

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-2275, 975))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", secondary_detail_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-2450, 1025))
    combine_xyz_node.location = Vector((-2450, 875))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.shader_body.secondary_detail_map_scale
    if shader.shader_body.secondary_detail_map_scale == 0.0:
        scale = 1.0

    secondary_detail_rescale_i = scale
    secondary_detail_rescale_j = scale
    if base_bitmap_count > 0 and secondary_detail_bitmap_count > 0 and rescale_detail:
        if base_bitmap_count > permutation_index:
            base_element = base_bitmap.bitmaps[permutation_index]
        else:
            base_element = base_bitmap.bitmaps[0]
        if secondary_detail_bitmap_count > permutation_index:
            secondary_detail_element = secondary_detail_bitmap.bitmaps[permutation_index]
        else:
            secondary_detail_element = secondary_detail_bitmap.bitmaps[0]

        secondary_detail_rescale_i *= base_element.width / secondary_detail_element.width
        secondary_detail_rescale_j *= base_element.height / secondary_detail_element.height

    combine_xyz_node.inputs[0].default_value = secondary_detail_rescale_i
    combine_xyz_node.inputs[1].default_value = secondary_detail_rescale_j
    combine_xyz_node.inputs[2].default_value = 1

    micro_detail_node = generate_image_node(mat, micro_detail_map, micro_detail_bitmap, micro_detail_map_name)
    if not micro_detail_node.image == None:
        micro_detail_node.image.alpha_mode = 'CHANNEL_PACKED'

    micro_detail_node.name = "Micro Detail Map"
    micro_detail_node.location = Vector((-2100, 775))

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-2275, 675))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", micro_detail_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-2450, 725))
    combine_xyz_node.location = Vector((-2450, 575))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.shader_body.micro_detail_map_scale
    if shader.shader_body.micro_detail_map_scale == 0.0:
        scale = 1.0

    micro_detail_rescale_i = scale
    micro_detail_rescale_j = scale
    if base_bitmap_count > 0 and micro_detail_bitmap_count > 0 and rescale_detail:
        if base_bitmap_count > permutation_index:
            base_element = base_bitmap.bitmaps[permutation_index]
        else:
            base_element = base_bitmap.bitmaps[0]
        if micro_detail_bitmap_count > permutation_index:
            micro_detail_element = micro_detail_bitmap.bitmaps[permutation_index]
        else:
            micro_detail_element = micro_detail_bitmap.bitmaps[0]

        micro_detail_rescale_i *= base_element.width / micro_detail_element.width
        micro_detail_rescale_j *= base_element.height / micro_detail_element.height

    combine_xyz_node.inputs[0].default_value = micro_detail_rescale_i
    combine_xyz_node.inputs[1].default_value = micro_detail_rescale_j
    combine_xyz_node.inputs[2].default_value = 1

    bump_node = generate_image_node(mat, bump_map, bump_bitmap, bump_map_name)
    if not bump_node.image == None:
        bump_node.image.colorspace_settings.name = 'Non-Color'

    bump_node.name = "Bump Map"
    bump_node.location = Vector((-700, -600))

    alpha_shader = EnvironmentFlags.alpha_tested in EnvironmentFlags(shader.shader_body.environment_flags)
    if alpha_shader:
        mat.shadow_method = 'CLIP'
        mat.blend_method = 'CLIP'

    mat.use_backface_culling = True

    connect_inputs(mat.node_tree, bump_node, "Alpha", bdsf_principled, "Alpha")

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-875, -800))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", bump_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    height_node = mat.node_tree.nodes.new("ShaderNodeBump")
    uv_map_node.location = Vector((-1075, -800))
    combine_xyz_node.location = Vector((-1075, -925))
    height_node.location = Vector((-425, -600))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)
    connect_inputs(mat.node_tree, bump_node, "Color", height_node, "Height")
    connect_inputs(mat.node_tree, height_node, "Normal", bdsf_principled, "Normal")

    if bump_bitmap:
        height_node.inputs[0].default_value = bump_bitmap.bitmap_body.bump_height

    scale = shader.shader_body.bump_map_scale
    if shader.shader_body.bump_map_scale == 0.0:
        scale = 1.0

    bump_rescale_i = scale
    bump_rescale_j = scale
    if base_bitmap_count > 0 and bump_bitmap_count > 0 and rescale_bump_maps:
        if base_bitmap_count > permutation_index:
            base_element = base_bitmap.bitmaps[permutation_index]
        else:
            base_element = base_bitmap.bitmaps[0]
        if bump_bitmap_count > permutation_index:
            bump_element = bump_bitmap.bitmaps[permutation_index]
        else:
            bump_element = bump_bitmap.bitmaps[0]

        bump_rescale_i *= base_element.width / bump_element.width
        bump_rescale_j *= base_element.height / bump_element.height

    combine_xyz_node.inputs[0].default_value = bump_rescale_i
    combine_xyz_node.inputs[1].default_value = bump_rescale_j
    combine_xyz_node.inputs[2].default_value = 1

    self_illumination_node = generate_image_node(mat, illum_map, illum_bitmap, illum_map_name)
    self_illumination_node.name = "Self Illumination Map"
    self_illumination_node.location = Vector((-2100.0, 1625.0))

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-2275, 1550))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", self_illumination_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-2450, 1625))
    combine_xyz_node.location = Vector((-2450, 1475))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.shader_body.map_scale
    if shader.shader_body.map_scale == 0.0:
        scale = 1.0

    combine_xyz_node.inputs[0].default_value = scale
    combine_xyz_node.inputs[1].default_value = scale
    combine_xyz_node.inputs[2].default_value = 1

    reflection_node = generate_image_node(mat, reflection_map, reflection_bitmap, reflection_map_name, True)
    reflection_node.name = "Reflection Map"
    reflection_node.location = Vector((-2100.0, 175.0))
    texture_coordinate_node = mat.node_tree.nodes.new("ShaderNodeTexCoord")
    texture_coordinate_node.location = Vector((-2275.0, 175.0))
    connect_inputs(mat.node_tree, texture_coordinate_node, "Reflection", reflection_node, "Vector")

    reflection_tint_node = generate_reflection_tint_logic_node(mat.node_tree)
    reflection_tint_node.location = Vector((-2000, -75.0))

    perpendicular_tint_node = mat.node_tree.nodes.new('ShaderNodeRGB')
    perpendicular_tint_node.outputs[0].default_value = shader.shader_body.perpendicular_color
    perpendicular_tint_node.location = Vector((-2175, -75.0))
    connect_inputs(mat.node_tree, perpendicular_tint_node, "Color", reflection_tint_node, "Perpendicular Tint")
    reflection_tint_node.inputs["Perpendicular Brightness"].default_value = shader.shader_body.perpendicular_brightness

    parallel_tint_node = mat.node_tree.nodes.new('ShaderNodeRGB')
    parallel_tint_node.outputs[0].default_value = shader.shader_body.parallel_color
    parallel_tint_node.location = Vector((-2175, -275.0))
    connect_inputs(mat.node_tree, parallel_tint_node, "Color", reflection_tint_node, "Parallel Tint")
    reflection_tint_node.inputs["Parallel Brightness"].default_value = shader.shader_body.parallel_brightness

    reflection_mix_node = mat.node_tree.nodes.new("ShaderNodeMix")
    reflection_mix_node.data_type = 'RGBA'
    reflection_mix_node.blend_type = "MULTIPLY"
    reflection_mix_node.clamp_result = True
    reflection_mix_node.inputs[0].default_value = 1
    reflection_mix_node.location = Vector((-1825, -75.0))
    connect_inputs(mat.node_tree, reflection_tint_node, "Color", reflection_mix_node, 6)
    connect_inputs(mat.node_tree, reflection_node, "Color", reflection_mix_node, 7)

    base_mix_node = mat.node_tree.nodes.new("ShaderNodeMix")
    base_mix_node.data_type = 'RGBA'
    base_mix_node.blend_type = "MULTIPLY"
    base_mix_node.clamp_result = True
    base_mix_node.inputs[0].default_value = 1
    base_mix_node.location = Vector((-1650.0, -75.0))
    connect_inputs(mat.node_tree, base_node, "Alpha", base_mix_node, 6)
    connect_inputs(mat.node_tree, reflection_mix_node, 2, base_mix_node, 7)

    if shader.shader_body.environment_type == EnvironmentTypeEnum.normal.value:
        blend_mix_node = mat.node_tree.nodes.new("ShaderNodeMix")
        blend_mix_node.data_type = 'RGBA'
        blend_mix_node.blend_type = "ADD"
        blend_mix_node.clamp_result = True
        blend_mix_node.inputs[0].default_value = 1
        blend_mix_node.location = Vector((-1475.0, -75.0))
        connect_inputs(mat.node_tree, base_mix_node, 2, blend_mix_node, 6)
        connect_inputs(mat.node_tree, base_node, "Color", blend_mix_node, 7)

        blend_biased_multiply_node = generate_biased_multiply_node(mat.node_tree)
        blend_biased_multiply_node.location = Vector((-1300, -75))
        connect_inputs(mat.node_tree, blend_mix_node, 2, blend_biased_multiply_node, "Color")
        connect_inputs(mat.node_tree, micro_detail_node, "Color", blend_biased_multiply_node, "Detail")
        blend_biased_multiply_node.inputs[2].default_value = (1, 1, 1, 1)

        blend_multiply_a_node = generate_multiply_node(mat.node_tree)
        blend_multiply_a_node.location = Vector((-1125, -75))
        connect_inputs(mat.node_tree, blend_biased_multiply_node, "Color", blend_multiply_a_node, "Color")
        connect_inputs(mat.node_tree, secondary_detail_node, "Color", blend_multiply_a_node, "Detail")
        blend_multiply_a_node.inputs[2].default_value = (1, 1, 1, 1)

        blend_multiply_b_node = generate_multiply_node(mat.node_tree)
        blend_multiply_b_node.location = Vector((-950, -75))
        connect_inputs(mat.node_tree, blend_multiply_a_node, "Color", blend_multiply_b_node, "Color")
        connect_inputs(mat.node_tree, primary_detail_node, "Color", blend_multiply_b_node, "Detail")
        connect_inputs(mat.node_tree, blend_multiply_b_node, "Color", bdsf_principled, "Base Color")
        blend_multiply_b_node.inputs[2].default_value = (1, 1, 1, 1)

    elif shader.shader_body.environment_type == EnvironmentTypeEnum.blended.value:
        blend_mix_node = mat.node_tree.nodes.new("ShaderNodeMix")
        blend_mix_node.data_type = 'RGBA'
        blend_mix_node.blend_type = "ADD"
        blend_mix_node.clamp_result = True
        blend_mix_node.inputs[0].default_value = 1
        blend_mix_node.location = Vector((-775.0, -240.0))
        connect_inputs(mat.node_tree, base_mix_node, 2, blend_mix_node, 6)
        connect_inputs(mat.node_tree, base_node, "Color", blend_mix_node, 7)

        blend_detail_mix_node = mat.node_tree.nodes.new("ShaderNodeMix")
        blend_detail_mix_node.data_type = 'RGBA'
        blend_detail_mix_node.blend_type = "MIX"
        blend_detail_mix_node.clamp_result = True
        blend_detail_mix_node.inputs[0].default_value = 1
        blend_detail_mix_node.location = Vector((-775.0, -240.0))
        connect_inputs(mat.node_tree, base_node, "Alpha", blend_detail_mix_node, 0)
        connect_inputs(mat.node_tree, secondary_detail_node, "Color", blend_detail_mix_node, 6)
        connect_inputs(mat.node_tree, primary_detail_node, "Color", blend_detail_mix_node, 7)

        blend_biased_multiply_node = generate_biased_multiply_node(mat.node_tree)
        blend_biased_multiply_node.inputs[2].default_value = (1, 1, 1, 1)
        connect_inputs(mat.node_tree, blend_mix_node, 2, blend_biased_multiply_node, "Color")
        connect_inputs(mat.node_tree, blend_detail_mix_node, 2, blend_biased_multiply_node, "Detail")
        connect_inputs(mat.node_tree, blend_biased_multiply_node, "Color", bdsf_principled, "Base Color")

    elif shader.shader_body.blended_base_specular == EnvironmentTypeEnum.blended_base_specular.value:
        blend_mix_node = mat.node_tree.nodes.new("ShaderNodeMix")
        blend_mix_node.data_type = 'RGBA'
        blend_mix_node.blend_type = "ADD"
        blend_mix_node.clamp_result = True
        blend_mix_node.inputs[0].default_value = 1
        blend_mix_node.location = Vector((-775.0, -240.0))
        connect_inputs(mat.node_tree, base_mix_node, 2, blend_mix_node, 6)
        connect_inputs(mat.node_tree, base_node, "Color", blend_mix_node, 7)

        blend_detail_mix_node = mat.node_tree.nodes.new("ShaderNodeMix")
        blend_detail_mix_node.data_type = 'RGBA'
        blend_detail_mix_node.blend_type = "MIX"
        blend_detail_mix_node.clamp_result = True
        blend_detail_mix_node.inputs[0].default_value = 1
        blend_detail_mix_node.location = Vector((-775.0, -240.0))
        connect_inputs(mat.node_tree, base_node, "Alpha", blend_detail_mix_node, 0)
        connect_inputs(mat.node_tree, secondary_detail_node, "Color", blend_detail_mix_node, 6)
        connect_inputs(mat.node_tree, primary_detail_node, "Color", blend_detail_mix_node, 7)

        blend_biased_multiply_node = generate_biased_multiply_node(mat.node_tree)
        blend_biased_multiply_node.inputs[2].default_value = (1, 1, 1, 1)
        connect_inputs(mat.node_tree, blend_mix_node, 2, blend_biased_multiply_node, "Color")
        connect_inputs(mat.node_tree, blend_detail_mix_node, 2, blend_biased_multiply_node, "Detail")
        connect_inputs(mat.node_tree, blend_biased_multiply_node, "Color", bdsf_principled, "Base Color")

    is_mirror_node = mat.node_tree.nodes.new("ShaderNodeValue")
    is_mirror_node.location = Vector((-950, -475))
    is_mirror_node.outputs[0].default_value = ReflectionFlags.dynamic_mirror in ReflectionFlags(shader.shader_body.reflection_flags)

    greater_than_node = mat.node_tree.nodes.new("ShaderNodeMath")
    greater_than_node.operation = 'GREATER_THAN'
    greater_than_node.use_clamp = True
    greater_than_node.inputs[1].default_value = 0
    greater_than_node.location = Vector((-775, -225))
    connect_inputs(mat.node_tree, is_mirror_node, "Value", greater_than_node, "Value")

    less_than_node = mat.node_tree.nodes.new("ShaderNodeMath")
    less_than_node.operation = 'LESS_THAN'
    less_than_node.use_clamp = True
    less_than_node.inputs[1].default_value = 1
    less_than_node.location = Vector((-600, -400))
    connect_inputs(mat.node_tree, is_mirror_node, "Value", less_than_node, "Value")

    subtract_node = mat.node_tree.nodes.new("ShaderNodeMath")
    subtract_node.operation = 'SUBTRACT'
    subtract_node.use_clamp = True
    subtract_node.inputs[0].default_value = 1
    subtract_node.location = Vector((-600, -225))
    connect_inputs(mat.node_tree, greater_than_node, "Value", subtract_node, 1)

    add_node = mat.node_tree.nodes.new("ShaderNodeMath")
    add_node.operation = 'ADD'
    add_node.use_clamp = True
    add_node.inputs[1].default_value = 1
    add_node.location = Vector((-425, -400))
    connect_inputs(mat.node_tree, less_than_node, "Value", add_node, 0)
    connect_inputs(mat.node_tree, subtract_node, "Value", add_node, 1)
    connect_inputs(mat.node_tree, greater_than_node, "Value", bdsf_principled, "Metallic")
    connect_inputs(mat.node_tree, add_node, "Value", bdsf_principled, "Roughness")

def generate_shader_transparent_meter(mat, shader, report):
    mat.use_nodes = True

    texture_root = config.HALO_1_DATA_PATH
    meter_map, meter_map_name = get_bitmap(shader.shader_body.meter_map, texture_root)
    meter_bitmap = shader.shader_body.meter_map.parse_tag(report, "halo1", "retail")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    mat.node_tree.nodes.remove(bdsf_principled)

    shader_mix_node = mat.node_tree.nodes.new("ShaderNodeMixShader")
    shader_mix_node.location = Vector((-175, 0))
    connect_inputs(mat.node_tree, shader_mix_node, "Shader", output_material_node, "Surface")

    invert_node = mat.node_tree.nodes.new("ShaderNodeInvert")
    emission_node = mat.node_tree.nodes.new("ShaderNodeEmission")
    bsdf_transparent_node = mat.node_tree.nodes.new("ShaderNodeBsdfTransparent")
    invert_node.location = Vector((-350, 125))
    emission_node.location = Vector((-350, 0))
    bsdf_transparent_node.location = Vector((-350, -125))
    invert_node.inputs[0].default_value = 1
    connect_inputs(mat.node_tree, invert_node, "Color", shader_mix_node, 0)
    connect_inputs(mat.node_tree, emission_node, "Emission", shader_mix_node, 1)
    connect_inputs(mat.node_tree, bsdf_transparent_node, "BSDF", shader_mix_node, 2)

    gamma_node = mat.node_tree.nodes.new("ShaderNodeGamma")
    gamma_node.location = Vector((-525, -125))
    gamma_node.inputs[1].default_value = 2.2

    meter_node = generate_image_node(mat, meter_map, meter_bitmap, meter_map_name)
    meter_node.image.alpha_mode = 'CHANNEL_PACKED'
    meter_node.location = Vector((-650, 175))
    connect_inputs(mat.node_tree, gamma_node, "Color", emission_node, "Color")
    connect_inputs(mat.node_tree, meter_node, "Alpha", emission_node, "Strength")
    connect_inputs(mat.node_tree, meter_node, "Alpha", invert_node, "Color")

    rgb_node = mat.node_tree.nodes.new("ShaderNodeRGB")
    rgb_node.location = Vector((-725, -125))
    rgb_node.outputs[0].default_value = shader.shader_body.background_color
    connect_inputs(mat.node_tree, rgb_node, "Color", gamma_node, "Color")

    mat.blend_method = 'BLEND'

def generate_shader_transparent_glass(mat, shader, report):
    mat.use_nodes = True

    texture_root = config.HALO_1_DATA_PATH
    background_tint_map, background_tint_map_name = get_bitmap(shader.shader_body.background_tint_map, texture_root)
    reflection_map, reflection_map_name = get_bitmap(shader.shader_body.reflection_map, texture_root)
    bump_map, bump_map_name = get_bitmap(shader.shader_body.bump_map, texture_root)
    diffuse_map, diffuse_map_name = get_bitmap(shader.shader_body.diffuse_map, texture_root)
    diffuse_detail_map, diffuse_detail_map_name = get_bitmap(shader.shader_body.diffuse_detail_map, texture_root)
    specular_map, specular_map_name = get_bitmap(shader.shader_body.specular_map, texture_root)
    specular_detail_map, specular_detail_map_name = get_bitmap(shader.shader_body.specular_detail_map, texture_root)

    background_tint_bitmap = shader.shader_body.background_tint_map.parse_tag(report, "halo1", "retail")
    reflection_bitmap = shader.shader_body.reflection_map.parse_tag(report, "halo1", "retail")
    bump_bitmap = shader.shader_body.bump_map.parse_tag(report, "halo1", "retail")
    diffuse_bitmap = shader.shader_body.diffuse_map.parse_tag(report, "halo1", "retail")
    diffuse_detail_bitmap = shader.shader_body.diffuse_detail_map.parse_tag(report, "halo1", "retail")
    specular_bitmap = shader.shader_body.specular_map.parse_tag(report, "halo1", "retail")
    specular_detail_bitmap = shader.shader_body.specular_detail_map.parse_tag(report, "halo1", "retail")

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    background_tint_node = generate_image_node(mat, background_tint_map, background_tint_bitmap, background_tint_map_name)
    reflection_node = generate_image_node(mat, reflection_map, reflection_bitmap, reflection_map_name)
    bump_node = generate_image_node(mat, bump_map, bump_bitmap, bump_map_name)

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-875, -800))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", bump_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    height_node = mat.node_tree.nodes.new("ShaderNodeBump")
    uv_map_node.location = Vector((-1075, -800))
    combine_xyz_node.location = Vector((-1075, -925))
    height_node.location = Vector((-425, -600))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)
    connect_inputs(mat.node_tree, bump_node, "Color", height_node, "Height")
    connect_inputs(mat.node_tree, height_node, "Normal", bdsf_principled, "Normal")

    if bump_bitmap:
        height_node.inputs[0].default_value = bump_bitmap.bitmap_body.bump_height

    scale = shader.shader_body.bump_map_scale
    if shader.shader_body.bump_map_scale == 0.0:
        scale = 1.0

    combine_xyz_node.inputs[0].default_value = scale
    combine_xyz_node.inputs[1].default_value = scale
    combine_xyz_node.inputs[2].default_value = 1

    diffuse_node = generate_image_node(mat, diffuse_map, diffuse_bitmap, diffuse_map_name)

    connect_inputs(mat.node_tree, diffuse_node, "Color", bdsf_principled, "Base Color")

    if diffuse_bitmap:
        ignore_alpha_bitmap = diffuse_bitmap.bitmap_body.format is FormatEnum.compressed_with_color_key_transparency.value
        if ignore_alpha_bitmap:
            diffuse_node.image.alpha_mode = 'NONE'
        else:
            connect_inputs(mat.node_tree, diffuse_node, "Alpha", bdsf_principled, "Alpha")
            mat.shadow_method = 'CLIP'
            mat.blend_method = 'BLEND'

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-2275, 1250))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", diffuse_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-2450, 1325))
    combine_xyz_node.location = Vector((-2450, 1175))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.shader_body.diffuse_map_scale
    if shader.shader_body.diffuse_map_scale == 0.0:
        scale = 1.0

    combine_xyz_node.inputs[0].default_value = scale
    combine_xyz_node.inputs[1].default_value = scale
    combine_xyz_node.inputs[2].default_value = 1

    diffuse_detail_node = generate_image_node(mat, diffuse_detail_map, diffuse_detail_bitmap, diffuse_detail_map_name)

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-2275, 1250))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", diffuse_detail_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-2450, 1325))
    combine_xyz_node.location = Vector((-2450, 1175))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.shader_body.diffuse_detail_map_scale
    if shader.shader_body.diffuse_detail_map_scale == 0.0:
        scale = 1.0

    combine_xyz_node.inputs[0].default_value = scale
    combine_xyz_node.inputs[1].default_value = scale
    combine_xyz_node.inputs[2].default_value = 1

    specular_node = generate_image_node(mat, specular_map, specular_bitmap, specular_map_name)

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-2275, 1250))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", specular_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-2450, 1325))
    combine_xyz_node.location = Vector((-2450, 1175))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.shader_body.specular_map_scale
    if shader.shader_body.specular_map_scale == 0.0:
        scale = 1.0

    combine_xyz_node.inputs[0].default_value = scale
    combine_xyz_node.inputs[1].default_value = scale
    combine_xyz_node.inputs[2].default_value = 1

    specular_detail_node = generate_image_node(mat, specular_detail_map, specular_detail_bitmap, specular_detail_map_name)

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-2275, 1250))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", specular_detail_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-2450, 1325))
    combine_xyz_node.location = Vector((-2450, 1175))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.shader_body.specular_detail_map_scale
    if shader.shader_body.specular_detail_map_scale == 0.0:
        scale = 1.0

    combine_xyz_node.inputs[0].default_value = scale
    combine_xyz_node.inputs[1].default_value = scale
    combine_xyz_node.inputs[2].default_value = 1

def generate_h1_shader(mat, tag_ref, shader_permutation_index, report):
    # 0 = Shader generation is disabled
    # 1 = Simple shader generation. Only the base map is generated
    # 2 = Full Shader generation
    if not config.SHADER_GEN == 0:
        shader = tag_ref.parse_tag(report, "halo1", "retail")
        if not shader == None:
            if shader.header.tag_group == "senv":
                if config.SHADER_GEN == 1:
                    generate_shader_environment_simple(mat, shader, shader_permutation_index, report)
                else:
                    generate_shader_environment(mat, shader, shader_permutation_index, report)

            elif shader.header.tag_group == "soso":
                if config.SHADER_GEN == 1:
                    generate_shader_model_simple(mat, shader, report)
                else:
                    generate_shader_model(mat, shader, report)

            elif shader.header.tag_group == "schi":
                if config.SHADER_GEN == 1:
                    generate_shader_transparent_chicago_simple(mat, shader, report)
                else:
                    print("Skipping shader_transparent_chicago")
                    #generate_shader_transparent_chicago(mat, shader, report)

            elif shader.header.tag_group == "scex":
                if config.SHADER_GEN == 1:
                    generate_shader_transparent_chicago_extended_simple(mat, shader, report)
                else:
                    print("Skipping shader_transparent_chicago_extended")
                    #generate_shader_transparent_chicago_extended(mat, shader, report)

            elif shader.header.tag_group == "sotr":
                if config.SHADER_GEN == 1:
                    generate_shader_transparent_generic_simple(mat, shader, report)
                else:
                    print("Skipping shader_transparent_generic")
                    #generate_shader_transparent_generic(mat, shader, report)

            elif shader.header.tag_group == "sgla":
                if config.SHADER_GEN == 1:
                    generate_shader_transparent_glass_simple(mat, shader, report)
                else:
                    generate_shader_transparent_glass(mat, shader, report)

            elif shader.header.tag_group == "smet":
                if config.SHADER_GEN == 1:
                    generate_shader_transparent_meter_simple(mat, shader, report)
                else:
                    generate_shader_transparent_meter(mat, shader, report)

            elif shader.header.tag_group == "spla":
                if config.SHADER_GEN == 1:
                    generate_shader_transparent_plasma_simple(mat, shader, report)
                else:
                    print("Skipping shader_transparent_plasma")
                    #generate_shader_transparent_plasma(mat, shader, report)

            elif shader.header.tag_group == "swat":
                if config.SHADER_GEN == 1:
                    generate_shader_transparent_water_simple(mat, shader, report)
                else:
                    print("Skipping shader_transparent_water")
                    #generate_shader_transparent_water(mat, shader, report)

def generate_shader_simple(mat, shader, report):
    mat.use_nodes = True

    texture_root = config.HALO_2_DATA_PATH
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
        base_bitmap = base_parameter.bitmap.parse_tag(report, "halo2", "retail")

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

def generate_h2_shader(mat, tag_ref, report):
    # 0 = Shader generation is disabled
    # 1 = Simple shader generation. Only the base map is generated
    # 2 = Full Shader generation
    if not config.SHADER_GEN == 0:
        shader = tag_ref.parse_tag(report, "halo2", "retail")
        if not shader == None:
            if shader.header.tag_group == "shad":
                if config.SHADER_GEN == 1:
                    generate_shader_simple(mat, shader, report)
                else:
                    print("Skipping shader")
                    #generate_shader_environment(mat, shader, report)
