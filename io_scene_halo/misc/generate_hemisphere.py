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

columm_rot = 13.84615384615385
column_elements = 26
row_rot = 11.25
row_elements = 8

def interpolate_color(color_a, color_b, steps):
    color_list = []
    rdelta, gdelta, bdelta = (color_b[0]-color_a[0])/steps, (color_b[1]-color_a[1])/steps, (color_b[2]-color_a[2])/steps
    r1, g1, b1 = color_a[0], color_a[1], color_a[2]
    color_list.append(color_a)
    for step in range(steps):
        r1 += rdelta
        g1 += gdelta
        b1 += bdelta
        color_list.append((r1, g1, b1))

    color_list.append(color_b)

    return color_list

def get_center_point(rotation, is_x_axis):
    light_spacing = row_rot
    if is_x_axis:
        light_spacing = columm_rot

    sun_id = round(rotation / light_spacing)
    print(light_spacing)
    print(rotation)
    print(is_x_axis)
    print(sun_id)
    return sun_id

def get_percentages(rotation, is_x_axis, color_loops):

    light_spacing = row_rot
    max_elements = row_elements
    if is_x_axis:
        light_spacing = columm_rot
        max_elements = column_elements

    percentage_list = []
    postitive_space_list = []
    negative_space_list = []
    sun_id = round(rotation / light_spacing)
    postive_space = max_elements - sun_id + 1

    if color_loops:
        halved_elements = round(max_elements / 2)
        for idx in range(halved_elements):
            percentage = 1 / halved_elements
            if idx > 0:
                percentage = percentage * (idx + 1)

            if idx == halved_elements - 1:
                percentage = 1.0

            negative_space_list.append(percentage)
            postitive_space_list.append(percentage)

        postitive_space_list.reverse()

        starting_point_list = []
        if sun_id > halved_elements:
            
            starting_point_list_reversed = []
            for idx in range(sun_id - halved_elements):
                starting_point_list_reversed.append(negative_space_list[idx])

            starting_point_list_reversed.reverse()
            starting_point_list = starting_point_list_reversed

            for idx in range(sun_id - halved_elements):
                starting_point_list.append(negative_space_list[idx])

            middle_point_list_reversed = []
            for idx in range(max_elements - sun_id):
                middle_point_list_reversed.append(postitive_space_list[idx])

            middle_point_list_reversed.reverse()
            starting_point_list = starting_point_list + middle_point_list_reversed

            for idx in range(max_elements - sun_id):
                starting_point_list.append(postitive_space_list[idx])

        else:
            for idx in range(sun_id):
                starting_point_list.append(negative_space_list[(idx + 1 ) * -1])

            starting_point_list.reverse()

            for idx in range(halved_elements):
                starting_point_list.append(postitive_space_list[idx])      

            for idx in range(max_elements - (halved_elements + sun_id)):
                starting_point_list.append(negative_space_list[idx])    

        percentage_list = starting_point_list

    else:
        for idx in range(sun_id):
            percentage = 1 / sun_id
            if idx > 0:
                percentage = percentage * (idx + 1)

            if idx == sun_id - 1:
                percentage = 1.0

            negative_space_list.append(percentage)

        for idx in range(postive_space):
            percentage = 1 / postive_space
            if idx > 0:
                percentage = percentage * (idx + 1)

            if not percentage == 1.0:
                postitive_space_list.append(percentage)

        postitive_space_list.reverse()
        percentage_list = negative_space_list + postitive_space_list

    return percentage_list

def darken_color(color, light_x_idx, light_y_idx, percentage_list_y, percentage_list_x):
    percentage_y = percentage_list_y[light_y_idx]
    percentage_x = percentage_list_x[light_x_idx]
    color_r, color_g, color_b = (color[0], color[1], color[2])
    color_r_y, color_g_y, color_b_y = (color_r * percentage_y), (color_g * percentage_y), (color_b * percentage_y)
    color_r_xy, color_g_xy, color_b_xy = ((color_r_y * percentage_x), (color_g_y * percentage_x), (color_b_y * percentage_x))
    return (color_r_xy, color_g_xy, color_b_xy)

def generate_hemisphere(zenith_color, horizon_color, strength, sun_yaw, sun_pitch):
    percentage_list_y = get_percentages(sun_pitch, False, False)
    percentage_list_x = get_percentages(sun_yaw, True, True)

    sun_row_id = get_center_point(sun_pitch, False)
    sun_column_id = get_center_point(sun_yaw, True)

    color_list = interpolate_color(zenith_color, horizon_color, 6)

    for light_column in range(column_elements):
        for light_row in range(row_elements):
            rot_tuple = (radians(90 + (row_rot * light_row)), 0, radians(columm_rot * light_column))
            name = 'skylight_%s' % (light_row + (8 * light_column))

            light_data = bpy.data.lights.new(name, "SUN")
            object_mesh = bpy.data.objects.new(name, light_data)
            bpy.context.collection.objects.link(object_mesh)

            object_mesh.rotation_euler = rot_tuple
            if light_column == sun_column_id and light_row == sun_row_id:
                print("%s is the sun point. Beat the shit out of him!!!" % name)
                object_mesh.data.energy = 0.0000471239
                object_mesh.data.color = (97070.6171875000, 82381.2265625000, 63777.9375000000)  

            else:
                object_mesh.data.energy = strength
                object_mesh.data.color = darken_color(color_list[light_row], light_column, light_row, percentage_list_y, percentage_list_x)

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.halo_bulk.generate_hemisphere()
