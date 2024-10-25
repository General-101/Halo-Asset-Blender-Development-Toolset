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

from ....global_functions import tag_format, shader_processing
from ....file_tag.h2.file_shader.format import FunctionTypeEnum

def write_body(output_stream, TAG, PARTICLE):
    PARTICLE.body_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<I', PARTICLE.flags))
    output_stream.write(struct.pack('<h', PARTICLE.particle_billboard_style))
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<h', PARTICLE.first_sequence_index))
    output_stream.write(struct.pack('<h', PARTICLE.sequence_count))
    PARTICLE.shader_template.write(output_stream, False, True)
    PARTICLE.parameters_tag_block.write(output_stream, False)
    for particle_property in PARTICLE.properties:
        output_stream.write(struct.pack('<H', particle_property.input_type))
        output_stream.write(struct.pack('<H', particle_property.range_type))
        output_stream.write(struct.pack('<H', particle_property.output_modifier))
        output_stream.write(struct.pack('<H', particle_property.output_modifier_input))
        shader_processing.write_function_size(output_stream, particle_property)

    PARTICLE.collision_effect.write(output_stream, False, True)
    PARTICLE.death_effect.write(output_stream, False, True)
    PARTICLE.locations_tag_block.write(output_stream, False)
    PARTICLE.attached_particle_systems_tag_block.write(output_stream, False)
    PARTICLE.shader_postprocess_definitions_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<40x'))

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
                    part_element.object_type.write(output_stream, False)
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
                    particle_system_element.particle.write(output_stream, False)
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
                        output_stream.write(struct.pack('<%ss' % particle_name_length, TAG.string_to_bytes(particle_system_element.particle.name, False)))
                        if len(particle_system_element.emitters) > 0:
                            particle_system_element.emitters_header.write(output_stream, TAG, True)
                            for emitter_element in particle_system_element.emitters:
                                emitter_element.particle_physics.write(output_stream, False)
                                for particle_property in emitter_element.particle_properties:
                                    output_stream.write(struct.pack('<H', particle_property.input_type))
                                    output_stream.write(struct.pack('<H', particle_property.range_type))
                                    output_stream.write(struct.pack('<H', particle_property.output_modifier))
                                    output_stream.write(struct.pack('<H', particle_property.output_modifier_input))
                                    shader_processing.write_function_size(output_stream, particle_property)

                                output_stream.write(struct.pack('<I', emitter_element.emission_shape))
                                for emitter_property in emitter_element.emitter_properties:
                                    output_stream.write(struct.pack('<H', emitter_property.input_type))
                                    output_stream.write(struct.pack('<H', emitter_property.range_type))
                                    output_stream.write(struct.pack('<H', emitter_property.output_modifier))
                                    output_stream.write(struct.pack('<H', emitter_property.output_modifier_input))
                                    shader_processing.write_function_size(output_stream, emitter_property)

                                output_stream.write(struct.pack('<fff', *emitter_element.translational_offset))
                                output_stream.write(struct.pack('<ff', *emitter_element.relative_direction))
                                output_stream.write(struct.pack('<8x'))
                                for particle_property in emitter_element.particle_properties:
                                    particle_property.function_header.write(output_stream, TAG, True)
                                    shader_processing.write_function(output_stream, TAG, particle_property)

                                for emitter_property in emitter_element.emitter_properties:
                                    emitter_property.function_header.write(output_stream, TAG, True)
                                    shader_processing.write_function(output_stream, TAG, emitter_property)

def build_asset(output_stream, PARTICLE, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    PARTICLE.header.write(output_stream, False, True)
    write_body(output_stream, TAG, PARTICLE)
    shader_template_name_length = len(PARTICLE.shader_template.name)
    if shader_template_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % shader_template_name_length, TAG.string_to_bytes(PARTICLE.shader_template.name, False)))

    shader_processing.write_parameters(output_stream, TAG, PARTICLE.parameters, PARTICLE.parameters_header)
    for particle_property in PARTICLE.properties:
        particle_property.function_header.write(output_stream, TAG, True)
        shader_processing.write_function(output_stream, TAG, particle_property)

    collision_effect_name_length = len(PARTICLE.collision_effect.name)
    if collision_effect_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % collision_effect_name_length, TAG.string_to_bytes(PARTICLE.collision_effect.name, False)))

    death_effect_name_length = len(PARTICLE.death_effect.name)
    if death_effect_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % death_effect_name_length, TAG.string_to_bytes(PARTICLE.death_effect.name, False)))

    write_locations(output_stream, TAG, PARTICLE.locations, PARTICLE.locations_header)
