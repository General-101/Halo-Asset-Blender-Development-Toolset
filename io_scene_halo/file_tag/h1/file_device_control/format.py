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

class ObjectFlags(Flag):
    does_not_cast_shadow = auto()
    transparent_self_occlusion = auto()
    brighter_than_it_should_be = auto()
    not_a_pathfinding_obstacle = auto()
    extension_of_parent = auto()
    cast_shadow_by_default = auto()
    does_not_have_remastered_geometry = auto()

class ObjectFunctionEnum(Enum):
    none = 0
    body_vitality = auto()
    shield_vitality = auto()
    recent_body_damage = auto()
    recent_shield_damage = auto()
    random_constant = auto()
    umbrella_shield_vitality = auto()
    shield_stun = auto()
    recent_umbrella_shield_vitality = auto()
    umbrella_shield_stun = auto()
    region_00_damage = auto()
    region_01_damage = auto()
    region_02_damage = auto()
    region_03_damage = auto()
    region_04_damage = auto()
    region_05_damage = auto()
    region_06_damage = auto()
    region_07_damage = auto()
    alive = auto()
    compass = auto()

class DeviceFlags(Flag):
    position_loops = auto()
    position_not_interpolated = auto()

class DeviceFunctionEnum(Enum):
    none = 0
    power = auto()
    change_in_power = auto()
    position = auto()
    change_in_position = auto()
    locked = auto()
    delay = auto()

class ControlTypeEnum(Enum):
    toggle_switch = 0
    on_button = auto()
    off_button = auto()
    call_button = auto()

class ControlFlags(Flag):
    touched_by_player = auto()
    destroyed = auto()

class ControlAsset():
    def __init__(self):
        self.header = None
        self.control_body = None
        self.attachments = None
        self.widgets = None
        self.functions = None
        self.change_colors = None
        self.predicted_resources = None

    class ControlBody:
        def __init__(self, object_flags=0, bounding_radius=0.0, bounding_offset=Vector(), origin_offset=Vector(), acceleration_scale=0.0, model=None, animation_graph=None,
                     collision_model=None, physics=None, modifier_shader=None, creation_effect=None, render_bounding_radius=0.0, object_a_in=0, object_b_in=0, object_c_in=0,
                     object_d_in=0, hud_text_message_index=0, forced_shader_permutation_index=0, attachments_tag_block=None, widgets_tag_block=None, functions_tag_block=None,
                     change_colors_tag_block=None, predicted_resources_tag_block=None, device_flags=0, power_transition_time=0.0, power_acceleration_time=0.0,
                     position_transition_time=0.0, position_acceleration_time=0.0, depowered_position_transition_time=0.0, depowered_position_acceleration_time=0.0,
                     machine_a_in=0, machine_b_in=0, machine_c_in=0, machine_d_in=0, open_up=None, close_down=None, opened=None, closed=None, depowered=None, repowered=None,
                     delay_time=0.0, delay_effect=None, automatic_activation_radius=0.0, control_type=0, control_flags=0, call_value=0, on=None, off=None, delay=None):
            self.object_flags = object_flags
            self.bounding_radius = bounding_radius
            self.bounding_offset = bounding_offset
            self.origin_offset = origin_offset
            self.acceleration_scale = acceleration_scale
            self.model = model
            self.animation_graph = animation_graph
            self.collision_model = collision_model
            self.physics = physics
            self.modifier_shader = modifier_shader
            self.creation_effect = creation_effect
            self.render_bounding_radius = render_bounding_radius
            self.object_a_in = object_a_in
            self.object_b_in = object_b_in
            self.object_c_in = object_c_in
            self.object_d_in = object_d_in
            self.hud_text_message_index = hud_text_message_index
            self.forced_shader_permutation_index = forced_shader_permutation_index
            self.attachments_tag_block = attachments_tag_block
            self.widgets_tag_block = widgets_tag_block
            self.functions_tag_block = functions_tag_block
            self.change_colors_tag_block = change_colors_tag_block
            self.predicted_resources_tag_block = predicted_resources_tag_block
            self.device_flags = device_flags
            self.power_transition_time = power_transition_time
            self.power_acceleration_time = power_acceleration_time
            self.position_transition_time = position_transition_time
            self.position_acceleration_time = position_acceleration_time
            self.depowered_position_transition_time = depowered_position_transition_time
            self.depowered_position_acceleration_time = depowered_position_acceleration_time
            self.machine_a_in = machine_a_in
            self.machine_b_in = machine_b_in
            self.machine_c_in = machine_c_in
            self.machine_d_in = machine_d_in
            self.open_up = open_up
            self.close_down = close_down
            self.opened = opened
            self.closed = closed
            self.depowered = depowered
            self.repowered = repowered
            self.delay_time = delay_time
            self.delay_effect = delay_effect
            self.automatic_activation_radius = automatic_activation_radius
            self.control_type = control_type
            self.control_flags = control_flags
            self.call_value = call_value
            self.on = on
            self.off = off
            self.delay = delay
