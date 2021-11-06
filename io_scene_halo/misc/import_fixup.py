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

from io import BytesIO, TextIOWrapper
import zipfile
import bpy
import bmesh

from os import path
from mathutils import Matrix
from io_scene_halo.file_jms import import_jms
from ..global_functions import mesh_processing

def model_fixup(context):
    object_list = list(context.scene.objects)
    processed_mesh_name_list = []
    for obj in object_list:
        if obj.type== 'MESH' and not obj.data.name in processed_mesh_name_list:
            render_only_material_idx = []
            processed_mesh_name_list.append(obj.data.name)
            mesh_processing.select_object(context, obj)
            bpy.ops.object.mode_set(mode = 'EDIT')

            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.merge_normals()
            context.view_layer.update()
            bpy.ops.mesh.select_all(action='DESELECT')
            for idx, slot in enumerate(obj.material_slots):
                if not "!" in slot.material.name:
                    bpy.context.object.active_material_index = idx
                    bpy.ops.object.material_slot_select()

                    bpy.ops.mesh.remove_doubles(threshold=0.01, use_sharp_edge_from_normals=True)
                    bpy.ops.mesh.select_all(action='DESELECT')

                else:
                    render_only_material_idx.append(idx)

            for material_idx in render_only_material_idx:
                bpy.context.object.active_material_index = material_idx
                bpy.ops.object.material_slot_select()

                bpy.ops.mesh.remove_doubles(threshold=0.01, use_sharp_edge_from_normals=True)
                bpy.ops.mesh.select_all(action='DESELECT')

            bpy.ops.mesh.customdata_custom_splitnormals_clear()
            bpy.ops.object.mode_set(mode = 'OBJECT')
            obj.data.use_auto_smooth = False
            mesh_processing.deselect_objects(context)


    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.halo_bulk.scale_model()
