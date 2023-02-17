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
from os import path, remove, chdir, rmdir
import zipfile
import bpy
from os.path import join as path_join

from ...file_gr2.nwo_utils import (
    deselect_all_objects,
    get_active_object,
)
from .collection_manager import GetCollIfExists

def ArmatureCreate(context, armature_type, control_bones):
    import_file = ''
    if armature_type == 'PEDESTAL':
        import_file = 'pedestal'
    else:
        import_file = 'unit'

    if control_bones:
        import_file += '_control'

    append_blend(import_file)

    if control_bones:
        deselect_all_objects()
        coll_name = '+exclude: bone_shapes'
        collection_index = GetCollIfExists(bpy.data, coll_name)
        # Delete duplicate custom shapes
        for ob in context.view_layer.objects:
            if ob.name.rpartition('.')[0] in ('shape_pedestal', 'shape_aim_control'):
                ob.select_set(True)
        bpy.ops.object.delete()
        # Select custom shapes
        for ob in context.view_layer.objects:
            if ob.name in ('shape_pedestal', 'shape_aim_control'):
                ob.select_set(True)

        if collection_index == -1:
            bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name=coll_name)
            collection_index = 0
        else:
            bpy.data.collections[collection_index]

        # Disable the bone shapes collection
        for layer in context.view_layer.layer_collection.children:
            if layer.collection == bpy.data.collections[collection_index]:
                layer.exclude = True

    # deselect_all_objects()
    # pedestal = 'b_pedestal'
    # pitch = 'b_aim_pitch'
    # yaw = 'b_aim_yaw'
    # shape_pedestal = None
    # shape_pitch = None
    # shape_yaw = None
    # # first create a custom bone shapes collection if enabled
    # if use_custom_bone_shapes:
    #     coll_name = '+exclude: bone_shapes'
    #     collection_index = GetCollIfExists(bpy.data, coll_name)
    #     if collection_index == -1:
    #         if ShapesCreate():
    #             shape_pedestal = context.selected_objects[2]
    #             shape_pitch = context.selected_objects[0]
    #             shape_yaw = context.selected_objects[1]
    #             bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name=coll_name)
    #             collection_index = 0
    #     else:
    #         existing_coll = bpy.data.collections[collection_index]
    #         shape_pedestal = existing_coll.objects[2]
    #         shape_pitch = existing_coll.objects[0]
    #         shape_yaw = existing_coll.objects[1]

    # bpy.ops.object.armature_add(enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    # arm = get_active_object()
    # arm.data.edit_bones[0].name = pedestal
    # if armature_type == 'UNIT':
    #     bpy.ops.armature.bone_primitive_add(name=pitch)
    #     bpy.ops.armature.bone_primitive_add(name=yaw)
    #     arm.data.edit_bones[1].parent = arm.data.edit_bones[0]
    #     arm.data.edit_bones[2].parent = arm.data.edit_bones[0]


    # for b in arm.data.edit_bones:
    #     b.tail[1] = 1
    #     b.tail[2] = 0
            
    # bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    # if use_custom_bone_shapes:
    #     arm.pose.bones[0].custom_shape = shape_pedestal
    #     if armature_type == 'UNIT':
    #         arm.pose.bones[1].custom_shape = shape_pitch
    #         arm.pose.bones[2].custom_shape = shape_yaw
        
    #     for layer in context.view_layer.layer_collection.children:
    #         if layer.collection == bpy.data.collections[collection_index]:
    #             layer.exclude = True

    return {'FINISHED'}


def append_blend(blend_name):
    successful = True
    script_folder_path = path.dirname(path.dirname(path.dirname(__file__)))
    path_relative = f'rigs/{blend_name}.blend'
    filepath = path.join(script_folder_path, "resources", path_relative)
    path_resources_zip = path.join(script_folder_path, "resources.zip")

    if path.exists(filepath):
        print(f"Loading {filepath} from disk")
        unzip_blend(filepath, False)
    elif path.exists(path_resources_zip):
        print(f"Loading {path_relative} from {path_resources_zip}")
        unzip_blend(path_resources_zip, True, path_relative)
    else:
        print('path_not_found')
        successful = False
    return successful

def unzip_blend(file, is_zip, path_relative='', inner_path='', object_name=''):
    extracted_file = ''
    if is_zip:
        chdir(path.dirname(__file__))
        with zipfile.ZipFile(file, "r") as zip:
            extracted_file = zip.extract(path_relative)
            with bpy.data.libraries.load(extracted_file, link=False) as (data_from, data_to):
                data_to.objects = data_from.objects
                
            for ob in data_to.objects:
                if ob is not None:
                    bpy.context.collection.objects.link(ob)
            # bpy.ops.wm.append(filepath=path_join(extracted_file, inner_path, object_name))

        remove(extracted_file)
        rmdir(path.dirname(extracted_file))

    else:
        with bpy.data.libraries.load(file, link=False) as (data_from, data_to):
            data_to.objects = data_from.objects
            
        for ob in data_to.objects:
            if ob is not None:
                bpy.context.collection.objects.link(ob)

