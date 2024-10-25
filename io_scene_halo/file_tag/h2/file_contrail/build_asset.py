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

def write_body(output_stream, TAG, CONTRAIL):
    CONTRAIL.body_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<h', CONTRAIL.flags))
    output_stream.write(struct.pack('<h', CONTRAIL.scale_flags))
    output_stream.write(struct.pack('<f', CONTRAIL.point_generation_rate))
    output_stream.write(struct.pack('<ff', *CONTRAIL.point_velocity))
    output_stream.write(struct.pack('<f', radians(CONTRAIL.point_velocity_cone_angle)))
    output_stream.write(struct.pack('<f', CONTRAIL.inherited_velocity_fraction))
    output_stream.write(struct.pack('<h', CONTRAIL.render_type))
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<f', CONTRAIL.texture_repeats_u))
    output_stream.write(struct.pack('<f', CONTRAIL.texture_repeats_v))
    output_stream.write(struct.pack('<f', CONTRAIL.texture_animation_u))
    output_stream.write(struct.pack('<f', CONTRAIL.texture_animation_v))
    output_stream.write(struct.pack('<f', CONTRAIL.animation_rate))
    CONTRAIL.render_bitmap.write(output_stream, False, True)
    output_stream.write(struct.pack('<h', CONTRAIL.first_sequence_index))
    output_stream.write(struct.pack('<h', CONTRAIL.sequence_count))
    output_stream.write(struct.pack('<40x'))
    output_stream.write(struct.pack('<h', CONTRAIL.shader_flags))
    output_stream.write(struct.pack('<h', CONTRAIL.framebuffer_blend_function))
    output_stream.write(struct.pack('<h', CONTRAIL.framebuffer_fade_mode))
    output_stream.write(struct.pack('<h', CONTRAIL.map_flags))
    output_stream.write(struct.pack('<28x'))
    CONTRAIL.secondary_bitmap.write(output_stream, False, True)
    output_stream.write(struct.pack('<h', CONTRAIL.anchor))
    output_stream.write(struct.pack('<h', CONTRAIL.secondary_flags))
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<h', CONTRAIL.u_animation_function))
    output_stream.write(struct.pack('<f', CONTRAIL.u_animation_period))
    output_stream.write(struct.pack('<f', CONTRAIL.u_animation_phase))
    output_stream.write(struct.pack('<f', CONTRAIL.u_animation_scale))
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<h', CONTRAIL.v_animation_function))
    output_stream.write(struct.pack('<f', CONTRAIL.v_animation_period))
    output_stream.write(struct.pack('<f', CONTRAIL.v_animation_phase))
    output_stream.write(struct.pack('<f', CONTRAIL.v_animation_scale))
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<h', CONTRAIL.rotation_animation_function))
    output_stream.write(struct.pack('<f', CONTRAIL.rotation_animation_period))
    output_stream.write(struct.pack('<f', CONTRAIL.rotation_animation_phase))
    output_stream.write(struct.pack('<f', CONTRAIL.rotation_animation_scale))
    output_stream.write(struct.pack('<ff', *CONTRAIL.rotation_animation_center))
    output_stream.write(struct.pack('<4x'))
    output_stream.write(struct.pack('<f', CONTRAIL.zsprite_radius_scale))
    output_stream.write(struct.pack('<20x'))
    CONTRAIL.point_states_tag_block.write(output_stream, False)

def write_point_states(output_stream, TAG, point_states, point_states_header):
    if len(point_states) > 0:
        point_states_header.write(output_stream, TAG, True)
        for point_state_element in point_states:
            output_stream.write(struct.pack('<ff', *point_state_element.duration))
            output_stream.write(struct.pack('<ff', *point_state_element.transition_duration))
            point_state_element.physics.write(output_stream, False, True)
            output_stream.write(struct.pack('<f', point_state_element.width))
            output_stream.write(struct.pack('<ffff', point_state_element.color_lower_bound[3], point_state_element.color_lower_bound[0], point_state_element.color_lower_bound[1], point_state_element.color_lower_bound[2]))
            output_stream.write(struct.pack('<ffff', point_state_element.color_upper_bound[3], point_state_element.color_upper_bound[0], point_state_element.color_upper_bound[1], point_state_element.color_upper_bound[2]))
            output_stream.write(struct.pack('<I', point_state_element.scale_flags))

        for point_state_element in point_states:
            physics_length = len(point_state_element.physics.name)
            if physics_length > 0:
                output_stream.write(struct.pack('<%ssx' % physics_length, TAG.string_to_bytes(point_state_element.physics.name, False)))

def build_asset(output_stream, CONTRAIL, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    CONTRAIL.header.write(output_stream, False, True)
    write_body(output_stream, TAG, CONTRAIL)

    render_bitmap_length = len(CONTRAIL.render_bitmap.name)
    if render_bitmap_length > 0:
        output_stream.write(struct.pack('<%ssx' % render_bitmap_length, TAG.string_to_bytes(CONTRAIL.render_bitmap.name, False)))

    secondary_bitmap_length = len(CONTRAIL.secondary_bitmap.name)
    if secondary_bitmap_length > 0:
        output_stream.write(struct.pack('<%ssx' % secondary_bitmap_length, TAG.string_to_bytes(CONTRAIL.secondary_bitmap.name, False)))

    write_point_states(output_stream, TAG, CONTRAIL.point_states, CONTRAIL.point_states_header)
