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

def convert_facemaps(context):
    selected_objects = context.selected_objects

    for ob in selected_objects:
        if ob.type == "MESH":
            object_regions = [region.name for region in ob.region_list]
            region_attribute = ob.data.get_custom_attribute()
            for facemap_idx, facemap in enumerate(ob.face_maps):
                if not facemap.name in object_regions:
                    ob.region_add(facemap.name)
                    object_regions.append(facemap.name)

                if ob.data.face_maps.active and len(ob.face_maps) > 0:
                    for face_idx, face in enumerate(ob.data.polygons):
                        face_map_value = ob.data.face_maps.active.data[face_idx].value
                        if face_map_value == (facemap_idx):
                            region_attribute.data[face_idx].value = object_regions.index(facemap.name) + 1

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.halo_bulk.convert_facemaps()
