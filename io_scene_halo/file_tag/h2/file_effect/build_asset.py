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
from ....global_functions import tag_format, shader_processing
from ....file_tag.h2.file_shader.format import FunctionTypeEnum

def write_body(output_stream, TAG, EFFECT):
    EFFECT.effect_body_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<I', EFFECT.effect_body.flags))
    output_stream.write(struct.pack('<h', EFFECT.effect_body.loop_start_event))
    output_stream.write(struct.pack('<6x'))
    EFFECT.effect_body.locations_tag_block.write(output_stream, False)
    EFFECT.effect_body.events_tag_block.write(output_stream, False)
    EFFECT.effect_body.looping_sound.write(output_stream, False, True)
    output_stream.write(struct.pack('<h', EFFECT.effect_body.location))
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<f', EFFECT.effect_body.always_play_distance))
    output_stream.write(struct.pack('<f', EFFECT.effect_body.never_play_distance))

def write_locations(output_stream, TAG, locations, locations_header):
    if len(locations) > 0:
        locations_header.write(output_stream, TAG, True)
        for location_element in locations:
            output_stream.write(struct.pack('>I', len(location_element.name)))

        for location_element in locations:
            name_length = len(location_element.name)
            if name_length > 0:
                output_stream.write(struct.pack('<%ss' % name_length, TAG.string_to_bytes(location_element.name, False)))

