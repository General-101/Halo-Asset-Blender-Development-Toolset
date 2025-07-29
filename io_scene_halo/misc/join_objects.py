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

def join_objects(context):
    active_object = context.object
    selected_objects = context.selected_objects

    if active_object.type == "MESH" and context.mode == "OBJECT" and not len(selected_objects) == 0:
        active_object_regions = [region.name for region in active_object.data.region_list]
        for ob in selected_objects:
            if ob.type == "MESH" and not ob == active_object:
                region_attribute = ob.data.get_custom_attribute()
                for region_idx, region in enumerate(ob.data.region_list):
                    if not region.name in active_object_regions:
                        active_object.data.region_add(region.name)
                        active_object_regions.append(region.name)

                    for data in region_attribute.data:
                        if data.value == (region_idx + 1):
                            data.value = active_object_regions.index(region.name) + 1

        bpy.ops.object.join()

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.halo_bulk.join_objects()
