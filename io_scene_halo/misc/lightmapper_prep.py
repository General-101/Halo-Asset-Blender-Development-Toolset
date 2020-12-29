# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2020 Steven Garcia
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

from math import radians

def lightmap_bulk(context, res_x, res_y, fix_rotation):
    scene = bpy.context.scene
    object_list = list(scene.objects)

    for object in object_list:
        if fix_rotation:
            object.rotation_euler =(0,0,radians(90.0))

        for material in object.material_slots:
            mat = bpy.data.materials[material.name]
            tex_node = None
            bsdf_node = None
            for node in mat.node_tree.nodes:
                if node.type == 'TEX_IMAGE':
                    tex_node = node

                elif node.type == 'BSDF_PRINCIPLED':
                    bsdf_node = node

            if bsdf_node is None:
                bsdf_node = mat.node_tree.nodes.new('ShaderNodeBsdfDiffuse')

            if tex_node is None:
                tex_node = mat.node_tree.nodes.new('ShaderNodeTexImage')

            lightmap_image = bpy.data.images.get(object.name)
            if lightmap_image is None:
                lightmap_image = bpy.data.images.new(object.name, res_x, res_y)

            tex_node.image = lightmap_image
            mat.node_tree.links.new(bsdf_node.inputs['Base Color'], tex_node.outputs['Color'])

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.halo_bulk.lightmapper_images()