def write_events(output_stream, TAG, events, events_header):
    if len(events) > 0:
        events_header.write(output_stream, TAG, True)
        for event_element in events:
            output_stream.write(struct.pack('<I', event_element.flags))
            output_stream.write(struct.pack('<f', event_element.skip_fraction))
            output_stream.write(struct.pack('<ff', event_element.delay_bounds[0], event_element.delay_bounds[1]))
            output_stream.write(struct.pack('<ff', event_element.duration_bounds[0], event_element.duration_bounds[1]))
            event_element.parts_tag_block.write(output_stream, False)
            event_element.beams_tag_block.write(output_stream, False)
            event_element.accelerations_tag_block.write(output_stream, False)
            event_element.particle_systems_tag_block.write(output_stream, False)

        for event_element in events:
            if len(event_element.parts) > 0:
                event_element.parts_header.write(output_stream, TAG, True)
                for part_element in event_element.parts:
                    output_stream.write(struct.pack('<H', part_element.create_in_environment))
                    output_stream.write(struct.pack('<H', part_element.create_in_mode))
                    output_stream.write(struct.pack('<h', part_element.location))
                    output_stream.write(struct.pack('<I', part_element.flags))
                    output_stream.write(struct.pack('<2x'))
                    part_element.object_type.write(output_stream, False, True)
                    output_stream.write(struct.pack('<ff', part_element.velocity_bounds[0], part_element.velocity_bounds[1]))
                    output_stream.write(struct.pack('<f', part_element.velocity_cone_angle))
                    output_stream.write(struct.pack('<ff', part_element.angular_velocity_bounds[0], part_element.angular_velocity_bounds[1]))
                    output_stream.write(struct.pack('<ff', part_element.radius_modifier_bounds[0], part_element.radius_modifier_bounds[1]))
                    output_stream.write(struct.pack('<I', part_element.a_scales_value))
                    output_stream.write(struct.pack('<I', part_element.b_scales_value))

                for part_element in event_element.parts:
                    object_name_length = len(part_element.object_type.name)
                    if object_name_length > 0:
                        output_stream.write(struct.pack('<%ssx' % object_name_length, TAG.string_to_bytes(part_element.object_type.name, False)))

            if len(event_element.beams) > 0:
                event_element.beams_header.write(output_stream, TAG, True)
                for beam_element in event_element.beams:
                    beam_element.shader.write(output_stream, False)
                    for beam_property in beam_element.properties:
                        shader_processing.write_function_size(output_stream, beam_property)
                    for beam_property in beam_element.properties:
                        beam_property.function_header.write(output_stream, TAG, True)
                        shader_processing.write_function(output_stream, TAG, beam_property)

            if len(event_element.accelerations) > 0:
                event_element.accelerations_header.write(output_stream, TAG, True)
                for acceleration_element in event_element.accelerations:
                    output_stream.write(struct.pack('<H', acceleration_element.create_in_environment))
                    output_stream.write(struct.pack('<H', acceleration_element.create_in_mode))
                    output_stream.write(struct.pack('<h', acceleration_element.location))
                    output_stream.write(struct.pack('<2x'))
                    output_stream.write(struct.pack('<f', acceleration_element.acceleration))
                    output_stream.write(struct.pack('<f', acceleration_element.inner_cone_angle))
                    output_stream.write(struct.pack('<f', acceleration_element.outer_cone_angle))

            if len(event_element.particle_systems) > 0:
                event_element.particle_systems_header.write(output_stream, TAG, True)
                for particle_system_element in event_element.particle_systems:
                    particle_system_element.particle.write(output_stream, False, True)
                    output_stream.write(struct.pack('<i', particle_system_element.location))
                    output_stream.write(struct.pack('<H', particle_system_element.coordinate_system))
                    output_stream.write(struct.pack('<H', particle_system_element.environment))
                    output_stream.write(struct.pack('<H', particle_system_element.disposition))
                    output_stream.write(struct.pack('<H', particle_system_element.camera_mode))
                    output_stream.write(struct.pack('<h', particle_system_element.sort_bias))
                    output_stream.write(struct.pack('<H', particle_system_element.flags))
                    output_stream.write(struct.pack('<f', particle_system_element.lod_in_distance))
                    output_stream.write(struct.pack('<f', particle_system_element.lod_feather_in_delta))
                    output_stream.write(struct.pack('<4x'))
                    output_stream.write(struct.pack('<f', particle_system_element.lod_out_distance))
                    output_stream.write(struct.pack('<f', particle_system_element.lod_feather_out_delta))
                    output_stream.write(struct.pack('<4x'))
                    particle_system_element.emitters_tag_block.write(output_stream, False)

                for particle_system_element in event_element.particle_systems:
                    particle_name_length = len(particle_system_element.particle.name)
                    if particle_name_length > 0:
                        output_stream.write(struct.pack('<%ssx' % particle_name_length, TAG.string_to_bytes(particle_system_element.particle.name, False)))

                    if len(particle_system_element.emitters) > 0:
                        particle_system_element.emitters_header.write(output_stream, TAG, True)
                        for emitter_element in particle_system_element.emitters:
                            emitter_element.particle_physics.write(output_stream, False, True)
                            for particle_property in emitter_element.particle_properties:
                                output_stream.write(struct.pack('<H', particle_property.input_type))
                                output_stream.write(struct.pack('<H', particle_property.range_type))
                                output_stream.write(struct.pack('<H', particle_property.output_modifier))
                                output_stream.write(struct.pack('<H', particle_property.output_modifier_input))
                                shader_processing.write_function_size(output_stream, particle_property)

                            output_stream.write(struct.pack('<I', emitter_element.emission_shape))
                            for emission_property in emitter_element.emission_properties:
                                output_stream.write(struct.pack('<H', emission_property.input_type))
                                output_stream.write(struct.pack('<H', emission_property.range_type))
                                output_stream.write(struct.pack('<H', emission_property.output_modifier))
                                output_stream.write(struct.pack('<H', emission_property.output_modifier_input))
                                shader_processing.write_function_size(output_stream, emission_property)

                            output_stream.write(struct.pack('<fff', *emitter_element.translational_offset))
                            output_stream.write(struct.pack('<ff', radians(emitter_element.relative_direction[0]), radians(emitter_element.relative_direction[1])))
                            output_stream.write(struct.pack('<8x'))

                        for emitter_element in particle_system_element.emitters:
                            particle_physics_length = len(emitter_element.particle_physics.name)
                            if particle_physics_length > 0:
                                output_stream.write(struct.pack('<%ssx' % particle_physics_length, TAG.string_to_bytes(emitter_element.particle_physics.name, False)))

                            for particle_property in emitter_element.particle_properties:
                                particle_property.function_header.write(output_stream, TAG, True)
                                shader_processing.write_function(output_stream, TAG, particle_property)

                            for emission_property in emitter_element.emission_properties:
                                emission_property.function_header.write(output_stream, TAG, True)
                                shader_processing.write_function(output_stream, TAG, emission_property)

def build_asset(output_stream, EFFECT, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    EFFECT.header.write(output_stream, False, True)
    write_body(output_stream, TAG, EFFECT)

    write_locations(output_stream, TAG, EFFECT.locations, EFFECT.locations_header)
    write_events(output_stream, TAG, EFFECT.events, EFFECT.events_header)

    looping_sound_name_length = len(EFFECT.effect_body.looping_sound.name)
    if looping_sound_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % looping_sound_name_length, TAG.string_to_bytes(EFFECT.effect_body.looping_sound.name, False)))