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

def write_file(filepath, report):
    mesh_list = list(bpy.data.meshes)
    mesh_count = len(mesh_list)

    file = open(filepath, 'w')

    file.write('%s\n' % mesh_count)
    for mesh in mesh_list:
        vert_count = len(mesh.vertices)
        vert_index_list = []
        pos_list = []
        uv_list = []
        file.write(
            '"%s"' % mesh.name +
            '\n%s' % vert_count
            )

        for vertex in mesh.vertices:
            pos = vertex.co
            pos_list.append(pos)

        for loop in mesh.loops:
            if loop.vertex_index not in vert_index_list:
                vert_index_list.append(loop.vertex_index)
                uv = (0.0, 0.0)
                if mesh.uv_layers.active:
                    uv = mesh.uv_layers.active.data[mesh.loops[loop.index].index].uv
                uv_list.append((uv, loop.vertex_index))

        uv_list.sort(key=lambda x:x[1])
        for index in range(vert_count):
            uv_set = uv_list[index]
            uv = uv_set[0]
            pos = pos_list[index]
            file.write(
                '\n%f\t%f\t%f' % (pos[0], pos[1], pos[2]) +
                '\n%f\t%f' % (uv[0], 1.0 - uv[1])
                )

        file.write('\n')

    file.close()
    report({'INFO'}, "Export completed successfully")
    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.export_luv.export()
