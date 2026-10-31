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
import struct
from ..global_functions import global_functions

def write_file(context, filepath, report):
    selected_objects = context.selected_objects
    if len(selected_objects) > 0:
        polygon_count = 0
        mesh_data = []
        for obj in selected_objects:
            if obj.type== 'MESH' and obj.data.vertex_colors:
                obj_data = obj.data
                polygon_count += len(obj_data.polygons)
                for face in obj_data.polygons:
                    for loop_index in face.loop_indices:
                        loop = obj_data.loops[loop_index]
                        vert = obj_data.vertices[loop.vertex_index]
                        pos = vert.co / 100
                        color = obj.data.vertex_colors.active.data[loop_index].color
                        mesh_data.append((pos, color))

        output_stream = open(filepath, 'wb')
        lmpf_string = "".join(reversed('LMPF'))
        output_stream.write(struct.pack('<4s', bytes(lmpf_string, 'utf-8')))
        output_stream.write(struct.pack('<I', polygon_count))
        for vertex in mesh_data:
            pos = vertex[0]
            color = vertex[1]
            output_stream.write(struct.pack('<fff', pos[0], pos[1], pos[2]))
            output_stream.write(struct.pack('<fff', color[0], color[1], color[2]))

        output_stream.close()
        report({'INFO'}, "Export completed successfully")
        return {'FINISHED'}

    else:
        raise global_functions.ParseError("You have no objects selected. Why are you even here then? Just to suffer?")

if __name__ == '__main__':
    bpy.ops.export_scene.qua()
