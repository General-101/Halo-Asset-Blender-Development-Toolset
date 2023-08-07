# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2023 SamDamDing AKA MercyMoon
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

import subprocess
import bpy
from ..global_functions import mesh_processing

def export_texture(context, directory):
    scene = context.scene
    for obj in bpy.context.scene.objects:
        for slot in obj.material_slots:
            if slot.material and slot.material.use_nodes:
                for node in slot.material.node_tree.nodes:
                    if node.type == 'TEX_IMAGE':
                        imagename=node.image.name
                        imagename = imagename.rpartition('.')
                        imagename = imagename[0]
                        node.image.filepath_raw = directory + imagename + ".tif"
                        print("Exporting " + node.image.name + " to " + node.image.filepath_raw)
                        node.image.file_format = "TIFF"
                        node.image.save()
    return {"FINISHED"}

def make_bitmaps(context, toolpath, directory):
    scene = context.scene
    H3EK = toolpath
    Tool = H3EK + r'\tool.exe'
    BitmapPath = directory
    BitmapPath = str(BitmapPath.split(H3EK)[1])
    BitmapPath = str(BitmapPath.split("data\\")[1])
    print("Making Bitmaps out of Tifs in " + directory)
    result = subprocess.Popen([Tool, "bitmaps", BitmapPath], cwd=H3EK)
    print("stdout:", result.stdout)
    return {'FINISHED'}

def enable_material_type(context):
    active_object = context.view_layer.objects.active
    if active_object.type== 'MESH':
        for material in active_object.data.materials:
            if getattr(material.ass_jms, 'is_bm') == False:
                setattr(material.ass_jms, 'is_bm', True)
            else:
                setattr(material.ass_jms, 'is_bm', False)
    return {"FINISHED"}

def set_material_type(context, material_type):
    active_object = context.view_layer.objects.active
    if active_object.type== 'MESH':
        for material in active_object.data.materials:
            if getattr(material.ass_jms, material_type) == False:
                setattr(material.ass_jms, material_type, True)
            else:
                setattr(material.ass_jms, material_type, False)
    return {"FINISHED"}

if __name__ == '__main__':
    bpy.ops.halo_mattools.export_texture()
