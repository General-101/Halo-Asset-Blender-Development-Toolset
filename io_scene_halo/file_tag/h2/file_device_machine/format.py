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
    search_cardinal_direction_lightmaps_on_failure = auto()
    unused = auto()
    not_a_pathfinding_obstacle = auto()
    extension_of_parent = auto()
    does_not_cause_collision_damage = auto()
    early_mover = auto()
    early_mover_localized_physics = auto()
    use_static_massive_lightmap_sample = auto()
    object_scales_attachments = auto()
    inherits_players_appearance = auto()
    dead_bipdes_cant_localize = auto()
    attach_to_clusters_by_dynamic_sphere = auto()
    effects_created_by_this_object_do_not_spawn_objects_in_multiplayer = auto()
    prophet_is_not_displayed_pegasus_builds = auto()

class LightmapShadowModeEnum(Enum):
    default = 0
    never = auto()
    always = auto()

class SweetenerSizeEnum(Enum):
    small = 0
    medium = auto()
    large = auto()

class DeviceFlags(Flag):
    position_loops = auto()
    unused = auto()
    allow_interpolation = auto()

class LightmapFlags(Flag):
    dont_use_in_lightmap = auto()
    dont_use_in_lightprobe = auto()

class MachineTypeEnum(Enum):
    door = 0
    platform = auto()
    gear = auto()

class MachineFlags(Flag):
    pathfinding_obstacle = auto()
    but_not_when_open = auto()
    elevator = auto()

class CollisionResponseEnum(Enum):
    pause_until_crushed = 0
    reverse_directions = auto()

class PathfindingPolicyEnum(Enum):
    discs = 0
    sectors = auto()
    cut_out = auto()
    none = auto()

class MachineAsset():
    def __init__(self):
        self.header = None
        self.machine_body_header = None
        self.machine_body = None
        self.ai_properties_header = None
        self.ai_properties = None
        self.functions_header = None
        self.functions = None
        self.attachments_header = None
        self.attachments = None
        self.widgets_header = None
        self.widgets = None
        self.old_functions_header = None
        self.old_functions = None
        self.change_colors_header = None
        self.change_colors = None
        self.predicted_resources_header = None
        self.predicted_resources = None

    class MachineBody:
        def __init__(self, object_flags=0, bounding_radius=0.0, bounding_offset=Vector(), acceleration_scale=0.0, lightmap_shadow_mode=0, sweetner_size=0, 
                     dynamic_light_sphere_radius=0.0, dynamic_light_sphere_offset=Vector(), default_model_variant="", default_model_variant_length=0, model=None, crate_object=None, 
                     modifier_shader=None, creation_effect=None, material_effects=None, ai_properties_tag_block=None, functions_tag_block=None, apply_collision_damage_scale=0.0, 
                     min_game_acc=0.0, max_game_acc=0.0, min_game_scale=0.0, max_game_scale=0.0, min_abs_acc=0.0, max_abs_acc=0.0, min_abs_scale=0.0, max_abs_scale=0.0, 
                     hud_text_message_index=0, attachments_tag_block=None, widgets_tag_block=None, old_functions_tag_block=None, change_colors_tag_block=None, 
                     predicted_resources_tag_block=None, device_flags=0, power_transition_time=0.0, power_acceleration_time=0.0, position_transition_time=0.0, 
                     position_acceleration_time=0.0, depowered_position_transition_time=0.0, depowered_position_acceleration_time=0.0, lightmap_flags=0, open_up=None, 
                     close_down=None, opened=None, closed=None, depowered=None, repowered=None, delay_time=0.0, delay_effect=None, automatic_activation_radius=0.0, machine_type=0, 
                     machine_flags=0, door_open_time=0.0, door_occlusion_time=(0.0, 0.0), collision_response=0, elevator_node=0, pathfinding_policy=0):
            self.object_flags = object_flags
            self.bounding_radius = bounding_radius
            self.bounding_offset = bounding_offset
            self.acceleration_scale = acceleration_scale
            self.lightmap_shadow_mode = lightmap_shadow_mode
            self.sweetner_size = sweetner_size
            self.dynamic_light_sphere_radius = dynamic_light_sphere_radius
            self.dynamic_light_sphere_offset = dynamic_light_sphere_offset
            self.default_model_variant = default_model_variant
            self.default_model_variant_length = default_model_variant_length
            self.model = model
            self.crate_object = crate_object
            self.modifier_shader = modifier_shader
            self.creation_effect = creation_effect
            self.material_effects = material_effects
            self.ai_properties_tag_block = ai_properties_tag_block
            self.functions_tag_block = functions_tag_block
            self.apply_collision_damage_scale = apply_collision_damage_scale
            self.min_game_acc = min_game_acc
            self.max_game_acc = max_game_acc
            self.min_game_scale = min_game_scale
            self.max_game_scale = max_game_scale
            self.min_abs_acc = min_abs_acc
            self.max_abs_acc = max_abs_acc
            self.min_abs_scale = min_abs_scale
            self.max_abs_scale = max_abs_scale
            self.hud_text_message_index = hud_text_message_index
            self.attachments_tag_block = attachments_tag_block
            self.widgets_tag_block = widgets_tag_block
            self.old_functions_tag_block = old_functions_tag_block
            self.change_colors_tag_block = change_colors_tag_block
            self.predicted_resources_tag_block = predicted_resources_tag_block
            self.device_flags = device_flags
            self.power_transition_time = power_transition_time
            self.power_acceleration_time = power_acceleration_time
            self.position_transition_time = position_transition_time
            self.position_acceleration_time = position_acceleration_time
            self.depowered_position_transition_time = depowered_position_transition_time
            self.depowered_position_acceleration_time = depowered_position_acceleration_time
            self.lightmap_flags = lightmap_flags
            self.open_up = open_up
            self.close_down = close_down
            self.opened = opened
            self.closed = closed
            self.depowered = depowered
            self.repowered = repowered
            self.delay_time = delay_time
            self.delay_effect = delay_effect
            self.automatic_activation_radius = automatic_activation_radius
            self.machine_type = machine_type
            self.machine_flags = machine_flags
            self.door_open_time = door_open_time
            self.door_occlusion_time = door_occlusion_time
            self.collision_response = collision_response
            self.elevator_node = elevator_node
            self.pathfinding_policy = pathfinding_policy
