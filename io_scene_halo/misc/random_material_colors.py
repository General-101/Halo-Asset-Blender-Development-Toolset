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

from ..global_functions import  global_functions

def get_linked_node(node, input_name, search_type):
    linked_node = None
    node_input = node.inputs[input_name]
    if node_input.is_linked:
        for node_link in node_input.links:
            if node_link.from_node.type == search_type:
                linked_node = node_link.from_node
                break

    return linked_node

def random_material_colors(context):
    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors
    for material in bpy.data.materials:
        new_diffuse = random_color_gen.next()
        material.diffuse_color = new_diffuse
        if material.use_nodes:
            if not material.node_tree == None:
                for node in material.node_tree.nodes:
                    if node.type == 'OUTPUT_MATERIAL':
                        bdsf_principled = get_linked_node(node, "Surface", "BSDF_PRINCIPLED")
                        if not bdsf_principled is None:
                            surface_input = node.inputs["Surface"]
                            if surface_input.is_linked:
                                surface_node = surface_input.links[0].from_node
                                diffuse_nodes = surface_node.inputs["Base Color"]
                                diffuse_nodes.default_value = new_diffuse

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.halo_bulk.random_material_colors()
