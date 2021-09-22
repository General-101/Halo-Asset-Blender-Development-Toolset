# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2020 Steven Garcia
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

from math import degrees, radians

def interpolate_color(color_a, color_b, steps):
    color_list = []
    rdelta, gdelta, bdelta = (color_b[0]-color_a[0])/steps, (color_b[1]-color_a[1])/steps, (color_b[2]-color_a[2])/steps
    r1 = color_a[0]
    g1 = color_a[1]
    b1 = color_a[2]
    color_list.append(color_a)
    for step in range(steps):
        r1 += rdelta
        g1 += gdelta
        b1 += bdelta
        color_list.append((r1, g1, b1))
    color_list.append(color_b)
    return color_list

def generate_hemisphere(zenith_color, horizon_color, strength):
    color_list = interpolate_color(zenith_color, horizon_color, 6)
    object_list = []
    for light_row in range(26):
        for light in range(8):
            rot_tuple = (radians(90 + (12.5 * light)), 0, radians(18 * light_row))
            name = 'skylight_%s' % (light + (8 * light_row))
            light_data = bpy.data.lights.new(name, "SUN")
            object_mesh = bpy.data.objects.new(name, light_data)
            bpy.context.collection.objects.link(object_mesh)
            object_mesh.data.color = color_list[light]
            object_mesh.data.energy = strength
            object_mesh.rotation_euler = rot_tuple

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.halo_bulk.generate_hemisphere()
