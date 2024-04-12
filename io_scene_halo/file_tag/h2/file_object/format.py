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

class PathfindingPolicyEnum(Enum):
    pathfinding_cut_out = 0
    pathfinding_static = auto()
    pathfinding_dynamic = auto()
    pathfinding_none = auto()

class SceneryFlags(Flag):
    physically_stimulates = auto()

class LightmappingPolicyEnum(Enum):
    per_vertex = 0
    per_pixel = auto()
    dynamic = auto()

class AIFlags(Flag):
    destroyable_cover = auto()
    pathfinding_ignore_when_dead = auto()
    dynamic_cover = auto()

class AISizeEnum(Enum):
    default = 0
    tiny = auto()
    small = auto()
    medium = auto()
    large = auto()
    huge = auto()
    immobile = auto()

class LeapJumpSpeedEnum(Enum):
    none = 0
    down = auto()
    step = auto()
    crouch = auto()
    stand = auto()
    storey = auto()
    tower = auto()
    infinite = auto()

class FunctionFlags(Flag):
    invert = auto()
    mapping_does_not_controls_active = auto()
    always_active = auto()
    random_time_offset = auto()

class ChangeColorEnum(Enum):
    none = 0
    primary = auto()
    secondary = auto()
    tertiary = auto()
    quaternary = auto()

class ScaleFlags(Flag):
    blend_in_hsv = auto()
    more_colors = auto()

class ResourceTypeEnum(Enum):
    bitmap = 0
    sound = auto()
    render_model_geometry = auto()
    cluster_geometry = auto()
    cluster_instanced_geometry = auto()
    lightmap_geometry_object_buckets = auto()
    lightmap_geometry_instance_buckets = auto()
    lightmap_cluster_bitmaps = auto()
    lightmap_instance_bitmaps = auto()

class ObjectAsset():
    def __init__(self):
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

    class ObjectBody:
        def __init__(self, object_flags=0, bounding_radius=0.0, bounding_offset=Vector(), acceleration_scale=0.0, lightmap_shadow_mode=0, sweetner_size=0, 
                     dynamic_light_sphere_radius=0.0, dynamic_light_sphere_offset=Vector(), default_model_variant="", default_model_variant_length=0, model=None, crate_object=None, 
                     modifier_shader=None, creation_effect=None, material_effects=None, ai_properties_tag_block=None, functions_tag_block=None, apply_collision_damage_scale=0.0, 
                     min_game_acc=0.0, max_game_acc=0.0, min_game_scale=0.0, max_game_scale=0.0, min_abs_acc=0.0, max_abs_acc=0.0, min_abs_scale=0.0, max_abs_scale=0.0, 
                     hud_text_message_index=0, attachments_tag_block=None, widgets_tag_block=None, old_functions_tag_block=None, change_colors_tag_block=None, 
                     predicted_resources_tag_block=None):
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

    class AIProperties:
        def __init__(self, ai_flags=0, ai_type_name="", ai_type_name_length=0, ai_size=0, leap_jump_speed=0):
            self.ai_flags = ai_flags
            self.ai_type_name = ai_type_name
            self.ai_type_name_length = ai_type_name_length
            self.ai_size = ai_size
            self.leap_jump_speed = leap_jump_speed

    class Function:
        def __init__(self, flags=0, import_name="", import_name_length=0, export_name="", export_name_length=0, turn_off_with="", turn_off_with_length=0, min_value=0, 
                     function_property=None, scale_by="", scale_by_length=0):
            self.flags = flags
            self.import_name = import_name
            self.import_name_length = import_name_length
            self.export_name = export_name
            self.export_name_length = export_name_length
            self.turn_off_with = turn_off_with
            self.turn_off_with_length = turn_off_with_length
            self.min_value = min_value
            self.function_property = function_property
            self.scale_by = scale_by
            self.scale_by_length = scale_by_length

    class Attachment:
        def __init__(self, attachment_type=None, marker="", marker_length=0, change_color=0, primary_scale="", primary_scale_length=0, secondary_scale="", secondary_scale_length=0):
            self.attachment_type = attachment_type
            self.marker = marker
            self.marker_length = marker_length
            self.change_color = change_color
            self.primary_scale = primary_scale
            self.primary_scale_length = primary_scale_length
            self.secondary_scale = secondary_scale
            self.secondary_scale_length = secondary_scale_length

    class StringEntry:
        def __init__(self, name="", name_length=0):
            self.name = name
            self.name_length = name_length

    class ChangeColor:
        def __init__(self, initial_permutations_tag_block=None, initial_permutations_header=None, initial_permutations=None, functions_tag_block=None, functions_header=None, 
                     functions=None):
            self.initial_permutations_tag_block = initial_permutations_tag_block
            self.initial_permutations_header = initial_permutations_header
            self.initial_permutations = initial_permutations
            self.functions_tag_block = functions_tag_block
            self.functions_header = functions_header
            self.functions = functions

    class InitialPermutations:
        def __init__(self, weight=0.0, color_lower_bound=(0, 0, 0, 0), color_upper_bound=(0, 0, 0, 0), variant_name="", variant_name_length=0):
            self.weight = weight
            self.color_lower_bound = color_lower_bound
            self.color_upper_bound = color_upper_bound
            self.variant_name = variant_name
            self.variant_name_length = variant_name_length

    class Function:
        def __init__(self, scale_flags=0, color_lower_bound=(0, 0, 0, 0), color_upper_bound=(0, 0, 0, 0), darken_by="", darken_by_length=0, scale_by="", scale_by_length=0):
            self.scale_flags = scale_flags
            self.color_lower_bound = color_lower_bound
            self.color_upper_bound = color_upper_bound
            self.darken_by = darken_by
            self.darken_by_length = darken_by_length
            self.scale_by = scale_by
            self.scale_by_length = scale_by_length

    class PredictedResources:
        def __init__(self, predicted_resources_type=0, resource_index=0, tag_index=0):
            self.predicted_resources_type = predicted_resources_type
            self.resource_index = resource_index
            self.tag_index = tag_index
