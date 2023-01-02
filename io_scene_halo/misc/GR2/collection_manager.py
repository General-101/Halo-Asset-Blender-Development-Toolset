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

def CreateCollections(context, ops, data, coll_type, coll_name):
    # iterates through the selected objects and applies the chosen collection type
    full_name = GetFullName(coll_type, coll_name)
    collection_index = GetCollIfExists(data, full_name)
    if collection_index == -1:
        ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name=full_name)
    else:
        for ob in context.selected_objects:
            for coll in ob.users_collection:
                coll.objects.unlink(ob)
            data.collections[collection_index].objects.link(ob)

    return {'FINISHED'}

def GetCollIfExists(data, full_name):
    collection_index = -1
    if len(data.collections) > 0:
        all_collections = data.collections
        for index, c in enumerate(all_collections):
            if c.name.replace(' ', '') == full_name.replace(' ', ''):
                collection_index = index
                break

    return collection_index

def GetFullName(coll_type, coll_name):
    prefix = ''
    match coll_type:
        case 'EXCLUDE':
            prefix = '+exclude:'
        case 'BSP':
            prefix = '+bsp:'
        case 'REGION':
            prefix = '+region:'
        case _:
            prefix = '+perm:'
    
    full_name_base = f'{prefix} {coll_name}'
    full_name = full_name_base

    # check if a collection by this name already exists, if so rename.
    duplicate = 1
    for c in bpy.data.collections:
        if max(c.name.rpartition('.')[0], c.name) == full_name:
            full_name = f'{full_name_base}.{duplicate:03d}'
            duplicate += 1

    return full_name
