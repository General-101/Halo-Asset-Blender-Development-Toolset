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
import bmesh

from ..global_functions import mesh_processing, global_functions

def create_facemap(context, level_of_detail, permutation_string, region_string, set_facemap):
    active_object = context.view_layer.objects.active
    region_name = ""
    if active_object:
        #This doesn't matter for CE but for Halo 2/3 the region or permutation names can't have any whitespace.
        #Lets fix that here to make sure nothing goes wrong.
        if not level_of_detail == "NONE":
            if not global_functions.string_empty_check(level_of_detail):
                region_name += level_of_detail

        if not global_functions.string_empty_check(permutation_string):
            if not global_functions.string_empty_check(region_name):
                region_name += " "

            region_name += permutation_string.replace(' ', '_').replace('\t', '_')

        if not global_functions.string_empty_check(region_string):
            if not global_functions.string_empty_check(region_name):
                region_name += " "

            region_name += region_string.replace(' ', '_').replace('\t', '_')

        if not global_functions.string_empty_check(region_name):
            active_object.region_add(region_name)

        if set_facemap:
            region_list = []
            for region in active_object.region_list:
                region_list.append(region.name)

            region_index = region_list.index(region_name)
            region_attribute = active_object.data.get_custom_attribute()
            if context.mode == 'EDIT_MESH':
                bm = bmesh.from_edit_mesh(active_object.data)

                surface_layer = bm.faces.layers.int.get("Region Assignment")
                for face in bm.faces:
                    face[surface_layer] = region_index + 1

                bmesh.update_edit_mesh(active_object.data)

            else:
                for face in active_object.data.polygons:
                    region_attribute.data[face.index].value = region_index + 1

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.halo_bulk.perm_region_set()
