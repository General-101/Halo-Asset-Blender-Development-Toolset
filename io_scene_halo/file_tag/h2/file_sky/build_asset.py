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

import struct

from math import radians
from ....global_functions import tag_format

def write_body(output_stream, TAG, SKY):
    SKY.sky_body_header.write(output_stream, TAG, True)
    SKY.sky_body.render_model.write(output_stream, False, True)
    SKY.sky_body.animation_graph.write(output_stream, False, True)
    output_stream.write(struct.pack('<I', SKY.sky_body.flags))
    output_stream.write(struct.pack('<f', SKY.sky_body.render_model_scale))
    output_stream.write(struct.pack('<f', SKY.sky_body.movement_scale))
    SKY.sky_body.cubemap_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<fff', SKY.sky_body.indoor_ambient_color[0], SKY.sky_body.indoor_ambient_color[1], SKY.sky_body.indoor_ambient_color[2]))
    output_stream.write(struct.pack('<4x'))
    output_stream.write(struct.pack('<fff', SKY.sky_body.outdoor_ambient_color[0], SKY.sky_body.outdoor_ambient_color[1], SKY.sky_body.outdoor_ambient_color[2]))
    output_stream.write(struct.pack('<4x'))
    output_stream.write(struct.pack('<f', SKY.sky_body.fog_spread_distance))
    SKY.sky_body.atmospheric_fog_tag_block.write(output_stream, False)
    SKY.sky_body.secondary_fog_tag_block.write(output_stream, False)
    SKY.sky_body.sky_fog_tag_block.write(output_stream, False)
    SKY.sky_body.patchy_fog_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', SKY.sky_body.amount))
    output_stream.write(struct.pack('<f', SKY.sky_body.threshold))
    output_stream.write(struct.pack('<f', SKY.sky_body.brightness))
    output_stream.write(struct.pack('<f', SKY.sky_body.gamma_power))
    SKY.sky_body.lights_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', radians(SKY.sky_body.global_sky_rotation)))
    SKY.sky_body.shader_functions_tag_block.write(output_stream, False)
    SKY.sky_body.animations_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<12x'))
    output_stream.write(struct.pack('<fff', SKY.sky_body.clear_color[0], SKY.sky_body.clear_color[1], SKY.sky_body.clear_color[2]))

def write_cubemaps(output_stream, TAG, cubemap, cubemap_header):
    if len(cubemap) > 0:
        cubemap_header.write(output_stream, TAG, True)
        for cubemap_element in cubemap:
            cubemap_element.cubemap_reference.write(output_stream, False, True)
            output_stream.write(struct.pack('<f', cubemap_element.power_scale))

        for cubemap_element in cubemap:
            cubemap_reference_length = len(cubemap_element.cubemap_reference.name)
            if cubemap_reference_length > 0:
                output_stream.write(struct.pack('<%ssx' % cubemap_reference_length, TAG.string_to_bytes(cubemap_element.cubemap_reference.name, False)))

def write_fog(output_stream, TAG, fog, fog_header):
    if len(fog) > 0:
        fog_header.write(output_stream, TAG, True)
        for fog_element in fog:
            output_stream.write(struct.pack('<fff', fog_element.color[0], fog_element.color[1], fog_element.color[2]))
            output_stream.write(struct.pack('<f', fog_element.maximum_density))
            output_stream.write(struct.pack('<f', fog_element.start_distance))
            output_stream.write(struct.pack('<f', fog_element.opaque_distance))

def write_sky_fog(output_stream, TAG, sky_fog, sky_fog_header):
    if len(sky_fog) > 0:
        sky_fog_header.write(output_stream, TAG, True)
        for sky_fog_element in sky_fog:
            output_stream.write(struct.pack('<fff', sky_fog_element.color[0], sky_fog_element.color[1], sky_fog_element.color[2]))
            output_stream.write(struct.pack('<f', sky_fog_element.maximum_density))

def write_patchy_fog(output_stream, TAG, patchy_fog, patchy_fog_header):
    if len(patchy_fog) > 0:
        patchy_fog_header.write(output_stream, TAG, True)
        for patchy_fog_element in patchy_fog:
            output_stream.write(struct.pack('<fff', patchy_fog_element.color[0], patchy_fog_element.color[1], patchy_fog_element.color[2]))
            output_stream.write(struct.pack('<12x'))
            output_stream.write(struct.pack('<ff', *patchy_fog_element.density))
            output_stream.write(struct.pack('<ff', *patchy_fog_element.distance))
            output_stream.write(struct.pack('<32x'))
            patchy_fog_element.patchy_fog.write(output_stream, False, True)

        for patchy_fog_element in patchy_fog:
            patchy_fog_length = len(patchy_fog_element.patchy_fog.name)
            if patchy_fog_length > 0:
                output_stream.write(struct.pack('<%ssx' % patchy_fog_length, TAG.string_to_bytes(patchy_fog_element.patchy_fog.name, False)))

