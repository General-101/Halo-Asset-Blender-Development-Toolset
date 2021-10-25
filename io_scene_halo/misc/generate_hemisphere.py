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
import math

from mathutils import Vector

columm_rot = 13.84615384615385
column_elements = 26
row_rot = 11.25
row_elements = 8

class SunSky:
    longitude_slices = 0
    lattitude_slices = 0
    dome_radius = 0.0
    horizontal_fov = 0.0
    vertical_fov = 0.0
    sky_type = 0
    cie_sky_number = 0
    hdr_map = ""
    haze_height = 0.0
    luminance_only = 0.0
    dome_intensity = 0.0
    override_zenith_color = 0
    zenith_color = Vector((0.0, 0.0, 0.0))
    override_horizon_color = 0
    horizon_color = Vector((0.0, 0.0, 0.0))
    sun_altittude = 0.0
    sun_heading = 0.0
    sun_intensity = 0.0
    sun_disc_size = 0.0
    windowing = 0.0
    override_sun_color = 0
    sun_color = Vector((0.0, 0.0, 0.0))
    air_cleaness = 0.0
    exposure = 0.0
    clamp_colors = 0

def interpolate_color(zenith_color, override_zenith_color, horizon_color, override_horizon_color, steps):
    color_list = []
    default_zenith = (0.894, 0.592, 0.349)
    default_horizon = (0.25, 0.62, 0.85)
    if not override_zenith_color:
        zenith_color = default_zenith

    if not override_horizon_color:
        horizon_color = default_horizon

    rdelta, gdelta, bdelta = (horizon_color[0]-zenith_color[0])/steps, (horizon_color[1]-zenith_color[1])/steps, (horizon_color[2]-zenith_color[2])/steps
    r1, g1, b1 = zenith_color[0], zenith_color[1], zenith_color[2]
    color_list.append(zenith_color)
    for step in range(steps):
        r1 += rdelta
        g1 += gdelta
        b1 += bdelta
        color_list.append((r1, g1, b1))

    color_list.append(horizon_color)

    return color_list

def get_center_point(rotation, is_x_axis):
    light_spacing = row_rot
    max_elements = row_elements
    if is_x_axis:
        light_spacing = columm_rot
        max_elements = column_elements

    sun_id = round(rotation / light_spacing)

    if sun_id >= max_elements:
        sun_bounds = max_elements - 1
        if is_x_axis:
            sun_bounds = 0

        sun_id =sun_bounds

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

def get_sun_color(sunsky):
    sun_color = sunsky.sun_color
    r, g, b = sun_color[0], sun_color[1], sun_color[2]

    sun_percentage = sunsky.sun_altittude / 90 * 1
    if sun_percentage < 0.05:
        sun_percentage = 0.05

    return (r * ((150000 * sunsky.sun_intensity) * sun_percentage), g * ((150000 * sunsky.sun_intensity) * sun_percentage), b * ((150000 * sunsky.sun_intensity) * sun_percentage))

def generate_hemisphere(context, report, longitude_slices, lattitude_slices, dome_radius, horizontal_fov, vertical_fov, sky_type, cie_sky_number, hdr_map, haze_height, luminance_only, dome_intensity, override_zenith_color, zenith_color, override_horizon_color, horizon_color, sun_altittude, sun_heading, sun_intensity, sun_disc_size, windowing, override_sun_color, sun_color, air_cleaness, exposure, clamp_colors):
    sunsky = SunSky
    sunsky.longitude_slices = longitude_slices
    sunsky.lattitude_slices = lattitude_slices
    sunsky.dome_radius = dome_radius
    sunsky.horizontal_fov = horizontal_fov
    sunsky.vertical_fov = vertical_fov
    sunsky.sky_type = sky_type
    sunsky.cie_sky_number = cie_sky_number
    sunsky.hdr_map = hdr_map
    sunsky.haze_height = haze_height
    sunsky.luminance_only = luminance_only
    sunsky.dome_intensity = dome_intensity
    sunsky.override_zenith_color = override_zenith_color
    sunsky.zenith_color = zenith_color
    sunsky.override_horizon_color = override_horizon_color
    sunsky.horizon_color = horizon_color
    sunsky.sun_altittude = sun_altittude
    sunsky.sun_heading = sun_heading
    sunsky.sun_intensity = sun_intensity
    sunsky.sun_disc_size = sun_disc_size
    sunsky.windowing = windowing
    sunsky.override_sun_color = override_sun_color
    sunsky.sun_color = sun_color
    sunsky.air_cleaness = air_cleaness
    sunsky.exposure = exposure
    sunsky.clamp_colors = clamp_colors

    k_sun_solid_angle= 0.00001 * 2.0 * math.pi
    k_dome_solid_angle= 0.01 * 2.0 * math.pi

    percentage_list_y = get_percentages(sunsky.sun_altittude, False, False)
    percentage_list_x = get_percentages(sunsky.sun_heading, True, True)

    sun_row_id = get_center_point(sunsky.sun_altittude, False)
    sun_column_id = get_center_point(sunsky.sun_heading, True)

    color_list = interpolate_color(sunsky.zenith_color, sunsky.override_zenith_color, sunsky.horizon_color, sunsky.override_horizon_color, (row_elements - 2))

    for light_column in range(column_elements):
        for light_row in range(row_elements):
            rot_tuple = (math.radians(90 + (row_rot * light_row)), 0, math.radians(columm_rot * light_column))
            name = 'skylight_%s' % (light_row + (8 * light_column))

            light_data = bpy.data.lights.get(name)
            if light_data is None:
                light_data = bpy.data.lights.new(name, "SUN")

            object_mesh = bpy.data.objects.get(name)
            if object_mesh is None:
                object_mesh = bpy.data.objects.new(name, light_data)
                context.collection.objects.link(object_mesh)

            object_mesh.rotation_euler = rot_tuple
            if light_column == sun_column_id and light_row == sun_row_id:
                report({'INFO'}, "%s is the sun point." % name)
                object_mesh.data.energy = k_sun_solid_angle * sunsky.windowing
                object_mesh.data.color = get_sun_color(sunsky)

            else:
                object_mesh.data.energy = k_dome_solid_angle
                object_mesh.data.color = darken_color(color_list[light_row], light_column, light_row, percentage_list_y, percentage_list_x)

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.halo_bulk.generate_hemisphere()
