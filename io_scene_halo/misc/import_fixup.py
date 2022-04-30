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

from ..global_functions import global_functions, mesh_processing

def merge_normals():
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.merge_normals()
    bpy.ops.mesh.select_all(action='DESELECT')

def merge_verts(material_idx_list, threshold):
    for material_idx in material_idx_list:
        bpy.context.object.active_material_index = material_idx
        bpy.ops.object.material_slot_select()

    bpy.ops.mesh.remove_doubles(threshold=threshold, use_sharp_edge_from_normals=True)
    bpy.ops.mesh.select_all(action='DESELECT')

def model_fixup(context, threshold):
    collections = []
    layer_collections = list(context.view_layer.layer_collection.children)

    while len(layer_collections) > 0:
        collection_batch = layer_collections
        layer_collections = []
        for collection in collection_batch:
            collections.append(collection)
            for collection_child in collection.children:
                layer_collections.append(collection_child)

    object_list = list(context.scene.objects)
    processed_mesh_name_list = []
    for obj in object_list:
        if obj.type== 'MESH' and not mesh_processing.set_ignore(collections, obj):
            edge_split = global_functions.EdgeSplit(True, False, 0.523599, True)
            mesh_processing.add_modifier(context, obj, False, edge_split, None)
            if not obj.data.name in processed_mesh_name_list:
                processed_mesh_name_list.append(obj.data.name)
                mesh_processing.select_object(context, obj)
                bpy.ops.object.mode_set(mode = 'EDIT')
                merge_normals()

                main_material_idx = []
                render_only_material_idx = []
                two_sided_material_idx = []
                media_material_idx = []
                portal_material_idx = []

                for idx, slot in enumerate(obj.material_slots):
                    mat = slot.material
                    if mat is not None:
                        if "!" in mat.name or mat.ass_jms.render_only:
                            render_only_material_idx.append(idx)

                        elif mat.name == "+portal" or mat.name == "+exactportal":
                            portal_material_idx.append(idx)

                        elif "%" in mat.name or mat.ass_jms.two_sided or "?" in mat.name or mat.ass_jms.transparent_2_sided:
                            two_sided_material_idx.append(idx)

                        elif mat.name == "+media" or mat.name == "+sound" or mat.name == "+unused" or mat.name == "+weatherpoly" or "$" in mat.name or mat.ass_jms.fog_plane:
                            media_material_idx.append(idx)

                        else:
                            main_material_idx.append(idx)

                merge_verts(main_material_idx, threshold)
                merge_verts(render_only_material_idx, threshold)
                merge_verts(two_sided_material_idx, threshold)
                merge_verts(media_material_idx, threshold)
                merge_verts(portal_material_idx, threshold)

                bpy.ops.mesh.customdata_custom_splitnormals_clear()
                bpy.ops.object.mode_set(mode = 'OBJECT')
                obj.data.use_auto_smooth = False
                mesh_processing.deselect_objects(context)

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.halo_bulk.import_fixup()
