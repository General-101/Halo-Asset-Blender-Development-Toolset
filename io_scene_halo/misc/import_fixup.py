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

from ..global_functions import global_functions, mesh_processing, resource_management

def merge_normals():
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.merge_normals()
    bpy.ops.mesh.select_all(action='DESELECT')

def merge_verts(material_idx_list, threshold):
    bpy.ops.mesh.select_all(action='DESELECT')
    for material_idx in material_idx_list:
        bpy.context.object.active_material_index = material_idx
        bpy.ops.object.material_slot_select()

    bpy.ops.mesh.remove_doubles(threshold=threshold, use_sharp_edge_from_normals=True)
    bpy.ops.mesh.select_all(action='DESELECT')

def model_fixup(context, threshold):
    hidden_geo = False
    nonrender_geo = True

    layer_collection_list = []
    object_list = []

    # Gather all scene resources that fit export criteria
    resource_management.gather_scene_resources(context, layer_collection_list, object_list, hidden_geo, nonrender_geo)

    processed_mesh_list = []

    edge_split = global_functions.EdgeSplit(True, False, 0.523599, True)
    for obj in object_list:
        if obj.type== 'MESH':
            mesh_processing.add_modifier(context, obj, False, edge_split, None)
            if not obj.data in processed_mesh_list:
                processed_mesh_list.append(obj.data)
                mesh_processing.select_object(context, obj)
                bpy.ops.object.mode_set(mode = 'EDIT')
                #merge_normals() # Seems to break more than it helps - General_101

                main_material_ids = []
                render_only_material_ids = []
                two_sided_material_ids = []
                media_material_ids = []
                seamsealer_material_ids = []
                portal_material_ids = []

                for idx, slot in enumerate(obj.material_slots):
                    mat = slot.material
                    if mat is not None:
                        mat_name = mat.name.lower()
                        if "!" in mat_name or mat.ass_jms.render_only:
                            render_only_material_ids.append(idx)

                        elif "+portal" in mat_name or "+exactportal" in mat_name:
                            portal_material_ids.append(idx)

                        elif "%" in mat_name or mat.ass_jms.two_sided or "?" in mat_name or mat.ass_jms.transparent_2_sided or "#" in mat_name or mat.ass_jms.transparent_1_sided:
                            two_sided_material_ids.append(idx)

                        elif "+media" in mat_name or "+sound" in mat_name or "+unused" in mat_name or "+weatherpoly" in mat_name or "$" in mat_name or mat.ass_jms.fog_plane:
                            media_material_ids.append(idx)

                        #elif "+seamsealer" in mat.name:
                            #seamsealer_material_ids.append(idx)

                        else:
                            main_material_ids.append(idx)

                merge_verts(main_material_ids, threshold)
                merge_verts(render_only_material_ids, threshold)
                merge_verts(two_sided_material_ids, threshold)
                merge_verts(media_material_ids, threshold)
                #merge_verts(seamsealer_material_ids, threshold)
                merge_verts(portal_material_ids, threshold)

                bpy.ops.mesh.customdata_custom_splitnormals_clear()
                bpy.ops.object.mode_set(mode = 'OBJECT')
                mesh_processing.deselect_objects(context)
                
                if (4, 1, 0) > bpy.app.version:
                    obj.data.use_auto_smooth = False

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.halo_bulk.import_fixup()
