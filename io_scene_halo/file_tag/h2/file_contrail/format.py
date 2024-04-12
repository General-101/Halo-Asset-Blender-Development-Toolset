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

from mathutils import Vector
from enum import Flag, Enum, auto

class ContrailAsset():
    def __init__(self):
        self.header = None
        self.contrail_body_header = None
        self.contrail_body = None
        self.point_states_header = None
        self.point_states = None

    class ContrailBody:
        def __init__(self, flags=0, scale_flags=0, point_generation_rate=0.0, point_velocity=(0.0, 0.0), point_velocity_cone_angle=(0.0, 0.0), inherited_velocity_fraction=0.0, 
                     render_type=0, texture_repeats_u=0.0, texture_repeats_v=0.0, texture_animation_u=0.0, texture_animation_v=0.0, animation_rate=0.0, render_bitmap=None, 
                     first_sequence_index=0, sequence_count=0, shader_flags=0, framebuffer_blend_function=0, framebuffer_fade_mode=0, map_flags=0, secondary_bitmap=None, anchor=0, 
                     secondary_flags=0, u_animation_function=0, u_animation_period=0.0, u_animation_phase=0.0, u_animation_scale=0.0, v_animation_function=0, v_animation_period=0.0, 
                     v_animation_phase=0.0, v_animation_scale=0.0, rotation_animation_function=0, rotation_animation_period=0.0, rotation_animation_phase=0.0, 
                     rotation_animation_scale=0.0, rotation_animation_center=(0.0, 0.0), zsprite_radius_scale=0.0, point_states_tag_block=None):
            self.flags = flags
            self.scale_flags = scale_flags
            self.point_generation_rate = point_generation_rate
            self.point_velocity = point_velocity
            self.point_velocity_cone_angle = point_velocity_cone_angle
            self.inherited_velocity_fraction = inherited_velocity_fraction
            self.render_type = render_type
            self.texture_repeats_u = texture_repeats_u
            self.texture_repeats_v = texture_repeats_v
            self.texture_animation_u = texture_animation_u
            self.texture_animation_v = texture_animation_v
            self.animation_rate = animation_rate
            self.render_bitmap = render_bitmap
            self.first_sequence_index = first_sequence_index
            self.sequence_count = sequence_count
            self.shader_flags = shader_flags
            self.framebuffer_blend_function = framebuffer_blend_function
            self.framebuffer_fade_mode = framebuffer_fade_mode
            self.map_flags = map_flags
            self.secondary_bitmap = secondary_bitmap
            self.anchor = anchor
            self.secondary_flags = secondary_flags
            self.u_animation_function = u_animation_function
            self.u_animation_period = u_animation_period
            self.u_animation_phase = u_animation_phase
            self.u_animation_scale = u_animation_scale
            self.v_animation_function = v_animation_function
            self.v_animation_period = v_animation_period
            self.v_animation_phase = v_animation_phase
            self.v_animation_scale = v_animation_scale
            self.rotation_animation_function = rotation_animation_function
            self.rotation_animation_period = rotation_animation_period
            self.rotation_animation_phase = rotation_animation_phase
            self.rotation_animation_scale = rotation_animation_scale
            self.rotation_animation_center = rotation_animation_center
            self.zsprite_radius_scale = zsprite_radius_scale
            self.point_states_tag_block = point_states_tag_block

    class PointState:
        def __init__(self, duration=(0.0, 0.0), transition_duration=(0.0, 0.0), physics=None, width=0.0, color_lower_bound=(0.0, 0.0, 0.0, 0.0), color_upper_bound=(0.0, 0.0, 0.0, 0.0), 
                     scale_flags=0):
            self.duration = duration
            self.transition_duration = transition_duration
            self.physics = physics
            self.width = width
            self.color_lower_bound = color_lower_bound
            self.color_upper_bound = color_upper_bound
            self.scale_flags = scale_flags
