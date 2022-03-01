# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2021 Steven Garcia
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
from ..global_functions import global_functions

def lightmap_bulk(context, res_x, res_y):
    object_list = list(context.scene.objects)

    for object in object_list:
        node_spacing = 20.0
        assigned_material_id = []
        if object.type == 'MESH':
            for polygon in object.data.polygons:
                material_id = global_functions.get_face_material(object, polygon)
                if not material_id in assigned_material_id:
                    assigned_material_id.append(material_id)

            for material_id in assigned_material_id:
                mat = object.material_slots[material_id].material
                mat.use_nodes = True
                lightmap_tex_node = None
                diffuse_tex_node = None
                normal_tex_node = None
                bsdf_node = None
                for node in mat.node_tree.nodes:
                    if node.type == 'TEX_IMAGE' and node.name == "lightmap_%s" % object.name:
                        lightmap_tex_node = node

                    elif node.type == 'TEX_IMAGE' and node.name == "diffuse_%s" % mat.name:
                        diffuse_tex_node = node

                    elif node.type == 'TEX_IMAGE' and node.name == "normal_%s" % mat.name:
                        normal_tex_node = node

                    elif node.type == 'BSDF_PRINCIPLED':
                        bsdf_node = node

                if bsdf_node is None:
                    bsdf_node = mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled')

                lightmap_image = bpy.data.images.get(object.name)
                if lightmap_image is None:
                    lightmap_image = bpy.data.images.new(object.name, res_x, res_y)

                if diffuse_tex_node is None:
                    diffuse_tex_node = mat.node_tree.nodes.new('ShaderNodeTexImage')
                    diffuse_tex_node.name = "diffuse_%s" % mat.name
                    mat.node_tree.links.new(bsdf_node.inputs['Base Color'], diffuse_tex_node.outputs['Color'])
                    diffuse_tex_node.location = Vector((bsdf_node.location.x + -250 + (-1 * node_spacing), bsdf_node.location.y))
                    diffuse_tex_node = mat.node_tree.nodes.new('ShaderNodeTexImage')

                if normal_tex_node is None:
                    normal_tex_node = mat.node_tree.nodes.new('ShaderNodeTexImage')
                    normal_tex_node.name = "normal_%s" % mat.name
                    mat.node_tree.links.new(bsdf_node.inputs['Normal'], normal_tex_node.outputs['Color'])
                    normal_tex_node.location = Vector((bsdf_node.location.x + -250 + (-1 * node_spacing), bsdf_node.location.y + -250))

                if lightmap_tex_node is None:
                    lightmap_tex_node = mat.node_tree.nodes.new('ShaderNodeTexImage')
                    lightmap_tex_node.name = "lightmap_%s" % object.name
                    lightmap_tex_node.location = Vector((bsdf_node.location.x, bsdf_node.location.y + -600 + (-1 * node_spacing)))

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.halo_bulk.lightmapper_images()
