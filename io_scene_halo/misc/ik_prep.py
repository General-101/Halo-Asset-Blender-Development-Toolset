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

from ..global_functions import mesh_processing

def move_objects(context):
    selected_objects_list = context.selected_objects
    armature = None
    bone_names = []
    for object in selected_objects_list:
        if object.type == 'ARMATURE':
            armature = object
            for bone in armature.data.bones:
                bone_names.append(bone.name)

    if armature:
        for object in selected_objects_list:
            if object.name in bone_names:
                idx = bone_names.index(object.name)

                mesh_processing.select_object(context, armature)
                bpy.ops.object.mode_set(mode = 'POSE')
                bone = armature.data.bones[idx]
                armature.data.bones.active = bone
                bone.select = True
                bpy.ops.view3d.snap_cursor_to_active()
                bone.select = False
                armature.data.bones.active = None
                bpy.ops.object.mode_set(mode = 'OBJECT')
                mesh_processing.deselect_objects(context)

                mesh_processing.select_object(context, object)
                bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
                mesh_processing.deselect_objects(context)

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.ik_prep.move_objects()