def write_lights(output_stream, TAG, lights, lights_header):
    if len(lights) > 0:
        lights_header.write(output_stream, TAG, True)
        for light_element in lights:
            output_stream.write(struct.pack('<fff', *light_element.direction_vector))
            output_stream.write(struct.pack('<ff', radians(light_element.direction[0]), radians(light_element.direction[1])))
            light_element.lens_flare.write(output_stream, False, True)
            light_element.fog_tag_block.write(output_stream, False)
            light_element.fog_opposite_tag_block.write(output_stream, False)
            light_element.radiosity_tag_block.write(output_stream, False)

        for light_element in lights:
            lens_flare_length = len(light_element.lens_flare.name)
            if lens_flare_length > 0:
                output_stream.write(struct.pack('<%ssx' % lens_flare_length, TAG.string_to_bytes(light_element.lens_flare.name, False)))

            if len(light_element.fog) > 0:
                light_element.fog_header.write(output_stream, TAG, True)
                for fog_element in light_element.fog:
                    output_stream.write(struct.pack('<fff', fog_element.color[0], fog_element.color[1], fog_element.color[2]))
                    output_stream.write(struct.pack('<f', fog_element.maximum_density))
                    output_stream.write(struct.pack('<f', fog_element.start_distance))
                    output_stream.write(struct.pack('<f', fog_element.opaque_distance))
                    output_stream.write(struct.pack('<ff', radians(fog_element.opaque_distance[0]), radians(fog_element.opaque_distance[1])))
                    output_stream.write(struct.pack('<f', fog_element.atmospheric_fog_influence))
                    output_stream.write(struct.pack('<f', fog_element.secondary_fog_influence))
                    output_stream.write(struct.pack('<f', fog_element.sky_fog_influence))

            if len(light_element.fog_opposite) > 0:
                light_element.fog_opposite_header.write(output_stream, TAG, True)
                for fog_opposite_element in light_element.fog_opposite:
                    output_stream.write(struct.pack('<fff', fog_opposite_element.color[0], fog_opposite_element.color[1], fog_opposite_element.color[2]))
                    output_stream.write(struct.pack('<f', fog_opposite_element.maximum_density))
                    output_stream.write(struct.pack('<f', fog_opposite_element.start_distance))
                    output_stream.write(struct.pack('<f', fog_opposite_element.opaque_distance))
                    output_stream.write(struct.pack('<ff', radians(fog_opposite_element.opaque_distance[0]), radians(fog_opposite_element.opaque_distance[1])))
                    output_stream.write(struct.pack('<f', fog_opposite_element.atmospheric_fog_influence))
                    output_stream.write(struct.pack('<f', fog_opposite_element.secondary_fog_influence))
                    output_stream.write(struct.pack('<f', fog_opposite_element.sky_fog_influence))

            if len(light_element.radiosity) > 0:
                light_element.radiosity_header.write(output_stream, TAG, True)
                for radiosity_element in light_element.radiosity:
                    output_stream.write(struct.pack('<I', radiosity_element.flags))
                    output_stream.write(struct.pack('<fff', radiosity_element.color[0], radiosity_element.color[1], radiosity_element.color[2]))
                    output_stream.write(struct.pack('<f', radiosity_element.power))
                    output_stream.write(struct.pack('<f', radiosity_element.test_distance))
                    output_stream.write(struct.pack('<12x'))
                    output_stream.write(struct.pack('<f', radians(radiosity_element.diameter)))

def write_shader_functions(output_stream, TAG, shader_functions, shader_functions_header):
    if len(shader_functions) > 0:
        shader_functions_header.write(output_stream, TAG, True)
        for shader_function_element in shader_functions:
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('<31sx', TAG.string_to_bytes(shader_function_element, False)))           

def write_animations(output_stream, TAG, animations, animations_header):
    if len(animations) > 0:
        animations_header.write(output_stream, TAG, True)
        for animation_element in animations:
            output_stream.write(struct.pack('<h', animation_element.animation_index))
            output_stream.write(struct.pack('<2x'))
            output_stream.write(struct.pack('<f', animation_element.period))
            output_stream.write(struct.pack('<28x'))

def build_asset(output_stream, SKY, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    SKY.header.write(output_stream, False, True)
    write_body(output_stream, TAG, SKY)

    render_model_length = len(SKY.sky_body.render_model.name)
    if render_model_length > 0:
        output_stream.write(struct.pack('<%ssx' % render_model_length, TAG.string_to_bytes(SKY.sky_body.render_model.name, False)))

    animation_graph_length = len(SKY.sky_body.animation_graph.name)
    if animation_graph_length > 0:
        output_stream.write(struct.pack('<%ssx' % animation_graph_length, TAG.string_to_bytes(SKY.sky_body.animation_graph.name, False)))

    write_cubemaps(output_stream, TAG, SKY.cubemap, SKY.cubemap_header)
    write_fog(output_stream, TAG, SKY.atmospheric_fog, SKY.atmospheric_fog_header)
    write_fog(output_stream, TAG, SKY.secondary_fog, SKY.secondary_fog_header)
    write_sky_fog(output_stream, TAG, SKY.sky_fog, SKY.sky_fog_header)
    write_sky_fog(output_stream, TAG, SKY.sky_fog, SKY.sky_fog_header)
    write_patchy_fog(output_stream, TAG, SKY.patchy_fog, SKY.patchy_fog_header)
    write_lights(output_stream, TAG, SKY.lights, SKY.lights_header)
    write_shader_functions(output_stream, TAG, SKY.shader_functions, SKY.shader_functions_header)
    write_animations(output_stream, TAG, SKY.animations, SKY.animations_header)
