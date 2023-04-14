# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Crisp
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

from io_scene_foundry.utils.nwo_utils import get_perm, deselect_all_objects, set_active_object

def jms_assign(context, report):
    jms_count = 0
    for obj in context.selected_objects:
        deselect_all_objects()
        jms_count += jms_process(context, report, obj)
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    report({'INFO'},f"Split {jms_count} meshes by face maps and updated regions & permutations")
    return {'FINISHED'}

def jms_process(context, report, obj):
    # Split object split by face map
    obj.select_set(True)
    set_active_object(obj)
    mesh_name = str(obj.name)
    if obj.type == 'MESH' and len(obj.face_maps) > 0:
        if obj.name.startswith('@'):
            prefix = '@'
        elif obj.name.startswith('$'):
            prefix = '$'
        else:
            prefix = ''
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        skip_rename = len(obj.face_maps) == 1
        while len(obj.face_maps) > 1:
            # Deselect all faces except those in the current face map
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.face_map_select()
                    
            # Split the mesh by the selected faces
            bpy.ops.mesh.separate(type='SELECTED')

            bpy.ops.object.face_map_remove()
            
            # Rename the newly created object to match the face map name
            # new_ob = bpy.context.active_object
            # new_ob.name = 'TEST'
            # new_ob.data.name = 'test'

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        # Remove unused face maps for objects
        new_selection = context.selected_objects
        for ob in new_selection:
            if ob.type == 'MESH':
                ob.select_set(True)
                context.view_layer.objects.active = ob
                bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                if len(obj.face_maps) > 1:
                    faces = ob.data.polygons
                    for f in faces:                   
                        f.select = False
                    index = 0 
                    for _ in range(len(ob.face_maps)):
                        ob.face_maps.active_index = index
                        bpy.ops.object.face_map_select()
                        if ob.data.count_selected_items()[2] > 0:
                            bpy.ops.object.face_map_deselect()
                            index +=1
                        else:
                            bpy.ops.object.face_map_remove()
                        
                    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                    ob.select_set(False)

        for ob in new_selection:
            ob.select_set(True)

        # for each mesh set the name to match the AMF naming convention (except if only one facemap exists)
        for ob in new_selection:
            if ob.type == 'MESH':
                fm_name = ob.face_maps.active.name
                fm_split = fm_name.split()
                # Get the perm and region name, ignoring the LODs if H2
                if len(fm_split) == 3:
                    # h2 jms
                    permutation = fm_split[1]
                    region = fm_split[2]
                elif len(fm_split) == 2:
                    permutation = fm_split[0]
                    region = fm_split[1]
                else:
                    # not a valid facemap
                    permutation = 'default'
                    region = 'default'
                
                # Set the mesh name
                if not skip_rename:
                    ob.name = f'{prefix}{region}:{permutation}'
                # Set the mesh regions / permutations up
                ob.nwo.Region_Name = region
                ob.nwo.Permutation_Name = permutation
            
        report({'INFO'},f"Split {mesh_name} by face maps and updated regions & permutations")
        return 1
    else:
        report({'WARNING'},f"{mesh_name} has no face maps")
        return 0


