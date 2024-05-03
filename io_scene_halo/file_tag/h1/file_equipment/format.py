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

class ItemFlags(Flag):
    always_maintains_z_up = auto()
    destroyed_by_explosions = auto()
    unaffected_by_gravity = auto()

class ItemFunctionEnum(Enum):
    none = 0

class PowerupTypeEnum(Enum):
    none = 0
    double_speed = auto()
    overshield = auto()
    active_camouflage = auto()
    full_spectrum_vision = auto()
    health = auto()
    grenade = auto()

class GrenadeTypeEnum(Enum):
    human_fragmentation = 0
    covenant_plasma = auto()
    grenade_type_2 = auto()
    grenade_type_3 = auto()

class EquipmentAsset():
    def __init__(self):
        self.header = None
        self.equipment_body = None
        self.attachments = None
        self.widgets = None
        self.functions = None
        self.change_colors = None
        self.predicted_resources = None

    class EquipmentBody:
        def __init__(self, object_flags=0, bounding_radius=0.0, bounding_offset=Vector(), origin_offset=Vector(), acceleration_scale=0.0, model=None, animation_graph=None,
                     collision_model=None, physics=None, modifier_shader=None, creation_effect=None, render_bounding_radius=0.0, object_a_in=0, object_b_in=0, object_c_in=0,
                     object_d_in=0, hud_text_message_index=0, forced_shader_permutation_index=0, attachments_tag_block=None, widgets_tag_block=None, functions_tag_block=None,
                     change_colors_tag_block=None, predicted_resources_tag_block=None, equipment_flags=0, message_index=0, sort_order=0, scale=0.0, hud_message_value_scale=0,
                     equipment_a_in=0, equipment_b_in=0, equipment_c_in=0, equipment_d_in=0, material_effects=None, collision_sound=None, detonation_delay=(0.0, 0.0),
                     detonating_effect=None, detonation_effect=None, powerup_type=0, grenade_type=0, powerup_time=0.0, pickup_sound=None):
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
            self.equipment_flags = equipment_flags
            self.message_index = message_index
            self.sort_order = sort_order
            self.scale = scale
            self.hud_message_value_scale = hud_message_value_scale
            self.equipment_a_in = equipment_a_in
            self.equipment_b_in = equipment_b_in
            self.equipment_c_in = equipment_c_in
            self.equipment_d_in = equipment_d_in
            self.material_effects = material_effects
            self.collision_sound = collision_sound
            self.detonation_delay = detonation_delay
            self.detonating_effect = detonating_effect
            self.detonation_effect = detonation_effect
            self.powerup_type = powerup_type
            self.grenade_type = grenade_type
            self.powerup_time = powerup_time
            self.pickup_sound = pickup_sound
